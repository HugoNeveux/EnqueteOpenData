import datetime

import pytz
import tweepy

from cartographie import *

DATE_CRIME = datetime.datetime(
            2022, 11, 28, 15, 5).astimezone(pytz.timezone("Europe/Paris"))

class Suspect:
    def __init__(self, nom: str, tweeter_id: str, number: str, color: str, twclient: tweepy.Client):
        """
        Class constructor. Initializes useful class attributes.
        """
        self.nom = nom
        self.tweeter_id = tweeter_id
        self.number = number
        self.client = twclient
        self.color = color
        # On recupère ici id en plus des infos dans le csv
        self.user_id = self.client.get_user(
            username=self.tweeter_id, user_auth=True).data.id
        self.loc_history = []
        self.is_suspect = True

    def __str__(self):
        """
        Used when printing an instance of this class. Shows an output like 
        Name:
            date, time: (longitude, latitude) [type: twitter | phone]
            ...
        """
        loc_hist_repr = [loc["date"].strftime("%d/%m/%Y, %H:%M:%S %Z") 
                         + f": ({loc['lat']}, {loc['long']}) [type: {loc['type']}]" 
                         for loc in self.loc_history]
        return self.nom + ': \n\t' + '\n\t'.join(loc_hist_repr)

    def get_twitter_loc_history(self):
        """
        Gets the suspect's location history from their tweets and adds it to 
        their location history.
        """
        response = self.client.get_users_tweets(
            self.user_id, user_auth=True, max_results=20, tweet_fields=["created_at", "geo"])
        for tweet in response.data:
            if tweet.geo and tweet.geo.get('coordinates'):
                self.loc_history.append({
                    "date": tweet.created_at.astimezone(pytz.timezone("Europe/Paris")),
                    "lat": tweet.geo["coordinates"]["coordinates"][1],
                    "long": tweet.geo["coordinates"]["coordinates"][0],
                    "type": "twitter"
                })
        self.sort_loc_history()

    def get_phone_loc_history(self, donnees_bornage: dict):
        """
        Gets the suspect's location history from their mobile phone data, and 
        adds it to their location history.
        """
        for antenne in donnees_bornage["antennes"]:
            for date, num in antenne["bornages"].items():
                dt_date = datetime.datetime.strptime(date, "%d/%m/%y-%Hh%M")
                if self.number in num:
                    self.loc_history.append({
                        "date": dt_date.astimezone(pytz.timezone("Europe/Paris")),
                        "lat": antenne["localisation"]["lat"],
                        "long": antenne["localisation"]["long"],
                        "type": "phone"
                    })
        self.sort_loc_history()

    def sort_loc_history(self):
        """
        Sorts the localization history in the chronological order.
        Using this function after editing the list (in both functions above,
        get_twitter_loc_history and get_phone_loc_history) ensures the location
        history is always sorted
        """
        self.loc_history.sort(key=lambda loc: loc["date"])

    def last_known_loc(self) -> dict:
        """
        Calculates the last known position before the crime date.
        Returns a location as a dictionary shaped like
        {
            "date": datetime,
            "lat": latitude (float),
            "long": longitude (float),
            "type": "phone" | "twitter"
        }
        """
        # loc_history is a sorted list : the first registered location is 
        # before the crime date
        location = self.loc_history[0] 
        interval_min = DATE_CRIME - location["date"]

        for dict_loc in self.loc_history:
            date = dict_loc["date"]
            interval = DATE_CRIME - date
            if interval <= interval_min and interval > datetime.timedelta(0, 0, 0):
                interval_min = interval
                location = dict_loc
        return location

    def first_known_loc(self) -> dict:
        """
        Calculates the first known position after the crime date.
        Returns a location as a dictionnary, like the function above.
        """
        location = self.loc_history[-1]
        interval_min = location["date"] - DATE_CRIME

        for dict_loc in self.loc_history:
            date = dict_loc["date"]
            interval = date - DATE_CRIME
            if interval <= interval_min and interval > datetime.timedelta(0, 0, 0):
                interval_min = interval 
                location = dict_loc 
        return location
        

    def draw_loc_history(self, map):
        """
        Draws the suspect's localization history on a map
        """
        lst_lat = [loc["lat"] for loc in self.loc_history]
        lst_long = [loc["long"] for loc in self.loc_history]
        tracer_ligne(map, lst_long, lst_lat, self.nom, self.color)
