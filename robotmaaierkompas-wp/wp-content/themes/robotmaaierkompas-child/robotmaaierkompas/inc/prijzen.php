<?php
/**
 * robotmaaierkompas.nl — prijs en knop in de productbox (besluit 6 oktober 2026)
 *
 * Bron: per model het veld "prijs" in modellen.json ({bedrag, winkel, datum, url, type}), gemaakt door
 * scripts/excel_naar_json.py uit het blad Prijzen. Een prijs wordt alleen getoond als hij geldig is:
 * - nieuw exemplaar en op voorraad (het script neemt alleen zulke regels over);
 * - van een winkel of de fabrikant (type "winkel" of "fabrikant"), geen marketplace, geen Bol;
 * - gezien op een datum van hoogstens 14 dagen geleden (RMK_PRIJS_MAX_DAGEN). Daarna verdwijnt hij vanzelf.
 * Tekst: "Laagste nieuwe prijs rond 899 euro bij Coolblue, gezien op 5 oktober 2026", met daaronder de knop
 * "Bekijk bij Coolblue": een gewone externe link naar de productpagina, zonder affiliatelink.
 * Geen geldige prijs: alleen de knop "Bekijk de actuele prijs" naar de fabrikantpagina (veld fabrikant_url).
 * Geen van beide: geen prijsblok.
 *
 * De productboxen in de pagina's hebben een scorecel met data-model="M002"; het prijsblok in die box wordt
 * bij het weergeven vervangen. Elke nacht leegt een taak de LiteSpeed-cache als er een prijs verlopen is.
 */

defined( 'ABSPATH' ) || exit;

const RMK_PRIJS_MAX_DAGEN = 14;

/** Domeinen waarvan we nooit een prijs of knop tonen: Bol en marketplaces. */
function rmk_price_blocked_hosts() {
	return apply_filters( 'rmk_price_blocked_hosts', array( 'bol.com', 's-bol.com', 'bol-cdn.com', 'amazon.nl', 'media-amazon.com', 'amazon.de', 'amazon.com', 'amzn.to', 'ebay.nl', 'ebay.de', 'marktplaats.nl', 'aliexpress.com', 'temu.com', 'awin1.com', 'zenaps.com', 'ds1.nl' ) );
}

function rmk_price_url_ok( $url ) {
	$parts = wp_parse_url( (string) $url );
	if ( empty( $parts['scheme'] ) || 'https' !== strtolower( $parts['scheme'] ) || empty( $parts['host'] ) ) {
		return false;
	}
	$host = strtolower( preg_replace( '/^www\./i', '', $parts['host'] ) );
	foreach ( rmk_price_blocked_hosts() as $d ) {
		if ( $host === $d || substr( $host, -strlen( '.' . $d ) ) === '.' . $d ) {
			return false;
		}
	}
	return true;
}

/** Leeftijd in dagen van een datum (JJJJ-MM-DD) ten opzichte van vandaag in de tijdzone van de site; null bij een ongeldige datum. */
function rmk_price_age_days( $date, $today = null ) {
	$tz = wp_timezone();
	$d  = DateTimeImmutable::createFromFormat( '!Y-m-d', (string) $date, $tz );
	if ( ! $d || $d->format( 'Y-m-d' ) !== $date ) {
		return null;
	}
	$t = $today ? DateTimeImmutable::createFromFormat( '!Y-m-d', $today, $tz ) : new DateTimeImmutable( 'today', $tz );
	return (int) $d->diff( $t )->format( '%r%a' );
}

/** De geldige prijs van een model, of null. */
function rmk_valid_price( array $m, $today = null ) {
	$p = isset( $m['prijs'] ) && is_array( $m['prijs'] ) ? $m['prijs'] : null;
	if ( ! $p || ! isset( $p['bedrag'], $p['winkel'], $p['datum'], $p['url'] ) ) {
		return null;
	}
	if ( ! is_numeric( $p['bedrag'] ) || $p['bedrag'] <= 0 || '' === trim( (string) $p['winkel'] ) ) {
		return null;
	}
	if ( ! in_array( isset( $p['type'] ) ? $p['type'] : '', array( 'winkel', 'fabrikant' ), true ) || ! rmk_price_url_ok( $p['url'] ) ) {
		return null;
	}
	if ( false !== stripos( $p['winkel'], 'bol' ) ) {
		return null;
	}
	$age = rmk_price_age_days( $p['datum'], $today );
	if ( null === $age || $age < 0 || $age > RMK_PRIJS_MAX_DAGEN ) {
		return null;
	}
	return $p;
}

