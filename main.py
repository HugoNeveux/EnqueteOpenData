from tools import *
from cartographie import *
from geo import *

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
            print(f'The murderer is {person.name}')