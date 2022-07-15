# This is the Mayan's FPL Players data structure

import requests
from venv.mfplPlayer import mfplPlayer
from tabulate import tabulate


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
            print(fpl_player['first_name'] + ', ' + fpl_player['second_name'] + ' URL:' + player_url)
            r = requests.get(player_url)
            fpl_element = r.json()

            # Create player data structure and save to dic (key is player ID)
            self.players_stats[player_id] = mfplPlayer(fpl_element, fpl_player, player_id, mfpl_data)


    # find all players with leading bsp before a game week and print their aggregated bps of the last
    #  <latest_stats_games> games before and teh gw points
    def print_top_latest_bps_players_on_gw(self, gw):
        top_players = {}
        print('')
        print('********** Calculating players latest bps for GW:' + str(gw) + '| # of players:' + str(len(self.players_stats)) + ' ********')

        table = []
        self.add_player_print_table_header(table)
        for player in self.players_stats.values():
            player.calc_latest_player_stats(gw)
            if player.latest_bps != None and player.latest_bps >= 60:
                #player.print_player_stats()
                player.add_player_to_print_table(table)

        print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))
        print("table size:", len(table)-1)

    def add_player_print_table_header(self, table):
        table.append(["Team", "Player", 'Position', 'Points', 'Minutes', 'Latest bsp', 'Latest ict', 'Latest Points',
                      'Last Game Points'])


#    def print_top_latest_bps_players_on_gw_table(self, gw):
#        top_players = {}
#        print('Calcing players latest bps for GW (Table):' + str(gw) + '| # of players:' + str(len(self.players_stats)))
#
#        table = [['Team', 'Player', 'Position', 'Latest Points', 'Latest bps', 'Latest ict', 'GW points']]
#
#        for player in self.players_stats.values():
#            player.calc_latest_player_stats(gw)
#            if player.latest_bps != None and player.latest_bps >= 50:
#                table.append(player.get_player_stats_row())
#
#
#        print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))

    # find all players with more than 6 points in a game week, and print their stats leading to this gw
    def print_top_players_by_point_on_gw(self, gw):
        print('')
        print('********** top players by points for GW:' + str(gw) + ' ******************')

        table = []
        self.add_player_print_table_header(table)

        for player in self.players_stats.values():
            if player.latest_gw_points >= 8:
                #player.print_player_stats()
                player.add_player_to_print_table(table)

        print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))
        print("table size:", len(table)-1)


