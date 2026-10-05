#!/usr/bin/env python3
"""
robotmaaierkompas.nl: modeldata (Excel) -> data/modellen.json

Gebruik:
    python3 scripts/excel_naar_json.py pad/naar/robotmaaierkompas_modeldata_v1.xlsx \
        [--uit wp-content/themes/robotmaaierkompas-child/robotmaaierkompas/data/modellen.json]

Leest de bladen Modellen, Bronnen, Prijzen en Reviews en schrijft modellen.json in het
formaat van data/modellen.voorbeeld.json (algemeen + modellen[].kosten), aangevuld met
specs, scores-onderdelen, prijzen en reviews voor de server-side score.

Regels (BLAUWDRUK hoofdstuk 8, 23 t/m 34 en de bouwopdracht):
- Een veld uit Modellen wordt alleen overgenomen als er in Bronnen een regel voor is met
  een bron (URL of omschrijving) en een geldige datum.
- Status "niet gevonden" of "niet geopend": waarde null.
- Status "tegenstrijdig" zonder gekozen waarde: null. Met een gekozen waarde in Modellen
  (bijvoorbeeld "tegenstrijdig, laagste waarde gebruikt"): die waarde, status tegenstrijdig.
- Meerdere bronregels voor hetzelfde veld: gecontroleerd > fabrikantclaim > winkelclaim.
- Modellen die als "niet leverbaar" zijn gemarkeerd worden overgeslagen.
- Er wordt niets geschat of aangevuld. Alles wat ontbreekt blijft null.
- Modellen met beschikbaarheid "uitverkocht" of "niet leverbaar" worden overgeslagen.
- Voorlopig geen Bol-gegevens: bronregels en reviews van bol.com worden overgeslagen.
- Geen winkelprijzen in de uitvoer (modellen.json is openbaar): aanschaf blijft null, geen prijslijst.
  Opmerkingen uit Bronnen gaan ook niet mee (die kunnen prijzen en interne notities bevatten).
"""
import argparse
import datetime as dt
import json
import re
import sys
import unicodedata

try:
    import openpyxl
except ImportError:  # pragma: no cover
    sys.exit("openpyxl ontbreekt: pip install openpyxl")

SCOREMODEL_VERSIE = "v1.0 (concept tot bevriezing)"

# Kolomkop in blad Modellen -> interne sleutel
KOLOMMEN = {
    "ID": "id", "Merk": "merk", "Model": "model", "Generatie of jaar": "generatie",
    "Kandidaat voor pagina": "kandidaat_paginas",
    "Navigatie (draad / GNSS / RTK / vision / RTK+vision / LiDAR)": "navigatie",
    "Zones of passages (ja/nee)": "zones", "Obstakelontwijking (ja/nee)": "obstakelontwijking",
    "Begrenzingsdraad nodig (ja/nee)": "begrenzingsdraad", "Max. tuingrootte (m²)": "max_tuingrootte_m2",
    "Max. helling (%)": "max_helling_pct", "Vierwielaandrijving (ja/nee)": "vierwielaandrijving",
    "Geluid dB(A)": "geluid_dba", "IP-klasse": "ip_klasse", "Maaibreedte (cm)": "maaibreedte_cm",
    "Maaihoogte (mm)": "maaihoogte_mm", "Pincode (1/0)": "pincode", "Alarm (1/0)": "alarm",
    "GPS-tracking (1/0)": "gps_tracking", "Mes-stop bij optillen/kantelen (1/0)": "mes_stop",
    "Obstakel-/personendetectie (1/0)": "obstakeldetectie", "Geofence-melding (1/0)": "geofence",
    "App iOS én Android (1/0)": "app_ios_android", "App kaart, zones, no-go (1/0)": "app_kaart",
    "Schema (1/0)": "app_schema", "Slimme-thuiskoppeling (1/0)": "app_smarthome",
    "Bediening zonder app (1/0)": "bediening_zonder_app", "Updates over de lucht (1/0)": "ota_updates",
    "App-rating (0-5)": "app_rating", "Garantie": "garantie",
    "Extra installatiekosten (euro, eenmalig)": "extra_installatiekosten", "Opmerking": "opmerking",
    "Mes-stop bij optillen/kantelen (1/0) - alleen informatie": "mes_stop",
    "Beschikbaarheid (nieuw / uitlopend / uitverkocht)": "beschikbaarheid",
}
NIET_SPEC = {"id", "merk", "model", "generatie", "kandidaat_paginas", "opmerking", "beschikbaarheid"}
NIET_LEVERBAAR = ("niet leverbaar", "uitverkocht")

