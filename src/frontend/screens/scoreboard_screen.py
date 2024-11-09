from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.properties import StringProperty, ObjectProperty, NumericProperty
from kivy.graphics import Color, Rectangle
from backend.game import Game
from frontend.screens.config import get_font_size, FONT_SIZE_RATIO_MEDIUM, ACCENT_COLOR
from backend.helper_functions import calculate_ranks

class ScoreboardScreen(Screen):
    game: Game = ObjectProperty(None)
    round_wind: str = StringProperty("")
    current_round_number = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.scoreboard = self.ids.scoreboard
        self.add_widget(self.layout)

    def on_enter(self):
        self.current_round_number = self.game.current_round_number
        self.update_round_wind()
        self.update_scoreboard()

    def update_round_wind(self):
        self.round_wind = self.game.get_round_wind_string()

    def update_scoreboard(self):
        self.scoreboard.clear_widgets()
        self.scoreboard.spacing = 0

        font_size = get_font_size(FONT_SIZE_RATIO_MEDIUM)

        # Add headers for the table
        self.scoreboard.add_widget(Label(text="Platz", bold=True, font_size=font_size))
        self.scoreboard.add_widget(Label(text="Spieler", bold=True, font_size=font_size))
        self.scoreboard.add_widget(Label(text="Punkte", bold=True, font_size=font_size))

        # Get ranks using helper function
        rank_map = calculate_ranks(self.game.players)

        # Display players in original order with their ranks
        for player in self.game.players:
            # Create and add labels directly
            rank_label = Label(text=str(rank_map[player]), font_size=font_size)
            name_label = Label(text=player.show(), font_size=font_size)
            points_label = Label(text=str(player.points_str), font_size=font_size)
            
            # If this is the round wind player, highlight all three labels
            if player.wind == self.game.round_wind:
                for label in [rank_label, name_label, points_label]:
                    with label.canvas.before:
                        Color(*ACCENT_COLOR)
                        Rectangle(pos=label.pos, size=label.size)
                    label.bind(pos=self._update_rect, size=self._update_rect)

            self.scoreboard.add_widget(rank_label)
            self.scoreboard.add_widget(name_label)
            self.scoreboard.add_widget(points_label)

    def _update_rect(self, instance, value):
        """Update the rectangle position and size when the layout changes."""
        instance.canvas.before.children[-1].pos = instance.pos
        instance.canvas.before.children[-1].size = instance.size

    def update_fonts(self):
        """Update all font sizes when window is resized"""
        font_size = get_font_size(FONT_SIZE_RATIO_MEDIUM)
        for child in self.scoreboard.children:
            if isinstance(child, Label):
                child.font_size = font_size
    
    def go_to_add_points(self, instance):
        self.manager.current = 'add_points'
