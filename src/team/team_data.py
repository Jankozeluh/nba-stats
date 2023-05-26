import pandas as pd
import streamlit
from nba_api.stats.endpoints import leaguestandingsv3


def get_team_data(season):
    standings = leaguestandingsv3.LeagueStandingsV3(season=season)
    team_data = standings.get_data_frames()[0]
    streamlit.write(team_data)
    return team_data
