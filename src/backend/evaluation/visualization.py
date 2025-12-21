import pandas as pd
from pathlib import Path
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

HTML_FILENAME = "evaluation_dashboard.html"


def create_interactive_html_dashboard(
    df_rounds: pd.DataFrame, 
    df_games: pd.DataFrame, 
    df_points: pd.DataFrame, 
    output_path: Path
) -> Path:
    """
    Create an interactive HTML dashboard with round filtering and chart type selection.
    
    Uses Plotly's updatemenus for client-side filtering without requiring a server.
    Pre-generates traces for all rounds and chart types, then toggles visibility via buttons.
    
    Args:
        df_rounds: Round-level metadata DataFrame
        df_games: Game-level metadata DataFrame
        df_points: Player-level points distribution DataFrame
        output_path: Path where HTML file should be saved
    
    Returns:
        Path to the generated HTML file
    """
    # Create figure with subplots
    fig = make_subplots(
        rows=1, cols=1,
        subplot_titles=('Timeline',)
    )
    
    # Get list of all rounds for filtering
    all_rounds = df_rounds[['runden_id', 'dateiname', 'rundenstart']].sort_values('rundenstart').to_dict('records')
    
    # Track trace indices for visibility toggling: {(chart_type, round_key): [trace_indices]}
    trace_indices = {}
    
    # Prepare data for continuous game index across all rounds
    df_points_sorted = df_points.merge(
        df_rounds[['runden_id', 'rundenstart']], 
        on='runden_id', 
        how='left'
    )
    
    # Add continuous game index
    df_points_sorted['continuous_game_index'] = df_points_sorted.groupby(['runden_id', 'spiel_index']).ngroup()
    
    # Calculate cumulative points for each player
    df_points_sorted = df_points_sorted.sort_values('continuous_game_index')
    df_points_sorted['cumulative_points'] = df_points_sorted.groupby('spieler')['punkte_delta'].cumsum()
    
    # === 1. Generate RANK Timeline traces ===
    
    # 1a. Rank Timeline for "All Rounds"
    trace_indices[('rang', 'all')] = []
    for player in sorted(df_points_sorted['spieler'].unique()):
        player_data = df_points_sorted[df_points_sorted['spieler'] == player]
        
        fig.add_trace(go.Scatter(
            x=player_data['continuous_game_index'],
            y=player_data['rang'],
            mode='lines+markers',
            name=player,
            line=dict(width=2),
            marker=dict(size=6),
            visible=True,  # Visible by default
            showlegend=True
        ))
        trace_indices[('rang', 'all')].append(len(fig.data) - 1)
    
    # 1b. Rank Timeline for each individual round
    for round_info in all_rounds:
        runden_id = round_info['runden_id']
        round_points = df_points[df_points['runden_id'] == runden_id].sort_values('spiel_index')
        
        if not round_points.empty:
            trace_indices[('rang', runden_id)] = []
            
            for player in sorted(round_points['spieler'].unique()):
                player_data = round_points[round_points['spieler'] == player]
                
                fig.add_trace(go.Scatter(
                    x=player_data['spiel_index'],
                    y=player_data['rang'],
                    mode='lines+markers',
                    name=player,
                    line=dict(width=2),
                    marker=dict(size=6),
                    visible=False,
                    showlegend=True
                ))
                trace_indices[('rang', runden_id)].append(len(fig.data) - 1)
    
    # === 2. Generate GESAMTPUNKTZAHL Timeline traces ===
    
    # 2a. Gesamtpunktzahl Timeline for "All Rounds"
    trace_indices[('gesamtpunktzahl', 'all')] = []
    for player in sorted(df_points_sorted['spieler'].unique()):
        player_data = df_points_sorted[df_points_sorted['spieler'] == player]
        
        fig.add_trace(go.Scatter(
            x=player_data['continuous_game_index'],
            y=player_data['cumulative_points'],
            mode='lines+markers',
            name=player,
            line=dict(width=2),
            marker=dict(size=6),
            visible=False,  # Hidden by default
            showlegend=True
        ))
        trace_indices[('gesamtpunktzahl', 'all')].append(len(fig.data) - 1)
    
    # 2b. Gesamtpunktzahl Timeline for each individual round
    for round_info in all_rounds:
        runden_id = round_info['runden_id']
        round_points = df_points[df_points['runden_id'] == runden_id].sort_values('spiel_index')
        
        if not round_points.empty:
            trace_indices[('gesamtpunktzahl', runden_id)] = []
            
            for player in sorted(round_points['spieler'].unique()):
                player_data = round_points[round_points['spieler'] == player]
                cumulative = player_data['punkte_delta'].cumsum()
                
                fig.add_trace(go.Scatter(
                    x=player_data['spiel_index'],
                    y=cumulative,
                    mode='lines+markers',
                    name=player,
                    line=dict(width=2),
                    marker=dict(size=6),
                    visible=False,
                    showlegend=True
                ))
                trace_indices[('gesamtpunktzahl', runden_id)].append(len(fig.data) - 1)
    
    # === 3. Create Chart Type Selection buttons ===
    chart_type_buttons = []
    
    # Rang button
    visibility_rang = [False] * len(fig.data)
    for idx in trace_indices.get(('rang', 'all'), []):
        visibility_rang[idx] = True
    
    chart_type_buttons.append(dict(
        label='Rang',
        method='update',
        args=[
            {'visible': visibility_rang},
            {'title.text': 'Rank Timeline - All Rounds',
             'yaxis.title.text': 'Rank',
             'yaxis.autorange': 'reversed'}
        ]
    ))
    
    # Gesamtpunktzahl button
    visibility_points = [False] * len(fig.data)
    for idx in trace_indices.get(('gesamtpunktzahl', 'all'), []):
        visibility_points[idx] = True
    
    chart_type_buttons.append(dict(
        label='Gesamtpunktzahl',
        method='update',
        args=[
            {'visible': visibility_points},
            {'title.text': 'Total Points Timeline - All Rounds',
             'yaxis.title.text': 'Cumulative Points',
             'yaxis.autorange': True}
        ]
    ))
    
    # === 4. Create Round Filter buttons ===
    round_buttons = []
    
    # "All Rounds" button - show rang by default
    visibility_all = [False] * len(fig.data)
    for idx in trace_indices.get(('rang', 'all'), []):
        visibility_all[idx] = True
    
    round_buttons.append(dict(
        label='All Rounds',
        method='update',
        args=[
            {'visible': visibility_all},
            {'title.text': 'Rank Timeline - All Rounds',
             'xaxis.title.text': 'Game Number (Continuous)'}
        ]
    ))
    
    # Individual round buttons
    for round_info in all_rounds:
        runden_id = round_info['runden_id']
        dateiname = round_info['dateiname']
        
        # Show rang by default when selecting a round
        visibility = [False] * len(fig.data)
        for idx in trace_indices.get(('rang', runden_id), []):
            visibility[idx] = True
        
        round_buttons.append(dict(
            label=dateiname,
            method='update',
            args=[
                {'visible': visibility},
                {'title.text': f'Rank Timeline - {dateiname}',
                 'xaxis.title.text': 'Game Number (Round)'}
            ]
        ))
    
    # === 5. Update layout with both button menus ===
    fig.update_layout(
        title='Rank Timeline - All Rounds',
        xaxis_title='Game Number (Continuous)',
        yaxis_title='Rank',
        height=600,
        template='plotly_white',
        showlegend=True,
        legend=dict(
            orientation='v',
            yanchor='top',
            y=1,
            xanchor='left',
            x=1.02
        ),
        updatemenus=[
            # Chart Type selector (Rang vs Gesamtpunktzahl)
            dict(
                buttons=chart_type_buttons,
                direction='down',
                showactive=True,
                x=0.01,
                xanchor='left',
                y=1.15,
                yanchor='top',
                bgcolor='lightblue',
                bordercolor='blue',
                borderwidth=1,
                font=dict(size=11)
            ),
            # Round filter selector
            dict(
                buttons=round_buttons,
                direction='down',
                showactive=True,
                x=0.15,
                xanchor='left',
                y=1.15,
                yanchor='top',
                bgcolor='lightgray',
                bordercolor='gray',
                borderwidth=1,
                font=dict(size=11)
            )
        ]
    )
    
    # Invert y-axis so rank 1 is at the top (for initial Rang view)
    fig.update_yaxes(autorange='reversed')
    
    # Save to HTML
    html_file = output_path / HTML_FILENAME
    fig.write_html(html_file)
    
    return html_file


