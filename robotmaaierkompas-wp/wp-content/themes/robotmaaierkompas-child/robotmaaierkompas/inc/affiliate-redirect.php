<?php
/**
 * robotmaaierkompas.nl — centrale affiliate-redirect /ga/[winkel]/[model]/
 *
 * - Doel-URL's staan in de optie rmk_affiliate_links (winkel => model-slug => URL), te beheren met
 *   wp rmk link <winkel> <model-slug> <url>. Alleen URL's op een domein uit rmk_affiliate_domains()
 *   worden geaccepteerd (geen open redirect).
 * - Elke klik wordt geteld in de tabel {prefix}rmk_clicks: tijdstip, winkel, model en de pagina waarop
 *   geklikt is (alleen het pad). Geen IP-adres, geen user-agent, geen cookie. Bots worden niet geteld.
 * - Antwoord: 302 met X-Robots-Tag: noindex, nofollow. Links naar /ga/ krijgen rel="sponsored nofollow"
 *   via rmk_add_affiliate_rel() in robotmaaierkompas-setup.php.
 * - Onbekende combinatie: 404 (ook noindex). Wijzig je de rewrite-regel: Instellingen > Permalinks > Opslaan.
 */

defined( 'ABSPATH' ) || exit;

const RMK_LINKS_OPTION = 'rmk_affiliate_links';
const RMK_CLICKS_DBV   = '1';

function rmk_clicks_table() {
	global $wpdb;
	return $wpdb->prefix . 'rmk_clicks';
}

function rmk_clicks_install() {
	if ( get_option( 'rmk_clicks_dbv' ) === RMK_CLICKS_DBV ) {
		return;
	}
	global $wpdb;
	require_once ABSPATH . 'wp-admin/includes/upgrade.php';
	dbDelta( 'CREATE TABLE ' . rmk_clicks_table() . " (
		id bigint(20) unsigned NOT NULL AUTO_INCREMENT,
		tijd datetime NOT NULL,
		winkel varchar(40) NOT NULL,
		model varchar(120) NOT NULL,
		pagina varchar(255) NOT NULL DEFAULT '',
		PRIMARY KEY  (id),
		KEY winkel_model (winkel,model),
		KEY tijd (tijd)
	) " . $wpdb->get_charset_collate() . ';' );
	update_option( 'rmk_clicks_dbv', RMK_CLICKS_DBV );
}
add_action( 'after_switch_theme', 'rmk_clicks_install' );
add_action( 'admin_init', 'rmk_clicks_install' );

add_action( 'init', function () {
	add_rewrite_rule( '^ga/([a-z0-9-]+)/([a-z0-9-]+)/?$', 'index.php?rmk_ga_winkel=$matches[1]&rmk_ga_model=$matches[2]', 'top' );
} );
add_filter( 'query_vars', function ( $vars ) {
	$vars[] = 'rmk_ga_winkel';
	$vars[] = 'rmk_ga_model';
	return $vars;
} );
add_action( 'after_switch_theme', 'flush_rewrite_rules' );

function rmk_affiliate_target( $winkel, $model ) {
	$links = (array) get_option( RMK_LINKS_OPTION, array() );
	$url   = isset( $links[ $winkel ][ $model ] ) ? $links[ $winkel ][ $model ] : '';
	$url   = apply_filters( 'rmk_affiliate_target', $url, $winkel, $model );
	if ( ! $url || ! wp_http_validate_url( $url ) || ! rmk_is_affiliate_url( $url ) ) {
		return '';
	}
	return $url;
}

function rmk_is_bot( $ua ) {
	return '' === $ua || (bool) preg_match( '/bot|crawl|spider|slurp|preview|monitor|curl|wget|python|headless/i', $ua );
}

