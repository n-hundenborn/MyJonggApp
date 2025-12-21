from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from backend.game import Game


class GameModeScreen(Screen):
    """Screen to select game mode: New Game or Game Evaluation."""
    game: Game = ObjectProperty(None)

    def __init__(self, **kwargs):
        """Initialize the GameModeScreen."""
        super().__init__(**kwargs)

    def start_new_game(self):
        """Navigate to start screen for a new game."""
        self.manager.current = 'start'

    def create_evaluation(self):
        """Navigate to evaluation screen."""
        self.manager.current = 'evaluation'

    def update_fonts(self):
        """Update all font sizes when window is resized."""
        # This will be called by the main app when window is resized
        pass
