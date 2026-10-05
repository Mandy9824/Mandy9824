<?php
/**
 * Title: RMK – Specs-tabel met statusbadges
 * Slug: robotmaaierkompas/specs-tabel
 * Categories: robotmaaierkompas
 * Description: Per waarde een status: gecontroleerd, fabrikantclaim, winkelclaim, tegenstrijdig, niet gevonden.
 * Viewport Width: 1280
 */
?>
<!-- wp:html -->
<div class="rmk-tablewrap">
  <table class="rmk-specs">
    <caption class="rmk-sr">Specificaties van [Modelnaam] met status per waarde</caption>
    <!-- Kies per rij één status: ok = gecontroleerd, maker = fabrikantclaim, shop = winkelclaim, conflict = tegenstrijdig, missing = niet gevonden.
         Tegenstrijdig: toon beide waarden met bron en reken met de minst gunstige. -->
    <tbody>
      <tr><th scope="row">Navigatie</th><td><div class="rmk-specs__val">[waarde]<span class="rmk-status rmk-status--[ok|maker|shop|conflict|missing]">[status]</span><span class="rmk-specs__note">Bron: [bron]</span></div></td></tr>
      <tr><th scope="row">Maximale oppervlakte</th><td><div class="rmk-specs__val">[waarde] m²<span class="rmk-status rmk-status--[ok|maker|shop|conflict|missing]">[status]</span><span class="rmk-specs__note">Bron: [bron]</span></div></td></tr>
      <tr><th scope="row">Maximale helling</th><td><div class="rmk-specs__val">[waarde]%<span class="rmk-status rmk-status--[ok|maker|shop|conflict|missing]">[status]</span><span class="rmk-specs__note">Bron: [bron]</span></div></td></tr>
      <tr><th scope="row">Minimale doorgang</th><td><div class="rmk-specs__val">[waarde] cm<span class="rmk-status rmk-status--[ok|maker|shop|conflict|missing]">[status]</span><span class="rmk-specs__note">Bron: [bron]</span></div></td></tr>
      <tr><th scope="row">Geluid</th><td><div class="rmk-specs__val">[waarde A] of [waarde B] dB(A)<span class="rmk-status rmk-status--conflict">Tegenstrijdig</span><span class="rmk-specs__note">[bron A]: [waarde A], [bron B]: [waarde B]. We rekenen met de minst gunstige waarde.</span></div></td></tr>
      <tr><th scope="row">Antidiefstal</th><td><div class="rmk-specs__val">[waarde]<span class="rmk-status rmk-status--[ok|maker|shop|conflict|missing]">[status]</span><span class="rmk-specs__note">Bron: [bron]</span></div></td></tr>
      <tr><th scope="row">Verbinding na gratis periode</th><td><div class="rmk-specs__val">—<span class="rmk-status rmk-status--missing">Niet gevonden</span></div></td></tr>
    </tbody>
  </table>
</div>
<div class="rmk-legend" style="margin-top: var(--rmk-space-3)">
  <div><span class="rmk-status rmk-status--ok">Gecontroleerd</span>gelezen in de handleiding of op de officiële pagina van de fabrikant</div>
  <div><span class="rmk-status rmk-status--maker">Fabrikantclaim</span>alleen in een datasheet of reclame van de fabrikant</div>
  <div><span class="rmk-status rmk-status--shop">Winkelclaim</span>alleen een winkel noemt het</div>
  <div><span class="rmk-status rmk-status--conflict">Tegenstrijdig</span>bronnen verschillen; beide getoond, gerekend met de minst gunstige</div>
  <div><span class="rmk-status rmk-status--missing">Niet gevonden</span>geen bron gevonden</div>
</div>
<!-- /wp:html -->
