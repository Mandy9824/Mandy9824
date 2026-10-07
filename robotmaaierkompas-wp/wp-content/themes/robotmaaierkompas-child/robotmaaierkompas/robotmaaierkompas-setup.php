<?php
/**
 * robotmaaierkompas.nl — thema-integratie (v1.1)
 * Plaats deze map als /wp-content/themes/<child-thema>/robotmaaierkompas/
 * en voeg in functions.php toe:  require_once get_stylesheet_directory() . '/robotmaaierkompas/robotmaaierkompas-setup.php';
 */

defined( 'ABSPATH' ) || exit;

define( 'RMK_DIR', __DIR__ );
define( 'RMK_URL', get_stylesheet_directory_uri() . '/robotmaaierkompas' );
define( 'RMK_VER', '1.3.4' );

/* ------------------------------------------------------------------------
 * 1. CSS en JS + configuratie voor rmk.js
 * --------------------------------------------------------------------- */
add_action( 'wp_enqueue_scripts', function () {
	// Snelheid (LCP): tokens.css en rmk.css worden verkleind inline in de <head> gezet in plaats van als twee
	// render-blokkerende bestanden (lab, mobiel: LCP pagina 12 van 2,6 naar 1,2 s). Uitzetten: filter rmk_inline_css.
	if ( apply_filters( 'rmk_inline_css', true ) && ( $css = rmk_inline_css() ) ) {
		wp_register_style( 'rmk', false, array(), RMK_VER );
		wp_enqueue_style( 'rmk' );
		wp_add_inline_style( 'rmk', $css );
	} else {
		wp_enqueue_style( 'rmk-tokens', RMK_URL . '/tokens.css', array(), RMK_VER );
		wp_enqueue_style( 'rmk', RMK_URL . '/rmk.css', array( 'rmk-tokens' ), RMK_VER );
		wp_enqueue_style( 'rmk-afwerking', RMK_URL . '/css/rmk-afwerking.css', array( 'rmk' ), RMK_VER );
		wp_enqueue_style( 'rmk-specificatiekaart', RMK_URL . '/css/rmk-specificatiekaart.css', array( 'rmk-afwerking' ), RMK_VER );
	}
	wp_enqueue_script( 'rmk', RMK_URL . '/rmk.js', array(), RMK_VER, array( 'strategy' => 'defer', 'in_footer' => true ) );
	$config = apply_filters( 'rmk_config', array(
		// Modelbestand voor de kostencalculator. Zie data/modellen.voorbeeld.json voor de opbouw.
		'modelsUrl'  => RMK_URL . '/data/modellen.json',
		// Betrouwbaarheid telt pas mee vanaf dit aantal gelezen reviews.
		'minReviews' => 50,
	) );
	wp_add_inline_script( 'rmk', 'window.rmkConfig=' . wp_json_encode( $config ) . ';', 'before' );
} );

/** Verkleinde inhoud van tokens.css + rmk.css + css/rmk-afwerking.css (afwerkpakket v1.2), gecachet per themaversie en bestandsdatum. */
function rmk_inline_css_files() {
	return array( 'tokens.css', 'rmk.css', 'css/rmk-afwerking.css', 'css/rmk-specificatiekaart.css' );
}
function rmk_inline_css() {
	$files = rmk_inline_css_files();
	$key   = 'rmk_css_' . md5( RMK_VER . implode( '', array_map( function ( $f ) { return is_readable( RMK_DIR . '/' . $f ) ? filemtime( RMK_DIR . '/' . $f ) : 0; }, $files ) ) );
	$css   = get_transient( $key );
	if ( false === $css ) {
		$css = '';
		foreach ( $files as $f ) {
			$c = is_readable( RMK_DIR . '/' . $f ) ? (string) file_get_contents( RMK_DIR . '/' . $f ) : '';
			$c = preg_replace( '#/\*.*?\*/#s', '', $c );
			// url(...) (ook ingebedde SVG-iconen) onaangetast laten tijdens het verkleinen.
			$urls = array();
			$c    = preg_replace_callback( '#url\((?:"[^"]*"|\'[^\']*\'|[^)]*)\)#', function ( $u ) use ( &$urls ) {
				$urls[] = $u[0];
				return '__RMKURL' . ( count( $urls ) - 1 ) . '__';
			}, $c );
			$c = preg_replace( '/\s+/', ' ', $c );
			$c = preg_replace( '/\s*([{};,])\s*/', '$1', $c ); // geen spaties rond ":" of ">" weghalen (selectors)
			$c = str_replace( ';}', '}', trim( $c ) );
			$c = preg_replace_callback( '#__RMKURL(\d+)__#', function ( $u ) use ( $urls ) { return $urls[ (int) $u[1] ]; }, $c );
			// url(...) is relatief aan het CSS-bestand; inline wordt dat relatief aan de pagina. Daarom de map van het bestand ervoor.
			$dir = trim( dirname( $f ), '.' );
			$base = RMK_URL . '/' . ( $dir ? $dir . '/' : '' );
			$css .= preg_replace( '#url\((?![\'"]?(?:data:|https?:|/))([\'"]?)#', 'url($1' . $base, $c );
		}
		set_transient( $key, $css, WEEK_IN_SECONDS );
	}
	return $css;
}

