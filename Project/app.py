# import flask dependencies
from flask import Flask, request, make_response, jsonify

from content.surfline.Spots import Spots
from content.surfline.report.tides import get_tides
from content.surfline.report.sunlights import get_sunlights
from content.surfline.report.reports import get_small_report, get_full_report
from content.surfline.spot import get_spot_suggestions


spots = Spots()

# initialize the flask app
app = Flask(__name__)

# default route
@app.route('/')
def hello_world():
   return 'Hello World!'


# function for responses
def results():
    # build a request object
    req = request.get_json(force=True)

    # fetch action from json
    intent = req.get('queryResult').get("intent").get("displayName")
    print(intent)
    
    if intent == "tasks":
        report_type = req.get('queryResult').get('parameters').get("type")
        if report_type == "tides":
            return get_tides(req, spots)
        elif report_type == "sunlight":
            return get_sunlights(req, spots)
        else:
            return get_small_report(req, spots, report_type)
        
    elif intent[:5] == "spots":
        return get_spot_suggestions(req, spots)
    
    elif intent == "report":
        return get_full_report(req, spots)
        
    return None


# create a route for webhook
@app.route('/webhook', methods=['POST', 'GET'])
def webhook():
    # return results()['fulfillmentText']
    return make_response(jsonify(results()))

# run the app
if __name__ == '__main__':
   app.run(debug=True)