function rmk_date_nl( $date ) {
	$maanden = array( 1 => 'januari', 'februari', 'maart', 'april', 'mei', 'juni', 'juli', 'augustus', 'september', 'oktober', 'november', 'december' );
	$d       = DateTimeImmutable::createFromFormat( '!Y-m-d', (string) $date );
	return $d ? $d->format( 'j' ) . ' ' . $maanden[ (int) $d->format( 'n' ) ] . ' ' . $d->format( 'Y' ) : '';
}

/** Prijsblok voor de productbox. */
function rmk_offer_html( array $m, $today = null ) {
	$p = rmk_valid_price( $m, $today );
	if ( $p ) {
		$winkel = trim( (string) $p['winkel'] );
		$bedrag = number_format( round( (float) $p['bedrag'] ), 0, ',', '.' );
		return '<div class="rmk-offer rmk-offer--stack"><span class="rmk-offer__line">Laagste nieuwe prijs rond <strong>' . esc_html( $bedrag ) . ' euro</strong> bij '
			. esc_html( $winkel ) . ', gezien op ' . esc_html( rmk_date_nl( $p['datum'] ) ) . '</span>'
			. '<a class="rmk-btn rmk-btn--primary" href="' . esc_url( $p['url'] ) . '" data-rmk-direct>Bekijk bij ' . esc_html( $winkel ) . '</a></div>';
	}
	$fab = isset( $m['fabrikant_url'] ) ? (string) $m['fabrikant_url'] : '';
	if ( $fab && rmk_price_url_ok( $fab ) ) {
		return '<div class="rmk-offer rmk-offer--stack"><a class="rmk-btn rmk-btn--secondary" href="' . esc_url( $fab ) . '" data-rmk-direct>Bekijk de actuele prijs</a></div>';
	}
	return '';
}

/** Vervangt in elke productbox (article.rmk-product met data-model) het prijsblok door rmk_offer_html(). */
function rmk_fill_offers( $html ) {
	if ( false === strpos( (string) $html, 'rmk-product' ) || false === strpos( (string) $html, 'rmk-offer' ) ) {
		return $html;
	}
	return preg_replace_callback( '#<article class="rmk-product"[^>]*>.*?</article>#s', function ( $a ) {
		if ( ! preg_match( '#data-model="([A-Za-z0-9-]+)"#', $a[0], $id ) || ! ( $m = rmk_get_model( $id[1] ) ) ) {
			return $a[0];
		}
		$offer = rmk_offer_html( $m );
		$done  = false;
		$a[0]  = rmk_fill_card( $a[0], $m );
		return preg_replace_callback( '#<div class="rmk-offer(?: [^"]*)?"[^>]*>(?:(?!</div>).)*</div>#s', function () use ( $offer, &$done ) {
			$out  = $done ? '' : $offer;
			$done = true;
			return $out;
		}, $a[0] );
	}, $html );
}
add_filter( 'render_block', function ( $content, $block ) {
	return 'core/html' === $block['blockName'] ? rmk_fill_offers( $content ) : $content;
}, 12, 2 ); // vóór de server-side score (prioriteit 15 en 16), die data-model uit de scorecel haalt

