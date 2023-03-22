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
            
        if report_type == "wind":
            text = "so, i m getting the wind for today"
            messages.append({"text": {"text": [text]}})
            if report["optimalScore"] == 2:
                messages.append({"text": {"text": ["it s firin"]}})
            forecast = "wind is {} ({}), with speed between {} and {} km/h".format(
                report["directionType"], int(report["direction"]), report["speed"], report["gust"])
            messages.append({"text": {"text": [forecast]}})
            
        if report_type == "swell":
            text = "so, i m getting the swell for today"
            messages.append({"text": {"text": [text]}})
            if report["optimalScore"] == 2:
                messages.append({"text": {"text": ["it s firin"]}})
            forecast = "swell is {}m high, with {}s period".format(
                round(report["height"], 2), report["period"])
            messages.append({"text": {"text": [forecast]}})   
        
        if report_type == "weather":
            text = "so, i m getting the weather for today"
            messages.append({"text": {"text": [text]}})
            temperature = "air temperature is {}".format(report["temperature"])
            condition = "it s {}".format(report["condition"].lower())
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
    
    
    
def get_full_report(request, spots):
    date = request.get('queryResult').get('parameters').get("date-time")
    city = request.get('queryResult').get('parameters').get("geo-city")
    substate = request.get('queryResult').get('parameters').get("geo-sub-state")
    state = request.get('queryResult').get('parameters').get("geo-state")
    country = request.get('queryResult').get('parameters').get("geo-country")
    
    spot = Spot(place=city, subregion=substate, region=state, country=country)
    value = spots.check_place(spot)
    print("full report", date, city, substate, state, country)
    
    if value:
        messages = []
        report = Report(spot, spots)
        text = "so, i m getting today s report"
        messages.append({"text": {"text": [text]}})
        
        # waves 
        waves = report.get_report("wave")
        forecast = "waves are {}, i mean {}m".format(waves["humanRelation"].lower(), waves["min"])
        messages.append({"text": {"text": [forecast]}})
        # wind 
        wind = report.get_report("wind")
        forecast = "wind is {} ({}), with speed between {} and {} km/h".format(wind["directionType"], int(wind["direction"]), wind["speed"], wind["gust"])
        messages.append({"text": {"text": [forecast]}})
        # weather
        weather = report.get_report("weather")
        forecast = "air temperature is {} and weather is {}".format(weather["temperature"], weather["condition"].lower())
        messages.append({"text": {"text": [forecast]}})  
        # tides 
        high = report.get_next_high_tide()
        low = report.get_next_low_tide()
        if high:
            high_tides = "the next high tide is {}, {}m".format(high[0].strftime("%H:%M"), high[1])
            messages.append({"text": {"text": [high_tides]}})
        if low:
            low_tides = "the next low tide is {}, {}m".format(low[0].strftime("%H:%M"), low[1])
            messages.append({"text": {"text": [low_tides]}})
        # sunlight
        now = datetime.now()
        sunlights = report.get_sunLights()
        if sunlights["sunset"] > now:
            print(sunlights["sunset"])
            text = "the sunset will be at {}".format(sunlights["sunset"].strftime("%H:%M"))
            messages.append({"text": {"text": [text]}})
        if sunlights["dusk"] > now:
            print(sunlights["dusk"])
            text = "the last light of sun today will be at {}".format(sunlights["dusk"].strftime("%H:%M"))
            messages.append({"text": {"text": [text]}})
        
        if (waves["optimalScore"] == 2) & (wind["optimalScore"] == 2):
            messages.append({"text": {"text": ["it will be firin"]}})
            
        return {
            "fulfillmentText": text, 
            "fulfillmentMessages": messages
        }
        
    text = "i didn't find your spot.. can you be more precise or look at the list"
    return {
        "fulfillmentText": text, 
    }