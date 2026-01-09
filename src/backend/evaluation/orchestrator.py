from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from backend.evaluation.excel_loader import get_dataframes_from_folder
from backend.evaluation.visualization import create_html_dashboard

def start_evaluation(folder_path: Path) -> tuple[Path, dict]:
    """
    Start the evaluation process for the given folder.
    
    Returns:
        tuple[Path, dict]: (html_file_path, loading_info)
        where loading_info contains {'loaded': [filenames], 'failed': [filenames]}
    
    Raises:
        ValueError: If no valid Excel files are found in the folder
    """

    df_rounds, df_games, df_points, loading_info = get_dataframes_from_folder(folder_path)
    
    # Check if any valid data was loaded
    if df_rounds.empty or not loading_info['loaded']:
        raise ValueError("Keine gültigen Excel-Dateien im Ordner")
    
    html_file = create_html_dashboard(df_rounds, df_games, df_points, folder_path)
    
    return html_file, loading_info