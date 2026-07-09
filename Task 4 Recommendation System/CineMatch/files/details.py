import customtkinter as ctk
from .theme import Theme
from .utils import get_movie_poster

class MovieDetailsWindow(ctk.CTkToplevel):
    def __init__(self, master, movie_data, on_favorite, on_recommend_similar, on_compare_queue_add, is_favorite=False):
        super().__init__(master)
        self.movie = movie_data
        
        self.title(f"{movie_data['Title']} - CineMatch AI")
        self.geometry("1200x1000")
        self.configure(fg_color=Theme.BG_COLOR)
        
        self.update_idletasks()
        self.transient(master)
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Poster
        poster_frame = ctk.CTkFrame(self, fg_color="transparent")
        poster_frame.grid(row=0, column=0, sticky="n", padx=30, pady=30)
        
        self.poster_lbl = ctk.CTkLabel(poster_frame, text="")
        self.poster_lbl.pack()
        
        def update_poster(new_img):
            try:
                self.poster_lbl.configure(image=new_img)
                self.poster_img = new_img # keep reference
            except Exception:
                pass
                
        self.poster_img = get_movie_poster(self.movie["Title"], size=(300, 450), callback=update_poster)
        self.poster_lbl.configure(image=self.poster_img)
        
        # Details
        details_scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        details_scroll.grid(row=0, column=1, sticky="nsew", padx=(0, 50), pady=50) #!!!!!!!!!!!!
        details_scroll.grid_columnconfigure(0, weight=1)
        
        title_lbl = ctk.CTkLabel(details_scroll, text=self.movie["Title"], font=ctk.CTkFont(family=Theme.FONT_FAMILY, size=36, weight="bold"), text_color=Theme.TEXT_COLOR, anchor="w")
        title_lbl.pack(anchor="w", pady=(0, 10))
        
        meta = f"⭐ {self.movie['IMDb Rating']} ({self.movie['Vote Count']} votes)   |   {self.movie['Release Year']}   |   {self.movie['Runtime']} min   |   {self.movie['Language']}"
        ctk.CTkLabel(details_scroll, text=meta, font=Theme.H3_FONT, text_color=Theme.RATING_COLOR, anchor="w").pack(anchor="w", pady=(0, 20))
        
        ctk.CTkLabel(details_scroll, text=self.movie["Overview"], font=Theme.BODY_FONT, text_color=Theme.TEXT_COLOR, justify="left", wraplength=400).pack(anchor="w", pady=(0, 20))
        
        specs = [
            ("Director", self.movie["Director"]),
            ("Cast", self.movie["Cast"]),
            ("Genres", self.movie["Genres"]),
            ("Keywords", self.movie["Keywords"]),
        ]
        
        for k, v in specs:
            f = ctk.CTkFrame(details_scroll, fg_color="transparent")
            f.pack(fill="x", pady=2)
            ctk.CTkLabel(f, text=f"{k}: ", font=Theme.BODY_BOLD, text_color=Theme.TEXT_MUTED).pack(side="left")
            ctk.CTkLabel(f, text=v, font=Theme.BODY_FONT, text_color=Theme.TEXT_COLOR, wraplength=350, justify="left").pack(side="left")
            
        # Recommendation Score/Reasons
        score = self.movie.get("recommendation_score", 0)
        if score > 0:
            score_frame = ctk.CTkFrame(details_scroll, fg_color=Theme.CARD_BG, corner_radius=Theme.CORNER_RADIUS)
            score_frame.pack(fill="x", pady=20, ipadx=15, ipady=15)
            
            ctk.CTkLabel(score_frame, text=f"{score}% Match", font=Theme.H2_FONT, text_color=Theme.SUCCESS_COLOR).pack(anchor="w")
            ctk.CTkLabel(score_frame, text="Why Recommended?", font=Theme.BODY_BOLD, text_color=Theme.TEXT_MUTED).pack(anchor="w", pady=(5, 5))
            
            for r in self.movie.get("reasons", []):
                ctk.CTkLabel(score_frame, text=f"✔ {r}", font=Theme.BODY_FONT, text_color=Theme.TEXT_COLOR).pack(anchor="w", padx=10)
        
        # Action Buttons
        btn_frame = ctk.CTkFrame(details_scroll, fg_color="transparent")
        btn_frame.pack(fill="x", pady=20)
        
        ctk.CTkButton(btn_frame, text="▶ Watch Trailer", font=Theme.BODY_BOLD, fg_color=Theme.ACCENT_COLOR, hover_color=Theme.ACCENT_HOVER).pack(side="left", padx=(0, 10))
        
        fav_text = "❤️ Remove Favorite" if is_favorite else "🤍 Add to Favorites"
        self.fav_btn = ctk.CTkButton(btn_frame, text=fav_text, font=Theme.BODY_BOLD, fg_color="transparent", border_width=1, border_color=Theme.TEXT_MUTED, hover_color=Theme.CARD_BG,
                                     command=lambda: on_favorite(self.movie, self.fav_btn))
        self.fav_btn.pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(btn_frame, text="Recommend Similar", font=Theme.BODY_BOLD, fg_color=Theme.CARD_BG, hover_color="#333333",
                      command=lambda: [self.destroy(), on_recommend_similar(self.movie['Movie ID'])]).pack(side="left", padx=(0, 10))
                      
        ctk.CTkButton(btn_frame, text="Compare", font=Theme.BODY_BOLD, fg_color="transparent", border_width=1, border_color=Theme.TEXT_MUTED, hover_color=Theme.CARD_BG,
                      command=lambda: on_compare_queue_add(self.movie)).pack(side="left")
