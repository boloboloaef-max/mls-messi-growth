from __future__ import annotations

import html
import json
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


ROOT = Path(__file__).resolve().parent
DOCS = ROOT / "docs"
DATA_PATH = ROOT / "mls_matches.csv"
MESSI_CUTOFF = pd.Timestamp("2023-07-21")
REQUIRED_COLUMNS = {
    "season", "date", "league", "team1", "team2", "score1", "score2",
    "xg1", "xg2", "source",
}

NAV_ITEMS = [
    ("index.html", "Home"),
    ("scoring-xg.html", "Scoring & xG"),
    ("messi-impact.html", "Messi Impact"),
    ("clubs-dynamics.html", "Club & League Dynamics"),
    ("explorer.html", "Match Explorer"),
    ("about.html", "About"),
]

PINK = "#E91E63"
PINK_LIGHT = "#F7B5CD"
NAVY = "#0F172A"
SLATE = "#475569"
TEAL = "#0EA5E9"
MUTED = "#64748B"

STYLE = """
<style>
  :root {
    color-scheme: light;
    --ink: #0f172a;
    --muted: #64748b;
    --paper: #f3f6fa;
    --card: #fff;
    --line: #e2e8f0;
    --navy: #0f172a;
    --pink: #e91e63;
    --pink-soft: #f7b5cd;
    --teal: #0ea5e9;
    --shadow: 0 12px 32px rgba(15, 23, 42, .07);
  }
  * { box-sizing: border-box; }
  body {
    margin: 0; background: var(--paper); color: var(--ink);
    font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    -webkit-font-smoothing: antialiased;
  }
  a { color: inherit; }
  .site-header { position: sticky; z-index: 20; top: 0; background: rgba(15, 23, 42, .97); color: #fff; box-shadow: 0 5px 24px rgba(0,0,0,.12); }
  .nav-wrap { width: min(1320px, calc(100% - 44px)); min-height: 72px; margin: auto; display: flex; align-items: center; justify-content: space-between; gap: 22px; }
  .brand { flex: 0 0 auto; color: #fff; font-size: 13px; font-weight: 850; letter-spacing: .1em; line-height: 1.25; text-decoration: none; text-transform: uppercase; }
  .brand span { display: block; color: var(--pink-soft); font-size: 10px; letter-spacing: .08em; }
  .nav-links { display: flex; align-items: center; gap: 4px; }
  .nav-links a { border-radius: 999px; color: #dbe3ef; font-size: 12px; font-weight: 700; padding: 10px 12px; text-decoration: none; white-space: nowrap; }
  .nav-links a:hover, .nav-links a[aria-current="page"] { background: rgba(233,30,99,.17); color: #ffc0d5; }
  main { min-height: calc(100vh - 180px); }
  .wrap { width: min(1160px, calc(100% - 44px)); margin: 0 auto; }
  .hero { padding: 58px 0 22px; }
  .eyebrow { color: var(--pink); font-size: 11px; font-weight: 850; letter-spacing: .15em; text-transform: uppercase; }
  h1 { max-width: 970px; margin: 14px 0 15px; font-size: clamp(38px, 6vw, 68px); letter-spacing: -.055em; line-height: 1.02; }
  h2 { margin: 0 0 10px; font-size: clamp(23px, 3vw, 32px); letter-spacing: -.04em; }
  h3 { margin: 0 0 8px; font-size: 18px; letter-spacing: -.02em; }
  p { color: #334155; font-size: 15px; line-height: 1.72; }
  .dek { max-width: 850px; margin: 0; color: #526176; font-size: 17px; line-height: 1.7; }
  .kpis { display: grid; grid-template-columns: repeat(4, minmax(0,1fr)); gap: 13px; margin: 16px 0 30px; }
  .kpi, .panel, .chart-card, .table-card, .profile-card { border: 1px solid var(--line); border-radius: 16px; background: var(--card); box-shadow: var(--shadow); }
  .kpi { min-height: 132px; padding: 18px 19px; transition: transform .18s ease, box-shadow .18s ease; }
  .kpi:hover { transform: translateY(-3px); box-shadow: 0 16px 36px rgba(15,23,42,.11); }
  .kpi-label { color: var(--muted); font-size: 11px; font-weight: 800; line-height: 1.4; }
  .kpi-value { margin: 12px 0 5px; font-size: clamp(25px, 3vw, 35px); font-weight: 850; letter-spacing: -.055em; }
  .kpi-note { color: #738197; font-size: 10px; line-height: 1.5; }
  .section { padding: 18px 0 30px; }
  .section-heading { display: flex; align-items: end; justify-content: space-between; gap: 24px; margin-bottom: 15px; }
  .section-heading p { max-width: 650px; margin: 0; color: var(--muted); font-size: 13px; }
  .chart-card { overflow: hidden; padding: 9px 10px 2px; }
  .chart-caption { display: flex; justify-content: space-between; gap: 18px; padding: 10px 14px 13px; color: var(--muted); font-size: 11px; line-height: 1.55; }
  .chart-caption strong { color: var(--ink); }
  .panel { padding: 20px; }
  .insight { margin: 12px 0 0; padding: 13px 15px; border-left: 3px solid var(--pink); border-radius: 0 10px 10px 0; background: #fff; color: #45546a; font-size: 13px; line-height: 1.65; }
  .data-note { margin: 18px 0 32px; border-left: 4px solid var(--teal); border-radius: 0 10px 10px 0; background: #e8f5fb; color: #42566a; font-size: 12px; line-height: 1.7; padding: 13px 16px; }
  .data-note a { color: #075985; font-weight: 750; }
  .controls { display: flex; flex-wrap: wrap; align-items: end; gap: 12px 18px; margin: 15px 0; }
  .control-label { display: block; margin-bottom: 6px; color: var(--muted); font-size: 10px; font-weight: 850; letter-spacing: .08em; text-transform: uppercase; }
  select { min-width: 190px; border: 1px solid #cbd5e1; border-radius: 9px; background: #fff; color: var(--ink); font: inherit; font-size: 13px; padding: 10px 32px 10px 12px; }
  .table-wrap { max-height: 580px; overflow: auto; }
  table { width: 100%; border-collapse: collapse; font-size: 12px; }
  th, td { padding: 11px 12px; border-bottom: 1px solid #e8edf3; text-align: left; white-space: nowrap; }
  th { position: sticky; top: 0; z-index: 1; background: #f1f5f9; color: #526176; font-size: 9px; letter-spacing: .08em; text-transform: uppercase; }
  td.num, th.num { text-align: right; }
  tbody tr:hover { background: #f8fafc; }
  .profile-card { padding: 24px; }
  .profile-card p { margin: 7px 0; }
  .profile-links { display: grid; grid-template-columns: repeat(2, minmax(0,1fr)); gap: 10px 22px; margin-top: 20px; }
  .profile-links a { color: #be185d; font-weight: 700; overflow-wrap: anywhere; }
  .site-footer { margin-top: 30px; background: var(--navy); color: #d6deea; }
  .footer-inner { width: min(1160px, calc(100% - 44px)); margin: auto; padding: 22px 0 27px; display: flex; justify-content: space-between; gap: 20px; font-size: 10px; line-height: 1.7; }
  .footer-inner a { color: #f9a8c4; }
  .plotly-graph-div { width: 100% !important; }
  @media (max-width: 980px) {
    .nav-wrap { align-items: flex-start; flex-direction: column; gap: 9px; padding: 15px 0 12px; }
    .nav-links { width: 100%; overflow-x: auto; padding-bottom: 3px; }
    .nav-links a { flex: 0 0 auto; }
    .hero { padding-top: 42px; }
    .kpis { grid-template-columns: repeat(2,minmax(0,1fr)); }
  }
  @media (max-width: 580px) {
    .wrap, .nav-wrap, .footer-inner { width: min(100% - 28px, 1160px); }
    .kpis { gap: 8px; }
    .kpi { min-height: 115px; padding: 13px; }
    .kpi-value { font-size: 26px; }
    .section-heading, .footer-inner { align-items: flex-start; flex-direction: column; }
    .chart-card { padding: 4px 4px 0; }
    .chart-caption { flex-direction: column; gap: 4px; }
    .panel, .profile-card { padding: 15px; }
    .profile-links { grid-template-columns: 1fr; }
    select { min-width: min(100%, 280px); }
  }
</style>
"""


