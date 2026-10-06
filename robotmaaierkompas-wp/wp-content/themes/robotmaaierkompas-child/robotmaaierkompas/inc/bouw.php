<?php
/**
 * robotmaaierkompas.nl — bouwhulpmiddelen (alleen voor beheerders)
 *
 * Gereedschap > Robotmaaierkompas in wp-admin, of via WP-CLI:
 *   wp rmk status                     controles van stap 0 (indexering, permalinks, HTTPS, fonts, data, cron)
 *   wp rmk paginas --user=<auteur>    paginastructuur als concepten (data/paginas.json); overschrijft niets
 *   wp rmk seo                        Yoast SEO instellen
 * Er wordt nooit iets gepubliceerd.
 */

defined( 'ABSPATH' ) || exit;

function rmk_pattern_content( $slug ) {
	$p = WP_Block_Patterns_Registry::get_instance()->get_registered( 'robotmaaierkompas/' . $slug );
	return $p ? $p['content'] : null;
}

function rmk_crumbs( $items ) {
	$h = '<nav class="rmk-crumbs" aria-label="Kruimelpad" style="padding-top: 16px"><ol><li><a href="/">Home</a></li>';
	foreach ( $items as $i => $it ) {
		$h .= $i === count( $items ) - 1 ? '<li aria-current="page">' . esc_html( $it[0] ) . '</li>' : '<li><a href="' . esc_attr( $it[1] ) . '">' . esc_html( $it[0] ) . '</a></li>';
	}
	return $h . '</ol></nav>';
}

function rmk_simple_page( $crumbs, $eyebrow, $title, $body ) {
	return '<!-- wp:group {"tagName":"main","anchor":"inhoud","className":"rmk","layout":{"type":"default"}} -->' . "\n"
		. '<main class="wp-block-group rmk" id="inhoud">' . "\n<!-- wp:html -->\n"
		. '<div class="rmk-container" style="padding-bottom: 64px">' . rmk_crumbs( $crumbs )
		. '<header class="rmk-pagehead" style="max-width: 48rem"><p class="rmk-eyebrow">' . esc_html( $eyebrow ) . '</p><h1>' . esc_html( $title ) . '</h1></header>'
		. '<div class="rmk-prose" style="max-width: 48rem">' . $body . '</div></div>'
		. "\n<!-- /wp:html -->\n</main>\n<!-- /wp:group -->";
}