/* Elke nacht: is er sinds gisteren een prijs verlopen, leeg dan de paginacache zodat hij ook daar verdwijnt. */
add_action( 'init', function () {
	if ( ! wp_next_scheduled( 'rmk_prijzen_verloop' ) ) {
		$t = new DateTimeImmutable( 'tomorrow 00:10', wp_timezone() );
		wp_schedule_event( $t->getTimestamp(), 'daily', 'rmk_prijzen_verloop' );
	}
} );
add_action( 'rmk_prijzen_verloop', function () {
	$tz        = wp_timezone();
	$gisteren  = ( new DateTimeImmutable( 'yesterday', $tz ) )->format( 'Y-m-d' );
	$verlopen  = false;
	foreach ( rmk_models_data()['modellen'] as $m ) {
		if ( rmk_valid_price( $m, $gisteren ) && ! rmk_valid_price( $m ) ) {
			$verlopen = true;
		}
	}
	if ( $verlopen ) {
		do_action( 'litespeed_purge_all' );
	}
} );

/* ------------------------------------------------------------------ Productbox: specificatiekaart, Beste voor, plus- en minpunten (1.3.2)
 * Pakket "specificatiekaart" (Claude Design, v1.3): zonder foto een kaart met merk, model en vijf kenmerken;
 * met foto dezelfde kaart met de foto en "Foto: (fabrikant)". Naam en score staan alleen in de kaart.
 * Beste voor, pluspunten en minpunten komen uit modellen.json (velden beste_voor, pluspunten, minpunten). */

function rmk_nl_number( $v ) {
	$v = (float) $v;
	return floor( $v ) == $v ? number_format( $v, 0, ',', '.' ) : number_format( $v, 1, ',', '.' );
}

/** De vijf kenmerken voor de kaart: [klasse, label, waarde of null]. */
function rmk_card_specs( array $m ) {
	$sv  = function ( $k ) use ( $m ) {
		return isset( $m['specs'][ $k ]['waarde'] ) && '' !== $m['specs'][ $k ]['waarde'] ? $m['specs'][ $k ]['waarde'] : null;
	};
	$nav = $sv( 'navigatie' );
	$map = array( 'rtk+vision' => 'RTK + camera', 'vision' => 'camera', 'lidar' => 'LiDAR', 'rtk' => 'RTK', 'gnss' => 'GNSS', 'draad' => 'draad', 'lidar+vision' => 'LiDAR + camera' );
	$nav = null === $nav ? null : ( isset( $map[ strtolower( $nav ) ] ) ? $map[ strtolower( $nav ) ] : $nav );
	$ver = isset( $m['verbinding']['extra'] ) ? $m['verbinding']['extra'] : null;
	$ver = array( 'ingebouwd' => '4G', 'module' => 'module', 'geen' => 'geen' )[ $ver ] ?? null;
	$opp = $sv( 'max_tuingrootte_m2' );
	$hel = $sv( 'max_helling_pct' );
	$gel = $sv( 'geluid_dba' );
	return array(
		array( 'oppervlak', 'Oppervlak', is_numeric( $opp ) ? rmk_nl_number( $opp ) . ' m²' : null ),
		array( 'helling', 'Helling', is_numeric( $hel ) ? rmk_nl_number( $hel ) . '%' : null ),
		array( 'navigatie', 'Navigatie', $nav ),
		array( 'geluid', 'Geluid', is_numeric( $gel ) ? rmk_nl_number( $gel ) . ' dB' : null ),
		array( 'verbinding', 'Verbinding', $ver ),
	);
}

