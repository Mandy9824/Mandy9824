# robotmaaierkompas.nl — ontwerp naar WordPress

Versie 1.1 · scoremodel v1.0 (concept tot bevriezing)

## Wat zit erin

| Bestand | Doel |
|---|---|
| `tokens.css` | **Het enige tokenbestand.** Kleuren, typografie, ruimte, radius, schaduw, beweging als CSS-variabelen (`--rmk-*`). |
| `rmk.css` | Alle componenten en layout, mobiel eerst. Leest alleen tokens. Statusiconen zitten in de CSS. |
| `rmk.js` | Geen afhankelijkheden. Scoreberekening en label, vergelijkingsfilter, kostencalculator, keuzehulp, cookiebanner. |
| `patterns/*.php` | 17 componentpatronen + 12 paginapatronen (WordPress 6.2+). |
| `patterns-bron/` | De HTML-bronnen van de patronen. |
| `data/modellen.voorbeeld.json` | Opbouw van het modelbestand voor de kostencalculator (alleen placeholders). |
| `robotmaaierkompas-setup.php` | Laadt CSS/JS en instellingen, fonts, patronen, publicatiecontrole en affiliate-rel. |

## Installeren

1. Kopieer de map naar je (child)thema: `wp-content/themes/<thema>/robotmaaierkompas/`.
2. Voeg in `functions.php` toe: `require_once get_stylesheet_directory() . '/robotmaaierkompas/robotmaaierkompas-setup.php';`
3. Zet de fonts als WOFF2 in `robotmaaierkompas/fonts/` (Atkinson Hyperlegible 400/700, Schibsted Grotesk variabel). Niet laden vanaf Google-servers.
4. Maak `data/modellen.json` met `scripts/excel_naar_json.py` uit het modelbestand (alleen velden met bron en datum).
5. Zet `header` en `footer` in je template-parts; plaats `cookiebanner` één keer in de footer-template.

## Scoremodel v1.0 (concept tot bevriezing)

| Onderdeel | Gewicht | Sleutel in de HTML |
|---|---|---|
| Betrouwbaarheid uit reviews | 25% | `betrouwbaarheid` |
| Navigatie en dekking | 20% | `navigatie` |
| Prijs-kwaliteit | 20% | `prijskwaliteit` |
| Hellingen en terrein | 10% | `hellingen` |
| App en bediening | 10% | `app` |
| Veiligheid | 10% | `veiligheid` |
| Geluid | 5% | `geluid` |

- Elk onderdeel heeft een waarde van 0 tot 10. Balkbreedte = waarde × 10%.
- Eindscore 0 tot 100 = som van (gewicht × waarde) ÷ 10.
- Betrouwbaarheid geldt als onbekend bij minder dan 50 gelezen reviews (`data-reviews`).
- **Label wordt berekend, niet ingetypt** (in `rmk.js`):
  - 7 van 7 onderdelen bekend: **Eindscore**.
  - 5 of 6 bekend: **Functiescore** met het label "voorlopig, zonder [namen van de ontbrekende onderdelen]". Rekenregel: gewogen gemiddelde van alleen de bekende onderdelen, omgerekend naar 0 tot 100. *Deze rekenregel heb ik gekozen omdat hij niet in de opdracht stond; pas hem aan als je het anders wilt.*
  - Minder dan 5 bekend: **geen score**.
- Waarden invullen: in het scoreblok per onderdeel `data-value` (getal of leeg); in tabellen en kaarten in `data-scores="betrouwbaarheid=…; navigatie=…; …; reviews=…"`. Leeg = onbekend.
- De score wordt ook server-side berekend (`inc/score.php`, zelfde regels), zodat hij zonder JavaScript in de HTML staat. Weergave met één decimaal (92,7); rangschikken op de onafgeronde waarde. Shortcodes: `[rmk_scoreblok model="M002"]` en `[rmk_scoretabel modellen="M001,M002"]` lezen `data/modellen.json`.

## Statussen

| Status | Klasse | Betekenis |
|---|---|---|
| Gecontroleerd | `rmk-status--ok` | Gelezen in de handleiding of op de officiële pagina van de fabrikant |
| Fabrikantclaim | `rmk-status--maker` | Alleen een datasheet of reclame van de fabrikant |
| Winkelclaim | `rmk-status--shop` | Alleen een winkel noemt het |
| Tegenstrijdig | `rmk-status--conflict` | Bronnen verschillen; beide getoond, gerekend met de minst gunstige waarde |
| Niet gevonden | `rmk-status--missing` | Geen bron gevonden |

## Publicatiecontrole

