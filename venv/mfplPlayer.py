# This is the Mayan's FPL Player data structure

# Players' positions for printing
positions = ("Goalkeeper", "Defender", "Midfielder", "Forward")

# How many weeks to look back when calculating stats
latest_stats_games = 3


class mfplPlayer:
    def __init__(self, fpl_element, fpl_player, fpl_id, mfpl_data):
        # Get player data
        self.fpl_id = fpl_id
        self.element_id = fpl_element['history'][0]['element']
        self.fpl_player = fpl_player
        self.future_fixtures = fpl_element['fixtures']
        self.played_fixtures = fpl_element['history']
        self.name = self.fpl_player['second_name']
        self.name += ', ' + self.fpl_player['first_name']
        self.team = mfpl_data.teams[fpl_player['team'] - 1]['name']
        self.position = positions[fpl_player['element_type'] - 1]

        #print ('initing ' + self.team + '/'s ' + self.name)

        # Reset fields
        self.total_played_min = None
        self.games_played = None
        self.ordered_games_list = [] # reversed ordered list of played game weeks
        self.ordered_games = {} # dic of played games
        self.latest_gw = -1 # latest played game (by the team, not the player)

        # load player's played games and stats
        for game in self.played_fixtures:
            round = float(game['round'])
            # if player have more than 1 game in a game week we will use gw+0.1 for the next game (i.e. 26.0 & 26.1)
            while round in self.ordered_games:
                round += 0.1
            self.ordered_games_list.append(round)
            self.ordered_games[round] = game
            if round > self.latest_gw:
                self.latest_gw = round

        # sort the played games
        self.ordered_games_list.reverse()
        print('mfpl_player init: ' + str(self.fpl_id) + ' ' + ", Team:" + self.team + '| '+ self.name + "| games:" + str(
            len(self.ordered_games)))

        #
        self.reset_stats()
        self.calc_stats(mfpl_data)
        #self.print_player_stats()

    def reset_stats(self):
        self.total_played_min = 0
        self.games_played = 0
        self.total_points = 0
        self.goals_scored = 0
        self.goals_conceded = 0

    def get_game_info(self, info, game, gw):
        #print('getting: ' + str(gw) + ' ' + info + " " + str(game[info]))
        return game[info]

    # calc latest stats before a given GW
    # Info - type of data to calc
    # index - the index in ordered_games_list that is the gw we are checking
    def get_latest_info(self, info, index):
        # reset return value
        val = 0.0
        # reset gw
        gw_id = -1

        try:
            # go over the last <latest_stats_games> team games before the relevant game we're checking
            for i in range(latest_stats_games):
                index = index + 1
                # find next gw to collect stats from
                gw_id = self.ordered_games_list[index]
                #print("get_latest_info retrieving:" + self.name + ':' + info + ' gw:' + str(gw_id) + ', index:' + str(index))
                # add this gw value to returned value
                val += float(self.get_game_info(info, self.ordered_games[gw_id], gw_id))
        except Exception as e:
            #print("get_latest_info exception: " + self.name + ': ' + str(index) + ':' + str(gw_id) + ':' + str(val) + ':' + str(
            #    len(self.ordered_games)) + ' exception: ' + str(e))
            e

        return val

    def get_latest_info_table(self, info, index):
        # reset return value
        t_val = []
        #print("get_latest_info_table " + info)

        try:
            # go over the last <latest_stats_games> team games before the relevant game we're checking
            for i in range(latest_stats_games):
                index = index + 1
                # find next gw to collect stats from
                gw_id = self.ordered_games_list[index]
                # print("get_latest_info retrieving:" + self.name + ':' + info + ' gw:' + str(gw_id) + ', index:' + str(index) + " " + str(latest_stats_games) + " " + str(float(self.get_game_info(info, self.ordered_games[gw_id], gw_id))))
                # add this gw value to returned value
                t_val.append(float(self.get_game_info(info, self.ordered_games[gw_id], gw_id)))
        except Exception as e:
            #print("get_latest_info exception: " + self.name + ': ' + str(index) + ':' + str(gw_id) + ':' + str(val) + ':' + str(
            #    len(self.ordered_games)) + ' exception: ' + str(e))
            e

        return t_val


    # calc overall stats for this player this season
    def calc_stats(self, mfpl_data):
        for game in self.ordered_games.values():
            gw = game['round']
            if game['minutes'] > 0:
                self.total_played_min += self.get_game_info('minutes', game, gw)
                self.games_played += 1
                self.total_points += self.get_game_info('total_points', game, gw)
                self.goals_scored += self.get_game_info('goals_scored', game, gw)
                self.goals_conceded += self.get_game_info('goals_conceded', game, gw)


        # calc the latest stats of the last gw teh team played for this player
        self.calc_latest_player_stats(self.latest_gw)



    # prints player and stats
    def add_player_to_print_table(self, table):
        table.append([self.team, self.name, self.position, str(self.total_points), str(self.total_played_min),
                      str(self.latest_bps), str(self.latest_ict_index), str(self.latest_points),
                      str(self.latest_game_gw_points)])

    # prints player and stats
    def add_player_to_trend_print_table(self, table):
        row = [self.team, self.name, self.position, str(self.latest_game_gw_points), str(self.latest_game_bonus_points),
               str(self.latest_game_bps)]

        #print(str(len(self.latest_points_table)),str(len(self.latest_bonus_points_table)), str(len(self.latest_bps_table)))
        for i in range(len(self.latest_points_table)):
            row.append(self.latest_points_table[i])

        for i in range(len(self.latest_bonus_points_table)):
            row.append(self.latest_bonus_points_table[i])

        for i in range(len(self.latest_bps_table)):
            row.append(self.latest_bps_table[i])

