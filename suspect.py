import datetime

import pytz
import tweepy

from cartographie import *


class Suspect:
    def __init__(self, nom: str, tweeter_id: int, number: int, twclient: tweepy.Client):
        """
        Class constructor. Initializes useful class attributes.
        """
        self.nom = nom
        self.tweeter_id = tweeter_id
        self.number = number
        self.client = twclient
        # On recupère ici id en plus des info dans le csv
        self.user_id = self.client.get_user(
            username=self.tweeter_id, user_auth=True).data.id
        self.loc_history = []
        self.is_suspect = True

    def __str__(self):
        loc_hist_repr = [loc["date"].strftime(
            "%d/%m/%Y, %H:%M:%S") + f": ({loc['lat']}, {loc['long']})" for loc in self.loc_history]
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
                    'date': tweet.created_at.astimezone(pytz.timezone("Europe/Paris")),
                    'lat': tweet.geo['coordinates']['coordinates'][1],
                    'long': tweet.geo['coordinates']['coordinates'][0]
                })

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
                        "long": antenne["localisation"]["long"]
                    })

    def last_known_loc(self):
        """
        Calculates the last known position before or after the crime date.
        """
        date_crime = datetime.datetime(
            2022, 11, 28, 15, 5).astimezone(pytz.timzeone("Europe/Paris"))
        interval_min = abs(date_crime - self.loc_history[0]["date"])
        last_loc = (self.loc_history[0]
                    ["lat"], self.loc_history[0]["long"])
        loc_date = self.loc_history[0]["date"]

        for dict_loc in self.loc_history:
            date, *latlong = dict_loc.values()
            interval = abs(date_crime - loc_date)
            if interval < interval_min:
                interval_min = interval
                last_loc = latlong
                loc_date = date
        return (loc_date, last_loc)

    def draw_loc_history(self, map):
        lst_lat = [loc["lat"] for loc in self.loc_history]
        lst_long = [loc["long"] for loc in self.loc_history]
        tracer_ligne(map, lst_long, lst_lat, self.nom)
