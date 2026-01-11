import hashlib
import pandas as pd


def prepare_round_data(
        filename: str,
        df_meta: pd.DataFrame,
        df_games: pd.DataFrame,
        df_standings: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Transforms and splits data into 3 DataFrames with different granularities:
    - df_rounds: Round-level metadata
    - df_games_meta: Game-level metadata
    - df_points: Player-level point distribution

    Returns:
        tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]: (df_rounds, df_games_meta, df_points)
    """
    # Generate hash from filename
    file_hash = hashlib.md5(filename.encode()).hexdigest()[:8]

    # 1. Create Runden-Metadaten (Round-level)
    df_meta.columns = ['rundenstart', 'rundenende', 'rundendauer', 'rundendauer_text']
    df_meta['runden_id'] = file_hash
    df_meta['dateiname'] = filename

    # Extract player names and calculate siegerpunkte from standings
    df_standings.columns = ['spieler_wind', 'spieler', 'punktestand', 'rang']
    df_standings = calculate_winning_points(df_standings)

    # Map wind positions to player names and siegerpunkte
    wind_mapping = {
        'Osten': 'osten',
        'Süden': 'sueden',
        'Westen': 'westen',
        'Norden': 'norden'
    }

    for _, row in df_standings.iterrows():
        wind_key = wind_mapping.get(row['spieler_wind'])
        if wind_key:
            df_meta[f'spieler_{wind_key}'] = row['spieler']
            df_meta[f'siegerpunkte_{wind_key}'] = row['siegerpunkte']

    # Select only required columns for round metadata
    df_rounds = df_meta[[
        'runden_id', 'dateiname', 'rundenstart', 'rundenende',
        'rundendauer', 'rundendauer_text',
        'spieler_osten', 'siegerpunkte_osten',
        'spieler_sueden', 'siegerpunkte_sueden',
        'spieler_westen', 'siegerpunkte_westen',
        'spieler_norden', 'siegerpunkte_norden'
    ]].copy()

    # 2. Create Spiel-Metadaten (Game-level)
    # Handle both old files (without spielstart/spielende) and new files (with them)
    expected_columns = [
        'spiel_index',
        'wind_des_spiels',
        'gewinner_wind',
        'spieler',
        'spieler_wind',
        'punkte_brutto',
        'verdopplungen',
        'punkte_netto',
        'punkte_delta',
        'punktestand',
        'rang'
    ]
    
    # Check if timing columns exist (new format)
    if len(df_games.columns) > 11:
        expected_columns.extend(['spielstart', 'spielende'])
    
    df_games.columns = expected_columns
    
    # Add timing columns as None if they don't exist (old format compatibility)
    if 'spielstart' not in df_games.columns:
        df_games['spielstart'] = None
    if 'spielende' not in df_games.columns:
        df_games['spielende'] = None

    # Extract unique game metadata (one row per game)
    df_games_meta = df_games[[
        'spiel_index', 'wind_des_spiels', 'gewinner_wind', 'spielstart', 'spielende'
    ]].drop_duplicates().copy()
    df_games_meta['runden_id'] = file_hash

    # Reorder columns
    df_games_meta = df_games_meta[[
        'runden_id', 'spiel_index', 'wind_des_spiels',
        'gewinner_wind', 'spielstart', 'spielende'
    ]]

    # 3. Create Spiel-Punkteverteilung (Player-level)
    df_points = df_games[[
        'spiel_index', 'spieler', 'spieler_wind',
        'punkte_brutto', 'verdopplungen', 'punkte_netto',
        'punkte_delta', 'punktestand', 'rang'
    ]].copy()
    df_points['runden_id'] = file_hash

    # Reorder columns
    df_points = df_points[[
        'runden_id', 'spiel_index', 'spieler', 'spieler_wind',
        'punkte_brutto', 'verdopplungen', 'punkte_netto',
        'punkte_delta', 'punktestand', 'rang'
    ]]

    return df_rounds, df_games_meta, df_points

def calculate_winning_points(df_standings: pd.DataFrame) -> pd.DataFrame:
    """
    First gets 2 points, second 1 point, others 0 points.
    """
    df_standings = df_standings.copy()
    df_standings['siegerpunkte'] = df_standings['rang'].apply(lambda x: 2 if x == 1 else (1 if x == 2 else 0))
    return df_standings
