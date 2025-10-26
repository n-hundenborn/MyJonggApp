"""
Button components for the application.
"""
from kivy.uix.button import Button
from kivy.metrics import dp
from frontend.shared.styles import apply_button_style

class StyledButton(Button):
    """A button with consistent styling."""
    def __init__(self, style='default', **kwargs):
        # Set default size if not provided
        if 'size_hint' not in kwargs:
            kwargs['size_hint'] = (None, None)
            kwargs['size'] = (dp(200), dp(50))
        if 'pos_hint' not in kwargs:
            kwargs['pos_hint'] = {'center_x': 0.5}
            
        super().__init__(**kwargs)
        apply_button_style(self, style)
