"""
Reusable styles and widget configurations for the application.
Provides consistent styling across all screens.
"""
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.event import EventDispatcher
from kivy.properties import NumericProperty

# Layout Constants
SCREEN_PADDING = dp(20)
SECTION_SPACING = dp(20)
WIDGET_SPACING = dp(10)
CONTENT_WIDTH = dp(800)  # Max width for content

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
        """Update all font sizes based on current window height with minimum sizes"""
        # Calculate base sizes
        height = Window.height
        # Add minimum sizes to prevent text from becoming too small
        min_small = 14
        min_medium = 16
        min_big = 20
        
        # Calculate sizes with minimums
        self.font_size_small = max(min_small, int(height * FONT_SIZE_RATIO_SMALL))
        self.font_size_medium = max(min_medium, int(height * FONT_SIZE_RATIO_MEDIUM))
        self.font_size_big = max(min_big, int(height * FONT_SIZE_RATIO_BIG))

# Global font config instance
font_config = FontConfig()

# Modern Color Palette
# Base Colors
BACKGROUND_COLOR = "#F8F9FA"  # Soft Off-White
SURFACE_COLOR = "#FFFFFF"     # Pure White
PRIMARY_COLOR = "#6366F1"     # Modern Indigo
SECONDARY_COLOR = "#64748B"   # Slate Gray

# Semantic Colors
SUCCESS_COLOR = "#10B981"     # Emerald Green (for winner)
WARNING_COLOR = "#F59E0B"     # Amber (for round wind)
TEXT_PRIMARY = "#1F2937"      # Dark Gray (main text)
TEXT_SECONDARY = "#6B7280"    # Medium Gray (secondary text)
BORDER_COLOR = "#E5E7EB"      # Light Gray (subtle borders)

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

# Button Styles
BUTTON_STYLES = {
    'default': {
        'background_color': K_PRIMARY,
        'background_normal': '',  # Remove default Kivy button texture
        'background_down': '',    # Remove default Kivy button texture
        'border_radius': [dp(8)],
        'padding': [dp(20), dp(10)],
        'color': K_SURFACE,  # Text color
    },
    'secondary': {
        'background_color': K_SECONDARY,
        'background_normal': '',
        'background_down': '',
        'border_radius': [dp(8)],
        'padding': [dp(20), dp(10)],
        'color': K_SURFACE,
    },
    'success': {
        'background_color': K_SUCCESS,
        'background_normal': '',
        'background_down': '',
        'border_radius': [dp(8)],
        'padding': [dp(20), dp(10)],
        'color': K_SURFACE,
    }
}

# Input Field Styles
INPUT_STYLES = {
    'default': {
        'background_color': K_SURFACE,
        'foreground_color': K_TEXT_PRIMARY,
        'border_color': K_BORDER,
        'border_width': dp(1),
        'padding': [dp(10), dp(5)],
        'border_radius': [dp(4)],
    },
    'focused': {
        'border_color': K_PRIMARY,
        'border_width': dp(2),
    }
}

# Card Styles
CARD_STYLES = {
    'default': {
        'background_color': K_SURFACE,
        'border_radius': [dp(12)],
        'padding': [dp(20)],
        'shadow_offset': (0, dp(2)),
        'shadow_color': (0, 0, 0, 0.1),  # Soft shadow
    }
}

# Table/Grid Styles
TABLE_STYLES = {
    'header': {
        'background_color': K_BACKGROUND,
        'text_color': K_TEXT_PRIMARY,
        'font_size': 'medium',
        'bold': True,
    },
    'row': {
        'background_color': K_SURFACE,
        'text_color': K_TEXT_PRIMARY,
        'alternate_color': hex_to_rgba(BACKGROUND_COLOR, 0.5),
    }
}

# Animation Configurations
ANIMATIONS = {
    'button_press': {
        'duration': 0.1,
        'transition': 'in_out_sine',
        'scale': 0.95,
    },
    'fade_in': {
        'duration': 0.2,
        'transition': 'in_out_sine',
    },
    'hover': {
        'duration': 0.1,
        'scale': 1.02,
    }
}

def apply_button_style(widget, style='default'):
    """Apply button styling to a widget"""
    style_dict = BUTTON_STYLES[style]
    for key, value in style_dict.items():
        setattr(widget, key, value)

def apply_input_style(widget, style='default'):
    """Apply input field styling to a widget"""
    style_dict = INPUT_STYLES[style]
    for key, value in style_dict.items():
        setattr(widget, key, value)

def apply_card_style(widget):
    """Apply card styling to a widget"""
    style_dict = CARD_STYLES['default']
    with widget.canvas.before:
        Color(*K_SURFACE)
        RoundedRectangle(
            pos=widget.pos,
            size=widget.size,
            radius=style_dict['border_radius']
        )
    widget.padding = style_dict['padding']

def apply_table_style(widget, row_type='row', index=None):
    """Apply table styling to a widget"""
    style_dict = TABLE_STYLES[row_type]
    if row_type == 'row' and index is not None:
        # Apply alternating row colors
        bg_color = (style_dict['alternate_color'] if index % 2 
                   else style_dict['background_color'])
    else:
        bg_color = style_dict['background_color']
    
    with widget.canvas.before:
        Color(*bg_color)
        Rectangle(pos=widget.pos, size=widget.size)
