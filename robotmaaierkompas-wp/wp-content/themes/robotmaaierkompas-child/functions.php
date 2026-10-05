<?php
/**
 * Robotmaaierkompas child theme.
 */
defined( 'ABSPATH' ) || exit;

require_once get_stylesheet_directory() . '/robotmaaierkompas/robotmaaierkompas-setup.php';
require_once get_stylesheet_directory() . '/robotmaaierkompas/inc/data.php';
require_once get_stylesheet_directory() . '/robotmaaierkompas/inc/score.php';
require_once get_stylesheet_directory() . '/robotmaaierkompas/inc/prijzen-bol.php';
require_once get_stylesheet_directory() . '/robotmaaierkompas/inc/affiliate-redirect.php';
require_once get_stylesheet_directory() . '/robotmaaierkompas/inc/techniek.php';
require_once get_stylesheet_directory() . '/robotmaaierkompas/inc/bouw.php';
require_once get_stylesheet_directory() . '/robotmaaierkompas/inc/auteur.php';

/* Geen stijlen van het hoofdthema laden die we niet gebruiken (fonts van Twenty Twenty-Five). */
add_action( 'wp_enqueue_scripts', function () {
	wp_dequeue_style( 'twentytwentyfive-style' );
}, 20 );
