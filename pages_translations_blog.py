"""Traductions du BLOG — index et articles.

Même réserve que pour les pages d'atterrissage (pages_translations_seo.py) :
ces articles ont été écrits pour un lectorat francophone et gardent leur URL
française. La traduction rend le blog lisible dans chaque langue ; elle ne
remplace pas, à terme, des articles pensés pour chaque marché.

Deux règles suivies ici :

  • les chiffres, dates et sources ne bougent pas — ils sont hors des clefs
    (`{0}`) et réinjectés tels quels. Un article qui cite une étude doit citer
    la même dans les huit langues ;
  • les noms propres (créateurs, plateformes, entreprises, pays cités comme
    marchés) restent tels quels. Traduire un nom de compte le rend introuvable.
"""
from __future__ import annotations

# ═══════════════════════════════════════════════════════════════════════════
# /blog — l'index
# ═══════════════════════════════════════════════════════════════════════════
T_BLOG: dict[str, dict[str, str]] = {}

T_BLOG["en"] = {
    "Blog TikTok Shop — conseils, chiffres et stratégies - Qeerah":
        "TikTok Shop blog — advice, figures and strategy - Qeerah",
    "Blog Qeerah - Articles sur TikTok Shop, tendances, stratégies et success stories":
        "Qeerah blog — articles on TikTok Shop: trends, strategy and success stories",
    "Blog TikTok Shop — conseils, chiffres et stratégies": "TikTok Shop blog — advice, figures and strategy",
    "Articles sourcés sur TikTok Shop : marchés ouverts, chiffres de ventes, tendances, stratégies et success stories de créateurs.":
        "Sourced articles on TikTok Shop: open markets, sales figures, trends, strategy and creator success stories.",
    "← Retour à l'accueil": "← Back to home",
    "📚 Blog Qeerah": "📚 Qeerah blog",
    "Conseils, tendances et stratégies pour réussir sur TikTok Shop":
        "Advice, trends and strategy for doing well on TikTok Shop",
    "💡 GUIDE TIKTOK SHOP": "💡 TIKTOK SHOP GUIDE",
    "TikTok Shop : c'est quoi, et peut-on vraiment gagner de l'argent avec ?":
        "TikTok Shop: what is it, and can you really make money with it?",
    "📅 Juillet {0}": "📅 July {0}",
    "⏱️ {0} min de lecture": "⏱️ {0} min read",
    "Ce qu'est TikTok Shop, comment ça marche, dans quels pays c'est disponible, et si on peut vraiment en vivre : chiffres, pays ouverts et créateurs millionnaires, sources à l'appui.":
        "What TikTok Shop is, how it works, which countries have it, and whether you can really live off it: figures, open markets and millionaire creators, with sources.",
    "Lire l'article →": "Read the article →",
    "📖 HISTOIRE": "📖 HISTORY",
    "L'histoire complète de TikTok Shop : Du lancement global à la domination française":
        "The full story of TikTok Shop: from global launch to dominating France",
    "📅 Mis à jour mai {0}": "📅 Updated May {0}",
    "Découvrez comment TikTok Shop est passé d'une expérience asiatique à une révolution mondiale du e-commerce. Nous retraçons le parcours depuis le lancement en {0} jusqu'à sa domination en France en {1}.":
        "How TikTok Shop went from an Asian experiment to a worldwide shake-up of e-commerce. We trace the path from the {0} launch to its grip on France in {1}.",
    "💰 SUCCESS STORIES": "💰 SUCCESS STORIES",
    "{0} créateurs TikTok Shop devenus millionnaires en {1}":
        "{0} TikTok Shop creators who became millionaires in {1}",
    "📅 Publié avril {0}": "📅 Published April {0}",
    "Analysez les success stories de créateurs qui ont transformé leurs vidéos virales en empires commerciaux. Découvrez leurs secrets, leurs stratégies et ce que vous pouvez en apprendre.":
        "A look at creators who turned viral videos into commercial empires. What they did, how they did it, and what you can take from it.",
    "🔮 TENDANCES": "🔮 TRENDS",
    "Top {0} des tendances TikTok Shop {1} qui vont dominer":
        "The top {0} TikTok Shop trends set to dominate {1}",
    "Les tendances évoluent rapidement sur TikTok. Découvrez les {0} tendances qui définissent le e-commerce sur la plateforme en {1} et comment les utiliser pour vos vidéos.":
        "Trends move fast on TikTok. Here are the {0} shaping commerce on the platform in {1}, and how to use them in your videos.",
    "📖 GUIDE": "📖 GUIDE",
    "Guide complet : Structurer sa stratégie TikTok Shop en {0}":
        "Complete guide: building your TikTok Shop strategy in {0}",
    "📅 Publié mars {0}": "📅 Published March {0}",
    "Un guide détaillé pour construire une stratégie TikTok Shop de A à Z. Couvrez le positionnement, la création de contenu, l'optimisation et la monétisation.":
        "A detailed guide to building a TikTok Shop strategy from scratch: positioning, making content, tightening it up, and earning from it.",
}

T_BLOG["de"] = {
    "Blog TikTok Shop — conseils, chiffres et stratégies - Qeerah":
        "TikTok-Shop-Blog — Tipps, Zahlen und Strategie - Qeerah",
    "Blog Qeerah - Articles sur TikTok Shop, tendances, stratégies et success stories":
        "Qeerah-Blog — Artikel über TikTok Shop: Trends, Strategien und Erfolgsgeschichten",
    "Blog TikTok Shop — conseils, chiffres et stratégies": "TikTok-Shop-Blog — Tipps, Zahlen und Strategie",
    "Articles sourcés sur TikTok Shop : marchés ouverts, chiffres de ventes, tendances, stratégies et success stories de créateurs.":
        "Belegte Artikel über TikTok Shop: offene Märkte, Verkaufszahlen, Trends, Strategien und Erfolgsgeschichten von Creators.",
    "← Retour à l'accueil": "← Zurück zur Startseite",
    "📚 Blog Qeerah": "📚 Qeerah-Blog",
    "Conseils, tendances et stratégies pour réussir sur TikTok Shop":
        "Tipps, Trends und Strategien, um auf TikTok Shop weiterzukommen",
    "💡 GUIDE TIKTOK SHOP": "💡 TIKTOK-SHOP-GUIDE",
    "TikTok Shop : c'est quoi, et peut-on vraiment gagner de l'argent avec ?":
        "TikTok Shop: Was ist das, und kann man damit wirklich Geld verdienen?",
    "📅 Juillet {0}": "📅 Juli {0}",
    "⏱️ {0} min de lecture": "⏱️ {0} Min. Lesezeit",
    "Ce qu'est TikTok Shop, comment ça marche, dans quels pays c'est disponible, et si on peut vraiment en vivre : chiffres, pays ouverts et créateurs millionnaires, sources à l'appui.":
        "Was TikTok Shop ist, wie es funktioniert, in welchen Ländern es verfügbar ist und ob man davon leben kann: Zahlen, offene Märkte und Millionen-Creators, mit Quellen.",
    "Lire l'article →": "Artikel lesen →",
    "📖 HISTOIRE": "📖 GESCHICHTE",
    "L'histoire complète de TikTok Shop : Du lancement global à la domination française":
        "Die ganze Geschichte von TikTok Shop: vom weltweiten Start bis zur Vorherrschaft in Frankreich",
    "📅 Mis à jour mai {0}": "📅 Aktualisiert im Mai {0}",
    "Découvrez comment TikTok Shop est passé d'une expérience asiatique à une révolution mondiale du e-commerce. Nous retraçons le parcours depuis le lancement en {0} jusqu'à sa domination en France en {1}.":
        "Wie TikTok Shop von einem asiatischen Versuch zu einem weltweiten Umbruch im E-Commerce wurde. Wir zeichnen den Weg vom Start {0} bis zur Vorherrschaft in Frankreich {1} nach.",
    "💰 SUCCESS STORIES": "💰 ERFOLGSGESCHICHTEN",
    "{0} créateurs TikTok Shop devenus millionnaires en {1}":
        "{0} TikTok-Shop-Creators, die {1} Millionäre wurden",
    "📅 Publié avril {0}": "📅 Veröffentlicht im April {0}",
    "Analysez les success stories de créateurs qui ont transformé leurs vidéos virales en empires commerciaux. Découvrez leurs secrets, leurs stratégies et ce que vous pouvez en apprendre.":
        "Ein Blick auf Creators, die virale Videos in Handelsimperien verwandelt haben. Was sie getan haben, wie sie es getan haben, und was du daraus mitnimmst.",
    "🔮 TENDANCES": "🔮 TRENDS",
    "Top {0} des tendances TikTok Shop {1} qui vont dominer":
        "Die Top {0} TikTok-Shop-Trends, die {1} bestimmen werden",
    "Les tendances évoluent rapidement sur TikTok. Découvrez les {0} tendances qui définissent le e-commerce sur la plateforme en {1} et comment les utiliser pour vos vidéos.":
        "Trends drehen sich auf TikTok schnell. Hier sind die {0}, die den Handel auf der Plattform {1} prägen — und wie du sie in deinen Videos nutzt.",
    "📖 GUIDE": "📖 GUIDE",
    "Guide complet : Structurer sa stratégie TikTok Shop en {0}":
        "Kompletter Guide: deine TikTok-Shop-Strategie {0} aufbauen",
    "📅 Publié mars {0}": "📅 Veröffentlicht im März {0}",
    "Un guide détaillé pour construire une stratégie TikTok Shop de A à Z. Couvrez le positionnement, la création de contenu, l'optimisation et la monétisation.":
        "Ein ausführlicher Guide, um eine TikTok-Shop-Strategie von Grund auf zu bauen: Positionierung, Inhalte, Feinschliff und Monetarisierung.",
}

T_BLOG["es"] = {
    "Blog TikTok Shop — conseils, chiffres et stratégies - Qeerah":
        "Blog de TikTok Shop — consejos, cifras y estrategia - Qeerah",
    "Blog Qeerah - Articles sur TikTok Shop, tendances, stratégies et success stories":
        "Blog de Qeerah — artículos sobre TikTok Shop: tendencias, estrategias e historias de éxito",
    "Blog TikTok Shop — conseils, chiffres et stratégies": "Blog de TikTok Shop — consejos, cifras y estrategia",
    "Articles sourcés sur TikTok Shop : marchés ouverts, chiffres de ventes, tendances, stratégies et success stories de créateurs.":
        "Artículos con fuentes sobre TikTok Shop: mercados abiertos, cifras de ventas, tendencias, estrategias e historias de éxito de creadores.",
    "← Retour à l'accueil": "← Volver al inicio",
    "📚 Blog Qeerah": "📚 Blog de Qeerah",
    "Conseils, tendances et stratégies pour réussir sur TikTok Shop":
        "Consejos, tendencias y estrategias para funcionar en TikTok Shop",
    "💡 GUIDE TIKTOK SHOP": "💡 GUÍA DE TIKTOK SHOP",
    "TikTok Shop : c'est quoi, et peut-on vraiment gagner de l'argent avec ?":
        "TikTok Shop: qué es y si de verdad se puede ganar dinero con ello",
    "📅 Juillet {0}": "📅 Julio de {0}",
    "⏱️ {0} min de lecture": "⏱️ {0} min de lectura",
    "Ce qu'est TikTok Shop, comment ça marche, dans quels pays c'est disponible, et si on peut vraiment en vivre : chiffres, pays ouverts et créateurs millionnaires, sources à l'appui.":
        "Qué es TikTok Shop, cómo funciona, en qué países está disponible y si de verdad se puede vivir de ello: cifras, mercados abiertos y creadores millonarios, con fuentes.",
    "Lire l'article →": "Leer el artículo →",
    "📖 HISTOIRE": "📖 HISTORIA",
    "L'histoire complète de TikTok Shop : Du lancement global à la domination française":
        "La historia completa de TikTok Shop: del lanzamiento global al dominio en Francia",
    "📅 Mis à jour mai {0}": "📅 Actualizado en mayo de {0}",
    "Découvrez comment TikTok Shop est passé d'une expérience asiatique à une révolution mondiale du e-commerce. Nous retraçons le parcours depuis le lancement en {0} jusqu'à sa domination en France en {1}.":
        "Cómo TikTok Shop pasó de ser un experimento asiático a una revolución mundial del comercio electrónico. Recorremos el camino desde el lanzamiento en {0} hasta su dominio en Francia en {1}.",
    "💰 SUCCESS STORIES": "💰 HISTORIAS DE ÉXITO",
    "{0} créateurs TikTok Shop devenus millionnaires en {1}":
        "{0} creadores de TikTok Shop que se hicieron millonarios en {1}",
    "📅 Publié avril {0}": "📅 Publicado en abril de {0}",
    "Analysez les success stories de créateurs qui ont transformé leurs vidéos virales en empires commerciaux. Découvrez leurs secrets, leurs stratégies et ce que vous pouvez en apprendre.":
        "Un repaso a creadores que convirtieron vídeos virales en imperios comerciales. Qué hicieron, cómo lo hicieron y qué puedes aprender de ello.",
    "🔮 TENDANCES": "🔮 TENDENCIAS",
    "Top {0} des tendances TikTok Shop {1} qui vont dominer":
        "Las {0} tendencias de TikTok Shop que van a dominar {1}",
    "Les tendances évoluent rapidement sur TikTok. Découvrez les {0} tendances qui définissent le e-commerce sur la plateforme en {1} et comment les utiliser pour vos vidéos.":
        "Las tendencias cambian rápido en TikTok. Estas son las {0} que definen el comercio en la plataforma en {1} y cómo usarlas en tus vídeos.",
    "📖 GUIDE": "📖 GUÍA",
    "Guide complet : Structurer sa stratégie TikTok Shop en {0}":
        "Guía completa: montar tu estrategia de TikTok Shop en {0}",
    "📅 Publié mars {0}": "📅 Publicado en marzo de {0}",
    "Un guide détaillé pour construire une stratégie TikTok Shop de A à Z. Couvrez le positionnement, la création de contenu, l'optimisation et la monétisation.":
        "Una guía detallada para construir una estrategia de TikTok Shop desde cero: posicionamiento, creación de contenido, optimización y monetización.",
}

