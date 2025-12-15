"""
Input components for the application.
"""
from kivy.uix.textinput import TextInput
from frontend.shared.styles import apply_input_style

class StyledInput(TextInput):
    """A text input with consistent styling."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        apply_input_style(self)
        
    def on_focus(self, instance, value):
        """Apply focused style when input is focused"""
        apply_input_style(self, 'focused' if value else 'default')
