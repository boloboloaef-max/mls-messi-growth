from __future__ import annotations

import html
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


ROOT = Path(__file__).resolve().parent
DOCS = ROOT / "docs"
DATA_PATH = ROOT / "mls_matches.csv"
REQUIRED_COLUMNS = {
    "season",
    "date",
    "league",
    "team1",
    "team2",
    "score1",
    "score2",
    "xg1",
    "xg2",
    "source",
}

NAV_ITEMS = [
    ("index.html", "Home"),
    ("explorer.html", "Club & Season Explorer"),
    ("inter-miami-story.html", "The Inter Miami Turning Point"),
    ("tactical-trends.html", "Home Advantage & Scoring Trends"),
]

STYLE = """
<style>
  :root {
    color-scheme: light;
    --ink: #13231f;
    --muted: #566862;
    --paper: #f5f6f1;
    --card: #ffffff;
    --line: #dce3dc;
    --forest: #174e3c;
    --lime: #d9f36a;
    --coral: #e85c4a;
    --shadow: 0 16px 44px rgba(21, 48, 37, .08);
  }
  * { box-sizing: border-box; }
  body {
    margin: 0;
    background: var(--paper);
    color: var(--ink);
    font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont,
      "Segoe UI", sans-serif;
    -webkit-font-smoothing: antialiased;
  }
  a { color: inherit; }
  .site-header {
    position: sticky;
    z-index: 20;
    top: 0;
    background: rgba(19, 35, 31, .97);
    color: #fff;
    box-shadow: 0 5px 24px rgba(0, 0, 0, .12);
  }
  .nav-wrap {
    width: min(1240px, calc(100% - 48px));
    min-height: 76px;
    margin: 0 auto;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 24px;
  }
  .brand {
    flex: 0 0 auto;
    color: #fff;
    font-size: 13px;
    font-weight: 800;
    letter-spacing: .12em;
    line-height: 1.25;
    text-decoration: none;
    text-transform: uppercase;
  }
  .brand span { display: block; color: var(--lime); font-size: 10px; }
  .nav-links { display: flex; align-items: center; gap: 7px; }
  .nav-links a {
    border-radius: 999px;
    color: #e2e8e4;
    font-size: 12px;
    font-weight: 650;
    padding: 10px 12px;
    text-decoration: none;
    white-space: nowrap;
  }
  .nav-links a:hover, .nav-links a[aria-current="page"] {
    background: rgba(217, 243, 106, .14);
    color: var(--lime);
  }
  main { min-height: calc(100vh - 190px); }
  .wrap { width: min(1120px, calc(100% - 48px)); margin: 0 auto; }
  .hero { padding: 72px 0 34px; }
  .eyebrow {
    color: var(--forest);
    font-size: 11px;
    font-weight: 850;
    letter-spacing: .16em;
    text-transform: uppercase;
  }
  h1 {
    max-width: 930px;
    margin: 15px 0 18px;
    font-size: clamp(38px, 6vw, 70px);
    letter-spacing: -.055em;
    line-height: .99;
  }
  h2 { margin: 0 0 12px; font-size: clamp(24px, 3.2vw, 34px); letter-spacing: -.035em; }
  h3 { margin: 0 0 9px; font-size: 18px; letter-spacing: -.02em; }
  p { color: #34443e; font-size: 16px; line-height: 1.75; }
  .dek { max-width: 780px; margin: 0; color: var(--muted); font-size: 18px; line-height: 1.7; }
  .section { padding: 24px 0 44px; }
  .section-heading {
    display: flex;
    align-items: end;
    justify-content: space-between;
    gap: 24px;
    margin-bottom: 18px;
  }
  .section-heading p { max-width: 650px; margin: 0; color: var(--muted); }
  .kpis {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 14px;
    margin: 18px 0 32px;
  }
  .kpi, .panel, .chart-card, .table-card, .story-copy {
    border: 1px solid var(--line);
    border-radius: 18px;
    background: var(--card);
    box-shadow: var(--shadow);
  }
  .kpi { min-height: 143px; padding: 20px; }
  .kpi-label { color: var(--muted); font-size: 12px; font-weight: 750; line-height: 1.4; }
  .kpi-value { margin: 13px 0 5px; font-size: clamp(27px, 3vw, 37px); font-weight: 830; letter-spacing: -.055em; }
  .kpi-note { color: #718078; font-size: 11px; line-height: 1.45; }
  .chart-card { overflow: hidden; padding: 13px 13px 4px; }
  .chart-caption {
    display: flex;
    justify-content: space-between;
    gap: 18px;
    padding: 13px 15px 15px;
    color: var(--muted);
    font-size: 12px;
    line-height: 1.55;
  }
  .chart-caption strong { color: var(--ink); }
  .panel { padding: 24px; }
  .controls {
    display: flex;
    flex-wrap: wrap;
    align-items: end;
    gap: 14px 20px;
    margin: 21px 0 16px;
  }
  .control-label {
    display: block;
    margin-bottom: 7px;
    color: var(--muted);
    font-size: 11px;
    font-weight: 800;
    letter-spacing: .08em;
    text-transform: uppercase;
  }
  select {
    min-width: 250px;
    border: 1px solid #cbd6ce;
    border-radius: 10px;
    background: #fff;
    color: var(--ink);
    font: inherit;
    font-size: 14px;
    padding: 11px 38px 11px 13px;
  }
  .button-group { display: flex; gap: 6px; }
  .filter-button {
    border: 1px solid #cbd6ce;
    border-radius: 999px;
    background: #fff;
    color: var(--ink);
    cursor: pointer;
    font: inherit;
    font-size: 12px;
    font-weight: 750;
    padding: 10px 14px;
  }
  .filter-button[aria-pressed="true"] { border-color: var(--forest); background: var(--forest); color: #fff; }
  .filter-button:focus-visible, select:focus-visible, a:focus-visible {
    outline: 3px solid var(--coral);
    outline-offset: 3px;
  }
  .table-wrap { overflow-x: auto; }
  table { width: 100%; border-collapse: collapse; font-size: 13px; }
  th, td { padding: 13px 14px; border-bottom: 1px solid #e8ede8; text-align: left; white-space: nowrap; }
  th { position: sticky; top: 0; background: #f1f5f0; color: #53635b; font-size: 10px; letter-spacing: .08em; text-transform: uppercase; }
  td.num, th.num { text-align: right; }
  tbody tr:hover { background: #f8faf6; }
  .story-copy { margin: 22px 0 34px; padding: 24px 30px; }
  .story-copy p { margin: 0 0 16px; }
  .story-copy p:last-child { margin-bottom: 0; }
  .data-note {
    margin: 22px 0 36px;
    border-left: 4px solid var(--forest);
    background: #eaf0e8;
    color: #45554e;
    font-size: 13px;
    line-height: 1.7;
    padding: 14px 17px;
  }
  .data-note a { color: var(--forest); font-weight: 700; }
  .site-footer { margin-top: 40px; background: #13231f; color: #d5dfd9; }
  .footer-inner {
    width: min(1120px, calc(100% - 48px));
    margin: 0 auto;
    padding: 24px 0 30px;
    display: flex;
    justify-content: space-between;
    gap: 20px;
    font-size: 11px;
    line-height: 1.7;
  }
  .footer-inner a { color: var(--lime); }
  .plotly-graph-div { width: 100% !important; }
  @media (max-width: 900px) {
    .nav-wrap { align-items: flex-start; flex-direction: column; gap: 10px; padding: 17px 0; }
    .nav-links { width: 100%; overflow-x: auto; padding-bottom: 2px; }
    .nav-links a { flex: 0 0 auto; }
    .hero { padding-top: 48px; }
    .kpis { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  }
  @media (max-width: 560px) {
    .wrap, .nav-wrap, .footer-inner { width: min(100% - 30px, 1120px); }
    .kpis { gap: 9px; }
    .kpi { min-height: 126px; padding: 15px; }
    .kpi-value { font-size: 28px; }
    .section-heading { align-items: flex-start; flex-direction: column; }
    .chart-card { padding: 5px 5px 0; }
    .chart-caption { flex-direction: column; }
    .panel { padding: 16px; }
    .story-copy { padding: 20px; }
    select { min-width: min(100%, 290px); }
    .footer-inner { flex-direction: column; }
  }
</style>
"""


