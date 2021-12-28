# This is the Mayan FPL data structure

positions = ("Goalkeeper", "Defender", "Midfielder", "Forward")

class mfplPlayer:
    def __init__(self, fpl_element, fpl_player, fpl_id, mfpl_data):
        self.fpl_id = fpl_id
        self.element_id = fpl_element['history'][0]['element']
        self.fpl_player = fpl_player

        self.total_played_min = None
        self.games_played = None
        self.future_fixtures = fpl_element['fixtures']
        self.played_fixtures = fpl_element['history']
        self.name = self.fpl_player['second_name']
        self.name += ', ' + self.fpl_player['first_name']
        #print('mfpl_player init: ' + str(self.fpl_id) + ' ' + self.name)
        self.team = mfpl_data.teams[fpl_player['team']-1]['name']
        self.position = positions[fpl_player['element_type']-1]

        self.reset_stats()
        self.calc_stats(mfpl_data)
        self.print_player_stats()


    def reset_stats(self):
        self.total_played_min = 0
        self.games_played = 0
        self.total_points = 0
        self.goals_scored = 0
        self.goals_conceded = 0

    def get_game_info(self, info, game, gw):
        #print('getting: ' + str(gw) +  ' ' + info + " " + str(game[info]))
        return game[info]

    def get_latest_info(self, rounds, ordered_games, info):
        r = -1
        val = 0.0
        try:
            for i in range(rounds):
                val += float(ordered_games[r][info])
                r = r-1
        except:
            print("get_latest_info exception: " + ':' + str(r) + ':' + str(val) + ':' + str(len(ordered_games)))

        return val


    def calc_stats(self, mfpl_data):
        ordered_games = []
        for game in self.played_fixtures:
            gw = game['round']
            ordered_games.append(game)
            # print('vs.:' + str(game['opponent_team']))
            #print('gameweek:' + str(gw) + ' minutes: ' + str(game['minutes']) + ' vs. ' + mfpl_data.teams[game['opponent_team']-1]['name'] + ' points:' + str(self.get_game_info('total_points',game, gw)))
            # print(str(game))
            if game['minutes'] > 0:
                self.total_played_min += self.get_game_info('minutes',game, gw)
                self.games_played += 1
                self.total_points += self.get_game_info('total_points',game, gw)
                self.goals_scored += self.get_game_info('goals_scored',game, gw)
                self.goals_conceded += self.get_game_info('goals_conceded',game, gw)
        rounds_to_lookback = 3
        round_to_calc = 0
        if len(ordered_games) >= rounds_to_lookback:
            self.latest_points = self.get_latest_info(3, ordered_games, 'total_points')
            self.latest_goals = self.get_latest_info(3, ordered_games, 'goals_scored')
            self.latest_bps = self.get_latest_info(3, ordered_games, 'bps')
            self.latest_ict_index = self.get_latest_info(3, ordered_games, 'ict_index')
        else:
            self.latest_points = 0
            self.latest_goals = 0
            self.latest_bps = 0
            self.latest_ict_index = 0



    def print_player_stats(self):
        print(self.team + ': ' + self.name + ': ' + self.position + ' ' +
              'Points:' + str(self.total_points) + ' Minutes: ' + str(self.total_played_min)  + ' latest bsp: ' + str(self.latest_bps) + ' latest ict: ' + str(self.latest_ict_index))


