from nba_api.stats.endpoints import commonplayerinfo, commonallplayers, playercareerstats
import pandas as pd


def get_player_names(player_name):
    players = commonallplayers.CommonAllPlayers()
    players_df = players.get_data_frames()[0]
    player_names = players_df["DISPLAY_FIRST_LAST"].tolist()
    matching_names = [name for name in player_names if player_name.lower() in name.lower()]
    return matching_names


def get_player_id(player_name):
    players = commonallplayers.CommonAllPlayers()
    players_df = players.get_data_frames()[0]
    player_id = players_df[players_df.DISPLAY_FIRST_LAST == player_name]["PERSON_ID"].values.tolist()
    return player_id[0] if player_id else None


def get_player_info(player_id):
    player_info = commonplayerinfo.CommonPlayerInfo(player_id=player_id)
    player_data = player_info.get_data_frames()[0]

    player_stats = {
        "Name": player_data["DISPLAY_FIRST_LAST"].values[0],
        "Team": player_data["TEAM_NAME"].values[0],
        "Position": player_data["POSITION"].values[0],
        "Height": player_data["HEIGHT"].values[0],
        "Weight": player_data["WEIGHT"].values[0],
        "College": player_data["SCHOOL"].values[0]
    }

    return pd.DataFrame(player_stats, index=[0])


def get_player_career_stats(player_id):
    player_career_stats = playercareerstats.PlayerCareerStats(player_id=player_id)
    player_career_data = player_career_stats.get_data_frames()[0]
    return player_career_data
