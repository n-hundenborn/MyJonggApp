import pandas as pd
from pathlib import Path
from backend.helper_functions import setup_logger

from backend.evaluation.transformations import prepare_round_data

logger = setup_logger(__name__)

def get_dataframes_from_file(file_path: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame] | None:
    """
    Load and transform data from a single Excel file.
    
    Returns:
        tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]: (df_rounds, df_games_meta, df_points)
        or None if loading fails
    """
    filename = file_path.stem
    logger.debug(f"Loading data from file: {filename}")
    try:
        df_metadata = pd.read_excel(file_path, sheet_name=0, engine='openpyxl')
        df_games = pd.read_excel(file_path, sheet_name=1, engine='openpyxl')
        df_standings = pd.read_excel(file_path, sheet_name=2, engine='openpyxl')
    except Exception as e:
        logger.error(f"Error loading {filename}: {e}")
        return None
    
    return prepare_round_data(filename, df_metadata, df_games, df_standings)


def get_dataframes_from_folder(folder_path: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Load and combine data from all Excel files in a folder.
    
    Returns:
        tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]: (df_rounds, df_games_meta, df_points)
        Three DataFrames with different granularities according to data structure.
    """
    all_rounds = []
    all_games = []
    all_points = []
    
    for file in folder_path.glob("*.xls*"):
        result = get_dataframes_from_file(file)
        if result is not None:
            df_rounds, df_games_meta, df_points = result
            if not df_rounds.empty:
                all_rounds.append(df_rounds)
                all_games.append(df_games_meta)
                all_points.append(df_points)

    logger.info(f"Loaded {len(all_rounds)} rounds from folder {folder_path}")
    
    df_rounds = pd.concat(all_rounds, ignore_index=True) if all_rounds else pd.DataFrame()
    df_games = pd.concat(all_games, ignore_index=True) if all_games else pd.DataFrame()
    df_points = pd.concat(all_points, ignore_index=True) if all_points else pd.DataFrame()
    
    return df_rounds, df_games, df_points

