<?php
/**
 * Bewaking van de Bol-prijstaak (1.3.8).
 *
 * Is de laatste geslaagde Bol-ronde ouder dan acht uur, dan krijgt de beheerder (admin_email) één e-mail via wp_mail,
 * met de tijd van de laatste ronde en de laatste fout. Eén e-mail per storing: de storing is voorbij zodra er weer een
 * ronde slaagt; een volgende storing geeft weer één e-mail. Geen sleutels, tokens of site-ID in de e-mail.
 *
 * Geslaagd = niet gestopt (geen tokenfout) en voor minstens één model een antwoord van bol.com (ok, geen aanbod of
 * ongeldig). Raakt de Bol-logica in inc/bol.php niet aan: leest alleen het rondelog en luistert naar rmk_bol_na_ronde.
 *
 * Controle: elk uur via een eigen taak, en (omdat juist de cron kan stilliggen) hooguit één keer per uur aan het einde
 * van een verzoek dat WordPress bereikt. Zonder de drie Bol-constanten doet dit bestand niets.
 */
defined( 'ABSPATH' ) || exit;

const RMK_BOL_BEWAKING_HOOK     = 'rmk_bol_bewaking';
const RMK_BOL_GESLAAGD_OPTION   = 'rmk_bol_laatst_geslaagd';   // start van de laatste geslaagde ronde
const RMK_BOL_STORING_OPTION    = 'rmk_bol_storing_gemeld';    // welke storing al gemeld is
const RMK_BOL_BEWAKING_VOLGENDE = 'rmk_bol_bewaking_volgende'; // vroegste tijd voor de volgende controle
const RMK_BOL_STORING_GRENS     = 8 * HOUR_IN_SECONDS;

/** Is deze ronde geslaagd? */
function rmk_bol_ronde_geslaagd( $log ) {
	return is_array( $log ) && empty( $log['gestopt'] ) && ! empty( $log['eind'] )
		&& (int) ( $log['ok'] ?? 0 ) + (int) ( $log['geen_aanbod'] ?? 0 ) + (int) ( $log['ongeldig'] ?? 0 ) > 0;
}

/* Na elke ronde: een geslaagde ronde bewaren (het rondelog houdt maar 20 rondes). */
add_action( 'rmk_bol_na_ronde', function ( $log ) {
	if ( rmk_bol_ronde_geslaagd( $log ) ) {
		update_option( RMK_BOL_GESLAAGD_OPTION, (int) $log['start'], false );
	}
} );

/** Start van de laatste geslaagde ronde, 0 als er nog geen is. */
function rmk_bol_laatst_geslaagd() {
	$t = (int) get_option( RMK_BOL_GESLAAGD_OPTION, 0 );
	foreach ( (array) get_option( RMK_BOL_LOG_OPTION, array() ) as $log ) {
		if ( rmk_bol_ronde_geslaagd( $log ) ) {
			return max( $t, (int) $log['start'] );
		}
	}
	return $t;
}

/** Tekst zonder de waarden van de Bol-constanten en zonder tokens. */
function rmk_bol_zonder_secrets( $tekst ) {
	$tekst = (string) $tekst;
	foreach ( array( 'RMK_BOL_CLIENT_ID', 'RMK_BOL_CLIENT_SECRET', 'RMK_BOL_SITE_ID' ) as $c ) {
		$v = defined( $c ) ? trim( (string) constant( $c ) ) : '';
		if ( strlen( $v ) >= 4 ) {
			$tekst = str_replace( $v, '…', $tekst );
		}
	}
	return preg_replace( '/(Bearer|Basic|access_token"?\s*[:=]\s*"?)\s*[A-Za-z0-9._~+\/=-]{8,}/i', '$1 …', $tekst );
}

/** De laatste fout uit het rondelog (nieuwste eerst, tot en met de laatste geslaagde ronde): de melding van een ronde,
 * of anders de eerste fout bij een model. */
function rmk_bol_laatste_fout( array $hist ) {
	foreach ( $hist as $log ) {
		$wanneer = wp_date( 'j-n-Y H:i', (int) ( $log['start'] ?? 0 ) );
		if ( ! empty( $log['melding'] ) ) {
			return $wanneer . ': ' . $log['melding'];
		}
		foreach ( (array) ( $log['modellen'] ?? array() ) as $id => $u ) {
			if ( 0 === strpos( (string) $u, 'fout' ) ) {
				return $wanneer . ', ' . $id . ': ' . $u;
			}
		}
		if ( rmk_bol_ronde_geslaagd( $log ) ) {
			break; // oudere fouten horen niet bij deze storing
		}
	}
	return 'geen fout sinds de laatste geslaagde ronde (draait de taak wel?)';
}

/**
 * De controle. Geeft terug wat er gebeurde: uit, ok, al_gemeld, gemeld of mail_mislukt.
 */
