"""Traductions des pages PRODUIT — tarifs, comparatif, crédits.

Rappel du fonctionnement (détails dans pages_i18n.py) : **la clef est le texte
français rendu**, nombres remplacés par `{0}`, `{1}`… Le nombre rencontré sur la
page est réinjecté dans la traduction, ce qui permet de changer un tarif ou un
quota sans décrocher les sept langues.

Trois règles suivies partout ici :

  • « Qeerah », « Qeerah Pro », « Feed Radar », « TikTok », « Stripe » et
    « Agency » ne se traduisent pas — ce sont des noms.
  • La mention fiscale française devient une phrase compréhensible hors de
    France, sans jamais prétendre autre chose que la réalité : le vendeur est
    une micro-entreprise française qui ne facture pas de TVA.
  • Les montants restent en euros. C'est ce qui est prélevé ; l'ordre de
    grandeur en devise locale est le sujet de la page d'accueil.

Le français n'est pas listé : il est la source. L'Irlande (`en-ie`) hérite de
l'anglais, comme sur l'accueil.
"""
from __future__ import annotations

# ═══════════════════════════════════════════════════════════════════════════
# /pricing
# ═══════════════════════════════════════════════════════════════════════════
T_PRICING: dict[str, dict[str, str]] = {
    "en": {
        "Tarifs — Qeerah": "Pricing — Qeerah",
        "Qeerah Pro — {0} € TTC/mois ou {1} € TTC/an. Accès à tout, sans engagement, annulation en {2} clic.":
            "Qeerah Pro — €{0}/month or €{1}/year, all taxes included. Everything unlocked, no commitment, cancel in {2} click.",
        "Qeerah Pro — {0} € TTC/mois ou {1} € TTC/an. Accès à toutes les fonctionnalités.":
            "Qeerah Pro — €{0}/month or €{1}/year, all taxes included. Every feature included.",
        "Détail des fonctionnalités": "Feature breakdown",
        "Crédits": "Credits",
        "Ouvrir l'app →": "Open the app →",
        "Une seule offre,": "One plan,",
        "tout est inclus": "everything included",
        "Pas de palier, pas de fonctionnalité verrouillée. Sans engagement, annulation en {0} clic.":
            "No tiers, no locked features. No commitment, cancel in {0} click.",
        "Mensuel": "Monthly",
        "Annuel": "Yearly",
        "−{0} %": "−{0}%",
        "par mois, TTC": "per month, tax included",
        "Soit {0} € sur un an.": "That's €{0} over a year.",
        "TVA non applicable, article {0} B du CGI.":
            "No VAT charged — French small-business exemption (art. {0} B, French tax code).",
        "{0} analyses de vidéos": "{0} video analyses",
        "par mois": "per month",
        "{0} crédits IA": "{0} AI credits",
        "par mois — environ {0} carrousels ({1} crédits chacun)":
            "per month — about {0} carousels ({1} credits each)",
        "Analyse approfondie": "In-depth analysis",
        "de chaque vidéo": "of every video",
        "Détection des": "Detection of",
        "CTA visuels et audio": "on-screen and spoken calls to action",
        "Analyse par": "Analysis by",
        "upload et par lien TikTok": "file upload and by TikTok link",
        "Analyse multi-liens": "Multi-link analysis",
        "et patterns récurrents": "and recurring patterns",
        "Coach IA": "AI coach",
        "et script personnalisé": "and a script written for you",
        "Données marché": "Market data",
        "et créateurs gagnants": "and winning creators",
        "et recherche de profil": "and profile search",
        "Studio d'accroches IA": "AI Hook Studio",
        "et Coach carrousel photo": "and Photo Carousel Coach",
        "Historique de tes analyses, sur tous tes appareils":
            "Your analysis history, on every device",
        "Résiliation à tout moment, en {0} clic": "Cancel any time, in {0} click",
        "S'abonner à Qeerah Pro →": "Subscribe to Qeerah Pro →",
        "Paiement sécurisé par Stripe · Activation immédiate":
            "Secure payment by Stripe · Instant activation",
        "Tu n'as pas encore de compte ?": "Don't have an account yet?",
        "{0} jours d'accès complet, sans carte bancaire — {1} analyses de vidéos et {2} essais sur chaque outil de création":
            "{0} days of full access, no card required — {1} video analyses and {2} free runs of every creative tool",
        "créer un compte gratuitement": "create a free account",
        "Voir le détail de toutes les fonctionnalités →": "See every feature in detail →",
        "️ Annulation à tout moment": "️ Cancel any time",
        "Paiement sécurisé (Stripe)": "Secure payment (Stripe)",
        "Activation immédiate": "Instant activation",
    },
    "pt-br": {
        "Tarifs — Qeerah": "Preços — Qeerah",
        "Qeerah Pro — {0} € TTC/mois ou {1} € TTC/an. Accès à tout, sans engagement, annulation en {2} clic.":
            "Qeerah Pro — € {0}/mês ou € {1}/ano, impostos incluídos. Tudo liberado, sem fidelidade, cancele em {2} clique.",
        "Qeerah Pro — {0} € TTC/mois ou {1} € TTC/an. Accès à toutes les fonctionnalités.":
            "Qeerah Pro — € {0}/mês ou € {1}/ano, impostos incluídos. Todos os recursos incluídos.",
        "Détail des fonctionnalités": "Todos os recursos",
        "Crédits": "Créditos",
        "Ouvrir l'app →": "Abrir o app →",
        "Une seule offre,": "Um único plano,",
        "tout est inclus": "tudo incluído",
        "Pas de palier, pas de fonctionnalité verrouillée. Sans engagement, annulation en {0} clic.":
            "Sem níveis, sem recurso bloqueado. Sem fidelidade, cancele em {0} clique.",
        "Mensuel": "Mensal",
        "Annuel": "Anual",
        "−{0} %": "−{0}%",
        "par mois, TTC": "por mês, impostos incluídos",
        "Soit {0} € sur un an.": "Dá € {0} no ano.",
        "TVA non applicable, article {0} B du CGI.":
            "Sem cobrança de IVA — isenção de microempresa francesa (art. {0} B do código tributário francês).",
        "{0} analyses de vidéos": "{0} análises de vídeo",
        "par mois": "por mês",
        "{0} crédits IA": "{0} créditos de IA",
        "par mois — environ {0} carrousels ({1} crédits chacun)":
            "por mês — cerca de {0} carrosséis ({1} créditos cada)",
        "Analyse approfondie": "Análise profunda",
        "de chaque vidéo": "de cada vídeo",
        "Détection des": "Detecção de",
        "CTA visuels et audio": "CTAs na tela e falados",
        "Analyse par": "Análise por",
        "upload et par lien TikTok": "upload de arquivo e por link do TikTok",
        "Analyse multi-liens": "Análise de vários links",
        "et patterns récurrents": "e padrões que se repetem",
        "Coach IA": "Coach de IA",
        "et script personnalisé": "e roteiro feito pra você",
        "Données marché": "Dados de mercado",
        "et créateurs gagnants": "e criadores que estão vendendo",
        "et recherche de profil": "e busca de perfil",
        "Studio d'accroches IA": "Estúdio de ganchos com IA",
        "et Coach carrousel photo": "e Coach de carrossel de fotos",
        "Historique de tes analyses, sur tous tes appareils":
            "Seu histórico de análises, em todos os aparelhos",
        "Résiliation à tout moment, en {0} clic": "Cancele quando quiser, em {0} clique",
        "S'abonner à Qeerah Pro →": "Assinar o Qeerah Pro →",
        "Paiement sécurisé par Stripe · Activation immédiate":
            "Pagamento seguro via Stripe · Ativação na hora",
        "Tu n'as pas encore de compte ?": "Ainda não tem conta?",
        "{0} jours d'accès complet, sans carte bancaire — {1} analyses de vidéos et {2} essais sur chaque outil de création":
            "{0} dias de acesso completo, sem cartão — {1} análises de vídeo e {2} usos grátis de cada ferramenta de criação",
        "créer un compte gratuitement": "criar uma conta grátis",
        "Voir le détail de toutes les fonctionnalités →": "Ver todos os recursos em detalhe →",
        "️ Annulation à tout moment": "️ Cancele quando quiser",
        "Paiement sécurisé (Stripe)": "Pagamento seguro (Stripe)",
        "Activation immédiate": "Ativação na hora",
    },
    "es": {
        "Tarifs — Qeerah": "Precios — Qeerah",
        "Qeerah Pro — {0} € TTC/mois ou {1} € TTC/an. Accès à tout, sans engagement, annulation en {2} clic.":
            "Qeerah Pro — {0} € al mes o {1} € al año, impuestos incluidos. Todo desbloqueado, sin permanencia, cancela en {2} clic.",
        "Qeerah Pro — {0} € TTC/mois ou {1} € TTC/an. Accès à toutes les fonctionnalités.":
            "Qeerah Pro — {0} € al mes o {1} € al año, impuestos incluidos. Todas las funciones incluidas.",
        "Détail des fonctionnalités": "Todas las funciones",
        "Crédits": "Créditos",
        "Ouvrir l'app →": "Abrir la app →",
        "Une seule offre,": "Un solo plan,",
        "tout est inclus": "todo incluido",
        "Pas de palier, pas de fonctionnalité verrouillée. Sans engagement, annulation en {0} clic.":
            "Sin niveles, sin funciones bloqueadas. Sin permanencia, cancela en {0} clic.",
        "Mensuel": "Mensual",
        "Annuel": "Anual",
        "−{0} %": "−{0} %",
        "par mois, TTC": "al mes, impuestos incluidos",
        "Soit {0} € sur un an.": "Son {0} € en un año.",
        "TVA non applicable, article {0} B du CGI.":
            "Sin IVA — exención de microempresa francesa (art. {0} B del código fiscal francés).",
        "{0} analyses de vidéos": "{0} análisis de vídeo",
        "par mois": "al mes",
        "{0} crédits IA": "{0} créditos de IA",
        "par mois — environ {0} carrousels ({1} crédits chacun)":
            "al mes — unos {0} carruseles ({1} créditos cada uno)",
        "Analyse approfondie": "Análisis a fondo",
        "de chaque vidéo": "de cada vídeo",
        "Détection des": "Detección de",
        "CTA visuels et audio": "CTA en pantalla y hablados",
        "Analyse par": "Análisis por",
        "upload et par lien TikTok": "subida de archivo y por enlace de TikTok",
        "Analyse multi-liens": "Análisis de varios enlaces",
        "et patterns récurrents": "y patrones que se repiten",
        "Coach IA": "Coach de IA",
        "et script personnalisé": "y guion hecho para ti",
        "Données marché": "Datos de mercado",
        "et créateurs gagnants": "y creadores que venden",
        "et recherche de profil": "y búsqueda de perfiles",
        "Studio d'accroches IA": "Estudio de ganchos con IA",
        "et Coach carrousel photo": "y Coach de carrusel de fotos",
        "Historique de tes analyses, sur tous tes appareils":
            "Tu historial de análisis, en todos tus dispositivos",
        "Résiliation à tout moment, en {0} clic": "Cancela cuando quieras, en {0} clic",
        "S'abonner à Qeerah Pro →": "Suscribirme a Qeerah Pro →",
        "Paiement sécurisé par Stripe · Activation immédiate":
            "Pago seguro con Stripe · Activación inmediata",
        "Tu n'as pas encore de compte ?": "¿Todavía no tienes cuenta?",
        "{0} jours d'accès complet, sans carte bancaire — {1} analyses de vidéos et {2} essais sur chaque outil de création":
            "{0} días de acceso completo, sin tarjeta — {1} análisis de vídeo y {2} usos gratis de cada herramienta de creación",
        "créer un compte gratuitement": "crear una cuenta gratis",
        "Voir le détail de toutes les fonctionnalités →": "Ver todas las funciones en detalle →",
        "️ Annulation à tout moment": "️ Cancela cuando quieras",
        "Paiement sécurisé (Stripe)": "Pago seguro (Stripe)",
        "Activation immédiate": "Activación inmediata",
    },
    "it": {
        "Tarifs — Qeerah": "Prezzi — Qeerah",
        "Qeerah Pro — {0} € TTC/mois ou {1} € TTC/an. Accès à tout, sans engagement, annulation en {2} clic.":
            "Qeerah Pro — {0} € al mese o {1} € all'anno, tasse incluse. Tutto sbloccato, senza vincoli, disdici in {2} clic.",
        "Qeerah Pro — {0} € TTC/mois ou {1} € TTC/an. Accès à toutes les fonctionnalités.":
            "Qeerah Pro — {0} € al mese o {1} € all'anno, tasse incluse. Tutte le funzioni incluse.",
        "Détail des fonctionnalités": "Tutte le funzioni",
        "Crédits": "Crediti",
        "Ouvrir l'app →": "Apri l'app →",
        "Une seule offre,": "Un solo piano,",
        "tout est inclus": "tutto incluso",
        "Pas de palier, pas de fonctionnalité verrouillée. Sans engagement, annulation en {0} clic.":
            "Niente livelli, niente funzioni bloccate. Senza vincoli, disdici in {0} clic.",
        "Mensuel": "Mensile",
        "Annuel": "Annuale",
        "−{0} %": "−{0}%",
        "par mois, TTC": "al mese, tasse incluse",
        "Soit {0} € sur un an.": "Fanno {0} € in un anno.",
        "TVA non applicable, article {0} B du CGI.":
            "Nessuna IVA applicata — esenzione per microimprese francesi (art. {0} B del codice fiscale francese).",
        "{0} analyses de vidéos": "{0} analisi di video",
        "par mois": "al mese",
        "{0} crédits IA": "{0} crediti IA",
        "par mois — environ {0} carrousels ({1} crédits chacun)":
            "al mese — circa {0} caroselli ({1} crediti ciascuno)",
        "Analyse approfondie": "Analisi approfondita",
        "de chaque vidéo": "di ogni video",
        "Détection des": "Rilevamento di",
        "CTA visuels et audio": "CTA a schermo e parlate",
        "Analyse par": "Analisi da",
        "upload et par lien TikTok": "file caricato e da link TikTok",
        "Analyse multi-liens": "Analisi di più link",
        "et patterns récurrents": "e schemi ricorrenti",
        "Coach IA": "Coach IA",
        "et script personnalisé": "e copione scritto per te",
        "Données marché": "Dati di mercato",
        "et créateurs gagnants": "e creator che vendono",
        "et recherche de profil": "e ricerca profili",
        "Studio d'accroches IA": "Studio di hook con IA",
        "et Coach carrousel photo": "e Coach carosello foto",
        "Historique de tes analyses, sur tous tes appareils":
            "Lo storico delle tue analisi, su tutti i tuoi dispositivi",
        "Résiliation à tout moment, en {0} clic": "Disdici quando vuoi, in {0} clic",
        "S'abonner à Qeerah Pro →": "Abbonati a Qeerah Pro →",
        "Paiement sécurisé par Stripe · Activation immédiate":
            "Pagamento sicuro con Stripe · Attivazione immediata",
        "Tu n'as pas encore de compte ?": "Non hai ancora un account?",
        "{0} jours d'accès complet, sans carte bancaire — {1} analyses de vidéos et {2} essais sur chaque outil de création":
            "{0} giorni di accesso completo, senza carta — {1} analisi di video e {2} prove gratuite di ogni strumento creativo",
        "créer un compte gratuitement": "crea un account gratis",
        "Voir le détail de toutes les fonctionnalités →": "Vedi tutte le funzioni nel dettaglio →",
        "️ Annulation à tout moment": "️ Disdici quando vuoi",
        "Paiement sécurisé (Stripe)": "Pagamento sicuro (Stripe)",
        "Activation immédiate": "Attivazione immediata",
    },
    "de": {
        "Tarifs — Qeerah": "Preise — Qeerah",
        "Qeerah Pro — {0} € TTC/mois ou {1} € TTC/an. Accès à tout, sans engagement, annulation en {2} clic.":
            "Qeerah Pro — {0} € im Monat oder {1} € im Jahr, inkl. Steuern. Alles freigeschaltet, ohne Bindung, Kündigung mit {2} Klick.",
        "Qeerah Pro — {0} € TTC/mois ou {1} € TTC/an. Accès à toutes les fonctionnalités.":
            "Qeerah Pro — {0} € im Monat oder {1} € im Jahr, inkl. Steuern. Alle Funktionen enthalten.",
        "Détail des fonctionnalités": "Alle Funktionen",
        "Crédits": "Guthaben",
        "Ouvrir l'app →": "App öffnen →",
        "Une seule offre,": "Ein einziges Angebot,",
        "tout est inclus": "alles ist dabei",
        "Pas de palier, pas de fonctionnalité verrouillée. Sans engagement, annulation en {0} clic.":
            "Keine Stufen, keine gesperrten Funktionen. Ohne Bindung, Kündigung mit {0} Klick.",
        "Mensuel": "Monatlich",
        "Annuel": "Jährlich",
        "−{0} %": "−{0} %",
        "par mois, TTC": "pro Monat, inkl. Steuern",
        "Soit {0} € sur un an.": "Macht {0} € im Jahr.",
        "TVA non applicable, article {0} B du CGI.":
            "Keine Mehrwertsteuer — französische Kleinunternehmerregelung (Art. {0} B, französisches Steuergesetzbuch).",
        "{0} analyses de vidéos": "{0} Videoanalysen",
        "par mois": "pro Monat",
        "{0} crédits IA": "{0} KI-Guthaben",
        "par mois — environ {0} carrousels ({1} crédits chacun)":
            "pro Monat — etwa {0} Karussells ({1} Guthaben pro Stück)",
        "Analyse approfondie": "Tiefe Analyse",
        "de chaque vidéo": "jedes Videos",
        "Détection des": "Erkennung von",
        "CTA visuels et audio": "Calls to Action im Bild und gesprochen",
        "Analyse par": "Analyse per",
        "upload et par lien TikTok": "Datei-Upload und per TikTok-Link",
        "Analyse multi-liens": "Analyse mehrerer Links",
        "et patterns récurrents": "und wiederkehrender Muster",
        "Coach IA": "KI-Coach",
        "et script personnalisé": "und ein Skript nur für dich",
        "Données marché": "Marktdaten",
        "et créateurs gagnants": "und Creators, die verkaufen",
        "et recherche de profil": "und Profilsuche",
        "Studio d'accroches IA": "KI-Hook-Studio",
        "et Coach carrousel photo": "und Fotokarussell-Coach",
        "Historique de tes analyses, sur tous tes appareils":
            "Dein Analyse-Verlauf, auf allen deinen Geräten",
        "Résiliation à tout moment, en {0} clic": "Jederzeit kündbar, mit {0} Klick",
        "S'abonner à Qeerah Pro →": "Qeerah Pro abonnieren →",
        "Paiement sécurisé par Stripe · Activation immédiate":
            "Sichere Zahlung über Stripe · Sofort aktiv",
        "Tu n'as pas encore de compte ?": "Noch kein Konto?",
        "{0} jours d'accès complet, sans carte bancaire — {1} analyses de vidéos et {2} essais sur chaque outil de création":
            "{0} Tage voller Zugang, ohne Kreditkarte — {1} Videoanalysen und {2} kostenlose Nutzungen jedes Kreativwerkzeugs",
        "créer un compte gratuitement": "kostenlos ein Konto erstellen",
        "Voir le détail de toutes les fonctionnalités →": "Alle Funktionen im Detail ansehen →",
        "️ Annulation à tout moment": "️ Jederzeit kündbar",
        "Paiement sécurisé (Stripe)": "Sichere Zahlung (Stripe)",
        "Activation immédiate": "Sofort aktiv",
    },
}


