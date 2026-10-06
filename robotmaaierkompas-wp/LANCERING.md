# Lancering robotmaaierkompas.nl: stappen voor Mandy

Stand: 6 oktober 2026, thema 1.3.3 (nog uploaden). Alles is nog concept en "Zoekmachines niet laten indexeren" staat aan.
Werk de stappen in deze volgorde af. Indexering gaat pas aan in stap 4, als alle pagina's van de eerste golf gepubliceerd en gecontroleerd zijn.

## 1. Vooraf (de dag ervoor)
1. Maak een back-up in hPanel (bestanden en database).
1. Staat thema 1.3.1 actief? Klik dan één keer op **Gereedschap > Robotmaaierkompas > Huisstijl toepassen** (sitepictogram en standaard deelafbeelding in Yoast).
2. Controleer in WordPress bij **Gereedschap > Robotmaaierkompas** of de statuscontroles groen zijn.
3. Lees de gegevens in **Colofon**, **Privacy** en **Contact** nog één keer na (naam, e-mailadres contact@robotmaaierkompas.nl, adres). Stuur een testmail naar contact@robotmaaierkompas.nl en kijk of hij aankomt.
4. Pagina 4: open de bronlinks in je eigen browser (zie het bouwlogboek, ronde 8 en 9).
5. **Prijzen verversen.** Een prijs in de productbox verdwijnt 14 dagen na de datum waarop hij gezien is; de huidige prijzen zijn van 5 oktober en verdwijnen na 19 oktober. Controleer vlak voor de lancering prijs en voorraad in het blad Prijzen van het Excel-bestand (nieuw, op voorraad, winkel of fabrikant, geen Bol, geen marketplace), zet de datum van die dag, en draai het script met `--upload` opnieuw.

## 2. Publiceren, in deze volgorde
De publicatiecontrole van het thema houdt een pagina tegen als er nog `[`, "Alfa", "Beta" of "gepeild" in staat. Zie je die melding, dan staat er nog een invulveld in.

| Volgorde | Pagina | ID | Adres |
|---|---|---|---|
| 1 | Privacy | 82 | /privacy/ |
| 2 | Cookies | 83 | /cookies/ |
| 3 | Affiliate-melding | 81 | /affiliate-melding/ |
| 4 | Redactiebeleid | 84 | /redactiebeleid/ |
| 5 | Colofon | 80 | /colofon/ |
| 6 | Contact | 79 | /contact/ |
| 7 | Over ons | 77 | /over-ons/ |
| 8 | Mandy van den Broek (auteur, onder Over ons) | 78 | /over-ons/mandy-van-den-broek/ |
| 9 | Hoe we beoordelen | 76 | /hoe-we-beoordelen/ |
| 10 | Kosten (pagina 12) | 18 | /robotmaaier-kosten/ |
| 11 | Robotmaaier zonder grensdraad (pagina 11) | 17 | /robotmaaier-zonder-grensdraad/ |
| 12 | Robotmaaier test (pagina 4) | 13 | /robotmaaier-test-consumentenbond/ |
| 13 | Robotmaaier zonder draad (pagina 1) | 11 | /robotmaaier-zonder-draad/ |
| 14 | Robotmaaiers vergelijken (pagina 2) | 12 | /robotmaaier-test-vergelijking/ |
| 15 | Homepage | 9 | / |

Waarom deze volgorde:
- Eerst de pagina's waar de footer en de cookiebanner naar linken.
- Daarna Over ons, en dan pas de auteurspagina eronder.
- Dan de pagina's waar de inhoud naar linkt. Pagina 2 linkt naar pagina 4, en pagina 1 naar pagina 11.
- De homepage als laatste: dat is de voorpagina (Instellingen > Lezen), en `/` geeft 404 tot hij gepubliceerd is.

Publiceer verder niets. De andere 61 pagina's blijven concept. Ze staan niet in het menu of de footer, en de eerste golf linkt er niet naar (gecontroleerd op 6 oktober).

## 3. Controleren vóór indexering (in een privévenster, niet ingelogd)
1. Open `https://robotmaaierkompas.nl/wp-json/rmk/v1` en `https://robotmaaierkompas.nl/wp-json/rmk/v1/status`. Beide moeten "Alleen voor beheerders" (401) geven, zonder gegevens.
1. Leeg de **LiteSpeed-cache** (beheerbalk > LiteSpeed Cache > Alles legen) en de **CDN-cache** in hPanel.
2. Open alle 15 adressen: geeft elk de pagina, zonder 404?
3. Klik in het menu en in de footer elke link aan; geen 404.
4. Kijk of de cookiebanner verschijnt, en of "Alles weigeren" hem sluit.
5. Pagina 12: werkt de kostencalculator (kies een model, zie je bedragen)?
6. Pagina 2: werken het filter en de sortering?
7. Mobiel (je telefoon): niets valt buiten het scherm.
8. Draai **PageSpeed Insights** (pagespeed.web.dev) op de homepage, pagina 1, pagina 2 en pagina 12, mobiel en desktop. Dat kan al voordat de indexering aan staat.
9. Draai de **Rich Results Test** van Google (search.google.com/test/rich-results) op pagina 1 en de auteurspagina. Verwacht: Artikel en Kruimelpad, zonder fouten, en géén Product of Review.

