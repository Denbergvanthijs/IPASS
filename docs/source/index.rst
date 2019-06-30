IPASS 2018 - 2019 Documentatie
=============================================
Hieronder vindt u de documentatie van het IPASS eindproject.

Repository
-------------
Deze repository bevat alle code, documentatie en de applicatie van het IPASS-project.
Alle code bevind zich in `ipass/`. Dit is de libary.
De code maakt gebruik van en genereerd data in `data/`.
De applicatie waarmee de functionaliteit aan de hand van verschillende
casussen wordt getoont is te vinden in `app.ipynb`.

Documentatie
----------------
De documentatie is te vinden in iedere functie. Tevens zijn er HTML-pagina's
gegenereerd, deze zijn te vinden in `docs/build/html/index.html`
De documentatie kan worden bijgewerkt met `make html`. Tevens kan de documentatie in
EPUB- of LaTeX-vorm worden gegenereerd met `make epub` resp. `make latex`.

Installatie
--------------
De libary is te installeren via Pypi met pip: `pip install IPASS-repo-denbergvanthijs`.
Vervolgens kan de repository worden geimporteerd als `ipass`.
De benodigde libary's zijn te vinden in `requirements.txt` en te installeren met:
`pip install -r requirements.txt `.
Het is aanbevolen om met een Anaconda omgeving te werken zodat de `GEOS` uitbreiding
in C goed wordt geinstalleerd. Deze komt standaard met Anaconda wanneer cartopy wordt geinstalleerd.

Om de code te testen kan het commando `pytest` worden uitgevoerd. Helaas zijn plots niet te testen.

© Thijs van den Berg 2019

1740697


Inhoud:
==========
.. toctree::
   :titlesonly:

   ipass
