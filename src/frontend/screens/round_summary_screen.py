from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.properties import ObjectProperty, NumericProperty
from backend.game import Game
from frontend.screens.config import get_font_size, FONT_SIZE_RATIO_MEDIUM, ACCENT_COLOR
from kivy.graphics import Color, Rectangle

class RoundSummaryScreen(Screen):
    """A screen for showing the round summary before confirming points."""
    game: Game = ObjectProperty(None)
    current_round_number = NumericProperty(0)

    def on_enter(self):
        """Update the display when entering the screen."""
        self.ids.summary_layout.clear_widgets()
        self.current_round_number = self.game.current_round_number
        
        # Get the last round
        current_round = self.game.rounds[-1]
        
        for player in self.game.players:
            player_layout = BoxLayout()
            
            # Find the score for this player
            score = next(score for score in current_round.scores if score.player == player)
            
            # Highlight round wind instead of winner
            if player.wind == current_round.round_wind:
                with player_layout.canvas.before:
                    Color(*ACCENT_COLOR)
                    self.rect = Rectangle(pos=player_layout.pos, size=player_layout.size)
                player_layout.bind(pos=self._update_rect, size=self._update_rect)

            # Player name
            player_layout.add_widget(Label(
                text=f"{player.show()}",
                font_size=get_font_size(FONT_SIZE_RATIO_MEDIUM)
            ))

            # Round points (calculated points)
            player_layout.add_widget(Label(
                text=str(score.calculated_points),
                font_size=get_font_size(FONT_SIZE_RATIO_MEDIUM)
            ))

            # Point change
            player_layout.add_widget(Label(
                text=str(score.net_points),
                font_size=get_font_size(FONT_SIZE_RATIO_MEDIUM)
            ))

            self.ids.summary_layout.add_widget(player_layout)

    def confirm_points(self):
        """Apply the points and proceed to the next screen."""
        current_round = self.game.rounds[-1]
        
        if self.game.is_game_over(current_round.winner):
            self.manager.current = 'game_over'
        else:
            self.game.start_new_round(current_round.winner)
            self.manager.current = 'scoreboard'

    def update_fonts(self):
        """Update all font sizes when window is resized."""
        font_size = get_font_size(FONT_SIZE_RATIO_MEDIUM)
        for child in self.ids.summary_layout.children:
            if isinstance(child, BoxLayout):
                for widget in child.children:
                    if isinstance(widget, Label):
                        widget.font_size = font_size

    def _update_rect(self, instance, value):
        """Update the rectangle position and size when the layout changes."""
        self.rect.pos = instance.pos
        self.rect.size = instance.size 