T_BLOG["it"] = {
    "Blog TikTok Shop — conseils, chiffres et stratégies - Qeerah":
        "Blog TikTok Shop — consigli, numeri e strategia - Qeerah",
    "Blog Qeerah - Articles sur TikTok Shop, tendances, stratégies et success stories":
        "Blog Qeerah — articoli su TikTok Shop: tendenze, strategie e storie di successo",
    "Blog TikTok Shop — conseils, chiffres et stratégies": "Blog TikTok Shop — consigli, numeri e strategia",
    "Articles sourcés sur TikTok Shop : marchés ouverts, chiffres de ventes, tendances, stratégies et success stories de créateurs.":
        "Articoli con fonti su TikTok Shop: mercati aperti, numeri di vendita, tendenze, strategie e storie di successo dei creator.",
    "← Retour à l'accueil": "← Torna alla home",
    "📚 Blog Qeerah": "📚 Blog Qeerah",
    "Conseils, tendances et stratégies pour réussir sur TikTok Shop":
        "Consigli, tendenze e strategie per andare bene su TikTok Shop",
    "💡 GUIDE TIKTOK SHOP": "💡 GUIDA A TIKTOK SHOP",
    "TikTok Shop : c'est quoi, et peut-on vraiment gagner de l'argent avec ?":
        "TikTok Shop: cos'è e si può davvero guadagnarci?",
    "📅 Juillet {0}": "📅 Luglio {0}",
    "⏱️ {0} min de lecture": "⏱️ {0} min di lettura",
    "Ce qu'est TikTok Shop, comment ça marche, dans quels pays c'est disponible, et si on peut vraiment en vivre : chiffres, pays ouverts et créateurs millionnaires, sources à l'appui.":
        "Cos'è TikTok Shop, come funziona, in quali paesi è disponibile e se ci si può davvero vivere: numeri, mercati aperti e creator milionari, con le fonti.",
    "Lire l'article →": "Leggi l'articolo →",
    "📖 HISTOIRE": "📖 STORIA",
    "L'histoire complète de TikTok Shop : Du lancement global à la domination française":
        "La storia completa di TikTok Shop: dal lancio globale al dominio in Francia",
    "📅 Mis à jour mai {0}": "📅 Aggiornato a maggio {0}",
    "Découvrez comment TikTok Shop est passé d'une expérience asiatique à une révolution mondiale du e-commerce. Nous retraçons le parcours depuis le lancement en {0} jusqu'à sa domination en France en {1}.":
        "Come TikTok Shop è passato da esperimento asiatico a rivoluzione mondiale dell'e-commerce. Ripercorriamo il percorso dal lancio nel {0} fino al dominio in Francia nel {1}.",
    "💰 SUCCESS STORIES": "💰 STORIE DI SUCCESSO",
    "{0} créateurs TikTok Shop devenus millionnaires en {1}":
        "{0} creator di TikTok Shop diventati milionari nel {1}",
    "📅 Publié avril {0}": "📅 Pubblicato ad aprile {0}",
    "Analysez les success stories de créateurs qui ont transformé leurs vidéos virales en empires commerciaux. Découvrez leurs secrets, leurs stratégies et ce que vous pouvez en apprendre.":
        "Uno sguardo ai creator che hanno trasformato video virali in imperi commerciali. Cosa hanno fatto, come, e cosa puoi portarti a casa.",
    "🔮 TENDANCES": "🔮 TENDENZE",
    "Top {0} des tendances TikTok Shop {1} qui vont dominer":
        "Le {0} tendenze TikTok Shop che domineranno il {1}",
    "Les tendances évoluent rapidement sur TikTok. Découvrez les {0} tendances qui définissent le e-commerce sur la plateforme en {1} et comment les utiliser pour vos vidéos.":
        "Le tendenze su TikTok cambiano in fretta. Ecco le {0} che definiscono il commercio sulla piattaforma nel {1} e come usarle nei tuoi video.",
    "📖 GUIDE": "📖 GUIDA",
    "Guide complet : Structurer sa stratégie TikTok Shop en {0}":
        "Guida completa: costruire la tua strategia TikTok Shop nel {0}",
    "📅 Publié mars {0}": "📅 Pubblicato a marzo {0}",
    "Un guide détaillé pour construire une stratégie TikTok Shop de A à Z. Couvrez le positionnement, la création de contenu, l'optimisation et la monétisation.":
        "Una guida dettagliata per costruire una strategia TikTok Shop da zero: posizionamento, creazione di contenuti, ottimizzazione e monetizzazione.",
}

T_BLOG["pt-br"] = {
    "Blog TikTok Shop — conseils, chiffres et stratégies - Qeerah":
        "Blog TikTok Shop — dicas, números e estratégia - Qeerah",
    "Blog Qeerah - Articles sur TikTok Shop, tendances, stratégies et success stories":
        "Blog da Qeerah — artigos sobre TikTok Shop: tendências, estratégias e histórias de sucesso",
    "Blog TikTok Shop — conseils, chiffres et stratégies": "Blog TikTok Shop — dicas, números e estratégia",
    "Articles sourcés sur TikTok Shop : marchés ouverts, chiffres de ventes, tendances, stratégies et success stories de créateurs.":
        "Artigos com fontes sobre TikTok Shop: mercados abertos, números de vendas, tendências, estratégias e histórias de sucesso de criadores.",
    "← Retour à l'accueil": "← Voltar ao início",
    "📚 Blog Qeerah": "📚 Blog da Qeerah",
    "Conseils, tendances et stratégies pour réussir sur TikTok Shop":
        "Dicas, tendências e estratégias para ir bem no TikTok Shop",
    "💡 GUIDE TIKTOK SHOP": "💡 GUIA DO TIKTOK SHOP",
    "TikTok Shop : c'est quoi, et peut-on vraiment gagner de l'argent avec ?":
        "TikTok Shop: o que é e dá mesmo para ganhar dinheiro com isso?",
    "📅 Juillet {0}": "📅 Julho de {0}",
    "⏱️ {0} min de lecture": "⏱️ {0} min de leitura",
    "Ce qu'est TikTok Shop, comment ça marche, dans quels pays c'est disponible, et si on peut vraiment en vivre : chiffres, pays ouverts et créateurs millionnaires, sources à l'appui.":
        "O que é o TikTok Shop, como funciona, em quais países está disponível e se dá mesmo para viver disso: números, mercados abertos e criadores milionários, com fontes.",
    "Lire l'article →": "Ler o artigo →",
    "📖 HISTOIRE": "📖 HISTÓRIA",
    "L'histoire complète de TikTok Shop : Du lancement global à la domination française":
        "A história completa do TikTok Shop: do lançamento global ao domínio na França",
    "📅 Mis à jour mai {0}": "📅 Atualizado em maio de {0}",
    "Découvrez comment TikTok Shop est passé d'une expérience asiatique à une révolution mondiale du e-commerce. Nous retraçons le parcours depuis le lancement en {0} jusqu'à sa domination en France en {1}.":
        "Como o TikTok Shop passou de experimento asiático a uma virada mundial no e-commerce. A gente refaz o caminho do lançamento em {0} até o domínio na França em {1}.",
    "💰 SUCCESS STORIES": "💰 HISTÓRIAS DE SUCESSO",
    "{0} créateurs TikTok Shop devenus millionnaires en {1}":
        "{0} criadores do TikTok Shop que viraram milionários em {1}",
    "📅 Publié avril {0}": "📅 Publicado em abril de {0}",
    "Analysez les success stories de créateurs qui ont transformé leurs vidéos virales en empires commerciaux. Découvrez leurs secrets, leurs stratégies et ce que vous pouvez en apprendre.":
        "Um olhar sobre criadores que transformaram vídeos virais em impérios comerciais. O que fizeram, como fizeram e o que dá para aprender com isso.",
    "🔮 TENDANCES": "🔮 TENDÊNCIAS",
    "Top {0} des tendances TikTok Shop {1} qui vont dominer":
        "As {0} tendências do TikTok Shop que vão dominar {1}",
    "Les tendances évoluent rapidement sur TikTok. Découvrez les {0} tendances qui définissent le e-commerce sur la plateforme en {1} et comment les utiliser pour vos vidéos.":
        "As tendências mudam rápido no TikTok. Estas são as {0} que definem o comércio na plataforma em {1} e como usá-las nos seus vídeos.",
    "📖 GUIDE": "📖 GUIA",
    "Guide complet : Structurer sa stratégie TikTok Shop en {0}":
        "Guia completo: montar sua estratégia de TikTok Shop em {0}",
    "📅 Publié mars {0}": "📅 Publicado em março de {0}",
    "Un guide détaillé pour construire une stratégie TikTok Shop de A à Z. Couvrez le positionnement, la création de contenu, l'optimisation et la monétisation.":
        "Um guia detalhado para construir uma estratégia de TikTok Shop do zero: posicionamento, criação de conteúdo, otimização e monetização.",
}

T_BLOG["en-ie"] = dict(T_BLOG["en"])
T_BLOG["es-mx"] = dict(T_BLOG["es"])


# ═══════════════════════════════════════════════════════════════════════════
# /blog/tendances-2026
# Les intitulés de tendance sont déjà en anglais dans l'original français
# (« Ultra-Micro Content », « Loop Stories »…) : ce sont des étiquettes du
# métier, on les garde partout plutôt que d'inventer un équivalent local.
# ═══════════════════════════════════════════════════════════════════════════
T_BLOG_TENDANCES: dict[str, dict[str, str]] = {}

T_BLOG_TENDANCES["en"] = {
    "Top {0} Tendances TikTok Shop {1} - Qeerah": "Top {0} TikTok Shop trends for {1} - Qeerah",
    "Top {0} des tendances TikTok Shop {1} qui vont dominer. Découvrez ce qui fonctionne et comment l'utiliser dans votre stratégie.":
        "The top {0} TikTok Shop trends set to dominate {1}. What works, and how to use it in your own strategy.",
    "Les {0} tendances qui définissent le e-commerce sur TikTok en {1}, et comment les utiliser concrètement dans vos vidéos.":
        "The {0} trends shaping commerce on TikTok in {1}, and how to put them to work in your videos.",
    "← Retour au blog": "← Back to the blog",
    "🔮 TENDANCES": "🔮 TRENDS",
    "Top {0} des tendances TikTok Shop {1} qui vont dominer":
        "The top {0} TikTok Shop trends set to dominate {1}",
    "Le paysage de TikTok Shop change constamment. Voici les {0} tendances qui dominent le marché en {1} et comment les exploiter pour votre croissance.":
        "The TikTok Shop landscape keeps shifting. Here are the {0} trends running the market in {1}, and how to use them to grow.",
    "{0}. 🎬 Ultra-Micro Content (UMC)": "{0}. 🎬 Ultra-Micro Content (UMC)",
    "Des vidéos de {0}-{1} secondes extrêmement punchy. Plus courtes que TikTok \"normal\", ultra-concentrated. Les créateurs testent {2}x plus de content.":
        "Videos of {0}-{1} seconds, extremely punchy. Shorter than “normal” TikTok, highly concentrated. Creators test {2}× more content.",
    "Comment l'utiliser :": "How to use it:",
    "Divisez vos vidéos en clips de {0}-{1} sec. Testez des dizaines de versions. Gardez seulement les top {2}%.":
        "Cut your videos into {0}-{1} second clips. Test dozens of versions. Keep only the top {2}%.",
    "{0}. 💬 \"Tell\" vs \"Show\"": "{0}. 💬 “Tell” vs “Show”",
    "Les créateurs gagnants parlent directement à la caméra. Plus de montage complexe, juste de la conversation honnête.":
        "The creators who win talk straight to camera. No elaborate editing, just honest conversation.",
    "Enregistrez vous en parlant naturellement. Pas de script. Juste vous, votre produit, et votre opinion.":
        "Record yourself talking naturally. No script. Just you, your product, and what you think of it.",
    "{0}. 🤝 \"Duets de produit\"": "{0}. 🤝 “Product duets”",
    "Créateurs qui réagissent aux vidéos d'autres créateurs en vendant \"contre-produit\" ou complément.":
        "Creators reacting to other creators' videos, selling either a counter-product or a complement.",
    "Surveillez les trends de votre niche. Créez des vidéos de réaction/amélioration.":
        "Watch the trends in your niche. Make reaction or one-better videos.",
    "{0}. 📊 \"Data-Backed Content\"": "{0}. 📊 “Data-backed content”",
    "Créateurs qui montrent les chiffres : \"{0}% des gens préfèrent...\", \"Mon audience m'a votée pour...\". Crédibilité extrême.":
        "Creators who show the numbers: “{0}% of people prefer…”, “my audience voted for…”. Enormous credibility.",
    "Collectez les feedbacks, créez des sondages, montrez les résultats. Les gens ADORENT voir les chiffres.":
        "Collect feedback, run polls, show the results. People LOVE seeing numbers.",
    "{0}. 🎯 \"Segment-Specific Content\"": "{0}. 🎯 “Segment-specific content”",
    "Au lieu de contenu générique, créateurs font des versions spécifiques : \"Pour les hommes\", \"Pour les mères\", \"Pour les freelancers\".":
        "Instead of generic content, creators make targeted versions: “for men”, “for mums”, “for freelancers”.",
    "Identifiez vos {0}-{1} segments clés. Créez du contenu adapté pour chacun.":
        "Identify your {0}-{1} key segments. Make content shaped for each one.",
    "{0}. 🔄 \"Loop Stories\"": "{0}. 🔄 “Loop stories”",
    "Vidéos qui boucles après {0} secondes avec des variations. Plus tu la regardes, plus tu vois de perspectives différentes.":
        "Videos that loop after {0} seconds with variations. The more you watch, the more you notice.",
    "Testez des hooks qui créent de la boucle naturelle. Les gens re-regardent = plus d'algorithme.":
        "Test hooks that create a natural loop. People rewatch = more algorithm.",
    "{0}. 💎 \"Scarcity + Authenticity\"": "{0}. 💎 “Scarcity + authenticity”",
    "\"Je n'en ai que {0} gauche\" combiné avec \"C'est mon dernier stock de celui-ci\". L'urgence combinée à l'honnêteté.":
        "“I've only got {0} left” combined with “this is my last stock of it”. Urgency paired with honesty.",
    "Montrez vraiment les limites. Soyez honnête sur les stocks. L'urgence authentique convertit {0}x mieux.":
        "Show the real limits. Be honest about stock. Genuine urgency converts {0}× better.",
    "{0}. 👥 \"Community-Driven Proof\"": "{0}. 👥 “Community-driven proof”",
    "Au lieu de testimonials statiques, créateurs montrent les vraies utilisations par d'autres utilisateurs. User-generated content à grande échelle.":
        "Instead of static testimonials, creators show real use by other customers. User-generated content at scale.",
    "Encouragez vos clients à créer du contenu avec vos produits. Répostez le meilleur. C'est TRÈS puissant.":
        "Get your customers making content with your products. Repost the best of it. It works extremely well.",
    "{0}. ⚡ \"Instant Gratification\"": "{0}. ⚡ “Instant gratification”",
    "Vidéos montrant les résultats IMMÉDIATEMENT. \"Voici avant/après en {0} secondes\". Pas d'attente.":
        "Videos showing the result IMMEDIATELY. “Here's before and after in {0} seconds.” No waiting.",
    "Si ton produit permet des résultats rapides, mets ça en avant. Si non, crée l'expectation de vitesse d'une autre façon.":
        "If your product delivers fast, lead with it. If it doesn't, create the sense of speed some other way.",
    "{0}. 🎭 \"Personality-Driven Sales\"": "{0}. 🎭 “Personality-driven sales”",
    "Les gens n'achètent pas les produits, ils achètent les créateurs. La personnalité EST le produit.":
        "People don't buy products, they buy creators. The personality IS the product.",
    "Montrez-vous plus. Vos opinions, votre sens de l'humour, vos croyances. Moins de \"produit\", plus de \"toi\".":
        "Show more of yourself. Your opinions, your humour, what you believe. Less “product”, more “you”.",
    "🎯 La Meta-Tendance : \"Menos es Más\"": "🎯 The meta-trend: less is more",
    "Observe attentivement : les {0} tendances ci-dessus convergen vers une seule chose :":
        "Look closely: the {0} trends above all point to one thing —",
    "plus simple, plus honnête, plus rapide": "simpler, more honest, faster",
    "Les créateurs gagnants en {0} ne sont pas ceux avec les meilleurs studios ou les vidéos les plus complexes. Ce sont ceux qui comprennent que le spectateur de TikTok veut de l'authenticité brute, pas de la perfection produite.":
        "The creators winning in {0} aren't the ones with the best studios or the most elaborate videos. They're the ones who understand that a TikTok viewer wants raw authenticity, not produced perfection.",
    "Analysez vos tendances maintenant": "Check your videos against these trends",
    "Utilisez Qeerah pour voir si vos vidéos suivent ces tendances {0}.":
        "Use Qeerah to see whether your videos follow these {0} trends.",
    "Analyser vos vidéos →": "Analyse your videos →",
}

