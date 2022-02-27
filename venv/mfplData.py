# This is the Mayan FPL data structure

import requests

# URL elements
fpl_base_url = 'https://fantasy.premierleague.com/api/'
fpl_bootstrat_url = 'bootstrap-static/'
fpl_fixtures_url = 'fixtures/'
fpl_player_data_url = 'element-summary/{}/'


# Bootstrap and Fixtures data structure
class mfplData:
    def __init__(self):
        return

    # Get bootstrap data from FPL website
    # j.keys - dict_keys(['events', 'game_settings', 'phases', 'teams', 'total_players', 'elements', 'element_stats', 'element_types'])
    def mfpl_get_bootstrap_info(self):
        # Get Bootstrap data from FPL website
        print("Reading new data from FPL")
        r = requests.get(fpl_base_url + fpl_bootstrat_url)
        j = r.json()

        # updating data from FPL website
        self.players = j['elements']
        self.teams = j['teams']
        self.phases = j['phases']
        self.total_players = j['total_players']
        self.pl_players_stats = j['element_stats']
        self.pl_players_types = j['element_types']
        self.phases = j['phases']

        return

    # Get fixtures data from FPL website
    # dict_keys(['code', 'event', 'finished', 'finished_provisional', 'id', 'kickoff_time', 'minutes',
    #    'provisional_start_time', 'started', 'team_a', 'team_a_score', 'team_h', 'team_h_score', 'stats',
    #    'team_h_difficulty', 'team_a_difficulty', 'pulse_id'])
    def mfpl_get_fixtures_info(self):
        r = requests.get(fpl_base_url + fpl_fixtures_url)
        self.fixtures = r.json()
        return

    # Print game week fixtures
    def mfpl_print_gw_fixtures(self, gw):
        # go over all fixtures and find those in this game week
        print("Game Week:" + str(gw))
        for f in self.fixtures:
            if f['event'] == gw:
                h_team = self.teams[f['team_h'] - 1]['name']
                a_team = self.teams[f['team_a'] - 1]['name']
                print(h_team + ' ' + str(f['team_h_score']) + ':' + str(f['team_a_score']) + ' ' + a_team)
        print("***********************")

    # Print all fixtures
    def mfpl_print_all_fixtures(self):
        for i in range(1, 38):
            self.mfpl_print_gw_fixtures(i)

    # print teams
    def print_teams(self):
        for team in self.teams:
            print(str(team['id']) + ': ' + team['name'] + 'PusleId: ' + str(team['pulse_id']))