def load_matches() -> pd.DataFrame:
    if not DATA_PATH.is_file():
        raise FileNotFoundError(f"Required local match dataset not found: {DATA_PATH}")
    matches = pd.read_csv(DATA_PATH)
    missing = REQUIRED_COLUMNS - set(matches.columns)
    if missing:
        raise ValueError(f"Dataset is missing columns: {', '.join(sorted(missing))}")
    matches = matches.loc[matches["league"].eq("Major League Soccer")].copy()
    if matches.empty:
        raise ValueError("No Major League Soccer records were found.")
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
    matches["goal_margin"] = matches["score1"] - matches["score2"]
    matches["xg_complete"] = matches[["xg1", "xg2"]].notna().all(axis=1)
    matches["total_xg"] = matches[["xg1", "xg2"]].sum(axis=1, min_count=2)
    return matches.sort_values(["date", "team1", "team2"]).reset_index(drop=True)


def appearances(matches: pd.DataFrame) -> pd.DataFrame:
    home = pd.DataFrame({
        "date": matches["date"], "season": matches["season"], "club": matches["team1"],
        "venue": "Home", "gf": matches["score1"], "ga": matches["score2"],
        "xgf": matches["xg1"], "xga": matches["xg2"],
    })
    away = pd.DataFrame({
        "date": matches["date"], "season": matches["season"], "club": matches["team2"],
        "venue": "Away", "gf": matches["score2"], "ga": matches["score1"],
        "xgf": matches["xg2"], "xga": matches["xg1"],
    })
    result = pd.concat([home, away], ignore_index=True)
    result["goal_diff"] = result["gf"] - result["ga"]
    result["win"] = result["goal_diff"] > 0
    result["draw"] = result["goal_diff"] == 0
    result["loss"] = result["goal_diff"] < 0
    return result


def site_nav(active_page: str) -> str:
    links = "".join(
        f'<a href="{href}"'
        f'{" aria-current=\"page\"" if href == active_page else ""}>{html.escape(label)}</a>'
        for href, label in NAV_ITEMS
    )
    return f"""
<header class="site-header"><div class="nav-wrap">
  <a class="brand" href="index.html">MLS · Matchbook<span>League evolution, in the match record</span></a>
  <nav class="nav-links" aria-label="Main navigation">{links}</nav>
</div></header>
"""


def page(title: str, active_page: str, body: str) -> str:
    document = f"""<!doctype html>
<html lang="en"><head>
  <meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="An observational MLS match analysis of scoring, clubs, expected goals and Lionel Messi's arrival, 2017–2025.">
  <title>{html.escape(title)} | MLS Matchbook</title>{STYLE}
  <script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
</head><body>
  {site_nav(active_page)}
  <main>{body}</main>
  <footer class="site-footer"><div class="footer-inner">
    <div>MLS Matchbook · Observational analysis, 2017–2025.<br>Match outcomes describe what happened; they do not establish why.</div>
    <div>Dataset: <a href="https://github.com/boloboloaf-hub/mls-messi-growth/blob/main/mls_matches.csv">mls_matches.csv</a>
    · <a href="https://github.com/boloboloaf-hub/mls-messi-growth">Project repository</a></div>
  </div></footer>
</body></html>
"""
    return "\n".join(line.rstrip() for line in document.splitlines()) + "\n"


def plot_html(figure: go.Figure, div_id: str, height: int = 480) -> str:
    for trace in figure.data:
        if not trace.hovertemplate:
            trace.hovertemplate = "%{x}<br>%{y}<extra></extra>"
    figure.update_layout(
        template="plotly_white", height=height, autosize=True,
        margin=dict(l=56, r=24, t=55, b=55),
        paper_bgcolor="white", plot_bgcolor="white",
        font=dict(family="Inter, system-ui, sans-serif", color=NAVY, size=11),
        hoverlabel=dict(bgcolor=NAVY, font_color="white"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0),
    )
    return figure.to_html(
        full_html=False, include_plotlyjs=False, div_id=div_id,
        config={"responsive": True, "displaylogo": False, "displayModeBar": True},
    )


