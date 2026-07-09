import customtkinter as ctk
import time
import threading
from tkinter import messagebox

from files.theme import Theme
from files.recommender import CineMatchRecommender
from files.database import DatabaseManager
from files.compare import CompareWindow
from files.search import SearchEngine
from files.sidebar import Sidebar
from files.genres import GenresWindow
from files.app_statistics import StatisticsWindow
from files.cards import MovieCard
from files.details import MovieDetailsWindow
from files.loading import LoadingOverlay
class CineMatchApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("CineMatch AI")
        self.geometry("1280x800")
        self.configure(fg_color=Theme.BG_COLOR)
        ctk.set_appearance_mode("dark")
        
        # Initialize Core
        self.recommender = CineMatchRecommender()
        self.db = DatabaseManager()
        self.search_engine = SearchEngine(self.recommender)
        
        self.current_view = None
        self.compare_queue = []
        
        self._build_ui()
        
    def _build_ui(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        callbacks = {
            "home": self.show_home,
            "search": self.show_search,
            "trending": self.show_trending,
            "top_rated": self.show_top_rated,
            "favorites": self.show_favorites,
            "compare": self.show_compare,
            "genres": self.show_genres,
            "statistics": self.show_statistics
        }
        
        self.sidebar = Sidebar(self, callbacks)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.main_area = ctk.CTkFrame(self, fg_color="transparent")
        self.main_area.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_area.grid_rowconfigure(1, weight=1)
        self.main_area.grid_columnconfigure(0, weight=1)
        
        # Background Gradient
        self._create_gradient_bg()
        
        self.header_frame = ctk.CTkFrame(self.main_area, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        self.view_title = ctk.CTkLabel(self.header_frame, text="", font=Theme.H1_FONT, text_color=Theme.TEXT_COLOR)
        self.view_title.pack(side="left")
        
        self.scrollable_frame = ctk.CTkScrollableFrame(self.main_area, fg_color="transparent")
        self.scrollable_frame.grid(row=1, column=0, sticky="nsew")
        
        self.loading_overlay = LoadingOverlay(self.main_area)
        self.show_home()
        
    def _create_gradient_bg(self):
        from PIL import Image
        width, height = 2000, 1200
        base = Image.new('RGB', (width, height), (0, 0, 0))
        top = Image.new('RGB', (width, height), (4, 40, 20)) # Dark Green
        mask = Image.new('L', (width, height))
        
        # Create gradient mask
        for y in range(height):
            # Fade from 255 to 0
            val = int(255 * (1 - (y / height)))
            mask.paste(val, (0, y, width, y+1))
            
        bg = Image.composite(top, base, mask)
        self.bg_image = ctk.CTkImage(light_image=bg, dark_image=bg, size=(width, height))
        
        self.bg_label = ctk.CTkLabel(self.main_area, text="", image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Lower the bg label so it stays behind other widgets
        self.bg_label.lower()
        
    def _clear_main(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
            
    def _render_movie_grid(self, movies, empty_msg="No movies found."):
        self._clear_main()
        
        if not movies:
            ctk.CTkLabel(self.scrollable_frame, text=empty_msg, font=Theme.H3_FONT, text_color=Theme.TEXT_MUTED).grid(row=0, column=0, pady=50)
            return
            
        cols = 4
        for i, m in enumerate(movies):
            is_fav = self.db.is_favorite(m['Movie ID'])
            card = MovieCard(self.scrollable_frame, m, self.on_movie_click, self.on_favorite_toggle, is_fav)
            card.grid(row=i//cols, column=i%cols, padx=10, pady=15, sticky="nsew")
            
    def show_home(self):
        self.current_view = "home"
        self.view_title.configure(text="Recently Viewed & Trending")
        self._clear_main()
        
        # Recently Viewed
        recent_ids = self.db.get_recently_viewed()
        recent_movies = self.recommender.get_movies_by_ids(recent_ids)
        
        if recent_movies:
            ctk.CTkLabel(self.scrollable_frame, text="Recently Viewed", font=Theme.H2_FONT, text_color=Theme.TEXT_COLOR).pack(anchor="w", pady=(0, 10))
            recent_frame = ctk.CTkScrollableFrame(self.scrollable_frame, orientation="horizontal", height=380, fg_color="transparent")
            recent_frame.pack(fill="x", pady=(0, 20))
            for m in recent_movies:
                is_fav = self.db.is_favorite(m['Movie ID'])
                card = MovieCard(recent_frame, m, self.on_movie_click, self.on_favorite_toggle, is_fav)
                card.pack(side="left", padx=10)
                
        # Trending
        ctk.CTkLabel(self.scrollable_frame, text="Trending Now", font=Theme.H2_FONT, text_color=Theme.TEXT_COLOR).pack(anchor="w", pady=(0, 10))
        trend_frame = ctk.CTkScrollableFrame(self.scrollable_frame, orientation="horizontal", height=380, fg_color="transparent")
        trend_frame.pack(fill="x")
        
        for m in self.recommender.get_trending(10):
            is_fav = self.db.is_favorite(m['Movie ID'])
            card = MovieCard(trend_frame, m, self.on_movie_click, self.on_favorite_toggle, is_fav)
            card.pack(side="left", padx=10)
            
    def show_search(self):
        self.current_view = "search"
        self.view_title.configure(text="Search Movies")
        self._clear_main()
        
        search_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        search_frame.pack(fill="x", pady=20)
        
        self.search_entry = ctk.CTkEntry(search_frame, width=400, placeholder_text="Type movie title, cast, genre...")
        self.search_entry.pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(search_frame, text="Search", fg_color=Theme.ACCENT_COLOR, hover_color=Theme.ACCENT_HOVER,
                      command=self._execute_search).pack(side="left")
                      
        self.search_results_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        self.search_results_frame.pack(fill="both", expand=True)
        
    def _execute_search(self):
        query = self.search_entry.get()
        results = self.search_engine.search(query)
        
        for widget in self.search_results_frame.winfo_children():
            widget.destroy()
            
        if not results:
            ctk.CTkLabel(self.search_results_frame, text="No matches found.", font=Theme.BODY_FONT, text_color=Theme.TEXT_MUTED).pack(pady=20)
            return
            
        cols = 4
        for i, m in enumerate(results):
            is_fav = self.db.is_favorite(m['Movie ID'])
            card = MovieCard(self.search_results_frame, m, self.on_movie_click, self.on_favorite_toggle, is_fav)
            card.grid(row=i//cols, column=i%cols, padx=10, pady=15, sticky="nsew")

    def show_trending(self):
        self.current_view = "trending"
        self.view_title.configure(text="Trending Movies")
        self.scrollable_frame.grid_columnconfigure((0,1,2,3), weight=1)
        self._render_movie_grid(self.recommender.get_trending(20))
        
    def show_top_rated(self):
        self.current_view = "top_rated"
        self.view_title.configure(text="Top Rated on IMDb")
        self.scrollable_frame.grid_columnconfigure((0,1,2,3), weight=1)
        self._render_movie_grid(self.recommender.get_top_rated(20))
        
    def show_favorites(self):
        self.current_view = "favorites"
        self.view_title.configure(text="Your Favorites 💚")
        self.scrollable_frame.grid_columnconfigure((0,1,2,3), weight=1)
        fav_ids = self.db.get_favorites()
        fav_movies = self.recommender.get_movies_by_ids(fav_ids)
        self._render_movie_grid(fav_movies, "You have no favorites yet.")
        
    def show_compare(self):
        self.current_view = "compare"
        self.view_title.configure(text="Compare Movies")
        self._clear_main()
        
        if len(self.compare_queue) < 2:
            ctk.CTkLabel(self.scrollable_frame, text="Please add exactly two movies to compare from the Movie Details window.", font=Theme.H3_FONT, text_color=Theme.TEXT_MUTED).pack(pady=50)
            
            # Show queue
            if self.compare_queue:
                ctk.CTkLabel(self.scrollable_frame, text="Currently in queue:", font=Theme.H3_FONT, text_color=Theme.TEXT_COLOR).pack(pady=(20, 10))
                for m in self.compare_queue:
                    ctk.CTkLabel(self.scrollable_frame, text=f"- {m['Title']}", font=Theme.BODY_FONT, text_color=Theme.TEXT_MUTED).pack()
            return
            
        # Execute comparison
        CompareWindow(self, self.compare_queue[0], self.compare_queue[1])
        
        # Clear queue after comparing
        self.compare_queue = []
        ctk.CTkLabel(self.scrollable_frame, text="Comparison opened in a new window. Queue cleared.", font=Theme.H3_FONT, text_color=Theme.SUCCESS_COLOR).pack(pady=50)
        
    def show_genres(self):
        self.view_title.configure(text="Browse by Genre")
        GenresWindow(self, self.recommender, self.db, self.on_movie_click, self.on_favorite_toggle)
        
    def show_statistics(self):
        self.view_title.configure(text="Statistics")
        StatisticsWindow(self, self.recommender, self.db)

    # --- Actions ---
    
    def on_movie_click(self, movie_data):
        self.db.add_recently_viewed(movie_data['Movie ID'])
        is_fav = self.db.is_favorite(movie_data['Movie ID'])
        MovieDetailsWindow(self, movie_data, self.on_favorite_toggle, self.generate_recommendations, self.on_compare_queue_add, is_fav)
        
    def on_compare_queue_add(self, movie_data):
        if any(m['Movie ID'] == movie_data['Movie ID'] for m in self.compare_queue):
            messagebox.showwarning("Compare", "Movie is already in the comparison queue.")
            return
            
        if len(self.compare_queue) >= 2:
            self.compare_queue.pop(0) # Remove oldest
            
        self.compare_queue.append(movie_data)
        
        if len(self.compare_queue) == 2:
            messagebox.showinfo("Compare", "Ready to compare! Go to the 'Compare Movies' tab in the sidebar.")
        else:
            messagebox.showinfo("Compare", "Movie added to compare queue. Add one more movie to compare.")
            
    def on_favorite_toggle(self, movie_data, btn_widget):
        m_id = movie_data['Movie ID']
        if self.db.is_favorite(m_id):
            self.db.remove_favorite(m_id)
            btn_widget.configure(fg_color="transparent")
            if hasattr(btn_widget, 'configure'):
                try:
                    btn_widget.configure(text="🤍 Add to Favorites") # if called from details window
                except:
                    pass
        else:
            self.db.add_favorite(m_id)
            btn_widget.configure(fg_color=Theme.ACCENT_COLOR)
            if hasattr(btn_widget, 'configure'):
                try:
                    btn_widget.configure(text="❤️ Remove Favorite") # if called from details window
                except:
                    pass
                    
        # Refresh if on favorites page
        if self.current_view == "favorites":
            self.show_favorites()
            
    def generate_recommendations(self, movie_id):
        target_movie = self.recommender.get_movie_by_id(movie_id)
        if not target_movie: return
        
        self.view_title.configure(text=f"Because you liked '{target_movie['Title']}'...")
        self._clear_main()
        self.scrollable_frame.grid_columnconfigure((0,1,2,3), weight=1)
        
        self.loading_overlay.grid(row=1, column=0, sticky="nsew")
        self.loading_overlay.start()
        
        def _process():
            self.loading_overlay.update_text("Analyzing Movie...")
            time.sleep(0.5)
            self.loading_overlay.update_text("Finding Similar Movies...")
            time.sleep(0.5)
            self.loading_overlay.update_text("Computing Similarity...")
            time.sleep(0.5)
            
            recs = self.recommender.recommend(movie_id, top_n=10)
            
            self.after(0, self._render_recommendations_done, recs)
            
        threading.Thread(target=_process, daemon=True).start()
        
    def _render_recommendations_done(self, recs):
        self.loading_overlay.stop()
        self.loading_overlay.grid_forget()
        self._render_movie_grid(recs)

if __name__ == "__main__":
    app = CineMatchApp()
    app.mainloop()

    