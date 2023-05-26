import streamlit as st
import requests
from src.player.chart_utils import *
from src.player.nba_api_utils import (
    get_player_names,
    get_player_id,
    get_player_info,
    get_player_career_stats,
)
from src.player.player_metrics import *


def show_player_stats():
    player_name = st.text_input("Enter player name:")
    player_names = get_player_names(player_name)

    if player_names:
        selected_player = st.selectbox("Select a player", player_names)
        player_id = get_player_id(selected_player)

        if player_id:
            player_info = get_player_info(player_id)
            player_career_stats = get_player_career_stats(player_id)

            # Display player information
            st.subheader("Player Information")
            st.subheader(player_info["Name"][0])
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Team:**", player_info["Team"][0])
                st.write("**College:**", player_info["College"][0])
                st.write("**Position:**", player_info["Position"][0])
            with col2:
                st.write("**Height:**", player_info["Height"][0])
                st.write("**Weight:**", player_info["Weight"][0])

            st.divider()

            st.subheader("Stats")
            selected_seasons = st.multiselect("Select seasons", player_career_stats["SEASON_ID"].unique())

            display_player_metrics(player_career_stats, selected_seasons)
            st.divider()
            display_player_stats(player_career_stats, selected_seasons)

            player_photo_url = f"https://cdn.nba.com/headshots/nba/latest/260x190/{player_id}.png"
            response = requests.get(player_photo_url, stream=True)
            if response.status_code == 200:
                st.image(player_photo_url, use_column_width=True)
            else:
                st.image('https://cdn.nba.com/headshots/nba/latest/260x190/fallback.png')


def display_player_stats(player_career_data, selected_seasons):
    for season in selected_seasons:
        st.subheader(f"Season {season}")
        season_data = player_career_data[player_career_data["SEASON_ID"] == season]

        team = season_data["TEAM_ABBREVIATION"].values[0]
        st.write(f"**Team:** {team}")
        #     # Bar Chart for Points
        #     display_bar_chart(season_data, x="PLAYER_ID", y="PTS"))
        #     # Line Chart for Assists
        #     display_line_chart(season_data, x="PLAYER_ID", y="AST")
        #     # Scatter Chart for Field Goal Percentage and Free Throw Percentage
        #     display_scatter_chart(season_data, x="FG_PCT", y="FT_PCT")

        # Display statistics as numbers in little boxes
        stats_columns = ["PTS", "AST", "REB", "FG_PCT", "FT_PCT", "STL", "BLK"]
        num_stats = len(stats_columns)
        num_columns = min(num_stats, 2)
        num_rows = -(-num_stats // num_columns)  # Ceiling division

        col1, col2 = st.columns(num_columns)

        for i, column in enumerate(stats_columns):
            stat_value = season_data[column].values[0]
            if i < num_rows:
                with col1:
                    st.metric(label=column, value=stat_value)
            else:
                with col2:
                    st.metric(label=column, value=stat_value)
