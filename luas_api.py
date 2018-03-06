import flask
from flask import request, jsonify
import luas.api
from luas.api import LuasDirection
from helpers.luas_list import luas_list


app = flask.Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Luas Information</h1>
<p>add '/stops' to url for information on all stops.</p>
<p>add '/stop?id=stop_id' for information on a particular stop.</p>
<p>ids range from 1 to 71</p>'''


@app.route('/stops', methods=['GET'])
def api_all():
    return jsonify(luas_list())


@app.route('/stop', methods=['GET'])
def api_id():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'id' in request.args:
        _id = int(request.args['id'])
    else:
        return "Error: No id field provided. Please specify an id."

    # Create an empty list for our results
    results = []

    # Loop through the data and match results that fit the requested ID.
    # IDs are unique, but other fields might return many results
    for stop in luas_list():
        if stop['stop_number'] == _id:
            lc = luas.api.LuasClient()
            inbound = dict(stop)
            outbound = dict(stop)

            inbound_dest = str(lc.next_tram(stop['abbr'], LuasDirection.Inbound).destination)
            try:
                inbound_due = int(lc.next_tram(stop['abbr'], LuasDirection.Inbound).due)
            except ValueError:
                inbound_due = 'DUE'
            inbound['destination'] = inbound_dest
            inbound['due'] = inbound_due

            outbound_dest = str(lc.next_tram(stop['abbr'], LuasDirection.Outbound).destination)
            try:
                outbound_due = int(lc.next_tram(stop['abbr'], LuasDirection.Outbound).due)
            except ValueError:
                outbound_due = 'DUE'
            outbound['destination'] = outbound_dest
            outbound['due'] = outbound_due

            results.append(inbound)
            results.append(outbound)
            print(results)

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(results)


app.run()
