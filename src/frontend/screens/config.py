from kivy.metrics import dp
from kivy.core.window import Window
from kivy.event import EventDispatcher
from kivy.properties import NumericProperty

# Font sizes as ratios of window height
FONT_SIZE_RATIO_SMALL = 0.025  # 2.5% of window height
FONT_SIZE_RATIO_MEDIUM = 0.035  # 3.5% of window height
FONT_SIZE_RATIO_BIG = 0.045    # 4.5% of window height

class FontConfig(EventDispatcher):
    """Reactive font configuration that updates when window size changes"""
    
    # Font size properties that automatically update
    font_size_small = NumericProperty(0)
    font_size_medium = NumericProperty(0)
    font_size_big = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Bind to window size changes
        Window.bind(size=self._update_font_sizes)
        # Initialize font sizes
        self._update_font_sizes()
    
    def _update_font_sizes(self, *args):
        """Update all font sizes based on current window height"""
        self.font_size_small = dp(Window.height * FONT_SIZE_RATIO_SMALL)
        self.font_size_medium = dp(Window.height * FONT_SIZE_RATIO_MEDIUM)
        self.font_size_big = dp(Window.height * FONT_SIZE_RATIO_BIG)

# Global font config instance
font_config = FontConfig()


# Modern Color Palette
# Base Colors
BACKGROUND_COLOR = "#F8F9FA"  # Soft Off-White
SURFACE_COLOR = "#FFFFFF"     # Pure White
PRIMARY_COLOR = "#6366F1"     # Modern Indigo
SECONDARY_COLOR = "#8B5CF6"   # Vibrant Purple

# Semantic Colors
SUCCESS_COLOR = "#10B981"     # Emerald Green (for winner)
WARNING_COLOR = "#F59E0B"     # Amber (for round wind)
TEXT_PRIMARY = "#1F2937"      # Dark Gray (main text)
TEXT_SECONDARY = "#6B7280"    # Medium Gray (secondary text)
BORDER_COLOR = "#E5E7EB"      # Light Gray (subtle borders)

# Convert hex to kivy color (RGBA float tuple)
def hex_to_rgba(hex_color, alpha=1):
    """Convert hex color to RGBA tuple"""
    hex_color = hex_color.lstrip('#')
    return (
        int(hex_color[0:2], 16) / 255,
        int(hex_color[2:4], 16) / 255,
        int(hex_color[4:6], 16) / 255,
        alpha
    )

# Kivy-ready color tuples
K_BACKGROUND = hex_to_rgba(BACKGROUND_COLOR)
K_SURFACE = hex_to_rgba(SURFACE_COLOR)
K_PRIMARY = hex_to_rgba(PRIMARY_COLOR)
K_SECONDARY = hex_to_rgba(SECONDARY_COLOR)
K_SUCCESS = hex_to_rgba(SUCCESS_COLOR)
K_WARNING = hex_to_rgba(WARNING_COLOR)
K_TEXT_PRIMARY = hex_to_rgba(TEXT_PRIMARY)
K_TEXT_SECONDARY = hex_to_rgba(TEXT_SECONDARY)
K_BORDER = hex_to_rgba(BORDER_COLOR)

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

# legacy stuff for backward compatibility
ACCENT_COLOR = K_PRIMARY
HIGHLIGHT_COLOR = K_WARNING

# def get_font_size(ratio):
#     """Calculate font size based on window height and given ratio (legacy function)"""
#     return dp(Window.height * ratio)
