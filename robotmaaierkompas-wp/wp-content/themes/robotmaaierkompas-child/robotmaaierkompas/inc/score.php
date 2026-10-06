<?php
/**
 * robotmaaierkompas.nl — scoremodel v1.0 server-side (zelfde regels als rmk.js)
 *
 * - Zeven onderdelen, elk 0 tot 10, gewichten 25/20/20/10/10/10/5.
 * - Betrouwbaarheid telt alleen bij minstens 50 gelezen reviews.
 * - 7 van 7 bekend: Eindscore. 5 of 6: Functiescore met het label "Betrouwbaarheid en prijs-kwaliteit worden toegevoegd zodra er genoeg reviews en prijzen zijn.". Minder: geen score.
 * - Weergave met één decimaal (92,7); rangschikken altijd op de onafgeronde waarde.
 *
 * Werkt in drie situaties:
 * 1. Patronen scoreblok / scoretabel met ingevulde data-value / data-scores: de score wordt
 *    bij het renderen in de HTML gezet (filter render_block).
 * 2. Shortcode [rmk_scoreblok model="M002"]: scoreblok uit data/modellen.json.
 * 3. Shortcode [rmk_scoretabel modellen="M001,M002,…"]: tabel uit modellen.json, gerangschikt.
 */

defined( 'ABSPATH' ) || exit;

function rmk_score_model() {
	return apply_filters( 'rmk_score_model', array(
		array( 'key' => 'betrouwbaarheid', 'label' => 'Betrouwbaarheid uit reviews', 'w' => 25 ),
		array( 'key' => 'navigatie',       'label' => 'Navigatie en dekking',        'w' => 20 ),
		array( 'key' => 'prijskwaliteit',  'label' => 'Prijs-kwaliteit',             'w' => 20 ),
		array( 'key' => 'hellingen',       'label' => 'Hellingen en terrein',        'w' => 10 ),
		array( 'key' => 'app',             'label' => 'App en bediening',            'w' => 10 ),
		array( 'key' => 'veiligheid',      'label' => 'Veiligheid',                  'w' => 10 ),
		array( 'key' => 'geluid',          'label' => 'Geluid',                      'w' => 5 ),
	) );
}

function rmk_min_reviews() {
	return (int) apply_filters( 'rmk_min_reviews', 50 );
}

/** Getal uit tekst, zoals parse() in rmk.js: placeholders "[…]" en lege waarden geven null. */
function rmk_parse_number( $v ) {
	if ( null === $v || is_bool( $v ) ) {
		return null;
	}
	if ( is_int( $v ) || is_float( $v ) ) {
		return is_finite( (float) $v ) ? (float) $v : null;
	}
	$t = trim( (string) $v );
	if ( '' === $t || preg_match( '/[\[\]]/', $t ) ) {
		return null;
	}
	$t = preg_replace( '/\s/u', '', $t );
	$t = preg_replace( '/\.(?=\d{3}(\D|$))/', '', $t ); // duizendtalpunt
	$t = str_replace( ',', '.', $t );
	if ( ! preg_match( '/^-?\d+(\.\d+)?/', $t, $m ) ) {
		return null;
	}
	return (float) $m[0];
}

/**
 * @param array      $values  [key => 0..10 of null]
 * @param float|null $reviews aantal gelezen reviews
 * @return array{kind:string,value:?float,known:int,total:int,missing:array,label:string}
 *         value is ONAFGEROND; gebruik rmk_format_score() voor weergave.
 */
