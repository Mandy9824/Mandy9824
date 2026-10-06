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
 * - Deelbeeld: Yoast gebruikt het uitgelichte beeld per pagina als og:image.
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
