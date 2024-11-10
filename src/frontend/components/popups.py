from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from frontend.screens.config import get_font_size, FONT_SIZE_RATIO_SMALL

class ErrorPopup(Popup):
    def __init__(self, error_message, **kwargs):
        super().__init__(**kwargs)
        self.title = 'Fehler'
        self.size_hint = (None, None)
        self.size = (600, 300)
        
        # Create content layout
        content = BoxLayout(orientation='vertical', padding=[20, 20])
        
        # Message label with word wrap
        message_label = Label(
            text=error_message,
            text_size=(560, None),
            size_hint_y=0.7,
            halign='center',
            valign='middle',
            font_size=get_font_size(FONT_SIZE_RATIO_SMALL * 0.8)
        )
        
        # Close button
        close_button = Button(
            text='Schließen',
            size_hint_y=0.3,
            size_hint_x=0.4,
            pos_hint={'center_x': 0.5},
            on_release=self.dismiss,
            font_size=get_font_size(FONT_SIZE_RATIO_SMALL * 0.8)
        )
        
        # Add widgets to layout
        content.add_widget(message_label)
        content.add_widget(close_button)
        
        # Set the content
        self.content = content

def show_error(message: str):
    """Utility function to show error popup"""
    popup = ErrorPopup(message)
    popup.open() 