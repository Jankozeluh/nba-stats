import matplotlib.pyplot as plt
import streamlit as st


def plot_standings_chart(team_data):
    team_data = team_data.sort_values(by="WinPCT", ascending=False)

    plt.figure(figsize=(8, 6))
    plt.barh(team_data["TeamName"], team_data["WinPCT"], color="royalblue")
    plt.xlabel("Win Percentage")
    plt.ylabel("Team")
    plt.title("NBA Standings")
    plt.tight_layout()
    st.pyplot(plt)
