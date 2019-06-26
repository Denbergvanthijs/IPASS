import matplotlib.pyplot as plt  # Voor de grafieken
import numpy as np  # Om data als arrays op te kunnen slaan en de normale verdeling te kunnen tekenen
from matplotlib import style  # Style van de grafiek aanpassen naar eigen smaak
from scipy.spatial import Voronoi
from scipy.stats import norm  # Om de lijn van de normale verdeling te tekenen. Getallen zijn zelf berekend.

from ipass import bereken

style.use('ggplot')


def normale_verdeling(mu, sigma, middelpuntAfstand, labels):
    """Plot-code afgeleid van: Thijs van den Berg (Jun. 2019)
       https://github.com/Denbergvanthijs/AC-opdrachten/

       Mu en Sigma zijn vaak 0 resp. 1
       MiddelpuntAfstand is de hemelsbrede afstand naar het middelpunt van twee punten."""
    plt.rcParams['figure.figsize'] = [9, 6]  # Grotere plots in Jupyter Notebook
    totaleOverlap = bereken.perc_overlap(middelpuntAfstand, mu, sigma)
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


def normale_verdeling_compleet(punten):
    """Plot de normale verdelingen van alle mogelijke combinaties van punten.
        Returned de afstand tot het middelpunt van alle combinaties.
        Een zichtbare Voronoi is niet nodig om berekeningen uit te voeren."""
    vor = Voronoi(punten)
    middelpuntAfstanden = bereken.middelpunt_afstand(punten)

    for i, punt in enumerate(middelpuntAfstanden):
        normale_verdeling(0, 1, punt, vor.points[vor.ridge_points[i]])
