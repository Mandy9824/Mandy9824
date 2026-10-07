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

---

## Ronde 7 (5 oktober 2026): na 1.2.4, menu, plugins, pagina 4, LCP

Alles is **concept**: 76 pagina's, 0 berichten, niets gepubliceerd. "Zoekmachines niet laten indexeren" staat aan.

### 1. Controle na 1.2.4 en de kruimelpadtitels
- **Filter "Zonder losse module of abonnement"** werkt met de live `rmk.js` 1.2.4: alleen de Gardena Smart Sileno Free 800 blijft over, en er zijn geen fouten.
- **robots.txt** heeft nu binnen de groep `User-agent: *` de regels `Disallow: /wp-json/rmk/` en `Disallow: /wp-content/uploads/rmk/`. Dat blijkt uit een verzoek dat de cache omzeilt.
  - De gewone URL gaf nog de oude versie, ook nadat ik de LiteSpeed-cache had geleegd. Die komt waarschijnlijk uit de **Hostinger-CDN** (header `server: hcdn`). Leeg de CDN-cache in hPanel, of wacht tot hij verloopt (max-age 7 dagen).
- **Fotoblokken op latere pagina's** (beste koop, grote en kleine tuin, goedkope robotmaaier, Husqvarna vs Gardena): geen `rmk-ph` meer in de HTML, en de productkoppen staan op één kolom.
- **Korte kruimelpadtitels** gezet. In het schema staat nu bijvoorbeeld "Home › Kosten" en "Home › Over ons › Mandy van den Broek", gelijk aan de zichtbare paden. Ook pagina 4: "Robotmaaier test".

### 2. Menu en footer (tijdelijk)
- De **template-onderdelen header en footer** zijn aangepast als aanpassing in de database (bron `custom`); de themabestanden zijn ongewijzigd.
  - Menu: Robotmaaier zonder draad · Kosten · Vergelijken (`/robotmaaier-test-vergelijking/`) · Hoe we beoordelen · Over ons.
  - Footer "Kiezen": Robotmaaier zonder draad, Vergelijken, Kosten. De kolom "Leren" (Kopersgids, Hulp) is weg. "Over ons" en de juridische links blijven.
  - Live gecontroleerd: geen links meer naar `/beste-robotmaaier/`, `/vergelijken/`, `/kopersgids/` of `/hulp/`, ook niet in de inhoud van de pagina's van de eerste golf.
- **Terugzetten** zodra die pagina's bestaan: in de site-editor bij Patronen > Template-onderdelen > Header en Footer kies je "Aanpassingen wissen". Dan geldt weer het volledige ontwerpmenu uit het thema.
- Let op: zolang de aanpassing bestaat, komen wijzigingen aan het header- of footerpatroon in het thema niet door.

### 3. Plugins en scripts van derden
- **Uitgeschakeld:** Hostinger Reach, Hostinger AI, Hostinger Easy Onboarding en Hostinger Tools. **Actief:** LiteSpeed Cache en Yoast SEO.
- Daarna gecontroleerd: http gaat nog met een 301 naar https, en www naar het adres zonder www (het werkt op serverniveau, niet via Hostinger Tools).
- **Vóór toestemming in Chromium:** geen enkel verzoek naar een ander domein dan robotmaaierkompas.nl. Er wordt geen cookie en geen localStorage gezet (alleen `wordpress_test_cookie`, en dat komt van de inlogpagina die ik zelf opende). De cookiebanner verschijnt. Het script `cdn-reach.hostinger.com/js/embed.js` is weg.

### 4. Metabeschrijvingen
Over ons en de auteurspagina: de teksten uit de opdracht staan in Yoast (gecontroleerd via `yoast_head_json`).

### 5. Tekstwijzigingen
- **Pagina 11:** de FAQ zegt nu "Bij de modellen die wij bekeken noemen fabrikanten hellingen van 30 tot 45%".
- **Pagina 12:** onderaan staat nu de zin over pagina 1 en 2, met links naar `/robotmaaier-zonder-draad/` en `/robotmaaier-test-vergelijking/`.
- **Methodepagina:** onder het scoremodel staat de zin met links naar pagina 1, pagina 2 en `/robotmaaier-kosten/`.

### 6. Pagina 4 `/robotmaaier-test-consumentenbond/` (#13)
- Gebouwd met het kopersgidspatroon:
  - titel en metabeschrijving uit het md-bestand, en de eerlijkheidsblok-variant "Gebaseerd op openbare pagina's van de genoemde organisaties, bekeken op 5 oktober 2026. We testen de maaiers niet zelf en nemen geen testcijfers over.";
  - de tabel, de gids met inhoudsopgave en een genummerd stappenplan;
  - vier FAQ-vragen, "Wat we niet weten" en het auteursblok;
  - interne links naar pagina 2 ("onze vergelijking", "de vergelijkingspagina"), `/robotmaaier-kosten/`, `/robotmaaier-zonder-draad/` ("Onze selectie") en de methodepagina (eerlijkheidsblok).
- **Bronnen:** gewone links, zonder `sponsored` of `nofollow`.
  - ⚠️ Het md-bestand geeft alleen domeinen. De links gaan daarom naar `https://www.test-aankoop.be`, `https://www.test.de/maehroboter/` en `https://www.consumentenbond.nl`. **Vul de precieze URL's in** (het Test-Aankoop-artikel en de vergelijker, de grasmaaierpagina van de Consumentenbond), en controleer de Stiftung Warentest-URL. Vanuit de bouwomgeving kon ik die sites niet openen.
- Gemeld en niet gewijzigd:
  - "getest" komt vier keer voor, telkens over de tests van andere organisaties ("Welke modellen precies zijn getest"), niet over ons.
  - De tekst noemt bedragen: "een set messen bij de geteste modellen tot 15 euro" (Stiftung Warentest) en "verpakkingen messen van ongeveer 15 tot 40 euro". Dat zijn afgeronde bedragen; de opdracht zegt "geen prijzen".
  - De cijfers van de tests (34 en 14 modellen, strook tot 20 cm) heb ik niet kunnen nagaan.

### 7. LCP van pagina 12 (lab, Lighthouse 12, mobiel)
- **LCP-element:** de alinea "Het korte antwoord" (tekst, geen afbeelding). De tijd zit vrijwel helemaal in de **render-vertraging**, door twee render-blokkerende stijlbladen (`tokens.css` en `rmk.css`, elk ongeveer 1,1 s op gesimuleerd 4G).
- Gemeten op de live paginaschil (mediaan van 3 metingen):

| Variant | LCP | FCP |
|---|---|---|
| Nu (twee CSS-bestanden) | 2,62 s | 2,07 s |
| CSS verkleind inline in de `<head>` | **1,23 s** | 1,23 s |
| Inline CSS en vet lettertype vooraf laden | 1,21 s | 1,21 s |

- **Thema 1.2.5:** `tokens.css` en `rmk.css` gaan verkleind inline in de `<head>`, gecachet per themaversie en bestandsdatum. Uitzetten kan met het filter `rmk_inline_css`. De editor gebruikt nog de bestanden. Het vooraf laden van het lettertype heb ik niet toegevoegd, want dat leverde minder dan 0,05 s op.
- Lokaal pixelvergelijking op 390 en 1366 px: inline CSS en de CSS-bestanden geven **identieke** screenshots.
- De inline CSS is ongeveer 39 KB (ongecomprimeerd) per pagina. Dat is de prijs voor één ronde minder.
- **Werkt pas na upload van 1.2.5.** Meet daarna opnieuw op de live site; na de lancering ook met PSI.

### Nog te doen
- [x] Mandy: thema 1.2.5 uploaden en activeren. Daarna meet ik de LCP van pagina 12 opnieuw (ronde 8).
- [ ] Mandy: de CDN-cache in hPanel legen (robots.txt).
- [x] Mandy: de precieze bron-URL's voor pagina 4 (ronde 8).
- [ ] Bij golf 2: de header- en footeraanpassing wissen, of de sectiepagina's eerst vullen en publiceren.

---

## Ronde 8 (6 oktober 2026): 1.2.5 live gemeten, bronnen pagina 4, bevriezing, lanceerlijst

Alles is **concept**: 76 pagina's, 0 berichten. Niets is gepubliceerd, ingepland, privé of wachtend. "Zoekmachines niet laten indexeren" staat aan. Het thema `robotmaaierkompas-child` 1.2.5 is actief.

### 1. Controle van 1.2.5 op de live site
- **De live HTML** bevat `<style id="rmk-inline-css">`, en `tokens.css` en `rmk.css` worden niet meer als bestand geladen.
- **De opzet:** de live paginaschil (`/?nc=…`, met header, footer, CSS, JS en lettertypen van robotmaaierkompas.nl) met de weergegeven conceptinhoud. Ter vergelijking dezelfde inhoud in de 1.2.4-schil van ronde 7 (met de twee CSS-bestanden).
- Lighthouse 12, mobiel, 3 metingen per variant:

| Pagina | Variant | Perf | LCP | FCP | CLS | TBT |
|---|---|---|---|---|---|---|
| P12 `/robotmaaier-kosten/` | 1.2.4 | 88–92 | 2,7–2,9 s | 2,1–2,4 s | 0 | 0–160 ms |
| P12 `/robotmaaier-kosten/` | **1.2.5 live** | **100** | **1,2 s** (3×) | 1,2 s | 0 | 0 ms |
| P1 `/robotmaaier-zonder-draad/` | 1.2.4 | 88–90 | 2,6 s | 2,4 s | 0 | 130–170 ms |
| P1 `/robotmaaier-zonder-draad/` | **1.2.5 live** | **100** | **1,4 s** (3×) | 1,4 s | 0 | 0–20 ms |

- **Ziet het er hetzelfde uit?** Ja, op 390 en 1366 px:
  - Ik heb van elk element op beide pagina's (534 en 871 elementen) de berekende stijlen en de positie en afmetingen vergeleken: **0 verschillen**. Alleen de ruwe tekst van tien CSS-variabelen verschilt: er staat geen spatie meer na een komma. Dat heeft geen invloed op de weergave.
  - De screenshots zijn identiek, op twee na. Bij P1 op 1366 px verschillen 36 pixels in de knoppen van de vaste cookiebanner. Bij P12 op 390 px verschilde bij één meting een handvol pixels, bij de herhaling niet. Dat is anti-aliasing: uitvergroot zijn de knoppen gelijk.

### 2. Bronnen pagina 4 (#13)
- De bronnenlijst heeft nu vier gewone links (zonder `sponsored` of `nofollow`), allemaal "bekeken op 5 oktober 2026":
  1. Test-Aankoop, nieuwsartikel: `https://www.test-aankoop.be/woning-energie/robotmaaiers/nieuws/test-beste-robotmaaiers-2026`
  2. Test-Aankoop, vergelijker: `https://www.test-aankoop.be/woning-energie/robotmaaiers/vergelijker`
  3. Stiftung Warentest: `https://www.test.de/maehroboter/`
  4. Consumentenbond: `https://www.consumentenbond.nl/grasmaaier`
- De afgeronde messenbedragen ("tot 15 euro", "ongeveer 15 tot 40 euro") staan er nog. Verder is er niets gewijzigd. De pagina is nog concept.
- **Bereikbaarheid:** vanuit de bouwomgeving kon ik de sites niet openen. De netwerkproxy blokkeert alle drie de domeinen (`CONNECT 403`, ook via de ophaaltool). Daarom heb ik in een zoekmachine gekeken of de adressen in de index staan:

| Link | Gevonden? |
|---|---|
| Vergelijker Test-Aankoop | ✅ In de index: "Vergelijk en koop de beste robotmaaier van 2026". |
| Consumentenbond `/grasmaaier` | ✅ In de index: "Best geteste grasmaaiers in 2026". Het gaat over grasmaaiers in het algemeen; de robotmaaiers staan onder `/grasmaaier/producten/robot-grasmaaier`. |
| ⚠️ Nieuwsartikel `…/nieuws/test-beste-robotmaaiers-2026` | **Niet gevonden.** Wel gevonden: `https://www.test-aankoop.be/woning-energie/robotmaaiers/nieuws/beste-robotmaaiers-test`, met de titel "Testaankoop test 30 robotmaaiers: dit zijn de beste robotgrasmaaiers van 2026". Misschien is jouw adres nieuwer of een doorverwijzing; dat kan ik niet nagaan. **Open het in je browser.** |
| ⚠️ `https://www.test.de/maehroboter/` | **Niet gevonden** als eigen pagina. De testpagina in de index is `https://www.test.de/Maehroboter-im-Test-4698387-0/` ("Mähroboter im Test"). Misschien verwijst `/maehroboter/` daarnaar door; **open het in je browser.** |

- ⚠️ Pagina 4 noemt bij Test-Aankoop 34 modellen. In de titel van het gevonden artikel staat "30 robotmaaiers", in de samenvatting "meer dan 30". Dat heb ik niet gewijzigd; controleer het in het artikel.

### 3. Thema bevroren op 1.2.5
Er komt geen nieuwe themaversie tenzij er een echte fout is. Wat er aan themawijzigingen opkomt, verzamel ik hier.

**Verzamelde themawijzigingen (niet uitgevoerd):**
- Geen fouten gevonden in deze ronde.
- *Menu en footer:* de themabestanden bevatten nog het volledige ontwerpmenu; live geldt de tijdelijke aanpassing in de database. Dit vraagt geen nieuwe versie: bij golf 2 kies je "Aanpassingen wissen".
- *Lettertype vooraf laden:* levert minder dan 0,05 s op (ronde 7) en is niet nodig.
- *Spaties in CSS-variabelen:* de verkleining haalt de spatie na komma's weg. Dat heeft geen invloed op de weergave en vraagt geen wijziging.

### 4. Lanceerlijst
Zie **`LANCERING.md`**. Daarin staan:
- de voorbereiding;
- de publicatievolgorde van de 15 pagina's: juridisch, dan Over ons en de auteur, dan de methode, dan pagina 12, 11, 4, 1 en 2, en de homepage als laatste;
- de controles vóór de indexering;
- wanneer de indexering aangaat;
- Search Console (DNS-verificatie, sitemap, URL-inspectie);
- Bing Webmaster Tools (importeren uit Search Console);
- de controles van de eerste week.

Op 6 oktober gecontroleerd voor die lijst:
- De 15 concepten van de eerste golf linken in de inhoud alleen naar elkaar. Pagina 2 linkt naar pagina 4, dus die gaan samen.
- Er staat geen `[`, `{{`, "Alfa", "Beta", "gepeild" of "Foto volgt" in de weergegeven tekst.

### Nog te doen
- [ ] Mandy: de twee ⚠️-bronlinks van pagina 4 in je browser openen, en het aantal modellen bij Test-Aankoop (34 of 30) nagaan.
- [ ] Mandy: de CDN-cache in hPanel legen (robots.txt). Dat staat ook in de lanceerlijst.
- [ ] Mandy: de lancering volgens `LANCERING.md`, op een datum die jij kiest.
- [ ] Na de bouw: de toepassingswachtwoorden intrekken.

---

## Ronde 9 (6 oktober 2026): pagina 4, tekstwijzigingen, prijzen in de productbox, thema 1.3.0

Alles is **concept**: 76 pagina's, niets is gepubliceerd. "Zoekmachines niet laten indexeren" staat aan. De themabevriezing op 1.2.5 is opgeheven voor deze ene opdracht: **thema 1.3.0** is gebouwd en lokaal getest. **Mandy moet het nog uploaden**; live draait nog 1.2.5.

### Netwerk
- Vanuit de bouwomgeving zijn alleen robotmaaierkompas.nl en een zoekmachine bereikbaar.
- **Geblokkeerd:** Coolblue, Bol, de sites van de fabrikanten (Navimow, Mova, Dreame, Eufy, Husqvarna, Gardena) en Test-Aankoop.
- Daardoor kon ik vandaag geen winkel- of fabrikantpagina openen. Zie "Prijzen", "Afbeeldingen" en "M003".

### 1. Pagina 4 (#13)
- De bronlink van het nieuwsartikel is nu `https://www.test-aankoop.be/woning-energie/robotmaaiers/nieuws/beste-robotmaaiers-test`.
- In de tabel staat nu "Een test van een dertigtal robotmaaiers in 2026 (34 modellen volgens hun nieuwsartikel)".
- Ook toegepast, uit de tekstwijzigingen:
  - het eerlijkheidsblok van pagina 4 ("… bekeken op 5 oktober 2026. We nemen geen testcijfers over.");
  - de eerste alinea (punt 11).

### 2. Tekstwijzigingen (tekstwijzigingen-afwerking.md)
Alleen de genoemde teksten zijn gewijzigd, en elke "was"-tekst is precies gevonden. De structuur is ongewijzigd: de vervangingen zijn gecontroleerd op hetzelfde aantal `div` en `ul`.