# Veldnaam in blad Bronnen (genormaliseerd, kleine letters) -> interne sleutel
BRONVELDEN = {
    "navigatie": "navigatie", "zones": "zones", "zones of passages": "zones",
    "obstakelontwijking": "obstakelontwijking", "begrenzingsdraad nodig": "begrenzingsdraad",
    "max. tuingrootte": "max_tuingrootte_m2", "max tuingrootte": "max_tuingrootte_m2",
    "max. helling": "max_helling_pct", "helling": "max_helling_pct",
    "vierwielaandrijving": "vierwielaandrijving", "aandrijving": "vierwielaandrijving",
    "geluid": "geluid_dba", "ip-klasse": "ip_klasse", "maaibreedte": "maaibreedte_cm",
    "maaihoogte": "maaihoogte_mm", "pincode": "pincode", "alarm": "alarm",
    "gps-tracking": "gps_tracking", "mes-stop bij optillen": "mes_stop", "optilsensor": "mes_stop",
    "mes-stop bij optillen/kantelen": "mes_stop",
    "obstakel-/personendetectie": "obstakeldetectie", "geofence-melding": "geofence",
    "app ios én android": "app_ios_android", "app: kaart, zones, no-go": "app_kaart",
    "app: schema": "app_schema", "app: slimme-thuiskoppeling": "app_smarthome",
    "bediening zonder app": "bediening_zonder_app", "updates over de lucht": "ota_updates",
    "app-rating": "app_rating", "garantie": "garantie",
    "extra installatiekosten": "extra_installatiekosten",
    "zones en passages": "zones", "passages": "zones", "obstakels": "obstakelontwijking", "detectie": "obstakeldetectie",
    "draad": "begrenzingsdraad", "ota": "ota_updates", "geofence": "geofence",
}
# Delen na een veldnaam die met "App" begint, gaan over de app (bijv. "App: kaart, zones, schema")
APP_DELEN = {
    "kaart": "app_kaart", "zones": "app_kaart", "no-go": "app_kaart", "kaart/no-go": "app_kaart",
    "schema": "app_schema", "ota": "ota_updates", "knoppen": "bediening_zonder_app",
    "bediening zonder app": "bediening_zonder_app", "slimme-thuiskoppeling": "app_smarthome",
}
STATUS_RANG = {"gecontroleerd": 3, "fabrikantclaim": 2, "winkelclaim": 1}
STATUS_LEEG = ("niet gevonden", "niet geopend")

# Kostenvelden zoals in modellen.voorbeeld.json
KOSTEN = ["aanschaf", "installatie", "antidiefstal", "antenne_gateway", "messen_per_jaar", "accu_prijs",
          "accu_levensduur_jaren", "stroom_kwh_per_seizoen", "verbinding_per_jaar",
          "gratis_periode_jaren", "onderhoud_per_jaar"]
# Bronnen-veldnamen die direct een kostenveld vullen, alleen als de waarde een los getal is
KOSTEN_BRONVELDEN = {
    "kosten: antidiefstal": "antidiefstal", "antidiefstalmodule": "antidiefstal",
    "kosten: antenne": "antenne_gateway", "antenne of gateway": "antenne_gateway",
    "kosten: messen per jaar": "messen_per_jaar", "accu prijs": "accu_prijs",
    "accu levensduur (jaren)": "accu_levensduur_jaren", "stroomverbruik (kwh per seizoen)": "stroom_kwh_per_seizoen",
    "verbinding per jaar": "verbinding_per_jaar", "gratis periode (jaren)": "gratis_periode_jaren",
    "onderhoud per jaar": "onderhoud_per_jaar",
}


