"""Gedeeld door scripts/ronde74_amazon_teksten.py (aanzetten) en scripts/ronde74_amazon_terug.py (terugdraaien).

Teksten: letterlijk uit tekstwijzigingen-amazon-affiliate.md, punten 1-8 (Mandy, 31 oktober 2026; dat bestand staat niet
in de repository). "Was" = de teksten na de Coolblue-ronde (ronde 59, coolblue_teksten_lib.py). Punt 9 (de Amazon-knop op
de kaart) staat in het thema (inc/amazon.php) en wordt hier niet toegepast.
Lezen, zoeken en schrijven: affiliate_teksten_lib (zelfde zes pagina's, de footer en de instelling rmk_advertentie_tekst).
Elke "Was"-tekst moet precies één keer voorkomen; anders schrijft het script niets en meldt het waar.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from coolblue_teksten_lib import C83_CB, ADVERTENTIE as ADVERTENTIE_CB  # noqa: F401 (ADVERTENTIE_CB: terugdraaien)

TEKST = [  # (doel, was, wordt): lopende tekst; tags ertussen mogen
    (81, 'robotmaaierkompas.nl verdient geld met affiliatelinks. Als je via een knop naar bol.com of Coolblue gaat en daar iets koopt, kunnen wij een commissie ontvangen van die winkel.',
         'robotmaaierkompas.nl verdient geld met affiliatelinks. Als je via een knop naar bol.com, Coolblue of Amazon gaat en daar iets koopt, kunnen wij een commissie ontvangen van die winkel.'),
    (77, 'We verdienen geld met affiliatelinks naar bol.com en Coolblue: koop je via een knop, dan kunnen wij een commissie ontvangen.',
         'We verdienen geld met affiliatelinks naar bol.com, Coolblue en Amazon: koop je via een knop, dan kunnen wij een commissie ontvangen.'),
    (80, 'We kunnen een commissie ontvangen als je via onze links naar bol.com of Coolblue iets koopt.',
         'We kunnen een commissie ontvangen als je via onze links naar bol.com, Coolblue of Amazon iets koopt. Als Amazon-partner verdien ik aan kwalificerende aankopen.'),
    (76, 'Koop je via een knop naar bol.com of Coolblue iets, dan kan die winkel ons een commissie betalen.',
         'Koop je via een knop naar bol.com, Coolblue of Amazon iets, dan kan die winkel ons een commissie betalen.'),
    ('footer', 'Wij kunnen een commissie ontvangen bij aankopen via links naar bol.com en Coolblue.',
               'Wij kunnen een commissie ontvangen bij aankopen via links naar bol.com, Coolblue en Amazon. Als Amazon-partner verdien ik aan kwalificerende aankopen.'),
    (82, 'Als je op een knop naar bol.com of Coolblue klikt, kan die winkel (en voor Coolblue het affiliatenetwerk Awin) een cookie plaatsen om te zien dat je via ons kwam. Lees het cookiebeleid van bol.com, Coolblue en Awin.',
         'Als je op een knop naar bol.com, Coolblue of Amazon klikt, kan die winkel (en voor Coolblue het affiliatenetwerk Awin) een cookie plaatsen om te zien dat je via ons kwam. Lees het cookiebeleid van bol.com, Coolblue, Awin en Amazon.'),
]
# Punt 1, tweede deel: alinea aan het einde van #81 (de pagina eindigt op "</p></article>", precies één keer).
A81_AM_SLOT = ('<p>Als Amazon-partner verdien ik aan kwalificerende aankopen. Bij Amazon tonen we geen prijzen of foto\'s: '
               'de prijs, de beschikbaarheid en de verkoper bekijk je op Amazon zelf. Wij zijn niet Amazon: bestellingen, '
               'betalingen en vragen over een bestelling lopen altijd via Amazon zelf.</p>')
# Punt 7: rij onder "Cookies van Coolblue en Awin na een klik".
C83_AM = ('<tr><th scope="row">Cookies van Amazon na een klik</th><td>Amazon ziet dat je via ons kwam</td>'
          '<td>Verschilt, zie het cookiebeleid van Amazon</td><td>Wordt door Amazon geplaatst</td></tr>')
# Punt 8: instelling rmk_advertentie_tekst.
ADVERTENTIE = ('Advertentie: via deze knoppen naar bol.com, Coolblue en Amazon krijgen wij mogelijk een commissie. '
               'Dat verandert de score niet. Als Amazon-partner verdien ik aan kwalificerende aankopen.')

# Stappen per richting: (doel, soort, zoek, vervang). soort 'exact' = letterlijke HTML, 'tekst' = lopende tekst.
AAN = [(d, 'tekst', o, n) for d, o, n in TEKST] \
    + [(81, 'exact', '</p></article>', '</p>' + A81_AM_SLOT + '</article>'),
       (83, 'exact', C83_CB, C83_CB + C83_AM)]
UIT = [(d, 'tekst', n, o) for d, o, n in TEKST] \
    + [(81, 'exact', A81_AM_SLOT, ''), (83, 'exact', C83_AM, '')]
