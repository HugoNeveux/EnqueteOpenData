import datetime
from constants import CRIME_DATE, CRIME_LOCATION

def innocent_suspect(ghclient, dict_loc: dict, suspect):
    """ 
    Innocents the suspect if they can't make it beetween their location and
    the crime scene 
    """
    time_format = "%Hh and %M minutes" 
    location = [dict_loc['lat'], dict_loc['long']]
    time = dict_loc['date']

    available_time = abs(CRIME_DATE - time)

    duration = ghclient.duration([location, CRIME_LOCATION], vehicle='car', unit='min')
    duration_to_crime_scene = datetime.timedelta(minutes=duration)
    
    # Taking the phone location delta (2 minutes) into account
    if dict_loc['type'] == "phone":
        duration_to_crime_scene -= datetime.timedelta(minutes=2)

    if available_time < duration_to_crime_scene:
        # Innocenting the suspect
        print(f"{suspect.name} : the suspect's last registered location is on " 
              f"{time.strftime(time_format)}. It is "
              f"{(available_time/datetime.timedelta(minutes=1)):.2f} minutes "
               "apart from the crime date and time, and they would need "
              f"{(duration_to_crime_scene.seconds)/60:.2f} minutes to get "
              f"there. Therefore, {suspect.name} is innocent.")
        suspect.is_suspect = False