# Files location and names
data_base_folder = '/Users/mayan/PycharmProjects/mfpl/data/'
bootstrap_data_file = 'bootstrap_data.pkl'
time_file = 'time.txt'
players_data_file = 'players_data.pkl'


# the game week we are testing (for now as a constant)
gw_to_test = 12

def set_gw_to_test(val):
    global gw_to_test
    gw_to_test = int(val)

