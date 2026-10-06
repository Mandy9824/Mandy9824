<?php
/**
 * Tests voor het prijsblok in de productbox (inc/prijzen.php) en de controle in de dataroute.
 * Draaien op een testsite: wp eval-file tests/prijs-test.php
 */
$fail = 0;
function pcheck( $naam, $ok, $info = '' ) {
	global $fail;
	echo ( $ok ? 'OK   ' : 'FOUT ' ) . $naam . ( $info ? "  ($info)" : '' ) . "\n";
	$fail += $ok ? 0 : 1;
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

// Dataroute
$data = array( 'modellen' => array( array( 'id' => 'M1', 'slug' => 'm1', 'naam' => 'M1', 'kosten' => array( 'aanschaf' => array( 'waarde' => null ) ), 'prijs' => $m['prijs'] ) ) );
pcheck( 'Dataroute accepteert een geldige prijs', array() === rmk_validate_modellen( $data ), implode( '; ', rmk_validate_modellen( $data ) ) );
$data['modellen'][0]['prijs']['type'] = 'marketplace';
pcheck( 'Dataroute weigert marketplace', (bool) rmk_validate_modellen( $data ) );
$data['modellen'][0]['prijs']['type'] = 'winkel'; $data['modellen'][0]['prijs']['bedrag'] = 899.5;
pcheck( 'Dataroute weigert bedrag met centen', (bool) rmk_validate_modellen( $data ) );

echo $fail ? "\n$fail test(s) mislukt\n" : "\nAlle prijstests geslaagd\n";
