# This is the Mayan's FPL Players data structure

import requests
from venv.mfplPlayer import mfplPlayer

# URL elements
fpl_base_url = 'https://fantasy.premierleague.com/api/'
fpl_player_data_url = 'element-summary/{}/'


# all Players
class mfplPlayers:
    def __init__(self):
        # all players data dictionaries, player id is the key
        self.players_stats = {}

    # Get every player data from FPL website
    def get_players_data(self, mfpl_data):
        for fpl_player in mfpl_data.players:
            # build player's url
            player_id = fpl_player['id']
            player_url = fpl_base_url + fpl_player_data_url.format(player_id)

            # retrieve player data from website
            r = requests.get(player_url)
            fpl_element = r.json()

            # Create player data structure and save to dic (key is player ID)
            self.players_stats[player_id] = mfplPlayer(fpl_element, fpl_player, player_id, mfpl_data)


    # find all players with leading bsp before a game week and print their aggregated bps of the last
    #  <latest_stats_games> games before and teh gw points
    def print_top_latest_bps_players_on_gw(self, gw):
        top_players = {}
        print('Calcing players latest bps for GW:' + str(gw) + '| # of players:' + str(len(self.players_stats)))
        for player in self.players_stats.values():
            player.calc_latest_player_stats(gw)
            if player.latest_bps != None and player.latest_bps >= 50:
                player.print_player_stats()


    # find all players with more than 6 points in a game week, and print their stats leading to this gw
    def print_top_players_by_point_on_gw(self, gw):
        for player in self.players_stats.values():
            gw_points = player.get_game_info('total_points',player.ordered_games[gw], gw)
            if gw_points >= 6:
                player.print_player_stats()



