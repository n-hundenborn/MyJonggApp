from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.properties import ObjectProperty, NumericProperty
from backend.game import Game, Wind
from backend.helper_functions import setup_logger
from frontend.screens.config import get_font_size, FONT_SIZE_RATIO_MEDIUM, FONT_SIZE_RATIO_SMALL, ACCENT_COLOR
from kivy.graphics import Color, Rectangle

# Configure logger
logger = setup_logger(__name__)

class AddPointsScreen(Screen):
    """A screen for adding points to players."""
    game: Game = ObjectProperty(None)
    current_round_number = NumericProperty(0)

    def __init__(self, **kwargs):
        """Initialize the AddPointsScreen."""
        super().__init__(**kwargs)
        self.player_inputs = {}
        self.winner_selection = None
        self.calculated_points_labels = {}

    def on_enter(self):
        self.current_round_number = self.game.current_round_number
        self.ids.players_layout.clear_widgets()
        self.player_inputs = {}
        self.winner_selection = None
        
        font_size = get_font_size(FONT_SIZE_RATIO_MEDIUM)

        for player in self.game.players:
            player_layout = BoxLayout()
            
            # Add background color for round wind player
            if player.wind == self.game.round_wind:
                with player_layout.canvas.before:
                    Color(*ACCENT_COLOR)
                    self.rect = Rectangle(pos=player_layout.pos, size=player_layout.size)
                player_layout.bind(pos=self._update_rect, size=self._update_rect)

            player_label = Label(
                text=f"{player.show()}:",
                font_size=get_font_size(FONT_SIZE_RATIO_SMALL)
            )
            
            # Player points input
            points_input = TextInput(
                input_filter='int',
                multiline=False,
                write_tab=False,
                hint_text='0',
                foreground_color=(0, 0, 0, 1),
                hint_text_color=(0.5, 0.5, 0.5, 1),
                font_size=font_size,
                halign='right'
            )
            points_input.bind(focus=self.on_focus, on_text_validate=self.on_text_validate)
            
            # Times doubled input
            times_doubled_input = TextInput(
                input_filter='int',
                multiline=False,
                write_tab=False,
                hint_text='0',
                foreground_color=(0, 0, 0, 1),
                hint_text_color=(0.5, 0.5, 0.5, 1),
                font_size=font_size,
                halign='right'
            )
            times_doubled_input.bind(focus=self.on_focus, on_text_validate=self.on_text_validate)
            
            # Use Wind instance as key
            self.player_inputs[player.wind] = (points_input, times_doubled_input)
            player_layout.add_widget(player_label)
            player_layout.add_widget(points_input)
            player_layout.add_widget(times_doubled_input)
            
            # Add winner checkbox
            winner_checkbox = CheckBox(group='winner')
            winner_checkbox.bind(active=lambda instance, value, player_wind=player.wind: self.on_winner_selected(player_wind, value))
            player_layout.add_widget(winner_checkbox)
            
            self.ids.players_layout.add_widget(player_layout)

    def update_fonts(self):
        """Update all font sizes when window is resized"""
        font_size = get_font_size(FONT_SIZE_RATIO_MEDIUM)
        font_size_small = get_font_size(FONT_SIZE_RATIO_SMALL)
        for wind, (points_input, times_doubled_input) in self.player_inputs.items():
            points_input.font_size = font_size
            times_doubled_input.font_size = font_size
        
        # Update labels with smaller font size
        for child in self.ids.players_layout.children:
            if isinstance(child, BoxLayout):
                for widget in child.children:
                    if isinstance(widget, Label):
                        widget.font_size = font_size_small

    def on_focus(self, instance, value):
        """
        Handle focus events for TextInput widgets.
        Args:
            instance: The TextInput widget that triggered the focus event
            value: Boolean indicating focus state (True = gained focus, False = lost focus)
        """
        # Only clear if the current value is '0' or empty
        if value and (instance.text == '0' or instance.text == ''):
            instance.text = ''
        elif not instance.text:
            instance.text = '0'

    def on_text_validate(self, instance):
        current_key = next((wind for wind, (input, _) in self.player_inputs.items() if input == instance), None)
        if current_key:
            keys = list(self.player_inputs.keys())
            current_index = keys.index(current_key)
            if current_index < len(keys) - 1:
                next_key = keys[current_index + 1]
                self.player_inputs[next_key][0].focus = True
            else:
                self.submit_points()

    def on_winner_selected(self, player_wind: Wind, value: bool) -> None:
        if value:
            self.winner_selection = player_wind

    def submit_points(self):
        winner_wind = self.winner_selection

        # Check if a winner has been selected
        if winner_wind is None:
            # Display an error message or handle the error as needed
            logger.error("Error: Please select a winner before submitting.")
            return  # Prevent submission if no winner is selected

        # Create a dictionary to store points for each player
        points = {}
        for wind, (points_input, times_doubled_input) in self.player_inputs.items():
            # Convert input text to integer values, defaulting to 0 if empty
            points_value = int(points_input.text) if points_input.text else 0
            times_doubled = int(times_doubled_input.text) if times_doubled_input.text else 0
            points[wind] = (points_value, times_doubled)
        
        # Process the points immediately
        self.game.process_points_input(points, winner_wind)
        
        # Navigate to summary screen
        self.manager.current = 'round_summary'

    def _update_rect(self, instance, value):
        """Update the rectangle position and size when the layout changes."""
        self.rect.pos = instance.pos
        self.rect.size = instance.size