def norm(s):
    return re.sub(r"\s+", " ", str(s or "").strip().lower())


def slugify(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def datum(v):
    """Geeft ISO-datum terug of None als er geen geldige datum is."""
    if isinstance(v, (dt.datetime, dt.date)):
        return v.strftime("%Y-%m-%d")
    t = str(v or "").strip()
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})", t)
    if m:
        try:
            dt.date(int(m[1]), int(m[2]), int(m[3]))
            return m.group(0)
        except ValueError:
            return None
    m = re.match(r"^(\d{1,2})-(\d{1,2})-(\d{4})$", t)
    if m:
        try:
            return dt.date(int(m[3]), int(m[2]), int(m[1])).strftime("%Y-%m-%d")
        except ValueError:
            return None
    return None


def getal(v):
    if v is None or isinstance(v, bool):
        return None
    if isinstance(v, (int, float)):
        return v
    t = str(v).strip().replace("€", "").replace(" ", "")
    if not re.fullmatch(r"-?\d+([.,]\d+)?", t):
        return None
    return float(t.replace(",", "."))


def leeg(v):
    return v is None or (isinstance(v, str) and v.strip() == "")


def blad(wb, naam):
    if naam not in wb.sheetnames:
        sys.exit(f"Blad '{naam}' ontbreekt in het Excel-bestand.")
    ws = wb[naam]
    rijen = list(ws.iter_rows(values_only=True))
    kop = [str(c).strip() if c is not None else "" for c in rijen[0]]
    uit = []
    for r in rijen[1:]:
        if all(leeg(c) for c in r):
            continue
        uit.append({kop[i]: r[i] for i in range(len(kop)) if kop[i]})
    return uit


def kolom(rij, *namen):
    """Waarde uit de eerste kolom waarvan de kop met een van de namen begint."""
    for k, v in rij.items():
        for n in namen:
            if norm(k).startswith(norm(n)):
                return v
    return None


def bron_velden(veld):
    """'Max. tuingrootte, helling, aandrijving' -> sleutels. Toelichting tussen haakjes telt niet mee."""
    v = norm(re.sub(r"\(.*?\)", "", str(veld or "")))
    if v in BRONVELDEN or v in KOSTEN_BRONVELDEN:
        return [BRONVELDEN.get(v) or KOSTEN_BRONVELDEN.get(v)]
    delen = [norm(d) for d in re.split(r",| en | / ", v) if norm(d)]
    uit, app = [], bool(delen) and delen[0].startswith("app")
    for d in delen:
        key = (APP_DELEN.get(d) if app else None) or BRONVELDEN.get(d) or KOSTEN_BRONVELDEN.get(d)
        if key:
            uit.append(key)
    return uit


def niet_leverbaar(*teksten):
    return any(re.search(r"niet\s+leverbaar", str(t or ""), re.I) for t in teksten)


# ---------------------------------------------------------------- scoreonderdelen
# Zelfde regels als blad Instellingen/Scores (v1.0), met de besluiten uit hoofdstuk 26 en 28:
# veiligheid zonder mes-stop (8 punten -> 0..10), app-rating niet afronden.
NAV = {"draad": 3, "gnss": 4, "rtk": 6, "vision": 6, "rtk+vision": 8, "lidar": 8}


def ja(v):
    return norm(v) in ("ja", "1", "true")


def s_navigatie(f):
    nav, zo, ob = f.get("navigatie"), f.get("zones"), f.get("obstakelontwijking")
    if leeg(nav) or leeg(zo) or leeg(ob) or norm(nav) not in NAV:
        return None
    return min(10, NAV[norm(nav)] + (1 if ja(zo) else 0) + (1 if ja(ob) else 0))


