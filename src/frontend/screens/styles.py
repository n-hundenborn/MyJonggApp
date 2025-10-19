"""
Reusable styles and widget configurations for the application.
Provides consistent styling across all screens.
"""
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.metrics import dp
from . import config

# Button Styles
BUTTON_STYLES = {
    'default': {
        'background_color': config.K_PRIMARY,
        'background_normal': '',  # Remove default Kivy button texture
        'background_down': '',    # Remove default Kivy button texture
        'border_radius': [dp(8)],
        'padding': [dp(20), dp(10)],
        'color': config.K_SURFACE,  # Text color
    },
    'secondary': {
        'background_color': config.K_SECONDARY,
        'background_normal': '',
        'background_down': '',
        'border_radius': [dp(8)],
        'padding': [dp(20), dp(10)],
        'color': config.K_SURFACE,
    },
    'success': {
        'background_color': config.K_SUCCESS,
        'background_normal': '',
        'background_down': '',
        'border_radius': [dp(8)],
        'padding': [dp(20), dp(10)],
        'color': config.K_SURFACE,
    }
}

# Input Field Styles
INPUT_STYLES = {
    'default': {
        'background_color': config.K_SURFACE,
        'foreground_color': config.K_TEXT_PRIMARY,
        'border_color': config.K_BORDER,
        'border_width': dp(1),
        'padding': [dp(10), dp(5)],
        'border_radius': [dp(4)],
    },
    'focused': {
        'border_color': config.K_PRIMARY,
        'border_width': dp(2),
    }
}

# Card Styles
CARD_STYLES = {
    'default': {
        'background_color': config.K_SURFACE,
        'border_radius': [dp(12)],
        'padding': [dp(20)],
        'shadow_offset': (0, dp(2)),
        'shadow_color': (0, 0, 0, 0.1),  # Soft shadow
    }
}

# Table/Grid Styles
TABLE_STYLES = {
    'header': {
        'background_color': config.K_BACKGROUND,
        'text_color': config.K_TEXT_PRIMARY,
        'font_size': 'medium',
        'bold': True,
    },
    'row': {
        'background_color': config.K_SURFACE,
        'text_color': config.K_TEXT_PRIMARY,
        'alternate_color': config.hex_to_rgba(config.BACKGROUND_COLOR, 0.5),
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
        Color(*config.K_SURFACE)
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
