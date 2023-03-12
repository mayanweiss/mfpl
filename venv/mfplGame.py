# This is the Mayan's FPL Game data structure

# Fixture structure:
# {'code': 2292838, 'event': 3, 'finished': True, 'finished_provisional': True, 'id': 29, 'kickoff_time': '2022-08-20T11:30:00Z',
# 'minutes': 90, 'provisional_start_time': False, 'started': True, 'team_a': 20, 'team_a_score': 0, 'team_h': 18, 'team_h_score': 1,
# 'stats': [
# {'identifier': 'goals_scored', 'a': [], 'h': [{'value': 1, 'element': 427}]},
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

#from venv.mfplData import mfplData

class mfplGame:
    def __init__(self, mfd):
        self.mfd = mfd
        self.round = 0
        self.fixture = None

        self.team_h_id = ''
        self.team_h_name = ''
        self.team_h_short_name = ''
        self.team_h_score = 0
        self.team_h_bps = 0

        # Away team info
        self.team_a_id = ''
        self.team_a_name = ''
        self.team_a_short_name = ''
        self.team_a_score = 0
        self.team_a_bps = 0

    def set_game_stats(self, fixture):

        # Home team info
        self.team_h_id = fixture["team_h"]
        self.fixture = fixture
        self.round = fixture['event']
        self.team_h_name = self.mfd.get_team_info_by_id(self.team_a_id, "name")
        self.team_h_short_name = self.mfd.get_team_info_by_id(self.team_a_id, "short_name")
        self.team_h_score = fixture["team_h_score"]
        self.team_h_bps = 0
        for identifier in fixture["stats"]:
            if identifier["identifier"] == "bps":
                for value in identifier['h']:
                    self.team_h_bps += value["value"]

        # Away team info
        self.team_a_id = fixture["team_a"]
        self.team_a_name = self.mfd.get_team_info_by_id(self.team_a_id, "name")
        self.team_a_short_name = self.mfd.get_team_info_by_id(self.team_a_id, "short_name")
        self.team_a_score = fixture["team_a_score"]
        self.team_a_bps = 0
        for identifier in fixture["stats"]:
            if identifier["identifier"] == "bps":
                for value in identifier['a']:
                    self.team_a_bps += value["value"]

    def is_team_h_win(self):
        if self.team_h_score > self.team_a_score:
            return True
        return False

    # {'identifier': 'goals_scored', 'a': [], 'h': [{'value': 1, 'element': 427}]},
    # {'identifier': 'assists', 'a': [], 'h': [{'value': 1, 'element': 448}]},
    # {'identifier': 'own_goals', 'a': [], 'h': []},
    # {'identifier': 'penalties_saved', 'a': [], 'h': []},
    # {'identifier': 'penalties_missed', 'a': [], 'h': []},
    # {'identifier': 'yellow_cards', 'a': [{'value': 1, 'element': 487}, {'value': 1, 'element': 516}], 'h': [{'value': 1, 'element': 427}, {'value': 1, 'element': 433}]},
    # {'identifier': 'red_cards', 'a': [], 'h': []},
    # {'identifier': 'saves', 'a': [{'value': 3, 'element': 478}], 'h': [{'value': 3, 'element': 425}]},
    # {'identifier': 'bonus', 'a': [], 'h': [{'value': 3, 'element': 448}, {'value': 2, 'element': 425}, {'value': 1, 'element': 427}]},

    def get_game_points(self, fpl_id):

        # which team is this
        team = ''
        if fpl_id == self.team_h_id:
            team = 'h'
        else:
            if fpl_id == self.team_a_id:
                team = 'a'
            else:
                print("get_game_points: wrong team id:" + str(fpl_id) + "home team:" + str(team_h_id) + "away team:" + str(team_a_id))
                return 0

        # start calculating point for the team
        points = 0

#        print("get_game_points - home team:" + str(self.team_h_id) + " away team:" + str(self.team_a_id)
#              + " round:" + str(self.round))

        # Gaols - 4 points per goal
        # TODO: update based on player position
        for content in self.fixture['stats'][0][team]:
            points += content['value']*4
#        print("  Goals - point:" + str(points))

        # Assists - 3 points per goal
        # TODO: update based on player position
        for content in self.fixture['stats'][1][team]:
            points += content['value']*3
