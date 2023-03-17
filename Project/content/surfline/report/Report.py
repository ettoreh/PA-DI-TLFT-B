from datetime import datetime
from pysurfline import SurfReport

from ..Spots import Spots
from ...utils.time import to_time



class Report():
    def __init__(self, spot, spots=Spots()) -> None:
        self.spot = spot
        self.id = spots.get_id(spot)
        self.link = "https://www.surfline.com/surf-report/{}/{}".format(
            self.id[0], self.id[1]
        )
        self.maps = "https://www.google.com/maps/place/{}".format(self.id[0])
        
        self.report = self.find_data()
        
        pass
    
    def redirect_to_website(self):
        return self.link
    
    def find_data(self, days=1, intervalHours=3):
        params = {
            "spotId": self.id[1],
            "days": days,
            "intervalHours": intervalHours,
        }
        report = SurfReport(params)
        report.api_log
        return report
    
    def get_sunLights(self):
        sunlight = self.report.get_dataframe("sunlightTimes")
        return {
                "dawn": to_time(sunlight["dawn"].values[0]),
                "sunrise": to_time(sunlight["sunrise"].values[0]),
                "sunset": to_time(sunlight["sunset"].values[0]),
                "dusk": to_time(sunlight["dusk"].values[0])
            }
        
    def get_tides(self):
        tides = self.report.get_dataframe("tides")
        tides = tides.loc[tides.type != "NORMAL"]
        return {
            to_time(i): [row["type"], row["height"]] for i, row in tides.iterrows()
        }
        
    def get_next_high_tide(self):
        tides = self.get_tides()
        tides = {k: v for k, v in tides.items() if v[0]=="HIGH"}
        now = datetime.now()
        for h, v in tides.items():
            if h > now:
                return (h, v[1])
        return None 
    
    def get_next_low_tide(self):
        tides = self.get_tides()
        tides = {k: v for k, v in tides.items() if v[0]=="LOW"}
        now = datetime.now()
        for h, v in tides.items():
            if h > now:
                return (h, v[1])
        return None 
    
    def get_weather_data(self):
        data = self.report.get_dataframe('weather')
        return {
            to_time(i): {
                "temperature": row["temperature"],
                "condition": row["condition"]
            } for i, row in data.iterrows()
        }
        
    def get_wind_data(self):
        data = self.report.get_dataframe('wind')
        return {
            to_time(i): {
                "speed": row["speed"],
                "direction": row["direction"],
                "directionType": row["directionType"],
                "gust": row["gust"],
                "optimalScore": row["optimalScore"]
            } for i, row in data.iterrows()
        }
    
    def get_wave_data(self):
        data = self.report.get_dataframe('wave')
        return {
            to_time(i): {
                "min": row["surf_min"],
                "max": row["surf_max"],
                "optimalScore": row["surf_optimalScore"],
                "humanRelation": row["surf_humanRelation"]
            } for i, row in data.iterrows()
        }
        
    def get_swell_data(self):
        data = self.report.get_dataframe('wave')
        return {
            to_time(i): {
                "height": row["swells"][0]['height'],
                "period": row["swells"][0]["period"],
                "impact": row["swells"][0]["impact"],
                "optimalScore": row["swells"][0]["optimalScore"]
            } for i, row in data.iterrows()
        }
        
    def get_report(self, report_type):
        data = {
            "weather": self.get_weather_data(),
            "wind": self.get_wind_data(),
            "wave": self.get_wave_data(),
            "swell": self.get_swell_data()
        }[report_type]
        now = datetime.now()
        for h, v in data.items():
            if h > now:
                return v
        return None 
    
        

if __name__=="__main__":
    from spots import Spot, Spots
    
    spots = Spots()
    spot = Spot(place='Trestraou')
    print(spots.check_place(spot))
    print(spot)
    
    report = Report(spot, spots)
    print(report.redirect_to_website())
    
    # print(report.get_sunLight())
    # print(report.get_tides())
    print(report.get_next_high_tide())
    print(report.get_next_low_tide())
    
    print(report.get_report("weather"))
    print(report.get_report("wave"))
    