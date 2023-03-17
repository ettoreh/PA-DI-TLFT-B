from content.surfline.Spots import Spot
from .Report import Report

def get_tides(request, spots):
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
        text = "so, i m getting the tide, today in {}".format(spot)
        messages.append({"text": {"text": [text]}})
        tides = Report(spot, spots)
        high = tides.get_next_high_tide()
        low = tides.get_next_low_tide()
        if high:
            print(high)
            high_tides = "the next high tide is {}, {}m".format(high[0], high[1])
            messages.append({"text": {"text": [high_tides]}})
        if low:
            print(low)
            low_tides = "the next low tide is {}, {}m".format(low[0], low[1])
            messages.append({"text": {"text": [low_tides]}})
        
        if len(messages) == 1:
            text = "it is already too late, come back tomorrow"
            messages = [{"text": {"text": [text]}}]
        
        return {
            "fulfillmentText": text, 
            "fulfillmentMessages": messages
        }
    
    text = "i didn't find your spot.. can you be more precise or look at the list"
    return {
        "fulfillmentText": text, 
    }