T_BLOG_TENDANCES["de"] = {
    "Top {0} Tendances TikTok Shop {1} - Qeerah": "Top {0} TikTok-Shop-Trends {1} - Qeerah",
    "Top {0} des tendances TikTok Shop {1} qui vont dominer. Découvrez ce qui fonctionne et comment l'utiliser dans votre stratégie.":
        "Die Top {0} TikTok-Shop-Trends, die {1} bestimmen werden. Was funktioniert, und wie du es in deiner Strategie einsetzt.",
    "Les {0} tendances qui définissent le e-commerce sur TikTok en {1}, et comment les utiliser concrètement dans vos vidéos.":
        "Die {0} Trends, die den Handel auf TikTok {1} prägen — und wie du sie konkret in deinen Videos nutzt.",
    "← Retour au blog": "← Zurück zum Blog",
    "🔮 TENDANCES": "🔮 TRENDS",
    "Top {0} des tendances TikTok Shop {1} qui vont dominer": "Die Top {0} TikTok-Shop-Trends, die {1} bestimmen werden",
    "Le paysage de TikTok Shop change constamment. Voici les {0} tendances qui dominent le marché en {1} et comment les exploiter pour votre croissance.":
        "Die Landschaft von TikTok Shop verschiebt sich ständig. Hier sind die {0} Trends, die den Markt {1} bestimmen, und wie du sie für dein Wachstum nutzt.",
    "{0}. 🎬 Ultra-Micro Content (UMC)": "{0}. 🎬 Ultra-Micro Content (UMC)",
    "Des vidéos de {0}-{1} secondes extrêmement punchy. Plus courtes que TikTok \"normal\", ultra-concentrated. Les créateurs testent {2}x plus de content.":
        "Videos von {0}-{1} Sekunden, extrem knackig. Kürzer als „normales“ TikTok, hochkonzentriert. Creators testen {2}× so viele Inhalte.",
    "Comment l'utiliser :": "So setzt du es ein:",
    "Divisez vos vidéos en clips de {0}-{1} sec. Testez des dizaines de versions. Gardez seulement les top {2}%.":
        "Zerleg deine Videos in Clips von {0}-{1} Sekunden. Teste Dutzende Fassungen. Behalte nur die besten {2} %.",
    "{0}. 💬 \"Tell\" vs \"Show\"": "{0}. 💬 „Tell“ statt „Show“",
    "Les créateurs gagnants parlent directement à la caméra. Plus de montage complexe, juste de la conversation honnête.":
        "Die Creators, die gewinnen, sprechen direkt in die Kamera. Kein aufwendiger Schnitt, einfach ehrliches Reden.",
    "Enregistrez vous en parlant naturellement. Pas de script. Juste vous, votre produit, et votre opinion.":
        "Nimm dich auf, während du normal redest. Kein Skript. Nur du, dein Produkt und deine Meinung.",
    "{0}. 🤝 \"Duets de produit\"": "{0}. 🤝 „Produkt-Duette“",
    "Créateurs qui réagissent aux vidéos d'autres créateurs en vendant \"contre-produit\" ou complément.":
        "Creators reagieren auf Videos anderer Creators und verkaufen dabei ein Gegen- oder Ergänzungsprodukt.",
    "Surveillez les trends de votre niche. Créez des vidéos de réaction/amélioration.":
        "Beobachte die Trends deiner Nische. Mach Reaktions- oder Besser-Videos.",
    "{0}. 📊 \"Data-Backed Content\"": "{0}. 📊 „Data-Backed Content“",
    "Créateurs qui montrent les chiffres : \"{0}% des gens préfèrent...\", \"Mon audience m'a votée pour...\". Crédibilité extrême.":
        "Creators, die Zahlen zeigen: „{0} % der Leute bevorzugen …“, „meine Community hat für … gestimmt“. Enorme Glaubwürdigkeit.",
    "Collectez les feedbacks, créez des sondages, montrez les résultats. Les gens ADORENT voir les chiffres.":
        "Sammle Rückmeldungen, mach Umfragen, zeig die Ergebnisse. Die Leute LIEBEN Zahlen.",
    "{0}. 🎯 \"Segment-Specific Content\"": "{0}. 🎯 „Segment-Specific Content“",
    "Au lieu de contenu générique, créateurs font des versions spécifiques : \"Pour les hommes\", \"Pour les mères\", \"Pour les freelancers\".":
        "Statt generischer Inhalte machen Creators gezielte Fassungen: „für Männer“, „für Mütter“, „für Selbstständige“.",
    "Identifiez vos {0}-{1} segments clés. Créez du contenu adapté pour chacun.":
        "Finde deine {0}-{1} wichtigsten Segmente. Mach für jedes passende Inhalte.",
    "{0}. 🔄 \"Loop Stories\"": "{0}. 🔄 „Loop Stories“",
    "Vidéos qui boucles après {0} secondes avec des variations. Plus tu la regardes, plus tu vois de perspectives différentes.":
        "Videos, die nach {0} Sekunden mit Variationen von vorn laufen. Je öfter du schaust, desto mehr fällt dir auf.",
    "Testez des hooks qui créent de la boucle naturelle. Les gens re-regardent = plus d'algorithme.":
        "Teste Hooks, die eine natürliche Schleife erzeugen. Leute schauen erneut = mehr Algorithmus.",
    "{0}. 💎 \"Scarcity + Authenticity\"": "{0}. 💎 „Knappheit + Ehrlichkeit“",
    "\"Je n'en ai que {0} gauche\" combiné avec \"C'est mon dernier stock de celui-ci\". L'urgence combinée à l'honnêteté.":
        "„Ich habe nur noch {0} übrig“ zusammen mit „das ist mein letzter Bestand davon“. Dringlichkeit gepaart mit Ehrlichkeit.",
    "Montrez vraiment les limites. Soyez honnête sur les stocks. L'urgence authentique convertit {0}x mieux.":
        "Zeig die echten Grenzen. Sei ehrlich beim Bestand. Echte Dringlichkeit konvertiert {0}× besser.",
    "{0}. 👥 \"Community-Driven Proof\"": "{0}. 👥 „Community-Driven Proof“",
    "Au lieu de testimonials statiques, créateurs montrent les vraies utilisations par d'autres utilisateurs. User-generated content à grande échelle.":
        "Statt statischer Testimonials zeigen Creators die echte Nutzung durch andere Kunden. User-generated Content im großen Stil.",
    "Encouragez vos clients à créer du contenu avec vos produits. Répostez le meilleur. C'est TRÈS puissant.":
        "Bring deine Kunden dazu, Inhalte mit deinen Produkten zu machen. Repost das Beste. Das wirkt sehr stark.",
    "{0}. ⚡ \"Instant Gratification\"": "{0}. ⚡ „Instant Gratification“",
    "Vidéos montrant les résultats IMMÉDIATEMENT. \"Voici avant/après en {0} secondes\". Pas d'attente.":
        "Videos, die das Ergebnis SOFORT zeigen. „Hier Vorher/Nachher in {0} Sekunden.“ Kein Warten.",
    "Si ton produit permet des résultats rapides, mets ça en avant. Si non, crée l'expectation de vitesse d'une autre façon.":
        "Wenn dein Produkt schnell liefert, stell das nach vorn. Wenn nicht, erzeuge das Gefühl von Tempo anders.",
    "{0}. 🎭 \"Personality-Driven Sales\"": "{0}. 🎭 „Personality-Driven Sales“",
    "Les gens n'achètent pas les produits, ils achètent les créateurs. La personnalité EST le produit.":
        "Die Leute kaufen keine Produkte, sie kaufen Creators. Die Persönlichkeit IST das Produkt.",
    "Montrez-vous plus. Vos opinions, votre sens de l'humour, vos croyances. Moins de \"produit\", plus de \"toi\".":
        "Zeig mehr von dir. Deine Meinungen, deinen Humor, wofür du stehst. Weniger „Produkt“, mehr „du“.",
    "🎯 La Meta-Tendance : \"Menos es Más\"": "🎯 Der Meta-Trend: weniger ist mehr",
    "Observe attentivement : les {0} tendances ci-dessus convergen vers une seule chose :":
        "Schau genau hin: Die {0} Trends oben laufen auf eine Sache hinaus —",
    "plus simple, plus honnête, plus rapide": "einfacher, ehrlicher, schneller",
    "Les créateurs gagnants en {0} ne sont pas ceux avec les meilleurs studios ou les vidéos les plus complexes. Ce sont ceux qui comprennent que le spectateur de TikTok veut de l'authenticité brute, pas de la perfection produite.":
        "Die Creators, die {0} gewinnen, sind nicht die mit den besten Studios oder den aufwendigsten Videos. Es sind die, die verstanden haben, dass ein TikTok-Zuschauer rohe Echtheit will, keine produzierte Perfektion.",
    "Analysez vos tendances maintenant": "Prüf deine Videos gegen diese Trends",
    "Utilisez Qeerah pour voir si vos vidéos suivent ces tendances {0}.":
        "Nutz Qeerah, um zu sehen, ob deine Videos diesen {0} Trends folgen.",
    "Analyser vos vidéos →": "Deine Videos analysieren →",
}

