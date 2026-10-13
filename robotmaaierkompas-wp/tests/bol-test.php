<?php
/**
 * Test van de Bol-koppeling (thema 1.3.6, inc/bol.php) met NAGEBOOTSTE antwoorden, zonder netwerk en zonder sleutels.
 * De vorm van de antwoorden en de link volgt het Logboek van robotmaaierkompas_modeldata_v1.xlsx (rijen 137-145).
 * Draaien: php tests/bol-test.php        (geen WordPress nodig: tests/wp-stub.php)
 */
require __DIR__ . '/wp-stub.php';
$T = dirname( __DIR__ ) . '/wp-content/themes/robotmaaierkompas-child/robotmaaierkompas';
define( 'RMK_DIR', $T );
require $T . '/inc/data.php';
require $T . '/inc/score.php';
require $T . '/inc/bol.php';
require $T . '/inc/prijzen.php';
require $T . '/inc/redactie.php';

$GLOBALS['fail'] = 0;
function t( $n, $ok, $info = '' ) {
	echo ( $ok ? 'OK   ' : 'FOUT ' ) . $n . ( $info && ! $ok ? "\n       $info" : '' ) . "\n";
	$GLOBALS['fail'] += $ok ? 0 : 1;
}
$GLOBALS['nu'] = strtotime( '2026-10-13 10:00:00 Europe/Amsterdam' );
add_filter( 'rmk_bol_nu', function () { return $GLOBALS['nu']; } );

/* ---------------------------------------------------------------- nagebootste Bol-API (vorm uit het Logboek) */
$GLOBALS['api'] = array( 'verzoeken' => array(), 'tokens' => 0, 'aanbod' => array(), 'token_ongeldig' => array() );
function json_antw( $code, $data, $type = 'application/json' ) {
	return array( 'response' => array( 'code' => $code ), 'body' => json_encode( $data ),
		'headers' => array( 'content-type' => $type, 'x-ratelimit-limit' => '10', 'x-ratelimit-remaining' => '9', 'x-ratelimit-reset' => '1' ) );
}
function probleem( $code, $title, $detail ) { // application/problem+json (Logboek 138)
	return json_antw( $code, array( 'type' => 'https://api.bol.com/problems', 'title' => $title, 'status' => $code, 'detail' => $detail, 'host' => 'api.bol.com', 'X-Request-ID' => 'test-' . $code ), 'application/problem+json' );
}
add_filter( 'pre_http_request', function ( $pre, $args, $url ) {
	$GLOBALS['api']['verzoeken'][] = array( 't' => microtime( true ), 'url' => $url, 'args' => $args );
	if ( 0 === strpos( $url, 'https://login.bol.com/token' ) ) { // Logboek 137
		$GLOBALS['api']['tokens']++;
		return json_antw( 200, array( 'access_token' => 'tok-' . $GLOBALS['api']['tokens'], 'token_type' => 'Bearer', 'expires_in' => 599, 'scope' => 'affiliate' ) );
	}
	if ( ! preg_match( '#^https://api\.bol\.com/marketing/catalog/v1/products/(\d+)/offers/best\?country-code=NL&include-seller=true$#', $url, $m ) ) {
		return probleem( 400, 'Bad Request', 'Onbekend verzoek in de test: ' . $url );
	}
	$token = substr( $args['headers']['Authorization'], 7 );
	if ( in_array( $token, $GLOBALS['api']['token_ongeldig'], true ) ) {
		return probleem( 401, 'Unauthorized', 'Token expired' );
	}
	$a = $GLOBALS['api']['aanbod'][ $m[1] ] ?? 'geen';
	if ( 'geen' === $a ) {
		return probleem( 404, 'Not Found', 'Unable to find offer' ); // Logboek 141
	}
	if ( 'fout' === $a ) {
		return probleem( 500, 'Internal Server Error', 'Something went wrong' );
	}
	return json_antw( 200, array( 'ean' => $m[1], 'countryCode' => 'NL', 'condition' => 'NEW', 'isPreOrder' => false, 'price' => $a[0],
		'url' => 'https://www.bol.com/nl/nl/p/x/' . $m[1] . '/', 'ultimateOrderTime' => '23:59', 'minDeliveryDate' => '2026-10-14',
		'maxDeliveryDate' => '2026-10-15', 'deliveryDescription' => 'Morgen in huis', 'seller' => array( 'name' => $a[1] ) ) );
}, 10, 3 );
function aanbod( array $a ) { $GLOBALS['api']['aanbod'] = $a; $GLOBALS['api']['verzoeken'] = array(); }

