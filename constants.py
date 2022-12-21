# 22101722 Florent Cheyron <florent.cheyron@etudiant.univ-rennes2.fr>
# 22107583 Hugo Neveux <hugo.neveux@etudiant.univ-rennes2.fr>
# File constants.py, december 2022

import datetime 
import pytz

CRIME_LOCATION = [48.11859, -1.70322]
CRIME_DATE = datetime.datetime(2022, 11, 28, 15, 5).astimezone(pytz.timezone("Europe/Paris"))
CRIME_DAY_BEGIN = datetime.datetime(2022, 11, 28, 0, 0).astimezone(pytz.timezone("Europe/Paris"))
CRIME_DAY_END = datetime.datetime(2022, 11, 28, 23, 59).astimezone(pytz.timezone("Europe/Paris"))

# Colors used to display the suspect on the map
SUSPECTS_COLORS = {
    "Jean-Michel": "purple",
    "Georges": "green",
    "Robert": "red",
    "Christiane": "blue"
}

# URL used to fetch information about antennas
PHONE_OPERATORS_URL = "http://my-json-server.typicode.com/alemaitr/python_opendata_l2/bornage"

# Source files
CREDENTIALS_FILE = "credentials.json"
SUSPECTS_FILE = "suspects.csv"
