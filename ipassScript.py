import os
import time

import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
import math
import matplotlib.lines as mlines
import matplotlib.pyplot as plt  # Voor de grafieken
import numpy as np  # Om data als arrays op te kunnen slaan en de normale verdeling te kunnen tekenen
import pandas as pd
from cartopy.io.img_tiles import Stamen
from geopy.geocoders import Nominatim
from matplotlib import style  # Style van de grafiek aanpassen naar eigen smaak
from matplotlib.patches import Ellipse
from scipy.spatial import Voronoi
from scipy.spatial import voronoi_plot_2d as vorPlot
from scipy.stats import norm  # Om de lijn van de normale verdeling te tekenen. Getallen zijn zelf berekend.

style.use('ggplot')


def berekenPercentageOverlap(middelpuntAfstand, mu, sigma):
    """Berekend het percentage overlap tussen twee punten.
       Als argument dient de afstand van de twee punten tot het middelpunt te worden gegeven."""
    return norm.cdf(-middelpuntAfstand + mu, loc=mu, scale=sigma) * 2


def berekenPercentageOverlapMatrix(punten, mu, sigma):
    overlapMatrix = []
    for punt1 in punten:
        for punt2 in punten:
            middelpunt = abs((punt2 - punt1) / 2)
            middelpuntAfstand = np.sqrt(  # Wortel van (A^2 + B^2)
                np.sum(  # A^2 + B^2
                    np.square(  # Macht van A en B
                        middelpunt)))  # (ΔA, ΔB)
            percentage = berekenPercentageOverlap(middelpuntAfstand, mu, sigma)
            overlapMatrix.append(percentage)

    return np.array(overlapMatrix).reshape(len(punten), len(punten))


def berekenGrens(grens, mu, sigma):
    """Berekend het aantal standaard deviaties dat nodig is om op een bepaalde cumulatieve kans te komen.
       Dezelfde functie als invNorm op de Texas Instruments grafische rekenmachines.
       0.00 < grens < 1.00
       Kan gebruikt worden om de hoogte van de Ellipse in Voronoi-diagrammen te bepalen"""
    return norm.ppf(grens, loc=mu, scale=sigma)


def berekenHelling(puntX, puntY):
    """Berekend de helling in graden tussen twee punten.
       Kan gebruikt worden om de richting van de Ellipse in Voronoi-diagrammen te bepalen"""
    delta = puntY - puntX

    if delta[0] != 0.0:  # ZeroDivisionError voorkomen
        richtingsCoefficient = delta[1] / delta[0]
        return math.degrees(math.atan(richtingsCoefficient))
    else:
        return -90


def berekenMiddelpuntAfstanden(punten):
    """Berekend de afstand tot het middelpunt voor iedere combinatie van twee punten.
       Input is een np.array() van N bij 2.
       Gebaseerd op: https://github.com/scipy/scipy/blob/master/scipy/spatial/_plotutils.py"""
    vor = Voronoi(punten)
    middelpuntAfstanden = []

    for punt in vor.ridge_points:
        middelpunt = vor.points[punt].mean(axis=0)
        middelpuntAfstand = np.sqrt(  # Wortel van (A^2 + B^2)
            np.sum(  # A^2 + B^2
                np.square(  # Macht van A en B
                    middelpunt - vor.points[punt][0])))  # (ΔA, ΔB)
        middelpuntAfstanden.append(middelpuntAfstand)
    return middelpuntAfstanden


def plotNormaleVerdeling(mu, sigma, middelpuntAfstand, labels):
    """Plot-code afgeleid van: Thijs van den Berg (Jun. 2019)
       https://github.com/Denbergvanthijs/AC-opdrachten/

       Mu en Sigma zijn vaak 0 resp. 1
       MiddelpuntAfstand is de hemelsbrede afstand naar het middelpunt van twee punten."""
    totaleOverlap = berekenPercentageOverlap(middelpuntAfstand, mu, sigma)
    lijn = np.linspace(mu - 4 * sigma - middelpuntAfstand,
                       mu + 4 * sigma + middelpuntAfstand)  # De lijn van de normale verdelingen

    plt.plot(lijn, norm.pdf(lijn, mu - middelpuntAfstand, sigma), label=labels[0])  # De linker normale verdeling
    plt.plot(lijn, norm.pdf(lijn, mu + middelpuntAfstand, sigma), label=labels[1])  # De rechter normale verdeling
    plt.axvline(x=mu, color="black", linestyle='--', label='Middelpunt')

    plt.xlim(mu - 3 * sigma - middelpuntAfstand,
             mu + 3 * sigma + middelpuntAfstand)  # Tenminste 99,8% zichtbaar van beide verdelingen
    plt.ylim(bottom=0)
    plt.xlabel("Aantal Standaard Deviaties")
    plt.ylabel("Kans")
    plt.title(
        f"{totaleOverlap * 100:.2f}% overlapt in totaal.\nAfstand tot het middelpunt: {middelpuntAfstand:.2f} SD.")
    plt.legend()

    plt.tight_layout()  # Zodat ook de astitels op de grafieken passen
    plt.show()