#        row_str = ""
#        for i in range(len(row)):
#            row_str += str(row[i])
#            row_str += ", "
#        print(row_str)


        table.append(row)

    # prints player and stats
    def print_player_stats(self):
        print(self.team + ': ' + self.name + ': ' + self.position + ' ' + ': ' +
              'Points:' + str(self.total_points) + ' Minutes: ' + str(self.total_played_min) + ' latest bsp: ' + str(
            self.latest_bps) + ' latest ict: ' + str(self.latest_ict_index) + ' latest points:' + str(self.latest_points) +
              ' Last game points:' + str(self.latest_game_gw_points))

    # prints player and stats
    def get_player_stats_row(self):
        return [self.team, self.name, self.position, self.total_points, self.latest_bps, self.latest_ict_index,
                self.latest_points]


    # calc lastest stats of a given gw
    def calc_latest_player_stats(self, gwToWatch):
        # reset index and return value
        index = -1
        val = 0.0

        # find index of the gw (or the week before in case the team didn't play in this gw)
        for i in range(len(self.ordered_games_list)):
            #print(str(self.ordered_games_list[i - 1] )+ ':' + str(index) + ':' + str(i))
            if self.ordered_games_list[i] <= gwToWatch:
                index = i
                #print('2: ' + str(self.ordered_games_list[i - 1]) + ':' + str(index) + ':' + str(i))
                break
        # if no GW found just return 0's (cloud happen when player joined the team after this GW)
        if index == -1:
            #print("gw wasn't found:", str(gwToWatch) + '|' + str(self.ordered_games_list))
            self.latest_points = 0
            self.latest_goals = 0
            self.latest_bps = 0
            self.latest_ict_index = 0
            self.latest_game_gw_points = 0
            self.latest_game_bonus_points = 0
            self.latest_game_bps = 0
            self.latest_bonus_points_table = []
            self.latest_bps_table = []
            self.latest_points_table = []
        else:
            # calc latest games stats for each of the below
            #gwToWatch = self.ordered_games_list[index-1]
            self.latest_points = self.get_latest_info('total_points', index)
            self.latest_goals = self.get_latest_info('goals_scored', index)
            self.latest_bps = self.get_latest_info('bps', index)
            self.latest_ict_index = self.get_latest_info('ict_index', index)
            # get this GW points (we usually want to compare latest stats with this gw points)
            self.latest_game_gw_points = self.get_game_info('total_points', self.ordered_games[self.ordered_games_list[index]], index)
            self.latest_game_bonus_points = self.get_game_info('bonus', self.ordered_games[self.ordered_games_list[index]], index)
            self.latest_bonus_points_table = self.get_latest_info_table('bonus', index)
            self.latest_bps_table = self.get_latest_info_table('bps', index)
            self.latest_points_table = self.get_latest_info_table('total_points', index)
            self.latest_game_bps = self.get_game_info('bps', self.ordered_games[self.ordered_games_list[index]], index)