function rmk_speccard_html( array $m ) {
	$specs = '';
	foreach ( rmk_card_specs( $m ) as $c ) {
		$specs .= null === $c[2]
			? '<div class="rmk-spec rmk-spec--' . $c[0] . ' is-missing"><dt>' . $c[1] . '</dt><dd><span aria-hidden="true">–</span><span class="rmk-sr">onbekend</span></dd></div>'
			: '<div class="rmk-spec rmk-spec--' . $c[0] . '"><dt>' . $c[1] . '</dt><dd>' . esc_html( $c[2] ) . '</dd></div>';
	}
	$f = isset( $m['foto'] ) && is_array( $m['foto'] ) && ! empty( $m['foto']['url'] ) && rmk_price_url_ok( $m['foto']['url'] ) ? $m['foto'] : null;
	if ( $f ) {
		$fab    = ! empty( $f['fabrikant'] ) ? $f['fabrikant'] : ( isset( $m['merk'] ) ? $m['merk'] : '' );
		$w      = ! empty( $f['breedte'] ) ? (int) $f['breedte'] : 800;
		$h      = ! empty( $f['hoogte'] ) ? (int) $f['hoogte'] : 600;
		$visual = '<div class="rmk-speccard__visual"><img src="' . esc_url( $f['url'] ) . '" alt="' . esc_attr( $m['naam'] . ', productfoto' ) . '" width="' . $w . '" height="' . $h . '" loading="lazy" decoding="async"></div>'
			. '<figcaption class="rmk-speccard__caption">Foto: ' . esc_html( $fab ) . '</figcaption>';
		$cls    = 'rmk-speccard rmk-speccard--photo';
	} else {
		$merk   = isset( $m['merk'] ) ? $m['merk'] : '';
		$model  = isset( $m['model'] ) && $m['model'] ? $m['model'] : $m['naam'];
		$visual = '<div class="rmk-speccard__visual" aria-hidden="true"><p class="rmk-speccard__brand">' . esc_html( $merk ) . '</p><p class="rmk-speccard__model">' . esc_html( $model ) . '</p></div>'
			. '<figcaption class="rmk-speccard__caption">Geen productfoto beschikbaar</figcaption>';
		$cls    = 'rmk-speccard';
	}
	return '<div class="' . $cls . '"><figure class="rmk-speccard__figure">' . $visual . '</figure><dl class="rmk-speccard__specs" aria-label="Belangrijkste kenmerken">' . $specs . '</dl></div>';
}

function rmk_proscons_html( array $m ) {
	$list = function ( $key, $titel, $cls ) use ( $m ) {
		$items = isset( $m[ $key ] ) && is_array( $m[ $key ] ) ? array_filter( array_map( 'strval', $m[ $key ] ) ) : array();
		return $items ? '<div><h4>' . $titel . '</h4><ul class="' . $cls . '"><li>' . implode( '</li><li>', array_map( 'esc_html', $items ) ) . '</li></ul></div>' : '';
	};
	$h = $list( 'pluspunten', 'Pluspunten', 'rmk-pros' ) . $list( 'minpunten', 'Minpunten', 'rmk-cons' );
	return $h ? '<div class="rmk-proscons">' . $h . '</div>' : '';
}

function rmk_fill_card( $article, array $m ) {
	// Bestaand beeldblok, plaatsvervanger of eerdere kaart weg; de kaart komt vooraan in de kop.
	$article = preg_replace( '#<div class="rmk-product__media">\s*(?:<!--.*?-->\s*)?(?:<figure\b.*?</figure>|<div class="rmk-ph">.*?</span></div>|<img\b[^>]*>)\s*</div>#s', '', $article );
	$article = preg_replace( '#<div class="rmk-speccard\b[^"]*">.*?</dl>\s*</div>#s', '', $article );
	$article = preg_replace( '#<div class="rmk-product__head(?: rmk-product__head--nomedia)?"(?: style="[^"]*")?>#', '<div class="rmk-product__head">' . rmk_speccard_html( $m ), $article, 1 );
	if ( ! empty( $m['beste_voor'] ) && false === strpos( $article, 'rmk-bestfor' ) ) {
		$article = preg_replace( '#(<h3\b[^>]*>.*?</h3>)#s', '$1<p class="rmk-bestfor"><span>Beste voor</span> ' . esc_html( $m['beste_voor'] ) . '</p>', $article, 1 );
	}
	// Analyse (1.3.4): eigen alinea onder "Beste voor", boven de plus- en minpunten.
	if ( ! empty( $m['analyse'] ) && false === strpos( $article, 'rmk-analyse' ) ) {
		$an      = '<p class="rmk-analyse">' . esc_html( $m['analyse'] ) . '</p>';
		$article = preg_match( '#<div class="rmk-proscons">#', $article )
			? preg_replace( '#(<div class="rmk-proscons">)#', $an . '$1', $article, 1 )
			: preg_replace( '#(<div class="rmk-product__aside)#', $an . '$1', $article, 1 );
	}
	if ( false === strpos( $article, 'rmk-proscons' ) && ( $pc = rmk_proscons_html( $m ) ) ) {
		$article = preg_replace( '#(<div class="rmk-product__aside)#', $pc . '$1', $article, 1, $n );
		if ( ! $n ) {
			$article = str_replace( '</article>', $pc . '</article>', $article );
		}
	}
	return $article;
}

