from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.properties import ObjectProperty
from backend.game import Game, Wind
from logging import getLogger, DEBUG
import logging

# Configure the default logger to save logs to a file
logging.basicConfig(
    level=DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename='app.log',  # Specify the log file name
    filemode='w'  # Overwrite the log file each time the program runs
)

logger = getLogger(__name__)
logger.setLevel(DEBUG)


class AddPointsScreen(Screen):
    """A screen for adding points to players."""
    game: Game = ObjectProperty(None)

    def __init__(self, **kwargs):
        """Initialize the AddPointsScreen."""
        super().__init__(**kwargs)
        self.player_inputs = {}
        self.winner_selection = None

    def on_enter(self):
        self.ids.players_layout.clear_widgets()  # Clear previous widgets
        self.player_inputs = {}
        self.winner_selection = None  # Reset winner selection when entering the screen

        for player in self.game.players:
            player_layout = BoxLayout()
            player_label = Label(text=f"{player.show()}:")
            
            # Player points input
            points_input = TextInput(
                input_filter='int',
                multiline=False,
                write_tab=False,
                hint_text='0',
                foreground_color=(0, 0, 0, 1),
                hint_text_color=(0.5, 0.5, 0.5, 1)
            )
            points_input.bind(focus=self.on_focus, on_text_validate=self.on_text_validate)
            
            # Times doubled input
            times_doubled_input = TextInput(
                input_filter='int',
                multiline=False,
                write_tab=False,
                hint_text='0',
                foreground_color=(0, 0, 0, 1),
                hint_text_color=(0.5, 0.5, 0.5, 1)
            )
            times_doubled_input.bind(focus=self.on_focus, on_text_validate=self.on_text_validate)
            
            # Use Wind instance as key
            self.player_inputs[player.wind] = (points_input, times_doubled_input)
            player_layout.add_widget(player_label)
            player_layout.add_widget(points_input)
            player_layout.add_widget(times_doubled_input)
            
            # Bind the player wind directly to the checkbox
            winner_checkbox = CheckBox(group='winner')
            winner_checkbox.bind(active=lambda instance, value, player_wind=player.wind: self.on_winner_selected(player_wind, value))
            player_layout.add_widget(winner_checkbox)
            
            self.ids.players_layout.add_widget(player_layout)  # Add to the layout defined in the kv file

    def on_focus(self, instance, value):
        if value:
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
        self.game.process_points_input(points, winner_wind)
        
        if self.game.is_game_over(winner_wind):
            self.manager.current = 'game_over'
        else:
            self.game.start_new_round(winner_wind)
            self.manager.current = 'scoreboard'
