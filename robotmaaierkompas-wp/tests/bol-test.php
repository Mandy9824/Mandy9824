<?php
/**
 * Test van de Bol-prijstaak met een NAGEBOOTSTE API (geen echte gegevens, geen netwerk).
 * Draaien: wp eval-file tests/bol-test.php
 * Na afloop worden alle testgegevens verwijderd.
 */
if ( ! defined( 'RMK_BOL_CLIENT_ID' ) ) { define( 'RMK_BOL_CLIENT_ID', 'test' ); define( 'RMK_BOL_CLIENT_SECRET', 'test' ); }
$GLOBALS["fail"] = 0;
function t( $n, $c, $i = "" ) { global $fail; echo ( $c ? 'OK   ' : 'FOUT ' ) . $n . ( $i ? "  ($i)" : '' ) . "\n"; if ( ! $c ) $fail++; }

$calls = array();
add_filter( 'pre_http_request', function ( $pre, $args, $url ) use ( &$calls ) {
	$calls[] = array( microtime( true ), $url );
	if ( false !== strpos( $url, 'login.bol.com' ) ) {
		return array( 'response' => array( 'code' => 200 ), 'headers' => array(), 'body' => wp_json_encode( array( 'access_token' => 'tok', 'expires_in' => 299 ) ) );
	}
	if ( false !== strpos( $url, '/products/0000000000001/' ) ) {
		return array( 'response' => array( 'code' => 200 ), 'headers' => array(), 'body' => wp_json_encode( array( 'offer' => array( 'price' => 123.45, 'deliveryDescription' => 'testlevering', 'seller' => array( 'name' => 'testverkoper' ) ), 'url' => 'https://www.bol.com/test' ) ) );
	}
	return array( 'response' => array( 'code' => 404 ), 'headers' => array(), 'body' => '' );
}, 10, 3 );

delete_transient( 'rmk_bol_token' );
update_option( RMK_BOL_EAN_OPTION, array( 'M002' => '0000000000001', 'M005' => '0000000000002', 'M001' => '0000000000003', 'M003' => '0000000000004' ) );
$log = rmk_bol_fetch_all();
t( 'Taak draait, 1 prijs gevonden', 1 === $log['ok'], wp_json_encode( $log['fout'] ) );
$min = INF;
for ( $i = 1; $i < count( $calls ); $i++ ) { $min = min( $min, $calls[ $i ][0] - $calls[ $i - 1 ][0] ); }
t( 'Maximaal 10 verzoeken per seconde', $min >= 0.099, count( $calls ) . ' verzoeken, kortste tussentijd ' . round( $min, 3 ) . ' s' );
$p = rmk_bol_price( 'M002' );
t( 'Prijs opgeslagen met tijdstip', $p && 123.45 === $p['prijs'] && abs( time() - $p['opgehaald'] ) < 60 );
t( 'Geen aanbod bij 404', 'geen aanbod' === get_option( RMK_BOL_OPTION )['M005']['status'] );
$html = rmk_bol_offer_html( 'M002', 'segway-navimow-i206-awd' );
t( 'Toont prijs met "Bron: bol.com"', false !== strpos( $html, 'Bron: bol.com' ) && false !== strpos( $html, '123,45' ), strip_tags( $html ) );

$store = get_option( RMK_BOL_OPTION );
$store['M002']['opgehaald'] = time() - DAY_IN_SECONDS - 1;
update_option( RMK_BOL_OPTION, $store );
t( 'Prijs ouder dan 24 uur wordt niet getoond', null === rmk_bol_price( 'M002' ) );
$html = rmk_bol_offer_html( 'M002', 'segway-navimow-i206-awd' );
t( 'Lege toestand "Prijs wordt bijgewerkt" met bron', false !== strpos( $html, 'Prijs wordt bijgewerkt' ) && false === strpos( $html, '123' ) && false !== strpos( $html, 'Bron: bol.com' ) );
add_filter( 'rmk_bol_max_age', function () { return 3 * DAY_IN_SECONDS; } );
t( 'Filter kan de 24 uur niet verruimen', null === rmk_bol_price( 'M002' ) );
t( 'Taak is ingepland', (bool) wp_next_scheduled( RMK_BOL_HOOK ), wp_date( 'Y-m-d H:i', wp_next_scheduled( RMK_BOL_HOOK ) ) );

delete_option( RMK_BOL_OPTION ); delete_option( RMK_BOL_EAN_OPTION ); delete_option( 'rmk_bol_laatste_run' ); delete_transient( 'rmk_bol_token' );
echo $GLOBALS["fail"] ? $GLOBALS["fail"] . " mislukt\n" : "Alle Bol-tests geslaagd (testgegevens verwijderd)\n";
