"""Traduction de la page d'accueil — rendu CÔTÉ SERVEUR, une URL par langue.

Pourquoi côté serveur et non plus dans le navigateur : une traduction posée par
JavaScript n'est pas indexée. Googlebot lit le HTML servi ; il voyait donc six
fois la même page française. Chaque langue a maintenant sa propre URL, son
propre HTML, son `<html lang>`, ses balises `hreflang` et son entrée de sitemap.

Fonctionnement : le gabarit `templates/homepage.html` reste écrit EN FRANÇAIS et
porte des attributs `data-i18n="clef"`. Au démarrage, ce module relit le HTML
déjà rendu par Jinja et en fabrique une variante par langue. Aucun coût par
requête — les six chaînes sont mises en cache, exactement comme l'était la
version française seule.

Le français n'est PAS listé dans `T` : c'est ce qui est écrit dans le gabarit,
il sert de source et de repli. Une clef absente d'une langue retombe donc sur le
français plutôt que d'afficher un trou.

Chaînes venant du serveur (offre d'essai, dimensions d'analyse) : elles ne sont
jamais recopiées ici. Le gabarit les dépose dans un attribut `data-var-*` et les
traductions y font référence par un jeton `{trial}`, `{trial_full}`, `{count}`,
`{dims}`. En français le jeton retombe sur la valeur serveur — site_content.py
reste la source unique (cf. son avertissement « Interdiction d'en écrire une
variante ailleurs »).
"""
from __future__ import annotations

import html as _html
import re

# ── Langues servies ──────────────────────────────────────────────────────────
# L'ordre fait foi : il pilote le sélecteur, les `hreflang` et le sitemap.
LANGS = ["fr", "en", "en-ie", "pt-br", "es", "es-mx", "it", "de"]

# Chemin public de chaque langue. Le français reste à la racine : c'est l'URL
# historique, déjà indexée, on ne la déplace pas.
LANG_PATHS = {
    "fr": "/", "en": "/en", "en-ie": "/en-ie", "pt-br": "/pt-br",
    "es": "/es", "es-mx": "/es-mx", "it": "/it", "de": "/de",
}

# Valeur de l'attribut `lang` du document (BCP 47).
HTML_LANG = {
    "fr": "fr", "en": "en", "en-ie": "en-IE", "pt-br": "pt-BR",
    "es": "es", "es-mx": "es-MX", "it": "it", "de": "de",
}

OG_LOCALE = {
    "fr": "fr_FR", "en": "en_US", "en-ie": "en_IE", "pt-br": "pt_BR",
    "es": "es_ES", "es-mx": "es_MX", "it": "it_IT", "de": "de_DE",
}

# Libellé du sélecteur. Drapeau + code : lisible sans connaître la langue.
# L'Espagne et le Mexique partagent la langue mais pas la formulation ni la
# devise : deux entrées distinctes, sinon le visiteur mexicain ne sait pas
# laquelle est la sienne.
LANG_LABEL = {
    "fr": "🇫🇷 FR", "en": "🇬🇧 EN", "en-ie": "🇮🇪 IE", "pt-br": "🇧🇷 PT",
    "es": "🇪🇸 ES", "es-mx": "🇲🇽 MX", "it": "🇮🇹 IT", "de": "🇩🇪 DE",
}

# Langue de repli quand l'en-tête Accept-Language ne correspond à rien.
DEFAULT = "fr"


# ── AFFICHAGE DU PRIX HORS ZONE EURO ─────────────────────────────────────────
# Décision (07/09/2026) : on AFFICHE un ordre de grandeur dans la devise locale,
# mais on FACTURE en euros. Aucun prix supplémentaire n'est créé dans Stripe —
# le chemin de facturation, réparé en août, n'est pas rouvert.
#
# Conséquence directe : ces taux ne servent QU'À L'AFFICHAGE. S'ils dérivent,
# le montant prélevé ne bouge pas d'un centime ; seul l'ordre de grandeur montré
# devient un peu moins juste. C'est aussi pourquoi la ligne affichée dit
# explicitement « à titre indicatif » et rappelle le prélèvement en euros.
#
# À rafraîchir de temps en temps. Unités de devise pour 1 euro.
FX = {
    "USD": (1.08, "US${v}"),
    "GBP": (0.85, "£{v}"),
    "BRL": (6.00, "R${v}"),
    # « MX$ » et non « $ » seul : au Mexique le signe dollar désigne aussi bien
    # le peso que le dollar américain, l'ambiguïté sur un prix est inacceptable.
    "MXN": (19.50, "MX${v}"),
}

# Devises montrées par langue. Une langue absente = marché de la zone euro :
# on n'affiche rien de plus, le prix en euros se suffit.
#   `en`  sert les États-Unis, le Royaume-Uni et Singapour — d'où le dollar ET
#         la livre. L'Irlande a désormais sa propre variante `en-ie`, absente de
#         ce dictionnaire : zone euro, donc aucune conversion à afficher.
#   `pt-br` sert le Brésil, `es-mx` le Mexique.
DISPLAY_CURRENCIES = {
    "en": ["USD", "GBP"],
    "pt-br": ["BRL"],
    "es-mx": ["MXN"],
}

# Langues dont le marché est HORS Union européenne : la mention française
# « TVA non applicable, article 293 B du CGI » y est remplacée par une
# formulation neutre. Elle ne prétend RIEN sur la fiscalité locale de l'acheteur
# — elle décrit seulement ce qui se passe au moment du paiement.
NON_EU_MARKETS = set(DISPLAY_CURRENCIES)


def _montant(valeur: float, devise: str, lang: str) -> str:
    """Formate un montant converti, arrondi à l'unité."""
    taux, gabarit = FX[devise]
    v = round(valeur * taux)
    # Séparateur de milliers : virgule en anglais, point en portugais.
    texte = f"{v:,}"
    if lang == "pt-br":
        texte = texte.replace(",", ".")
    return gabarit.format(v=texte)


def prix_affiches(lang: str) -> tuple[str, str] | None:
    """(mensuel, annuel) dans la ou les devises du marché, ou None en zone euro."""
    devises = DISPLAY_CURRENCIES.get(lang)
    if not devises:
        return None
    try:
        import site_content  # source unique des montants (jamais recopiés ici)
        mois, an = site_content.PRICE_MONTH, site_content.PRICE_YEAR
    except Exception:
        return None
    return (
        " / ".join(_montant(mois, d, lang) for d in devises),
        " / ".join(_montant(an, d, lang) for d in devises),
    )


