<?php
/**
 * robotmaaierkompas.nl — uitgelicht beeld in de kop (1.3.3)
 *
 * - Kernpagina's, gidsen en de methodepagina: het uitgelichte beeld (16:9) komt direct onder de paginakop,
 *   met breedte, hoogte en srcset (wp_get_attachment_image).
 * - Homepage: het beeld is de achtergrond van de hero, met een donkergroene verloop-overlay (contrast AA) en
 *   daarboven het hoogtelijnen- en kompasmotief.
 * - Het kopbeeld is het LCP-element: fetchpriority="high" en geen lazy loading. Alle andere beelden in de inhoud
 *   krijgen lazy loading (wp_omit_loading_attr_threshold = 0).
 * - Alt-tekst: die uit de mediabibliotheek. Leeg = decoratief (de H1 zegt al waar de pagina over gaat).
 * - Deelbeeld (1.3.4): altijd het standaard deelbeeld van Claude Design (1200 x 630, PNG, Yoast-instelling
 *   og_default_image_id), niet het WebP-kopbeeld: dat tonen niet alle sociale platforms.
 */

defined( 'ABSPATH' ) || exit;

add_filter( 'wp_omit_loading_attr_threshold', '__return_zero' );

function rmk_header_image_tag( $post_id, $sizes, $class ) {
	$id = (int) get_post_thumbnail_id( $post_id );
	if ( ! $id ) {
		return '';
	}
	return wp_get_attachment_image( $id, 'full', false, array(
		'class'         => $class,
		'sizes'         => $sizes,
		'loading'       => 'eager',
		'fetchpriority' => 'high',
		'decoding'      => 'async',
		'alt'           => (string) get_post_meta( $id, '_wp_attachment_image_alt', true ),
	) );
}

add_filter( 'render_block', function ( $content, $block ) {
	static $done = false;
	if ( $done || 'core/html' !== $block['blockName'] || is_admin() ) {
		return $content;
	}
	$post_id = get_queried_object_id();
	if ( ! $post_id || ! is_singular( 'page' ) || ! has_post_thumbnail( $post_id ) || get_the_ID() !== $post_id ) {
		return $content;
	}
	// Homepage: beeld als achtergrond van de hero
	if ( false !== strpos( $content, '<section class="rmk-hero ' ) || false !== strpos( $content, '<section class="rmk-hero"' ) ) {
		$img = rmk_header_image_tag( $post_id, '100vw', 'rmk-hero__bg' );
		$new = preg_replace( '#<section class="rmk-hero([^"]*)"([^>]*)>#', '<section class="rmk-hero rmk-hero--photo$1"$2>' . $img, $content, 1, $n );
		if ( $n ) {
			$done = true;
			return $new;
		}
	}
	// Kernpagina's en gidsen: beeld onder de paginakop
	if ( preg_match( '#<header class="rmk-pagehead[^"]*"[^>]*>.*?</header>#s', $content, $m ) ) {
		$narrow = false !== strpos( $content, 'rmk-column--narrow' );
		$sizes  = $narrow ? '(min-width: 54rem) 50rem, calc(100vw - 2rem)' : '(min-width: 68rem) 60rem, calc(100vw - 2rem)';
		$img    = rmk_header_image_tag( $post_id, $sizes, 'rmk-pagehead__img' );
		if ( $img ) {
			$done = true;
			return str_replace( $m[0], $m[0] . '<figure class="rmk-pagehead__media">' . $img . '</figure>', $content );
		}
	}
	return $content;
}, 11, 2 );

/* Deelbeeld: het standaard deelbeeld komt als eerste in de Open Graph-afbeeldingen, vóór het uitgelichte beeld. Yoast
   toont alleen het eerste beeld (og:image en twitter:image). */
add_filter( 'wpseo_add_opengraph_images', function ( $container ) {
	$id = function_exists( 'YoastSEO' ) ? (int) YoastSEO()->helpers->options->get( 'og_default_image_id' ) : 0;
	if ( $id && is_object( $container ) && method_exists( $container, 'add_image_by_id' ) ) {
		$container->add_image_by_id( $id );
	}
	return $container;
} );
add_filter( 'wpseo_twitter_image', function ( $url ) {
	$id = function_exists( 'YoastSEO' ) ? (int) YoastSEO()->helpers->options->get( 'og_default_image_id' ) : 0;
	return $id && ( $u = wp_get_attachment_url( $id ) ) ? $u : $url;
} );
// Yoast zet alle verzamelde beelden in og:image; alleen het eerste (het standaard deelbeeld) blijft staan.
add_filter( 'wpseo_frontend_presentation', function ( $presentation ) {
	if ( is_object( $presentation ) ) {
		try {
			$imgs = $presentation->open_graph_images;
			if ( is_array( $imgs ) && count( $imgs ) > 1 ) {
				$presentation->open_graph_images = array_slice( $imgs, 0, 1, true );
			}
		} catch ( Exception $e ) { // geen Open Graph voor dit type
		}
	}
	return $presentation;
} );
