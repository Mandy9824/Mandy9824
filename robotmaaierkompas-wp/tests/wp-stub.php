<?php
/**
 * Minimale nagebootste WordPress-omgeving om themacode zonder WordPress te testen (php tests/<test>.php).
 * Alleen de functies die inc/bol.php, inc/prijzen.php, inc/score.php, inc/redactie.php en inc/data.php gebruiken.
 * Geen netwerk: elke HTTP-aanvraag gaat via de filter pre_http_request (nagebootste antwoorden in de test).
 */
define( 'ABSPATH', '/' );
define( 'MINUTE_IN_SECONDS', 60 );
define( 'HOUR_IN_SECONDS', 3600 );
define( 'DAY_IN_SECONDS', 86400 );
define( 'WEEK_IN_SECONDS', 604800 );
define( 'MB_IN_BYTES', 1048576 );

$GLOBALS['wp_filters'] = array();
$GLOBALS['wp_options'] = array();
$GLOBALS['wp_trans']   = array();
$GLOBALS['wp_cron']    = array();
$GLOBALS['wp_routes']  = array();
$GLOBALS['wp_acties']  = array(); // telt do_action-aanroepen
$GLOBALS['wp_post']    = array( 'id' => 11, 'slug' => 'robotmaaier-zonder-draad' );

function add_filter( $h, $f, $p = 10, $n = 1 ) { $GLOBALS['wp_filters'][ $h ][ $p ][] = array( $f, $n ); return true; }
function add_action( $h, $f, $p = 10, $n = 1 ) { return add_filter( $h, $f, $p, $n ); }
function remove_filter( $h, $f, $p = 10 ) {
	foreach ( $GLOBALS['wp_filters'][ $h ][ $p ] ?? array() as $i => $c ) {
		if ( $c[0] === $f ) { unset( $GLOBALS['wp_filters'][ $h ][ $p ][ $i ] ); }
	}
	return true;
}
function remove_action( $h, $f, $p = 10 ) { return remove_filter( $h, $f, $p ); }
function remove_all_filters( $h ) { unset( $GLOBALS['wp_filters'][ $h ] ); }
function apply_filters( $h, $v, ...$a ) {
	$fs = $GLOBALS['wp_filters'][ $h ] ?? array();
	ksort( $fs );
	foreach ( $fs as $lijst ) {
		foreach ( $lijst as $c ) {
			$v = call_user_func_array( $c[0], array_slice( array_merge( array( $v ), $a ), 0, max( 1, $c[1] ) ) );
		}
	}
	return $v;
}
function do_action( $h, ...$a ) {
	$GLOBALS['wp_acties'][ $h ] = ( $GLOBALS['wp_acties'][ $h ] ?? 0 ) + 1;
	$GLOBALS['wp_acties_args'][ $h ][] = $a;
	$fs = $GLOBALS['wp_filters'][ $h ] ?? array();
	ksort( $fs );
	foreach ( $fs as $lijst ) {
		foreach ( $lijst as $c ) {
			call_user_func_array( $c[0], array_slice( $a, 0, max( 0, $c[1] ) ?: count( $a ) ) );
		}
	}
}
function add_shortcode() {}
function register_setting() {}
function get_option( $k, $d = false ) { return array_key_exists( $k, $GLOBALS['wp_options'] ) ? $GLOBALS['wp_options'][ $k ] : $d; }
function update_option( $k, $v, $al = null ) { $GLOBALS['wp_options'][ $k ] = $v; return true; }
function delete_option( $k ) { unset( $GLOBALS['wp_options'][ $k ] ); return true; }
function get_transient( $k ) {
	$t = $GLOBALS['wp_trans'][ $k ] ?? null;
	return $t && $t[1] > rmk_bol_nu() ? $t[0] : false;
}
function set_transient( $k, $v, $s ) { $GLOBALS['wp_trans'][ $k ] = array( $v, rmk_bol_nu() + $s ); return true; }
function delete_transient( $k ) { unset( $GLOBALS['wp_trans'][ $k ] ); return true; }
function wp_next_scheduled( $h ) { return $GLOBALS['wp_cron'][ $h ][0] ?? false; }
function wp_schedule_event( $t, $r, $h ) { $GLOBALS['wp_cron'][ $h ] = array( $t, $r ); return true; }
function wp_clear_scheduled_hook( $h ) { unset( $GLOBALS['wp_cron'][ $h ] ); return 1; }
function wp_timezone() { return new DateTimeZone( 'Europe/Amsterdam' ); }
function wp_date( $f, $t = null ) { return ( new DateTimeImmutable( '@' . ( $t ?? time() ) ) )->setTimezone( wp_timezone() )->format( $f ); }
function wp_parse_url( $u, $c = -1 ) { return parse_url( $u, $c ); }
function esc_html( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES, 'UTF-8' ); }
function esc_attr( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES, 'UTF-8' ); }
function esc_url( $s ) { return str_replace( '&', '&#038;', (string) $s ); } // zoals WordPress: & wordt &#038;
function wp_json_encode( $d, $o = 0 ) { return json_encode( $d, $o ); }
function wp_list_pluck( $l, $k ) { return array_map( function ( $x ) use ( $k ) { return is_array( $x ) ? $x[ $k ] : $x->$k; }, $l ); }
function sanitize_html_class( $c ) { return preg_replace( '/[^A-Za-z0-9_-]/', '', $c ); }
function mysql2date( $f, $d ) { return ( new DateTimeImmutable( $d ) )->format( $f ); }
function get_the_ID() { return $GLOBALS['wp_post']['id']; }
function get_queried_object_id() { return $GLOBALS['wp_post']['id']; }
function get_post_field( $f, $id ) { return 'post_name' === $f ? $GLOBALS['wp_post']['slug'] : ''; }
function current_user_can() { return $GLOBALS['wp_admin'] ?? false; }
function register_rest_route( $ns, $r, $a ) { $GLOBALS['wp_routes'][ $ns . $r ] = $a; }
function rest_ensure_response( $d ) { return $d; }
function wp_upload_dir() { return array( 'basedir' => sys_get_temp_dir(), 'baseurl' => 'https://example.test/uploads' ); }
function trailingslashit( $s ) { return rtrim( $s, '/' ) . '/'; }
function is_wp_error( $x ) { return $x instanceof WP_Error; }
class WP_Error {
	public $code, $message;
	function __construct( $c = '', $m = '', $d = null ) { $this->code = $c; $this->message = $m; }
	function get_error_message() { return $this->message; }
}
// HTTP via pre_http_request (zoals WordPress); zonder nagebootst antwoord: fout, nooit netwerk.
function wp_remote_request( $url, $args = array() ) {
	$r = apply_filters( 'pre_http_request', false, $args, $url );
	return false === $r ? new WP_Error( 'geen_netwerk', 'Geen netwerk in de test.' ) : $r;
}
function wp_remote_retrieve_response_code( $r ) { return is_array( $r ) ? $r['response']['code'] : ''; }
function wp_remote_retrieve_body( $r ) { return is_array( $r ) ? $r['body'] : ''; }
function wp_remote_retrieve_header( $r, $h ) { return is_array( $r ) ? ( $r['headers'][ strtolower( $h ) ] ?? '' ) : ''; }
