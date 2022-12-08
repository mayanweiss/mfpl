# this is the main running code for Mayan's Fantasy Premier League (mfpl) code
import sys
sys.path.append(".")

#from venv.mfplData import *
#from venv.mfplPlayers import *
import venv.mfplData as mfplData
import venv.mfplPlayers as mfplPlayers
import venv.mfplPlayer as mfplPlayer
from flask import Flask, render_template, url_for
import pickle
import time
from html import unescape  # python 3.x
from venv.forms import HeaderForm
from mfplHelpers import data_base_folder, bootstrap_data_file, time_file, players_data_file

# Flask configurations
app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'



# decides if we should load new data from website based on checking if this is a new day
def is_load_data_from_fpl_():
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
    mfd = mfplData.mfplData()

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
    players = mfplPlayers.mfplPlayers()

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


def readForm(form):
    try:
        print("Setting latest_stats_games to " +  str(form.lookback.data) + str(form.lookback.meta))
        mfplPlayer.set_latest_stats_games(form.lookback.data)
        print("Setting latest_stats_games to " +  str(form.lookback.data))
    except ValueError:
        print("Setting latest_stats_games to default 4")

    try:
        mfplPlayer.gw_to_test
        mfplPlayer.set_gw_to_test(form.round.data)
        print("Setting gw_to_test to " +  str(form.round.data))
    except ValueError:
        print("Setting gw_to_test to default 12")




@app.route("/home", methods=['GET', 'POST'])
@app.route("/", methods=['GET', 'POST'])
def run():
    form = HeaderForm()
    if form.lookback.data != None and form.round.data != None :
        readForm(form)

    # is data on files up to date?
    is_load_data_from_fpl = is_load_data_from_fpl_()
    #is_load_data_from_fpl = True

    # get all data loaded to objects
    mfd = load_fpl_bootstrap_data(is_load_data_from_fpl )
    players = load_fpl_players_data(is_load_data_from_fpl, mfd) #, True)

    # run testing logic functions
    # players.print_top_latest_bps_players_on_gw_table(gw_to_test)
    tables = []
    tables.append(players.print_top_players_per_game_per_cost(mfplPlayer.gw_to_test))

    #tables.append(players.print_top_latest_bps_players_on_gw(gw_to_test))

    #tables.append(players.print_top_players_by_point_on_gw(gw_to_test))

    #tables.append(players.print_top_players_bonus_and_bps_trend(gw_to_test))

    return unescape(render_template('homepage.html', tables=tables, form=form))

    # Done
    print("All Done :)")

if __name__ == '__main__':
    app.run(degub=True)
    #run()
