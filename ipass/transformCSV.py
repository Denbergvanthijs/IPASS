import os
import time

import pandas as pd
from geopy.geocoders import Nominatim


def straat2coord(filePath, woonplaats, woonplaatsHeader, adresHeader, sep=";"):
    """Berekend aan de hand van een CSV-bestand de breedte- en hoogtegraad.
       Resultaten worden opgeslagen in een nieuw CSV-bestand `data/geoDataKDV.csv`.
       Als input wordt om een woonplaats gevraagd. Alle punten die aan de waarde 'woonplaats voldoen'
       in de kolom 'woonplaatsHeader' worden geimporteerd.

       De breedte- en lengtegraad van de waardes die zich bevinden in de kolom 'adresHeader' worden opgevraagd.
       Duplicaten worden direct overgeslagen.
    """
    print("Even geduld a.u.b, dit kan even duren...")
    data = pd.read_csv(filePath, sep=sep)  # Data uitlezen uit bestand
    subset = data.loc[data[woonplaatsHeader] == woonplaats]  # Selectie maken van de data

    geolocator = Nominatim(user_agent="IPASS Project - Thijs van den Berg 2019")  # Variabele opzetten voor API-calls
    geoLocaties = pd.DataFrame(columns=['latitude', 'longitude'])  # DataFrame

    for adres in subset[adresHeader].drop_duplicates():  # Ieder adres omzetten naar coördinaten
        try:
            locatie = geolocator.geocode(f"{adres} {woonplaats}")
        except GeocoderTimedOut:
            pass

        if locatie is not None:
            geoLocaties = geoLocaties.append({'latitude': locatie.latitude, 'longitude': locatie.longitude},
                                             ignore_index=True)

        time.sleep(0.5)  # ToManyRequestsError

    bestand = os.path.basename(filePath)
    fileName = os.path.splitext(bestand)[0]
    geoLocaties.to_csv(f"data/output/geo_{fileName}.csv", index=False)  # Data opslaan tbv de snelheid
    print(geoLocaties.head())


def coord2coord(filePath, latNaam, longNaam):
    """Haalt uit een CSV-bestand de latitude- en longitudekolom.
       De gebruiker dient de namen van de kolommen waarde latitude en logitude
       zijn opgeslagen op te geven.
       Deze kolommen worden opgeslagen in een nieuw bestand met de prefix `geo_`.

       Het bestand kan vervolgens worden gebruikt om Voronoi's of kaarten te maken.
       """

    print("Even geduld a.u.b, dit kan even duren...")
    data = pd.read_csv(filePath, sep=";")  # Data uitlezen uit bestand

    geoLocaties = data[[latNaam, longNaam]].rename(columns={latNaam: "latitude", longNaam: "longitude"})

    bestand = os.path.basename(filePath)
    fileName = os.path.splitext(bestand)[0]
    geoLocaties.to_csv(f"data/output/geo_{fileName}.csv", index=False)  # Data opslaan tbv de snelheid
    print("Klaar!")
