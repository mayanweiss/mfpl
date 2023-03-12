# Files location and names
data_base_folder = '/Users/mayan/PycharmProjects/mfpl/data/'
bootstrap_data_file = 'bootstrap_data.pkl'
time_file = 'time.txt'
players_data_file = 'players_data.pkl'
teams_data_file = 'teams_data.pkl'
csv_output = 'outputTable.csv'
improvement_csv_output = 'improvementOutputTable.csv'


# the game week we are testing (for now as a constant)
gw_to_test = 12
def set_gw_to_test(val):
    global gw_to_test
    gw_to_test = int(val)

def get_gw_to_test():
    return gw_to_test

# How many weeks to look back when calculating stats
latest_stats_games = 4
def set_latest_stats_games(val):
    global latest_stats_games
    latest_stats_games = int(val)
def get_latest_stats_games():
    return latest_stats_games