def _add_rank_timeline_traces(fig, df_points, runden_id, trace_map, map_key):
    """Add rank timeline traces for a specific round or all rounds."""
    # Filter data if specific round
    df = df_points[df_points['runden_id'] == runden_id] if runden_id else df_points
    
    if df.empty:
        return
    
    # Group by player and plot rank over games
    for player in df['spieler'].unique():
        player_data = df[df['spieler'] == player].sort_values(['runden_id', 'spiel_index'])
        
        trace = go.Scatter(
            x=player_data['spiel_index'] if runden_id else range(len(player_data)),
            y=player_data['rang'],
            mode='lines+markers',
            name=player,
            visible=(map_key == 'all'),  # Only "All Rounds" visible by default
            showlegend=True
        )
        fig.add_trace(trace, row=1, col=1)
        
        # Track this trace for visibility toggling
        if map_key not in trace_map:
            trace_map[map_key] = []
        trace_map[map_key].append(len(fig.data) - 1)


def _add_cumulative_points_traces(fig, df_points, runden_id, trace_map, map_key):
    """Add cumulative points timeline traces."""
    df = df_points[df_points['runden_id'] == runden_id] if runden_id else df_points
    
    if df.empty:
        return
    
    # Calculate running sum of punkte_delta per player
    for player in df['spieler'].unique():
        player_data = df[df['spieler'] == player].sort_values(['runden_id', 'spiel_index'])
        cumsum = player_data['punkte_delta'].cumsum()
        
        trace = go.Scatter(
            x=list(range(len(cumsum))),
            y=list(cumsum),
            mode='lines+markers',
            name=player,
            visible=(map_key == 'all'),
            showlegend=False
        )
        fig.add_trace(trace, row=1, col=2)
        
        if map_key not in trace_map:
            trace_map[map_key] = []
        trace_map[map_key].append(len(fig.data) - 1)


