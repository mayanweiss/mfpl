# web_service.py
from flask import Flask, render_template, url_for, make_response
from html import unescape
from venv.forms import HeaderForm
from mfplHelpers import get_latest_stats_games, get_gw_to_test, set_latest_stats_games, set_gw_to_test, set_is_get_data, get_is_get_data
from data_retrieval_service import load_fpl_bootstrap_data, load_fpl_players_data
from data_processing_service import get_fpl_teams_data, process_data
import logging

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    try:
        logger.info("Accessing homepage")
        form = HeaderForm()
        if form.lookback.data is not None and form.round.data is not None:
            readForm(form)
        
        is_load_data_from_fpl = get_is_get_data()
        logger.info(f"Loading data from FPL: {is_load_data_from_fpl}")
        
        mfd = load_fpl_bootstrap_data(is_load_data_from_fpl)
        players = load_fpl_players_data(is_load_data_from_fpl, mfd)
        teams = get_fpl_teams_data(mfd)
        tables = process_data(mfd, players, teams)
        
        #set next call not to reload from FPL site
        form.isGetData.data = False
        return unescape(render_template('homepage.html', tables=tables, form=form,
                                    round=get_gw_to_test(), lookback=get_latest_stats_games()))
    except Exception as e:
        logger.error(f"Error in homepage: {str(e)}")
        return render_template('error.html', error=str(e)), 500

@app.route("/retrivedata", methods=['GET'])
def retriveDataFromFPL():
    try:
        logger.info("Retrieving data from FPL")
        mfd = load_fpl_bootstrap_data(True)
        load_fpl_players_data(True, mfd)
        return make_response('OK', 200)
    except Exception as e:
        logger.error(f"Error retrieving data: {str(e)}")
        return make_response(f'Error: {str(e)}', 500)

if __name__ == '__main__':
    app.run(debug=True)