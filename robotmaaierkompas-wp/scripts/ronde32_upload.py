#!/usr/bin/env python3
"""Ronde 32: pagina 1 (#11 robotmaaier-zonder-draad), bronnenlijst: label "Appwinkel" in plaats van "Handleiding"
bij de bronnen in de App Store en Google Play. Verder niets. De pagina houdt haar status.

Het wachtwoord komt alleen uit de omgevingsvariabele RMK_WP_APP_PASSWORD (nooit in dit bestand).
Gebruik:  python3 scripts/ronde32_upload.py           (proefdraai, schrijft niets)
          python3 scripts/ronde32_upload.py --schrijf
"""
import base64, json, os, re, sys, urllib.request, urllib.error

ROOT = 'https://robotmaaierkompas.nl/wp-json/'
USER = os.environ.get('RMK_WP_USER', 'mandy98@live.nl')
PW = os.environ.get('RMK_WP_APP_PASSWORD')
SCHRIJF = '--schrijf' in sys.argv
if not PW:
    sys.exit('RMK_WP_APP_PASSWORD ontbreekt in de omgeving.')
AUTH = 'Basic ' + base64.b64encode(f'{USER}:{PW}'.encode()).decode()
APP = re.compile(r'(<li><div><a href="https://(?:apps\.apple\.com|play\.google\.com)/[^"]*">[^<]*</a><div class="rmk-sources__meta"><span class="rmk-chip">)Handleiding(</span>)')


def api(path, data=None):
    req = urllib.request.Request(ROOT + path, method='POST' if data is not None else 'GET',
                                 data=json.dumps(data, ensure_ascii=False).encode() if data is not None else None,
                                 headers={'Authorization': AUTH, 'Content-Type': 'application/json', 'Cache-Control': 'no-cache'})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f'{path}: {e.code} {e.read()[:300]!r}')


p = api('wp/v2/pages/11?context=edit')
raw = p['content']['raw']
nieuw, n = APP.subn(r'\1Appwinkel\2', raw)
print(f'#11 {p["slug"]} ({p["status"]}): {n} app-bronnen "Handleiding" -> "Appwinkel"')
over = re.findall(r'<a href="https://(?:apps\.apple\.com|play\.google\.com)/[^"]*">[^<]*</a><div class="rmk-sources__meta"><span class="rmk-chip">(?!Appwinkel)([^<]+)', nieuw)
if over:
    sys.exit(f'Nog app-bronnen met een ander label: {over}. Niets gewijzigd.')
# Controle: alleen het woord in die chips verandert
assert nieuw.replace('Appwinkel', 'Handleiding') == raw.replace('Appwinkel', 'Handleiding')
if not SCHRIJF or n == 0:
    sys.exit(0)
api('wp/v2/pages/11', {'content': nieuw})
q = api('wp/v2/pages/11?context=edit')
print(f'opgeslagen; status {q["status"]}; inhoud zoals bedoeld: {q["content"]["raw"] == nieuw}')
