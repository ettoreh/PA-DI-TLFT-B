import os 
import json

from difflib import SequenceMatcher



class Spots():
    def __init__(self) -> None:
        self.file_path = "Project/content/data/spot_id_list.json"
        self.spot_list = self.load_spot_list()
        
    def load_spot_list(self):
        file = open(self.file_path)
        data = json.load(file)
        return data
    
    def check_continent(self, spot):
        if spot.continent in self.spot_list.keys():
            return True
        else:
            for cntnt in self.spot_list.keys():
                if SequenceMatcher(None, cntnt, spot.continent).ratio() > 0.8:
                    spot.continent = cntnt
                    return True
        spot.continent = ""
        return False
    
    def check_country(self, spot):
        self.check_continent(spot)
        if spot.continent:
            if spot.country in self.spot_list[spot.continent].keys():
                return True
            else:
                for cntr in self.spot_list[spot.continent].keys():
                    if SequenceMatcher(None, cntr, spot.country).ratio() > 0.8:
                        spot.country = cntr
                        return True
        else:
            for continent in self.spot_list.keys():
                if spot.country in self.spot_list[continent].keys():
                    spot.continent = continent
                    return True
                else:
                    for cntr in self.spot_list[continent].keys():
                        if SequenceMatcher(None, cntr, spot.country).ratio() > 0.8:
                            spot.continent = continent
                            spot.country = cntr
                            return True
        spot.country = ""
        return False
    
    def check_region(self, spot):
        self.check_country(spot)
        if spot.continent:
            if spot.country:
                if spot.region in self.spot_list[spot.continent][spot.country].keys():
                    return True
                else:
                    for rgn in self.spot_list[spot.continent][spot.country].keys():
                        if SequenceMatcher(None, rgn, spot.region).ratio() > 0.8:
                            self.region = rgn
                            return True              
        else:
            for continent in self.spot_list.keys():
                for country in self.spot_list[continent].keys():
                    if spot.region in self.spot_list[continent][country].keys():
                        spot.continent = continent
                        spot.country = country
                        return True
                    else:
                        for rgn in self.spot_list[continent][country].keys():
                            if SequenceMatcher(None, rgn, spot.region).ratio() > 0.8:
                                spot.continent = continent
                                spot.country = country
                                spot.region = rgn
                                return True
        spot.region = ""
        return False
    
    def check_subregion(self, spot):
        self.check_region(spot)
        if spot.continent:
            if spot.country:
                if spot.region:
                    if spot.subregion in self.spot_list[spot.continent][spot.country][spot.region].keys():
                        return True
                    else:
                        for sbrgn in self.spot_list[spot.continent][spot.country][spot.region].keys():
                            if SequenceMatcher(None, sbrgn, spot.subregion).ratio() > 0.8:
                                spot.subregion = sbrgn
                                return True
        else:
            for continent in self.spot_list.keys():
                for country in self.spot_list[continent].keys():
                    for region in self.spot_list[continent][country].keys():
                        if spot.subregion in self.spot_list[continent][country][region].keys():
                            spot.continent = continent
                            spot.country = country
                            spot.region = region
                            return True
                        else:
                            for sbrgn in self.spot_list[continent][country][region].keys():
                                if SequenceMatcher(None, sbrgn, spot.region).ratio() > 0.8:
                                    spot.continent = continent
                                    spot.country = country
                                    spot.region = region
                                    spot.subregion = sbrgn
                                    return True
        spot.subregion = ""
        return False
    
    def check_place(self, spot):
        self.check_subregion(spot)
        if spot.continent:
            if spot.country:
                if spot.region:
                    if spot.subregion:
                        if spot.place in self.spot_list[spot.continent][spot.country][spot.region][spot.subregion].keys():
                            return True
                        else:
                            for plc in self.spot_list[spot.continent][spot.country][spot.region][spot.subregion].keys():
                                if SequenceMatcher(None, plc, spot.place).ratio() > 0.8:
                                    spot.places = plc
                                    return True
        for continent in self.spot_list.keys():
            for country in self.spot_list[continent].keys():
                for region in self.spot_list[continent][country].keys():
                    for subregion in self.spot_list[continent][country][region].keys():
                        if spot.place in self.spot_list[continent][country][region][subregion].keys():
                            spot.continent = continent
                            spot.country = country
                            spot.region = region
                            spot.subregion = subregion
                            return True
                        else:
                            for plc in self.spot_list[continent][country][region][subregion].keys():
                                if SequenceMatcher(None, plc, spot.place).ratio() > 0.8:
                                    spot.continent = continent
                                    spot.country = country
                                    spot.region = region
                                    spot.subregion = subregion
                                    spot.place = plc
                                    return True      
        spot.place = ""                   
        return False
        
    def suggest_spots(self, spot):
        if spot.continent:
            if spot.country:
                if spot.region:
                    if spot.subregion:
                        if spot.place:
                            suggest = list(self.spot_list[spot.continent][spot.country][spot.region][spot.subregion].keys())
                            suggest.remove(spot.place) 
                            return suggest
                        return list(self.spot_list[spot.continent][spot.country][spot.region][spot.subregion].keys())
                    return list(self.spot_list[spot.continent][spot.country][spot.region].keys())
                return list(self.spot_list[spot.continent][spot.country].keys())
            return list(self.spot_list[spot.continent].keys())
        return list(self.spot_list.keys())
    
    def get_id(self, spot):
        return self.spot_list[spot.continent][spot.country][spot.region][spot.subregion][spot.place]
        

    
    
class Spot():
    def __init__(self, place="", subregion="", region="", country="",
                 continent="") -> None:
        self.continent = continent
        self.country = country
        self.region = region
        self.subregion = subregion
        self.place = place
        
    def __str__(self) -> str:
        text = ""
        if self.place:
            text += self.place+', '
        if self.subregion:
            text += self.subregion+', '
        if self.region:
            text += self.region+', '
        if self.country:
            text += self.country+', '
        if self.continent:
            text += self.continent+', '
        return text[:-2]
    
    
       
if __name__ == "__main__":
    spots = Spots()
    
    spot1 = Spot(continent='EUrope', country='france', region='Brittany')
    
    print(spots.check_continent(spot1))
    print(spots.check_country(spot1))
    
    print()
    spot2 = Spot(region='Bretagne')
    print(spots.check_continent(spot2))
    print(spots.check_country(spot2))
    print(spots.check_region(spot2))
    print(spot2)
    spot2.subregion = "morbihan"
    print(spots.check_subregion(spot2))
    print(spot2)
    print(spots.suggest_spots(spot2))
    
    spot3 = Spot(place='Trestraou')
    print(spots.check_place(spot3))
    print(spot3)
    print(spots.suggest_spots(spot3))
    
    spot4 = Spot(continent='EUrope', country='france', region='Brittany', place='Guidel')
    
    print(spots.check_continent(spot4))
    print(spots.check_country(spot4))
    print(spots.check_region(spot4))
    print(spots.check_subregion(spot4))
    print(spots.check_place(spot4))
    print(spot4)