def load_matches() -> pd.DataFrame:
    if not DATA_PATH.is_file():
        raise FileNotFoundError(f"Required local match dataset not found: {DATA_PATH}")
    matches = pd.read_csv(DATA_PATH)
    missing_columns = REQUIRED_COLUMNS - set(matches.columns)
    if missing_columns:
        raise ValueError(f"Dataset is missing columns: {', '.join(sorted(missing_columns))}")
    matches = matches.loc[matches["league"].eq("Major League Soccer")].copy()
    if len(matches) < 1_000:
        raise ValueError(f"Expected thousands of MLS matches; found only {len(matches):,}.")

    matches["date"] = pd.to_datetime(matches["date"], errors="raise")
    matches["season"] = pd.to_numeric(matches["season"], errors="raise").astype(int)
    for column in ("score1", "score2", "xg1", "xg2"):
        matches[column] = pd.to_numeric(matches[column], errors="coerce")
    if matches[["score1", "score2"]].isna().any().any():
        raise ValueError("Every match must have a recorded home and away score.")
    if (matches[["score1", "score2"]] < 0).any().any():
        raise ValueError("Match scores cannot be negative.")
    if matches["source"].isna().any():
        raise ValueError("Every match must have source attribution.")

    matches["total_goals"] = matches["score1"] + matches["score2"]
    matches["xg_complete"] = matches[["xg1", "xg2"]].notna().all(axis=1)
    matches["total_xg"] = matches[["xg1", "xg2"]].sum(axis=1, min_count=2)
    matches["home_xg"] = matches["xg1"].where(matches["xg_complete"])
    matches["away_xg"] = matches["xg2"].where(matches["xg_complete"])
    if not matches["xg_complete"].any():
        raise ValueError("The dataset has no complete expected-goals observations.")
    return matches.sort_values(["date", "team1", "team2"]).reset_index(drop=True)


