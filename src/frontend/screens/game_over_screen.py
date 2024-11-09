from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.properties import ObjectProperty, StringProperty
from backend.game import Game
from frontend.screens.config import get_font_size, FONT_SIZE_RATIO_MEDIUM
from backend.helper_functions import calculate_ranks

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
        font_size = get_font_size(FONT_SIZE_RATIO_MEDIUM)

        # Add headers for the table
        self.ids.scoreboard.add_widget(Label(text="Platz", bold=True, font_size=font_size))
        self.ids.scoreboard.add_widget(Label(text="Spieler", bold=True, font_size=font_size))
        self.ids.scoreboard.add_widget(Label(text="Punkte", bold=True, font_size=font_size))

        rank_map = calculate_ranks(self.game.players)

        # Sort players by rank for display
        sorted_players = sorted(self.game.players, key=lambda p: rank_map[p])
        for player in sorted_players:
            self.ids.scoreboard.add_widget(Label(text=str(rank_map[player]), font_size=font_size))
            self.ids.scoreboard.add_widget(Label(text=player.show(), font_size=font_size))
            self.ids.scoreboard.add_widget(Label(text=player.points_str, font_size=font_size))

    def update_winner(self):
        # Get player with rank 1
        rank_map = calculate_ranks(self.game.players)
        winner = min(self.game.players, key=lambda p: rank_map[p])
        self.winner_text = f"{winner.name} gewinnt!"

    def update_fonts(self):
        """Update all font sizes when window is resized"""
        font_size = get_font_size(FONT_SIZE_RATIO_MEDIUM)
        for child in self.ids.scoreboard.children:
            if isinstance(child, Label):
                child.font_size = font_size
