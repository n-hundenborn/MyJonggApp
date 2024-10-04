from kivy.app import App
from backend.game import Game
from kivy.uix.screenmanager import ScreenManager
from frontend.screens.start_screen import StartScreen
from frontend.screens.scoreboard_screen import ScoreboardScreen
from frontend.screens.add_points_screen import AddPointsScreen
from frontend.screens.game_over_screen import GameOverScreen

class GameApp(App):
    def build(self):
        self.title = 'MyJong Calculator'
        game_instance = Game()
        sm = ScreenManager()
        sm.add_widget(StartScreen(name='start', game=game_instance))
        sm.add_widget(ScoreboardScreen(name='scoreboard', game=game_instance))
        sm.add_widget(AddPointsScreen(name='add_points', game=game_instance))
        sm.add_widget(GameOverScreen(name='game_over', game=game_instance))
        return sm

if __name__ == '__main__':
    GameApp().run()