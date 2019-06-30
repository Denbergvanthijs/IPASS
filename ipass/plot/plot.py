import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
import matplotlib.lines as mlines
import matplotlib.pyplot as plt  # Voor de grafieken
import numpy as np  # Om data als arrays op te kunnen slaan en de normale verdeling te kunnen tekenen
import pandas as pd
from cartopy.io.img_tiles import Stamen
from matplotlib import style  # Style van de grafiek aanpassen naar eigen smaak
from matplotlib.patches import Ellipse
from scipy.spatial import Voronoi
from scipy.spatial import voronoi_plot_2d as SPvorPlot

from ipass import bereken

style.use('seaborn')


def voronoi(punten: np.ndarray, mu: float, sigma: float, tekst: bool = True, ellipse: bool = True) -> None:
    """Plot een Voronoi-diagram ter grote van de maximale x en y-coördinaten.
       Bij ieder middelpunt is eventueel het %-overlap te zien en het daarbijbehordende bereik.

       :param punten: Numpy array van n bij 2. Iedere row bevat een x en y coördinaat.
       :param mu: gemiddelde van de normale verdelingen
       :param sigma: standaard deviatie van de normale verdelingen
       :param tekst: keuze of de percentages zichtbaar zijn in de plot.
                     Aan te raden om uit te zetten bij veel punten.
       :param ellipse: keuze of de ellipsen zichtbaar zijn in de plot.
                     Aan te raden om uit te zetten bij veel punten

       :returns: Plot met een Voronoi-diagram en stippen op de coordinaten meegegeven in 'punten'
       """
    if not isinstance(punten, np.ndarray) or not isinstance(mu, (float, int)) or not isinstance(sigma, (float, int)) \
            or not isinstance(tekst, bool) or not isinstance(ellipse, bool):
        raise ValueError("Verkeerde waardes meegegeven als argumenten")

    plt.rcParams['figure.figsize'] = [8, 8]  # Grotere plots in Jupyter Notebook

    vor = Voronoi(punten)
    SPvorPlot(vor)
    ax = plt.gca()

    if tekst or ellipse:
        mid_afstanden = bereken.middelpunt_afstanden(punten)
        for i, punt in enumerate(vor.ridge_points):
            perc_overlap = bereken.perc_overlap(mid_afstanden[i], mu, sigma)
            middelpunt = vor.points[punt].mean(axis=0)

            if round(perc_overlap * 100, 2) > 0.00:  # Als er meer dan 0.00% overlap is, teken dan
                if ellipse:
                    graden = bereken.helling(vor.points[punt][0], vor.points[punt][1])
                    grens = bereken.grens(0.999, mu, sigma)
                    ax.add_artist(
                        Ellipse((middelpunt[0], middelpunt[1]), sigma * perc_overlap, grens - mid_afstanden[i],
                                angle=graden, color="red", fill=False))
                if tekst:
                    plt.text(middelpunt[0], middelpunt[1], f"{round(perc_overlap * 100, 2)}%")

    plt.title(f"Aantal punten: {punten.shape[0]}")
    plt.xlabel("X-coördinaten")
    plt.ylabel("Y-coördinaten")

    if ellipse:
        legenda = (mlines.Line2D([0], [0], marker='o', color='w', label='Punt', markerfacecolor='b', markersize=15),
                   mlines.Line2D([0], [0], marker='o', color='w', label='Overlapping', markerfacecolor='r',
                                 markersize=15))
    else:
        legenda = [mlines.Line2D([0], [0], marker='o', color='w', label='Punt', markerfacecolor='b', markersize=15)]

    plt.legend(handles=legenda)
    plt.show()


