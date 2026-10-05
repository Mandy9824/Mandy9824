<?php
/**
 * robotmaaierkompas.nl — techniek: consent-gestuurde meetcode, schema-afspraken, WebP, noindex, snelheid.
 *
 * Meetcode (instellen in wp-config.php, niet in git):
 *   define( 'RMK_GA4_ID', 'G-XXXXXXX' );                 // of laat weg: dan wordt er niets geladen
 *   define( 'RMK_GSC_VERIFICATIE', 'code-uit-search-console' ); // liever DNS-verificatie, zie bouwlogboek
 * Beide worden pas geladen nadat de bezoeker in de cookiebanner toestemming geeft voor statistieken
 * (event rmk:consent uit rmk.js, detail.stats === true).
 */

defined( 'ABSPATH' ) || exit;

/* ------------------------------------------------------------------ 1. Meetcode alleen na toestemming */
add_action( 'wp_enqueue_scripts', function () {
	$ga  = defined( 'RMK_GA4_ID' ) ? preg_replace( '/[^A-Z0-9-]/', '', strtoupper( RMK_GA4_ID ) ) : '';
	$gsc = defined( 'RMK_GSC_VERIFICATIE' ) ? preg_replace( '/[^A-Za-z0-9_-]/', '', RMK_GSC_VERIFICATIE ) : '';
	if ( ! $ga && ! $gsc ) {
		return;
	}
	$js = '(function(){var done=false;window.addEventListener("rmk:consent",function(e){'
		. 'if(done||!e.detail||!e.detail.stats)return;done=true;';
	if ( $gsc ) {
		$js .= 'var m=document.createElement("meta");m.name="google-site-verification";m.content=' . wp_json_encode( $gsc ) . ';document.head.appendChild(m);';
	}
	if ( $ga ) {
		$js .= 'var s=document.createElement("script");s.async=true;s.src="https://www.googletagmanager.com/gtag/js?id=' . $ga . '";document.head.appendChild(s);'
			. 'window.dataLayer=window.dataLayer||[];window.gtag=function(){dataLayer.push(arguments);};gtag("js",new Date());'
			. 'gtag("config",' . wp_json_encode( $ga ) . ',{anonymize_ip:true});';
	}
	$js .= '});})();';
	// Vóór rmk.js, zodat de luisteraar er is als rmk.js een eerder opgeslagen keuze doorgeeft.
	wp_add_inline_script( 'rmk', $js, 'before' );
}, 20 );

/* ------------------------------------------------------------------ 2. Schema (Yoast SEO) */
// Pagina's als Article (met auteur, datePublished en dateModified), zoals BLAUWDRUK hoofdstuk 10.
// Yoast geeft Article-schema aan berichttypen die 'author' ondersteunen.
add_action( 'init', function () {
	add_post_type_support( 'page', 'author' );
} );
// Nooit Product, Review, AggregateRating of Offer in het schema: we testen niet zelf.
add_filter( 'wpseo_schema_graph', function ( $graph ) {
	$verboden = array( 'Product', 'Review', 'AggregateRating', 'Offer', 'IndividualProduct' );
	return array_values( array_filter( $graph, function ( $piece ) use ( $verboden ) {
		$t = isset( $piece['@type'] ) ? (array) $piece['@type'] : array();
		return ! array_intersect( $t, $verboden );
	} ) );
}, 99 );
// Person: alternateName uit het gebruikersprofiel (veld rmk_alternate_name, komma-gescheiden), zie BLAUWDRUK hoofdstuk 7.
// sameAs komt uit de Yoast-profielvelden van de gebruiker (andere sites, LinkedIn).
add_filter( 'wpseo_schema_person_data', function ( $data, $user_id ) {
	$alt = $user_id ? trim( (string) get_user_meta( $user_id, 'rmk_alternate_name', true ) ) : '';
	if ( $alt ) {
		$data['alternateName'] = array_values( array_filter( array_map( 'trim', explode( ',', $alt ) ) ) );
	}
	// sameAs: één URL per regel in het profielveld rmk_same_as, samengevoegd met wat Yoast al heeft.
	$same = $user_id ? preg_split( '/[\s,]+/', (string) get_user_meta( $user_id, 'rmk_same_as', true ), -1, PREG_SPLIT_NO_EMPTY ) : array();
	$same = array_values( array_filter( array_map( 'esc_url_raw', $same ) ) );
	if ( $same ) {
		$data['sameAs'] = array_values( array_unique( array_merge( isset( $data['sameAs'] ) ? (array) $data['sameAs'] : array(), $same ) ) );
	}
	return $data;
}, 10, 2 );

// Yoast-metabeschrijving per pagina via de REST-API (meta._yoast_wpseo_metadesc), alleen voor wie de pagina mag bewerken.
add_action( 'init', function () {
	foreach ( array( 'page', 'post' ) as $type ) {
		register_post_meta( $type, '_yoast_wpseo_metadesc', array(
			'type'          => 'string',
			'single'        => true,
			'show_in_rest'  => true,
			'auth_callback' => function ( $allowed, $meta_key, $post_id ) {
				return current_user_can( 'edit_post', $post_id );
			},
		) );
	}
} );

// Beide velden zijn via de REST-API (/wp/v2/users/<id>, "meta") te zetten door wie de gebruiker mag bewerken.
add_action( 'init', function () {
	foreach ( array( 'rmk_alternate_name', 'rmk_same_as' ) as $key ) {
		register_meta( 'user', $key, array(
			'type'          => 'string',
			'single'        => true,
			'show_in_rest'  => true,
			'auth_callback' => function ( $allowed, $meta_key, $object_id ) {
				return current_user_can( 'edit_user', $object_id );
			},
		) );
	}
} );

/* ------------------------------------------------------------------ 3. Afbeeldingen: WebP en lazy loading */
// Nieuwe JPEG- en PNG-uploads krijgen WebP-afmetingen (WordPress-kern, vanaf 5.8; GD of Imagick met WebP nodig).
add_filter( 'image_editor_output_format', function ( $formats ) {
	$formats['image/jpeg'] = 'image/webp';
	$formats['image/png']  = 'image/webp';
	return $formats;
} );
add_filter( 'wp_lazy_loading_enabled', '__return_true' ); // standaard al aan; hier vastgelegd

/* ------------------------------------------------------------------ 4. Noindex op zoekresultaten, tag- en auteursarchieven */
// Yoast doet dit ook via de instellingen; dit is een vangnet als de plugin uit staat.
add_filter( 'wp_robots', function ( $robots ) {
	if ( is_search() || is_tag() || is_author() || is_date() || is_attachment() ) {
		$robots['noindex'] = true;
		$robots['follow']  = true;
	}
	return $robots;
} );

/* ------------------------------------------------------------------ 5. Snelheid: overbodige onderdelen uit */
remove_action( 'wp_head', 'print_emoji_detection_script', 7 );
remove_action( 'wp_print_styles', 'print_emoji_styles' );
remove_action( 'wp_head', 'wp_generator' );
remove_action( 'wp_head', 'wlwmanifest_link' );
remove_action( 'wp_head', 'rsd_link' );
