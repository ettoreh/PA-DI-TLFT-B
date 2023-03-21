from .Spots import Spot
from .report.Report import Report



def _generate_suggestions(values, type=['country', 'region']):
    if values:
        text = f"please choose on {type[1]} out of those:"
        messages = [
            {"text": {"text": [text]}}
        ]
        for value in values:
            messages.append({"text": {"text": [value]}})

        return {
            "fulfillmentText": text,
                    "fulfillmentMessages": messages
                }

    else:
        text = f"i didn't find this {type[0]}.. choose one in the list"
        return {
                "fulfillmentText": text,
        }

def _generate_more(spot):
    report = Report(spot)
    text1 = "you can see where it is there"
    text2 = "or you can visit surfline for more infos"
    messages = [
        {"text": {"text": [text1]}},
        {"text": {"text": [report.maps]}},
        {"text": {"text": [text2]}},
        {"text": {"text": [report.link]}}
    ]

    return {
        "fulfillmentText": text1,
        "fulfillmentMessages": messages
    }




def get_spot_suggestions(request, spots):

    country = request.get('queryResult').get('parameters').get("geo-country")
    region = request.get('queryResult').get('parameters').get("geo-state")
    subregion = request.get('queryResult').get('parameters').get("geo-sub-state")
    place = request.get('queryResult').get('parameters').get("geo-city")
    intent = request.get('queryResult').get("intent").get("displayName")

    print(place)
    if intent == "spots - yes":
        spot = Spot(country=country, region=region, subregion=subregion, place=place)
        print(spot)
        spots.check_place(spot)
        return _generate_more(spot)

    print(subregion)
    if subregion:
        spot = Spot(country=country, region=region, subregion=subregion)
        spots.check_subregion(spot)
        values = spots.suggest_spots(spot)
        return _generate_suggestions(values, ['subregion', 'places'])

    print(region)
    if region:
        spot = Spot(country=country, region=region)
        spots.check_region(spot)
        values = spots.suggest_spots(spot)
        return _generate_suggestions(values, ['region', 'subregion'])

    print(country)
    if country:
        spot = Spot(country=country)
        spots.check_country(spot)
        values = spots.suggest_spots(spot)
        return _generate_suggestions(values)

    return None