# ── Traductions ──────────────────────────────────────────────────────────────
T: dict[str, dict[str, str]] = {

    # ═══════════════════════════ ANGLAIS ═══════════════════════════
    "en": {
        "meta_title": "Qeerah — TikTok Shop video analysis tool",
        "meta_desc": "Qeerah — TikTok Shop video analysis tool. Built by creators, for TikTok Shop creators. Analyse any video and copy the winning method. {trial}.",
        "og_title": "Qeerah — TikTok Shop video analysis tool",
        "og_desc": "Built by creators, for TikTok Shop creators. Analyse your videos and copy the winning method. {trial}.",
        "tw_desc": "Built by creators, for TikTok Shop creators. Analyse your videos and copy the winning method.",

        "trial_offer": "7 days of full access, no credit card",
        "trial_full": "7 days of full access, no credit card — 10 video analyses and 3 free uses of each creation tool",
        "dims": "Hook, Retention, Selling, Emotion, Conversion, Algorithm, Overall score",

        "nav_how": "How it works", "nav_features": "Features", "nav_pricing": "Pricing",
        "nav_try": "Try it free", "nav_login": "Log in",

        "hero_badge": "TikTok Shop video analysis tool",
        "hero_h1": "You know your video flopped. <span style=\"white-space:nowrap\">Not why.</span> So you go and make the same one again.",
        "hero_sub": "Drop in the link of a video that's crushing it: 30 seconds later you know exactly what makes it sell — the hook, the pacing, the moment it lands — and how to pull that off with your own product. No more guessing.",
        "hero_social": "Built by creators, for TikTok Shop creators",

        "auth_eyebrow": "Proven in the field",
        "auth_sub": "Built with 10+ established French TikTok Shop creators and tuned on 1,000+ videos from the best creators across several markets — not marketing guesswork.",
        "auth_stat_1": "top videos analysed",
        "auth_stat_2": "selling levers decoded",
        "auth_stat_3": "French TikTok Shop creators put their expertise into the app",
        "auth_stat_4": "markets analysed",
        "c_fr": "France", "c_us": "United States", "c_uk": "United Kingdom",
        "c_br": "Brazil", "c_de": "Germany", "c_ites": "Italy &amp; Spain",

        "mock_1": "✅ Strong hook (9/10)",
        "mock_2": "⚠️ Missing call to action",
        "mock_3": "Optimal length (15s)",
        "mock_4": "💰 Price detected: €29.99",

        "demo_tag": "Sample analysis",
        "demo_title": "Here's exactly what you get",
        "demo_p": "A complete report in 30 seconds, from a single link.",
        "demo_url": "qeerah.com/app — analysis running",
        "demo_step_0": "Reading the TikTok link",
        "demo_step_1": "Extracting images and audio",
        "demo_step_2": "Analysing the hook and retention",
        "demo_step_3": "Detecting the selling triggers",
        "demo_step_4": "Writing the action plan",
        "demo_row_1": "Hook: direct question, strong interruption from the very first second",
        "demo_row_2": "Social proof and scarcity fire between 0:04 and 0:11",
        "demo_row_3": "Late call to action — attention starts dropping at 0:14",
        "demo_pause": "Pause", "demo_pause_aria": "Pause the demonstration",
        "demo_resume": "Play the demonstration again",
        "demo_resume_aria": "Play the demonstration again",
        "demo_tabs_aria": "Report detail",
        "demo_tab_0": "Hook decoded", "demo_tab_1": "Triggers", "demo_tab_2": "Action plan",
        "panel0_h3": "Why this hook holds attention",
        "panel0_quote": "“You do this every morning and it's exactly what's damaging your skin.”",
        "panel0_li1": "<strong>Type</strong> — gentle accusation: the viewer feels involved before understanding why.",
        "panel0_li2": "<strong>Interruption strength</strong> — high: the subject is named within the first 1.2 seconds.",
        "panel0_li3": "<strong>Implicit promise</strong> — “I'll tell you what to do instead”, delivered at 0:06.",
        "panel1_h3": "The triggers that fire",
        "panel1_li1": "<strong>Social proof</strong> — “thousands of people” at 0:04, no verifiable figure but enough to reassure.",
        "panel1_li2": "<strong>Authority</strong> — technical vocabulary at 0:07, which establishes legitimacy.",
        "panel1_li3": "<strong>Scarcity</strong> — limited stock mentioned at 0:11.",
        "panel1_li4": "<strong>Missing: reciprocity</strong> — no advice given before the sale, the most profitable lever to add here.",
        "panel2_h3": "What you change on your next video",
        "panel2_li1": "Move the call to action to <strong>0:08</strong> instead of 0:14: attention drops before it arrives.",
        "panel2_li2": "Add a visual demonstration between 0:05 and 0:09, the most-watched stretch.",
        "panel2_li3": "Reuse the hook structure, adapted to your product — three variants are suggested to you.",

        "tool_btn_analyze": "Analyse a video", "tool_btn_carousel": "Create a carousel",
        "tool_btn_scripts": "Generate scripts", "badge_new": "NEW",
        "tool_title": "Analyse your video now",
        "tool_ph": "Paste the TikTok video link",
        "tool_ph_aria": "Link of the TikTok video to analyse",
        "tool_paste": "Paste", "tool_paste_aria": "Paste from clipboard",
        "tool_hint": "Example: https://www.tiktok.com/@account/video/123456789",
        "tool_analyze_url": "Analyse this video",
        "tool_upload_switch": "or upload a video file instead",
        "tool_drop": "Click or drop your video here",
        "tool_drop_hint": "MP4, MOV • 500 MB maximum",
        "tool_analyze_file": "Analyse this file",
        "tool_note": "{trial}",
        "loading_text": "Extracting images…",
        "results_counter": "{trial} — create your account to use it",
        "res_score_label": "Persuasion score / 100",
        "res_produit": "Product", "res_prix": "Price",
        "res_hook": "Hook type", "res_force": "Hook strength",
        "res_viral": "Viral potential",
        "mi_title": "Market data",
        "mi_lock_title": "Included in Qeerah Pro",
        "mi_lock_sub": "Market data + competitive advice",
        "mi_context": "Context", "mi_top_products": "Top products",
        "mi_trending": "📈 Trends", "mi_top_creators": "Top creators", "mi_actions": "Actions",
        "res_strengths": "Strengths", "res_weak": "To improve",
        "verdict_lock": "Detailed verdict included in <strong>Qeerah Pro</strong>",
        "see_plans": "See the plans →",
        "verdict_h3": "Verdict",
        "verdict_sample": "Sample verdict: “Excellent video with a very strong hook…”",
        "reco_lock": "Personalised recommendations included in <strong>Qeerah Pro</strong>",
        "reco_h3": "Best hook for this product",
        "reco_type": "Hook type: CURIOSITY",
        "reco_why": "It works because…",
        "reco_examples": "3 examples to test:",
        "btn_another": "Analyse another video", "btn_plans": "See the plans",

        "how_title": "How does it work?",
        "how_sub": "3 steps to decode any viral video",
        "how_1_h": "1. Paste a TikTok link",
        "how_1_p": "Any TikTok Shop video, viral or not. A few seconds are enough.",
        "how_2_h": "2. The analysis breaks down what sells",
        "how_2_p": "Analysis across {count} dimensions: {dims}.",
        "how_3_h": "3. Apply the method to your product",
        "how_3_p": "A detailed action plan to reproduce the success with YOUR products.",

        "feat_title": "The full breakdown",
        "feat_sub": "Everything top creators keep to themselves, laid out in real time",
        "feat_1_h": "See why people scroll past you in 3 seconds",
        "feat_1_p": "Your hook gets a score, and whatever's pushing people away gets named: the type, how hard it interrupts, whether the promise lands.",
        "feat_2_h": "Spot the triggers that make people buy — in your videos and your competitors'",
        "feat_2_p": "Authority, social proof, scarcity, urgency: the ones the video fires, and the ones it's missing.",
        "feat_3_h": "Pinpoint the exact second people drop off",
        "feat_3_p": "Open loops, cuts, transitions: what holds attention, and what kills it.",
        "feat_4_h": "Work out why they watch and never click",
        "feat_4_p": "Calls to action, spelled out or implied, objections answered or left hanging.",
        "feat_5_h": "Find out why TikTok pushed their video and not yours",
        "feat_5_p": "The signals the algorithm rewards, and the ones yours is missing.",
        "feat_6_h": "Take the winner's hooks, rewritten for your product",
        "feat_6_p": "Hooks rewritten, calls to action sharpened, angles ready to film.",

        "fr_sub": "The TikTok Shop videos crushing it right now, with their estimated revenue",
        "fr_loading": "Loading…", "fr_today": "Videos of the day", "fr_views": "— views",
        "fr_lock": "The rest of Feed Radar", "fr_create": "Create an account",
        "fr_unlock": "Unlock Feed Radar — {trial} →",
        "fr_views_word": "views", "fr_gmv_real": "Actual revenue", "fr_gmv_est": "Est. revenue",
        "fr_unlock_n": "Unlock the {n} others",
        "fr_thumb_alt": "Thumbnail of the TikTok video by",

        "tm_title": "They use Qeerah", "tm_sub": "Feedback from creators like you",
        "tm_all": "See all the reviews →",

        "pr_title": "One single plan",
        "pr_sub": "Everything is included. No tiers, no locked features.",
        # Pas de « incl. tax » ici : hors zone euro, la ligne du dessous annonce
        # qu'aucune taxe n'est ajoutée. Les deux se contredisaient.
        "pr_period": "per month — or €299/year (2 months free)",
        "pr_li1": "<strong>Video analyses</strong> included every month",
        "pr_li2": "Analysis by <strong>upload and by TikTok link</strong>",
        "pr_li3": "<strong>Guidance</strong>, personalised scripts and multi-link analysis",
        "pr_li4": "<strong>Market data</strong>, Feed Radar and profile search",
        "pr_li5": "🎬 Hook studio and 📸 photo carousel coach",
        "pr_cta": "Subscribe to Qeerah Pro →",
        "pr_vat": "VAT not applicable, article 293 B of the French tax code.",
        # Marchés hors UE (États-Unis, Royaume-Uni, Singapour) : formulation
        # neutre, qui décrit le paiement sans rien affirmer sur la fiscalité
        # locale de l'acheteur.
        "pr_vat_intl": "Charged in euros — no tax is added at checkout.",
        "pr_approx": "≈ {m}/month · {y}/year, indicative only — you are charged in euros.",
        "pr_no_account": "No account yet? <strong>{trial}</strong> on sign-up, with 10 analyses to try it out.",
        "pr_create": "Create an account →",
        "pr_compare": "See the full feature breakdown →",
        "pr_badge1": "🛡 No commitment",
        "pr_badge2": "💳 Secure payment (Stripe)",
        "pr_badge3": "⚡ Instant activation · cancel in 1 click",

        "faq_title": "Frequently asked questions",
        "faq_sub": "Everything you need to know before getting started.",
        "faq_q1": "What exactly is Qeerah?",
        "faq_a1": "Qeerah analyses the videos and products that <strong>sell the most on TikTok Shop</strong>, then generates carousels, hooks and optimised prompts from a single link. Find what works, recreate it for your product.",
        "faq_q2": "Can I try it without paying?",
        "faq_a2": "Yes: <strong>{trial_full}</strong>. You only move to a subscription if you want to continue beyond that.",
        "faq_q3": "How do credits work?",
        "faq_a3": "A single pot of credits shared between the <strong>hook studio</strong> and <strong>the carousel creator</strong> (1 carousel ≈ 10 credits), renewed every month. Top-up packs are available from €9 in your account.",
        "faq_q4": "Where does your TikTok Shop data come from?",
        "faq_a4": "From real sales tracked over the <strong>last 30 days</strong>, country by country. You see the creators and products that actually perform — not numbers pulled out of thin air.",
        "faq_q5": "Can I cancel at any time?",
        "faq_a5": "Yes, no commitment. Cancellation takes effect at the end of the current period, in 1 click from your Stripe customer portal.",
        "faq_q6": "Are my products and generations private?",
        "faq_a6": "Yes. Your generations are tied to your account and are never shared. GDPR-compliant hosting.",

        "ft_product": "Product", "ft_how": "How it works", "ft_features": "Features",
        "ft_faq": "FAQ", "ft_pricing": "Pricing", "ft_compare": "Compare plans",
        "ft_credits": "Credits",
        "ft_resources": "Resources",
        "ft_res1": "Analyse a TikTok Shop video",
        "ft_res2": "Products that sell in France",
        "ft_res3": "My video is getting no views",
        "ft_res4": "All articles",
        "ft_company": "Company", "ft_about": "About", "ft_blog": "Blog",
        "ft_contact": "Contact", "ft_affiliate": "Become an affiliate",
        "ft_legal": "Legal", "ft_terms": "Terms of use", "ft_cgv": "Terms of sale",
        "ft_privacy": "Privacy", "ft_mentions": "Legal notice",
        "ft_cookies": "Manage cookies",
        "ft_social": "Social",
        "ft_copy": "© 2026 Qeerah - Dope Ventures. All rights reserved",
        "ft_made": "Made with ❤️ in France 🇫🇷",
    },

    # ═══════════════════════════ PORTUGAIS (BRÉSIL) ═══════════════════════════
    "pt-br": {
        "meta_title": "Qeerah — Ferramenta de análise de vídeo TikTok Shop",
        "meta_desc": "Qeerah — Ferramenta de análise de vídeo TikTok Shop. Feito por criador, para criador do TikTok Shop. Analise qualquer vídeo e copie o método que vende. {trial}.",
        "og_title": "Qeerah — Ferramenta de análise de vídeo TikTok Shop",
        "og_desc": "Feito por criador, para criador do TikTok Shop. Analise seus vídeos e copie o método que vende. {trial}.",
        "tw_desc": "Feito por criador, para criador do TikTok Shop. Analise seus vídeos e copie o método que vende.",

        "trial_offer": "7 dias de acesso completo, sem cartão de crédito",
        "trial_full": "7 dias de acesso completo, sem cartão de crédito — 10 análises de vídeo e 3 usos gratuitos de cada ferramenta de criação",
        "dims": "Gancho, Retenção, Venda, Emoção, Conversão, Algoritmo, Nota geral",

        "nav_how": "Como funciona", "nav_features": "Recursos", "nav_pricing": "Preços",
        "nav_try": "Testar de graça", "nav_login": "Entrar",

        "hero_badge": "Ferramenta de análise de vídeo TikTok Shop",
        "hero_h1": "Você sabe que seu vídeo não vendeu. <span style=\"white-space:nowrap\">Não sabe por quê.</span> Aí grava o mesmo de novo.",
        "hero_sub": "Cole o link de um vídeo que tá bombando: em 30 segundos você sabe exatamente o que faz ele vender — o gancho, o ritmo, a hora que a ficha cai — e como repetir isso no seu produto. Chega de achismo.",
        "hero_social": "Feito por criador, para criador do TikTok Shop",

        "auth_eyebrow": "Método testado na prática",
        "auth_sub": "Feito com a experiência de mais de 10 criadores franceses já consolidados no TikTok Shop e calibrado em mais de 1.000 vídeos dos melhores criadores de vários mercados — nada de achismo de marketing.",
        "auth_stat_1": "melhores vídeos analisados",
        "auth_stat_2": "gatilhos de venda decodificados",
        "auth_stat_3": "criadores franceses do TikTok Shop colocaram sua experiência no app",
        "auth_stat_4": "mercados analisados",
        "c_fr": "França", "c_us": "Estados Unidos", "c_uk": "Reino Unido",
        "c_br": "Brasil", "c_de": "Alemanha", "c_ites": "Itália e Espanha",

        "mock_1": "✅ Gancho forte (9/10)",
        "mock_2": "⚠️ Chamada para ação ausente",
        "mock_3": "Duração ideal (15s)",
        "mock_4": "💰 Preço detectado: 29,99 €",

        "demo_tag": "Exemplo de análise",
        "demo_title": "Veja exatamente o que você recebe",
        "demo_p": "Um relatório completo em 30 segundos, a partir de um simples link.",
        "demo_url": "qeerah.com/app — análise em andamento",
        "demo_step_0": "Leitura do link do TikTok",
        "demo_step_1": "Extração das imagens e do áudio",
        "demo_step_2": "Análise do gancho e da retenção",
        "demo_step_3": "Detecção dos gatilhos de venda",
        "demo_step_4": "Redação do plano de ação",
        "demo_row_1": "Gancho: pergunta direta, interrupção forte já no 1º segundo",
        "demo_row_2": "Prova social e escassez ativadas entre 0:04 e 0:11",
        "demo_row_3": "Chamada para ação tardia — a atenção começa a cair em 0:14",
        "demo_pause": "Pausar", "demo_pause_aria": "Pausar a demonstração",
        "demo_resume": "Rodar a demonstração de novo",
        "demo_resume_aria": "Rodar a demonstração de novo",
        "demo_tabs_aria": "Detalhe do relatório",
        "demo_tab_0": "Gancho decifrado", "demo_tab_1": "Gatilhos",
        "demo_tab_2": "Plano de ação",
        "panel0_h3": "Por que esse gancho prende",
        "panel0_quote": "“Você faz isso toda manhã e é exatamente o que estraga a sua pele.”",
        "panel0_li1": "<strong>Tipo</strong> — acusação leve: o espectador se sente atingido antes de entender por quê.",
        "panel0_li2": "<strong>Força de interrupção</strong> — alta: o assunto é nomeado em 1,2 segundo.",
        "panel0_li3": "<strong>Promessa implícita</strong> — “vou te dizer o que fazer no lugar”, cumprida em 0:06.",
        "panel1_h3": "Os gatilhos ativados",
        "panel1_li1": "<strong>Prova social</strong> — “milhares de pessoas” em 0:04, sem número verificável mas suficiente para tranquilizar.",
        "panel1_li2": "<strong>Autoridade</strong> — vocabulário técnico em 0:07, que instala a legitimidade.",
        "panel1_li3": "<strong>Escassez</strong> — menção a estoque limitado em 0:11.",
        "panel1_li4": "<strong>Ausente: reciprocidade</strong> — nenhum conselho oferecido antes da venda, é o gatilho mais rentável a acrescentar aqui.",
        "panel2_h3": "O que você muda no próximo vídeo",
        "panel2_li1": "Antecipar a chamada para ação para <strong>0:08</strong> em vez de 0:14: a atenção cai antes que ela chegue.",
        "panel2_li2": "Acrescentar uma demonstração visual entre 0:05 e 0:09, o trecho mais assistido.",
        "panel2_li3": "Reaproveitar a estrutura do gancho, adaptada ao seu produto — três variantes são sugeridas.",

        "tool_btn_analyze": "Analisar um vídeo", "tool_btn_carousel": "Criar um carrossel",
        "tool_btn_scripts": "Gerar roteiros", "badge_new": "NOVO",
        "tool_title": "Analise seu vídeo agora",
        "tool_ph": "Cole o link do vídeo do TikTok",
        "tool_ph_aria": "Link do vídeo do TikTok a analisar",
        "tool_paste": "Colar", "tool_paste_aria": "Colar da área de transferência",
        "tool_hint": "Exemplo: https://www.tiktok.com/@conta/video/123456789",
        "tool_analyze_url": "Analisar este vídeo",
        "tool_upload_switch": "ou mande um arquivo de vídeo",
        "tool_drop": "Clique ou arraste seu vídeo aqui",
        "tool_drop_hint": "MP4, MOV • 500 MB no máximo",
        "tool_analyze_file": "Analisar este arquivo",
        "tool_note": "{trial}",
        "loading_text": "Extraindo as imagens…",
        "results_counter": "{trial} — crie sua conta para aproveitar",
        "res_score_label": "Nota de persuasão / 100",
        "res_produit": "Produto", "res_prix": "Preço",
        "res_hook": "Tipo de gancho", "res_force": "Força do gancho",
        "res_viral": "Potencial viral",
        "mi_title": "Dados de mercado",
        "mi_lock_title": "Incluído no Qeerah Pro",
        "mi_lock_sub": "Dados de mercado + conselhos competitivos",
        "mi_context": "Contexto", "mi_top_products": "Principais produtos",
        "mi_trending": "📈 Tendências", "mi_top_creators": "Principais criadores",
        "mi_actions": "Ações",
        "res_strengths": "Pontos fortes", "res_weak": "A melhorar",
        "verdict_lock": "Veredito detalhado incluído no <strong>Qeerah Pro</strong>",
        "see_plans": "Ver os planos →",
        "verdict_h3": "Veredito",
        "verdict_sample": "Exemplo de veredito: “Vídeo excelente com gancho muito forte…”",
        "reco_lock": "Recomendações personalizadas incluídas no <strong>Qeerah Pro</strong>",
        "reco_h3": "Melhor gancho para este produto",
        "reco_type": "Tipo de gancho: CURIOSIDADE",
        "reco_why": "Funciona porque…",
        "reco_examples": "3 exemplos para testar:",
        "btn_another": "Analisar outro vídeo", "btn_plans": "Ver os planos",

        "how_title": "Como funciona?",
        "how_sub": "3 etapas para decifrar qualquer vídeo viral",
        "how_1_h": "1. Cole um link do TikTok",
        "how_1_p": "Qualquer vídeo do TikTok Shop, viral ou não. Alguns segundos bastam.",
        "how_2_h": "2. A análise destrincha o que faz vender",
        "how_2_p": "Análise em {count} dimensões: {dims}.",
        "how_3_h": "3. Aplique o método ao seu produto",
        "how_3_p": "Plano de ação detalhado para reproduzir o sucesso com os SEUS produtos.",

        "feat_title": "A análise completa",
        "feat_sub": "Tudo o que os grandes criadores guardam pra si, aberto em tempo real",
        "feat_1_h": "Descubra por que passam direto em 3 segundos",
        "feat_1_p": "Seu gancho ganha uma nota e o que espanta o público aparece com nome: o tipo, a força da interrupção, se a promessa se cumpre ou não.",
        "feat_2_h": "Ache os gatilhos que fazem comprar — nos seus vídeos e nos do concorrente",
        "feat_2_p": "Autoridade, prova social, escassez, urgência: os que o vídeo dispara e os que ficaram de fora.",
        "feat_3_h": "Descubra o segundo exato em que o povo larga o vídeo",
        "feat_3_p": "Ganchos em aberto, cortes, transições: o que segura a atenção e o que derruba.",
        "feat_4_h": "Entenda por que assistem e nunca clicam",
        "feat_4_p": "Chamadas para ação faladas ou subentendidas, objeções respondidas ou deixadas no ar.",
        "feat_5_h": "Saiba por que o TikTok entregou o vídeo dele e não o seu",
        "feat_5_p": "Os sinais que o algoritmo premia e os que faltam no seu.",
        "feat_6_h": "Pegue os ganchos de quem vendeu, reescritos pro seu produto",
        "feat_6_p": "Ganchos reescritos, chamadas para ação afiadas, ângulos prontos pra gravar.",

        "fr_sub": "Os vídeos do TikTok Shop que estão bombando agora, com o faturamento estimado",
        "fr_loading": "Carregando…", "fr_today": "Vídeos do dia",
        "fr_views": "— visualizações",
        "fr_lock": "O resto do Feed Radar", "fr_create": "Criar uma conta",
        "fr_unlock": "Desbloquear o Feed Radar — {trial} →",
        "fr_views_word": "visualizações", "fr_gmv_real": "Faturamento real",
        "fr_gmv_est": "Faturamento estimado",
        "fr_unlock_n": "Desbloqueie os outros {n}",
        "fr_thumb_alt": "Miniatura do vídeo do TikTok de",

        "tm_title": "Eles usam o Qeerah", "tm_sub": "Os retornos de criadores como você",
        "tm_all": "Ver todos os depoimentos →",

        "pr_title": "Um único plano",
        "pr_sub": "Está tudo incluído. Sem níveis, sem recurso bloqueado.",
        "pr_period": "por mês — ou 299 €/ano (2 meses grátis)",
        "pr_li1": "<strong>Análises de vídeos</strong> incluídas todo mês",
        "pr_li2": "Análise por <strong>upload e por link do TikTok</strong>",
        "pr_li3": "<strong>Orientação</strong>, roteiro personalizado e análise de vários links",
        "pr_li4": "<strong>Dados de mercado</strong>, Feed Radar e busca de perfil",
        "pr_li5": "🎬 Estúdio de ganchos e 📸 coach de carrossel de fotos",
        "pr_cta": "Assinar o Qeerah Pro →",
        "pr_vat": "IVA não aplicável, artigo 293 B do código tributário francês.",
        "pr_vat_intl": "Cobrado em euros — nenhum imposto é acrescentado no pagamento.",
        "pr_approx": "≈ {m}/mês · {y}/ano, a título indicativo — a cobrança é feita em euros.",
        "pr_no_account": "Ainda não tem conta? <strong>{trial}</strong> no cadastro, com 10 análises para testar.",
        "pr_create": "Criar uma conta →",
        "pr_compare": "Ver o detalhe de todos os recursos →",
        "pr_badge1": "🛡 Sem fidelidade",
        "pr_badge2": "💳 Pagamento seguro (Stripe)",
        "pr_badge3": "⚡ Ativação imediata · cancelamento em 1 clique",

        "faq_title": "Perguntas frequentes",
        "faq_sub": "Tudo o que você precisa saber antes de começar.",
        "faq_q1": "O que é o Qeerah exatamente?",
        "faq_a1": "O Qeerah analisa os vídeos e produtos que <strong>mais vendem no TikTok Shop</strong> e gera, a partir de um simples link, carrosséis, ganchos e instruções otimizadas para converter. Descubra o que funciona e recrie no seu produto.",
        "faq_q2": "Posso testar sem pagar?",
        "faq_a2": "Sim: <strong>{trial_full}</strong>. Você só passa para uma assinatura se quiser continuar depois disso.",
        "faq_q3": "Como funcionam os créditos?",
        "faq_a3": "Um único saldo de créditos compartilhado entre o <strong>estúdio de ganchos</strong> e <strong>o criador de carrosséis</strong> (1 carrossel ≈ 10 créditos), renovado todo mês. Pacotes extras estão disponíveis a partir de 9 € na sua conta.",
        "faq_q4": "De onde vêm os seus dados do TikTok Shop?",
        "faq_a4": "De vendas reais dos <strong>últimos 30 dias</strong>, país por país. Você vê os criadores e produtos que realmente vendem — não número chutado.",
        "faq_q5": "Posso cancelar quando quiser?",
        "faq_a5": "Sim, sem fidelidade. O cancelamento vale a partir do fim do período em curso, em 1 clique no seu portal de cliente Stripe.",
        "faq_q6": "Meus produtos e gerações são privados?",
        "faq_a6": "Sim. Suas gerações ficam ligadas à sua conta e nunca são compartilhadas. Hospedagem em conformidade com o RGPD.",

        "ft_product": "Produto", "ft_how": "Como funciona", "ft_features": "Recursos",
        "ft_faq": "FAQ", "ft_pricing": "Preços", "ft_compare": "Comparar os planos",
        "ft_credits": "Créditos",
        "ft_resources": "Recursos úteis",
        "ft_res1": "Analisar um vídeo do TikTok Shop",
        "ft_res2": "Produtos que vendem na França",
        "ft_res3": "Meu vídeo não tem visualizações",
        "ft_res4": "Todos os artigos",
        "ft_company": "Empresa", "ft_about": "Sobre", "ft_blog": "Blog",
        "ft_contact": "Contato", "ft_affiliate": "Seja um afiliado",
        "ft_legal": "Jurídico", "ft_terms": "Termos de uso",
        "ft_cgv": "Condições de venda",
        "ft_privacy": "Privacidade", "ft_mentions": "Informações legais",
        "ft_cookies": "Gerenciar cookies",
        "ft_social": "Redes",
        "ft_copy": "© 2026 Qeerah - Dope Ventures. Todos os direitos reservados",
        "ft_made": "Made with ❤️ in France 🇫🇷",
    },

    # ═══════════════════════════ ESPAGNOL ═══════════════════════════
    "es": {
        "meta_title": "Qeerah — Herramienta de análisis de vídeo de TikTok Shop",
        "meta_desc": "Qeerah — Herramienta de análisis de vídeo de TikTok Shop. Hecho por creadores, para creadores de TikTok Shop. Analiza cualquier vídeo y copia el método que vende. {trial}.",
        "og_title": "Qeerah — Herramienta de análisis de vídeo de TikTok Shop",
        "og_desc": "Hecho por creadores, para creadores de TikTok Shop. Analiza tus vídeos y copia el método que vende. {trial}.",
        "tw_desc": "Hecho por creadores, para creadores de TikTok Shop. Analiza tus vídeos y copia el método que vende.",

        "trial_offer": "7 días de acceso completo, sin tarjeta bancaria",
        "trial_full": "7 días de acceso completo, sin tarjeta bancaria — 10 análisis de vídeo y 3 usos gratuitos de cada herramienta de creación",
        "dims": "Gancho, Retención, Venta, Emoción, Conversión, Algoritmo, Puntuación global",

        "nav_how": "Cómo funciona", "nav_features": "Funciones", "nav_pricing": "Precios",
        "nav_try": "Probar gratis", "nav_login": "Iniciar sesión",

        "hero_badge": "Herramienta de análisis de vídeo de TikTok Shop",
        "hero_h1": "Sabes que tu vídeo no vendió. <span style=\"white-space:nowrap\">No por qué.</span> Así que grabas otra vez el mismo.",
        "hero_sub": "Pega el enlace de un vídeo que está arrasando: en 30 segundos sabes exactamente qué lo hace vender — el gancho, el ritmo, el momento en que engancha — y cómo repetirlo con tu producto. Se acabó ir a ciegas.",
        "hero_social": "Hecho por creadores, para creadores de TikTok Shop",

        "auth_eyebrow": "Método probado sobre el terreno",
        "auth_sub": "Hecho con la experiencia de más de 10 creadores franceses ya consolidados en TikTok Shop y afinado sobre más de 1000 vídeos de los mejores creadores de varios mercados — nada de suposiciones de marketing.",
        "auth_stat_1": "mejores vídeos analizados",
        "auth_stat_2": "palancas de venta descifradas",
        "auth_stat_3": "creadores franceses de TikTok Shop han puesto su experiencia en la app",
        "auth_stat_4": "mercados analizados",
        "c_fr": "Francia", "c_us": "Estados Unidos", "c_uk": "Reino Unido",
        "c_br": "Brasil", "c_de": "Alemania", "c_ites": "Italia y España",

        "mock_1": "✅ Gancho potente (9/10)",
        "mock_2": "⚠️ Falta la llamada a la acción",
        "mock_3": "Duración óptima (15 s)",
        "mock_4": "💰 Precio detectado: 29,99 €",

        "demo_tag": "Ejemplo de análisis",
        "demo_title": "Esto es exactamente lo que recibes",
        "demo_p": "Un informe completo en 30 segundos, a partir de un simple enlace.",
        "demo_url": "qeerah.com/app — análisis en curso",
        "demo_step_0": "Lectura del enlace de TikTok",
        "demo_step_1": "Extracción de las imágenes y del audio",
        "demo_step_2": "Análisis del gancho y de la retención",
        "demo_step_3": "Detección de los disparadores de venta",
        "demo_step_4": "Redacción del plan de acción",
        "demo_row_1": "Gancho: pregunta directa, interrupción fuerte desde el 1.er segundo",
        "demo_row_2": "Prueba social y escasez activadas entre 0:04 y 0:11",
        "demo_row_3": "Llamada a la acción tardía — la atención empieza a caer en 0:14",
        "demo_pause": "Pausar", "demo_pause_aria": "Pausar la demostración",
        "demo_resume": "Volver a lanzar la demostración",
        "demo_resume_aria": "Volver a lanzar la demostración",
        "demo_tabs_aria": "Detalle del informe",
        "demo_tab_0": "Gancho descifrado", "demo_tab_1": "Disparadores",
        "demo_tab_2": "Plan de acción",
        "panel0_h3": "Por qué este gancho retiene",
        "panel0_quote": "«Haces esto todas las mañanas y es justo lo que estropea tu piel.»",
        "panel0_li1": "<strong>Tipo</strong> — acusación suave: el espectador se siente aludido antes de entender por qué.",
        "panel0_li2": "<strong>Fuerza de interrupción</strong> — alta: el tema se nombra en los primeros 1,2 segundos.",
        "panel0_li3": "<strong>Promesa implícita</strong> — «voy a decirte qué hacer en su lugar», cumplida en 0:06.",
        "panel1_h3": "Los disparadores activados",
        "panel1_li1": "<strong>Prueba social</strong> — «miles de personas» en 0:04, sin cifra verificable pero suficiente para tranquilizar.",
        "panel1_li2": "<strong>Autoridad</strong> — vocabulario técnico en 0:07, que instala la legitimidad.",
        "panel1_li3": "<strong>Escasez</strong> — mención de un stock limitado en 0:11.",
        "panel1_li4": "<strong>Ausente: reciprocidad</strong> — ningún consejo ofrecido antes de la venta, es la palanca más rentable que añadir aquí.",
        "panel2_h3": "Lo que cambias en tu próximo vídeo",
        "panel2_li1": "Adelantar la llamada a la acción a <strong>0:08</strong> en lugar de 0:14: la atención cae antes de que llegue.",
        "panel2_li2": "Añadir una demostración visual entre 0:05 y 0:09, la zona más vista.",
        "panel2_li3": "Reutilizar la estructura del gancho, adaptada a tu producto — se te proponen tres variantes.",

        "tool_btn_analyze": "Analizar un vídeo", "tool_btn_carousel": "Crear un carrusel",
        "tool_btn_scripts": "Generar guiones", "badge_new": "NUEVO",
        "tool_title": "Analiza tu vídeo ahora",
        "tool_ph": "Pega el enlace del vídeo de TikTok",
        "tool_ph_aria": "Enlace del vídeo de TikTok que analizar",
        "tool_paste": "Pegar", "tool_paste_aria": "Pegar desde el portapapeles",
        "tool_hint": "Ejemplo: https://www.tiktok.com/@cuenta/video/123456789",
        "tool_analyze_url": "Analizar este vídeo",
        "tool_upload_switch": "o sube un archivo de vídeo",
        "tool_drop": "Haz clic o suelta aquí tu vídeo",
        "tool_drop_hint": "MP4, MOV • 500 MB máximo",
        "tool_analyze_file": "Analizar este archivo",
        "tool_note": "{trial}",
        "loading_text": "Extrayendo las imágenes…",
        "results_counter": "{trial} — crea tu cuenta para aprovecharlo",
        "res_score_label": "Puntuación de persuasión / 100",
        "res_produit": "Producto", "res_prix": "Precio",
        "res_hook": "Tipo de gancho", "res_force": "Fuerza del gancho",
        "res_viral": "Potencial viral",
        "mi_title": "Datos de mercado",
        "mi_lock_title": "Incluido en Qeerah Pro",
        "mi_lock_sub": "Datos de mercado + consejos competitivos",
        "mi_context": "Contexto", "mi_top_products": "Top productos",
        "mi_trending": "📈 Tendencias", "mi_top_creators": "Top creadores",
        "mi_actions": "Acciones",
        "res_strengths": "Puntos fuertes", "res_weak": "A mejorar",
        "verdict_lock": "Veredicto detallado incluido en <strong>Qeerah Pro</strong>",
        "see_plans": "Ver los planes →",
        "verdict_h3": "Veredicto",
        "verdict_sample": "Ejemplo de veredicto: «Vídeo excelente con un gancho muy fuerte…»",
        "reco_lock": "Recomendaciones personalizadas incluidas en <strong>Qeerah Pro</strong>",
        "reco_h3": "Mejor gancho para este producto",
        "reco_type": "Tipo de gancho: CURIOSIDAD",
        "reco_why": "Funciona porque…",
        "reco_examples": "3 ejemplos que probar:",
        "btn_another": "Analizar otro vídeo", "btn_plans": "Ver los planes",

        "how_title": "¿Cómo funciona?",
        "how_sub": "3 pasos para descifrar cualquier vídeo viral",
        "how_1_h": "1. Pega un enlace de TikTok",
        "how_1_p": "Cualquier vídeo de TikTok Shop, viral o no. Bastan unos segundos.",
        "how_2_h": "2. El análisis desmonta lo que hace vender",
        "how_2_p": "Análisis en {count} dimensiones: {dims}.",
        "how_3_h": "3. Aplica el método a tu producto",
        "how_3_p": "Plan de acción detallado para reproducir el éxito con TUS productos.",

        "feat_title": "El análisis completo",
        "feat_sub": "Todo lo que los mejores creadores se callan, sobre la mesa y en directo",
        "feat_1_h": "Descubre por qué te pasan de largo en 3 segundos",
        "feat_1_p": "Tu gancho recibe una nota y lo que espanta al público aparece con nombre: el tipo, la fuerza con que corta, si la promesa se cumple o no.",
        "feat_2_h": "Caza los disparadores que hacen comprar — en lo tuyo y en la competencia",
        "feat_2_p": "Autoridad, prueba social, escasez, urgencia: los que el vídeo dispara y los que se ha dejado fuera.",
        "feat_3_h": "Localiza el segundo exacto en que la gente se larga",
        "feat_3_p": "Bucles abiertos, cortes, transiciones: lo que sujeta la atención y lo que la tira por tierra.",
        "feat_4_h": "Entiende por qué miran y nunca hacen clic",
        "feat_4_p": "Llamadas a la acción dichas o insinuadas, objeciones resueltas o dejadas en el aire.",
        "feat_5_h": "Averigua por qué TikTok empujó su vídeo y no el tuyo",
        "feat_5_p": "Las señales que el algoritmo premia y las que le faltan al tuyo.",
        "feat_6_h": "Quédate con los ganchos del que vendió, reescritos para tu producto",
        "feat_6_p": "Ganchos reescritos, llamadas a la acción afiladas, ángulos listos para grabar.",

        "fr_sub": "Los vídeos de TikTok Shop que arrasan ahora mismo, con su facturación estimada",
        "fr_loading": "Cargando…", "fr_today": "Vídeos del día",
        "fr_views": "— visualizaciones",
        "fr_lock": "El resto del Feed Radar", "fr_create": "Crear una cuenta",
        "fr_unlock": "Desbloquear el Feed Radar — {trial} →",
        "fr_views_word": "visualizaciones", "fr_gmv_real": "Facturación real",
        "fr_gmv_est": "Facturación estimada",
        "fr_unlock_n": "Desbloquea los {n} restantes",
        "fr_thumb_alt": "Miniatura del vídeo de TikTok de",

        "tm_title": "Usan Qeerah", "tm_sub": "Las opiniones de creadores como tú",
        "tm_all": "Ver todas las opiniones →",

        "pr_title": "Una sola oferta",
        "pr_sub": "Todo incluido. Sin niveles, sin funciones bloqueadas.",
        "pr_period": "al mes, IVA incl. — o 299 € IVA incl./año (2 meses gratis)",
        "pr_li1": "<strong>Análisis de vídeos</strong> incluidos cada mes",
        "pr_li2": "Análisis por <strong>archivo y por enlace de TikTok</strong>",
        "pr_li3": "<strong>Acompañamiento</strong>, guion personalizado y análisis de varios enlaces",
        "pr_li4": "<strong>Datos de mercado</strong>, Feed Radar y búsqueda de perfil",
        "pr_li5": "🎬 Estudio de ganchos y 📸 coach de carrusel de fotos",
        "pr_cta": "Suscribirse a Qeerah Pro →",
        "pr_vat": "IVA no aplicable, artículo 293 B del código fiscal francés.",
        "pr_no_account": "¿Aún no tienes cuenta? <strong>{trial}</strong> al registrarte, con 10 análisis para probar.",
        "pr_create": "Crear una cuenta →",
        "pr_compare": "Ver el detalle de todas las funciones →",
        "pr_badge1": "🛡 Sin compromiso",
        "pr_badge2": "💳 Pago seguro (Stripe)",
        "pr_badge3": "⚡ Activación inmediata · cancelación en 1 clic",

        "faq_title": "Preguntas frecuentes",
        "faq_sub": "Todo lo que hay que saber antes de empezar.",
        "faq_q1": "¿Qué es Qeerah exactamente?",
        "faq_a1": "Qeerah analiza los vídeos y productos que <strong>más venden en TikTok Shop</strong> y genera, a partir de un simple enlace, carruseles, ganchos e instrucciones optimizadas para convertir. Descubre lo que funciona y recréalo en tu producto.",
        "faq_q2": "¿Puedo probarlo sin pagar?",
        "faq_a2": "Sí: <strong>{trial_full}</strong>. Solo pasas a una suscripción si quieres continuar más allá.",
        "faq_q3": "¿Cómo funcionan los créditos?",
        "faq_a3": "Un único saldo de créditos compartido entre el <strong>estudio de ganchos</strong> y <strong>el creador de carruseles</strong> (1 carrusel ≈ 10 créditos), renovado cada mes. Hay packs adicionales desde 9 € en tu cuenta.",
        "faq_q4": "¿De dónde vienen tus datos de TikTok Shop?",
        "faq_a4": "De ventas reales de los <strong>últimos 30 días</strong>, país por país. Ves los creadores y productos que venden de verdad — no cifras puestas a ojo.",
        "faq_q5": "¿Puedo cancelar en cualquier momento?",
        "faq_a5": "Sí, sin compromiso. La cancelación surte efecto al final del periodo en curso, en 1 clic desde tu portal de cliente Stripe.",
        "faq_q6": "¿Mis productos y generaciones son privados?",
        "faq_a6": "Sí. Tus generaciones están vinculadas a tu cuenta y nunca se comparten. Alojamiento conforme al RGPD.",

        "ft_product": "Producto", "ft_how": "Cómo funciona", "ft_features": "Funciones",
        "ft_faq": "FAQ", "ft_pricing": "Precios", "ft_compare": "Comparar los planes",
        "ft_credits": "Créditos",
        "ft_resources": "Recursos",
        "ft_res1": "Analizar un vídeo de TikTok Shop",
        "ft_res2": "Productos que venden en Francia",
        "ft_res3": "Mi vídeo no tiene visualizaciones",
        "ft_res4": "Todos los artículos",
        "ft_company": "Empresa", "ft_about": "Sobre nosotros", "ft_blog": "Blog",
        "ft_contact": "Contacto", "ft_affiliate": "Hazte afiliado",
        "ft_legal": "Legal", "ft_terms": "Condiciones de uso",
        "ft_cgv": "Condiciones de venta",
        "ft_privacy": "Privacidad", "ft_mentions": "Aviso legal",
        "ft_cookies": "Gestionar las cookies",
        "ft_social": "Redes",
        "ft_copy": "© 2026 Qeerah - Dope Ventures. Todos los derechos reservados",
        "ft_made": "Made with ❤️ in France 🇫🇷",
    },

    # ═══════════════════════════ ITALIEN ═══════════════════════════
    "it": {
        "meta_title": "Qeerah — Strumento di analisi video per TikTok Shop",
        "meta_desc": "Qeerah — Strumento di analisi video per TikTok Shop. Fatto da creator, per i creator di TikTok Shop. Analizza qualsiasi video e copia il metodo che vende. {trial}.",
        "og_title": "Qeerah — Strumento di analisi video per TikTok Shop",
        "og_desc": "Fatto da creator, per i creator di TikTok Shop. Analizza i tuoi video e copia il metodo che vende. {trial}.",
        "tw_desc": "Fatto da creator, per i creator di TikTok Shop. Analizza i tuoi video e copia il metodo che vende.",

        "trial_offer": "7 giorni di accesso completo, senza carta di credito",
        "trial_full": "7 giorni di accesso completo, senza carta di credito — 10 analisi di video e 3 utilizzi gratuiti di ogni strumento di creazione",
        "dims": "Gancio, Ritenzione, Vendita, Emozione, Conversione, Algoritmo, Punteggio globale",

        "nav_how": "Come funziona", "nav_features": "Funzionalità", "nav_pricing": "Prezzi",
        "nav_try": "Provalo gratis", "nav_login": "Accedi",

        "hero_badge": "Strumento di analisi video per TikTok Shop",
        "hero_h1": "Sai che il tuo video non ha venduto. <span style=\"white-space:nowrap\">Non perché.</span> Così ne giri un altro uguale.",
        "hero_sub": "Incolla il link di un video che sta spaccando: in 30 secondi sai esattamente cosa lo fa vendere — il gancio, il ritmo, il momento in cui scatta — e come rifarlo con il tuo prodotto. Basta andare a intuito.",
        "hero_social": "Fatto da creator, per i creator di TikTok Shop",

        "auth_eyebrow": "Metodo provato sul campo",
        "auth_sub": "Nato dall'esperienza di oltre 10 creator francesi già affermati su TikTok Shop e tarato su più di 1000 video dei migliori creator di diversi mercati — niente supposizioni di marketing.",
        "auth_stat_1": "video migliori analizzati",
        "auth_stat_2": "leve di vendita decodificate",
        "auth_stat_3": "creator francesi di TikTok Shop hanno messo la loro esperienza nell'app",
        "auth_stat_4": "mercati analizzati",
        "c_fr": "Francia", "c_us": "Stati Uniti", "c_uk": "Regno Unito",
        "c_br": "Brasile", "c_de": "Germania", "c_ites": "Italia e Spagna",

        "mock_1": "✅ Gancio efficace (9/10)",
        "mock_2": "⚠️ Invito all'azione mancante",
        "mock_3": "Durata ottimale (15s)",
        "mock_4": "💰 Prezzo rilevato: 29,99 €",

        "demo_tag": "Esempio di analisi",
        "demo_title": "Ecco esattamente cosa ricevi",
        "demo_p": "Un rapporto completo in 30 secondi, a partire da un semplice link.",
        "demo_url": "qeerah.com/app — analisi in corso",
        "demo_step_0": "Lettura del link TikTok",
        "demo_step_1": "Estrazione delle immagini e dell'audio",
        "demo_step_2": "Analisi del gancio e della ritenzione",
        "demo_step_3": "Rilevamento delle leve di vendita",
        "demo_step_4": "Stesura del piano d'azione",
        "demo_row_1": "Gancio: domanda diretta, interruzione forte già dal 1º secondo",
        "demo_row_2": "Prova sociale e scarsità attivate tra 0:04 e 0:11",
        "demo_row_3": "Invito all'azione tardivo — l'attenzione inizia a calare a 0:14",
        "demo_pause": "Metti in pausa",
        "demo_pause_aria": "Metti in pausa la dimostrazione",
        "demo_resume": "Rifai partire la dimostrazione",
        "demo_resume_aria": "Rifai partire la dimostrazione",
        "demo_tabs_aria": "Dettaglio del rapporto",
        "demo_tab_0": "Gancio decifrato", "demo_tab_1": "Leve",
        "demo_tab_2": "Piano d'azione",
        "panel0_h3": "Perché questo gancio tiene",
        "panel0_quote": "«Lo fai tutte le mattine ed è esattamente ciò che rovina la tua pelle.»",
        "panel0_li1": "<strong>Tipo</strong> — accusa gentile: chi guarda si sente chiamato in causa prima di capire perché.",
        "panel0_li2": "<strong>Forza di interruzione</strong> — alta: l'argomento è nominato entro 1,2 secondi.",
        "panel0_li3": "<strong>Promessa implicita</strong> — «ti dico cosa fare invece», mantenuta a 0:06.",
        "panel1_h3": "Le leve attivate",
        "panel1_li1": "<strong>Prova sociale</strong> — «migliaia di persone» a 0:04, senza cifra verificabile ma sufficiente a rassicurare.",
        "panel1_li2": "<strong>Autorevolezza</strong> — lessico tecnico a 0:07, che installa la legittimità.",
        "panel1_li3": "<strong>Scarsità</strong> — menzione di scorte limitate a 0:11.",
        "panel1_li4": "<strong>Assente: reciprocità</strong> — nessun consiglio offerto prima della vendita, è la leva più redditizia da aggiungere qui.",
        "panel2_h3": "Cosa cambi nel tuo prossimo video",
        "panel2_li1": "Anticipare l'invito all'azione a <strong>0:08</strong> invece di 0:14: l'attenzione cala prima che arrivi.",
        "panel2_li2": "Aggiungere una dimostrazione visiva tra 0:05 e 0:09, la zona più guardata.",
        "panel2_li3": "Riprendere la struttura del gancio, adattata al tuo prodotto — ti vengono proposte tre varianti.",

        "tool_btn_analyze": "Analizza un video", "tool_btn_carousel": "Crea un carosello",
        "tool_btn_scripts": "Genera copioni", "badge_new": "NOVITÀ",
        "tool_title": "Analizza il tuo video adesso",
        "tool_ph": "Incolla il link del video TikTok",
        "tool_ph_aria": "Link del video TikTok da analizzare",
        "tool_paste": "Incolla", "tool_paste_aria": "Incolla dagli appunti",
        "tool_hint": "Esempio: https://www.tiktok.com/@account/video/123456789",
        "tool_analyze_url": "Analizza questo video",
        "tool_upload_switch": "oppure carica un file video",
        "tool_drop": "Clicca o trascina qui il tuo video",
        "tool_drop_hint": "MP4, MOV • 500 MB massimo",
        "tool_analyze_file": "Analizza questo file",
        "tool_note": "{trial}",
        "loading_text": "Estrazione delle immagini…",
        "results_counter": "{trial} — crea il tuo account per approfittarne",
        "res_score_label": "Punteggio di persuasione / 100",
        "res_produit": "Prodotto", "res_prix": "Prezzo",
        "res_hook": "Tipo di gancio", "res_force": "Forza del gancio",
        "res_viral": "Potenziale virale",
        "mi_title": "Dati di mercato",
        "mi_lock_title": "Incluso in Qeerah Pro",
        "mi_lock_sub": "Dati di mercato + consigli competitivi",
        "mi_context": "Contesto", "mi_top_products": "Top prodotti",
        "mi_trending": "📈 Tendenze", "mi_top_creators": "Top creator",
        "mi_actions": "Azioni",
        "res_strengths": "Punti forti", "res_weak": "Da migliorare",
        "verdict_lock": "Verdetto dettagliato incluso in <strong>Qeerah Pro</strong>",
        "see_plans": "Vedi i piani →",
        "verdict_h3": "Verdetto",
        "verdict_sample": "Esempio di verdetto: «Video eccellente con un gancio molto forte…»",
        "reco_lock": "Consigli su misura inclusi in <strong>Qeerah Pro</strong>",
        "reco_h3": "Miglior gancio per questo prodotto",
        "reco_type": "Tipo di gancio: CURIOSITÀ",
        "reco_why": "Funziona perché…",
        "reco_examples": "3 esempi da testare:",
        "btn_another": "Analizza un altro video", "btn_plans": "Vedi i piani",

        "how_title": "Come funziona?",
        "how_sub": "3 passaggi per decifrare qualsiasi video virale",
        "how_1_h": "1. Incolla un link TikTok",
        "how_1_p": "Qualsiasi video di TikTok Shop, virale o no. Bastano pochi secondi.",
        "how_2_h": "2. L'analisi smonta ciò che fa vendere",
        "how_2_p": "Analisi su {count} dimensioni: {dims}.",
        "how_3_h": "3. Applica il metodo al tuo prodotto",
        "how_3_p": "Piano d'azione dettagliato per riprodurre il successo con i TUOI prodotti.",

        "feat_title": "L'analisi completa",
        "feat_sub": "Tutto quello che i migliori creator si tengono per sé, messo nero su bianco in tempo reale",
        "feat_1_h": "Scopri perché ti scorrono via in 3 secondi",
        "feat_1_p": "Il tuo gancio prende un voto e quello che fa scappare la gente viene detto chiaro: il tipo, quanto interrompe, se la promessa viene mantenuta o no.",
        "feat_2_h": "Becca le leve che fanno comprare — nei tuoi video e in quelli dei concorrenti",
        "feat_2_p": "Autorevolezza, prova sociale, scarsità, urgenza: quelle che il video accende e quelle che si è perso.",
        "feat_3_h": "Individua il secondo esatto in cui la gente molla",
        "feat_3_p": "Domande lasciate in sospeso, stacchi, transizioni: cosa tiene incollati e cosa fa cadere tutto.",
        "feat_4_h": "Capisci perché guardano e non cliccano mai",
        "feat_4_p": "Inviti all'azione detti o sottintesi, obiezioni risolte o lasciate lì.",
        "feat_5_h": "Scopri perché TikTok ha spinto il suo video e non il tuo",
        "feat_5_p": "I segnali che l'algoritmo premia e quelli che al tuo mancano.",
        "feat_6_h": "Prenditi i ganci di chi ha venduto, riscritti sul tuo prodotto",
        "feat_6_p": "Ganci riscritti, inviti all'azione affilati, angoli pronti da girare.",

        "fr_sub": "I video di TikTok Shop che stanno spaccando in questo momento, con il fatturato stimato",
        "fr_loading": "Caricamento…", "fr_today": "Video del giorno",
        "fr_views": "— visualizzazioni",
        "fr_lock": "Il resto del Feed Radar", "fr_create": "Crea un account",
        "fr_unlock": "Sblocca il Feed Radar — {trial} →",
        "fr_views_word": "visualizzazioni", "fr_gmv_real": "Fatturato reale",
        "fr_gmv_est": "Fatturato stimato",
        "fr_unlock_n": "Sblocca gli altri {n}",
        "fr_thumb_alt": "Miniatura del video TikTok di",

        "tm_title": "Usano Qeerah", "tm_sub": "I riscontri di creator come te",
        "tm_all": "Vedi tutte le recensioni →",

        "pr_title": "Una sola offerta",
        "pr_sub": "Tutto è incluso. Nessun livello, nessuna funzione bloccata.",
        "pr_period": "al mese, IVA incl. — oppure 299 € IVA incl./anno (2 mesi in omaggio)",
        "pr_li1": "<strong>Analisi di video</strong> incluse ogni mese",
        "pr_li2": "Analisi tramite <strong>caricamento e link TikTok</strong>",
        "pr_li3": "<strong>Affiancamento</strong>, copione personalizzato e analisi di più link",
        "pr_li4": "<strong>Dati di mercato</strong>, Feed Radar e ricerca di profilo",
        "pr_li5": "🎬 Studio di ganci e 📸 coach carosello foto",
        "pr_cta": "Abbonati a Qeerah Pro →",
        "pr_vat": "IVA non applicabile, articolo 293 B del codice fiscale francese.",
        "pr_no_account": "Non hai ancora un account? <strong>{trial}</strong> all'iscrizione, con 10 analisi per provare.",
        "pr_create": "Crea un account →",
        "pr_compare": "Vedi il dettaglio di tutte le funzionalità →",
        "pr_badge1": "🛡 Senza vincoli",
        "pr_badge2": "💳 Pagamento sicuro (Stripe)",
        "pr_badge3": "⚡ Attivazione immediata · disdetta in 1 clic",

        "faq_title": "Domande frequenti",
        "faq_sub": "Tutto quello che serve sapere prima di iniziare.",
        "faq_q1": "Cos'è esattamente Qeerah?",
        "faq_a1": "Qeerah analizza i video e i prodotti che <strong>vendono di più su TikTok Shop</strong>, poi genera da un semplice link caroselli, ganci e istruzioni ottimizzate per convertire. Scopri cosa funziona, ricrealo sul tuo prodotto.",
        "faq_q2": "Posso provarlo senza pagare?",
        "faq_a2": "Sì: <strong>{trial_full}</strong>. Passi a un abbonamento solo se vuoi continuare oltre.",
        "faq_q3": "Come funzionano i crediti?",
        "faq_a3": "Un unico monte crediti condiviso tra lo <strong>studio di ganci</strong> e <strong>il creatore di caroselli</strong> (1 carosello ≈ 10 crediti), rinnovato ogni mese. Pacchetti extra si comprano da 9 € dal tuo account.",
        "faq_q4": "Da dove arrivano i tuoi dati di TikTok Shop?",
        "faq_a4": "Da vendite vere degli <strong>ultimi 30 giorni</strong>, paese per paese. Vedi i creator e i prodotti che vendono davvero — non numeri buttati lì a occhio.",
        "faq_q5": "Posso disdire quando voglio?",
        "faq_a5": "Sì, senza vincoli. La disdetta ha effetto alla fine del periodo in corso, in 1 clic dal tuo portale cliente Stripe.",
        "faq_q6": "I miei prodotti e le mie generazioni sono privati?",
        "faq_a6": "Sì. Le tue generazioni sono legate al tuo account e non vengono mai condivise. Hosting conforme al GDPR.",

        "ft_product": "Prodotto", "ft_how": "Come funziona", "ft_features": "Funzionalità",
        "ft_faq": "FAQ", "ft_pricing": "Prezzi", "ft_compare": "Confronta i piani",
        "ft_credits": "Crediti",
        "ft_resources": "Risorse",
        "ft_res1": "Analizzare un video TikTok Shop",
        "ft_res2": "Prodotti che vendono in Francia",
        "ft_res3": "Il mio video non fa visualizzazioni",
        "ft_res4": "Tutti gli articoli",
        "ft_company": "Azienda", "ft_about": "Chi siamo", "ft_blog": "Blog",
        "ft_contact": "Contatti", "ft_affiliate": "Diventa affiliato",
        "ft_legal": "Legale", "ft_terms": "Condizioni d'uso",
        "ft_cgv": "Condizioni di vendita",
        "ft_privacy": "Riservatezza", "ft_mentions": "Note legali",
        "ft_cookies": "Gestisci i cookie",
        "ft_social": "Social",
        "ft_copy": "© 2026 Qeerah - Dope Ventures. Tutti i diritti riservati",
        "ft_made": "Made with ❤️ in France 🇫🇷",
    },

    # ═══════════════════════════ ALLEMAND ═══════════════════════════
    "de": {
        "meta_title": "Qeerah — Videoanalyse für TikTok Shop",
        "meta_desc": "Qeerah — Videoanalyse für TikTok Shop. Von Creators gemacht, für TikTok-Shop-Creators. Analysiere jedes Video und übernimm die Methode, die verkauft. {trial}.",
        "og_title": "Qeerah — Videoanalyse für TikTok Shop",
        "og_desc": "Von Creators gemacht, für TikTok-Shop-Creators. Analysiere deine Videos und übernimm die Methode, die verkauft. {trial}.",
        "tw_desc": "Von Creators gemacht, für TikTok-Shop-Creators. Analysiere deine Videos und übernimm die Methode, die verkauft.",

        "trial_offer": "7 Tage voller Zugang, ohne Kreditkarte",
        "trial_full": "7 Tage voller Zugang, ohne Kreditkarte — 10 Videoanalysen und 3 kostenlose Nutzungen jedes Kreativwerkzeugs",
        "dims": "Hook, Bindung, Verkauf, Emotion, Conversion, Algorithmus, Gesamtwertung",

        "nav_how": "So funktioniert's", "nav_features": "Funktionen",
        "nav_pricing": "Preise", "nav_try": "Kostenlos testen", "nav_login": "Anmelden",

        "hero_badge": "Videoanalyse für TikTok Shop",
        "hero_h1": "Du weißt, dass dein Video nichts verkauft hat. <span style=\"white-space:nowrap\">Nur nicht, warum.</span> Also drehst du das gleiche nochmal.",
        "hero_sub": "Pack den Link von einem Video rein, das gerade abgeht: 30 Sekunden später weißt du genau, was es verkaufen lässt — der Hook, das Tempo, der Moment, in dem es klickt — und wie du das mit deinem eigenen Produkt hinbekommst. Schluss mit Raten.",
        "hero_social": "Von Creators gemacht, für TikTok-Shop-Creators",

        "auth_eyebrow": "In der Praxis erprobt",
        "auth_sub": "Entstanden mit über 10 etablierten französischen TikTok-Shop-Creators und geeicht an mehr als 1000 Videos der besten Creators aus mehreren Märkten — kein Marketing-Bauchgefühl.",
        "auth_stat_1": "Top-Videos analysiert",
        "auth_stat_2": "Verkaufshebel entschlüsselt",
        "auth_stat_3": "französische TikTok-Shop-Creators haben ihr Wissen in die App eingebracht",
        "auth_stat_4": "Märkte analysiert",
        "c_fr": "Frankreich", "c_us": "Vereinigte Staaten", "c_uk": "Vereinigtes Königreich",
        "c_br": "Brasilien", "c_de": "Deutschland", "c_ites": "Italien &amp; Spanien",

        "mock_1": "✅ Starker Hook (9/10)",
        "mock_2": "⚠️ Call to Action fehlt",
        "mock_3": "Optimale Länge (15 s)",
        "mock_4": "💰 Erkannter Preis: 29,99 €",

        "demo_tag": "Beispielanalyse",
        "demo_title": "Genau das bekommst du",
        "demo_p": "Ein vollständiger Bericht in 30 Sekunden, aus einem einfachen Link.",
        "demo_url": "qeerah.com/app — Analyse läuft",
        "demo_step_0": "TikTok-Link wird gelesen",
        "demo_step_1": "Bilder und Ton werden extrahiert",
        "demo_step_2": "Hook und Bindung werden analysiert",
        "demo_step_3": "Verkaufsauslöser werden erkannt",
        "demo_step_4": "Aktionsplan wird geschrieben",
        "demo_row_1": "Hook: direkte Frage, starke Unterbrechung schon in der 1. Sekunde",
        "demo_row_2": "Sozialer Beweis und Knappheit greifen zwischen 0:04 und 0:11",
        "demo_row_3": "Call to Action kommt zu spät — die Aufmerksamkeit fällt ab 0:14",
        "demo_pause": "Pausieren", "demo_pause_aria": "Die Vorführung pausieren",
        "demo_resume": "Vorführung nochmal abspielen",
        "demo_resume_aria": "Vorführung nochmal abspielen",
        "demo_tabs_aria": "Details des Berichts",
        "demo_tab_0": "Hook entschlüsselt", "demo_tab_1": "Auslöser",
        "demo_tab_2": "Aktionsplan",
        "panel0_h3": "Warum dieser Hook hält",
        "panel0_quote": "„Du machst das jeden Morgen, und genau das schadet deiner Haut.“",
        "panel0_li1": "<strong>Typ</strong> — sanfter Vorwurf: Die Zuschauer fühlen sich angesprochen, bevor sie verstehen, warum.",
        "panel0_li2": "<strong>Unterbrechungskraft</strong> — hoch: Das Thema wird in den ersten 1,2 Sekunden benannt.",
        "panel0_li3": "<strong>Implizites Versprechen</strong> — „Ich sage dir, was du stattdessen tun sollst“, eingelöst bei 0:06.",
        "panel1_h3": "Die aktivierten Auslöser",
        "panel1_li1": "<strong>Sozialer Beweis</strong> — „Tausende von Menschen“ bei 0:04, ohne überprüfbare Zahl, aber ausreichend zur Beruhigung.",
        "panel1_li2": "<strong>Autorität</strong> — Fachvokabular bei 0:07, das Glaubwürdigkeit schafft.",
        "panel1_li3": "<strong>Knappheit</strong> — Hinweis auf begrenzten Bestand bei 0:11.",
        "panel1_li4": "<strong>Fehlt: Gegenseitigkeit</strong> — kein Rat vor dem Verkauf, das ist hier der lohnendste Hebel zum Ergänzen.",
        "panel2_h3": "Was du im nächsten Video änderst",
        "panel2_li1": "Den Call to Action auf <strong>0:08</strong> statt 0:14 vorziehen: Die Aufmerksamkeit fällt, bevor er kommt.",
        "panel2_li2": "Zwischen 0:05 und 0:09 was zum Zeigen einbauen, das ist der meistgesehene Abschnitt.",
        "panel2_li3": "Die Struktur des Hooks übernehmen, auf dein Produkt angepasst — drei Varianten bekommst du vorgeschlagen.",

        "tool_btn_analyze": "Ein Video analysieren",
        "tool_btn_carousel": "Ein Karussell erstellen",
        "tool_btn_scripts": "Skripte erzeugen", "badge_new": "NEU",
        "tool_title": "Analysiere dein Video jetzt",
        "tool_ph": "Füge den Link des TikTok-Videos ein",
        "tool_ph_aria": "Link des zu analysierenden TikTok-Videos",
        "tool_paste": "Einfügen", "tool_paste_aria": "Aus der Zwischenablage einfügen",
        "tool_hint": "Beispiel: https://www.tiktok.com/@konto/video/123456789",
        "tool_analyze_url": "Dieses Video analysieren",
        "tool_upload_switch": "oder lade stattdessen eine Videodatei hoch",
        "tool_drop": "Klick hier oder zieh dein Video rein",
        "tool_drop_hint": "MP4, MOV • maximal 500 MB",
        "tool_analyze_file": "Diese Datei analysieren",
        "tool_note": "{trial}",
        "loading_text": "Bilder werden extrahiert…",
        "results_counter": "{trial} — erstelle dein Konto, um es zu nutzen",
        "res_score_label": "Überzeugungswertung / 100",
        "res_produit": "Produkt", "res_prix": "Preis",
        "res_hook": "Art des Hooks", "res_force": "Stärke des Hooks",
        "res_viral": "Virales Potenzial",
        "mi_title": "Marktdaten",
        "mi_lock_title": "In Qeerah Pro enthalten",
        "mi_lock_sub": "Marktdaten + Wettbewerbstipps",
        "mi_context": "Kontext", "mi_top_products": "Top-Produkte",
        "mi_trending": "📈 Trends", "mi_top_creators": "Top-Creators",
        "mi_actions": "Maßnahmen",
        "res_strengths": "Stärken", "res_weak": "Zu verbessern",
        "verdict_lock": "Ausführliches Urteil in <strong>Qeerah Pro</strong> enthalten",
        "see_plans": "Die Pläne ansehen →",
        "verdict_h3": "Urteil",
        "verdict_sample": "Beispielurteil: „Ausgezeichnetes Video mit sehr starkem Hook…“",
        "reco_lock": "Persönliche Empfehlungen in <strong>Qeerah Pro</strong> enthalten",
        "reco_h3": "Bester Hook für dieses Produkt",
        "reco_type": "Art des Hooks: NEUGIER",
        "reco_why": "Das wirkt, weil…",
        "reco_examples": "3 Beispiele zum Testen:",
        "btn_another": "Ein anderes Video analysieren", "btn_plans": "Die Pläne ansehen",

        "how_title": "Wie funktioniert das?",
        "how_sub": "3 Schritte, um jedes virale Video zu entschlüsseln",
        "how_1_h": "1. Füge einen TikTok-Link ein",
        "how_1_p": "Jedes beliebige TikTok-Shop-Video, viral oder nicht. Ein paar Sekunden genügen.",
        "how_2_h": "2. Die Analyse zerlegt, was verkauft",
        "how_2_p": "Analyse in {count} Dimensionen: {dims}.",
        "how_3_h": "3. Wende die Methode auf dein Produkt an",
        "how_3_p": "Ausführlicher Aktionsplan, um den Erfolg mit DEINEN Produkten zu wiederholen.",

        "feat_title": "Die komplette Analyse",
        "feat_sub": "Alles, was Top-Creators für sich behalten — in Echtzeit auf den Tisch gelegt",
        "feat_1_h": "Sieh, warum man in 3 Sekunden an dir vorbeiwischt",
        "feat_1_p": "Dein Hook kriegt eine Note, und was die Leute vertreibt, wird beim Namen genannt: die Art, wie hart er unterbricht, ob das Versprechen aufgeht.",
        "feat_2_h": "Finde die Auslöser, die zum Kauf führen — bei dir wie bei der Konkurrenz",
        "feat_2_p": "Autorität, sozialer Beweis, Knappheit, Dringlichkeit: die, die das Video zündet, und die, die es sich spart.",
        "feat_3_h": "Finde die genaue Sekunde, in der die Leute abspringen",
        "feat_3_p": "Offene Fragen, Schnitte, Übergänge: was dranbleiben lässt und was alles kippt.",
        "feat_4_h": "Versteh, warum sie zusehen und nie klicken",
        "feat_4_p": "Calls to Action, ausgesprochen oder nur angedeutet, Einwände ausgeräumt oder offen gelassen.",
        "feat_5_h": "Finde heraus, warum TikTok sein Video gepusht hat und nicht deins",
        "feat_5_p": "Die Signale, die der Algorithmus belohnt, und die, die deinem fehlen.",
        "feat_6_h": "Hol dir die Hooks von dem, der verkauft hat — auf dein Produkt umgeschrieben",
        "feat_6_p": "Hooks neu geschrieben, Calls to Action zugespitzt, Ansätze fertig zum Drehen.",

        "fr_sub": "Die TikTok-Shop-Videos, die gerade durch die Decke gehen, mit geschätztem Umsatz",
        "fr_loading": "Wird geladen…", "fr_today": "Videos des Tages",
        "fr_views": "— Aufrufe",
        "fr_lock": "Der Rest des Feed Radar", "fr_create": "Konto erstellen",
        "fr_unlock": "Feed Radar freischalten — {trial} →",
        "fr_views_word": "Aufrufe", "fr_gmv_real": "Echter Umsatz",
        "fr_gmv_est": "Geschätzter Umsatz",
        "fr_unlock_n": "Die anderen {n} freischalten",
        "fr_thumb_alt": "Vorschaubild des TikTok-Videos von",

        "tm_title": "Sie nutzen Qeerah", "tm_sub": "Rückmeldungen von Creators wie dir",
        "tm_all": "Alle Erfahrungsberichte ansehen →",

        "pr_title": "Ein einziges Angebot",
        "pr_sub": "Alles ist enthalten. Keine Stufen, keine gesperrten Funktionen.",
        "pr_period": "pro Monat, inkl. MwSt. — oder 299 € inkl. MwSt./Jahr (2 Monate geschenkt)",
        "pr_li1": "<strong>Videoanalysen</strong> jeden Monat enthalten",
        "pr_li2": "Analyse per <strong>Upload und per TikTok-Link</strong>",
        "pr_li3": "<strong>Begleitung</strong>, persönliches Skript und Analyse mehrerer Links",
        "pr_li4": "<strong>Marktdaten</strong>, Feed Radar und Profilsuche",
        "pr_li5": "🎬 Hook-Studio und 📸 Fotokarussell-Coach",
        "pr_cta": "Qeerah Pro abonnieren →",
        "pr_vat": "Keine Mehrwertsteuer, Artikel 293 B des französischen Steuergesetzbuchs.",
        "pr_no_account": "Noch kein Konto? <strong>{trial}</strong> bei der Anmeldung, mit 10 Analysen zum Ausprobieren.",
        "pr_create": "Konto erstellen →",
        "pr_compare": "Alle Funktionen im Detail ansehen →",
        "pr_badge1": "🛡 Ohne Bindung",
        "pr_badge2": "💳 Sichere Zahlung (Stripe)",
        "pr_badge3": "⚡ Sofort aktiv · Kündigung mit 1 Klick",

        "faq_title": "Häufige Fragen",
        "faq_sub": "Alles, was du vor dem Start wissen musst.",
        "faq_q1": "Was ist Qeerah genau?",
        "faq_a1": "Qeerah analysiert die Videos und Produkte, die <strong>auf TikTok Shop am meisten verkaufen</strong>, und erzeugt aus einem einfachen Link Karussells, Hooks und optimierte Vorgaben, die konvertieren. Finde heraus, was funktioniert, und baue es für dein Produkt nach.",
        "faq_q2": "Kann ich es testen, ohne zu zahlen?",
        "faq_a2": "Ja: <strong>{trial_full}</strong>. Du wechselst nur dann zu einem Abo, wenn du darüber hinaus weitermachen willst.",
        "faq_q3": "Wie funktionieren die Guthaben?",
        "faq_a3": "Ein einziger Guthabentopf, geteilt zwischen dem <strong>Hook-Studio</strong> und <strong>dem Karussell-Ersteller</strong> (1 Karussell ≈ 10 Guthaben), monatlich erneuert. Zusatzpakete gibt es ab 9 € in deinem Konto.",
        "faq_q4": "Woher kommen deine TikTok-Shop-Daten?",
        "faq_a4": "Aus echten Verkäufen der <strong>letzten 30 Tage</strong>, Land für Land. Du siehst die Creators und Produkte, die wirklich liefern — keine über den Daumen gepeilten Zahlen.",
        "faq_q5": "Kann ich jederzeit kündigen?",
        "faq_a5": "Ja, ohne Bindung. Die Kündigung wird zum Ende des laufenden Zeitraums wirksam, mit 1 Klick in deinem Stripe-Kundenportal.",
        "faq_q6": "Sind meine Produkte und Generierungen privat?",
        "faq_a6": "Ja. Deine Generierungen sind an dein Konto gebunden und werden nie geteilt. DSGVO-konformes Hosting.",

        "ft_product": "Produkt", "ft_how": "So funktioniert es", "ft_features": "Funktionen",
        "ft_faq": "FAQ", "ft_pricing": "Preise", "ft_compare": "Pläne vergleichen",
        "ft_credits": "Guthaben",
        "ft_resources": "Ressourcen",
        "ft_res1": "Ein TikTok-Shop-Video analysieren",
        "ft_res2": "Produkte, die in Frankreich verkaufen",
        "ft_res3": "Mein Video bekommt keine Aufrufe",
        "ft_res4": "Alle Artikel",
        "ft_company": "Unternehmen", "ft_about": "Über uns", "ft_blog": "Blog",
        "ft_contact": "Kontakt", "ft_affiliate": "Partner werden",
        "ft_legal": "Rechtliches", "ft_terms": "Nutzungsbedingungen",
        "ft_cgv": "Verkaufsbedingungen",
        "ft_privacy": "Datenschutz", "ft_mentions": "Impressum",
        "ft_cookies": "Cookies verwalten",
        "ft_social": "Netzwerke",
        "ft_copy": "© 2026 Qeerah - Dope Ventures. Alle Rechte vorbehalten",
        "ft_made": "Made with ❤️ in France 🇫🇷",
    },
}


