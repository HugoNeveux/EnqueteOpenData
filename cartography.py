# File created by Aurélie Lemaitre, providing a simple interface to draw maps
# This file was updated to avoid bokeh.tile_providers, which is deprecated

import numpy as np
from bokeh.plotting import figure, show

def coor_wgs84_to_web_mercator(lon, lat):
    """
    Converts decimal longitude/latitude to Web Mercator format
    """
    k = 6378137
    x = lon * (k * np.pi/180.0)
    y = np.log(np.tan((90 + lat) * np.pi/360.0)) * k
    return (x,y)


def create_map(Titre):
    """
    Création de la figure avec arrière plan
    """
    TOOLTIPS = [("", "$name")]
    p = figure(x_axis_type="mercator", y_axis_type="mercator",tooltips=TOOLTIPS, title=Titre,x_range=(-500000, 500000), y_range=(6000000, 6500000),)
    p.add_tile("CARTODBPOSITRON")
    return p


def plot_point(carte,long,lat,label,couleur="red"):
    x,y = coor_wgs84_to_web_mercator(long,lat)
    carte.diamond(x,y,color=couleur,size=10,name=label)


def show_map(carte):
    show(carte)


def plot_line(carte, lst_long, lst_lat, label, couleur="red"):
    x = []
    y = []
    for i in range(0,len(lst_lat)):
        cx,cy = coor_wgs84_to_web_mercator(lst_long[i],lst_lat[i])
        x.append(cx)
        y.append(cy)

    carte.line(x=x,y=y,color = couleur,width=2,name=label)

# carte = creer_carte("Bretagne")
# tracer_point(carte,-1.6742900,48.1119800,"Rennes","blue")
# tracer_point(carte, -2.025674, 48.649337, "Saint-Malo","yellow")
# tracer_ligne(carte,[-1.6742900,-1.8,-2.025674],[48.1119800,48.42,48.649337],"Rennes - Saint-Malo" )

# afficher_carte(carte)