function rmk_bol_bewaking() {
	if ( ! rmk_bol_geconfigureerd() ) {
		return array( 'status' => 'uit' );
	}
	$nu       = rmk_bol_nu();
	$hist     = (array) get_option( RMK_BOL_LOG_OPTION, array() );
	$geslaagd = rmk_bol_laatst_geslaagd();
	// Nog nooit geslaagd: tellen vanaf de oudste ronde in het log. Zonder log is er nog niets te melden.
	$oudste = $hist ? end( $hist ) : null;
	$sinds  = $geslaagd ? $geslaagd : ( $oudste ? (int) $oudste['start'] : 0 );
	if ( ! $sinds || $nu - $sinds <= RMK_BOL_STORING_GRENS ) {
		if ( false !== get_option( RMK_BOL_STORING_OPTION, false ) ) {
			delete_option( RMK_BOL_STORING_OPTION ); // storing voorbij
		}
		return array( 'status' => 'ok', 'laatst_geslaagd' => $geslaagd );
	}
	// Eén storing = dezelfde laatste geslaagde ronde.
	$gemeld = get_option( RMK_BOL_STORING_OPTION, false );
	if ( is_array( $gemeld ) && (int) $gemeld['geslaagd'] === $geslaagd ) {
		return array( 'status' => 'al_gemeld', 'laatst_geslaagd' => $geslaagd );
	}
	$laatste = $hist ? $hist[0] : null;
	$next    = wp_next_scheduled( RMK_BOL_RONDE_HOOK );
	$uren    = (int) floor( ( $nu - $sinds ) / HOUR_IN_SECONDS );
	$regels  = array(
		$geslaagd
			? 'De laatste geslaagde Bol-ronde was op ' . wp_date( 'j-n-Y H:i', $geslaagd ) . ' (' . $uren . ' uur geleden).'
			: 'Er is nog geen geslaagde Bol-ronde (de oudste ronde in het log was ' . $uren . ' uur geleden).',
		'Laatste ronde: ' . ( $laatste ? wp_date( 'j-n-Y H:i', (int) $laatste['start'] ) . ( ! empty( $laatste['gestopt'] ) ? ' (gestopt)' : '' ) : 'geen' ) . '.',
		'Laatste fout: ' . rmk_bol_laatste_fout( $hist ),
		'Volgende geplande ronde: ' . ( $next ? wp_date( 'j-n-Y H:i', $next ) . ( $next < $nu - 15 * MINUTE_IN_SECONDS ? ' (al voorbij: de cron lijkt niet te draaien)' : '' ) : 'geen' ) . '.',
		'',
		'Zonder nieuwe ronde verdwijnt een Bol-prijs 12 uur na het ophalen vanzelf van de site; de knop naar bol.com blijft.',
		'Controleer het statusoverzicht in wp-admin (Gereedschap > Robotmaaierkompas), de cron in hPanel (wp-cron.php elke 15 minuten) en /wp-json/rmk/v1/bol-status.',
		'Over deze storing krijg je geen nieuwe e-mail. Na de volgende geslaagde ronde is de storing voorbij.',
	);
	$onderwerp = '[Robotmaaierkompas] Bol-prijzen niet bijgewerkt sinds ' . ( $geslaagd ? wp_date( 'j-n H:i', $geslaagd ) : 'de start' );
	$ok        = wp_mail( get_option( 'admin_email' ), $onderwerp, rmk_bol_zonder_secrets( implode( "\n", $regels ) ) );
	if ( $ok ) {
		update_option( RMK_BOL_STORING_OPTION, array( 'geslaagd' => $geslaagd, 'gemeld' => $nu ), false );
	}
	return array( 'status' => $ok ? 'gemeld' : 'mail_mislukt', 'laatst_geslaagd' => $geslaagd );
}

/* Planning: elk uur, alleen met de Bol-constanten. */
add_action( 'init', function () {
	if ( ! rmk_bol_geconfigureerd() ) {
		if ( wp_next_scheduled( RMK_BOL_BEWAKING_HOOK ) ) {
			wp_clear_scheduled_hook( RMK_BOL_BEWAKING_HOOK );
		}
		return;
	}
	if ( ! wp_next_scheduled( RMK_BOL_BEWAKING_HOOK ) ) {
		wp_schedule_event( rmk_bol_nu() + 300, 'hourly', RMK_BOL_BEWAKING_HOOK );
	}
} );
add_action( RMK_BOL_BEWAKING_HOOK, 'rmk_bol_bewaking' );
add_action( 'switch_theme', function () {
	wp_clear_scheduled_hook( RMK_BOL_BEWAKING_HOOK );
} );

/* Reserve als de cron stilligt: hooguit één keer per uur, aan het einde van een verzoek (de optie wordt automatisch geladen). */
add_action( 'shutdown', function () {
	if ( ! rmk_bol_geconfigureerd() || (int) get_option( RMK_BOL_BEWAKING_VOLGENDE, 0 ) > rmk_bol_nu() ) {
		return;
	}
	update_option( RMK_BOL_BEWAKING_VOLGENDE, rmk_bol_nu() + HOUR_IN_SECONDS, true );
	rmk_bol_bewaking();
} );
