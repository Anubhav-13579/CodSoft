class Theme:
    # Black & Neon Green Aesthetic
    BG_COLOR = "#000000"           # Pure Black Background
    SIDEBAR_BG = "#030a05"         # Very Deep Green (gradient effect)
    CARD_BG = "#0a1a10"            # Dark Green Cards
    ACCENT_COLOR = "#00FF66"       # Neon Green Accent
    ACCENT_HOVER = "#00E55C"       # Slightly darker Neon Green for hover
    TEXT_COLOR = "#E6FFED"         # Bright green-tinted white
    TEXT_MUTED = "#6F9C7D"         # Muted green for secondary text
    RATING_COLOR = "#FFD700"       # Gold for IMDb ratings (kept for contrast)
    SUCCESS_COLOR = "#00FF66"      # Neon Green
    
    # Fonts
    FONT_FAMILY = "Inter" # Default to system sans-serif if Inter is missing
    H1_FONT = (FONT_FAMILY, 28, "bold")
    H2_FONT = (FONT_FAMILY, 22, "bold")
    H3_FONT = (FONT_FAMILY, 18, "bold")
    BODY_FONT = (FONT_FAMILY, 14)
    BODY_BOLD = (FONT_FAMILY, 14, "bold")
    SMALL_FONT = (FONT_FAMILY, 12)
    
    # Corners
    CORNER_RADIUS = 6
    BUTTON_RADIUS = 4
