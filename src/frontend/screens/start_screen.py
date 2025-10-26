from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty
from backend.game import Wind, Game
from frontend.screens.config import IDIOT_NAMES
from frontend.screens.styles import font_config
from random import sample

class StartScreen(Screen):
    """A screen for entering player names and starting the game."""
    game: Game = ObjectProperty(None)

    def __init__(self, **kwargs):
        """Initialize the StartScreen.
        Creates a layout with input fields for player names and a start button."""
        super().__init__(**kwargs)

        # Populate player inputs dynamically
        player_inputs_container = self.ids.player_inputs_container
        self.player_inputs = []  # Initialize the list to hold player inputs
        
        font_size = font_config.font_size_big
        
        for wind in list(Wind):
            player_layout = BoxLayout()
            player_layout.add_widget(Label(
                text=str(wind),
                font_size=font_size,
                height=font_size * 2.5,  # Match TextInput height
                size_hint_y=None,  # Disable vertical size hint
                valign='middle',  # Vertical center alignment
                text_size=(None, font_size * 2.5)  # Enable text vertical alignment
            ))
            player_input = TextInput(
                multiline=False,
                write_tab=False,
                font_size=font_size,
                halign='left',
                padding_y=(font_size/2, font_size/2),
                height=font_size * 2.5,
                size_hint_y=None,
            )
            player_input.bind(on_text_validate=self.on_text_validate)
            self.player_inputs.append(player_input)
            player_layout.add_widget(player_input)
            player_inputs_container.add_widget(player_layout)

    def on_text_validate(self, instance):
        """Handle the 'Enter' key press in text input fields."""        
        index = self.player_inputs.index(instance)
        if index < len(self.player_inputs) - 1:
            self.player_inputs[index + 1].focus = True
        else:
            self.start_game(instance)

    def start_game(self, instance):
        """Start the game with the entered player names."""
        
        # Count empty inputs to determine how many random names we need
        empty_inputs = sum(1 for input in self.player_inputs if not input.text.strip())
        # Get random unique names for empty inputs
        random_names = sample(IDIOT_NAMES, min(empty_inputs, len(IDIOT_NAMES)))
        random_names_iter = iter(random_names)
        
        player_names = []
        for input in self.player_inputs:
            name = input.text.strip()
            if not name:
                try:
                    name = next(random_names_iter)
                except StopIteration:
                    name = f"Spieler {len(player_names) + 1}"
            player_names.append(name)
        
        self.game.set_players(player_names)
        self.game.start_game()
        self.manager.current = 'add_points'

    def update_fonts(self):
        """Update all font sizes when window is resized"""
        # Update TextInputs and Labels
        for i, input in enumerate(self.player_inputs):
            input.font_size = font_config.font_size_medium
            # Update the corresponding label in the same layout
            player_layout = input.parent
            if player_layout and len(player_layout.children) > 1:
                label = player_layout.children[1]  # Label is typically the first child (shown last due to Kivy ordering)
                if hasattr(label, 'font_size'):
                    label.font_size = font_config.font_size_big