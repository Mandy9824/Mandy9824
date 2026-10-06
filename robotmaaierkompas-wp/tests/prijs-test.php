<?php
/**
 * Tests voor het prijsblok in de productbox (inc/prijzen.php) en de controle in de dataroute.
 * Draaien op een testsite: wp eval-file tests/prijs-test.php
 */
$GLOBALS['rmk_fail'] = 0; // wp eval-file draait in een functie: daarom $GLOBALS
function pcheck( $naam, $ok, $info = '' ) {
	echo ( $ok ? 'OK   ' : 'FOUT ' ) . $naam . ( $info ? "  ($info)" : '' ) . "\n";
	$GLOBALS['rmk_fail'] += $ok ? 0 : 1;
}
$m = array( 'id' => 'T1', 'fabrikant_url' => 'https://fabrikant.example/product',
	'prijs' => array( 'bedrag' => 899, 'winkel' => 'Coolblue', 'datum' => '2026-10-05', 'url' => 'https://www.coolblue.nl/product/1/x.html', 'type' => 'winkel' ) );

$h = rmk_offer_html( $m, '2026-10-06' );
pcheck( 'Geldige prijs: zin met bedrag, winkel en datum', false !== strpos( $h, 'Laagste nieuwe prijs rond <strong>899 euro</strong> bij Coolblue, gezien op 5 oktober 2026' ), $h );
pcheck( 'Geldige prijs: knop "Bekijk bij Coolblue" naar de productpagina', false !== strpos( $h, 'href="https://www.coolblue.nl/product/1/x.html"' ) && false !== strpos( $h, '>Bekijk bij Coolblue</a>' ) );
pcheck( 'Knop krijgt geen sponsored/nofollow (gewone link)', false === strpos( rmk_add_affiliate_rel( $h ), 'sponsored' ) );
pcheck( 'Dag 14 nog geldig', null !== rmk_valid_price( $m, '2026-10-19' ) );
pcheck( 'Dag 15 verlopen: alleen "Bekijk de actuele prijs" naar de fabrikant', '' === (string) rmk_valid_price( $m, '2026-10-20' ) && false !== strpos( rmk_offer_html( $m, '2026-10-20' ), 'href="https://fabrikant.example/product"' ) && false === strpos( rmk_offer_html( $m, '2026-10-20' ), 'euro' ) );
pcheck( 'Datum in de toekomst ongeldig', null === rmk_valid_price( $m, '2026-10-04' ) );
$b = $m; $b['prijs']['url'] = 'https://www.bol.com/nl/p/x/1/';
pcheck( 'Bol-URL ongeldig', null === rmk_valid_price( $b, '2026-10-06' ) );
$b = $m; $b['prijs']['winkel'] = 'Bol.com';
pcheck( 'Winkel Bol ongeldig', null === rmk_valid_price( $b, '2026-10-06' ) );
$b = $m; $b['prijs']['type'] = 'marketplace';
pcheck( 'Marketplace ongeldig', null === rmk_valid_price( $b, '2026-10-06' ) );
$b = $m; $b['prijs']['url'] = 'http://www.coolblue.nl/x';
pcheck( 'Geen https ongeldig', null === rmk_valid_price( $b, '2026-10-06' ) );
$b = $m; $b['prijs']['bedrag'] = 1299.99;
pcheck( 'Bedrag afgerond op hele euro\'s (1.300)', false !== strpos( rmk_offer_html( $b, '2026-10-06' ), '1.300 euro' ) );
$b = $m; unset( $b['prijs'], $b['fabrikant_url'] );
pcheck( 'Geen prijs en geen fabrikantpagina: geen prijsblok', '' === rmk_offer_html( $b, '2026-10-06' ) );

// Productbox in de inhoud: prijsblok vervangen op basis van data-model
$box = '<article class="rmk-product" aria-labelledby="x"><div class="rmk-scorecell" data-rmk-score data-model="M002"></div>'
	. '<div class="rmk-product__aside rmk-offers"><div class="rmk-offer"><span class="rmk-offer__price rmk-offer__price--empty">Bekijk de prijs bij de winkel</span><span class="rmk-offer__src">We tonen voorlopig geen winkelprijzen.</span></div></div></article>';
$out = rmk_fill_offers( $box );
pcheck( 'Productbox: oude tekst weg', false === strpos( $out, 'We tonen voorlopig' ) && false === strpos( $out, 'Bekijk de prijs bij de winkel' ) );
pcheck( 'Productbox: prijsblok uit modellen.json of fabrikantknop', false !== strpos( $out, 'Laagste nieuwe prijs rond' ) || false !== strpos( $out, 'Bekijk de actuele prijs' ) || false !== strpos( $out, 'rmk-offers"></div>' ), substr( strip_tags( $out ), 0, 120 ) );
pcheck( 'Productbox zonder bekend model blijft ongewijzigd', $box === rmk_fill_offers( str_replace( 'M002', 'X999', $box ) ) || false !== strpos( rmk_fill_offers( str_replace( 'M002', 'X999', $box ) ), 'Bekijk de prijs bij de winkel' ) );


// Productbox: specificatiekaart, foto, Beste voor, plus- en minpunten (1.3.2)
$fm  = array( 'id' => 'T2', 'naam' => 'Gardena Testmaaier', 'merk' => 'Gardena', 'model' => 'Testmaaier',
	'specs' => array( 'max_tuingrootte_m2' => array( 'waarde' => 1500 ), 'max_helling_pct' => array( 'waarde' => 32.5 ), 'navigatie' => array( 'waarde' => 'RTK+vision' ), 'geluid_dba' => array( 'waarde' => null ) ),
	'verbinding' => array( 'extra' => 'ingebouwd' ), 'beste_voor' => 'Grote tuinen', 'pluspunten' => array( 'Plus <1>' ), 'minpunten' => array( 'Min 1', 'Min 2' ) );