| Punt | Waar | Gedaan |
|---|---|---|
| 1, 2 | Homepage (#9) | Openingstekst en het tweede punt van "Wat we anders doen". De vetgedrukte eerste zin blijft vet. |
| 3 | Eerlijkheidsblok | Op p1, p2, p11 en p12 de nieuwe zin, met een link naar `/hoe-we-beoordelen/`. Pagina 4 kreeg zijn eigen variant. Ook het patroon is bijgewerkt, met `[datum]` als invulveld. |
| 4 | Scoreblok en scorecel | Het label is nu "Betrouwbaarheid en prijs-kwaliteit worden toegevoegd zodra er genoeg reviews en prijzen zijn." (PHP en rmk.js). Het woord "Functiescore" staat er al vlak boven als soort score, dus samen lees je "Functiescore. Betrouwbaarheid …". Daarom staat het er niet nog een keer in. In de balkjes blijft "onvoldoende data", en de rekenregels zijn ongewijzigd. Alle acht modellen met een functiescore missen precies betrouwbaarheid en prijs-kwaliteit, dus het label klopt bij elk model. |
| 5 | Productbox | Zie hieronder. |
| 6 | Over ons (#77) | Nieuwe alinea. |
| 7 | Footer | In het thema en in de tijdelijke live footer (template-onderdeel `custom`): "Wij vergelijken robotmaaiers op specificaties, kosten en reviews. Zie Hoe we beoordelen." Live gecontroleerd. |
| 8 | Methodepagina (#76) | Eerste alinea. De kop "Wat we wel en niet doen" heet nu "Onze werkwijze", ook in de inhoudsopgave; de vier punten zijn vervangen. |
| 9 | Pagina 1 (#11) | De drie teksten, en de kop "Wat we nog uitzoeken". |
| 10 | Pagina 2 (#12) | Openingsalinea. De bestaande link "over onafhankelijke tests" blijft. |
| 11 | Pagina 4 | Zie 1. |
| 12 | Redactiebeleid (#84) | Nieuwe zin. De affiliate-melding heeft geen vergelijkbare zin. |

**Gemeld, niet gewijzigd** (staat niet in de opdracht):
- ⚠️ **Auteursblok** (themapatroon, op elke pagina): "Op deze site test ze de maaiers niet zelf: …". En de **auteurspagina** (#78): "Op robotmaaierkompas.nl test ze de maaiers niet zelf." Volgens de toon hoort deze zin alleen op de methodepagina en Over ons.
- **Methodepagina:**
  - "met het label 'voorlopig, zonder' gevolgd door de ontbrekende onderdelen". Dat label bestaat niet meer.
  - "Op dit moment tonen we nog geen winkelprijzen." Dat klopt niet meer zodra 1.3.0 live staat.
  - Hetzelfde "voorlopig, zonder" staat in de uitleg op de latere pagina's #14, #15, #16 en #64.
- **Pagina 1:**
  - de koppen "(functiescore 92,7, voorlopig)" en "(87,3, voorlopig)";
  - "Alle scores zijn voorlopig".
- **Pagina 2:** "met het label 'voorlopig'".
- **Pagina 12:**
  - "voorlopige functiescores" en "Die scores zijn voorlopig: …";
  - de kop "Wat we nog niet weten" (punt 9 gold alleen voor pagina 1).
- **Footer:** "Koop je via een winkelknop, dan krijgen wij mogelijk een commissie." Er zijn geen affiliatelinks.
- Kop-aan-kop #26 (latere golf, nog met invulvelden): dezelfde lege prijstoestand als het patroon ("Bekijk de actuele prijs" naar `[fabrikantpagina Model A/B]`).

### 3. Prijzen in de productbox (thema 1.3.0, `inc/prijzen.php`)
- **Geldige prijs.** De productbox toont "Laagste nieuwe prijs rond **899 euro** bij Coolblue, gezien op 5 oktober 2026". Daaronder staat de knop "Bekijk bij Coolblue": een gewone link naar de productpagina, zonder `/ga/`, zonder `sponsored` en zonder affiliatecode.
  - Coolblue staat in de lijst met affiliatedomeinen. Knoppen uit `inc/prijzen.php` zijn daarom uitgezonderd van het automatische `rel="sponsored nofollow"` (attribuut `data-rmk-direct`).
- **Geen geldige prijs.** Dan alleen de knop "Bekijk de actuele prijs" naar de fabrikantpagina. Is er ook geen fabrikantpagina bekend, dan is er geen prijsblok.
- **Geldig betekent:**
  - een bedrag, winkel, datum en https-URL zijn ingevuld;
  - het type is winkel of fabrikant (geen marketplace);
  - het is geen Bol (URL en naam) en niet Amazon, eBay, Marktplaats, AliExpress, Temu of een trackingdomein;
  - de datum ligt **niet langer dan 14 dagen** terug (dag 14 telt nog mee, dag 15 niet) en niet in de toekomst.
- Bedragen worden afgerond op hele euro's.
- **Automatisch verdwijnen.** De geldigheid wordt bij elke weergave berekend. Daarnaast leegt een nachtelijke taak (`rmk_prijzen_verloop`, 00:10) de LiteSpeed-cache zodra er een prijs is verlopen, zodat de prijs niet in een gecachte pagina blijft staan.
- **Werking.** De productboxen in de pagina's hebben een scorecel met `data-model`. Het prijsblok in die box wordt bij het weergeven ingevuld, vóór de server-side score.
  - In de inhoud van pagina 1 staat nu `<div class="rmk-offer"></div>`. **Tot 1.3.0 live staat, is dat vak in de voorvertoning leeg.**
- **modellen.json** (script `excel_naar_json.py`): per model `prijs` = {bedrag, winkel, datum, url, type} en `fabrikant_url`, en in `algemeen` de velden `prijzen_gecontroleerd_op` en `prijs_max_dagen`.
  - Bron is het blad **Prijzen** van het Excel-bestand: regels met "Op voorraad" = ja (volgens Leesmij betekent dat ook een nieuw exemplaar), type winkel of fabrikant, en een URL in de kolom Bron. Bol-regels worden overgeslagen.
  - Aanschaf in de calculator blijft leeg, zoals besloten.
  - De dataroute accepteert het veld `prijs` alleen met een heel bedrag, type winkel of fabrikant, en een toegestane https-URL.
- **Live:** het modelbestand is via de dataroute opgeslagen (gegenereerd 6-10-2026 10:11). Met 1.2.5 heeft dat geen zichtbaar effect.
- **Tests:**
  - `tests/prijs-test.php` (nieuw): 18 van 18 geslaagd, onder andere voor 14 en 15 dagen, Bol, marketplace, http, afronding en de dataroute.
  - `tests/score-test.php`: alles geslaagd; PHP en rmk.js zijn gelijk in 2001 gevallen.
  - `tests/bol-test.php`: alles geslaagd.
  - Lokaal weergegeven met de echte inhoud van pagina 1, op 390 en 1366 px: geen horizontaal scrollen en geen JavaScript-fouten.

### 4. Prijzen van de acht modellen
**Gecontroleerd op 6 oktober 2026, maar niet ververst.** De winkel- en fabrikantsites zijn vanuit de bouwomgeving geblokkeerd. Ik kon dus geen enkele prijs met de datum van vandaag bevestigen, en heb er daarom ook geen een met die datum ingevuld.

Gebruikt worden de prijzen uit het blad Prijzen van het Excel-bestand, gezien op **5 oktober 2026**. Ze zijn geldig tot en met 19 oktober.

| Model | Getoond | Bron (blad Prijzen) |
|---|---|---|
| M002 Navimow i206 AWD | rond 899 euro bij Coolblue | coolblue.nl/product/975016 |
| M004 Mova LiDAX Ultra 800 | rond 699 euro bij Mova | nl.mova.tech (fabrikant) |
| M005 Mova LiDAX Ultra 1200 | rond 814 euro bij Mova | nl.mova.tech (fabrikant) |
| M006 Eufy E15 Solo | rond 918 euro bij Coolblue | coolblue.nl/product/975391 |
| M008 Dreame A1 Pro | rond 729 euro bij Coolblue | coolblue.nl/product/962143 |
| M010 Husqvarna 410VE NERA | rond 3.049 euro bij Husqvarna | husqvarna.com/nl (fabrikant) |
| M011 Gardena Sileno Free 800 | rond 1.099 euro bij Coolblue | coolblue.nl/product/959330 |
| M001 Navimow i105E | **geen prijs.** Alleen Bol of een marketplace-verkoper had het op voorraad; Navimow en Hornbach niet. Daarom staat er alleen de knop "Bekijk de actuele prijs" naar de Navimow-pagina. | — |

- Opgevallen: M002 heeft in het blad Prijzen geen fabrikantregel. Verloopt de Coolblue-prijs, dan is er bij M002 geen knop meer.
- **Vóór 19 oktober** (en vlak voor de lancering): prijs en voorraad opnieuw controleren in het Excel-bestand, de datum aanpassen, en het script met `--upload` draaien. Dit staat ook in `LANCERING.md`.

### 5. Afbeeldingen
Ik heb niets gedownload en niets geplaatst. De fabrikantsites zijn geblokkeerd, dus geen enkele gebruiksvoorwaarde kon ik lezen. Dit vond ik via de zoekmachine:

| Fabrikant | Pers- of mediapagina | Voorwaarde |
|---|---|---|
| Segway-Ninebot / Navimow | Geen persmap gevonden. Wel "About us" (navimow.segway.com/pages/about-us) en nieuws (navimow.segway.com/ie/news/…). | Onbekend: **weggelaten** |
| Mova | Geen persmap gevonden; alleen persberichten via PR Newswire. | Onbekend: **weggelaten** |
| Dreame | Geen persmap gevonden. | Onbekend: **weggelaten** |
| Eufy | Geen persmap gevonden. | Onbekend: **weggelaten** |
| Husqvarna | Press room per land (bijv. `https://www.husqvarna.com/ie/learn-and-discover/press-room/`); volgens een persbericht staan de beelden in een image bank op `www.husqvarna.com/press`. Perscontact: press@husqvarna.se. | De algemene gebruiksvoorwaarden zeggen "alleen persoonlijk, niet-commercieel gebruik, tenzij anders vermeld in de Husqvarna Social Media Newsroom". De voorwaarde van de image bank zelf kon ik niet lezen: **weggelaten** |
| Gardena | Geen persmap gevonden. | Onbekend: **weggelaten** |

De productboxen blijven zonder foto. Het bijschrift "Foto: (fabrikant)" en de alt-tekst kunnen erbij zodra een beeld met een duidelijke voorwaarde er is.

### 6. Layout (voorlopig, tot het pakket van Claude Design er is)
- De containers stonden al gecentreerd (1152 px). De paginakop, het kruimelpad, het eerlijkheidsblok en de tekstkolom stonden daarbinnen links.
- In 1.3.0 staan ze nu gecentreerd op leesbreedte (42rem), met één CSS-regel in `rmk.css`. Tabellen, de calculator en tweekolomsblokken blijven op de volle containerbreedte, ook gecentreerd.
- Mobiel is ongewijzigd.
- Klein verschil: paginakoppen met een eigen `max-width: 48rem` in de inhoud (kopersgids, juridisch, hulp) staan iets breder dan het kruimelpad.
- Logo, favicon en het deelbeeld volgen met het Claude Design-pakket.

### 7. M003 Segway Navimow i210 LiDAR (één model per sessie)
- **Niet afgerond.** Voor dezelfde stappen als eerder (waarde met bron en datum in het Excel-bestand, dan het script) moet ik de pagina's van de fabrikant en de winkels kunnen openen. Die zijn geblokkeerd. Ik heb niets ingevuld en niets geschat.
- **Te koop in Nederland: alleen een aanwijzing uit de zoekmachine, niet geopend.**
  - Proshop.nl noemt de "Segway Navimow i210e LiDAR Pro", op voorraad.
  - MediaMarkt **België** noemt de "i210 LiDAR Pro".
  - Bij Coolblue of Navimow NL heb ik niets kunnen controleren.
- ⚠️ **Vraag:** is M003 "i210 LiDAR" hetzelfde model als de "i210E LiDAR Pro" bij de winkels? Dat kan ik niet nagaan.
- M003 is niet als niet leverbaar gemarkeerd: dat is niet vastgesteld. De volgende modellen (Husqvarna Automower 305 en 310, Gardena Sileno Minimo 250 en 500) volgen in latere sessies, één per sessie.

### Nog te doen
- [ ] Mandy: **thema 1.3.0 uploaden en activeren** (`robotmaaierkompas-child.zip`). Daarna controleer ik de productboxen, het label en de centrering live.
- [ ] Mandy: zet in de netwerkinstellingen van deze omgeving de nodige domeinen open. Dan kan ik prijzen verversen, M003 en de volgende modellen uitzoeken en de persvoorwaarden lezen. Nodig zijn onder andere coolblue.nl, nl.navimow.com, navimow.segway.com, nl.mova.tech, nl.dreametech.com, eufy.com, husqvarna.com, gardena.com, proshop.nl en mediamarkt.nl. Een andere mogelijkheid: jij vult de Excel-rijen aan.
- [ ] Mandy: beslissen over de gemelde zinnen (auteursblok, methode, pagina 1, 2 en 12, en de commissiezin in de footer).
- [ ] Prijzen verversen vóór 19 oktober.

---

## Ronde 10 (6 oktober 2026): thema 1.3.1, het afwerkpakket van Claude Design en 1.3.0 samen

Alles is **concept**: 76 pagina's, niets is gepubliceerd. "Zoekmachines niet laten indexeren" staat aan. Er is geen netwerktoegang gebruikt voor beelden of prijzen; die blijven voor de datasessie. **Mandy moet 1.3.1 nog uploaden**; live draait nog 1.2.5.

### Afwerkpakket (README stap 1 tot 9)
| Stap | Gedaan |
|---|---|
| 1. Samenvoegen | `css/`, `logo/`, `iconen/`, `illustraties/` en `deelafbeelding/` staan naast `tokens.css` en `rmk.css`. De snippets en de README staan in `patterns-bron/afwerking/` (niet in de zip). De voorbeeldpagina's zijn alleen lokaal gebruikt. Ik heb de SVG's nagekeken: geen scripts en geen externe verwijzingen. |
| 2. CSS laden | **In de inline CSS** (punt 5 van de opdracht): `rmk_inline_css()` verkleint nu `tokens.css`, `rmk.css` en `css/rmk-afwerking.css`. `url()` wordt per bestand goed gezet, dus `../illustraties/…` werkt. Valt de inline CSS uit (filter `rmk_inline_css`), dan wordt `rmk-afwerking.css` na `rmk.css` geladen. Ook toegevoegd aan `add_editor_style()`. De tijdelijke centreerregels uit 1.3.0 zijn weg; de hoofdkolom komt nu uit `.rmk-column`. |
| 3. Favicon en deelafbeelding | `favicon.svg`, `favicon-32.png` en `apple-touch-icon-180.png` gaan via `wp_head`. De standaard-icoontags van WordPress staan uit, zodat er geen dubbele zijn; Yoast zet zelf geen favicon. **Sitepictogram** (`favicon-512.png`) en **standaard og:image in Yoast** (`deelafbeelding-1200x630.png`): de knop **Gereedschap > Robotmaaierkompas > Huisstijl toepassen** (of `POST /wp-json/rmk/v1/huisstijl`) zet beide als PNG in de mediabibliotheek. De omzetting naar WebP staat daarbij uit, want WebP gaf een verkeerd `og:image:type`. Lokaal getest: `og:image` = de PNG van 1200×630. **Kan pas na de upload van 1.3.1.** De statuspagina heeft er twee controles bij. |
| 4. Logo | Header (`logo-horizontaal-licht.svg`) en footer (`logo-horizontaal-donker.svg`, lazy, onder de vouw). Een filter vervangt elk `a.rmk-logo` bij het weergeven, ook in de live header- en footeraanpassing (template-onderdelen `custom`). Daardoor hoefde ik daar niets aan te passen en is er vóór de upload geen kapot logo. |
| 5. Hoofdkolom | Alle `rmk-container`s in de 76 concepten en de paginapatronen kregen `rmk-column`. `--narrow` voor kopersgidsen (o.a. pagina 4 en 11), hulp, methode, Over ons, auteur en juridisch; `--wide` voor de groep met de vergelijkingstabel op pagina 2. Groepsblokken: `className` en HTML zijn gelijk aangepast (blokvalidatie). |
| 6. Kernpagina's | Pagina 1, 2 en 12, de latere toplijsten en de patronen toplijst, vergelijking en kosten hebben nu de lichte kop met hoogtelijnen (`rmk-pageband`), het icoon en een gecentreerde kop. De eigen eyebrow, H1 en "Door … bijgewerkt op" blijven; de snippettekst is niet gebruikt. |
| 7. Homepage | Zie hieronder. |
| 8. Productfoto's | Zie "Productbox". |
| 9. Publicatiecontrole | Ongewijzigd. In de concepten van de eerste golf staan geen `[haken]` (gecontroleerd); de invulplekken staan alleen in de patronen. |

### Correcties en besluiten
1. **Hero:**
   - Lead: de tekst uit tekstwijzigingen-afwerking.md, niet de snippettekst. De eigen H1 blijft.
   - Eyebrow: "Onafhankelijk vergeleken", uit het ontwerp.
   - Knoppen: de snippet linkte naar `/beste-robotmaaier/` en `/vergelijken/`, die er nog niet zijn. Nu gaan ze naar "Bekijk de robotmaaiers zonder draad" (`/robotmaaier-zonder-draad/`) en "Zelf vergelijken" (`/robotmaaier-test-vergelijking/`).
   - **Eerlijkheidsblok:** overal de nieuwe tekst. Pagina's met het patroon gebruiken de patroontekst uit 1.3.0, de andere hebben de tekst in de inhoud. Er staat nergens meer oude tekst.
2. **Vier ingangen:** naar `/robotmaaier-zonder-draad/`, `/robotmaaier-test-vergelijking/`, `/robotmaaier-zonder-grensdraad/` en `/robotmaaier-kosten/`.
   - Titels en regels komen van de bestaande kaarten. Voor "Robotmaaier zonder grensdraad" is de regel afgeleid van de titel van die pagina: "Hoe werkt het met RTK, camera of LiDAR, en wanneer kies je het?"
   - Het onderdeel "Hoe we beoordelen" is nu een donkere sectie met de bestaande kaarttekst.
   - **Keuzehulp:** de sectie "Begin bij je tuin, niet bij het merk" met de illustratie `tuin.svg` en de knop "Naar de keuzehulp" gaat naar `/robotmaaier-zonder-draad/#keuzehulp`. Het keuzehulpblok op pagina 1 kreeg dat anker. De keuzehulp zelf staat niet meer op de homepage.
   - **Onlangs bijgewerkt:** de shortcode `[rmk_onlangs_bijgewerkt]` toont de drie laatst bijgewerkte gepubliceerde pagina's, met Nederlandse datum. De homepage, verplichte pagina's en sectiepagina's tellen niet mee. Bij minder dan drie verschijnt er niets; live is dat nu het geval, want er is niets gepubliceerd.
   - Verder op de homepage: "Wat we anders doen", "Wie zit erachter?", het auteursblok en de affiliate-melding, in de hoofdkolom.
   - **Achtergronden:** donker (hero), vertrouwensstrook, wit (ingangen), licht groen (keuzehulp), standaard, en donker groen (Hoe we beoordelen).
3. **Productbox:**
   - Geen Bol; de prijsregel uit 1.3.0 blijft.
   - Het fotokader uit het pakket (`rmk-photo--square`, bijschrift "Foto: (fabrikant)", alt "(model), productfoto") komt er alleen als het model in modellen.json een `foto` heeft. Bol-, Amazon- en marketplace-domeinen worden geweigerd, ook de beeldserver van Bol `s-bol.com`. De dataroute controleert dit veld ook.
   - In de patronen staat de plaatsvervanger uit het pakket. Die wordt bij het weergeven altijd weggehaald (filter, plus CSS als vangnet), dus nooit getoond op een gepubliceerde pagina.
   - Er zijn nu geen foto's: dat is voor de datasessie.
4. **Tekstwijzigingen:**
   - **Auteursblok** (patroon) en de tweede alinea van de **auteurspagina** (#78): de nieuwe teksten.
   - **Methodepagina** (#76): de prijszin is vervangen door "Een prijs noemen we alleen met de winkel en een datum. Prijzen ouder dan 14 dagen verdwijnen automatisch, en we tonen geen prijzen van marketplace-verkopers." Het label "voorlopig, zonder" is vervangen door het nieuwe scorelabel.
   - **Pagina 1** (#11): de koppen "(functiescore 92,7)", "(87,3)" enzovoort, zonder "voorlopig". "Alle scores zijn voorlopig en komen uit …" is "Alle scores komen uit …" geworden.
   - **Pagina 2** (#12): ", met het label 'voorlopig'" is weggehaald.
   - **Pagina 12** (#18): "voorlopige functiescores" is "functiescores" geworden, en "Die scores zijn voorlopig:" is "Die scores zijn functiescores:" geworden.
   - In de eerste golf staat nergens meer "voorlopig" of "niet zelf".
   - **Footer** (thema en live aanpassing, live gecontroleerd): "Wij kunnen een commissie ontvangen bij aankopen via links op deze site. Zie de affiliate-melding."
   - Niet gewijzigd: de zin van het patroon affiliate-melding ("Advertentie: via deze knoppen krijgen wij mogelijk een commissie …"). Die stond niet in de opdracht.
5. **CSS en LCP:** zie hieronder.
6. **Logo, favicon, sitepictogram en deelafbeelding:** zie stap 3 en 4.
7. **Afbeeldingen en prijzen:** niet aangeraakt.

### Browsertest (Chromium, lokale testsite met de live header en footer en de nieuwe inhoud)
| Breedte | Menu | Overig |
|---|---|---|
| 1440 en 1366 px | **Vijf items zichtbaar**, elk op één regel (44 px), geen menuknop | Hoofdkolom 1088 px gecentreerd, tekstpagina's 864 px. Geen horizontaal scrollen. |
| 1280 en 1024 px | Menuknop. Het pakket klapt het menu in tussen 64 en 82rem, zodat items nooit over twee regels lopen. | Geen horizontaal scrollen |
| 390 px (mobiel) | **Ingeklapt** tot de menuknop; uitgeklapt staan alle vijf items onder elkaar | Geen horizontaal scrollen |

- Getest: homepage, pagina 1, 2, 4 en 12, de methodepagina en de auteurspagina. Geen JavaScript-fouten. De enige consolemelding was de auteursfoto van het live domein, die het testcertificaat in de testomgeving niet laadde.
- Gecontroleerd:
  - de links van de homepage (zie hierboven);
  - het anker `#keuzehulp` op pagina 1;
  - de prijsregels in de productboxen ("Laagste nieuwe prijs rond 899 euro bij Coolblue, gezien op 5 oktober 2026");
  - het nieuwe label in de scorecellen;
  - de kostencalculator (730 euro over 5 jaar geeft 146 euro per jaar);
  - het filter met de tabel op pagina 2 (8 rijen);
  - favicon, logo's en `og:image`;
  - dat er geen plaatsvervanger op de pagina's staat.

### LCP (Lighthouse 12, mobiel, 3 metingen, met gzip zoals de live server)
- **Het LCP-element is nu de H1 in de nieuwe kop**, in Schibsted Grotesk.
  - In 1.3.1 wordt dat lettertype vooraf geladen. Dat scheelt 0,4 s in FCP.
  - Het footerlogo laadt lazy.

| Pagina | LCP | FCP | CLS | TBT | Score |
|---|---|---|---|---|---|
| P1 `/robotmaaier-zonder-draad/` | **1,8 s** (3×) | 0,9 s | 0 | 40 ms | 100 |
| P12 `/robotmaaier-kosten/` | **1,9 / 1,9 / 1,8 s** | 0,9 s | 0 | 10–40 ms | 100 |

- Doel onder 2 s: gehaald, maar met weinig marge. Dat komt door de lettertypen van de kop (47 KB) en de basistekst.
- **Eerlijk vergeleken met eerdere rondes:**
  - De metingen van ronde 7 en 8 (1,2 en 1,4 s) waren te gunstig. De lettertypen laadden daar niet in de testopstelling (ander domein).
  - Zonder gzip komt dezelfde pagina op 2,4 s.
  - Na de upload meet ik het opnieuw op de live site, na de lancering ook met PSI.

### Thema 1.3.1 (gebouwd en lokaal getest; Mandy moet het nog uploaden)
- **Tests:**
  - `tests/score-test.php`: geslaagd.
  - `tests/prijs-test.php`: 23 van 23 geslaagd, nu ook voor foto en plaatsvervanger. De teller werkte niet goed binnen `wp eval-file`; dat is hersteld.
  - `tests/bol-test.php`: geslaagd.
  - PHP-lint: alles in orde.
- Zip `robotmaaierkompas-child.zip`: 392 KB.
- **Let op tot de upload:** de concepten verwijzen al naar het icoon in de kop (`logo/icoon-*.svg`) en naar `illustraties/tuin.svg`. In de voorvertoning ontbreken die beelden tot 1.3.1 actief is.

### Nog te doen
- [ ] Mandy: **1.3.1 uploaden en activeren**, en daarna **Huisstijl toepassen** (Gereedschap > Robotmaaierkompas). Daarna controleer ik live het logo, het favicon, `og:image`, het menu en de LCP.
- [ ] Datasessie: foto's (met een duidelijke voorwaarde), prijzen verversen vóór 19 oktober, en M003.

---

## Ronde 11 (6 oktober 2026): thema 1.3.2, productbox met specificatiekaart

Alles is **concept**: 76 pagina's, niets is gepubliceerd. "Zoekmachines niet laten indexeren" staat aan. Live draait **1.3.1**, dat Mandy heeft geüpload. **1.3.2 is gebouwd en lokaal getest; Mandy moet het nog uploaden.**

### 1. Titel en score
- Op pagina 1 (#11) zijn de zeven H3's boven de kaarten weg, zoals "Segway Navimow i206 AWD (functiescore 92,7)".
- Naam en score staan nu alleen in de kaart.

### 2. Scorelabel
- Het gestippelde kader is weg.
- Onder de score staat nu "Functiescore: wat deze maaier kan. Hoe we scoren", met een link naar `/hoe-we-beoordelen/`. Dat geldt in de productbox, in het scoreblok en in rmk.js; PHP en JS zijn gelijk (2001 gevallen getest).
- **In tabellen** staat de regel één keer onder de tabel in plaats van in elke rij. Dat geldt voor de scoretabel (shortcode) en voor de vergelijkingstabel op pagina 2 (#12, één regel toegevoegd).

### 3. Teksten in de kaart
- `modellen-teksten.json` staat in de repository als `scripts/modellen_teksten.json`.
  - Het script zet `beste_voor`, `pluspunten` en `minpunten` in modellen.json; de acht modellen worden alle acht gevonden.
  - Live opgeslagen via de dataroute (gegenereerd 6-10-2026 15:45).
  - De dataroute controleert de velden: een tekst of een lijst van hoogstens 8 teksten, elk hoogstens 300 tekens.
- In de kaart:
  - "Beste voor" met de tekst;
  - de pluspunten en minpunten als lijsten met de plus- en mintekens uit het ontwerp, over de volle kaartbreedte.
- Op pagina 1 zijn de losse alinea's weg: twaalf alinea's "Voor wie / Pluspunten / Minpunten", en de drie vrije alinea's bij de i105E, de E15 Solo en de Gardena (die herhaalden hetzelfde). Lege secties zijn opgeruimd.
- ⚠️ **Daarmee verdwenen ook drie zinnen die niet in de nieuwe teksten staan:**
  - i105E: "Het stond nog bij een winkel nieuw te koop."
  - E15 Solo: "die twee cijfers komen niet overeen" (de minpunt noemt wel 40% en 32,5%).
  - Gardena: "geen 4G".
  Wil je ze terug, zet ze dan in modellen_teksten.json.
- Gevolg: de scoretabel op pagina 1 toont nu ook de kolom "Beste voor", omdat die tekst er is. De kolom "Prijs vanaf" zegt nog "bij de winkel"; de prijs staat in de kaart.

### 4. Specificatiekaart (pakket v1.3, README stap 1 tot 5)
- **Samengevoegd:**
  - `css/rmk-specificatiekaart.css`, 5 iconen en 2 illustraties;
  - de snippets in `patterns-bron/specificatiekaart/`.
  - Er wordt niets overschreven. De bestanden bevatten geen scripts en geen externe verwijzingen.
- **CSS:** in de inline CSS, na rmk-afwerking. De verkleining laat `url(...)` en de ingebedde SVG-iconen nu onaangetast. Als bestand alleen als de inline CSS uit staat; ook in de editor.
- **Productbox** (wordt bij het weergeven gevuld uit modellen.json):
  - Zonder foto: de kaart met merk en model in het vlak (`aria-hidden`, want de H3 noemt ze), en "Geen productfoto beschikbaar".
  - Met foto: de fotovariant met "Foto: (fabrikant)" en alt-tekst. Bol-, Amazon- en marketplace-domeinen worden geweigerd.
  - **Vijf kenmerken:** oppervlak (`max_tuingrootte_m2`), helling (`max_helling_pct`), navigatie (RTK + camera, camera, LiDAR, RTK), geluid (`geluid_dba`, als "59 dB") en verbinding (4G, module, geen).
  - Ontbreekt een waarde, dan komt de `is-missing`-chip, met "onbekend" voor schermlezers. Bij de acht modellen ontbreekt niets.
- **Patronen:** de productboxen en kop-aan-kop hebben de kaart met invulvelden.
- **Indeling op desktop** (vanaf 768 px): de kaart staat links; rechts staan titel, "Beste voor", score en prijs; de plus- en minpunten staan eronder over de volle breedte. Op mobiel staat alles onder elkaar. Eerst stond de titel in een smalle middenkolom; dat is aangepast.
- **Geen lege ruimte onderin:** gemeten 1 px tussen de laatste inhoud en de rand, bij alle 8 kaarten en op alle breedtes.

### 5. Browsertest (Chromium, lokaal, live header en footer)
| Breedte | Resultaat |
|---|---|
| 1440 / 1366 px | Menu met vijf items zichtbaar. Kaarten in twee kolommen. Geen horizontaal scrollen. |
| 1024 / 768 px | Menuknop. Kaarten in twee kolommen. Geen horizontaal scrollen. |
| 390 px | Menuknop. De kaart staat bovenaan in de productbox, de chips in twee kolommen en de vijfde over de volle breedte. Geen horizontaal scrollen. |

- Geen JavaScript-fouten op de homepage, pagina 1, 2 en 12.
- Er zijn geen gestippelde kaders meer bij de scores.
- Op pagina 1 staan 8 kaarten, elk met "Beste voor", plus- en minpunten en een prijsregel (bij de i105E de knop "Bekijk de actuele prijs").

### 6. LCP (Lighthouse 12, mobiel, gzip, 3 metingen)
| Pagina | LCP | FCP | CLS | TBT | Score |
|---|---|---|---|---|---|
| P1 | **1,8 s** (3×) | 0,9–1,0 s | 0 | 0–120 ms | 99–100 |
| P12 | **1,8 / 1,8 / 1,7 s** | 0,9 s | 0 | 0–30 ms | 100 |

Het doel van onder 2 s is gehaald. Het LCP-element is de H1 in de kop.

### 7. Gevonden en hersteld: een beheerroute stond in de cache
- **Fout:** LiteSpeed cachete het antwoord van `GET /wp-json/rmk/v1/status` op een verzoek met een toepassingswachtwoord. LiteSpeed ziet zo'n verzoek niet als ingelogd. Daardoor was de statuslijst ook **zonder inloggen** te zien.
  - Inhoud: de bouwcontroles, zoals indexering, permalinks, plugininstellingen en de naam van de Yoast-persoon.
  - Geen wachtwoorden, sleutels of conceptteksten.
  - Andere routes heb ik nagelopen (pagina's met `context=edit`, instellingen, template-onderdelen, thema's, gebruikers, modellen): die gaven zonder inloggen 401 en werden niet gecachet.
- **Direct gedaan:** de cache geleegd via de dataroute. Daarna gaf `/rmk/v1/status` zonder inloggen 401.
- **In 1.3.2:** antwoorden van `/rmk/v1/` en elk REST-antwoord aan een ingelogde gebruiker of een verzoek met Basic-authenticatie krijgen `litespeed_control_set_nocache`, `Cache-Control: no-store, private` en `X-LiteSpeed-Cache-Control: no-cache`. Lokaal gecontroleerd.
- **Tot 1.3.2 live staat:** de status alleen bekijken via Gereedschap > Robotmaaierkompas, niet via de REST-route.

### Ook gedaan
**Huisstijl:** live toegepast via de route `rmk/v1/huisstijl` (onderdeel van ronde 10, punt 6).
- Sitepictogram is bijlage 216 (`favicon-512.png`).
- De standaard og:image in Yoast is `deelafbeelding-1200x630-1.png` (bijlage 217).
- De statuscontroles voor beide zijn groen.

### Tests
- `score-test.php`: geslaagd.
- `prijs-test.php`: **29 van 29** geslaagd, nu ook voor kaart, kenmerken, `is-missing`, foto, Bol-beeld, dubbel vullen en label.
- `bol-test.php`: geslaagd.
- PHP-lint: in orde.
- De zip is 404 KB.

### Nog te doen
- [ ] Mandy: **1.3.2 uploaden en activeren.** Daarna controleer ik live de kaarten, het label, de cacheheaders van `/rmk/v1/status` en de LCP.
- [ ] Mandy: beslissen over de drie verdwenen zinnen (zie punt 3).
- [ ] Datasessie: foto's (alleen met een duidelijke voorwaarde), prijzen verversen vóór 19 oktober, en M003.

---

## Ronde 12 (6 oktober 2026): thema 1.3.3, prijzen in de tabellen en geen cache voor de REST-API

Alles is **concept**: niets is gepubliceerd. "Zoekmachines niet laten indexeren" staat aan. Live draait **1.3.2**. **1.3.3 is gebouwd en lokaal getest; Mandy moet het nog uploaden.**

Er is nog geen release met uitgelichte beelden, dus dit werk zit in 1.3.3.

### 1. Prijs in de scoretabel (pagina 1) en de vergelijkingstabel (pagina 2)
- **Pagina 1** (shortcode `[rmk_scoretabel]`):
  - De kolom "Prijs vanaf" ("bij de winkel") heet nu **"Laagste nieuwe prijs"**.
  - Inhoud: "rond 899 euro" met de winkel klein eronder.
  - De regels zijn dezelfde als in de productbox: nieuw, op voorraad, winkel of fabrikant, geen Bol of marketplace, hoogstens 14 dagen oud. Anders "–" (schermlezers horen "geen actuele prijs").
- **Pagina 2** (#12) had geen prijskolom. Die heb ik toegevoegd: de kopkolom "Laagste nieuwe prijs" en per rij een cel `data-rmk-price="Mxxx"`, die bij het weergeven uit modellen.json wordt gevuld en dus ook vanzelf verloopt.
  - Rijen met een geldige prijs krijgen ook `data-price`, zodat sorteren op prijs en het budgetfilter werken.
- **Onder elke tabel** staat één regel: "Prijzen gezien op 5 oktober 2026. Laagste nieuwe prijs bij een winkel of de fabrikant, afgerond." Zijn er geen geldige prijzen, dan verdwijnt die regel.
- De patronen scoretabel en vergelijkingstabel zijn op dezelfde manier aangepast.
- Lokaal weergegeven:

| Model | Prijs in de tabel |
|---|---|
| M002 Navimow i206 AWD | rond 899 euro, Coolblue |
| M010 Husqvarna 410VE NERA | rond 3.049 euro, Husqvarna |
| M005 Mova LiDAX Ultra 1200 | rond 814 euro, Mova |
| M004 Mova LiDAX Ultra 800 | rond 699 euro, Mova |
| M008 Dreame A1 Pro | rond 729 euro, Coolblue |
| M001 Navimow i105E | – |
| M006 Eufy E15 Solo | rond 918 euro, Coolblue |
| M011 Gardena Sileno Free 800 | rond 1.099 euro, Coolblue |

- **Twee fouten gevonden en hersteld:**
  - Op pagina 2 werd de pagina op 1366 px **breder dan het scherm** (scrollWidth 1754). Oorzaak: de verborgen schermlezertekst (`.rmk-sr`, absoluut) in de prijscel viel buiten het scrollvak van de tabel. `.rmk-tablewrap` heeft nu `position: relative`; de tabel scrolt binnen haar vak, met de eerste kolom vast.
  - Op mobiel viel bij de scoretabel op pagina 1 "Functiescore, van 100" **buiten de kaart**. Dat komt door de kolom "Beste voor" uit 1.3.2. Nu staat "Beste voor" over de volle breedte onder naam en score, en de score is smaller en loopt door op de volgende regel.
- **Browsertest** (Chromium, 1366 en 390 px):
  - pagina 1 en 2 zonder horizontaal scrollen en zonder JavaScript-fouten;
  - de datumregel en de scoreregel staan onder beide tabellen.

### 2. Geen cache voor `/wp-json/`
- **1.3.3:**
  - Elk antwoord van een echte REST-aanvraag krijgt `litespeed_control_set_nocache`, `Cache-Control: no-store, no-cache, private, max-age=0`, `X-LiteSpeed-Cache-Control: no-cache`, `CDN-Cache-Control: no-store` en `Surrogate-Control: no-store`.
  - Gebeurt al bij `rest_api_init`, dus ook bij fouten.
  - Interne REST-aanroepen op gewone pagina's laten de paginacache met rust: lokaal gecontroleerd dat gewone pagina's geen no-store krijgen.
- **`/wp-json/rmk/` alleen voor beheerders:**
  - Ook de naamruimte-index `/wp-json/rmk/v1` geeft zonder beheerder 401 "Alleen voor beheerders".
  - `rmk/v1` en de routes staan niet meer in de openbare index `/wp-json/`.
  - Lokaal gecontroleerd zonder inloggen.
- **Live nu (1.3.2), zonder inloggen:**

| Adres | Antwoord |
|---|---|
| `/wp-json/rmk/v1/status` en `/modellen` | 401, met no-store |
| `/wp-json/rmk/v1` | 200, met alleen de lijst van routes. Geen gegevens, maar wel zichtbaar. Na 1.3.3: 401. |
| `/wp-json/` | noemt `rmk/v1` en zijn zeven routes. Na 1.3.3 niet meer. |

- **Hostinger-CDN:** de CDN gaf voor `/wp-json/rmk/v1` de status `DYNAMIC` (niet gecachet). Met `CDN-Cache-Control: no-store` hoort dat zo te blijven. Een uitzondering voor `/wp-json/*` in hPanel bij de CDN-instellingen is een extra vangnet; dat kan alleen Mandy.
- **Na de upload van 1.3.3** (gaat niet vóór de upload): ik controleer zonder inloggen of `/wp-json/rmk/`, `/wp-json/rmk/v1` en `/wp-json/rmk/v1/status` geen gegevens teruggeven, en of de cacheheaders en `x-hcdn-cache-status` kloppen. Mandy kan hetzelfde in een privévenster doen (zie LANCERING.md, stap 3).

### 3. De drie weggehaalde zinnetjes
Die blijven weg, zoals besloten.

### Tests
- `prijs-test.php`: **34 van 34** geslaagd, nu ook voor de tabelcel, "–", prijzen ouder dan 14 dagen en de datumregel.
- `score-test.php`: geslaagd.
- `bol-test.php`: geslaagd. De prijscel zonder prijs is nu "–".
- PHP-lint: in orde.
- De zip is 404 KB.

### Nog te doen
- [ ] Mandy: **1.3.3 uploaden en activeren.** Daarna controleer ik zonder inloggen `/wp-json/rmk/` en de cacheheaders.
- [ ] Mandy, als extra vangnet: in hPanel bij de CDN-instellingen `/wp-json/*` uitsluiten van de cache.
- [ ] Datasessie: prijzen verversen vóór 19 oktober (anders tonen beide tabellen "–" en verdwijnt de datumregel), foto's en M003.

### Aanvulling ronde 12: uitgelichte beelden (in dezelfde release 1.3.3)
1.3.3 was nog niet geüpload, dus de beelden zitten in dezelfde release.

**Gekoppeld (live, concepten):**

| Pagina | Uitgelicht beeld (bijlage) |
|---|---|
| homepage (#9) | homepage-hero (225), 1440×810 |
| /robotmaaier-zonder-draad/ (#11) | zonder-draad-header (226), 1440×810 |
| /robotmaaier-kosten/ (#18) | kosten-header (223), 1600×900 |
| /robotmaaier-test-vergelijking/ (#12) | vergelijken-header (224), 1280×720 |
| /robotmaaier-zonder-grensdraad/ (#17) | zonder-grensdraad-header (222), 1600×900 |
| /robotmaaier-test-consumentenbond/ (#13) | tests-header (221), 1600×900 |
| /hoe-we-beoordelen/ (#76) | methode-header (220), 1600×900 |

- Alle zeven zijn 16:9 WebP, met de WordPress-formaten 768, 1024 en (bij 1600) 1536.
- Het zijn sfeerfoto's van tuinen, een tafel en een vergrootglas, zonder herkenbaar merk of model. **Alt-tekst:** in de mediabibliotheek leeg, dus decoratief. De H1 ernaast zegt waar de pagina over gaat. Vult Mandy een alt-tekst in, dan wordt die gebruikt.

**Deelbeeld in Yoast:** per pagina het uitgelichte beeld, gecontroleerd via `yoast_head_json`.
- Eerst gaf Yoast nog het standaardbeeld. De REST-API zet het uitgelichte beeld pas ná het opslaan, en Yoast had zijn index al bijgewerkt. Na een tweede opslag kloppen ze alle zeven.
- ⚠️ De deelbeelden zijn **WebP**. De meeste platforms tonen dat, maar niet allemaal; een JPEG- of PNG-versie van 1200×630 is het veiligst. Dat is een keuze voor Mandy.

**Thema (`inc/beeld.php`):**
- **Kernpagina's, gidsen en de methodepagina:** het beeld staat onder de paginakop, in een 16:9-kader, met `width`, `height`, `srcset` en `sizes` (60rem of, in een smalle kolom, 50rem).
- **Homepage:** het beeld is de achtergrond van de hero. Daarop ligt een donkergroen verloop (`#133B26` op 90 / 85 / 92%) en daarboven het hoogtelijnen- en kompasmotief op 35%.
- **Contrast** (gemeten in Chromium op het lichtste punt achter de tekst, tekst onzichtbaar gemaakt):

| Tekst | 1366 px | 390 px |
|---|---|---|
| H1 | 6,42:1 | 7,09:1 |
| Introductie | 7,50:1 | 7,49:1 |
| "Onafhankelijk vergeleken" | 4,74:1 | 4,88:1 |

  Alles haalt AA. Bij het eerste verloop (86/80/90%) kwam "Onafhankelijk vergeleken" op 4,14:1; daarom is het verloop donkerder gemaakt.
- **Laden:** het kopbeeld heeft `fetchpriority="high"` en `loading="eager"`. Alle andere beelden in de inhoud laden lazy (`wp_omit_loading_attr_threshold` = 0): auteursfoto, kompasicoon, tuinillustratie, footerlogo en foto's in de kaarten.
  - Uitzondering: het headerlogo, klein en boven de vouw, laadt gewoon.
- **Browsertest** (1366 en 390 px): homepage, pagina 1, 4 en 12 en de methodepagina, zonder horizontaal scrollen en zonder JavaScript-fouten.
  - Mobiel laadt het 768-formaat, desktop het 1024-formaat (hero: 1440).

**LCP (Lighthouse 12, mobiel, gzip, 3 metingen per pagina):**

| Pagina | LCP | FCP | LCP-element |
|---|---|---|---|
| Homepage | 2,3 / 2,3 / 2,3 s | 0,9 s | hero-foto |
| P1 | 2,3 / 2,3 / 2,3 s | 0,9 s | kopfoto |
| P12 | 2,1 / 2,1 / 2,1 s | 0,9 s | kopfoto |

- CLS is 0, TBT 0–70 ms, score 98–99.
- ⚠️ **Het doel van onder 2,0 s wordt met de foto als LCP-element niet gehaald.** Wel valt het binnen "goed" van Core Web Vitals (≤ 2,5 s).
- **Proeven:**

| Proef | LCP |
|---|---|
| Kopbeeld 640 px (36–45 KB) of 480 px (23–28 KB) in plaats van 768 px (78–82 KB) | 2,0 s |
| Plus een preload van het beeld bovenaan de `<head>` | 2,0 s |
| Zonder preload van het kop-lettertype | 2,0 s (FCP 1,4 s) |
| Pagina 1 zonder kopbeeld | 1,9 s |
| Lettertypen als Latin-subset | scheelt maar 3 KB, dus geen winst |

  De ondergrens in deze labopstelling ligt rond 1,9–2,0 s: een gesimuleerde TTFB van 450 ms, plus de lettertypen (samen ruim 80 KB).
- **Opties** (Mandy kiest):
  1. **Een kleinere mobiele versie** (bijv. 680 px breed, kwaliteit 60–75, ongeveer 40 KB): ongeveer 2,0 s. Vraagt een extra beeldformaat in het thema en het opnieuw aanmaken van de formaten voor de zeven beelden.
  2. **Op mobiel het beeld kleiner of lager in de pagina**, zodat de H1 het LCP-element blijft: ongeveer 1,9 s.
  3. **Zo laten** (2,1–2,3 s in het lab) en na de lancering de echte cijfers van PSI en Search Console afwachten. De lab-TTFB is strenger dan een gecachte LiteSpeed-pagina.
  4. Het kop-lettertype (variabel, 47 KB) beperken tot de gebruikte gewichten. Verwachte winst: 0,05–0,1 s.
- **Mijn advies:** 1 en 2 samen als 2,0 s een harde grens is, anders 3.

**Tests:** score-, prijs- (34/34) en Bol-tests geslaagd, PHP-lint in orde, de zip is 408 KB.

---

## Ronde 13 (7 oktober 2026): thema 1.3.4, inhoudsopgave, analyse in de kaart, hub en deelbeeld

Alles is **concept**: 76 pagina's, niets is gepubliceerd. "Zoekmachines niet laten indexeren" staat aan. Live draait **1.3.3**. **1.3.4 is gebouwd en lokaal getest; Mandy moet het nog uploaden.**

### Controle na de upload van 1.3.3 (live, zonder inloggen)
- **`/wp-json/rmk/`:**
  - `/wp-json/rmk` en `/rmk/` geven 404.
  - `/rmk/v1`, `/rmk/v1/`, `/status`, `/modellen` en `/huisstijl` geven 401 "Alleen voor beheerders".
  - Allemaal met `Cache-Control: no-store` en `X-LiteSpeed-Cache-Control: no-cache`. Er komen geen gegevens terug.
- **De index `/wp-json/`** kwam nog uit een cache van vóór 1.3.3 (LiteSpeed én CDN: HIT) en noemde `rmk/v1` nog.
  - Ik heb LiteSpeed geleegd via de dataroute (bij het opslaan van de analyseteksten).
  - Daarna: `rmk/v1` staat niet meer in de index, `no-store` en `CDN-Cache-Control: no-store`, en de CDN-status is DYNAMIC.
- **Gewone pagina's** blijven cachebaar.
  - Kanttekening: `/` geeft nu 404, omdat de homepage concept is, en krijgt daardoor geen cache.

### 1. Inhoudsopgave (methodepagina, pagina 4 en 11) en filters (pagina 2)
- **Oorzaak:** vanaf 64rem (1024 px) was het blok vastgeplakt. In de smalle kolom stond het dan bóven de tekst in plaats van ernaast, en tijdens het scrollen schoof het over de tekst.
- **In 1.3.4:**
  - Onder 75rem (1200 px) is het nooit vastgeplakt (`position: static`); het staat dan boven de tekst.
  - Vanaf 75rem staat het in een eigen gridkolom (13–16rem) naast de tekst, alleen dáár vastgeplakt, met een maximale hoogte en eigen scroll.
  - Op die schermen is de smalle kolom van pagina's met een inhoudsopgave 64rem breed. Paginakop en kopbeeld blijven op 50rem.
- **Getest in Chromium** (methodepagina, pagina 4, 11 en 2; 390, 768, 1024 en 1440 px). Bij het scrollen door de hele pagina gemeten of het blok tekst, kopjes, lijsten of tabellen bedekt:

| Breedte | Stand | Overlap |
|---|---|---|
| 390 / 768 / 1024 px | `static` (pagina 2 op 1024 px: filters naast de tabel, niet vastgeplakt) | 0 |
| 1440 px | `sticky`, naast de tekst | 0 |

  Geen horizontaal scrollen en geen JavaScript-fouten.

### 2. Analyse in de kaart
- `modellen-analyse.json` staat als `scripts/modellen_analyse.json` in de repository. Het script zet per model het veld `analyse`; de acht modellen worden alle acht gevonden.
- Live opgeslagen via de dataroute (gegenereerd 7-10-2026 12:37). De dataroute controleert het veld (tekst van hoogstens 1500 tekens).
- **Kaart:** de analyse staat als eigen alinea onder "Beste voor" en het prijsblok en boven de plus- en minpunten, over de volle breedte en op leesbreedte. Lokaal gecontroleerd: bij alle 8 kaarten staat ze op die plek. Op 1440 en 390 px is er geen horizontaal scrollen.
- **Pas zichtbaar met 1.3.4.**

### 3. Hub `/beste-robotmaaier/` (#10, concept)
- **Gebouwd uit `pagina-3-beste-robotmaaier.md`**, met de opbouw van pagina-hub:
  - titel, metabeschrijving en de kruimelpadtitel "Beste robotmaaiers";
  - het eerlijkheidsblok, "Bijgewerkt op 7 oktober 2026";
  - het korte antwoord, de vier stappen (genummerde lijst), de keuzehulp (patroon, anker `#keuzehulp`), de situatietabel, "Waar let je op?", "Onafhankelijke tests" en "Zo beoordelen we";
  - drie FAQ-vragen, de bronnen en het auteursblok.
- **Controle:** één H1, geen invulvelden, geen Bol, geen €-teken, geen `/ga/`. Links alleen naar bestaande pagina's: de vijf kernpagina's, `/hoe-we-beoordelen/`, de auteur en `#keuzehulp`.
- **Bronnenlijst:** het md-bestand gaf geen bronnen. De lijst bevat daarom de bronregels uit het Excel-bestand voor de gegevens in de tabel (navigatie, helling, oppervlak, verbinding, geluid) van de zes genoemde modellen: 12 bronnen, plus het scoremodel. Winkel- en Bol-bronnen zijn overgeslagen.
- Niet gebruikt: de blokken "Sterkst bij" en "Alles over" van het hubpatroon. Daar is geen tekst voor.
- **Menu en footer** (live, tijdelijke aanpassingen): "Beste robotmaaiers" staat weer als eerste item in het menu, het mobiele menu en de footerkolom "Kiezen".
  - Zes items passen vanaf 1313 px op één regel; daaronder komt de menuknop (afwerkpakket).
- **Homepage** (#9): de eerste ingangskaart is nu "Beste robotmaaiers" naar `/beste-robotmaaier/`.
  - De korte tekst "Kies in vier stappen de robotmaaier die bij jouw tuin past." en de linktekst "Kies per situatie" heb ik afgeleid van de hubtekst.
  - De link naar `/robotmaaier-zonder-draad/` blijft in de hero-knop.
- **LANCERING.md:** 16 pagina's; de hub als nummer 15, vóór de homepage. Bijgewerkt: het aantal adressen, de sitemap en de URL-inspectie. De persmappen staan nu bij de voorbereiding.

### 4. Deelbeeld
- Voor alle pagina's het standaard deelbeeld van Claude Design: `deelafbeelding-1200x630-1.png`, de Yoast-instelling `og_default_image_id`.
- In 1.3.4 komt het als eerste in de Open Graph-beelden, en Yoast toont daarna alleen dat ene beeld. `twitter:image` is hetzelfde beeld.
- Lokaal gecontroleerd op de homepage, pagina 1, de methodepagina en de auteurspagina: één `og:image` (PNG 1200×630) en geen WebP of auteursfoto meer.
- **Pas zichtbaar met 1.3.4.**

### 5 en 6
- **LCP:** niet verder geoptimaliseerd (2,1–2,3 s lab), zoals besloten.
- **Kopbeelden:** blijven decoratief, met een lege alt-tekst.

### Gemeld, niet gewijzigd
De methodepagina (#76) noemt bij "Eindscore of functiescore" nog het label uit ronde 10: "Betrouwbaarheid en prijs-kwaliteit worden toegevoegd zodra er genoeg reviews en prijzen zijn." Sinds 1.3.2 is dat label "Functiescore: wat deze maaier kan." Pas ik aan als Mandy dat wil.

### Modellen voor de tweede golf (één per sessie; deze sessie: Segway Navimow)
- **Niet afgerond.** De bronnen zijn vanuit de bouwomgeving nog steeds niet bereikbaar: nl.navimow.com, navimow.segway.com, coolblue.nl, proshop.nl en mansier.com.
- Ik heb niets ingevuld, niets geschat en geen model als niet leverbaar gemarkeerd.
- **Alleen een aanwijzing uit de zoekmachine** (niet geopend, niet bevestigd voor Nederland): Navimow verkoopt in Europa de i2 AWD-reeks (i205, i206, i208, i209 AWD), de i2 LiDAR-reeks en de H2-reeks. De i105E is al M001 (volgens het Excel-bestand alleen nog refurbished bij Navimow NL).
- **Nodig:** zet de domeinen open (zie ronde 9), of vul de Excel-rijen in. Daarna doe ik Navimow, in een volgende sessie Husqvarna 105, 305 en 310 (met draad), en daarna Gardena Sileno Minimo 250 en 500 en City 250.
- Prijzen en persmappen staan in LANCERING.md als stap vóór de lancering. De huidige prijzen verlopen na 19 oktober.

### Tests
- `prijs-test.php`: **36 van 36** geslaagd, nu ook voor de analyse en dubbel vullen.
- Score- en Bol-tests: geslaagd.
- PHP-lint: in orde.
- De zip is 408 KB.

### Nog te doen
- [ ] Mandy: **1.3.4 uploaden en activeren.** Daarna controleer ik live de inhoudsopgave, de analyse, `og:image` en de hub.
- [ ] Mandy: de CDN-cache in hPanel legen. De CDN had `/wp-json/` nog bewaard; dat is nu ververst, maar een volledige CDN-leging is het zekerst.
- [ ] Mandy: de methodezin over het scorelabel (zie hierboven).
- [ ] Netwerktoegang of Excel-rijen voor de modellen van de tweede golf; prijzen verversen vóór 19 oktober.

## Ronde 13b (7 oktober 2026): opnieuw geprobeerd
- Live draait nog thema **1.3.3** (gezien in de openbare `style.css`). De live controle van 1.3.4 wacht dus nog op de upload.
- Navimow opnieuw geprobeerd: navimow.com, segway.com, husqvarna.com, gardena.com en coolblue.nl zijn nog steeds **geblokkeerd** door het netwerkbeleid van de bouwomgeving. Er is niets ingevoerd en niets als niet leverbaar gemarkeerd.
- Nodig: deze domeinen toevoegen onder *Allowed domains* in de netwerkinstellingen van de omgeving, of de Excel-rijen zelf invullen.

## Ronde 15 (7 oktober 2026): mesjespagina, methodezin en links
**Live is nog niets gewijzigd.** In deze sessie staat het wachtwoord niet in de omgevingsvariabele `RMK_WP_APP_PASSWORD`, en het direct gebruiken ervan in een opdracht werd door de beveiliging van de sessie geweigerd. Alles is lokaal gebouwd en getest. Het uploadscript staat klaar in de repo.

### Klaargezet
1. **Methodepagina (#76):** de labelzin wordt "Een functiescore laat zien wat een maaier kan. Betrouwbaarheid en prijs-kwaliteit voegen we toe zodra er genoeg reviews en prijzen zijn." De oude zin kwam lokaal één keer voor, alleen op deze pagina.
2. **Nieuwe conceptpagina `robotmaaier-mesjes`** uit `pagina-robotmaaier-mesjes.md`, met het patroon pagina-kopersgids:
   - kruimelpad, eerlijkheidsblok ("Gebaseerd op handleidingen en fabrikantpagina's, bijgewerkt op 7 oktober 2026. We testen de maaiers niet zelf."), inhoudsopgave in de eigen kolom, tabel, vier FAQ's, "Wat we nog niet weten", bronnen en auteursblok;
   - metabeschrijving uit het md-bestand, kruimelpadtitel "Robotmaaier mesjes";
   - interne links: /robotmaaier-kosten/ ("Zie robotmaaier kosten"), /robotmaaier-test-vergelijking/ (op "de modellen die wij bekeken" in het korte antwoord), /hoe-we-beoordelen/ (eerlijkheidsblok). /beste-robotmaaier/ zit alleen in menu en footer: er staat in de tekst geen passende zin voor, en ik heb er geen bijgeschreven.
   - **Bronnen** uit het blad Bronnen van het Excel-bestand: per merk de fabrikantpagina (prijs) en de handleiding (vervangtermijn), plus Stiftung Warentest (test.de/maehroboter, al gebruikt op pagina 4). Geen winkels, geen Bol.
3. **Kostenpagina (#18), onder Messen:** "Hoe vaak je de mesjes vervangt en wat ze per merk kosten, lees je op de pagina robotmaaier mesjes."
4. **Hub (#10), bij Onderhoud en messen:** "Prijzen en vervangtermijnen per merk staan op de pagina robotmaaier mesjes."
5. **LANCERING.md:** 17 pagina's, de mesjespagina als nummer 11 direct na de kostenpagina; tellingen, URL-inspectie en de stap prijzen verversen (ook de messenprijzen) bijgewerkt.

### Gecontroleerd (lokaal, Chromium, 390, 768, 1024 en 1440 px)
- Op de vier pagina's geen `[`, `{{`, "Alfa", "Beta" of "gepeild" in de tekst; één h1; geen horizontale scroll; geen scriptfouten.
- Inhoudsopgave mesjespagina: niet sticky tot 1024 px, sticky in de eigen kolom op 1440 px, nergens over de tekst.
- Ankerlinks in de inhoudsopgave werken. De interne links in de inhoud geven allemaal 200. Alleen de footerlinks naar privacy, cookies, contact, colofon en affiliate-melding geven lokaal 404, omdat die pagina's alleen live bestaan.
- De jaarbedragen in de tabel nagerekend: Mova 24 tot 33, Dreame 32 tot 43, Eufy 27 tot 53 euro. Klopt.

### Om op te letten
- **Navimow "ongeveer 25 euro voor 12":** de fabrikantpagina noemt volgens het Excel-bestand 25 euro zonder aantal; het aantal 12 komt van een winkelpagina (Coolblue). De tekst staat zo ook al op de kostenpagina. Ik heb hem niet veranderd. Wil je "voor 12" laten staan?
- **Kostenpagina, bronnenlijst:** een paar fabrikantpagina's (Navimow, Husqvarna, Eufy en Dreame messen) hebben daar het label "Handleiding" in plaats van "Fabrikant". Op de mesjespagina staat het goed. Niet veranderd; zeg het als ik het op de kostenpagina moet rechtzetten.

### Uploaden (volgende sessie, als `RMK_WP_APP_PASSWORD` in de omgeving staat)
`python3 scripts/ronde15_upload.py` (proefdraai) en daarna met `--schrijf`. Het script past de drie zinnen alleen aan als de oude tekst precies één keer voorkomt, maakt de mesjespagina als **concept**, en controleert daarna live de interne links en de invulvelden.

### Nog te doen
- [ ] Mandy: het wachtwoord als geheim `RMK_WP_APP_PASSWORD` in de omgeving zetten (nieuwe sessie nodig), daarna upload ik ronde 15.
- [ ] Mandy: 1.3.4 uploaden en activeren (live draait 1.3.3).
- [ ] Mandy: de Navimow-zin "voor 12" bevestigen.

## Ronde 16 (7 oktober 2026): hub beste-robotmaaier, versie 2
Op verzoek geen upload: lokaal gebouwd en getest. De inhoud staat in `scripts/ronde16/hub.json`, als concept, met de metabeschrijving uit het md-bestand en de kruimelpadtitel "Beste robotmaaiers".

### Gebouwd
- Inhoud uit `pagina-3-beste-robotmaaier-v2.md`, patroon pagina-hub. Titel: "Beste robotmaaier (2026): onze selectie per situatie".
- **Vijf productkaarten** in deze volgorde: M002, M010, M005, M008, M011. Ze gebruiken hetzelfde skelet als op /robotmaaier-zonder-draad/. Het thema vult de specificatiekaart, "Beste voor", de analyse, de plus- en minpunten, de functiescore en de prijsregel (laagste nieuwe prijs met winkel en datum). De zin "Waarom deze" staat steeds onder de kaart.
- **Functiescores** uit de tabel "In een oogopslag" nagerekend met de scorecode van het thema: 92,7 / 87,3 / 80,5 / 78,6 / 60,9. Ze kloppen. De modelnamen in die tabel linken naar hun kaart op dezelfde pagina.
- **Links:** naar /hoe-we-beoordelen/#scoremodel, /robotmaaier-zonder-draad/, /robotmaaier-test-vergelijking/, /robotmaaier-zonder-grensdraad/, /robotmaaier-kosten/, /robotmaaier-mesjes/ en /robotmaaier-test-consumentenbond/ (Meer lezen), plus #keuzehulp en de selectie (FAQ).
- De zin met de link naar de mesjespagina bij "Onderhoud en messen" (ronde 15) is erin gehouden. Het uploadscript van ronde 15 ziet hem dan als "al aangepast".
- **Bronnen** per model (vijf groepen) uit het blad Bronnen:
  - één regel per bron, met de velden zonder dubbele regels voor dezelfde bron en hetzelfde veld;
  - de domeinnaam staat erbij, en bij één regel in het Excel-bestand met meerdere URL's ook het pad;
  - labels: Handleiding, Fabrikant of Appwinkel;
  - 33 regels; overgeslagen: 43 regels van winkels, winkelclaims, "niet gevonden" en "niet geopend", plus de Bol-regels;
  - prijzen staan met winkel en datum in de kaart;
  - daarna het scoremodel als eigen methode.

### Gecontroleerd (lokaal, 390, 768, 1024 en 1440 px)
- Vijf kaarten compleet: specificatiekaart, Beste voor, analyse, plus- en minpunten, score en prijsregel.
- Geen `[`, `{{` of invulveld. Geen Bol en geen affiliatelinks (`/ga/` of sponsored). Eén h1, geen horizontale scroll, geen scriptfouten.
- Ankerlinks werken. Alle interne links in de inhoud geven 200. Alleen de footerlinks naar de juridische pagina's geven lokaal 404, omdat die pagina's alleen live bestaan.
- Menu en footer: "Beste robotmaaiers" wijst naar /beste-robotmaaier/. De eerste ingangskaart op de homepage wijst naar /beste-robotmaaier/ (zelfde inhoud als live sinds ronde 13).

### Om op te letten
- /robotmaaier-mesjes/ bestaat live pas na de upload van ronde 15. Upload ronde 15 dus vóór of samen met deze hub.
- De prijsknoppen in de kaarten ("Bekijk bij Coolblue" en andere) zijn gewone links naar de winkel of fabrikant, net als op pagina 1, en geen affiliatelinks. De prijzen zijn van 5 oktober en verdwijnen na 19 oktober vanzelf uit de kaart.
- Bij Husqvarna staat in "Waarom deze" "rond 3.000 euro"; de prijsregel in de kaart zegt "rond 3.049 euro". Niet veranderd.

### Nog te doen
- [ ] Upload van ronde 15 en ronde 16 zodra `RMK_WP_APP_PASSWORD` in de omgeving staat (op jouw teken).

## Ronde 17 (7 oktober 2026): upload ronde 15 en 16, niet gelukt
**Het wachtwoord werkte niet, want het was in deze sessie niet beschikbaar.** De omgevingsvariabele `RMK_WP_APP_PASSWORD` is hier leeg; er is geen variabele met die naam of een vergelijkbare naam. Er was geen melding van de beveiliging: het script stopte zelf met "RMK_WP_APP_PASSWORD ontbreekt in de omgeving." De proxy voegt ook geen inloggegevens toe: een verzoek zonder login naar `/wp-json/wp/v2/users/me` gaf 401 "Je bent momenteel niet ingelogd". Een geheim dat je in de omgeving zet, geldt pas voor een **nieuwe sessie**. Deze sessie liep al.

Daarom is **live niets gewijzigd**: geen nieuwe pagina, geen tekstwijziging.

### Wel gedaan
- **Hubtekst:** "rond 3.000 euro" is "ruim 3.000 euro" geworden in `scripts/ronde16/hub.json`, alleen in de zin "Waarom deze" bij Husqvarna. De prijsregel in de kaart blijft "rond 3.049 euro bij Husqvarna" (lokaal gecontroleerd).
- **`scripts/ronde16_upload.py`:** werkt de hub (#10) alleen bij als die een concept is. Daarna controleert het live: de vijf kaarten in de juiste volgorde, zes brongroepen (vijf modellen en de eigen methode), geen invulvelden, geen Bol en geen affiliatelinks.
- **Controle zonder inloggen (live):**
  - `/wp-json/rmk/v1`, `/status` en `/modellen` geven 401 "Alleen voor beheerders.";
  - `/wp-json/wp/v2/pages/10` geeft 401; zoeken op de slugs beste-robotmaaier en robotmaaier-mesjes geeft een lege lijst; `status=draft` is verboden (400);
  - `/beste-robotmaaier/`, `/robotmaaier-mesjes/` en `/?page_id=10` (ook met preview) geven 404;
  - `/wp-content/uploads/rmk/` geeft 403. De sitemap bevat alleen `/`. robots.txt blokkeert `/wp-json/rmk/` en `/wp-content/uploads/rmk/`.
  - Het themabestand `data/modellen.json` is openbaar leesbaar (200). Het bevat dezelfde gegevens als de pagina's (specificaties, scores, teksten en prijzen met winkel), geen Bol-gegevens, en de EAN-velden zijn leeg. Dat was al zo; niet veranderd.

### Volgende sessie (met het geheim actief)
1. `python3 scripts/ronde15_upload.py`, daarna met `--schrijf`
2. `python3 scripts/ronde16_upload.py`, daarna met `--schrijf`
3. Daarna live controleren zoals gevraagd in ronde 17 (concepten ingelogd bekijken, links, bronnen, en opnieuw de controle zonder inloggen).

### Nog te doen
- [ ] Een nieuwe sessie starten, zodat het geheim `RMK_WP_APP_PASSWORD` geladen is; dan upload en controle van ronde 15 en 16.

## Ronde 18 (7 oktober 2026): upload ronde 15 en 16 gelukt
Het geheim `RMK_WP_APP_PASSWORD` stond in deze sessie in de omgeving; inloggen werkte. **Niets gepubliceerd**: alle pagina's zijn concept gebleven.

### Gedaan
1. `scripts/ronde15_upload.py` (proefdraai, daarna `--schrijf`):
   - tekstwijzigingen op hoe-we-beoordelen (#76), robotmaaier-kosten (#18) en beste-robotmaaier (#10); alle drie bleven concept;
   - nieuwe conceptpagina **robotmaaier-mesjes, id 236**.
   - Controle van het script: op alle vier de pagina's ontbreekt geen interne link en staan geen invulvelden.
2. `scripts/ronde16_upload.py` (proefdraai, daarna `--schrijf`): hub #10 bijgewerkt naar versie 2, status concept.
   - Controle van het script: kaarten M002, M010, M005, M008, M011 in die volgorde, 6 brongroepen, geen invulvelden, geen Bol, geen affiliatelinks.

### Live gecontroleerd (ingelogd, via de REST-API)
- **Hub (#10), weergegeven inhoud:** vijf productkaarten in de juiste volgorde (Navimow i206 AWD, Husqvarna 410VE NERA, Mova LiDAX Ultra 1200, Dreame A1 Pro, Gardena Sileno Free 800), elk met specificatiekaart, Beste voor, pluspunten en prijsregel. Bronnen per model: 6, 7, 8, 8 en 4 regels, daarna "Scoremodel v1.0" als eigen methode. Geen invulvelden, geen bol.com, geen `/ga/` of sponsored. De zin met de link naar /robotmaaier-mesjes/ staat erin.
- **Interne links hub:** /, /hoe-we-beoordelen/, /over-ons/mandy-van-den-broek/, /robotmaaier-kosten/, /robotmaaier-mesjes/, /robotmaaier-test-consumentenbond/, /robotmaaier-test-vergelijking/, /robotmaaier-zonder-draad/, /robotmaaier-zonder-grensdraad/. Ze bestaan allemaal (als concept).
- **Mesjespagina (#236):** concept, 11 bronregels, geen invulvelden, geen Bol, geen affiliatelinks; links naar /, /hoe-we-beoordelen/, /over-ons/mandy-van-den-broek/, /robotmaaier-kosten/ en /robotmaaier-test-vergelijking/.

### Live gecontroleerd zonder inloggen
- /beste-robotmaaier/, /robotmaaier-mesjes/, /?page_id=10, /?page_id=236 (ook met preview): 404.
- /wp-json/wp/v2/pages/10 en /236: 401. Zoeken op de slugs en `/wp-json/wp/v2/search?search=mesjes`: lege lijst. `status=draft`: 400. `/?s=mesjes`, `/page-sitemap.xml` en `/feed/` tonen niets van de concepten.
- /wp-json/rmk/v1: 401 "Alleen voor beheerders.".

### Nog te doen
- [ ] Mandy: 1.3.4 uploaden en activeren (live draait 1.3.3, laatst gezien in ronde 13b).
- [ ] Mandy: de Navimow-zin "voor 12" bevestigen (ronde 15).
- [ ] Publiceren volgens LANCERING.md, op jouw teken; de mesjespagina heeft nu id 236.

## Ronde 19 (7 oktober 2026): 1.3.4 live, Navimow-messen, bronlabels kostenpagina
**Niets gepubliceerd**: alle gewijzigde pagina's zijn concept gebleven.

### 1. Themaversie
- **Live draait 1.3.4.** De pagina's laden de themabestanden met `?ver=1.3.4`, en `style.css?ver=1.3.4` meldt "Version: 1.3.4". De ingebouwde CSS bevat de regels van 1.3.4 (75rem-kolom, `rmk-analyse`).
- **Kanttekening:** het kale adres `/wp-content/themes/robotmaaierkompas-child/style.css` (zonder `?ver=`) gaf nog "Version: 1.3.3". Dat komt uit de CDN-cache: `x-hcdn-cache-status: HIT` en een `last-modified` van vóór de upload, met `max-age` van 7 dagen. Het is een cacheprobleem zonder gevolgen voor bezoekers, want de site gebruikt dat adres niet. Niet veranderd; een volledige leging van de CDN-cache in hPanel ruimt het op.

### 2. Tekstwijzigingen (`scripts/ronde19_upload.py`, proefdraai en daarna `--schrijf`)
- **Navimow-messen** is nu "ongeveer 25 euro per verpakking (het aantal messen is niet bevestigd)":
  - in de tabel op de mesjespagina (#236; was "ongeveer 25 euro voor 12");
  - in de tabel op de kostenpagina (#18; was "ongeveer 25 euro voor 12 stuks").
  - Na afloop staat de nieuwe zin op beide pagina's één keer en is de oude tekst weg. De lokale kopie `scripts/ronde15/mesjes.json` is ook bijgewerkt.
- **Bronlabels op de kostenpagina (#18):** "Handleiding" staat alleen nog bij pdf's en het documentarchief van Husqvarna (`/tdrdownload/`). Tien fabrikantpagina's kregen "Fabrikant":
  - Navimow Access+ en Blade Assembly Plus;
  - Husqvarna EPOS RS1 en Endurance-messen;
  - Gardena Sileno Free 800;
  - Eufy 4G-FAQ (service.eufy.com) en messen;
  - Dreame: link-module 1 jaar, link-module 3 jaar en messen.
  - Ongewijzigd: "Handleiding (kopie op mansier.com)" en "Eigen methode".
- De labels op de mesjespagina klopten al.

### 3. Live gecontroleerd, ingelogd
Gebruikt: de weergegeven inhoud uit de REST-API (`context=edit`), en voor de opmaak die inhoud in Chromium in de live 1.3.4-pagina gezet (de concepten zijn niet als voorbeeld te openen met een toepassingswachtwoord).
- **Inhoudsopgave/filters** op de methodepagina (#76), pagina 4 (#13), pagina 11 (#17), de mesjespagina (#236) en pagina 2 (#12), op 390, 768, 1024 en 1440 px:
  - tot en met 1024 px `static`, op 1440 px `sticky` in de eigen kolom;
  - tijdens het scrollen nergens over de tekst (0 overlap);
  - geen scriptfouten.
- **Bevinding, niet gewijzigd:** de methodepagina scrolt op 390 px horizontaal (ongeveer 25 px).
  - De scoremodeltabel is 415 px breed; de kolom is 351 px.
  - Oorzaak: `section.rmk-prose` heeft in de flexkolom `.rmk-split__main` `min-width: auto`. Daardoor groeit het blok mee met de tabel, in plaats van dat de tabel in haar eigen scrollvak (`.rmk-tablewrap`) blijft.
  - Mogelijke oplossing in het thema: `.rmk-split__main > * { min-width: 0; }`.
  - De andere vier pagina's scrollen niet horizontaal.
- **Analyse in de kaart:** op de hub (#10) 5 van 5 kaarten en op pagina 1 (#11) 8 van 8 kaarten, steeds vóór de plus- en minpunten.
- **Deelbeeld:**
  - op 10 pagina's (9, 10, 11, 12, 13, 17, 18, 76, 78, 236) precies één `og:image`, namelijk `deelafbeelding-1200x630-1.png`;
  - `twitter:image` is hetzelfde beeld;
  - het bestand zelf geeft 200 `image/png`, 1200 × 630.

### 4. Live gecontroleerd zonder inloggen
- /beste-robotmaaier/, /robotmaaier-mesjes/, /robotmaaier-kosten/, /hoe-we-beoordelen/, `?page_id=18` en `?page_id=236&preview=true`: 404.
- /wp-json/wp/v2/pages/18 en /236: 401. Zoeken op de slug of op "verpakking" in de REST-API: lege lijst.
- `/?s=verpakking`: geen resultaten (alleen de vaste menu- en footerlinks).
- `page-sitemap.xml` en `/feed/`: niets van de concepten.
- /wp-json/rmk/v1 en /status: 401.

### Nog te doen
- [ ] Mandy: CDN-cache in hPanel volledig legen (kale `style.css` nog 1.3.3).
- [ ] Mandy: beslissen of de tabeloverloop op de methodepagina (390 px) in het thema opgelost moet worden.
- [ ] Prijzen verversen vóór 19 oktober; publiceren volgens LANCERING.md op jouw teken.