function rmk_compute_score( array $values, $reviews ) {
	$model   = rmk_score_model();
	$known   = array();
	$missing = array();
	$sum_w   = 0;
	$sum_wv  = 0.0;
	foreach ( $model as $p ) {
		$v = isset( $values[ $p['key'] ] ) ? rmk_parse_number( $values[ $p['key'] ] ) : null;
		if ( 'betrouwbaarheid' === $p['key'] && ( null === $reviews || $reviews < rmk_min_reviews() ) ) {
			$v = null;
		}
		if ( null !== $v && $v >= 0 && $v <= 10 ) {
			$known[] = $p;
			$sum_w  += $p['w'];
			$sum_wv += $p['w'] * $v;
		} else {
			$missing[] = $p;
		}
	}
	$res = array( 'known' => count( $known ), 'total' => count( $model ), 'missing' => $missing, 'value' => null, 'kind' => 'geen', 'label' => '' );
	if ( count( $known ) === count( $model ) ) {
		$res['kind']  = 'eind';
		$res['value'] = $sum_wv / 10;
	} elseif ( count( $known ) >= 5 ) {
		$res['kind']  = 'functie';
		$res['value'] = $sum_wv / $sum_w * 10;
		// Label (1.3.2): "Functiescore: wat deze maaier kan." met daarachter de link "Hoe we scoren" (rmk_score_label_html).
		// In de balkjes blijft "onvoldoende data".
		$res['label'] = 'Functiescore: wat deze maaier kan.';
	}
	return $res;
}

/** Label onder de score, zonder kader: tekst plus de link "Hoe we scoren". */
function rmk_score_label_html( $label ) {
	return $label ? esc_html( $label ) . ' <a href="/hoe-we-beoordelen/">Hoe we scoren</a>' : '';
}

function rmk_join_names( array $a ) {
	if ( count( $a ) < 2 ) {
		return implode( '', $a );
	}
	return implode( ', ', array_slice( $a, 0, -1 ) ) . ' en ' . end( $a );
}

/** Eén decimaal, Nederlandse notatie. Afronden zoals rmk.js: Math.round(x * 10) / 10. */
function rmk_round1( $value ) {
	return floor( $value * 10 + 0.5 ) / 10;
}

function rmk_format_number( $value, $decimals = 1 ) {
	$r = $decimals ? rmk_round1( $value ) : round( $value );
	$s = number_format( $r, $decimals, ',', '.' );
	return $decimals ? preg_replace( '/,0$/', '', $s ) : $s; // 10,0 -> 10 (zoals toLocaleString)
}

function rmk_format_score( $value ) {
	return null === $value ? '–' : number_format( rmk_round1( $value ), 1, ',', '.' );
}

function rmk_score_kind_label( $kind ) {
	$k = array( 'eind' => 'Eindscore', 'functie' => 'Functiescore', 'geen' => 'Geen score' );
	return $k[ $kind ];
}

/** Sorteert modellen op onafgeronde score (hoog naar laag); zonder score achteraan. */
function rmk_rank( array $items, $score_key = 'score' ) {
	usort( $items, function ( $a, $b ) use ( $score_key ) {
		$va = isset( $a[ $score_key ]['value'] ) ? $a[ $score_key ]['value'] : -1;
		$vb = isset( $b[ $score_key ]['value'] ) ? $b[ $score_key ]['value'] : -1;
		return $vb <=> $va;
	} );
	return $items;
}

/* ------------------------------------------------------------------ modelbestand */

function rmk_models_data() {
	static $data = null;
	if ( null === $data ) {
		$file = apply_filters( 'rmk_models_file', RMK_DIR . '/data/modellen.json' );
		$json = is_readable( $file ) ? json_decode( (string) file_get_contents( $file ), true ) : null;
		$data = is_array( $json ) ? $json : array( 'modellen' => array() );
	}
	return $data;
}

/** Zoek op ID (M002) of slug. */
function rmk_get_model( $id ) {
	foreach ( rmk_models_data()['modellen'] as $m ) {
		if ( strcasecmp( $m['id'], $id ) === 0 || $m['slug'] === $id ) {
			return $m;
		}
	}
	return null;
}

function rmk_model_score( array $m ) {
	return rmk_compute_score( isset( $m['scores'] ) ? $m['scores'] : array(), isset( $m['reviews_gelezen'] ) ? $m['reviews_gelezen'] : null );
}

/* ------------------------------------------------------------------ HTML */

function rmk_score_notes( array $r ) {
	if ( 'eind' === $r['kind'] ) {
		return '';
	}
	if ( 'functie' === $r['kind'] ) {
		return 'Berekend over ' . $r['known'] . ' van ' . $r['total'] . ' onderdelen.';
	}
	return 'Te weinig gegevens: ' . $r['known'] . ' van ' . $r['total'] . ' onderdelen bekend, minimaal 5 nodig.';
}