# ── Langues tenues à part ────────────────────────────────────────────────────
# homepage_translations_extra.py contient les marchés préparés mais pas tous
# ouverts (Mexique, Asie-Pacifique). On ne fusionne QUE ce que `LANGS` déclare :
# ouvrir un marché de plus revient alors à l'ajouter aux cinq dictionnaires de
# configuration ci-dessus et à lui créer une route — les traductions suivent
# toutes seules. Un échec d'import ne doit pas empêcher le site de démarrer.
try:
    from homepage_translations_extra import T_EXTRA

    T.update({code: trad for code, trad in T_EXTRA.items() if code in LANGS})
except Exception as _e:  # pragma: no cover - filet au démarrage
    print(f"[i18n] traductions supplémentaires non chargées ({_e})")

# Ces marchés-là sont tous hors UE : la mention « TVA non applicable, article
# 293 B du CGI » n'a rien à y faire. `_price_block` la remplace déjà, mais on en
# fait aussi le DÉFAUT — ainsi, même si ce remplacement venait à ne pas passer,
# la page ne peut pas retomber sur une mention fiscale française.
for _code, _trad in T.items():
    if "pr_vat" not in _trad and "pr_vat_intl" in _trad:
        _trad["pr_vat"] = _trad["pr_vat_intl"]


