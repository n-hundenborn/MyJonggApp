import pandas as pd
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from backend.evaluation.excel_loader import get_dataframes_from_folder
from backend.evaluation.visualization import create_interactive_html_dashboard

DEBUG = True

def start_evaluation(folder_path: Path) -> Path:
    """Start the evaluation process for the given folder."""

    df_rounds, df_games, df_points = get_dataframes_from_folder(folder_path)
    
    html_file = create_interactive_html_dashboard(df_rounds, df_games, df_points, folder_path)
    
    return html_file