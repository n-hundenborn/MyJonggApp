import pandas as pd
from pathlib import Path
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

PODIUM_COLORS = ['#FFD700', '#C0C0C0', '#CD7F32', "#939393"]  # Gold, Silver, Bronze, 4th is Black
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
    # use parent foldername to create filename
    html_file = 'Auswertung_' + output_path.parent.name + '.html'
    filepath = output_path / html_file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html_content)

    return filepath


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
            'Punkteverteilung je Spieler (Boxplot)',
            'Wind-Vorteil Analyse'
        ),
        specs=[
            [{'type': 'bar'}, {'type': 'bar'}],
            [{'type': 'scatter', 'colspan': 2}, None],
            [{'type': 'bar'}, {'type': 'bar'}]
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
            go.Bar(
                x=list(players), 
                y=list(points), 
                name='Siegerpunkte',
                marker_color=bar_colors, 
                text=list(points),
                textposition='outside',
                textfont=dict(size=17, color='black'),
                showlegend=False
            ),
            row=1, col=1
        )

    # Gesamtpunktzahl by Player
    total_points = df_points.groupby('spieler')['punkte_delta'].sum().sort_values(ascending=False)

    bar_colors = [PODIUM_COLORS[i] if i < len(PODIUM_COLORS) else '#A9A9A9' for i in range(len(total_points))]
    formatted_points = [f"{int(val):,}".replace(",", ".") for val in total_points.values]
    fig.add_trace(
        go.Bar(
            x=total_points.index, 
            y=total_points.values, 
            name='Gesamtpunktzahl',
            marker_color=bar_colors, 
            text=formatted_points,
            textposition='outside',
            textfont=dict(size=14, color='black'),
            showlegend=False
        ),
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
        player_color = player_color_map.get(player, '#7f7f7f')
        fig.add_trace(
            go.Scatter(
                x=player_data['continuous_game_index'] + 1,
                y=player_data['cumulative_points'],
                mode='lines+markers',
                name=player,
                line=dict(width=2, color=player_color),
                marker=dict(size=4, color=player_color)
            ),
            row=2, col=1
        )

    # Boxplot for Points Distribution
    all_players = sorted(df_points['spieler'].unique())
    num_players = len(all_players)
    
    # Track where boxplot traces start
    boxplot_start_idx = len(fig.data)
    
    for player in all_players:
        player_data = df_points[df_points['spieler'] == player]
        player_color = player_color_map.get(player, '#7f7f7f')
        
        # Netto points boxplot
        fig.add_trace(
            go.Box(
                y=player_data['punkte_netto'],
                name=player,
                marker_color=player_color,
                visible=True,
                showlegend=False
            ),
            row=3, col=1
        )
        
        # Delta points boxplot
        fig.add_trace(
            go.Box(
                y=player_data['punkte_delta'],
                name=player,
                marker_color=player_color,
                visible=False,
                showlegend=False
            ),
            row=3, col=1
        )

    # Wind Advantage Analysis
    # Find round winners (rank 1 at final game of each round)
    final_games = df_points.groupby('runden_id')['spiel_index'].max().reset_index()
    final_games.columns = ['runden_id', 'final_spiel_index']
    
    round_winners = df_points.merge(final_games, on='runden_id')
    round_winners = round_winners[
        (round_winners['spiel_index'] == round_winners['final_spiel_index']) &
        (round_winners['rang'] == 1)
    ]
    
    # Count wins by wind position
    wind_wins = round_winners['spieler_wind'].value_counts()
    total_rounds = len(df_rounds)
    
    # Define fixed wind order (matching Wind enum in game.py)
    wind_order = ['Osten', 'Süden', 'Westen', 'Norden']
    
    # Calculate win rates for each wind
    wind_win_rates = []
    wind_win_counts = []
    for wind in wind_order:
        wins = wind_wins.get(wind, 0)
        rate = (wins / total_rounds * 100) if total_rounds > 0 else 0
        wind_win_rates.append(rate)
        wind_win_counts.append(wins)
    
    # Create bar chart with expected 25% line
    fig.add_trace(
        go.Bar(
            x=wind_order,
            y=wind_win_rates,
            name='Gewinnrate',
            marker_color=['#ff9999', '#ffcc99', '#99ccff', '#99ff99'],
            text=wind_win_counts,
            textposition='inside',
            insidetextanchor='start',
            textfont=dict(size=17, color='black'),
            showlegend=False
        ),
        row=3, col=2
    )
    
    # Add expected 25% reference line
    fig.add_hline(
        y=25,
        line_dash="dash",
        line_color="red",
        row=3, col=2
    )
    
    fig.update_yaxes(
        title_text="Gewinnrate (%)",
        row=3, col=2
    )
    
    fig.update_xaxes(
        title_text="Windposition",
        row=3, col=2
    )

    # Update layout
    total_traces = len(fig.data)
    
    # Build visibility arrays for toggle buttons
    # All traces before boxplots stay visible (podium bars + timeline)
    base_visibility = [True] * boxplot_start_idx
    
    # For netto: show first set of boxplots (netto), hide second set (delta)
    netto_boxplot_visibility = []
    for i in range(num_players):
        netto_boxplot_visibility.extend([True, False])
    
    # For delta: hide first set of boxplots (netto), show second set (delta)
    delta_boxplot_visibility = []
    for i in range(num_players):
        delta_boxplot_visibility.extend([False, True])
    
    # Wind analysis trace at the end should always be visible
    wind_visibility = [True]
    
    netto_visible = base_visibility + netto_boxplot_visibility + wind_visibility
    delta_visible = base_visibility + delta_boxplot_visibility + wind_visibility
    
    fig.update_layout(
        height=1200,
        title_text="Mahjong Dashboard - Übersicht aller Runden",
        title_font_size=24,
        showlegend=True,
        template='plotly_white',
        barmode='stack',
        legend=dict(
            orientation='h',
            yanchor='top',
            y=0.70,
            xanchor='left',
            x=0.0
        ),
        updatemenus=[
            dict(
                type="buttons",
                direction="left",
                buttons=[
                    dict(
                        args=[
                            {"visible": netto_visible},
                            {"yaxis4.title.text": "Nettopunkte (inkl. Verdopplungen)"}
                        ],
                        label="Nettopunkte",
                        method="update"
                    ),
                    dict(
                        args=[
                            {"visible": delta_visible},
                            {"yaxis4.title.text": "Punkte Delta (mit Schulden)"}
                        ],
                        label="Punktedifferenz",
                        method="update"
                    )
                ],
                active=0,
                showactive=True,
                x=0.0,
                xanchor="left",
                y=-0.05,
                yanchor="top",
                bgcolor="lightgray",
                bordercolor="gray",
                borderwidth=1
            )
        ]
    )

    # Update axes
    # Add extra space at top for Siegerpunkte labels
    max_siegerpunkte = max(points) if sorted_players else 0
    fig.update_xaxes(
        row=1, col=1,
        tickfont=dict(size=14)
    )
    fig.update_yaxes(
        title_text="Siegerpunkte", 
        row=1, col=1, 
        range=[0, max_siegerpunkte * 1.15]
    )

    max_gesamtpunktzahl = total_points.max() if len(total_points) > 0 else 0
    min_gesamtpunktzahl = total_points.min() if len(total_points) > 0 else 0
    y_range_buffer = abs(max_gesamtpunktzahl - min_gesamtpunktzahl) * 0.15
    fig.update_xaxes(
        row=1, col=2,
        tickfont=dict(size=14)
    )
    fig.update_yaxes(
        title_text="Gesamtpunktzahl", 
        row=1, col=2,
        range=[min_gesamtpunktzahl - y_range_buffer, max_gesamtpunktzahl + y_range_buffer]
    )

    # X-axis for cumulative timeline: show all games if <= 25, otherwise every 2nd
    max_games = df_points_sorted['continuous_game_index'].max() if not df_points_sorted.empty else 0
    game_tick_interval = 1 if max_games <= 25 else 2
    fig.update_xaxes(
        title_text="Spielnummer (alle Runden)", 
        row=2, col=1, 
        dtick=game_tick_interval,
        tick0=1,
        range=[0.5, max_games + 1.5]
    )
    fig.update_yaxes(title_text="Gesamtpunktzahl", row=2, col=1)

    fig.update_xaxes(
        row=3, col=1,
        tickfont=dict(size=14)
    )
    fig.update_yaxes(title_text="Nettopunkte (inkl. Verdopplungen)", row=3, col=1)
    
    fig.update_xaxes(
        row=3, col=2,
        tickfont=dict(size=14)
    )

    return fig
