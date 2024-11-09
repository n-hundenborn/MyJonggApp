from kivy.app import App
from backend.game import Game
from kivy.uix.screenmanager import ScreenManager
from frontend.screens.start_screen import StartScreen
from frontend.screens.scoreboard_screen import ScoreboardScreen
from frontend.screens.add_points_screen import AddPointsScreen
from frontend.screens.game_over_screen import GameOverScreen
from kivy.core.window import Window
from kivy.clock import Clock
import os
import sys
from kivy.resources import resource_add_path, resource_find

if hasattr(sys, '_MEIPASS'):
    resource_add_path(os.path.join(sys._MEIPASS))

class GameApp(App):
    def build(self):
        Window.size = (1024, 768)
        Window.bind(on_resize=self._on_resize)
        
        self.title = 'MyJong Calculator'
        game_instance = Game()
        self.sm = ScreenManager()
        self.sm.add_widget(StartScreen(name='start', game=game_instance))
        self.sm.add_widget(ScoreboardScreen(name='scoreboard', game=game_instance))
        self.sm.add_widget(AddPointsScreen(name='add_points', game=game_instance))
        self.sm.add_widget(GameOverScreen(name='game_over', game=game_instance))
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