# ── Irlande ──────────────────────────────────────────────────────────────────
# Même anglais que /en, mais l'Irlande est dans la ZONE EURO. Toute la
# différence tient au bloc prix : pas de conversion en dollars ni en livres, et
# la mention 293 B y est la bonne. D'où une variante à part entière plutôt qu'un
# simple drapeau de plus pointant vers la page américaine.
T["en-ie"] = dict(T["en"])


# ── Traduction d'une clef ────────────────────────────────────────────────────
def t(key: str, lang: str) -> str | None:
    """Traduction, ou None s'il faut garder le français du gabarit."""
    return T.get(lang, {}).get(key)


# Jetons `{...}` : le nom `trial` renvoie vers la clef `trial_offer`.
_ALIAS = {"trial": "trial_offer"}


def _fill(value: str, dvars: dict[str, str], lang: str) -> str:
    """Remplace {trial}, {trial_full}, {count}, {dims} dans une traduction.

    Priorité : traduction de la langue, puis la valeur `data-var-*` déposée par
    le gabarit (donc site_content.py). Un jeton inconnu est laissé tel quel
    plutôt que d'être effacé — un trou se voit, une accolade aussi, mais elle
    n'invente rien.
    """
    def repl(m: re.Match) -> str:
        name = m.group(1)
        traduit = t(_ALIAS.get(name, name), lang)
        if traduit is not None:
            return traduit
        return dvars.get(name, m.group(0))

    return re.sub(r"\{(\w+)\}", repl, value)


