from datetime import datetime

from content.surfline.Spots import Spot
from .Report import Report


def get_small_report(request, spots, report_type):
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
        report = Report(spot, spots).get_report(report_type)
        print(report)
        
        if report_type == "wave":
            text = "so, i m getting the waves for today"
            messages.append({"text": {"text": [text]}})
            if report["optimalScore"] == 2:
                messages.append({"text": {"text": ["it s firin"]}})
            forecast = "waves are {}, i mean {}m".format(report["humanRelation"].lower(), report["min"])
            messages.append({"text": {"text": [forecast]}})
            
        if report_type == "wave":
            text = "so, i m getting the wind for today"
            messages.append({"text": {"text": [text]}})
            if report["optimalScore"] == 2:
                messages.append({"text": {"text": ["it s firin"]}})
            forecast = "wind is {} ({}), with speed between {} and {}".format(
                report["directionType"], int(report["direction"]), report["speed"], report["gust"])
            messages.append({"text": {"text": [forecast]}})
            
        if report_type == "swell":
            text = "so, i m getting the swell for today"
            messages.append({"text": {"text": [text]}})
            if report["optimalScore"] == 2:
                messages.append({"text": {"text": ["it s firin"]}})
            forecast = "swell is {}m high, with {}s period".format(
                report["height"], report["period"])
            messages.append({"text": {"text": [forecast]}})   
        
        if report_type == "weather":
            text = "so, i m getting the weather for today"
            messages.append({"text": {"text": [text]}})
            temperature = "".format(report["temperature"])
        
            condition = "swell is {}m high, with {}s period".format(
                report["condition"])
            messages.append({"text": {"text": [temperature]}})  
            messages.append({"text": {"text": [condition]}})  
            
        return {
            "fulfillmentText": text, 
            "fulfillmentMessages": messages
        }
    
    text = "i didn't find your spot.. can you be more precise or look at the list"
    return {
        "fulfillmentText": text, 
    }