def s_hellingen(f):
    h = getal(f.get("max_helling_pct"))
    if h is None:
        return None
    basis = 10 if h >= 50 else 8 if h >= 40 else 6 if h >= 30 else 4 if h >= 20 else 2
    return min(10, basis + (1 if ja(f.get("vierwielaandrijving")) else 0))


def s_geluid(f):
    d = getal(f.get("geluid_dba"))
    if d is None:
        return None
    return 10 if d <= 50 else 8 if d <= 55 else 6 if d <= 60 else 4 if d <= 65 else 2


def s_app(f):
    keys = ["app_ios_android", "app_kaart", "app_schema", "app_smarthome", "bediening_zonder_app", "ota_updates"]
    vals = [getal(f.get(k)) for k in keys]
    r = getal(f.get("app_rating"))
    if any(v is None for v in vals) or r is None:
        return None
    pts = 2 * vals[0] + 2 * vals[1] + vals[2] + vals[3] + vals[4] + vals[5]
    pts += 2 if r >= 4.5 else 1 if r >= 4.0 else 0
    return min(10, pts)


def s_veiligheid(f):
    keys = ["pincode", "alarm", "gps_tracking", "obstakeldetectie", "geofence"]
    vals = [getal(f.get(k)) for k in keys]
    if any(v is None for v in vals):
        return None
    pts = 2 * vals[0] + 2 * vals[1] + 2 * vals[2] + vals[3] + vals[4]
    return round(pts / 8 * 10, 4)


