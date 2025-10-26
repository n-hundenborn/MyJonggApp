from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty, StringProperty
from frontend.screens.styles import font_config
from backend.data_export import prepare_dataframes_for_saving, save_dataframes_to_excel
from datetime import datetime
import pandas as pd
from kivy.clock import Clock
from frontend.components.popups import show_error

class SaveGameScreen(Screen):
    game_data = ObjectProperty(None, force_dispatch=True)
    save_status = StringProperty("")
    game = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.filename_input = None
        self.save_button = None
        self.is_saved = False  # New flag to track save status

    def on_enter(self):
        self.ids.save_container.clear_widgets()
        
        # Add title
        title = Label(
            text="Speichern",
            font_size=font_config.font_size_big,
            size_hint_y=0.2
        )
        self.ids.save_container.add_widget(title)

        # Add helper label for filename input
        filename_helper = Label(
            text="Bitte geben Sie einen Dateinamen für die Rundenaufzeichnung ein:",
            font_size=font_config.font_size_medium,
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
            font_size=font_config.font_size_medium,
            size_hint_y=0.1,
            hint_text="Dateiname (ohne .xlsx)"
        )
        self.ids.save_container.add_widget(self.filename_input)

        # Add status label
        self.status_label = Label(
            text=self.save_status,
            font_size=font_config.font_size_medium,
            size_hint_y=0.2,
            size_hint_x=0.9,
            halign='center',
            valign='middle',
            text_size=(self.width, None)
        )
        self.ids.save_container.add_widget(self.status_label)

    def save_game(self):
        # If already saved, just proceed to final screen
        if self.is_saved:
            self.proceed_to_final()
            return

        if self.game_data is None:
            show_error("Keine Rundendaten vorhanden")
            return

        # Use default filename if input is empty
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        default_filename = f"mahjongg_round_{timestamp}"
        filename = f"{self.filename_input.text or default_filename}"
        
        # Disable input field and update with final filename
        self.filename_input.text = filename
        self.filename_input.disabled = True
        
        self.save_status = "Speichere Statistiken..."
        self.status_label.text = self.save_status
        
        def save_and_update_button(dt):
            try:
                df_rounds, df_standings = prepare_dataframes_for_saving(self.game_data)
                # Get folder path from the game instance
                folder_path = self.game.game_folder if self.game else None
                
                filename_saved = save_dataframes_to_excel(df_rounds, df_standings, filename, folder_path, game=self.game)
                self.save_status = f"Runde erfolgreich gespeichert unter {filename_saved}."
                self.status_label.text = self.save_status
                # Update button text and behavior
                save_button = self.ids.save_button
                save_button.text = 'Weiter'
                self.is_saved = True  # Mark as saved after successful save
            except Exception as e:
                show_error(f"Fehler beim Speichern: {str(e)}")

        Clock.schedule_once(save_and_update_button, 0.1)

    def proceed_to_final(self):
        self.manager.current = 'final'

    def update_data(self, game_data: pd.DataFrame):
        self.game_data = game_data

    def update_fonts(self):
        """Update all font sizes when window is resized"""
        # Update dynamic widgets if they exist
        if hasattr(self, 'filename_input') and self.filename_input:
            self.filename_input.font_size = font_config.font_size_medium
        if hasattr(self, 'status_label') and self.status_label:
            self.status_label.font_size = font_config.font_size_medium
        
        # Update all children in save_container
        if hasattr(self, 'ids') and hasattr(self.ids, 'save_container'):
            for child in self.ids.save_container.children:
                if isinstance(child, Label):
                    # Title gets big font, others get medium font
                    if child.text == "Speichern":
                        child.font_size = font_config.font_size_big
                    else:
                        child.font_size = font_config.font_size_medium
                elif isinstance(child, TextInput):
                    child.font_size = font_config.font_size_medium


