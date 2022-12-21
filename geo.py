import datetime
from constants import CRIME_DATE, CRIME_LOCATION

def temps_to_UFR(gh_client, dico: dict, suspect):
    """ 
    Innocent the suspect if he can't make it beetween his location and
    the murder location 
    """
    lieu = [dico['lat'], dico['long']]
    heure = dico['date']

    time_to_murder = abs(CRIME_DATE - heure)

    duration = gh_client.duration([lieu, CRIME_LOCATION], vehicle='car', unit='min')
    time_to_go = datetime.timedelta(minutes=duration)
    
    # Si la dernière loc est par bornage on verifie avec les 2 minutes d'écart
    if dico['type'] == "phone":
        time_to_go -= datetime.timedelta(minutes=2)

    if time_to_murder < time_to_go:
        # le suspect est donc innocent 
        suspect.is_suspect = False
