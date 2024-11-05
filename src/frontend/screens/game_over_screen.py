from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.properties import ObjectProperty, StringProperty
from backend.game import Game
from frontend.screens.config import FONT_SIZE_MEDIUM, FONT_SIZE_BIG

class GameOverScreen(Screen):
    game: Game = ObjectProperty(None)
    winner_text = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_enter(self):
        self.update_scoreboard()
        self.update_winner()

    def update_scoreboard(self):
        self.ids.scoreboard.clear_widgets()

        # Add headers for the table
        self.ids.scoreboard.add_widget(Label(text="Platz", bold=True, font_size=FONT_SIZE_MEDIUM))
        self.ids.scoreboard.add_widget(Label(text="Wind", bold=True, font_size=FONT_SIZE_MEDIUM))
        self.ids.scoreboard.add_widget(Label(text="Name", bold=True, font_size=FONT_SIZE_MEDIUM))
        self.ids.scoreboard.add_widget(Label(text="Punkte", bold=True, font_size=FONT_SIZE_MEDIUM))

        # Get final standings and populate the scoreboard
        standings = self.game.get_final_standings()
        for player, rank in standings:
            self.ids.scoreboard.add_widget(Label(text=str(rank), font_size=FONT_SIZE_MEDIUM))
            self.ids.scoreboard.add_widget(Label(text=str(player.wind), font_size=FONT_SIZE_MEDIUM))
            self.ids.scoreboard.add_widget(Label(text=player.name, font_size=FONT_SIZE_MEDIUM))
            self.ids.scoreboard.add_widget(Label(text=player.points_str, font_size=FONT_SIZE_MEDIUM))

    def update_winner(self):
        standings = self.game.get_final_standings()
        winner, _ = standings[0]
        self.winner_text = f"{winner.name} gewinnt!"