def page_hero(eyebrow: str, heading: str, dek: str) -> str:
    return (
        '<section class="hero"><div class="eyebrow">' + eyebrow + "</div>"
        f"<h1>{heading}</h1><p class=\"dek\">{dek}</p></section>"
    )


def kpi_cards(matches: pd.DataFrame, apps: pd.DataFrame, *, section: bool = True) -> str:
    total_matches = len(matches)
    goals = int(matches["total_goals"].sum())
    xg_count = int(matches["xg_complete"].sum())
    miami = apps.loc[apps["club"].eq("Inter Miami CF")].copy()
    pre = miami.loc[miami["date"] < MESSI_CUTOFF, "gf"]
    post = miami.loc[miami["date"] >= MESSI_CUTOFF, "gf"]
    delta = post.mean() - pre.mean() if len(pre) and len(post) else float("nan")
    delta_text = f"{delta:+.2f}" if pd.notna(delta) else "n/a"
    opening = '<section class="kpis" aria-label="Dataset summary">' if section else '<div class="kpis" aria-label="Dataset summary">'
    closing = "</section>" if section else "</div>"
    return f"""
{opening}
  <article class="kpi"><div class="kpi-label">MLS matches</div><div class="kpi-value">{total_matches:,}</div><div class="kpi-note">Observed completed matches · {matches.season.min()}–{matches.season.max()}</div></article>
  <article class="kpi"><div class="kpi-label">Goals recorded</div><div class="kpi-value">{goals:,}</div><div class="kpi-note">Home and away score totals in the CSV</div></article>
  <article class="kpi"><div class="kpi-label">Complete xG matches</div><div class="kpi-value">{xg_count:,}</div><div class="kpi-note">Both team xG values present; no missing xG imputed</div></article>
  <article class="kpi"><div class="kpi-label">Inter Miami goals / match change</div><div class="kpi-value">{delta_text}</div><div class="kpi-note">Before vs. on/after 21 Jul 2023 · {len(pre)} vs. {len(post)} team appearances</div></article>
{closing}"""


def chart_section(kicker: str, title: str, description: str, chart: str, takeaway: str = "") -> str:
    insight = f'<p class="insight">{takeaway}</p>' if takeaway else ""
    return f"""
<section class="section"><div class="section-heading"><div><div class="eyebrow">{kicker}</div><h2>{title}</h2></div><p>{description}</p></div>
  <div class="chart-card">{chart}</div>{insight}
</section>"""


def home_season_chart(matches: pd.DataFrame) -> go.Figure:
    summary = matches.groupby("season", as_index=False).agg(
        matches=("total_goals", "size"),
        home=("score1", "mean"),
        away=("score2", "mean"),
        total=("total_goals", "mean"),
    )
    fig = go.Figure()
    for key, name, color in (("home", "Home goals / match", PINK), ("away", "Away goals / match", TEAL)):
        fig.add_trace(go.Scatter(
            x=summary["season"], y=summary[key], mode="lines+markers", name=name,
            line=dict(color=color, width=3), marker=dict(size=8),
            customdata=summary[["matches", "total"]].to_numpy(),
            hovertemplate=f"Season %{{x}}<br>{name}: %{{y:.2f}}<br>Total goals / match: %{{customdata[1]:.2f}}<br>Matches: %{{customdata[0]}}<extra></extra>",
        ))
    fig.update_layout(title="Scoring output by season", hovermode="x unified")
    fig.update_xaxes(title="Season", dtick=1)
    fig.update_yaxes(title="Goals per match", rangemode="tozero")
    fig.add_vline(x=2023, line_dash="dot", line_color=SLATE, annotation_text="Messi arrives July 2023")
    return fig


def home_results_chart(matches: pd.DataFrame) -> go.Figure:
    rows = []
    for season, group in matches.groupby("season", sort=True):
        n = len(group)
        rows.append({
            "season": season, "matches": n,
            "Home win": group["score1"].gt(group["score2"]).mean() * 100,
            "Draw": group["score1"].eq(group["score2"]).mean() * 100,
            "Away win": group["score1"].lt(group["score2"]).mean() * 100,
        })
    summary = pd.DataFrame(rows)
    fig = go.Figure()
    for label, color in (("Home win", PINK), ("Draw", MUTED), ("Away win", TEAL)):
        fig.add_trace(go.Bar(
            x=summary.season, y=summary[label], name=label,
            marker_color=color, customdata=summary[["matches"]].to_numpy(),
            hovertemplate=f"Season %{{x}}<br>{label}: %{{y:.1f}}%<br>Matches: %{{customdata[0]}}<extra></extra>",
        ))
    fig.update_layout(title="How each season's matches ended", barmode="stack", hovermode="x unified")
    fig.update_xaxes(title="Season", dtick=1)
    fig.update_yaxes(title="Share of matches", ticksuffix="%", range=[0, 100])
    return fig


