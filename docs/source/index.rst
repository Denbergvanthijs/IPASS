PlaguePy
=============================================

Deze repository bevat alle code, documentatie en de applicatie van het IPASS-project. Alle code bevind zich in `plaguepy/`. Dit is de library. De code maakt gebruik van en genereerd data in `data/`. De applicatie waarmee de functionaliteit aan de hand van verschillende casussen wordt getoont is te vinden in `app.ipynb`.

Documentatie
----------------
De documentatie is te vinden in iedere functie. Tevens zijn er HTML-pagina's gegenereerd, deze zijn te vinden in `docs/build/html/index.html`. Via ReadTheDocs.io is de laatste versie van de documentatie te zien via https://plaguepy.readthedocs.io/). De documentatie kan worden bijgewerkt met `make html`. Tevens kan de documentatie in EPUB- of LaTeX-vorm worden gegenereerd met `make epub` resp. `make latex`.

Installatie
--------------
De library is te installeren via Pypi met pip: `pip install plaguepy`. Vervolgens kan de repository worden geimporteerd als `plaguepy`.   De benodigde libary's zijn te vinden in `requirements.txt` en te installeren met:

pip install -r requirements.txt

Het is aanbevolen om met een Anaconda omgeving te werken zodat de GEOS, https://trac.osgeo.org/osgeo4w/, uitbreiding in C goed wordt geinstalleerd. Deze komt standaard met Anaconda wanneer cartopy wordt geinstalleerd. Mocht u `cartopy` zelf willen installeren, dan is voor Windows aan te raden om de volgende pre-build binary, https://www.lfd.uci.edu/~gohlke/pythonlibs/#cartopy, te gebruiken.

Om de code te testen kan het commando `pytest` worden uitgevoerd. Helaas zijn plots niet te testen.


> © Thijs van den Berg 2019
> 1740697


Inhoud
------------
.. toctree::
   :titlesonly:

   plaguepy
