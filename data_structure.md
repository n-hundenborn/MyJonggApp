# Datenstruktur Dokumentation

## Übersicht

Dieses Dokument beschreibt die Datenstruktur bestehend aus drei Tabellen mit unterschiedlichen Granularitäten: Runden-Metadaten, Spiel-Metadaten und Spiel-Punkteverteilung.

## Tabellenstruktur

### 1. Runden-Metadaten (Runden-Ebene)

**Granularität**: Eine Zeile pro Runde  
**Eindeutiger Schlüssel**: `runden_id`

| Spaltenname | Typ | Beschreibung |
|-------------|------|-------------|
| `runden_id` | Primärschlüssel | Eindeutiger Bezeichner für jede Runde |
| `dateiname` | String | Zugehöriger Dateiname |
| `rundenstart` | DateTime | Startzeitpunkt der Runde |
| `rundenende` | DateTime | Endzeitpunkt der Runde |
| `rundendauer` | Dauer | Gesamtdauer der Runde |
| `'rundendauer_text'` | Dauer | Gesamtdauer der Runde formatiert |
| `spieler_osten` | String | Name des Ost-Spielers |
| `siegerpunkte_osten` | Integer | Gesamtpunkte des Ost-Spielers |
| `spieler_sueden` | String | Name des Süd-Spielers |
| `siegerpunkte_sueden` | Integer | Gesamtpunkte des Süd-Spielers |
| `spieler_westen` | String | Name des Westen-Spielers |
| `siegerpunkte_westen` | Integer | Gesamtpunkte des Westen-Spielers |
| `spieler_norden` | String | Name des Nord-Spielers |
| `siegerpunkte_norden` | Integer | Gesamtpunkte des Nord-Spielers |

**Beziehungen**:
- Eine Runde enthält mehrere Spiele (1:N mit Spiel-Metadaten)

---

### 2. Spiel-Metadaten (Spiel-Ebene)

**Granularität**: Eine Zeile pro Spiel  
**Eindeutiger Schlüssel**: `runden_id` + `spiel_index`

| Spaltenname | Typ | Beschreibung |
|-------------|------|-------------|
| `runden_id` | Fremdschlüssel | Referenziert Runden-Metadaten |
| `spiel_index` | Integer | Fortlaufende Spielnummer innerhalb der Runde |
| `wind_des_spiels` | String | Führer für dieses Spiel (Ost, Süd, westen, Nord) |
| `gewinner_wind` | String | Wind des Gewinners (Ost, Süd, westen, Nord) |
| `spielstart` | DateTime | Startzeitpunkt des Spiels |
| `spielende` | DateTime | Endzeitpunkt des Spiels |

**Beziehungen**:
- Mehrere Spiele pro Runde (N:1 mit Runden-Metadaten)
- Ein Spiel hat mehrere Punkteverteilungen (1:N mit Spiel-Punkteverteilung)

---

### 3. Spiel-Punkteverteilung (Spiel-Spieler-Ebene)

**Granularität**: Eine Zeile pro Spieler pro Spiel  
**Eindeutiger Schlüssel**: `runden_id` + `spiel_index` + `spieler`

| Spaltenname | Typ | Beschreibung |
|-------------|------|-------------|
| `runden_id` | Fremdschlüssel | Referenziert Runden-Metadaten |
| `spiel_index` | Integer | Fortlaufende Spielnummer innerhalb der Runde |
| `spieler` | String | Spielername |
| `spieler_wind` | String | Wind des Spielers (Ost, Süd, West, Nord) |
| `punkte_brutto` | Integer | Bruttopunkte vor Verdopplungen |
| `verdopplungen` | Integer | Anzahl der Verdopplungen |
| `punkte_netto` | Integer | Nettopunkte nach Verdopplungen |
| `punkte_delta` | Integer | Punkteveränderung für diesen Spieler in diesem Spiel |
| `punktestand` | Integer | Kumulierter Punktestand des Spielers nach diesem Spiel |
| `rang` | Integer | Rang des Spielers nach diesem Spiel |

**Beziehungen**:
- Mehrere Zeilen pro Spiel (N:1 mit Spiel-Metadaten)
- Mehrere Zeilen pro Runde (N:1 mit Runden-Metadaten)

---

## Entity-Relationship-Diagramm

