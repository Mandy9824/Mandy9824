"""Gedeeld door scripts/ronde55_coolblue_teksten.py (aanzetten) en scripts/ronde55_coolblue_terug.py (terugdraaien).

Nieuwe teksten: letterlijk uit tekstwijzigingen-coolblue-affiliate.md, punten 1-8 (Mandy, oktober 2026; dat bestand staat
niet in de repository). Oude teksten ("Was"): zoals ronde 39 ze zette (= de nieuwe teksten in affiliate_teksten_lib.py).
Punt 9 van het md (de knop zelf) staat in het thema (inc/coolblue.php); daar volgt het thema de opdracht van ronde 55
(prijs uit de feed, foto, laagste prijs bovenaan, clickref model + slug), die van punt 9 afwijkt.
Lezen, zoeken en schrijven: affiliate_teksten_lib (zelfde zeven teksten en de instelling rmk_advertentie_tekst).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from affiliate_teksten_lib import A81_NIEUW, A81_SLOT, C83_NIEUW, ADVERTENTIE as ADVERTENTIE_BOL

TEKST = [  # (doel, oud, nieuw): lopende tekst; tags ertussen mogen, een link "affiliate-melding" blijft staan
    (77, 'We verdienen geld met affiliatelinks naar bol.com: koop je via een knop, dan kunnen wij een commissie ontvangen. Zie de affiliate-melding.',
         'We verdienen geld met affiliatelinks naar bol.com en Coolblue: koop je via een knop, dan kunnen wij een commissie ontvangen. Zie de affiliate-melding.'),
    (80, 'We kunnen een commissie ontvangen als je via onze links naar bol.com iets koopt. Zie de affiliate-melding.',
         'We kunnen een commissie ontvangen als je via onze links naar bol.com of Coolblue iets koopt. Zie de affiliate-melding.'),
    (76, 'Koop je via een knop naar bol.com iets, dan kan bol.com ons een commissie betalen. Jij betaalt niets extra. De volgorde in onze lijsten volgt de score, niet de commissie. Zie ook de affiliate-melding.',
         'Koop je via een knop naar bol.com of Coolblue iets, dan kan die winkel ons een commissie betalen. Jij betaalt niets extra. De volgorde in onze lijsten volgt de score, niet de commissie. Zie ook de affiliate-melding.'),
    ('footer', 'Wij kunnen een commissie ontvangen bij aankopen via links naar bol.com. Zie de affiliate-melding.',
               'Wij kunnen een commissie ontvangen bij aankopen via links naar bol.com en Coolblue. Zie de affiliate-melding.'),
    (82, 'Als je op een knop naar bol.com klikt, kan bol.com een cookie plaatsen om te zien dat je via ons kwam. Lees het cookiebeleid van bol.com.',
         'Als je op een knop naar bol.com of Coolblue klikt, kan die winkel (en voor Coolblue het affiliatenetwerk Awin) een cookie plaatsen om te zien dat je via ons kwam. Lees het cookiebeleid van bol.com, Coolblue en Awin.'),
]
A81_CB = ('<p>robotmaaierkompas.nl verdient geld met affiliatelinks. Als je via een knop naar bol.com of Coolblue gaat en daar iets koopt, kunnen wij een commissie ontvangen van die winkel. '
          'Jij betaalt niets extra. Knoppen naar andere winkels en naar fabrikanten zijn gewone links waar we op dit moment niets aan verdienen; verandert dat, dan melden we het hier.</p>')
A81_CB_SLOT = ('<p>Voor Coolblue geldt hetzelfde: bestellingen, betalingen en vragen over een bestelling lopen altijd via Coolblue zelf. '
               'Wij zijn niet Coolblue. Onze links naar Coolblue lopen via het affiliatenetwerk Awin.</p>')
C83_CB = ('<tr><th scope="row">Cookies van Coolblue en Awin na een klik</th><td>Coolblue en Awin zien dat je via ons kwam</td>'
          '<td>Verschilt, zie het cookiebeleid van Coolblue en Awin</td><td>Wordt door Coolblue of Awin geplaatst</td></tr>')
ADVERTENTIE = 'Advertentie: via deze knoppen naar bol.com en Coolblue krijgen wij mogelijk een commissie. Dat verandert de score niet.'

# Stappen per richting: (doel, soort, zoek, vervang). soort 'exact' = letterlijke HTML, 'tekst' = lopende tekst.
AAN = [(81, 'exact', A81_NIEUW, A81_CB), (81, 'exact', A81_SLOT, A81_SLOT + A81_CB_SLOT)] \
    + [(d, 'tekst', o, n) for d, o, n in TEKST] \
    + [(83, 'exact', C83_NIEUW, C83_NIEUW + C83_CB)]
UIT = [(81, 'exact', A81_CB, A81_NIEUW), (81, 'exact', A81_CB_SLOT, '')] \
    + [(d, 'tekst', n, o) for d, o, n in TEKST] \
    + [(83, 'exact', C83_CB, '')]
