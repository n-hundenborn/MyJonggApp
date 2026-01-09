from kivy.app import App
from backend.game import Game
from kivy.uix.screenmanager import ScreenManager
from frontend.screens.welcome_screen import WelcomeScreen
from frontend.screens.game_mode_screen import GameModeScreen
from frontend.screens.start_screen import StartScreen
from frontend.screens.scoreboard_screen import ScoreboardScreen
from frontend.screens.add_points_screen import AddPointsScreen
from frontend.screens.game_over_screen import GameOverScreen
from frontend.screens.final_screen import FinalScreen
from frontend.screens.save_game_screen import SaveGameScreen
from frontend.screens.round_summary_screen import RoundSummaryScreen
from kivy.core.window import Window
from kivy.clock import Clock
import os
import sys
from kivy.resources import resource_add_path

# Add the resource path for PyInstaller bundled files
# This is needed when running the bundled executable
if hasattr(sys, '_MEIPASS'):
    resource_add_path(os.path.join(sys._MEIPASS))

class GameApp(App):
    def build(self):
        Window.size = (1024, 768)
        Window.bind(on_resize=self._on_resize)
        
        self.title = 'Myjongg Calculator'
        game_instance = Game()
        self.sm = ScreenManager()

        # Add screens that need direct game instance
        screens = {
            'welcome': WelcomeScreen(name='welcome', game=game_instance),
            'game_mode': GameModeScreen(name='game_mode', game=game_instance),
            'start': StartScreen(name='start', game=game_instance),
            'scoreboard': ScoreboardScreen(name='scoreboard', game=game_instance),
            'add_points': AddPointsScreen(name='add_points', game=game_instance),
            'round_summary': RoundSummaryScreen(name='round_summary', game=game_instance),
            'game_over': GameOverScreen(name='game_over'),
            'save_game': SaveGameScreen(name='save_game', game=game_instance),
            'final': FinalScreen(name='final', game=game_instance)
        }
        
        for screen in screens.values():
            self.sm.add_widget(screen)

        # Set welcome screen as initial screen
        self.sm.current = 'welcome'

        # Define update_game_data function
        def update_game_data():
            game_data = game_instance.create_game_dataframe()
            for screen_name in ['game_over', 'save_game', 'final']:
                if screen_name in screens:
                    screen = screens[screen_name]
                    if hasattr(screen, 'update_data'):
                        screen.update_data(game_data)

        # Add method to update screens before transition
        def pre_transition(*args):
            next_screen = args[1]  # The screen we're transitioning to
            if next_screen in screens:
                screen_instance = screens[next_screen]
                if hasattr(screen_instance, 'update_scoreboard'):
                    screen_instance.update_scoreboard()
                if hasattr(screen_instance, 'update_round_wind'):
                    screen_instance.update_round_wind()

        # Bind the update methods
        self.sm.bind(
            current=lambda instance, value: 
                update_game_data() if value in ['game_over', 'save_game', 'final'] else None
        )
        self.sm.bind(current=pre_transition)

        return self.sm

    def _on_resize(self, instance, width, height):
        # Schedule the update for the next frame to ensure all widgets are ready
        Clock.schedule_once(lambda dt: self._update_fonts())

    def _update_fonts(self):
        # Force all screens to update their fonts
        for screen in self.sm.screens:
            if hasattr(screen, 'update_fonts'):
                screen.update_fonts()


if __name__ == '__main__':
    from multiprocessing import Process, freeze_support
    freeze_support()
    Process(target=GameApp().run()).start()