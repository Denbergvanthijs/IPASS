import matplotlib.pyplot as plt  # Voor de grafieken
import numpy as np  # Om data als arrays op te kunnen slaan en de normale verdeling te kunnen tekenen

from ipass import bereken


def verloop(punten, vector, perioden, mu=0, sigma=1, legenda=True):
    """Plot het verloop van matrix-vector multiplicatie."""
    print("Even geduld a.u.b, dit kan even duren...")
    plt.rcParams['figure.figsize'] = [8, 8]  # Grotere plots in Jupyter Notebook
    matrix = bereken.perc_overlap_matrix(punten, mu, sigma)
    lijst = []

    for periode in range(perioden + 1):
        verloopMatrix = vector.dot(np.linalg.matrix_power(matrix, periode))
        verloopMatrix = np.where(verloopMatrix > 1, 1, verloopMatrix)
        lijst.append(verloopMatrix)
    lijst = np.vstack(lijst)

    for i, tijdstip in enumerate(lijst.T):
        plt.plot(tijdstip, label=f"Punt {punten[i]}")

    if legenda:
        plt.legend(loc="lower right")

    plt.xlabel("Periodes")
    plt.ylabel("Infectiegraad")
    plt.xlim(0, perioden)
    plt.ylim(0, 1.1)
    plt.title(f"Aantal punten: {len(punten)}")
    plt.tight_layout()  # Alles past zo beter op de grafiek
    plt.show()
