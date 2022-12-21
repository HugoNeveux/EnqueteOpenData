import datetime
from pytz import timezone


def temps_to_UFR (gh_client, dico: dict, suspect)-> None:
    """ 
    Innocent the suspect if he can't make it beetween his location and
    the murder location 
    """
    CRIME_LOCATION = [48.11859, -1.70322]
    DATE_CRIME = datetime.datetime(2022, 11, 28, 15, 5).astimezone(timezone("Europe/Paris"))

    lieu = [dico['lat'], dico['long']]
    heure = dico['date']

    format = "%Hh et %Mminutes"

    time_to_crime_scene = abs(DATE_CRIME - heure)

    duree = gh_client.duration([lieu, CRIME_LOCATION], vehicle='car', unit='min')
    time_to_go = datetime.timedelta(minutes= duree)

    # Si la dernière loc est par bornage on verifie avec les 2 minutes d'écart 
    if dico['type'] == "phone" :
        time_to_go -= datetime.timedelta(minutes=2)

    if time_to_crime_scene < time_to_go :
        # le suspect est donc innocent 
        print(f"Le suspect : {suspect.name} a été localisé à {heure.strftime(format)}, or on est a {(time_to_crime_scene/datetime.timedelta(minutes=1)):.2f} minutes de l'heure du meurtre et il faudrait {(time_to_go.seconds)/60:.2f}minutes pour aller sur les lieux du crime, donc {suspect.name} est innocent.e")

        suspect.is_suspect = False
