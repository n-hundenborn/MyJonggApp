# Visualisierungsideen für das Mahjong Dashboard

Basierend auf der verfügbaren Datenstruktur - organisiert nach Erkenntniskategorien.

## **Spielerleistung & Spielstil**

1. **Verdopplungen Heatmap** - Zeigt wie aggressiv jeder Spieler Verdopplungen nutzt (Korrelation zwischen `verdopplungen` Anzahl und Erfolgsquote)

2. **Risikoprofil Streudiagramm** - Durchschnittliche `punkte_netto` vs. Volatilität (Standardabweichung) für jeden Spieler um konservative vs. aggressive Spieler zu zeigen

3. **Comeback Kings** - Verfolgt `rang` Änderungen innerhalb von Runden um zu identifizieren wer sich von schlechten Positionen erholt vs. wer die Führung hält

4. **Konsistenz Matrix** - Gestapeltes Balkendiagramm zeigt % der Spiele die jeder Spieler auf Rang 1-4 beendet

## **Positionsanalyse**

5. **Wind-Vorteil Analyse** - Gewinnrate aufgeschlüsselt nach `spieler_wind` Position (hat Ost/Dealer einen Vorteil?)

6. **Positions-Performance Heatmap** - Durchschnittliche `punkte_delta` je Spieler nach Wind-Position

7. **Dealer-Behalte-Rate** - Wie oft bleibt `wind_des_spiels` beim selben Spieler (erfolgreiche Verteidigungen)

## **Zeitliche Muster**

8. **Spieldauer Timeline** - Berechne `spielende - spielstart` und zeige Muster über `spiel_index` (werden Spiele schneller/langsamer?)

9. **Leistung nach Spielnummer** - Durchschnittliche `punkte_netto` nach `spiel_index` um zu sehen ob Ermüdung das Spiel beeinflusst

10. **Rundendauer Einfluss** - Korreliert `rundendauer` mit der Gesamtspanne der `siegerpunkte`?

## **Spieldynamik**

11. **Brutto vs. Netto Effizienz** - Streudiagramm: `punkte_brutto` vs. `punkte_netto` eingefärbt nach `verdopplungen` um Verdopplungseffektivität zu zeigen

12. **Punkteschwankungen Histogramm** - Verteilung von `punkte_delta` um typische Gewinne/Verluste zu zeigen

13. **Führungswechsel Timeline** - Animiere `rang` Änderungen während einer Runde

## **Direktvergleiche**

14. **Spieler Matchup Matrix** - Wenn zwei bestimmte Spieler in der gleichen Runde sind, wer tendiert dazu höher zu landen?

15. **Gewinner Analyse** - Vergleiche `gewinner_wind` Verteilung mit den erwarteten 25% pro Position

## **Implementierungsvorschläge**

Die interessantesten Visualisierungen für die nächsten Dashboard-Erweiterungen:

### Priorität 1 (Sofort umsetzbar)
- **Verdopplungen Heatmap** (Idee 1)
- **Konsistenz Matrix** (Idee 4)
- **Wind-Vorteil Analyse** (Idee 5)

### Priorität 2 (Mittelfristig)
- **Risikoprofil Streudiagramm** (Idee 2)
- **Positions-Performance Heatmap** (Idee 6)
- **Punkteschwankungen Histogramm** (Idee 12)

### Priorität 3 (Langfristig / Fortgeschritten)
- **Comeback Kings** (Idee 3)
- **Führungswechsel Timeline** (Idee 13)
- **Spieler Matchup Matrix** (Idee 14)

## Nächste Schritte

Welche 2-3 dieser Visualisierungen wären am interessantesten für die Mahjong-Gruppe?