function rmk_log_click( $winkel, $model ) {
	global $wpdb;
	rmk_clicks_install();
	$ref    = isset( $_SERVER['HTTP_REFERER'] ) ? wp_unslash( $_SERVER['HTTP_REFERER'] ) : '';
	$pagina = '';
	if ( $ref && wp_parse_url( $ref, PHP_URL_HOST ) === wp_parse_url( home_url(), PHP_URL_HOST ) ) {
		$pagina = substr( (string) wp_parse_url( $ref, PHP_URL_PATH ), 0, 255 );
	}
	$wpdb->insert( rmk_clicks_table(), array(
		'tijd'   => current_time( 'mysql', true ),
		'winkel' => $winkel,
		'model'  => $model,
		'pagina' => $pagina,
	), array( '%s', '%s', '%s', '%s' ) );
}

add_action( 'template_redirect', function () {
	$winkel = get_query_var( 'rmk_ga_winkel' );
	$model  = get_query_var( 'rmk_ga_model' );
	if ( ! $winkel || ! $model ) {
		return;
	}
	$winkel = sanitize_key( $winkel );
	$model  = sanitize_title( $model );
	header( 'X-Robots-Tag: noindex, nofollow', true );
	nocache_headers();
	do_action( 'litespeed_control_set_nocache', 'rmk affiliate-redirect' ); // anders telt een gecachte redirect geen klik
	$target = rmk_affiliate_target( $winkel, $model );
	if ( ! $target ) {
		status_header( 404 );
		header( 'Content-Type: text/plain; charset=utf-8' );
		echo 'Deze winkellink bestaat (nog) niet.';
		exit;
	}
	$ua = isset( $_SERVER['HTTP_USER_AGENT'] ) ? (string) wp_unslash( $_SERVER['HTTP_USER_AGENT'] ) : '';
	if ( ! rmk_is_bot( $ua ) ) {
		rmk_log_click( $winkel, $model );
	}
	wp_redirect( $target, 302, 'robotmaaierkompas' ); // wp_redirect, niet wp_safe_redirect: doel is extern en hierboven gecontroleerd
	exit;
}, 0 );

/* SEO-plugins: /ga/ nooit in sitemaps of index (voor de zekerheid; het zijn geen berichten). */
add_filter( 'wp_robots', function ( $robots ) {
	if ( get_query_var( 'rmk_ga_winkel' ) ) {
		$robots['noindex']  = true;
		$robots['nofollow'] = true;
	}
	return $robots;
} );

if ( defined( 'WP_CLI' ) && WP_CLI ) {
	WP_CLI::add_command( 'rmk link', function ( $args ) {
		list( $winkel, $model, $url ) = array_pad( $args, 3, '' );
		$winkel = sanitize_key( $winkel );
		$model  = sanitize_title( $model );
		if ( ! $winkel || ! $model || ! wp_http_validate_url( $url ) ) {
			WP_CLI::error( 'Gebruik: wp rmk link <winkel> <model-slug> <affiliate-url>' );
		}
		if ( ! rmk_is_affiliate_url( $url ) ) {
			WP_CLI::error( 'Dit domein staat niet in rmk_affiliate_domains(). Voeg het daar eerst toe.' );
		}
		$links                      = (array) get_option( RMK_LINKS_OPTION, array() );
		$links[ $winkel ][ $model ] = esc_url_raw( $url );
		update_option( RMK_LINKS_OPTION, $links, false );
		WP_CLI::success( "/ga/$winkel/$model/ wijst nu naar $url" );
	} );
	WP_CLI::add_command( 'rmk kliks', function () {
		global $wpdb;
		rmk_clicks_install();
		$rows = $wpdb->get_results( 'SELECT winkel, model, COUNT(*) AS kliks, MAX(tijd) AS laatste FROM ' . rmk_clicks_table() . ' GROUP BY winkel, model ORDER BY kliks DESC', ARRAY_A );
		WP_CLI\Utils\format_items( 'table', $rows ? $rows : array(), array( 'winkel', 'model', 'kliks', 'laatste' ) );
	} );
}
