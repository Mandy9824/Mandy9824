<?php
/**
 * Test thema 1.3.8 met NAGEBOOTSTE antwoorden, zonder netwerk en zonder sleutels:
 * - inc/bol-bewaking.php: e-mail als de laatste geslaagde Bol-ronde ouder is dan 8 uur, één per storing, zonder secrets;
 * - specificatiekaart: chip "Verbinding" met Wifi en Bluetooth, geen chip bij een onbekende waarde,
 *   geen "Geen productfoto beschikbaar".
 * Draaien: php tests/bewaking-test.php            (met nagebootste Bol-constanten)
 *          php tests/bewaking-test.php zonder     (zonder Bol-constanten: er mag niets gebeuren)
 */
require __DIR__ . '/wp-stub.php';
$T = dirname( __DIR__ ) . '/wp-content/themes/robotmaaierkompas-child/robotmaaierkompas';
define( 'RMK_DIR', $T );
$ZONDER = in_array( 'zonder', $argv, true );
if ( ! $ZONDER ) {
	define( 'RMK_BOL_CLIENT_ID', 'test-id-1234' );
	define( 'RMK_BOL_CLIENT_SECRET', 'test-geheim-5678' );
	define( 'RMK_BOL_SITE_ID', '1549381' );
}
require $T . '/inc/data.php';
require $T . '/inc/score.php';
require $T . '/inc/bol.php';
require $T . '/inc/bol-bewaking.php';
require $T . '/inc/prijzen.php';

$GLOBALS['fail'] = 0;
function t( $n, $ok, $info = '' ) {
	echo ( $ok ? 'OK   ' : 'FOUT ' ) . $n . ( $info && ! $ok ? "\n       $info" : '' ) . "\n";
	$GLOBALS['fail'] += $ok ? 0 : 1;
}
$GLOBALS['mails'] = array();
function wp_mail( $aan, $onderwerp, $tekst ) {
	$GLOBALS['mails'][] = compact( 'aan', 'onderwerp', 'tekst' );
	return empty( $GLOBALS['mail_faalt'] );
}
$GLOBALS['wp_options']['admin_email'] = 'beheer@example.test';
$GLOBALS['nu'] = strtotime( '2026-10-17 12:00:00 Europe/Amsterdam' );
add_filter( 'rmk_bol_nu', function () { return $GLOBALS['nu']; } );
function ronde( $start, $soort ) { // nagebootst rondelog, zoals rmk_bol_ronde() het schrijft
	$log = array( 'start' => $start, 'eind' => $start + 5, 'ok' => 0, 'geen_aanbod' => 0, 'ongeldig' => 0, 'fout' => 0, 'verzoeken' => 0, 'gestopt' => false, 'melding' => '' );
	if ( 'ok' === $soort ) {
		$log['ok'] = 11;
	} elseif ( 'token' === $soort ) {
		$log['gestopt'] = true;
		$log['melding'] = 'Gestopt na de eerste tokenfout (login.bol.com: HTTP 401, invalid_client, Bearer abcdefghijklmnop, test-geheim-5678). Geen aanbiedingen opgehaald; controleer RMK_BOL_CLIENT_ID en RMK_BOL_CLIENT_SECRET.';
	} elseif ( '500' === $soort ) {
		$log['fout'] = 11;
		$log['modellen'] = array( 'M002' => 'fout: HTTP 500, Internal Server Error' );
	}
	$hist = (array) get_option( RMK_BOL_LOG_OPTION, array() );
	array_unshift( $hist, $log );
	update_option( RMK_BOL_LOG_OPTION, array_slice( $hist, 0, 20 ), false );
	do_action( 'rmk_bol_na_ronde', $log );
}
$H = HOUR_IN_SECONDS;