# ═══════════════════════════════════════════════════════════════════════════
# /pricing/compare
# Le tableau vit dans un <script data-i18n-js> : ses libellés sont traduits
# comme le reste, cf. pages_i18n.traduire_script.
# ═══════════════════════════════════════════════════════════════════════════
T_COMPARE: dict[str, dict[str, str]] = {
    "en": {
        "Détail des fonctionnalités — Qeerah": "Feature breakdown — Qeerah",
        "Tout ce qui est inclus dans Qeerah Pro, fonctionnalité par fonctionnalité. Et ce que couvre une offre Agency sur devis.":
            "Everything Qeerah Pro includes, feature by feature. And what a quoted Agency plan covers.",
        "Tout ce qui est inclus dans Qeerah Pro, fonctionnalité par fonctionnalité.":
            "Everything Qeerah Pro includes, feature by feature.",
        "Tarifs": "Pricing",
        "Crédits": "Credits",
        "Ouvrir l'app →": "Open the app →",
        "Tout ce qui est inclus": "Everything that's included",
        "Une offre unique, sans fonctionnalité verrouillée. Les besoins multi-comptes se traitent sur devis.":
            "A single plan, with no locked features. Multi-seat needs are handled by quote.",
        "Fonctionnalité": "Feature",
        "Notre offre": "Our plan",
        "TTC/mois": "per month, tax incl.",
        "ou {0} € TTC/an": "or €{0}/year, tax incl.",
        "Sur devis": "By quote",
        "S'abonner →": "Subscribe →",
        "Nous contacter": "Contact us",
        "Prix TTC. TVA non applicable, article {0} B du CGI. Sans engagement, résiliation à tout moment.":
            "Prices include tax. No VAT charged — French small-business exemption (art. {0} B). No commitment, cancel any time.",
        # Tableau
        "Analyse vidéo": "Video analysis",
        "Analyses de vidéos": "Video analyses",
        "Score détaillé sur {0}": "Detailed score out of {0}",
        "Analyse approfondie multi-dimensions": "In-depth, multi-dimension analysis",
        "Détection des CTA visuels et audio": "Detection of on-screen and spoken calls to action",
        "Analyse par upload de fichier": "Analysis by file upload",
        "Analyse par lien TikTok": "Analysis by TikTok link",
        "Analyse multi-liens et patterns": "Multi-link analysis and patterns",
        "Analyse en arrière-plan + e-mail": "Background analysis + email",
        "Historique sur tous tes appareils": "History on every device",
        "Coaching et création": "Coaching and creation",
        "Coach IA et script personnalisé": "AI coach and a script written for you",
        "Structures gagnantes détectées": "Winning structures, detected",
        "Studio d'accroches IA (prompts vidéo)": "AI Hook Studio (video prompts)",
        "Coach carrousel photo (carrousels)": "Photo Carousel Coach (carousels)",
        "Générateur de carrousels par IA": "AI carousel generator",
        "Données marché": "Market data",
        "Feed Radar (vidéos qui percent)": "Feed Radar (videos taking off)",
        "Recherche de profil TikTok": "TikTok profile search",
        "Créateurs gagnants et tendances": "Winning creators and trends",
        "Produits et vidéos recommandés": "Recommended products and videos",
        "Compte et facturation": "Account and billing",
        "Nombre d'utilisateurs": "Number of users",
        "Facture avec TVA et n° d'entreprise": "Invoice with VAT and company number",
        "Sans engagement": "No commitment",
        "Résiliation en {0} clic": "Cancel in {0} click",
        "Support": "Support",
        "Crédits IA (achat facultatif)": "AI credits (optional purchase)",
        "Packs de crédits pour les images IA": "Credit packs for AI images",
        "Sur mesure": "Tailored",
        "Plusieurs": "Several",
        "Selon contrat": "Per contract",
        "E-mail": "Email",
        "Dédié": "Dedicated",
        "En option": "Optional",
    },
    "pt-br": {
        "Détail des fonctionnalités — Qeerah": "Todos os recursos — Qeerah",
        "Tout ce qui est inclus dans Qeerah Pro, fonctionnalité par fonctionnalité. Et ce que couvre une offre Agency sur devis.":
            "Tudo o que o Qeerah Pro inclui, recurso por recurso. E o que cobre um plano Agency sob orçamento.",
        "Tout ce qui est inclus dans Qeerah Pro, fonctionnalité par fonctionnalité.":
            "Tudo o que o Qeerah Pro inclui, recurso por recurso.",
        "Tarifs": "Preços",
        "Crédits": "Créditos",
        "Ouvrir l'app →": "Abrir o app →",
        "Tout ce qui est inclus": "Tudo o que está incluído",
        "Une offre unique, sans fonctionnalité verrouillée. Les besoins multi-comptes se traitent sur devis.":
            "Um plano único, sem recurso bloqueado. Necessidades com várias contas são tratadas sob orçamento.",
        "Fonctionnalité": "Recurso",
        "Notre offre": "Nosso plano",
        "TTC/mois": "por mês, impostos incl.",
        "ou {0} € TTC/an": "ou € {0}/ano, impostos incl.",
        "Sur devis": "Sob orçamento",
        "S'abonner →": "Assinar →",
        "Nous contacter": "Fale com a gente",
        "Prix TTC. TVA non applicable, article {0} B du CGI. Sans engagement, résiliation à tout moment.":
            "Preços com impostos. Sem IVA — isenção de microempresa francesa (art. {0} B). Sem fidelidade, cancele quando quiser.",
        "Analyse vidéo": "Análise de vídeo",
        "Analyses de vidéos": "Análises de vídeo",
        "Score détaillé sur {0}": "Nota detalhada de {0}",
        "Analyse approfondie multi-dimensions": "Análise profunda em várias dimensões",
        "Détection des CTA visuels et audio": "Detecção de CTAs na tela e falados",
        "Analyse par upload de fichier": "Análise por upload de arquivo",
        "Analyse par lien TikTok": "Análise por link do TikTok",
        "Analyse multi-liens et patterns": "Análise de vários links e padrões",
        "Analyse en arrière-plan + e-mail": "Análise em segundo plano + e-mail",
        "Historique sur tous tes appareils": "Histórico em todos os aparelhos",
        "Coaching et création": "Coaching e criação",
        "Coach IA et script personnalisé": "Coach de IA e roteiro feito pra você",
        "Structures gagnantes détectées": "Estruturas vencedoras detectadas",
        "Studio d'accroches IA (prompts vidéo)": "Estúdio de ganchos com IA (prompts de vídeo)",
        "Coach carrousel photo (carrousels)": "Coach de carrossel de fotos (carrosséis)",
        "Générateur de carrousels par IA": "Gerador de carrosséis com IA",
        "Données marché": "Dados de mercado",
        "Feed Radar (vidéos qui percent)": "Feed Radar (vídeos que estão bombando)",
        "Recherche de profil TikTok": "Busca de perfil no TikTok",
        "Créateurs gagnants et tendances": "Criadores que vendem e tendências",
        "Produits et vidéos recommandés": "Produtos e vídeos recomendados",
        "Compte et facturation": "Conta e cobrança",
        "Nombre d'utilisateurs": "Número de usuários",
        "Facture avec TVA et n° d'entreprise": "Nota com impostos e CNPJ/registro",
        "Sans engagement": "Sem fidelidade",
        "Résiliation en {0} clic": "Cancelamento em {0} clique",
        "Support": "Suporte",
        "Crédits IA (achat facultatif)": "Créditos de IA (compra opcional)",
        "Packs de crédits pour les images IA": "Pacotes de créditos para imagens de IA",
        "Sur mesure": "Sob medida",
        "Plusieurs": "Vários",
        "Selon contrat": "Conforme contrato",
        "E-mail": "E-mail",
        "Dédié": "Dedicado",
        "En option": "Opcional",
    },
    "es": {
        "Détail des fonctionnalités — Qeerah": "Todas las funciones — Qeerah",
        "Tout ce qui est inclus dans Qeerah Pro, fonctionnalité par fonctionnalité. Et ce que couvre une offre Agency sur devis.":
            "Todo lo que incluye Qeerah Pro, función por función. Y lo que cubre un plan Agency con presupuesto.",
        "Tout ce qui est inclus dans Qeerah Pro, fonctionnalité par fonctionnalité.":
            "Todo lo que incluye Qeerah Pro, función por función.",
        "Tarifs": "Precios",
        "Crédits": "Créditos",
        "Ouvrir l'app →": "Abrir la app →",
        "Tout ce qui est inclus": "Todo lo que está incluido",
        "Une offre unique, sans fonctionnalité verrouillée. Les besoins multi-comptes se traitent sur devis.":
            "Un plan único, sin funciones bloqueadas. Las necesidades con varias cuentas se tratan con presupuesto.",
        "Fonctionnalité": "Función",
        "Notre offre": "Nuestro plan",
        "TTC/mois": "al mes, impuestos incl.",
        "ou {0} € TTC/an": "o {0} € al año, impuestos incl.",
        "Sur devis": "Con presupuesto",
        "S'abonner →": "Suscribirme →",
        "Nous contacter": "Contactar",
        "Prix TTC. TVA non applicable, article {0} B du CGI. Sans engagement, résiliation à tout moment.":
            "Precios con impuestos. Sin IVA — exención de microempresa francesa (art. {0} B). Sin permanencia, cancela cuando quieras.",
        "Analyse vidéo": "Análisis de vídeo",
        "Analyses de vidéos": "Análisis de vídeo",
        "Score détaillé sur {0}": "Puntuación detallada sobre {0}",
        "Analyse approfondie multi-dimensions": "Análisis a fondo en varias dimensiones",
        "Détection des CTA visuels et audio": "Detección de CTA en pantalla y hablados",
        "Analyse par upload de fichier": "Análisis por subida de archivo",
        "Analyse par lien TikTok": "Análisis por enlace de TikTok",
        "Analyse multi-liens et patterns": "Análisis de varios enlaces y patrones",
        "Analyse en arrière-plan + e-mail": "Análisis en segundo plano + correo",
        "Historique sur tous tes appareils": "Historial en todos tus dispositivos",
        "Coaching et création": "Coaching y creación",
        "Coach IA et script personnalisé": "Coach de IA y guion hecho para ti",
        "Structures gagnantes détectées": "Estructuras ganadoras detectadas",
        "Studio d'accroches IA (prompts vidéo)": "Estudio de ganchos con IA (prompts de vídeo)",
        "Coach carrousel photo (carrousels)": "Coach de carrusel de fotos (carruseles)",
        "Générateur de carrousels par IA": "Generador de carruseles con IA",
        "Données marché": "Datos de mercado",
        "Feed Radar (vidéos qui percent)": "Feed Radar (vídeos que despegan)",
        "Recherche de profil TikTok": "Búsqueda de perfiles de TikTok",
        "Créateurs gagnants et tendances": "Creadores que venden y tendencias",
        "Produits et vidéos recommandés": "Productos y vídeos recomendados",
        "Compte et facturation": "Cuenta y facturación",
        "Nombre d'utilisateurs": "Número de usuarios",
        "Facture avec TVA et n° d'entreprise": "Factura con IVA y número de empresa",
        "Sans engagement": "Sin permanencia",
        "Résiliation en {0} clic": "Cancelación en {0} clic",
        "Support": "Soporte",
        "Crédits IA (achat facultatif)": "Créditos de IA (compra opcional)",
        "Packs de crédits pour les images IA": "Packs de créditos para imágenes con IA",
        "Sur mesure": "A medida",
        "Plusieurs": "Varios",
        "Selon contrat": "Según contrato",
        "E-mail": "Correo",
        "Dédié": "Dedicado",
        "En option": "Opcional",
    },
    "it": {
        "Détail des fonctionnalités — Qeerah": "Tutte le funzioni — Qeerah",
        "Tout ce qui est inclus dans Qeerah Pro, fonctionnalité par fonctionnalité. Et ce que couvre une offre Agency sur devis.":
            "Tutto quello che c'è in Qeerah Pro, funzione per funzione. E cosa copre un piano Agency su preventivo.",
        "Tout ce qui est inclus dans Qeerah Pro, fonctionnalité par fonctionnalité.":
            "Tutto quello che c'è in Qeerah Pro, funzione per funzione.",
        "Tarifs": "Prezzi",
        "Crédits": "Crediti",
        "Ouvrir l'app →": "Apri l'app →",
        "Tout ce qui est inclus": "Tutto ciò che è incluso",
        "Une offre unique, sans fonctionnalité verrouillée. Les besoins multi-comptes se traitent sur devis.":
            "Un piano unico, senza funzioni bloccate. Le esigenze multi-account si trattano su preventivo.",
        "Fonctionnalité": "Funzione",
        "Notre offre": "Il nostro piano",
        "TTC/mois": "al mese, tasse incl.",
        "ou {0} € TTC/an": "o {0} € all'anno, tasse incl.",
        "Sur devis": "Su preventivo",
        "S'abonner →": "Abbonati →",
        "Nous contacter": "Contattaci",
        "Prix TTC. TVA non applicable, article {0} B du CGI. Sans engagement, résiliation à tout moment.":
            "Prezzi tasse incluse. Nessuna IVA — esenzione per microimprese francesi (art. {0} B). Senza vincoli, disdici quando vuoi.",
        "Analyse vidéo": "Analisi video",
        "Analyses de vidéos": "Analisi di video",
        "Score détaillé sur {0}": "Punteggio dettagliato su {0}",
        "Analyse approfondie multi-dimensions": "Analisi approfondita su più dimensioni",
        "Détection des CTA visuels et audio": "Rilevamento delle CTA a schermo e parlate",
        "Analyse par upload de fichier": "Analisi da file caricato",
        "Analyse par lien TikTok": "Analisi da link TikTok",
        "Analyse multi-liens et patterns": "Analisi di più link e schemi",
        "Analyse en arrière-plan + e-mail": "Analisi in background + email",
        "Historique sur tous tes appareils": "Storico su tutti i tuoi dispositivi",
        "Coaching et création": "Coaching e creazione",
        "Coach IA et script personnalisé": "Coach IA e copione scritto per te",
        "Structures gagnantes détectées": "Strutture vincenti rilevate",
        "Studio d'accroches IA (prompts vidéo)": "Studio di hook con IA (prompt video)",
        "Coach carrousel photo (carrousels)": "Coach carosello foto (caroselli)",
        "Générateur de carrousels par IA": "Generatore di caroselli con IA",
        "Données marché": "Dati di mercato",
        "Feed Radar (vidéos qui percent)": "Feed Radar (video che stanno esplodendo)",
        "Recherche de profil TikTok": "Ricerca profili TikTok",
        "Créateurs gagnants et tendances": "Creator che vendono e tendenze",
        "Produits et vidéos recommandés": "Prodotti e video consigliati",
        "Compte et facturation": "Account e fatturazione",
        "Nombre d'utilisateurs": "Numero di utenti",
        "Facture avec TVA et n° d'entreprise": "Fattura con IVA e partita IVA",
        "Sans engagement": "Senza vincoli",
        "Résiliation en {0} clic": "Disdetta in {0} clic",
        "Support": "Assistenza",
        "Crédits IA (achat facultatif)": "Crediti IA (acquisto facoltativo)",
        "Packs de crédits pour les images IA": "Pacchetti di crediti per le immagini IA",
        "Sur mesure": "Su misura",
        "Plusieurs": "Più di uno",
        "Selon contrat": "Secondo contratto",
        "E-mail": "Email",
        "Dédié": "Dedicata",
        "En option": "Opzionale",
    },
    "de": {
        "Détail des fonctionnalités — Qeerah": "Alle Funktionen — Qeerah",
        "Tout ce qui est inclus dans Qeerah Pro, fonctionnalité par fonctionnalité. Et ce que couvre une offre Agency sur devis.":
            "Alles, was in Qeerah Pro steckt, Funktion für Funktion. Und was ein Agency-Angebot auf Anfrage abdeckt.",
        "Tout ce qui est inclus dans Qeerah Pro, fonctionnalité par fonctionnalité.":
            "Alles, was in Qeerah Pro steckt, Funktion für Funktion.",
        "Tarifs": "Preise",
        "Crédits": "Guthaben",
        "Ouvrir l'app →": "App öffnen →",
        "Tout ce qui est inclus": "Alles, was dabei ist",
        "Une offre unique, sans fonctionnalité verrouillée. Les besoins multi-comptes se traitent sur devis.":
            "Ein einziges Angebot, ohne gesperrte Funktionen. Mehrere Konten regeln wir auf Anfrage.",
        "Fonctionnalité": "Funktion",
        "Notre offre": "Unser Angebot",
        "TTC/mois": "pro Monat, inkl. Steuern",
        "ou {0} € TTC/an": "oder {0} € im Jahr, inkl. Steuern",
        "Sur devis": "Auf Anfrage",
        "S'abonner →": "Abonnieren →",
        "Nous contacter": "Kontakt aufnehmen",
        "Prix TTC. TVA non applicable, article {0} B du CGI. Sans engagement, résiliation à tout moment.":
            "Preise inkl. Steuern. Keine Mehrwertsteuer — französische Kleinunternehmerregelung (Art. {0} B). Ohne Bindung, jederzeit kündbar.",
        "Analyse vidéo": "Videoanalyse",
        "Analyses de vidéos": "Videoanalysen",
        "Score détaillé sur {0}": "Detaillierte Wertung von {0}",
        "Analyse approfondie multi-dimensions": "Tiefe Analyse über mehrere Dimensionen",
        "Détection des CTA visuels et audio": "Erkennung von Calls to Action im Bild und gesprochen",
        "Analyse par upload de fichier": "Analyse per Datei-Upload",
        "Analyse par lien TikTok": "Analyse per TikTok-Link",
        "Analyse multi-liens et patterns": "Analyse mehrerer Links und Muster",
        "Analyse en arrière-plan + e-mail": "Analyse im Hintergrund + E-Mail",
        "Historique sur tous tes appareils": "Verlauf auf allen deinen Geräten",
        "Coaching et création": "Coaching und Erstellung",
        "Coach IA et script personnalisé": "KI-Coach und Skript nur für dich",
        "Structures gagnantes détectées": "Erkannte Erfolgsmuster",
        "Studio d'accroches IA (prompts vidéo)": "KI-Hook-Studio (Video-Prompts)",
        "Coach carrousel photo (carrousels)": "Fotokarussell-Coach (Karussells)",
        "Générateur de carrousels par IA": "Karussell-Generator mit KI",
        "Données marché": "Marktdaten",
        "Feed Radar (vidéos qui percent)": "Feed Radar (Videos, die durchstarten)",
        "Recherche de profil TikTok": "TikTok-Profilsuche",
        "Créateurs gagnants et tendances": "Creators, die verkaufen, und Trends",
        "Produits et vidéos recommandés": "Empfohlene Produkte und Videos",
        "Compte et facturation": "Konto und Abrechnung",
        "Nombre d'utilisateurs": "Zahl der Nutzer",
        "Facture avec TVA et n° d'entreprise": "Rechnung mit Steuer und Firmennummer",
        "Sans engagement": "Ohne Bindung",
        "Résiliation en {0} clic": "Kündigung mit {0} Klick",
        "Support": "Support",
        "Crédits IA (achat facultatif)": "KI-Guthaben (optional zukaufbar)",
        "Packs de crédits pour les images IA": "Guthabenpakete für KI-Bilder",
        "Sur mesure": "Maßgeschneidert",
        "Plusieurs": "Mehrere",
        "Selon contrat": "Laut Vertrag",
        "E-mail": "E-Mail",
        "Dédié": "Fest zugeteilt",
        "En option": "Optional",
    },
}


