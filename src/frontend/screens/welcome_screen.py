from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty
from backend.game import Game
from datetime import datetime
import os
from plyer import filechooser

class WelcomeScreen(Screen):
    """Welcome screen for selecting game folder before starting a new game."""
    game: Game = ObjectProperty(None)
    folder_info = StringProperty("Kein Ordner ausgewählt")
    last_used_folder = StringProperty("")
    can_proceed = ObjectProperty(False)

    def __init__(self, **kwargs):
        """Initialize the WelcomeScreen."""
        super().__init__(**kwargs)

    def on_enter(self):
        """Called when entering the screen."""
        # Update folder info display
        self.update_folder_info()

    def update_folder_info(self):
        """Update the folder info display."""
        if self.game and self.game.game_folder:
            self.folder_info = f"Spielordner: {self.game.game_folder}"
            self.can_proceed = True
        else:
            self.folder_info = "Kein Ordner ausgewählt"
            self.can_proceed = False

    def get_default_folder_name(self) -> str:
        """Generate default folder name in format mahjongg-YYYY-MM-DD."""
        return f"mahjongg-{datetime.now().strftime('%Y-%m-%d')}"

    def select_folder(self):
        """Open folder picker dialog to select/create game folder."""
        # Use last used folder as starting directory if available
        start_dir = self.last_used_folder if self.last_used_folder else os.getcwd()
        
        try:
            selected_folder = filechooser.choose_dir(
                title="Spielordner auswählen oder erstellen",
                path=start_dir
            )
            
            if selected_folder and len(selected_folder) > 0:
                folder_path = selected_folder[0]
                self.set_game_folder(folder_path)
                self.last_used_folder = folder_path
            else:
                # User cancelled, stay on welcome screen
                print("User cancelled folder selection")
                
        except Exception as e:
            print(f"Error selecting folder: {e}")
            # Stay on welcome screen if there's an error

    def use_default_folder(self):
        """Create and use default folder in current directory."""
        default_name = self.get_default_folder_name()
        default_path = os.path.join(os.getcwd(), default_name)
        
        try:
            # Create folder if it doesn't exist
            if not os.path.exists(default_path):
                os.makedirs(default_path)
            
            print(f"Using default folder: {default_path}")
            self.set_game_folder(default_path)
            self.last_used_folder = default_path
            print(f"Can proceed: {self.can_proceed}")
            
        except Exception as e:
            print(f"Error creating default folder: {e}")

    def set_game_folder(self, folder_path: str):
        """Set the game folder and update display."""
        if self.game:
            self.game.set_game_folder(folder_path)
        self.update_folder_info()

    def proceed_to_start_screen(self):
        """Proceed to start screen if folder is selected."""
        if self.game and self.game.game_folder:
            self.manager.current = 'start'
        else:
            # This shouldn't happen as buttons should be disabled, but just in case
            print("No folder selected")

    def update_fonts(self):
        """Update all font sizes when window is resized."""
        # This will be called by the main app when window is resized
        pass
