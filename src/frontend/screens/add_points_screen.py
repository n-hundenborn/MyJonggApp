from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.properties import ObjectProperty, NumericProperty
from backend.game import Game, Wind
from backend.helper_functions import setup_logger
from frontend.screens.config import get_font_size, FONT_SIZE_RATIO_MEDIUM, FONT_SIZE_RATIO_SMALL, ACCENT_COLOR, HIGHLIGHT_COLOR, font_config
from kivy.graphics import Color, Rectangle
from kivy.animation import Animation
from frontend.components.popups import show_error

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
        self.rect = None

    def on_enter(self):
        self.current_round_number = self.game.current_round_number
        self.ids.players_layout.clear_widgets()
        self.player_inputs = {}
        self.winner_selection = None

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
                font_size=font_config.font_size_medium
            )
            
            # Player points input
            points_input = TextInput(
                input_filter='int',
                multiline=False,
                write_tab=False,
                hint_text='0',
                foreground_color=(0, 0, 0, 1),
                hint_text_color=(0.5, 0.5, 0.5, 1),
                font_size=font_config.font_size_medium,
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
                font_size=font_config.font_size_medium,
                halign='right'
            )
            times_doubled_input.bind(focus=self.on_focus, on_text_validate=self.on_text_validate)
            
            # Use Wind instance as key
            self.player_inputs[player.wind] = (points_input, times_doubled_input)
            player_layout.add_widget(player_label)
            player_layout.add_widget(points_input)
            player_layout.add_widget(times_doubled_input)
            
            # Add winner checkbox with background for flashing
            checkbox_container = BoxLayout()
            with checkbox_container.canvas.before:
                Color(0, 0, 0, 0)  # Start transparent
                checkbox_container.rect = Rectangle(pos=checkbox_container.pos, size=checkbox_container.size)
            checkbox_container.bind(pos=lambda obj, pos: setattr(obj.rect, 'pos', pos),
                                 size=lambda obj, size: setattr(obj.rect, 'size', size))
            
            winner_checkbox = CheckBox(group='winner')
            winner_checkbox.bind(active=lambda instance, value, player_wind=player.wind: self.on_winner_selected(player_wind, value))
            checkbox_container.add_widget(winner_checkbox)
            player_layout.add_widget(checkbox_container)
            
            self.ids.players_layout.add_widget(player_layout)

    def update_fonts(self):
        """Update all font sizes when window is resized"""
        for wind, (points_input, times_doubled_input) in self.player_inputs.items():
            points_input.font_size = font_config.font_size_medium
            times_doubled_input.font_size = font_config.font_size_medium
        
        for child in self.ids.players_layout.children:
            if isinstance(child, BoxLayout):
                for widget in child.children:
                    if isinstance(widget, Label):
                        widget.font_size = font_config.font_size_medium

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
        else:
            # Clear winner selection when checkbox is unchecked
            self.winner_selection = None

    def submit_points(self):
        winner_wind = self.winner_selection

        # Check if a winner has been selected with animation feedback
        if winner_wind is None:
            for child in self.ids.players_layout.children:
                if isinstance(child, BoxLayout):
                    checkbox_container = next((w for w in child.children if isinstance(w, BoxLayout)), None)
                    if checkbox_container and hasattr(checkbox_container, 'rect'):
                        # Flash animation with HIGHLIGHT_COLOR
                        anim = (
                            Animation(rgba=(*HIGHLIGHT_COLOR[:3], 0.8), duration=0.2) +
                            Animation(rgba=(0, 0, 0, 0), duration=0.2) +
                            Animation(rgba=(*HIGHLIGHT_COLOR[:3], 0.8), duration=0.2) +
                            Animation(rgba=(0, 0, 0, 0), duration=0.2)
                        )
                        anim.start(checkbox_container.canvas.before.children[0])
            
            show_error("Bitte wählen Sie einen Gewinner aus.")
            return

        # Create a dictionary to store points for each player
        points = {}
        for wind, (points_input, times_doubled_input) in self.player_inputs.items():
            try:
                points_value = int(points_input.text) if points_input.text else 0
                times_doubled = int(times_doubled_input.text) if times_doubled_input.text else 0
                
                # Calculate the final value to check if it's too large
                calculated_value = points_value * (2 ** times_doubled)
                
                # Check if the calculated value is too large
                if calculated_value > 999999999:  # 1 billion - 1
                    show_error("Die berechneten Punkte sind zu groß. Bitte reduzieren Sie die Punkte oder die Verdoppelungen.")
                    return
                    
                points[wind] = (points_value, times_doubled)
            except (OverflowError, ValueError):
                show_error("Fehler: Die eingegebene Zahl ist zu groß oder ungültig.")
                return
        
        # Process the points immediately
        self.game.process_points_input(points, winner_wind)
        
        # Navigate to summary screen
        self.manager.current = 'round_summary'

    def _update_rect(self, instance, value):
        """Update the rectangle position and size when the layout changes."""
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def update_round_wind(self):
        """Update the display when the round wind changes."""
        if hasattr(self, 'ids') and hasattr(self.ids, 'players_layout'):
            self.ids.players_layout.clear_widgets()
            self.on_enter()
