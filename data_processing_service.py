# data_processing_service.py
import venv.mfplPlayer as mfplPlayer


def process_data(mfd, players, teams):
    tables = []
    tables.append([teams.print_teams_table(mfplPlayer.get_gw_to_test()), "Teams FPL points table"])
    tables.append([players.print_top_players_per_game_per_cost(mfplPlayer.get_gw_to_test()), "Top Players per Game per Cost"])
    tables.append([players.improving_players_table(mfplPlayer.get_gw_to_test()), "Top Improving Players"])
    return tables