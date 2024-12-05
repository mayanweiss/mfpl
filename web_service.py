# web_service.py
from flask import Flask, render_template, url_for, make_response
from html import unescape
from venv.forms import HeaderForm
from mfplHelpers import get_latest_stats_games, get_gw_to_test, set_latest_stats_games, set_gw_to_test, set_is_get_data, get_is_get_data
from data_retrieval_service import load_fpl_bootstrap_data, load_fpl_players_data
from data_processing_service import get_fpl_teams_data, process_data

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

def readForm(form):
    try:
        set_latest_stats_games(form.lookback.data)
    except ValueError:
        set_latest_stats_games(4)
    try:
        set_gw_to_test(form.round.data)
    except ValueError:
        set_gw_to_test(12)
    try:
        set_is_get_data(form.isGetData.data)
    except ValueError:
        set_is_get_data(False)

@app.route("/home", methods=['GET', 'POST'])
@app.route("/", methods=['GET', 'POST'])
def run():
    form = HeaderForm()
    if form.lookback.data is not None and form.round.data is not None:
        readForm(form)
    is_load_data_from_fpl = get_is_get_data()
    mfd = load_fpl_bootstrap_data(is_load_data_from_fpl)
    players = load_fpl_players_data(is_load_data_from_fpl, mfd)
    teams = get_fpl_teams_data(mfd)
    tables = process_data(mfd, players, teams)
    form.isGetData.data = False
    return unescape(render_template('homepage.html', tables=tables, form=form,
                                    round=get_gw_to_test(), lookback=get_latest_stats_games()))

@app.route("/retrivedata", methods=['GET'])
def retriveDataFromFPL():
    mfd = load_fpl_bootstrap_data(True)
    load_fpl_players_data(True, mfd)
    return make_response('OK', 200)

if __name__ == '__main__':
    app.run(debug=True)