import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
import matplotlib.pyplot as plt  # Voor de grafieken
import pandas as pd
from cartopy.io.img_tiles import Stamen


def kaart(filePath, terrein=True, cropped=True):
    """Maakt een kaart gebaseerd op de coordinaten in een CSV-bestand.

    terrein=True kan enkele seconden langer duren dan False. Echter krijgt de kaart dan wel een grafische background.
    cropped=False om een kaart van geheel Nederland te krijgen. Dit is handig wanneer de punten niet op één enkele
    woonplaats zijn gebasseerd.
    """
    print("Kaart aan het maken. \nEven geduld a.u.b, dit kan even duren...")
    plt.rcParams['figure.figsize'] = [8, 8]  # Grotere plots in Jupyter Notebook
    coordinaten = pd.read_csv(filePath, sep=",")
    coordinaten = coordinaten.loc[
        (coordinaten['latitude'] < 53.5) & (coordinaten['latitude'] > 50.7) & (coordinaten['longitude'] < 7.3) & (
                coordinaten['longitude'] > 3.3)]  # Filter Nederland
    coordinaten = coordinaten.values[:, :]  # DataFrame omzetten naar NP-array

    sf_path = 'data/shapefiles/gadm36_NLD_2.shp'
    sf_data = list(shpreader.Reader(sf_path).geometries())
    ax = plt.axes(projection=ccrs.EuroPP())

    if terrein:
        stamen_terrain = Stamen('terrain-background')
        ax.add_image(stamen_terrain, 12)
        ax.add_geometries(sf_data, ccrs.PlateCarree(), edgecolor='black', facecolor='none', alpha=1)
    else:
        ax.add_geometries(sf_data, ccrs.PlateCarree(), edgecolor='black', facecolor='orange', alpha=0.2, )

    if cropped:
        ax.set_extent([min(coordinaten[:, 1]), max(coordinaten[:, 1]),
                       min(coordinaten[:, 0]), max(coordinaten[:, 0])])  # Grootte gelijk aan min/max van coordinaten
    else:
        ax.set_extent([3.3, 7.3, 50.7, 53.5])  # Filter Nederland

    for lat, long in coordinaten:  # Stippen tekenen
        ax.plot(long, lat, marker='o', markersize=3, color="green", transform=ccrs.PlateCarree())

    plt.show()