def plotAlleNormaleVerdelingen(punten):
    """Plot de normale verdelingen van alle mogelijke combinaties van punten.
        Returned de afstand tot het middelpunt van alle combinaties.
        Een zichtbare Voronoi is niet nodig om berekeningen uit te voeren."""
    vor = Voronoi(punten)
    middelpuntAfstanden = berekenMiddelpuntAfstanden(punten)

    for i, punt in enumerate(middelpuntAfstanden):
        plotNormaleVerdeling(0, 1, punt, vor.points[vor.ridge_points[i]])


def plotVoronoi(punten):
    """Plot een Voronoi-diagram ter grote van de maximale x en y-coördinaten."""
    vorPlot(Voronoi(punten))
    plt.xlabel("X-coördinaten")
    plt.ylabel("Y-coördinaten")
    plt.legend(
        handles=[mlines.Line2D([0], [0], marker='o', color='w', label='Punt', markerfacecolor='r', markersize=15)])
    plt.show()


def plotVoronoiCompleet(punten, mu, sigma):
    """Plot een Voronoi-diagram ter grote van de maximale x en y-coördinaten.
       Bij ieder middelpunt is het %-overlap te zien en het daarbijbehordende bereik."""
    middelpuntAfstanden = berekenMiddelpuntAfstanden(punten)
    vor = Voronoi(punten)
    vorPlot(vor)
    ax = plt.gca()

    for i, punt in enumerate(vor.ridge_points):
        totaleOverlap = berekenPercentageOverlap(middelpuntAfstanden[i], mu, sigma)
        middelpunt = vor.points[punt].mean(axis=0)
        graden = berekenHelling(vor.points[punt][0], vor.points[punt][1])
        grens = berekenGrens(0.999, mu, sigma)

        if round(totaleOverlap * 100, 2) > 0.00:
            ax.add_artist(Ellipse((middelpunt[0], middelpunt[1]), sigma * totaleOverlap, grens - middelpuntAfstanden[i],
                                  angle=graden, color="green", fill=False))
            plt.text(middelpunt[0], middelpunt[1], f"{round(totaleOverlap * 100, 2)}%")
            plt.plot([middelpunt[0]], [middelpunt[1]], marker='o', markersize=3, color="green")

    plt.xlabel("X-coördinaten")
    plt.ylabel("Y-coördinaten")
    legenda = [mlines.Line2D([0], [0], marker='o', color='w', label='Punt', markerfacecolor='r', markersize=15),
               mlines.Line2D([0], [0], marker='o', color='w', label='Mid. van 2 punten', markerfacecolor='g',
                             markersize=15)]
    plt.legend(handles=legenda)
    plt.show()


def plotVerloop(matrix, vector, perioden, labels):
    """Plot het verloop van matrix-vector multiplicatie."""
    lijst = []
    for x in range(perioden + 1):
        lijst.append(vector.dot(np.linalg.matrix_power(matrix, x)))
    lijst = np.vstack(lijst)

    for i, tijdstip in enumerate(lijst.T):
        plt.plot(tijdstip, label=f"Punt {labels[i]}")

    plt.xlabel("N-dagen")
    plt.ylabel("Infectiegraad")
    plt.xlim(0, perioden)
    plt.ylim(0, 1)
    plt.legend()
    plt.tight_layout()  # Alles past zo beter op de grafiek
    plt.show()


