# data_retrieval_service.py
import time
import pickle
import os
from mfpl_web_service import logger
#from flask import Flask, render_template, url_for
from mfplHelpers import data_base_folder, time_file, bootstrap_data_file, players_data_file
import venv.mfplData as mfplData
import venv.mfplPlayers as mfplPlayers
from venv.mfplTeams import mfplTeams
from mfpl_web_service import logger

def get_fpl_teams_data(mfd):
    teams = mfplTeams()
    teams.get_teams_data(mfd)
    return teams


def is_load_data_from_fpl_():
    time_f = os.path.join(data_base_folder, time_file)
    os.makedirs(os.path.dirname(time_f), exist_ok=True)
    try:
        f = open(time_f, 'r')
    except FileNotFoundError:
        f = open(time_f, 'x')
        f.write(time.asctime())
        f = open(time_f, 'r')
    time_string = f.readline()
    try:
        previous_time = time.strptime(time_string, "%a %b %d %H:%M:%S %Y")
    except ValueError:
        previous_time = time.gmtime(0)
    f.close()
    current_time = time.localtime()
    if previous_time[2] == current_time[2]:
        return False
    else:
        f = open(time_f, 'w')
        f.write(time.asctime())
        f.close()
        return True


def get_fpl_bootstrap_data_from_fpl():
    mfd = mfplData.mfplData()
    data_file = os.path.join(data_base_folder, bootstrap_data_file)
    os.makedirs(os.path.dirname(data_file), exist_ok=True)

    logger.info("Fetching bootstrap data from FPL...")
    mfd.mfpl_get_bootstrap_info()
    mfd.mfpl_get_fixtures_info()
    replace_data_on_file(mfd, data_file)
    return mfd

def get_fpl_bootstrap_data_from_file():
    data_file = os.path.join(data_base_folder, bootstrap_data_file)
    os.makedirs(os.path.dirname(data_file), exist_ok=True)

    try:
        logger.info("Loading bootstrap data from file...")
        mfd = get_data_from_file(data_file)
    except:
        logger.error("Error loading bootstrap data, fetching from FPL...")
        mfd = get_fpl_bootstrap_data_from_fpl()
    if mfd is None:
        logger.error("Error loading bootstrap data, fetching from FPL...")
        return get_fpl_bootstrap_data_from_fpl()
    return mfd



def load_fpl_bootstrap_data(load_data_from_fpl, force_update=False):
    if load_data_from_fpl or force_update:
        return get_fpl_bootstrap_data_from_fpl()
    else:
        return get_fpl_bootstrap_data_from_file()


def get_fpl_players_data_from_fpl(mfd):
    players = mfplPlayers.mfplPlayers()
    data_file = os.path.join(data_base_folder, players_data_file)
    os.makedirs(os.path.dirname(data_file), exist_ok=True)

    logger.info("Fetching players data from FPL...")
    players.get_players_data(mfd, is_sleep=False)
    replace_data_on_file(players, data_file)
    return players


def get_fpl_players_data_from_file(mfd, is_sleep=True):
    players = mfplPlayers.mfplPlayers()
    data_file = os.path.join(data_base_folder, players_data_file)
    os.makedirs(os.path.dirname(data_file), exist_ok=True)

    try:
        logger.info("Loading players data from file...")
        players = get_data_from_file(data_file)
    except:
        logger.error("Error loading players data, fetching from FPL...")
        players.get_players_data(mfd, is_sleep)
        replace_data_on_file(players, data_file)
    return players


def load_fpl_players_data(load_data_from_fpl, mfd, force_update=False, is_sleep=True):
    data_file = os.path.join(data_base_folder, players_data_file)
    os.makedirs(os.path.dirname(data_file), exist_ok=True)
    
    if load_data_from_fpl or force_update or not os.path.exists(data_file):
        return get_fpl_players_data_from_fpl(mfd)
    else:
        return get_fpl_players_data_from_file(mfd, is_sleep)


def replace_data_on_file(obj, filename):
    logger.info(f'Replacing data on file: {filename}')
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'wb') as outp:
        pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)


def get_data_from_file(filename):
    logger.info(f'Getting data from file: {filename}')
    if os.path.exists(filename):
        with open(filename, 'rb') as inp:
            return pickle.load(inp)
    else:
        logger.error(f'File does not exist: {filename}')
        return None


def main():
    while True:
        mfd = load_fpl_bootstrap_data(True)
        load_fpl_players_data(True, mfd, is_sleep=False)
        time.sleep(60*60*24) # 24 hours in seconds
        logger.info("Sleeping for 24 hours...")

if __name__ == "__main__":
    main()
