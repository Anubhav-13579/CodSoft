import customtkinter as ctk
from .theme import Theme

class Sidebar(ctk.CTkFrame):
    def __init__(self, master, callbacks, **kwargs):
        super().__init__(master, fg_color=Theme.SIDEBAR_BG, width=220, corner_radius=0, **kwargs)
        self.callbacks = callbacks
        
        self.grid_rowconfigure(10, weight=1) # Spacer
        
        # Logo Area
        logo_lbl = ctk.CTkLabel(self, text="🎬🍿 CineMatch ✨", font=ctk.CTkFont(family=Theme.FONT_FAMILY, size=24, weight="bold"), text_color=Theme.ACCENT_COLOR)
        logo_lbl.grid(row=0, column=0, padx=25, pady=(35, 45), sticky="w")
        
        # Menu Items
        menu_items = [
            ("🏠 Home", "home"),
            ("🔎 Search", "search"),
            ("🔥 Trending", "trending"),
            ("⭐ Top Rated", "top_rated"),
            ("❤️ Favorites", "favorites"),
            ("📊 Compare Movies", "compare"),
            ("🎭 Browse Genres", "genres"),
            ("📈 Statistics", "statistics")
        ]
        
        self.buttons = {}
        
        for i, (text, key) in enumerate(menu_items, start=1):
            btn = ctk.CTkButton(self, text=text, font=ctk.CTkFont(family=Theme.FONT_FAMILY, size=15, weight="bold"), 
                                fg_color="transparent", text_color=Theme.TEXT_MUTED,
                                hover_color="#252525", anchor="w", corner_radius=10, height=42,
                                command=lambda k=key: self._on_nav_click(k))
            btn.grid(row=i, column=0, sticky="ew", padx=20, pady=5)
            self.buttons[key] = btn
            
        # Exit at bottom
        exit_btn = ctk.CTkButton(self, text="🚪 Exit ✌️", font=ctk.CTkFont(family=Theme.FONT_FAMILY, size=15, weight="bold"), 
                                 fg_color="transparent", text_color="#d65c5c",
                                 hover_color="#2b1a1a", anchor="w", corner_radius=10, height=42, command=self.master.destroy)
        exit_btn.grid(row=11, column=0, sticky="ew", padx=20, pady=(0, 30))
        
        self.active_key = None
        # self._on_nav_click("home")  # Initial view handled by app after UI is ready
            
    def _on_nav_click(self, key):
        if self.active_key:
            self.buttons[self.active_key].configure(fg_color="transparent", text_color=Theme.TEXT_MUTED)
            
        self.buttons[key].configure(fg_color=Theme.CARD_BG, text_color=Theme.ACCENT_COLOR)
        self.active_key = key
        
        if key in self.callbacks:
            self.callbacks[key]()
