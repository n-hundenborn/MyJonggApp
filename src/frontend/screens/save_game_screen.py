from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty, StringProperty
from frontend.screens.config import get_font_size, FONT_SIZE_RATIO_MEDIUM, FONT_SIZE_RATIO_BIG
from backend.helper_functions import save_dataframes_to_excel
from datetime import datetime
from kivy.clock import Clock

class SaveGameScreen(Screen):
    game_data = ObjectProperty(None, force_dispatch=True)
    save_status = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.filename_input = None
        self.save_button = None

    def on_enter(self):
        self.ids.save_container.clear_widgets()
        
        # Add title
        title = Label(
            text="Spiel speichern",
            font_size=get_font_size(FONT_SIZE_RATIO_BIG),
            size_hint_y=0.2
        )
        self.ids.save_container.add_widget(title)

        # Generate default filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        default_filename = f"mahjongg_game_{timestamp}"

        # Add filename input
        self.filename_input = TextInput(
            text=default_filename,
            multiline=False,
            font_size=get_font_size(FONT_SIZE_RATIO_MEDIUM),
            size_hint_y=0.1,
        )
        self.ids.save_container.add_widget(self.filename_input)

        # Add status label
        self.status_label = Label(
            text=self.save_status,
            font_size=get_font_size(FONT_SIZE_RATIO_MEDIUM),
            size_hint_y=0.2,
            size_hint_x=0.9,
            halign='center',
            valign='middle',
            text_size=(self.width, None)
        )
        self.ids.save_container.add_widget(self.status_label)

    def save_game(self):
        if self.game_data is None:
            self.save_status = "Keine Spieldaten vorhanden"
            self.status_label.text = self.save_status
            return

        filename = f"{self.filename_input.text}.xlsx"
        self.save_status = "Speichere Spielstatistiken..."
        self.status_label.text = self.save_status
        
        def save_and_update_button(dt):
            try:
                file_name = save_dataframes_to_excel(self.game_data, filename)
                self.save_status = f"Spiel erfolgreich gespeichert als {file_name}"
                self.status_label.text = self.save_status
                # Update button text and behavior
                save_button = self.ids.save_button
                save_button.text = 'Weiter zu Statistiken'
                save_button.unbind(on_release=self.save_game)
                save_button.bind(on_release=lambda x: self.proceed_to_stats())
            except Exception as e:
                self.save_status = f"Fehler beim Speichern: {str(e)}"
                self.status_label.text = self.save_status

        Clock.schedule_once(save_and_update_button, 0.5)

    def proceed_to_stats(self):
        self.manager.current = 'stats'