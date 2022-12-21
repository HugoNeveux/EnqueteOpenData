import tweepy 
import graphh 
import json
import requests
import csv

from suspect import Suspect
from constants import PHONE_OPERATORS_URL, SUSPECTS_COLORS
from cartography import *

def api_init() -> tuple[tweepy.Client, graphh.GraphHopper]:
    """
    Uses the credentials.json file to intiialize both tweepy and graphhopper 
    clients.
    """
    with open("credentials.json", "r") as fp:
        data = json.load(fp)
    twitter_keys = data["twitter"]

    # Twitter client
    client_tw = tweepy.Client(
        consumer_key=twitter_keys["CONSUMER_KEY"],
        consumer_secret=twitter_keys["CONSUMER_SECRET"],
        access_token=twitter_keys["ACCESS_TOKEN"],
        access_token_secret=twitter_keys["ACCESS_TOKEN_SECRET"])

    # GraphHopper client
    client_gh = graphh.GraphHopper(api_key=data["graphhopper"])
    
    return client_tw, client_gh


def import_suspects(twpclient: tweepy.Client) -> list[Suspect]:
    """
    Reads the suspects.csv file and initializes a list of suspects using 
    collected data.
    """
    with open('suspects.csv', 'r', encoding="utf-8") as fich:
        reader = csv.DictReader(fich, delimiter=';')
        return [Suspect(pers["PRENOM"], pers["IDENTIFIANT_TWITTER"],
                        pers["TELEPHONE"], SUSPECTS_COLORS[pers["PRENOM"]],
                        twpclient) for pers in reader]

def plot_map(lst_suspects: list[Suspect]):
    """
    Plots the map displaying all registered locations for each suspect.
    """
    map = create_map("Bretagne")
    for s in lst_suspects:
        s.draw_loc_history(map)
    show_map(map)


def get_provider_data() -> dict:
    """
    Fetches the json file containing data about antennas and the location of
    each suspect's phone. 
    """
    return requests.get(PHONE_OPERATORS_URL).json()