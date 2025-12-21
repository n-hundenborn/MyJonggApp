# Plan: Interactive HTML Dashboard mit 3-Tabellen-Struktur

Umbau der Evaluation auf ein interaktives HTML-Dashboard (statisch, kein Server nötig) mit getrennten DataFrames für Runden-, Spiel- und Spieler-Granularität. Nutzt Plotly's `updatemenus` und `buttons` für Client-seitige Filterung nach einzelnen Runden. Zeigt Timelines für Ränge, Punktestände und Gewinner-Podien.

## Steps

1. **Refactor [get_dataframe_from_folder](src/backend/evaluation/transformations.py)** um 3 separate DataFrames zurückzugeben: `df_rounds` (Runden-Metadaten mit `runden_id`, `dateiname`, `rundenstart`, `rundenende`, `rundendauer`, `spieler_osten/sueden/westen/norden`, `siegerpunkte_osten/sueden/westen/norden`), `df_games` (Spiel-Metadaten mit `runden_id`, `spiel_index`, `wind_des_spiels`, `gewinner_wind`, `spielstart`, `spielende`), `df_points` (Punkteverteilung mit `runden_id`, `spiel_index`, `spieler`, `spieler_wind`, `punkte_brutto`, `verdopplungen`, `punkte_netto`, `punkte_delta`, `punktestand`, `rang`) gemäß [data_structure.md](data_structure.md)

2. **Create new visualization function** in [visualization.py](src/backend/evaluation/visualization.py): Refactor `create_html_dashboard` zu `create_interactive_html_dashboard(df_rounds, df_games, df_points, output_path)` die die 3 DataFrames entgegennimmt

3. **Implement round filter with Plotly updatemenus** im HTML: Nutze `fig.update_layout(updatemenus=[...])` mit Buttons für jede Runde ("All Rounds" + eine Option pro `runden_id`). Jeder Button toggled die Sichtbarkeit (`visible`) der entsprechenden Traces für die jeweilige Runde. Pre-generiere alle Traces für alle Runden, die dann per Button ein-/ausgeblendet werden

4. **Create timeline charts** mit `make_subplots` und `go.Scatter`: Rang-Timeline (X: `spiel_index` kombiniert über Runden mit fortlaufendem Index, Y: `rang`, eine Line pro `spieler` aus `df_points`), Gesamtpunktzahl-Timeline (Running Sum von `punkte_delta` pro `spieler` über alle Spiele berechnet mit `cumsum()`), Siegerpunkte-Timeline (nur bei Einzelrunden-Ansicht: Running Sum der Siegerpunkte pro Spieler innerhalb der Runde aus `df_points.punktestand` gefiltert)

5. **Create podium visualization** mit custom Plotly Figure (4 Bars in Podiumsform: 2nd/1st/3rd/4th Platzierung): Ein Podium für Gewinner nach Siegerpunkten (Summe aller `siegerpunkte_*` Spalten aus `df_rounds` gruppiert nach Spielername), ein Podium für Gewinner nach Gesamtpunktzahl (Summe aller `punkte_delta` aus `df_points` gruppiert nach `spieler`)

6. **Update [orchestrator.py](src/backend/evaluation/orchestrator.py)** um die 3 DataFrames von `get_dataframe_from_folder` zu empfangen und `create_interactive_html_dashboard(df_rounds, df_games, df_points, output_path)` zu callen. Gibt wie bisher den Pfad zum generierten HTML-File zurück

## Further Considerations

1. **Trace-Generierung für alle Runden:** Da alle Traces pre-generiert werden, kann bei vielen Runden (>20) die HTML-Datei groß werden (>5MB). Ist das akzeptabel oder soll ein Limit gesetzt werden?

2. **Interaktivitäts-Limitierung:** Plotly `updatemenus` erlauben nur Button-basierte Filterung (kein Dropdown wie in Dash). Multiple Selection (mehrere Runden gleichzeitig) ist nicht out-of-the-box möglich. Soll das erweitert werden mit Custom JavaScript?

3. **Layout & Styling:** Plotly-Templates vorgeschlagen (`plotly`, `plotly_white`, `plotly_dark`). Welches Theme bevorzugen Sie?
