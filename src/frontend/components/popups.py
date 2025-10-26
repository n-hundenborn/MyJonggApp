"""
Popup components for the application.
"""
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from frontend.shared.styles import (
    font_config, K_SURFACE, K_TEXT_PRIMARY, CARD_STYLES
)
from .buttons import StyledButton
from .cards import Card

class ErrorPopup(Popup):
    def __init__(self, error_message, **kwargs):
        # Set modern styling before init
        kwargs.update({
            'background': '',  # Remove default background
            'background_color': [0, 0, 0, 0],  # Transparent
            'title': 'Fehler',
            'title_size': font_config.font_size_big,
            'title_align': 'center',
            'title_color': K_TEXT_PRIMARY,
            'separator_height': 0,  # Remove separator
            'size_hint': (0.8, None),  # 80% width, fixed height
            'height': dp(250),  # Fixed height
            'size_hint_min_x': dp(400),  # Minimum width
        })
        super().__init__(**kwargs)
        
        # Store references for font updates
        self.message_label = None
        self.close_button = None
        
        # Create content layout with card styling
        content = Card()
        
        # Apply card styling to popup
        with self.canvas.before:
            Color(*K_SURFACE)
            self.background_rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=CARD_STYLES['default']['border_radius']
            )
        self.bind(pos=self._update_background, size=self._update_background)
        
        # Message label with modern styling
        self.message_label = Label(
            text=error_message,
            text_size=(None, None),
            size_hint_y=0.7,
            halign='center',
            valign='middle',
            font_size=font_config.font_size_medium,
            color=K_TEXT_PRIMARY
        )
        
        # Close button with modern styling
        self.close_button = StyledButton(
            text='Verstanden',
            on_release=self.dismiss
        )
        
        # Add widgets to layout
        content.add_widget(self.message_label)
        content.add_widget(self.close_button)
        
        # Set the content
        self.content = content
        
        # Bind to window resize to update fonts and layout
        Window.bind(size=self._on_window_resize)
        
        # Update text_size after content is ready
        self.bind(size=self._update_text_size)
    
    def _update_background(self, instance, value):
        """Update the background rectangle when popup size/position changes"""
        if hasattr(self, 'background_rect'):
            self.background_rect.pos = self.pos
            self.background_rect.size = self.size

    def _on_window_resize(self, *args):
        """Update popup elements when window is resized"""
        # Update title font size
        self.title_size = font_config.font_size_big
        
        if self.message_label:
            self.message_label.font_size = font_config.font_size_medium
            # Update text wrapping
            self.message_label.text_size = (self.width * 0.9, None)
    
    def _update_text_size(self, *args):
        """Update text wrapping size when popup size changes"""
        if self.message_label and self.size[0] > 0:
            # Set text_size to 90% of popup width to allow for padding
            self.message_label.text_size = (self.size[0] * 0.9, None)
    
    def dismiss(self, *args):
        """Clean up window binding when popup is dismissed"""
        Window.unbind(size=self._on_window_resize)
        super().dismiss()

def show_error(message: str):
    """Utility function to show error popup"""
    popup = ErrorPopup(message)
    popup.open()