def scoring_xg_charts(matches: pd.DataFrame) -> tuple[go.Figure, go.Figure, go.Figure]:
    xgm = matches.loc[matches["xg_complete"]].copy()
    seasonal = xgm.groupby("season", as_index=False).agg(
        fixtures=("total_goals", "size"),
        goals=("total_goals", "mean"),
        xg=("total_xg", "mean"),
    )
    trend = go.Figure()
    for column, label, color, dash in (
        ("goals", "Actual goals per match", PINK, "solid"),
        ("xg", "Combined xG per match", TEAL, "dash"),
    ):
        trend.add_trace(go.Scatter(
            x=seasonal.season, y=seasonal[column], mode="lines+markers", name=label,
            line=dict(color=color, width=3, dash=dash), marker=dict(size=8),
            customdata=seasonal[["fixtures"]].to_numpy(),
            hovertemplate=f"Season %{{x}}<br>{label}: %{{y:.2f}}<br>Complete xG matches: %{{customdata[0]}}<extra></extra>",
        ))
    trend.update_layout(title="Goals and expected goals on the same fixtures", hovermode="x unified")
    trend.update_xaxes(title="Season", dtick=1)
    trend.update_yaxes(title="Per match", rangemode="tozero")

    sides = pd.concat([
        xgm[["date", "season", "team1", "team2", "score1", "xg1"]].rename(
            columns={"team1": "club", "team2": "opponent", "score1": "goals", "xg1": "xg"}
        ).assign(venue="Home"),
        xgm[["date", "season", "team2", "team1", "score2", "xg2"]].rename(
            columns={"team2": "club", "team1": "opponent", "score2": "goals", "xg2": "xg"}
        ).assign(venue="Away"),
    ], ignore_index=True)
    scatter = go.Figure()
    for venue, color in (("Home", PINK), ("Away", TEAL)):
        side = sides.loc[sides.venue.eq(venue)]
        scatter.add_trace(go.Scattergl(
            x=side.xg, y=side.goals, mode="markers", name=venue,
            marker=dict(color=color, size=5, opacity=.48),
            customdata=side[["club", "opponent", "date", "season"]].to_numpy(),
            hovertemplate="%{customdata[0]} vs %{customdata[1]} · %{customdata[2]|%b %d, %Y}<br>Season %{customdata[3]} · %{fullData.name}<br>xG: %{x:.2f}<br>Goals: %{y:.0f}<extra></extra>",
        ))
    extent = max(float(sides["xg"].max()), float(sides["goals"].max()))
    scatter.add_trace(go.Scatter(
        x=[0, extent], y=[0, extent], mode="lines", name="Goals = xG",
        line=dict(color=SLATE, dash="dot"), hovertemplate="Reference: goals equal xG<extra></extra>",
    ))
    scatter.update_layout(title="Observed team goals against expected goals", hovermode="closest")
    scatter.update_xaxes(title="Expected goals (xG)", rangemode="tozero")
    scatter.update_yaxes(title="Goals scored", rangemode="tozero")

    margins = pd.concat([
        pd.DataFrame({"season": xgm.season, "venue": "Home", "finish": xgm.score1 - xgm.xg1}),
        pd.DataFrame({"season": xgm.season, "venue": "Away", "finish": xgm.score2 - xgm.xg2}),
    ], ignore_index=True)
    distribution = go.Figure()
    for venue, color in (("Home", PINK), ("Away", TEAL)):
        part = margins.loc[margins.venue.eq(venue)]
        distribution.add_trace(go.Box(
            x=part.season, y=part.finish, name=venue, boxpoints="outliers",
            marker_color=color, line_color=color, quartilemethod="inclusive",
            hovertemplate=f"Season %{{x}} · {venue}<br>Goals minus xG: %{{y:.2f}}<extra></extra>",
        ))
    distribution.update_layout(title="Finishing margin by season and venue", boxmode="group", hovermode="closest")
    distribution.update_xaxes(title="Season", dtick=1)
    distribution.update_yaxes(title="Goals − xG per team-match", zeroline=True)
    return trend, scatter, distribution


def messi_charts(apps: pd.DataFrame) -> tuple[go.Figure, go.Figure, go.Figure]:
    miami = apps.loc[apps.club.eq("Inter Miami CF")].copy()
    miami["period"] = miami.date.ge(MESSI_CUTOFF).map({False: "Before 21 Jul 2023", True: "On/after 21 Jul 2023"})
    period = miami.groupby(["period", "venue"], as_index=False).agg(
        matches=("gf", "size"), gf=("gf", "mean"), ga=("ga", "mean"), gd=("goal_diff", "mean")
    )
    period_order = ["Before 21 Jul 2023", "On/after 21 Jul 2023"]
    colors = {"Before 21 Jul 2023": SLATE, "On/after 21 Jul 2023": PINK}

    venue = go.Figure()
    categories = []
    for label in period_order:
        for venue_name in ("Home", "Away"):
            categories.append(f"{'Before' if label.startswith('Before') else 'On/after'} · {venue_name}")
    for metric, title, period_colors in (
        ("gf", "Goals for", ["#CBD5E1", "#CBD5E1", PINK, PINK]),
        ("ga", "Goals against", ["#7DD3FC", "#7DD3FC", TEAL, TEAL]),
    ):
        values = []
        custom = []
        for label in period_order:
            for venue_name in ("Home", "Away"):
                item = period.loc[(period.period == label) & (period.venue == venue_name)].iloc[0]
                values.append(item[metric])
                custom.append([item.matches, item.gd, label, venue_name])
        venue.add_trace(go.Bar(
            x=categories, y=values, name=title, marker_color=period_colors,
            customdata=custom,
            hovertemplate="%{customdata[3]} · %{customdata[2]}<br>" + title +
                          ": %{y:.2f} / match<br>Goal diff: %{customdata[1]:+.2f}" +
                          "<br>Team appearances: %{customdata[0]}<extra></extra>",
        ))
    venue.update_layout(title="Inter Miami scoring by venue and period", barmode="group", hovermode="closest")
    venue.update_xaxes(title="Match venue")
    venue.update_yaxes(title="Goals per team appearance", rangemode="tozero")

    dist = go.Figure()
    for label in period_order:
        part = miami.loc[miami.period.eq(label)]
        dist.add_trace(go.Box(
            x=[label] * len(part), y=part.goal_diff, name=label, boxpoints="outliers",
            marker_color=colors[label], line_color=colors[label],
            customdata=part[["date", "venue", "gf", "ga"]].to_numpy(),
            hovertemplate="%{customdata[0]|%b %d, %Y} · %{customdata[1]}<br>Goal differential: %{y:+.0f}<br>Goals: %{customdata[2]:.0f}–%{customdata[3]:.0f}<extra></extra>",
        ))
    dist.update_layout(title="Distribution of Inter Miami match goal differentials", hovermode="closest")
    dist.update_xaxes(title="Period relative to 21 July 2023")
    dist.update_yaxes(title="Goals for − goals against", zeroline=True)

    season = miami.groupby(["season", "venue"], as_index=False).agg(
        matches=("gf", "size"), gf=("gf", "mean"), ga=("ga", "mean"), gd=("goal_diff", "mean")
    )
    trajectory = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=.14,
                               subplot_titles=("Home appearances", "Away appearances"))
    for venue_name, rownum in (("Home", 1), ("Away", 2)):
        subset = season.loc[season.venue.eq(venue_name)].sort_values("season")
        for column, label, color, dash in (
            ("gf", "Goals for", PINK, "solid"), ("ga", "Goals against", TEAL, "dash")
        ):
            trajectory.add_trace(go.Scatter(
                x=subset.season, y=subset[column], mode="lines+markers",
                name=f"{venue_name} · {label}", line=dict(color=color, width=2.5, dash=dash),
                customdata=subset[["matches", "gd"]].to_numpy(),
                hovertemplate=f"Season %{{x}} · {venue_name}<br>{label}: %{{y:.2f}} / match<br>Goal differential: %{{customdata[1]:+.2f}}<br>Appearances: %{{customdata[0]}}<extra></extra>",
            ), row=rownum, col=1)
    trajectory.add_vline(x=2023, line_dash="dot", line_color=SLATE,
                         annotation_text="21 Jul cutoff falls within 2023", row="all", col=1)
    trajectory.update_xaxes(title_text="Season", dtick=1, row=2, col=1)
    trajectory.update_yaxes(title_text="Goals / appearance", rangemode="tozero")
    trajectory.update_layout(title="Inter Miami season trajectory", hovermode="x unified")
    return venue, dist, trajectory


