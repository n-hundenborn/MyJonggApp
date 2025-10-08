from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.core.window import Window
from frontend.screens.config import font_config

class ErrorPopup(Popup):
    def __init__(self, error_message, **kwargs):
        super().__init__(**kwargs)
        self.title = 'Fehler'
        self.title_size = font_config.font_size_big
        self.title_align = 'center'
        
        # Make popup size responsive to window size
        self.size_hint = (0.8, 0.4)  # 80% width, 40% height of window
        self.size_hint_min = (400, 200)  # Minimum size
        
        # Store references for font updates
        self.message_label = None
        self.close_button = None
        
        # Bind to window resize to update title font too
        Window.bind(size=self._on_window_resize)
        
        # Create content layout with responsive padding
        content = BoxLayout(
            orientation='vertical', 
            padding=[Window.width * 0.02, Window.height * 0.02]  # 2% of window dimensions
        )
        
        # Message label with responsive font size
        self.message_label = Label(
            text=error_message,
            text_size=(None, None),  # Will be set after layout
            size_hint_y=0.7,
            halign='center',
            valign='middle',
            font_size=font_config.font_size_medium
        )
        
        # Close button with responsive font size
        self.close_button = Button(
            text='Verstanden',
            size_hint_y=0.3,
            size_hint_x=0.4,
            pos_hint={'center_x': 0.5},
            on_release=self.dismiss,
            font_size=font_config.font_size_medium
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
    
    def _on_window_resize(self, *args):
        """Update popup elements when window is resized"""
        # Update title font size
        self.title_size = font_config.font_size_big
        
        if self.message_label:
            self.message_label.font_size = font_config.font_size_medium
        if self.close_button:
            self.close_button.font_size = font_config.font_size_medium
        
        # Update padding based on new window size
        if self.content:
            self.content.padding = [Window.width * 0.02, Window.height * 0.02]
    
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