def _data_vars(open_tag: str) -> dict[str, str]:
    """Récupère les `data-var-nom="valeur"` portés par une balise ouvrante."""
    return {
        m.group(1): m.group(2)
        for m in re.finditer(r'data-var-([\w]+)="([^"]*)"', open_tag)
    }


# ── Réécriture du HTML ───────────────────────────────────────────────────────
# Le contenu d'un élément traduit ne contient jamais un élément du MÊME nom
# (vérifié dans le gabarit) : la première balise fermante correspondante est
# donc bien la bonne, et une expression régulière suffit — pas besoin d'ajouter
# une dépendance d'analyse HTML, dont une montée de version a déjà cassé la
# facturation par le passé.
_RE_TEXT = re.compile(
    r'(<(\w+)\b[^>]*\bdata-i18n="([\w]+)"[^>]*>)(.*?)(</\2>)', re.S
)
_RE_HTML = re.compile(
    r'(<(\w+)\b[^>]*\bdata-i18n-html="([\w]+)"[^>]*>)(.*?)(</\2>)', re.S
)


def _translate_bodies(html: str, lang: str) -> str:
    def repl_text(m: re.Match) -> str:
        val = t(m.group(3), lang)
        if val is None:
            return m.group(0)
        rempli = _fill(val, _data_vars(m.group(1)), lang)
        # Contenu textuel : on échappe, sauf les entités déjà écrites dans la
        # traduction (`&amp;` dans « Italy & Spain ») qu'on ne double pas.
        rempli = _html.escape(rempli, quote=False).replace("&amp;amp;", "&amp;")
        return m.group(1) + rempli + m.group(5)

    def repl_html(m: re.Match) -> str:
        val = t(m.group(3), lang)
        if val is None:
            return m.group(0)
        return m.group(1) + _fill(val, _data_vars(m.group(1)), lang) + m.group(5)

    html = _RE_HTML.sub(repl_html, html)
    html = _RE_TEXT.sub(repl_text, html)
    return html