$EAN = array( 'M002' => '8721264220318', 'M011' => '4066407025219', 'M004' => '6977973410621', 'M005' => '6977973410782' );
$m002 = rmk_get_model( 'M002' );
$m011 = rmk_get_model( 'M011' );
$m004 = rmk_get_model( 'M004' );
function kaart( $id ) { // productkaart zoals op de hub en pagina 1
	$m = rmk_get_model( $id );
	$a = 'p-' . $m['slug'];
	return '<article class="rmk-product" aria-labelledby="' . $a . '"><div class="rmk-product__head rmk-product__head--nomedia" style="grid-template-columns: 1fr"><div class="rmk-product__title"><h3 id="' . $a . '">' . $m['naam'] . '</h3>'
		. '<div class="rmk-scorecell" data-rmk-score data-model="' . $id . '"><div class="rmk-minis"><b data-out="total">–</b><small data-out="kind">Score</small></div><span class="rmk-provisional" data-out="label" hidden></span></div></div></div>'
		. '<div class="rmk-product__aside rmk-offers"><div class="rmk-offer"></div></div></article>';
}
$kaart_135 = rmk_fill_offers( kaart( 'M002' ) ); // referentie: zonder Bol, zoals 1.3.5

/* ---------------------------------------------------------------- A. zonder constanten: alles zoals 1.3.5 */
echo "\nA. Constanten ontbreken\n";
aanbod( array( $EAN['M002'] => array( 899, 'bol.com' ) ) );
do_action( 'init' );
t( 'Geen ingeplande taak', ! wp_next_scheduled( RMK_BOL_RONDE_HOOK ) );
$log = rmk_bol_ronde();
t( 'Ronde doet niets (geen verzoeken)', 0 === count( $GLOBALS['api']['verzoeken'] ) && false !== strpos( $log['melding'], 'ontbreken' ) );
t( 'Kaart gelijk aan 1.3.5 (geen Bol-regel, geen Bol-foto)', rmk_fill_offers( kaart( 'M002' ) ) === $kaart_135 && false === strpos( $kaart_135, 'bol' ) );

