from kivy.metrics import dp, sp
from kivy.core.window import Window

# Font sizes as ratios of window height
FONT_SIZE_RATIO_SMALL = 0.02  # 2.5% of window height
FONT_SIZE_RATIO_MEDIUM = 0.029  # 3.5% of window height
FONT_SIZE_RATIO_BIG = 0.035    # 4.5% of window height

# Color palette (using RGBA format)
PRIMARY_COLOR = (0.15, 0.2, 0.3, 1)    # Deep Navy Blue
SECONDARY_COLOR = (0.2, 0.2, 0.25, 1)  # Dark Slate
ACCENT_COLOR = (0.3, 0.4, 0.45, 1)     # Muted Teal
HIGHLIGHT_COLOR = (0.25, 0.25, 0.3, 1)  # Soft Dark Gray

IDIOT_NAMES = [
    "Dumpfbacke",
    "Lausbube",
    "Schluckspecht",
    "Taugenichts",
    "Dummkopf",
    "Schlafmütze",
    "Pfosten",
    "Blödmann",
    "Dödel",
    "Trottel",
    "Schluri",
    "Schlunz",
    "Schlappohr",
]

def get_font_size(ratio):
    """Calculate font size based on window height and given ratio"""
    return dp(Window.height * ratio)