$kop = '<article class="rmk-product"><div class="rmk-product__head rmk-product__head--nomedia" style="grid-template-columns: 1fr"><div class="rmk-product__title"><h3 id="x">Gardena Testmaaier</h3></div></div><div class="rmk-product__aside rmk-offers"></div></article>';
$k = rmk_fill_card( $kop, $fm );
pcheck( 'Kaart zonder foto: merk en model in het vlak, "Geen productfoto beschikbaar"', false !== strpos( $k, 'rmk-speccard__brand">Gardena<' ) && false !== strpos( $k, 'rmk-speccard__model">Testmaaier<' ) && false !== strpos( $k, 'Geen productfoto beschikbaar' ) && false === strpos( $k, '--nomedia' ) );
pcheck( 'Kenmerken: 1.500 m², 32,5%, RTK + camera, 4G', false !== strpos( $k, '<dd>1.500 m²</dd>' ) && false !== strpos( $k, '<dd>32,5%</dd>' ) && false !== strpos( $k, '<dd>RTK + camera</dd>' ) && false !== strpos( $k, '<dd>4G</dd>' ) );
pcheck( 'Ontbrekend geluid: is-missing met "onbekend"', false !== strpos( $k, 'rmk-spec--geluid is-missing' ) && false !== strpos( $k, '<span class="rmk-sr">onbekend</span>' ) );
pcheck( 'Beste voor na de h3', false !== strpos( $k, '</h3><p class="rmk-bestfor"><span>Beste voor</span> Grote tuinen</p>' ) );
pcheck( 'Plus- en minpunten als lijsten, ge-escaped, voor het prijsblok', false !== strpos( $k, '<ul class="rmk-pros"><li>Plus &lt;1&gt;</li></ul>' ) && false !== strpos( $k, '<ul class="rmk-cons"><li>Min 1</li><li>Min 2</li></ul></div></div><div class="rmk-product__aside' ) );
$fm2 = $fm; $fm2['foto'] = array( 'url' => 'https://www.gardena.com/x.png' );
$k2 = rmk_fill_card( $kop, $fm2 );
pcheck( 'Met foto: fotovariant met "Foto: Gardena" en alt-tekst', false !== strpos( $k2, 'rmk-speccard--photo' ) && false !== strpos( $k2, 'Foto: Gardena' ) && false !== strpos( $k2, 'alt="Gardena Testmaaier, productfoto"' ) && false === strpos( $k2, 'Geen productfoto' ) );
$fm3 = $fm; $fm3['foto'] = array( 'url' => 'https://media.s-bol.com/x.jpg' );
pcheck( 'Geen Bol-afbeelding (dan de kaart zonder foto)', false === strpos( rmk_fill_card( $kop, $fm3 ), 's-bol' ) );
pcheck( 'Tweede keer vullen geeft geen dubbele kaart', 1 === substr_count( rmk_fill_card( $k, $fm ), 'rmk-speccard__specs' ) );
$ph  = '<article class="rmk-product"><div class="rmk-product__head"><div class="rmk-product__media"><!-- x --><figure class="rmk-photo rmk-photo--square rmk-photo--placeholder"><div class="rmk-photo__frame"><img src="p.svg" alt=""></div><figcaption>Foto volgt</figcaption></figure></div><div class="rmk-product__title"></div></div></article>';
pcheck( 'Plaatsvervanger wordt weggehaald (nooit op een gepubliceerde pagina)', false === strpos( rmk_strip_photo_placeholders( $ph ), 'Foto volgt' ) );
pcheck( 'Plaatsvervanger wordt vervangen door de kaart', false === strpos( rmk_fill_card( $ph, $fm ), 'Foto volgt' ) && false !== strpos( rmk_fill_card( $ph, $fm ), 'rmk-speccard' ) );
$GLOBALS['rmk_lbl'] = rmk_score_label_html( 'Functiescore: wat deze maaier kan.' );
pcheck( 'Scorelabel met link "Hoe we scoren"', 'Functiescore: wat deze maaier kan. <a href="/hoe-we-beoordelen/">Hoe we scoren</a>' === $GLOBALS['rmk_lbl'] );

// Dataroute
$data = array( 'modellen' => array( array( 'id' => 'M1', 'slug' => 'm1', 'naam' => 'M1', 'kosten' => array( 'aanschaf' => array( 'waarde' => null ) ), 'prijs' => $m['prijs'] ) ) );
pcheck( 'Dataroute accepteert een geldige prijs', array() === rmk_validate_modellen( $data ), implode( '; ', rmk_validate_modellen( $data ) ) );
$data['modellen'][0]['prijs']['type'] = 'marketplace';
pcheck( 'Dataroute weigert marketplace', (bool) rmk_validate_modellen( $data ) );
$data['modellen'][0]['prijs']['type'] = 'winkel'; $data['modellen'][0]['prijs']['bedrag'] = 899.5;
pcheck( 'Dataroute weigert bedrag met centen', (bool) rmk_validate_modellen( $data ) );

echo $GLOBALS['rmk_fail'] ? "\n" . $GLOBALS['rmk_fail'] . " test(s) mislukt\n" : "\nAlle prijstests geslaagd\n";
