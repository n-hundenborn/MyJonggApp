from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
import pandas as pd
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, NumericProperty
from frontend.screens.config import font_config

class StatsScreen(Screen):
    game_data = ObjectProperty(None, force_dispatch=True)
    current_page = NumericProperty(0)
    total_pages = NumericProperty(3)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.displays = [
            self.create_points_over_time_display,
            self.create_final_standings_display,
            self.create_wins_distribution_display
        ]

    def create_points_over_time_display(self):
        return Label(
            text="Punkteverlauf über Zeit\n\nHier könnte ihre Statistik stehen!",
            font_size=font_config.font_size_medium
        )

    def create_final_standings_display(self):
        final_round = self.game_data['round'].max()
        final_scores = self.game_data[self.game_data['round'] == final_round].sort_values('running_sum', ascending=False)
        
        text = "Endstand:\n\n"
        for i, (_, row) in enumerate(final_scores.iterrows(), 1):
            text += f"{i}. {row['player']}: {int(row['running_sum'])} Punkte\n"
            
        return Label(
            text=text,
            font_size=font_config.font_size_medium
        )

    def create_wins_distribution_display(self):
        # Get unique rounds and their winners, then count them
        wins = self.game_data.drop_duplicates('round')['winner'].value_counts()
        
        text = "Gewonnene Runden:\n\n"
        for player, count in wins.items():
            text += f"{player}: {int(count)} Runden\n"
            
        return Label(
            text=text,
            font_size=font_config.font_size_medium
        )

    def on_enter(self, *args):
        """Called when the screen is entered"""
        self.update_stats()

    def update_stats(self):
        self.ids.stats_container.clear_widgets()
        
        # Create and add the current display
        display = self.displays[self.current_page]()
        self.ids.stats_container.add_widget(display)

        # Add navigation buttons
        nav_layout = BoxLayout(
            orientation='horizontal',
            spacing=10,
            size_hint_y=0.1
        )
        
        prev_button = Button(
            text="Vorherige",
            font_size=font_config.font_size_medium,
            disabled=self.current_page == 0,
            on_release=self.previous_page
        )
        
        page_label = Label(
            text=f"{self.current_page + 1}/{self.total_pages}",
            font_size=font_config.font_size_medium,
            size_hint_x=0.5
        )
        
        next_button = Button(
            text="Nächste",
            font_size=font_config.font_size_medium,
            disabled=self.current_page == self.total_pages - 1,
            on_release=self.next_page
        )
        
        nav_layout.add_widget(prev_button)
        nav_layout.add_widget(page_label)
        nav_layout.add_widget(next_button)
        
        self.ids.stats_container.add_widget(nav_layout)

    def next_page(self, *args):
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.update_stats()

    def previous_page(self, *args):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_stats()

    def update_data(self, game_data: pd.DataFrame):
        self.game_data = game_data

    def update_fonts(self):
        """Update all font sizes when window is resized"""
        # Update all children in stats_container
        if hasattr(self, 'ids') and hasattr(self.ids, 'stats_container'):
            for child in self.ids.stats_container.children:
                if isinstance(child, Label):
                    child.font_size = font_config.font_size_medium
                elif isinstance(child, Button):
                    child.font_size = font_config.font_size_medium
                elif isinstance(child, BoxLayout):
                    # Handle navigation buttons layout
                    for nav_child in child.children:
                        if isinstance(nav_child, (Label, Button)):
                            nav_child.font_size = font_config.font_size_medium

