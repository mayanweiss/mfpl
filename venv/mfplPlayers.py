# All players data

import requests
from venv.mfplPlayer import mfplPlayer

fpl_base_url = 'https://fantasy.premierleague.com/api/'
fpl_player_data_url = 'element-summary/{}/'


class mfplPlayers:
    def __init__(self, fpl_players, mfpl_data):
        self.fpl_players = fpl_players
        players_stats = {}

        for fpl_player in self.fpl_players:
            player_id = fpl_player['id']
            player_url = fpl_base_url + fpl_player_data_url.format(player_id)
            r = requests.get(player_url)
            fpl_element = r.json()
            players_stats[player_id] = mfplPlayer(fpl_element, fpl_player, player_id, mfpl_data)




