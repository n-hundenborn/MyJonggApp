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
            <span style="margin-left: 30px; font-size: 14px; color: white; font-style: italic;">
                Nettopunkte: Punkte inkl. Verdopplungen | Punktedifferenz: Nettopunkte inkl. Schulden mit allen Spielern
            </span>
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
    5. Wind-Vorteil Analyse
    6. Performance als Wind des Spiels
    """
    # Create subplot grid
    fig = make_subplots(
        rows=5, cols=2,
        subplot_titles=(
            'Podium - Siegerpunkte',
            'Podium - Gesamtpunktzahl',
            'Laufende Summe der Gesamtpunktzahl über alle Spiele',
            'Punkteverteilung je Spieler (Boxplot)',
            'Ø Punkte',
            'Spielführer Analyse',
            'Ø Punkte als Spielführer',
            'Wind-Vorteil Analyse'
        ),
        specs=[
            [{'type': 'bar'}, {'type': 'bar'}],
            [{'type': 'scatter', 'colspan': 2}, None],
            [{'type': 'box'}, {'type': 'bar'}],
            [{'type': 'box'}, {'type': 'bar'}],
            [{'type': 'bar', 'colspan': 2}, None]
        ],
        vertical_spacing=0.08,
        horizontal_spacing=0.12,
        row_heights=[0.20, 0.30, 0.18, 0.18, 0.14]
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
                textposition='inside',
                insidetextanchor='start',
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
            showlegend=False
        ),
        row=1, col=2
    )
    
    # Add text labels at y=0
    fig.add_trace(
        go.Scatter(
            x=total_points.index,
            y=[0] * len(total_points),
            mode='text',
            text=formatted_points,
            textposition='top center',
            textfont=dict(size=14, color='black'),
            showlegend=False,
            hoverinfo='skip'
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
    # Use consistent player order from Siegerpunkte ranking
    all_players = [player for player, _ in sorted_players] if sorted_players else sorted(df_points['spieler'].unique())
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

    # Average points bar chart per player (row 3, col 2)
    avg_netto_per_player = df_points.groupby('spieler')['punkte_netto'].mean().reset_index(name='avg_netto')
    avg_delta_per_player = df_points.groupby('spieler')['punkte_delta'].mean().reset_index(name='avg_delta')
    avg_points_per_player = avg_netto_per_player.merge(avg_delta_per_player, on='spieler')
    
    # Use consistent player order from Siegerpunkte ranking
    player_order = [player for player, _ in sorted_players] if sorted_players else sorted(avg_points_per_player['spieler'].unique())
    avg_points_per_player['spieler'] = pd.Categorical(avg_points_per_player['spieler'], categories=player_order, ordered=True)
    avg_points_per_player = avg_points_per_player.sort_values('spieler')
    
    bar_colors_avg_player = [player_color_map.get(player, '#7f7f7f') for player in avg_points_per_player['spieler']]
    
    # Netto average bar chart (visible by default)
    formatted_avg_netto = [f"{int(val):,}".replace(",", ".") for val in avg_points_per_player['avg_netto']]
    fig.add_trace(
        go.Bar(
            x=avg_points_per_player['spieler'],
            y=avg_points_per_player['avg_netto'],
            name='Ø Netto',
            marker_color=bar_colors_avg_player,
            showlegend=False,
            visible=True
        ),
        row=3, col=2
    )
    
    # Add text labels at y=0 for netto
    fig.add_trace(
        go.Scatter(
            x=avg_points_per_player['spieler'],
            y=[0] * len(avg_points_per_player),
            mode='text',
            text=formatted_avg_netto,
            textposition='top center',
            textfont=dict(size=14, color='black'),
            showlegend=False,
            hoverinfo='skip',
            visible=True
        ),
        row=3, col=2
    )
    
    # Delta average bar chart (hidden by default)
    formatted_avg_delta = [f"{int(val):,}".replace(",", ".") for val in avg_points_per_player['avg_delta']]
    fig.add_trace(
        go.Bar(
            x=avg_points_per_player['spieler'],
            y=avg_points_per_player['avg_delta'],
            name='Ø Delta',
            marker_color=bar_colors_avg_player,
            showlegend=False,
            visible=False
        ),
        row=3, col=2
    )
    
    # Add text labels at y=0 for delta
    fig.add_trace(
        go.Scatter(
            x=avg_points_per_player['spieler'],
            y=[0] * len(avg_points_per_player),
            mode='text',
            text=formatted_avg_delta,
            textposition='top center',
            textfont=dict(size=14, color='black'),
            showlegend=False,
            hoverinfo='skip',
            visible=False
        ),
        row=3, col=2
    )
    
    fig.update_xaxes(
        row=3, col=2,
        tickfont=dict(size=14)
    )
    
    # Calculate shared y-axis range for both average bar charts (row 3 col 2 and row 4 col 2)
    # For netto values
    all_netto_values = list(avg_points_per_player['avg_netto'])
    all_delta_values = list(avg_points_per_player['avg_delta'])

    # Wind Advantage Analysis (moved to row 5)
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
        row=5, col=1
    )
    
    # Add expected 25% reference line
    fig.add_hline(
        y=25,
        line_dash="dash",
        line_color="red",
        row=5, col=1
    )
    
    fig.update_yaxes(
        title_text="Gewinnrate (%)",
        row=5, col=1
    )
    
    fig.update_xaxes(
        title_text="Windposition",
        row=5, col=1
    )

    # Wind Performance Analysis (as wind_des_spiels)
    # Merge df_points with df_games to get wind_des_spiels
    df_wind_analysis = df_points.merge(
        df_games[['runden_id', 'spiel_index', 'wind_des_spiels', 'gewinner_wind']],
        on=['runden_id', 'spiel_index'],
        how='left'
    )
    
    # Filter for games where player was the wind of the game
    df_as_wind = df_wind_analysis[df_wind_analysis['spieler_wind'] == df_wind_analysis['wind_des_spiels']]
    
    # Calculate per-round statistics for each player
    # 1. Total netto points as wind_des_spiels per round
    df_netto_as_wind = df_as_wind.groupby(
        ['runden_id', 'spieler']
    )['punkte_netto'].sum().reset_index(name='netto_as_wind')
    
    # 2. Total delta points as wind_des_spiels per round
    df_delta_as_wind = df_as_wind.groupby(
        ['runden_id', 'spieler']
    )['punkte_delta'].sum().reset_index(name='delta_as_wind')
    
    # Merge both statistics
    df_wind_stats = df_netto_as_wind.merge(
        df_delta_as_wind,
        on=['runden_id', 'spieler'],
        how='outer'
    ).fillna(0)
    
    # Create boxplots for each player (netto and delta, togglable with main boxplot)
    # Use consistent player order from Siegerpunkte ranking
    all_players_sorted = [player for player, _ in sorted_players] if sorted_players else sorted(df_points['spieler'].unique())
    num_players_wind = len(all_players_sorted)
    
    for player in all_players_sorted:
        player_stats = df_wind_stats[df_wind_stats['spieler'] == player]
        player_color = player_color_map.get(player, '#7f7f7f')
        
        # Netto points boxplot (visible by default)
        fig.add_trace(
            go.Box(
                y=player_stats['netto_as_wind'],
                name=player,
                marker_color=player_color,
                visible=True,
                showlegend=False
            ),
            row=4, col=1
        )
        
        # Delta points boxplot (hidden by default)
        fig.add_trace(
            go.Box(
                y=player_stats['delta_as_wind'],
                name=player,
                marker_color=player_color,
                visible=False,
                showlegend=False
            ),
            row=4, col=1
        )
    
    fig.update_yaxes(title_text="Nettopunkte als Wind des Spiels", row=4, col=1)

    # Bar charts: Average points as wind_des_spiels
    # Calculate average netto and delta points for each player
    avg_netto_as_wind = df_as_wind.groupby('spieler')['punkte_netto'].mean().reset_index(name='avg_netto')
    avg_delta_as_wind = df_as_wind.groupby('spieler')['punkte_delta'].mean().reset_index(name='avg_delta')
    
    # Merge and use consistent player order from Siegerpunkte ranking
    avg_points_as_wind = avg_netto_as_wind.merge(avg_delta_as_wind, on='spieler')
    player_order = [player for player, _ in sorted_players] if sorted_players else sorted(avg_points_as_wind['spieler'].unique())
    avg_points_as_wind['spieler'] = pd.Categorical(avg_points_as_wind['spieler'], categories=player_order, ordered=True)
    avg_points_as_wind = avg_points_as_wind.sort_values('spieler')
    
    # Create bar colors using player color map
    bar_colors_avg = [player_color_map.get(player, '#7f7f7f') for player in avg_points_as_wind['spieler']]
    
    # Netto average bar chart (visible by default)
    formatted_netto = [f"{int(val):,}".replace(",", ".") for val in avg_points_as_wind['avg_netto']]
    fig.add_trace(
        go.Bar(
            x=avg_points_as_wind['spieler'],
            y=avg_points_as_wind['avg_netto'],
            name='Ø Netto als Wind',
            marker_color=bar_colors_avg,
            showlegend=False,
            visible=True
        ),
        row=4, col=2
    )
    
    # Add text labels at y=0 for netto
    fig.add_trace(
        go.Scatter(
            x=avg_points_as_wind['spieler'],
            y=[0] * len(avg_points_as_wind),
            mode='text',
            text=formatted_netto,
            textposition='top center',
            textfont=dict(size=14, color='black'),
            showlegend=False,
            hoverinfo='skip',
            visible=True
        ),
        row=4, col=2
    )
    
    # Delta average bar chart (hidden by default)
    formatted_delta = [f"{int(val):,}".replace(",", ".") for val in avg_points_as_wind['avg_delta']]
    fig.add_trace(
        go.Bar(
            x=avg_points_as_wind['spieler'],
            y=avg_points_as_wind['avg_delta'],
            name='Ø Delta als Wind',
            marker_color=bar_colors_avg,
            showlegend=False,
            visible=False
        ),
        row=4, col=2
    )
    
    # Add text labels at y=0 for delta
    fig.add_trace(
        go.Scatter(
            x=avg_points_as_wind['spieler'],
            y=[0] * len(avg_points_as_wind),
            mode='text',
            text=formatted_delta,
            textposition='top center',
            textfont=dict(size=14, color='black'),
            showlegend=False,
            hoverinfo='skip',
            visible=False
        ),
        row=4, col=2
    )
    
    fig.update_xaxes(
        row=4, col=2,
        tickfont=dict(size=14)
    )
    
    # Collect values from row 4 col 2 bar charts for shared y-axis range
    all_netto_values.extend(list(avg_points_as_wind['avg_netto']))
    all_delta_values.extend(list(avg_points_as_wind['avg_delta']))
    
    # Calculate shared y-axis ranges with some padding
    netto_min = min(all_netto_values) if all_netto_values else 0
    netto_max = max(all_netto_values) if all_netto_values else 0
    delta_min = min(all_delta_values) if all_delta_values else 0
    delta_max = max(all_delta_values) if all_delta_values else 0
    
    # Add 10% padding at bottom and top
    netto_range_size = abs(netto_max - netto_min)
    netto_padding = netto_range_size * 0.10 if netto_range_size > 0 else 100
    delta_range_size = abs(delta_max - delta_min)
    delta_padding = delta_range_size * 0.10 if delta_range_size > 0 else 100
    
    # Set initial y-axis ranges for both bar charts (netto by default)
    # Ensure lower bound never exceeds 0
    shared_netto_range = [min(0, netto_min - netto_padding), netto_max + netto_padding]
    shared_delta_range = [min(0, delta_min - delta_padding), delta_max + delta_padding]
    
    fig.update_yaxes(title_text="Ø Nettopunkte", range=shared_netto_range, row=3, col=2)
    fig.update_yaxes(title_text="Ø Nettopunkte", range=shared_netto_range, row=4, col=2)

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
    
    # Average points per player bar charts + text labels: netto visible, delta hidden
    # Each has: bar + scatter text = 2 traces
    avg_player_bar_netto_visibility = [True, True, False, False]  # netto bar + text visible, delta bar + text hidden
    avg_player_bar_delta_visibility = [False, False, True, True]  # netto bar + text hidden, delta bar + text visible
    
    # Wind analysis trace should always be visible
    wind_visibility = [True]
    
    # Wind performance boxplots: netto visible, delta hidden (same pattern as main boxplot)
    wind_perf_netto_visibility = []
    for i in range(num_players_wind):
        wind_perf_netto_visibility.extend([True, False])
    
    # Wind performance boxplots: netto hidden, delta visible
    wind_perf_delta_visibility = []
    for i in range(num_players_wind):
        wind_perf_delta_visibility.extend([False, True])
    
    # Average points as wind bar charts + text labels: netto visible, delta hidden
    # Each has: bar + scatter text = 2 traces
    avg_wind_bar_netto_visibility = [True, True, False, False]  # netto bar + text visible, delta bar + text hidden
    avg_wind_bar_delta_visibility = [False, False, True, True]  # netto bar + text hidden, delta bar + text visible
    
    netto_visible = base_visibility + netto_boxplot_visibility + avg_player_bar_netto_visibility + wind_visibility + wind_perf_netto_visibility + avg_wind_bar_netto_visibility
    delta_visible = base_visibility + delta_boxplot_visibility + avg_player_bar_delta_visibility + wind_visibility + wind_perf_delta_visibility + avg_wind_bar_delta_visibility
    
    fig.update_layout(
        height=1600,
        title_text="Mahjong Dashboard - Übersicht aller Runden",
        title_font_size=24,
        showlegend=True,
        template='plotly_white',
        barmode='stack',
        legend=dict(
            orientation='h',
            yanchor='top',
            y=0.55,
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
                            {
                                "yaxis4.title.text": "Nettopunkte (inkl. Verdopplungen)",
                                "yaxis5.title.text": "Ø Nettopunkte",
                                "yaxis5.range": shared_netto_range,
                                "yaxis6.title.text": "Nettopunkte als Wind des Spiels",
                                "yaxis7.title.text": "Ø Nettopunkte",
                                "yaxis7.range": shared_netto_range
                            }
                        ],
                        label="Nettopunkte",
                        method="update"
                    ),
                    dict(
                        args=[
                            {"visible": delta_visible},
                            {
                                "yaxis4.title.text": "Punkte Delta (mit Schulden)",
                                "yaxis5.title.text": "Ø Punkte Delta",
                                "yaxis5.range": shared_delta_range,
                                "yaxis6.title.text": "Punkte Delta als Wind des Spiels",
                                "yaxis7.title.text": "Ø Punkte Delta",
                                "yaxis7.range": shared_delta_range
                            }
                        ],
                        label="Punktedifferenz",
                        method="update"
                    )
                ],
                active=0,
                showactive=True,
                x=0.0,
                xanchor="left",
                y=0.50,
                yanchor="bottom",
                bgcolor="lightgray",
                bordercolor="gray",
                borderwidth=1
            )
        ]
    )

    # Update axes
    # Add extra space at top for Siegerpunkte labels
    max_siegerpunkte = max(points) if sorted_players else 0
    min_siegerpunkte = min(points) if sorted_players else 0
    y_range_sieger = abs(max_siegerpunkte - min_siegerpunkte)
    # Add 20% buffer at top for text labels
    y_range_buffer_top_sieger = y_range_sieger * 0.20
    fig.update_xaxes(
        row=1, col=1,
        tickfont=dict(size=14)
    )
    fig.update_yaxes(
        title_text="Siegerpunkte", 
        row=1, col=1, 
        range=[min_siegerpunkte if min_siegerpunkte < 0 else 0, max_siegerpunkte + y_range_buffer_top_sieger]
    )

    max_gesamtpunktzahl = total_points.max() if len(total_points) > 0 else 0
    min_gesamtpunktzahl = total_points.min() if len(total_points) > 0 else 0
    y_range_total = abs(max_gesamtpunktzahl - min_gesamtpunktzahl)
    y_range_buffer_top = y_range_total * 0.20
    y_range_buffer_bottom = y_range_total * 0.15
    fig.update_xaxes(
        row=1, col=2,
        tickfont=dict(size=14)
    )
    fig.update_yaxes(
        title_text="Gesamtpunktzahl", 
        row=1, col=2,
        range=[min_gesamtpunktzahl - y_range_buffer_bottom, max_gesamtpunktzahl + y_range_buffer_top]
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
