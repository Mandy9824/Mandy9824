<?php
/**
 * Test van de Amazon-knop (thema 1.3.13, inc/amazon.php) met NAGEBOOTSTE modelgegevens, zonder netwerk.
 * Er wordt geen enkele link gevolgd of aangeklikt; alleen de vorm van de HTML wordt gecontroleerd.
 *
 * Nagebootste modellen (op basis van data/modellen.json uit het thema):
 *   M004  ASIN + "Knop: ja"                                   -> knop
 *   M008  ASIN + "Knop: ja", met Bol- en Coolblue-regel       -> knop ONDER Bol en Coolblue
 *   M002  geen ASIN (geen blok amazon)                        -> geen knop
 *   M011  ASIN + "Knop: nee" (knop false)                     -> geen knop
 *   M050  ASIN + "Knop: ja" in het blad, maar uitgesloten     -> geen knop
 *
 * Draaien: php tests/amazon-test.php            (alles aan: RMK_AMAZON_TAG + RMK_AMAZON_ACTIVE, ook Bol en Coolblue aan)
 *          php tests/amazon-test.php uit        (RMK_AMAZON_TAG wel, RMK_AMAZON_ACTIVE niet)
 *          php tests/amazon-test.php zonder     (geen Amazon-constanten)
 *          php tests/amazon-test.php tagfout    (RMK_AMAZON_TAG ongeldig, schakelaar aan)
 * In de modi uit, zonder en tagfout moet de kaart byte voor byte gelijk zijn aan die zonder inc/amazon.php (= 1.3.12).
 */
require __DIR__ . '/wp-stub.php';
$T = dirname( __DIR__ ) . '/wp-content/themes/robotmaaierkompas-child/robotmaaierkompas';
define( 'RMK_DIR', $T );
$MODUS = $argv[1] ?? 'aan';

// Bol en Coolblue staan in alle modi aan (zoals live), zodat de volgorde gecontroleerd kan worden.
define( 'RMK_BOL_CLIENT_ID', 'test-id' );
define( 'RMK_BOL_CLIENT_SECRET', 'test-geheim' );
define( 'RMK_BOL_SITE_ID', '1549381' );
define( 'RMK_AFFILIATE_ACTIVE', true );
define( 'RMK_COOLBLUE_FEED_URL', 'https://productdata.awin.com/datafeed/download/apikey/GEHEIM/fid/95886/' );
define( 'RMK_COOLBLUE_AWMID', 85161 );
define( 'RMK_COOLBLUE_AWAFFID', 3126598 );
define( 'RMK_COOLBLUE_ACTIVE', true );
if ( 'aan' === $MODUS || 'uit' === $MODUS ) {
	define( 'RMK_AMAZON_TAG', 'robotmaaier-21' );
}
if ( 'tagfout' === $MODUS ) {
	define( 'RMK_AMAZON_TAG', 'robotmaaier-21&x=1' );
}
if ( 'aan' === $MODUS || 'tagfout' === $MODUS ) {
	define( 'RMK_AMAZON_ACTIVE', true );
}

function wp_remote_get( $url, $args = array() ) { return wp_remote_request( $url, $args + array( 'method' => 'GET' ) ); }
function get_temp_dir() { return sys_get_temp_dir() . '/'; }
function wp_mail() { return true; }

// Geen enkel HTTP-verzoek toegestaan: elk verzoek wordt geteld (en nooit echt gedaan, zie wp-stub.php).
$GLOBALS['verzoeken'] = array();
add_filter( 'pre_http_request', function ( $pre, $args, $url ) {
	$GLOBALS['verzoeken'][] = $url;
	return new WP_Error( 'geen_netwerk', 'Geen netwerk in de test.' );
}, 10, 3 );

/* ---------------------------------------------------------------- nagebootste modelgegevens */
$ASIN = array( 'M004' => 'B0GD2CXRNY', 'M008' => 'B0DR35G7P3', 'M011' => 'B0DMF82WY3', 'M050' => 'B0913J9BTB' );
$data = json_decode( file_get_contents( $T . '/data/modellen.json' ), true );
$m50  = $data['modellen'][0];
$m50  = array_merge( $m50, array( 'id' => 'M050', 'slug' => 'worx-landroid-s-wr165e-m500-plus', 'naam' => 'Worx Landroid S WR165E (M500 Plus)', 'ean' => null ) );
unset( $m50['bol'], $m50['coolblue'] );
$data['modellen'][] = $m50;
foreach ( $data['modellen'] as &$m ) {
	if ( 'M004' === $m['id'] || 'M008' === $m['id'] || 'M050' === $m['id'] ) {
		$m['amazon'] = array( 'asin' => $ASIN[ $m['id'] ], 'knop' => true );
	}
	if ( 'M011' === $m['id'] ) {
		$m['amazon'] = array( 'asin' => $ASIN['M011'], 'knop' => false );
	}
	if ( 'M008' === $m['id'] ) {
		$m['bol']      = array( 'product_url' => 'https://www.bol.com/nl/nl/p/dreame-a1-pro/9300000000000/', 'afbeelding' => null );
		$m['coolblue'] = array( 'merchant_product_id' => '962143', 'product_url' => 'https://www.coolblue.nl/product/962143/x.html' );
	}
}
unset( $m );
$MODELLEN = tempnam( sys_get_temp_dir(), 'rmkmod' );
file_put_contents( $MODELLEN, json_encode( $data ) );
add_filter( 'rmk_models_file', function () use ( $MODELLEN ) { return $MODELLEN; }, 20 );