## 4. Indexering aanzetten
1. Ga naar **Instellingen > Lezen**, zet het vinkje bij "Zoekmachines niet laten indexeren" **uit** en sla op.
2. Leeg opnieuw de LiteSpeed-cache en de CDN-cache.
3. Controleer in een privévenster:
   - `https://robotmaaierkompas.nl/robots.txt` bevat geen `Disallow: /`, wel `Disallow: /wp-json/rmk/` en `Disallow: /wp-content/uploads/rmk/`, en een regel `Sitemap:`.
   - `https://robotmaaierkompas.nl/sitemap_index.xml` opent. In `page-sitemap.xml` staan precies de 15 gepubliceerde pagina's en geen concepten.
   - In de broncode van een pagina (Ctrl+U) staat `index, follow` bij `robots` en een `canonical` naar het eigen adres.

## 5. Google Search Console (search.google.com/search-console)
1. Voeg een **domeineigendom** toe: `robotmaaierkompas.nl`.
2. Verifieer met het **DNS-TXT-record**: plak het record in hPanel bij Domeinen > DNS-zone. Dan is er geen code op de site nodig. Verificatie kan een paar minuten tot een paar uur duren.
3. Ga naar **Sitemaps** en dien `sitemap_index.xml` in. Na een dag moet de status "Geslaagd" zijn, met 15 ontdekte pagina's.
4. Gebruik **URL-inspectie** op de homepage, pagina 1, 2, 4, 11 en 12 en de methodepagina, en vraag voor elk "Indexering aanvragen" (er zit een daglimiet op).
5. Controleer bij **Instellingen > robots.txt** of Google de nieuwe robots.txt heeft opgehaald.
6. Controleer **Beveiliging en handmatige acties**; daar hoort niets te staan.

## 6. Bing Webmaster Tools (bing.com/webmasters)
1. Log in en kies **Importeren uit Google Search Console**. Dan worden de site en de sitemap overgenomen. Lukt dat niet: voeg de site handmatig toe en verifieer met een DNS-record (CNAME) in hPanel.
2. Controleer bij **Sitemaps** of `https://robotmaaierkompas.nl/sitemap_index.xml` erin staat, en dien hem anders in.
3. Gebruik **URL-inspectie** op de homepage en vraag om indexering ("Request indexing").

## 7. De eerste week
**Dag 1 tot 3:**
- In Search Console, bij **Pagina's**: welke pagina's zijn geïndexeerd, en wat staat er bij "Niet geïndexeerd"? Verwacht zijn alleen meldingen als "Ontdekt/gecrawld, momenteel niet geïndexeerd" (dat is normaal in het begin), en "Uitgesloten door noindex" alleen voor zoekresultaten, tags of auteursarchief.
- Is de sitemap "Geslaagd", zonder fouten?
- Staan er 404-fouten of serverfouten (5xx) in de lijst?
- Bing: dezelfde controle bij **Sitemaps** en **Site Explorer**.

**Elke dag een paar minuten:**
- Open de homepage en pagina 12 niet ingelogd: laden ze, en werkt de calculator?
- Zoek in Google op `site:robotmaaierkompas.nl`. Er horen alleen gepubliceerde pagina's te verschijnen, geen concepten, `/ga/`, `/wp-json/` of `modellen.json`.
- Kijk of er mail binnenkomt op contact@robotmaaierkompas.nl.

**Aan het eind van de week:**
- Bekijk in Search Console bij **Prestaties** de eerste zoekopdrachten en vertoningen. Na een paar dagen komen er cijfers.
- Draai PageSpeed Insights opnieuw op dezelfde vier pagina's. Velddata (Core Web Vitals, INP) komen pas na een paar weken met genoeg bezoek.
- Maak opnieuw een back-up.
- Trek de **toepassingswachtwoorden** in die tijdens de bouw zijn gebruikt (Gebruikers > Profiel > Toepassingswachtwoorden), zodra de bouw klaar is. Maak alleen een nieuw wachtwoord aan als er weer gewerkt moet worden.

## Bewust nog niet bij deze lancering
- Geen affiliatelinks, geen Bol-gegevens of prijzen. De prijstaak blijft uit.
- Geen meetcode (GA4). Die komt pas als `RMK_GA4_ID` in wp-config.php staat, en laadt alleen na toestemming in de cookiebanner. Pas dan de privacy- en cookiepagina aan.
- Header en footer houden het tijdelijke menu. Bij golf 2 kies je in de site-editor "Aanpassingen wissen", zodra de sectiepagina's gevuld en gepubliceerd zijn.
- HSTS is optioneel (hPanel).