if ( $ZONDER ) {
	$voor = $GLOBALS['wp_options'];
	ronde( $GLOBALS['nu'] - 30 * $H, 'token' ); // ook met een oud log: niets doen
	$voor = $GLOBALS['wp_options'];
	do_action( 'init' );
	$r = rmk_bol_bewaking();
	do_action( 'shutdown' );
	t( 'Zonder Bol-constanten: bewaking "uit"', 'uit' === $r['status'] );
	t( 'Zonder Bol-constanten: geen e-mail', ! $GLOBALS['mails'] );
	t( 'Zonder Bol-constanten: geen geplande taken', ! wp_next_scheduled( RMK_BOL_BEWAKING_HOOK ) && ! wp_next_scheduled( RMK_BOL_RONDE_HOOK ) );
	t( 'Zonder Bol-constanten: geen opties geschreven', $voor === $GLOBALS['wp_options'] );
	echo $GLOBALS['fail'] ? "\n{$GLOBALS['fail']} FOUT\n" : "\nAlles geslaagd.\n";
	exit( $GLOBALS['fail'] ? 1 : 0 );
}

/* ---------------------------------------------------------------- bewaking */
do_action( 'init' );
t( 'Taak rmk_bol_bewaking elk uur gepland', 'hourly' === ( $GLOBALS['wp_cron'][ RMK_BOL_BEWAKING_HOOK ][1] ?? '' ) );
t( 'Nog geen ronde: niets te melden', 'ok' === rmk_bol_bewaking()['status'] && ! $GLOBALS['mails'] );

ronde( $GLOBALS['nu'] - 2 * $H, 'ok' );
t( 'Geslaagde ronde 2 uur geleden: ok, geen e-mail', 'ok' === rmk_bol_bewaking()['status'] && ! $GLOBALS['mails'] );
t( 'Geslaagde ronde bewaard in rmk_bol_laatst_geslaagd', $GLOBALS['nu'] - 2 * $H === get_option( RMK_BOL_GESLAAGD_OPTION ) );

$GLOBALS['nu'] += 4 * $H;
ronde( $GLOBALS['nu'], 'token' );
t( 'Tokenfout, laatste geslaagde 6 uur geleden: nog geen e-mail', 'ok' === rmk_bol_bewaking()['status'] && ! $GLOBALS['mails'] );

$GLOBALS['nu'] += 2 * $H + 60; // laatste geslaagde nu 8 uur en 1 minuut geleden
ronde( $GLOBALS['nu'] - 30, 'token' );
$r = rmk_bol_bewaking();
$m = $GLOBALS['mails'][0] ?? array( 'aan' => '', 'onderwerp' => '', 'tekst' => '' );
t( 'Ouder dan 8 uur: één e-mail aan de beheerder', 'gemeld' === $r['status'] && 1 === count( $GLOBALS['mails'] ) && 'beheer@example.test' === $m['aan'] );
t( 'E-mail noemt de tijd van de laatste geslaagde ronde', false !== strpos( $m['tekst'], 'De laatste geslaagde Bol-ronde was op 17-10-2026 10:00 (8 uur geleden).' ), $m['tekst'] );
t( 'E-mail noemt de laatste ronde en de laatste fout', false !== strpos( $m['tekst'], 'Laatste ronde: 17-10-2026 18:00 (gestopt).' ) && false !== strpos( $m['tekst'], 'Laatste fout: 17-10-2026 18:00: Gestopt na de eerste tokenfout' ), $m['tekst'] );
t( 'E-mail zonder secrets (geen client-id, secret, site-ID of token)', false === strpos( $m['tekst'] . $m['onderwerp'], 'test-geheim-5678' ) && false === strpos( $m['tekst'], 'test-id-1234' ) && false === strpos( $m['tekst'], '1549381' ) && false === strpos( $m['tekst'], 'abcdefghijklmnop' ) && false === strpos( $m['tekst'], 'partner.bol.com' ), $m['tekst'] );
t( 'Onderwerp', '[Robotmaaierkompas] Bol-prijzen niet bijgewerkt sinds 17-10 10:00' === $m['onderwerp'], $m['onderwerp'] );

