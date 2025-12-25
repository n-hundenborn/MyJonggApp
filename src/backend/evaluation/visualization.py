import pandas as pd
from pathlib import Path
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

HTML_FILENAME = "evaluation_dashboard.html"
PODIUM_COLORS = ['#FFD700', '#C0C0C0', '#CD7F32', '#8B7D6B']  # Gold, Silver, Bronze, 4th
PLAYER_COLORS = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f']  # Neutral distinguishable colors for players


def create_html_dashboard(
    df_rounds: pd.DataFrame,
    df_games: pd.DataFrame,
    df_points: pd.DataFrame,
    output_path: Path
) -> Path:
    """
    Create an interactive HTML dashboard with navigation support.

    Currently showing:
    - Page 1 (Overview): Aggregate statistics across all rounds

    Extendable for future pages (e.g., Round Details, Player Analysis)

    Args:
        df_rounds: Round-level metadata DataFrame
        df_games: Game-level metadata DataFrame
        df_points: Player-level points distribution DataFrame
        output_path: Path where HTML file should be saved

    Returns:
        Path to the generated HTML file
    """
    # Create page figures
    fig_overview = _create_overview_figure(df_rounds, df_games, df_points)
    # fig_detail = _create_detail_figure(df_rounds, df_games, df_points)  # Future: Round Details

    # Convert figures to HTML divs
    overview_html = fig_overview.to_html(full_html=False, include_plotlyjs='cdn', div_id='overview-page')
    # detail_html = fig_detail.to_html(full_html=False, include_plotlyjs=False, div_id='detail-page')  # Future

    # Create complete HTML with navigation structure (extensible for future pages)
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Mahjong Evaluation Dashboard</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f5f5f5;
            }}
            .nav-bar {{
                background-color: #2c3e50;
                padding: 15px 30px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                position: sticky;
                top: 0;
                z-index: 1000;
            }}
            .nav-button {{
                background-color: #3498db;
                color: white;
                border: none;
                padding: 10px 25px;
                margin-right: 10px;
                cursor: pointer;
                border-radius: 5px;
                font-size: 16px;
                transition: background-color 0.3s;
            }}
            .nav-button:hover {{
                background-color: #2980b9;
            }}
            .nav-button.active {{
                background-color: #27ae60;
            }}
            .page {{
                display: none;
                padding: 20px;
                animation: fadeIn 0.3s;
            }}
            .page.active {{
                display: block;
            }}
            @keyframes fadeIn {{
                from {{ opacity: 0; }}
                to {{ opacity: 1; }}
            }}
            .page-title {{
                color: #2c3e50;
                font-size: 28px;
                margin-bottom: 20px;
                padding-bottom: 10px;
                border-bottom: 3px solid #3498db;
            }}
        </style>
    </head>
    <body>
        <div class="nav-bar">
            <button class="nav-button active" id="btn-overview" onclick="showPage('overview')">
                📊 Gesamtansicht - alle Runden
            </button>
            <!-- Future pages can be added here -->
        </div>

        <div id="overview-page" class="page active">
            {overview_html}
        </div>

        <!-- Future page containers can be added here -->

        <script>
            function showPage(pageId) {{
                // Hide all pages
                const pages = document.querySelectorAll('.page');
                pages.forEach(page => page.classList.remove('active'));

                // Remove active state from all buttons
                const buttons = document.querySelectorAll('.nav-button');
                buttons.forEach(btn => btn.classList.remove('active'));

                // Show selected page
                document.getElementById(pageId + '-page').classList.add('active');
                document.getElementById('btn-' + pageId).classList.add('active');

                // Scroll to top
                window.scrollTo({{ top: 0, behavior: 'smooth' }});
            }}
        </script>
    </body>
    </html>
    """

    # Save to file
    html_file = output_path / HTML_FILENAME
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    return html_file


def _create_overview_figure(
    df_rounds: pd.DataFrame,
    df_games: pd.DataFrame,
    df_points: pd.DataFrame
) -> go.Figure:
    """
    Create overview page figure with aggregate statistics across all rounds.

    Visualizations:
    1. Podium - Siegerpunkte
    2. Podium - Gesamtpunktzahl
    3. Laufende Summe der Gesamtpunktzahl über alle Spiele
    4. Ø Nettopunkte je Spieler
    """
    # Create subplot grid
    fig = make_subplots(
        rows=3, cols=2,
        subplot_titles=(
            'Podium - Siegerpunkte',
            'Podium - Gesamtpunktzahl',
            'Laufende Summe der Gesamtpunktzahl über alle Spiele',
            'Ø Nettopunkte je Spieler',
            ''
        ),
        specs=[
            [{'type': 'bar'}, {'type': 'bar'}],
            [{'type': 'scatter', 'colspan': 2}, None],
            [{'type': 'bar'}, None]
        ],
        vertical_spacing=0.12,
        horizontal_spacing=0.12,
        row_heights=[0.3, 0.4, 0.3]
    )

    # Siegerpunkte by Player
    siegerpunkte_data = {}
    for wind in ['osten', 'sueden', 'westen', 'norden']:
        player_col = f'spieler_{wind}'
        points_col = f'siegerpunkte_{wind}'

        if player_col in df_rounds.columns:
            for _, row in df_rounds.iterrows():
                player = row[player_col]
                points = row[points_col]
                siegerpunkte_data[player] = siegerpunkte_data.get(player, 0) + points

    sorted_players = sorted(siegerpunkte_data.items(), key=lambda x: x[1], reverse=True)
    
    # Create player-to-color mapping based on Siegerpunkte ranking
    player_color_map = {}
    if sorted_players:
        for i, (player, _) in enumerate(sorted_players):
            player_color_map[player] = PLAYER_COLORS[i % len(PLAYER_COLORS)]
        
        players, points = zip(*sorted_players)
        bar_colors = [PODIUM_COLORS[i] if i < len(PODIUM_COLORS) else '#A9A9A9' for i in range(len(players))]
        fig.add_trace(
            go.Bar(x=list(players), y=list(points), name='Siegerpunkte',
                   marker_color=bar_colors, showlegend=False),
            row=1, col=1
        )

    # Gesamtpunktzahl by Player
    total_points = df_points.groupby('spieler')['punkte_delta'].sum().sort_values(ascending=False)

    bar_colors = [PODIUM_COLORS[i] if i < len(PODIUM_COLORS) else '#A9A9A9' for i in range(len(total_points))]
    fig.add_trace(
        go.Bar(x=total_points.index, y=total_points.values, name='Gesamtpunktzahl',
               marker_color=bar_colors, showlegend=False),
        row=1, col=2
    )

    # Cumulative Points Timeline
    # Prepare continuous game index
    df_points_sorted = df_points.merge(
        df_rounds[['runden_id', 'rundenstart']],
        on='runden_id',
        how='left'
    ).sort_values(['rundenstart', 'spiel_index'])

    df_points_sorted['continuous_game_index'] = df_points_sorted.groupby(
        ['runden_id', 'spiel_index']
    ).ngroup()

    # Calculate cumulative points
    df_points_sorted = df_points_sorted.sort_values('continuous_game_index')
    df_points_sorted['cumulative_points'] = df_points_sorted.groupby('spieler')['punkte_delta'].cumsum()

    for player in sorted(df_points_sorted['spieler'].unique()):
        player_data = df_points_sorted[df_points_sorted['spieler'] == player]
        player_color = player_color_map.get(player, '#7f7f7f')  # Default gray if not found
        fig.add_trace(
            go.Scatter(
                x=player_data['continuous_game_index'],
                y=player_data['cumulative_points'],
                mode='lines+markers',
                name=player,
                line=dict(width=2, color=player_color),
                marker=dict(size=4, color=player_color)
            ),
            row=2, col=1
        )

    # Average Points per Game
    avg_points = df_points.groupby('spieler')['punkte_netto'].mean().sort_values(ascending=False)
    bar_colors = [player_color_map.get(player, '#7f7f7f') for player in avg_points.index]
    fig.add_trace(
        go.Bar(x=avg_points.index, y=avg_points.values, name='Avg Points',
               marker_color=bar_colors, showlegend=False),
        row=3, col=1
    )

    # Update layout
    fig.update_layout(
        height=1200,
        title_text="Mahjong Dashboard - Übersicht aller Runden",
        title_font_size=24,
        showlegend=True,
        template='plotly_white',
        barmode='stack',
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.15,
            xanchor='center',
            x=0.5
        )
    )

    # Update axes
    fig.update_xaxes(title_text="Spieler", row=1, col=1)
    fig.update_yaxes(title_text="Siegerpunkte", row=1, col=1)

    fig.update_xaxes(title_text="Spieler", row=1, col=2)
    fig.update_yaxes(title_text="Gesamtpunktzahl", row=1, col=2)

    fig.update_xaxes(title_text="Spielnummer (alle Runden)", row=2, col=1)
    fig.update_yaxes(title_text="Gesamtpunktzahl", row=2, col=1)

    fig.update_xaxes(title_text="Spieler", row=3, col=1)
    fig.update_yaxes(title_text="Ø Punkte inkl. Verdopplungen", row=3, col=1)

    return fig
