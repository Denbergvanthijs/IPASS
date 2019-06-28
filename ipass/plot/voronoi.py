import matplotlib.lines as mlines
import matplotlib.pyplot as plt  # Voor de grafieken
import numpy as np
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
       :param ellipse keuze of de ellipsen zichtbaar zijn in de plot.
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