require $T . '/inc/data.php';
require $T . '/inc/score.php';
require $T . '/inc/bol.php';
require $T . '/inc/coolblue.php';
require $T . '/inc/prijzen.php';
require $T . '/inc/redactie.php';

$GLOBALS['fail'] = 0;
function t( $n, $ok, $info = '' ) {
	echo ( $ok ? 'OK   ' : 'FOUT ' ) . $n . ( $info && ! $ok ? "\n       $info" : '' ) . "\n";
	$GLOBALS['fail'] += $ok ? 0 : 1;
}
$GLOBALS['nu'] = strtotime( '2026-10-31 12:00:00 Europe/Amsterdam' );
add_filter( 'rmk_coolblue_nu', function () { return $GLOBALS['nu']; } );
add_filter( 'rmk_bol_nu', function () { return $GLOBALS['nu']; } );

// Bol-aanbod en Coolblue-feed voor M008 (vers), zodat beide regels in de kaart staan.
$m8 = rmk_get_model( 'M008' );
update_option( RMK_BOL_AANBOD_OPTION, array( 'M008' => array( 'status' => 'ok', 'prijs' => 729.0, 'verkoper' => 'bol.com', 'partner' => false, 'url' => '', 'ean' => preg_replace( '/\D/', '', $m8['ean'] ), 'tijd' => $GLOBALS['nu'] ) ) );
update_option( RMK_CB_STORE_OPTION, array(
	'opgehaald' => $GLOBALS['nu'] - 3600, 'hash' => str_repeat( 'a', 64 ), 'hash_sinds' => $GLOBALS['nu'] - 3600, 'rijen' => 2324,
	'producten' => array( 'M008' => array( 'merchant_product_id' => '962143', 'prijs' => 729.0, 'in_stock' => 1, 'afbeelding' => '', 'url' => 'https://www.coolblue.nl/product/962143/x.html' ) ),
) );

function kaart( $id ) { // productkaart zoals op de hub en pagina 1
	$m = rmk_get_model( $id );
	$a = 'p-' . $m['slug'];
	return '<article class="rmk-product" aria-labelledby="' . $a . '"><div class="rmk-product__head rmk-product__head--nomedia" style="grid-template-columns: 1fr"><div class="rmk-product__title"><h3 id="' . $a . '">' . $m['naam'] . '</h3>'
		. '<div class="rmk-scorecell" data-rmk-score data-model="' . $id . '"><div class="rmk-minis"><b data-out="total">–</b><small data-out="kind">Score</small></div><span class="rmk-provisional" data-out="label" hidden></span></div></div></div>'
		. '<div class="rmk-product__aside rmk-offers"><div class="rmk-offer"></div></div></article>';
}
function amregel( $html ) {
	return preg_match( '#<div class="rmk-offer rmk-offer--stack rmk-offer--amazon".*?</div>#s', $html, $m ) ? $m[0] : '';
}
$IDS = array( 'M002', 'M004', 'M008', 'M011', 'M050' );

// Referentie: dezelfde kaarten met de code van 1.3.12 (inc/amazon.php nog niet geladen; prijzen.php controleert function_exists).
$ref = array();
foreach ( $IDS as $id ) {
	$ref[ $id ] = rmk_fill_offers( kaart( $id ) );
}
$ref_content = apply_filters( 'the_content', '<p>Inleiding</p>' . implode( '', $ref ) );
$ref_route   = json_encode( rmk_bol_prijzen_publiek( implode( ',', $IDS ) ) );
$ref_cfg     = json_encode( apply_filters( 'rmk_config', array() ) );
$ref_opties  = $GLOBALS['wp_options'];

require $T . '/inc/amazon.php';
$kaart = array();
foreach ( $IDS as $id ) {
	$kaart[ $id ] = rmk_fill_offers( kaart( $id ) );
}
$content = apply_filters( 'the_content', '<p>Inleiding</p>' . implode( '', $kaart ) );

echo "\nModus: $MODUS\n";
t( 'Bol- en Coolblue-regel staan in de referentiekaart van M008', false !== strpos( $ref['M008'], 'data-rmk-bol-model="M008"' ) && false !== strpos( $ref['M008'], 'data-rmk-cb-model="M008"' ) );

