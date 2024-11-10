import logging
from logging import getLogger, DEBUG
import pandas as pd

def setup_logger(logger_name: str, file_name: str = 'app.log', verbose: bool = True) -> logging.Logger:
    """Configure and return a logger that saves logs to a file.
    
    Args:
        logger_name: Name of the logger to create
        verbose: If True, includes timestamp and metadata. If False, logs only the message
        
    Returns:
        Configured logger instance
    """
    logger = getLogger(logger_name)
    logger.setLevel(DEBUG)

    # Create a file handler which logs even debug messages, overwriting old logs
    file_handler = logging.FileHandler(file_name, mode='w', encoding='utf-8')
    file_handler.setLevel(DEBUG)

    # Create console handler for simple logging
    console_handler = logging.StreamHandler()
    console_handler.setLevel(DEBUG)

    # Choose format based on verbose flag
    if verbose:
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    else:
        formatter = logging.Formatter('%(message)s')

    # Apply formatters to handlers
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

def calculate_ranks(items, key_func=lambda x: x.points):
    """Calculate ranks for items, handling ties correctly (1,2,2,4).
    
    Args:
        items: Sequence of items to be ranked
        key_func: Function to extract the value to rank by (default: x.points)
    
    Returns:
        Dictionary mapping items to their ranks
    """
    # Create mapping of values to items
    value_to_items = {}
    for item in items:
        value = key_func(item)
        value_to_items.setdefault(value, []).append(item)
    
    # Sort unique values in descending order
    sorted_values = sorted(value_to_items.keys(), reverse=True)
    
    # Create rank mapping
    rank_map = {}
    current_rank = 1
    for value in sorted_values:
        # All items with same value get same rank
        items_at_this_value = value_to_items[value]
        for item in items_at_this_value:
            rank_map[item] = current_rank
        # Skip ranks based on how many items were tied
        current_rank += len(items_at_this_value)
    
    return rank_map

def save_dataframes_to_excel(df: pd.DataFrame, filename: str) -> str:
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
    
    # Save both sheets to Excel with adjusted column widths
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        df_rounds_german.to_excel(writer, sheet_name='Runden', index=False)
        df_standings_german.to_excel(writer, sheet_name='Endstand', index=False)
        
        # Adjust column widths for Runden sheet
        worksheet = writer.sheets['Runden']
        for col in 'ABCDEFGHIJK':  # Added one more column
            worksheet.column_dimensions[col].width = 18

        # Adjust column widths for Endstand sheet
        worksheet = writer.sheets['Endstand']
        for col in 'ABCD':
            worksheet.column_dimensions[col].width = 18
    
    logger = getLogger(__name__)
    logger.info(f"Game results saved to {filename}")
    
    return filename