/** Volledig scoreblok, dezelfde markup als patterns/scoreblok.php maar met ingevulde waarden. */
function rmk_render_scoreblok( array $values, $reviews, $id_suffix, $updated = '' ) {
	$r     = rmk_compute_score( $values, $reviews );
	$total = rmk_format_score( $r['value'] );
	$kind  = rmk_score_kind_label( $r['kind'] );
	$cls   = 'rmk-score' . ( 'functie' === $r['kind'] ? ' rmk-score--provisional' : '' ) . ( 'geen' === $r['kind'] ? ' rmk-score--none' : '' );
	$aria  = null === $r['value'] ? 'Geen score' : $kind . ' ' . $total . ' van 100';
	$width = null === $r['value'] ? 0 : rmk_round1( $r['value'] );
	$miss  = wp_list_pluck( $r['missing'], 'key' );
	$id    = 'score-' . sanitize_html_class( $id_suffix );

	$h  = '<section class="' . esc_attr( $cls ) . '" data-rmk-score data-ssr="1" data-total="' . esc_attr( null === $r['value'] ? '' : $r['value'] ) . '" aria-labelledby="' . esc_attr( $id ) . '">';
	$h .= '<div class="rmk-score__head"><div class="rmk-score__total"><b data-out="total">' . esc_html( $total ) . '</b><span>/ 100</span></div>';
	$h .= '<div class="rmk-score__kind"><strong id="' . esc_attr( $id ) . '" data-out="kind">' . esc_html( $kind ) . '</strong></div></div><p class="rmk-scorenote" data-out="label"' . ( $r['label'] ? '' : ' hidden' ) . '>' . rmk_score_label_html( $r['label'] ) . '</p>';
	$h .= '<div class="rmk-scale" role="img" data-out="bar" aria-label="' . esc_attr( $aria ) . '"><i style="width:' . esc_attr( $width ) . '%"></i></div><ul class="rmk-parts">';
	foreach ( rmk_score_model() as $p ) {
		$v       = isset( $values[ $p['key'] ] ) ? rmk_parse_number( $values[ $p['key'] ] ) : null;
		$empty   = in_array( $p['key'], $miss, true );
		$val_txt = $empty ? 'onvoldoende data' : rmk_format_number( $v ) . ' / 10';
		if ( $empty ) {
			$bar_aria = ( 'betrouwbaarheid' === $p['key'] && null !== $v ) ? 'Onvoldoende data: minder dan ' . rmk_min_reviews() . ' gelezen reviews' : 'Onvoldoende data';
		} else {
			$bar_aria = rmk_format_number( $v ) . ' van 10';
		}
		$extra = 'betrouwbaarheid' === $p['key'] ? ' data-reviews="' . esc_attr( null === $reviews ? '' : $reviews ) . '"' : '';
		$h    .= '<li class="rmk-part' . ( $empty ? ' rmk-part--empty' : '' ) . '" data-key="' . esc_attr( $p['key'] ) . '" data-value="' . esc_attr( null === $v ? '' : $v ) . '"' . $extra . '>';
		$h    .= '<span class="rmk-part__label">' . esc_html( $p['label'] ) . ' <small>' . (int) $p['w'] . '%</small></span><span class="rmk-part__val">' . esc_html( $val_txt ) . '</span>';
		$h    .= '<div class="rmk-bar" role="img" aria-label="' . esc_attr( $bar_aria ) . '"><i style="width:' . esc_attr( $empty ? 0 : $v * 10 ) . '%"></i></div></li>';
	}
	$h .= '</ul><p class="rmk-small" data-out="note">' . esc_html( rmk_score_notes( $r ) ) . '</p>';
	$h .= '<div class="rmk-score__foot"><span>' . ( $updated ? 'Bijgewerkt op ' . esc_html( $updated ) : '' ) . '</span><span>Scoremodel v1.0 (concept tot bevriezing)</span><a href="/hoe-we-beoordelen/#scoremodel">Hoe we scoren</a></div></section>';
	return $h;
}

