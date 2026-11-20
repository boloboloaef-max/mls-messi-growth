# The MLS Matchbook

A static, match-level study of MLS scoring and Lionel Messi's arrival in the league. The site covers completed matches from 2017 through 2025 and is generated into `docs/`.

## Build

Install Python 3 with `pandas` and `plotly`, then run:

```sh
python build_site.py
```

The builder reads the checked-in `mls_matches.csv` and creates six pages:

- `docs/index.html` — executive overview and league trends
- `docs/scoring-xg.html` — observed goals, expected goals and finishing margins
- `docs/messi-impact.html` — Inter Miami before/after July 21, 2023
- `docs/clubs-dynamics.html` — club attack, defense and home-field patterns
- `docs/explorer.html` — interactive team, season and match-record explorer
- `docs/about.html` — author, project links and data source

## Data and scope

`mls_matches.csv` contains 4,088 completed match records, 12,124 goals and 2,504 matches with complete paired xG, across nine seasons from 2017 through 2025. It combines the Major League Soccer rows from a 2023-01-01 archive of FiveThirtyEight's Club Soccer Predictions SPI match file with completed 2023–2025 MLS scoreboard events from ESPN. All-Star games are excluded.

Scores cover 2017–2025. Paired expected goals are available for 2,504 matches in the FiveThirtyEight archive (2017–2022); the ESPN supplement has no xG values. The site reports this limitation and does not impute missing xG. The comparisons are descriptive and do not establish that Messi, venue, or any other factor caused a change in results.