/* ------------------------------------------------------------------ Prijs in tabellen (1.3.3)
 * Scoretabel en vergelijkingstabel: "rond 899 euro" met de winkel klein eronder, alleen bij een geldige prijs
 * (zelfde regels als de productbox), anders "–". Onder de tabel één regel met de datum waarop de prijzen zijn gezien. */

function rmk_price_cell( array $m ) {
	$p = rmk_valid_price( $m );
	if ( ! $p ) {
		return '<span aria-hidden="true">–</span><span class="rmk-sr">geen actuele prijs</span>';
	}
	return 'rond ' . esc_html( number_format( round( (float) $p['bedrag'] ), 0, ',', '.' ) ) . ' euro<br><span class="rmk-small">' . esc_html( $p['winkel'] ) . '</span>';
}

/** "Prijzen gezien op 5 oktober 2026." voor de geldige prijzen van deze modellen; leeg als er geen is. */
function rmk_price_date_line( array $models ) {
	$dates = array();
	foreach ( $models as $m ) {
		if ( $m && ( $p = rmk_valid_price( $m ) ) ) {
			$dates[] = $p['datum'];
		}
	}
	if ( ! $dates ) {
		return '';
	}
	sort( $dates );
	$min = reset( $dates );
	$max = end( $dates );
	$txt = $min === $max ? 'Prijzen gezien op ' . rmk_date_nl( $min ) . '.' : 'Prijzen gezien tussen ' . rmk_date_nl( $min ) . ' en ' . rmk_date_nl( $max ) . '.';
	return '<p class="rmk-small rmk-pricedate">' . esc_html( $txt ) . ' Laagste nieuwe prijs bij een winkel of de fabrikant, afgerond.</p>';
}

/** In de inhoud: <td data-rmk-price="M002"></td>, <p data-rmk-prijsdatum="M002,M010"></p> en data-price op tr[data-model]. */
function rmk_fill_table_prices( $html ) {
	if ( false === strpos( (string) $html, 'data-rmk-price' ) && false === strpos( (string) $html, 'data-rmk-prijsdatum' ) ) {
		return $html;
	}
	$html = preg_replace_callback( '#(<td\b[^>]*\bdata-rmk-price="([A-Za-z0-9-]+)"[^>]*>)(.*?)(</td>)#s', function ( $c ) {
		$m = rmk_get_model( $c[2] );
		return $c[1] . ( $m ? rmk_price_cell( $m ) : '–' ) . $c[4];
	}, $html );
	// data-price (voor sorteren en het budgetfilter) op de rij van een model met een geldige prijs
	$html = preg_replace_callback( '#<tr\b([^>]*)\bdata-price=""([^>]*)>(.*?)</tr>#s', function ( $r ) {
		if ( ! preg_match( '#data-rmk-price="([A-Za-z0-9-]+)"#', $r[3], $id ) || ! ( $m = rmk_get_model( $id[1] ) ) || ! ( $p = rmk_valid_price( $m ) ) ) {
			return $r[0];
		}
		return '<tr' . $r[1] . 'data-price="' . (int) round( (float) $p['bedrag'] ) . '"' . $r[2] . '>' . $r[3] . '</tr>';
	}, $html );
	return preg_replace_callback( '#<p\b[^>]*\bdata-rmk-prijsdatum="([A-Za-z0-9,\s-]+)"[^>]*>\s*</p>#', function ( $c ) {
		return rmk_price_date_line( array_map( 'rmk_get_model', array_filter( array_map( 'trim', explode( ',', $c[1] ) ) ) ) );
	}, $html );
}
add_filter( 'render_block', function ( $content, $block ) {
	return 'core/html' === $block['blockName'] ? rmk_fill_table_prices( $content ) : $content;
}, 13, 2 );
