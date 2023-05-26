import streamlit as st
from src.team.team_data import get_team_data
from src.team.team_visuals import plot_standings_chart


def show():
    st.title("Team Stats")

    season = st.text_input("Enter season (e.g., 2021-2022):")
    if season:
        team_data = get_team_data(season)

        st.subheader("Team Win Percentages")
        plot_standings_chart(team_data)