def straat2Coord(filePath, woonplaats, woonplaatsHeader, adresHeader):
    """Berekend aan de hand van een CSV-bestand de breedte- en hoogtegraad.
       Resultaten worden opgeslagen in een nieuw CSV-bestand `data/geoDataKDV.csv`.
       Als input wordt om een woonplaats gevraagd. Alle punten die aan de waarde 'woonplaats voldoen'
       in de kolom 'woonplaatsHeader' worden geimporteerd.

       De breedte- en lengtegraad van de waardes die zich bevinden in de kolom 'adresHeader' worden opgevraagd.
       Duplicaten worden direct overgeslagen.
    """
    print("Even geduld a.u.b, dit kan even duren...")
    data = pd.read_csv(filePath, sep=";")  # Data uitlezen uit bestand
    subset = data.loc[data[woonplaatsHeader] == woonplaats]  # Selectie maken van de data

    geolocator = Nominatim(user_agent="IPASS Project - Thijs van den Berg 2019")  # Variabele opzetten voor API-calls
    geoLocaties = pd.DataFrame(columns=['latitude', 'longitude'])  # DataFrame

    for adres in subset[adresHeader].drop_duplicates():  # Ieder adres omzetten naar coördinaten
        locatie = geolocator.geocode(f"{adres} {woonplaats}")
        geoLocaties = geoLocaties.append({'latitude': locatie.latitude, 'longitude': locatie.longitude},
                                         ignore_index=True)
        time.sleep(0.5)  # ToManyRequestsError

    bestand = os.path.basename(filePath)
    fileName = os.path.splitext(bestand)[0]
    geoLocaties.to_csv(f"data/geo_{fileName}.csv", index=False)  # Data opslaan tbv de snelheid
    print(geoLocaties.head())


def coord2Coord(filePath, latNaam, longNaam):
    """Haalt uit een CSV-bestand de latitude- en longitudekolom.
       De gebruiker dient de namen van de kolommen waarde latitude en logitude
       zijn opgeslagen op te geven.
       Deze kolommen worden opgeslagen in een nieuw bestand met de prefix `geo_`.
       
       Het bestand kan vervolgens worden gebruikt om Voronoi's of kaarten te maken.
       """

    print("Even geduld a.u.b, dit kan even duren...\n")
    data = pd.read_csv(filePath, sep=";")  # Data uitlezen uit bestand

    geoLocaties = data[[latNaam, longNaam]].rename(columns={latNaam: "latitude", longNaam: "longitude"})

    bestand = os.path.basename(filePath)
    fileName = os.path.splitext(bestand)[0]
    geoLocaties.to_csv(f"data/geo_{fileName}.csv", index=False)  # Data opslaan tbv de snelheid
    print("Klaar!")


def kaartMaken(filePath, terrein=True, cropped=True):
    """Maakt een kaart gebaseerd op de coordinaten in een CSV-bestand.

    terrein=True kan enkele seconden langer duren dan False. Echter krijgt de kaart dan wel een grafische background.
    cropped=False om een kaart van geheel Nederland te krijgen. Dit is handig wanneer de punten niet op één enkele
    woonplaats zijn gebasseerd.
    """
    print("Kaart aan het maken. \nEven geduld a.u.b, dit kan even duren...")
    coordinaten = pd.read_csv(filePath, sep=",")
    coordinaten = coordinaten.loc[(coordinaten['latitude'] < 53.5) & (coordinaten['latitude'] > 50.7) &
                                  (coordinaten['longitude'] < 7.3) & (
                                          coordinaten['longitude'] > 3.3)]  # Filter Nederland
    coordinaten = coordinaten.values[:, :]  # DataFrame omzetten naar NP-array

    shapeFile = 'shapefiles/gadm36_NLD_2.shp'
    kaart = list(shpreader.Reader(shapeFile).geometries())
    ax = plt.axes(projection=ccrs.EuroPP())

    if terrein:
        stamen_terrain = Stamen('terrain-background')
        ax.add_image(stamen_terrain, 12)
        ax.add_geometries(kaart, ccrs.PlateCarree(), edgecolor='black', facecolor='none', alpha=1)
    else:
        ax.add_geometries(kaart, ccrs.PlateCarree(), edgecolor='black', facecolor='orange', alpha=0.2, )

    if cropped:
        ax.set_extent([min(coordinaten[:, 1]), max(coordinaten[:, 1]),
                       min(coordinaten[:, 0]), max(coordinaten[:, 0])])  # Grootte gelijk aan min/max van coordinaten
    else:
        ax.set_extent([3.3, 7.3, 50.7, 53.5])  # Filter Nederland

    for lat, long in coordinaten:  # Stippen tekenen
        ax.plot(long, lat, marker='o', markersize=3, color="green", transform=ccrs.PlateCarree())

    plt.show()
