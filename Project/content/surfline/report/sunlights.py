from datetime import datetime

from content.surfline.Spots import Spot
from .Report import Report

def get_sunlights(request, spots):
    report_type = request.get('queryResult').get('parameters').get("type")
    date = request.get('queryResult').get('parameters').get("date-time")
    city = request.get('queryResult').get('parameters').get("geo-city")
    substate = request.get('queryResult').get('parameters').get("geo-sub-state")
    state = request.get('queryResult').get('parameters').get("geo-state")
    country = request.get('queryResult').get('parameters').get("geo-country")
    
    spot = Spot(place=city, subregion=substate, region=state, country=country)
    value = spots.check_place(spot)
    print(report_type, date, city, substate, state, country)
    
    if value:
        messages = []
        text = "so, i m getting the sunlights for today"
        messages.append({"text": {"text": [text]}})
        sunlights = Report(spot, spots).get_sunLights()
        print(sunlights)
        
        now = datetime.now()
        
        if sunlights["dawn"] > now:
            print(sunlights["dawn"])
            text = "the first light today will be at {}".format(sunlights["dawn"])
            messages.append({"text": {"text": [text]}})
        if sunlights["sunrise"] > now:
            print(sunlights["sunrise"])
            text = "the sunrise will be at ".format(sunlights["sunrise"])
            messages.append({"text": {"text": [text]}})
        if sunlights["sunset"] > now:
            print(sunlights["sunset"])
            text = "the sunset will be at {}".format(sunlights["sunset"])
            messages.append({"text": {"text": [text]}})
        if sunlights["dusk"] > now:
            print(sunlights["dusk"])
            text = "the last light of sun today will be at {}".format(sunlights["dusk"])
            messages.append({"text": {"text": [text]}})
            
        if len(messages) == 1:
            text = "it is already night, come back tomorrow"
            messages = [{"text": {"text": [text]}}]
        
        return {
            "fulfillmentText": text, 
            "fulfillmentMessages": messages
        }
        
    text = "i didn't find your spot.. can you be more precise or look at the list"
    return {
        "fulfillmentText": text, 
    }
