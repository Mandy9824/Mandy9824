<?php
/**
 * robotmaaierkompas.nl — auteur: "laatst nagekeken" en de automatische artikellijst
 *
 * - <time data-rmk-modified></time> (in het auteursblok) wordt bij het renderen gevuld met de datum
 *   van de laatste wijziging van de pagina waarop het blok staat.
 * - [rmk_artikelen_auteur] toont de gepubliceerde pagina's en berichten van de auteur van de huidige
 *   pagina (of auteur="<id>"), zonder de verplichte pagina's, sectiepagina's en de homepage.
 *   Geen gepubliceerde artikelen: er wordt niets getoond, ook geen kop.
 */

defined( 'ABSPATH' ) || exit;

add_filter( 'render_block', function ( $content, $block ) {
	if ( 'core/html' !== $block['blockName'] || false === strpos( $content, 'data-rmk-modified></time>' ) ) {
		return $content;
	}
	$id = get_the_ID() ? get_the_ID() : get_queried_object_id();
	if ( ! $id ) {
		return $content;
	}
	$time = '<time datetime="' . esc_attr( get_post_modified_time( 'Y-m-d', false, $id ) ) . '" data-rmk-modified>' . esc_html( get_the_modified_date( 'j F Y', $id ) ) . '</time>';
	return str_replace( '<time data-rmk-modified></time>', $time, $content );
}, 16, 2 );

add_shortcode( 'rmk_artikelen_auteur', function ( $atts ) {
	$a      = shortcode_atts( array( 'auteur' => 0 ), $atts );
	$author = (int) $a['auteur'] ? (int) $a['auteur'] : (int) get_post_field( 'post_author', get_the_ID() );
	if ( ! $author ) {
		return '';
	}
	$posts = get_posts( array(
		'post_type'      => array( 'page', 'post' ),
		'post_status'    => 'publish',
		'author'         => $author,
		'posts_per_page' => 50,
		'orderby'        => 'modified',
		'order'          => 'DESC',
		'post__not_in'   => array( get_the_ID(), (int) get_option( 'page_on_front' ) ),
		'meta_query'     => array(
			'relation' => 'OR',
			array( 'key' => 'rmk_pagina_soort', 'compare' => 'NOT EXISTS' ),
			array( 'key' => 'rmk_pagina_soort', 'value' => '^(verplicht|sectie|homepage)', 'compare' => 'NOT REGEXP' ),
		),
	) );
	if ( ! $posts ) {
		return '';
	}
	$name  = get_the_author_meta( 'display_name', $author );
	$cards = '';
	foreach ( $posts as $p ) {
		$cards .= '<a class="rmk-card" href="' . esc_url( get_permalink( $p ) ) . '"><span class="rmk-meta">Bijgewerkt op ' . esc_html( rmk_date_nl( get_post_modified_time( 'Y-m-d', false, $p ) ) ) . '</span><h3>' . esc_html( get_the_title( $p ) ) . '</h3></a>';
	}
	return '<section class="rmk-section" aria-labelledby="art" style="display: flex; flex-direction: column; gap: 16px"><h2 id="art" style="font-size: var(--rmk-fs-xl)">Artikelen van ' . esc_html( $name ) . '</h2><div class="rmk-grid rmk-grid--wide">' . $cards . '</div></section>';
} );

/**
 * [rmk_onlangs_bijgewerkt] (homepage): de drie laatst bijgewerkte gepubliceerde pagina's, zonder de homepage,
 * verplichte pagina's en sectiepagina's. Zijn er minder dan drie, dan wordt het blok niet getoond.
 */
add_shortcode( 'rmk_onlangs_bijgewerkt', function () {
	$posts = get_posts( array(
		'post_type'      => array( 'page', 'post' ),
		'post_status'    => 'publish',
		'posts_per_page' => 3,
		'orderby'        => 'modified',
		'order'          => 'DESC',
		'post__not_in'   => array_filter( array( (int) get_option( 'page_on_front' ), (int) get_the_ID() ) ),
		'meta_query'     => array(
			'relation' => 'OR',
			array( 'key' => 'rmk_pagina_soort', 'compare' => 'NOT EXISTS' ),
			array( 'key' => 'rmk_pagina_soort', 'value' => '^(verplicht|sectie|homepage)', 'compare' => 'NOT REGEXP' ),
		),
	) );
	if ( count( $posts ) < 3 ) {
		return '';
	}
	$cards = '';
	foreach ( $posts as $p ) {
		$cards .= '<a class="rmk-card" href="' . esc_url( get_permalink( $p ) ) . '"><span class="rmk-meta">Bijgewerkt op ' . esc_html( rmk_date_nl( get_post_modified_time( 'Y-m-d', false, $p ) ) ) . '</span><h3>' . esc_html( get_the_title( $p ) ) . '</h3><span class="rmk-card__more">Lezen</span></a>';
	}
	return '<section class="rmk-section" aria-labelledby="onlangs"><div class="rmk-container rmk-column"><div class="rmk-section-head"><h2 id="onlangs">Onlangs bijgewerkt</h2></div><div class="rmk-grid">' . $cards . '</div></div></section>';
} );