def s_betrouwbaarheid(gelezen, storingen, minimum=50):
    if gelezen is None or gelezen < minimum or storingen is None:
        return None
    a = storingen / gelezen
    return 10 if a <= 0.03 else 8 if a <= 0.06 else 6 if a <= 0.10 else 4 if a <= 0.15 else 2 if a <= 0.25 else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("xlsx")
    ap.add_argument("--uit", default="wp-content/themes/robotmaaierkompas-child/robotmaaierkompas/data/modellen.json")
    args = ap.parse_args()

    wb = openpyxl.load_workbook(args.xlsx, data_only=True)
    modellen, bronnen, prijzen, reviews = (blad(wb, n) for n in ("Modellen", "Bronnen", "Prijzen", "Reviews"))
    minimum = 50
    if "Instellingen" in wb.sheetnames:
        for r in wb["Instellingen"].iter_rows(values_only=True):
            if r and r[0] and str(r[0]).startswith("Minimum aantal gelezen reviews") and getal(r[1]):
                minimum = int(getal(r[1]))

    rapport = {"overgeslagen_niet_leverbaar": [], "velden_zonder_bron": {}, "velden_null_door_status": {},
               "bol_bronnen_overgeslagen": 0, "bol_reviews_overgeslagen": 0, "beschikbaarheid_onbekend": []}
    uit_modellen = []

    for m in modellen:
        rij = {KOLOMMEN.get(k.strip(), None): v for k, v in m.items()}
        rij.pop(None, None)
        mid = str(rij.get("id") or "").strip()
        if not mid:
            continue
        mbron = [b for b in bronnen if str(kolom(b, "Model-ID") or "").strip() == mid]
        mprijs = [p for p in prijzen if str(kolom(p, "Model-ID") or "").strip() == mid]
        mrev = [r for r in reviews if str(kolom(r, "Model-ID") or "").strip() == mid]

        # Alleen de kolom Beschikbaarheid of een bronstatus "niet leverbaar"; vrije tekst in Opmerking telt niet
        # (die kan bijvoorbeeld "niet leverbaar bij de fabrikant, wel bij een winkel" zeggen).
        if norm(rij.get("beschikbaarheid")) in NIET_LEVERBAAR or any(norm(kolom(b, "Status")) in NIET_LEVERBAAR for b in mbron):
            rapport["overgeslagen_niet_leverbaar"].append(mid)
            continue

        # Beste bronregel per veld
        beste = {}
        for b in mbron:
            status = norm(kolom(b, "Status"))
            regel = {"bron": str(kolom(b, "Bron") or "").strip(), "datum": datum(kolom(b, "Datum")),
                     "status": status, "bronwaarde": None if leeg(kolom(b, "Waarde")) else str(kolom(b, "Waarde")),
                     "opmerking": None if leeg(kolom(b, "Opmerking")) else str(kolom(b, "Opmerking"))}
            if "bol.com" in norm(regel["bron"]) or "bol.com" in norm(kolom(b, "Veld")):
                rapport["bol_bronnen_overgeslagen"] += 1  # voorlopig geen Bol-gegevens
                continue
            for key in bron_velden(kolom(b, "Veld")):
                oud = beste.get(key)
                rang = STATUS_RANG.get(status.split(",")[0].strip(), 0)
                if oud is None or rang > STATUS_RANG.get(oud["status"].split(",")[0].strip(), 0):
                    beste[key] = regel

        specs, velden = {}, {}
        zonder, door_status = [], []
        for key, waarde in rij.items():
            if key in NIET_SPEC or leeg(waarde):
                continue
            b = beste.get(key)
            if not b or not b["bron"] or not b["datum"]:
                zonder.append(key)
                continue
            if b["status"].startswith(STATUS_LEEG):
                door_status.append(key)
                continue
            # tegenstrijdig: alleen met gekozen waarde in Modellen (die er hier is, want waarde niet leeg)
            velden[key] = waarde
            specs[key] = {"waarde": waarde, "status": b["status"], "bron": b["bron"], "datum": b["datum"]}
        # Bronregels met status "niet gevonden" of tegenstrijdig zonder waarde: wel tonen, waarde null
        for key, b in beste.items():
            if key in specs or key in KOSTEN:
                continue
            if b["bron"] and b["datum"] and (b["status"].startswith(STATUS_LEEG) or b["status"].startswith("tegenstrijdig")):
                specs[key] = {"waarde": None, "status": b["status"], "bron": b["bron"], "datum": b["datum"]}
                if key not in door_status:
                    door_status.append(key)
        if zonder:
            rapport["velden_zonder_bron"][mid] = sorted(zonder)
        if door_status:
            rapport["velden_null_door_status"][mid] = sorted(door_status)

        # Prijzen: alleen regels met bron en datum. Bol-prijzen niet statisch tonen.
        p_uit = []
        for p in mprijs:
            prijs, d, bron = getal(kolom(p, "Prijs")), datum(kolom(p, "Datum")), str(kolom(p, "Bron") or "").strip()
            if prijs is None or not d or not bron:
                continue
            winkel = str(kolom(p, "Winkel") or "").strip()
            p_uit.append({"winkel": winkel, "prijs": prijs, "datum": d,
                          "op_voorraad": None if leeg(kolom(p, "Op voorraad")) else norm(kolom(p, "Op voorraad")),
                          "affiliate_mogelijk": None if leeg(kolom(p, "Affiliatelink")) else norm(kolom(p, "Affiliatelink")),
                          "bron": bron,
                          "opmerking": None if leeg(kolom(p, "Opmerking")) else str(kolom(p, "Opmerking")),
                          "statisch_tonen": "bol" not in norm(winkel)})
        geldig = [p for p in p_uit if p["statisch_tonen"] and p["op_voorraad"] == "ja"
                  and "marketplace" not in norm(p["opmerking"]) and "partner" not in norm(p["opmerking"])]
        laagste = min(geldig, key=lambda p: p["prijs"]) if geldig else None

        # Reviews: alleen regels met bron en peildatum
        r_uit, gelezen, storingen = [], 0, 0
        for r in mrev:
            bron, d = str(kolom(r, "Bron") or "").strip(), datum(kolom(r, "Peildatum"))
            if not bron or not d:
                continue
            if "bol" in norm(bron):
                rapport["bol_reviews_overgeslagen"] += 1  # voorlopig geen Bol-gegevens
                continue
            if norm(kolom(r, "Niet-onafhankelijk")) == "ja":
                continue  # fabrikant of ander land: telt niet als onafhankelijk
            e = {"bron": bron, "peildatum": d,
                 "aantal_totaal": getal(kolom(r, "Aantal reviews totaal")),
                 "gemiddelde": getal(kolom(r, "Gemiddelde")),
                 "aantal_gelezen": getal(kolom(r, "Aantal gelezen")),
                 "structurele_storingen": getal(kolom(r, "Structurele storingen")),
                 "installatie_of_gebruiksfouten": getal(kolom(r, "Installatie")),
                 "gepoold": None if leeg(kolom(r, "Gepoold")) else norm(kolom(r, "Gepoold")),
                 "opmerking": None if leeg(kolom(r, "Opmerking")) else str(kolom(r, "Opmerking"))}
            r_uit.append(e)
            if e["aantal_gelezen"]:
                gelezen += e["aantal_gelezen"]
                storingen += e["structurele_storingen"] or 0

        f = velden
        scores = {
            "betrouwbaarheid": s_betrouwbaarheid(gelezen, storingen, minimum),
            "navigatie": s_navigatie(f),
            "prijskwaliteit": None,  # mediaanprijs per klasse is nog niet ingevuld (blad Instellingen)
            "hellingen": s_hellingen(f),
            "app": s_app(f),
            "veiligheid": s_veiligheid(f),
            "geluid": s_geluid(f),
        }

        naam = f"{rij.get('merk') or ''} {rij.get('model') or ''}".strip()
        kosten = {k: {"waarde": None, "bron": None, "datum": None} for k in KOSTEN}
        # Geen winkelprijzen in de zichtbare weergave (besluit 5 oktober 2026): aanschaf blijft leeg.
        if "extra_installatiekosten" in specs and getal(specs["extra_installatiekosten"]["waarde"]) is not None:
            s = specs["extra_installatiekosten"]
            kosten["installatie"] = {"waarde": getal(s["waarde"]), "bron": s["bron"], "datum": s["datum"]}
        for key, b in beste.items():
            if key in KOSTEN and key not in ("aanschaf", "installatie") and b["bron"] and b["datum"] \
                    and not b["status"].startswith(STATUS_LEEG) and getal(b["bronwaarde"]) is not None:
                kosten[key] = {"waarde": getal(b["bronwaarde"]), "bron": b["bron"], "datum": b["datum"]}

        if leeg(rij.get("beschikbaarheid")):
            rapport["beschikbaarheid_onbekend"].append(mid)
        uit_modellen.append({
            "id": mid, "slug": slugify(naam), "naam": naam, "merk": rij.get("merk"), "model": rij.get("model"),
            "kosten": kosten,
            "specs": specs,
            "scores": scores,
            "reviews_gelezen": gelezen,
            "beschikbaarheid": None if leeg(rij.get("beschikbaarheid")) else norm(rij.get("beschikbaarheid")),
            "reviews": r_uit,
            "ean": None,  # nog niet in het Excel-bestand; nodig voor de Bol-prijstaak
        })

    data = {
        "_uitleg": "Gegenereerd uit het modelbestand door scripts/excel_naar_json.py. Niet met de hand bewerken: "
                   "pas het Excel-bestand aan en draai het script opnieuw. Waarde null = geen bron, niet gevonden, "
                   "niet geopend of tegenstrijdig zonder gekozen waarde.",
        "gegenereerd": dt.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "bronbestand": args.xlsx.split("/")[-1],
        "scoremodel": SCOREMODEL_VERSIE,
        "algemeen": {"stroomprijs_per_kwh": {"waarde": None, "bron": None, "datum": None}},
        "modellen": uit_modellen,
    }
    with open(args.uit, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print(json.dumps({"geschreven": args.uit, "modellen": len(uit_modellen), **rapport}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