Berichten en pagina's kunnen niet gepubliceerd of ingepland worden zolang de inhoud `[`, `Alfa`, `Beta` of `gepeild` bevat. Opslaan als concept kan wel. Blokcommentaar en geregistreerde shortcodes tellen niet mee; ingevoegde patronen wel. In de blokeditor zie je een foutmelding; in andere editors wordt de pagina een concept met een melding. Andere berichttypen toevoegen: filter `rmk_checked_post_types`.

Let op: template-onderdelen (header, footer) worden niet gecontroleerd. Zet daar dus geen placeholders in. (Er is geen KvK-nummer; dat is weggehaald.)

## Kostencalculator

- Geen standaardwaarden en geen voorinstelling. Alle velden zijn leeg tot de bezoeker iets invult of een model kiest.
- Velden: aanschaf, installatie, **eenmalige opties** (antidiefstalmodule, antenne of gateway), messen per jaar, accuprijs en levensduur, stroomverbruik en stroomprijs, **verbinding per jaar na de gratis periode** (met de gratis periode in jaren), onderhoud per jaar, aantal jaren.
- Kiest de bezoeker een model uit `data/modellen.json`, dan staat bij elk veld "Bron: … · datum". Velden zonder waarde in het bestand tonen "Niet in het modelbestand"; een zelf aangepast veld toont "Eigen invoer".
- Lege velden tellen niet mee en worden onder de uitkomst genoemd.

## Eigen vuistregel (keuzehulp en filter)

De marges zijn **eigen vuistregels, geen bron**: +30% op de oppervlakte voor een open gazon, +50% bij zones, bomen of smalle doorgangen. De reden: fabrikanten noemen de maximale oppervlakte onder gunstige omstandigheden. Beide plekken leggen dit uit op de pagina. De oude factor 1,25 in het filter is vervallen; filter en keuzehulp gebruiken nu dezelfde regel. Aanpassen: `window.rmkConfig.margin = {open: …, complex: …}` via het filter `rmk_config`.

## Affiliate-links

`rel="sponsored nofollow"` wordt toegevoegd aan links naar alle domeinen in `rmk_affiliate_domains()` (inclusief subdomeinen) en aan het eigen redirectpad `/ga/`. Bestaande rel-waarden blijven staan. In de lijst staan bol.com, Coolblue, Amazon.nl (en amzn.to), Awin (awin1.com, zenaps.com) en Daisycon (ds1.nl). Merkprogramma's voeg je later toe in die functie of via het filter `rmk_affiliate_domains`. Werkt in berichtinhoud, alle blokken (ook header en footer) en tekstwidgets.

## Menu

Beste robotmaaiers · Kopersgids · Vergelijkingen · Hulp en onderhoud · Hoe we beoordelen · Over ons (`/over-ons/`).

## Toegankelijkheid en snelheid

Alle tekst/achtergrond-paren ≥ 4,5:1, focusring, klikdoelen ≥ 44 px, `prefers-reduced-motion`. FAQ en mobiel menu werken zonder JS. Brede tabellen scrollen in een eigen vak.

## Toegevoegd bij de bouw (5 oktober 2026)

| Bestand | Doel |
|---|---|
| `inc/score.php` | Scoremodel v1.0 server-side, gelijk aan `rmk.js` (getest in `tests/score-test.php`). |
| `inc/prijzen-bol.php` | Prijstaak Bol-partner-API (2× per dag, max. 10 verzoeken/s), opslag met tijdstip, "Bron: bol.com", niets ouder dan 24 uur. |
| `inc/affiliate-redirect.php` | `/ga/[winkel]/[model]/` met kliktelling (zonder persoonsgegevens), noindex, 302. |
| `inc/techniek.php` | Meetcode pas na toestemming, schema-afspraken voor Yoast (Article/Person/BreadcrumbList, nooit Product/Review), WebP, noindex-vangnet. |
| `inc/bouw.php` | Gereedschap > Robotmaaierkompas: controles, paginastructuur als concepten, Yoast instellen (ook via `wp rmk …`). |
| `data/paginas.json` | De paginastructuur (hoofdstuk 2–4 en 7). |
| `fonts/` | Atkinson Hyperlegible 400/700 en Schibsted Grotesk variabel (WOFF2, latin, SIL OFL 1.1). |

Links in de patronen volgen nu de URL's uit hoofdstuk 2: `/hoe-we-beoordelen/`, `/over-ons/`, `/robotmaaier-kosten/`, `/robotmaaier-test-vergelijking/` (filtertabel), `/cookies/`, `/affiliate-melding/`, `/colofon/`, `/redactiebeleid/`. "KvK [nummer]" is weggehaald uit footer en juridisch patroon. `rmk.js` toont scores met één decimaal.
