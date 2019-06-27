import matplotlib.lines as mlines
import matplotlib.pyplot as plt  # Voor de grafieken
from matplotlib.patches import Ellipse
from scipy.spatial import Voronoi
from scipy.spatial import voronoi_plot_2d as SPvorPlot

from ipass import bereken


def voronoi(punten):
    """Plot een Voronoi-diagram ter grote van de maximale x en y-coördinaten."""
    plt.rcParams['figure.figsize'] = [8, 8]  # Grotere plots in Jupyter Notebook
    SPvorPlot(Voronoi(punten))
    plt.xlabel("X-coördinaten")
    plt.ylabel("Y-coördinaten")
    plt.legend(
        handles=[mlines.Line2D([0], [0], marker='o', color='w', label='Punt', markerfacecolor='r', markersize=15)])
    plt.show()


def voronoi_compleet(punten, mu, sigma, tekst=True):
    """Plot een Voronoi-diagram ter grote van de maximale x en y-coördinaten.
       Bij ieder middelpunt is het %-overlap te zien en het daarbijbehordende bereik."""
    plt.rcParams['figure.figsize'] = [8, 8]  # Grotere plots in Jupyter Notebook
    middelpunt_afstanden = bereken.middelpunt_afstanden(punten)
    vor = Voronoi(punten)
    SPvorPlot(vor)
    ax = plt.gca()

    for i, punt in enumerate(vor.ridge_points):
        totaleOverlap = bereken.perc_overlap(middelpunt_afstanden[i], mu, sigma)
        middelpunt = vor.points[punt].mean(axis=0)
        graden = bereken.helling(vor.points[punt][0], vor.points[punt][1])
        grens = bereken.grens(0.999, mu, sigma)

        if round(totaleOverlap * 100, 2) > 0.00:
            ax.add_artist(Ellipse((middelpunt[0], middelpunt[1]), sigma * totaleOverlap, grens - middelpunt_afstanden[i],
                                  angle=graden, color="green", fill=False))
            if tekst:
                plt.text(middelpunt[0], middelpunt[1], f"{round(totaleOverlap * 100, 2)}%")
            plt.plot([middelpunt[0]], [middelpunt[1]], marker='o', markersize=3, color="green")

    plt.xlabel("X-coördinaten")
    plt.ylabel("Y-coördinaten")
    legenda = [mlines.Line2D([0], [0], marker='o', color='w', label='Punt', markerfacecolor='r', markersize=15),
               mlines.Line2D([0], [0], marker='o', color='w', label='Mid. van 2 punten', markerfacecolor='g',
                             markersize=15)]
    plt.legend(handles=legenda)
    plt.show()