if ( 'aan' !== $MODUS ) {
	foreach ( $IDS as $id ) {
		t( "$id: kaart byte voor byte gelijk aan 1.3.12", $ref[ $id ] === $kaart[ $id ] );
	}
	t( 'pagina-inhoud (met advertentie-regel) byte voor byte gelijk', $ref_content === $content );
	t( 'nergens "amazon" in de kaarten', false === stripos( implode( '', $kaart ), 'amazon' ) );
	t( 'rmk_amazon_zichtbaar() is false', false === rmk_amazon_zichtbaar() );
	if ( 'tagfout' === $MODUS ) {
		t( 'ongeldige tag: status meldt dat', false !== strpos( rmk_amazon_status_tekst(), 'geen geldige tag' ) );
	}
	if ( 'uit' === $MODUS ) {
		t( 'status: tag aanwezig, knop verborgen', false !== strpos( rmk_amazon_status_tekst(), 'verborgen (RMK_AMAZON_ACTIVE uit)' ) );
	}
} else {
	$r4 = amregel( $kaart['M004'] );
	$r8 = amregel( $kaart['M008'] );
	t( 'M004 (ASIN, Knop: ja): Amazon-knop', '' !== $r4 );
	t( 'M008 (ASIN, Knop: ja): Amazon-knop', '' !== $r8 );
	t( 'M002 (geen ASIN): geen knop', '' === amregel( $kaart['M002'] ) && $ref['M002'] === $kaart['M002'] );
	t( 'M011 (Knop: nee): geen knop', '' === amregel( $kaart['M011'] ) && $ref['M011'] === $kaart['M011'] );
	t( 'M050 (Knop: ja in het blad, uitgesloten): geen knop', '' === amregel( $kaart['M050'] ) && $ref['M050'] === $kaart['M050'] );
	t( 'M050 staat in rmk_amazon_uitgesloten() met een reden', ! empty( rmk_amazon_uitgesloten()['M050'] ) );

	// Vorm van de link: exact https://www.amazon.nl/dp/<ASIN>?tag=robotmaaier-21
	preg_match_all( '#<a\b[^>]*>#', $r4 . $r8, $as );
	t( 'precies één link per Amazon-regel', 2 === count( $as[0] ) );
	foreach ( array( 'M004' => $r4, 'M008' => $r8 ) as $id => $r ) {
		preg_match( '#href="([^"]*)"#', $r, $h );
		t( "$id: href exact https://www.amazon.nl/dp/{$ASIN[$id]}?tag=robotmaaier-21", ( $h[1] ?? '' ) === 'https://www.amazon.nl/dp/' . $ASIN[ $id ] . '?tag=robotmaaier-21', $h[1] ?? '' );
		$p = parse_url( html_entity_decode( $h[1] ?? '' ) );
		t( "$id: alleen de parameter tag, geen fragment, host www.amazon.nl", 'tag=robotmaaier-21' === ( $p['query'] ?? '' ) && ! isset( $p['fragment'] ) && 'www.amazon.nl' === $p['host'] && 'https' === $p['scheme'] );
		t( "$id: rel=\"sponsored nofollow\"", false !== strpos( $r, 'rel="sponsored nofollow"' ) );
		t( "$id: knoptekst en regel eronder", false !== strpos( $r, '>Bekijk bij Amazon</a><span class="rmk-offer__src">Je gaat naar Amazon.nl. Prijs, beschikbaarheid en verkoper bekijk je daar.</span>' ) );
		t( "$id: geen prijs, foto, beoordeling, korting of doorgestreepte prijs", ! preg_match( '#<img|<del|<s>|<strike|euro|€|\d+,\d\d|ster|beoordel|review|korting|aanbieding|%|line-through|data-rmk-prijs|data-rmk-cb|data-rmk-bol#i', $r ) );
		t( "$id: geen verkorte link (amzn.to, a.co)", ! preg_match( '#amzn\.to|//a\.co/#', $r ) );
		t( "$id: geen target of onclick (statische link)", ! preg_match( '#target=|onclick|data-rmk-direct#', $r ) );
	}
	$k = $kaart['M008'];
	t( 'M008: volgorde Bol, Coolblue, Amazon', strpos( $k, 'data-rmk-bol-model' ) < strpos( $k, 'data-rmk-cb-model' ) && strpos( $k, 'data-rmk-cb-model' ) < strpos( $k, 'rmk-offer--amazon' ) );
	t( 'M008: Amazon-regel is de laatste regel in de kaart', false === strpos( substr( $k, strpos( $k, 'rmk-offer--amazon' ) ), 'rmk-offer--', 20 ) );
	t( 'M008: alles vóór de Amazon-regel gelijk aan 1.3.12', str_replace( $r8, '', $k ) === $ref['M008'] );
	t( 'M004: alles behalve de Amazon-regel gelijk aan 1.3.12', str_replace( $r4, '', $kaart['M004'] ) === $ref['M004'] );
	t( 'scorecellen ongewijzigd', preg_replace( '#<div class="rmk-offer rmk-offer--stack rmk-offer--amazon".*?</div>#s', '', implode( '', $kaart ) ) === implode( '', $ref ) );

	// Advertentie-regel: één keer, boven de eerste knop (blijft boven Bol).
	t( 'advertentie-regel één keer, boven de eerste knop', 1 === substr_count( $content, 'rmk-affnote' ) && strpos( $content, 'rmk-affnote' ) < strpos( $content, 'data-rmk-bol' ) );
	t( 'pagina-inhoud: alleen de twee Amazon-regels erbij', str_replace( array( $r4, $r8 ), '', $content ) === $ref_content );

	// Alleen Amazon in een kaart (geen Bol, geen Coolblue): advertentie-regel boven de Amazon-knop.
	$alleen = apply_filters( 'the_content', '<p>x</p>' . $kaart['M004'] );
	t( 'alleen een Amazon-knop op de pagina: advertentie-regel erboven', 1 === substr_count( $alleen, 'rmk-affnote' ) && strpos( $alleen, 'rmk-affnote' ) < strpos( $alleen, 'rmk-offer--amazon' ) );

	t( 'status: zichtbaar, 2 modellen met een knop (M004, M008; niet M011 en M050)', false !== strpos( rmk_amazon_status_tekst(), 'zichtbaar (2 modellen' ), rmk_amazon_status_tekst() );

	// Robuustheid van de modelgegevens
	$m = rmk_get_model( 'M004' );
	foreach ( array( 'kleine letters' => 'b0gd2cxrny', 'te kort' => 'B0GD2CXRN', 'met parameter' => 'B0GD2CXRNY?x=1', 'met pad' => '../B0GD2CXR' ) as $wat => $asin ) {
		$m['amazon'] = array( 'asin' => $asin, 'knop' => true );
		t( "ongeldige ASIN ($wat): geen knop", '' === rmk_amazon_regel_html( $m ) );
	}
	$m['amazon'] = array( 'asin' => 'B0GD2CXRNY', 'knop' => 'ja' );
	t( 'knop "ja" als tekst (geen true): geen knop', '' === rmk_amazon_regel_html( $m ) );
}