/* ---------------------------------------------------------------- B. constanten, RMK_AFFILIATE_ACTIVE uit */
echo "\nB. Constanten aanwezig (testwaarden), RMK_AFFILIATE_ACTIVE uit\n";
define( 'RMK_BOL_CLIENT_ID', 'test-id' );
define( 'RMK_BOL_CLIENT_SECRET', 'test-geheim' );
define( 'RMK_BOL_SITE_ID', '1549381' );
do_action( 'init' );
$c = wp_next_scheduled( RMK_BOL_RONDE_HOOK );
t( 'Taak ingepland, elke 6 uur (vier keer per dag)', $c && 'rmk_zes_uur' === $GLOBALS['wp_cron'][ RMK_BOL_RONDE_HOOK ][1] && 21600 === apply_filters( 'cron_schedules', array() )['rmk_zes_uur']['interval'] );
aanbod( array( $EAN['M002'] => array( 899, 'bol.com' ), $EAN['M011'] => array( 1049.95, 'JGStore.nl' ), $EAN['M004'] => 'geen', $EAN['M005'] => 'fout' ) );
$purge = $GLOBALS['wp_acties']['litespeed_purge_all'] ?? 0;
$log   = rmk_bol_ronde();
$v     = $GLOBALS['api']['verzoeken'];
t( 'Ronde draait wel (voor /bol-status): 1 token + 11 aanbiedingen', 12 === count( $v ) && 1 === $GLOBALS['api']['tokens'], count( $v ) . ' verzoeken' );
t( 'Paginacache geleegd na de ronde', ( $GLOBALS['wp_acties']['litespeed_purge_all'] ?? 0 ) === $purge + 1 );
t( 'Geen Bol-regel en geen Bol-foto (schakelaar uit)', rmk_fill_offers( kaart( 'M002' ) ) === $kaart_135 );
t( 'Geen advertentie-regel (schakelaar uit)', apply_filters( 'the_content', rmk_fill_offers( kaart( 'M002' ) ) ) === $kaart_135 );
// Vorm van de verzoeken (Logboek 137, 138, 141)
$tok = $v[0];
t( 'Token: POST login.bol.com met Basic base64(id:secret) en Accept: application/json', 'POST' === $tok['args']['method'] && 'https://login.bol.com/token?grant_type=client_credentials' === $tok['url']
	&& 'Basic ' . base64_encode( 'test-id:test-geheim' ) === $tok['args']['headers']['Authorization'] && 'application/json' === $tok['args']['headers']['Accept'] );
$of = $v[1];
t( 'Aanbod: GET /offers/best?country-code=NL&include-seller=true, Bearer, Accept-Language: nl', 'GET' === $of['args']['method'] && 'Bearer tok-1' === $of['args']['headers']['Authorization']
	&& 'nl' === $of['args']['headers']['Accept-Language'] && 'application/json' === $of['args']['headers']['Accept'] && false !== strpos( $of['url'], '/offers/best?country-code=NL&include-seller=true' ) );
t( 'Geen beoordelingen opgehaald (geen /ratings)', ! array_filter( $v, function ( $x ) { return false !== strpos( $x['url'], '/ratings' ); } ) );
$gaps = array();
for ( $i = 1; $i < count( $v ); $i++ ) { $gaps[] = $v[ $i ]['t'] - $v[ $i - 1 ]['t']; }
t( 'Maximaal 10 verzoeken per seconde (minstens 0,1 s ertussen)', min( $gaps ) >= 0.099, 'kleinste tussenpoos ' . round( min( $gaps ), 3 ) . ' s' );
$store = get_option( RMK_BOL_AANBOD_OPTION );
t( 'Uitkomsten: M002 ok (bol zelf), M011 ok (partner), M004 geen aanbod (404), M005 fout (500)',
	'ok' === $store['M002']['status'] && false === $store['M002']['partner'] && 'ok' === $store['M011']['status'] && true === $store['M011']['partner']
	&& 'geen_aanbod' === $store['M004']['status'] && 404 === $store['M004']['http'] && 'fout' === $store['M005']['status'], json_encode( array_map( function ( $x ) { return $x['status']; }, $store ) ) );
$alles = json_encode( get_option( RMK_BOL_AANBOD_OPTION ) ) . json_encode( get_option( RMK_BOL_LOG_OPTION ) ) . json_encode( rmk_bol_status() );
t( 'Geen secrets of tokens in opslag, log of /bol-status', false === strpos( $alles, 'test-geheim' ) && false === strpos( $alles, 'test-id' ) && false === strpos( $alles, 'tok-' ) && false === strpos( $alles, base64_encode( 'test-id:test-geheim' ) ) );
t( 'Log noemt de fout leesbaar (problem+json, X-Request-ID)', false !== strpos( $log['modellen']['M005'], 'Something went wrong' ) && false !== strpos( $log['modellen']['M005'], 'X-Request-ID test-500' ) );
do_action( 'rest_api_init' );
$r = $GLOBALS['wp_routes']['rmk/v1/bol-status'];
$GLOBALS['wp_admin'] = false;
$geen = ! call_user_func( $r['permission_callback'] );
$GLOBALS['wp_admin'] = true;
t( 'bol-status geweigerd voor niet-beheerders, toegestaan voor beheerders', $geen && call_user_func( $r['permission_callback'] ) && 'GET' === $r['methods'] );
$st = call_user_func( $r['callback'] );
t( 'bol-status: uitkomst per model, constanten alleen als ja/nee', true === $st['constanten_aanwezig'] && 'ok' === $st['modellen']['M002']['uitkomst'] && 'geen_aanbod' === $st['modellen']['M004']['uitkomst'] && ! $st['modellen']['M002']['op_de_site'] );