T_BLOG_TENDANCES["es"] = {
    "Top {0} Tendances TikTok Shop {1} - Qeerah": "Las {0} tendencias de TikTok Shop en {1} - Qeerah",
    "Top {0} des tendances TikTok Shop {1} qui vont dominer. Découvrez ce qui fonctionne et comment l'utiliser dans votre stratégie.":
        "Las {0} tendencias de TikTok Shop que van a dominar {1}. Qué funciona y cómo usarlo en tu estrategia.",
    "Les {0} tendances qui définissent le e-commerce sur TikTok en {1}, et comment les utiliser concrètement dans vos vidéos.":
        "Las {0} tendencias que definen el comercio en TikTok en {1} y cómo aplicarlas en tus vídeos.",
    "← Retour au blog": "← Volver al blog",
    "🔮 TENDANCES": "🔮 TENDENCIAS",
    "Top {0} des tendances TikTok Shop {1} qui vont dominer": "Las {0} tendencias de TikTok Shop que van a dominar {1}",
    "Le paysage de TikTok Shop change constamment. Voici les {0} tendances qui dominent le marché en {1} et comment les exploiter pour votre croissance.":
        "El panorama de TikTok Shop cambia sin parar. Estas son las {0} tendencias que dominan el mercado en {1} y cómo aprovecharlas para crecer.",
    "{0}. 🎬 Ultra-Micro Content (UMC)": "{0}. 🎬 Ultra-Micro Content (UMC)",
    "Des vidéos de {0}-{1} secondes extrêmement punchy. Plus courtes que TikTok \"normal\", ultra-concentrated. Les créateurs testent {2}x plus de content.":
        "Vídeos de {0}-{1} segundos muy directos. Más cortos que el TikTok «normal», ultraconcentrados. Los creadores prueban {2} veces más contenido.",
    "Comment l'utiliser :": "Cómo usarlo:",
    "Divisez vos vidéos en clips de {0}-{1} sec. Testez des dizaines de versions. Gardez seulement les top {2}%.":
        "Corta tus vídeos en clips de {0}-{1} s. Prueba decenas de versiones. Quédate solo con el {2} % mejor.",
    "{0}. 💬 \"Tell\" vs \"Show\"": "{0}. 💬 «Tell» frente a «Show»",
    "Les créateurs gagnants parlent directement à la caméra. Plus de montage complexe, juste de la conversation honnête.":
        "Los creadores que ganan hablan directamente a cámara. Sin montaje complejo, solo conversación honesta.",
    "Enregistrez vous en parlant naturellement. Pas de script. Juste vous, votre produit, et votre opinion.":
        "Grábate hablando con naturalidad. Sin guion. Solo tú, tu producto y tu opinión.",
    "{0}. 🤝 \"Duets de produit\"": "{0}. 🤝 «Dúos de producto»",
    "Créateurs qui réagissent aux vidéos d'autres créateurs en vendant \"contre-produit\" ou complément.":
        "Creadores que reaccionan a vídeos de otros creadores vendiendo un producto rival o complementario.",
    "Surveillez les trends de votre niche. Créez des vidéos de réaction/amélioration.":
        "Vigila las tendencias de tu nicho. Haz vídeos de reacción o de mejora.",
    "{0}. 📊 \"Data-Backed Content\"": "{0}. 📊 «Data-Backed Content»",
    "Créateurs qui montrent les chiffres : \"{0}% des gens préfèrent...\", \"Mon audience m'a votée pour...\". Crédibilité extrême.":
        "Creadores que enseñan las cifras: «el {0} % de la gente prefiere…», «mi público votó por…». Credibilidad enorme.",
    "Collectez les feedbacks, créez des sondages, montrez les résultats. Les gens ADORENT voir les chiffres.":
        "Recoge opiniones, haz encuestas, enseña los resultados. A la gente le ENCANTA ver números.",
    "{0}. 🎯 \"Segment-Specific Content\"": "{0}. 🎯 «Segment-Specific Content»",
    "Au lieu de contenu générique, créateurs font des versions spécifiques : \"Pour les hommes\", \"Pour les mères\", \"Pour les freelancers\".":
        "En vez de contenido genérico, los creadores hacen versiones específicas: «para hombres», «para madres», «para autónomos».",
    "Identifiez vos {0}-{1} segments clés. Créez du contenu adapté pour chacun.":
        "Identifica tus {0}-{1} segmentos clave. Crea contenido a medida para cada uno.",
    "{0}. 🔄 \"Loop Stories\"": "{0}. 🔄 «Loop Stories»",
    "Vidéos qui boucles après {0} secondes avec des variations. Plus tu la regardes, plus tu vois de perspectives différentes.":
        "Vídeos que se repiten a los {0} segundos con variaciones. Cuanto más los ves, más detalles descubres.",
    "Testez des hooks qui créent de la boucle naturelle. Les gens re-regardent = plus d'algorithme.":
        "Prueba ganchos que creen un bucle natural. La gente lo vuelve a ver = más algoritmo.",
    "{0}. 💎 \"Scarcity + Authenticity\"": "{0}. 💎 «Escasez + autenticidad»",
    "\"Je n'en ai que {0} gauche\" combiné avec \"C'est mon dernier stock de celui-ci\". L'urgence combinée à l'honnêteté.":
        "«Solo me quedan {0}» junto con «es mi último stock de este». Urgencia combinada con honestidad.",
    "Montrez vraiment les limites. Soyez honnête sur les stocks. L'urgence authentique convertit {0}x mieux.":
        "Enseña los límites reales. Sé honesto con el stock. La urgencia auténtica convierte {0} veces mejor.",
    "{0}. 👥 \"Community-Driven Proof\"": "{0}. 👥 «Community-Driven Proof»",
    "Au lieu de testimonials statiques, créateurs montrent les vraies utilisations par d'autres utilisateurs. User-generated content à grande échelle.":
        "En vez de testimonios estáticos, los creadores muestran usos reales de otros clientes. Contenido de usuarios a gran escala.",
    "Encouragez vos clients à créer du contenu avec vos produits. Répostez le meilleur. C'est TRÈS puissant.":
        "Anima a tus clientes a crear contenido con tus productos. Republica lo mejor. Funciona muy bien.",
    "{0}. ⚡ \"Instant Gratification\"": "{0}. ⚡ «Instant Gratification»",
    "Vidéos montrant les résultats IMMÉDIATEMENT. \"Voici avant/après en {0} secondes\". Pas d'attente.":
        "Vídeos que enseñan el resultado DE INMEDIATO. «Aquí el antes y el después en {0} segundos.» Sin esperas.",
    "Si ton produit permet des résultats rapides, mets ça en avant. Si non, crée l'expectation de vitesse d'une autre façon.":
        "Si tu producto da resultados rápidos, ponlo por delante. Si no, crea esa sensación de rapidez de otra forma.",
    "{0}. 🎭 \"Personality-Driven Sales\"": "{0}. 🎭 «Personality-Driven Sales»",
    "Les gens n'achètent pas les produits, ils achètent les créateurs. La personnalité EST le produit.":
        "La gente no compra productos, compra creadores. La personalidad ES el producto.",
    "Montrez-vous plus. Vos opinions, votre sens de l'humour, vos croyances. Moins de \"produit\", plus de \"toi\".":
        "Muéstrate más. Tus opiniones, tu humor, lo que defiendes. Menos «producto» y más «tú».",
    "🎯 La Meta-Tendance : \"Menos es Más\"": "🎯 La meta-tendencia: menos es más",
    "Observe attentivement : les {0} tendances ci-dessus convergen vers une seule chose :":
        "Fíjate bien: las {0} tendencias de arriba apuntan a una sola cosa:",
    "plus simple, plus honnête, plus rapide": "más simple, más honesto, más rápido",
    "Les créateurs gagnants en {0} ne sont pas ceux avec les meilleurs studios ou les vidéos les plus complexes. Ce sont ceux qui comprennent que le spectateur de TikTok veut de l'authenticité brute, pas de la perfection produite.":
        "Los creadores que ganan en {0} no son los que tienen mejores estudios ni los vídeos más elaborados. Son los que entienden que el espectador de TikTok quiere autenticidad en bruto, no perfección producida.",
    "Analysez vos tendances maintenant": "Comprueba tus vídeos frente a estas tendencias",
    "Utilisez Qeerah pour voir si vos vidéos suivent ces tendances {0}.":
        "Usa Qeerah para ver si tus vídeos siguen estas {0} tendencias.",
    "Analyser vos vidéos →": "Analizar tus vídeos →",
}

T_BLOG_TENDANCES["it"] = {
    "Top {0} Tendances TikTok Shop {1} - Qeerah": "Le {0} tendenze TikTok Shop del {1} - Qeerah",
    "Top {0} des tendances TikTok Shop {1} qui vont dominer. Découvrez ce qui fonctionne et comment l'utiliser dans votre stratégie.":
        "Le {0} tendenze TikTok Shop che domineranno il {1}. Cosa funziona e come usarlo nella tua strategia.",
    "Les {0} tendances qui définissent le e-commerce sur TikTok en {1}, et comment les utiliser concrètement dans vos vidéos.":
        "Le {0} tendenze che definiscono il commercio su TikTok nel {1} e come usarle concretamente nei tuoi video.",
    "← Retour au blog": "← Torna al blog",
    "🔮 TENDANCES": "🔮 TENDENZE",
    "Top {0} des tendances TikTok Shop {1} qui vont dominer": "Le {0} tendenze TikTok Shop che domineranno il {1}",
    "Le paysage de TikTok Shop change constamment. Voici les {0} tendances qui dominent le marché en {1} et comment les exploiter pour votre croissance.":
        "Il panorama di TikTok Shop cambia di continuo. Ecco le {0} tendenze che dominano il mercato nel {1} e come sfruttarle per crescere.",
    "{0}. 🎬 Ultra-Micro Content (UMC)": "{0}. 🎬 Ultra-Micro Content (UMC)",
    "Des vidéos de {0}-{1} secondes extrêmement punchy. Plus courtes que TikTok \"normal\", ultra-concentrated. Les créateurs testent {2}x plus de content.":
        "Video da {0}-{1} secondi, molto diretti. Più corti del TikTok «normale», ultraconcentrati. I creator testano {2} volte più contenuti.",
    "Comment l'utiliser :": "Come usarla:",
    "Divisez vos vidéos en clips de {0}-{1} sec. Testez des dizaines de versions. Gardez seulement les top {2}%.":
        "Spezza i tuoi video in clip da {0}-{1} secondi. Testa decine di versioni. Tieni solo il {2} % migliore.",
    "{0}. 💬 \"Tell\" vs \"Show\"": "{0}. 💬 «Tell» contro «Show»",
    "Les créateurs gagnants parlent directement à la caméra. Plus de montage complexe, juste de la conversation honnête.":
        "I creator che vincono parlano dritti in camera. Niente montaggio complicato, solo conversazione onesta.",
    "Enregistrez vous en parlant naturellement. Pas de script. Juste vous, votre produit, et votre opinion.":
        "Registrati mentre parli in modo naturale. Nessun copione. Solo tu, il tuo prodotto e la tua opinione.",
    "{0}. 🤝 \"Duets de produit\"": "{0}. 🤝 «Duetti di prodotto»",
    "Créateurs qui réagissent aux vidéos d'autres créateurs en vendant \"contre-produit\" ou complément.":
        "Creator che reagiscono ai video di altri creator vendendo un prodotto alternativo o complementare.",
    "Surveillez les trends de votre niche. Créez des vidéos de réaction/amélioration.":
        "Tieni d'occhio le tendenze della tua nicchia. Fai video di reazione o di miglioramento.",
    "{0}. 📊 \"Data-Backed Content\"": "{0}. 📊 «Data-Backed Content»",
    "Créateurs qui montrent les chiffres : \"{0}% des gens préfèrent...\", \"Mon audience m'a votée pour...\". Crédibilité extrême.":
        "Creator che mostrano i numeri: «il {0} % delle persone preferisce…», «il mio pubblico ha votato per…». Credibilità altissima.",
    "Collectez les feedbacks, créez des sondages, montrez les résultats. Les gens ADORENT voir les chiffres.":
        "Raccogli feedback, fai sondaggi, mostra i risultati. La gente ADORA vedere i numeri.",
    "{0}. 🎯 \"Segment-Specific Content\"": "{0}. 🎯 «Segment-Specific Content»",
    "Au lieu de contenu générique, créateurs font des versions spécifiques : \"Pour les hommes\", \"Pour les mères\", \"Pour les freelancers\".":
        "Invece di contenuti generici, i creator fanno versioni mirate: «per uomini», «per mamme», «per freelance».",
    "Identifiez vos {0}-{1} segments clés. Créez du contenu adapté pour chacun.":
        "Individua i tuoi {0}-{1} segmenti chiave. Crea contenuti su misura per ognuno.",
    "{0}. 🔄 \"Loop Stories\"": "{0}. 🔄 «Loop Stories»",
    "Vidéos qui boucles après {0} secondes avec des variations. Plus tu la regardes, plus tu vois de perspectives différentes.":
        "Video che ripartono dopo {0} secondi con delle varianti. Più li guardi, più cose noti.",
    "Testez des hooks qui créent de la boucle naturelle. Les gens re-regardent = plus d'algorithme.":
        "Prova hook che creano un loop naturale. La gente riguarda = più algoritmo.",
    "{0}. 💎 \"Scarcity + Authenticity\"": "{0}. 💎 «Scarsità + autenticità»",
    "\"Je n'en ai que {0} gauche\" combiné avec \"C'est mon dernier stock de celui-ci\". L'urgence combinée à l'honnêteté.":
        "«Me ne restano solo {0}» insieme a «è la mia ultima scorta di questo». Urgenza unita all'onestà.",
    "Montrez vraiment les limites. Soyez honnête sur les stocks. L'urgence authentique convertit {0}x mieux.":
        "Mostra i limiti veri. Sii onesto sulle scorte. L'urgenza autentica converte {0} volte meglio.",
    "{0}. 👥 \"Community-Driven Proof\"": "{0}. 👥 «Community-Driven Proof»",
    "Au lieu de testimonials statiques, créateurs montrent les vraies utilisations par d'autres utilisateurs. User-generated content à grande échelle.":
        "Invece di testimonianze statiche, i creator mostrano l'uso reale da parte di altri clienti. Contenuti degli utenti su larga scala.",
    "Encouragez vos clients à créer du contenu avec vos produits. Répostez le meilleur. C'est TRÈS puissant.":
        "Spingi i tuoi clienti a creare contenuti con i tuoi prodotti. Ripubblica i migliori. Funziona moltissimo.",
    "{0}. ⚡ \"Instant Gratification\"": "{0}. ⚡ «Instant Gratification»",
    "Vidéos montrant les résultats IMMÉDIATEMENT. \"Voici avant/après en {0} secondes\". Pas d'attente.":
        "Video che mostrano il risultato SUBITO. «Ecco prima e dopo in {0} secondi.» Nessuna attesa.",
    "Si ton produit permet des résultats rapides, mets ça en avant. Si non, crée l'expectation de vitesse d'une autre façon.":
        "Se il tuo prodotto dà risultati rapidi, mettilo davanti. Se no, crea l'idea di velocità in un altro modo.",
    "{0}. 🎭 \"Personality-Driven Sales\"": "{0}. 🎭 «Personality-Driven Sales»",
    "Les gens n'achètent pas les produits, ils achètent les créateurs. La personnalité EST le produit.":
        "La gente non compra prodotti, compra creator. La personalità È il prodotto.",
    "Montrez-vous plus. Vos opinions, votre sens de l'humour, vos croyances. Moins de \"produit\", plus de \"toi\".":
        "Mostrati di più. Le tue opinioni, il tuo umorismo, ciò in cui credi. Meno «prodotto», più «te».",
    "🎯 La Meta-Tendance : \"Menos es Más\"": "🎯 La meta-tendenza: meno è meglio",
    "Observe attentivement : les {0} tendances ci-dessus convergen vers une seule chose :":
        "Guarda bene: le {0} tendenze qui sopra puntano tutte a una cosa sola:",
    "plus simple, plus honnête, plus rapide": "più semplice, più onesto, più veloce",
    "Les créateurs gagnants en {0} ne sont pas ceux avec les meilleurs studios ou les vidéos les plus complexes. Ce sont ceux qui comprennent que le spectateur de TikTok veut de l'authenticité brute, pas de la perfection produite.":
        "I creator che vincono nel {0} non sono quelli con gli studi migliori o i video più elaborati. Sono quelli che hanno capito che chi guarda TikTok vuole autenticità grezza, non perfezione confezionata.",
    "Analysez vos tendances maintenant": "Verifica i tuoi video su queste tendenze",
    "Utilisez Qeerah pour voir si vos vidéos suivent ces tendances {0}.":
        "Usa Qeerah per vedere se i tuoi video seguono queste {0} tendenze.",
    "Analyser vos vidéos →": "Analizza i tuoi video →",
}

