from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty, StringProperty
from frontend.screens.config import get_font_size, FONT_SIZE_RATIO_MEDIUM, FONT_SIZE_RATIO_BIG
from backend.helper_functions import prepare_dataframes_for_saving, save_dataframes_to_excel
from datetime import datetime
import pandas as pd
from kivy.clock import Clock
from frontend.components.popups import show_error

class SaveGameScreen(Screen):
    game_data = ObjectProperty(None, force_dispatch=True)
    save_status = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.filename_input = None
        self.save_button = None
        self.is_saved = False  # New flag to track save status

    def on_enter(self):
        self.ids.save_container.clear_widgets()
        
        # Add title
        title = Label(
            text="Spiel speichern",
            font_size=get_font_size(FONT_SIZE_RATIO_BIG),
            size_hint_y=0.2
        )
        self.ids.save_container.add_widget(title)

        # Add helper label for filename input
        filename_helper = Label(
            text="Bitte geben Sie einen Dateinamen für die Spielaufzeichnung ein:",
            font_size=get_font_size(FONT_SIZE_RATIO_MEDIUM),
            size_hint_y=0.1
        )
        self.ids.save_container.add_widget(filename_helper)

        # Generate default filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        default_filename = f"mahjongg_game_{timestamp}"

        # Add filename input
        self.filename_input = TextInput(
            text=default_filename,
            multiline=False,
            font_size=get_font_size(FONT_SIZE_RATIO_MEDIUM),
            size_hint_y=0.1,
            hint_text="Dateiname (ohne .xlsx)"
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
        # If already saved, just proceed to stats
        if self.is_saved:
            self.proceed_to_stats()
            return

        if self.game_data is None:
            show_error("Keine Spieldaten vorhanden")
            return

        # Use default filename if input is empty
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        default_filename = f"mahjongg_game_{timestamp}"
        filename = f"{self.filename_input.text or default_filename}"
        
        # Disable input field and update with final filename
        self.filename_input.text = filename
        self.filename_input.disabled = True
        
        self.save_status = "Speichere Spielstatistiken..."
        self.status_label.text = self.save_status
        
        def save_and_update_button(dt):
            try:
                df_rounds, df_standings = prepare_dataframes_for_saving(self.game_data)
                filename_saved = save_dataframes_to_excel(df_rounds, df_standings, filename)
                self.save_status = f"Spiel erfolgreich gespeichert als {filename_saved}"
                self.status_label.text = self.save_status
                # Update button text and behavior
                save_button = self.ids.save_button
                save_button.text = 'Weiter zu Statistiken'
                self.is_saved = True  # Mark as saved after successful save
            except Exception as e:
                show_error(f"Fehler beim Speichern: {str(e)}")

        Clock.schedule_once(save_and_update_button, 0.5)

    def proceed_to_stats(self):
        self.manager.current = 'stats'

    def update_data(self, game_data: pd.DataFrame):
        self.game_data = game_data