#        print("  Assists - point:" + str(points))

        # Own Goals - -2 points per goal
        for content in self.fixture['stats'][2][team]:
            points += content['value']*-2
#        print("  Own Goals - point:" + str(points))

        # Penalties Saved - 3 points per save
        for content in self.fixture['stats'][3][team]:
            points += content['value']*3
#        print("  Penalties Saved - point:" + str(points))

        # Penalties Missed - -2 points per miss
        for content in self.fixture['stats'][4][team]:
            points += content['value']*-2
#        print("  Penalties Missed - point:" + str(points))

        # Yellow Cards - -1 points per card
        for content in self.fixture['stats'][5][team]:
            points += content['value']*-1
#        print("  Yellow Cards - point:" + str(points))

        # Red Cards - -2 points per card
        for content in self.fixture['stats'][6][team]:
            points += content['value']*-2
#        print("  Red Cards - point:" + str(points))

        # Saves - point per 3 saves
        for content in self.fixture['stats'][1][team]:
            points += int(round(content['value']/3))
#        print("  Saves - point:" + str(points))

        # Bonus - bonus point as is
        for content in self.fixture['stats'][1][team]:
            points += content['value']
#        print("  Bonus - point:" + str(points))

        return points

    def get_game_goals_scored(self, fpl_id):
        if fpl_id == self.team_h_id:
            return self.team_h_score
        else:
            if fpl_id == self.team_a_id:
                return self.team_a_score
            else:
                print("get_game_goals_scored: wrong team id:" + str(fpl_id) + "home team:" + str(team_h_id) + "away team:" + str(team_a_id))
                return 0

    def get_home_game_goals_scored(self, fpl_id):
        if fpl_id == self.team_h_id:
            return self.team_h_score
        else:
            return 0

    def get_away_game_goals_scored(self, fpl_id):
        if fpl_id == self.team_a_id:
            return self.team_a_score
        else:
            return 0

    def get_game_goals_conceded(self, fpl_id):
        if fpl_id == self.team_a_id:
            return self.team_h_score
        else:
            if fpl_id == self.team_h_id:
                return self.team_a_score
            else:
                print("get_game_goals_conceded: wrong team id:" + str(fpl_id) + "home team:" + str(
                    team_h_id) + "away team:" + str(team_a_id))
                return 0

    def get_home_game_goals_conceded(self, fpl_id):
        if fpl_id == self.team_h_id:
            return self.team_a_score
        else:
            return 0

    def get_away_game_goals_conceded(self, fpl_id):
        if fpl_id == self.team_a_id:
            return self.team_h_score
        else:
            return 0

    def get_home_game_points(self, fpl_id):
        if fpl_id == self.team_a_id:
            return 0
        else:
            return self.get_game_points(fpl_id)

    def get_away_game_points(self, fpl_id):
        if fpl_id == self.team_h_id:
            return 0
        else:
            return self.get_game_points(fpl_id)


# a = {'code': 2292838, 'event': 3, 'finished': True, 'finished_provisional': True, 'id': 29, 'kickoff_time': '2022-08-20T11:30:00Z','minutes': 90, 'provisional_start_time': False, 'started': True, 'team_a': 20, 'team_a_score': 0, 'team_h': 18, 'team_h_score': 1,'stats': [{'identifier': 'goals_scored', 'a': [], 'h': [{'value': 1, 'element': 427}]},{'identifier': 'assists', 'a': [], 'h': [{'value': 1, 'element': 448}]},{'identifier': 'own_goals', 'a': [], 'h': []},{'identifier': 'penalties_saved', 'a': [], 'h': []},{'identifier': 'penalties_missed', 'a': [], 'h': []},{'identifier': 'yellow_cards', 'a': [{'value': 1, 'element': 487}, {'value': 1, 'element': 516}], 'h': [{'value': 1, 'element': 427}, {'value': 1, 'element': 433}]},{'identifier': 'red_cards', 'a': [], 'h': []},{'identifier': 'saves', 'a': [{'value': 3, 'element': 478}], 'h': [{'value': 3, 'element': 425}]}],'team_h_difficulty': 2, 'team_a_difficulty': 4, 'pulse_id': 74939}
