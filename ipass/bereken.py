import math
import numpy as np  # Om data als arrays op te kunnen slaan en de normale verdeling te kunnen tekenen
from scipy.spatial import Voronoi
from scipy.stats import norm  # Om de lijn van de normale verdeling te tekenen. Getallen zijn zelf berekend.


def perc_overlap(middelpuntAfstand, mu, sigma):
    """Berekend het percentage overlap tussen twee punten.
       Als argument dient de afstand van de twee punten tot het middelpunt te worden gegeven."""
    return norm.cdf(-middelpuntAfstand + mu, loc=mu, scale=sigma) * 2


def perc_overlap_matrix(punten, mu, sigma):
    overlapMatrix = []
    for punt1 in punten:
        for punt2 in punten:
            middelpunt = abs((punt2 - punt1) / 2)
            middelpuntAfstand = np.sqrt(  # Wortel van (A^2 + B^2)
                np.sum(  # A^2 + B^2
                    np.square(  # Macht van A en B
                        middelpunt)))  # (ΔA, ΔB)
            percentage = perc_overlap(middelpuntAfstand, mu, sigma)
            overlapMatrix.append(percentage)

    return np.array(overlapMatrix).reshape(len(punten), len(punten))


def grens(grens, mu, sigma):
    """Berekend het aantal standaard deviaties dat nodig is om op een bepaalde cumulatieve kans te komen.
       Dezelfde functie als invNorm op de Texas Instruments grafische rekenmachines.
       0.00 < grens < 1.00
       Kan gebruikt worden om de hoogte van de Ellipse in Voronoi-diagrammen te bepalen"""
    return norm.ppf(grens, loc=mu, scale=sigma)


def helling(puntX, puntY):
    """Berekend de helling in graden tussen twee punten.
       Kan gebruikt worden om de richting van de Ellipse in Voronoi-diagrammen te bepalen"""
    delta = puntY - puntX

    if delta[0] != 0.0:  # ZeroDivisionError voorkomen
        richtingsCoefficient = delta[1] / delta[0]
        return math.degrees(math.atan(richtingsCoefficient))
    else:
        return -90


def middelpunt_afstand(punten):
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