/** Invulvelden per juridische pagina (geen tekst bedacht: alleen wat er moet staan). */
function rmk_legal_body( $kind ) {
	switch ( $kind ) {
		case 'contact':
			return '<h2 style="margin-top: 0">Contact</h2><p>E-mail: [e-mailadres]</p><p>[Optioneel: contactformulier. Kies eerst een formulierplugin en noem die in de privacyverklaring.]</p>'
				. '<p>Een fout gezien? Zie <a href="/redactiebeleid/#correcties">Redactiebeleid en correcties</a>.</p>';
		case 'colofon':
			return '<h2 style="margin-top: 0">Colofon</h2><p>Naam: [naam of handelsnaam]</p><p>Adres: [adres of postadres]</p><p>E-mail: [e-mailadres]</p>'
				. '<p>[Alleen invullen als je het hebt: btw-nummer.]</p><p>Auteur en redactie: <a href="/over-ons/mandy-van-den-broek/">[naam auteur]</a></p>';
		case 'affiliate':
			return '<h2 style="margin-top: 0">Zo verdienen we geld</h2><p>[Uitleg affiliatelinks: welke winkels en netwerken, dat je niets extra betaalt, dat de score en de volgorde niet veranderen door commissie.]</p>'
				. '<h2>Welke programma\'s</h2><p>[Lijst van partnerprogramma\'s waarbij je bent aangesloten, pas invullen na goedkeuring.]</p>'
				. '<h2>Prijzen</h2><p>[Uitleg dat we voorlopig geen winkelprijzen tonen; bij elk model staat "Bekijk de prijs bij de winkel".]</p>';
		case 'cookies':
			return '<h2 style="margin-top: 0">Welke cookies</h2><div class="rmk-tablewrap"><table class="rmk-table"><thead><tr><th scope="col">Naam</th><th scope="col">Doel</th><th scope="col">Bewaartermijn</th><th scope="col">Toestemming nodig</th></tr></thead><tbody>'
				. '<tr><th scope="row">rmk_consent</th><td>[doel: bewaart je cookiekeuze]</td><td>[termijn]</td><td>[ja/nee]</td></tr>'
				. '<tr><th scope="row">[statistieken]</th><td>[doel]</td><td>[termijn]</td><td>[ja/nee]</td></tr>'
				. '<tr><th scope="row">[affiliate-cookies van winkels]</th><td>[doel]</td><td>[termijn]</td><td>[ja/nee]</td></tr>'
				. '</tbody></table></div><p><a href="#cookie-instellingen">Cookie-instellingen wijzigen</a></p>';
		case 'redactiebeleid':
			return '<h2 style="margin-top: 0">Hoe we werken</h2><p>[Hoe pagina\'s tot stand komen: specificaties, reviews, scoremodel; we testen niet zelf.]</p>'
				. '<h2>Hoe vaak we bijwerken</h2><p>[Hoe vaak pagina\'s, scores en prijzen worden bijgewerkt.]</p>'
				. '<h2 id="correcties">Correcties</h2><p>[Hoe je een fout meldt: e-mail [e-mailadres], met model en bron. Hoe en waar we wijzigingen vermelden.]</p>';
	}
	return '';
}


/**
 * Maakt alle pagina's uit data/paginas.json aan als concept. Bestaande pagina's (zelfde pad) blijven ongemoeid.
 * @return array{aangemaakt:int, log:string[]}
 */
function rmk_build_pages( $author_id ) {
	$list = json_decode( (string) file_get_contents( RMK_DIR . '/data/paginas.json' ), true );
	$log  = array();
	if ( ! $list || ! $author_id ) {
		return array( 'aangemaakt' => 0, 'log' => array( 'FOUT: paginas.json niet leesbaar of geen auteur.' ) );
	}
	$ids     = array();
	$created = 0;
	foreach ( $list['paginas'] as $p ) {
		$parent_id = 0;
		$path      = $p['slug'];
		if ( ! empty( $p['ouder'] ) ) {
			$parent_id = isset( $ids[ $p['ouder'] ] ) ? $ids[ $p['ouder'] ] : 0;
			$path      = $p['ouder'] . '/' . $p['slug'];
		}
		$existing = get_page_by_path( $path, OBJECT, 'page' );
		if ( $existing ) {
			$ids[ $p['slug'] ] = $existing->ID;
			$log[] = "bestaat al: /$path/ (#{$existing->ID}, {$existing->post_status})";
			continue;
		}

		$kind = isset( $p['inhoud'] ) ? $p['inhoud'] : '';
		if ( 'overzicht' === $kind ) {
			$content = rmk_simple_page( array( array( $p['titel'], '' ) ), 'Overzicht', $p['titel'], '<p>[Overzichtspagina: korte inleiding en links naar de pagina\'s in deze sectie.]</p>' );
		} elseif ( 'over-ons' === $kind ) {
			$content = rmk_simple_page( array( array( 'Over ons', '' ) ), 'Over ons', 'Over ons',
				'<p>[Wie zit erachter, sinds wanneer en waarom deze site. Eerlijke werkwijze: we testen robotmaaiers niet zelf, we vergelijken specificaties met een openbaar scoremodel en lezen gebruikersreviews.]</p>'
				. '<p>Hoe de scores tot stand komen staat op <a href="/hoe-we-beoordelen/">Hoe we beoordelen</a>. Auteur: <a href="/over-ons/mandy-van-den-broek/">[naam auteur]</a>.</p>' )
				. "\n" . '<!-- wp:pattern {"slug":"robotmaaierkompas/auteursblok"} /-->';
		} else {
			$content = rmk_pattern_content( $p['patroon'] );
			if ( null === $content ) {
				$log[] = "FOUT /$path/: patroon {$p['patroon']} niet gevonden";
				continue;
			}
			if ( 'pagina-juridisch' === $p['patroon'] ) {
				$content = str_replace( '[Titel juridische pagina]', $p['titel'], $content );
				if ( $kind ) {
					$content = preg_replace( '#(<article class="rmk-split__main rmk-prose">).*?(</article>)#s', '$1' . str_replace( '$', '\$', rmk_legal_body( $kind ) ) . '$2', $content, 1 );
				}
			}
		}

		$id = wp_insert_post( array(
			'post_type'    => 'page',
			'post_status'  => 'draft',
			'post_title'   => $p['titel'],
			'post_author'  => $author_id,
			'post_name'    => $p['slug'],
			'post_parent'  => $parent_id,
			'post_content' => wp_slash( $content ),
			'meta_input'   => array( 'rmk_pagina_soort' => $p['soort'] ),
		), true );
		if ( is_wp_error( $id ) ) {
			$log[] = "FOUT /$path/: " . $id->get_error_message();
			continue;
		}
		$ids[ $p['slug'] ] = $id;
		$created++;
		$log[] = "concept: /$path/ (#$id, {$p['soort']})";
		if ( ! empty( $p['voorpagina'] ) ) {
			update_option( 'show_on_front', 'page' );
			update_option( 'page_on_front', $id );
		}
	}
	return array( 'aangemaakt' => $created, 'log' => $log );
}

