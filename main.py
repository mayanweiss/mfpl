# this is the main running code for Mayan's Fantasy Premier League (mfpl) code
import sys
sys.path.append(".")

#from venv.mfplData import *
#from venv.mfplPlayers import *
import venv.mfplData as mfplData
import venv.mfplPlayers as mfplPlayers
import venv.mfplPlayer as mfplPlayer
from mfplHelpers import get_latest_stats_games, get_gw_to_test, set_latest_stats_games, set_gw_to_test, \
                        set_is_get_data, get_is_get_data

from flask import Flask, render_template, url_for
import pickle
import time
from html import unescape  # python 3.x
from venv.forms import HeaderForm
from mfplHelpers import data_base_folder, bootstrap_data_file, time_file, players_data_file, teams_data_file

from venv.mfplTeams import mfplTeams

# Flask configurations
app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

# TODO - replace all mfd references to a singleton


# decides if we should load new data from website based on checking if this is a new day
def is_load_data_from_fpl_():
    # print(data_base_folder + time_file)

    # read time of last get from fpl website
    try:
        f = open(data_base_folder + time_file, 'r')
    except FileNotFoundError:
        f = open(data_base_folder + time_file, 'x')
        f = open(data_base_folder + time_file, 'r')
    time_string = f.readline()
    print('Last data retrieving time from FPL:' + time_string)
    # convert string to time
    try:
        previous_time = time.strptime(time_string, "%a %b %d %H:%M:%S %Y")
    except ValueError:
        previous_time = time.gmtime(0)
    f.close()

    # Get current time
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


# Load teams data - must be taken from bootstrap data
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


# Load players data
def get_fpl_teams_data(mfd):
    # Create empty teams data obj
    teams = mfplTeams()

    # extract data
    teams.get_teams_data(mfd)

    return teams


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
        print("Setting latest_stats_games to " + str(form.lookback.data))
        set_latest_stats_games(form.lookback.data)
        print("Set latest_stats_games to " + str(get_latest_stats_games()))
    except ValueError:
        print("Setting latest_stats_games to default 4")

    try:
        print("Setting gw_to_test to " + str(form.round.data))
        set_gw_to_test(form.round.data)
        print("Set gw_to_test to " + str(get_gw_to_test()))
    except ValueError:
        print("Setting gw_to_test to default 12")

    try:
        print("Setting is_get_data to " + str(form.isGetData.data))
        set_is_get_data(form.isGetData.data)
        print("Set is_get_data to " + str(get_is_get_data()))
    except ValueError:
        print("Setting is_get_data to default False")


@app.route("/home", methods=['GET', 'POST'])
@app.route("/", methods=['GET', 'POST'])
def run():
    form = HeaderForm()
    if form.lookback.data != None and form.round.data != None :
        readForm(form)

    # is data on files up to date?
    is_load_data_from_fpl = get_is_get_data()
    #is_load_data_from_fpl = False

    print("get_is_get_data is:" + str(get_is_get_data()))

    # get all data loaded to objects
    mfd = load_fpl_bootstrap_data(is_load_data_from_fpl)
    players = load_fpl_players_data(is_load_data_from_fpl, mfd)
    # Does NOT load data just extracts it from mfd
    teams = get_fpl_teams_data(mfd)

    # run testing logic functions
    # players.print_top_latest_bps_players_on_gw_table(gw_to_test)
    tables = []
    tables.append([teams.print_teams_table(mfplPlayer.get_gw_to_test()),
                   "Teams FPL points table"])
    tables.append([players.print_top_players_per_game_per_cost(mfplPlayer.get_gw_to_test()),
                   "Top Players per Game per Cost"])
    tables.append([players.improving_players_table(mfplPlayer.get_gw_to_test()),
                   "Top Improving Players"])

    #tables.append(players.print_top_latest_bps_players_on_gw(gw_to_test))

    #tables.append(players.print_top_players_by_point_on_gw(gw_to_test))

    #tables.append(players.print_top_players_bonus_and_bps_trend(gw_to_test))

    print("is_load_data_from_fpl:" + str(is_load_data_from_fpl))
    form.isGetData.data = False
    return unescape(render_template('homepage.html', tables=tables, form=form, round = get_gw_to_test(), lookback = get_latest_stats_games() ))

    # Done
    print("All Done :)")

if __name__ == '__main__':
    app.run(degub=True)
    #run()