def _translate_attr(html: str, marker: str, target: str, lang: str) -> str:
    """Traduit un attribut (placeholder, aria-label) sur les balises marquées."""
    tag_re = re.compile(r'<\w+\b[^>]*\b' + marker + r'="[\w]+"[^>]*>')

    def repl(m: re.Match) -> str:
        tag = m.group(0)
        km = re.search(marker + r'="([\w]+)"', tag)
        if not km:
            return tag
        val = t(km.group(1), lang)
        if val is None:
            return tag
        val = _html.escape(_fill(val, _data_vars(tag), lang), quote=True)
        if re.search(r'\b' + target + r'="[^"]*"', tag):
            return re.sub(
                r'\b' + target + r'="[^"]*"', lambda _: f'{target}="{val}"',
                tag, count=1,
            )
        return tag[:-1] + f' {target}="{val}">'

    return tag_re.sub(repl, html)


def chemin_langue(lang: str, chemin_fr: str = "/") -> str:
    """URL d'une page dans une langue donnée.

    Le français garde son chemin historique (`/`, `/pricing`, `/about`…) : ces
    URL sont déjà indexées, on ne les déplace pas. Les autres langues sont
    préfixées par leur code — `/en`, `/en/pricing`, `/es-mx/about`.
    """
    if lang == DEFAULT:
        return chemin_fr
    prefixe = LANG_PATHS[lang]
    return prefixe if chemin_fr == "/" else prefixe + chemin_fr