// Dataroute: blok amazon
$fout = function ( $a ) use ( $data ) { $d = $data; $d['modellen'][1]['amazon'] = $a; return rmk_validate_modellen( $d ); };
t( 'dataroute: modelgegevens met blok amazon {asin, knop} toegestaan', array() === rmk_validate_modellen( $data ) );
t( 'dataroute: extra veld (prijs) geweigerd', (bool) $fout( array( 'asin' => 'B0GD2CXRNY', 'knop' => true, 'prijs' => 899 ) ) );
t( 'dataroute: afbeelding geweigerd', (bool) $fout( array( 'asin' => 'B0GD2CXRNY', 'knop' => true, 'afbeelding' => 'https://m.media-amazon.com/x.jpg' ) ) );
t( 'dataroute: ongeldige ASIN geweigerd', (bool) $fout( array( 'asin' => 'b0gd2cxrny', 'knop' => true ) ) );
t( 'dataroute: knop als tekst geweigerd', (bool) $fout( array( 'asin' => 'B0GD2CXRNY', 'knop' => 'ja' ) ) );

// Geen verzoek naar Amazon (of waar dan ook), prijsroute en configuratie van rmk.js ongewijzigd.
do_action( 'init' );
t( 'prijsroute /rmk/v1/bol-prijs gelijk aan 1.3.12', json_encode( rmk_bol_prijzen_publiek( implode( ',', $IDS ) ) ) === $ref_route );
t( 'rmk.js-configuratie gelijk aan 1.3.12', json_encode( apply_filters( 'rmk_config', array() ) ) === $ref_cfg );
t( 'geen enkel HTTP-verzoek (dus ook niet naar Amazon)', array() === $GLOBALS['verzoeken'], implode( ', ', $GLOBALS['verzoeken'] ) );
t( 'geen opties veranderd door inc/amazon.php', $ref_opties === array_intersect_key( $GLOBALS['wp_options'], $ref_opties ) );
t( 'geen ingeplande taak voor Amazon', ! array_filter( array_keys( $GLOBALS['wp_cron'] ), function ( $h ) { return false !== stripos( $h, 'amazon' ); } ) );

echo "\n" . ( $GLOBALS['fail'] ? $GLOBALS['fail'] . ' FOUT(EN)' : 'Alles geslaagd' ) . "\n";
exit( $GLOBALS['fail'] ? 1 : 0 );
