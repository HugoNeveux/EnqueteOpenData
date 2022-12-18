import graphh


def duree_to_UFR(gh_client: graphh.GraphHopper, lieu: tuple[float]):
    coord_lieu_1 = gh_client.address_to_latlong(lieu)
    coord_lieu_2 = gh_client.address_to_latlong('Villejean-Université, Rennes, France')
    return gh_client.duration([coord_lieu_1, coord_lieu_2], vehicle='car', unit='min')
