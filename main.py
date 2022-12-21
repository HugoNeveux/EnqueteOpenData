#!/usr/bin/python3

from tools import *
from cartographie import *
from geo import *

import argparse as agp

if __name__ == "__main__":
    parser = agp.ArgumentParser(description="Parse command line arguments")
    parser.add_argument("--show-map", action="store_true", default=False, 
                        help="Display a map in your browser with every"
                             " suspect's location history.")
    parser.add_argument("--verbose", "-v", action="store_true", default=False,
                        help="Display more information when running the"
                             " program.")
    parser.add_argument("--show-paths", action="store_true", default=False,
                        help="Print each position (as a couple of coords)"
                             " for each suspect, with information on the"
                             " time and the source of this location.")
    
    args = parser.parse_args()

    # Define a function which will print text if the verbose option was 
    # selected, else do nothing
    verboseprint = print if args.verbose else lambda *a, **k: None

    # Initialize clients and suspects
    verboseprint("Initializing clients...")
    twclient, ghclient = api_init()
    lst_suspects = import_suspects(twclient)
    verboseprint("Complete.")

    # Fetch data from phone antennas
    verboseprint("Fetching phone location data...")
    phone_loc_history = get_provider_data()
    verboseprint("Complete.")

    for person in lst_suspects:
        verboseprint(f"Building location history for {person.name}...")
        # Build the suspect's location history
        person.get_twitter_loc_history()
        person.get_phone_loc_history(phone_loc_history)
        verboseprint(f"Complete.")

        if args.show_paths:
            print(person)

        # First attempt to innocent the suspect, using their last known 
        # location *before* the crime
        innocent_suspect(ghclient, person.last_known_loc(), person)

        # If it isn't sufficient, try again with their first known location
        # *after* the crime
        if person.is_suspect:
            innocent_suspect(ghclient, person.first_known_loc(), person)
        
    for person in lst_suspects:
        if person.is_suspect:
            print(f'The murderer is {person.name}')
            person.loc_history.append({
                    "date": CRIME_DATE,
                    "lat": CRIME_LOCATION[0],
                    "long": CRIME_LOCATION[1],
                    "type": None
                })
            person.sort_loc_history()
    
    if args.show_map:
        verboseprint("Displaying map...")
        plot_map(lst_suspects)