def club_charts(matches: pd.DataFrame, apps: pd.DataFrame) -> tuple[go.Figure, go.Figure, go.Figure]:
    club = apps.groupby("club", as_index=False).agg(
        matches=("gf", "size"), gf=("gf", "mean"), ga=("ga", "mean"), goal_diff=("goal_diff", "mean")
    )
    top = club.sort_values(["gf", "matches"], ascending=[False, False]).head(12).sort_values("gf")
    bar = go.Figure(go.Bar(
        x=top.gf, y=top.club, orientation="h", marker_color=[PINK if c == "Inter Miami CF" else TEAL for c in top.club],
        customdata=top[["matches", "ga", "goal_diff"]].to_numpy(),
        hovertemplate="%{y}<br>Goals scored / appearance: %{x:.2f}<br>Goals conceded / appearance: %{customdata[1]:.2f}<br>Goal differential: %{customdata[2]:+.2f}<br>Team appearances: %{customdata[0]}<extra></extra>",
    ))
    bar.update_layout(title="Highest-scoring clubs across the full dataset", showlegend=False)
    bar.update_xaxes(title="Goals scored per team appearance", rangemode="tozero")
    bar.update_yaxes(title="")

    scatter = go.Figure()
    scatter.add_trace(go.Scatter(
        x=club.gf, y=club.ga, mode="markers+text", text=club.club, textposition="top center",
        textfont=dict(size=9, color=SLATE), marker=dict(
            size=club.matches, sizemode="area", sizeref=2.0 * club.matches.max() / (34 ** 2),
            sizemin=7, color=[PINK if c == "Inter Miami CF" else TEAL for c in club.club],
            opacity=.72, line=dict(color="white", width=1),
        ),
        customdata=club[["matches", "goal_diff"]].to_numpy(),
        hovertemplate="%{text}<br>Goals for / appearance: %{x:.2f}<br>Goals against / appearance: %{y:.2f}<br>Goal differential: %{customdata[1]:+.2f}<br>Team appearances: %{customdata[0]}<extra></extra>",
    ))
    league_attack = apps.gf.mean()
    league_defense = apps.ga.mean()
    scatter.add_vline(x=league_attack, line_dash="dot", line_color=SLATE,
                      annotation_text=f"League scoring {league_attack:.2f}")
    scatter.add_hline(y=league_defense, line_dash="dot", line_color=SLATE,
                      annotation_text=f"League conceded {league_defense:.2f}")
    scatter.update_layout(title="Attacking output vs. defensive record")
    scatter.update_xaxes(title="Goals scored per appearance", rangemode="tozero")
    scatter.update_yaxes(title="Goals conceded per appearance", rangemode="tozero")

    rows = []
    for year, group in matches.groupby("season", sort=True):
        n = len(group)
        rows.append({
            "season": year,
            "Home win": group.score1.gt(group.score2).mean() * 100,
            "Draw": group.score1.eq(group.score2).mean() * 100,
            "Away win": group.score1.lt(group.score2).mean() * 100,
            "Home goals edge": group.score1.mean() - group.score2.mean(),
            "matches": n,
        })
    outcome = pd.DataFrame(rows)
    advantage = go.Figure()
    for label, color in (("Home win", PINK), ("Draw", MUTED), ("Away win", TEAL)):
        advantage.add_trace(go.Scatter(
            x=outcome.season, y=outcome[label], name=label, mode="lines+markers",
            line=dict(color=color, width=2.5), marker=dict(size=7),
            customdata=outcome[["matches", "Home goals edge"]].to_numpy(),
            hovertemplate=f"Season %{{x}}<br>{label}: %{{y:.1f}}%<br>Home goals edge: %{{customdata[1]:+.2f}} / match<br>Matches: %{{customdata[0]}}<extra></extra>",
        ))
    advantage.update_layout(title="Home-field outcomes and scoring edge", hovermode="x unified")
    advantage.update_xaxes(title="Season", dtick=1)
    advantage.update_yaxes(title="Share of matches", ticksuffix="%", range=[0, 70])
    return bar, scatter, advantage