/* ---------------------------------------------------------------- C. RMK_AFFILIATE_ACTIVE aan */
echo "\nC. RMK_AFFILIATE_ACTIVE aan\n";
define( 'RMK_AFFILIATE_ACTIVE', true );
$k2 = rmk_fill_offers( kaart( 'M002' ) );
$verwacht = 'https://partner.bol.com/click/click?p=2&t=url&s=1549381&f=api&url=https%3A%2F%2Fwww.bol.com%2Fnl%2Fnl%2Fp%2Fnavimow-robotgrasmaaier-i206-600m2-nrtk-vision-awd%2F9300000251586857%2F&name=Segway%20Navimow%20i206%20AWD&subid=robotmaaier-zonder-draad';
t( 'Affiliatelink exact (Logboek 144: p,t,s,f,url,name; f=api; subid = paginaslug)', false !== strpos( $k2, 'href="' . esc_url( $verwacht ) . '"' ), $k2 );
t( 'Bol zelf: "899 euro. Prijs bij bol.com, bijgewerkt om 10:00." zonder partnertekst', false !== strpos( $k2, '<strong>899 euro</strong>. Prijs bij bol.com, bijgewerkt om 10:00.</span>' ) && false === strpos( $k2, 'via een partner' ) );
t( 'Knop "Bekijk bij bol.com" met rel="sponsored nofollow"', (bool) preg_match( '#<a class="rmk-btn rmk-btn--primary" href="[^"]+" rel="sponsored nofollow" data-rmk-bol-link>Bekijk bij bol.com</a>#', $k2 ) );
t( 'Eronder: "Je gaat naar bol.com. Bron: bol.com."', false !== strpos( $k2, '<span class="rmk-offer__src">Je gaat naar bol.com. Bron: bol.com.</span>' ) );
t( 'Geen Bol-beoordelingen', ! preg_match( '/beoordel|sterren|rating|4,2/i', $k2 ) );
t( 'Bestaand prijsblok blijft (Coolblue of "Bekijk de actuele prijs") en staat erboven', strpos( $k2, 'data-rmk-direct' ) < strpos( $k2, 'data-rmk-bol' ) );
t( 'Foto van bol.com: oorspronkelijke URL 550 px, met "Foto: bol.com"', false !== strpos( $k2, 'src="' . $m002['bol']['afbeelding']['url'] . '"' ) && false !== strpos( $k2, '550x424.jpg' )
	&& false !== strpos( $k2, 'width="550" height="424"' ) && false !== strpos( $k2, '>Foto: bol.com</figcaption>' ) && false !== strpos( $k2, 'rmk-speccard--photo' ) );