/** Compacte scorecel (scoretabel, vergelijkingstabel). */
function rmk_render_scorecell( array $values, $reviews, $with_label = true ) {
	$r     = rmk_compute_score( $values, $reviews );
	$pairs = array();
	foreach ( rmk_score_model() as $p ) {
		$v       = isset( $values[ $p['key'] ] ) ? rmk_parse_number( $values[ $p['key'] ] ) : null;
		$pairs[] = $p['key'] . '=' . ( null === $v ? '' : $v );
	}
	$pairs[] = 'reviews=' . ( null === $reviews ? '' : $reviews );
	$minis   = 'rmk-minis' . ( 'functie' === $r['kind'] ? ' rmk-minis--provisional' : '' ) . ( 'geen' === $r['kind'] ? ' rmk-minis--none' : '' );
	$kind    = rmk_score_kind_label( $r['kind'] ) . ( null === $r['value'] ? '' : ', van 100' );
	return '<div class="rmk-scorecell" data-rmk-score data-ssr="1" data-kind="' . esc_attr( $r['kind'] ) . '" data-total="' . esc_attr( null === $r['value'] ? '' : $r['value'] ) . '" data-scores="' . esc_attr( implode( '; ', $pairs ) ) . '">'
		. '<div class="' . esc_attr( $minis ) . '"><b data-out="total">' . esc_html( rmk_format_score( $r['value'] ) ) . '</b><small data-out="kind">' . esc_html( $kind ) . '</small></div>'
		. ( $with_label ? '<p class="rmk-scorenote" data-out="label"' . ( $r['label'] ? '' : ' hidden' ) . '>' . rmk_score_label_html( $r['label'] ) . '</p>' : '' ) . '</div>';
}

/* ------------------------------------------------------------------ shortcodes */

add_shortcode( 'rmk_scoreblok', function ( $atts ) {
	$a = shortcode_atts( array( 'model' => '' ), $atts );
	$m = rmk_get_model( $a['model'] );
	if ( ! $m ) {
		return current_user_can( 'edit_posts' ) ? '<p class="rmk-small">Model "' . esc_html( $a['model'] ) . '" staat niet in modellen.json.</p>' : '';
	}
	$data = rmk_models_data();
	return rmk_render_scoreblok( $m['scores'], $m['reviews_gelezen'], $m['slug'], isset( $data['gegenereerd'] ) ? mysql2date( 'j F Y', $data['gegenereerd'] ) : '' );
} );

add_shortcode( 'rmk_scoretabel', function ( $atts ) {
	$a     = shortcode_atts( array( 'modellen' => '' ), $atts );
	$ids   = array_filter( array_map( 'trim', explode( ',', $a['modellen'] ) ) );
	$items = array();
	foreach ( $ids as $id ) {
		$m = rmk_get_model( $id );
		if ( $m ) {
			$items[] = array( 'm' => $m, 'score' => rmk_model_score( $m ) );
		}
	}
	$items     = rmk_rank( $items );
	$show_best = (bool) array_filter( $items, function ( $it ) { return ! empty( $it['m']['beste_voor'] ); } );
	$rows      = '';
	$n     = 0;
	foreach ( $items as $it ) {
		$m     = $it['m'];
		$rank  = null === $it['score']['value'] ? '–' : (string) ( ++$n );
		$price = function_exists( 'rmk_price_cell' ) ? rmk_price_cell( $m ) : '–';
		$best  = $show_best ? '<td class="c-best">' . esc_html( isset( $m['beste_voor'] ) ? $m['beste_voor'] : '' ) . '</td>' : '';
		$rows .= '<tr data-model="' . esc_attr( $m['slug'] ) . '"><td class="c-rank"><span class="rmk-ranknum">' . esc_html( $rank ) . '</span></td>'
			. '<th scope="row" class="c-model">' . esc_html( $m['naam'] ) . '</th>' . $best
			. '<td class="is-num c-score">' . rmk_render_scorecell( $m['scores'], $m['reviews_gelezen'], false ) . '</td>'
			. '<td class="is-num c-price" data-label="Laagste nieuwe prijs">' . $price . '</td>'
			. '<td class="c-go"><a href="#p-' . esc_attr( $m['slug'] ) . '">Details</a></td></tr>';
	}
	return '<div class="rmk-tablewrap"><table class="rmk-table rmk-table--cards"><caption>Scores volgens scoremodel v1.0 (concept tot bevriezing). Volgorde op de onafgeronde score. Modellen zonder score staan onderaan.</caption>'
		. '<thead><tr><th scope="col">#</th><th scope="col">Model</th>' . ( $show_best ? '<th scope="col">Beste voor</th>' : '' ) . '<th scope="col" class="is-num">Score</th><th scope="col" class="is-num">Laagste nieuwe prijs</th><th scope="col"><span class="rmk-sr">Details</span></th></tr></thead>'
		. '<tbody>' . $rows . '</tbody></table></div>'
		. ( function_exists( 'rmk_price_date_line' ) ? rmk_price_date_line( wp_list_pluck( $items, 'm' ) ) : '' )
		// Eén regel onder de tabel in plaats van een label per rij.
		. ( array_filter( $items, function ( $it ) { return 'functie' === $it['score']['kind']; } ) ? '<p class="rmk-scorenote">' . rmk_score_label_html( 'Functiescore: wat deze maaier kan.' ) . '</p>' : '' );
} );

