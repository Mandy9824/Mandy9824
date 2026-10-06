<?php
/**
 * Test scoremodel server-side (PHP) tegen de verwachte waarden en tegen rmk.js.
 * Draaien: php tests/score-test.php   (Node moet geïnstalleerd zijn voor de vergelijking met rmk.js)
 */
define( 'ABSPATH', __DIR__ );
function apply_filters( $n, $v ) { return $v; }
function add_filter() {} function add_shortcode() {}
function esc_attr( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES ); }
function esc_html( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES ); }
function sanitize_html_class( $s ) { return preg_replace( '/[^A-Za-z0-9_-]/', '', $s ); }
function wp_list_pluck( $l, $f ) { return array_map( function ( $x ) use ( $f ) { return $x[ $f ]; }, $l ); }
define( 'RMK_DIR', dirname( __DIR__ ) . '/wp-content/themes/robotmaaierkompas-child/robotmaaierkompas' );
require RMK_DIR . '/inc/score.php';

$fail = 0;
function check( $name, $cond, $info = '' ) { global $fail; echo ( $cond ? 'OK   ' : 'FOUT ' ) . $name . ( $info ? "  ($info)" : '' ) . "\n"; if ( ! $cond ) { $fail++; } }

// 1. M002: waarden uit BLAUWDRUK hoofdstuk 24/28 (functiescore zonder betrouwbaarheid en prijs-kwaliteit)
$m002 = array( 'betrouwbaarheid' => null, 'navigatie' => 10, 'prijskwaliteit' => null, 'hellingen' => 8, 'app' => 10, 'veiligheid' => 10, 'geluid' => 6 );
$r = rmk_compute_score( $m002, null );
check( 'M002 soort = functiescore', 'functie' === $r['kind'], $r['kind'] );
check( 'M002 weergave 92,7', '92,7' === rmk_format_score( $r['value'] ), rmk_format_score( $r['value'] ) . ' / onafgerond ' . $r['value'] );
check( 'M002 label', 'Betrouwbaarheid en prijs-kwaliteit worden toegevoegd zodra er genoeg reviews en prijzen zijn.' === $r['label'], $r['label'] );

// 2. Model met zeven onderdelen (testwaarden, geen echt model)
$vol = array( 'betrouwbaarheid' => 8, 'navigatie' => 8, 'prijskwaliteit' => 7.3, 'hellingen' => 6, 'app' => 9, 'veiligheid' => 7.5, 'geluid' => 4 );
$r = rmk_compute_score( $vol, 120 );
$expect = ( 25 * 8 + 20 * 8 + 20 * 7.3 + 10 * 6 + 10 * 9 + 10 * 7.5 + 5 * 4 ) / 10; // 75,1
check( 'Volledig model = eindscore', 'eind' === $r['kind'] );
check( 'Volledig model waarde', abs( $r['value'] - $expect ) < 1e-9 && '75,1' === rmk_format_score( $r['value'] ), rmk_format_score( $r['value'] ) );
check( 'Volledig model geen label', '' === $r['label'] );

// 3. Minder dan 50 gelezen reviews: betrouwbaarheid telt niet -> functiescore
$r = rmk_compute_score( $vol, 49 );
check( '49 reviews -> functiescore', 'functie' === $r['kind'] && 'Betrouwbaarheid en prijs-kwaliteit worden toegevoegd zodra er genoeg reviews en prijzen zijn.' === $r['label'], $r['label'] );
$r = rmk_compute_score( $vol, 50 );
check( '50 reviews -> eindscore', 'eind' === $r['kind'] );

// 4. Vier onderdelen -> geen score
$r = rmk_compute_score( array( 'navigatie' => 10, 'hellingen' => 8, 'veiligheid' => 10, 'geluid' => 6 ), null );
check( '4 onderdelen -> geen score', 'geen' === $r['kind'] && null === $r['value'] && '–' === rmk_format_score( $r['value'] ) );

// 5. Placeholders tellen als onbekend
$r = rmk_compute_score( array( 'navigatie' => '[0–10]', 'hellingen' => '8', 'app' => '10', 'veiligheid' => '10', 'geluid' => '6', 'prijskwaliteit' => '7,5' ), null );
check( 'Placeholder [0–10] = onbekend', 5 === $r['known'] );

// 6. Rangschikking op onafgeronde waarde
$items = rmk_rank( array(
	array( 'id' => 'A', 'score' => array( 'value' => 80.54 ) ),
	array( 'id' => 'B', 'score' => array( 'value' => 80.46 ) ),
	array( 'id' => 'C', 'score' => array( 'value' => null ) ),
	array( 'id' => 'D', 'score' => array( 'value' => 80.5 ) ),
) );
check( 'Rangschikking onafgerond (A, D, B, C)', 'ADBC' === implode( '', array_column( $items, 'id' ) ), implode( '', array_column( $items, 'id' ) ) . ' — A en B tonen allebei 80,5' );

