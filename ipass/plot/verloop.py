import matplotlib.pyplot as plt  # Voor de grafieken
import numpy as np  # Om data als arrays op te kunnen slaan en de normale verdeling te kunnen tekenen
from matplotlib import style  # Style van de grafiek aanpassen naar eigen smaak
from numpy.linalg import matrix_power

from ipass import bereken

style.use('seaborn')


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

    plt.rcParams['figure.figsize'] = [8, 8]  # Grotere plots in Jupyter Notebook
    matrix_percentages = bereken.perc_overlap_matrix(punten, mu, sigma)
    matrix_verloop = []

    for periode in range(perioden + 1):
        # Reken voor iedere periode het matrix vector dotproduct uit
        matrix_vec = vector.dot(matrix_power(matrix_percentages, periode))
        matrix_verloop.append(np.where(matrix_vec > 1, 1, matrix_vec))

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
    plt.show()
