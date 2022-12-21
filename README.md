# Enquête Open Data

End of semester project in a "Python and open data" class, in L2 MIASHS at the Université Rennes 2.

## Setup

In order to use the right version of every python module used, please run `pip install -r requirements.txt`. 

Of course, it is a better practise to use a virtual environment to install these modules and run this program.

## Usage
```
usage: td10-11.py [-h] [--show-map] [--verbose] [--show-paths]

Parse command line arguments

options:
  -h, --help     show this help message and exit
  --show-map     Display a map in your browser with every suspect's location history.
  --verbose, -v  Display more information when running the program.
  --show-paths   Print each position (as a couple of coords) for each suspect, with information on the time and the source of      
                 this location.
```

### Ways to use this program

First, running the program without any option will disculpate every suspect, and print which person is guilty.
```
python3 td10-11.py
```

Then, you can choose to display a map 
```
python3 td10-11.py --show-map
```

You can also choose to print *a lot* of text by using both options designed for it
```
python3 td10-11.py -v --show-paths
```

And of course, you can combinate every option.
```
python3 td10-11.py -v --show-map --show-paths
```

## Credits

This program was made by Florent Cheyron (22101722, <florent.cheyron@etudiant.univ-rennes2.fr>) and Hugo Neveux (22107583, <hugo.neveux@etudiant.univ-rennes2.fr>) in december 2022.