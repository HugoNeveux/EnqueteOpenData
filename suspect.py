# 22101722 Florent Cheyron <florent.cheyron@etudiant.univ-rennes2.fr>
# 22107583 Hugo Neveux <hugo.neveux@etudiant.univ-rennes2.fr>
# File suspect.py, december 2022

import datetime
import pytz
import tweepy

from cartography import *
from constants import *

class Suspect:
    def __init__(self, name: str, twitter_username: str, phone_number: str, color: str, twclient: tweepy.Client):
        """
        Class constructor. Initializes useful class attributes and gets the suspect's twitter id.

        name: The suspect's name
        twitter_username: The suspect's twitter account @
        phone_number: The suspect's phone number
        color: The suspect's color, used to draw their successive locations on a map
        twclient: A tweepy client object, used to get tweets written by the suspect, and their geolocalizations
        """
        self.name = name
        self.number = phone_number
        self.client = twclient
        self.color = color

        # Get the suspect's twitter id
        self.user_id = self.client.get_user(
            username=twitter_username, user_auth=True).data.id
        
        # Initialize the location history
        self.loc_history = []
        # By default, everyone is a suspect
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
        return self.name + ': \n\t' + '\n\t'.join(loc_hist_repr)


    def get_twitter_loc_history(self):
        """
        Gets the suspect's location history from their tweets and adds it to 
        their location history.
        """
        response = self.client.get_users_tweets(
            self.user_id, user_auth=True, max_results=20, 
            tweet_fields=["created_at", "geo"], start_time = CRIME_DAY_BEGIN, 
            end_time = CRIME_DAY_END)

        for tweet in response.data:
            if tweet.geo and tweet.geo.get('coordinates'):
                self.loc_history.append({
                    "date": tweet.created_at.astimezone(pytz.timezone("Europe/Paris")),
                    "lat": tweet.geo["coordinates"]["coordinates"][1],
                    "long": tweet.geo["coordinates"]["coordinates"][0],
                    "type": "twitter"
                })

        # Ensure loc_history is a sorted list
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
        
        # Ensore loc_history is a sorted list
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
        interval_min = CRIME_DATE - location["date"]

        for dict_loc in self.loc_history:
            date = dict_loc["date"]
            interval = CRIME_DATE - date
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
        interval_min = location["date"] - CRIME_DATE

        for dict_loc in self.loc_history:
            date = dict_loc["date"]
            interval = date - CRIME_DATE
            if interval <= interval_min and interval > datetime.timedelta(0, 0, 0):
                interval_min = interval 
                location = dict_loc 
        return location
        

    def draw_loc_history(self, map):
        """
        Draws the suspect's localization history on a map. 
        Dots represent the suspect's known location at a time, and lines are
        the suspect's path between those dots.
        """
        lst_lat = []
        lst_long = []

        time_format = "%Hh:%Mm:%Ss"

        # Plotting the map only for the 28/11/2022
        for loc in self.loc_history:
            if loc["date"] > CRIME_DAY_BEGIN and loc["date"] < CRIME_DAY_END:
                hour = loc["date"].strftime(time_format)
                plot_point(map, loc["long"], loc["lat"], hour, self.color)
                lst_lat.append(loc["lat"])
                lst_long.append(loc["long"])
        plot_line(map, lst_long, lst_lat, self.name, self.color)

        # Crime location point
        plot_point(map, CRIME_LOCATION[1], CRIME_LOCATION[0], "Crime location at 15h05", "yellow")