# ═══════════════════════════════════════════════════════════════════════════
# /credits
# ═══════════════════════════════════════════════════════════════════════════
T_CREDITS: dict[str, dict[str, str]] = {
    "en": {
        "Crédits — Qeerah": "Credits — Qeerah",
        "Recharge tes crédits Photo Slide & Studio d'accroches IA — packs dès {0} €.":
            "Top up your Photo Carousel Coach and AI Hook Studio credits — packs from €{0}.",
        "Tarifs": "Pricing",
        "Comparer": "Compare",
        "Ouvrir l'app →": "Open the app →",
        "Recharge tes crédits": "Top up your credits",
        "Crédits Photo Slide & Studio d'accroches IA · valables {0} mois · renouvelables à tout moment":
            "Photo Carousel Coach & AI Hook Studio credits · valid {0} month · top up any time",
        "Ton solde": "Your balance",
        "📅 Abonnement": "📅 Subscription",
        "🛒 Crédits achetés": "🛒 Credits bought",
        "Total disponible": "Total available",
        "Packs de crédits": "Credit packs",
        "⚠️ Validité {0} mois après achat · notification avant expiration. Les crédits d'abonnement se renouvellent chaque mois (non reportés).":
            "⚠️ Valid {0} month after purchase · you're warned before they expire. Subscription credits renew every month (they don't carry over).",
    },
    "pt-br": {
        "Crédits — Qeerah": "Créditos — Qeerah",
        "Recharge tes crédits Photo Slide & Studio d'accroches IA — packs dès {0} €.":
            "Recarregue seus créditos do Coach de carrossel e do Estúdio de ganchos com IA — pacotes a partir de € {0}.",
        "Tarifs": "Preços",
        "Comparer": "Comparar",
        "Ouvrir l'app →": "Abrir o app →",
        "Recharge tes crédits": "Recarregue seus créditos",
        "Crédits Photo Slide & Studio d'accroches IA · valables {0} mois · renouvelables à tout moment":
            "Créditos do Coach de carrossel e do Estúdio de ganchos com IA · válidos por {0} mês · recarregue quando quiser",
        "Ton solde": "Seu saldo",
        "📅 Abonnement": "📅 Assinatura",
        "🛒 Crédits achetés": "🛒 Créditos comprados",
        "Total disponible": "Total disponível",
        "Packs de crédits": "Pacotes de créditos",
        "⚠️ Validité {0} mois après achat · notification avant expiration. Les crédits d'abonnement se renouvellent chaque mois (non reportés).":
            "⚠️ Válidos por {0} mês após a compra · avisamos antes de expirar. Os créditos da assinatura renovam todo mês (não acumulam).",
    },
    "es": {
        "Crédits — Qeerah": "Créditos — Qeerah",
        "Recharge tes crédits Photo Slide & Studio d'accroches IA — packs dès {0} €.":
            "Recarga tus créditos del Coach de carrusel y del Estudio de ganchos con IA — packs desde {0} €.",
        "Tarifs": "Precios",
        "Comparer": "Comparar",
        "Ouvrir l'app →": "Abrir la app →",
        "Recharge tes crédits": "Recarga tus créditos",
        "Crédits Photo Slide & Studio d'accroches IA · valables {0} mois · renouvelables à tout moment":
            "Créditos del Coach de carrusel y del Estudio de ganchos con IA · válidos {0} mes · recarga cuando quieras",
        "Ton solde": "Tu saldo",
        "📅 Abonnement": "📅 Suscripción",
        "🛒 Crédits achetés": "🛒 Créditos comprados",
        "Total disponible": "Total disponible",
        "Packs de crédits": "Packs de créditos",
        "⚠️ Validité {0} mois après achat · notification avant expiration. Les crédits d'abonnement se renouvellent chaque mois (non reportés).":
            "⚠️ Válidos {0} mes desde la compra · te avisamos antes de que caduquen. Los créditos de la suscripción se renuevan cada mes (no se acumulan).",
    },
    "it": {
        "Crédits — Qeerah": "Crediti — Qeerah",
        "Recharge tes crédits Photo Slide & Studio d'accroches IA — packs dès {0} €.":
            "Ricarica i crediti del Coach carosello foto e dello Studio di hook con IA — pacchetti da {0} €.",
        "Tarifs": "Prezzi",
        "Comparer": "Confronta",
        "Ouvrir l'app →": "Apri l'app →",
        "Recharge tes crédits": "Ricarica i tuoi crediti",
        "Crédits Photo Slide & Studio d'accroches IA · valables {0} mois · renouvelables à tout moment":
            "Crediti Coach carosello foto e Studio di hook con IA · validi {0} mese · ricaricabili quando vuoi",
        "Ton solde": "Il tuo saldo",
        "📅 Abonnement": "📅 Abbonamento",
        "🛒 Crédits achetés": "🛒 Crediti acquistati",
        "Total disponible": "Totale disponibile",
        "Packs de crédits": "Pacchetti di crediti",
        "⚠️ Validité {0} mois après achat · notification avant expiration. Les crédits d'abonnement se renouvellent chaque mois (non reportés).":
            "⚠️ Validi {0} mese dall'acquisto · ti avvisiamo prima della scadenza. I crediti dell'abbonamento si rinnovano ogni mese (non si accumulano).",
    },
    "de": {
        "Crédits — Qeerah": "Guthaben — Qeerah",
        "Recharge tes crédits Photo Slide & Studio d'accroches IA — packs dès {0} €.":
            "Lade dein Guthaben für Fotokarussell-Coach und KI-Hook-Studio auf — Pakete ab {0} €.",
        "Tarifs": "Preise",
        "Comparer": "Vergleichen",
        "Ouvrir l'app →": "App öffnen →",
        "Recharge tes crédits": "Guthaben aufladen",
        "Crédits Photo Slide & Studio d'accroches IA · valables {0} mois · renouvelables à tout moment":
            "Guthaben für Fotokarussell-Coach und KI-Hook-Studio · {0} Monat gültig · jederzeit aufladbar",
        "Ton solde": "Dein Guthaben",
        "📅 Abonnement": "📅 Abo",
        "🛒 Crédits achetés": "🛒 Gekauftes Guthaben",
        "Total disponible": "Insgesamt verfügbar",
        "Packs de crédits": "Guthabenpakete",
        "⚠️ Validité {0} mois après achat · notification avant expiration. Les crédits d'abonnement se renouvellent chaque mois (non reportés).":
            "⚠️ {0} Monat gültig ab Kauf · wir melden uns vor dem Verfall. Abo-Guthaben erneuert sich jeden Monat (kein Übertrag).",
    },
}


