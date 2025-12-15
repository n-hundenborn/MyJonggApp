from logging import getLogger
import pandas as pd
import os
from pathlib import Path


def create_metadata_dataframe(game) -> pd.DataFrame:
    """Create a metadata DataFrame with game timing information.
    
    Args:
        game: Game object containing start_time and end_time
        
    Returns:
        DataFrame with game metadata in Plotly-friendly format
    """
    if game.start_time is None or game.end_time is None:
        # Return empty DataFrame if times not set
        return pd.DataFrame({
            'Spielstart': [None],
            'Spielende': [None],
            'Dauer (Sekunden)': [None],
            'Dauer (formatiert)': [None]
        })
    
    # Calculate duration
    duration = game.end_time - game.start_time
    duration_seconds = int(duration.total_seconds())
    
    # Format duration as human-readable string
    hours = duration_seconds // 3600
    minutes = (duration_seconds % 3600) // 60
    seconds = duration_seconds % 60
    duration_formatted = f"{hours}h {minutes}m {seconds}s"
    
    # Create DataFrame with ISO 8601 formatted timestamps
    metadata = {
        'Spielstart': [game.start_time.isoformat()],
        'Spielende': [game.end_time.isoformat()],
        'Dauer (Sekunden)': [duration_seconds],
        'Dauer (formatiert)': [duration_formatted]
    }
    
    return pd.DataFrame(metadata)


def prepare_dataframes_for_saving(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Saves game data to an Excel file with German column names.
    
    Args:
        df: DataFrame containing round-by-round data
        filename: Name of the file to save the data to
        
    Returns:
        str: Path to the created Excel file
    """
    # Create standings DataFrame from the last round
    last_round = df['round'].max()
    df_standings = df[df['round'] == last_round][
        ['wind', 'player', 'running_sum', 'rank']
    ].sort_values('rank')
    
    # Define column name mappings
    rounds_columns = {
        'round': 'Runde',
        'round_wind': 'Wind der Runde',
        'winner': 'Gewinner',
        'player': 'Spieler',
        'wind': 'Wind',
        'base_points': 'Basispunkte',
        'doublings': 'Verdopplungen',
        'calculated_points': 'Rundenpunkte',
        'net_points': 'Punkteänderung',
        'running_sum': 'Laufende Summe',
        'rank': 'Rang'
    }
    
    standings_columns = {
        'wind': 'Wind',
        'player': 'Spieler',
        'running_sum': 'Laufende Summe',
        'rank': 'Rang'
    }
    
    # Create copies with German column names for Excel
    df_rounds_german = df.copy()
    df_rounds_german.rename(columns=rounds_columns, inplace=True)
    
    df_standings_german = df_standings.copy()
    df_standings_german.rename(columns=standings_columns, inplace=True)
    
    return df_rounds_german, df_standings_german


def save_dataframes_to_excel(df_rounds: pd.DataFrame, df_standings: pd.DataFrame, filename: str, folder_path: str | Path = None, game=None) -> str:
    filename = filename + ".xlsx"
    
    # Use folder_path if provided, otherwise save in current directory
    if folder_path:
        folder_path = Path(folder_path) if isinstance(folder_path, str) else folder_path
        full_path = folder_path / filename
    else:
        full_path = Path(filename)
    
    with pd.ExcelWriter(full_path, engine='openpyxl') as writer:
        # Add metadata sheet first if game object is provided
        if game is not None:
            df_metadata = create_metadata_dataframe(game)
            df_metadata.to_excel(writer, sheet_name='Spielinfo', index=False)
            
            # Adjust column widths for Spielinfo sheet
            worksheet = writer.sheets['Spielinfo']
            for col in 'ABCD':
                worksheet.column_dimensions[col].width = 25
        
        df_rounds.to_excel(writer, sheet_name='Runden', index=False)
        df_standings.to_excel(writer, sheet_name='Endstand', index=False)
        
        # Adjust column widths for Runden sheet
        worksheet = writer.sheets['Runden']
        for col in 'ABCDEFGHIJK':
            worksheet.column_dimensions[col].width = 18

        # Adjust column widths for Endstand sheet
        worksheet = writer.sheets['Endstand']
        for col in 'ABCD':
            worksheet.column_dimensions[col].width = 18
    
    logger = getLogger(__name__)
    logger.info(f"Game results saved to {full_path}")
    
    return str(full_path)

