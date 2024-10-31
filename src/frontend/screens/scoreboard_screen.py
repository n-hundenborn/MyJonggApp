from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.properties import StringProperty, ObjectProperty
from backend.game import Game
from frontend.screens.config import FONT_SIZE_MEDIUM

class ScoreboardScreen(Screen):
    game: Game = ObjectProperty(None)
    round_wind: str = StringProperty("")  # Initialize with an empty string

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = BoxLayout(orientation='vertical')
        self.scoreboard = self.ids.scoreboard  # Reference to the scoreboard BoxLayout
        self.add_widget(self.layout)

    def on_enter(self):
        self.update_round_wind()
        self.update_scoreboard()

    def update_round_wind(self):
        self.round_wind = self.game.get_round_wind_string()  # Update the round wind string

    def update_scoreboard(self):
        self.scoreboard.clear_widgets()

        # Add headers for the table
        self.scoreboard.add_widget(Label(text="Wind", bold=True, font_size=FONT_SIZE_MEDIUM))
        self.scoreboard.add_widget(Label(text="Name", bold=True, font_size=FONT_SIZE_MEDIUM))
        self.scoreboard.add_widget(Label(text="Punkte", bold=True, font_size=FONT_SIZE_MEDIUM))

        # Populate the scoreboard with player data
        for player in self.game.players:
            self.scoreboard.add_widget(Label(text=player.wind.value, font_size=FONT_SIZE_MEDIUM))
            self.scoreboard.add_widget(Label(text=player.name, font_size=FONT_SIZE_MEDIUM))
            self.scoreboard.add_widget(Label(text=str(player.points_str), font_size=FONT_SIZE_MEDIUM))

    def go_to_add_points(self, instance):
        self.manager.current = 'add_points'