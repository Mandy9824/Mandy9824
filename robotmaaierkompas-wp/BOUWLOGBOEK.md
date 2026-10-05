# Bouwlogboek robotmaaierkompas.nl

Bouwronde 1, 5 oktober 2026. Ontwerp v1.1, scoremodel v1.0 (concept tot bevriezing).

## Eerst lezen: wat wel en niet op de echte site is gebeurd

**Op robotmaaierkompas.nl is niets veranderd.** De bouwomgeving kon de site niet bereiken: het netwerkbeleid van de omgeving weigert `robotmaaierkompas.nl` (en ook `bol.com`, `wordpress.org` en de Bol-API-documentatie). Ook het adres van de site stond niet in de opdracht; ik ben uitgegaan van `https://robotmaaierkompas.nl`.

Daarom heb ik alles gebouwd en getest op een **lokale kopie**: WordPress 7.1.2, Twenty Twenty-Five, Yoast SEO 28.6. Het resultaat is een installatiepakket plus een knop in wp-admin die stap 0 controleert en stap 2 en 7 uitvoert. Op de echte site doe je het zelf in ongeveer 20 minuten (zie [Installatie op de live site](#installatie-op-de-live-site)), of je laat de host toe in de omgevingsinstellingen en ik doe het in een volgende sessie.

Er is lokaal en live **niets gepubliceerd** en er zijn **geen artikelen** geschreven. Er staan geen specs, prijzen, reviewcijfers of bronnen in die niet uit het Excel-bestand komen.

Deze repository is **openbaar**. Daarom staan de blauwdruk, het Excel-bestand, wachtwoorden en API-sleutels er niet in (zie `.gitignore`).

---

## Stap 0: veiligheid

| Onderdeel | Lokaal | Live |
|---|---|---|
| Volledige back-up vooraf | Gedaan (database en wp-content, archief buiten de repo) | **Open**: hPanel > Back-ups, of een back-upplugin |
| "Zoekmachines niet laten indexeren" | Aan (`blog_public = 0`) | **Open** |
| Standaardvoorbeeldpagina's weg | "Hallo wereld", "Voorbeeldpagina" en het concept "Privacybeleid" verwijderd | **Open** |
| Lichte blokthema-basis met child theme | Twenty Twenty-Five + child theme `robotmaaierkompas-child` | **Open** (zip uploaden) |
| Toepassingswachtwoord met zo min mogelijk rechten | Aparte gebruiker `rmk-bouw` met rol **Redacteur** en eigen toepassingswachtwoord | **Open**, zie hieronder |
| Permalinks op berichtnaam | `/%postname%/` | **Open** |
| HTTPS controleren | Niet van toepassing (lokaal) | **Open**: kon niet testen. Controle staat in Gereedschap > Robotmaaierkompas |

**Over het toepassingswachtwoord.** Het wachtwoord dat je in de opdracht gaf hoort bij jouw eigen account. Dat account is waarschijnlijk beheerder, dus het heeft niet "zo min mogelijk rechten". Bovendien staat het nu in een chatgesprek. Mijn advies:
1. Trek dat toepassingswachtwoord in (Gebruikers > Profiel > Toepassingswachtwoorden).
2. Maak een aparte gebruiker, bijvoorbeeld `rmk-bouw`, met rol **Redacteur**. Dat is het minimum om pagina's als concept te maken en te bewerken. Geef die gebruiker een eigen toepassingswachtwoord.
3. Thema en plugins installeren kan een redacteur niet. Dat doe je eenmalig zelf als beheerder (stap 1 van de installatie hieronder).
4. Trek ook het wachtwoord van `rmk-bouw` in als de bouw klaar is (BLAUWDRUK hoofdstuk 11).

## Stap 1: ontwerp installeren

- Ontwerp v1.1 staat in `wp-content/themes/robotmaaierkompas-child/robotmaaierkompas/` en wordt geladen vanuit `functions.php` van het child theme (README installatie, punt 1 en 2).
- **Lettertypen** zelf gehost in `robotmaaierkompas/fonts/`: `atkinson-hyperlegible-400.woff2`, `atkinson-hyperlegible-700.woff2`, `schibsted-grotesk-var.woff2` (variabel, gewicht 400 tot 900). Bron: de Fontsource-pakketten op npm (versie 5.3.0), subset latin (dekt het Nederlands). Licentie SIL OFL 1.1, licentiebestanden staan erbij. Er wordt niets van Google-servers geladen (gecontroleerd in de HTML); de lettertypen van Twenty Twenty-Five worden niet geladen.
- Header en footer zitten in de template-onderdelen van het child theme (`parts/header.html`, `parts/footer.html`), de cookiebanner staat één keer in de footer (README punt 5).
- **Patronen in de blokeditor:** alle 29 patronen (17 componenten, 12 pagina's) zijn geregistreerd in de categorieën "Robotmaaierkompas – componenten" en "Robotmaaierkompas – pagina's". Gecontroleerd via de REST-route die de blokeditor gebruikt.
- Paginatemplates `page.html` en `front-page.html` zetten geen extra `<main>` om de inhoud, omdat de paginapatronen dat zelf doen.

## Stap 2: sitestructuur

- **76 conceptpagina's**, structuur in `robotmaaierkompas/data/paginas.json`: homepage (ingesteld als voorpagina), hub, alle 13 kernpagina's, sectiepagina's `/merken/`, `/vergelijken/`, `/kopersgids/`, `/hulp/`, vijf merkpagina's, 39 gidspagina's (clusters A tot D, F en G), 10 hulppagina's (cluster E) en de verplichte pagina's: `/hoe-we-beoordelen/`, `/over-ons/`, `/over-ons/mandy-van-den-broek/`, `/contact/`, `/colofon/`, `/affiliate-melding/`, `/privacy/`, `/cookies/`, `/redactiebeleid/`. De privacypagina is gekoppeld in Instellingen > Privacy.
- Elke pagina heeft het patroon van zijn type (toplijst, vergelijking, kosten, merk, kop-aan-kop, kopersgids, hulp, methode, auteur, juridisch). Placeholders tussen [haken] blijven staan, zodat publiceren geblokkeerd is tot alles is ingevuld. Alle 76 pagina's worden door de publicatiecontrole tegengehouden (gecontroleerd).
- **Menu en footer** volgens het ontwerp, met de URL's uit hoofdstuk 2: Beste robotmaaiers · Kopersgids · Vergelijkingen · Hulp en onderhoud · Hoe we beoordelen · Over ons. Footer: Kiezen, Leren, Over ons (met Contact en Redactiebeleid), en onderaan Privacy, Cookies, Affiliate-melding, Colofon, Cookie-instellingen.
- **"KvK [nummer]" is weg** uit de footer, het juridische patroon (ook de HTML-bron) en de README. Gecontroleerd: geen enkele pagina bevat nog "KvK".
- **Eigenaargegevens** staan als invulvelden in de concepten: `[naam of handelsnaam]`, `[adres of postadres]`, `[e-mailadres]`, `[naam auteur]`, `[initialen]` enzovoort.

Keuzes die ik heb gemaakt (pas aan als je het anders wilt):
- Het ontwerp linkte naar `/methode/`, `/kosten/`, `/cookieverklaring/`, `/disclaimer/` en `/toegankelijkheid/`. Ik heb de URL's uit hoofdstuk 2 aangehouden. `/disclaimer/` is `/affiliate-melding/` geworden; `/toegankelijkheid/` staat niet in de blauwdruk en is uit de footer gehaald.
- "Zelf filteren" en de keuzehulp gaan naar kernpagina 2 `/robotmaaier-test-vergelijking/` (de filtertabel). Het menu-item "Vergelijkingen" gaat naar `/vergelijken/`, de sectie met de X-vs-Y-pagina's.
- Het dropdownmenu onder "Beste robotmaaiers" uit hoofdstuk 2 zit niet in het ontwerp. Ik heb het ontwerp gevolgd, dus geen dropdown.
- Slugs die niet letterlijk in de blauwdruk staan, heb ik afgeleid van de hoofdterm, bijvoorbeeld `/robotmaaier-beste-koop/`, `/robotmaaier-grote-tuin/` en `/robotmaaier-test-consumentenbond/`.
- Niet aangemaakt: "Robotmaaier voor hellingen" (blauwdruk: één pagina met pagina 9 tot volume blijkt), "Robotmaaier voor 500, 1000, 1500 en 2000 m²" (overlapt met 9 en 10, eerst beslissen), cluster H (fase 2, na volumecheck) en "Bosch, Stiga, Honda" (één pagina of drie?).
- "Over ons" is een eigen pagina met de over-ons-tekst uit het ontwerp en het auteursblok. Het methodepatroon bevat ook nog een kopje "Over ons". Dat dubbele stuk moet je bij het invullen weghalen of inkorten.

## Stap 3: data

- Script: `scripts/excel_naar_json.py <pad naar xlsx>` schrijft `robotmaaierkompas/data/modellen.json`.
- Het formaat volgt `modellen.voorbeeld.json` (`algemeen` en `modellen[].slug/naam/kosten`). Er komen extra sleutels bij voor de server-side score: `id`, `specs` (waarde, status, bron, datum), `scores` (zeven onderdelen), `reviews_gelezen`, `prijzen`, `reviews` en `ean`.
- Regels: een veld komt alleen mee als er in blad Bronnen een regel is met een bron en een datum. Bij "niet gevonden" of "niet geopend" blijft de waarde null. Bij "tegenstrijdig" zonder gekozen waarde ook. Bij meerdere bronnen telt gecontroleerd boven fabrikantclaim boven winkelclaim. Modellen met "niet leverbaar" worden overgeslagen.
- Prijzen: een vaste prijs telt alleen mee als hij op voorraad is en niet van bol.com komt. Bol-prijzen mogen alleen via de API (art. 3.7, zie stap 5).
- Scoreonderdelen worden berekend uit alleen de overgenomen velden, met de regels van hoofdstuk 8. Daarbij zijn twee besluiten verwerkt: veiligheid zonder mes-stop (gedeeld door 8, keer 10; hoofdstuk 26) en de app-rating niet afronden (hoofdstuk 28).

**Resultaat met het geleverde bestand:** 14 modellen, geen enkel model gemarkeerd als niet leverbaar.
- Overgeslagen velden zonder bronregel: M001 en M003 (begrenzingsdraad), M004 (navigatie, zones, obstakelontwijking, begrenzingsdraad) en M005 (obstakeldetectie).
- Op null door de status: M002 app iOS/Android ("niet gevonden") en vierwielaandrijving ("tegenstrijdig").
- Scores: M002 heeft vier onderdelen (navigatie 10, hellingen 8, veiligheid 10, geluid 6) en krijgt dus **geen score**. M005 heeft er drie, M001 en M003 elk één. M006 tot en met M014 hebben nog geen data.
- `kosten.aanschaf` is overal null: geen enkele prijsregel is "op voorraad = ja", en de Bol-prijzen gelden niet als vaste prijs.

⚠️ **Vraag 1:** het Excel-bestand lijkt de versie van **4 oktober** te zijn. Alleen M002 is ingevuld, plus een paar velden van M001, M003, M004, M005 en M013. De blauwdruk (hoofdstuk 25 tot 34) beschrijft data van 5 oktober voor M001, M004 tot M006 en M008 tot M011: app-rating 4,51, functiescores, prijzen en "niet leverbaar" voor M009. Die data staat niet in dit bestand. Heb je een nieuwere versie? Dan draai ik het script opnieuw; het script hoeft daarvoor niet te veranderen.

## Stap 4: score server-side

- `inc/score.php` rekent met dezelfde regels als `rmk.js`: zeven onderdelen, betrouwbaarheid pas vanaf 50 gelezen reviews, eindscore alleen bij 7 van 7, functiescore bij 5 of 6 met het label "voorlopig, zonder …", en anders geen score.
- De score staat in de HTML, ook zonder JavaScript. Dat werkt op drie manieren: in de patronen scoreblok en scorecel (bij het renderen), met `[rmk_scoreblok model="M002"]` en met `[rmk_scoretabel modellen="…"]` (gerangschikt).
- Weergave met **één decimaal** (92,7), zowel in PHP als in `rmk.js`. Daarvoor is `rmk.js` aangepast: het rondde eerst af op een geheel getal. Rangschikken gebeurt altijd op de **onafgeronde** waarde (in PHP en in het vergelijkingsfilter).
- Tests (`php tests/score-test.php`), allemaal geslaagd:
  - M002 met de waarden uit de blauwdruk (navigatie 10, hellingen 8, app 10, veiligheid 10, geluid 6): **Functiescore 92,7**, "voorlopig, zonder betrouwbaarheid uit reviews en prijs-kwaliteit".
  - Model met zeven onderdelen (testwaarden, geen echt model): **Eindscore 75,1**.
  - 49 tegenover 50 gelezen reviews, vier onderdelen (geen score), placeholders en rangschikking (80,54 boven 80,5 boven 80,46).
  - PHP en `rmk.js` (in Node) geven in 2.001 gevallen precies dezelfde uitkomst.
  - In een echte paginaweergave zonder JavaScript stond `92,7` met "Functiescore" in de HTML.
- Let op: met het huidige Excel-bestand krijgt M002 géén 92,7, omdat de app-velden daar niet in staan (zie vraag 1). De test gebruikt daarom de waarden uit de blauwdruk.

## Stap 5: prijzen (Bol-partner-API)

- `inc/prijzen-bol.php` haalt de prijzen op. De taak draait **twee keer per dag** via WP-Cron, zodat één mislukte ronde de prijzen nog niet laat verlopen. Er gaan **maximaal 10 verzoeken per seconde** uit (gemeten: minstens 0,1 s tussen verzoeken), en bij een 429-antwoord wacht de taak (Retry-After).
- Per model worden prijs, link, levertekst, verkoper en **tijdstip** opgeslagen. De productbox en de scoretabel tonen een prijs alleen met **"Bron: bol.com · prijs van [datum, tijd]"** en **nooit als hij ouder is dan 24 uur**. Een filter kan die grens niet verruimen. Is er geen prijs, dan staat er "Prijs wordt bijgewerkt" met een knop "Bekijk de prijs bij bol.com".
- Na elke ronde wordt de paginacache (LiteSpeed) geleegd, zodat een gecachte pagina geen verlopen prijs blijft tonen.
- Getest met een nagebootste API: prijs, tijdstip, bron, 404, de grens van 24 uur, de lege toestand en de planning werken. **Niet getest tegen de echte API**: er zijn geen sleutels en `api.bol.com` was niet bereikbaar.
- Nodig voordat het werkt: de API-sleutels in `wp-config.php` en een **EAN per model** (`wp rmk bol-ean M002 <EAN>`). EAN's staan nog niet in het Excel-bestand; ik heb ze niet opgezocht en niet verzonnen.

⚠️ **Voorwaarden art. 3.1, 3.7 en 3.11: niet zelf kunnen lezen.** De voorwaarden (partnerblog.bol.com, affiliate.bol.com) en de API-documentatie (api.bol.com) waren geblokkeerd. Wat ik wel weet, en wat volgens mij niet past bij ons gebruik:

1. **Art. 3.1 (volgens hoofdstuk 24: alleen gebruiken om verkeer naar bol te sturen).** Het ontwerp zet in de productbox een bol-knop met prijs naast knoppen van andere winkels. De scoretabel heeft een kolom "Prijs vanaf", en de kostencalculator kan een prijs als aanschaf gebruiken. Dat is Bol-data naast affiliatelinks naar andere winkels, en dat botst met 3.1. Ik heb het zo gebouwd dat Bol-prijzen alleen in het bol-prijsveld en in "Prijs vanaf" komen, nooit in de calculator of in een vergelijking van winkelprijzen. Maar productboxen met meerdere winkels blijven een vraag voor **Bol-partnersupport** (dat stond al in hoofdstuk 24).
2. **Art. 3.7 (prijs en voorraad actueel; volgens een zoekresultaat staat daar ook wat over lokaal opslaan).** Opgelost met de grens van 24 uur en het legen van de cache. Of Bol "actueel" strenger bedoelt dan 24 uur, kon ik niet nalezen.
3. **Art. 3.11 (opslaan toegestaan).** We slaan alleen prijs, link, levertekst, verkoper en tijdstip op. Geen reviewteksten.
4. **Snelheidslimiet.** De opdracht noemt 10 verzoeken per seconde. Een zoekresultaat over de algemene voorwaarden van de **oude Open API** noemt **maximaal 1.200 verzoeken per uur** (gemiddeld 0,33 per seconde). Er lijkt inmiddels een nieuwe Marketing Catalog API te zijn. Controleer welke API en welke limiet voor jouw account gelden. Met 14 modellen blijven we ruim onder beide grenzen, en de limiet is instelbaar (filter `rmk_bol_max_rps`).
5. **Endpoints niet gecontroleerd.** Ik heb het token-adres (`login.bol.com/token`) en de offer-route (`/marketing/catalog/v1/products/{ean}/offers/best`) uit mijn kennis gehaald, niet uit de documentatie. Controleer ze voordat je de sleutels invult. Ze zijn aan te passen met de filters `rmk_bol_token_url` en `rmk_bol_offer_url`.

Lees de voorwaarden in je Bol-partneraccount na en laat me weten wat er in 3.1, 3.7 en 3.11 staat. Dan pas ik de bouw aan.

## Stap 6: affiliate

- `/ga/[winkel]/[model]/` (`inc/affiliate-redirect.php`): een 302-redirect met **X-Robots-Tag: noindex, nofollow** en no-cache (ook voor LiteSpeed). Het doel moet op een affiliate-domein staan, anders wordt het geweigerd; zo kan het pad niet als open redirect worden misbruikt.
- **Klikregistratie** in de tabel `wp_rmk_clicks`: tijdstip, winkel, model en het pad van de pagina waarop geklikt is. Geen IP-adres, geen user-agent, geen cookie. Bots worden niet geteld. Bekijken met `wp rmk kliks`.
- Doel-URL's instellen met `wp rmk link <winkel> <model-slug> <affiliatelink>`. Er staan nog **geen echte links** in.
- **rel="sponsored nofollow"** komt automatisch op links naar `/ga/` en naar de domeinen in `rmk_affiliate_domains()`. Die lijst bevat nu bol.com, coolblue.nl en coolblue.be, amazon.nl en amzn.to, awin1.com en zenaps.com (Awin), en ds1.nl (Daisycon). Merkprogramma's komen later.
- Getest: redirect, noindex-header, 404 bij een onbekende combinatie, weigeren van een domein dat niet in de lijst staat, kliktelling met paginapad, geen telling voor Googlebot, en rel-attributen op alle domeinen. De testlink en de testklik zijn daarna verwijderd.
- Controleer in je Daisycon-account welk trackingdomein je links echt gebruiken. Daisycon gebruikt meerdere domeinen; ds1.nl is er één van.

## Stap 7: SEO en techniek

- **Gekozen: Yoast SEO.** Reden: het schema van Yoast (Article, WebPage, BreadcrumbList, WebSite, Person) bevat zonder WooCommerce geen Product of Review. Instellen gaat via Gereedschap > Robotmaaierkompas > "Yoast SEO instellen" (of `wp rmk seo`):
  - titels "[titel] - robotmaaierkompas.nl", zonder automatisch sjabloon voor metabeschrijvingen (die schrijf je per pagina);
  - XML-sitemap aan;
  - noindex op tags, datum- en auteursarchieven, bijlagen en zoekresultaten;
  - breadcrumbs aan;
  - pagina's als Article met auteur;
  - reacties uit.
- **Canonicals**: Yoast zet een zelfverwijzende canonical. Zolang de site op noindex staat, laat Yoast de canonical weg; dat is normaal.
- **Schema**: in de lokale paginaweergave stond Article, WebPage, BreadcrumbList, WebSite en Person. Een filter haalt altijd Product, Review, AggregateRating en Offer weg. Pagina's ondersteunen nu "auteur", zodat Article met Person werkt. Voor `alternateName` (Mandy Brook) is er een profielveld `rmk_alternate_name`; `sameAs` vul je in bij de Yoast-profielvelden van je gebruiker.
- **Search Console en analytics pas na toestemming**: de code wordt pas geladen als de bezoeker in de cookiebanner "statistieken" aanvinkt (event `rmk:consent`). De ID's zet je in `wp-config.php` (`RMK_GA4_ID`, `RMK_GSC_VERIFICATIE`). Twee kanttekeningen:
  - Search Console controleert de verificatietag in de HTML. Een tag die pas na toestemming via JavaScript komt, wordt waarschijnlijk niet gevonden. **Gebruik DNS-verificatie** (TXT-record bij Hostinger). Dat vraagt geen code op de site en geen toestemming.
  - Er is nog geen analyticsdienst gekozen. Ik heb Google Analytics 4 voorbereid, omdat dat bij Search Console aansluit. Voor een "privacyvriendelijke" dienst zonder cookies (hoofdstuk 11) is mogelijk geen toestemming nodig. Dat is jouw keuze.
- **WebP**: nieuwe JPEG- en PNG-uploads krijgen WebP-versies (WordPress-kern). De server ondersteunt het lokaal; op Hostinger controleert het statuspaneel dit.
- **Lazy loading**: standaard in WordPress voor afbeeldingen in de inhoud (de eerste grote afbeelding krijgt fetchpriority in plaats van lazy). Het patroon productbox noemt `loading="lazy"` in de instructie voor de productfoto.
- **Caching**: kon ik niet lokaal installeren. Op Hostinger: **LiteSpeed Cache**, met:
  - paginacache aan;
  - browsercache aan;
  - CSS en JS verkleinen (niet combineren, eerst testen);
  - "Do Not Cache URIs": `/ga/`;
  - lazy load voor afbeeldingen aan;
  - WebP via LiteSpeed of de kern.
  De code doet zelf al twee dingen: `/ga/` is uitgesloten van de cache en de cache wordt geleegd na elke prijsronde.
- Verder: emoji-script, generator-tag en wlwmanifest/rsd uit.
- **Core Web Vitals (labmeting, Lighthouse 12, mobiel, lokale server zonder compressie of cache, uitgelogd beeld):**

| Pagina | Prestatie | Toegankelijkheid | Best practices | LCP | CLS | TBT | Grootte |
|---|---|---|---|---|---|---|---|
| Homepage | 98 | 100 | 100 | 2,0 s | 0 | 0 ms | 189 KiB |
| Zonder draad (toplijst) | 98 | 100 | 100 | 2,1 s | 0,028 | 0 ms | 197 KiB |
| Test en vergelijking | 98 | 100 | 100 | 2,0 s | 0,047 | 0 ms | 190 KiB |
| Kosten (calculator) | 96 | 100 | 100 | 2,5 s | 0 | 0 ms | 234 KiB |

  Alles valt binnen de groene grenzen (LCP ≤ 2,5 s, CLS ≤ 0,1). Dit zijn labwaarden. **Veldwaarden** (CrUX, Search Console) komen pas na de lancering. Meet dan opnieuw met PageSpeed Insights op de live site, met de cache aan.
- **www naar non-www** en HTTPS-redirect: regel je bij Hostinger (hPanel), niet in het thema.

## Stap 8: controle

- Publicatiecontrole getest met de blokeditor-route (REST) en met de klassieke route:
  - Een nieuwe pagina met "[" direct publiceren gaf **400 rmk_placeholders**: "Publiceren geblokkeerd: de inhoud bevat nog "[" …".
  - Opslaan als concept: mag wel.
  - Daarna publiceren of inplannen: beide geblokkeerd.
  - Via `wp_insert_post` (WP-CLI): de pagina blijft concept.
  - De echte conceptpagina Colofon publiceren: geblokkeerd.
- Losse controles: een geregistreerde shortcode en JSON-haken in blokcommentaar tellen niet mee; een ingevoegd patroon, "Alfa" en "gepeild" wel.
- Alle 76 conceptpagina's bevatten een markering en zijn dus niet per ongeluk te publiceren. Gepubliceerde pagina's of berichten: **0**.
- Let op (README): header en footer worden niet gecontroleerd. Daar staan nu geen placeholders meer in.

---

## Installatie op de live site

1. **Back-up** maken (hPanel > Websites > Back-ups).
2. Instellingen > Lezen: **"Zoekmachines ontmoedigen"** aanvinken.
3. Berichten > "Hallo wereld!" en Pagina's > "Voorbeeldpagina" en "Privacybeleid" naar de prullenbak, en de prullenbak legen.
4. Instellingen > Permalinks: **Berichtnaam**.
5. Controleer dat Twenty Twenty-Five geïnstalleerd is. Upload `robotmaaierkompas-child.zip` (maken met `scripts/maak-zip.sh`) via Weergave > Thema's > Nieuw thema > Thema uploaden, en activeer het.
6. Plugins: **Yoast SEO** en **LiteSpeed Cache** installeren en activeren. Stel LiteSpeed in zoals in stap 7.
7. Gereedschap > **Robotmaaierkompas**: bekijk de controles, klik op "Paginastructuur als concepten aanmaken" (jij wordt de auteur) en daarna op "Yoast SEO instellen".
8. Instellingen > Privacy: kies de pagina "Privacyverklaring".
9. Zet in `wp-config.php` (via bestandsbeheer, niet in git):
   ```php
   define( 'RMK_BOL_CLIENT_ID', '' );      // uit je Bol-partneraccount
   define( 'RMK_BOL_CLIENT_SECRET', '' );
   // define( 'RMK_GA4_ID', 'G-…' );       // pas als je analytics hebt gekozen
   define( 'DISABLE_WP_CRON', true );     // alleen als je stap 10 doet
   ```
10. hPanel > Geavanceerd > Cronjobs: elke 15 minuten `wp cron event run --due-now --path=<pad naar public_html>` (of `php <pad>/wp-cron.php`). WP-Cron zonder bezoekers draait anders niet.
11. Kijk opnieuw in Gereedschap > Robotmaaierkompas: alles moet groen zijn, behalve de Bol-sleutels als je die nog niet hebt.
12. `data/modellen.json` bijwerken: draai `python3 scripts/excel_naar_json.py <xlsx>` en upload het bestand naar `wp-content/themes/robotmaaierkompas-child/robotmaaierkompas/data/`.

---

## Wat Mandy nog zelf moet invullen of nakijken

**Beslissen of aanleveren**
- [ ] Vraag 1: de nieuwste versie van het Excel-bestand.
- [ ] Bol-voorwaarden art. 3.1, 3.7 en 3.11 nalezen, en de vraag over productboxen met meerdere winkels aan Bol-partnersupport stellen.
- [ ] Bol-API: sleutels in `wp-config.php`, API-versie, limiet en endpoints controleren.
- [ ] EAN per model (bron: verpakking of officiële productpagina).
- [ ] Affiliatelinks per winkel en model (`wp rmk link …`) zodra programma's zijn goedgekeurd. Het juiste Daisycon-trackingdomein.
- [ ] Analytics kiezen (GA4 of een dienst zonder cookies). Search Console via DNS verifiëren.
- [ ] Mediaanprijzen per capaciteitsklasse (blad Instellingen). Zonder die prijzen is prijs-kwaliteit voor geen enkel model te scoren, en is er dus nergens een eindscore.
- [ ] Of er een dropdown onder "Beste robotmaaiers" moet (blauwdruk ja, ontwerp nee).
- [ ] Of de slugs van kernpagina's 4, 5, 9, 10 en 11 goed zijn, en wat er met de pagina's gebeurt die ik niet heb aangemaakt (zie stap 2).
- [ ] Yoast "Organisatie of persoon": nu "organisatie robotmaaierkompas.nl" zonder logo. Een persoon (jij) kan ook. Kies.

**Eigenaargegevens (invulvelden in de concepten)**
- [ ] Colofon: naam of handelsnaam, adres of postadres (eventueel een postadres in plaats van je thuisadres), e-mailadres, en een btw-nummer alleen als je dat hebt.
- [ ] Contact: e-mailadres, en een formulier of niet (zo ja: welke plugin, en noem die in de privacyverklaring).
- [ ] Auteurspagina: naam, echte foto (dezelfde als op je andere sites), bio volgens hoofdstuk 7 (geen "ik heb getest"), links naar je andere sites en LinkedIn. In je gebruikersprofiel: `rmk_alternate_name` = "Mandy Brook" en de sameAs-links in Yoast.
- [ ] Over ons: twee tot drie zinnen. Haal ook het dubbele kopje "Over ons" uit de methodepagina weg.
- [ ] `[e-mailadres]` in het correctieblok van de methodepagina en op Redactiebeleid.

**Juridisch en privacy (laten nakijken; ik ben geen jurist)**
- [ ] Privacyverklaring: verwerkingen, grondslag, bewaartermijnen en rechten (AVG). Neem op wat de site doet: de cookiebanner bewaart de keuze (`rmk_consent`, cookie en localStorage, 1 jaar); de kliktelling slaat geen persoonsgegevens op; analytics en Search Console pas na toestemming; Yoast en LiteSpeed; de host (Hostinger).
- [ ] Cookiebeleid: de tabel invullen (rmk_consent, statistieken, affiliate-cookies van winkels). Controleer of de redirect via `/ga/` (cookies van het netwerk) toestemming vraagt.
- [ ] Affiliate-melding: welke programma's, en uitleg over commissie en de Bol-bron.
- [ ] Redactiebeleid: werkwijze, hoe vaak bijwerken, correcties.
- [ ] Informatieplicht en colofon bij KvK of ACM controleren (zonder KvK-inschrijving: wat is verplicht?).
- [ ] De belofte "volgorde volgt de score, niet de commissie" (methodepagina en footer): klopt technisch (`[rmk_scoretabel]` rangschikt op de score). Laat hem alleen staan als je er ook in de tekst naar handelt (hoofdstuk 32, punt 9).

**Techniek op de live site**
- [ ] De installatiestappen hierboven, en de HTTPS-controle.
- [ ] Na de bouw: het toepassingswachtwoord van `rmk-bouw` intrekken, en het in de chat gedeelde wachtwoord nu al.
- [ ] Bij de lancering: indexering bewust weer aanzetten, PageSpeed Insights draaien en de sitemap indienen in Search Console.

## Wat is gedaan (samengevat)

| Stap | Lokaal gebouwd en getest | Live |
|---|---|---|
| 0 Veiligheid | ✅ | open (niet bereikbaar) |
| 1 Ontwerp, fonts, patronen | ✅ | zip klaar |
| 2 Sitestructuur, menu, footer, KvK weg | ✅ 76 concepten | knop in wp-admin |
| 3 Excel naar JSON | ✅ (met de versie van 4 oktober) | bestand uploaden |
| 4 Score server-side | ✅ alle tests geslaagd | met het thema |
| 5 Bol-prijzen | ✅ met nagebootste API | sleutels, EAN's, voorwaarden open |
| 6 /ga/-redirect | ✅ | links invullen |
| 7 SEO en techniek | ✅ Yoast, schema, consent, WebP, CWV-lab groen | LiteSpeed, DNS-verificatie |
| 8 Publicatiecontrole | ✅ "[" blokkeert publiceren | — |

Gestopt na stap 8.

## Bestanden in deze repository

```
robotmaaierkompas-wp/
├── BOUWLOGBOEK.md                     dit bestand
├── scripts/
│   ├── excel_naar_json.py             stap 3
│   └── maak-zip.sh                    installatiepakket child theme
├── tests/
│   ├── score-test.php (+ score-js.js) stap 4: PHP tegen verwachting en tegen rmk.js
│   └── bol-test.php                   stap 5: prijstaak met nagebootste API (wp eval-file)
└── wp-content/themes/robotmaaierkompas-child/
    ├── style.css, functions.php, theme.json
    ├── parts/ (header, footer + cookiebanner), templates/ (page, front-page, single)
    └── robotmaaierkompas/             ontwerp v1.1 + inc/, fonts/, data/
```

---

## Bouwronde 2 (5 oktober 2026): gestopt bij stap 1

- **Domein niet bereikbaar vanuit de bouwomgeving.** `robotmaaierkompas.nl` bestaat (DNS wijst naar Hostinger), maar de omgeving weigert de verbinding: `403 host_not_allowed` ("Host not in allowlist"). Daardoor heb ik HTTPS niet kunnen controleren, geen back-up gemaakt en niets geïnstalleerd. Op de live site is niets veranderd en niets gepubliceerd.
- **Het nieuwe Excel-bestand is niet aangeleverd.** In de map staat alleen het bestand van 4 oktober, met de bladen Leesmij, Instellingen, Modellen, Bronnen, Prijzen, Reviews en Scores. Daar zit geen blad Overzicht in en het bevat 14 modellen in plaats van 10. Daarom heb ik het script niet opnieuw gedraaid.
- Stap 2 tot en met 6 zijn niet uitgevoerd. Ze hangen af van stap 1 en van het nieuwe bestand.

---

## Bouwronde 3 (5 oktober 2026): live site, eerste stappen

**Besluit: voorlopig geen Bol-gegevens.** De sleutels zijn van een andere site. Daarom:
- **Prijstaak uit.** `rmk_bol_enabled()` is onwaar, tenzij `RMK_BOL_ENABLED` in wp-config.php op true staat. Er gaan geen API-verzoeken uit, er wordt geen taak ingepland en een eerder ingeplande taak wordt weggehaald. EAN's worden niet opgezocht.
- **Productboxen** (beide patronen) en kop-aan-kop tonen alleen de lege toestand "Bekijk de prijs bij de winkel", zonder winkelknop en zonder link. De verwijzingen naar bol.com zijn uit de patronen gehaald, en de prijzenalinea op de methodepagina is een invulveld geworden.
- **Geen affiliatelinks aangemaakt.** De optie `rmk_affiliate_links` is leeg; het statuspaneel controleert dat.
- **Open vraag:** in de opdracht staat "WEL Bol-afbeeldingen". Dat heb ik niet gebouwd. Het staat haaks op "geen Bol-gegevens" en zou de API of een feed nodig hebben. Laat weten wat je bedoelt.

### Stap 1: indexering, Hallo wereld, permalinks
- Bij de start was de site **indexeerbaar** (`max-image-preview:large`, geen noindex) en stond "Hallo wereld" openbaar.
- **"Hallo wereld" verwijderd**, met de voorbeeldreactie erbij. `/hello-world/` geeft nu 404. Er zijn 0 berichten en 0 reacties.
- **Permalinks staan op berichtnaam.** De link was `/hello-world/` en `/wp-json/` werkt.
- **"Zoekmachines niet laten indexeren" staat nu aan.** De homepage geeft `noindex, nofollow` en de sitemaps geven 404. Die instelling is in wp-admin gezet, niet door mij: de standaard-API kan dit niet. Het thema v1.2.0 heeft er nu een route voor, `POST /wp-json/rmk/v1/noindex`, en die kan de indexering alleen aanzetten.
- `robots.txt` noemt nog `wp-sitemap.xml`. Dat is normaal: WordPress zet de blokkade in de meta-tag, niet in robots.txt.

### Stap 2: thema, Yoast, structuur
- **Yoast SEO 28.6 is geïnstalleerd en actief** via de plugin-API.
- De beheerder heet nu **"Mandy van den Broek"** (voor- en achternaam, weergavenaam). De gebruikersnaam en slug blijven `admin`; Yoast zet de auteursarchieven uit.
- **Child theme: nog niet actief.** Twenty Twenty-Five staat nog aan. Mandy uploadt `robotmaaierkompas-child.zip` **versie 1.2.0** zelf. Daarna doe ik via de beheerroutes (alleen voor beheerders):
  - `POST /rmk/v1/noindex` (voor de zekerheid),
  - `POST /rmk/v1/paginas` (76 concepten; daarbij wordt ook de privacypagina gekoppeld),
  - `POST /rmk/v1/seo` (Yoast op **Persoon**, de huidige gebruiker = Mandy van den Broek),
  - `GET /rmk/v1/status`.

  De knoppen in Gereedschap > Robotmaaierkompas doen hetzelfde. Er is bewust geen route om te publiceren of om de indexering uit te zetten.
- Lokaal getest: een redacteur krijgt 403, en noindex, seo (person, gebruiker 1), paginas en status werken.

### Stap 3: data uit het nieuwe Excel-bestand (bladen o.a. Overzicht en Logboek)
- Het script herkent nu de nieuwe kolom **Beschikbaarheid**. Modellen met "uitverkocht" of "niet leverbaar" vallen weg, en alleen die kolom of een bronstatus telt. Vrije tekst in Opmerking telt niet meer: daardoor werd M001 eerst ten onrechte overgeslagen, omdat er "niet leverbaar bij Navimow NL zelf, wel nieuw bij Bol" staat.
- Het script herkent ook samengestelde veldnamen in Bronnen ("Zones / obstakels / draad", "App iOS én Android, kaart/no-go, schema, OTA", toelichting tussen haakjes).
- **Uitvoer:** 13 modellen. **M009 (uitverkocht) staat er niet in.** M001 staat er als "uitlopend" wel in. M006-G is geen eigen rij in Modellen; het is een variant met dezelfde score.
- **Scores:** alle onderdeelscores van alle 13 modellen zijn gelijk aan blad Scores. Volgorde: M002 **92,7**, M010 87,3, M004 80,5, M005 80,5, M008 78,6, M001 75,9, M006 63,2, M011 60,9. M003, M007 en M012 tot en met M014 hebben geen score (nog niet uitgezocht, beschikbaarheid onbekend).
- **Geen prijzen en geen Bol-gegevens in modellen.json** (het bestand is openbaar). Er is geen prijslijst, `aanschaf` is overal null, en 10 Bol-bronregels en 6 Bol-reviewregels zijn overgeslagen. Opmerkingen uit Bronnen gaan niet mee, want die bevatten prijzen en interne notities.
- `tests/score-test.php` controleert dit nu ook: M002 92,7, geen M009, geen niet-leverbare modellen, geen prijzen of bol.com. Alle tests geslaagd.
- Let op: `modellen.json` gaat mee in de zip. Bij een nieuwe Excel-versie: script draaien en de zip opnieuw uploaden (of alleen dat bestand vervangen).

### Stap 4: controle
- Live: **0 berichten, 1 pagina** (het concept "Privacybeleid" van WordPress zelf), **niets gepubliceerd**. De homepage geeft `noindex, nofollow`.
- Geen sleutels, wachtwoorden of toepassingswachtwoorden in de repository (gecontroleerd).

### Nog te doen door Mandy
- [ ] `robotmaaierkompas-child.zip` (v1.2.0) uploaden en activeren. Daarna meld ik dat de bouwstappen gedaan kunnen worden.
- [ ] Bedoeling van "WEL Bol-afbeeldingen" uitleggen.
- [ ] Het concept "Privacybeleid" van WordPress (slug `privacy-policy`) mag weg zodra onze `/privacy/` er staat.
- [ ] Het toepassingswachtwoord van het beheerdersaccount intrekken na de bouw (het staat in de chat).
- [ ] De lijst "Wat Mandy nog zelf moet invullen of nakijken" hierboven (auteurspagina, eigenaargegevens, juridische teksten, DNS-verificatie voor Search Console).

## Bouwronde 3, vervolg: child theme actief, bouwstappen live uitgevoerd

- **Child theme `robotmaaierkompas-child` 1.2.0 is actief.** Mandy heeft het geüpload en geactiveerd. Activeren kan niet via de API.
- `POST /rmk/v1/noindex` geeft `blog_public = 0`. De homepage geeft `noindex, nofollow`.
- **`POST /rmk/v1/paginas`: 76 concepten aangemaakt, zonder fouten.** Auteur is Mandy van den Broek (gebruiker 1). De privacypagina is gekoppeld, en de homepage is de voorpagina (concept, dus `/` geeft 404 tot de lancering).
- **Yoast:** `POST /rmk/v1/seo` gaf ok, en daarna is via Yoast's eigen route `configuration/site_representation` ingesteld: **Persoon = gebruiker 1**. Het schema op de site toont nu de uitgever als **Person "Mandy van den Broek"**.
  - De Yoast-controle in het statuspaneel van 1.2.0 meldt dit ten onrechte als "let op": hij las de waarde met `WPSEO_Options::get`. In **1.2.1** gebruikt hij de helper van Yoast, net als de schema-uitvoer. Upload 1.2.1 wanneer het uitkomt; het is niet dringend.
- Het standaardconcept "Privacybeleid" van WordPress (`privacy-policy`) is verwijderd. Onze `/privacy/` staat er.
- Het concept "Affiliate-melding" is aangepast: het kopje "Prijzen van bol.com" is vervangen door een invulveld over "geen winkelprijzen". Ook het sjabloon in `bouw.php` is aangepast.
- **Bedieningsfout, hersteld:** door een fout in mijn eigen script is één keer een lege conceptpagina (#86) aangemaakt. Die is meteen verwijderd. Hij is nooit gepubliceerd.

### Tests tegen de live omgeving
| Test | Uitkomst |
|---|---|
| Publicatiecontrole: tijdelijk concept met "[" inplannen voor 2030 | **400 rmk_placeholders**; de pagina bleef concept. Daarna verwijderd. (Bewust "inplannen" gebruikt en niet "publiceren": het is dezelfde controle, en bij een fout zou er niets openbaar worden.) |
| Score server-side: `[rmk_scoreblok model="M002"]` in de weergegeven HTML | **`92,7`, "Functiescore", "voorlopig, zonder betrouwbaarheid uit reviews en prijs-kwaliteit"** |
| Prijstaak | Statuspaneel: **uitgeschakeld, niet ingepland**. Geen verzoeken naar bol.com. |
| Affiliatelinks | Statuspaneel: geen links ingesteld. Geen concept bevat bol.com of affiliatelinks. |
| Eindstand | **76 pagina's, alle concept; 0 berichten; niets gepubliceerd.** Geen pagina zonder placeholder, geen "KvK". Indexering geblokkeerd, HTTPS geldig, fonts zelf gehost, Yoast 28.6 actief, WebP mogelijk. |

---

## Besluit 5 oktober 2026: productafbeeldingen

- **Geen Bol-afbeeldingen en geen Google-afbeeldingen. Niets van afbeeldingensites halen.** Tot er een veilige bron is, staan overal de plaatsvervangers uit het ontwerp ("Foto volgt", `rmk-ph`). Daarmee is de open vraag over "WEL Bol-afbeeldingen" uit ronde 3 beantwoord.
- Veilige bronnen voor later:
  1. de persmap of mediapagina van de fabrikant, met de gebruiksvoorwaarden en een bronvermelding;
  2. foto's die de PR-afdeling van de fabrikant aanlevert;
  3. na acceptatie door Bol: Bol-afbeeldingen via de API, met de oorspronkelijke URL.
- Gecontroleerd: het thema en de scripts laden geen externe afbeeldingen. De patronen productbox, productbox-zonder-prijs en kop-aan-kop gebruiken de plaatsvervanger.
- Auteursfoto: Mandy heeft vier versies aangeleverd (400 en 800 px, WebP en JPG). Ze staan **niet in deze openbare repository**. Mandy uploadt ze zelf in Media, met alt-tekst "Mandy van den Broek".

---

## Ronde 4 (5 oktober 2026): teksten, auteursfoto en pagina 12

Bronnen: `teksten-site.md`, `pagina-12-wat-kost-een-robotmaaier.md` en de foto's van Mandy. Alle pagina's zijn **concept** gebleven en er is niets gepubliceerd. De teksten staan woord voor woord zoals aangeleverd. Ik heb alleen links toegevoegd waar de tekst naar een pagina of het e-mailadres verwijst. De bestanden zelf staan niet in deze openbare repository.

### Live gedaan
- **Media:** `mandy-van-den-broek-800.webp` (#89) en `-400.webp` (#90), met alt-tekst "Mandy van den Broek".
- **Auteurspagina** `/over-ons/mandy-van-den-broek/`: foto (400, en 800 voor scherpe schermen), naam, bio (Achtergrond en Werkwijze), drie links (rel="me") en het contactblok. Nog open, want niet in de tekst:
  - `[rol]` (chip onder de naam);
  - "Verantwoordelijk voor" `[taak]`;
  - de kaarten bij "Artikelen van Mandy van den Broek" (er zijn nog geen gepubliceerde artikelen).
- **Over ons:** titel "Over robotmaaierkompas.nl", twee alinea's, met links naar de auteurspagina en naar "Zo verdienen we geld".
- **Contact, Privacyverklaring** ("Laatst bijgewerkt: oktober 2026"), **Cookiebeleid** (tabel), **Affiliate-melding** en **Redactiebeleid** (titel aangepast; het anker `#correcties` zit op "Fouten"): tekst geplaatst. De regel "Versie [versie] · geldig vanaf [datum]" heb ik weggehaald, want daar is geen tekst voor aangeleverd. **Deze vijf pagina's hebben geen invulvelden meer en zijn dus publiceerbaar.** Mandy publiceert ze zelf.
- **Colofon:** tekst geplaatst. De "Opmerking voor Mandy (niet publiceren)" over het adres staat tussen [haken] in een kader, zodat publiceren geblokkeerd blijft tot hij weg is. Er staat geen adres, geen KvK en geen btw.
- **Hoe we beoordelen:** het dubbele kopje "Over ons" is weg; de inhoudsopgave linkt nu naar `/over-ons/`. Het invulveld `[e-mailadres]` in het correctieblok is ingevuld met contact@robotmaaierkompas.nl. Ook het patroon is aangepast. Nog open: zeven keer `[toelichting]` in de scoretabel, en de prijzenalinea.
- **Pagina 12 `/robotmaaier-kosten/`:** titel "Wat kost een robotmaaier? Prijzen en verborgen kosten (2026)", opgebouwd binnen het kostenpatroon:
  - eerlijkheidsblok in de variant zonder reviewaantal;
  - de tekst met twee tabellen;
  - de **kostencalculator** met `data-models="M001,M002,M004,M005,M006,M008,M010,M011"`;
  - de FAQ (drie vragen uit de tekst) en "Wat we nog niet weten";
  - een **bronnenlijst met 18 bronnen** uit blad Bronnen (handleidingen en fabrikantpagina's, met datum), plus het scoremodel.

  Kruimelpad: Home > Kosten, zoals de URL-structuur; het patroon had Kopersgids. Geen productboxen, geen Bol-gegevens, geen affiliatelinks (gecontroleerd in de weergegeven HTML).

### Pagina 12: winkelprijzen in de tekst (besluit nodig)
De opdracht zegt "geen winkelprijzen", maar de tekst bevat ze wel. Ik heb niets weggehaald of herschreven. Elke passage staat tussen haken als `[Winkelprijs, niet tonen zonder besluit: …]`, en dat blokkeert publiceren:
1. "Het korte antwoord": de prijsrange 700 tot 3.050 euro ("van een winkel of de fabrikant").
2. "Wat betaal je voor de maaier zelf?": de prijsranges per model.
3. Messentabel, Navimow i206 AWD: "24,99 euro voor 12". Die prijs komt van **Coolblue** (winkelclaim); de andere messenprijzen komen van de fabrikant.
4. Rekenvoorbeeld: "aanschaf rond 730 euro (Coolblue, …)" en het totaal dat daarop rust.
5. FAQ: "(rond 730 euro)" en "(rond 1.100 euro)".

### Pagina 12: gecontroleerd tegen het Excel-bestand
- **Klopt met fabrikantbronnen:** Access+ 99,99 euro met 1 jaar data en daarna 29,90 euro per jaar (M001); link-module 249 euro (M004, M005); reserve-accu 79 euro (M004); Dreame-module 69 of 99,99 euro; messen van Mova 14,99, Dreame 19,99, Eufy 39,99 en Husqvarna 26,99; referentiestation 309 euro (adviesprijs); Gardena zonder abonnement; Eufy VS 19,99 dollar.
- **Let op:**
  - De tekst noemt bij wifi "Dreame A1 Pro en **Ecovacs-modellen**". Ecovacs (M009) is uitverkocht en zit niet in de selectie van acht.
  - "3 jaar gratis service volgens Mova NL" klopt met Mova NL. In het Excel-bestand staat de gratis periode als tegenstrijdig (Mova US zegt 1 jaar).
  - "Messen voor 160 tot 215 euro over vijf jaar" en "Per jaar (eigen berekening)" zijn eigen berekeningen uit de tekst; die heb ik niet nagerekend.

### Kostencalculator (modellen.json)
- Nieuw: `scripts/kosten_toewijzing.json` legt vast welk kostenveld uit welke bronregel komt. Alleen fabrikant- of handleidingregels tellen, dus geen winkelclaim, niet geopend of tegenstrijdig. Het bedrag komt met een vaste regex uit de kolom Waarde.
- Ingevuld:
  - installatie 0 (alle acht, handleiding);
  - M001: antidiefstal 99,99, verbinding 29,90 per jaar, gratis periode 1 jaar;
  - M004 en M005: antidiefstal 249 en accu 79;
  - M011: verbinding 0 ("geen abonnement").
- **Leeg gelaten, en waarom:**
  - aanschaf: geen winkelprijzen;
  - messen per jaar: alleen een eigen bandbreedte, geen bedrag uit een bron;
  - M002: 4G-verlenging niet gevonden, en de messenprijs komt alleen van een winkel;
  - M006: abonnementsprijs EU niet gevonden;
  - M008: twee module-opties, keuze nodig;
  - M010: referentiestation alleen zonder dekking, en de 4G-kosten zijn niet bevestigd;
  - M011: gateway (fabrikant spreekt zichzelf tegen);
  - accu-levensduur, stroom en onderhoud: overal niet gevonden.
- Op de live site staat nog `modellen.json` uit thema 1.2.0, zonder deze kostenvelden. Die van 1.2.2 heeft ze wel.

### Thema 1.2.2 (in de repository; Mandy moet het nog uploaden)
- `rmk.js`: de calculator toont alleen de modellen uit `data-models`. In 1.2.0 staan alle 13 in de keuzelijst.
- Auteursblok: foto uit Media (`mandy-van-den-broek-400`), naam "Mandy van den Broek" en de profiellink zijn ingevuld. Nog open: `[rol]`, `[Eén of twee zinnen …]` en "Laatst nagekeken op [datum]". Daardoor blijven alle pagina's met een auteursblok geblokkeerd.
- Person-schema:
  - Profielvelden `rmk_alternate_name` en `rmk_same_as`, via de API te zetten.
  - `alternateName` en `sameAs` komen daaruit in het Yoast-schema. Lokaal getest: Person met alternateName "Mandy Brook" en de drie links.
  - Yoast voegt zelf het websiteveld van de gebruiker toe aan sameAs.
- `_yoast_wpseo_metadesc` is via de API te zetten, voor de metabeschrijving van pagina 12.
- Het methodepatroon heeft geen dubbel "Over ons" meer.

### Na het uploaden van 1.2.2 (nog niet gedaan)
- Profiel van gebruiker 1: `rmk_alternate_name` = "Mandy Brook" en `rmk_same_as` = de drie links.
- Metabeschrijving van pagina 12 uit het md-bestand.
- Controle dat de calculator alleen de acht modellen toont, met bron en datum bij de ingevulde kosten.

---

## Ronde 5 (5 oktober 2026): profiel, besluiten pagina 12, methode, pagina 1, dataroute

Alles is **concept** gebleven: 76 pagina's in concept, 0 berichten, niets gepubliceerd, en de homepage geeft `noindex, nofollow`. Er zijn geen prijzen, geen Bol-gegevens en geen affiliatelinks geplaatst.

### Live gedaan (met thema 1.2.2)
- **Profiel van gebruiker 1:** `rmk_alternate_name` = "Mandy Brook" en `rmk_same_as` = keukenapparaatgids.nl, compareaitools.org en de LinkedIn-link. In het schema van de site staat nu Person "Mandy van den Broek", met alternateName "Mandy Brook" en sameAs met die drie links. Yoast voegt zelf ook het siteadres toe.
- **Schemafoto** via Yoast op `mandy-van-den-broek-800.webp`. Dat was een Gravatar.
- **Metabeschrijvingen** van pagina 12, pagina 1 en de methodepagina staan uit de md-bestanden in Yoast; gecontroleerd via `yoast_head_json`.
- **Calculator (thema 1.2.2):** het filter op de acht modellen werkt, en `modellen.json` heeft de kostenvelden van ronde 4. De messen en de Dreame-module uit ronde 5 komen er pas in met 1.2.3 of via de dataroute.
- **Auteursblok (1.2.2):** foto, naam en profiellink staan erin. Rol, bio en datum volgen met 1.2.3.
- **Pagina 12:** de besluiten zijn verwerkt.
  - Alle haken zijn weg.
  - Navimow-messen: "ongeveer 25 euro voor 12 stuks".
  - Rekenvoorbeeld: "aanschaf rond 730 euro (laagste nieuwe prijs op 5 oktober 2026)".
  - "Ecovacs-modellen" is weg; er staat nu "Dreame A1 Pro: een 2,4 GHz wifi-signaal wordt aanbevolen voor de app."
  - Er staat geen winkelnaam meer in de tekst. Afgeronde bedragen met "ongeveer" of "rond" zijn blijven staan.
  - De pagina heeft **geen invulvelden meer en is dus publiceerbaar**.
- **Colofon:** alleen de vier zinnen uit de opdracht. De opmerking voor Mandy is weg. Publiceerbaar.
- **Auteurspagina:** rol "Oprichter en redacteur" en verantwoordelijk voor "Onderzoek, scoremodel en redactie". De vaste artikelkaarten zijn vervangen door `[rmk_artikelen_auteur]`, een automatische lijst van gepubliceerde pagina's van deze auteur, zonder verplichte pagina's, sectiepagina's en homepage. Zonder gepubliceerde artikelen toont die niets, ook geen kop. **Werkt pas met 1.2.3**; tot dan staat de shortcode als tekst in het concept en blijft publiceren geblokkeerd.
- **Hoe we beoordelen:**
  - opnieuw opgebouwd met de tekst uit het md-bestand, binnen het methodepatroon;
  - titel "Hoe we beoordelen: scoremodel, bronnen en statussen";
  - in het kort, wel/niet, scoretabel met de kolom **"Gebaseerd op"** (de zeven omschrijvingen uit punt 5), geluid en helling;
  - eindscore of functiescore, statusbadges met de definities uit de tekst, reviews, keuzehulp en marges, prijzen, verdienmodel;
  - **Versies** met alleen de twee regels uit de tekst, en het correctieblok.

  Er zijn geen invulvelden meer in de pagina zelf. Hij blijft geblokkeerd door het auteursblok tot 1.2.3.
- **Pagina 1 `/robotmaaier-zonder-draad/`:** gebouwd met het toplijstpatroon.
  - Titel uit het md-bestand, "Door Mandy van den Broek · bijgewerkt op 5 oktober 2026", en het eerlijkheidsblok in de variant zonder reviewaantal.
  - Tabel "Welke past bij jouw tuin?" en de keuzehulp.
  - **Scoretabel** `[rmk_scoretabel]` met de acht modellen, op volgorde van de onafgeronde score: M002 92,7, M010 87,3, M005 80,5, M004 80,5, M008 78,6, M001 75,9, M006 63,2, M011 60,9. Elke rij toont "Functiescore" met "voorlopig, zonder betrouwbaarheid uit reviews en prijs-kwaliteit". De lege kolom "Beste voor" verdwijnt met 1.2.3.
  - Acht **productboxen (zonder prijs):** naam, score uit modellen.json, de plaatsvervanger "Foto volgt" en "Bekijk de prijs bij de winkel". Geen knop, geen prijs, geen winkel.
  - Bij elk model staan de teksten uit het md-bestand onder de box.
  - FAQ (drie vragen), "Wat we nog niet weten", **bronnenlijst met 49 bron-URL's** uit blad Bronnen (fabrikanten en handleidingen; winkels, Bol, "niet gevonden/geopend" en winkelclaims weggelaten), en het auteursblok.
  - Weggelaten, omdat er geen tekst voor was: "Snel kiezen", de standaardinleiding en "Zo hebben we vergeleken" uit het patroon, en in de productboxen "beste voor", de reviewregel en plus- en minpunten (die staan als tekst onder de box).
- **Scoreblokken in de productboxen:** in 1.2.2 staat in de HTML nog "–", en de browser rekent de score uit `data-scores`. Met 1.2.3 staat de score al in de HTML (`data-model`).
- **Links:** `/robotmaaier-kosten/`, `/robotmaaier-test-vergelijking/` en `/hoe-we-beoordelen/` bestaan als concept. Voor `/robotmaaier-zonder-grensdraad/` is de slug van kernpagina 11 aangepast (was `robotmaaier-zonder-begrenzingsdraad`), ook in `paginas.json`. Alle vier zijn concept, dus voor bezoekers geven ze 404 tot ze zijn gepubliceerd.
- **Publiceerbaar** (geen invulveld meer): affiliate-melding, colofon, contact, cookies, privacy, redactiebeleid en robotmaaier-kosten.

### Data
- Besluiten in `scripts/kosten_toewijzing.json` ("besluiten"):
  - messen per jaar: M004 en M005 28 euro, M008 38 euro, M006 40 euro, als "eigen berekening uit de opgave van de fabrikant", met de datum en de URL (`bron_url`) van de messenregel;
  - M008 antidiefstal 99,99 euro, met als toelichting "met 3 jaar service; ook verkrijgbaar voor 69 euro met 1 jaar service";
  - Mova accu 79 euro, levensduur leeg;
  - aanschaf leeg.
- De calculator toont de toelichting achter de bron (1.2.3).

### Thema 1.2.3 (gebouwd en lokaal getest; Mandy moet het nog uploaden)
- **Dataroute** `POST /wp-json/rmk/v1/modellen` en `GET` (alleen beheerders). Het bestand wordt gecontroleerd en geweigerd bij: geen lijst, ontbrekend id/slug/naam, een prijslijst, een ingevulde aanschaf, bol.com of meer dan 2 MB. Daarna wordt het opgeslagen in de database (`rmk_modellen`) en in `wp-content/uploads/rmk/modellen.json`, en wordt de cache geleegd. De calculator en de scores gebruiken dan die versie; zonder opgeslagen versie gebruikt de site het bestand uit het thema. Het statuspaneel toont de bron.
  - Script: `RMK_WP_APP_PASSWORD=… python3 scripts/excel_naar_json.py <xlsx> --upload https://robotmaaierkompas.nl --gebruiker <naam>`. Het wachtwoord gaat alleen via een omgevingsvariabele, nooit als argument of in de repository.
  - Lokaal getest: een redacteur krijgt 403, en "geen modellen", "bol.com" en "aanschaf" worden geweigerd met 400. Uploaden lukt: 13 modellen, het uploadbestand bestaat en `modelsUrl` wijst ernaar.
- **Auteursblok:** rol "Oprichter en redacteur", de bio uit de opdracht, en "Laatst nagekeken op" met de datum van de laatste wijziging van de pagina (gevuld bij het renderen). Geen invulvelden meer.
- `[rmk_artikelen_auteur]`; scorecel met `data-model` (server-side score); de kolom "Beste voor" in de scoretabel verdwijnt als die leeg is; de toelichting staat in de calculator.

### Na het uploaden van 1.2.3 (nog niet gedaan)
1. `excel_naar_json.py … --upload` draaien, zodat de messen en de Dreame-module live staan.
2. Controleren: auteursblok (rol, bio, datum), artikellijst (leeg zolang er niets gepubliceerd is), productboxscores in de HTML, scoretabel zonder lege kolom, en de toelichting in de calculator.
3. Daarna zijn ook Over ons, Hoe we beoordelen en pagina 1 vrij van invulvelden. Die blijven concept tot Mandy ze publiceert.

---

## Ronde 6 (5 oktober 2026): data live, homepage, pagina 2 en 11, lanceervoorbereiding

Alles is **concept** gebleven: 76 pagina's, 0 berichten, niets gepubliceerd. "Zoekmachines niet laten indexeren" staat aan. De voorpagina-instelling is niet gewijzigd (pagina 9).

### 1. Modelbestand via de dataroute (thema 1.2.3)
- `excel_naar_json.py … --upload`, met het wachtwoord alleen via `RMK_WP_APP_PASSWORD`, staat nu in de database en in `uploads/rmk/`. Het statuspaneel zegt "via de API opgeslagen", en `modelsUrl` op de site wijst naar `uploads/rmk/modellen.json`.
- **Calculator, getest in Chromium** met de live `rmk.js` en het live modelbestand:
  - de keuzelijst toont precies de acht modellen;
  - Dreame: Link-module 99,99 euro met als toelichting "met 3 jaar service; ook verkrijgbaar voor 69 euro met 1 jaar service", messen 38 euro als "eigen berekening uit de opgave van de fabrikant";
  - Mova 800 en 1200: messen 28 euro, accu 79 euro, levensduur leeg;
  - Eufy: messen 40 euro;
  - aanschaf overal leeg. Daardoor toont de calculator pas een uitkomst als de bezoeker zelf een aanschafprijs invult; zo is hij ontworpen.
- **Auteursblok** op pagina 1, de methodepagina en Over ons: foto, rol "Oprichter en redacteur", de bio, en "Laatst nagekeken op 5 oktober 2026" (de datum van de laatste wijziging).
- **Artikellijst** op de auteurspagina: de shortcode werkt. Hij toont nu niets, ook geen kop, omdat er nog niets gepubliceerd is.
- **Productboxen:** de score staat in de HTML (16 scorecellen op pagina 1, allemaal "functie", 92,7 tot 60,9). De lege kolom "Beste voor" is weg.
- Nieuw in de data: `scripts/verbinding_toewijzing.json`, met per model een korte omschrijving van verbinding en diefstalbeveiliging, de bronregel en een filtercategorie (`geen`, `module`, `ingebouwd`), zonder bedragen. Alleen M011 krijgt "geen", want alleen daar bevestigt de fabrikant "geen abonnement". Bij M010 zijn de 4G-kosten op termijn niet bevestigd, dus "ingebouwd".

### 2. Homepage en pagina 2 (en pagina 11)
- **Homepage (#9):** titel uit het md-bestand. De hero heeft H1 en introtekst, zonder de knoppen en het label "Onafhankelijk vergeleken" uit het patroon (geen tekst in het bestand); de illustratie (geen productfoto) staat erin. Verder:
  - kaarten "Waar wil je mee beginnen?" naar pagina 1, 12, 2 en de methodepagina;
  - de keuzehulp;
  - "Wat we anders doen" en "Wie zit erachter?" (met een link naar Over ons);
  - het auteursblok en de affiliate-melding.

  Weggelaten, omdat er geen tekst voor was: de standaard keuzehulp-inleiding, "Kies per situatie", "Hoe we beoordelen" (stappen) en "Onlangs bijgewerkt".
- **Pagina 2 (#12):** de filterbare **vergelijkingstabel** voor de acht modellen, uit modellen.json:
  - kolommen Functiescore, Navigatie, Oppervlak, Helling, Geluid en Verbinding, elk met een statusbadge;
  - per model "Bijgewerkt op …" en een link naar zijn productbox op pagina 1.
  - Filters: navigatie (RTK of GPS, Camera, LiDAR), oppervlak met marge, helling, en **"Zonder losse module of abonnement"**. Dat laatste filter werkt pas met 1.2.4 (lokaal getest: alleen Gardena blijft over).
  - Weggehaald: het budgetveld, sorteren op prijs, "Alleen met eindscore", de kolommen "Doorgang" en "Prijs vanaf", en de prijszin in het bijschrift.
  - Verder: de tekst, "Wat de kolommen betekenen", de keuzehulp, drie FAQ-vragen, een bronnenlijst met 22 fabrikant- en handleidingbronnen, en de link "de pagina over onafhankelijke tests" naar `/robotmaaier-test-consumentenbond/` (kernpagina 4, concept).
  - Getest in Chromium: navigatie- en oppervlaktefilter werken (900 m² geeft Husqvarna, Mova 1200 en Dreame), net als de keuzehulp.
  - **Eigen fout, hersteld:** mijn eerste versie van de tabel haalde bij het verwijderen van het budgetveld ook het einde van het filterformulier en de sorteerkeuze weg. Daardoor werkte de keuzehulp niet (JavaScript-fout). Opnieuw opgebouwd met een exacte vervanging, en daarna voor alle 14 gebouwde pagina's gecontroleerd dat de HTML goed sluit.
- **Pagina 11 (#17) `/robotmaaier-zonder-grensdraad/`** met het kopersgidspatroon: titel en H1, eerlijkheidsblok, kort antwoord, de gids met inhoudsopgave (vijf koppen), de tabel voor- en nadelen, de keuzehulp, vier FAQ-vragen, een bronnenlijst (18 bronnen) en het auteursblok. Gecontroleerd tegen modellen.json: referentiestation 309 euro, de gateway met LAN-kabel, Mova en Dreame zonder antenne maar met module voor GPS, en Navimow met netwerk-RTK. Dat klopt allemaal.
  - Let op: de FAQ zegt "hellingen tot 30 of 45%". De Eufy E15 Solo staat in het modelbestand op 32,5% (tegenstrijdig, laagste waarde).
- **Metabeschrijvingen** voor homepage, pagina 2 en pagina 11 staan in Yoast.

### 3. Links en woordgebruik
- Alle interne links in de inhoud van de acht pagina's van de eerste golf wijzen naar bestaande concepten, en ankers bestaan. Geen kapotte links.
- Wel en niet gelinkt in de inhoud (afgezien van menu en footer):

| van \ naar | home | p1 | p2 | p12 | methode |
|---|---|---|---|---|---|
| home | — | ja | ja | ja | ja |
| p1 | ja | — | ja | ja | ja |
| p2 | ja | ja | — | **nee** | ja |
| p12 | ja | **nee** | **nee** | — | ja |
| methode | ja | **nee** | **nee** | **nee** | — |

  Niet toegevoegd, omdat er geen tekst voor is. Het menu en de footer bevatten wel links naar de methodepagina en naar kosten.
- **"getest" en "onze test" komen nergens voor**, niet in de 76 concepten en niet in het thema.

### Lanceervoorbereiding
**1. Fotoplaatsvervangers.**
- Pagina 1: de beeldblokken "Foto volgt" zijn uit de inhoud gehaald en de productkoppen zijn één kolom.
- Thema 1.2.4: een filter haalt bij het renderen elk beeldblok weg dat alleen de plaatsvervanger bevat, met CSS als vangnet. Een echte `<img>` blijft staan. Dat geldt voor de latere golven (beste koop, grote en kleine tuin, goedkope robotmaaier, Husqvarna vs Gardena) en de kop-aan-kop-pagina.

**2. SEO per pagina** (homepage, p1, p2, p11, p12, methode, Over ons, auteur), via de Yoast-uitvoer in de API, want concepten zijn niet openbaar:
- **H1:** precies één per pagina.
- **Titels:** uniek.
- **Metabeschrijving:** aanwezig bij zes pagina's; **ontbreekt bij Over ons en de auteurspagina** (niet aangeleverd; niet verzonnen).
- **Canonical:** Yoast laat die weg zolang een pagina noindex of concept is. Lokaal gecontroleerd dat een gepubliceerde, indexeerbare pagina een **zelfverwijzende canonical** krijgt en in de sitemap komt.
- **Schema** (gecontroleerd op structuur, verwijzingen en verplichte velden): per pagina Article, WebPage, BreadcrumbList, WebSite en Person/Organization. Op de auteurspagina komt ImageObject erbij. Er zijn geen fouten, geen ontbrekende verwijzingen en geen Product of Review. `datePublished` staat bij concepten op een nepdatum; dat wordt bij publiceren de echte datum.
  - Een officiële validator (validator.schema.org of de Rich Results Test van Google) kan alleen openbare URL's lezen: draai die na publicatie.
- **Breadcrumbs:** zichtbaar op alle pagina's behalve de homepage, en BreadcrumbList in het schema. Pagina 1 had in het zichtbare pad "Beste robotmaaiers", maar staat niet onder de hub; dat is weggehaald, zodat zichtbaar pad en schema overeenkomen. Yoast gebruikt in het schema de volledige SEO-titel als naam. In 1.2.4 kan de korte kruimelpadtitel (`_yoast_wpseo_bctitle`) via de API worden gezet.
- **Mobiel** (390 px) en desktop (1366 px) in Chromium: geen horizontaal scrollen, geen JavaScript-fouten.

**3. Sitemap, robots en redirects (live):**
- `http://` geeft een 301 naar `https://`, en `www.` een 301 naar het adres zonder www, met behoud van pad en querystring.
- Sitemap: `sitemap_index.xml` geeft 404 en `wp-sitemap.xml` een 301 daarnaartoe; dat is normaal zolang de site noindex is. `page-sitemap.xml` bevat alleen `/`, **geen concepten**.
- `robots.txt` (live, gecachet door LiteSpeed) is de standaard van WordPress met `Sitemap: …/wp-sitemap.xml`, en daarmee na de lancering bruikbaar via de 301. Met 1.2.4 komen er `Disallow: /wp-json/rmk/` en `Disallow: /wp-content/uploads/rmk/` bij, binnen de groep `User-agent: *` (lokaal getest naast het Yoast-blok).
- Er wordt geen HSTS-header meegestuurd. Dat is optioneel; aanzetten kan in hPanel.
- **PageSpeed Insights:** niet uitvoerbaar. De API gaf 429 (geen API-sleutel), en de pagina's zijn concepten, dus voor PSI 404. Gemeten met **Lighthouse 12 (lab)** op de echte paginaschil (header, footer, CSS, JS en lettertypen van robotmaaierkompas.nl) met de weergegeven conceptinhoud:

| Pagina | Mobiel perf | LCP | CLS | TBT | Desktop perf | LCP | CLS | TBT |
|---|---|---|---|---|---|---|---|---|
| Homepage | 97 | 2,1 s | 0 | 80 ms | 99 | 0,7 s | 0 | 0 ms |
| P1 zonder draad | 93 | 2,4 s | 0 | 130 ms | 100 | 0,7 s | 0 | 0 ms |
| P2 vergelijken | 93 | 2,4 s | 0 | 120 ms | 100 | 0,6 s | 0 | 0 ms |
| P11 zonder grensdraad | 96 | 2,1 s | 0 | 80 ms | 100 | 0,6 s | 0 | 0 ms |
| P12 kosten | 95 | 2,5 s | 0 | 80 ms | 100 | 0,7 s | 0 | 0 ms |
| Hoe we beoordelen | 96 | 2,2 s | 0 | 80 ms | 100 | 0,6 s | 0 | 0 ms |
| Over ons | 95 | 2,1 s | 0 | 20 ms | 100 | 0,6 s | 0 | 0 ms |
| Auteur | 97 | 2,2 s | 0 | 20 ms | 100 | 0,6 s | 0 | 0 ms |

  - **INP kan een labmeting niet geven** (daar zijn echte bezoekers voor nodig). TBT is de labvervanger en is overal laag. Alle LCP- en CLS-waarden vallen binnen "goed" (LCP ≤ 2,5 s, CLS ≤ 0,1); P12 zit precies op de grens van 2,5 s.
  - Toegankelijkheid 98 en best practices 96. Toegankelijkheid: de automatische skiplink van WordPress wijst naar een niet-bestaand element; die staat in 1.2.4 uit, de eigen skiplink "Naar de inhoud" blijft. Best practices: een lettertypefout die alleen in de testopstelling optreedt (ander domein).
  - Na de lancering, met de pagina's openbaar: PSI mobiel en desktop opnieuw draaien. Velddata (CrUX, INP) komen pas na enkele weken bezoek.

**4. Nooit in de sitemap en nooit indexeerbaar:**
- **Concepten:** Yoast neemt alleen gepubliceerde, indexeerbare pagina's op (lokaal en live gecontroleerd). In 1.2.4 sluit `wpseo_exclude_from_sitemap_by_post_ids` ook alle concepten, ingeplande, wachtende en privépagina's expliciet uit, en de kernsitemap van WordPress vraagt alleen `publish` op. Voor bezoekers geven concepten 404.
- **`/ga/`:** `X-Robots-Tag: noindex, nofollow` (live: 404 met noindex, want er zijn geen links ingesteld), en geen onderdeel van een sitemap.
- **Beheerroutes `/wp-json/rmk/v1/…`:** 401 zonder beheerder, met `X-Robots-Tag: noindex`. In 1.2.4 ook `noindex, nofollow` op de antwoorden en Disallow in robots.txt.
- **`uploads/rmk/modellen.json`** is openbaar (nodig voor de calculator) en heeft in 1.2.4 een Disallow in robots.txt. Er staan geen prijzen en geen Bol-gegevens in.

### Bevindingen en vragen voor Mandy
- ⚠️ **Menu en footer linken naar pagina's buiten de eerste golf:** `/beste-robotmaaier/`, `/vergelijken/`, `/kopersgids/` en `/hulp/`. Na de lancering van alleen de eerste golf geven die op elke pagina een 404. Kies een van deze opties:
  - die vier sectiepagina's mee publiceren (ze hebben nog alleen een invulveld, dus er is tekst nodig);
  - of het menu tijdelijk aanpassen, bijvoorbeeld "Beste robotmaaiers" naar `/robotmaaier-zonder-draad/`, "Vergelijkingen" naar `/robotmaaier-test-vergelijking/`, en Kopersgids en Hulp tot golf 2 uit het menu. Dat is een themawijziging.
- ⚠️ **Hostinger Reach** laadt `cdn-reach.hostinger.com/js/embed.js` op elke pagina, zonder toestemming en zonder vermelding in de privacyverklaring. Ook Hostinger AI Assistant en Easy Onboarding zijn actief. Zet plugins die je niet gebruikt uit, of neem ze op in de privacyverklaring en de cookiebanner.
- Metabeschrijvingen voor **Over ons** en de **auteurspagina** ontbreken.
- Pagina 11: "hellingen tot 30 of 45%" tegenover 32,5% bij de Eufy E15 Solo.
- Pagina 2 linkt in de tekst naar kernpagina 4 (`/robotmaaier-test-consumentenbond/`). Die is nog een leeg concept. Publiceer je pagina 2 in de eerste golf, dan moet die link eruit of moet pagina 4 mee.

### Thema 1.2.4 (gebouwd en lokaal getest; Mandy moet het nog uploaden)
- Lege fotoplaatsvervangers weg (filter en CSS).
- Filter "Zonder losse module of abonnement".
- Noindex op de beheerroutes, en robots.txt-regels binnen de groep `User-agent: *`.
- Uitsluiting van concepten in de sitemap.
- `_yoast_wpseo_bctitle` via de API.
- De automatische skiplink van WordPress uit.

**Na het uploaden van 1.2.4 (nog niet gedaan):**
1. Korte kruimelpadtitels zetten: p1 "Robotmaaier zonder draad", p2 "Robotmaaiers vergelijken", p11 "Robotmaaier zonder grensdraad", p12 "Kosten", methode "Hoe we beoordelen", Over ons "Over ons", auteur "Mandy van den Broek".
2. Controleren: robots.txt, het filter op pagina 2, en het verdwijnen van plaatsvervangers op de latere-golfpagina's.
3. Bij de lancering: indexering aan, sitemap indienen in Search Console (DNS-verificatie), PSI en de Rich Results Test van Google op de openbare URL's.