def site_nav(active_page: str) -> str:
    links = "".join(
        f'<a href="{href}"'
        f'{" aria-current=\"page\"" if href == active_page else ""}>{html.escape(label)}</a>'
        for href, label in NAV_ITEMS
    )
    return f"""
<header class="site-header">
  <div class="nav-wrap">
    <a class="brand" href="index.html">The MLS Matchbook<span>US Soccer · Data &amp; analysis</span></a>
    <nav class="nav-links" aria-label="Main navigation">{links}</nav>
  </div>
</header>
"""


def page(title: str, active_page: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="A match-by-match study of MLS scoring, club performance and Lionel Messi's impact.">
  <title>{html.escape(title)} | The MLS Matchbook</title>
  {STYLE.strip()}
</head>
<body>
  {site_nav(active_page).strip()}
  <main>{body}</main>
  <footer class="site-footer">
    <div class="footer-inner">
      <div>Matchbook · An observational look at MLS, 2017–2025.<br>Scores describe what happened; they do not establish why.</div>
      <div>Data: <a href="https://github.com/naspli/dataviz/tree/master/soccer-spi/data-20230101">FiveThirtyEight SPI archive</a>
      · <a href="https://site.api.espn.com/apis/site/v2/sports/soccer/usa.1/scoreboard?dates=2025&amp;limit=1000">ESPN MLS scoreboard</a></div>
    </div>
  </footer>
</body>
</html>
"""


def plot_html(
    figure: go.Figure,
    div_id: str,
    *,
    static: bool = False,
    height: int = 570,
) -> str:
    figure.update_layout(
        template="plotly_white",
        height=height,
        autosize=True,
        margin=dict(l=56, r=28, t=48, b=55),
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(family="Inter, system-ui, sans-serif", color="#263b33", size=12),
        hoverlabel=dict(bgcolor="#13231f", font_color="white"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0),
    )
    return figure.to_html(
        full_html=False,
        include_plotlyjs="cdn",
        div_id=div_id,
        config={
            "responsive": True,
            "displaylogo": False,
            "displayModeBar": not static,
            "staticPlot": static,
        },
    )


def home_figure(matches: pd.DataFrame) -> go.Figure:
    figure = go.Figure()
    hover = matches[["team1", "team2", "score1", "score2"]].to_numpy()
    figure.add_trace(
        go.Scattergl(
            x=matches["date"],
            y=matches["total_goals"],
            customdata=hover,
            mode="markers",
            name="Match goals · all records",
            marker=dict(color="#174e3c", size=5, opacity=0.2),
            hovertemplate=(
                "%{x|%b %d, %Y}<br>%{customdata[0]} – %{customdata[1]}"
                "<br>Score: %{customdata[2]:.0f}–%{customdata[3]:.0f}"
                "<br>Total goals: %{y:.0f}<extra></extra>"
            ),
        )
    )

    xg_matches = matches.loc[matches["xg_complete"]]
    xg_hover = xg_matches[["team1", "team2", "xg1", "xg2"]].to_numpy()
    figure.add_trace(
        go.Scattergl(
            x=xg_matches["date"],
            y=xg_matches["total_xg"],
            customdata=xg_hover,
            mode="markers",
            name="Expected goals · complete xG records",
            marker=dict(color="#e85c4a", size=5, opacity=0.16, symbol="diamond"),
            hovertemplate=(
                "%{x|%b %d, %Y}<br>%{customdata[0]} – %{customdata[1]}"
                "<br>Home xG: %{customdata[2]:.2f}"
                "<br>Away xG: %{customdata[3]:.2f}"
                "<br>Combined xG: %{y:.2f}<extra></extra>"
            ),
        )
    )

    by_season = matches.groupby("season", as_index=False).agg(
        avg_goals=("total_goals", "mean")
    )
    xg_by_season = (
        xg_matches.groupby("season", as_index=False)
        .agg(avg_xg=("total_xg", "mean"))
    )
    by_season["season_date"] = pd.to_datetime(by_season["season"].astype(str) + "-07-01")
    xg_by_season["season_date"] = pd.to_datetime(
        xg_by_season["season"].astype(str) + "-07-01"
    )
    figure.add_trace(
        go.Scatter(
            x=by_season["season_date"],
            y=by_season["avg_goals"],
            mode="lines+markers",
            name="Season average · goals",
            line=dict(color="#174e3c", width=3),
            marker=dict(size=8),
            hovertemplate="Season %{x|%Y}<br>Goals per match: %{y:.2f}<extra></extra>",
        )
    )
    figure.add_trace(
        go.Scatter(
            x=xg_by_season["season_date"],
            y=xg_by_season["avg_xg"],
            mode="lines+markers",
            name="Season average · xG",
            line=dict(color="#e85c4a", width=3, dash="dash"),
            marker=dict(size=8, symbol="diamond"),
            hovertemplate="Season %{x|%Y}<br>Expected goals per match: %{y:.2f}<extra></extra>",
        )
    )
    figure.update_layout(
        title=dict(text="Every match, one changing scoring story", x=0.02, xanchor="left"),
        xaxis=dict(title="Match date", rangeslider=dict(visible=True), showgrid=False),
        yaxis=dict(title="Combined goals or expected goals per match", rangemode="tozero"),
        hovermode="closest",
    )
    return figure


def team_performance(matches: pd.DataFrame) -> pd.DataFrame:
    home = pd.DataFrame(
        {
            "season": matches["season"],
            "club": matches["team1"],
            "venue": "Home",
            "goals_for": matches["score1"],
            "goals_against": matches["score2"],
            "xg_for": matches["home_xg"],
        }
    )
    away = pd.DataFrame(
        {
            "season": matches["season"],
            "club": matches["team2"],
            "venue": "Away",
            "goals_for": matches["score2"],
            "goals_against": matches["score1"],
            "xg_for": matches["away_xg"],
        }
    )
    long = pd.concat([home, away], ignore_index=True)
    long["win"] = long["goals_for"] > long["goals_against"]
    grouped = (
        long.groupby(["season", "club", "venue"], as_index=False)
        .agg(
            matches=("goals_for", "size"),
            wins=("win", "sum"),
            goals_per_match=("goals_for", "mean"),
            xg_per_match=("xg_for", "mean"),
            xg_matches=("xg_for", "count"),
        )
    )
    grouped["win_rate"] = grouped["wins"] / grouped["matches"] * 100
    return grouped


def explorer_figure(performance: pd.DataFrame, clubs: list[str]) -> go.Figure:
    palette = px.colors.qualitative.Alphabet
    color_map = {club: palette[i % len(palette)] for i, club in enumerate(clubs)}
    color_map["Inter Miami CF"] = "#e85c4a"
    figure = go.Figure()
    default_club = "Inter Miami CF" if "Inter Miami CF" in clubs else clubs[0]
    for club in clubs:
        for venue in ("Home", "Away"):
            group = performance.loc[
                (performance["club"] == club) & (performance["venue"] == venue)
            ].sort_values("season")
            customdata = [
                [
                    int(row.matches),
                    row.win_rate,
                    f"{row.xg_per_match:.2f}" if pd.notna(row.xg_per_match) else "not available",
                    int(row.xg_matches),
                ]
                for row in group.itertuples()
            ]
            figure.add_trace(
                go.Scatter(
                    x=group["season"],
                    y=group["goals_per_match"],
                    customdata=customdata,
                    mode="lines+markers",
                    name=f"{club} · {venue.lower()}",
                    meta={"club": club, "venue": venue},
                    visible=club == default_club,
                    line=dict(
                        color=color_map[club],
                        width=3 if club == default_club else 2,
                        dash="solid" if venue == "Home" else "dash",
                    ),
                    marker=dict(size=8, symbol="circle" if venue == "Home" else "square"),
                    hovertemplate=(
                        "Season %{x}<br>Venue: "
                        + venue.lower()
                        + "<br>Average goals scored: %{y:.2f}"
                        "<br>Win rate: %{customdata[1]:.1f}%"
                        "<br>Average xG: %{customdata[2]}"
                        "<br>Matches with xG: %{customdata[3]} of %{customdata[0]}"
                        "<br>Matches: %{customdata[0]}<extra></extra>"
                    ),
                )
            )
    figure.update_layout(
        title=dict(text="Season-by-season club output", x=0.02, xanchor="left"),
        xaxis=dict(
            title="Season",
            dtick=1,
            rangeslider=dict(visible=True),
            range=[min(performance["season"]), max(performance["season"])],
        ),
        yaxis=dict(title="Goals scored per match", rangemode="tozero"),
        hovermode="closest",
        showlegend=False,
    )
    return figure


def club_table(matches: pd.DataFrame, clubs: list[str]) -> str:
    rows = []
    for club in clubs:
        home = matches.loc[matches["team1"].eq(club)]
        away = matches.loc[matches["team2"].eq(club)]
        games = len(home) + len(away)
        wins = int((home["score1"] > home["score2"]).sum()) + int(
            (away["score2"] > away["score1"]).sum()
        )
        goals = int(home["score1"].sum() + away["score2"].sum())
        xg_total = float(home["home_xg"].sum() + away["away_xg"].sum())
        xg_games = int(home["home_xg"].count() + away["away_xg"].count())
        goals_avg = goals / games if games else 0
        xg_avg = f"{xg_total / xg_games:.2f}" if xg_games else "—"
        rows.append(
            (club, games, f"{wins / games:.1%}" if games else "—", f"{goals_avg:.2f}", xg_avg, xg_games)
        )
    rows.sort(key=lambda row: (-row[1], row[0]))
    body = "".join(
        "<tr>"
        f"<td>{html.escape(club)}</td>"
        f'<td class="num">{games:,}</td>'
        f'<td class="num">{win_rate}</td>'
        f'<td class="num">{goals_avg}</td>'
        f'<td class="num">{xg_avg}</td>'
        f'<td class="num">{xg_games:,}</td>'
        "</tr>"
        for club, games, win_rate, goals_avg, xg_avg, xg_games in rows
    )
    return f"""
<div class="table-wrap">
  <table>
    <thead><tr>
      <th>Club</th><th class="num">Matches</th><th class="num">Win rate</th>
      <th class="num">Goals / match</th><th class="num">xG / match</th><th class="num">xG matches</th>
    </tr></thead>
    <tbody>{body}</tbody>
  </table>
</div>
"""


def explorer_script() -> str:
    return """
<script>
(() => {
  const chart = document.getElementById("club-chart");
  const clubSelect = document.getElementById("club-select");
  const buttons = [...document.querySelectorAll("[data-venue-filter]")];
  let venueFilter = "Both";

  function applyFilters() {
    const selectedClub = clubSelect.value;
    const visibility = chart.data.map((trace) =>
      trace.meta.club === selectedClub &&
      (venueFilter === "Both" || trace.meta.venue === venueFilter)
    );
    Plotly.restyle(chart, { visible: visibility });
  }

  clubSelect.addEventListener("change", applyFilters);
  buttons.forEach((button) => {
    button.addEventListener("click", () => {
      venueFilter = button.dataset.venueFilter;
      buttons.forEach((item) =>
        item.setAttribute("aria-pressed", String(item === button))
      );
      applyFilters();
    });
  });
  applyFilters();
})();
</script>
"""


def inter_miami_figure(matches: pd.DataFrame) -> go.Figure:
    recent = matches.loc[matches["season"].between(2020, 2025)].copy()
    recent["group"] = "Rest of MLS"
    recent.loc[
        recent["team1"].eq("Inter Miami CF") | recent["team2"].eq("Inter Miami CF"),
        "group",
    ] = "Inter Miami fixtures"
    summary = (
        recent.groupby(["season", "group"], as_index=False)
        .agg(matches=("total_goals", "size"), goals=("total_goals", "mean"))
    )
    xg_summary = (
        recent.loc[recent["xg_complete"]]
        .groupby(["season", "group"], as_index=False)
        .agg(xg_matches=("total_xg", "size"), xg=("total_xg", "mean"))
    )
    figure = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.15,
        subplot_titles=("Total goals per match", "Combined expected goals per match"),
    )
    colors = {"Inter Miami fixtures": "#e85c4a", "Rest of MLS": "#174e3c"}
    for label in ("Inter Miami fixtures", "Rest of MLS"):
        goals = summary.loc[summary["group"].eq(label)].sort_values("season")
        figure.add_trace(
            go.Scatter(
                x=goals["season"],
                y=goals["goals"],
                customdata=goals[["matches"]].to_numpy(),
                mode="lines+markers",
                name=label,
                legendgroup=label,
                line=dict(color=colors[label], width=3),
                marker=dict(size=8),
                hovertemplate=(
                    "Season %{x}<br>Goals per match: %{y:.2f}"
                    "<br>Fixtures: %{customdata[0]}<extra></extra>"
                ),
            ),
            row=1,
            col=1,
        )
        xg = xg_summary.loc[xg_summary["group"].eq(label)].sort_values("season")
        figure.add_trace(
            go.Scatter(
                x=xg["season"],
                y=xg["xg"],
                customdata=xg[["xg_matches"]].to_numpy(),
                mode="lines+markers",
                name=label,
                legendgroup=label,
                showlegend=False,
                line=dict(color=colors[label], width=3, dash="dash"),
                marker=dict(size=8, symbol="diamond"),
                hovertemplate=(
                    "Season %{x}<br>Expected goals per match: %{y:.2f}"
                    "<br>Fixtures with xG: %{customdata[0]}<extra></extra>"
                ),
            ),
            row=2,
            col=1,
        )
    figure.add_vline(
        x=2023,
        line_color="#77867e",
        line_dash="dot",
        line_width=2,
        annotation_text="Messi joins · 2023",
        annotation_position="top",
    )
    figure.update_xaxes(title_text="Season", dtick=1, range=[2019.5, 2025.5], row=2, col=1)
    figure.update_yaxes(title_text="Goals", rangemode="tozero", row=1, col=1)
    figure.update_yaxes(title_text="Combined xG", rangemode="tozero", row=2, col=1)
    figure.update_layout(
        title=dict(text="The change appears after the arrival—not all at once", x=0.02, xanchor="left"),
        hovermode="x unified",
    )
    return figure


def tactical_figure(matches: pd.DataFrame) -> go.Figure:
    years = []
    for season, group in matches.groupby("season", sort=True):
        xg_matches = group.loc[group["xg_complete"]]
        years.append(
            {
                "season": int(season),
                "home_goals": group["score1"].mean(),
                "away_goals": group["score2"].mean(),
                "home_xg": xg_matches["xg1"].mean(),
                "away_xg": xg_matches["xg2"].mean(),
                "home_win": group["score1"].gt(group["score2"]).mean() * 100,
                "draw": group["score1"].eq(group["score2"]).mean() * 100,
                "away_win": group["score1"].lt(group["score2"]).mean() * 100,
                "home_conversion": (
                    xg_matches["score1"].sum() / xg_matches["xg1"].sum()
                    if len(xg_matches)
                    else None
                ),
                "away_conversion": (
                    xg_matches["score2"].sum() / xg_matches["xg2"].sum()
                    if len(xg_matches)
                    else None
                ),
            }
        )
    summary = pd.DataFrame(years)
    figure = make_subplots(
        rows=3,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.11,
        subplot_titles=(
            "Goals and expected goals per team, per match",
            "Match result share",
            "Goals scored per expected goal",
        ),
    )
    series = [
        ("home_goals", "Home goals", "#174e3c", "solid", 1),
        ("away_goals", "Away goals", "#e85c4a", "solid", 1),
        ("home_xg", "Home xG · through 2022", "#174e3c", "dash", 1),
        ("away_xg", "Away xG · through 2022", "#e85c4a", "dash", 1),
        ("home_win", "Home win", "#174e3c", "solid", 2),
        ("draw", "Draw", "#74827b", "dot", 2),
        ("away_win", "Away win", "#e85c4a", "solid", 2),
        ("home_conversion", "Home goals / xG · through 2022", "#174e3c", "solid", 3),
        ("away_conversion", "Away goals / xG · through 2022", "#e85c4a", "solid", 3),
    ]
    for column, label, color, dash, row in series:
        data = summary.loc[summary[column].notna()]
        figure.add_trace(
            go.Scatter(
                x=data["season"],
                y=data[column],
                mode="lines+markers",
                name=label,
                legendgroup=label,
                line=dict(color=color, dash=dash, width=2.5),
                marker=dict(size=7),
                hovertemplate=f"Season %{{x}}<br>{label}: %{{y:.2f}}<extra></extra>",
            ),
            row=row,
            col=1,
        )
    figure.update_xaxes(title_text="Season", dtick=1, row=3, col=1)
    figure.update_yaxes(title_text="Goals / xG", rangemode="tozero", row=1, col=1)
    figure.update_yaxes(title_text="Share (%)", range=[0, 65], row=2, col=1)
    figure.update_yaxes(title_text="Goals per xG", range=[0.6, 1.5], row=3, col=1)
    figure.update_layout(
        title=dict(text="The home side scores more—and wins more often", x=0.02, xanchor="left"),
        hovermode="x unified",
    )
    return figure


def build_site(matches: pd.DataFrame) -> None:
    DOCS.mkdir(exist_ok=True)
    match_count = len(matches)
    season_count = matches["season"].nunique()
    goal_count = int(matches["total_goals"].sum())
    xg_matches = int(matches["xg_complete"].sum())
    mean_xg = matches.loc[matches["xg_complete"], "total_xg"].mean()
    clubs = sorted(set(matches["team1"]) | set(matches["team2"]))

    home_plot = plot_html(home_figure(matches), "league-trajectory-chart", height=650)
    home_body = f"""
<div class="wrap">
  <section class="hero">
    <div class="eyebrow">A match-by-match look at the modern MLS</div>
    <h1>The growth of U.S. soccer—and the Messi effect</h1>
    <p class="dek">Major League Soccer's recent evolution is written into its match scores. This project follows the league from its 2017 season through 2025, then looks closer at the arrival of Lionel Messi and what changed around Inter Miami.</p>
  </section>
  <section class="kpis" aria-label="Dataset summary">
    <article class="kpi"><div class="kpi-label">Total real matches analyzed</div><div class="kpi-value">{match_count:,}</div><div class="kpi-note">Completed MLS fixtures, 2017–2025</div></article>
    <article class="kpi"><div class="kpi-label">Seasons covered</div><div class="kpi-value">{season_count}</div><div class="kpi-note">{matches["season"].min()} through {matches["season"].max()}</div></article>
    <article class="kpi"><div class="kpi-label">Total goals scored</div><div class="kpi-value">{goal_count:,}</div><div class="kpi-note">Home and away goals combined</div></article>
    <article class="kpi"><div class="kpi-label">Average expected goals per match</div><div class="kpi-value">{mean_xg:.2f}</div><div class="kpi-note">Combined xG per match · {xg_matches:,} complete xG records</div></article>
  </section>
  <section class="section">
    <div class="section-heading">
      <div><div class="eyebrow">League trajectory</div><h2>One point for every game</h2></div>
      <p>Scores extend through 2025. Expected-goal observations are available in the FiveThirtyEight archive through 2022; both measures are shown at match level where recorded, with season averages to make the long view legible.</p>
    </div>
    <div class="chart-card">{home_plot}
      <div class="chart-caption"><span><strong>How to read it:</strong> faint marks are individual matches; solid and dashed lines are season averages.</span><span>Hover for exact match scores or xG.</span></div>
    </div>
  </section>
  <div class="data-note"><strong>Data in brief.</strong> The local file combines 2,505 MLS rows from an archived FiveThirtyEight SPI match file with 1,583 completed non-All-Star MLS scoreboard events from ESPN for 2023–2025. xG is not supplied in the later ESPN rows, so no post-2022 xG values are imputed. The analysis is descriptive, not causal.</div>
</div>
"""
    (DOCS / "index.html").write_text(
        page("The growth of U.S. soccer and the Messi effect", "index.html", home_body),
        encoding="utf-8",
    )

    performance = team_performance(matches)
    explorer_plot = plot_html(
        explorer_figure(performance, clubs), "club-chart", height=550
    )
    club_options = "".join(
        f'<option value="{html.escape(club, quote=True)}"'
        f'{" selected" if club == "Inter Miami CF" else ""}>'
        f"{html.escape(club)}</option>"
        for club in clubs
    )
    explorer_body = f"""
<div class="wrap">
  <section class="hero">
    <div class="eyebrow">Club &amp; season explorer</div>
    <h1>Put the match record in your hands</h1>
    <p class="dek">Choose a club, switch between its home and away form, then narrow the seasons with the chart's range slider. Each point summarizes that club's completed matches in that season.</p>
  </section>
  <section class="section">
    <div class="panel">
      <div class="controls">
        <div><label class="control-label" for="club-select">Select a club</label><select id="club-select">{club_options}</select></div>
        <div><span class="control-label">Match venue</span><div class="button-group" role="group" aria-label="Filter by match venue">
          <button class="filter-button" type="button" data-venue-filter="Both" aria-pressed="true">Home + Away</button>
          <button class="filter-button" type="button" data-venue-filter="Home" aria-pressed="false">Home</button>
          <button class="filter-button" type="button" data-venue-filter="Away" aria-pressed="false">Away</button>
        </div></div>
      </div>
      <p>Hover any season for the exact match count, win rate, goals scored per game and available expected goals. The xG field is blank for post-2022 matches because the supplemental scoreboard does not publish it.</p>
      <div class="chart-card">{explorer_plot}</div>
    </div>
  </section>
  <section class="section">
    <div class="section-heading"><div><div class="eyebrow">League-wide reference</div><h2>Every club in the record</h2></div>
      <p>Club totals combine home and away appearances across the available seasons. xG averages use only matches with a complete xG pair.</p>
    </div>
    <div class="table-card"><div class="table-wrap">{club_table(matches, clubs)}</div></div>
  </section>
  <div class="data-note"><strong>Reading the chart.</strong> Lines show goals scored per match; hover details also report win rate and mean xG. xG coverage is limited to complete FiveThirtyEight records, while goals and results extend through 2025.</div>
</div>
{explorer_script()}
"""
    (DOCS / "explorer.html").write_text(
        page("Club & season explorer", "explorer.html", explorer_body),
        encoding="utf-8",
    )

    inter_plot = plot_html(
        inter_miami_figure(matches), "inter-miami-chart", static=True, height=670
    )
    inter_body = f"""
<div class="wrap">
  <section class="hero">
    <div class="eyebrow">The Inter Miami turning point</div>
    <h1>A superstar changed the spotlight. The scoreline took longer.</h1>
    <p class="dek">Lionel Messi arrived in South Florida in July 2023. Season-level match records put that moment in context—and show why the most striking shift appears in the seasons that followed.</p>
  </section>
  <section class="section">
    <div class="chart-card">{inter_plot}
      <div class="chart-caption"><span><strong>Inter Miami fixtures</strong> includes every match involving the club; <strong>Rest of MLS</strong> excludes those fixtures.</span><span>The chart is fixed for reading; no zoom or filter controls.</span></div>
    </div>
    <div class="story-copy">
      <p>Inter Miami's first three seasons were not a steady climb into high-scoring games. Its matches averaged 2.63 total goals in 2020, 2.62 in 2021 and 3.03 in 2022. In 2023—the season Messi joined in July—the full-season average was 2.79, almost level with the rest of MLS at 2.76. That is a useful reminder: a season-wide average blurs the before-and-after inside a campaign.</p>
      <p>The contrast becomes pronounced in the next two seasons. Miami fixtures averaged 3.76 total goals in 2024 and 4.03 in 2025, compared with 3.07 and 2.94 across the rest of the league. Miami itself scored an average 2.27 and 2.52 goals per match in those seasons, respectively. A more forceful attack is consistent with the pattern; the scores alone cannot separate Messi's contribution from teammates, opponents, game state or other roster changes.</p>
      <p>For U.S. soccer ahead of the 2026 FIFA World Cup, the record points to both the pull of a global star and the importance of what happens after the headline signing. Inter Miami became a more prolific, higher-event team over time, but this comparison measures goals—not attendance, broadcast reach or the independent effect of one player. It is evidence of a striking change, not a causal verdict.</p>
    </div>
    <div class="data-note"><strong>Coverage note.</strong> Goal totals include 2020–2025 completed league and postseason fixtures. Paired xG is available only through 2022 in these sources, so the xG series ends before Messi's arrival. Messi joined during the 2023 season; this chart does not isolate his appearances.</div>
  </section>
</div>
"""
    (DOCS / "inter-miami-story.html").write_text(
        page("The Inter Miami turning point", "inter-miami-story.html", inter_body),
        encoding="utf-8",
    )

    tactical_plot = plot_html(
        tactical_figure(matches), "home-advantage-chart", static=True, height=810
    )
    tactical_body = f"""
<div class="wrap">
  <section class="hero">
    <div class="eyebrow">Home advantage &amp; scoring trends</div>
    <h1>Home still matters. The margin has moved.</h1>
    <p class="dek">Across thousands of MLS fixtures, home teams score more and win more often. Season-by-season trends show that advantage is not fixed—and that away sides have become more competitive in the most recent records.</p>
  </section>
  <section class="section">
    <div class="chart-card">{tactical_plot}
      <div class="chart-caption"><span>Expected goals and conversion ratios stop at 2022, the last MLS season with paired xG in the archive.</span><span>Static chart · match outcomes and scoring rates are season aggregates.</span></div>
    </div>
    <div class="story-copy">
      <p>Across all 4,088 matches from 2017–2025, the home team scored 1.74 goals per game and the away team 1.23. Home sides won 49.0% of fixtures; away sides won 26.2%, with the remainder drawn. That is a clear home edge in results as well as output, but it is an average across changing clubs, schedules and seasons—not a rule for any single match.</p>
      <p>The available xG records help separate chance creation from finishing. In 2,504 matches with complete xG, home teams averaged 1.65 xG and 1.77 actual goals, while away teams averaged 1.21 xG and 1.20 goals. Goals per xG were 1.07 at home and 0.99 away. These ratios describe realized scoring against this dataset's expected-goal estimates; they are not a pure measure of skill or shot quality.</p>
      <p>The gap has also narrowed in recent seasons: home teams won 51.1% of recorded games in 2017–2022, compared with 45.8% in 2023–2025, while away wins rose from 25.1% to 28.0%. The later period lacks xG, so the score data can show a shift in outcomes but not whether chance quality or finishing drove it. It is a useful signal of a changing league, not proof that travel or venue mattered less.</p>
    </div>
    <div class="data-note"><strong>Method.</strong> The first panel compares home/away goals per match with paired xG; the second shows each result type as a share of matches; the third divides goals scored by xG for seasons with coverage. For the later years, only final scores and outcomes are available.</div>
  </section>
</div>
"""
    (DOCS / "tactical-trends.html").write_text(
        page("Home advantage & scoring trends", "tactical-trends.html", tactical_body),
        encoding="utf-8",
    )

    print(
        f"Built {len(NAV_ITEMS)} pages from {match_count:,} matches "
        f"({season_count} seasons, {goal_count:,} goals, {xg_matches:,} complete xG records)."
    )


if __name__ == "__main__":
    build_site(load_matches())
