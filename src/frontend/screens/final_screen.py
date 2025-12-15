from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
import pandas as pd
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from frontend.shared.styles import font_config
import subprocess
import os

class FinalScreen(Screen):
    game_data = ObjectProperty(None, force_dispatch=True)
    game = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_enter(self, *args):
        """Called when the screen is entered"""
        self.update_display()

    def update_display(self):
        """Display final game statistics"""
        self.ids.final_container.clear_widgets()
        
        if self.game_data is None or len(self.game_data) == 0:
            self.ids.final_container.add_widget(Label(
                text="Keine Statistiken verfügbar",
                font_size=font_config.font_size_medium
            ))
            return
        
        # Get final standings
        final_round = self.game_data['round'].max()
        final_scores = self.game_data[self.game_data['round'] == final_round].sort_values('rank')
        
        # Create header
        header = Label(
            text="Endstand",
            font_size=font_config.font_size_big,
            bold=True,
            size_hint_y=0.15
        )
        self.ids.final_container.add_widget(header)
        
        # Create standings display
        standings_text = ""
        for _, row in final_scores.iterrows():
            points_formatted = f"{int(row['running_sum']):,}".replace(",", ".")
            standings_text += f"{int(row['rank'])}. [{row['wind']}] {row['player']}: {points_formatted} Punkte\n"
        
        standings_label = Label(
            text=standings_text,
            font_size=font_config.font_size_medium,
            halign='center',
            valign='middle'
        )
        self.ids.final_container.add_widget(standings_label)
        
        # Add wins distribution
        wins = self.game_data.drop_duplicates('round')['winner'].value_counts()
        wins_text = "\n\nGewonnene Spiele:\n"
        for wind, count in wins.items():
            wins_text += f"{wind}: {int(count)}\n"
        
        wins_label = Label(
            text=wins_text,
            font_size=font_config.font_size_medium,
            halign='center',
            valign='middle'
        )
        self.ids.final_container.add_widget(wins_label)
    
    def open_game_folder(self):
        """Open the game folder in the system file explorer"""
        if self.game and self.game.game_folder:
            folder_path = self.game.game_folder
            if folder_path.exists():
                if os.name == 'nt':  # Windows
                    subprocess.Popen(['explorer', str(folder_path)])
                elif os.name == 'posix':  # macOS and Linux
                    if os.uname().sysname == 'Darwin':  # macOS
                        subprocess.Popen(['open', str(folder_path)])
                    else:  # Linux
                        subprocess.Popen(['xdg-open', str(folder_path)])
    
    def start_new_game(self):
        """Reset the game and navigate to welcome screen"""
        if self.game:
            self.game.reset_game()
            self.manager.current = 'welcome'

    def update_data(self, game_data: pd.DataFrame):
        self.game_data = game_data

    def update_fonts(self):
        """Update all font sizes when window is resized"""
        # Update all children in final_container
        if hasattr(self, 'ids') and hasattr(self.ids, 'final_container'):
            for child in self.ids.final_container.children:
                if isinstance(child, Label):
                    # Header gets big font, others get medium font
                    if hasattr(child, 'bold') and child.bold:
                        child.font_size = font_config.font_size_big
                    else:
                        child.font_size = font_config.font_size_medium


