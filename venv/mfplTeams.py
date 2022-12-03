# This is the Mayan's FPL Teams data structure

import requests
from venv.mfplTeam import mfplTeam


# Fixture:
# {'code': 2292838, 'event': 3, 'finished': True, 'finished_provisional': True, 'id': 29, 'kickoff_time': '2022-08-20T11:30:00Z',
# 'minutes': 90, 'provisional_start_time': False, 'started': True, 'team_a': 20, 'team_a_score': 0, 'team_h': 18, 'team_h_score': 1,
# 'stats': [{'identifier': 'goals_scored', 'a': [], 'h': [{'value': 1, 'element': 427}]},
# {'identifier': 'assists', 'a': [], 'h': [{'value': 1, 'element': 448}]},
# {'identifier': 'own_goals', 'a': [], 'h': []},
# {'identifier': 'penalties_saved', 'a': [], 'h': []},
# {'identifier': 'penalties_missed', 'a': [], 'h': []},
# {'identifier': 'yellow_cards', 'a': [{'value': 1, 'element': 487}, {'value': 1, 'element': 516}], 'h': [{'value': 1, 'element': 427}, {'value': 1, 'element': 433}]},
# {'identifier': 'red_cards', 'a': [], 'h': []},
# {'identifier': 'saves', 'a': [{'value': 3, 'element': 478}], 'h': [{'value': 3, 'element': 425}]},
# {'identifier': 'bonus', 'a': [], 'h': [{'value': 3, 'element': 448}, {'value': 2, 'element': 425}, {'value': 1, 'element': 427}]},
# {'identifier': 'bps', 'a': [{'value': 21, 'element': 480}, {'value': 16, 'element': 484}, {'value': 14, 'element': 478},
#                           {'value': 13, 'element': 477}, {'value': 13, 'element': 503}, {'value': 12, 'element': 589},
#                           {'value': 9, 'element': 482}, {'value': 8, 'element': 516}, {'value': 7, 'element': 486},
#                           {'value': 6, 'element': 483}, {'value': 6, 'element': 579}, {'value': 5, 'element': 479},
#                           {'value': 4, 'element': 476}, {'value': 4, 'element': 487}, {'value': 4, 'element': 491},
#                           {'value': 3, 'element': 481}],
#                        'h': [{'value': 33, 'element': 448}, {'value': 31, 'element': 425}, {'value': 30, 'element': 427},
#                           {'value': 29, 'element': 445}, {'value': 25, 'element': 430}, {'value': 25, 'element': 432},
#                           {'value': 25, 'element': 435}, {'value': 20, 'element': 440}, {'value': 12, 'element': 433},
#                           {'value': 9, 'element': 446}, {'value': 4, 'element': 436}, {'value': 4, 'element': 444},
#                           {'value': 3, 'element': 454}, {'value': -2, 'element': 428}]}],
# 'team_h_difficulty': 2, 'team_a_difficulty': 4, 'pulse_id': 74939}

# all Teams
class mfplTeams:
    def __init__(self):
        # all players data dictionaries, player id is the key
        self.teams = {}

    def get_teams_data(self, teams, fixtures):

        for team in teams:
            self.teams[team['id']] = mfplTeam(team)

        for fixutre in fixtures:
            self.teams[fixture['team_a']].add_game(fixture)
            self.teams[fixture['team_h']].add_game(fixture)






