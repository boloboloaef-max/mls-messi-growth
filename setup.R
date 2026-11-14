if (!require("tidyverse")) install.packages("tidyverse", repos = "https://cloud.r-project.org")
if (!require("plotly")) install.packages("plotly", repos = "https://cloud.r-project.org")
if (!require("worldfootballR")) install.packages("worldfootballR", repos = "https://cloud.r-project.org")

library(tidyverse)
library(worldfootballR)

# Descargar miles de partidos reales de la MLS (2018-2026)
mls <- fb_match_results(country = "USA", gender = "M", season_end_year = 2018:2026)
write_csv(mls, "mls_matches.csv")
