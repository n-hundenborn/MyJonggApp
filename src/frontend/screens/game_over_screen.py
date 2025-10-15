from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.properties import ObjectProperty, StringProperty
from frontend.screens.config import font_config
import pandas as pd

class GameOverScreen(Screen):
    game_data = ObjectProperty(None, force_dispatch=True)
    winner_text = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_enter(self):
        self.update_scoreboard()
        self.update_winner()

    def update_scoreboard(self):
        self.ids.scoreboard.clear_widgets()
        font_size = font_config.font_size_medium

        # Add headers for the table
        self.ids.scoreboard.add_widget(Label(text="Platz", bold=True, font_size=font_size))
        self.ids.scoreboard.add_widget(Label(text="Spieler", bold=True, font_size=font_size))
        self.ids.scoreboard.add_widget(Label(text="Punkte", bold=True, font_size=font_size))

        # Get the last round's data for each player
        if self.game_data is not None:
            last_round_data = self.game_data.loc[self.game_data['round'] == self.game_data['round'].max()]
            
            # Sort by rank
            sorted_data = last_round_data.sort_values('rank')
            
            for _, row in sorted_data.iterrows():
                self.ids.scoreboard.add_widget(Label(text=str(row['rank']), font_size=font_size))
                self.ids.scoreboard.add_widget(Label(text=f"[{row['wind']}] {row['player']}", font_size=font_size))
                self.ids.scoreboard.add_widget(Label(text=f"{row['running_sum']:,}".replace(",", "."), font_size=font_size))

    def update_winner(self):
        if self.game_data is not None:
            # Get the last round's data and find the player with rank 1
            last_round_data = self.game_data.loc[self.game_data['round'] == self.game_data['round'].max()]
            winner_data = last_round_data.loc[last_round_data['rank'] == 1].iloc[0]
            self.winner_text = f"{winner_data['player']} gewinnt!"

    def update_fonts(self):
        """Update all font sizes when window is resized"""
        for child in self.ids.scoreboard.children:
            if isinstance(child, Label):
                child.font_size = font_config.font_size_medium

    def proceed_to_save_game(self):
        self.manager.current = 'save_game'

    def update_data(self, game_data: pd.DataFrame):
        """Update screen with game data"""
        self.game_data = game_data
        self.update_scoreboard()
        self.update_winner()
