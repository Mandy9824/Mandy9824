<?php
/**
 * Test thema 1.3.16: Coolblue-foto alleen van https://coolblue.bynder.com of https://image.coolblue.nl (precies die hosts,
 * geen http, geen jokertekens, geen andere subdomeinen, geen poort of gebruikersnaam). Zonder netwerk: de opgeslagen feed
 * (optie rmk_coolblue_feed) wordt nagebootst zoals de ronde hem bewaart. De afbeeldingsadressen zijn testadressen.
 * Draaien: php tests/coolblue-foto-test.php
 */
require __DIR__ . '/wp-stub.php';
$T = dirname( __DIR__ ) . '/wp-content/themes/robotmaaierkompas-child/robotmaaierkompas';
define( 'RMK_DIR', $T );
define( 'RMK_COOLBLUE_FEED_URL', 'https://productdata.awin.com/datafeed/download/apikey/GEHEIM0123456789abcdef/fid/95886/format/csv/compression/gzip/' );
define( 'RMK_COOLBLUE_AWMID', 85161 );
define( 'RMK_COOLBLUE_AWAFFID', 3126598 );
define( 'RMK_COOLBLUE_ACTIVE', true );
function wp_remote_get( $url, $args = array() ) { $GLOBALS['verzoeken'] = ( $GLOBALS['verzoeken'] ?? 0 ) + 1; return new WP_Error( 'x', 'geen netwerk' ); }
function get_temp_dir() { return sys_get_temp_dir() . '/'; }
add_filter( 'pre_http_request', function () { $GLOBALS['verzoeken'] = ( $GLOBALS['verzoeken'] ?? 0 ) + 1; return new WP_Error( 'x', 'geen netwerk' ); } );

$data = json_decode( file_get_contents( $T . '/data/modellen.json' ), true );
$ids  = array_column( $data['modellen'], 'id' );
if ( ! in_array( 'M008', $ids, true ) ) {
	$data['modellen'][] = array( 'id' => 'M008', 'slug' => 'dreame-a1-pro', 'naam' => 'Dreame A1 Pro', 'scores' => array() );
}
foreach ( $data['modellen'] as &$m ) {
	if ( 'M008' === $m['id'] ) {
		$m['coolblue'] = array( 'merchant_product_id' => '962143', 'product_url' => 'https://www.coolblue.nl/product/962143/dreame-a1-pro.html' );
		unset( $m['bol'], $m['foto'] ); // geen Bol-foto: de Coolblue-foto moet het fotovak vullen
	}
}
unset( $m );
$MODELLEN = tempnam( sys_get_temp_dir(), 'rmkmod' );
file_put_contents( $MODELLEN, json_encode( $data ) );
add_filter( 'rmk_models_file', function () use ( $MODELLEN ) { return $MODELLEN; }, 20 );
foreach ( array( 'data', 'score', 'bol', 'coolblue', 'prijzen' ) as $f ) {
	require "$T/inc/$f.php";
}
$GLOBALS['fail'] = 0;
function t( $n, $ok, $info = '' ) {
	echo ( $ok ? 'OK   ' : 'FOUT ' ) . $n . ( $info && ! $ok ? "\n       $info" : '' ) . "\n";
	$GLOBALS['fail'] += $ok ? 0 : 1;
}

// 1. De regel zelf
$ja  = array(
	'https://image.coolblue.nl/max/500x500/products/962143.jpg',
	'https://IMAGE.Coolblue.NL/max/500x500/products/962143.jpg',          // host zonder hoofdlettergevoeligheid (zoals 1.3.15)
	'https://coolblue.bynder.com/transform/x/962143?io=transform:fit,height:800',
);
$nee = array(
	'http://image.coolblue.nl/max/500x500/p.jpg'           => 'http',
	'//image.coolblue.nl/p.jpg'                            => 'zonder schema',
	'HTTPS://image.coolblue.nl/p.jpg'                      => 'schema in hoofdletters',
	'https://images.coolblue.nl/p.jpg'                     => 'ander subdomein (images)',
	'https://cdn.image.coolblue.nl/p.jpg'                  => 'subdomein van image.coolblue.nl',
	'https://www.coolblue.nl/p.jpg'                        => 'www.coolblue.nl',
	'https://coolblue.nl/p.jpg'                            => 'coolblue.nl zelf',
	'https://image.coolblue.be/p.jpg'                      => 'coolblue.be',
	'https://image.coolblue.nl.evil.example/p.jpg'         => 'image.coolblue.nl als begin van een ander domein',
	'https://evilimage.coolblue.nl/p.jpg'                  => 'host die eindigt op image.coolblue.nl',
	'https://image.coolblue.nl./p.jpg'                     => 'punt achter de host',
	'https://image.coolblue.nl:8443/p.jpg'                 => 'poort',
	'https://user@image.coolblue.nl/p.jpg'                 => 'gebruikersnaam',
	'https://user:geheim@image.coolblue.nl/p.jpg'          => 'gebruikersnaam en wachtwoord',
	'https://evil.example/?u=https://image.coolblue.nl/p.jpg' => 'image.coolblue.nl alleen in de query',
	'https://images2.productserve.com/?url=ssl%3Aimage.coolblue.nl%2Fp.jpg' => 'Awin-beeldserver',
	'https://*.coolblue.nl/p.jpg'                          => 'jokerteken',
	'https://coolblue.bynder.com:443/x'                    => 'bynder met poort',
	'http://coolblue.bynder.com/x'                         => 'bynder met http',
	''                                                      => 'leeg',
	'geen url'                                              => 'geen URL',
);
foreach ( $ja as $u ) {
	t( 'toegestaan: ' . $u, true === rmk_coolblue_afbeelding_ok( $u ) );
}
foreach ( $nee as $u => $waarom ) {
	t( 'geweigerd (' . $waarom . '): ' . ( '' === $u ? '(leeg)' : $u ), false === rmk_coolblue_afbeelding_ok( $u ) );
}
t( 'precies twee hosts, zonder jokertekens', array( 'coolblue.bynder.com', 'image.coolblue.nl' ) === rmk_coolblue_afbeelding_hosts() );

