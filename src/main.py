from kivy.app import App
from backend.game import Game
from kivy.uix.screenmanager import ScreenManager
from frontend.screens.start_screen import StartScreen
from frontend.screens.scoreboard_screen import ScoreboardScreen
from frontend.screens.add_points_screen import AddPointsScreen
from frontend.screens.game_over_screen import GameOverScreen
from frontend.screens.stats_screen import StatsScreen
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
            'start': StartScreen(name='start', game=game_instance),
            'scoreboard': ScoreboardScreen(name='scoreboard', game=game_instance),
            'add_points': AddPointsScreen(name='add_points', game=game_instance),
            'round_summary': RoundSummaryScreen(name='round_summary', game=game_instance),
            'game_over': GameOverScreen(name='game_over'),
            'save_game': SaveGameScreen(name='save_game'),
            'stats': StatsScreen(name='stats')
        }
        
        for screen in screens.values():
            self.sm.add_widget(screen)

        # Define update_game_data function
        def update_game_data():
            game_data = game_instance.create_game_dataframe()
            for screen_name in ['game_over', 'save_game', 'stats']:
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
                update_game_data() if value in ['game_over', 'save_game', 'stats'] else None
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
    GameApp().run()