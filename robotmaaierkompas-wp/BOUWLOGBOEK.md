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

## Ronde 20 (7 oktober 2026): tabeloverloop via aanvullende CSS, paginatekst eerste golf
**Niets gepubliceerd**: alle pagina's zijn concept gebleven. Geen nieuwe thema-zip.

### 1. Aanvullende CSS (Global Styles, gebruikersstijlen #8 van robotmaaierkompas-child)
- Vooraf was `styles` leeg; er is geen bestaande CSS overschreven. De instellingen (`settings`) zijn ongewijzigd.
- **De gevraagde regel alleen was niet genoeg.** Live met `.rmk-split__main > * { min-width: 0; }` bleef de methodepagina op 390 px 434 px breed.
- **Echte oorzaak:**
  - `.rmk-prose { margin-inline: auto; }`: in een flexkolom laten automatische marges het blok niet uitrekken. Het wordt zo breed als de minimale breedte van de tabel (413 px).
  - `.rmk-column .rmk-prose { max-width: none; }` heft een algemene `max-width` op.
  - De aanvullende CSS staat in de pagina vóór de themastijl (`global-styles-inline-css` vóór `rmk-inline-css`). Bij gelijke specificiteit wint dus het thema; daarom is de selector één klasse specifieker gemaakt.
- **Opgeslagen CSS:**
  ```css
  .rmk-split__main > * { min-width: 0; }
  .rmk-split > .rmk-split__main > .rmk-prose { min-width: 0; max-width: 100%; }
  ```
- **Live gecontroleerd** (concepttekst in de live pagina, Chromium, net als in ronde 19):
  - methodepagina op 390 px: de pagina is 390 px breed, scrolt niet meer zijwaarts, en de scoremodeltabel scrolt in haar eigen vak (349 van 413 px);
  - op 768, 1024 en 1440 px geen zijwaarts scrollen;
  - pagina 2, 4 en 11 en de mesjespagina op 390 px ook niet.
- **Vergelijking vóór en na** (zelfde regel ingevoegd in de browser): de breedte en positie van alle blokken in `.rmk-split__main` en alle tabelvakken zijn gemeten op 8 pagina's × 4 breedtes. Alleen de methodepagina op 390 px veranderde.
- **In de volgende themaversie (1.3.5) opnemen** in `rmk.css`, bij de regels voor de inhoudsopgave:
  ```css
  .rmk-split__main > * { min-width: 0; }
  .rmk-split__main > .rmk-prose { max-width: 100%; }
  ```
  Haal daarna de aanvullende CSS weer weg (Weergave > Editor > Stijlen > Aanvullende CSS).

### 2. Paginatekst eerste golf
- `paginatekst-eerste-golf.md` is gemaakt uit de weergegeven inhoud van de 17 conceptpagina's (volgorde van LANCERING.md). Per pagina staan erin:
  - titel, adres (slug), metabeschrijving en het aantal H1's;
  - de volledige tekst als gewone tekst;
  - de bronnenlijst met URL;
  - de interne links met doeladres.
- Het bestand bevat geen HTML. Het staat **niet in de repository en niet op de site**; het is alleen in de sessie aan Mandy gegeven.
- **Uitkomst:**
  - alle 17 pagina's hebben precies één H1;
  - de header en footer van het thema voegen geen H1 toe.
- **Opvallend:**
  - De zes juridische en contactpagina's hebben **geen metabeschrijving**: privacy, cookies, affiliate-melding, redactiebeleid, colofon en contact.
  - De homepage heeft geen kruimelpadtitel. Dat is normaal voor een voorpagina.
  - Mesjespagina: na de wijziging van ronde 19 staat er onder de tabel nog: "Dat ligt in dezelfde orde van grootte als wat wij zien voor een verpakking van 12, maar het hangt af van het aantal messen per verpakking." Niet veranderd; zeg het als die zin aangepast moet worden.

### Nog te doen
- [ ] Thema 1.3.5: de CSS-regels hierboven in `rmk.css`, daarna de aanvullende CSS verwijderen.
- [ ] Mandy: metabeschrijvingen voor de zes juridische pagina's (of bewust leeg laten).
- [ ] Mandy: de zin "een verpakking van 12" op de mesjespagina.
- [ ] CDN-cache volledig legen; prijzen verversen vóór 19 oktober; publiceren op jouw teken.

## Ronde 21 (8 oktober 2026): tekstwijzigingen na controle 1
Uitgevoerd volgens `tekstwijzigingen-controle1.md` (secties A tot en met D), met `scripts/ronde21_upload.py` (proefdraai, daarna `--schrijf`). Geen nieuwe thema-zip.
**Niets gepubliceerd**: alle 77 pagina's zijn concept, er zijn 0 gepubliceerde berichten.