def verloop(punten: np.ndarray, vector: np.ndarray, perioden: int, mu: float = 0, sigma: float = 1,
            legenda: bool = True) -> None:
    """Plot het verloop van een verspreiding waarbij het begin van de infectie
       in de vector wordt aangegeven. Verspreiding op tijdstip t gaat
       volgende de formule v·M^t.

       :param punten: Numpy array van n bij 2. Iedere row bevat een x en y coördinaat.
       :param vector: Numpy array van n bij 1. Bevat per cell 0 of 1.
                      Iedere cell waar 1 staat, begint de infectie.
       :param perioden:  Het aantal perioden dat het verloop berekend en getoont moet worden.
       :param mu: gemiddelde van de normale verdelingen
       :param sigma: standaard deviatie van de normale verdelingen
       :param legenda: optioneel, toont de legenda.
              Aangeraden om uit te zetten als er heel veel punten dienen te worden geplot

       :returns: Plot met het verloop van de infectiegraad/verspreiding van de punten
    """
    if not isinstance(punten, np.ndarray) or not isinstance(vector, np.ndarray) or not isinstance(perioden, int) \
            or not isinstance(mu, (float, int)) or not isinstance(sigma, (float, int)) or not isinstance(legenda, bool):
        raise ValueError("Verkeerde waardes meegegeven als argumenten")

    if punten.shape[0] != vector.shape[0]:
        raise ValueError("Vector en punten moeten even lang zijn.")

    print("Even geduld a.u.b, dit kan even duren...")

    # plt.rcParams['figure.figsize'] = [8, 8]  # Grotere plots in Jupyter Notebook
    matrix_percentages = bereken.perc_overlap_matrix(punten, mu, sigma)
    matrix_verloop = []

    for periode in range(perioden + 1):
        # Reken voor iedere periode het matrix vector dotproduct uit
        i = 0
        matrix = matrix_percentages.copy()
        while i != periode:
            matrix = bereken.matrix_maal_matrix(matrix, matrix_percentages)
            i += 1
        matrix_verloop.append(vector.dot(matrix))
    matrix_verloop = np.vstack(matrix_verloop)  # Maakt van een lijst met lijsten een numpy array

    for i, periode in enumerate(matrix_verloop.T):
        plt.plot(periode, label=f"Punt {punten[i]}")  # Plot de infectiegraad van ieder punt tijdens iedere periode

    if legenda:
        plt.legend(loc="lower right")

    plt.xlabel("Periodes")
    plt.ylabel("Infectiegraad")
    plt.xlim(0, perioden)
    plt.ylim(0, 1.1)
    plt.title(f"Aantal punten: {punten.shape[0]}")
    plt.tight_layout()  # Alles past zo beter op de grafiek
    plt.savefig('verloop.eps', format='eps', dpi=1000)
    plt.show()


def kaart(file_path: str, terrein: bool = True, sep: str = ",") -> None:
    """Maakt een kaart gebaseerd op de coordinaten in een CSV-bestand.

    :param file_path: Pad naar het te plotten CSV-bestand
    :param terrein: optioneel, zorgt voor een grafische achtergrond van de plot. Kan enkele seconden langer duren.
    :param sep: optioneel, seperator van het CSV-bestand

    :returns: Een kaart met de geplotte punten, al dan niet met een 'terrein-achtergrond'
    """
    if not isinstance(file_path, str) or not isinstance(terrein, bool) or not isinstance(sep, str):
        raise ValueError("Verkeerde waardes meegegeven als argumenten")

    print("Kaart aan het maken. \nEven geduld a.u.b, dit kan even duren...")
    # plt.rcParams['figure.figsize'] = [8, 8]  # Grotere plots in Jupyter Notebook

    coordinaten = pd.read_csv(file_path, sep=sep)
    coordinaten = coordinaten.loc[(coordinaten['latitude'] < 53.5) & (coordinaten['latitude'] > 50.7) &
                                  (coordinaten['longitude'] < 7.3) & (coordinaten['longitude'] > 3.3)]  # Filter NL
    coordinaten = coordinaten.values[:, :]  # DataFrame omzetten naar NP-array

    sf_path = 'data/shapefiles/gadm36_NLD_2.shp'
    sf_data = list(shpreader.Reader(sf_path).geometries())

    ax = plt.axes(projection=ccrs.EuroPP())
    if terrein:
        ax.add_image(Stamen('terrain-background'), 12)
        ax.add_geometries(sf_data, ccrs.PlateCarree(), edgecolor='black', facecolor='none', alpha=1)
    else:
        ax.add_geometries(sf_data, ccrs.PlateCarree(), edgecolor='black', facecolor='orange', alpha=0.2)

    ax.set_extent([min(coordinaten[:, 1]), max(coordinaten[:, 1]),
                   min(coordinaten[:, 0]), max(coordinaten[:, 0])])  # Grootte gelijk aan min/max van coordinaten

    for lat, long in coordinaten:  # Stippen tekenen
        ax.plot(long, lat, marker='o', markersize=3, color="green", transform=ccrs.PlateCarree())

    plt.savefig('kaart.eps', format='eps', dpi=1000)
    plt.show()
