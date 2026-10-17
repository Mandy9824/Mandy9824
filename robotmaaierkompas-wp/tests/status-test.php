<?php
/**
 * Test van het statusoverzicht (inc/bouw.php, rmk_status_checks), regel "Bol-prijstaak draait" (1.3.8):
 * "Te oud: stel een echte cron in" alleen als de controle mislukt. Zonder WordPress en zonder sleutels.
 * Draaien: php tests/status-test.php            (met nagebootste Bol-constanten)
 *          php tests/status-test.php zonder     (zonder Bol-constanten: geen regel over de prijstaak)
 */
require __DIR__ . '/wp-stub.php';
$T = dirname( __DIR__ ) . '/wp-content/themes/robotmaaierkompas-child/robotmaaierkompas';
define( 'RMK_DIR', $T );
const RMK_LINKS_OPTION = 'rmk_links';
$ZONDER = in_array( 'zonder', $argv, true );
if ( ! $ZONDER ) {
	define( 'RMK_BOL_CLIENT_ID', 'test-id-1234' );
	define( 'RMK_BOL_CLIENT_SECRET', 'test-geheim-5678' );
	define( 'RMK_BOL_SITE_ID', '1549381' );
}
require $T . '/inc/bol.php';
require $T . '/inc/bouw.php';
function home_url() { return 'https://robotmaaierkompas.nl'; }
function site_url() { return 'https://robotmaaierkompas.nl'; }
function is_ssl() { return true; }
function get_posts() { return array(); }
function wp_count_posts() { return (object) array( 'publish' => 18 ); }
function rmk_models_data() { return array( 'modellen' => array() ); }
function rmk_affiliate_actief() { return true; }
function wp_image_editor_supports() { return true; }
function wp_get_attachment_url() { return ''; }
function get_the_author_meta() { return ''; }

$GLOBALS['fail'] = 0;
function t( $n, $ok, $info = '' ) {
	echo ( $ok ? 'OK   ' : 'FOUT ' ) . $n . ( $info && ! $ok ? "\n       $info" : '' ) . "\n";
	$GLOBALS['fail'] += $ok ? 0 : 1;
}
function regel() {
	foreach ( rmk_status_checks() as $c ) {
		if ( 0 === strpos( $c['label'], 'Bol-prijstaak draait' ) ) {
			return $c;
		}
	}
	return null;
}
if ( $ZONDER ) {
	t( 'Zonder Bol-constanten: geen regel over de prijstaak', null === regel() );
} else {
	$GLOBALS['wp_cron'][ RMK_BOL_RONDE_HOOK ] = array( time() + 3 * HOUR_IN_SECONDS, 'rmk_zes_uur' );
	update_option( RMK_BOL_LOG_OPTION, array( array( 'start' => time() - 2 * HOUR_IN_SECONDS ) ) );
	$r = regel();
	t( 'Ronde 2 uur geleden: OK, zonder "Te oud"', $r && $r['ok'] && false === strpos( $r['info'], 'Te oud' ) && preg_match( '/^laatste ronde \S+ \S+, volgende \S+ \S+\.$/', $r['info'] ), $r ? $r['info'] : '' );
	update_option( RMK_BOL_LOG_OPTION, array( array( 'start' => time() - 9 * HOUR_IN_SECONDS ) ) );
	$r = regel();
	t( 'Ronde 9 uur geleden: mislukt, met "Te oud: stel een echte cron in"', $r && ! $r['ok'] && false !== strpos( $r['info'], '. Te oud: stel een echte cron in (wp rmk bol-ronde).' ), $r ? $r['info'] : '' );
	update_option( RMK_BOL_LOG_OPTION, array() );
	$r = regel();
	t( 'Nog geen ronde: mislukt, met "Te oud"', $r && ! $r['ok'] && 0 === strpos( $r['info'], 'nog geen ronde' ) && false !== strpos( $r['info'], 'Te oud' ), $r ? $r['info'] : '' );
}
echo $GLOBALS['fail'] ? "\n{$GLOBALS['fail']} FOUT\n" : "\nAlles geslaagd.\n";
exit( $GLOBALS['fail'] ? 1 : 0 );
