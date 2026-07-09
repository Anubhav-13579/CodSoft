import customtkinter as ctk
from .theme import Theme

class LoadingOverlay(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=Theme.BG_COLOR, **kwargs)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)
        
        # Netflix style loading (red spinner)
        self.spinner = ctk.CTkProgressBar(self, mode="indeterminate", width=300, height=8, fg_color=Theme.CARD_BG, progress_color=Theme.ACCENT_COLOR)
        self.spinner.grid(row=1, column=0, pady=(0, 20))
        
        self.status_label = ctk.CTkLabel(self, text="Analyzing Movie...", font=Theme.H2_FONT, text_color=Theme.TEXT_COLOR)
        self.status_label.grid(row=2, column=0, pady=10)
        
    def start(self):
        self.spinner.start()
        
    def stop(self):
        self.spinner.stop()
        
    def update_text(self, text):
        self.status_label.configure(text=text)
