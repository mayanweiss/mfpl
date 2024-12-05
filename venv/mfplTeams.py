# This is the Mayan's FPL Teams data structure

import requests
from venv.mfplTeam import mfplTeam
from tabulate import tabulate
import os


# all Teams
class mfplTeams:
    def __init__(self):
        self.teams = {}
        self.mfd = None
        self.fplTeams = None
        self.fixtures = None


    def get_teams_data(self, mfd):

        self.mfd = mfd

        self.fplTeams = mfd.teams
        self.fixtures = mfd.fixtures

        # set teams data in mfpl teams data structure
        for fplTeam in self.fplTeams:
            self.teams[fplTeam['id']] = mfplTeam(fplTeam, self.mfd)

        # go over all games in the league and add them (+ stats to finished games) to each team
        for fixture in self.fixtures:
            self.teams[fixture['team_a']].add_game(fixture)
            self.teams[fixture['team_h']].add_game(fixture)

        # sort each team's games based on order
        for team in self.teams.values():
            team.sort_games()
            team.calc_games()

    def print_teams_table (self, gw):
        print('********** print league table for GW:' + str(gw) + ' ******************')

        table = []

        for team in self.teams.values():
            team.add_team_print_table(table)

#        # Sort table
        table = sorted(sorted(table, key=lambda x: float(x[2]) - float(x[3]), reverse=True), key=lambda x: float(x[1]), reverse=True)
#        table = sorted(table, key=lambda x: float(x[1]), reverse=True)

        self.add_teams_print_table_header(table)

#        # write table to csv file
#        content = tabulate(table, tablefmt="tsv")
#        text_file = open(os.path.join(data_base_folder, csv_output), "w")
#        text_file.write(content)
#        text_file.close()

        # print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))
        print(tabulate(table, headers='firstrow', tablefmt='csv'))
        print("table size:", len(table) - 1)

        return tabulate(table, headers='firstrow', tablefmt='html')

    def add_teams_print_table_header(self, table):
        header = ["Team", 'Points', 'Goals', 'Conceded', 'Home Points', 'Home Goals', 'Home Conceded', 'Away Points', 'Away Goals', 'Away Conceded']

        table.insert(0, header)