```
┌─────────────────────────────┐
│   Runden-Metadaten          │
│  (runden_id)                │
│  - dateiname                │
│  - rundenstart              │
│  - rundenende               │
│  - rundendauer              │
│  - spieler_osten            │
│  - siegerpunkte_osten       │
│  - ...                      │
└───────────┬─────────────────┘
            │ 1
            │
            │ N
┌───────────┴─────────────────┐
│   Spiel-Metadaten           │
│  (runden_id +               │
│   spiel_index)              │
│  - wind_des_spiels          │
│  - gewinner_wind            │
│  - spielstart               │
│  - spielende                │
└───────────┬─────────────────┘
            │ 1
            │
            │ N
┌───────────┴─────────────────┐
│  Spiel-Punktevert.          │
│  (runden_id +               │
│   spiel_index + spieler)    │
│  - spieler_wind             │
│  - punkte_brutto            │
│  - verdopplungen            │
│  - punkte_netto             │
│  - punkte_delta             │
│  - punktestand              │
│  - rang                     │
└─────────────────────────────┘
```

## Datenhierarchie

```
Runde (runden_id)
  └── Spiel 1 (spiel_index = 1)
      ├── Spieler A (Ost): punkte_delta, punktestand, rang
      ├── Spieler B (Süd): punkte_delta, punktestand, rang
      ├── Spieler C (West): punkte_delta, punktestand, rang
      └── Spieler D (Nord): punkte_delta, punktestand, rang
  └── Spiel 2 (spiel_index = 2)
      ├── Spieler A (Ost): punkte_delta, punktestand, rang
      ├── Spieler B (Süd): punkte_delta, punktestand, rang
      ├── Spieler C (West): punkte_delta, punktestand, rang
      └── Spieler D (Nord): punkte_delta, punktestand, rang
  └── Spiel N (spiel_index = N)
      └── ...
```

## Wichtige Beziehungen

1. **Runde → Spiel**: Eins-zu-Viele
   - Jede Runde (`runden_id`) enthält mehrere Spiele
   - Jedes Spiel wird durch `runden_id` + `spiel_index` identifiziert

2. **Spiel → Punkteverteilung**: Eins-zu-Viele
   - Jedes Spiel hat mehrere Punkteeinträge (typischerweise einen pro Spieler)
   - Jeder Punkteeintrag wird durch `runden_id` + `spiel_index` + `spieler` identifiziert

3. **Runde → Punkteverteilung**: Eins-zu-Viele (indirekt)
   - Über die Spiel-Beziehung

## Beispieldaten

### Runden-Metadaten
| runden_id | dateiname | rundenstart | rundenende | rundendauer | spieler_osten | siegerpunkte_osten |
|-----------|----------|------------|----------|----------|-------------|-------------------|
| R001 | game_2025_01.txt | 2025-01-15 14:00 | 2025-01-15 16:30 | 02:30:00 | Alice | 45000 |

### Spiel-Metadaten
| runden_id | spiel_index | wind_des_spiels | gewinner_wind | spielstart | spielende |
|-----------|-----------|---------------|--------|------------|----------|
| R001 | 1 | Ost | Ost | 2025-01-15 14:00 | 2025-01-15 14:20 |
| R001 | 2 | Ost | Süd | 2025-01-15 14:22 | 2025-01-15 14:45 |

### Spiel-Punkteverteilung
| runden_id | spiel_index | wind_des_spiels | gewinner_wind | spieler | spieler_wind | punkte_brutto | verdopplungen | punkte_netto | punkte_delta | punktestand | rang |
|-----------|-------------|-----------------|---------------|---------|--------------|---------------|---------------|--------------|--------------|-------------|------|
| R001 | 1 | Ost | Ost | Alice | Ost | 4000 | 1 | 8000 | 8000 | 33000 | 1 |
| R001 | 1 | Ost | Ost | Bob | Süd | 1000 | 1 | -2000 | -2000 | 23000 | 3 |
| R001 | 1 | Ost | Ost | Carol | West | 1500 | 1 | -3000 | -3000 | 22000 | 4 |
| R001 | 1 | Ost | Ost | Dave | Nord | 1500 | 1 | -3000 | -3000 | 25000 | 2 |
| R001 | 2 | Ost | Süd | Alice | Ost | 500 | 0 | -1000 | -1000 | 32000 | 1 |
| R001 | 2 | Ost | Süd | Bob | Süd | 2500 | 1 | 5000 | 5000 | 28000 | 2 |
| R001 | 2 | Ost | Süd | Carol | West | 1000 | 1 | -2000 | -2000 | 20000 | 4 |
| R001 | 2 | Ost | Süd | Dave | Nord | 1000 | 1 | -2000 | -2000 | 23000 | 3 |
