import os
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty
from kivy.clock import Clock
from backend.game import Game
from backend.evaluation.orchestrator import start_evaluation


class GameModeScreen(Screen):
    """Screen to select game mode: New Game or Game Evaluation."""
    game: Game = ObjectProperty(None)
    folder_info = StringProperty("Kein Ordner ausgewählt")
    is_loading = BooleanProperty(False)
    status_message = StringProperty("")

    def __init__(self, **kwargs):
        """Initialize the GameModeScreen."""
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
        # Reset status message when entering screen
        self.status_message = ""

    def start_new_game(self):
        """Navigate to start screen for a new game."""
        self.manager.current = 'start'

    def create_evaluation(self):
        """Create evaluation for the game folder."""
        if not (self.game and self.game.game_folder):
            self.status_message = "Fehler: Kein Ordner ausgewählt"
            return
        
        if self.is_loading:
            return  # Prevent multiple clicks
        
        # Start loading state
        self.is_loading = True
        self.status_message = "Dashboard wird erstellt..."
        
        # Schedule the actual work to run after UI update
        Clock.schedule_once(lambda dt: self._run_evaluation(), 0.1)
    
    def _run_evaluation(self):
        """Perform the actual evaluation work."""
        try:
            evaluation_filename = start_evaluation(self.game.game_folder)
            
            if evaluation_filename:
                self.status_message = f"Dashboard erfolgreich erstellt"
                # Open the file with the default system application
                os.startfile(evaluation_filename)
            else:
                self.status_message = "Fehler: Dashboard konnte nicht erstellt werden"
        except Exception as e:
            self.status_message = f"Fehler: {str(e)}"
        finally:
            self.is_loading = False

    def open_folder(self):
        """Open the game folder in the OS file explorer."""
        if self.game and self.game.game_folder:
            folder_path = str(self.game.game_folder)
            if os.path.exists(folder_path):
                os.startfile(folder_path)
            else:
                self.status_message = "Fehler: Ordner existiert nicht"
        else:
            self.status_message = "Fehler: Kein Ordner ausgewählt"

    def back_to_folder_selection(self):
        """Navigate back to welcome screen to select another folder."""
        self.manager.current = 'welcome'

    def update_fonts(self):
        """Update all font sizes when window is resized."""
        # This will be called by the main app when window is resized
        pass