add_action( 'after_setup_theme', function () {
	add_theme_support( 'editor-styles' );
	add_editor_style( array( 'robotmaaierkompas/tokens.css', 'robotmaaierkompas/rmk.css', 'robotmaaierkompas/css/rmk-afwerking.css', 'robotmaaierkompas/css/rmk-specificatiekaart.css' ) );
} );

/* ------------------------------------------------------------------------
 * 1b. Favicon (afwerkpakket). Het sitepictogram (Instellingen > Algemeen, favicon-512.png) blijft ingesteld voor
 *     WordPress en Yoast, maar de <link>-tags komen van hier: SVG, PNG 32 en apple-touch-icon. Yoast zet geen favicon.
 * --------------------------------------------------------------------- */
remove_action( 'wp_head', 'wp_site_icon', 99 );
add_action( 'wp_head', function () {
	echo '<link rel="icon" href="' . esc_url( RMK_URL . '/logo/favicon.svg' ) . '" type="image/svg+xml">' . "\n";
	echo '<link rel="icon" href="' . esc_url( RMK_URL . '/logo/favicon-32.png' ) . '" sizes="32x32">' . "\n";
	echo '<link rel="apple-touch-icon" href="' . esc_url( RMK_URL . '/logo/apple-touch-icon-180.png' ) . '">' . "\n";
}, 2 );

/* Logo als bestand (afwerkpakket): elk <a class="rmk-logo"> in header en footer krijgt het logobestand, ook in
 * template-onderdelen die in de site-editor zijn aangepast. Header: licht (donkere tekst), footer: donker. */
function rmk_logo_html( $variant ) {
	$file = 'donker' === $variant ? 'logo-horizontaal-donker.svg' : 'logo-horizontaal-licht.svg';
	$lazy = 'donker' === $variant ? ' loading="lazy" decoding="async"' : ''; // footerlogo staat onder de vouw
	return '<a class="rmk-logo" href="/" aria-label="robotmaaierkompas.nl, naar de homepage"><img src="' . esc_url( RMK_URL . '/logo/' . $file ) . '" alt="" width="344" height="44"' . $lazy . '></a>';
}
function rmk_replace_logo( $html ) {
	if ( false === strpos( (string) $html, 'class="rmk-logo"' ) ) {
		return $html;
	}
	$variant = false !== strpos( $html, 'rmk-footer' ) ? 'donker' : 'licht';
	return preg_replace_callback( '#<a class="rmk-logo"[^>]*>.*?</a>#s', function () use ( $variant ) {
		return rmk_logo_html( $variant );
	}, $html );
}
add_filter( 'render_block', function ( $content, $block ) {
	return 'core/html' === $block['blockName'] ? rmk_replace_logo( $content ) : $content;
}, 14, 2 );

add_filter( 'body_class', function ( $classes ) {
	$classes[] = 'rmk';
	return $classes;
} );

/* ------------------------------------------------------------------------
 * 2. Fonts zelf hosten (WOFF2 in /fonts)
 * --------------------------------------------------------------------- */
add_action( 'wp_head', function () {
	$f = RMK_URL . '/fonts/';
	echo '<link rel="preload" href="' . esc_url( $f . 'atkinson-hyperlegible-400.woff2' ) . '" as="font" type="font/woff2" crossorigin>' . "\n";
	// 1.3.1: de paginakop (h1, LCP-element op homepage en kernpagina's) staat in Schibsted Grotesk; die ook vooraf laden.
	echo '<link rel="preload" href="' . esc_url( $f . 'schibsted-grotesk-var.woff2' ) . '" as="font" type="font/woff2" crossorigin>' . "\n";
	echo '<style>
@font-face{font-family:"Atkinson Hyperlegible";src:url(' . esc_url( $f . 'atkinson-hyperlegible-400.woff2' ) . ') format("woff2");font-weight:400;font-display:swap}
@font-face{font-family:"Atkinson Hyperlegible";src:url(' . esc_url( $f . 'atkinson-hyperlegible-700.woff2' ) . ') format("woff2");font-weight:700;font-display:swap}
@font-face{font-family:"Schibsted Grotesk";src:url(' . esc_url( $f . 'schibsted-grotesk-var.woff2' ) . ') format("woff2");font-weight:400 900;font-display:swap}
</style>' . "\n";
}, 1 );