for ( $i = 0; $i < 5; $i++ ) { // dezelfde storing: elk uur een controle, ook via shutdown
	$GLOBALS['nu'] += $H;
	ronde( $GLOBALS['nu'], 0 === $i % 2 ? 'token' : '500' );
	rmk_bol_bewaking();
	do_action( 'shutdown' );
}
t( 'Zelfde storing (5 uur later, nog steeds mislukt): geen tweede e-mail', 1 === count( $GLOBALS['mails'] ) );

ronde( $GLOBALS['nu'] + 60, 'ok' );
$GLOBALS['nu'] += 120;
t( 'Weer een geslaagde ronde: storing voorbij', 'ok' === rmk_bol_bewaking()['status'] && false === get_option( RMK_BOL_STORING_OPTION, false ) );

$GLOBALS['nu'] += 9 * $H; // nieuwe storing: de cron ligt stil, geen nieuwe rondes
$r = rmk_bol_bewaking();
$m = end( $GLOBALS['mails'] );
t( 'Nieuwe storing (cron ligt stil): weer één e-mail', 'gemeld' === $r['status'] && 2 === count( $GLOBALS['mails'] ) );
t( 'Cron ligt stil: geen oude fout van vóór de geslaagde ronde, wel "al voorbij" bij de volgende ronde', false !== strpos( $m['tekst'], 'Laatste fout: geen fout sinds de laatste geslaagde ronde' ) && false !== strpos( $m['tekst'], '(al voorbij: de cron lijkt niet te draaien)' ), $m['tekst'] );
t( 'Nieuwe storing: daarna niet opnieuw', 'al_gemeld' === rmk_bol_bewaking()['status'] && 2 === count( $GLOBALS['mails'] ) );

// Mail mislukt: niet als gemeld bewaren, later opnieuw proberen.
ronde( $GLOBALS['nu'], 'ok' );
rmk_bol_bewaking();
$GLOBALS['nu'] += 9 * $H;
ronde( $GLOBALS['nu'], '500' );
$GLOBALS['mail_faalt'] = true;
$r1 = rmk_bol_bewaking();
$GLOBALS['mail_faalt'] = false;
$r2 = rmk_bol_bewaking();
$m  = end( $GLOBALS['mails'] );
t( 'wp_mail mislukt: volgende controle probeert opnieuw', 'mail_mislukt' === $r1['status'] && 'gemeld' === $r2['status'] );
t( 'Fout bij een model in de e-mail', false !== strpos( $m['tekst'], 'M002: fout: HTTP 500' ), $m['tekst'] );

// Nooit geslaagd, alleen tokenfouten sinds 9 uur.
$GLOBALS['wp_options'] = array( 'admin_email' => 'beheer@example.test' );
$GLOBALS['mails']      = array();
ronde( $GLOBALS['nu'] - 9 * $H, 'token' );
ronde( $GLOBALS['nu'] - 3 * $H, 'token' );
$r = rmk_bol_bewaking();
t( 'Nog nooit geslaagd, eerste ronde 9 uur geleden: één e-mail', 'gemeld' === $r['status'] && 1 === count( $GLOBALS['mails'] ) && false !== strpos( $GLOBALS['mails'][0]['tekst'], 'Er is nog geen geslaagde Bol-ronde' ) );

// Shutdown-reserve: hooguit één keer per uur.
$GLOBALS['wp_options'] = array( 'admin_email' => 'beheer@example.test' );
$GLOBALS['mails']      = array();
ronde( $GLOBALS['nu'] - 10 * $H, 'ok' );
do_action( 'shutdown' );
do_action( 'shutdown' );
t( 'Shutdown-reserve meldt de storing één keer', 1 === count( $GLOBALS['mails'] ) );
t( 'Shutdown-reserve wacht een uur', (int) get_option( RMK_BOL_BEWAKING_VOLGENDE ) === $GLOBALS['nu'] + $H );