def explorer_figures(matches: pd.DataFrame, apps: pd.DataFrame) -> tuple[go.Figure, go.Figure, go.Figure, list[str]]:
    margin = go.Figure(go.Histogram(
        x=matches.goal_margin, nbinsx=17, marker_color=TEAL, opacity=.86,
        customdata=matches[["team1", "team2", "score1", "score2", "date"]].to_numpy(),
        hovertemplate="Home goal margin: %{x}<br>Matches in bin: %{y}<extra></extra>",
    ))
    margin.update_layout(title="Distribution of home-team goal margins", bargap=.06)
    margin.update_xaxes(title="Home goals − away goals", zeroline=True)
    margin.update_yaxes(title="Number of matches")

    byseason = matches.groupby("season", as_index=False).agg(
        matches=("total_goals", "size"), avg_goals=("total_goals", "mean"),
        five_plus=("total_goals", lambda values: values.ge(5).mean() * 100),
    )
    high = go.Figure()
    high.add_trace(go.Bar(
        x=byseason.season, y=byseason.five_plus, name="Matches with 5+ goals",
        marker_color=PINK, customdata=byseason[["matches", "avg_goals"]].to_numpy(),
        hovertemplate="Season %{x}<br>Matches with 5+ goals: %{y:.1f}%<br>Average total goals: %{customdata[1]:.2f}<br>Matches: %{customdata[0]}<extra></extra>",
    ))
    high.add_trace(go.Scatter(
        x=byseason.season, y=byseason.avg_goals, name="Average total goals",
        mode="lines+markers", yaxis="y2", line=dict(color=TEAL, width=3),
        customdata=byseason[["matches", "five_plus"]].to_numpy(),
        hovertemplate="Season %{x}<br>Average total goals: %{y:.2f}<br>5+ goal matches: %{customdata[1]:.1f}%<br>Matches: %{customdata[0]}<extra></extra>",
    ))
    high.update_layout(
        title="High-scoring match share and mean goals",
        yaxis=dict(title="Matches with 5+ goals", ticksuffix="%"),
        yaxis2=dict(title="Average total goals", overlaying="y", side="right"),
        hovermode="x unified",
    )
    high.update_xaxes(title="Season", dtick=1)

    clubs = sorted(apps.club.unique())
    figure = go.Figure()
    for club_name in clubs:
        for venue in ("Home", "Away"):
            subset = apps.loc[(apps.club == club_name) & (apps.venue == venue)]
            grouped = subset.groupby("season", as_index=False).agg(
                appearances=("gf", "size"), goals=("gf", "mean"), goal_diff=("goal_diff", "mean")
            )
            figure.add_trace(go.Scatter(
                x=grouped.season, y=grouped.goals, mode="lines+markers",
                name=f"{club_name} · {venue}", meta={"club": club_name, "venue": venue},
                visible=club_name == ("Inter Miami CF" if "Inter Miami CF" in clubs else clubs[0]),
                line=dict(color=PINK if club_name == "Inter Miami CF" else TEAL,
                          dash="solid" if venue == "Home" else "dash", width=2.5),
                customdata=grouped[["appearances", "goal_diff"]].to_numpy(),
                hovertemplate=f"Season %{{x}} · {club_name} · {venue}<br>Goals scored / appearance: %{{y:.2f}}<br>Goal differential: %{{customdata[1]:+.2f}}<br>Appearances: %{{customdata[0]}}<extra></extra>",
            ))
    figure.update_layout(title="Choose a club to compare its season output", showlegend=False, hovermode="x unified")
    figure.update_xaxes(title="Season", dtick=1)
    figure.update_yaxes(title="Goals scored per appearance", rangemode="tozero")
    return margin, high, figure, clubs


def table_rows(matches: pd.DataFrame) -> str:
    records = []
    for row in matches.sort_values("date", ascending=False).itertuples():
        records.append({
            "date": row.date.strftime("%Y-%m-%d"),
            "season": int(row.season),
            "home": str(row.team1),
            "away": str(row.team2),
            "score": f"{row.score1:g}–{row.score2:g}",
            "goals": int(row.total_goals),
            "margin": f"{row.goal_margin:+g}",
            "xg": f"{row.xg1:.2f}–{row.xg2:.2f}" if row.xg_complete else "—",
            "source": str(row.source),
        })
    return json.dumps(records, ensure_ascii=False).replace("</", "<\\/")


def explorer_script() -> str:
    return """
<script>
(() => {
  const chart = document.getElementById("club-season-chart");
  const clubSelect = document.getElementById("club-select");
  const seasonSelect = document.getElementById("match-season");
  const matchTeamSelect = document.getElementById("match-team");
  const rows = JSON.parse(document.getElementById("match-data").textContent);
  const tbody = document.getElementById("match-rows");
  const count = document.getElementById("match-count");

  function applyClub() {
    const club = clubSelect.value;
    const visible = chart.data.map(trace => trace.meta.club === club);
    Plotly.restyle(chart, {visible});
  }
  function renderMatches() {
    const season = seasonSelect.value;
    const team = matchTeamSelect.value;
    const filtered = rows.filter(row =>
      (season === "all" || String(row.season) === season) &&
      (team === "all" || row.home === team || row.away === team)
    ).slice(0, 100);
    count.textContent = `Showing ${filtered.length.toLocaleString()} of ${rows.filter(row =>
      (season === "all" || String(row.season) === season) &&
      (team === "all" || row.home === team || row.away === team)
    ).length.toLocaleString()} matching observed fixtures (maximum 100 displayed).`;
    tbody.replaceChildren(...filtered.map(row => {
      const tr = document.createElement("tr");
      [row.date, row.season, row.home, row.away, row.score, row.goals, row.margin, row.xg, row.source]
        .forEach(value => { const td = document.createElement("td"); td.textContent = value; tr.appendChild(td); });
      return tr;
    }));
  }
  clubSelect.addEventListener("change", applyClub);
  seasonSelect.addEventListener("change", renderMatches);
  matchTeamSelect.addEventListener("change", renderMatches);
  applyClub();
  renderMatches();
})();
</script>
"""


