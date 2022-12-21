import csv
import json

import requests
import tweepy
import graphh

from cartographie import *
from geo import *
from suspect import Suspect

SUSPECTS_COLORS = {
    "Jean-Michel": "purple",
    "Georges": "green",
    "Robert": "red",
    "Christiane": "blue"
}

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
    map = creer_carte("Bretagne")
    for s in lst_suspects:
        s.draw_loc_history(map)
    afficher_carte(map)


def get_provider_data() -> dict:
    """
    Fetches the json file containing data about antennas and the location of
    each suspect's phone. 
    """
    return requests.get(
        "http://my-json-server.typicode.com/alemaitr/python_opendata_l2/bornage").json()


if __name__ == "__main__":
    # Initialize clients and suspects 
    twclient, ghclient = api_init()
    lst_suspects = import_suspects(twclient)

    # Fetch data from phone antennas
    phone_loc_history = get_provider_data()

    for person in lst_suspects:
        # Build the suspect's location history
        person.get_twitter_loc_history()
        person.get_phone_loc_history(phone_loc_history)

        # First attempt to innocent the suspect, using their last known 
        # location *before* the crime
        innocent_suspect(ghclient, person.last_known_loc(), person)

        # If it isn't sufficient, try again with their first known location
        # *after* the crime
        if person.is_suspect:
            innocent_suspect(ghclient, person.first_known_loc(), person)
        
    for person in lst_suspects :
        if person.is_suspect:
            print(f'Le meurtrier est donc : {person.name}')

    # dessine la map
    # plot_map(lst_suspect)