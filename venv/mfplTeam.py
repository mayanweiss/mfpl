# This is the Mayan's FPL Team data structure

# Team
# {'code': 3, 'draw': 0, 'form': None, 'id': 1, 'loss': 0, 'name': 'Arsenal', 'played': 0, 'points': 0, 'position': 0,
# 'short_name': 'ARS', 'strength': 4, 'team_division': None, 'unavailable': False, 'win': 0, 'strength_overall_home': 1200,
# 'strength_overall_away': 1270, 'strength_attack_home': 1160, 'strength_attack_away': 1230, 'strength_defence_home': 1160,
# 'strength_defence_away': 1240, 'pulse_id': 1}

from venv.mfplGame import mfplGame
from mfplHelpers import get_latest_stats_games, get_gw_to_test

class mfplTeam:
    def __init__(self, fpl_Team, mfd):

        self.mfd = mfd

        # Get player data
        self.name = fpl_Team['name']
        self.short_name = fpl_Team['short_name']
        self.fpl_id = fpl_Team['id']

        self.games = []

        self.points = 0
        self.home_points = 0
        self.away_points = 0
        self.goals_scored = 0
        self.goals_conceded = 0
        self.home_goals_scored = 0
        self.home_goals_conceded = 0
        self.away_goals_scored = 0
        self.away_goals_conceded = 0

    # add a game for this team
    def add_game(self, fixture):
        game = mfplGame(self.mfd)

        # if game finished => get stats
        if fixture['finished'] is True:
            game.set_game_stats(fixture)

        # Add to games
        self.games.append(game)

    def sort_games(self):
        sorted(self.games, key=lambda x: float(x.round))

    def calc_games(self):
        gw = get_gw_to_test()
        look_back = get_latest_stats_games()
        print("calc_games for:" + self.name )

        for game in self.games:
            if game.round > gw or game.round <= (gw-look_back):
                continue
            self.points += game.get_game_points(self.fpl_id)
            self.home_points += game.get_home_game_points(self.fpl_id)
            self.away_points += game.get_away_game_points(self.fpl_id)
            self.goals_scored += game.get_game_goals_scored(self.fpl_id)
            self.goals_conceded += game.get_game_goals_conceded(self.fpl_id)
            self.home_goals_scored += game.get_home_game_goals_scored(self.fpl_id)
            self.home_goals_conceded += game.get_home_game_goals_conceded(self.fpl_id)
            self.away_goals_scored += game.get_away_game_goals_scored(self.fpl_id)
            self.away_goals_conceded += game.get_away_game_goals_conceded(self.fpl_id)

    def add_team_print_table(self, table):
        row = [self.name, str(self.points), str(self.goals_scored), str(self.goals_conceded),
               str(self.home_points), str(self.home_goals_scored), str(self.home_goals_conceded),
               str(self.away_points), str(self.away_goals_scored), str(self.away_goals_conceded)]

        table.append(row)
