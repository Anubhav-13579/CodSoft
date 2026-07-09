import customtkinter as ctk
from .theme import Theme
from .cards import MovieCard

class GenresWindow(ctk.CTkToplevel):
    def __init__(self, master, recommender, db, on_movie_click, on_favorite_toggle):
        super().__init__(master)
        self.title("Browse by Genre - CineMatch AI")
        self.geometry("900x700")
        self.configure(fg_color=Theme.BG_COLOR)
        self.recommender = recommender
        self.db = db
        self.on_movie_click = on_movie_click
        self.on_favorite_toggle = on_favorite_toggle
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        header = ctk.CTkLabel(self, text="Select a Genre", font=Theme.H1_FONT, text_color=Theme.TEXT_COLOR)
        header.grid(row=0, column=0, pady=20)
        
        # Genre list on left
        left_frame = ctk.CTkFrame(self, fg_color="transparent")
        left_frame.grid(row=1, column=0, sticky="nsw", padx=20)
        left_frame.grid_rowconfigure(0, weight=1)
        left_frame.grid_columnconfigure(0, weight=1)
        
        self.genre_listbox = ctk.CTkScrollableFrame(left_frame, fg_color="transparent", width=200)
        self.genre_listbox.pack(fill="both", expand=True)
        
        for genre in self.recommender.get_all_genres():
            btn = ctk.CTkButton(self.genre_listbox, text=genre, font=Theme.BODY_FONT,
                                 fg_color="transparent", text_color=Theme.TEXT_MUTED,
                                 hover_color=Theme.CARD_BG, anchor="w",
                                 command=lambda g=genre: self._load_genre_movies(g))
            btn.pack(fill="x", pady=2, padx=5)
        
        # Movies display on right
        self.movies_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.movies_frame.grid(row=1, column=0, sticky="nsew", padx=(250, 20), pady=10)
        self.movies_frame.grid_columnconfigure((0,1,2,3), weight=1)
        
    def _load_genre_movies(self, genre):
        movies = self.recommender.get_by_genre(genre, top_n=100)
        for w in self.movies_frame.winfo_children():
            w.destroy()
        cols = 4
        for i, m in enumerate(movies):
            is_fav = False
            card = MovieCard(self.movies_frame, m, self.on_movie_click, self.on_favorite_toggle, is_fav)
            card.grid(row=i//cols, column=i%cols, padx=10, pady=15, sticky="nsew")
