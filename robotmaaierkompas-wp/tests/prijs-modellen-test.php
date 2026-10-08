<?php
/**
 * Prijsregels (inc/prijzen.php) op de echte modelgegevens, zonder WordPress.
 * Gebruik: php tests/prijs-modellen-test.php <modellen.json> [datum JJJJ-MM-DD]
 * <modellen.json>: de "data" uit GET /wp-json/rmk/v1/modellen (of data/modellen.json uit het thema).
 * Toont per model wat de kaart laat zien op de gegeven datum en controleert de regels:
 * hoogstens 14 dagen oud, geen Bol of marketplace, en zonder geldige prijs alleen "Bekijk de actuele prijs".
 */
define( 'ABSPATH', __DIR__ );
function add_filter() {}
function add_action() {}
function apply_filters( $n, $v ) { return $v; }
function esc_html( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES ); }
function esc_attr( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES ); }
function esc_url( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES ); }
function wp_parse_url( $u, $c = -1 ) { return parse_url( $u, $c ); }
function wp_timezone() { return new DateTimeZone( 'Europe/Amsterdam' ); }
function wp_next_scheduled() { return false; }
function wp_schedule_event() {}
$GLOBALS['rmk_data'] = json_decode( file_get_contents( $argv[1] ), true );
function rmk_models_data() { return $GLOBALS['rmk_data']; }
function rmk_get_model( $id ) {
	foreach ( rmk_models_data()['modellen'] as $m ) {
		if ( $m['id'] === $id ) {
			return $m;
		}
	}
	return null;
}
require dirname( __DIR__ ) . '/wp-content/themes/robotmaaierkompas-child/robotmaaierkompas/inc/prijzen.php';

$dag  = isset( $argv[2] ) ? $argv[2] : '2026-10-08';
$fail = 0;
foreach ( rmk_models_data()['modellen'] as $m ) {
	$p     = isset( $m['prijs'] ) ? $m['prijs'] : null;
	$geldig = rmk_valid_price( $m, $dag );
	$html  = rmk_offer_html( $m, $dag );
	$tekst = trim( preg_replace( '/\s+/', ' ', strip_tags( $html ) ) );
	$bol   = $p && ( false !== stripos( (string) ( $p['winkel'] ?? '' ), 'bol' ) || false !== stripos( (string) ( $p['url'] ?? '' ), 'bol.com' ) );
	$fout  = array();
	if ( $geldig && rmk_price_age_days( $p['datum'], $dag ) > 14 ) { $fout[] = 'prijs ouder dan 14 dagen getoond'; }
	if ( $bol && ( $geldig || false !== stripos( $html, 'bol' ) ) ) { $fout[] = 'Bol-prijs getoond'; }
	if ( ! $geldig && $html && false !== strpos( $tekst, 'euro' ) ) { $fout[] = 'bedrag zonder geldige prijs'; }
	if ( ! $geldig && $html && 'Bekijk de actuele prijs' !== $tekst ) { $fout[] = 'zonder geldige prijs iets anders dan "Bekijk de actuele prijs"'; }
	$fail += count( $fout );
	printf( "%-5s %-34s %-22s %s%s\n", $m['id'], mb_substr( $m['naam'] ?? '', 0, 34 ),
		$p ? ( ( $p['bedrag'] ?? '?' ) . ' ' . ( $p['winkel'] ?? '?' ) . ' ' . ( $p['datum'] ?? '?' ) ) : '(geen prijs)',
		$tekst ?: '(geen prijsblok)', $fout ? '   <-- FOUT: ' . implode( ', ', $fout ) : '' );
}
echo $fail ? "\n$fail FOUT op $dag\n" : "\nRegels in orde op $dag\n";
exit( $fail ? 1 : 0 );