T_BLOG_TENDANCES["pt-br"] = {
    "Top {0} Tendances TikTok Shop {1} - Qeerah": "As {0} tendências do TikTok Shop em {1} - Qeerah",
    "Top {0} des tendances TikTok Shop {1} qui vont dominer. Découvrez ce qui fonctionne et comment l'utiliser dans votre stratégie.":
        "As {0} tendências do TikTok Shop que vão dominar {1}. O que funciona e como usar na sua estratégia.",
    "Les {0} tendances qui définissent le e-commerce sur TikTok en {1}, et comment les utiliser concrètement dans vos vidéos.":
        "As {0} tendências que definem o comércio no TikTok em {1} e como aplicá-las nos seus vídeos.",
    "← Retour au blog": "← Voltar ao blog",
    "🔮 TENDANCES": "🔮 TENDÊNCIAS",
    "Top {0} des tendances TikTok Shop {1} qui vont dominer": "As {0} tendências do TikTok Shop que vão dominar {1}",
    "Le paysage de TikTok Shop change constamment. Voici les {0} tendances qui dominent le marché en {1} et comment les exploiter pour votre croissance.":
        "O cenário do TikTok Shop muda o tempo todo. Estas são as {0} tendências que dominam o mercado em {1} e como usá-las para crescer.",
    "{0}. 🎬 Ultra-Micro Content (UMC)": "{0}. 🎬 Ultra-Micro Content (UMC)",
    "Des vidéos de {0}-{1} secondes extrêmement punchy. Plus courtes que TikTok \"normal\", ultra-concentrated. Les créateurs testent {2}x plus de content.":
        "Vídeos de {0}-{1} segundos, bem diretos. Mais curtos que o TikTok “normal”, ultraconcentrados. Os criadores testam {2}× mais conteúdo.",
    "Comment l'utiliser :": "Como usar:",
    "Divisez vos vidéos en clips de {0}-{1} sec. Testez des dizaines de versions. Gardez seulement les top {2}%.":
        "Corte seus vídeos em clipes de {0}-{1} s. Teste dezenas de versões. Fique só com os {2} % melhores.",
    "{0}. 💬 \"Tell\" vs \"Show\"": "{0}. 💬 “Tell” x “Show”",
    "Les créateurs gagnants parlent directement à la caméra. Plus de montage complexe, juste de la conversation honnête.":
        "Os criadores que ganham falam direto para a câmera. Nada de montagem complexa, só conversa honesta.",
    "Enregistrez vous en parlant naturellement. Pas de script. Juste vous, votre produit, et votre opinion.":
        "Grave você falando naturalmente. Sem roteiro. Só você, seu produto e sua opinião.",
    "{0}. 🤝 \"Duets de produit\"": "{0}. 🤝 “Duetos de produto”",
    "Créateurs qui réagissent aux vidéos d'autres créateurs en vendant \"contre-produit\" ou complément.":
        "Criadores que reagem a vídeos de outros criadores vendendo um produto rival ou complementar.",
    "Surveillez les trends de votre niche. Créez des vidéos de réaction/amélioration.":
        "Fique de olho nas tendências do seu nicho. Faça vídeos de reação ou de melhoria.",
    "{0}. 📊 \"Data-Backed Content\"": "{0}. 📊 “Data-Backed Content”",
    "Créateurs qui montrent les chiffres : \"{0}% des gens préfèrent...\", \"Mon audience m'a votée pour...\". Crédibilité extrême.":
        "Criadores que mostram os números: “{0} % das pessoas preferem…”, “meu público votou em…”. Credibilidade enorme.",
    "Collectez les feedbacks, créez des sondages, montrez les résultats. Les gens ADORENT voir les chiffres.":
        "Colete feedback, faça enquetes, mostre os resultados. As pessoas AMAM ver números.",
    "{0}. 🎯 \"Segment-Specific Content\"": "{0}. 🎯 “Segment-Specific Content”",
    "Au lieu de contenu générique, créateurs font des versions spécifiques : \"Pour les hommes\", \"Pour les mères\", \"Pour les freelancers\".":
        "Em vez de conteúdo genérico, os criadores fazem versões específicas: “para homens”, “para mães”, “para freelancers”.",
    "Identifiez vos {0}-{1} segments clés. Créez du contenu adapté pour chacun.":
        "Identifique seus {0}-{1} segmentos principais. Crie conteúdo sob medida para cada um.",
    "{0}. 🔄 \"Loop Stories\"": "{0}. 🔄 “Loop Stories”",
    "Vidéos qui boucles après {0} secondes avec des variations. Plus tu la regardes, plus tu vois de perspectives différentes.":
        "Vídeos que voltam ao início depois de {0} segundos com variações. Quanto mais você assiste, mais coisa percebe.",
    "Testez des hooks qui créent de la boucle naturelle. Les gens re-regardent = plus d'algorithme.":
        "Teste ganchos que criam um loop natural. As pessoas reveem = mais algoritmo.",
    "{0}. 💎 \"Scarcity + Authenticity\"": "{0}. 💎 “Escassez + autenticidade”",
    "\"Je n'en ai que {0} gauche\" combiné avec \"C'est mon dernier stock de celui-ci\". L'urgence combinée à l'honnêteté.":
        "“Só tenho mais {0}” junto com “é o meu último estoque desse”. Urgência combinada com honestidade.",
    "Montrez vraiment les limites. Soyez honnête sur les stocks. L'urgence authentique convertit {0}x mieux.":
        "Mostre os limites de verdade. Seja honesto sobre o estoque. Urgência autêntica converte {0}× melhor.",
    "{0}. 👥 \"Community-Driven Proof\"": "{0}. 👥 “Community-Driven Proof”",
    "Au lieu de testimonials statiques, créateurs montrent les vraies utilisations par d'autres utilisateurs. User-generated content à grande échelle.":
        "Em vez de depoimentos estáticos, os criadores mostram o uso real por outros clientes. Conteúdo de usuários em escala.",
    "Encouragez vos clients à créer du contenu avec vos produits. Répostez le meilleur. C'est TRÈS puissant.":
        "Incentive seus clientes a criar conteúdo com seus produtos. Reposte os melhores. Funciona MUITO bem.",
    "{0}. ⚡ \"Instant Gratification\"": "{0}. ⚡ “Instant Gratification”",
    "Vidéos montrant les résultats IMMÉDIATEMENT. \"Voici avant/après en {0} secondes\". Pas d'attente.":
        "Vídeos que mostram o resultado NA HORA. “Olha o antes e depois em {0} segundos.” Sem espera.",
    "Si ton produit permet des résultats rapides, mets ça en avant. Si non, crée l'expectation de vitesse d'une autre façon.":
        "Se seu produto dá resultado rápido, coloque isso na frente. Se não, crie essa sensação de rapidez de outro jeito.",
    "{0}. 🎭 \"Personality-Driven Sales\"": "{0}. 🎭 “Personality-Driven Sales”",
    "Les gens n'achètent pas les produits, ils achètent les créateurs. La personnalité EST le produit.":
        "As pessoas não compram produtos, compram criadores. A personalidade É o produto.",
    "Montrez-vous plus. Vos opinions, votre sens de l'humour, vos croyances. Moins de \"produit\", plus de \"toi\".":
        "Apareça mais. Suas opiniões, seu humor, o que você defende. Menos “produto”, mais “você”.",
    "🎯 La Meta-Tendance : \"Menos es Más\"": "🎯 A metatendência: menos é mais",
    "Observe attentivement : les {0} tendances ci-dessus convergen vers une seule chose :":
        "Olhe com atenção: as {0} tendências acima apontam para uma coisa só:",
    "plus simple, plus honnête, plus rapide": "mais simples, mais honesto, mais rápido",
    "Les créateurs gagnants en {0} ne sont pas ceux avec les meilleurs studios ou les vidéos les plus complexes. Ce sont ceux qui comprennent que le spectateur de TikTok veut de l'authenticité brute, pas de la perfection produite.":
        "Os criadores que ganham em {0} não são os que têm os melhores estúdios nem os vídeos mais elaborados. São os que entenderam que quem assiste TikTok quer autenticidade crua, não perfeição produzida.",
    "Analysez vos tendances maintenant": "Confira seus vídeos frente a essas tendências",
    "Utilisez Qeerah pour voir si vos vidéos suivent ces tendances {0}.":
        "Use a Qeerah para ver se seus vídeos seguem essas {0} tendências.",
    "Analyser vos vidéos →": "Analisar seus vídeos →",
}

T_BLOG_TENDANCES["en-ie"] = dict(T_BLOG_TENDANCES["en"])
T_BLOG_TENDANCES["es-mx"] = dict(T_BLOG_TENDANCES["es"])


# ═══════════════════════════════════════════════════════════════════════════
# /blog/createurs-millionnaires
# Les pseudonymes (@stylebymariana…) et les montants ne sont pas traduits :
# un compte renommé devient introuvable, et un chiffre doit rester le même
# dans les huit langues.
# ═══════════════════════════════════════════════════════════════════════════
T_BLOG_CREATEURS: dict[str, dict[str, str]] = {}

