"""
Card components for the application.
"""
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp
from frontend.shared.styles import apply_card_style, CARD_STYLES

class Card(BoxLayout):
    """A card container with consistent styling."""
    def __init__(self, **kwargs):
        # Set default padding and spacing
        kwargs.setdefault('padding', CARD_STYLES['default']['padding'])
        kwargs.setdefault('spacing', dp(20))
        kwargs.setdefault('orientation', 'vertical')
        
        super().__init__(**kwargs)
        apply_card_style(self)
