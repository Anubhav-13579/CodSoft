import customtkinter as ctk
from .theme import Theme
from .utils import get_movie_poster

class CompareWindow(ctk.CTkToplevel):
    def __init__(self, master, movie1, movie2):
        super().__init__(master)
        self.m1 = movie1
        self.m2 = movie2
        
        self.title("Compare Movies - CineMatch AI")
        self.geometry("900x700")
        self.configure(fg_color=Theme.BG_COLOR)
        
        self.update_idletasks()
        self.transient(master)
        
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=20, pady=20)
        self.scroll.grid_columnconfigure((0, 1, 2), weight=1)
        
        self._build_ui()
        
    def _build_ui(self):
        # Headers
        ctk.CTkLabel(self.scroll, text="Specification", font=Theme.H2_FONT, text_color=Theme.TEXT_MUTED).grid(row=0, column=0, pady=10, sticky="w")
        
        # M1 Header
        m1_f = ctk.CTkFrame(self.scroll, fg_color="transparent")
        m1_f.grid(row=0, column=1, pady=10)
        ctk.CTkLabel(m1_f, text="", image=get_movie_poster(self.m1["Title"], (100, 150))).pack()
        ctk.CTkLabel(m1_f, text=self.m1["Title"], font=Theme.H3_FONT, text_color=Theme.TEXT_COLOR, wraplength=250).pack()
        
        # M2 Header
        m2_f = ctk.CTkFrame(self.scroll, fg_color="transparent")
        m2_f.grid(row=0, column=2, pady=10)
        ctk.CTkLabel(m2_f, text="", image=get_movie_poster(self.m2["Title"], (100, 150))).pack()
        ctk.CTkLabel(m2_f, text=self.m2["Title"], font=Theme.H3_FONT, text_color=Theme.TEXT_COLOR, wraplength=250).pack()
        
        rows = [
            ("Director", self.m1["Director"], self.m2["Director"], None),
            ("Release Year", str(self.m1["Release Year"]), str(self.m2["Release Year"]), None),
            ("Runtime (min)", str(self.m1["Runtime"]), str(self.m2["Runtime"]), None),
            ("IMDb Rating", f"⭐ {self.m1['IMDb Rating']}", f"⭐ {self.m2['IMDb Rating']}", self._cmp_rating),
            ("Popularity", str(self.m1["Popularity"]), str(self.m2["Popularity"]), self._cmp_popularity),
            ("Vote Count", f"{self.m1['Vote Count']:,}", f"{self.m2['Vote Count']:,}", self._cmp_votes),
            ("Genres", self.m1["Genres"], self.m2["Genres"], None),
            ("Language", self.m1["Language"], self.m2["Language"], None)
        ]
        
        for i, (label, v1, v2, cmp_func) in enumerate(rows, start=1):
            ctk.CTkLabel(self.scroll, text=label, font=Theme.BODY_BOLD, text_color=Theme.TEXT_MUTED).grid(row=i, column=0, sticky="w", pady=15)
            
            c1, c2 = Theme.TEXT_COLOR, Theme.TEXT_COLOR
            if cmp_func:
                win = cmp_func()
                if win == 1: c1 = Theme.SUCCESS_COLOR
                elif win == 2: c2 = Theme.SUCCESS_COLOR
                
            ctk.CTkLabel(self.scroll, text=v1, font=Theme.BODY_FONT, text_color=c1, wraplength=250, justify="left").grid(row=i, column=1, sticky="w")
            ctk.CTkLabel(self.scroll, text=v2, font=Theme.BODY_FONT, text_color=c2, wraplength=250, justify="left").grid(row=i, column=2, sticky="w")
            
            if i < len(rows):
                ctk.CTkFrame(self.scroll, height=1, fg_color=Theme.CARD_BG).grid(row=i, column=0, columnspan=3, sticky="ew", pady=(15, 0))
                
        ctk.CTkButton(self.scroll, text="Close Compare", fg_color=Theme.ACCENT_COLOR, hover_color=Theme.ACCENT_HOVER, command=self.destroy).grid(row=len(rows)+1, column=1, pady=40)
        
    def _cmp_rating(self):
        if self.m1['IMDb Rating'] > self.m2['IMDb Rating']: return 1
        if self.m2['IMDb Rating'] > self.m1['IMDb Rating']: return 2
        return 0
        
    def _cmp_popularity(self):
        if self.m1['Popularity'] > self.m2['Popularity']: return 1
        if self.m2['Popularity'] > self.m1['Popularity']: return 2
        return 0
        
    def _cmp_votes(self):
        if self.m1['Vote Count'] > self.m2['Vote Count']: return 1
        if self.m2['Vote Count'] > self.m1['Vote Count']: return 2
        return 0
