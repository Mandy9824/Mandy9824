# robotmaaierkompas.nl — afwerkronde (v1.2)

Aanvulling op het pakket `robotmaaierkompas-wp` (v1.1). Dezelfde tokens (`tokens.css`), dezelfde `.rmk-`klassen en dezelfde toegankelijkheidsregels. Geen externe lettertypen of afbeeldingen: alles is SVG, op de PNG-exports van icoon en deelafbeelding na.

## Inhoud

| Map | Inhoud |
|---|---|
| `css/rmk-afwerking.css` | Eén CSS-bestand. Laden **na** `tokens.css` en `rmk.css`. Gebruikt alleen bestaande tokens. |
| `logo/` | `logo-horizontaal-licht.svg`, `logo-horizontaal-donker.svg`, `logo-gestapeld-licht.svg`, `logo-gestapeld-donker.svg`, `icoon-licht.svg`, `icoon-donker.svg`, `favicon.svg`, `favicon-512.png`, `apple-touch-icon-180.png`, `favicon-32.png`. Tekst is omgezet naar paden, dus het logo hangt niet af van een geladen lettertype. |
| `deelafbeelding/` | `deelafbeelding-1200x630.svg` en `.png` (Open Graph / social). |
| `iconen/` | Losse iconen (24 px, lijn 1,75, `currentColor`) en `iconen.svg` als sprite (`<use href="…/iconen.svg#rmk-i-beste">`). |
| `illustraties/` | `tuin.svg`, `gazon.svg`, `kompas.svg`, `hero-hoogtelijnen.svg` (achtergrond donkere kop), `motief-hoogtelijnen-licht.svg` (achtergrond lichte kop), `foto-plaatsvervanger.svg`. |
| `snippets/` | HTML-blokken voor WordPress (`core/html`): hero, vertrouwensstrook, ingangen, sectiekop, paginakop voor kernpagina's, fotokader (met en zonder foto), illustratie, header-logo. `[pad naar robotmaaierkompas]` vervangen door de themamap-URL. |
| `voorbeeld/` | `homepage.html` en `kernpagina.html` om het resultaat in de browser te bekijken (na het samenvoegen, zie stap 1). |

## Wat er is gewijzigd

1. **Logo:** het woordmerk "robotmaaierkompas" met een compact kompasicoon (ring, vier streepjes, naald). De noordnaald is kompasgroen, de zuidnaald veldsteen. Er zitten geen merkverwijzingen of blauwe tinten in. Het favicon is een groen vlak met een witte ring, zonder streepjes, zodat het ook op 16 px leesbaar blijft.
2. **Uitlijning:**
   - `.rmk-column` maakt een vaste hoofdkolom van 60rem en centreert die. `.rmk-column--narrow` is voor tekstpagina's, `.rmk-column--wide` voor de vergelijkingstabel.
   - `.rmk-pagehead--center` en `.rmk-section-head` centreren de kop en de introductie.
   - Lopende tekst (`.rmk-prose`) blijft links uitgelijnd binnen de kolom.
   - De zijmarges groeien mee tot 4rem.
3. **Homepage en kernpagina's:**
   - **Koppen:** de homepage krijgt een donkere kop met hoogtelijnen en een kompasmotief (`.rmk-hero--motif .rmk-hero--center`), de kernpagina's een lichte kop met hetzelfde motief (`.rmk-pageband`).
   - **Ingangen en vertrouwen:** vier ingangen met iconen (`.rmk-entries`, `.rmk-entry`) en een vertrouwensstrook met drie punten (`.rmk-trust`).
   - **Achtergronden:** secties kunnen afwisselen tussen wit, licht groen en donker groen (`--alt`, `--brand`, `--dark`).
   - **Kaarten en ruimte:** `.rmk-card` krijgt een rustige schaduw, een hover-rand, een zichtbare focusring en een pijl bij "Lees meer". Tussen secties zit meer ruimte.
   - **Menu:** valt bij een middelgroot scherm terug op de menuknop, zodat menu-items nooit over twee regels lopen.