/** Yoast SEO-instellingen (BLAUWDRUK hoofdstuk 2, 10 en 11). */
/** @param int $person_user_id Gebruiker die Yoast als Persoon (eigenaar van de site) gebruikt. */
function rmk_configure_seo( $person_user_id = 0 ) {
	if ( ! class_exists( 'WPSEO_Options' ) ) {
		return new WP_Error( 'rmk_yoast', 'Yoast SEO is niet actief.' );
	}
	$titles = array(
		'separator'                    => 'sc-dash',
		'title-home-wpseo'             => '%%sitename%% %%sep%% %%sitedesc%%',
		'title-page'                   => '%%title%% %%page%% %%sep%% %%sitename%%',
		'title-post'                   => '%%title%% %%page%% %%sep%% %%sitename%%',
		'metadesc-page'                => '',
		'metadesc-post'                => '',
		'noindex-tax-post_tag'         => true,
		'noindex-tax-post_format'      => true,
		'disable-post_format'          => true,
		'noindex-author-wpseo'         => true,
		'disable-author'               => true,
		'noindex-archive-wpseo'        => true,
		'disable-date'                 => true,
		'noindex-attachment'           => true,
		'disable-attachment'           => true,
		'breadcrumbs-enable'           => true,
		'breadcrumbs-home'             => 'Home',
		'breadcrumbs-sep'              => '›',
		'breadcrumbs-display-blog-page'=> false,
		'schema-page-type-page'        => 'WebPage',
		'schema-article-type-page'     => 'Article',
		'schema-page-type-post'        => 'WebPage',
		'schema-article-type-post'     => 'Article',
		'company_or_person'            => 'person',
		'company_or_person_user_id'    => (int) ( $person_user_id ? $person_user_id : get_current_user_id() ),
		'website_name'                 => 'robotmaaierkompas.nl',
		'display-metabox-pt-attachment'=> false,
	);
	foreach ( $titles as $k => $v ) {
		WPSEO_Options::set( $k, $v );
	}
	foreach ( array(
		'enable_xml_sitemap'      => true,
		'tracking'                => false,
		'enable_enhanced_slack_sharing' => false,
		'remove_shortlinks'       => true,
		'remove_rest_api_links'   => false,
		'remove_rsd_wlw_links'    => true,
		'remove_oembed_links'     => false,
		'remove_generator'        => true,
		'remove_emoji_scripts'    => true,
		'remove_feed_global_comments' => true,
		'remove_feed_post_comments'   => true,
		'search_cleanup'          => true,
		'deny_search_crawling'    => true,
	) as $k => $v ) {
		if ( null !== WPSEO_Options::get( $k, null ) ) {
			WPSEO_Options::set( $k, $v );
		}
	}
	// Sitemap: alleen pagina's (er is geen blog). Berichten blijven bestaan maar komen niet in de sitemap zolang ze er niet zijn.
	WPSEO_Options::set( 'noindex-post', false );
	WPSEO_Options::set( 'noindex-page', false );

	// Reacties staan uit: geen blog, geen reacties (minder spam en minder persoonsgegevens).
	update_option( 'default_comment_status', 'closed' );
	update_option( 'default_ping_status', 'closed' );

	return true;
}

