from kivy.metrics import dp
from kivy.core.window import Window
from kivy.event import EventDispatcher
from kivy.properties import NumericProperty

# Font sizes as ratios of window height
FONT_SIZE_RATIO_SMALL = 0.02  # 2.5% of window height
FONT_SIZE_RATIO_MEDIUM = 0.029  # 3.5% of window height
FONT_SIZE_RATIO_BIG = 0.035    # 4.5% of window height

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
    """Calculate font size based on window height and given ratio (legacy function)"""
    return dp(Window.height * ratio)