$k11 = rmk_fill_offers( kaart( 'M011' ) );
t( 'Partner: "1.049,95 euro. Prijs bij bol.com, bijgewerkt om 10:00, via een partner van bol.com."', false !== strpos( $k11, '<strong>1.049,95 euro</strong>. Prijs bij bol.com, bijgewerkt om 10:00, via een partner van bol.com.' ) );
$k4 = rmk_fill_offers( kaart( 'M004' ) );
t( 'Geen aanbod (404): geen Bol-regel, specificatiekaart zonder foto', false === strpos( $k4, 'data-rmk-bol' ) && false === strpos( $k4, 'speccard--photo' ) && false !== strpos( $k4, 'rmk-speccard' ) );
$k5 = rmk_fill_offers( kaart( 'M005' ) );
t( 'Foutmelding (500): geen Bol-regel', false === strpos( $k5, 'data-rmk-bol' ) );
$k10 = rmk_fill_offers( kaart( 'M010' ) );
t( 'Model zonder EAN (M010): geen Bol-regel', false === strpos( $k10, 'data-rmk-bol' ) );
$pagina = apply_filters( 'the_content', '<p>Intro</p>' . kaart( 'M004' ) . $k2 . $k11 );
t( 'Advertentie-regel één keer, direct boven de eerste kaart met een Bol-knop', 1 === substr_count( $pagina, 'rmk-affnote' ) && strpos( $pagina, 'rmk-affnote' ) > strpos( $pagina, 'p-mova-lidax-ultra-800' ) && strpos( $pagina, 'rmk-affnote' ) < strpos( $pagina, 'data-rmk-bol' ) );
$GLOBALS['wp_post']['slug'] = 'Beste_Robotmaaier!';
t( 'subid: alleen kleine letters, cijfers en koppeltekens', false !== strpos( rmk_fill_offers( kaart( 'M002' ) ), 'subid=besterobotmaaier"' ) );
$GLOBALS['wp_post']['slug'] = 'robotmaaier-zonder-draad';
t( 'Paginacache: TTL niet langer dan de geldigheid van de prijs', isset( $GLOBALS['wp_acties_args']['litespeed_control_set_ttl'] ) && end( $GLOBALS['wp_acties_args']['litespeed_control_set_ttl'] )[0] <= 12 * 3600 );

/* ---------------------------------------------------------------- D. verlopen prijs */
echo "\nD. Verlopen prijs (12 uur)\n";
$GLOBALS['nu'] += 11 * 3600 + 59 * 60;
t( 'Na 11 uur 59: Bol-regel staat er nog ("bijgewerkt om 10:00")', false !== strpos( rmk_fill_offers( kaart( 'M002' ) ), 'bijgewerkt om 10:00' ) );
$GLOBALS['nu'] += 61;
$k = rmk_fill_offers( kaart( 'M002' ) );
t( 'Na 12 uur en 1 seconde: Bol-regel en Bol-foto weg, kaart gelijk aan 1.3.5', false === strpos( $k, 'data-rmk-bol' ) && false === strpos( $k, 's-bol.com' ) && $k === $kaart_135 );

/* ---------------------------------------------------------------- E. token hergebruiken en verlopen token */
echo "\nE. Token\n";
$GLOBALS['nu']               = strtotime( '2026-10-13 16:00:00 Europe/Amsterdam' );
$GLOBALS['wp_trans']         = array();
$GLOBALS['api']['tokens']    = 0;
aanbod( array( $EAN['M002'] => array( 899, 'bol.com' ) ) );
rmk_bol_ronde();
$GLOBALS['nu'] += 300; // 5 minuten later: token (599 s) nog geldig
rmk_bol_ronde();
t( 'Token hergebruikt binnen de verlooptijd (2 rondes, 1 token)', 1 === $GLOBALS['api']['tokens'] );
$GLOBALS['nu'] += 270; // 570 s na uitgifte: binnen 30 s van afloop -> nieuw token
rmk_bol_ronde();
t( 'Nieuw token 30 s voor afloop (expires_in uit het antwoord)', 2 === $GLOBALS['api']['tokens'] );
$GLOBALS['api']['token_ongeldig'] = array( 'tok-2' ); // server weigert het nog "geldige" token (401)
aanbod( array( $EAN['M002'] => array( 909, 'bol.com' ), $EAN['M011'] => array( 1049.95, 'JGStore.nl' ) ) );
$log = rmk_bol_ronde();
$st  = get_option( RMK_BOL_AANBOD_OPTION );
t( 'Verlopen token (401): één keer vernieuwd, daarna gewoon verder', 3 === $GLOBALS['api']['tokens'] && 'ok' === $st['M002']['status'] && 909.0 === (float) $st['M002']['prijs'] && 'ok' === $st['M011']['status'], json_encode( $log ) );
t( 'Na vernieuwing gebruiken de volgende modellen het nieuwe token (geen tweede 401 per model)', 3 === $GLOBALS['api']['tokens'] );
$GLOBALS['api']['token_ongeldig'] = array();

