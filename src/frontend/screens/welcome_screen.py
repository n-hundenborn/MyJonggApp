from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty
from backend.game import Game
from datetime import datetime
import os
import sys
from tkinter import filedialog
import tkinter as tk
from pathlib import Path

class WelcomeScreen(Screen):
    """Welcome screen for selecting game folder before starting a new game."""
    game: Game = ObjectProperty(None)
    folder_info = StringProperty("Kein Ordner ausgewählt")
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
            # Shorten the path if it's too long
            path = str(self.game.game_folder)
            if len(path) > 70:  # Adjust this number based on your needs
                # Keep the first part and last part, with ... in between
                parts = self.game.game_folder.parts
                if len(parts) > 4:
                    shortened = str(self.game.game_folder.parts[0]) + os.sep + '...' + os.sep + os.sep.join(parts[-2:])
                else:
                    shortened = path
            else:
                shortened = path
            self.folder_info = f"Rundenordner:\n{shortened}"
            self.can_proceed = True
        else:
            self.folder_info = "Kein Ordner ausgewählt"
            self.can_proceed = False

    def get_default_folder_name(self) -> str:
        """Generate default folder name in format mahjongg-YYYY-MM-DD."""
        return f"mahjongg-{datetime.now().strftime('%Y-%m-%d')}"

    def get_program_directory(self) -> str:
        """Get the directory where the program is located."""
        if hasattr(sys, '_MEIPASS'):
            # Running as PyInstaller bundle, use the directory of the executable
            return os.path.dirname(sys.executable)
        else:
            # Running as script, use current working directory
            return os.getcwd()
    
    def select_folder(self):
        """Open folder picker dialog to select/create game folder."""
        # Determine starting directory with priority:
        # 1. Previous game folder (if exists)
        # 2. Program directory
        start_dir = self.get_program_directory()
        
        if self.game and self.game.game_folder and self.game.game_folder.exists():
            start_dir = str(self.game.game_folder)
        
        try:
            # Create a hidden root window for the dialog
            root = tk.Tk()
            root.withdraw()  # Hide the root window
            root.attributes('-topmost', True)  # Bring dialog to front
            
            selected_folder = filedialog.askdirectory(
                title="Spielordner auswählen oder erstellen",
                initialdir=start_dir
            )
            
            root.destroy()  # Clean up the root window
            
            if selected_folder:
                print(f"Selected folder: {selected_folder}")
                self.set_game_folder(selected_folder)
                print(f"Can proceed: {self.can_proceed}")
            else:
                # User cancelled, stay on welcome screen
                print("User cancelled folder selection")
                
        except Exception as e:
            print(f"Error selecting folder: {e}")
            # Stay on welcome screen if there's an error

    def use_default_folder(self):
        """Set default folder path (folder will be created when proceeding)."""
        default_name = self.get_default_folder_name()
        default_path = os.path.join(self.get_program_directory(), default_name)
        
        print(f"Selected default folder: {default_path}")
        # Just set the path, don't create the folder yet
        self.set_game_folder(default_path)
        print(f"Can proceed: {self.can_proceed}")

    def set_game_folder(self, folder_path: str | Path):
        """Set the game folder and update display."""
        if self.game:
            self.game.set_game_folder(folder_path)
        self.update_folder_info()

    def proceed_to_start_screen(self):
        """Proceed to start screen. Creates folder if it doesn't exist yet."""
        if not self.game or not self.game.game_folder:
            print("No folder selected")

        folder_path = str(self.game.game_folder)
        # Create folder if it doesn't exist
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Created folder: {folder_path}")
        
        self.manager.current = 'start'

    def update_fonts(self):
        """Update all font sizes when window is resized."""
        # This will be called by the main app when window is resized
        pass