def _hreflang_block(base: str, chemin_fr: str = "/") -> str:
    """Balises `alternate` — identiques sur toutes les variantes, comme l'exige
    Google : chaque version doit se déclarer ET déclarer toutes les autres."""
    liens = "".join(
        f'  <link rel="alternate" hreflang="{HTML_LANG[l]}" '
        f'href="{base}{chemin_langue(l, chemin_fr)}">\n'
        for l in LANGS
    )
    liens += f'  <link rel="alternate" hreflang="x-default" href="{base}{chemin_fr}">\n'
    return liens


def _replace_meta(html: str, lang: str, base: str, chemin_fr: str = "/") -> str:
    """Titre, description, Open Graph, canonique et `lang` du document."""
    url = base + chemin_langue(lang, chemin_fr)

    # `lang` du document + canonique + og:url : valables pour TOUTES les langues,
    # français compris (sans quoi /en et / partageraient la même canonique et
    # Google n'indexerait qu'une seule des six).
    html = re.sub(r'<html lang="[^"]*"', f'<html lang="{HTML_LANG[lang]}"', html, count=1)
    html = re.sub(
        r'(<link rel="canonical" href=")[^"]*(">)',
        lambda m: m.group(1) + url + m.group(2), html, count=1,
    )
    html = re.sub(
        r'(<meta property="og:url" content=")[^"]*(">)',
        lambda m: m.group(1) + url + m.group(2), html, count=1,
    )
    html = re.sub(
        r'(<meta property="og:locale" content=")[^"]*(">)',
        lambda m: m.group(1) + OG_LOCALE[lang] + m.group(2), html, count=1,
    )

    titre = t("meta_title", lang)
    if titre:
        dvars = {}
        m = re.search(r'data-var-trial="([^"]*)"', html)
        if m:
            dvars["trial"] = m.group(1)

        def esc(v: str) -> str:
            return _html.escape(_fill(v, dvars, lang), quote=True)

        html = re.sub(r"<title>.*?</title>", f"<title>{esc(titre)}</title>",
                      html, count=1, flags=re.S)
        for pattern, key in (
            (r'(<meta name="description" content=")[^"]*(">)', "meta_desc"),
            (r'(<meta property="og:title" content=")[^"]*(">)', "og_title"),
            (r'(<meta property="og:description" content=")[^"]*(">)', "og_desc"),
            (r'(<meta name="twitter:title" content=")[^"]*(">)', "og_title"),
            (r'(<meta name="twitter:description" content=")[^"]*(">)', "tw_desc"),
        ):
            v = t(key, lang)
            if v:
                html = re.sub(
                    pattern,
                    lambda m, _v=esc(v): m.group(1) + _v + m.group(2),
                    html, count=1,
                )

    # Les `hreflang` s'ajoutent juste avant </head>, sur TOUTES les variantes.
    html = html.replace("</head>", _hreflang_block(base, chemin_fr) + "</head>", 1)
    return html


