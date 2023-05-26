import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit as st
from nba_api.stats.endpoints import CommonTeamRoster, TeamDashboardByGeneralSplits


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


def calculate_triple_double_probability(player_career_data):
    points = player_career_data['PTS'].mean()
    rebounds = player_career_data['REB'].mean()
    assists = player_career_data['AST'].mean()

    triple_double_prob = ((points >= 10) + (rebounds >= 10) + (assists >= 10)) / 3

    return triple_double_prob


def calculate_impact_score(player_career_data):
    # Compute an "impact score" as a simplistic alternative to win shares
    # We'll use PTS, REB, AST, STL, BLK, and TOV
    # The weights are arbitrary and you might want to adjust them
    weights = {
        "PTS": player_career_data["PTS"],
        "REB": player_career_data["REB"],
        "AST": player_career_data["AST"],
        "STL": player_career_data["STL"],
        "BLK": player_career_data["BLK"],
        "TOV": player_career_data["TOV"]
    }
    impact_score = sum(player_career_data[stat].mean() * weight for stat, weight in weights.items())
    return impact_score


def calculate_clutch_shooting_percentage(player_career_data):
    clutch_shooting_percentage = player_career_data['FG3_PCT'].mean()
    return clutch_shooting_percentage


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


def calculate_scoring_composition(player_career_data):
    # Check for missing values
    if player_career_data[['FGM', 'FG3M', 'FTM', 'PTS']].isnull().any().any():
        st.warning('Missing data for scoring composition. Cannot plot.')
        return None, None, None

    # Calculate total points from 2PT field goals, 3PT field goals, and free throws
    pts_from_2pt_fg = player_career_data['FGM'] * 2 - player_career_data['FG3M'] * 3
    pts_from_3pt_fg = player_career_data['FG3M'] * 3
    pts_from_ft = player_career_data['FTM'] * 1

    # Calculate scoring composition percentages
    total_pts = player_career_data['PTS']
    pts_from_2pt_fg_pct = pts_from_2pt_fg / total_pts
    pts_from_3pt_fg_pct = pts_from_3pt_fg / total_pts
    pts_from_ft_pct = pts_from_ft / total_pts

    return pts_from_2pt_fg_pct, pts_from_3pt_fg_pct, pts_from_ft_pct


def visualize_scoring_composition(pts_from_2pt_fg_pct, pts_from_3pt_fg_pct, pts_from_ft_pct):
    # Ensure the percentages are float
    pts_from_2pt_fg_pct = pts_from_2pt_fg_pct.values[0]
    pts_from_3pt_fg_pct = pts_from_3pt_fg_pct.values[0]
    pts_from_ft_pct = pts_from_ft_pct.values[0]

    # Create DataFrame for plotting
    scoring_composition = pd.DataFrame({
        'Scoring Source': ['2PT Field Goals', '3PT Field Goals', 'Free Throws'],
        'Percentage': [pts_from_2pt_fg_pct, pts_from_3pt_fg_pct, pts_from_ft_pct]
    })

    # Plot bar chart
    fig = px.bar(scoring_composition, x='Scoring Source', y='Percentage',
                 title='Scoring Composition', color='Scoring Source',
                 color_discrete_sequence=px.colors.qualitative.Pastel)

    fig.update_layout(xaxis_title='Scoring Source',
                      yaxis_title='Percentage of Total Points',
                      yaxis=dict(
                          tickformat=".2%",
                      ))
    st.plotly_chart(fig)


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


def display_player_metrics(player_career_data):
    st.subheader("Player Metrics")

    efficiency_rating = calculate_efficiency_rating(player_career_data)
    visualize_efficiency_rating(efficiency_rating)

    scoring_efficiency_data = calculate_scoring_efficiency(player_career_data)
    visualize_scoring_efficiency(scoring_efficiency_data)

    pie = calculate_pie(player_career_data)
    visualize_pie(pie)

    pts_from_2pt_fg_pct, pts_from_3pt_fg_pct, pts_from_ft_pct = calculate_scoring_composition(player_career_data)
    visualize_scoring_composition(pts_from_2pt_fg_pct, pts_from_3pt_fg_pct, pts_from_ft_pct)
