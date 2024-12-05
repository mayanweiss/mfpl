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
    try:
        f = open(time_f, 'r')
    except FileNotFoundError:
        f = open(time_f, 'x')
        f = open(time_f, 'r')
    time_string = f.readline()
    previous_time = time.strptime(time_string, "%a %b %d %H:%M:%S %Y")
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
    if load_data_from_fpl or force_update:
        mfd.mfpl_get_bootstrap_info()
        mfd.mfpl_get_fixtures_info()
        replace_data_on_file(mfd, os.path.join(data_base_folder, bootstrap_data_file))
    else:
        mfd = get_data_from_file(os.path.join(data_base_folder, bootstrap_data_file))
    return mfd


def load_fpl_players_data(load_data_from_fpl, mfd, force_update=False):
    players = mfplPlayers.mfplPlayers()
    if load_data_from_fpl or force_update:
        players.get_players_data(mfd)
        replace_data_on_file(players, os.path.join(data_base_folder, players_data_file))
    else:
        players = get_data_from_file(os.path.join(data_base_folder, players_data_file))
    return players


def replace_data_on_file(obj, filename):
    print('Replacing data on file:', filename)
    with open(filename, 'wb') as outp:
        pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)


def get_data_from_file(filename):
    print('Getting data from file:', filename)
    with open(filename, 'rb') as inp:
        return pickle.load(inp)
