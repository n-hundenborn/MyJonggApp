from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.properties import StringProperty, ObjectProperty
from backend.game import Game

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
        self.scoreboard.add_widget(Label(text="Wind", bold=True))
        self.scoreboard.add_widget(Label(text="Name", bold=True))
        self.scoreboard.add_widget(Label(text="Punkte", bold=True))

        # Populate the scoreboard with player data
        for player in self.game.players:
            self.scoreboard.add_widget(Label(text=player.wind.value))
            self.scoreboard.add_widget(Label(text=player.name))
            self.scoreboard.add_widget(Label(text=str(player.points)))

    def go_to_add_points(self, instance):
        self.manager.current = 'add_points'