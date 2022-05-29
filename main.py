# this is the main running code for Mayan's Fantasy Premier League (mfpl) code
import sys
sys.path.append(".")

from venv.mfplData import *
from venv.mfplPlayers import *
import pickle
import time
#import pandas
#import tabulate

# Files location and names
data_base_folder = '/Users/mayan/PycharmProjects/mfpl/data/'
bootstrap_data_file = 'bootstrap_data.pkl'
time_file = 'time.txt'
players_data_file = 'players_data.pkl'


# the game week we are testing (for now as a constant)
gw_to_test = 28.1


# decides if we should load new data from website based on checking if this is a new day
def is_load_data_from_fpl():
    # print(data_base_folder + time_file)

    # read time of last get from fpl website
    f = open(data_base_folder + time_file, 'r')
    time_string = f.readline()
    print('Last data retrieving time from FPL:' + time_string)
    # convert string to time
    previous_time = time.strptime(time_string, "%a %b %d %H:%M:%S %Y")
    f.close()

    #get current time
    current_time = time.localtime()
    print('Current time:' + time.asctime(current_time))

    # if same day of month, don't retrieve data
    if previous_time[2] == current_time[2]:
        return False
    else:
        # update time file to current time
        f = open(data_base_folder + time_file, 'w')
        f.write(time.asctime())
        f.close()
        return True


# Load Bootstrap and Fixures data
def load_fpl_bootstrap_data(load_data_from_fpl, force_update=False):
    # Create empty mfpl data obj
    mfd = mfplData()

    # Do we need to load data from FPL website?
    if load_data_from_fpl or force_update:
        # Retrieve bootstrap and fixtures data from FPL website
        print("Retrieving bootstrap and fixtures data from FPL website")
        mfd.mfpl_get_bootstrap_info()
        mfd.mfpl_get_fixtures_info()
        # write bootstrap and fixtures data to file
        replace_data_on_file(mfd, data_base_folder + bootstrap_data_file)
    else:
        # Read data from file
        print("Loading bootstrap and fixtures from data file")
        mfd = get_data_from_file(data_base_folder + bootstrap_data_file)

    return mfd


# Load players data
def load_fpl_players_data(load_data_from_fpl, mfd, force_update=False):
    # Create empty players data obj
    players = mfplPlayers()

    # Do we need to load data from FPL website?
    if load_data_from_fpl or force_update:
        # Retrieve players data from FPL website
        print("Retrieving players data from FPL website")
        players.get_players_data(mfd)
        # write players data to file
        replace_data_on_file(players, data_base_folder + players_data_file)
    else:
        # Read data from file
        print("Loading players from data file")
        players = get_data_from_file(data_base_folder + players_data_file)

    return players

# overwrite data file
def replace_data_on_file(obj, filename):
    print("replacing pkl file:" + filename)
    with open(filename, 'wb') as outp:  # Overwrites any existing file.
        pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)

# load data from file
def get_data_from_file(filename):
    print("loading pkl file:" + filename)
    with open(filename, 'rb') as inp:
        return pickle.load(inp)


if __name__ == '__main__':
    # is data on files up to date?
    is_load_data_from_fpl = is_load_data_from_fpl()

    # get all data loaded to objects
    mfd = load_fpl_bootstrap_data(is_load_data_from_fpl )
    players = load_fpl_players_data(is_load_data_from_fpl, mfd) #, True)

    # run testing logic functions
    # players.print_top_latest_bps_players_on_gw_table(gw_to_test)
    players.print_top_latest_bps_players_on_gw(gw_to_test)
    players.print_top_players_by_point_on_gw(gw_to_test)

    # Done
    print("All Done :)")