/* ------------------------------------------------------------------ patronen met handmatig ingevulde waarden */

/**
 * Zet de score server-side in een scoreblok of scorecel uit de patronen.
 * Placeholders ([0–10]) gelden als onbekend, net als in rmk.js.
 */
function rmk_ssr_scores( $html ) {
	if ( false === strpos( (string) $html, 'data-rmk-score' ) || false !== strpos( $html, 'data-ssr="1"' ) ) {
		return $html;
	}
	// Volledige scoreblokken
	$html = preg_replace_callback( '#<section\b[^>]*\bdata-rmk-score\b[^>]*>.*?</section>#s', function ( $mm ) {
		$sec = $mm[0];
		if ( ! preg_match_all( '#<li\b[^>]*\bdata-key="([a-z]+)"[^>]*>#', $sec, $lis, PREG_SET_ORDER ) ) {
			return $sec;
		}
		$values  = array();
		$reviews = null;
		foreach ( $lis as $li ) {
			$values[ $li[1] ] = preg_match( '#data-value="([^"]*)"#', $li[0], $v ) ? rmk_parse_number( html_entity_decode( $v[1] ) ) : null;
			if ( 'betrouwbaarheid' === $li[1] && preg_match( '#data-reviews="([^"]*)"#', $li[0], $rv ) ) {
				$reviews = rmk_parse_number( html_entity_decode( $rv[1] ) );
			}
		}
		$suffix  = preg_match( '#aria-labelledby="score-([^"]*)"#', $sec, $s ) ? $s[1] : 'model';
		$updated = preg_match( '#Bijgewerkt op ([^<]*)</span>#', $sec, $u ) ? trim( $u[1] ) : '';
		return rmk_render_scoreblok( $values, $reviews, $suffix, $updated );
	}, $html );
	// Compacte scorecellen
	// Scorecel met data-model="M002": waarden rechtstreeks uit modellen.json
	$html = preg_replace_callback( '#<div class="rmk-scorecell" data-rmk-score (?:data-scores="[^"]*" )?data-model="([A-Za-z0-9-]+)"[^>]*>.*?</span></div>#s', function ( $mm ) {
		$m = rmk_get_model( $mm[1] );
		return $m ? rmk_render_scorecell( $m['scores'], $m['reviews_gelezen'] ) : $mm[0];
	}, $html );
	$html = preg_replace_callback( '#<div class="rmk-scorecell" data-rmk-score data-scores="([^"]*)">.*?</span></div>#s', function ( $mm ) {
		$values  = array();
		$reviews = null;
		foreach ( explode( ';', html_entity_decode( $mm[1] ) ) as $pair ) {
			$kv = explode( '=', $pair, 2 );
			if ( count( $kv ) < 2 ) {
				continue;
			}
			$k = trim( $kv[0] );
			$v = rmk_parse_number( $kv[1] );
			if ( 'reviews' === $k ) {
				$reviews = $v;
			} else {
				$values[ $k ] = $v;
			}
		}
		return rmk_render_scorecell( $values, $reviews );
	}, $html );
	return $html;
}
add_filter( 'render_block', function ( $content, $block ) {
	return 'core/html' === $block['blockName'] ? rmk_ssr_scores( $content ) : $content;
}, 15, 2 );
