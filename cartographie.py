

import numpy as np
from bokeh.plotting import figure, show
from bokeh.tile_providers import Vendors, get_provider


#Converts decimal longitude/latitude to Web Mercator format
def coor_wgs84_to_web_mercator(lon, lat):
    k = 6378137
    x = lon * (k * np.pi/180.0)
    y = np.log(np.tan((90 + lat) * np.pi/360.0)) * k
    return (x,y)


def creer_carte(Titre):
    #Création de la figure avec arrière plan
    TOOLTIPS = [("", "$name")]
    p = figure(x_axis_type="mercator", y_axis_type="mercator",tooltips=TOOLTIPS, title=Titre,x_range=(-500000, 500000), y_range=(6000000, 6500000),)
    tile_provider = get_provider(Vendors.CARTODBPOSITRON)
    p.add_tile(tile_provider)

    return p

def tracer_point(carte,long,lat,label,couleur="red"):
    x,y = coor_wgs84_to_web_mercator(long,lat)
    carte.diamond(x,y,color=couleur,size=10,name=label)


def afficher_carte(carte):
    show(carte)

def tracer_ligne(carte, lst_long, lst_lat, label, couleur="red"):
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


