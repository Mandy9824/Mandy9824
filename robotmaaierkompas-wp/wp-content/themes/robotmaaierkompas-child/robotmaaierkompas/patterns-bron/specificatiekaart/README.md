# robotmaaierkompas.nl — specificatiekaart (v1.3)

Aanvulling op `robotmaaierkompas-wp` (v1.1) en `robotmaaierkompas-afwerking` (v1.2). Gebruikt dezelfde tokens, `.rmk-`klassen en toegankelijkheidsregels. Er worden geen externe bestanden geladen: de iconen zitten ingebed in de CSS en de achtergronden zijn lokale SVG's.

## Inhoud

| Map | Inhoud |
|---|---|
| `css/rmk-specificatiekaart.css` | De kaart, de kenmerkchips en de plaatsing in de productbox. Laden na `rmk-afwerking.css`. |
| `iconen/` | `oppervlak.svg`, `helling.svg`, `navigatie.svg`, `geluid.svg`, `verbinding.svg` (24 px, lijn 1,75, `currentColor`) en de sprite `iconen-specificaties.svg`. |
| `illustraties/` | `specificatiekaart-kompas.svg` (hoogtelijnen met kompas) en `specificatiekaart-tuin.svg` (gazon met maaibanen). |
| `snippets/` | `specificatiekaart.html`, `specificatiekaart-tuin.html`, `specificatiekaart-foto.html`, `productbox-kop-met-specificatiekaart.html`. Invulplekken staan tussen [haken], dus de bestaande publicatiecontrole houdt ze tegen tot ze zijn ingevuld. |
| `voorbeeld/specificatiekaart.html` | Kaarten met en zonder foto naast elkaar, en de kaart in de productbox. |

## Hoe de kaart werkt

- **Varianten:** `.rmk-speccard` heeft een vlak met hoogtelijnen en kompas. `--tuin` heeft een vlak met een gazon. `--photo` toont de productfoto.
- **Beeldvlak:** 4:3, met dezelfde rand en hoek als het fotokader (`.rmk-photo`).
  - Zonder foto: merk en modelnaam groot in het vlak, met het bijschrift "Geen productfoto beschikbaar".
  - Met foto: de foto zonder bijsnijden op een rustige stenen achtergrond, met het bijschrift "Foto: fabrikant".
  - Vlak, bijschrift en chips zijn in alle varianten even groot, zodat een model met en een model zonder foto naast elkaar rustig ogen.
- **Vijf kenmerken** als `<dl>` met chips: oppervlak (m²), helling (%), navigatie (RTK, camera, LiDAR, draad), geluid (dB) en verbinding (4G, module, geen).
  - Elke chip heeft een icoon in kompasgroen.
  - Ontbreekt een waarde, gebruik dan de `is-missing`-variant. Die toont "–", en schermlezers horen "onbekend". De chip heeft een gestippelde rand, zodat kleur niet het enige signaal is.
- **Mobiel eerst:** chips staan in twee kolommen en de vijfde chip krijgt de volle breedte. Vanaf 480 px staan ze in automatische kolommen. In de productbox staat de kaart bovenaan en vanaf 768 px links naast de titel.
- **Contrast (gemeten):**
  - merk op het vlak 7,9:1
  - modelnaam 15,8:1
  - chiplabel 6,6:1
  - lege waarde 6,1:1
  - icoon 7,1:1
- **Hoog contrast:** in de Windows-modus volgen de iconen de systeemkleur.

## Instructies voor Claude Code

1. **Samenvoegen:** kopieer `css/`, `iconen/` en `illustraties/` naar `wp-content/themes/<thema>/robotmaaierkompas/`. Er wordt niets overschreven.
2. **CSS laden:** voeg in `robotmaaierkompas-setup.php` na `rmk-afwerking` toe:
   ```php
   wp_enqueue_style( 'rmk-specificatiekaart', RMK_URL . '/css/rmk-specificatiekaart.css', array( 'rmk-afwerking' ), RMK_VER );
   ```
   Voeg `robotmaaierkompas/css/rmk-specificatiekaart.css` ook toe aan `add_editor_style()`.
3. **Productboxen:** vervang in `patterns-bron/c-productbox.html` en `c-productbox-zonder-prijs.html` het blok `<div class="rmk-product__head">…</div>` door `snippets/productbox-kop-met-specificatiekaart.html`.
   - Zet in dat blok `{{MINIS}}` en de reviewregel terug onder "Beste voor".
   - Draai daarna `build2.py` opnieuw.
   - Bij een model met foto: vervang de kaart door `snippets/specificatiekaart-foto.html`.
4. **Kop-aan-kop en vergelijkingen:** zet twee kaarten in `<div class="rmk-speccards">`.
5. **Merk en model:** in de productbox staan merk en modelnaam in het vlak met `aria-hidden="true"`, omdat de `<h3>` ze al noemt. Los gebruikt (zonder kop erboven) haal je dat `aria-hidden` weg.

## Gewijzigd ten opzichte van v1.2

- Nieuw: de specificatiekaart in drie varianten, vijf kenmerkiconen, twee achtergrondvlakken en vier snippets.
- In de productbox maakt de kaart de kopkolom breder, alleen wanneer er een kaart in staat (`:has()`). Productboxen zonder kaart blijven precies hetzelfde.
- Bestaande bestanden zijn niet aangepast.
