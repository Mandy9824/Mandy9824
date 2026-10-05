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