// 7. HTML bevat de score (server-side), zonder JavaScript
$html = rmk_render_scoreblok( $m002, null, 'm002' );
check( 'HTML scoreblok bevat 92,7', false !== strpos( $html, '<b data-out="total">92,7</b>' ) && false !== strpos( $html, 'Functiescore' ) );
$pat  = file_get_contents( RMK_DIR . '/patterns/scoreblok.php' );
$pat  = str_replace( array( 'data-key="navigatie" data-value="[0–10]"', 'data-key="hellingen" data-value="[0–10]"', 'data-key="app" data-value="[0–10]"', 'data-key="veiligheid" data-value="[0–10]"', 'data-key="geluid" data-value="[0–10]"' ),
	array( 'data-key="navigatie" data-value="10"', 'data-key="hellingen" data-value="8"', 'data-key="app" data-value="10"', 'data-key="veiligheid" data-value="10"', 'data-key="geluid" data-value="6"' ), $pat );
check( 'Patroon scoreblok server-side ingevuld', false !== strpos( rmk_ssr_scores( $pat ), '<b data-out="total">92,7</b>' ) );
$cell = '<div class="rmk-scorecell" data-rmk-score data-scores="betrouwbaarheid=; navigatie=10; prijskwaliteit=; hellingen=8; app=10; veiligheid=10; geluid=6; reviews="><div class="rmk-minis"><b data-out="total">–</b><small data-out="kind">Score</small></div><span class="rmk-provisional" data-out="label" hidden></span></div>';
check( 'Patroon scorecel server-side ingevuld', false !== strpos( rmk_ssr_scores( $cell ), '>92,7</b>' ) );

// 8. Vergelijking met rmk.js (zelfde invoer, 2000 willekeurige gevallen)
$cases = array();
mt_srand( 42 );
for ( $i = 0; $i < 2000; $i++ ) {
	$v = array();
	foreach ( rmk_score_model() as $p ) { $v[ $p['key'] ] = mt_rand( 0, 4 ) ? round( mt_rand( 0, 1000 ) / 100, 2 ) : null; }
	$cases[] = array( 'v' => $v, 'reviews' => mt_rand( 0, 1 ) ? mt_rand( 0, 150 ) : null );
}
$cases[] = array( 'v' => $m002, 'reviews' => null );
file_put_contents( sys_get_temp_dir() . '/rmk-cases.json', json_encode( $cases ) );
$js = shell_exec( 'node ' . escapeshellarg( __DIR__ . '/score-js.js' ) . ' ' . escapeshellarg( sys_get_temp_dir() . '/rmk-cases.json' ) . ' 2>&1' );
$js = json_decode( (string) $js, true );
if ( ! is_array( $js ) ) {
	check( 'rmk.js draait in Node', false, 'geen uitvoer' );
} else {
	$diff = 0;
	foreach ( $cases as $i => $c ) {
		$p = rmk_compute_score( $c['v'], $c['reviews'] );
		$j = $js[ $i ];
		if ( $p['kind'] !== $j['kind'] || $p['label'] !== $j['label'] || rmk_format_score( $p['value'] ) !== $j['shown'] || ( null !== $p['value'] && abs( $p['value'] - $j['value'] ) > 1e-9 ) ) {
			$diff++;
			if ( $diff < 4 ) { echo '  verschil: ' . json_encode( array( $c, $p['kind'], rmk_format_score( $p['value'] ), $j ) ) . "\n"; }
		}
	}
	check( 'PHP gelijk aan rmk.js in ' . count( $cases ) . ' gevallen', 0 === $diff, $diff . ' verschillen' );
}
// 9. Echt modelbestand (data/modellen.json uit het Excel-bestand)
$data = json_decode( file_get_contents( RMK_DIR . '/data/modellen.json' ), true );
$byid = array();
foreach ( $data['modellen'] as $m ) { $byid[ $m['id'] ] = $m; }
$r = isset( $byid['M002'] ) ? rmk_compute_score( $byid['M002']['scores'], $byid['M002']['reviews_gelezen'] ) : null;
check( 'modellen.json: M002 functiescore 92,7', $r && 'functie' === $r['kind'] && '92,7' === rmk_format_score( $r['value'] ), $r ? rmk_format_score( $r['value'] ) . ' ' . $r['kind'] : 'M002 ontbreekt' );
check( 'modellen.json: M009 (uitverkocht) staat er niet in', ! isset( $byid['M009'] ) );
check( 'modellen.json: geen niet-leverbare modellen', ! array_filter( $data['modellen'], function ( $m ) { return in_array( $m['beschikbaarheid'], array( 'uitverkocht', 'niet leverbaar' ), true ); } ) );
check( 'modellen.json: geen prijslijsten, geen aanschaf en geen bol.com', false === stripos( json_encode( $data ), 'bol.com' ) && ! array_filter( $data['modellen'], function ( $m ) { return isset( $m['prijzen'] ) || null !== $m['kosten']['aanschaf']['waarde']; } ) );
check( 'modellen.json: prijzen alleen van winkel of fabrikant, hele euro\'s', ! array_filter( $data['modellen'], function ( $m ) { return ! empty( $m['prijs'] ) && ( ! in_array( $m['prijs']['type'], array( 'winkel', 'fabrikant' ), true ) || ! is_int( $m['prijs']['bedrag'] ) ); } ) );
$rows = array();
foreach ( $byid as $id => $m ) { $rows[] = array( 'id' => $id, 'score' => rmk_model_score( $m ) ); }
echo '  ranglijst: ' . implode( ', ', array_map( function ( $x ) { return $x['id'] . ' ' . rmk_format_score( $x['score']['value'] ); }, rmk_rank( $rows ) ) ) . "\n";

echo $fail ? "\n$fail test(s) mislukt\n" : "\nAlle tests geslaagd\n";
exit( $fail ? 1 : 0 );
