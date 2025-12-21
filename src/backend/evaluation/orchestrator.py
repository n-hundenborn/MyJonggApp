import pandas as pd
from pathlib import Path

from backend.evaluation.excel_loader import get_dataframes_from_folder
from backend.evaluation.visualization import create_html_dashboard

DEBUG = True

def start_evaluation(folder_path: Path) -> Path:
    """Start the evaluation process for the given folder."""

    df_rounds, df_games, df_points = get_dataframes_from_folder(folder_path)
    
    # TODO: Update to use new create_interactive_html_dashboard with 3 DataFrames
    # For now, merge back to single DataFrame for compatibility

    
    html_file = create_html_dashboard(df, folder_path)
    
    return html_file