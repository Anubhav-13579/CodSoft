import customtkinter as ctk
from .theme import Theme

class StatisticsWindow(ctk.CTkToplevel):
    def __init__(self, master, recommender, db):
        super().__init__(master)
        self.title("CineMatch Statistics")
        self.geometry("600x500")
        self.configure(fg_color=Theme.BG_COLOR)
        self.recommender = recommender
        self.db = db
        
        self.grid_columnconfigure(0, weight=1)
        
        header = ctk.CTkLabel(self, text="Statistics Dashboard", font=Theme.H1_FONT, text_color=Theme.TEXT_COLOR)
        header.grid(row=0, column=0, pady=20)
        
        # Compute stats
        total_movies = len(self.recommender.df)
        avg_rating = self.recommender.df['IMDb Rating'].mean()
        top_genre_series = self.recommender.df['Genres'].str.split(',').explode().str.strip().value_counts()
        top_genre = top_genre_series.idxmax() if not top_genre_series.empty else "N/A"
        most_popular = self.recommender.df.loc[self.recommender.df['Popularity'].idxmax()]
        highest_rated = self.recommender.df.loc[self.recommender.df['IMDb Rating'].idxmax()]
        favorites_count = len(self.db.get_favorites())
        
        # Helper to create rows
        def add_row(label, value, row):
            ctk.CTkLabel(self, text=label, font=Theme.BODY_BOLD, text_color=Theme.TEXT_MUTED).grid(row=row, column=0, sticky="w", padx=30, pady=5)
            ctk.CTkLabel(self, text=value, font=Theme.BODY_FONT, text_color=Theme.TEXT_COLOR).grid(row=row, column=0, sticky="e", padx=30, pady=5)
        
        add_row("Total Movies", str(total_movies), 1)
        add_row("Average IMDb Rating", f"{avg_rating:.2f}", 2)
        add_row("Top Genre", top_genre, 3)
        add_row("Most Popular Movie", most_popular['Title'], 4)
        add_row("Highest Rated Movie", highest_rated['Title'], 5)
        add_row("Favorites Count", str(favorites_count), 6)
        
        # Close button
        ctk.CTkButton(self, text="Close", fg_color=Theme.ACCENT_COLOR, hover_color=Theme.ACCENT_HOVER,
                      command=self.destroy).grid(row=7, column=0, pady=30)