/** Controles voor stap 0 en de techniek. */
function rmk_status_checks() {
	$c    = array();
	$add  = function ( $ok, $label, $info = '' ) use ( &$c ) {
		$c[] = array( 'ok' => $ok, 'label' => $label, 'info' => $info );
	};
	$add( '0' === (string) get_option( 'blog_public' ), 'Zoekmachines niet laten indexeren staat aan', 'Pas op de lanceerdatum bewust uitzetten.' );
	$add( '/%postname%/' === get_option( 'permalink_structure' ), 'Permalinks op berichtnaam', (string) get_option( 'permalink_structure' ) );
	$add( 0 === strpos( home_url(), 'https://' ) && 0 === strpos( site_url(), 'https://' ), 'Site- en WordPress-adres gebruiken HTTPS', home_url() );
	$add( is_ssl() || ( defined( 'WP_CLI' ) && WP_CLI ), 'Deze verbinding is HTTPS', is_ssl() ? 'ja' : ( defined( 'WP_CLI' ) && WP_CLI ? 'via WP-CLI niet te zien' : 'nee' ) );
	$sample = get_posts( array( 'post_type' => array( 'post', 'page' ), 'post_status' => 'any', 'name' => 'hello-world', 'numberposts' => 1 ) ) ?: get_posts( array( 'post_type' => 'page', 'post_status' => 'any', 'name' => 'sample-page', 'numberposts' => 1 ) );
	$add( ! $sample, 'Standaardvoorbeeldpagina\'s verwijderd', $sample ? 'nog aanwezig: ' . $sample[0]->post_name : '' );
	$fonts = array( 'atkinson-hyperlegible-400.woff2', 'atkinson-hyperlegible-700.woff2', 'schibsted-grotesk-var.woff2' );
	$miss  = array_filter( $fonts, function ( $f ) { return ! is_readable( RMK_DIR . '/fonts/' . $f ); } );
	$add( ! $miss, 'Lettertypen zelf gehost (WOFF2)', $miss ? 'ontbreekt: ' . implode( ', ', $miss ) : '' );
	$data = rmk_models_data();
	$saved = get_option( 'rmk_modellen' );
	$add( ! empty( $data['modellen'] ), 'Modelbestand aanwezig', ( $saved ? 'via de API opgeslagen op ' . wp_date( 'j-n-Y H:i', $saved['opgeslagen'] ) : 'uit het thema' ) . ( isset( $data['gegenereerd'] ) ? ', gegenereerd ' . $data['gegenereerd'] . ', ' . count( $data['modellen'] ) . ' modellen' : '' ) );
	$pub = (int) wp_count_posts( 'page' )->publish + (int) wp_count_posts( 'post' )->publish;
	$add( 0 === $pub, 'Niets gepubliceerd', $pub . ' gepubliceerd' );
	$next = wp_next_scheduled( RMK_BOL_HOOK );
	$add( ! rmk_bol_enabled() && ! $next, 'Prijstaak uitgeschakeld (voorlopig geen Bol-gegevens)', rmk_bol_enabled() ? 'STAAT AAN' : ( $next ? 'nog ingepland' : 'uit' ) );
	$links = array_filter( (array) get_option( RMK_LINKS_OPTION, array() ) );
	$add( ! $links, 'Geen affiliatelinks ingesteld', $links ? count( $links ) . ' winkels met links' : '' );
	// Lees via Yoast's eigen helper (zoals de schema-uitvoer); WPSEO_Options::get gaf live een verouderde waarde.
	$yo     = function ( $k ) {
		return function_exists( 'YoastSEO' ) ? YoastSEO()->helpers->options->get( $k ) : ( class_exists( 'WPSEO_Options' ) ? WPSEO_Options::get( $k ) : null );
	};
	$person = (int) $yo( 'company_or_person_user_id' );
	$add( 'person' === $yo( 'company_or_person' ) && $person, 'Yoast: site vertegenwoordigt een persoon', $person ? get_the_author_meta( 'display_name', $person ) : '' );
	$add( class_exists( 'WPSEO_Options' ), 'Yoast SEO actief', defined( 'WPSEO_VERSION' ) ? WPSEO_VERSION : '' );
	$add( wp_image_editor_supports( array( 'mime_type' => 'image/webp' ) ), 'Server kan WebP maken' );
	$icon = (int) get_option( 'site_icon' );
	$add( $icon > 0, 'Sitepictogram ingesteld (favicon-512.png)', $icon ? (string) wp_get_attachment_url( $icon ) : 'Gereedschap > Robotmaaierkompas > Huisstijl toepassen' );
	$og = (string) $yo( 'og_default_image' );
	$add( '' !== $og, 'Yoast: standaard deelafbeelding (og:image)', $og ? $og : 'Gereedschap > Robotmaaierkompas > Huisstijl toepassen' );
	return $c;
}

