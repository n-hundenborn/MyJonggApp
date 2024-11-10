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
        self.sm.add_widget(StartScreen(name='start', game=game_instance))
        self.sm.add_widget(ScoreboardScreen(name='scoreboard', game=game_instance))
        self.sm.add_widget(AddPointsScreen(name='add_points', game=game_instance))
        self.sm.add_widget(RoundSummaryScreen(name='round_summary', game=game_instance))

        # Create screens that only need the DataFrame
        game_over_screen = GameOverScreen(name='game_over')
        save_game_screen = SaveGameScreen(name='save_game')
        stats_screen = StatsScreen(name='stats')

        # Add method to update DataFrame when needed
        def update_game_data(*args):
            df = game_instance.create_game_dataframe()
            game_over_screen.game_data = df
            save_game_screen.game_data = df
            stats_screen.game_data = df

        # Bind the update method to screen transitions
        self.sm.bind(current=lambda instance, value: 
            update_game_data() if value in ['game_over', 'save_game', 'stats'] else None
        )

        # Add the screens to the manager
        self.sm.add_widget(game_over_screen)
        self.sm.add_widget(save_game_screen)
        self.sm.add_widget(stats_screen)

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