4. **Beeldstijl:**
   - **Illustraties:** vlakke illustraties van tuin, gazon en kompas. De maaier in de illustraties is een abstracte vorm, geen herkenbaar model.
   - **Fotokader:** `.rmk-photo` heeft een vaste verhouding (4:3, of 1:1 met `--square`), een rustige stenen achtergrond en het bijschrift "Foto: fabrikant". Foto's worden niet bijgesneden (`object-fit: contain`).
5. **Licht en toegankelijk:**
   - Geen nieuwe kleuren; alle tekstcombinaties blijven ≥ 4,5:1.
   - Bewegingen zijn alleen kleur- en schaduwovergangen, en die vallen weg bij `prefers-reduced-motion`.
   - Decoratieve beelden hebben `alt=""` of zijn CSS-achtergronden.

## Instructies voor Claude Code

1. **Samenvoegen:** kopieer de inhoud van deze map naar `wp-content/themes/<thema>/robotmaaierkompas/`, zodat `css/`, `logo/`, `iconen/`, `illustraties/` naast `tokens.css` en `rmk.css` staan.
2. **CSS laden:** voeg in `robotmaaierkompas-setup.php`, na de regel voor `rmk.css`, toe:
   ```php
   wp_enqueue_style( 'rmk-afwerking', RMK_URL . '/css/rmk-afwerking.css', array( 'rmk' ), RMK_VER );
   ```
   Voeg `robotmaaierkompas/css/rmk-afwerking.css` ook toe aan `add_editor_style()`.
3. **Favicon en deelafbeelding:** zet in `wp_head`, alleen als er geen SEO-plugin is die dit al doet:
   ```php
   echo '<link rel="icon" href="' . esc_url( RMK_URL . '/logo/favicon.svg' ) . '" type="image/svg+xml">';
   echo '<link rel="icon" href="' . esc_url( RMK_URL . '/logo/favicon-32.png' ) . '" sizes="32x32">';
   echo '<link rel="apple-touch-icon" href="' . esc_url( RMK_URL . '/logo/apple-touch-icon-180.png' ) . '">';
   ```
   Gebruik `favicon-512.png` als sitepictogram (Customizer of `site_icon`) en `deelafbeelding/deelafbeelding-1200x630.png` als standaard og:image in de SEO-plugin.
4. **Logo:** vervang in `patterns/header.php` de inline logo-SVG door `snippets/header-logo.html`. Doe hetzelfde in `patterns/footer.php` met `logo-horizontaal-donker.svg`.
5. **Hoofdkolom:** voeg in `build2.py` en de paginapatronen `rmk-column` toe aan elke `rmk-container`:
   - `rmk-column--wide` bij de vergelijkingstabel;
   - `rmk-column--narrow` bij kopersgids, hulp, methode, auteur en juridisch.
6. **Kernpagina's (toplijst, vergelijkingen, kosten):** vervang de paginakop door `snippets/paginakop-kernpagina.html`.
7. **Homepage:**
   - Vervang de hero door `snippets/hero.html` en zet direct daaronder `snippets/vertrouwensstrook.html`.
   - Vervang "Kies per situatie" door `snippets/ingangen.html`.
   - Wissel de sectieachtergronden af: standaard, `--brand`, `--alt`, `--dark`.
   - Gebruik `snippets/sectiekop.html` voor de sectiekoppen.
8. **Productfoto's:** zet in `productbox*.php` het `{{PHOTO}}`-deel om naar `snippets/fotokader.html`, met `rmk-photo--square`. Zonder foto gebruik je `snippets/fotokader-plaatsvervanger.html`.
9. **Publicatiecontrole:** de snippets bevatten `[haken]` op invulplekken. De bestaande controle blokkeert publiceren tot die zijn ingevuld.

## Keuzes die ik voor je heb gemaakt

- **Vier ingangen:** Beste robotmaaiers, Vergelijkingen, Kopersgids en Kosten. Er is ook een icoon voor Hulp en onderhoud als je die liever gebruikt.
- **Kolombreedtes:** 60rem voor kernpagina's, 46rem (`--narrow`) voor tekstpagina's.
- **Kader voor productfoto's:** 4:3 als standaard, met een 1:1-variant voor de productbox.