/* ------------------------------------------------------------------ wp-admin */
add_action( 'admin_menu', function () {
	add_management_page( 'Robotmaaierkompas', 'Robotmaaierkompas', 'manage_options', 'rmk-bouw', 'rmk_admin_page' );
} );

function rmk_admin_page() {
	if ( ! current_user_can( 'manage_options' ) ) {
		return;
	}
	$result = null;
	if ( isset( $_POST['rmk_actie'] ) && check_admin_referer( 'rmk_bouw' ) ) {
		$actie = sanitize_key( $_POST['rmk_actie'] );
		if ( 'paginas' === $actie ) {
			$r      = rmk_build_pages( get_current_user_id() );
			$result = $r['aangemaakt'] . " concepten aangemaakt.\n" . implode( "\n", $r['log'] );
		} elseif ( 'seo' === $actie ) {
			$r      = rmk_configure_seo( get_current_user_id() );
			$result = is_wp_error( $r ) ? $r->get_error_message() : 'Yoast SEO ingesteld.';
		} elseif ( 'huisstijl' === $actie ) {
			$r      = rmk_apply_huisstijl();
			$result = is_wp_error( $r ) ? $r->get_error_message() : "Sitepictogram en standaard deelafbeelding ingesteld.\n" . $r['og_default_image'];
		}
	}
	echo '<div class="wrap"><h1>Robotmaaierkompas: bouw en controle</h1>';
	if ( $result ) {
		echo '<div class="notice notice-info"><pre style="white-space:pre-wrap">' . esc_html( $result ) . '</pre></div>';
	}
	echo '<h2>Controles</h2><table class="widefat striped" style="max-width:60rem"><tbody>';
	foreach ( rmk_status_checks() as $c ) {
		echo '<tr><td style="width:2rem">' . ( $c['ok'] ? '✅' : '⚠️' ) . '</td><td>' . esc_html( $c['label'] ) . '</td><td>' . esc_html( $c['info'] ) . '</td></tr>';
	}
	echo '</tbody></table><h2>Acties</h2><form method="post">';
	wp_nonce_field( 'rmk_bouw' );
	echo '<p><button class="button button-primary" name="rmk_actie" value="paginas">Paginastructuur als concepten aanmaken</button> <span class="description">Jij wordt de auteur. Bestaande pagina\'s blijven ongemoeid. Er wordt niets gepubliceerd.</span></p>';
	echo '<p><button class="button" name="rmk_actie" value="seo">Yoast SEO instellen</button></p>';
	echo '<p><button class="button" name="rmk_actie" value="huisstijl">Huisstijl toepassen</button> <span class="description">Sitepictogram (favicon-512.png) en de standaard deelafbeelding in Yoast (deelafbeelding-1200x630.png).</span></p></form></div>';
}

