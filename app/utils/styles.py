# UI Styling configurations

COLORS = {
    "primary": "#2D3E50",     # Dark blue
    "secondary": "#E74C3C",   # Red
    "background": "#F5F6FA",  # Light grey
    "surface": "#FFFFFF",     # White
    "text": "#2C3E50",        # Dark text
    "text_light": "#FFFFFF",  # Light text
    "success": "#27AE60",     # Green
    "error": "#C0392B"        # Dark red
}

FONTS = {
    "h1": ("Inter", 24, "bold"),
    "h2": ("Inter", 18, "bold"),
    "body": ("Inter", 12),
    "button": ("Inter", 12, "bold")
}

PAD = {
    "small": 5,
    "medium": 10,
    "large": 20
}

def apply_styles(root):
    # Optional styling adjustments to root tk window
    root.configure(bg=COLORS["background"])
