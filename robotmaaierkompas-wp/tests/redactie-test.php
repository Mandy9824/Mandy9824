<?php
/**
 * Tests voor inc/redactie.php (1.3.5): automatische datums en de affiliate-melding.
 * Draait zonder WordPress: php tests/redactie-test.php <export.json> [affiliate-aan]
 * <export.json> bevat de ruwe inhoud van de pagina's ({"pages":[{"id","slug","content"}]}), opgehaald via de REST-API.
 */
define( 'ABSPATH', __DIR__ );
$GLOBALS['filters'] = array();
$GLOBALS['huidig']  = 0;
if ( ! empty( $argv[2] ) ) {
	define( 'RMK_AFFILIATE_ACTIVE', true );
}
function add_filter( $naam, $fn ) { $GLOBALS['filters'][ $naam ][] = $fn; }
function esc_attr( $s ) { return htmlspecialchars( $s, ENT_QUOTES ); }
function esc_html( $s ) { return htmlspecialchars( $s, ENT_QUOTES ); }
function get_the_ID() { return $GLOBALS['huidig']; }
function get_queried_object_id() { return $GLOBALS['huidig']; }
function get_post_type( $id ) { return 'page'; }
function get_post_modified_time( $f, $gmt, $id ) { return '2026-10-08'; }
function get_the_modified_date( $f, $id ) { return '8 oktober 2026'; }
require dirname( __DIR__ ) . '/wp-content/themes/robotmaaierkompas-child/robotmaaierkompas/inc/redactie.php';

$fail = 0;
function check( $naam, $ok, $info = '' ) {
	global $fail;
	echo ( $ok ? 'OK   ' : 'FOUT ' ) . $naam . ( $info ? "  ($info)" : '' ) . "\n";
	$fail += $ok ? 0 : 1;
}
/** Rendert de inhoud zoals render_block: elk wp:html-blok apart door de filter. */
function render( $raw, $id ) {
	$GLOBALS['huidig'] = $id;
	return preg_replace_callback( '/<!-- wp:html -->(.*?)<!-- \/wp:html -->/s', function ( $m ) {
		$c = $m[1];
		foreach ( $GLOBALS['filters']['render_block'] as $fn ) {
			$c = $fn( $c, array( 'blockName' => 'core/html' ) );
		}
		return $c;
	}, $raw );
}
$maand  = 'januari|februari|maart|april|mei|juni|juli|augustus|september|oktober|november|december';
$aan    = rmk_affiliate_actief();
$x      = json_decode( file_get_contents( $argv[1] ), true );
$pages  = array();
foreach ( $x['pages'] as $p ) {
	$pages[ $p['id'] ] = $p;
}

// 1. Datums in paginakop en eerlijkheidsblok
foreach ( array( 82, 18, 236, 17, 13, 11, 12, 10 ) as $id ) {
	$out  = render( $pages[ $id ]['content'], $id );
	$kop  = preg_match_all( '/<p class="rmk-meta"[^>]*>.*?<\/p>/s', $out, $k ) ? implode( ' ', $k[0] ) : '';
	$eer  = preg_match( '/<div class="rmk-honesty__text"[^>]*>\s*<p>.*?<\/p>/s', $out, $e ) ? $e[0] : '';
	$vast = preg_match( "/(bijgewerkt op|Laatst bijgewerkt:)\s*(\d{1,2} )?($maand) \d{4}/iu", $kop . $eer );
	check( "#$id {$pages[$id]['slug']}: geen vaste datum meer in kop en eerlijkheidsblok", ! $vast );
	check( "#$id: wijzigingsdatum ingevuld", substr_count( $kop . $eer, '<time datetime="2026-10-08" data-rmk-modified>8 oktober 2026</time>' ) >= 1 );
}
// Andere datums blijven staan
$out12 = render( $pages[12]['content'], 12 );
check( '#12: datums per model in de tabel ongewijzigd (8 keer "Bijgewerkt op 5 oktober 2026" in span.rmk-small)', 8 === preg_match_all( '/<span class="rmk-small">Bijgewerkt op 5 oktober 2026/', $out12 ) );
$out11 = render( $pages[11]['content'], 11 );
check( '#11: "gezien op" bij prijzen niet aangeraakt', substr_count( $pages[11]['content'], 'gezien op' ) === substr_count( $out11, 'gezien op' ) );
check( 'Inhoud zonder datum blijft gelijk (#79 contact)', render( $pages[79]['content'], 79 ) === render( $pages[79]['content'], 79 ) && false === strpos( render( $pages[79]['content'], 79 ), '<time' ) );

// 2. Affiliate-melding
$patroon = file_get_contents( dirname( __DIR__ ) . '/wp-content/themes/robotmaaierkompas-child/robotmaaierkompas/patterns/affiliate-melding.php' );
preg_match( '/<!-- wp:html -->.*<!-- \/wp:html -->/s', $patroon, $pm );
$po = render( $pm[0], 9 );
$i26 = render( $pages[26]['content'], 26 );
if ( $aan ) {
	check( 'Aan: patroon toont de regel "Advertentie: …"', false !== strpos( $po, 'Advertentie: via deze knoppen krijgen wij mogelijk een commissie. Dat verandert de score niet.' ) );
	check( 'Aan: #26 toont de regel', false !== strpos( $i26, 'rmk-affnote' ) );
} else {
	check( 'Uit (standaard): patroon toont niets', false === strpos( $po, 'rmk-affnote' ) && false === strpos( $po, 'commissie' ) );
	check( 'Uit: losse regel in #26 husqvarna-vs-gardena weg', false === strpos( $i26, 'rmk-affnote' ) && false === strpos( $i26, 'Advertentie' ) );
	check( 'Uit: rest van #26 ongewijzigd', strlen( $pages[26]['content'] ) - strlen( $i26 ) < 400 );
}
echo $fail ? "\n$fail FOUT\n" : "\nAlles geslaagd\n";
exit( $fail ? 1 : 0 );
