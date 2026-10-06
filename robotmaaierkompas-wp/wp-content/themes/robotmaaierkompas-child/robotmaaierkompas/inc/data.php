<?php
/**
 * robotmaaierkompas.nl — modelbestand via de API bijwerken, zonder nieuwe thema-zip
 *
 * - POST /wp-json/rmk/v1/modellen  (alleen beheerders, bijv. met een toepassingswachtwoord)
 *   Body: de volledige inhoud van modellen.json. Wordt gecontroleerd en opgeslagen in de database
 *   (optie rmk_modellen) en als bestand in wp-content/uploads/rmk/modellen.json voor de calculator.
 * - GET  /wp-json/rmk/v1/modellen  (alleen beheerders): wat er nu is opgeslagen, met bron en tijdstip.
 * - Zonder opgeslagen versie gebruikt de site het bestand uit het thema (data/modellen.json).
 * - Geweigerd: geen lijst "modellen", modellen zonder id/slug/naam, een prijslijst ("prijzen"),
 *   een ingevulde aanschafprijs of bol.com-gegevens (besluit 5 oktober 2026), of meer dan 2 MB.
 * - Toegestaan (besluit 6 oktober 2026): per model één "prijs" {bedrag (hele euro's), winkel, datum, url,
 *   type winkel of fabrikant}; geen Bol en geen marketplace. Zie inc/prijzen.php.
 */

defined( 'ABSPATH' ) || exit;

const RMK_MODELLEN_OPTION = 'rmk_modellen';

function rmk_modellen_upload_paths() {
	$u = wp_upload_dir( null, false );
	return array( 'dir' => trailingslashit( $u['basedir'] ) . 'rmk', 'url' => trailingslashit( $u['baseurl'] ) . 'rmk' );
}

/** Geeft een lijst met fouten terug; leeg = in orde. */
function rmk_validate_modellen( $data ) {
	$err = array();
	if ( ! is_array( $data ) || ! isset( $data['modellen'] ) || ! is_array( $data['modellen'] ) ) {
		return array( 'Geen lijst "modellen".' );
	}
	foreach ( $data['modellen'] as $i => $m ) {
		foreach ( array( 'id', 'slug', 'naam' ) as $k ) {
			if ( empty( $m[ $k ] ) || ! is_string( $m[ $k ] ) ) {
				$err[] = "Model $i: '$k' ontbreekt.";
			}
		}
		if ( isset( $m['prijzen'] ) ) {
			$err[] = "Model $i: bevat een prijslijst (alleen één veld \"prijs\" per model).";
		}
		if ( isset( $m['prijs'] ) && null !== $m['prijs'] ) {
			$pr = $m['prijs'];
			if ( ! is_array( $pr ) || ! isset( $pr['bedrag'], $pr['winkel'], $pr['datum'], $pr['url'], $pr['type'] ) ) {
				$err[] = "Model $i: prijs mist bedrag, winkel, datum, url of type.";
			} elseif ( ! in_array( $pr['type'], array( 'winkel', 'fabrikant' ), true ) ) {
				$err[] = "Model $i: prijs is niet van een winkel of de fabrikant.";
			} elseif ( ! rmk_price_url_ok( $pr['url'] ) ) {
				$err[] = "Model $i: prijs-URL is geen https-productpagina van een toegestane winkel.";
			} elseif ( ! is_int( $pr['bedrag'] ) || $pr['bedrag'] <= 0 ) {
				$err[] = "Model $i: prijsbedrag moet een heel getal in euro's zijn.";
			}
		}
		if ( ! empty( $m['foto'] ) && ( ! is_array( $m['foto'] ) || empty( $m['foto']['url'] ) || ! rmk_price_url_ok( $m['foto']['url'] ) ) ) {
			$err[] = "Model $i: foto moet een https-URL zijn, niet van Bol of een marketplace.";
		}
		if ( isset( $m['kosten']['aanschaf']['waarde'] ) && null !== $m['kosten']['aanschaf']['waarde'] ) {
			$err[] = "Model $i: aanschafprijs is ingevuld (moet leeg blijven).";
		}
	}
	if ( false !== stripos( wp_json_encode( $data ), 'bol.com' ) ) {
		$err[] = 'Bevat bol.com-gegevens (voorlopig geen Bol-gegevens).';
	}
	return $err;
}

add_filter( 'rmk_models_file', function ( $file ) {
	$p = rmk_modellen_upload_paths();
	return get_option( RMK_MODELLEN_OPTION ) && is_readable( $p['dir'] . '/modellen.json' ) ? $p['dir'] . '/modellen.json' : $file;
} );

add_filter( 'rmk_config', function ( $config ) {
	$saved = get_option( RMK_MODELLEN_OPTION );
	if ( $saved ) {
		$p                    = rmk_modellen_upload_paths();
		$config['modelsUrl'] = $p['url'] . '/modellen.json?v=' . rawurlencode( (string) $saved['opgeslagen'] );
	}
	return $config;
} );

function rmk_save_modellen( array $data ) {
	$p = rmk_modellen_upload_paths();
	if ( ! wp_mkdir_p( $p['dir'] ) ) {
		return new WP_Error( 'rmk_upload', 'Kan wp-content/uploads/rmk niet aanmaken.' );
	}
	$json = wp_json_encode( $data, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT );
	if ( false === file_put_contents( $p['dir'] . '/modellen.json', $json ) ) {
		return new WP_Error( 'rmk_upload', 'Kan modellen.json niet schrijven.' );
	}
	$meta = array(
		'opgeslagen'  => time(),
		'gegenereerd' => isset( $data['gegenereerd'] ) ? (string) $data['gegenereerd'] : '',
		'bronbestand' => isset( $data['bronbestand'] ) ? (string) $data['bronbestand'] : '',
		'modellen'    => count( $data['modellen'] ),
		'door'        => get_current_user_id(),
	);
	update_option( RMK_MODELLEN_OPTION, $meta, false );
	update_option( RMK_MODELLEN_OPTION . '_data', $data, false );
	do_action( 'litespeed_purge_all' ); // scores en calculator staan in gecachte pagina's
	return $meta;
}

add_action( 'rest_api_init', function () {
	$admin = function () {
		return current_user_can( 'manage_options' );
	};
	register_rest_route( 'rmk/v1', '/modellen', array(
		array(
			'methods'             => 'GET',
			'permission_callback' => $admin,
			'callback'            => function () {
				$meta = get_option( RMK_MODELLEN_OPTION );
				return rest_ensure_response( array( 'bron' => $meta ? 'database en uploads' : 'thema', 'meta' => $meta, 'data' => rmk_models_data() ) );
			},
		),
		array(
			'methods'             => 'POST',
			'permission_callback' => $admin,
			'callback'            => function ( WP_REST_Request $req ) {
				if ( strlen( $req->get_body() ) > 2 * MB_IN_BYTES ) {
					return new WP_Error( 'rmk_te_groot', 'Bestand groter dan 2 MB.', array( 'status' => 413 ) );
				}
				$data = json_decode( $req->get_body(), true );
				$err  = rmk_validate_modellen( $data );
				if ( $err ) {
					return new WP_Error( 'rmk_ongeldig', implode( ' ', $err ), array( 'status' => 400 ) );
				}
				$r = rmk_save_modellen( $data );
				return is_wp_error( $r ) ? $r : rest_ensure_response( $r );
			},
		),
	) );
} );