T_BLOG_CREATEURS["en"] = {
    "{0} Créateurs TikTok Shop Devenus Millionnaires - Qeerah":
        "{0} TikTok Shop creators who became millionaires - Qeerah",
    "{0} créateurs TikTok Shop devenus millionnaires en {1}. Découvrez leurs stratégies, leurs secrets et ce que vous pouvez en apprendre.":
        "{0} TikTok Shop creators who became millionaires in {1}. Their strategies, what they did differently, and what you can take from it.",
    "{0} créateurs TikTok Shop devenus millionnaires": "{0} TikTok Shop creators who became millionaires",
    "Les stratégies et patterns communs des créateurs qui ont transformé leurs vidéos en empires commerciaux sur TikTok Shop.":
        "The strategies and shared patterns of creators who turned their videos into commercial empires on TikTok Shop.",
    "← Retour au blog": "← Back to the blog",
    "💰 SUCCESS STORIES": "💰 SUCCESS STORIES",
    "{0} créateurs TikTok Shop devenus millionnaires en {1}":
        "{0} TikTok Shop creators who became millionaires in {1}",
    "📅 Avril {0}": "📅 April {0}",
    "👤 Par l'équipe Qeerah": "👤 By the Qeerah team",
    "⏱️ {0} min": "⏱️ {0} min",
    "Vous vous demandez si c'est vraiment possible de devenir millionnaire sur TikTok Shop ? La réponse est oui. Voici les histoires de {0} créateurs qui l'ont fait, et ce que nous pouvons en apprendre.":
        "Wondering whether it's really possible to become a millionaire on TikTok Shop? It is. Here are the stories of {0} creators who did it, and what we can learn from them.",
    "{0}. 👗 @stylebymariana - Beauté & Mode": "{0}. 👗 @stylebymariana — beauty & fashion",
    "La créatrice qui a disrupta la mode française": "The creator who shook up French fashion",
    "Followers": "Followers",
    "GMV {0}": "GMV {0}",
    "{0} mois": "{0} months",
    "Pour {0}M€": "To reach €{0}M",
    "Mariana a commencé sans produits propres. Elle revenait des accessoires de mode éthiques et les présentait dans ses vidéos. En {0} mois, elle a atteint {1} figures. Son secret : l'authententicité. Elle montre vraiment comment porter les pièces, des hauls complets, des réactions honnêtes.":
        "Mariana started with no products of her own. She resold ethical fashion accessories and showed them in her videos. In {0} months she reached {1} figures. Her secret: authenticity. She really shows how to wear the pieces — full hauls, honest reactions.",
    "🔑 Le Secret :": "🔑 The secret:",
    "Elle crée du contenu {0}-{1} fois par jour. Chaque vidéo teste une angle différent. Elle analyse immédiatement ce qui fonctionne et duplique les meilleures performances.":
        "She makes content {0}-{1} times a day. Each video tests a different angle. She looks straight away at what worked and doubles down on the best performers.",
    "{0}. 💪 @fitbyalexis - Fitness & Nutrition": "{0}. 💪 @fitbyalexis — fitness & nutrition",
    "Du coach personnel à l'empire fitness": "From personal trainer to fitness empire",
    "Alexis vendait des guides de fitness et de nutrition. Rien de spectaculaire. Mais il a compris quelque chose : la transformation. Les vidéos \"before/after\" d'une journée avec ses produits généraient {0}% plus de ventes. Il a pivotté complètement vers le storytelling de transformation.":
        "Alexis sold fitness and nutrition guides. Nothing spectacular. But he understood one thing: transformation. Before/after videos of a single day with his products generated {0}% more sales. He pivoted entirely to transformation storytelling.",
    "\"Voici mon produit\".": "“here's my product”.",
    "{0}. 🏠 @homedesignbysarah - Décoration & Mobilier": "{0}. 🏠 @homedesignbysarah — interiors & furniture",
    "Comment vendre des meubles sur TikTok": "How to sell furniture on TikTok",
    "Sarah montrait les mêmes meubles en {0} contextes différents. \"Voici ce meuble dans mon salon moderne\" → \"Voici le même dans un loft industriel\" → \"Voici dans un petit appartement\". Elle a compris que le problème n'était pas le produit, mais les doutes du client : \"Est-ce que ça va match mon intérieur ?\"":
        "Sarah showed the same furniture in {0} different settings. “Here's this piece in my modern living room” → “here's the same one in an industrial loft” → “here it is in a small flat”. She worked out that the problem wasn't the product but the customer's doubt: “will it fit my place?”",
    "Elle crée des \"inspiration rooms\" complètes. Pas juste un meuble, un mood board entier. Le client voit où ça va, comment ça s'assortit, pourquoi c'est beau.":
        "She builds complete “inspiration rooms”. Not one piece of furniture — a whole mood board. The customer sees where it goes, what it sits with, why it looks good.",
    "{0}. 💼 @techreviewjean - Électronique & Tech": "{0}. 💼 @techreviewjean — electronics & tech",
    "Devenir l'expert qui vend": "Becoming the expert who sells",
    "Jean revend des téléphones, ordinateurs, et gadgets tech. Mais il ne les vend pas — il les explique. Comparaisons détaillées, cas d'usage spécifiques, alternatives considérées. Il est devenu la source de confiance #{0} pour la tech en France sur TikTok.":
        "Jean resells phones, computers and tech gadgets. But he doesn't sell them — he explains them. Detailed comparisons, specific use cases, alternatives weighed up. He became the #{0} trusted source for tech in France on TikTok.",
    "Il crée des vidéos \"FAQ\" anticipées. Il devine les objections avant que le client les ait. \"Oui, je sais que c'est cher, mais voici pourquoi c'est le seul choix logique...\"":
        "He makes pre-emptive FAQ videos. He guesses the objections before the customer has them. “Yes, I know it's expensive, but here's why it's the only sensible choice…”",
    "💡 Les Patterns Communs": "💡 What they have in common",
    "Si vous analysez ces {0} créateurs (et les {1} autres qu'on aurait pu inclure), des patterns clairs émergent :":
        "Look at these {0} creators (and the {1} others we could have included) and clear patterns emerge:",
    "{0}. Spécialisation extrême": "{0}. Extreme specialisation",
    "Aucun d'eux ne vend \"tout\". Ils sont devenus experts reconnus dans une niche étroite. Mariana = mode éthique. Alexis = transformation fitness. Sarah = décoration accessible. Jean = tech simplifiée.":
        "None of them sells “everything”. Each became a recognised expert in a narrow niche. Mariana = ethical fashion. Alexis = fitness transformation. Sarah = affordable interiors. Jean = tech made simple.",
    "Produit": "Product",
    "Ils passent {0}% de leur attention sur le contenu et {1}% sur le produit. La plupart des créateurs échouent font l'inverse : {2}% contenu, {3}% promotion produit.":
        "They put {0}% of their attention on the content and {1}% on the product. Most creators who fail do the opposite: {2}% content, {3}% product promotion.",
    "{0}. Vitesse d'itération": "{0}. Speed of iteration",
    "Ils publient beaucoup. Mariana publie {0}-{1} fois par jour. Cela veut dire qu'elle teste {2}-{3} angles différents. En une semaine, elle a {4}-{5} variables testées. Elle peut ajuster rapidement ce qui fonctionne.":
        "They publish a lot. Mariana posts {0}-{1} times a day, which means she tests {2}-{3} different angles. In a week that's {4}-{5} variables tested. She can adjust fast around what works.",
    "{0}. Humanité authentique": "{0}. Genuine humanity",
    "Aucun n'est parfait. Ils montrent leurs faiblesses, leurs échecs, leur processus. Les gens n'achètent pas aux experts parfaits, ils achètent aux humains qu'ils reconnaissent et en qui ils ont confiance.":
        "None of them is perfect. They show their weak spots, their failures, how they work. People don't buy from flawless experts, they buy from humans they recognise and trust.",
    "Devenez-vous le prochain créateur millionnaire ?": "Will you be the next creator to get there?",
    "Utilisez Qeerah pour analyser vos vidéos comme le font les top créateurs.":
        "Use Qeerah to analyse your videos the way the top creators do.",
    "Commencer l'analyse →": "Start analysing →",
}

T_BLOG_CREATEURS["de"] = {
    "{0} Créateurs TikTok Shop Devenus Millionnaires - Qeerah":
        "{0} TikTok-Shop-Creators, die Millionäre wurden - Qeerah",
    "{0} créateurs TikTok Shop devenus millionnaires en {1}. Découvrez leurs stratégies, leurs secrets et ce que vous pouvez en apprendre.":
        "{0} TikTok-Shop-Creators, die {1} Millionäre wurden. Ihre Strategien, was sie anders gemacht haben, und was du daraus mitnimmst.",
    "{0} créateurs TikTok Shop devenus millionnaires": "{0} TikTok-Shop-Creators, die Millionäre wurden",
    "Les stratégies et patterns communs des créateurs qui ont transformé leurs vidéos en empires commerciaux sur TikTok Shop.":
        "Die Strategien und gemeinsamen Muster von Creators, die ihre Videos auf TikTok Shop in Handelsimperien verwandelt haben.",
    "← Retour au blog": "← Zurück zum Blog",
    "💰 SUCCESS STORIES": "💰 ERFOLGSGESCHICHTEN",
    "{0} créateurs TikTok Shop devenus millionnaires en {1}":
        "{0} TikTok-Shop-Creators, die {1} Millionäre wurden",
    "📅 Avril {0}": "📅 April {0}",
    "👤 Par l'équipe Qeerah": "👤 Vom Qeerah-Team",
    "⏱️ {0} min": "⏱️ {0} Min.",
    "Vous vous demandez si c'est vraiment possible de devenir millionnaire sur TikTok Shop ? La réponse est oui. Voici les histoires de {0} créateurs qui l'ont fait, et ce que nous pouvons en apprendre.":
        "Du fragst dich, ob man auf TikTok Shop wirklich Millionär werden kann? Ja, kann man. Hier sind die Geschichten von {0} Creators, die es geschafft haben, und was sich daraus lernen lässt.",
    "{0}. 👗 @stylebymariana - Beauté & Mode": "{0}. 👗 @stylebymariana — Beauty & Mode",
    "La créatrice qui a disrupta la mode française": "Die Creatorin, die die französische Mode aufgemischt hat",
    "Followers": "Follower",
    "GMV {0}": "GMV {0}",
    "{0} mois": "{0} Monate",
    "Pour {0}M€": "Bis zu {0} Mio. €",
    "Mariana a commencé sans produits propres. Elle revenait des accessoires de mode éthiques et les présentait dans ses vidéos. En {0} mois, elle a atteint {1} figures. Son secret : l'authententicité. Elle montre vraiment comment porter les pièces, des hauls complets, des réactions honnêtes.":
        "Mariana fing ohne eigene Produkte an. Sie verkaufte faire Modeaccessoires weiter und zeigte sie in ihren Videos. In {0} Monaten kam sie auf {1} Stellen. Ihr Geheimnis: Echtheit. Sie zeigt wirklich, wie man die Teile trägt — komplette Hauls, ehrliche Reaktionen.",
    "🔑 Le Secret :": "🔑 Das Geheimnis:",
    "Elle crée du contenu {0}-{1} fois par jour. Chaque vidéo teste une angle différent. Elle analyse immédiatement ce qui fonctionne et duplique les meilleures performances.":
        "Sie macht {0}- bis {1}-mal am Tag Inhalte. Jedes Video testet einen anderen Winkel. Sie schaut sofort, was funktioniert, und legt bei den besten nach.",
    "{0}. 💪 @fitbyalexis - Fitness & Nutrition": "{0}. 💪 @fitbyalexis — Fitness & Ernährung",
    "Du coach personnel à l'empire fitness": "Vom Personal Trainer zum Fitness-Imperium",
    "Alexis vendait des guides de fitness et de nutrition. Rien de spectaculaire. Mais il a compris quelque chose : la transformation. Les vidéos \"before/after\" d'une journée avec ses produits généraient {0}% plus de ventes. Il a pivotté complètement vers le storytelling de transformation.":
        "Alexis verkaufte Fitness- und Ernährungsguides. Nichts Spektakuläres. Aber er hat eines verstanden: Verwandlung. Vorher/Nachher-Videos von einem einzigen Tag mit seinen Produkten brachten {0} % mehr Verkäufe. Er stellte komplett auf Verwandlungsgeschichten um.",
    "\"Voici mon produit\".": "„hier ist mein Produkt“.",
    "{0}. 🏠 @homedesignbysarah - Décoration & Mobilier": "{0}. 🏠 @homedesignbysarah — Einrichtung & Möbel",
    "Comment vendre des meubles sur TikTok": "Wie man auf TikTok Möbel verkauft",
    "Sarah montrait les mêmes meubles en {0} contextes différents. \"Voici ce meuble dans mon salon moderne\" → \"Voici le même dans un loft industriel\" → \"Voici dans un petit appartement\". Elle a compris que le problème n'était pas le produit, mais les doutes du client : \"Est-ce que ça va match mon intérieur ?\"":
        "Sarah zeigte dieselben Möbel in {0} verschiedenen Umgebungen. „Hier das Stück in meinem modernen Wohnzimmer“ → „hier dasselbe in einem Industrieloft“ → „hier in einer kleinen Wohnung“. Sie begriff, dass nicht das Produkt das Problem war, sondern der Zweifel der Kundschaft: „Passt das zu mir zu Hause?“",
    "Elle crée des \"inspiration rooms\" complètes. Pas juste un meuble, un mood board entier. Le client voit où ça va, comment ça s'assortit, pourquoi c'est beau.":
        "Sie baut ganze „Inspiration Rooms“. Nicht nur ein Möbelstück, ein komplettes Moodboard. Die Kundschaft sieht, wohin es passt, womit es sich verträgt, warum es gut aussieht.",
    "{0}. 💼 @techreviewjean - Électronique & Tech": "{0}. 💼 @techreviewjean — Elektronik & Technik",
    "Devenir l'expert qui vend": "Der Experte werden, der verkauft",
    "Jean revend des téléphones, ordinateurs, et gadgets tech. Mais il ne les vend pas — il les explique. Comparaisons détaillées, cas d'usage spécifiques, alternatives considérées. Il est devenu la source de confiance #{0} pour la tech en France sur TikTok.":
        "Jean verkauft Handys, Computer und Technikspielzeug weiter. Aber er verkauft sie nicht — er erklärt sie. Ausführliche Vergleiche, konkrete Anwendungsfälle, abgewogene Alternativen. Er wurde die Vertrauensquelle Nr. {0} für Technik in Frankreich auf TikTok.",
    "Il crée des vidéos \"FAQ\" anticipées. Il devine les objections avant que le client les ait. \"Oui, je sais que c'est cher, mais voici pourquoi c'est le seul choix logique...\"":
        "Er macht vorweggenommene FAQ-Videos. Er errät die Einwände, bevor die Kundschaft sie hat. „Ja, ich weiß, es ist teuer, aber hier ist, warum es die einzig vernünftige Wahl ist …“",
    "💡 Les Patterns Communs": "💡 Was sie gemeinsam haben",
    "Si vous analysez ces {0} créateurs (et les {1} autres qu'on aurait pu inclure), des patterns clairs émergent :":
        "Sieht man sich diese {0} Creators an (und die {1} weiteren, die wir hätten aufnehmen können), treten klare Muster hervor:",
    "{0}. Spécialisation extrême": "{0}. Radikale Spezialisierung",
    "Aucun d'eux ne vend \"tout\". Ils sont devenus experts reconnus dans une niche étroite. Mariana = mode éthique. Alexis = transformation fitness. Sarah = décoration accessible. Jean = tech simplifiée.":
        "Keiner von ihnen verkauft „alles“. Jeder wurde anerkannter Fachmensch in einer engen Nische. Mariana = faire Mode. Alexis = Fitness-Verwandlung. Sarah = bezahlbare Einrichtung. Jean = Technik einfach erklärt.",
    "Produit": "Produkt",
    "Ils passent {0}% de leur attention sur le contenu et {1}% sur le produit. La plupart des créateurs échouent font l'inverse : {2}% contenu, {3}% promotion produit.":
        "Sie stecken {0} % ihrer Aufmerksamkeit in den Inhalt und {1} % in das Produkt. Die meisten Creators, die scheitern, machen es umgekehrt: {2} % Inhalt, {3} % Produktwerbung.",
    "{0}. Vitesse d'itération": "{0}. Tempo beim Ausprobieren",
    "Ils publient beaucoup. Mariana publie {0}-{1} fois par jour. Cela veut dire qu'elle teste {2}-{3} angles différents. En une semaine, elle a {4}-{5} variables testées. Elle peut ajuster rapidement ce qui fonctionne.":
        "Sie veröffentlichen viel. Mariana postet {0}- bis {1}-mal am Tag, testet also {2} bis {3} verschiedene Winkel. In einer Woche sind das {4} bis {5} getestete Variablen. So kann sie schnell nachsteuern.",
    "{0}. Humanité authentique": "{0}. Echte Menschlichkeit",
    "Aucun n'est parfait. Ils montrent leurs faiblesses, leurs échecs, leur processus. Les gens n'achètent pas aux experts parfaits, ils achètent aux humains qu'ils reconnaissent et en qui ils ont confiance.":
        "Keiner ist perfekt. Sie zeigen ihre Schwächen, ihre Fehlschläge, ihren Weg. Die Leute kaufen nicht bei makellosen Fachleuten, sie kaufen bei Menschen, die sie wiedererkennen und denen sie vertrauen.",
    "Devenez-vous le prochain créateur millionnaire ?": "Bist du der oder die Nächste?",
    "Utilisez Qeerah pour analyser vos vidéos comme le font les top créateurs.":
        "Nutz Qeerah, um deine Videos so zu analysieren wie die Top-Creators.",
    "Commencer l'analyse →": "Analyse starten →",
}