def about_body(matches: pd.DataFrame, apps: pd.DataFrame) -> str:
    pre = apps.loc[(apps.club == "Inter Miami CF") & (apps.date < MESSI_CUTOFF), "gf"]
    post = apps.loc[(apps.club == "Inter Miami CF") & (apps.date >= MESSI_CUTOFF), "gf"]
    about_kpis = kpi_cards(matches, apps, section=False)
    source_paragraph = (
        f"The observational dataset <code>mls_matches.csv</code> contains {len(matches):,} MLS matches "
        f"across {matches.season.nunique()} seasons ({matches.season.min()}–{matches.season.max()}), "
        f"with {int(matches.total_goals.sum()):,} goals and {int(matches.xg_complete.sum()):,} matches "
        "with complete paired expected-goals records. Scores extend through 2025; xG is present only "
        "where both source values were recorded, and no missing values are estimated. "
        '<a href="https://github.com/boloboloaf-hub/mls-messi-growth/blob/main/mls_matches.csv">View the source data file</a>.'
    )
    return f"""
<div class="wrap">
  <section aria-label="Author and project links">
    <div class="hero"><div class="eyebrow">Project &amp; author</div><h1>About this work</h1>
      <p class="dek">A match-level study of MLS scoring, club performance and the timing of Lionel Messi’s arrival.</p></div>
    {about_kpis}
    <div class="profile-card">
      <div class="eyebrow">Author</div><h2>Angel Emilio Frias Arias</h2>
      <p>Data Science &amp; Analytics student at New College of Florida and a varsity collegiate soccer forward.</p>
      <div class="profile-links">
        <div><strong>Contact</strong><br><a href="mailto:a.friasarias28@ncf.edu">a.friasarias28@ncf.edu</a></div>
        <div><strong>GitHub account</strong><br><a href="https://github.com/boloboloaf-hub">github.com/boloboloaf-hub</a></div>
        <div><strong>Project repository</strong><br><a href="https://github.com/boloboloaf-hub/mls-messi-growth">github.com/boloboloaf-hub/mls-messi-growth</a></div>
        <div><strong>Institution</strong><br><a href="https://www.ncf.edu">New College of Florida</a></div>
      </div>
    </div>
  </section>
  <section class="section" aria-label="Data source">
    <div class="eyebrow">Data source</div><h2>Observed match records</h2>
    <div class="data-note">{source_paragraph}</div>
  </section>
</div>"""


