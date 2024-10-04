from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty
from backend.game import Wind, Game

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
        for wind in list(Wind):
            player_layout = BoxLayout()
            player_layout.add_widget(Label(text=str(wind)))
            player_input = TextInput(multiline=False, write_tab=False)
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
        self.game.set_players([input.text for input in self.player_inputs])
        self.manager.current = 'scoreboard'