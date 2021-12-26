# this is the main running code for Mayan's Fantasy Premier League (mfpl) code
import sys
import time

sys.path.append(".")

from venv.mfplData import *
from venv.mfplPlayers import *

if __name__ == '__main__':
    mfd = mfplData(time.localtime())
    mfd.mfpl_get_bootstrap_info()
    mfd.mfpl_get_fixures_info()
    players = mfplPlayers(mfd.players, mfd)
    #fd.mfpl_print_all_fixtures()

    #fpl_player_data_url_321 = 'https://fantasy.premierleague.com/api/element-summary/321/'
#    id = mfd.players[221]["id"]
#    player_url = fpl_base_url + fpl_player_data_url.format(id)
#    r = requests.get(player_url)
#    fpl_element = r.json()
#    print(fpl_element.keys())
#    player = mfplPlayer(fpl_element, mfd, id)
#    player.print_player_stats()
    #mfd.print_teams()
    #mfd.print_plyers()
    print("All Done :)")


