import streamlit as st
from pages import player_stats_page, team_stats_page


def main():
    st.sidebar.title("NBA Stats Dashboard")
    page_options = ["Player Stats", "Team Stats"]
    selected_page = st.sidebar.selectbox("Select a page", page_options)

    if selected_page == "Player Stats":
        player_stats_page.show()
    elif selected_page == "Team Stats":
        team_stats_page.show()


if __name__ == "__main__":
    main()
