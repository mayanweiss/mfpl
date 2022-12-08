# This is the Mayan's FPL Players data structure

import requests
from venv.mfplPlayer import mfplPlayer
from venv.mfplPlayer import latest_stats_games
from tabulate import tabulate
import time
from mfplHelpers import data_base_folder, csv_output
# Files location and names
#data_base_folder = '/Users/mayan/PycharmProjects/mfpl/data/'
#bootstrap_data_file = 'outputTable.csv'


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
        count = 0
        for fpl_player in mfpl_data.players:
            # build player's url
            player_id = fpl_player['id']
            player_url = fpl_base_url + fpl_player_data_url.format(player_id)

            try:
                # retrieve player data from website
                print(fpl_player['first_name'] + ', ' + fpl_player['second_name'] + ' URL:' + player_url)
                r = requests.get(player_url)
                fpl_element = r.json()
            except Exception as e:
                print('get_players_data exception caught:' + str(e))
                time.sleep(60)


            # Create player data structure and save to dic (key is player ID)
            self.players_stats[player_id] = mfplPlayer(fpl_element, fpl_player, player_id, mfpl_data)
            #count += 1
            #if count > 9:
            #    time.sleep(10)
            #    count = 0


    # find all players with leading bsp before a game week and print their aggregated bps of the last
    #  <latest_stats_games> games before and teh gw points
    def print_top_latest_bps_players_on_gw(self, gw):
        print('********** Calculating players latest bps for GW:' + str(gw) + '| # of players:' + str(len(self.players_stats)) + ' ********')

        table = []
        self.add_player_print_table_header(table)

        # add to table each player that latest bps are high
        for player in self.players_stats.values():
            player.calc_latest_player_stats(gw)
            if player.latest_bps != None and player.latest_bps >= 60:
                #player.print_player_stats()
                player.add_player_to_print_table(table)

        print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))
        print("table size:", len(table)-1)


        return tabulate(table, headers='firstrow', tablefmt='html')

    def add_player_print_table_header(self, table):
        table.append(["Team", "Player", 'Position', 'Points', 'Minutes', 'Latest bsp', 'Latest ict', 'Latest Points',
                      'Last Game Points'])


    # find all players with more than 6 points in a game week, and print their stats leading to this gw
    def print_top_players_by_point_on_gw(self, gw):
        print('********** top players by points for GW:' + str(gw) + ' ******************')

        table = []
        self.add_player_print_table_header(table)

        # add to table each player that latest points are high
        for player in self.players_stats.values():
            player.calc_latest_player_stats(gw)
            if player.latest_game_gw_points >= 8:
                #player.print_player_stats()
                player.add_player_to_print_table(table)

        print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))
        print("table size:", len(table)-1)

        return tabulate(table, headers='firstrow', tablefmt='html')



    def print_top_players_bonus_and_bps_trend(self, gw):
        print('********** top players bonus and bps trend for GW:' + str(gw) + ' ******************')

        table = []
        self.add_player_bonus_trend_print_table_header(table)

        # add to table each player that latest bonus points are high
        for player in self.players_stats.values():
            player.calc_latest_player_stats(gw)
            if player.latest_game_bonus_points > 0:
                # player.print_player_stats()
                player.add_player_to_trend_print_table(table)

        print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))
        print("table size:", len(table) - 1)

        return tabulate(table, headers='firstrow', tablefmt='html')


    def add_player_bonus_trend_print_table_header(self, table):
        header = ["Team", "Player", 'Position', 'Points', 'Bonus', 'bps']
        for i in range(latest_stats_games):
            header.append("points-" + str(i+1))
        for i in range(latest_stats_games):
            header.append("bonus-" + str(i+1))
        for i in range(latest_stats_games):
            header.append("bps-" + str(i+1))

        table.append(header)



    def print_top_players_per_game_per_cost(self, gw):
        print('********** top players bonus and bps trend for GW:' + str(gw) + ' ******************')

        table = []

        # add to table each player that latest points per game per cost are high or have high latest points
        for player in self.players_stats.values():
            player.calc_latest_player_stats(gw)
            if (player.latest_points_p_game_p_cost > 0.79 and player.latest_points > 10) or player.latest_points > 18:
                # player.print_player_stats()
                player.add_player_to_point_p_game_p_cost_print_table(table)

        # Sort table
        table = sorted(sorted(table, key=lambda x: float(x[4]), reverse=True), key=lambda x: float(x[6]), reverse=True)


        self.add_player_per_game_per_cost_print_table_header(table)

        # write table to csv file
        content = tabulate(table, tablefmt="tsv")
        text_file = open(data_base_folder + csv_output, "w")
        text_file.write(content)
        text_file.close()


        #print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))
        print(tabulate(table, headers='firstrow', tablefmt='csv'))
        print("table size:", len(table) - 1)

        return tabulate(table, headers='firstrow', tablefmt='html')

    def add_player_per_game_per_cost_print_table_header(self, table):
        header = ["Team", "Player", 'Position', 'Points', 'Points per game per cost', 'cost', 'Weighted Points', 'Weighted points per game per cost', 'Latest GW points']

        table.insert(0, header)

