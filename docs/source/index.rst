IPASS 2018 - 2019 Documentatie
=============================================
Hieronder vindt u de documentatie van het IPASS eindproject.

Deze repository bevat alle code, documentatie en de applicatie van het IPASS-project.
Alle code bevind zich in `ipass/`. Dit is de libary.
De code maakt gebruik van en genereerd data in `data/`.
De applicatie waarmee de functionaliteit aan de hand van verschillende
casussen wordt getoont is te vinden in `app.ipynb`.

De documentatie is te vinden in iedere functie. Tevens zijn er HTML-pagina's
gegenereerd, deze zijn te vinden in `docs/build/html/index.html`
De documentatie kan worden bijgewerkt met `make html`. Tevens kan de documentatie in
EPUB- of LaTeX-vorm worden gegenereerd met `make epub` resp. `make latex`.

De benodigde libary's zijn te vinden in `requirements.txt` en te installeren met:
`pip install -r requirements.txt `

Om de code te testen kan het commando `pytest` worden uitgevoerd. Helaas zijn plots niet te testen.

© Thijs van den Berg 2019
1740697


Inhoud:
==========
.. toctree::
   :titlesonly:

   ipass