/* ------------------------------------------------------------------------
 * 3. Patrooncategorieën + loader
 * --------------------------------------------------------------------- */
add_action( 'init', function () {
	register_block_pattern_category( 'robotmaaierkompas', array( 'label' => 'Robotmaaierkompas – componenten' ) );
	register_block_pattern_category( 'robotmaaierkompas-paginas', array( 'label' => 'Robotmaaierkompas – pagina\'s' ) );

	if ( file_exists( get_stylesheet_directory() . '/patterns/scoreblok.php' ) ) {
		return; // Patronen staan in <thema>/patterns: WordPress laadt ze zelf.
	}
	foreach ( glob( RMK_DIR . '/patterns/*.php' ) as $file ) {
		$head = get_file_data( $file, array( 'title' => 'Title', 'slug' => 'Slug', 'cats' => 'Categories', 'desc' => 'Description', 'types' => 'Block Types', 'post' => 'Post Types' ) );
		if ( empty( $head['slug'] ) ) {
			continue;
		}
		ob_start();
		include $file;
		$content = ob_get_clean();
		register_block_pattern( $head['slug'], array_filter( array(
			'title'       => $head['title'],
			'description' => $head['desc'],
			'categories'  => array_map( 'trim', explode( ',', $head['cats'] ) ),
			'blockTypes'  => $head['types'] ? array_map( 'trim', explode( ',', $head['types'] ) ) : null,
			'postTypes'   => $head['post'] ? array_map( 'trim', explode( ',', $head['post'] ) ) : null,
			'content'     => $content,
		) ) );
	}
} );

/* ------------------------------------------------------------------------
 * 4. Publicatiecontrole: niet publiceren zolang er placeholders of
 *    voorbeelddata in staan ("[", "Alfa", "Beta", "gepeild").
 * --------------------------------------------------------------------- */
function rmk_checked_post_types() {
	return apply_filters( 'rmk_checked_post_types', array( 'post', 'page' ) );
}

/** Geeft de gevonden markeringen terug (lege array = in orde). */
function rmk_find_markers( $content ) {
	if ( function_exists( 'do_blocks' ) && has_blocks( $content ) ) {
		$content .= "\n" . do_blocks( $content ); // ook ingevoegde patronen en dynamische blokken meenemen
	}
	$text = preg_replace( '/<!--.*?-->/s', '', (string) $content ); // blokcommentaar bevat JSON met haken
	$text = strip_shortcodes( $text );                                  // geregistreerde shortcodes zijn geen placeholder
	$found = array();
	if ( false !== strpos( $text, '[' ) ) {
		$found[] = '[';
	}
	if ( preg_match( '/\bAlfa\b/u', $text ) ) {
		$found[] = 'Alfa';
	}
	if ( preg_match( '/\bBeta\b/u', $text ) ) {
		$found[] = 'Beta';
	}
	if ( false !== stripos( $text, 'gepeild' ) ) {
		$found[] = 'gepeild';
	}
	return apply_filters( 'rmk_found_markers', $found, $content );
}

function rmk_marker_message( $found ) {
	return sprintf(
		'Publiceren geblokkeerd: de inhoud bevat nog %s. Vul alle placeholders tussen [haken] in en verwijder voorbeelddata. Opslaan als concept kan wel.',
		implode( ', ', array_map( function ( $m ) { return '"' . $m . '"'; }, $found ) )
	);
}

/* Blokeditor (REST): duidelijke foutmelding in plaats van stil terugzetten. */
add_action( 'init', function () {
	foreach ( rmk_checked_post_types() as $type ) {
		add_filter( "rest_pre_insert_{$type}", function ( $prepared, $request ) {
			$id      = isset( $prepared->ID ) ? (int) $prepared->ID : 0;
			$status  = isset( $prepared->post_status ) ? $prepared->post_status : ( $id ? get_post_status( $id ) : 'draft' );
			$content = isset( $prepared->post_content ) ? $prepared->post_content : ( $id ? get_post_field( 'post_content', $id ) : '' );
			if ( in_array( $status, array( 'publish', 'future' ), true ) ) {
				$found = rmk_find_markers( $content );
				if ( $found ) {
					return new WP_Error( 'rmk_placeholders', rmk_marker_message( $found ), array( 'status' => 400 ) );
				}
			}
			return $prepared;
		}, 10, 2 );
	}
}, 20 );