def _price_block(html: str, lang: str) -> str:
    """Hors zone euro : ajoute l'ordre de grandeur en devise locale et remplace
    la mention fiscale française par une formulation neutre.

    En zone euro, ne touche à rien : le prix en euros se suffit et la mention
    293 B y est la bonne."""
    if lang not in NON_EU_MARKETS:
        return html

    prix = prix_affiches(lang)
    if prix:
        gabarit = t("pr_approx", lang)
        if gabarit:
            ligne = _html.escape(
                gabarit.replace("{m}", prix[0]).replace("{y}", prix[1]),
                quote=False,
            )
            html = re.sub(
                r'(<div id="pr-approx"[^>]*>)(</div>)',
                lambda m: m.group(1) + ligne + m.group(2),
                html, count=1,
            )

    neutre = t("pr_vat_intl", lang)
    if neutre:
        html = re.sub(
            r'(<div id="pr-vat"[^>]*>).*?(</div>)',
            lambda m: m.group(1) + _html.escape(neutre, quote=False) + m.group(2),
            html, count=1, flags=re.S,
        )
    return html


def _select_current(html: str, lang: str) -> str:
    """Marque l'option courante du sélecteur (le rendu est désormais statique :
    sans `selected` écrit ici, le menu afficherait toujours « FR »)."""
    def repl(m: re.Match) -> str:
        code = m.group(1)
        return (f'<option value="{code}" selected>' if code == lang
                else f'<option value="{code}">')

    return re.sub(r'<option value="([\w-]+)"(?: selected)?>', repl, html)


def build(html_fr: str, base_url: str, chemin_fr: str = "/",
          traductions: "dict[str, dict[str, str]] | None" = None) -> dict[str, str]:
    """Fabrique une variante par langue à partir du HTML français déjà rendu.

    Générique : sert la page d'accueil comme n'importe quelle autre page du
    site. Deux paramètres suffisent à l'adapter —

      `chemin_fr`   : l'URL française de la page (« / », « /pricing »…). Les
                      autres langues en sont déduites (« /en/pricing »), ce qui
                      alimente la canonique, l'Open Graph et les hreflang.
      `traductions` : dictionnaire propre à la page. Absent → on utilise `T`,
                      celui de l'accueil.

    Toute langue qui échoue retombe sur le français : une erreur de traduction
    ne doit jamais faire tomber une page.
    """
    global _ACTIF
    pages: dict[str, str] = {}
    for lang in LANGS:
        try:
            # Dictionnaire consulté par t() le temps de fabriquer cette page.
            # build() ne tourne qu'AU DÉMARRAGE, avant que le serveur n'accepte
            # la moindre requête : pas de concurrence possible ici.
            _ACTIF = traductions if traductions is not None else T
            page = html_fr
            if lang != DEFAULT:
                page = _translate_bodies(page, lang)
                page = _translate_attr(page, "data-i18n-ph", "placeholder", lang)
                page = _translate_attr(page, "data-i18n-aria", "aria-label", lang)
            page = _price_block(page, lang)
            page = _replace_meta(page, lang, base_url, chemin_fr)
            page = _select_current(page, lang)
            page = _liens_langue(page, lang, chemin_fr)
            pages[lang] = page
        except Exception as e:  # pragma: no cover - filet de sécurité au boot
            print(f"[i18n] '{chemin_fr}' variante '{lang}' non générée ({e}) — repli français")
            pages[lang] = html_fr
        finally:
            _ACTIF = T
    return pages


def _liens_langue(html: str, lang: str, chemin_fr: str) -> str:
    """Réécrit les cibles du sélecteur pour rester sur la MÊME page.

    Sans ça, un lecteur de la page tarifs en allemand qui bascule en italien
    serait renvoyé à l'accueil italien au lieu de `/it/pricing`.
    Le gabarit expose ses cibles dans un attribut `data-chemin-fr` ; on les
    recalcule ici, une fois pour toutes, au démarrage.
    """
    if chemin_fr == "/":
        return html   # l'accueil utilise déjà les chemins par défaut

    def repl(m: re.Match) -> str:
        code = m.group(1)
        if code not in LANG_PATHS:
            return m.group(0)
        return f'<option value="{code}" data-url="{chemin_langue(code, chemin_fr)}"'

    return re.sub(r'<option value="([\w-]+)"', repl, html)


def match_accept_language(header: str) -> str | None:
    """Langue préférée du navigateur parmi celles servies, sinon None.

    Sert uniquement à PROPOSER une redirection depuis « / » ; on ne redirige
    jamais un robot ni de force — Google demande que chaque URL reste
    accessible telle quelle.
    """
    if not header:
        return None
    for morceau in header.split(","):
        code = morceau.split(";")[0].strip().lower()
        if not code:
            continue
        if code in LANG_PATHS:
            return code
        if code.startswith("pt"):
            return "pt-br"
        base = code.split("-")[0]
        if base in LANG_PATHS:
            return base
    return None