# ── Irlande : même anglais que /en (cf. homepage_i18n) ───────────────────────
for _dico in (T_PRICING, T_COMPARE, T_CREDITS):
    _dico["en-ie"] = dict(_dico["en"])

# ── Mexique : l'espagnol d'Espagne, avec les écarts qui comptent ─────────────
# Seules les entrées listées ici changent ; le reste vient de `es`.
_MX_PRICING = {
    "Ouvrir l'app →": "Abrir la app →",
    "Tu n'as pas encore de compte ?": "¿Todavía no tienes cuenta?",
    "{0} analyses de vidéos": "{0} análisis de video",
    "de chaque vidéo": "de cada video",
    "CTA visuels et audio": "CTA en pantalla y hablados",
    "upload et par lien TikTok": "subida de archivo y por enlace de TikTok",
    "{0} jours d'accès complet, sans carte bancaire — {1} analyses de vidéos et {2} essais sur chaque outil de création":
        "{0} días de acceso completo, sin tarjeta — {1} análisis de video y {2} usos gratis de cada herramienta de creación",
    "Historique de tes analyses, sur tous tes appareils":
        "Tu historial de análisis, en todos tus dispositivos",
}
_MX_COMPARE = {
    "Analyse vidéo": "Análisis de video",
    "Analyses de vidéos": "Análisis de video",
    "Analyse par lien TikTok": "Análisis por enlace de TikTok",
    "Studio d'accroches IA (prompts vidéo)": "Estudio de ganchos con IA (prompts de video)",
    "Feed Radar (vidéos qui percent)": "Feed Radar (videos que despegan)",
    "Produits et vidéos recommandés": "Productos y videos recomendados",
    "Facture avec TVA et n° d'entreprise": "Factura con impuestos y número de empresa",
}
T_PRICING["es-mx"] = {**T_PRICING["es"], **_MX_PRICING}
T_COMPARE["es-mx"] = {**T_COMPARE["es"], **_MX_COMPARE}
T_CREDITS["es-mx"] = dict(T_CREDITS["es"])