/* Klassieke editor, snelle bewerking, importscripts: terugzetten naar concept + melding. */
add_filter( 'wp_insert_post_data', function ( $data ) {
	if ( in_array( $data['post_type'], rmk_checked_post_types(), true ) && in_array( $data['post_status'], array( 'publish', 'future' ), true ) ) {
		$found = rmk_find_markers( wp_unslash( $data['post_content'] ) );
		if ( $found ) {
			$data['post_status'] = 'draft';
			set_transient( 'rmk_blocked_' . get_current_user_id(), $found, 120 );
		}
	}
	return $data;
}, 99 );

add_action( 'admin_notices', function () {
	$key   = 'rmk_blocked_' . get_current_user_id();
	$found = get_transient( $key );
	if ( $found ) {
		delete_transient( $key );
		echo '<div class="notice notice-error"><p>' . esc_html( rmk_marker_message( $found ) ) . ' De pagina is als concept opgeslagen.</p></div>';
	}
} );

/* ------------------------------------------------------------------------
 * 5. Affiliate-links: rel="sponsored nofollow" op alle affiliate-domeinen
 *    en op het eigen redirectpad /ga/. Bestaande rel-waarden blijven behouden.
 * --------------------------------------------------------------------- */
function rmk_affiliate_domains() {
	// Voeg hier de domeinen van je andere partnerprogramma's toe (zonder www).
	// Subdomeinen tellen automatisch mee: 'bol.com' dekt ook partner.bol.com.
	return apply_filters( 'rmk_affiliate_domains', array(
		'bol.com',       // Bol-partnerprogramma (partner.bol.com valt eronder)
		'coolblue.nl',   // Coolblue (via Awin of Partnerize, zie BLAUWDRUK hoofdstuk 21)
		'coolblue.be',
		'amazon.nl',     // Amazon PartnerNet
		'amzn.to',       // verkorte Amazon-partnerlinks
		'awin1.com',     // Awin-trackinglinks
		'zenaps.com',    // Awin-trackinglinks (tweede domein)
		'ds1.nl',        // Daisycon-trackinglinks; controleer in je Daisycon-account welk trackingdomein je links gebruiken
		// Merkprogramma's later toevoegen, bijvoorbeeld 'robotmaaiers.nl' (Daisycon-campagne) of een merkdomein.
	) );
}

function rmk_is_affiliate_url( $href ) {
	$href = trim( html_entity_decode( (string) $href ) );
	if ( preg_match( '#^/ga(/|$|\?)#i', $href ) ) {
		return true; // relatief redirectpad
	}
	$parts = wp_parse_url( $href );
	if ( empty( $parts['host'] ) ) {
		return false;
	}
	$host = strtolower( preg_replace( '/^www\./i', '', $parts['host'] ) );
	$site = strtolower( preg_replace( '/^www\./i', '', (string) wp_parse_url( home_url(), PHP_URL_HOST ) ) );
	if ( $host === $site ) {
		return isset( $parts['path'] ) && preg_match( '#^/ga(/|$)#i', $parts['path'] );
	}
	foreach ( rmk_affiliate_domains() as $domain ) {
		$domain = strtolower( ltrim( $domain, '.' ) );
		if ( $host === $domain || substr( $host, -strlen( '.' . $domain ) ) === '.' . $domain ) {
			return true;
		}
	}
	return false;
}

function rmk_add_affiliate_rel( $html ) {
	if ( false === stripos( (string) $html, '<a' ) || ! class_exists( 'WP_HTML_Tag_Processor' ) ) {
		return $html;
	}
	$p = new WP_HTML_Tag_Processor( $html );
	while ( $p->next_tag( 'a' ) ) {
		$href = $p->get_attribute( 'href' );
		// Winkelknoppen uit inc/prijzen.php zijn gewone links naar de productpagina, geen affiliatelinks.
		if ( null !== $p->get_attribute( 'data-rmk-direct' ) && ! preg_match( '#^/ga(/|$|\?)#i', (string) $href ) ) {
			continue;
		}
		if ( ! is_string( $href ) || ! rmk_is_affiliate_url( $href ) ) {
			continue;
		}
		$rel = preg_split( '/\s+/', strtolower( trim( (string) $p->get_attribute( 'rel' ) ) ), -1, PREG_SPLIT_NO_EMPTY );
		$rel = array_unique( array_merge( $rel, array( 'sponsored', 'nofollow' ) ) );
		if ( '_blank' === $p->get_attribute( 'target' ) ) {
			$rel[] = 'noopener';
		}
		$p->set_attribute( 'rel', implode( ' ', array_unique( $rel ) ) );
	}
	return $p->get_updated_html();
}
add_filter( 'the_content', 'rmk_add_affiliate_rel', 20 );
add_filter( 'render_block', 'rmk_add_affiliate_rel', 20 ); // ook header, footer en andere template-onderdelen
add_filter( 'widget_text', 'rmk_add_affiliate_rel', 20 );