T_BLOG_CREATEURS["es"] = {
    "{0} Créateurs TikTok Shop Devenus Millionnaires - Qeerah":
        "{0} creadores de TikTok Shop que se hicieron millonarios - Qeerah",
    "{0} créateurs TikTok Shop devenus millionnaires en {1}. Découvrez leurs stratégies, leurs secrets et ce que vous pouvez en apprendre.":
        "{0} creadores de TikTok Shop que se hicieron millonarios en {1}. Sus estrategias, qué hicieron distinto y qué puedes aprender de ello.",
    "{0} créateurs TikTok Shop devenus millionnaires": "{0} creadores de TikTok Shop que se hicieron millonarios",
    "Les stratégies et patterns communs des créateurs qui ont transformé leurs vidéos en empires commerciaux sur TikTok Shop.":
        "Las estrategias y los patrones comunes de creadores que convirtieron sus vídeos en imperios comerciales en TikTok Shop.",
    "← Retour au blog": "← Volver al blog",
    "💰 SUCCESS STORIES": "💰 HISTORIAS DE ÉXITO",
    "{0} créateurs TikTok Shop devenus millionnaires en {1}":
        "{0} creadores de TikTok Shop que se hicieron millonarios en {1}",
    "📅 Avril {0}": "📅 Abril de {0}",
    "👤 Par l'équipe Qeerah": "👤 Por el equipo de Qeerah",
    "⏱️ {0} min": "⏱️ {0} min",
    "Vous vous demandez si c'est vraiment possible de devenir millionnaire sur TikTok Shop ? La réponse est oui. Voici les histoires de {0} créateurs qui l'ont fait, et ce que nous pouvons en apprendre.":
        "¿Te preguntas si de verdad se puede llegar a millonario en TikTok Shop? Sí se puede. Estas son las historias de {0} creadores que lo lograron y lo que podemos aprender de ellas.",
    "{0}. 👗 @stylebymariana - Beauté & Mode": "{0}. 👗 @stylebymariana — belleza y moda",
    "La créatrice qui a disrupta la mode française": "La creadora que sacudió la moda francesa",
    "Followers": "Seguidores",
    "GMV {0}": "GMV {0}",
    "{0} mois": "{0} meses",
    "Pour {0}M€": "Hasta {0} M€",
    "Mariana a commencé sans produits propres. Elle revenait des accessoires de mode éthiques et les présentait dans ses vidéos. En {0} mois, elle a atteint {1} figures. Son secret : l'authententicité. Elle montre vraiment comment porter les pièces, des hauls complets, des réactions honnêtes.":
        "Mariana empezó sin productos propios. Revendía accesorios de moda éticos y los enseñaba en sus vídeos. En {0} meses llegó a {1} cifras. Su secreto: la autenticidad. Enseña de verdad cómo se llevan las prendas, hauls completos, reacciones honestas.",
    "🔑 Le Secret :": "🔑 El secreto:",
    "Elle crée du contenu {0}-{1} fois par jour. Chaque vidéo teste une angle différent. Elle analyse immédiatement ce qui fonctionne et duplique les meilleures performances.":
        "Crea contenido {0}-{1} veces al día. Cada vídeo prueba un ángulo distinto. Mira enseguida qué funciona y repite lo que mejor rinde.",
    "{0}. 💪 @fitbyalexis - Fitness & Nutrition": "{0}. 💪 @fitbyalexis — fitness y nutrición",
    "Du coach personnel à l'empire fitness": "De entrenador personal a imperio del fitness",
    "Alexis vendait des guides de fitness et de nutrition. Rien de spectaculaire. Mais il a compris quelque chose : la transformation. Les vidéos \"before/after\" d'une journée avec ses produits généraient {0}% plus de ventes. Il a pivotté complètement vers le storytelling de transformation.":
        "Alexis vendía guías de fitness y nutrición. Nada espectacular. Pero entendió una cosa: la transformación. Los vídeos de antes y después de un solo día con sus productos generaban un {0} % más de ventas. Giró por completo hacia el relato de transformación.",
    "\"Voici mon produit\".": "«aquí está mi producto».",
    "{0}. 🏠 @homedesignbysarah - Décoration & Mobilier": "{0}. 🏠 @homedesignbysarah — decoración y muebles",
    "Comment vendre des meubles sur TikTok": "Cómo vender muebles en TikTok",
    "Sarah montrait les mêmes meubles en {0} contextes différents. \"Voici ce meuble dans mon salon moderne\" → \"Voici le même dans un loft industriel\" → \"Voici dans un petit appartement\". Elle a compris que le problème n'était pas le produit, mais les doutes du client : \"Est-ce que ça va match mon intérieur ?\"":
        "Sarah enseñaba los mismos muebles en {0} contextos distintos. «Aquí este mueble en mi salón moderno» → «aquí el mismo en un loft industrial» → «aquí en un piso pequeño». Entendió que el problema no era el producto, sino la duda del cliente: «¿pegará con mi casa?»",
    "Elle crée des \"inspiration rooms\" complètes. Pas juste un meuble, un mood board entier. Le client voit où ça va, comment ça s'assortit, pourquoi c'est beau.":
        "Crea «inspiration rooms» completas. No un mueble suelto, sino un mood board entero. El cliente ve dónde encaja, con qué combina y por qué queda bien.",
    "{0}. 💼 @techreviewjean - Électronique & Tech": "{0}. 💼 @techreviewjean — electrónica y tecnología",
    "Devenir l'expert qui vend": "Convertirse en el experto que vende",
    "Jean revend des téléphones, ordinateurs, et gadgets tech. Mais il ne les vend pas — il les explique. Comparaisons détaillées, cas d'usage spécifiques, alternatives considérées. Il est devenu la source de confiance #{0} pour la tech en France sur TikTok.":
        "Jean revende móviles, ordenadores y gadgets. Pero no los vende: los explica. Comparativas detalladas, casos de uso concretos, alternativas valoradas. Se convirtió en la fuente de confianza n.º {0} de tecnología en Francia dentro de TikTok.",
    "Il crée des vidéos \"FAQ\" anticipées. Il devine les objections avant que le client les ait. \"Oui, je sais que c'est cher, mais voici pourquoi c'est le seul choix logique...\"":
        "Hace vídeos de preguntas frecuentes por adelantado. Adivina las objeciones antes de que el cliente las tenga. «Sí, ya sé que es caro, pero mira por qué es la única opción lógica…»",
    "💡 Les Patterns Communs": "💡 Lo que tienen en común",
    "Si vous analysez ces {0} créateurs (et les {1} autres qu'on aurait pu inclure), des patterns clairs émergent :":
        "Si miras a estos {0} creadores (y los {1} más que podríamos haber incluido), aparecen patrones claros:",
    "{0}. Spécialisation extrême": "{0}. Especialización extrema",
    "Aucun d'eux ne vend \"tout\". Ils sont devenus experts reconnus dans une niche étroite. Mariana = mode éthique. Alexis = transformation fitness. Sarah = décoration accessible. Jean = tech simplifiée.":
        "Ninguno vende «de todo». Cada uno se hizo experto reconocido en un nicho estrecho. Mariana = moda ética. Alexis = transformación fitness. Sarah = decoración asequible. Jean = tecnología explicada fácil.",
    "Produit": "Producto",
    "Ils passent {0}% de leur attention sur le contenu et {1}% sur le produit. La plupart des créateurs échouent font l'inverse : {2}% contenu, {3}% promotion produit.":
        "Dedican el {0} % de su atención al contenido y el {1} % al producto. La mayoría de los creadores que fracasan hacen lo contrario: {2} % contenido, {3} % promoción del producto.",
    "{0}. Vitesse d'itération": "{0}. Velocidad de iteración",
    "Ils publient beaucoup. Mariana publie {0}-{1} fois par jour. Cela veut dire qu'elle teste {2}-{3} angles différents. En une semaine, elle a {4}-{5} variables testées. Elle peut ajuster rapidement ce qui fonctionne.":
        "Publican mucho. Mariana publica {0}-{1} veces al día, o sea que prueba {2}-{3} ángulos distintos. En una semana lleva {4}-{5} variables probadas. Puede ajustar rápido en torno a lo que funciona.",
    "{0}. Humanité authentique": "{0}. Humanidad auténtica",
    "Aucun n'est parfait. Ils montrent leurs faiblesses, leurs échecs, leur processus. Les gens n'achètent pas aux experts parfaits, ils achètent aux humains qu'ils reconnaissent et en qui ils ont confiance.":
        "Ninguno es perfecto. Enseñan sus debilidades, sus fracasos, su proceso. La gente no compra a expertos impecables: compra a personas en las que se reconoce y en las que confía.",
    "Devenez-vous le prochain créateur millionnaire ?": "¿Serás tú el próximo?",
    "Utilisez Qeerah pour analyser vos vidéos comme le font les top créateurs.":
        "Usa Qeerah para analizar tus vídeos como hacen los mejores creadores.",
    "Commencer l'analyse →": "Empezar el análisis →",
}

