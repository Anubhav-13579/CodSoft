import customtkinter as ctk
from .theme import Theme
from .utils import get_movie_poster

class MovieCard(ctk.CTkFrame):
    def __init__(self, master, movie_data, on_click, on_favorite, is_favorite=False, **kwargs):
        super().__init__(master, fg_color=Theme.CARD_BG, corner_radius=Theme.CORNER_RADIUS, **kwargs)
        self.movie = movie_data
        
        # We need to make the whole card clickable. In CustomTkinter, it's easiest to make the background a button
        # or bind clicks to inner widgets. We will use inner widgets.
        
        self.grid_columnconfigure(0, weight=1)
        
        # 1. Poster
        def update_poster(new_img):
            try:
                self.poster_lbl.configure(image=new_img)
                self.poster_img = new_img # keep reference
            except Exception:
                pass
                
        self.poster_img = get_movie_poster(movie_data["Title"], size=(160, 240), callback=update_poster)
        self.poster_lbl = ctk.CTkLabel(self, text="", image=self.poster_img, cursor="hand2")
        self.poster_lbl.grid(row=0, column=0, pady=(0, 10))
        self.poster_lbl.bind("<Button-1>", lambda e: on_click(movie_data))
        
        # Match Score (Absolute Top Right of poster via place or simple grid)
        score = movie_data.get("recommendation_score", 0)
        if score > 0:
            color = Theme.SUCCESS_COLOR if score >= 75 else (Theme.RATING_COLOR if score >= 50 else Theme.TEXT_MUTED)
            score_lbl = ctk.CTkLabel(self, text=f"{score}% Match", font=Theme.BODY_BOLD, text_color=color)
            score_lbl.grid(row=1, column=0, sticky="w", padx=10)
            
        # 2. Title
        self.title_lbl = ctk.CTkLabel(self, text=movie_data["Title"], font=Theme.H3_FONT, text_color=Theme.TEXT_COLOR, anchor="w")
        self.title_lbl.grid(row=2, column=0, sticky="ew", padx=10)
        
        # 3. IMDb Rating & Year & Runtime
        meta_text = f"⭐ {movie_data['IMDb Rating']}   {movie_data['Release Year']}   {movie_data['Runtime']}m"
        self.meta_lbl = ctk.CTkLabel(self, text=meta_text, font=Theme.SMALL_FONT, text_color=Theme.TEXT_MUTED, anchor="w")
        self.meta_lbl.grid(row=3, column=0, sticky="ew", padx=10)
        
        # 4. Action Buttons (View Details, Favorite)
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=4, column=0, sticky="ew", padx=10, pady=(10, 10))
        btn_frame.grid_columnconfigure(0, weight=1)
        
        self.details_btn = ctk.CTkButton(btn_frame, text="View Details", font=Theme.BODY_FONT, fg_color=Theme.ACCENT_COLOR,
                                         hover_color=Theme.ACCENT_HOVER, corner_radius=Theme.BUTTON_RADIUS, height=28,
                                         text_color="black",
                                         command=lambda: on_click(movie_data))
        self.details_btn.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        
        fav_color = Theme.ACCENT_COLOR if is_favorite else "transparent"
        self.fav_btn = ctk.CTkButton(btn_frame, text="♥", font=Theme.BODY_FONT, width=30, fg_color=fav_color,
                                     border_width=1, border_color=Theme.TEXT_MUTED, hover_color=Theme.ACCENT_HOVER, corner_radius=Theme.BUTTON_RADIUS, height=28,
                                     text_color="black",
                                     command=lambda: on_favorite(movie_data, self.fav_btn))
        self.fav_btn.grid(row=0, column=1)