/* ---------------------------------------------------------------- F. aanbod verdwijnt of wordt ongeldig */
echo "\nF. Aanbod verdwijnt\n";
aanbod( array() );
rmk_bol_ronde();
t( 'Volgende ronde zonder aanbod (404): Bol-regel meteen weg', false === strpos( rmk_fill_offers( kaart( 'M002' ) ), 'data-rmk-bol' ) );
aanbod( array( $EAN['M002'] => array( 0, 'bol.com' ) ) );
rmk_bol_ronde();
t( '200 zonder geldige prijs: status ongeldig, geen Bol-regel', 'ongeldig' === get_option( RMK_BOL_AANBOD_OPTION )['M002']['status'] && false === strpos( rmk_fill_offers( kaart( 'M002' ) ), 'data-rmk-bol' ) );

$GLOBALS['een_keer_429'] = true;
add_filter( 'pre_http_request', function ( $pre, $args, $url ) {
	if ( false !== strpos( $url, '/offers/best' ) && ! empty( $GLOBALS['een_keer_429'] ) ) {
		$GLOBALS['een_keer_429'] = false;
		$r = probleem( 429, 'Too Many Requests', 'Rate limit exceeded' );
		$r['headers']['x-ratelimit-remaining'] = '0';
		return $r;
	}
	return $pre;
}, 5, 3 );
aanbod( array( $EAN['M002'] => array( 899, 'bol.com' ) ) );
$t0 = microtime( true );
rmk_bol_ronde();
t( '429: wacht x-ratelimit-reset (1 s) en probeert één keer opnieuw', 'ok' === get_option( RMK_BOL_AANBOD_OPTION )['M002']['status'] && microtime( true ) - $t0 >= 1.0 );

/* ---------------------------------------------------------------- G. dataroute */
echo "\nG. Dataroute (validatie)\n";
$d = rmk_models_data();
t( 'Modelgegevens met ean en bol-blok worden geaccepteerd', array() === rmk_validate_modellen( $d ), implode( ' ', rmk_validate_modellen( $d ) ) );
$x = $d; $x['modellen'][1]['bol']['prijs'] = 899;
t( 'Bol-prijs in de gegevens geweigerd', (bool) rmk_validate_modellen( $x ) );
$x = $d; $x['modellen'][1]['bol']['beoordeling'] = 4.2;
t( 'Bol-beoordeling in de gegevens geweigerd', (bool) rmk_validate_modellen( $x ) );
$x = $d; $x['modellen'][1]['prijs']['url'] = 'https://www.bol.com/nl/p/x/1/';
t( 'bol.com buiten het blok "bol" geweigerd', (bool) rmk_validate_modellen( $x ) );
$x = $d; $x['modellen'][1]['bol']['afbeelding']['url'] = 'https://voorbeeld.nl/a.jpg';
t( 'Afbeelding buiten media.s-bol.com geweigerd', (bool) rmk_validate_modellen( $x ) );

echo "\n" . ( $GLOBALS['fail'] ? $GLOBALS['fail'] . ' FOUT(EN)' : 'Alles geslaagd' ) . "\n";
exit( $GLOBALS['fail'] ? 1 : 0 );
