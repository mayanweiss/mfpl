# This is the Mayan's FPL Team data structure

# Team
# {'code': 3, 'draw': 0, 'form': None, 'id': 1, 'loss': 0, 'name': 'Arsenal', 'played': 0, 'points': 0, 'position': 0,
# 'short_name': 'ARS', 'strength': 4, 'team_division': None, 'unavailable': False, 'win': 0, 'strength_overall_home': 1200,
# 'strength_overall_away': 1270, 'strength_attack_home': 1160, 'strength_attack_away': 1230, 'strength_defence_home': 1160,
# 'strength_defence_away': 1240, 'pulse_id': 1}

class mfplTeam:
    def __init__(self, fpl_Team):
        # Get player data
        self.name = fpl_Team['name']
        self.short_name = fpl_Team['short_name']
        self.fpl_id = fpl_Team['id']

        self.games = []

    def add_game(self, game):
        self.games.append(game)

    def sort_games(self):
        sorted(self.games, key=lambda x: float(x{'round'}))


