import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from nba_api.stats.endpoints import leaguestandingsv3


def show():
    st.title("Team Stats")

    season = st.text_input("Enter season (e.g., 2021-2022):")
    if season:
        standings = leaguestandingsv3.LeagueStandingsV3(season=season)
        team_data = standings.get_data_frames()[0]
        st.dataframe(team_data)

        if st.checkbox("Show Standings Chart"):
            plot_standings_chart(team_data)


def plot_standings_chart(team_data):
    team_data = team_data.sort_values(by="WIN_PCT", ascending=False)

    plt.figure(figsize=(8, 6))
    plt.barh(team_data["TEAM_NAME"], team_data["WIN_PCT"], color="royalblue")
    plt.xlabel("Win Percentage")
    plt.ylabel("Team")
    plt.title("NBA Standings")
    plt.tight_layout()
    st.pyplot(plt)
