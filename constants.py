import datetime 
import pytz

CRIME_LOCATION = [48.11859, -1.70322]
CRIME_DATE = datetime.datetime(2022, 11, 28, 15, 5).astimezone(pytz.timezone("Europe/Paris"))

# Colors used to display the suspect on the map
SUSPECTS_COLORS = {
    "Jean-Michel": "purple",
    "Georges": "green",
    "Robert": "red",
    "Christiane": "blue"
}

# URL used to fetch information about antennas
PHONE_OPERATORS_URL = "http://my-json-server.typicode.com/alemaitr/python_opendata_l2/bornage"