/* ------------------------------------------------------------------ REST (beheerders, ook met een toepassingswachtwoord)
 * GET  /wp-json/rmk/v1/status
 * POST /wp-json/rmk/v1/noindex   zet "Zoekmachines niet laten indexeren" AAN (kan het niet uitzetten)
 * POST /wp-json/rmk/v1/paginas   paginastructuur als concepten (huidige gebruiker is auteur)
 * POST /wp-json/rmk/v1/seo       Yoast instellen; persoon = huidige gebruiker
 * POST /wp-json/rmk/v1/huisstijl sitepictogram en standaard og:image (afwerkpakket)
 * Er is bewust geen route om te publiceren of de indexering uit te zetten. */
add_action( 'rest_api_init', function () {
	$admin = function () {
		return current_user_can( 'manage_options' );
	};
	register_rest_route( 'rmk/v1', '/status', array( 'methods' => 'GET', 'permission_callback' => $admin, 'callback' => function () {
		return rest_ensure_response( rmk_status_checks() );
	} ) );
	register_rest_route( 'rmk/v1', '/noindex', array( 'methods' => 'POST', 'permission_callback' => $admin, 'callback' => function () {
		update_option( 'blog_public', '0' );
		do_action( 'litespeed_purge_all' );
		return rest_ensure_response( array( 'blog_public' => get_option( 'blog_public' ) ) );
	} ) );
	register_rest_route( 'rmk/v1', '/paginas', array( 'methods' => 'POST', 'permission_callback' => $admin, 'callback' => function () {
		$r = rmk_build_pages( get_current_user_id() );
		$privacy = get_page_by_path( 'privacy', OBJECT, 'page' );
		if ( $privacy ) {
			update_option( 'wp_page_for_privacy_policy', $privacy->ID );
		}
		return rest_ensure_response( $r );
	} ) );
	register_rest_route( 'rmk/v1', '/seo', array( 'methods' => 'POST', 'permission_callback' => $admin, 'callback' => function () {
		$r = rmk_configure_seo( get_current_user_id() );
		return is_wp_error( $r ) ? $r : rest_ensure_response( array( 'ok' => true ) );
	} ) );
} );

/**
 * Huisstijl (afwerkpakket): sitepictogram = favicon-512.png en de standaard og:image in Yoast = deelafbeelding-1200x630.png.
 * Beide worden als bijlage in de mediabibliotheek gezet (één keer; daarna hergebruikt) vanuit de themamap.
 */