def build_site(matches: pd.DataFrame) -> None:
    DOCS.mkdir(exist_ok=True)
    apps = appearances(matches)
    kpis = kpi_cards(matches, apps)
    common_note = (
        "All figures are computed from the checked-in match-level CSV. Paired xG is available "
        "only where both values are present; missing xG is never imputed. Descriptive patterns "
        "are not causal estimates."
    )

    home = f"""
<div class="wrap">
  {page_hero("Executive overview · 2017–2025", "MLS is changing. The match record shows where.", "A data-first overview of league scoring and outcomes across nine seasons, with Lionel Messi’s July 2023 arrival treated as a clear time marker—not a causal explanation.")}
  {kpis}
  {chart_section("League trajectory", "Goals scored by home and away teams", "Season averages make the scoring trend readable while preserving the home/away split. The 2023 season includes matches both before and after the July 21 cutoff.", plot_html(home_season_chart(matches), "home-scoring-chart"), "The season marker is context, not a split-season estimate: 2023 combines pre- and post-cutoff matches.")}
  {chart_section("Competitive balance", "How matches ended, season by season", "A stacked view of observed home wins, draws and away wins; each segment is calculated from that season’s recorded final scores.", plot_html(home_results_chart(matches), "home-results-chart"), "Hover a season to see the actual match count behind its result shares.")}
  <div class="data-note">{common_note} The file covers {len(matches):,} matches and {int(matches.total_goals.sum()):,} goals; {int(matches.xg_complete.sum()):,} matches contain complete paired xG.</div>
</div>"""
    (DOCS / "index.html").write_text(page("MLS evolution and Messi impact", "index.html", home), encoding="utf-8")

    goal_trend, xg_scatter, finishing = scoring_xg_charts(matches)
    scoring = f"""
<div class="wrap">
  {page_hero("Scoring & expected goals", "What was scored—and what was expected?", "Compare realized goals with observed xG, then inspect how the goals-minus-xG finishing margin varies by season and venue.")}
  {kpis}
  {chart_section("League scoring", "Goals and xG on the same match sample", "Both seasonal series use only matches with complete paired xG, so the actual-goal and expected-goal averages are comparable.", plot_html(goal_trend, "scoring-trend-chart"), "The xG series ends with the seasons for which paired estimates are actually recorded; there is no extrapolated post-2022 xG.")}
  {chart_section("Match-level efficiency", "Actual goals against expected goals", "Each point is one team’s score and xG in one match. Points above the reference line finished above the recorded expectation; points below finished under it.", plot_html(xg_scatter, "goals-xg-scatter", 540), "A match-level finishing margin is noisy: it is a descriptive difference, not a stable measure of individual finishing skill.")}
  {chart_section("Finishing distribution", "Goals minus xG, by season and venue", "Boxes summarize the distribution of team-match finishing margins across complete-xG observations; hover outliers for the exact value.", plot_html(finishing, "finishing-box-chart", 520), "The center and spread show how outcomes vary around xG; values are not available in the later score-only data.")}
  <div class="data-note">{common_note}</div>
</div>"""
    (DOCS / "scoring-xg.html").write_text(page("Scoring and expected goals", "scoring-xg.html", scoring), encoding="utf-8")

    venue_fig, goal_diff_fig, miami_trend = messi_charts(apps)
    before = apps.loc[(apps.club == "Inter Miami CF") & (apps.date < MESSI_CUTOFF)]
    after = apps.loc[(apps.club == "Inter Miami CF") & (apps.date >= MESSI_CUTOFF)]
    gf_delta = after.gf.mean() - before.gf.mean()
    gd_delta = after.goal_diff.mean() - before.goal_diff.mean()
    messi = f"""
<div class="wrap">
  {page_hero("Messi Impact · before / after 21 July 2023", "Inter Miami’s match profile shifted after July 2023.", "Compare Inter Miami team appearances before and on/after the July 21, 2023 cutoff. This descriptive comparison includes the club’s whole match record in each period—not an estimate of Messi’s individual contribution.")}
  {kpis}
  {chart_section("Home and away", "Scoring and conceding rates by period", "Goals for and against per Inter Miami team appearance, split by venue and the exact July 21 cutoff.", plot_html(venue_fig, "miami-venue-chart", 510), f"Observed team goals per appearance changed by {gf_delta:+.2f} and average goal differential by {gd_delta:+.2f} between the pre-cutoff and later periods; the comparison does not control for roster, opponent or season.")}
  {chart_section("Match outcomes", "The distribution of goal differential", "Each box displays the Inter Miami match-level goal differential distribution for one period; the width reflects observed match variation.", plot_html(goal_diff_fig, "miami-goal-diff-chart", 500), f"Pre-cutoff matches: {len(before)} team appearances; on/after-cutoff: {len(after)}. Both sample sizes appear in the hoverable team-level records.")}
  {chart_section("Season trajectory", "How Miami’s home and away form evolved", "Season averages are separated by venue and show goals for and against. The vertical marker identifies the season containing the cutoff; 2023 itself spans both periods.", plot_html(miami_trend, "miami-season-chart", 610), "Season averages can conceal within-season changes. The July 2023 cutoff is applied to match dates in the before/after comparison above.")}
  <div class="data-note">{common_note} The data record scores rather than player appearances, so this page describes an Inter Miami change around Messi’s arrival and cannot assign that change to one player.</div>
</div>"""
    (DOCS / "messi-impact.html").write_text(page("Inter Miami and the Messi-era comparison", "messi-impact.html", messi), encoding="utf-8")

    club_bar, club_scatter, home_field = club_charts(matches, apps)
    club_dynamics = f"""
<div class="wrap">
  {page_hero("Club & league dynamics", "Compare attacking output, defense and home advantage.", "Club rates aggregate real home and away appearances across the available seasons. Hover marks for sample sizes; totals are not adjusted for schedule or season length.")}
  {kpis}
  {chart_section("Attacking leaderboard", "Clubs with the highest goals per appearance", "Clubs are ranked on the mean goals they scored per recorded team appearance across 2017–2025; the hover includes appearances and goals conceded.", plot_html(club_bar, "club-scoring-chart", 570), "A rate describes scoring output, not overall team quality; opponents, match counts and the mix of seasons differ by club.")}
  {chart_section("Attack vs. defense", "The club efficiency quadrant", "Each bubble is a club, sized by recorded appearances. The vertical and horizontal references are the dataset’s appearance-weighted league means.", plot_html(club_scatter, "club-efficiency-chart", 620), "Lower on the vertical axis means fewer goals conceded; farther right means more goals scored. Hover labels carry exact club-level values.")}
  {chart_section("Home-field advantage", "Result shares and home scoring edge", "Season-level shares compare home wins, draws and away wins. Hover also reports the home-minus-away goals-per-match edge and season sample size.", plot_html(home_field, "home-field-chart", 500), "Home advantage is summarized from match outcomes and scores; this CSV does not measure travel, attendance or other explanatory factors.")}
  <div class="data-note">{common_note}</div>
</div>"""
    (DOCS / "clubs-dynamics.html").write_text(page("Club and league dynamics", "clubs-dynamics.html", club_dynamics), encoding="utf-8")

    margin_fig, high_fig, team_fig, clubs = explorer_figures(matches, apps)
    club_options = "".join(
        f'<option value="{html.escape(name, quote=True)}"{" selected" if name == "Inter Miami CF" else ""}>{html.escape(name)}</option>'
        for name in clubs
    )
    seasons = sorted(matches.season.unique())
    season_options = '<option value="all">All seasons</option>' + "".join(
        f'<option value="{year}">{year}</option>' for year in seasons
    )
    match_options = '<option value="all">All clubs</option>' + "".join(
        f'<option value="{html.escape(name, quote=True)}">{html.escape(name)}</option>'
        for name in clubs
    )
    explorer = f"""
<div class="wrap">
  {page_hero("Match Explorer · interactive", "Filter the record. Inspect the match.", "Explore goal margins and season-level scoring, then select a club, season or both to see observed fixture scores, xG coverage and source attribution.")}
  {kpis}
  {chart_section("Goal margins", "Home-team scoring margin distribution", "Positive values indicate a home win, zero a draw, and negative values an away win. The histogram bins are built from each match’s recorded score.", plot_html(margin_fig, "goal-margin-chart", 450), "The shape is a league-wide distribution; filters below let you inspect the underlying match records.")}
  {chart_section("High-scoring matches", "Five or more goals, by season", "Bars show the observed share of matches with at least five combined goals. The line uses a second axis for the season mean total goals.", plot_html(high_fig, "high-scoring-chart", 490), "Both metrics use the same season match rows and update only from recorded final scores.")}
  <section class="section"><div class="section-heading"><div><div class="eyebrow">Interactive club breakdown</div><h2>Season-by-season team output</h2></div><p>Choose any club to display its home and away goals per appearance. Dashed lines indicate away fixtures.</p></div>
    <div class="panel"><div class="controls"><div><label class="control-label" for="club-select">Club chart</label><select id="club-select">{club_options}</select></div></div>
    <div class="chart-card">{plot_html(team_fig, "club-season-chart", 500)}</div></div>
  </section>
  <section class="section"><div class="section-heading"><div><div class="eyebrow">Match-level records</div><h2>Filter the source matches</h2></div><p>Exact scores, total goals, home margin, paired xG when available, and the source attribution recorded in the CSV.</p></div>
    <div class="panel"><div class="controls">
      <div><label class="control-label" for="match-season">Season</label><select id="match-season">{season_options}</select></div>
      <div><label class="control-label" for="match-team">Club in match</label><select id="match-team">{match_options}</select></div>
    </div>
    <p id="match-count" aria-live="polite"></p>
    <div class="table-card"><div class="table-wrap"><table><thead><tr><th>Date</th><th>Season</th><th>Home club</th><th>Away club</th><th>Score</th><th class="num">Goals</th><th class="num">Home margin</th><th>xG (home–away)</th><th>Recorded source</th></tr></thead><tbody id="match-rows"></tbody></table></div></div>
    </div>
  </section>
  <script type="application/json" id="match-data">{table_rows(matches)}</script>
  <div class="data-note">{common_note} The table displays up to 100 matching rows at a time; it does not sample or alter the underlying CSV.</div>
</div>
{explorer_script()}"""
    (DOCS / "explorer.html").write_text(page("Interactive MLS match explorer", "explorer.html", explorer), encoding="utf-8")

    about = about_body(matches, apps)
    (DOCS / "about.html").write_text(page("About and data source", "about.html", about), encoding="utf-8")

    for obsolete_page in ("inter-miami-story.html", "tactical-trends.html"):
        obsolete_path = DOCS / obsolete_page
        if obsolete_path.is_file():
            obsolete_path.unlink()

    print(
        f"Built {len(NAV_ITEMS)} pages from {len(matches):,} observed matches "
        f"({matches.season.nunique()} seasons, {int(matches.total_goals.sum()):,} goals, "
        f"{int(matches.xg_complete.sum()):,} complete xG matches)."
    )


if __name__ == "__main__":
    build_site(load_matches())
