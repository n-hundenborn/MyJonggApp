from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.properties import StringProperty, ObjectProperty, NumericProperty
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from backend.game import Game
from frontend.shared.styles import K_PRIMARY, font_config
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
        self._keyboard = None

    def on_enter(self):
        self.current_round_number = self.game.current_round_number
        self.update_round_wind()
        self.update_scoreboard()
        # Set up keyboard when entering screen
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        if self._keyboard:
            self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def on_pre_leave(self):
        # Clean up keyboard when leaving screen
        self._keyboard_closed()

    def _keyboard_closed(self):
        if self._keyboard:
            self._keyboard.unbind(on_key_down=self._on_keyboard_down)
            self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[0] in (13, 271):  # 13 = main Enter, 271 = numpad Enter
            if hasattr(self.ids, 'points_button'):
                self.ids.points_button.trigger_action(duration=0.1)
                return True
        return False

    def update_round_wind(self):
        self.round_wind = self.game.get_round_wind_string()

    def update_scoreboard(self):
        self.scoreboard.clear_widgets()
        self.scoreboard.spacing = 0

        font_size = font_config.font_size_medium

        # Add headers for the table
        self.scoreboard.add_widget(Label(text="Platz", bold=True, font_size=font_size))
        self.scoreboard.add_widget(Label(text="Spieler", bold=True, font_size=font_size))
        self.scoreboard.add_widget(Label(text="Punkte", bold=True, font_size=font_size))

        # Get ranks using helper function
        rank_map = calculate_ranks(self.game.players)

        # Sort players by rank (ascending order of rank_map values means descending ranks)
        sorted_players = sorted(self.game.players, key=lambda p: rank_map[p])
        
        # Display players in rank order
        for player in sorted_players:
            # Create and add labels directly
            rank_label = Label(text=str(rank_map[player]), font_size=font_size)
            name_label = Label(text=player.show(), font_size=font_size)
            points_label = Label(text=str(player.points_str), font_size=font_size)
            
            # If this is the round wind player, highlight all three labels
            if player.wind == self.game.round_wind:
                for label in [rank_label, name_label, points_label]:
                    with label.canvas.before:
                        Color(*K_PRIMARY)
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
        for child in self.scoreboard.children:
            if isinstance(child, Label):
                child.font_size = font_config.font_size_medium
    

    def go_to_add_points(self, instance):
        self.manager.current = 'add_points'
