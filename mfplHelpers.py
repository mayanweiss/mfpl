# Files location and names
data_base_folder = './data/'
bootstrap_data_file = 'bootstrap_data.pkl'
time_file = 'time.txt'
players_data_file = 'players_data.pkl'
teams_data_file = 'teams_data.pkl'
csv_output = 'outputTable.csv'
improvement_csv_output = 'improvementOutputTable.csv'


# the game week we are testing (for now as a constant)
gw_to_test = 1
def set_gw_to_test(val):
    global gw_to_test
    gw_to_test = int(val)

def get_gw_to_test():
    return gw_to_test

# How many weeks to look back when calculating stats
latest_stats_games = 1
def set_latest_stats_games(val):
    global latest_stats_games
    latest_stats_games = int(val)
def get_latest_stats_games():
    return latest_stats_games

# should we update data from FPL website or not
is_get_data = False
def set_is_get_data(val):
    global is_get_data
    is_get_data = bool(val)
def get_is_get_data():
    return is_get_data