function rmk_media_from_theme( $rel, $title ) {
	$found = get_posts( array( 'post_type' => 'attachment', 'post_status' => 'inherit', 'meta_key' => 'rmk_bron', 'meta_value' => $rel, 'numberposts' => 1, 'fields' => 'ids' ) );
	if ( $found ) {
		return (int) $found[0];
	}
	require_once ABSPATH . 'wp-admin/includes/file.php';
	require_once ABSPATH . 'wp-admin/includes/media.php';
	require_once ABSPATH . 'wp-admin/includes/image.php';
	$tmp = wp_tempnam( basename( $rel ) );
	if ( ! $tmp || ! copy( RMK_DIR . '/' . $rel, $tmp ) ) {
		return new WP_Error( 'rmk_media', 'Kan ' . $rel . ' niet kopiëren.' );
	}
	// Als PNG bewaren (geen omzetting naar WebP): og:image en het sitepictogram werken zo overal.
	$keep = function () { return array(); };
	add_filter( 'image_editor_output_format', $keep, PHP_INT_MAX );
	$id = media_handle_sideload( array( 'name' => basename( $rel ), 'tmp_name' => $tmp ), 0, $title );
	remove_filter( 'image_editor_output_format', $keep, PHP_INT_MAX );
	if ( is_wp_error( $id ) ) {
		return $id;
	}
	update_post_meta( $id, 'rmk_bron', $rel );
	update_post_meta( $id, '_wp_attachment_image_alt', '' );
	return (int) $id;
}

function rmk_apply_huisstijl() {
	$icon = rmk_media_from_theme( 'logo/favicon-512.png', 'robotmaaierkompas sitepictogram' );
	if ( is_wp_error( $icon ) ) {
		return $icon;
	}
	update_option( 'site_icon', $icon );
	$og = rmk_media_from_theme( 'deelafbeelding/deelafbeelding-1200x630.png', 'robotmaaierkompas deelafbeelding' );
	if ( is_wp_error( $og ) ) {
		return $og;
	}
	$url = wp_get_attachment_url( $og );
	if ( function_exists( 'YoastSEO' ) ) {
		YoastSEO()->helpers->options->set( 'og_default_image', $url );
		YoastSEO()->helpers->options->set( 'og_default_image_id', $og );
	} elseif ( class_exists( 'WPSEO_Options' ) ) {
		WPSEO_Options::set( 'og_default_image', $url );
		WPSEO_Options::set( 'og_default_image_id', $og );
	} else {
		return new WP_Error( 'rmk_yoast', 'Yoast SEO is niet actief.' );
	}
	return array( 'site_icon' => $icon, 'og_default_image' => $url, 'og_default_image_id' => $og );
}

add_action( 'rest_api_init', function () {
	register_rest_route( 'rmk/v1', '/huisstijl', array( 'methods' => 'POST', 'permission_callback' => function () { return current_user_can( 'manage_options' ); }, 'callback' => function () {
		$r = rmk_apply_huisstijl();
		return is_wp_error( $r ) ? $r : rest_ensure_response( $r );
	} ) );
} );

/* ------------------------------------------------------------------ WP-CLI */
if ( defined( 'WP_CLI' ) && WP_CLI ) {
	WP_CLI::add_command( 'rmk status', function () {
		foreach ( rmk_status_checks() as $c ) {
			WP_CLI::log( ( $c['ok'] ? '[ok]   ' : '[let op] ' ) . $c['label'] . ( $c['info'] ? ' — ' . $c['info'] : '' ) );
		}
	} );
	WP_CLI::add_command( 'rmk paginas', function () {
		if ( ! get_current_user_id() ) {
			WP_CLI::error( 'Geef de auteur mee: --user=<gebruikersnaam>.' );
		}
		$r = rmk_build_pages( get_current_user_id() );
		foreach ( $r['log'] as $l ) {
			WP_CLI::log( $l );
		}
		WP_CLI::success( $r['aangemaakt'] . ' concepten aangemaakt.' );
	} );
	WP_CLI::add_command( 'rmk seo', function () {
		$r = rmk_configure_seo( get_current_user_id() );
		is_wp_error( $r ) ? WP_CLI::error( $r->get_error_message() ) : WP_CLI::success( 'Yoast SEO ingesteld.' );
	} );
}
