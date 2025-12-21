import os
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty

from backend.game import Game
from backend.evaluation.orchestrator import start_evaluation


class EvaluationScreen(Screen):
    """Screen for creating game evaluation."""
    game: Game = ObjectProperty(None)
    folder_info = StringProperty("Kein Ordner ausgewählt")

    def __init__(self, **kwargs):
        """Initialize the EvaluationScreen."""
        super().__init__(**kwargs)

    def on_enter(self):
        """Called when entering the screen."""
        self.update_folder_info()

    def update_folder_info(self):
        """Update the folder info display."""
        if self.game and self.game.game_folder:
            self.folder_info = f"Ordner: {str(self.game.game_folder)}"
        else:
            self.folder_info = "Kein Ordner ausgewählt"

    def create_evaluation(self):
        """Create evaluation for the game folder."""
        if not (self.game and self.game.game_folder):
            print("No folder selected")
            return
        
        evaluation_filename = start_evaluation(self.game.game_folder)
        
        if evaluation_filename:
            # Open the file with the default system application
            os.startfile(evaluation_filename)

    def back_to_menu(self):
        """Return to game mode selection screen."""
        self.manager.current = 'game_mode'

    def update_fonts(self):
        """Update all font sizes when window is resized."""
        # This will be called by the main app when window is resized
        pass
