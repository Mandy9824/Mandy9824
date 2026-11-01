#!/usr/bin/env python3
"""Ronde 88, stap 1: Husqvarna-pagina (#20, MET DE HAND), FAQ "Welke Husqvarna Automower heeft GPS?": zin vervangen.
Gebruik:  python3 scripts/ronde88_husqvarna_faq.py [--schrijf]"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ronde88_lib import pas_toe
WAS = 'Bij de andere modellen is er geen GPS zonder losse Connect Kit.'
WORDT = 'Ook de uitlopende 410VE NERA heeft GPS-tracking standaard. Bij de andere modellen is er geen GPS zonder losse Connect Kit.'
pas_toe(20, [('<summary>Welke Husqvarna Automower heeft GPS?</summary><div><p>De 430V en 450V NERA hebben GPS-tracking standaard, via de ingebouwde 4G. ' + WAS,
              '<summary>Welke Husqvarna Automower heeft GPS?</summary><div><p>De 430V en 450V NERA hebben GPS-tracking standaard, via de ingebouwde 4G. ' + WORDT,
              'FAQ GPS-zin')], '--schrijf' in sys.argv, 'husqvarna-faq')