T_BLOG_CREATEURS["it"] = {
    "{0} Créateurs TikTok Shop Devenus Millionnaires - Qeerah":
        "{0} creator di TikTok Shop diventati milionari - Qeerah",
    "{0} créateurs TikTok Shop devenus millionnaires en {1}. Découvrez leurs stratégies, leurs secrets et ce que vous pouvez en apprendre.":
        "{0} creator di TikTok Shop diventati milionari nel {1}. Le loro strategie, cosa hanno fatto di diverso e cosa puoi imparare.",
    "{0} créateurs TikTok Shop devenus millionnaires": "{0} creator di TikTok Shop diventati milionari",
    "Les stratégies et patterns communs des créateurs qui ont transformé leurs vidéos en empires commerciaux sur TikTok Shop.":
        "Le strategie e gli schemi comuni dei creator che hanno trasformato i loro video in imperi commerciali su TikTok Shop.",
    "← Retour au blog": "← Torna al blog",
    "💰 SUCCESS STORIES": "💰 STORIE DI SUCCESSO",
    "{0} créateurs TikTok Shop devenus millionnaires en {1}": "{0} creator di TikTok Shop diventati milionari nel {1}",
    "📅 Avril {0}": "📅 Aprile {0}",
    "👤 Par l'équipe Qeerah": "👤 Dal team Qeerah",
    "⏱️ {0} min": "⏱️ {0} min",
    "Vous vous demandez si c'est vraiment possible de devenir millionnaire sur TikTok Shop ? La réponse est oui. Voici les histoires de {0} créateurs qui l'ont fait, et ce que nous pouvons en apprendre.":
        "Ti chiedi se si possa davvero diventare milionari su TikTok Shop? Sì. Ecco le storie di {0} creator che ce l'hanno fatta e cosa se ne può imparare.",
    "{0}. 👗 @stylebymariana - Beauté & Mode": "{0}. 👗 @stylebymariana — bellezza e moda",
    "La créatrice qui a disrupta la mode française": "La creator che ha scosso la moda francese",
    "Followers": "Follower",
    "GMV {0}": "GMV {0}",
    "{0} mois": "{0} mesi",
    "Pour {0}M€": "Fino a {0} mln €",
    "Mariana a commencé sans produits propres. Elle revenait des accessoires de mode éthiques et les présentait dans ses vidéos. En {0} mois, elle a atteint {1} figures. Son secret : l'authententicité. Elle montre vraiment comment porter les pièces, des hauls complets, des réactions honnêtes.":
        "Mariana ha iniziato senza prodotti propri. Rivendeva accessori di moda etica e li mostrava nei suoi video. In {0} mesi è arrivata a {1} cifre. Il suo segreto: l'autenticità. Mostra davvero come si indossano i capi, haul completi, reazioni sincere.",
    "🔑 Le Secret :": "🔑 Il segreto:",
    "Elle crée du contenu {0}-{1} fois par jour. Chaque vidéo teste une angle différent. Elle analyse immédiatement ce qui fonctionne et duplique les meilleures performances.":
        "Pubblica contenuti {0}-{1} volte al giorno. Ogni video prova un taglio diverso. Guarda subito cosa funziona e replica i risultati migliori.",
    "{0}. 💪 @fitbyalexis - Fitness & Nutrition": "{0}. 💪 @fitbyalexis — fitness e nutrizione",
    "Du coach personnel à l'empire fitness": "Da personal trainer a impero del fitness",
    "Alexis vendait des guides de fitness et de nutrition. Rien de spectaculaire. Mais il a compris quelque chose : la transformation. Les vidéos \"before/after\" d'une journée avec ses produits généraient {0}% plus de ventes. Il a pivotté complètement vers le storytelling de transformation.":
        "Alexis vendeva guide di fitness e nutrizione. Niente di clamoroso. Ma ha capito una cosa: la trasformazione. I video prima/dopo di una sola giornata con i suoi prodotti generavano il {0} % di vendite in più. Ha virato del tutto sul racconto della trasformazione.",
    "\"Voici mon produit\".": "«ecco il mio prodotto».",
    "{0}. 🏠 @homedesignbysarah - Décoration & Mobilier": "{0}. 🏠 @homedesignbysarah — arredo e mobili",
    "Comment vendre des meubles sur TikTok": "Come vendere mobili su TikTok",
    "Sarah montrait les mêmes meubles en {0} contextes différents. \"Voici ce meuble dans mon salon moderne\" → \"Voici le même dans un loft industriel\" → \"Voici dans un petit appartement\". Elle a compris que le problème n'était pas le produit, mais les doutes du client : \"Est-ce que ça va match mon intérieur ?\"":
        "Sarah mostrava gli stessi mobili in {0} contesti diversi. «Ecco questo pezzo nel mio salotto moderno» → «ecco lo stesso in un loft industriale» → «ecco in un piccolo appartamento». Ha capito che il problema non era il prodotto ma il dubbio del cliente: «starà bene a casa mia?»",
    "Elle crée des \"inspiration rooms\" complètes. Pas juste un meuble, un mood board entier. Le client voit où ça va, comment ça s'assortit, pourquoi c'est beau.":
        "Costruisce intere «inspiration room». Non un mobile soltanto, un moodboard completo. Il cliente vede dove sta bene, con cosa si abbina, perché funziona.",
    "{0}. 💼 @techreviewjean - Électronique & Tech": "{0}. 💼 @techreviewjean — elettronica e tecnologia",
    "Devenir l'expert qui vend": "Diventare l'esperto che vende",
    "Jean revend des téléphones, ordinateurs, et gadgets tech. Mais il ne les vend pas — il les explique. Comparaisons détaillées, cas d'usage spécifiques, alternatives considérées. Il est devenu la source de confiance #{0} pour la tech en France sur TikTok.":
        "Jean rivende telefoni, computer e gadget tecnologici. Ma non li vende: li spiega. Confronti dettagliati, casi d'uso concreti, alternative valutate. È diventato la fonte di fiducia n. {0} per la tecnologia in Francia su TikTok.",
    "Il crée des vidéos \"FAQ\" anticipées. Il devine les objections avant que le client les ait. \"Oui, je sais que c'est cher, mais voici pourquoi c'est le seul choix logique...\"":
        "Fa video di FAQ anticipate. Indovina le obiezioni prima che il cliente le abbia. «Sì, lo so che costa, ma ecco perché è l'unica scelta sensata…»",
    "💡 Les Patterns Communs": "💡 Cosa hanno in comune",
    "Si vous analysez ces {0} créateurs (et les {1} autres qu'on aurait pu inclure), des patterns clairs émergent :":
        "Se guardi questi {0} creator (e gli altri {1} che avremmo potuto includere), emergono schemi chiari:",
    "{0}. Spécialisation extrême": "{0}. Specializzazione estrema",
    "Aucun d'eux ne vend \"tout\". Ils sont devenus experts reconnus dans une niche étroite. Mariana = mode éthique. Alexis = transformation fitness. Sarah = décoration accessible. Jean = tech simplifiée.":
        "Nessuno di loro vende «tutto». Ognuno è diventato un riferimento in una nicchia stretta. Mariana = moda etica. Alexis = trasformazione fitness. Sarah = arredo accessibile. Jean = tecnologia spiegata semplice.",
    "Produit": "Prodotto",
    "Ils passent {0}% de leur attention sur le contenu et {1}% sur le produit. La plupart des créateurs échouent font l'inverse : {2}% contenu, {3}% promotion produit.":
        "Mettono il {0} % dell'attenzione sul contenuto e il {1} % sul prodotto. La maggior parte dei creator che falliscono fa il contrario: {2} % contenuto, {3} % promozione del prodotto.",
    "{0}. Vitesse d'itération": "{0}. Velocità di iterazione",
    "Ils publient beaucoup. Mariana publie {0}-{1} fois par jour. Cela veut dire qu'elle teste {2}-{3} angles différents. En une semaine, elle a {4}-{5} variables testées. Elle peut ajuster rapidement ce qui fonctionne.":
        "Pubblicano molto. Mariana pubblica {0}-{1} volte al giorno, quindi prova {2}-{3} tagli diversi. In una settimana sono {4}-{5} variabili testate. Può correggere in fretta puntando su ciò che funziona.",
    "{0}. Humanité authentique": "{0}. Umanità autentica",
    "Aucun n'est parfait. Ils montrent leurs faiblesses, leurs échecs, leur processus. Les gens n'achètent pas aux experts parfaits, ils achètent aux humains qu'ils reconnaissent et en qui ils ont confiance.":
        "Nessuno è perfetto. Mostrano i loro limiti, i fallimenti, il processo. La gente non compra dagli esperti impeccabili: compra da persone in cui si riconosce e di cui si fida.",
    "Devenez-vous le prochain créateur millionnaire ?": "Sarai tu il prossimo?",
    "Utilisez Qeerah pour analyser vos vidéos comme le font les top créateurs.":
        "Usa Qeerah per analizzare i tuoi video come fanno i migliori creator.",
    "Commencer l'analyse →": "Inizia l'analisi →",
}

T_BLOG_CREATEURS["pt-br"] = {
    "{0} Créateurs TikTok Shop Devenus Millionnaires - Qeerah":
        "{0} criadores do TikTok Shop que viraram milionários - Qeerah",
    "{0} créateurs TikTok Shop devenus millionnaires en {1}. Découvrez leurs stratégies, leurs secrets et ce que vous pouvez en apprendre.":
        "{0} criadores do TikTok Shop que viraram milionários em {1}. As estratégias deles, o que fizeram de diferente e o que dá para aprender.",
    "{0} créateurs TikTok Shop devenus millionnaires": "{0} criadores do TikTok Shop que viraram milionários",
    "Les stratégies et patterns communs des créateurs qui ont transformé leurs vidéos en empires commerciaux sur TikTok Shop.":
        "As estratégias e os padrões em comum de criadores que transformaram seus vídeos em impérios comerciais no TikTok Shop.",
    "← Retour au blog": "← Voltar ao blog",
    "💰 SUCCESS STORIES": "💰 HISTÓRIAS DE SUCESSO",
    "{0} créateurs TikTok Shop devenus millionnaires en {1}": "{0} criadores do TikTok Shop que viraram milionários em {1}",
    "📅 Avril {0}": "📅 Abril de {0}",
    "👤 Par l'équipe Qeerah": "👤 Pelo time da Qeerah",
    "⏱️ {0} min": "⏱️ {0} min",
    "Vous vous demandez si c'est vraiment possible de devenir millionnaire sur TikTok Shop ? La réponse est oui. Voici les histoires de {0} créateurs qui l'ont fait, et ce que nous pouvons en apprendre.":
        "Você se pergunta se dá mesmo para ficar milionário no TikTok Shop? Dá. Estas são as histórias de {0} criadores que conseguiram e o que dá para aprender com elas.",
    "{0}. 👗 @stylebymariana - Beauté & Mode": "{0}. 👗 @stylebymariana — beleza e moda",
    "La créatrice qui a disrupta la mode française": "A criadora que sacudiu a moda francesa",
    "Followers": "Seguidores",
    "GMV {0}": "GMV {0}",
    "{0} mois": "{0} meses",
    "Pour {0}M€": "Até € {0} mi",
    "Mariana a commencé sans produits propres. Elle revenait des accessoires de mode éthiques et les présentait dans ses vidéos. En {0} mois, elle a atteint {1} figures. Son secret : l'authententicité. Elle montre vraiment comment porter les pièces, des hauls complets, des réactions honnêtes.":
        "Mariana começou sem produtos próprios. Revendia acessórios de moda ética e mostrava nos vídeos. Em {0} meses chegou a {1} dígitos. O segredo dela: autenticidade. Ela mostra de verdade como usar as peças, hauls completos, reações honestas.",
    "🔑 Le Secret :": "🔑 O segredo:",
    "Elle crée du contenu {0}-{1} fois par jour. Chaque vidéo teste une angle différent. Elle analyse immédiatement ce qui fonctionne et duplique les meilleures performances.":
        "Ela cria conteúdo {0}-{1} vezes por dia. Cada vídeo testa um ângulo diferente. Olha na hora o que funcionou e repete o que rende mais.",
    "{0}. 💪 @fitbyalexis - Fitness & Nutrition": "{0}. 💪 @fitbyalexis — fitness e nutrição",
    "Du coach personnel à l'empire fitness": "De personal trainer a império fitness",
    "Alexis vendait des guides de fitness et de nutrition. Rien de spectaculaire. Mais il a compris quelque chose : la transformation. Les vidéos \"before/after\" d'une journée avec ses produits généraient {0}% plus de ventes. Il a pivotté complètement vers le storytelling de transformation.":
        "Alexis vendia guias de treino e nutrição. Nada de espetacular. Mas entendeu uma coisa: transformação. Vídeos de antes e depois de um único dia com os produtos dele geravam {0} % mais vendas. Ele virou de vez para a narrativa de transformação.",
    "\"Voici mon produit\".": "“aqui está o meu produto”.",
    "{0}. 🏠 @homedesignbysarah - Décoration & Mobilier": "{0}. 🏠 @homedesignbysarah — decoração e móveis",
    "Comment vendre des meubles sur TikTok": "Como vender móveis no TikTok",
    "Sarah montrait les mêmes meubles en {0} contextes différents. \"Voici ce meuble dans mon salon moderne\" → \"Voici le même dans un loft industriel\" → \"Voici dans un petit appartement\". Elle a compris que le problème n'était pas le produit, mais les doutes du client : \"Est-ce que ça va match mon intérieur ?\"":
        "Sarah mostrava os mesmos móveis em {0} contextos diferentes. “Aqui essa peça na minha sala moderna” → “aqui a mesma num loft industrial” → “aqui num apartamento pequeno”. Ela entendeu que o problema não era o produto, e sim a dúvida do cliente: “vai combinar com a minha casa?”",
    "Elle crée des \"inspiration rooms\" complètes. Pas juste un meuble, un mood board entier. Le client voit où ça va, comment ça s'assortit, pourquoi c'est beau.":
        "Ela monta “inspiration rooms” inteiras. Não um móvel solto, um mood board completo. O cliente vê onde encaixa, com o que combina e por que fica bonito.",
    "{0}. 💼 @techreviewjean - Électronique & Tech": "{0}. 💼 @techreviewjean — eletrônicos e tecnologia",
    "Devenir l'expert qui vend": "Virar o especialista que vende",
    "Jean revend des téléphones, ordinateurs, et gadgets tech. Mais il ne les vend pas — il les explique. Comparaisons détaillées, cas d'usage spécifiques, alternatives considérées. Il est devenu la source de confiance #{0} pour la tech en France sur TikTok.":
        "Jean revende celulares, computadores e gadgets. Mas ele não vende: ele explica. Comparações detalhadas, casos de uso concretos, alternativas avaliadas. Virou a fonte de confiança n.º {0} de tecnologia na França dentro do TikTok.",
    "Il crée des vidéos \"FAQ\" anticipées. Il devine les objections avant que le client les ait. \"Oui, je sais que c'est cher, mais voici pourquoi c'est le seul choix logique...\"":
        "Ele faz vídeos de perguntas frequentes antecipadas. Adivinha as objeções antes de o cliente ter. “Sim, eu sei que é caro, mas olha por que é a única escolha lógica…”",
    "💡 Les Patterns Communs": "💡 O que eles têm em comum",
    "Si vous analysez ces {0} créateurs (et les {1} autres qu'on aurait pu inclure), des patterns clairs émergent :":
        "Se você olhar esses {0} criadores (e os outros {1} que dariam para incluir), aparecem padrões claros:",
    "{0}. Spécialisation extrême": "{0}. Especialização extrema",
    "Aucun d'eux ne vend \"tout\". Ils sont devenus experts reconnus dans une niche étroite. Mariana = mode éthique. Alexis = transformation fitness. Sarah = décoration accessible. Jean = tech simplifiée.":
        "Nenhum deles vende “tudo”. Cada um virou referência reconhecida num nicho estreito. Mariana = moda ética. Alexis = transformação fitness. Sarah = decoração acessível. Jean = tecnologia explicada fácil.",
    "Produit": "Produto",
    "Ils passent {0}% de leur attention sur le contenu et {1}% sur le produit. La plupart des créateurs échouent font l'inverse : {2}% contenu, {3}% promotion produit.":
        "Eles colocam {0} % da atenção no conteúdo e {1} % no produto. A maioria dos criadores que fracassa faz o contrário: {2} % conteúdo, {3} % divulgação do produto.",
    "{0}. Vitesse d'itération": "{0}. Velocidade de teste",
    "Ils publient beaucoup. Mariana publie {0}-{1} fois par jour. Cela veut dire qu'elle teste {2}-{3} angles différents. En une semaine, elle a {4}-{5} variables testées. Elle peut ajuster rapidement ce qui fonctionne.":
        "Eles publicam muito. Mariana posta {0}-{1} vezes por dia, ou seja, testa {2}-{3} ângulos diferentes. Em uma semana são {4}-{5} variáveis testadas. Dá para ajustar rápido em cima do que funciona.",
    "{0}. Humanité authentique": "{0}. Humanidade de verdade",
    "Aucun n'est parfait. Ils montrent leurs faiblesses, leurs échecs, leur processus. Les gens n'achètent pas aux experts parfaits, ils achètent aux humains qu'ils reconnaissent et en qui ils ont confiance.":
        "Nenhum é perfeito. Eles mostram as fraquezas, os fracassos, o processo. As pessoas não compram de especialistas impecáveis: compram de gente com quem se identificam e em quem confiam.",
    "Devenez-vous le prochain créateur millionnaire ?": "Você vai ser o próximo?",
    "Utilisez Qeerah pour analyser vos vidéos comme le font les top créateurs.":
        "Use a Qeerah para analisar seus vídeos como fazem os melhores criadores.",
    "Commencer l'analyse →": "Começar a análise →",
}

T_BLOG_CREATEURS["en-ie"] = dict(T_BLOG_CREATEURS["en"])
T_BLOG_CREATEURS["es-mx"] = dict(T_BLOG_CREATEURS["es"])