def _add_running_points_traces(fig, df_points, runden_id, trace_map, map_key):
    """Add running points within a round (only for single round view)."""
    if not runden_id:
        return
    
    df = df_points[df_points['runden_id'] == runden_id]
    
    if df.empty:
        return
    
    for player in df['spieler'].unique():
        player_data = df[df['spieler'] == player].sort_values('spiel_index')
        
        trace = go.Scatter(
            x=list(player_data['spiel_index']),
            y=list(player_data['punktestand']),
            mode='lines+markers',
            name=player,
            visible=False,  # Hidden by default
            showlegend=False
        )
        fig.add_trace(trace, row=2, col=1)
        
        if map_key not in trace_map:
            trace_map[map_key] = []
        trace_map[map_key].append(len(fig.data) - 1)


def _add_podium_traces(fig, df_rounds, df_points, runden_id, trace_map, map_key):
    """Add podium visualizations for siegerpunkte and gesamtpunktzahl."""
    # Siegerpunkte Podium
    if runden_id:
        round_data = df_rounds[df_rounds['runden_id'] == runden_id]
    else:
        round_data = df_rounds
    
    # Extract player names and siegerpunkte
    siegerpunkte_data = {}
    for wind in ['osten', 'sueden', 'westen', 'norden']:
        player_col = f'spieler_{wind}'
        points_col = f'siegerpunkte_{wind}'
        
        if player_col in round_data.columns:
            for _, row in round_data.iterrows():
                player = row[player_col]
                points = row[points_col]
                siegerpunkte_data[player] = siegerpunkte_data.get(player, 0) + points
    
    # Sort by points
    sorted_players = sorted(siegerpunkte_data.items(), key=lambda x: x[1], reverse=True)
    
    if sorted_players:
        players, points = zip(*sorted_players)
        
        trace = go.Bar(
            x=list(players),
            y=list(points),
            name='Siegerpunkte',
            visible=(map_key == 'all'),
            marker_color='lightseagreen',
            showlegend=False
        )
        fig.add_trace(trace, row=2, col=2)
        
        if map_key not in trace_map:
            trace_map[map_key] = []
        trace_map[map_key].append(len(fig.data) - 1)
    
    # Gesamtpunktzahl Podium
    df = df_points[df_points['runden_id'] == runden_id] if runden_id else df_points
    
    if not df.empty:
        gesamtpunkte = df.groupby('spieler')['punkte_delta'].sum().sort_values(ascending=False)
        
        trace = go.Bar(
            x=gesamtpunkte.index,
            y=gesamtpunkte.values,
            name='Gesamtpunktzahl',
            visible=(map_key == 'all'),
            marker_color='coral',
            showlegend=False
        )
        fig.add_trace(trace, row=3, col=1)
        
        if map_key not in trace_map:
            trace_map[map_key] = []
        trace_map[map_key].append(len(fig.data) - 1)


def _create_filter_buttons(all_rounds, trace_map, fig):
    """Create filter buttons for round selection."""
    buttons = []
    
    # "All Rounds" button
    visibility = [False] * len(fig.data)
    for trace_idx in trace_map.get('all', []):
        visibility[trace_idx] = True
    
    buttons.append(
        dict(
            label='All Rounds',
            method='update',
            args=[
                {'visible': visibility},
                {'title': 'Mahjong Dashboard - All Rounds'}
            ]
        )
    )
    
    # Individual round buttons
    for round_info in all_rounds:
        runden_id = round_info['runden_id']
        dateiname = round_info['dateiname']
        
        visibility = [False] * len(fig.data)
        for trace_idx in trace_map.get(runden_id, []):
            visibility[trace_idx] = True
        
        buttons.append(
            dict(
                label=dateiname,
                method='update',
                args=[
                    {'visible': visibility},
                    {'title': f'Mahjong Dashboard - {dateiname}'}
                ]
            )
        )
    
    return buttons

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
