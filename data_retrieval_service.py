# data_retrieval_service.py
import time
import pickle
import os
#from flask import Flask, render_template, url_for
from mfplHelpers import data_base_folder, time_file, bootstrap_data_file, players_data_file
import venv.mfplData as mfplData
import venv.mfplPlayers as mfplPlayers


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


def load_fpl_bootstrap_data(load_data_from_fpl, force_update=False):
    mfd = mfplData.mfplData()
    data_file = os.path.join(data_base_folder, bootstrap_data_file)
    os.makedirs(os.path.dirname(data_file), exist_ok=True)
    
    if load_data_from_fpl or force_update or not os.path.exists(data_file):
        print("Fetching bootstrap data from FPL...")
        mfd.mfpl_get_bootstrap_info()
        mfd.mfpl_get_fixtures_info()
        replace_data_on_file(mfd, data_file)
    else:
        try:
            print("Loading bootstrap data from file...")
            mfd = get_data_from_file(data_file)
        except:
            print("Error loading bootstrap data, fetching from FPL...")
            mfd.mfpl_get_bootstrap_info()
            mfd.mfpl_get_fixtures_info()
            replace_data_on_file(mfd, data_file)
    return mfd


def load_fpl_players_data(load_data_from_fpl, mfd, force_update=False):
    players = mfplPlayers.mfplPlayers()
    data_file = os.path.join(data_base_folder, players_data_file)
    os.makedirs(os.path.dirname(data_file), exist_ok=True)
    
    if load_data_from_fpl or force_update or not os.path.exists(data_file):
        print("Fetching players data from FPL...")
        players.get_players_data(mfd)
        replace_data_on_file(players, data_file)
    else:
        try:
            print("Loading players data from file...")
            players = get_data_from_file(data_file)
        except:
            print("Error loading players data, fetching from FPL...")
            players.get_players_data(mfd)
            replace_data_on_file(players, data_file)
    return players


def replace_data_on_file(obj, filename):
    print('Replacing data on file:', filename)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'wb') as outp:
        pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)


def get_data_from_file(filename):
    print('Getting data from file:', filename)
    with open(filename, 'rb') as inp:
        return pickle.load(inp)