/* ---------------------------------------------------------------- specificatiekaart */
$basis = array( 'id' => 'M900', 'naam' => 'Husqvarna Testmaaier', 'merk' => 'Husqvarna', 'model' => 'Testmaaier',
	'specs' => array( 'max_tuingrootte_m2' => array( 'waarde' => 600 ), 'max_helling_pct' => array( 'waarde' => 40 ), 'navigatie' => array( 'waarde' => 'rtk' ), 'geluid_dba' => array( 'waarde' => 58 ) ) );
$chip = function ( $extra ) use ( $basis ) {
	$m = $basis;
	if ( null !== $extra ) {
		$m['verbinding'] = array( 'tekst' => 'x', 'extra' => $extra );
	}
	$h = rmk_speccard_html( $m );
	return preg_match( '#<div class="rmk-spec rmk-spec--verbinding[^"]*"><dt>Verbinding</dt><dd>(.*?)</dd></div>#', $h, $x ) ? $x[1] : null;
};
t( 'Chip Verbinding: wifi -> Wifi', 'Wifi' === $chip( 'wifi' ) );
t( 'Chip Verbinding: bluetooth -> Bluetooth', 'Bluetooth' === $chip( 'bluetooth' ) );
t( 'Chip Verbinding: ingebouwd -> 4G, module, geen (ongewijzigd)', '4G' === $chip( 'ingebouwd' ) && 'module' === $chip( 'module' ) && 'geen' === $chip( 'geen' ) );
t( 'Chip Verbinding: onbekende waarde of leeg -> geen chip (geen streepje)', null === $chip( 'satelliet' ) && null === $chip( null ) && null === $chip( '' ) );
$h = rmk_speccard_html( $basis );
t( 'Andere onbekende kenmerken houden hun streepje', 0 === substr_count( $h, 'is-missing' ) && 4 === substr_count( $h, 'class="rmk-spec ' ) );
t( 'Zonder foto: geen "Geen productfoto beschikbaar", geen beeldvlak, alleen de kenmerken', false === strpos( $h, 'Geen productfoto' ) && false === strpos( $h, 'rmk-speccard__visual' ) && false === strpos( $h, '<figure' ) && false !== strpos( $h, 'rmk-speccard rmk-speccard--specs' ) );
$mf         = $basis;
$mf['foto'] = array( 'url' => 'https://media.s-bol.com/abc/550x424.jpg', 'fabrikant' => 'bol.com', 'breedte' => 550, 'hoogte' => 424, 'bron' => 'bol' );
$hf         = rmk_speccard_html( $mf );
t( 'Met bol-foto: fotovariant, img met data-rmk-foto (voor rmk.js), "Foto: bol.com"', false !== strpos( $hf, 'rmk-speccard--photo' ) && false !== strpos( $hf, '<img data-rmk-foto src="https://media.s-bol.com/abc/550x424.jpg"' ) && false !== strpos( $hf, 'Foto: bol.com' ) );
$art = '<article class="rmk-product"><div class="rmk-product__head"><div class="rmk-speccard"><figure class="rmk-speccard__figure"><div class="rmk-speccard__visual" aria-hidden="true"><p class="rmk-speccard__brand">X</p><p class="rmk-speccard__model">Y</p></div><figcaption class="rmk-speccard__caption">Geen productfoto beschikbaar</figcaption></figure><dl class="rmk-speccard__specs"></dl></div><div class="rmk-product__title"><h3>Y</h3></div></div></article>';
$v1  = rmk_fill_card( $art, $basis );
t( 'Oude kaart in de pagina-inhoud wordt vervangen; tweede keer vullen geeft geen dubbele kaart', false === strpos( $v1, 'Geen productfoto' ) && 1 === substr_count( rmk_fill_card( $v1, $basis ), 'rmk-speccard__specs' ) );

echo $GLOBALS['fail'] ? "\n{$GLOBALS['fail']} FOUT\n" : "\nAlles geslaagd.\n";
exit( $GLOBALS['fail'] ? 1 : 0 );
