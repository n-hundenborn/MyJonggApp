import pandas as pd
from pathlib import Path
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

HTML_FILENAME = "evaluation_dashboard.html"

def create_html_dashboard(df: pd.DataFrame, output_path: Path) -> Path:
    """
    Create an HTML dashboard with multiple visualizations for game evaluation.
    
    Args:
        df: DataFrame with game data (from get_dataframe_from_folder)
        output_path: Path where HTML file should be saved
    
    Returns:
        Path to the generated HTML file
    """
    # Create subplot grid (3 rows, 2 columns for 5-6 visualizations)
    fig = make_subplots(
        rows=3, cols=2,
        subplot_titles=(
            'Winning Points by Player',
            'Average Points per Game',
            'Win Rate by Player Position (Wind)',
            'Points Distribution',
            'Games Played Over Time',
            'Ranking Distribution'
        ),
        specs=[
            [{'type': 'bar'}, {'type': 'bar'}],
            [{'type': 'bar'}, {'type': 'box'}],
            [{'type': 'scatter'}, {'type': 'bar'}]
        ],
        vertical_spacing=0.12,
        horizontal_spacing=0.1
    )
    
    # 1. Winning Points by Player
    winning_points = df.groupby('spieler')['siegerpunkte'].sum().sort_values(ascending=False)
    fig.add_trace(
        go.Bar(x=winning_points.index, y=winning_points.values, name='Siegerpunkte',
               marker_color='lightseagreen'),
        row=1, col=1
    )
    
    # 2. Average Points per Game
    avg_points = df.groupby('spieler')['punkte_netto'].mean().sort_values(ascending=False)
    fig.add_trace(
        go.Bar(x=avg_points.index, y=avg_points.values, name='Ø Punkte',
               marker_color='coral'),
        row=1, col=2
    )
    
    # 3. Win Rate by Player Position
    win_rate = df[df['rang'] == 1].groupby('spieler_wind').size()
    total_games = df.groupby('spieler_wind').size()
    win_percentage = (win_rate / total_games * 100).fillna(0)
    fig.add_trace(
        go.Bar(x=win_percentage.index, y=win_percentage.values, name='Gewinnrate %',
               marker_color='mediumpurple'),
        row=2, col=1
    )
    
    # 4. Points Distribution (Box plot)
    for player in df['spieler'].unique():
        player_data = df[df['spieler'] == player]['punkte_netto']
        fig.add_trace(
            go.Box(y=player_data, name=player, showlegend=False),
            row=2, col=2
        )
    
    # 5. Games Played Over Time
    df_sorted = df.sort_values('rundenstart')
    games_over_time = df_sorted.groupby('rundenstart').size().cumsum()
    fig.add_trace(
        go.Scatter(x=games_over_time.index, y=games_over_time.values, 
                   mode='lines+markers', name='Spiele gesamt',
                   line=dict(color='royalblue', width=2)),
        row=3, col=1
    )
    
    # 6. Ranking Distribution
    ranking_dist = df.groupby(['spieler', 'rang']).size().unstack(fill_value=0)
    for rank in ranking_dist.columns:
        fig.add_trace(
            go.Bar(x=ranking_dist.index, y=ranking_dist[rank], 
                   name=f'Rang {rank}'),
            row=3, col=2
        )
    
    # Update layout
    fig.update_layout(
        height=1200,
        title_text="Mahjong Game Evaluation Dashboard",
        title_font_size=20,
        showlegend=True,
        barmode='stack'
    )
    
    # Update axes labels
    fig.update_xaxes(title_text="Spieler", row=1, col=1)
    fig.update_yaxes(title_text="Siegerpunkte", row=1, col=1)
    
    fig.update_xaxes(title_text="Spieler", row=1, col=2)
    fig.update_yaxes(title_text="Ø Netto Punkte", row=1, col=2)
    
    fig.update_xaxes(title_text="Wind Position", row=2, col=1)
    fig.update_yaxes(title_text="Gewinnrate (%)", row=2, col=1)
    
    fig.update_xaxes(title_text="Spieler", row=2, col=2)
    fig.update_yaxes(title_text="Punkte Netto", row=2, col=2)
    
    fig.update_xaxes(title_text="Datum", row=3, col=1)
    fig.update_yaxes(title_text="Anzahl Spiele", row=3, col=1)
    
    fig.update_xaxes(title_text="Spieler", row=3, col=2)
    fig.update_yaxes(title_text="Anzahl", row=3, col=2)
    
    # Save to HTML
    html_file = output_path / HTML_FILENAME
    fig.write_html(html_file)
    
    return html_file
