import requests
import streamlit as st
import pandas as pd
import plotly.express as px
from nba_api.stats.endpoints import TeamDashLineups, CommonTeamRoster, TeamDashboardByGeneralSplits


def calculate_efficiency_rating(player_career_data):
    efficiency_rating = (
        player_career_data.groupby("SEASON_ID")
        .apply(
            lambda x: x["PTS"]
                      + x["REB"]
                      + x["AST"]
                      + x["STL"]
                      + x["BLK"]
                      - (x["FGA"] - x["FGM"])
                      - (x["FTA"] - x["FTM"])
                      - x["TOV"]
        )
        .reset_index(name="Efficiency Rating")
    )
    return efficiency_rating


def calculate_scoring_efficiency(player_career_data):
    player_career_data["Scoring Efficiency"] = player_career_data["PTS"] / player_career_data["FGA"]
    return player_career_data


def calculate_triple_double_probability(player_career_data, player_averages):
    # Implement your calculation logic here
    # Use player_career_data and player_averages to estimate the probability
    # of achieving a triple-double in a game
    pass


def calculate_win_shares(player_career_data):
    # Implement your calculation logic here
    # Use player_career_data to estimate the number of wins a player contributes
    pass


def calculate_pie(player_career_data):
    # Get team ID and season
    player_team_id = player_career_data["TEAM_ID"].iloc[0]
    player_season = player_career_data["SEASON_ID"].iloc[0]

    # Retrieve team roster
    team_roster = CommonTeamRoster(team_id=player_team_id, season=player_season)
    team_roster_data = team_roster.get_data_frames()[0]

    # Extract team ID and season from roster data
    team_id = team_roster_data["TeamID"].iloc[0]  # Adjust column name if necessary
    season = team_roster_data["SEASON"].iloc[0]  # Adjust column name if necessary

    # Retrieve team dashboard by general splits
    team_dashboard = TeamDashboardByGeneralSplits(team_id=team_id, season=season)
    team_dashboard_data = team_dashboard.get_data_frames()[0]

    # Calculate team totals
    team_totals = {
        "PTS": team_dashboard_data["PTS"].sum(),
        "REB": team_dashboard_data["REB"].sum(),
        "AST": team_dashboard_data["AST"].sum(),
        "STL": team_dashboard_data["STL"].sum(),
        "BLK": team_dashboard_data["BLK"].sum(),
        "TOV": team_dashboard_data["TOV"].sum()
    }

    # Calculate PIE
    epsilon = 1e-8  # Small constant to avoid division by zero
    pie = (
        (player_career_data["PTS"]
         + player_career_data["REB"]
         + player_career_data["AST"]
         + player_career_data["STL"]
         + player_career_data["BLK"]
         - player_career_data["TOV"])
        / (team_totals["PTS"]
           + team_totals["REB"]
           + team_totals["AST"]
           + team_totals["STL"]
           + team_totals["BLK"]
           - team_totals["TOV"]
           + epsilon)  # Add epsilon to avoid division by zero
    )
    return pie


def calculate_clutch_shooting_percentage(player_career_data):
    # Implement your calculation logic here
    # Calculate the shooting percentage in clutch situations compared to overall shooting percentage
    pass


def visualize_efficiency_rating(efficiency_rating):
    fig = px.line(efficiency_rating, x="SEASON_ID", y="Efficiency Rating", title="Efficiency Rating Over Seasons")
    st.plotly_chart(fig)


def visualize_scoring_efficiency(scoring_efficiency):
    fig = px.line(scoring_efficiency, x="SEASON_ID", y="Scoring Efficiency", title="Scoring Efficiency Over Seasons")
    fig.update_xaxes(title="Season")
    fig.update_yaxes(title="Scoring Efficiency")
    st.plotly_chart(fig)


def visualize_pie(pie):
    fig = px.line(x=pie.index, y=pie, title="Player Impact Estimate Over Seasons")
    fig.update_xaxes(title="Season")
    fig.update_yaxes(title="Player Impact Estimate")
    st.plotly_chart(fig)


def display_player_metrics(player_career_data, selected_seasons):
    st.subheader("Player Metrics")

    # Calculate efficiency rating
    efficiency_rating = calculate_efficiency_rating(player_career_data)
    visualize_efficiency_rating(efficiency_rating)

    scoring_efficiency_data = calculate_scoring_efficiency(player_career_data)
    visualize_scoring_efficiency(scoring_efficiency_data)

    # Calculate and visualize other metrics

    # Example: Calculate and visualize PIE
    pie = calculate_pie(player_career_data)
    visualize_pie(pie)
