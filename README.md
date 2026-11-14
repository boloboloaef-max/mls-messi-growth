# The MLS Matchbook

A static, match-level study of MLS scoring and Lionel Messi's arrival in the league. The site covers completed matches from 2017 through 2025 and is generated into `docs/`.

## Build

Install Python 3 with `pandas` and `plotly`, then run:

```sh
python build_site.py
```

The builder reads the checked-in `mls_matches.csv` and creates four pages:

- `docs/index.html` — league overview and match-level scoring trajectory
- `docs/explorer.html` — club and season comparison with interactive filters
- `docs/inter-miami-story.html` — Inter Miami and the post-2023 scoring shift
- `docs/tactical-trends.html` — home advantage, outcomes and xG trends

## Data and scope

`mls_matches.csv` contains 4,088 completed match records. It combines the Major League Soccer rows from a 2023-01-01 archive of FiveThirtyEight's Club Soccer Predictions SPI match file with completed 2023–2025 MLS scoreboard events from ESPN. The original FiveThirtyEight CSV endpoint now redirects away from the dataset; the archived mirror is linked in the site footer. All-Star games are excluded.

Scores cover 2017–2025. Paired expected goals are available for 2,504 matches in the FiveThirtyEight archive (2017–2022); the ESPN supplement has no xG values. The site reports this limitation and does not impute missing xG. The comparisons are descriptive and do not establish that Messi, venue, or any other factor caused a change in results.