### Toegepast (elke "Was"-tekst kwam precies één keer voor)
- **A1** Affiliate-melding (#81): eerste alinea vervangen; de tweede alinea ("Dat verandert de score of de volgorde niet...") staat er nog.
- **A2** Over ons (#77): nieuwe zin met een link naar /affiliate-melding/. Die link was er eerder niet, dus hij zit nu in de nieuwe zin. De links naar /hoe-we-beoordelen/#verdienmodel en /hoe-we-beoordelen/ uit de oude zin zijn weg, zoals de nieuwe tekst voorschrijft.
- **A3** Colofon (#80) en **A4** Hoe we beoordelen (#76, "Zo verdienen we geld"): vervangen, met de link naar de affiliate-melding.
- **A5** Footer: de aangepaste footer in de site-editor (template part `robotmaaierkompas-child//footer`) is vervangen; geldt op alle pagina's.
- **A6** "Advertentie: via deze knoppen krijgen wij mogelijk een commissie...":
  - **Homepage (#9):** het blok met het patroon `robotmaaierkompas/affiliate-melding` is uit de inhoud gehaald. Terugzetten: in de editor het patroon "RMK – Affiliate-melding" weer onder het auteursblok zetten.
  - **Overal:** in de aanvullende CSS staat nu `.rmk-affnote { display: none !important; }`. Dat geldt ook voor #26 husqvarna-vs-gardena (tweede golf), die de regel los in de inhoud heeft. Daar staat de zin nog wel in de HTML, maar hij is verborgen.
  - Weghalen zodra de affiliateprogramma's zijn goedgekeurd.
- **B7** Husqvarna:
  - **Hub:** "ruim 3.000 euro" is "boven de 3.000 euro" geworden.
  - **Modelgegevens M010** (analyse en minpunt): bijgewerkt via de dataroute `rmk/v1/modellen`. Ik heb de live gegevens opgehaald en alleen die twee velden veranderd; het Excel-bestand staat niet in de repository. Ook lokaal bijgewerkt: `scripts/modellen_analyse.json`, `scripts/modellen_teksten.json` en het themabestand `data/modellen.json`.
  - De nieuwe analyse en het nieuwe minpunt staan in de kaarten op pagina 1 (#11) en op de hub (#10).
- **B8** en **B9** mesjespagina (#236): het eerlijkheidsblok heeft dezelfde opmaak als op de hub (vet deel met de link naar /hoe-we-beoordelen/), en de zin onder de tabel is vervangen.
- **C** Metabeschrijvingen: alle 17 gezet in Yoast (`_yoast_wpseo_metadesc`), tussen 62 en 136 tekens. Live gecontroleerd in `yoast_head_json`.
- **D** "Laatst nagekeken op":
  - Dit was al automatisch: het auteursblok vult de datum van de laatste wijziging van de pagina in.
  - Na deze ronde staat op alle pagina's met een auteursblok "8 oktober 2026". Bij het publiceren wordt dat de publicatiedag, overal gelijk.
  - Niet automatisch zijn de vaste datums in de paginakop en het eerlijkheidsblok ("bijgewerkt op 5 oktober 2026" of "7 oktober 2026"). Die stonden niet in de lijst en zijn niet veranderd.

### Gemeld, niet veranderd
- **Kostenpagina (#18):** "…en de Husqvarna Automower 410VE NERA rond de 3.000 euro". Andere woorden, niet in de lijst.
- **Het openbare themabestand** `/wp-content/themes/.../data/modellen.json` (reserve uit de zip van 1.3.4) bevat nog "rond 3.000 euro". De site gebruikt de opgeslagen gegevens uit de database; het lokale themabestand is bijgewerkt en gaat mee in 1.3.5.

### Live gecontroleerd
- **Ingelogd, 17 pagina's:**
  - de nieuwe teksten staan op de juiste pagina's;
  - "commissie", "Advertentie", "rond 3.000 euro", "ruim 3.000", "voor een verpakking van 12" en "We testen de maaiers niet zelf" komen nergens meer voor, ook niet in de footer of de header.
- **Zonder inloggen:**
  - de openbare footer toont de nieuwe zin, zonder "commissie" of "Advertentie";
  - de conceptadressen en `?page_id=` (ook met preview) geven 404;
  - de REST-API geeft 401 of een lege lijst, en `rmk/v1/modellen` geeft 401;
  - de zoekfunctie, `page-sitemap.xml` en de feed tonen niets van de concepten.
- **Nieuw bestand `paginatekst-eerste-golf.md`** (versie 8 oktober): alleen in de sessie aan Mandy gegeven, niet in de repository en niet op de site. Het bevat geen HTML en geen "commissie", en alle 17 pagina's hebben een metabeschrijving en één H1.

### Nog te doen
- [ ] Bij goedkeuring van de affiliateprogramma's: de oorspronkelijke zinnen terugzetten (oude teksten in `scripts/ronde21_upload.py`), het patroon op de homepage terugzetten en de CSS-regel `.rmk-affnote` weghalen.
- [ ] Thema 1.3.5: de CSS-regels van ronde 20 en het bijgewerkte `data/modellen.json`.
- [ ] Beslissen over "rond de 3.000 euro" op de kostenpagina en over de vaste datums in paginakop en eerlijkheidsblok.
- [ ] CDN-cache legen; prijzen verversen vóór 19 oktober; publiceren op jouw teken.

## Ronde 22 (8 oktober 2026): kostenpagina, modelgegevens, thema 1.3.5
**Niets gepubliceerd**: alle 77 pagina's zijn concept, er zijn 0 gepubliceerde berichten. Live draait nog **1.3.4**; **1.3.5 is gebouwd en getest; Mandy moet het nog uploaden.**

### 1. Kostenpagina (#18)
- "…en de Husqvarna Automower 410VE NERA rond de 3.000 euro" is "…boven de 3.000 euro" geworden. De pagina is concept gebleven.
- "rond de 3.000 euro" kwam verder nergens voor: niet in de andere 76 pagina's, de modelgegevens of de template parts.

### 2. Modelgegevens met nieuwe prijzen: niet gedaan
- **Het nieuwste `robotmaaierkompas_modeldata_v1.xlsx` staat niet in deze sessie.** In de uploadmap staat alleen `tekstwijzigingen-controle1.md`, en op de schijf staat geen xlsx.
- In Google Drive staat alleen een spreadsheet `robotmaaierkompas_modeldata_v1` van 5 oktober. Die is ouder dan de live gegevens (gegenereerd op 7 oktober), dus niet gebruikt.
- **Live is niets geüpload.** De tabellen en kaarten zijn dus niet veranderd: de prijzen zijn nog die van 5 oktober.
- **Wel gecontroleerd op de live modelgegevens**, met `tests/prijs-modellen-test.php`, de echte prijsfuncties uit `inc/prijzen.php`, op 8, 19 en 20 oktober:
  - tot en met 19 oktober tonen de kaarten de prijs met winkel en datum; vanaf 20 oktober (meer dan 14 dagen oud) is de prijs weg;
  - modellen zonder geldige prijs tonen alleen "Bekijk de actuele prijs" naar de fabrikantpagina;
  - er staan geen Bol-prijzen in de gegevens, en een Bol-winkel of -URL wordt geweigerd (code en eerdere tests).
- **Gevonden:** M002 (Navimow i206 AWD) heeft geen `fabrikant_url`. Vanaf 20 oktober toont die kaart daarom **niets** (geen prijs en geen knop). Het adres van de fabrikantpagina moet in het Excel-bestand; ik heb het niet zelf ingevuld.
- **M003 (Navimow i210 LiDAR)** staat in geen van de 17 pagina's:
  - de scoretabel op pagina 1 noemt de acht modellen expliciet;
  - de calculator op de kostenpagina is beperkt tot `data-models="M001,M002,M004,M005,M006,M008,M010,M011"`;
  - de keuzehulp toont geen modellen.
  - M003 staat wel in het modelbestand, zonder prijs.

### 3. Thema 1.3.5 (`robotmaaierkompas-child.zip`, 412 KB, versie 1.3.5)
- **(a) Tabellen naast de inhoudsopgave:** in `css/rmk-afwerking.css`, direct na `.rmk-column .rmk-prose`:
  `.rmk-split__main > * { min-width: 0; }` en `.rmk-split__main > .rmk-prose { max-width: 100%; }`.
  - Extra, gevonden bij het testen: `h1 { overflow-wrap: break-word; }`. Op Over ons paste "robotmaaierkompas.nl" in de H1 op 390 px niet, en de pagina scrolde 15 px zijwaarts (ook in 1.3.4). Nu breekt het woord af ("robotmaaierkompas / .nl").
- **(b) `data/modellen.json`:** bevat al dezelfde gegevens als live, inclusief de M010-tekst uit ronde 21. De enige verschillen zijn notatie van PHP (`1.0` tegenover `1`). Nieuwe prijzen volgen met het nieuwe Excel-bestand.
- **(c) Automatische datums:** in het nieuwe bestand `inc/redactie.php`.
  - De datum in de paginakop (`p.rmk-meta`: "bijgewerkt op …", op privacy "Laatst bijgewerkt: …") en in het eerlijkheidsblok ("Bijgewerkt op …") wordt bij het renderen de datum van de laatste wijziging van de pagina, als `<time datetime>`.
  - Andere datums blijven staan: per model in de tabel op pagina 2 en "gezien op" bij prijzen.
- **(d) `RMK_AFFILIATE_ACTIVE`** (in wp-config.php, standaard uit):
  - zolang de instelling uit staat, haalt het thema elke `<p class="rmk-affnote">` uit de uitvoer: uit het patroon affiliate-melding en uit losse kopieën, zoals in #26;
  - met `define( 'RMK_AFFILIATE_ACTIVE', true );` komt de regel terug;
  - het statusoverzicht (Gereedschap > Robotmaaierkompas) toont de stand.
  - De CSS-truc `.rmk-affnote { display: none }` is in het thema niet meer nodig.
- **Aanvullende CSS:** blijft staan tot 1.3.5 live actief is; anders komen de tabeloverloop en de regel op #26 tijdelijk terug.
  - `scripts/ronde22_na_upload.py` controleert eerst of 1.3.5 actief is, en haalt dan de blokken van ronde 20 en 21 weg.
  - Op de huidige CSS getest: daarna is de aanvullende CSS leeg.
- Versie in `style.css` en `RMK_VER`: 1.3.5. PHP-lint: geen fouten.

### 4. Tests
- **Lokale WordPress-testsite:** opgezet met WordPress 7.1.3 en SQLite van GitHub (wordpress.org is geblokkeerd). Het overzetten van de live inhoud werd geweigerd door de beveiliging van de sessie (gedownloade code draaien). Daarom zonder WordPress getest:
  - `tests/redactie-test.php`: datums en affiliate-melding op de echte inhoud van de 17 pagina's en #26, met de instelling uit en aan. Alles geslaagd.
  - `tests/prijs-modellen-test.php`: zie hierboven.
- **Browsertest** (Chromium):
  - Opzet: de live paginaskelet met header en footer, de weergegeven conceptinhoud en de CSS van 1.3.4 en 1.3.5, zonder de aanvullende CSS.
  - 17 pagina's, op 390, 768, 1024 en 1440 px.
  - **1.3.5:** geen zijwaarts scrollen, één H1, inhoudsopgave `static` tot en met 1024 px en `sticky` op 1440 px, 0 overlap, geen scriptfouten, de regel "Advertentie" nergens zichtbaar.
  - **Verschil met 1.3.4:** alleen de methodepagina op 390 px, die nu 390 px breed is (was 439 px), en de afbreking van de H1 op Over ons.
- **LCP** (labmeting):
  - Opzet: dezelfde statische kopie, mobiel profiel Moto G4, 150 ms latency, 1,6 Mbit/s, processor 4× trager, mediaan van 3 metingen.

  | Pagina | 1.3.4 | 1.3.5 | LCP-element |
  |---|---|---|---|
  | Homepage | 0,76 s | 0,76 s | `p.rmk-lead` |
  | Pagina 1 (zonder draad) | 0,76 s | 0,76 s | H1 |
  | Pagina 12 (kosten) | 0,76 s | 0,76 s | H1 |

  - 1.3.5 maakt de LCP niet trager. De waarden zijn lager dan de eerdere PageSpeed-metingen (2,1–2,3 s), omdat de HTML hier lokaal komt en de server- en cachetijd van Hostinger niet meetelt.
  - Na de lancering opnieuw meten met PageSpeed Insights.
- **Storing:** tijdens deze ronde gaf de live site ongeveer een kwartier 307, 502 en 504, ook voor gewone afbeeldingen (CDN of hosting). Daarna werkte alles weer. In die tijd is er niets naar de site geschreven.

### Live gecontroleerd (na de storing)
- 77 pagina's, allemaal concept; 0 gepubliceerde berichten; actief thema 1.3.4.
- Zonder inloggen: /robotmaaier-kosten/ en `?page_id=18` geven 404; de REST-API (`pages/18`, `rmk/v1/modellen`) geeft 401.

### Nog te doen
- [ ] Mandy: het nieuwste `robotmaaierkompas_modeldata_v1.xlsx` in de sessie zetten (bijlage). Daarna upload ik de nieuwe prijzen en meld ik oud en nieuw per tabel en kaart.
- [ ] Mandy: in het Excel-bestand de fabrikantpagina (`fabrikant_url`) van M002 Navimow i206 AWD invullen.
- [ ] Mandy: 1.3.5 uploaden en activeren; daarna draai ik `scripts/ronde22_na_upload.py --schrijf` en controleer ik live.
- [ ] Mandy: wil je op Over ons een nettere afbreking ("robotmaaier / kompas.nl")? Dat kan met een `<wbr>` in de H1 (tekstwijziging).
- [ ] Prijzen verversen vóór 19 oktober; publiceren op jouw teken.

## Ronde 23 (8 oktober 2026): 1.3.5 live, aanvullende CSS weg, Over ons, LANCERING.md
**Niets gepubliceerd**: alle 77 pagina's zijn concept, er zijn 0 gepubliceerde berichten.

### 1. Thema 1.3.5 actief, aanvullende CSS weg
- Live is `robotmaaierkompas-child` **1.3.5** actief; de pagina's laden `rmk.js?ver=1.3.5`.
- `scripts/ronde22_na_upload.py` (proefdraai, daarna `--schrijf`): de blokken van ronde 20 (tabelregels) en ronde 21 (`.rmk-affnote`) zijn elk één keer gevonden en weggehaald. **De aanvullende CSS is nu leeg.**
- **Live gecontroleerd** (weergegeven inhoud door 1.3.5, in de live pagina zonder aanvullende CSS, Chromium):
  - methodepagina en Over ons op 360, 390, 768, 1024 en 1440 px, de andere 15 pagina's op 390 px: 26 metingen, nergens zijwaarts scrollen, geen scriptfouten;
  - methodepagina op 390 px: de scoremodeltabel scrolt in haar eigen vak (349 van 413 px);
  - de regel "Advertentie" staat nergens: niet in de 17 pagina's, niet in #26 husqvarna-vs-gardena (de themafilter haalt hem weg, zonder CSS) en niet op de openbare pagina; ook "commissie" staat niet op de openbare pagina;
  - de datums in paginakop en eerlijkheidsblok zijn automatisch (`<time … data-rmk-modified>`); op pagina 2 blijven de 8 datums per model in de tabel staan.

### 2. M002 Navimow i206 AWD, fabrikantpagina: niet ingevuld
- Het opgegeven adres is `nl.navimow.com/products/seel-4-year-product-protection-plan-for-navimow-i-series-i206e-awd` (met zoekparameters).
  - Volgens het adres is dat een **garantieplan van Seel** ("4-year product protection plan"), en voor de **i206e** AWD, niet de productpagina van de i206 AWD.
  - navimow.com is vanuit de bouwomgeving geblokkeerd, dus ik kon de pagina niet openen.
  - Niet ingesteld: een knop "Bekijk de actuele prijs" zou bezoekers naar een garantieplan sturen. In de opdracht stond bovendien nog "PLAK HIER HET ADRES".
- **Het thema doet het al goed.** Op een lokale kopie met een voorbeeldadres toont de kaart van M002 tot en met 19 oktober de prijs (899 euro bij Coolblue), en vanaf 20 oktober alleen "Bekijk de actuele prijs" met een link naar dat adres. Er hoeft alleen het juiste adres in de modelgegevens.
- **De andere zeven modellen van de eerste golf hebben een fabrikantpagina:** M001, M004 en M005 (dezelfde Mova-pagina voor de 800 en de 1200), M006, M008, M010 en M011. Of die adressen nog werken, kon ik niet nakijken: de fabrikantdomeinen zijn hier geblokkeerd.

### 3. Over ons (#77): zachte koppelstreep
- In de inhoud is `<h1>Over robotmaaierkompas.nl</h1>` (één keer gevonden) `<h1>Over robotmaaier&shy;kompas.nl</h1>` geworden. De pagina is concept gebleven.
- De paginatitel (voor `<title>`, het kruimelpad en Yoast) is ongewijzigd "Over robotmaaierkompas.nl", zodat er geen zachte koppelstreep in zoekresultaten komt.
- **Uitkomst, gezien op schermafbeeldingen:**
  - op 360 en 390 px staat er "Over robotmaaier-" / "kompas.nl", zonder zijwaarts scrollen;
  - op 768 en 1024 px staat de kop op één regel;
  - vanaf 1280 px staat de kop door de grotere letter (56 px) en `text-wrap: balance` toch op twee regels: nu "Over robotmaaier-" / "kompas.nl", zonder de koppelstreep zou het "Over" / "robotmaaierkompas.nl" zijn.

### 4. LANCERING.md
- De stap "Prijzen verversen" is uit de voorbereiding gehaald. Onder "Bewust nog niet" staat nu waarom: prijzen verversen we pas als er bezoekers zijn, en na 19 oktober tonen de kaarten alleen "Bekijk de actuele prijs". Ook de messenprijzen blijven zo staan.
- **Nieuw, in "De eerste week":** op de lanceerdag een uptimemonitor instellen voor de homepage en pagina 12 (`/robotmaaier-kosten/`). Elke 5 minuten, met een mail bij storing, en pas aanzetten na het publiceren.
- De themastap (1.3.5) staat op "gedaan", en de standregel is bijgewerkt.

### Live gecontroleerd zonder inloggen
- /over-ons/, /hoe-we-beoordelen/ en `?page_id=77` geven 404; `/wp-json/wp/v2/pages/77` geeft 401; zoeken in de REST-API geeft een lege lijst.

### Nog te doen
- [ ] Mandy: het adres van de **productpagina** van de Navimow i206 AWD (niet het garantieplan, niet de i206e) aanleveren; daarna zet ik het in de modelgegevens van M002.
- [ ] Mandy: het nieuwste Excel-bestand als bijlage, voor de nieuwe prijzen (zie ronde 22). Volgens LANCERING.md niet nodig vóór de lancering.
- [ ] Publiceren volgens LANCERING.md op jouw teken; daarna de uptimemonitor.

## Ronde 24 (8 oktober 2026): fabrikantpagina M002
**Niets gepubliceerd**: alle 77 pagina's zijn concept, er zijn 0 gepubliceerde berichten.

### Gedaan
- **Live modelgegevens:** bij M002 (Segway Navimow i206 AWD) is `fabrikant_url` gezet op `https://be.navimow.com/products/navimow-i2-awd-robot-lawn-mower` (de pagina van de i2 AWD-serie, opgegeven door Mandy).
  - Via de dataroute `rmk/v1/modellen`: de live gegevens zijn opgehaald, alleen dit ene veld is veranderd, en het geheel is teruggezet.
  - Vóór en na vergeleken: het enige verschil is `modellen[1]/fabrikant_url` (was leeg).
  - Back-up van vóór de wijziging in de sessie.
- **Lokale themakopie** `data/modellen.json` (reserve): hetzelfde adres, zodat een volgende themaversie gelijk loopt. Niet opnieuw gezipt; de site gebruikt de gegevens uit de database.

### Gecontroleerd
- **Kaart van M002** (met de prijsfuncties van het thema op de live gegevens, `tests/prijs-modellen-test.php`):
  - 9 en 19 oktober: "Laagste nieuwe prijs rond 899 euro bij Coolblue, gezien op 5 oktober 2026" met "Bekijk bij Coolblue";
  - 20 oktober (prijs ouder dan 14 dagen): alleen de knop "Bekijk de actuele prijs", met de link naar `https://be.navimow.com/products/navimow-i2-awd-robot-lawn-mower`.
- **Live (ingelogd, weergegeven inhoud):** op de hub (#10) en pagina 1 (#11) toont de kaart van M002 vandaag nog de prijs van 5 oktober, zoals bedoeld.
- **Fabrikantpagina van de andere zeven modellen** (alleen of het veld is ingevuld; de domeinen zijn hier niet te openen): alle zeven ingevuld met een https-adres: M001 (nl.navimow.com), M004 en M005 (dezelfde pagina op nl.mova.tech), M006 (eufy.com/nl), M008 (nl.dreametech.com), M010 (husqvarna.com/nl), M011 (gardena.com/nl).
- **Zonder inloggen:** `rmk/v1/modellen` geeft 401.

### Om op te letten
- Het adres van M002 staat op de **Belgische** Navimow-site (be.navimow.com); M001 linkt naar de Nederlandse (nl.navimow.com). Op verzoek zo ingesteld.

### Nog te doen
- [ ] Publiceren volgens LANCERING.md op jouw teken; daarna de uptimemonitor.
- [ ] Nieuwe prijzen pas als er bezoekers zijn (zie LANCERING.md).

## Ronde 25 (9 oktober 2026): live site, #66 naar de prullenbak, robots.txt en sitemaps
De site is live: **17 pagina's gepubliceerd** (de eerste golf), 59 concepten, 1 in de prullenbak. Niets teruggezet naar concept; geen nieuwe thema-zip.

### 1. Conceptsjabloon #66 "Onderhoud en mesjes vervangen" naar de prullenbak
- #66 had slug `robotmaaier-mesjes-vervangen` en stond als concept onder #65 `hulp` (pad /hulp/robotmaaier-mesjes-vervangen/). Het is een dubbel onderwerp met de gepubliceerde mesjespagina #236.
- **Vooraf gecontroleerd: er linkt niets naar #66.** Gezocht op de slug, `?page_id=66` en `?p=66` in:
  - de ruwe en weergegeven inhoud van de 17 gepubliceerde pagina's;
  - de aangepaste header en footer;
  - het navigatiemenu;
  - de andere concepten;
  - de openbare homepage.
  Geen treffers. #66 had geen subpagina's.
- Via `DELETE /wp/v2/pages/66` zonder `force`: status nu `trash`, dus herstelbaar via Pagina's > Prullenbak. Er is een back-up van de inhoud in de sessie.
- **Voor en na:** 60 concepten, 17 gepubliceerd → 59 concepten, 17 gepubliceerd, 1 in de prullenbak. De andere conceptsjablonen zijn niet aangeraakt.

### 2. robots.txt en sitemaps
- **robots.txt**, gewoon en met `?nc=<tijd>`: beide 200, `text/plain`, CDN `MISS`, en precies dezelfde inhoud (**geen verschil**):
  ```
  # START YOAST BLOCK
  User-agent: *
  Disallow: /wp-json/rmk/
  Disallow: /wp-content/uploads/rmk/
  Disallow: /?s=
  Disallow: /page/*/?s=
  Disallow: /search/

  Sitemap: https://robotmaaierkompas.nl/sitemap_index.xml
  # END YOAST BLOCK
  ```
  - Geen `Disallow: /`.
  - Wel `/wp-json/rmk/` en `/wp-content/uploads/rmk/`.
  - Eén `Sitemap:`-regel, naar `sitemap_index.xml`.
  - **Geen verwijzing naar wp-sitemap.xml** en geen dubbele of tegenstrijdige regels.
  - **Niets veranderd**; dat was niet nodig.
- **(a) Yoast XML-sitemaps staan aan.** `sitemap_index.xml` wordt door Yoast SEO 28.6 gemaakt, en `wp-sitemap.xml` stuurt met een 301 door naar `sitemap_index.xml`.
- **(b) `sitemap_index.xml`:** geeft 200 (ook met cacheparameter) en verwijst alleen naar `page-sitemap.xml` (lastmod 2026-10-09 09:32).
  - `page-sitemap.xml` bevat precies de 17 gepubliceerde pagina's, en geen concepten of prullenbakpagina's. Vergeleken met de lijst uit de REST-API: identiek.
  - `post-sitemap.xml` geeft 200 maar is leeg (0 URL's, 0 gepubliceerde berichten) en staat niet in de index.
  - `author-sitemap.xml` en `category-sitemap.xml` geven 404.
- **(c)** Zie robots.txt hierboven: in orde.
- **LiteSpeed-cache geleegd** via de dataroute: `POST /rmk/v1/modellen` met de huidige gegevens, ongewijzigd teruggezet (inhoud identiek, alleen `opgeslagen` is bijgewerkt).
  - Daarna gaf de eerste aanvraag op /, /beste-robotmaaier/ en /robotmaaier-zonder-draad/ `x-litespeed-cache: miss`, en de tweede `hit`.
  - **Bewust niet gebruikt:** de route `/rmk/v1/noindex`. Die leegt ook de cache, maar zet "Zoekmachines niet laten indexeren" weer **aan** (`blog_public = 0`). Op de live site nooit aanroepen.
- **Mandy:** leeg ook de **CDN-cache in hPanel** (Website > Prestaties > CDN > Cache legen). Bij deze controles gaf de CDN overal `MISS`, maar een volledige leging is het zekerst.

### 3. Controle van drie pagina's (als browser en als Googlebot)

| Pagina | HTTP | X-Robots-Tag | meta robots | canonical | in sitemap |
|---|---|---|---|---|---|
| / | 200 | geen | index, follow (+ max-image-preview:large, max-snippet:-1, max-video-preview:-1) | https://robotmaaierkompas.nl/ (zelf) | ja |
| /beste-robotmaaier/ | 200 | geen | index, follow (idem) | …/beste-robotmaaier/ (zelf) | ja |
| /robotmaaier-zonder-draad/ | 200 | geen | index, follow (idem) | …/robotmaaier-zonder-draad/ (zelf) | ja |

### Statusoverzicht (Gereedschap > Robotmaaierkompas)
- "Zoekmachines niet laten indexeren staat aan": **NEE**. Dat is nu juist goed: indexeren staat aan.
- "Niets gepubliceerd": **NEE** (17 gepubliceerd). Ook dat is goed.
- Die twee controles zijn nog geformuleerd voor de tijd vóór de lancering. Alle andere controles zijn OK: Yoast 28.6, `RMK_AFFILIATE_ACTIVE` uit, geen affiliatelinks, prijstaak uit.

### Nog te doen
- [ ] Mandy: CDN-cache legen in hPanel.
- [ ] Mandy: Search Console en Bing (LANCERING.md, stap 5 en 6) en de uptimemonitor (stap 7).
- [ ] Bij een volgende themaversie: de twee statuscontroles omzetten naar de situatie na de lancering, en de route `/rmk/v1/noindex` weghalen of beveiligen.

## Ronde 26 (9 oktober 2026): hercontrole #66, drie pagina's, page-sitemap en robots.txt
Alleen controles; **niets gewijzigd**. Niets teruggezet naar concept, geen thema-zip, robots.txt niet aangeraakt.

### 1. #66 "Onderhoud en mesjes vervangen"
- Stond al sinds ronde 25 in de prullenbak (status `trash`, slug nu `robotmaaier-mesjes-vervangen__trashed`). Niet opnieuw verwijderd.
- Opnieuw gecontroleerd: er linkt niets naar #66. Niet vanuit de 17 gepubliceerde pagina's (ruw en weergegeven), niet vanuit de header, de footer of het navigatiemenu. Het oude adres /hulp/robotmaaier-mesjes-vervangen/ geeft 404.
- Stand: 17 gepubliceerd, 59 concepten, 1 in de prullenbak. De andere conceptsjablonen zijn niet aangeraakt.

### 2. Drie pagina's (als browser en als Googlebot)
- /, /beste-robotmaaier/ en /robotmaaier-zonder-draad/:
  - HTTP 200, zonder doorverwijzing;
  - geen X-Robots-Tag-header;
  - meta robots "index, follow" (plus de max-…-waarden van Yoast);
  - een canonical naar het eigen adres;
  - alle drie staan in /page-sitemap.xml.

### 3. /page-sitemap.xml (met cacheparameter, HTTP 200)
- Precies de 17 gepubliceerde pagina's, zonder concepten of de prullenbakpagina. Vergeleken met de REST-API: identiek. De lijst:
  - /
  - /privacy/
  - /cookies/
  - /affiliate-melding/
  - /redactiebeleid/
  - /colofon/
  - /contact/
  - /over-ons/
  - /over-ons/mandy-van-den-broek/
  - /hoe-we-beoordelen/
  - /robotmaaier-kosten/
  - /robotmaaier-mesjes/
  - /robotmaaier-zonder-grensdraad/
  - /robotmaaier-test-consumentenbond/
  - /robotmaaier-zonder-draad/
  - /robotmaaier-test-vergelijking/
  - /beste-robotmaaier/

### 4. /robots.txt?nc=… (HTTP 200, CDN MISS, last-modified 09:46:47 GMT)
```
# START YOAST BLOCK
User-agent: *
Disallow: /wp-admin/
Allow: /wp-admin/admin-ajax.php
Disallow: /wp-json/rmk/
Disallow: /wp-content/uploads/rmk/

Sitemap: https://robotmaaierkompas.nl/sitemap_index.xml
# END YOAST BLOCK
```
- **Veranderd sinds ronde 25** (een paar minuten eerder; niet door mij):
  - **erbij:** `Disallow: /wp-admin/` en `Allow: /wp-admin/admin-ajax.php`;
  - **weg:** `Disallow: /?s=`, `Disallow: /page/*/?s=` en `Disallow: /search/`.
- Geen `Disallow: /`. `/wp-json/rmk/` en `/wp-content/uploads/rmk/` staan er nog, met één `Sitemap:`-regel naar `sitemap_index.xml`, zonder verwijzing naar wp-sitemap.xml.
- Op verzoek niets gewijzigd: Mandy regelt robots.txt zelf in Yoast of hPanel.

## Voor de volgende themaversie (1.3.6)
**Pas maken bij een echte wijziging aan het thema, of wanneer Mandy erom vraagt.** Nu geen zip gemaakt.

1. **Route `/rmk/v1/noindex` en de bijbehorende knop volledig verwijderen.**
   - De route (`inc/bouw.php`, in `rest_api_init`) zet `blog_public` op `0`: "Zoekmachines niet laten indexeren" gaat dan weer aan. Daarna leegt hij de LiteSpeed-cache.
   - Op de live site is dat schadelijk. Haal de route weg en ook de knop of actie in Gereedschap > Robotmaaierkompas die hem aanroept.
   - Controleer daarna dat `POST /wp-json/rmk/v1/noindex` 404 geeft (`rest_no_route`).
2. **De twee controles in het statusoverzicht omkeren of vervangen** (`rmk_status_checks()` in `inc/bouw.php`), zodat ze de lancering weerspiegelen:
   - "Zoekmachines niet laten indexeren staat aan" is nu OK als `blog_public = 0`. Dat moet worden: "Zoekmachines mogen de site indexeren", OK als `blog_public = 1`.
   - "Niets gepubliceerd" is nu OK bij 0 gepubliceerde pagina's. Vervangen door bijvoorbeeld "De eerste golf is gepubliceerd" (de 17 pagina's uit LANCERING.md hebben status `publish`, en verder niets onverwachts), of weglaten.
3. **Alle andere beheerroutes die de indexering of publicatie kunnen aanpassen controleren en melden.**
   - Startpunt, de routes die ik eerder in `inc/bouw.php` en `inc/data.php` zag (allemaal `manage_options`):
     - `POST /rmk/v1/paginas`: `rmk_build_pages()`, maakt of wijzigt pagina's, en zet de privacypagina;
     - `POST /rmk/v1/seo`: `rmk_configure_seo()`, past Yoast-instellingen aan (mogelijk ook indexering of sitemaps);
     - `POST /rmk/v1/huisstijl`: sitepictogram en standaard deelafbeelding;
     - `POST /rmk/v1/modellen`: modelgegevens en het legen van de cache;
     - `GET /rmk/v1/status`: alleen lezen.
   - Per route nagaan of hij `blog_public`, de paginastatus (publiceren of terug naar concept), Yoast-noindex of de sitemap kan veranderen.
   - Melden wat elke route doet. Routes die alleen bij de bouw nodig waren (zoals `/paginas` en `/seo`) weghalen of achter een extra instelling zetten (bijvoorbeeld `RMK_BOUWMODUS` in wp-config.php).
   - Ook de knoppen in Gereedschap > Robotmaaierkompas en de WP-CLI-commando's (als die er zijn) meenemen.
   - Pas daarna de zip maken en testen.

### Aanvulling voor 1.3.6 (9 oktober 2026)
Alleen genoteerd; geen zip.

- **(a) Bouwroutes achter `RMK_BOUW_ACTIVE`.** `/rmk/v1/paginas`, `/rmk/v1/seo` en `/rmk/v1/huisstijl`, en hun knoppen in Gereedschap > Robotmaaierkompas, alleen als `define( 'RMK_BOUW_ACTIVE', true );` in wp-config.php staat. **Standaard uit.**
  - Zonder die constante worden de routes **niet geregistreerd** (niet alleen geweigerd), en de knoppen worden niet getoond.
  - Een aanroep geeft dan 404 `rest_no_route`.
- **(b) `/rmk/v1/modellen` en `/rmk/v1/status` blijven:**
  - uitsluitend voor beheerders (`permission_callback` met `current_user_can( 'manage_options' )`);
  - nooit gecachet (`Cache-Control: no-store` en `X-LiteSpeed-Cache-Control: no-cache`, zoals nu voor `/wp-json/rmk/`);
  - zonder mogelijkheid om de indexering (`blog_public`), de publicatiestatus van pagina's, Yoast-instellingen of de sitemap te wijzigen.
  - `/modellen` slaat alleen de modelgegevens op en leegt de cache; `/status` leest alleen.
  - Bij het bouwen nalopen welke functies `/modellen` aanroept: `rmk_validate_modellen()` en `rmk_save_modellen()` mogen niets anders schrijven dan de opties `rmk_modellen` en `rmk_modellen_data` en het bestand in `uploads/rmk/`.
- **(c) Nieuwe test: elke rmk-route geeft zonder inloggen 401 of 404.**
  - Haal (zonder inloggen) de index `/wp-json/` en, als die bestaat, `/wp-json/rmk/v1` op. Neem daarnaast de bekende lijst mee (`/rmk/v1`, `/status`, `/modellen`, `/noindex`, `/paginas`, `/seo`, `/huisstijl`), zodat ook routes die niet in de index staan getest worden.
  - Roep elke route aan met GET en POST, zonder inloggegevens en zonder cookies.
  - Verwacht: 401 (`rest_forbidden` of "Alleen voor beheerders.") of 404 (`rest_no_route`), nooit 200 of een andere code. Geen gegevens in de antwoorden. Na 1.3.6 moeten `/noindex`, en zonder `RMK_BOUW_ACTIVE` ook `/paginas`, `/seo` en `/huisstijl`, 404 geven.
  - Als script in `tests/` (bijvoorbeeld `tests/rmk-routes-test.py`), te draaien tegen de live site. Een POST zonder inloggen kan niets wijzigen, dus de test is ook live veilig.

## Ronde 27 (10 oktober 2026): fabrikantpagina M002 naar de Nederlandse Navimow-site
### Gewijzigd (live)
- In de live modelgegevens (`rmk/v1/modellen`) staat bij **M002 (Segway Navimow i206 AWD)** `fabrikant_url` nu op `https://nl.navimow.com/products/navimow-i2-awd-robot-lawn-mower`. Dat is de Nederlandse pagina van de i2 AWD-serie, die de datasessie als bron heeft gebruikt. Eerst stond hier de Belgische pagina `https://be.navimow.com/products/navimow-i2-awd-robot-lawn-mower` (ronde 24). Nu linken M001 en M002 allebei naar nl.navimow.com.
- Werkwijze: de live gegevens opgehaald, alleen dit ene veld veranderd en het geheel teruggezet. Daarna opnieuw opgehaald en vóór en na vergeleken: het enige verschil is `modellen[1]/fabrikant_url`. De andere velden en modellen (13 in totaal), de prijzen, scores en teksten zijn gelijk gebleven. Bij het opslaan wordt de paginacache zelf geleegd.
- **Niet gewijzigd:** pagina's, thema, en de lokale themakopie `data/modellen.json` in deze repository. Daar staat bij M002 nog de be-pagina. De site gebruikt de gegevens uit de database, dus dat heeft live geen effect. Geen zip.

### Gecontroleerd
- **Kaart van M002:** de prijsfuncties van het thema (`rmk_offer_html`, ongewijzigd sinds 1.3.0) gedraaid op de live gegevens van na de wijziging.
  - 19 oktober (dag 14): "Laagste nieuwe prijs rond 899 euro bij Coolblue, gezien op 5 oktober 2026", met de knop "Bekijk bij Coolblue".
  - 20 oktober (dag 15, prijs verlopen): alleen de knop **"Bekijk de actuele prijs"**, met de link naar `https://nl.navimow.com/products/navimow-i2-awd-robot-lawn-mower`.
- **Live** op /robotmaaier-zonder-draad/ toont de kaart van M002 vandaag nog de Coolblue-prijs van 5 oktober, zoals bedoeld.
- De Navimow-pagina zelf is vanuit deze omgeving niet te openen (de proxy blokkeert nl.navimow.com). Het adres is overgenomen zoals je het opgaf.

### Om op te letten
- De lokale themakopie (be-pagina) loopt nu niet gelijk met de live gegevens (nl-pagina). Bij een volgende themaversie of upload van het modelbestand de nl-pagina overnemen, anders komt de be-pagina terug.

## Ronde 28 (12 oktober 2026): Navimow-modellen M015 tot en met M018, conceptpagina Segway Navimow
**Niets gepubliceerd**: 17 gepubliceerd (ongewijzigd), 60 concepten (was 59, plus de nieuwe pagina), 0 gepubliceerde berichten. Geen thema-zip.

Aangeleverd: het nieuwste `robotmaaierkompas_modeldata_v1.xlsx` (M018 toegevoegd op 12 oktober), `pagina-segway-navimow.md` en `modellen-teksten-navimow.json`.

### 1. Modelgegevens (live, via `rmk/v1/modellen`)
- **Geüpload: de 13 live modellen ongewijzigd, plus M015, M016, M017 en M018**: 17 modellen. Ook de algemene velden (`gegenereerd`, `algemeen`) zijn ongewijzigd, zodat de datums op de pagina's niet verschuiven.
- De vier nieuwe modellen komen uit het Excel-bestand via `scripts/excel_naar_json.py` (zelfde regels als altijd: alleen velden met bron en datum, geen Bol).
  - **M015 Navimow i210 LiDAR Pro:** functiescore **96,4** (navigatie 10, hellingen 10, app 10, veiligheid 10, geluid 6).
  - **M016 Navimow i205 AWD:** functiescore **92,7**. Beide gelijk aan het blad Scores.
  - **M017 Navimow i220 LiDAR Pro** en **M018 Navimow X420**: niveau basis, `"niveau": "basis"`, alle scoreonderdelen leeg, dus **geen score**. Alleen de kernvelden (navigatie, draad, oppervlak, helling, geluid, verbinding).
  - **Prijzen: geen.** Het blad Prijzen heeft geen regels voor M015 tot en met M018, dus er staat ook geen Bol-gegeven in (de hele upload bevat geen "bol").
  - **Fabrikantpagina** (`fabrikant_url`, voor de knop "Bekijk de actuele prijs"): uit de bronregel "Beschikbaarheid fabrikant" (gecontroleerd):
    - M015 en M017: `https://nl.navimow.com/products/navimow-i2-lidar-pro-robot-lawn-mower`
    - M016: `https://nl.navimow.com/products/navimow-i2-awd-robot-lawn-mower` (dezelfde als M002)
    - M018: `https://nl.navimow.com/products/navimow-x4-robot-lawn-mower`
    - M001 en M002 hadden al een nl.navimow.com-pagina (ongewijzigd).
  - **Teksten** (beste_voor, analyse, plus- en minpunten) uit `modellen-teksten-navimow.json`.
  - **Verbinding** "4G ingebouwd; na het eerste jaar betaald" (kaartveld "4G"), en de kosten 29,99 euro per jaar na 1 gratis jaar.
- **Vóór en na vergeleken:** de 13 bestaande modellen zijn identiek; de vier nieuwe staan erin zoals verstuurd (alleen notatieverschil 10.0 tegenover 10).
- **Weergave van alle 17 gepubliceerde pagina's vóór en na de upload vergeleken** (kaarten, scores, scorecellen, tabelrijen en de volledige tekst): **alles gelijk**.
  - Hub /beste-robotmaaier/: dezelfde 5 kaarten (i206 AWD 92,7, 410VE NERA 87,3, LiDAX Ultra 1200 80,5, A1 Pro 78,6, Sileno Free 800 60,9).
  - Pagina 1 /robotmaaier-zonder-draad/: dezelfde 8 kaarten en scoretabel.
  - **M003 (i210 LiDAR) staat op geen enkele gepubliceerde pagina**; M015 tot en met M018 ook niet.
- **Scriptaanpassingen** (`scripts/`), zodat een nieuwe run hetzelfde oplevert:
  - `excel_naar_json.py`:
    - herkent de veldnaam "App: iOS/Android, …, smart home, …" (anders ontbrak de app-score en kreeg M015 geen score);
    - neemt de fabrikantpagina uit "Beschikbaarheid fabrikant" als er geen prijsregel van de fabrikant is;
    - geeft modellen met "NIVEAU BASIS" in de opmerking geen score.
  - `modellen_teksten.json` en `modellen_analyse.json`: de Navimow-teksten erbij.
  - `verbinding_toewijzing.json` en `kosten_toewijzing.json`: de regels voor M015 tot en met M018.
- **Lokale themakopie** `data/modellen.json` (reserve): gelijk aan live. Daarmee staat de nl-pagina van M002 (ronde 27) er nu ook in.

### 2. Conceptpagina segway-navimow-robotmaaier (#264)
- **Status concept**, hoofdniveau (`/segway-navimow-robotmaaier/`, net als de gepubliceerde pagina's; niet onder het concept /merken/). Titel en metabeschrijving uit de md; kruimelpadtitel "Segway Navimow robotmaaier".
- Opbouw: patroon pagina-merk (eyebrow "Merk"), met het skelet van de hub. Gebouwd met `scripts/ronde28_bouw.py`, de inhoud staat in `scripts/ronde28/navimow.json`, en `scripts/ronde28_upload.py` maakt of werkt de pagina alleen als concept bij.
- **Zes productkaarten** in de volgorde van de tekst: i205 AWD (M016), i206 AWD (M002), i210 LiDAR Pro (M015), i220 LiDAR Pro (M017), X420 (M018), i105E (M001). De kop "### …" uit de md is de titel van de kaart (geen dubbele kop).
  - Het thema vult per kaart de specificatiekaart, Beste voor, analyse, plus- en minpunten en het prijsblok in.
  - **Scores:** 92,7 / 92,7 / 96,4 / – / – / 75,9.
  - **M017 en M018: "Niet beoordeeld"**, als vaste cel zonder `data-rmk-score`. Het thema hoeft daarvoor niet te veranderen.
  - **Prijsblok:** vijf kaarten tonen "Bekijk de actuele prijs" naar de Navimow-pagina. M002 toont tot en met 19 oktober "rond 899 euro bij Coolblue" en daarna ook de knop. Zo laten op verzoek: de regel "geen prijzen van winkels met naam" gaat over de lopende tekst.
- **Lopende tekst:** geen winkelnamen bij prijzen. Alle bedragen zijn van Navimow (4G, Access+, messen, garage, antenneset).
- **Interne links:**
  - in de tekst: Hoe we beoordelen (#scoremodel), de keuzehulp op /robotmaaier-zonder-draad/#keuzehulp, /robotmaaier-mesjes/, /robotmaaier-kosten/ en /robotmaaier-zonder-grensdraad/ (FAQ);
  - een lijst "Meer lezen" (toegevoegd, de md had er geen) met /beste-robotmaaier/, /robotmaaier-zonder-draad/, /robotmaaier-test-vergelijking/ en /robotmaaier-kosten/;
  - de modelnamen in beide tabellen linken naar hun kaart.
- **FAQ:** zes vragen. Daarna "Wat we nog niet weten" met een mailto-link.
- **Bronnen** per model uit het blad Bronnen (handleidingen, fabrikantpagina's en appwinkels; geen winkels, winkelclaims of Bol), en het scoremodel als eigen methode.
  - Bij een regel met twee adressen op hetzelfde domein staat "pdf-bijlage" of "supportartikel" in plaats van het lange pad; anders scrolde de pagina op 360 px zijwaarts.
- Auteursblok als patroon.

### 3. Links vanaf de hub en pagina 1: klaargezet, niet geplaatst
- **Besluit Mandy:** de hub en pagina 1 zijn gepubliceerd, de Navimow-pagina is een concept. Een link zou nu een 404 geven, dus de links worden nog niet geplaatst.
- `scripts/ronde28_links.py` voegt toe: "Alle Segway Navimow-modellen die nu nieuw te koop zijn, met kosten: zie Segway Navimow robotmaaier." (link naar /segway-navimow-robotmaaier/):
  - **/beste-robotmaaier/ (#10):** als eerste regel onder "Meer lezen";
  - **/robotmaaier-zonder-draad/ (#11):** als alinea direct onder "De modellen een voor een".
- Getest op kopieën van de live inhoud: precies één ankerpunt, en verder verandert er niets.
- **Live geweigerd:** "/segway-navimow-robotmaaier/ is niet gepubliceerd". Het script schrijft pas als de pagina gepubliceerd is.
- De hub en pagina 1 zijn niet aangeraakt (inhoud en wijzigingsdatum gelijk aan vóór deze ronde).

### 4. Controles
- **Interne links** op de nieuwe pagina: alle 12 adressen geven 200 (zonder inloggen), alle ankers bestaan (6 kaarten, #scoremodel, #verdienmodel, #keuzehulp).
- **Geen `[`, geen `{{` of invulveld**, geen Bol, geen affiliatelinks (`/ga/`, sponsored). Eén h1.
- **Browser** (Chromium, de weergegeven conceptinhoud in het live paginaskelet), op 360, 390, 768, 1024 en 1440 px: geen zijwaarts scrollen, geen scriptfouten, 6 kaarten, twee keer "Niet beoordeeld".
- **Niets gepubliceerd:**
  - 17 gepubliceerd (dezelfde lijst), 60 concepten, geen statuswijzigingen, 0 berichten;
  - zonder inloggen geven /segway-navimow-robotmaaier/ en `?page_id=264` 404;
  - de REST-API zonder inloggen geeft een lege lijst;
  - de page-sitemap bevat 17 URL's, zonder Navimow-pagina.
- **paginatekst-navimow.md** (de volledige weergegeven tekst, met kaarten en bronnen) als download aan Mandy gegeven, niet in de repository.

### Om op te letten
- **Analyse van M002** (bestaande tekst, niet gewijzigd): "In onze functiescore staat dit model bovenaan". Op de Navimow-pagina scoort M015 hoger (96,4), en die analyse zegt hetzelfde. Op de hub en pagina 1 klopt de zin wel, want daar staat M015 niet. Aanpassen kan alleen in de modelgegevens, en dan geldt het voor alle pagina's.
- **Het nieuwe Excel-bestand heeft nieuwere prijzen (7 oktober) voor de bestaande modellen.** Die zijn niet geüpload: de bestaande modellen moesten ongewijzigd blijven. Live staan nog de prijzen van 5 oktober, die na 19 oktober vervallen.
- **M002 in het Excel-bestand** heeft geen fabrikantpagina (geen prijsregel van de fabrikant en geen regel "Beschikbaarheid fabrikant"). Wie de modelgegevens opnieuw uit het Excel-bestand maakt, verliest de nl-pagina van M002, tenzij die regel erin komt.
- **M001 in de kaart:** navigatie "RTK + camera" (bestaande modelgegevens); de tabel in de md zegt "Eigen GNSS-antenne met camera". Niet gewijzigd.

### Nog te doen
- [ ] Mandy: de conceptpagina #264 nalezen en publiceren op jouw teken. Daarna draai ik `python3 scripts/ronde28_links.py --schrijf` voor de links op de hub en pagina 1, en controleer ik live.

## Ronde 29 (12 oktober 2026): analyse M002, "Waarom deze" op de hub, App Store-links
**Niets gepubliceerd**: 17 gepubliceerd, 60 concepten (ongewijzigd), 0 berichten. Geen thema-zip. Gebruikt: `scripts/ronde29_upload.py` (proefdraai, daarna `--schrijf`), en voor het concept #264 `ronde28_bouw.py` en `ronde28_upload.py`.

### 1. Analyse M002 (live modelgegevens)
- "In onze functiescore staat dit model bovenaan." is "In onze functiescore scoort dit model hoog (92,7)." geworden.
- **Vóór en na vergeleken:** het enige verschil in de 17 modellen is `M002.analyse`; de algemene velden zijn ongewijzigd.
- **Live zichtbaar:** op de hub, pagina 1 en de Navimow-pagina (#264, ingelogd) staat de nieuwe zin, en de oude nergens meer.
- `scripts/modellen_analyse.json` is ook aangepast, zodat een nieuwe omzetting uit het Excel-bestand de nieuwe zin houdt. De lokale themakopie `data/modellen.json` is gelijk aan live.
- **Wel nog "bovenaan":** de analyse van M015 (i210 LiDAR Pro, 96,4) zegt "In onze functiescore staat dit model bovenaan, maar …". Op de Navimow-pagina klopt dat; M015 staat op geen andere pagina. Niet gewijzigd.

### 2. Hub (#10), "Waarom deze" bij de i206 AWD
- "de hoogste functiescore in onze selectie, helling tot 45%" is "een van de hoogste functiescores in onze selectie, helling tot 45%" geworden (één keer gevonden). De status is "gepubliceerd" gebleven.
- **Komt de zin elders voor?** Gezocht in de ruwe inhoud van alle 77 pagina's:
  - de zin met "helling tot 45%" alleen op de hub;
  - **"de hoogste functiescore in onze selectie"** staat ook op de Navimow-pagina (#264, concept), maar bij de **i210 LiDAR Pro** (M015, 96,4): "Waarom deze: de hoogste functiescore in onze selectie. LiDAR met camera …". Dat klopt daar, dus niet gewijzigd.

### 3. App Store-links in de bronnenlijsten
- **Vervangen:** alle itunes.apple.com-links (`lookup?id=…` en `search?term=…`) door de App Store-pagina van dezelfde app. Het label is niet veranderd. Op de hub en #264 staat in de linktekst nu "(apps.apple.com)".

  | App | Nieuw adres |
  |---|---|
  | Navimow | https://apps.apple.com/nl/app/navimow/id1602205067 |
  | MOVAhome | https://apps.apple.com/nl/app/movahome/id6499421624 |
  | Automower Connect | https://apps.apple.com/nl/app/id983601778 |
  | Dreamehome | https://apps.apple.com/nl/app/id1564419343 |
  | GARDENA smart system | https://apps.apple.com/nl/app/id971199503 |
  | Anker eufy | https://apps.apple.com/nl/app/id1424956516 |

  - De naam in het pad staat er alleen bij Navimow en MOVAhome: die adressen staan zo in het Excel-bestand.
  - apps.apple.com is vanuit de bouwomgeving geblokkeerd, dus de andere namen kon ik niet controleren. Daarom de vorm zonder naam (`/nl/app/id<nummer>`); dat is ook een geldig App Store-adres, en Apple stuurt het door naar de app-pagina.
- **Per pagina:**
  - **hub (#10):** 5 links. De twee regels van de i206 AWD met nu hetzelfde adres zijn één regel geworden: "App iOS én Android, App-rating (apps.apple.com)" (34 naar 33 regels);
  - **pagina 1 (#11):** 6 links;
  - **Navimow-pagina (#264, concept):** opnieuw gebouwd, alleen de app-regels zijn veranderd (bij M002 ook samengevoegd).
  - Op de andere 74 pagina's stonden geen itunes-links.
  - Live (zonder inloggen) staan op de hub en pagina 1 0 itunes-links.
- **Script:**
  - `excel_naar_json.py` heeft nu de functie `app_store()`. Die zet elk itunes-adres in de bronnen (specificaties, reviews, verbinding en kosten) om naar apps.apple.com.
  - Getest op het Excel-bestand: geen itunes-adressen meer, en verder dezelfde uitvoer als ronde 28.
  - Eén uitzondering: ECOVACS HOME (M009) heeft in het Excel-bestand geen app-nummer en blijft dus staan. M009 wordt overgeslagen (uitverkocht).
  - `ronde28_bouw.py` gebruikt dezelfde functie.
- **Gezien, niet gewijzigd:** op pagina 1 hebben de app-bronnen het label **"Handleiding"** in plaats van "Appwinkel" (alle 16 app-regels). Dat was al zo.

### 4. Controles
- **Weergave van alle 17 gepubliceerde pagina's vóór en na vergeleken:**
  - hub: dezelfde 5 kaarten in dezelfde volgorde (92,7 / 87,3 / 80,5 / 78,6 / 60,9);
  - pagina 1: dezelfde 8 kaarten (92,7 / 87,3 / 80,5 / 80,5 / 78,6 / 75,9 / 63,2 / 60,9);
  - de scorecellen en tabelrijen op de hub, pagina 1 en de vergelijkingspagina zijn gelijk.
  - De tekst verschilt alleen waar bedoeld. Op / en /over-ons/mandy-van-den-broek/ staat bij de hub en pagina 1 in "Onlangs bijgewerkt" nu "Bijgewerkt op 12 oktober 2026" (automatisch, omdat ze zijn opgeslagen).
- **M002 heeft nog de fabrikantpagina** `https://nl.navimow.com/products/navimow-i2-awd-robot-lawn-mower`. Met de prijsfunctie van het thema op de live gegevens:
  - 19 oktober: "rond 899 euro bij Coolblue";
  - 20 oktober: alleen "Bekijk de actuele prijs" naar die pagina.
- **Niets gepubliceerd:** 17 gepubliceerd, 60 concepten, 0 berichten. #264 is nog concept.

## Ronde 30 (13 oktober 2026): thema 1.3.6, Bol-koppeling
**Niets gepubliceerd** (17 gepubliceerd, 60 concepten). Live is alleen de modelgegevens gewijzigd (stap 7, eerste deel). Thema 1.3.6 is gebouwd en getest; **Mandy moet het nog uploaden**. Zip: `robotmaaierkompas-child.zip`, 420 KB, versie 1.3.6.

Bronnen: het nieuwste `robotmaaierkompas_modeldata_v1.xlsx` (blad "Bol", Logboek rijen 136-148) en `tekstwijzigingen-affiliate-live.md`. Geen van beide staat in de repository of op de site. **Enige bron voor de vorm van de API en de links: Logboek rijen 137-145.** Besluiten Mandy: f=api (niet TXL), subid = paginaslug, geen Bol-beoordelingen.
- **Sleutels:** volgens Logboek rij 136 heeft het onderzoeksvenster de sleutels in de chat gekregen. Ze staan niet in het Excel-bestand; ik heb ze nergens gezien of gebruikt. Alle tests gebruiken nep-waarden. Advies uit rij 136: het secret roteren.

### 1. Bol-regel in de productkaart (`inc/bol.php`, nieuw; `inc/prijzen-bol.php` verwijderd)
- Alleen bij een **geldig Bol-aanbod**, onder het bestaande prijsblok (Coolblue of "Bekijk de actuele prijs" blijft staan):
  - "**899 euro**. Prijs bij bol.com, bijgewerkt om 14:05." Bij een eerdere dag: "bijgewerkt gisteren om …".
  - Bij een partner: "…, via een partner van bol.com." Partner = seller.name is niet "bol.com" (Logboek 141).
  - De knop "Bekijk bij bol.com" met `rel="sponsored nofollow"`.
  - Eronder: "Je gaat naar bol.com. Bron: bol.com."
  - Geen beoordelingen: /ratings wordt niet opgehaald.
- **Geldig betekent:**
  - 200 van /offers/best met een prijs groter dan 0;
  - condition NEW, geen voorbestelling, met een verkopernaam en dezelfde EAN;
  - niet ouder dan 12 uur;
  - model met EAN en bol-product-URL in de modelgegevens;
  - de drie Bol-constanten aanwezig **en** `RMK_AFFILIATE_ACTIVE` aan.
- **Eigen keuze, niet uit het Logboek:** een aanbod dat voorbesteld moet worden (`isPreOrder`) of niet nieuw is, toon ik niet. Zo'n maaier is nu niet nieuw te koop.
- **Paginacache:** de LiteSpeed-TTL van een pagina met een Bol-regel is nooit langer dan de resterende geldigheid van de prijs (`litespeed_control_set_ttl`).

### 2. Affiliatelink (Logboek 144-145)
- `https://partner.bol.com/click/click?p=2&t=url&s=<RMK_BOL_SITE_ID>&f=api&url=<bol-product-URL>&name=<modelnaam>&subid=<paginaslug>`
- **Codering:** de waarden volledig gecodeerd met PHP `rawurlencode`. Dat is gelijk aan Python `quote(waarde, safe="")` uit het Logboek.
- **Subid:** de slug van de pagina waarop de knop staat; alleen kleine letters, cijfers en koppeltekens.
- **Getest:** de link van de i206 AWD is gelijk aan die uit het blad Bol, met f=TXL vervangen door f=api en `&subid=robotmaaier-zonder-draad` erachter.
- `/ga/` blijft voor links die geen Bol zijn; de Bol-knop gaat rechtstreeks naar partner.bol.com.

### 3. Prijstaak
- **Planning:** vier keer per dag (WP-Cron, eigen schema "rmk_zes_uur"). Handmatig, of als echte cron: `wp rmk bol-ronde`. Stappen voor een echte cron in hPanel: LANCERING.md, "Bol-koppeling aanzetten".
- **Token** (Logboek 137): POST login.bol.com met Basic base64(id:secret). Hergebruikt tot 30 s voor `expires_in`, bewaard als transient en nooit gelogd. Bij een 401 vernieuwt de taak het token één keer en probeert opnieuw.
- **Aanbod** (Logboek 138, 141): GET `/products/{ean}/offers/best?country-code=NL&include-seller=true` met Bearer, `Accept: application/json` en `Accept-Language: nl`.
- **Snelheid:** minstens 0,1 s tussen verzoeken (maximaal 10 per seconde). Bij `x-ratelimit-remaining` 0 of een 429 wacht de taak `x-ratelimit-reset` af en probeert één keer opnieuw.
- **Uitkomst per model:** ok, geen_aanbod (404 "Unable to find offer"), ongeldig of fout. Bij geen aanbod, een fout of 404 verdwijnt de Bol-regel bij de volgende weergave.
- **Na elke ronde:** de LiteSpeed-cache wordt geleegd.
- **Log** (laatste 20 rondes) zonder secrets of tokens: per model de uitkomst, de HTTP-code en title/detail/X-Request-ID uit problem+json.
- **`/rmk/v1/bol-status`:** alleen voor beheerders, nooit gecachet (alle /wp-json/). Toont per model uitkomst, prijs, verkoper, tijd, geldig tot en of de regel op de site staat. De constanten alleen als ja/nee.
- **Constanten zonder schakelaar:** de taak draait (zodat bol-status gevuld is), maar de site toont niets.
- **Zonder constanten:** geen verzoeken, geen taak, geen Bol-regel. Alles zoals in 1.3.5.

### 4. Afbeeldingen
- Bij een geldig aanbod vervangt de foto van bol.com het beeldvlak van de specificatiekaart:
  - de oorspronkelijke 550-px-URL op media.s-bol.com, met `width` en `height` en `loading="lazy"`;
  - "Foto: bol.com";
  - nooit lokaal opgeslagen.
- Zonder aanbod blijft de specificatiekaart zonder foto.

### 5. Schakelaar
- **`RMK_AFFILIATE_ACTIVE` uit (standaard):** geen Bol-regel, geen Bol-foto, geen advertentie-regel. Getest: de kaart is byte voor byte gelijk aan 1.3.5.
- **Aan:** de advertentie-regel komt één keer per pagina, direct boven de eerste kaart met een Bol-knop (als er nog geen staat).
  - De tekst is voorlopig de huidige ("Advertentie: via deze knoppen krijgen wij mogelijk een commissie. Dat verandert de score niet.").
  - Hij is instelbaar via de instelling `rmk_advertentie_tekst`, zodat de tekst uit het md-bestand (punt 8) later zonder nieuwe zip kan.
- **Teksten uit tekstwijzigingen-affiliate-live.md: niet toegepast.** Klaargezet in `scripts/ronde30_affiliate_teksten.py`.
  - Proefdraai: alle "Was"-teksten precies één keer gevonden: #81 (eerste alinea, en de alinea over score en volgorde blijft), #77, #80, #76, de footer, #82 en #83.
  - Letterlijk zoeken vond #77, #80, #76 en de footer niet, omdat "affiliate-melding" daar een link is. Het script zoekt met tags ertussen en houdt die link in de nieuwe tekst.
  - Punt 8 (advertentie-tekst) kan pas met 1.3.6 actief.

### 6. Lijst voor 1.3.6
- **`/rmk/v1/noindex` en de knop:** verwijderd.
- **Statuscontroles omgekeerd:**
  - "Zoekmachines mogen de site indexeren": OK bij `blog_public = 1`;
  - "De eerste golf is gepubliceerd": de 17 pagina's van ronde 26.
  - De oude controle "Prijstaak uitgeschakeld" is vervangen door "Bol-koppeling" en "Bol-prijstaak draait": laatste ronde minder dan 7 uur geleden, anders het advies voor een echte cron.
- **`RMK_BOUW_ACTIVE`** (standaard uit): /paginas, /seo en /huisstijl worden zonder deze constante niet geregistreerd. Hun knoppen en de WP-CLI-commando's `rmk paginas` en `rmk seo` ook niet.
- **404 in plaats van 401:** `inc/techniek.php` gaf voor elke /rmk/-route 401, ook voor routes die niet bestaan. Nu geeft een niet-bestaande route 404 `rest_no_route`; bestaande routes geven niet-beheerders nog steeds 401.
- **`/modellen` en `/status`:** ongewijzigd, alleen voor beheerders en nooit gecachet. `rmk_save_modellen()` schrijft alleen de opties `rmk_modellen` en `rmk_modellen_data`, het bestand in uploads/rmk en leegt de cache.
- **`tests/rmk-routes-test.py`** (nieuw): elke route met GET en POST, zonder inloggen, moet 401 of 404 geven zonder gegevens. Met `--na-136` moeten de vier verwijderde of uitgeschakelde routes 404 `rest_no_route` geven. Live (1.3.5): 0 fouten (alles 401).
- **Dataroute:** accepteert nu per model `ean` (8-14 cijfers) en een blok `bol` met alleen `product_url` (www.bol.com) en `afbeelding` (media.s-bol.com). Een Bol-prijs, een Bol-beoordeling of bol.com buiten dat blok wordt geweigerd.
- **Themabestand `data/modellen.json`:** gelijk aan live, plus het blok "bol". De nl-fabrikantpagina van M002 staat erin.

### 7. Modelgegevens
- **`scripts/excel_naar_json.py`:**
  - leest de kolom "Fabrikantpagina (URL)"; die gaat voor, en is hij leeg, dan zoals voorheen;
  - leest het blad Bol: `ean` en `bol` {product_url, afbeelding {url, breedte, hoogte}} uit de 550-px-URL;
  - geen prijzen, verkopers of beoordelingen;
  - gekoppeld: M001, M002, M004, M005, M006, M008, M011, M015, M016, M017, M018. Niet op Bol: M010.
- **Upload (`scripts/ronde30_upload.py`):** neemt alleen `fabrikant_url`, `ean` en `bol` over in de live gegevens; prijzen, scores, teksten en specificaties blijven zoals live. Een volledige nieuwe omzetting zou ook de prijzen van 7 oktober en de bronvermeldingen veranderen; dat is niet gedaan.
  - **Nu live:** EAN bij 11 modellen en de fabrikantpagina van M003 (nl.navimow.com i2 LiDAR; M003 staat op geen pagina).
  - **Het blok "bol" nog niet:** de live dataroute (1.3.5) weigert elke "bol.com". Na de activering van 1.3.6 hetzelfde script opnieuw draaien; het zet "bol" er dan bij.
  - **Weergave van alle 17 gepubliceerde pagina's vóór en na de upload: identiek.** Hub: 5 kaarten (92,7 / 87,3 / 80,5 / 78,6 / 60,9); pagina 1: 8 kaarten in dezelfde volgorde.

### 8. Tests
- **`tests/bol-test.php`** (nieuw, `php tests/bol-test.php`): 45 controles met nagebootste antwoorden in de vorm van het Logboek, via `tests/wp-stub.php` (nagebootste WordPress, geen netwerk). **Alles geslaagd.** Getest:
  - zonder constanten;
  - met constanten en de schakelaar uit;
  - schakelaar aan: aanbod van bol zelf, van een partner, geen aanbod (404), een foutmelding (500), een model zonder EAN;
  - verlopen prijs (11 uur 59 nog zichtbaar, 12 uur en 1 seconde weg);
  - token hergebruikt, nieuw token 30 s voor afloop, verlopen token (401), 429 met wachten;
  - de exacte linkvorm, subid alleen kleine letters, cijfers en koppeltekens, maximaal 10 verzoeken per seconde;
  - geen secrets of tokens in opslag, log of bol-status;
  - bol-status alleen voor beheerders;
  - de validatie van de dataroute.
- **Oude `tests/prijs-test.php` tegen de nieuwe code:** alles geslaagd tot het onderdeel over fotoplaatsvervangers. Dat gebruikt `inc/techniek.php`, die de nagebootste omgeving niet laadt; los van Bol.
- **Browser** (Chromium):
  - Opzet: de live pagina's met de 1.3.6-weergave via de echte themafuncties, Bol aan met nagebootste uitkomsten. Pagina 1 heeft 6 Bol-regels en de hub 4. De afbeeldingen van media.s-bol.com (hier geblokkeerd) vervangen door afbeeldingen van dezelfde afmetingen.
  - Op 360, 390, 768, 1024 en 1440 px: geen zijwaarts scrollen, geen scriptfouten, één h1, één advertentie-regel per pagina met Bol-knoppen, alle foto's geladen.
- **LCP** (zelfde opzet als ronde 22: mobiel, 150 ms, 1,6 Mbit/s, processor 4× trager, mediaan van 3, statische kopie):

  | Pagina | 1.3.5 | 1.3.6, Bol aan | LCP-element |
  |---|---|---|---|
  | Homepage | 1,16 s | 1,16 s | afbeelding `rmk-hero__bg` |
  | Pagina 1 (zonder draad) | 0,58 s | 0,62 s | H1 |
  | Pagina 12 (kosten) | 0,37 s | 0,40 s | H1 |

  Binnen de meetruis. De Bol-foto's staan onder de vouw en laden lui. Na het aanzetten opnieuw meten met PageSpeed Insights (met de echte foto's en de serverlatency).

### Om op te letten
- **CDN van Hostinger:** de cache in hPanel wordt niet automatisch geleegd na een prijsronde. Als de CDN pagina's bewaart, kan een Bol-prijs daar langer staan. Na het aanzetten controleren (header `x-hcdn-cache-status`) en zo nodig de CDN voor HTML uitzetten.
- **Twijfels uit het blad Bol** (Logboek 147): M004 heeft een serietitel, M018 een titelfout (55% tegenover 84%), en de specificaties van M015/M016 op bol.com wijken af. We tonen alleen prijs en foto, geen Bol-specificaties.

### Nog te doen
- [ ] Mandy: 1.3.6 uploaden en activeren; daarna de stappen in LANCERING.md, "Bol-koppeling aanzetten" (sleutels, echte cron, controle).
- [ ] Claude, na de activering: `scripts/ronde30_upload.py … --schrijf` (blok "bol") en `tests/rmk-routes-test.py --na-136`, en live controleren.
- [ ] Mandy: zeggen wanneer de schakelaar aan mag; dan `scripts/ronde30_affiliate_teksten.py --schrijf`.

## Ronde 31 (13 oktober 2026): 1.3.6 live, Bol-blok in de modelgegevens, routetest, CDN
**Niets gepubliceerd door mij.** Live gewijzigd door mij: alleen de modelgegevens (blok "bol"). `RMK_AFFILIATE_ACTIVE` niet aangezet, teksten niet toegepast.

### 1. Thema 1.3.6 live
- **Versie:** actief thema `robotmaaierkompas-child` **1.3.6** (REST). Het publieke `style.css` zegt Version 1.3.6, en de pagina's laden `rmk.js?ver=1.3.6`.
  - De CSS van het thema staat inline in de `<head>` (sinds 1.3.x, voor de LCP). Een apart stylesheet met `?ver=` bestaat daardoor niet.
- **Weergave van de 17 gepubliceerde pagina's: gelijk aan de meting na ronde 30.**
  - Hub: 5 kaarten (92,7 / 87,3 / 80,5 / 78,6 / 60,9).
  - Pagina 1: 8 kaarten in dezelfde volgorde.
  - Nergens een Bol-regel, -knop of -foto.
- **Navimow-pagina (#264):** 6 kaarten met dezelfde scores en prijsblokken als in ronde 29, geen Bol.

### Navimow-pagina gepubliceerd (niet door mij)
- #264 `/segway-navimow-robotmaaier/` is om **12:19:57 gepubliceerd** (revisie 12:19:47), op het account van Mandy. Om 12:1x was hij bij mijn eerste controle nog concept.
- Deze sessie heb ik geen enkel schrijfverzoek naar een pagina gedaan, alleen naar de modelgegevens (12:20:00).
- **Inhoud:** gelijk aan ronde 29, op één ding na: de blokeditor heeft het auteursblok-patroon uitgeschreven. Dat gebeurt bij openen en opslaan in de editor.
- **Openbaar sinds de publicatie:**
  - HTTP 200, geen noindex, in de page-sitemap (nu 18 URL's);
  - genoemd op de homepage en de auteurspagina ("Onlangs bijgewerkt"). Daarom verschilt de tekst van die twee pagina's van de eerste meting; kaarten en scores niet.
- Nu er 18 pagina's gepubliceerd zijn, zegt het statusoverzicht "17 van 17 (in totaal 18 gepubliceerde pagina's)". Dat is correct.
- **Gevolg:** de links vanaf de hub en pagina 1 naar deze pagina (ronde 28, `scripts/ronde28_links.py`) kunnen nu. **Niet gedaan:** dat is niet gevraagd.

### 2. Blok "bol" in de modelgegevens
- `scripts/ronde30_upload.py` (proefdraai, daarna `--schrijf`): alleen het veld `bol` bij de 11 gekoppelde modellen veranderd. De rest is gelijk aan vóór de upload (op de notatie 10.0/10 na). Opgeslagen om 12:20.

  | Model | EAN | bol-product-URL (pad) | foto (550 px) |
  |---|---|---|---|
  | M001 Navimow i105E | 8720254406855 | …/segway-navimow-i105e-robotmaaier-500-m-…/9300000177752213/ | 550×434 |
  | M002 Navimow i206 AWD | 8721264220318 | …/navimow-robotgrasmaaier-i206-600m2-nrtk-vision-awd/9300000251586857/ | 550×424 |
  | M004 Mova LiDAX Ultra 800 | 6977973410621 | …/mova-robotmaaier-lidax-ultra-serie-…/9300000262912566/ | 550×269 |
  | M005 Mova LiDAX Ultra 1200 | 6977973410782 | …/mova-lidax-ultra-1200-robotmaaier-…/9300000268371191/ | 550×357 |
  | M006 Eufy E15 Solo | 0194644388737 | …/eufy-robotgrasmaaier-e15-…/9300000275806803/ | 550×489 |
  | M008 Dreame A1 Pro | 6977328063366 | …/dreame-roboticmower-a1-pro-…/9300000225519126/ | 550×348 |
  | M011 Gardena Smart Sileno Free 800 | 4066407025219 | …/gardena-smart-sileno-free-800-robotmaaier/9300000222525633/ | 550×368 |
  | M015 Navimow i210 LiDAR Pro | 8721264220455 | …/navimow-i210-lidar-pro-robotgrasmaier-…/9300000251586859/ | 550×550 |
  | M016 Navimow i205 AWD | 8721264220424 | …/segway-navimow-i205-awd-robotmaaier-…/9300000269439068/ | 550×540 |
  | M017 Navimow i220 LiDAR Pro | 8721264220486 | …/segway-navimow-i220-lidar-pro-…/9300000266952936/ | 550×497 |
  | M018 Navimow X420 | 8721264221216 | …/segway-navimow-x420e-…/9300000266952935/ | 550×392 |

  - Alle 11 gelijk aan het blad Bol: EAN, product-URL en de afbeeldings-URL van 550 px.
  - **Geen blok "bol":** M003, M007, M010 (niet op Bol), M012, M013 en M014.
  - Geen Bol-prijzen, -verkopers of -beoordelingen in de gegevens, en "bol.com" komt alleen in het blok "bol" voor.
- **Na de upload:**
  - de 17 eerste-golfpagina's: kaarten, scores en volgorde gelijk;
  - 0 Bol-sporen (`partner.bol.com`, `media.s-bol.com`, `data-rmk-bol`, "Prijs bij bol.com") op de openbare pagina's en in de Navimow-pagina;
  - `/rmk/v1/bol-status` (ingelogd): constanten_aanwezig **false**, affiliate_actief **false**, geen ronde ingepland, alle 11 modellen "nog niet opgehaald";
  - statusoverzicht: alles OK, "Bol-koppeling: uit, constanten ontbreken".

### 3. Routetest (`python3 tests/rmk-routes-test.py --na-136`, zonder inloggen): 0 fouten
| Route | GET | POST |
|---|---|---|
| /rmk/v1 | 401 | 401 |
| /rmk/v1/status | 401 | 401 |
| /rmk/v1/modellen | 401 | 401 |
| /rmk/v1/bol-status | 401 | 401 |
| /rmk/v1/noindex | 404 rest_no_route | 404 rest_no_route |
| /rmk/v1/paginas | 404 rest_no_route | 404 rest_no_route |
| /rmk/v1/seo | 404 rest_no_route | 404 rest_no_route |
| /rmk/v1/huisstijl | 404 rest_no_route | 404 rest_no_route |

Geen gegevens in de antwoorden. De bouwroutes geven 404, omdat `RMK_BOUW_ACTIVE` niet aan staat.

### 4. Hostinger-CDN en de Bol-prijzen (onderzoek; niets aan de site gedaan)
**Gemeten** (zonder inloggen, 13 oktober 12:22-12:27, elke 10 s de hub):
- De CDN **cachet de HTML**: `x-hcdn-cache-status: HIT` met `age` tot **292 s**, op randservers in Boston (bos), Istanbul (imm) en Kuala Lumpur (kul). Na 5 minuten nog steeds HIT, dus de bewaartijd is minstens 5 minuten; het maximum is niet gemeten.
- De HTML-pagina's krijgen **geen Cache-Control-header** van de site. Statische bestanden krijgen `public, max-age=604800`.
- De REST-API krijgt al `Cache-Control: no-store`, `CDN-Cache-Control: no-store` en `X-LiteSpeed-Cache-Control: no-cache` (sinds 1.3.3).
- De `litespeed_control_set_ttl` uit 1.3.6 geldt alleen voor LiteSpeed op de server, **niet voor de CDN**. `litespeed_purge_all` na een prijsronde leegt ook alleen LiteSpeed.

**Wat Hostinger erover zegt** (de sites van Hostinger zijn hier geblokkeerd; dit komt uit zoekresultaten en is dus niet zelf nagelezen):
- De CDN legen kan in hPanel alleen voor de **hele site**: Websites > Prestaties > CDN > "Flush cache"; het werkt binnen seconden. Per URL legen kan alleen in Cache Manager, en dat is de LiteSpeed-cache, niet de CDN.
- De instellingen zijn **per domein**; een uitzondering per pagina of pad is niet gevonden.
- Hostinger zegt dat HTML "in het algemeen" niet aan de rand wordt gecachet. Mijn meting laat zien dat het hier wel gebeurt.
- De Hostinger-API heeft volgens kopieën van de documentatie `DELETE https://developers.hostinger.com/api/hosting/v1/accounts/{username}/websites/{domain}/cache/clear`. Volgens die beschrijving leegt dat de servercache en, als de CDN aan staat, ook de CDN. Niet gecontroleerd tegen de officiële documentatie.
- Of de CDN `Cache-Control`/`CDN-Cache-Control` van de site volgt, is niet gedocumenteerd gevonden.

**Voorstel** (in deze volgorde):
1. **Eerst meten, voordat de schakelaar aan gaat** (kan ik doen, alleen lezen): een uur lang elke minuut de hub opvragen om de echte bewaartijd van de CDN te vinden.
   - **Bewaartijd een paar minuten:** dan is het risico klein. De Bol-regel zegt zelf "bijgewerkt om …", en een prijs staat hooguit enkele minuten langer dan 12 uur.
2. **Kortere cache voor pagina's met een Bol-regel (thema 1.3.7, klein):** op pagina's met een Bol-regel `Cache-Control: public, max-age=0, s-maxage=600` en `CDN-Cache-Control: max-age=600` meesturen, en op andere pagina's niets veranderen.
   - Of de Hostinger-CDN dat volgt, testen we na de upload met dezelfde meting.
   - Volgt de CDN het niet, dan doet het ook geen kwaad.
3. **Automatisch legen na elke prijsronde (thema 1.3.7):** na `rmk_bol_ronde` de Hostinger-API aanroepen (bovenstaand endpoint).
   - Daarvoor zijn een **API-token van Hostinger** en de gebruikersnaam van het hostingaccount nodig, als constanten in wp-config.php (`RMK_HOSTINGER_API_TOKEN`, `RMK_HOSTINGER_USERNAME`); nooit in git.
   - Dat leegt vier keer per dag de hele site-cache. Bij deze kleine site is dat geen probleem; de eerste bezoeker daarna wacht iets langer.
4. **Werkt geen van beide:** de CDN voor het hele domein uitzetten. Die pagina's kunnen niet als enige buiten de CDN. De afbeeldingen en CSS hebben er dan ook geen baat meer van. De LCP opnieuw meten; LiteSpeed op de server cachet de pagina's nog steeds.

**Stappen voor Mandy in hPanel** (namen volgens de gevonden documentatie; kunnen iets afwijken):
- **Nu niets.**
- **Bij het aanzetten van de schakelaar:** Websites > robotmaaierkompas.nl > Prestaties > CDN > "Flush cache" (hele site). Daarna leeg ik de LiteSpeed-cache via de site.
- **Voor punt 3, alleen als je kiest voor automatisch legen:** in hPanel een API-token aanmaken (Account > API; alleen rechten voor hosting/cache als dat kan) en het token en de gebruikersnaam in wp-config.php zetten. Het token nooit in een chat of e-mail. Dan maak ik 1.3.7.
- **Voor punt 4:** Prestaties > CDN > CDN uitschakelen (per domein). Zeg het vooraf, dan meet ik de LCP voor en na.

### 5. Nog te doen door Mandy voor de activering (LANCERING.md, "Bol-koppeling aanzetten")
- [ ] **Secret roteren** in het Bol-Partnerplatform (het stond in een chatbericht, Logboek rij 136).
- [ ] **Constanten in wp-config.php:** `RMK_BOL_CLIENT_ID`, `RMK_BOL_CLIENT_SECRET`, `RMK_BOL_SITE_ID` (1549381). Nog niet aanwezig (bol-status: constanten_aanwezig false).
- [ ] **Echte cron** in hPanel (Geavanceerd > Cron-taken), één van de twee:
  - elke 15 minuten `wget -q -O /dev/null "https://robotmaaierkompas.nl/wp-cron.php?doing_wp_cron"` en `define( 'DISABLE_WP_CRON', true );`, of
  - elke 6 uur `wp --path=<WordPress-map> rmk bol-ronde`.
- [ ] Daarna laat je het mij weten. Ik controleer dan `/rmk/v1/bol-status`: de eerste ronde, de uitkomst per model, en dat er nog niets op de site staat.
- [ ] **CDN:** kies uit het voorstel hierboven (eerst meten aanbevolen).
- [ ] **Schakelaar:** zeggen wanneer `RMK_AFFILIATE_ACTIVE` aan mag. Dan pas ik de teksten toe (`scripts/ronde30_affiliate_teksten.py --schrijf`), en daarna leeg je de CDN.
- [ ] **Links:** wil je nu de links vanaf de hub en pagina 1 naar de (inmiddels gepubliceerde) Navimow-pagina? Dan draai ik `scripts/ronde28_links.py --schrijf`.

## Ronde 32 (13 oktober 2026): links naar de Navimow-pagina, CDN-meting, eerste Bol-ronde, labels pagina 1
**Gepubliceerd:** alleen de twee links in stap 1 (op al gepubliceerde pagina's). `RMK_AFFILIATE_ACTIVE` niet aangezet, teksten niet toegepast. Geen thema-zip.

### 1. Links naar /segway-navimow-robotmaaier/ (13:21:38 UTC)
- `scripts/ronde28_links.py --schrijf`:
  - **hub (#10):** eerste regel onder "Meer lezen";
  - **pagina 1 (#11):** alinea direct onder "De modellen een voor een".
  - Tekst: "Alle Segway Navimow-modellen die nu nieuw te koop zijn, met kosten: zie Segway Navimow robotmaaier." Beide pagina's zijn gepubliceerd gebleven.
- **Gecontroleerd:**
  - De ruwe inhoud vóór en na vergeleken: op #10 alleen die ene regel, op #11 die ene alinea (plus stap 4). Titel en meta gelijk.
  - Openbaar (met cacheparameter): de regel en `href="/segway-navimow-robotmaaier/"` staan op beide pagina's. Het doel geeft 200.
  - Kaarten, scorecellen en tabelrijen van de hub en pagina 1 zijn gelijk aan ronde 31.
  - Op / en de auteurspagina verandert alleen de datum in "Onlangs bijgewerkt".

### 4. Pagina 1 (#11) (13:21:44 UTC)
- `scripts/ronde32_upload.py --schrijf`: de **16 app-bronnen** (App Store en Google Play) hebben nu het label **"Appwinkel"** in plaats van "Handleiding". Verder niets veranderd (gecontroleerd met de omgekeerde vervanging).
- **"In onze functiescore staat dit model bovenaan":** was al gedaan in ronde 29. De analyse van M002 in de modelgegevens zegt "scoort dit model hoog (92,7)", en op pagina 1 en de hub staat "bovenaan" nergens meer.
  - Alleen de Navimow-pagina toont het nog, bij **M015** (i210 LiDAR Pro, 96,4). Daar klopt het; niet gewijzigd.

### 2. CDN-meting (13:12-14:12 UTC, elke minuut de hub en pagina 1, alleen lezen; 122 metingen)
- **Alles HTTP 200.** Hub: 43 keer HIT en 18 keer MISS op de CDN; pagina 1: 40 HIT, 21 MISS.
  - 13 randservers in Boston, Istanbul, Tokio en San Francisco.
  - Geen `Cache-Control` op de HTML.
  - **0 Bol-sporen** en geen Bol-regel (die bestaat nog niet).
- **Maximale bewaartijd:** de CDN serveerde de HTML tot **`age` 3140 s (52 minuten)** als HIT. Na de bekende wijziging was het maximum 2879 s (48 minuten, kopie van 13:23 nog op 14:11).
  - Binnen het meetuur is **geen enkele verlooptijd** gezien: de kopieën blijven staan tot ze worden vervangen. De echte bovengrens is dus langer dan 52 minuten en onbekend.
  - `age` loopt gelijk op met de tijd sinds de pagina opnieuw is opgebouwd (bij LiteSpeed). Het is de leeftijd van de kopie, niet alleen de tijd op de rand.
- **Gedrag bij de bekende wijziging (13:21:38-13:21:44):**
  - vanaf de eerste meting erna (13:22:20) gaf **elk antwoord de nieuwe versie** met de link, op alle randservers;
  - ook servers die om 13:21 nog de oude versie als HIT gaven (bos-edge8, imm-edge5);
  - **geen enkele keer de oude versie na de wijziging.**
  - Opslaan in WordPress leegt dus (via LiteSpeed) ook de kopieën op de Hostinger-CDN van die pagina.
- **Gevolg voor de Bol-prijzen:**
  - Zonder legen zou een pagina met Bol-regel minstens een uur, waarschijnlijk veel langer, de oude prijs tonen.
  - Met legen verdwijnt de oude versie wel meteen. De prijsronde roept na elke ronde `litespeed_purge_all` aan. Of dát ook de CDN leegt, is niet gemeten (opslaan van een pagina wel).
  - **Te controleren bij de eerste geslaagde ronde:** de tijd in de Bol-regel op de openbare pagina moet direct na de ronde de nieuwe tijd zijn. Dat kan ik meten zodra de schakelaar aan staat, of eerder op een testpagina.
  - **Restrisico:** valt de prijstaak weg (geen cron, geen ronde), dan wordt er niet geleegd, en kan een prijs na 12 uur nog op de CDN staan. Voorstel voor 1.3.7: bij het verlopen van een prijs (12 uur na de ronde) zelf de cache legen met een eenmalige geplande taak. Klein; nog niet gebouwd.

### 3. Eerste Bol-ronde (constanten door Mandy gezet)
- **`/rmk/v1/bol-status` (ingelogd):** constanten_aanwezig **true**, affiliate_actief **false**.
- **Eerste ronde: 13:15:06-13:15:07 UTC**, 11 verzoeken.
  - **Alle 11 modellen "fout: Token: HTTP 401"**: login.bol.com weigert de inloggegevens bij het ophalen van het token. 0 aanbiedingen, 0 verkopers, 0 geen-aanbod.
  - Er is dus nog niets opgehaald. Het log bevat geen sleutels of tokens.
- **Volgende ronde:** 19:13 UTC (vier keer per dag). Of er een echte cron staat, is van buiten niet te zien. Deze ronde is gestart door een bezoek (WP-Cron); de meting deed elke minuut een bezoek.
- **Statusoverzicht:** "Bol-koppeling: constanten aanwezig, Bol-regel verborgen" en "Bol-prijstaak draait": OK.
- **Geen Bol-regel op de site:** 0 Bol-sporen in alle 122 metingen. Ook na de ronde is de kaart gelijk aan 1.3.5.

### Om op te letten (voor Mandy)
- **Token 401:** controleer in wp-config.php `RMK_BOL_CLIENT_ID` en `RMK_BOL_CLIENT_SECRET`:
  - precies zoals in het Partnerplatform (Open API), zonder spaties of regeleinde binnen de aanhalingstekens;
  - bij een geroteerd secret het **nieuwe** secret.
  - Daarna draait de volgende ronde (19:13 UTC) vanzelf, of eerder met `wp rmk bol-ronde` (WP-CLI). Ik kijk dan opnieuw in bol-status.
- **Tijdzone van de site staat op UTC** (Instellingen > Algemeen: geen tijdzone). De Bol-regel zegt "bijgewerkt om HH:MM" in de tijd van de site, dus nu twee uur te vroeg voor Nederland.
  - **Vóór het aanzetten:** Instellingen > Algemeen > Tijdzone op "Amsterdam" zetten.
  - Dat verandert ook de tijden in het statusoverzicht en in bol-status. De datums op de pagina's blijven gelijk, op een wijziging rond middernacht na.
- **Verbetering voor 1.3.7 (klein, nog niet gebouwd):** na een mislukt token stopt de ronde nu niet. Hij probeert per model opnieuw een token (11 keer per ronde). Beter: na de eerste tokenfout stoppen.

### Nog te doen
- [ ] Mandy: Client ID en secret in wp-config.php controleren (401); de tijdzone op Amsterdam zetten.
- [ ] Claude: na de volgende ronde bol-status bekijken (aanbiedingen, verkopers, fouten).
- [ ] Bij de eerste geslaagde ronde met de schakelaar aan: meten of de CDN de nieuwe prijs meteen toont.
- [ ] Besluit over 1.3.7: cache legen bij het verlopen van een prijs; stoppen na een tokenfout.

## Ronde 33 (13 oktober 2026): bol-status na de nieuwe sleutels, thema 1.3.7 (prijs uit een niet-gecachete route)

### 1. Bol-status (ingelogd, 17:13 UTC)
- **Nog geen ronde na de update.** De laatste ronde is nog die van **13:15 UTC**: 11 verzoeken, alle 11 modellen "fout: Token: HTTP 401", 0 aanbiedingen.
  - Constanten aanwezig: true; affiliate_actief: false; volgende ronde: "2026-10-13 19:13".
  - Of de nieuwe sleutels werken, is dus nog niet te zien: er is sinds de update geen token gevraagd.
- **Tijdzone:** de REST-instellingen geven `timezone` nog leeg, en de tijden in bol-status zijn dezelfde als vóór de wijziging (13:15, 19:13). Met Amsterdam zou dat 15:15 en 21:13 zijn. De nieuwe tijdzone lijkt dus nog niet opgeslagen (of een UTC-verschuiving is gekozen in plaats van de stad).

### Checklist 401 (voor Mandy, zonder aannames over de waarden)
1. In wp-config.php staan `RMK_BOL_CLIENT_ID` en `RMK_BOL_CLIENT_SECRET` precies zoals in het Partnerplatform (Open API): geen spatie of regeleinde binnen de aanhalingstekens, gewone rechte aanhalingstekens.
2. Het secret is het **nieuwe** (na het roteren), niet het oude.
3. De constanten staan boven de regel `/* That's all, stop editing! */` en er staat geen tweede `define` van dezelfde naam.
4. Na 1.3.7: één ronde starten (POST `/wp-json/rmk/v1/bol-ronde`, ingelogd), of wachten op de volgende geplande ronde. Daarna bol-status bekijken.
5. Tijdzone: Instellingen > Algemeen > Tijdzone "Amsterdam" kiezen en op **Wijzigingen opslaan** klikken.

### 2. Thema 1.3.7
- **(a) Prijs niet meer in de HTML.** De Bol-regel in de HTML bevat alleen de knop, de bronregel en een leeg, verborgen prijsvak (`data-rmk-bol-prijs hidden`).
  - rmk.js haalt bij het laden `GET /wp-json/rmk/v1/bol-prijs?modellen=…` op (één verzoek per pagina, `cache: 'no-store'`, zonder cookies) en vult het vak met textContent: "**X euro**. Prijs bij bol.com, bijgewerkt om HH:MM[, via een partner van bol.com]."
  - De route is publiek en geeft alleen wat al op de site mag staan: status, model, EAN, prijs, prijs_tekst, verkoper, partner, tijd, tijd_tekst, geldig_tot. Geen links met site-ID, geen tokens, geen sleutels. Maximaal 30 model-ID's (`M` + 3-4 cijfers).
  - Headers via inc/techniek.php (alle /wp-json/): `Cache-Control: no-store, no-cache, private, max-age=0`, `CDN-Cache-Control: no-store`, `Surrogate-Control: no-store`, LiteSpeed no-cache.
  - Zonder JavaScript, bij een fout of bij een verlopen prijs (`geldig_tot` voorbij) blijft alleen de knop. Bij "geen aanbod" verdwijnt de hele regel.
  - Met de schakelaar uit: geen Bol-regel en geen `bolPrijsUrl` in de configuratie; de route geeft dan een lege lijst.
  - Daarmee is het CDN-probleem uit ronde 32 (HTML > 52 minuten op de CDN) voor de prijs opgelost; een oude HTML-kopie bevat geen prijs meer.
- **(b) Stoppen na de eerste tokenfout.** De ronde vraagt eerst één token. Mislukt dat, dan stopt de ronde (1 verzoek in plaats van 11), blijft de vorige uitkomst per model staan, en meldt bol-status `gestopt: true` met "Gestopt na de eerste tokenfout (…). Geen aanbiedingen opgehaald; controleer RMK_BOL_CLIENT_ID en RMK_BOL_CLIENT_SECRET." Ook een tokenfout halverwege (vernieuwen) stopt de ronde.
- **(c) Beheerroute** `POST /wp-json/rmk/v1/bol-ronde`: alleen `manage_options`, nooit gecachet; start één ronde en geeft het rondelog terug (aantallen en melding, geen sleutels).
- **(d) Routetest** `tests/rmk-routes-test.py`: alle rmk-routes zonder inloggen 401/404 en zonder gegevens, behalve GET bol-prijs: die mag 200 geven, maar alleen met de toegestane velden, zonder verboden tekst (partner.bol.com, secret, token, …) en met no-store in Cache-Control én CDN-Cache-Control. Nieuwe vlag `--na-137` (bol-prijs 200, POST bol-ronde 401). Live op 1.3.6: 0 fouten.
- Versie 1.3.7 in robotmaaierkompas-setup.php, style.css en README.

### 3. Tests (niets gepubliceerd; RMK_AFFILIATE_ACTIVE niet aangezet; teksten niet toegepast)
- **`php tests/bol-test.php`: 59 OK, alles geslaagd.** Nagebootst: bol zelf, partner, geen aanbod, fout (500), verlopen token (vernieuwen), geweigerd token (stopt na 1 verzoek, store blijft), verlopen prijs, schakelaar uit en aan, beheerroute start een ronde, geen prijs in de HTML.
- **Browser (Chromium, statische kopie van de live pagina's met de 1.3.7-weergave, nagebootste prijsroute), pagina 1:**

  | Scenario | Uitkomst |
  |---|---|
  | ok | 5 regels met prijs, M011 "via een partner van bol.com", M005 (fout in de ronde) alleen de knop; 1 verzoek |
  | geen aanbod M005 | regel M005 verborgen, de rest met prijs |
  | route geeft 500 | alle 6 alleen de knop, 0 JavaScript-fouten |
  | prijzen verlopen | alle 6 alleen de knop |
  | zonder JavaScript | alle 6 alleen de knop |
  | schakelaar uit | 0 Bol-regels, 0 verzoeken naar de route |
- **Breedtes 360, 390, 768, 1024, 1440 px** (pagina 1, hub, home, kosten): nergens horizontaal scrollen, 0 fouten; pagina 1 6 regels (5 met prijs), hub 4 (3 met prijs).
- **LCP** (zelfde opzet als ronde 22/30: mobiel, 150 ms, 1,6 Mbit/s, processor 4× trager, mediaan van 3; prijsroute met 300 ms vertraging):

  | Pagina | 1.3.6, Bol aan | 1.3.7, Bol aan | LCP-element |
  |---|---|---|---|
  | Home | 1,16 s | 1,11 s | hero-afbeelding |
  | Pagina 1 (zonder draad) | 0,47 s | 0,52 s | H1 |
  | Pagina 12 (kosten) | 0,32 s | 0,31 s | H1 |

  Binnen de meetruis; de prijs komt later binnen maar is nooit het LCP-element.
- PHP-lint van alle bestanden en `node --check rmk.js`: geen fouten. Zip gecontroleerd: alleen de plaatsaanduiding `'…'` bij de constanten, geen xlsx en geen tekstwijzigingen-md.

### Na de upload van 1.3.7 (Claude)
1. `python3 tests/rmk-routes-test.py --na-136 --na-137` (verwacht 0 fouten; controleert ook de no-store-headers van bol-prijs op de CDN).
2. Ingelogd POST `/rmk/v1/bol-ronde`, dan `/rmk/v1/bol-status`: werken de nieuwe sleutels (aanbiedingen, verkopers), of "gestopt na de eerste tokenfout"?
3. Met de schakelaar nog uit blijft de site gelijk: geen Bol-regel, geen verzoek naar de prijsroute.

### Nog te doen
- [ ] Mandy: 1.3.7 uploaden; de checklist hierboven bij een nieuwe 401; tijdzone opslaan.
- [ ] Claude: na de upload de drie stappen hierboven.
- [ ] Schakelaar en teksten (ronde30_affiliate_teksten.py) pas op Mandy's woord.

## Ronde 34 (13 oktober 2026): na de upload van 1.3.7, eerste ronde via de beheerroute

Tijden in Amsterdamse tijd. Niets gepubliceerd; RMK_AFFILIATE_ACTIVE niet aangezet; teksten niet toegepast.

### 1. Controles
- **Actief thema 1.3.7**; tijdzone van de site nu `Europe/Amsterdam` (de tijden in bol-status zijn mee verschoven: de ronde van 13:15 UTC staat nu als 15:15).
- **`python3 tests/rmk-routes-test.py --na-136 --na-137`: 0 fouten.**
  - Alle rmk-routes zonder inloggen 401 (`rest_forbidden`) of, voor noindex/paginas/seo/huisstijl, 404 `rest_no_route`.
  - GET `/rmk/v1/bol-prijs`: 200 met 0 modellen (schakelaar uit), `Cache-Control: no-store, no-cache, private, max-age=0`, CDN `DYNAMIC` (niet gecachet).
  - POST `/rmk/v1/bol-ronde` zonder inloggen: 401.

### 2. Eén ronde via POST /rmk/v1/bol-ronde (ingelogd, 19:24:21)
- **Token: HTTP 401.** De ronde **stopte na 1 verzoek** (het tokenverzoek), zoals bedoeld in 1.3.7: "Gestopt na de eerste tokenfout (Token: HTTP 401). Geen aanbiedingen opgehaald; controleer RMK_BOL_CLIENT_ID en RMK_BOL_CLIENT_SECRET."
- **Per model:** geen aanbod en geen verkoper opgehaald. Alle 11 (M001, M002, M004, M005, M006, M008, M011, M015-M018) houden de uitkomst van de vorige ronde (15:15): "fout: Token: HTTP 401", niet op de site.
- Constanten aanwezig: true; affiliate_actief: false; volgende geplande ronde: 21:13.
- Het antwoord en bol-status bevatten geen sleutels of tokens.

### 3. Geen Bol-regel op de site (schakelaar uit)
- Alle 18 openbare adressen (home en 17 pagina's), elk twee keer (gewoon en met een extra parameter om de CDN-kopie te omzeilen): HTTP 200, thema 1.3.7.
- **0 keer** `data-rmk-bol`, `rmk-offer--bol`, "Bekijk bij bol.com", `partner.bol.com`, `media.s-bol.com`, `bolPrijsUrl` of `bol-prijs`. Ook geen advertentie-regel in `<main>`; `rmk-affnote` komt alleen voor als CSS-klasse in de inline stijl.

### Checklist 401 (bijgewerkt; tijdzone en constanten zijn al gecontroleerd)
1. Staan de waarden tussen **dubbele** aanhalingstekens, zet ze dan tussen **enkele**: binnen dubbele aanhalingstekens vervangt PHP een `$` met wat erop volgt.
2. Client ID en secret komen uit **hetzelfde, actieve sleutelpaar**, aangemaakt voor de Open API (Marketing Catalog) in het Partnerplatform van het account met de site-ID. Na roteren of een nieuw paar: beide waarden van het nieuwe paar.
3. Gelijk aan het Partnerplatform: geen spatie, tab of regeleinde vóór of na de waarde binnen de aanhalingstekens; niets weggevallen bij kopiëren.
4. Om te scheiden of het aan de sleutels of aan de site ligt: laat het onderzoeksvenster (dat de sleutels mag zien) met dezelfde waarden één tokenverzoek doen. Lukt dat daar wel, dan ligt het aan de site; zeg het mij.
5. Daarna: zeg het, dan start ik één ronde via de beheerroute (of wacht op 21:13) en kijk in bol-status.

### Nog te doen
- [ ] Mandy: checklist 401.
- [ ] Claude: daarna één ronde starten en bol-status bekijken.
- [ ] Schakelaar en teksten pas op Mandy's woord.

## Ronde 35 (13 oktober 2026): eerste geslaagde Bol-ronde

Tijden in Amsterdamse tijd. Niets gepubliceerd; RMK_AFFILIATE_ACTIVE niet aangezet; teksten niet toegepast.

### 1. Ronde via POST /rmk/v1/bol-ronde (ingelogd, 19:29:59-19:30:03)
- **Token geslaagd.** 12 verzoeken (1 token + 11 aanbiedingen), niet gestopt, geen melding.
- **8 met aanbod, 3 zonder aanbod, 0 ongeldig, 0 fout.** Geldig tot 14 oktober 07:29/07:30 (12 uur).

  | Model | Uitkomst | Prijs | Verkoper |
  |---|---|---|---|
  | M001 Segway Navimow i105E | aanbod | 799 | bol.com |
  | M002 Segway Navimow i206 AWD | aanbod | 899 | bol.com |
  | M004 Mova LiDAX Ultra 800 | geen aanbod (404 "Unable to find offer") | – | – |
  | M005 Mova LiDAX Ultra 1200 | aanbod | 763 | bol.com |
  | M006 Eufy E15 Solo | aanbod | 824 | bol.com |
  | M008 Dreame A1 Pro | aanbod | 719 | bol.com |
  | M011 Gardena Smart Sileno Free 800 | aanbod | 799,99 | JGStore.nl (partner van bol.com) |
  | M015 Segway Navimow i210 LiDAR Pro | geen aanbod (404) | – | – |
  | M016 Segway Navimow i205 AWD | geen aanbod (404) | – | – |
  | M017 Segway Navimow i220 LiDAR Pro | aanbod | 2.439 | bol.com |
  | M018 Segway Navimow X420 | aanbod | 2.906 | bol.com |

- Alle modellen `op_de_site: false` (schakelaar uit). Constanten aanwezig; affiliate_actief false; volgende geplande ronde 21:13.
- Antwoord en bol-status bevatten geen sleutels of tokens.

### 2. Niets op de site
- 18 openbare adressen, elk twee keer (gewoon en langs de CDN-kopie): **0** Bol-regels, knoppen, `partner.bol.com`, `media.s-bol.com`, `bolPrijsUrl`, prijsteksten of verkopersnamen; geen advertentie-regel in `<main>`.
- Publieke prijsroute GET `/rmk/v1/bol-prijs`: 200 met **0 modellen** (schakelaar uit), no-store, CDN `DYNAMIC`.
- Routetest `--na-136 --na-137`: 0 fouten.

### Nog te doen
- [ ] Mandy: besluit over de schakelaar. Bij aan: tegelijk `scripts/ronde30_affiliate_teksten.py --schrijf` en de CDN-meting uit ronde 32 (prijs direct zichtbaar).
- [ ] Ter info: M004, M015 en M016 hebben nu geen aanbod bij bol.com; met de schakelaar aan krijgen die kaarten geen Bol-regel.

## Ronde 36 (13-14 oktober 2026): activering voorbereid, controle van de geplande Bol-rondes

Tijden in Amsterdamse tijd. Niets gepubliceerd; RMK_AFFILIATE_ACTIVE niet aangezet; teksten niet toegepast; geen script met `--schrijf` gedraaid.

### 1. Activering voorbereid (niet uitgevoerd)
- **`scripts/affiliate_teksten_lib.py`** (nieuw): alle oude en nieuwe teksten op één plek, plus zoeken/vervangen en schrijven.
  - Nieuwe teksten letterlijk uit tekstwijzigingen-affiliate-live.md (automatisch vergeleken: alle paginateksten komen overeen; het md-bestand staat niet in de repository).
  - Oude teksten zoals ze nu live staan (#81 eerste alinea, #82 punt "Winkels en affiliatenetwerken", #83 tabelrij letterlijk overgenomen).
  - Elke stap zoekt zijn tekst; niet precies één keer gevonden → melding en **niets geschreven**. Al toegepast → "al gedaan" (nogmaals draaien verandert niets).
- **`scripts/ronde30_affiliate_teksten.py`** (herschreven): punten 1-8 uit het md-bestand (#81, #77, #80, #76, footer, #82, #83, advertentie-tekst).
  - Proefdraai nu: **geen meldingen**, alle 8 "Was"-teksten precies één keer gevonden; thema 1.3.7; advertentie-tekst nu leeg.
  - Met `--schrijf`: eerst een volledige kopie van de zeven teksten en de instelling in `backups/` (niet in git), dan alleen `content` sturen (pagina's houden hun status), en per pagina controleren dat de inhoud is zoals bedoeld.
- **`scripts/ronde30_affiliate_terug.py`** (nieuw): zet de oude teksten terug en maakt de advertentie-tekst leeg; vervangt alleen de nieuwe tekststukken, andere wijzigingen blijven. Noodgeval: `--backup <kopie>` zet de volledige inhoud uit de kopie terug.
  - Proefdraai nu: alles "al gedaan" (de oude teksten staan er).
  - **Heen-en-terugtest in het geheugen** op de live inhoud: aanzetten en daarna terugdraaien geeft **exact** de huidige inhoud van alle zeven teksten (ook de links naar de affiliate-melding); twee keer aanzetten of twee keer terugdraaien verandert niets.
- **`scripts/bol_regel_controle.py`** (nieuw, alleen lezen): per model de uitkomst van de laatste ronde, of de Bol-regel met de schakelaar aan zichtbaar zou zijn, wat de publieke prijsroute geeft, op welke pagina's de kaart staat en waar nu een Bol-regel staat. Van elke gevonden link alleen de **vorm** (`https://partner.bol.com/click/click?p=2&t=url&s=<SITE_ID>&f=api&url=https://www.bol.com/nl/nl/p/…&name=<modelnaam>&subid=<paginaslug>`), plus `rel="sponsored nofollow"` en de bronregel. **Volgt geen link**; de site-ID wordt nooit getoond.
  - Getest op de 1.3.7-weergave uit ronde 33 (6 regels, alle vormen goed) en op een foute link (verkeerde subid en url-host worden gemeld).
  - Live nu (schakelaar uit): **0 Bol-regels op 18 adressen, prijsroute leeg, geen fouten.** Met de schakelaar aan zouden er Bol-regels komen bij M001, M002, M005, M006, M008, M011, M017, M018; niet bij M004, M015, M016 (geen aanbod).

### Volgorde bij het aanzetten (pas op Mandy's woord)
1. Mandy: `define( 'RMK_AFFILIATE_ACTIVE', true );` in wp-config.php.
2. Claude: `python3 scripts/ronde30_affiliate_teksten.py` (proefdraai, geen meldingen?) en dan `--schrijf`.
3. LiteSpeed-cache en CDN legen; `python3 scripts/bol_regel_controle.py` (verwacht: Bol-regels precies op de kaarten van de 8 modellen met aanbod, alle links in de juiste vorm, 0 fouten).
4. **Terug:** Mandy haalt de regel `RMK_AFFILIATE_ACTIVE` weg; Claude draait `python3 scripts/ronde30_affiliate_terug.py --schrijf`; cache legen; controle opnieuw (0 Bol-regels).

### 2. Controle geplande rondes (uitgevoerd vrijdag 16 oktober, 21:23)
- **De geplande controles van 13 en 14 oktober (21:45, 03:45, 09:45) zijn niet op tijd uitgevoerd**: deze werksessie lag stil en kreeg ze pas op 16 oktober 21:22. Tussenstanden zijn daardoor niet vastgelegd.
- **bol-status bij aankomst (21:23:00):** laatste ronde nog steeds de handmatige van **13 oktober 19:29:59-19:30:03**; volgende ronde "**13 oktober 21:13**", dus ruim drie dagen te laat. Statusoverzicht: "Bol-prijstaak draait (laatste ronde minder dan 7 uur geleden)": **niet OK**.
- **Conclusie: de rondes van 13 oktober 21:13 en alle daarna (14, 15 en 16 oktober, vier per dag) zijn overgeslagen.** De prijzen waren vanaf 14 oktober 07:30 verlopen (met de schakelaar aan hadden de kaarten alleen de knop getoond).
  - Waarschijnlijke oorzaak: WP-Cron start alleen als een bezoek PHP laat draaien. De pagina's komen uit de LiteSpeed-cache en de CDN, dus gewone bezoeken starten de taak niet (of `DISABLE_WP_CRON` staat aan zonder echte cron). Van buiten niet te onderscheiden.
- **Na een aanroep van `wp-cron.php` (21:23)** startte de achterstallige ronde meteen: **21:23:21-21:23:22, 12 verzoeken, token geslaagd, 8 aanbod, 3 geen aanbod, 0 fout**; volgende ronde 17 oktober 03:13. Die aanroep is precies wat de cron in hPanel moet doen.

  | Model | Prijs | Verkoper | Verschil met 13-10 |
  |---|---|---|---|
  | M001 Segway Navimow i105E | 799 | bol.com | gelijk |
  | M002 Segway Navimow i206 AWD | 899 | bol.com | gelijk |
  | M004 Mova LiDAX Ultra 800 | geen aanbod | – | gelijk |
  | M005 Mova LiDAX Ultra 1200 | 763 | bol.com | gelijk |
  | M006 Eufy E15 Solo | 814 | Startbuy.eu (partner) | was 824 bij bol.com |
  | M008 Dreame A1 Pro | 719 | bol.com | gelijk |
  | M011 Gardena Smart Sileno Free 800 | 633 | bol.com | was 799,99 bij JGStore.nl (partner) |
  | M015 Segway Navimow i210 LiDAR Pro | geen aanbod | – | gelijk |
  | M016 Segway Navimow i205 AWD | geen aanbod | – | gelijk |
  | M017 Segway Navimow i220 LiDAR Pro | 2.379 | bol.com | was 2.439 |
  | M018 Segway Navimow X420 | 2.759 | bol.com | was 2.906 |

- **Niets van Bol op de site:** `scripts/bol_regel_controle.py`: schakelaar uit, 0 Bol-regels op 18 openbare adressen, publieke prijsroute leeg, geen fouten; alle modellen `op_de_site: false`.

### Wat Mandy met de cron moet doen (vóór het aanzetten)
1. hPanel > Geavanceerd > **Cron-taken**, een nieuwe taak **elke 15 minuten** (LANCERING.md stap 3), één van beide:
   - `wget -q -O /dev/null "https://robotmaaierkompas.nl/wp-cron.php?doing_wp_cron"`, en in wp-config.php `define( 'DISABLE_WP_CRON', true );` (zodat bezoeken het niet meer hoeven te doen); of
   - elke 6 uur `wp --path=<map van WordPress> rmk bol-ronde` (als WP-CLI beschikbaar is).
2. Staat `DISABLE_WP_CRON` al in wp-config.php zonder zo'n taak, dan is dat de oorzaak: de taak toevoegen.
3. Daarna controleer ik na twee geplande rondes (bijvoorbeeld 03:13 en 09:13) of bol-status ze laat zien en het statusoverzicht weer OK is.

### Nog te doen
- [ ] Mandy: echte cron in hPanel.
- [ ] Claude: daarna twee rondes controleren. De schakelaar pas aan als de rondes vanzelf draaien.

## Ronde 37 (16-17 oktober 2026): rondes na het corrigeren van de cron

Tijden in Amsterdamse tijd. Mandy: cron in hPanel elke 15 minuten op `wp-cron.php`, `DISABLE_WP_CRON` gezet. Niets gepubliceerd; RMK_AFFILIATE_ACTIVE niet aangezet; teksten niet toegepast.

### Eerste lezing (16 oktober 21:47)
- **Nog geen geplande ronde na het instellen van de cron.** Laatste ronde is nog die van **21:23:21** (door mijn aanroep van `wp-cron.php` in ronde 36, niet door de cron): 8 aanbod, 3 geen aanbod, 0 fout. Volgende geplande ronde: **17 oktober 03:13**.
- Statusoverzicht "Bol-prijstaak draait": OK. (Kleine onvolkomenheid in het thema: de info-tekst zegt ook bij OK "Te oud: stel een echte cron in"; alleen tekst, niet aangepast.)
- Controles ingepland om 03:35 en 09:35, zonder zelf een ronde te starten of `wp-cron.php` aan te roepen.

### Controle 1 (17 oktober 03:36, op tijd)
- **Geplande ronde vanzelf gedraaid: 03:15:02-03:15:04** (gepland 03:13; de cron van elk kwartier pakte hem op). Niet door mij gestart; geen `wp-cron.php` aangeroepen.
- 12 verzoeken, token geslaagd, **8 aanbod, 3 geen aanbod, 0 fout**, niet gestopt. Volgende: 09:13.
- Per model gelijk aan 16-10 21:23: M001 799, M002 899, M005 763, M008 719, M011 633, M017 2.379, M018 2.759 (bol.com); M006 814 (Startbuy.eu, partner); M004, M015, M016 geen aanbod.

### Controle 2 (17 oktober 09:36, op tijd) en conclusie
- **Geplande ronde vanzelf gedraaid: 09:15:03-09:15:04** (gepland 09:13). Niet door mij gestart; geen `wp-cron.php` aangeroepen. 12 verzoeken, token geslaagd, **8 aanbod, 3 geen aanbod, 0 fout**. Volgende: 15:13. Statusoverzicht "Bol-prijstaak draait": OK.
- **Twee geplande rondes achter elkaar vanzelf gedraaid: 03:15 en 09:15**, elk ongeveer 2 minuten na het geplande tijdstip (de cron draait elk kwartier). Geen ronde overgeslagen; beide controles op tijd uitgevoerd.
- **Per model in beide rondes gelijk** (ook gelijk aan 16-10 21:23): M001 799, M002 899, M005 763, M008 719, M011 633, M017 2.379, M018 2.759 bij bol.com; M006 814 bij Startbuy.eu (partner); M004, M015, M016 geen aanbod. Geen verschillen.
- **Niets van Bol op de site:** `scripts/bol_regel_controle.py`: schakelaar uit, 0 Bol-regels op 18 openbare adressen, publieke prijsroute leeg, geen fouten.
- De cron werkt. Volgende stap (alleen op Mandy's woord): de schakelaar aan en de teksten toepassen volgens de volgorde in ronde 36.

### Herbevestiging op verzoek (17 oktober 12:12)
- bol-status nu: laatste ronde **09:15** (8 aanbod, 3 geen aanbod, 0 fout, 12 verzoeken), volgende 15:13; statusoverzicht OK. Dit klopt met de vastgelegde lezingen van 03:36 (ronde **03:15**) en 09:36 (ronde **09:15**).
- bol-status bewaart alleen de laatste ronde; de ronde van 03:15 is bevestigd via de lezing van 03:36. Tussen 03:15 en 09:15 was geen andere ronde gepland, dus niets overgeslagen.
- Per model ongewijzigd (zie controle 2). `scripts/bol_regel_controle.py`: 0 Bol-regels op 18 adressen, prijsroute leeg, geen fouten.

## Ronde 38 (17 oktober 2026): schakelaar aan, controle vóór de teksten (gestopt bij afwijking)

Tijden in Amsterdamse tijd. Mandy: `RMK_AFFILIATE_ACTIVE` aan. Stap 2 (teksten) en stap 3 **niet** uitgevoerd; niets geschreven op de site.

### 1. Controle per model (12:24)
- **Afwijking:** `scripts/bol_regel_controle.py` op de gewone adressen: schakelaar **aan**, publieke prijsroute geeft de prijzen, maar **0 Bol-regels** op 18 adressen → 8 fouten (kaarten van M001, M002, M005, M006, M008, M011, M017, M018 zonder Bol-regel).
- **Oorzaak:** de pagina's komen nog uit de **LiteSpeed-cache** van vóór het aanzetten (`x-litespeed-cache: hit`, geen `data-rmk-bol`, geen `bolPrijsUrl`). Dezelfde pagina met een extra parameter (`?rmkvers=…`, `x-litespeed-cache: miss`) heeft wél 6 Bol-regels en de advertentie-regel. De cache is na het aanzetten niet geleegd (LANCERING stap 6).
- **Verse weergave (alleen lezen, met extra parameter, links niet gevolgd): alles goed, 0 fouten.**
  - **14 Bol-regels**: precies op de kaarten van de 8 modellen met aanbod (hub 4, pagina 1 6, Navimow-pagina 4). **M004, M015, M016 geen Bol-regel.**
  - Elke link: `https://partner.bol.com/click/click?p=2&t=url&s=<SITE_ID>&f=api&url=https://www.bol.com/nl/nl/p/…&name=<modelnaam>&subid=<paginaslug>`, overal dezelfde (numerieke) site-ID, `rel="sponsored nofollow"`, bronregel "Je gaat naar bol.com. Bron: bol.com.".
  - **Prijs uit de route** (1 verzoek naar `/rmk/v1/bol-prijs` per pagina), bijvoorbeeld "899 euro. Prijs bij bol.com, bijgewerkt om 09:15."; **M006: "814 euro. Prijs bij bol.com, bijgewerkt om 09:15, via een partner van bol.com."**
  - Advertentie-regel boven de eerste Bol-knop: nog de standaardtekst van het thema ("Advertentie: via deze knoppen krijgen wij mogelijk een commissie. …"); de tekst uit het md-bestand komt pas met stap 2.
  - 390 en 1440 px: geen horizontaal scrollen, 0 JavaScript-fouten. Foto's: `img` met de oorspronkelijke URL op media.s-bol.com; laden kon niet in de sandbox (die host is daar geblokkeerd), dus de foto zelf is niet visueel gecontroleerd.

### Wat nodig is om verder te gaan
1. Mandy (of na akkoord ik): **LiteSpeed-cache legen** (LiteSpeed Cache > Alles legen) en **CDN legen** (hPanel > Prestaties > CDN > Cache legen).
2. Daarna opnieuw `scripts/bol_regel_controle.py` op de gewone adressen (verwacht: 14 Bol-regels, 0 fouten), en pas dan stap 2 (teksten) en stap 3.

## Ronde 39 (17 oktober 2026): Bol-regels live, affiliateteksten toegepast

Tijden in Amsterdamse tijd. Mandy: LiteSpeed- en CDN-cache geleegd na het aanzetten van `RMK_AFFILIATE_ACTIVE`.

### 1. Controle per model op de gewone adressen (12:35, zonder cache-omzeiling)
- `scripts/bol_regel_controle.py`: **14 Bol-regels, 0 fouten**: hub 4, pagina 1 6, Navimow-pagina 4, precies op de kaarten van M001, M002, M005, M006, M008, M011, M017, M018. **M004, M015, M016 geen Bol-regel.**
- Elke link `https://partner.bol.com/click/click?p=2&t=url&s=<SITE_ID>&f=api&url=https://www.bol.com/nl/nl/p/…&name=<modelnaam>&subid=<paginaslug>`, één numerieke site-ID, `rel="sponsored nofollow"`, bronregel aanwezig. Links niet gevolgd.

### 2. Affiliateteksten (12:36)
- `scripts/ronde30_affiliate_teksten.py` proefdraai: **geen meldingen**. Daarna `--schrijf`:
  - #76, #77, #80, #81, #82, #83 opgeslagen (status publish blijft publish; inhoud telkens zoals bedoeld), footer opgeslagen, `rmk_advertentie_tekst` = "Advertentie: via deze knoppen naar bol.com krijgen wij mogelijk een commissie. Dat verandert de score niet."
  - Kopie van de oude teksten: `backups/affiliate-voor-20261017-103623.json` (niet in git, alleen in deze werkomgeving; `ronde30_affiliate_terug.py` werkt ook zonder deze kopie).
- **Controle op alle 18 adressen** (tekst zonder HTML, verse weergave én gewone adressen):
  - "Op dit moment verdienen we niets": **0 keer**, op geen enkele pagina.
  - Nieuwe footer ("Wij kunnen een commissie ontvangen bij aankopen via links naar bol.com.") op **18 van 18**.
  - Nieuwe zinnen op hun pagina: affiliate-melding (eerste alinea en slotalinea), over-ons, colofon, hoe-we-beoordelen ("…volgt de score, niet de commissie."), privacy (cookie van bol.com), cookies (rij "Cookies van bol.com na een klik").
  - Advertentie-regel met de nieuwe tekst en bronvermelding "Je gaat naar bol.com. Bron: bol.com." op de 3 pagina's met Bol-regels (hub, pagina 1, Navimow).

### 3. Na het opslaan
- Mandy moet de **caches opnieuw legen** (LiteSpeed en CDN), omdat de footer op elke pagina staat.
- Gewone adressen direct na het opslaan (12:37, nog vóór dat legen): alle 18 HTTP 200, LiteSpeed `miss`, CDN `MISS`, overal de nieuwe teksten en 0 oude zinnen (het opslaan van de footer leegde kennelijk de LiteSpeed-cache al). Bol-controle: 14 regels, 0 fouten. Routetest `--na-136 --na-137`: **0 fouten**.
- **Niets ging mis; het terugdraaiscript is niet gebruikt.**

### Voor de volgende themaversie
- **Productfoto van bol.com laadt niet:** het fotovak verbergen en alleen de specificatiekaart tonen. Dus geen alt-tekst in een grijs vak (zoals in de schermafbeeldingen van ronde 38, waar media.s-bol.com geblokkeerd was). Bijvoorbeeld met `onerror` op de `img` (of een kleine listener in rmk.js) die het hele fotoblok inclusief "Foto: bol.com" weghaalt; zonder JavaScript blijft het gewone gedrag.

## Ronde 40 (17 oktober 2026): nieuwe Navimow-modellen op pagina 1 en de hub

Bron: tekstwijzigingen-navimow-op-pagina1-en-hub.md (Mandy, 17 oktober; niet in de repository). Uitgevoerd met `scripts/ronde40_navimow_p1_hub.py` via de WordPress-API en de dataroute, zonder thema-zip. Pagina's bleven gepubliceerd.

### Kopieën
- `backups/pagina10-11-voor-20261017-110533.json` en `backups/ronde40-voor-20261017-112010.json` (inhoud, status en meta van #10 en #11 vóór de wijziging; niet in git, alleen in deze werkomgeving).

### A. Pagina 1 (#11)
- Metabeschrijving: "Acht robotmaaiers…" → "Tien robotmaaiers…".
- "acht" → "tien" op 2 plekken: korte antwoord ("We vergeleken tien modellen…") en kop "Vergelijking van de tien modellen". De zinnen "De volledige vergelijking van acht modellen" en "de acht modellen" uit het md staan niet op pagina 1.
- "Welke past bij jouw tuin?": rij "Tuin tot ongeveer 1.000 m² met veel obstakels | Segway Navimow i210 LiDAR Pro | LiDAR met camera en netwerk-RTK, helling 55% volgens de handleiding" direct onder de eerste rij.
- Scoretabel: `[rmk_scoretabel modellen="M015,M002,M016,M010,M005,M004,M008,M001,M006,M011"]`. Kaarten M015 (vóór) en M016 (na) de i206, hetzelfde kaartskelet als op de Navimow-pagina; het thema vult analyse, plus- en minpunten en de knop.
- "Hoogste functiescore" bij M002: komt op pagina 1 niet voor; niets te vervangen. De kaart van M015 zegt "In onze functiescore staat dit model bovenaan" (uit de modelgegevens).

### B. Hub (#10)
- Metabeschrijving "Vijf keuzes…" → "Zes keuzes…"; korte antwoord "vijf modellen" → "zes modellen".
- "In een oogopslag": rij "Tuin tot ongeveer 1.000 m² met veel obstakels, zonder antenne | Segway Navimow i210 LiDAR Pro | 96,4" onder de eerste rij; de modelnaam linkt, net als de andere rijen, naar de kaart (`#p-segway-navimow-i210-lidar-pro`).
- Na de i206-kaart: H3 "Tuin tot 1.000 m² met veel obstakels: Segway Navimow i210 LiDAR Pro", kaart M015, "Waarom deze:" zoals in het md.
- "Alle acht modellen naast elkaar" → "Alle tien modellen naast elkaar". **Extra (zelfde verwijzing naar pagina 1):** in "Meer lezen" "Robotmaaier zonder draad: de acht modellen vergeleken." → "de tien modellen vergeleken.".
- Niet gewijzigd: "Waarom deze" bij de i206 ("een van de hoogste functiescores in onze selectie"); klopt nog (92,7, tweede plaats).

### C. Controle (live, na het legen van LiteSpeed via de dataroute)
- **Pagina 1**, 10 kaarten en scoretabel in deze volgorde: i210 LiDAR Pro 96,4 · i206 AWD 92,7 · i205 AWD 92,7 · Husqvarna 410VE NERA 87,3 · Mova 1200 80,5 · Mova 800 80,5 · Dreame A1 Pro 78,6 · i105E 75,9 · Eufy E15 63,2 · Gardena 800 60,9. Klopt met het modelbestand en het md.
- **Hub**: 6 kaarten (i206, i210 LiDAR Pro, Husqvarna, Mova 1200, Dreame, Gardena); tabel "In een oogopslag" met de nieuwe rij als tweede.
- Alle kaarten tonen "Functiescore: wat deze maaier kan. Hoe we scoren". **M015 en M016: geen Bol-regel**, knop "Bekijk de actuele prijs" naar nl.navimow.com; "Geen productfoto beschikbaar"-vak (geen bol-foto), zoals op de Navimow-pagina.
- Geen "[", "]" of "{" in de zichtbare tekst; de enige invulvelden zijn die van de bestaande tuingrootte-keuzehulp.
- 390 en 1440 px: geen horizontale scroll, 0 JavaScript-fouten. Alle 11 interne adressen HTTP 200; alle ankers (#p-…) bestaan.
- Bol-controle: 14 Bol-regels (hub 4, pagina 1 6, Navimow 4), 0 fouten.
- **Mandy: CDN-cache legen** (hPanel > Prestaties > CDN).

### Open punt (niet in het md, niet gedaan)
- De bronnenlijsten van pagina 1 en de hub bevatten per model bronnen; voor M015 en M016 staan daar nog geen bronnen (wel op de Navimow-pagina). Overnemen kan, op Mandy's woord.

## Ronde 41 (17 oktober 2026): bronnen M015/M016, Husqvarna 305E NERA op de mesjespagina

Uitgevoerd met `scripts/ronde41_bronnen_mesjes.py` (proefdraai zonder meldingen, daarna `--schrijf`), zonder thema-zip. Kopie vooraf: `backups/ronde41-voor-20261017-125109.json` (niet in git). #10, #11 en #236 bleven gepubliceerd; inhoud telkens zoals bedoeld. LiteSpeed geleegd via de dataroute (modelgegevens ongewijzigd). **Mandy: CDN-cache legen.**

### 1. Bronnen M015 en M016 (overgenomen van de Navimow-pagina #264, 5 regels per model)
- **Hub (#10):** blok "Segway Navimow i210 LiDAR Pro" (kop + 5 bronnen) direct na het i206-blok, net als op #264. M016 staat niet op de hub (geen kaart), dus geen bronnen van M016 op de hub.
- **Pagina 1 (#11):** die bronnenlijst is één platte lijst met de modelnaam vóór elke regel (niet per model gegroepeerd zoals #264). Om de rest niet te veranderen: 10 regels ("Segway Navimow i210 LiDAR Pro: …" en daarna "Segway Navimow i205 AWD: …") direct na de laatste i206-regel, zodat de Navimow-bronnen bij elkaar staan.
- Geen dubbele regels (live gecontroleerd: hub 38 bronnen, pagina 1 60 bronnen, 0 dubbel).

### 2. Mesjespagina (#236)
- Tabel: rij "Husqvarna Automower 305E NERA | Endurance 26,99 euro of Classic 22,99 euro (het aantal messen per verpakking is niet bevestigd) | hoofdschijf elke 3 tot 6 weken | niet berekend: het aantal per schijf is onbekend" direct onder de 410VE NERA.
- Onder "Husqvarna robotmaaier mesjes", na de bestaande alinea: "Voor de Automower 305E NERA noemt Husqvarna Endurance-messen (26,99 euro) en Classic-messen (22,99 euro); de messen van de hoofdschijf gaan volgens Husqvarna 3 tot 6 weken mee."
- **Klopt niet meer (niet gewijzigd, op Mandy's woord):** de bestaande alinea eindigt met "Voor andere Husqvarna-modellen hebben we de mesjes nog niet uitgezocht." Die staat nu direct boven de nieuwe alinea over de 305E NERA. Voorstel: "Voor andere Husqvarna-modellen dan de 410VE NERA en de 305E NERA hebben we de mesjes nog niet uitgezocht." Elders noemt de pagina alleen de 410VE NERA in de bronnenlijst (twee regels); voor de 305E NERA staat daar nog geen bron.
- Live: 390 en 1440 px zonder horizontale scroll, 0 JavaScript-fouten, geen "[" of "{".

### Voor thema 1.3.8
- (a) De regel "Geen productfoto beschikbaar" (en het placeholder-vak met de modelnaam) weghalen.
- (b) Als de Bol-foto niet laadt: het fotovak verbergen en alleen de specificatiekaart tonen (geen alt-tekst in een grijs vak; zie ronde 39).
- (c) Statusoverzicht "Bol-prijstaak draait": de tekst "Te oud: stel een echte cron in (wp rmk bol-ronde)." alleen tonen als de controle mislukt; bij OK alleen laatste en volgende ronde.
- (d) E-mail naar de beheerder als de prijstaak langer dan acht uur niet heeft gedraaid (één keer per storing, niet bij elke paginaweergave; bijvoorbeeld via een dagelijkse controle die naar `laatste_ronde.start` kijkt).

## Ronde 42 (17 oktober 2026): mesjespagina, 305E NERA afgemaakt

Uitgevoerd met `scripts/ronde42_mesjes_305e.py` (proefdraai zonder meldingen, daarna `--schrijf`). Kopie vooraf: `backups/ronde42-voor-20261017-130310.json` (niet in git). #236 bleef gepubliceerd; inhoud zoals bedoeld. LiteSpeed geleegd via de dataroute (modelgegevens ongewijzigd). **Mandy: CDN-cache legen.** Het nieuwe Excel-bestand (17 oktober) is alleen gelezen en staat niet in de repository.

- **Zin vervangen:** "Voor andere Husqvarna-modellen hebben we de mesjes nog niet uitgezocht." → "Voor andere Husqvarna-modellen dan de 410VE NERA en de 305E NERA hebben we de mesjes nog niet uitgezocht."
- **Bronnen (3 regels, direct na de twee 410VE NERA-regels), uit het blad Bronnen, M020, veld "Extra kosten: messen", 17 oktober 2026:**
  - "Husqvarna Automower 305E NERA: Endurance-messen, prijs" (husqvarna.com, endurance-blades, fits-to 970819612), Fabrikant;
  - "Husqvarna Automower 305E NERA: Classic-messen, prijs" (husqvarna.com, classic-blades, fits-to 970819612), Fabrikant;
  - "Husqvarna Automower 305E NERA: vervangtermijn messen" (Gebruiksaanwijzing Automower 305E/310E NERA NL, 2866-001, par. 7.1), Handleiding.
  - Live: 14 bronnen, 0 dubbel.
- **Nog een zin die alleen van de 410VE NERA uitgaat (niet gewijzigd):** onder "Wat we nog niet weten": "De mesjes van Gardena en andere Husqvarna-modellen: die hebben we nog niet uitgezocht." Voorstel: "De mesjes van Gardena en van andere Husqvarna-modellen dan de 410VE NERA en de 305E NERA: die hebben we nog niet uitgezocht." De overige zinnen met 410VE NERA gaan echt over dat model (alinea en tabelrij).
- Ter info uit het Excel-bestand (niet toegepast): bij de 305E NERA zitten 6 reservemessen in de doos, en de handleiding noemt ook de EdgeCut-schijf (9 tot 12 weken).

## Ronde 43 (17 oktober 2026): Husqvarna-modellen, conceptpagina husqvarna-robotmaaier

Aangeleverd: nieuwste `robotmaaierkompas_modeldata_v1.xlsx` (alleen gelezen, niet in de repository), `pagina-husqvarna-robotmaaier.md`, `modellen-teksten-husqvarna.json`. Gepubliceerd is alleen de wijziging op de mesjespagina (stap 4).

### 1. Modelgegevens (dataroute, `scripts/ronde43_upload.py`)
- **De 17 live modellen en de algemene velden ongewijzigd** (ook M010 met zijn teksten); erbij: M019, M020, M021, M022 (21 modellen). Kopie vooraf: `backups/modellen-voor-ronde43.json` (niet in git).
- M020 (305E NERA), M021 (305, met draad) en M022 (310E NERA) uit `excel_naar_json.py`, met fabrikantpagina (husqvarna.com/nl/…) en de teksten uit `modellen-teksten-husqvarna.json` (toegevoegd aan `scripts/modellen_teksten.json` en `modellen_analyse.json`). Geen EAN, geen Bol, geen prijs.
- **Omzetter gerepareerd:** de veldnaam "App: kaart/no-go, schema, …" (M020) werd niet herkend, waardoor M020 geen app-score kreeg. Nu herkend; functiescores (berekend met de themacode): **M020 69,5, M022 69,5, M021 52,7**, M010 ongewijzigd 87,3 (gelijk aan de md).
- **M019 (Automower 105):** de omzetter slaat niet-leverbare modellen over; daarom als leeg record (zoals M013): naam, slug, beschikbaarheid "niet leverbaar", fabrikantpagina = de Husqvarna-ondersteuningspagina "Niet meer leverbaar". Geen specificaties, scores, prijs of teksten.
- **Controle:** alle 18 openbare pagina's vóór en na de upload vergeleken (kaarten, scores, volledige tekst): **geen enkel verschil**. Volgorde en scores van hub, pagina 1 en Navimow-pagina ongewijzigd. M019 staat op geen enkele pagina als kaart of gegeven. (De hub-FAQ noemt al "Husqvarna Automower 105 en 305 … voegen we toe": bestaande tekst, zie open punten.)
- Live opgeslagen M019 `specs` als `[]` in plaats van `{}` (PHP); onschuldig.

### 2. Conceptpagina husqvarna-robotmaaier (id 20, concept)
- Gebouwd met `scripts/ronde43_bouw.py` (afgeleid van ronde 28, patroon pagina-merk), inhoud in `scripts/ronde43/husqvarna.json`, op de site gezet met `scripts/ronde43_pagina.py` (alleen als concept).
- Er bestond al een concept met deze slug (id 20): het lege sjabloon "[Merknaam] robotmaaiers …" van 6 oktober. Dat is bijgewerkt; de oude versie staat als revisie 147 in WordPress.
- Vier kaarten in de volgorde van de md: 410VE NERA 87,3 · 310E NERA 69,5 · 305E NERA 69,5 · 305 (met draad) 52,7. **Geen Bol-regel** en geen advertentie-regel. M020, M021, M022: knop "Bekijk de actuele prijs" naar de fabrikantpagina. M010 toont nog "rond 3.049 euro bij Husqvarna, gezien op 5 oktober" met "Bekijk bij Husqvarna" (fabrikantprijs, zoals op hub en pagina 1; na 14 dagen vanzelf "Bekijk de actuele prijs").
- Bronnen per model uit het blad Bronnen (handleidingen, husqvarna.com, appwinkels; geen winkels, geen "niet gevonden"): 410VE 7, 310E 13, 305E 15, 305 13 regels.
- Controle (weergegeven inhoud in de omhulling van de hub, 390 en 1440 px): geen horizontale scroll (de modellentabel schuift binnen haar vak), 0 JavaScript-fouten, geen "[", "]", "{" of invulveld, alle ankers bestaan; interne links (/, hub, pagina 1, zonder-grensdraad, test-vergelijking, kosten, mesjes, hoe-we-beoordelen, auteur) allemaal HTTP 200.
- **Download:** `paginatekst-husqvarna.md` (volledige weergegeven tekst; niet in de repository).

### 3. Links naar de nieuwe pagina: klaargezet, niet gedraaid
- `scripts/ronde43_links.py`: hub "Meer lezen" (na de Navimow-regel), pagina 1 onder "De modellen een voor een" (na de Navimow-zin), mesjespagina onder "Husqvarna robotmaaier mesjes": "Welke Automower past bij welke tuin? Zie Husqvarna robotmaaier." Weigert zolang de pagina geen status publish heeft (getest). Alle drie ankers komen nu precies één keer voor.

### 4. Mesjespagina (#236), gepubliceerd (`scripts/ronde43_mesjes.py`)
- "Wat we nog niet weten": "… andere Husqvarna-modellen dan de 410VE NERA, 305E NERA en 310E NERA: die hebben we nog niet uitgezocht."
- Tabelrij: "Husqvarna Automower 305E en 310E NERA".
- Kopie: `backups/ronde43-mesjes-voor-20261017-133245.json`. Live gecontroleerd; 390/1440 px zonder scroll, geen "[" of "{". LiteSpeed geleegd via de dataroute. **Mandy: CDN-cache legen.**

### Controles
- Routetest `--na-136 --na-137`: 0 fouten. Bol-controle: 14 Bol-regels, 0 fouten (ongewijzigd).

### Open punten (niet gedaan)
- Mesjespagina, alinea onder "Husqvarna robotmaaier mesjes": "Voor andere Husqvarna-modellen dan de 410VE NERA en de 305E NERA …" noemt de 310E NERA niet.
- Hub-FAQ "Zijn dit alle robotmaaiers?": "Modellen met begrenzingsdraad, zoals de Husqvarna Automower 105 en 305 …, voegen we toe." De 105 is niet meer leverbaar en de 305 staat nu op de Husqvarna-pagina.
- Specificatiekaart van M020, M021, M022: "Verbinding –" (geen regel in `verbinding_toewijzing.json`); de md-tabel noemt wifi/Bluetooth. Kan in de toewijzing worden aangevuld.

## Ronde 44 (17 oktober 2026): tekstwijzigingen na de Husqvarna-pagina (zonder thema-zip)
Bron: `tekstwijzigingen-husqvarna-ronde.md` met aanvulling (niet in de repository). Alles via de WordPress-API en de dataroute.

### Kopieën vooraf (niet in git)
- `backups/ronde44-paginas-voor-20261017-175607.json` (pagina's 10, 11, 18, 20, 236, 264), `backups/ronde44-modellen-voor-20261017-175607.json`, `backups/ronde44-teksten-voor-20261017-175748.json`.

### Teksten (`scripts/ronde44_teksten.py`): elke "Was"-tekst precies één keer gevonden
- **A** hub #10, FAQ: "… zoals de Husqvarna Automower 305 (zie de pagina Husqvarna robotmaaier) en de Gardena Sileno Minimo …".
- **B** mesjes #236: "Voor de Automower 305E en 310E NERA noemt …".
- **C1** kosten #18, Yoast-metabeschrijving: "… Meer dan tien modellen, met bron en datum."
- **C2** "Bij de modellen die wij hebben uitgezocht". "acht" kwam verder nergens op de kostenpagina voor.
- **C3** drie rijen vóór Gardena in "Verbinding en antidiefstal" (Navimow i205/i210/i220/X420, Husqvarna 305E en 310E NERA, Husqvarna 305 met draad).
- **C4** punt na de 410VE NERA onder "Antenne, gateway of dekking".
- Husqvarna-concept #20 (blijft concept): "… dan is de 305 met draad het meest vergelijkbare model met draad in ons overzicht". Ook in `scripts/ronde43/husqvarna.json`.
- Statussen ongewijzigd (#10, #18, #236 publish; #20 draft).
- **"Automower 105"** staat op geen enkele gepubliceerde pagina meer (alleen nog op het Husqvarna-concept, bewust).

### Modelgegevens (`scripts/ronde44_data.py`, dataroute)
- **D** verbinding M020 "Wifi" (extra wifi), M022 "Wifi" (wifi), M021 "Bluetooth" (bluetooth). Toewijzing in `scripts/verbinding_toewijzing.json`, die `excel_naar_json.py` gebruikt (docstring bijgewerkt); een volgende upload maakt het niet meer leeg.
- M010: alleen het minpunt "IPX5" weg (ook in `scripts/modellen_teksten.json`). Verder niets aan M010.
- Het script controleert dat alleen deze velden veranderen; alle andere modellen en algemene velden gelijk.
- **Beperking:** de chip "Verbinding" op de kaarten van M020-M022 toont nog "–". Het thema (`rmk_card_specs()` in `inc/prijzen.php`) kent alleen ingebouwd/module/geen. Zonder thema-zip niet op te lossen. **Voor 1.3.8:** `wifi` → "Wifi" en `bluetooth` → "Bluetooth" in die mapping.

### Controles
- Momentopname van alle 18 openbare pagina's vóór en na: **kaarten, scores en volgorde overal gelijk.** Tekstverschillen alleen waar verwacht: hub (A + kaart M010 zonder IPX5), pagina 1 (kaart M010), kosten, mesjes, en op home en de auteurspagina de lijst "recent bijgewerkt" (de kostenpagina staat nu bovenaan).
- 390 en 1440 px (hub, pagina 1, kosten, mesjes, Navimow, Husqvarna-concept in de omhulling van de hub): geen horizontale scroll, 0 JavaScript-fouten, geen "[", "]", "{" of "}". De enige invoervelden zijn de bestaande tuinkeuzehulp (hub, pagina 1) en kostencalculator. Husqvarna-concept: 87,3 / 69,5 / 69,5 / 52,7 ongewijzigd, IPX5 weg, verbinding nog [4G, –, –, –] (zie beperking).
- LiteSpeed geleegd via de dataroute. **Mandy: CDN-cache legen.**

### Klaargezet, niet gedraaid: `scripts/ronde44_links.py`
- Pas draaien als Mandy meldt dat husqvarna-robotmaaier gepubliceerd is (weigert anders). Vervangt `scripts/ronde43_links.py` (het mesjes-anker daarvan klopt niet meer na B; gemarkeerd als niet meer draaien).
- Zes regels: hub "Meer lezen", pagina 1, mesjespagina, kosten **C5**, Navimow "Meer lezen" ("Husqvarna robotmaaier: de Automower-modellen vergeleken."), Husqvarna "Meer lezen" ("Segway Navimow robotmaaier: alle modellen die nu nieuw te koop zijn."). Alle ankers komen nu precies één keer voor.
- Gebruik: `python3 scripts/ronde44_links.py` (proef), daarna `--schrijf`; dan links controleren, cache legen.

### Open punten (niet gedaan)
- Navimow-pagina #264, "Meer lezen": "Robotmaaier zonder draad: acht modellen vergeleken." (pagina 1 heeft nu meer modellen).
- Mesjespagina #236: de alinea "Voor andere Husqvarna-modellen dan de 410VE NERA en de 305E NERA hebben we de mesjes nog niet uitgezocht" noemt de 310E NERA niet (de zin onder "Wat we nog niet weten" wel).
- Thema 1.3.8: verbindingschip wifi/bluetooth (zie boven).