// 2. De kaart: met https://image.coolblue.nl een foto met "Foto: Coolblue"; anders geen fotovak, wel de Coolblue-regel
$nu   = time();
$feed = function ( $img ) use ( $nu ) {
	$GLOBALS['wp_options'][ RMK_CB_STORE_OPTION ] = array( 'opgehaald' => $nu - 3600, 'hash_sinds' => $nu - 3600, 'rijen' => 5066, 'producten' => array(
		'M008' => array( 'merchant_product_id' => '962143', 'prijs' => 699.0, 'in_stock' => true, 'afbeelding' => $img, 'url' => 'https://www.coolblue.nl/product/962143/dreame-a1-pro.html' ) ) );
};
$kaart = function () {
	return rmk_fill_offers( '<article class="rmk-product" aria-labelledby="p-dreame-a1-pro"><div class="rmk-product__head rmk-product__head--nomedia" style="grid-template-columns: 1fr"><div class="rmk-product__title"><h3 id="p-dreame-a1-pro">Dreame A1 Pro</h3><div class="rmk-scorecell" data-rmk-score data-model="M008"></div></div></div><div class="rmk-product__aside rmk-offers"><div class="rmk-offer"></div></div></article>' );
};
$IMG = 'https://image.coolblue.nl/max/500x500/products/962143.jpg';
$feed( $IMG );
$k = $kaart();
t( 'kaart: Coolblue-regel', false !== strpos( $k, 'rmk-offer--coolblue' ) );
t( 'kaart: foto met het ongewijzigde feedadres', false !== strpos( $k, 'src="' . esc_url( $IMG ) . '"' ), $k );
t( 'kaart: bijschrift "Foto: Coolblue", alt "Dreame A1 Pro, productfoto", data-rmk-foto-bron="coolblue"',
	false !== strpos( $k, '<figcaption class="rmk-speccard__caption">Foto: Coolblue</figcaption>' ) && false !== strpos( $k, 'alt="Dreame A1 Pro, productfoto"' ) && false !== strpos( $k, 'data-rmk-foto-bron="coolblue"' ) );
t( 'kaart: één foto, lazy en async', 1 === substr_count( $k, '<img ' ) && false !== strpos( $k, 'loading="lazy"' ) && false !== strpos( $k, 'decoding="async"' ) );
file_put_contents( sys_get_temp_dir() . '/rmk-kaart-m008.html', $k );
foreach ( array( 'http://image.coolblue.nl/p.jpg', 'https://images.coolblue.nl/p.jpg', 'https://image.coolblue.nl:8443/p.jpg', '' ) as $u ) {
	$feed( $u );
	$k = $kaart();
	t( 'kaart zonder foto maar met Coolblue-regel bij ' . ( '' === $u ? '(leeg)' : $u ), false === strpos( $k, '<img ' ) && false === strpos( $k, 'Foto: Coolblue' ) && false !== strpos( $k, 'rmk-offer--coolblue' ) );
}
$feed( 'https://coolblue.bynder.com/transform/x/962143?io=transform:fit,height:800' );
t( 'bynder blijft werken', false !== strpos( $kaart(), 'Foto: Coolblue' ) );

// 3. Een geldige Bol-foto gaat nog steeds voor (volgorde ongewijzigd): rmk_fill_offers kiest eerst rmk_bol_foto().
$src = file_get_contents( "$T/inc/prijzen.php" );
t( 'volgorde Bol-foto, dan Coolblue-foto ongewijzigd', 1 === preg_match( '#rmk_bol_foto\( \$m \) \).*?elseif.*?rmk_coolblue_foto\( \$m \)#s', $src ) );
t( 'geen HTTP-verzoeken', 0 === ( $GLOBALS['verzoeken'] ?? 0 ) );

echo $GLOBALS['fail'] ? "\n{$GLOBALS['fail']} FOUT\n" : "\nAlles OK\n";
exit( $GLOBALS['fail'] ? 1 : 0 );
