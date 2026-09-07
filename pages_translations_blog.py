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


# ═══════════════════════════════════════════════════════════════════════════
# /blog/histoire-tiktok-shop
# ═══════════════════════════════════════════════════════════════════════════
T_BLOG_HISTOIRE: dict[str, dict[str, str]] = {}

T_BLOG_HISTOIRE["en"] = {
    "Histoire de TikTok Shop : De la Chine à la France - Qeerah":
        "The story of TikTok Shop: from China to France - Qeerah",
    "L'histoire complète de TikTok Shop : Du lancement à la domination mondiale. Découvrez comment TikTok Shop a révolutionné le e-commerce.":
        "The full story of TikTok Shop, from launch to global reach — and how it turned e-commerce on its head.",
    "L'histoire complète de TikTok Shop : de la Chine à la domination mondiale":
        "The full story of TikTok Shop: from China to global reach",
    "Comment TikTok Shop est passé d'une expérience asiatique à une révolution mondiale du e-commerce, de {0} à aujourd'hui.":
        "How TikTok Shop went from an Asian experiment to a worldwide shake-up of e-commerce, from {0} to today.",
    "← Retour au blog": "← Back to the blog",
    "📖 HISTOIRE": "📖 HISTORY",
    "L'histoire complète de TikTok Shop : De la Chine à la domination mondiale":
        "The full story of TikTok Shop: from China to global reach",
    "📅 Mis à jour mai {0}": "📅 Updated May {0}",
    "👤 Par l'équipe Qeerah": "👤 By the Qeerah team",
    "⏱️ {0} min": "⏱️ {0} min",
    "🌍 Prologue : L'ère du e-commerce social": "🌍 Prologue: the age of social commerce",
    "Le e-commerce a longtemps été dominé par les marketplaces traditionnelles : Amazon, eBay, Alibaba. Mais depuis quelques années, une révolution s'opère. Le shopping social — la fusion du divertissement et du commerce — est devenu la norme. TikTok Shop en est la manifestation la plus claire et la plus puissante.":
        "For a long time e-commerce belonged to the traditional marketplaces: Amazon, eBay, Alibaba. But over the last few years something has shifted. Social shopping — entertainment and commerce fused together — has become the norm. TikTok Shop is its clearest and most powerful form.",
    "📱 {0} : Les débuts en Asie du Sud-Est": "📱 {0}: the start in Southeast Asia",
    "ByteDance, la société mère de TikTok, lance": "ByteDance, TikTok's parent company, launches",
    "en {0} en Thaïlande et en Indonésie. L'objectif était simple : transformer la plateforme de divertissement en machine de vente e-commerce. Les résultats ont été spectaculaires.":
        "in {0} in Thailand and Indonesia. The goal was simple: turn an entertainment platform into a selling machine. The results were spectacular.",
    "En quelques mois, les créateurs thaïlandais et indonésiens ont généré des millions en ventes directement depuis leurs vidéos. C'était une révolution pour ces marchés — plus besoin de site e-commerce complexe, plus besoin de publicité coûteuse. Juste du contenu, et des ventes instantanées.":
        "Within months, Thai and Indonesian creators were making millions in sales straight from their videos. For those markets it changed everything — no complicated online shop, no expensive advertising. Just content, and sales on the spot.",
    "💡 Insight :": "💡 The insight:",
    "Les premiers testeurs asiatiques ont rapidement compris que le secret n'était pas le produit, mais le contenu. Un créateur avec une audience fidèle et du contenu authentique pouvait vendre presque n'importe quoi.":
        "The first Asian testers quickly worked out that the secret wasn't the product but the content. A creator with a loyal audience and honest content could sell almost anything.",
    "🇨🇳 {0}-{1} : La domination chinoise": "🇨🇳 {0}-{1}: China takes the lead",
    "Douyin (la version chinoise de TikTok) intègre déjà le live shopping depuis des années. ByteDance étend ces capacités à TikTok Shop sur le marché chinois. Les chiffres deviennent fous :":
        "Douyin (TikTok's Chinese version) had been doing live shopping for years. ByteDance brought those capabilities to TikTok Shop in the Chinese market. The numbers went wild:",
    "Des centaines de milliards en GMV (Gross Merchandise Value) annuels":
        "Hundreds of billions in annual GMV (gross merchandise value)",
    "Des millions de créateurs générant des revenus six ou sept chiffres":
        "Millions of creators earning six or seven figures",
    "La naissance de la catégorie \"live shopping\" comme format dominant":
        "The birth of live shopping as the dominant format",
    "La Chine devient le laboratoire d'innovation de TikTok Shop, établissant les patterns que le reste du monde suivrait.":
        "China became TikTok Shop's laboratory, setting the patterns the rest of the world would follow.",
    "🇺🇸 {0} : L'arrivée chaotique aux USA": "🇺🇸 {0}: a messy arrival in the US",
    "TikTok Shop arrive finalement aux États-Unis en {0}, mais avec des obstacles politiques et réglementaires. Malgré les défis législatifs, la plateforme gagne rapidement du terrain aux USA, principalement parmi la Génération Z et les créateurs de niche.":
        "TikTok Shop finally reached the United States in {0}, but with political and regulatory obstacles in the way. Despite the legislative fights, the platform gained ground fast, mostly among Gen Z and niche creators.",
    "Les créateurs américains découvrent rapidement que la formule fonctionne : contenu authentique + audience engagée = ventes directes. Des créateurs de mode, beauté, fitness et bien-être dominent les premiers mois.":
        "American creators quickly found the formula worked: honest content + an engaged audience = direct sales. Fashion, beauty, fitness and wellness creators led the first months.",
    "🇫🇷 Fin {0} - Aujourd'hui : L'explosion française": "🇫🇷 Late {0} to today: France takes off",
    "TikTok Shop arrive en France fin {0} et le marché explose. En {1}, la France est l'un des plus grands marchés TikTok Shop en Europe. Voici pourquoi :":
        "TikTok Shop landed in France in late {0} and the market took off. By {1} France is one of the largest TikTok Shop markets in Europe. Here's why:",
    "Audience jeune :": "A young audience:",
    "TikTok a une base d'utilisateurs énorme en France ({0}+ millions)":
        "TikTok has a huge user base in France ({0}+ million)",
    "Culture créative :": "A creative culture:",
    "Les Français embrassent les créateurs et les influenceurs": "French audiences take to creators and influencers",
    "Marché de niche :": "Room for niches:",
    "Les petites marques et créateurs trouvent un canal direct sans coûts publicitaires énormes":
        "Small brands and creators get a direct channel without huge ad budgets",
    "Beauté et Mode :": "Beauty and fashion:",
    "Deux catégories où la France excelle": "Two categories where France is strong",
    "💰 L'impact économique": "💰 The economic impact",
    "En {0}, TikTok Shop représente une part significative du e-commerce en France. Des chiffres estimés :":
        "In {0}, TikTok Shop accounts for a meaningful share of French e-commerce. Estimated figures:",
    "Plus de {0} créateurs vendant activement sur TikTok Shop en France":
        "More than {0} creators actively selling on TikTok Shop in France",
    "Des transactions quotidiennes dans les milliards d'euros": "Daily transactions in the billions of euros",
    "Plus de {0} PME françaises intégrées à la plateforme": "More than {0} French small businesses on the platform",
    "🔮 Qu'est-ce qui a changé ?": "🔮 What actually changed",
    "TikTok Shop n'a pas inventé le shopping social, mais c'est la plateforme qui l'a démocratisé. Avant, il fallait :":
        "TikTok Shop didn't invent social shopping, but it is the platform that opened it to everyone. Before, you needed:",
    "Un site e-commerce": "An online shop",
    "Un budget marketing": "A marketing budget",
    "Une expertise technique": "Technical know-how",
    "Des infrastructures logistiques": "Logistics behind you",
    "Avec TikTok Shop, il te faut juste :": "With TikTok Shop, all you need is:",
    "Un téléphone": "A phone",
    "Du contenu authentique": "Honest content",
    "Une audience engagée": "An engaged audience",
    "🚀 Les leçons clés": "🚀 The lessons that matter",
    "{0}. Le contenu est roi": "{0}. Content rules",
    "Les meilleurs vendeurs sur TikTok Shop ne sont pas nécessairement les meilleurs marketers. Ce sont les créateurs qui font du contenu authentique et divertissant. Le produit vient en second.":
        "The best sellers on TikTok Shop aren't necessarily the best marketers. They're the creators who make honest, entertaining content. The product comes second.",
    "la promotion": "promotion",
    "Vous ne pouvez pas \"acheter\" une audience sur TikTok Shop. Vous devez la construire. Les créateurs avec une vraie communauté vendent {0}x plus que ceux avec simplement des followers.":
        "You can't buy an audience on TikTok Shop. You have to build one. Creators with a real community sell {0}× more than those who merely have followers.",
    "{0}. La niche c'est l'argent": "{0}. The niche is where the money is",
    "Les plus grands vendeurs se concentrent sur une niche spécifique et deviennent incontournables dans cette niche. Pas de généralistes, seulement des spécialistes.":
        "The biggest sellers pick one narrow niche and become impossible to ignore within it. No generalists, only specialists.",
    "📊 Les chiffres aujourd'hui (mai {0})": "📊 Where the numbers stand (May {0})",
    "TikTok Shop France : ~{0} milliards € annuels estimés": "TikTok Shop France: an estimated €{0} billion a year",
    "Créateurs gagnant {0} chiffres+ : ~{1}": "Creators earning {0} figures or more: ~{1}",
    "Catégories dominantes : Mode, Beauté, Bien-être, Électronique, Maison":
        "Leading categories: fashion, beauty, wellness, electronics, home",
    "Âge moyen des vendeurs : {0}-{1} ans": "Average age of sellers: {0}-{1}",
    "🎯 Conclusion : Ce n'est que le début": "🎯 In closing: this is only the beginning",
    "TikTok Shop ne va que croître. Les prédictions pour {0}-{1} ? Des intégrations plus profondes, plus de tools d'analyse (comme Qeerah 😉), et potentiellement le plus grand changement : les agences et les marques établies qui vont entièrement réviser leur stratégie autour de TikTok Shop.":
        "TikTok Shop is only going to grow. Predictions for {0}-{1}? Deeper integrations, more analysis tools (like Qeerah 😉), and possibly the biggest shift of all: agencies and established brands rebuilding their whole strategy around TikTok Shop.",
    "L'histoire de TikTok Shop n'est qu'au chapitre {0}. Nous sommes au moment clé où les créateurs peut devenir millionnaire, où les agences peuvent scaler leurs clients, et où les marques peuvent atteindre leur audience de manière directe et authentique.":
        "The story of TikTok Shop is only at chapter {0}. This is the moment where creators can get rich, where agencies can scale their clients, and where brands can reach their audience directly and honestly.",
    "Prêt à analyser vos vidéos TikTok Shop ?": "Ready to analyse your TikTok Shop videos?",
    "Utilisez Qeerah pour comprendre exactement ce qui fonctionne dans votre contenu.":
        "Use Qeerah to see exactly what's working in your content.",
    "Commencer gratuitement →": "Start free →",
}

T_BLOG_HISTOIRE["de"] = {
    "Histoire de TikTok Shop : De la Chine à la France - Qeerah":
        "Die Geschichte von TikTok Shop: von China nach Frankreich - Qeerah",
    "L'histoire complète de TikTok Shop : Du lancement à la domination mondiale. Découvrez comment TikTok Shop a révolutionné le e-commerce.":
        "Die ganze Geschichte von TikTok Shop, vom Start bis zur weltweiten Reichweite — und wie es den E-Commerce umgekrempelt hat.",
    "L'histoire complète de TikTok Shop : de la Chine à la domination mondiale":
        "Die ganze Geschichte von TikTok Shop: von China zur weltweiten Reichweite",
    "Comment TikTok Shop est passé d'une expérience asiatique à une révolution mondiale du e-commerce, de {0} à aujourd'hui.":
        "Wie TikTok Shop von einem asiatischen Versuch zu einem weltweiten Umbruch im E-Commerce wurde, von {0} bis heute.",
    "← Retour au blog": "← Zurück zum Blog",
    "📖 HISTOIRE": "📖 GESCHICHTE",
    "L'histoire complète de TikTok Shop : De la Chine à la domination mondiale":
        "Die ganze Geschichte von TikTok Shop: von China zur weltweiten Reichweite",
    "📅 Mis à jour mai {0}": "📅 Aktualisiert im Mai {0}",
    "👤 Par l'équipe Qeerah": "👤 Vom Qeerah-Team",
    "⏱️ {0} min": "⏱️ {0} Min.",
    "🌍 Prologue : L'ère du e-commerce social": "🌍 Vorspann: die Zeit des Social Commerce",
    "Le e-commerce a longtemps été dominé par les marketplaces traditionnelles : Amazon, eBay, Alibaba. Mais depuis quelques années, une révolution s'opère. Le shopping social — la fusion du divertissement et du commerce — est devenu la norme. TikTok Shop en est la manifestation la plus claire et la plus puissante.":
        "Lange gehörte der E-Commerce den klassischen Marktplätzen: Amazon, eBay, Alibaba. Doch seit einigen Jahren verschiebt sich etwas. Social Shopping — Unterhaltung und Handel verschmolzen — ist zur Norm geworden. TikTok Shop ist davon die klarste und stärkste Ausprägung.",
    "📱 {0} : Les débuts en Asie du Sud-Est": "📱 {0}: der Anfang in Südostasien",
    "ByteDance, la société mère de TikTok, lance": "ByteDance, die Muttergesellschaft von TikTok, startet",
    "en {0} en Thaïlande et en Indonésie. L'objectif était simple : transformer la plateforme de divertissement en machine de vente e-commerce. Les résultats ont été spectaculaires.":
        "{0} in Thailand und Indonesien. Das Ziel war einfach: aus einer Unterhaltungsplattform eine Verkaufsmaschine machen. Die Ergebnisse waren spektakulär.",
    "En quelques mois, les créateurs thaïlandais et indonésiens ont généré des millions en ventes directement depuis leurs vidéos. C'était une révolution pour ces marchés — plus besoin de site e-commerce complexe, plus besoin de publicité coûteuse. Juste du contenu, et des ventes instantanées.":
        "Binnen Monaten machten thailändische und indonesische Creators Millionen an Umsatz direkt aus ihren Videos. Für diese Märkte änderte das alles — kein aufwendiger Onlineshop mehr, keine teure Werbung. Nur Inhalt, und Verkäufe auf der Stelle.",
    "💡 Insight :": "💡 Die Erkenntnis:",
    "Les premiers testeurs asiatiques ont rapidement compris que le secret n'était pas le produit, mais le contenu. Un créateur avec une audience fidèle et du contenu authentique pouvait vendre presque n'importe quoi.":
        "Die ersten asiatischen Tester begriffen schnell, dass das Geheimnis nicht das Produkt war, sondern der Inhalt. Ein Creator mit treuem Publikum und ehrlichen Inhalten konnte fast alles verkaufen.",
    "🇨🇳 {0}-{1} : La domination chinoise": "🇨🇳 {0}-{1}: China übernimmt die Führung",
    "Douyin (la version chinoise de TikTok) intègre déjà le live shopping depuis des années. ByteDance étend ces capacités à TikTok Shop sur le marché chinois. Les chiffres deviennent fous :":
        "Douyin (die chinesische Version von TikTok) machte seit Jahren Live-Shopping. ByteDance brachte diese Möglichkeiten auf TikTok Shop im chinesischen Markt. Die Zahlen wurden verrückt:",
    "Des centaines de milliards en GMV (Gross Merchandise Value) annuels":
        "Hunderte Milliarden GMV (Gross Merchandise Value) pro Jahr",
    "Des millions de créateurs générant des revenus six ou sept chiffres":
        "Millionen Creators mit sechs- oder siebenstelligen Einnahmen",
    "La naissance de la catégorie \"live shopping\" comme format dominant":
        "Die Geburt des Live-Shoppings als bestimmendes Format",
    "La Chine devient le laboratoire d'innovation de TikTok Shop, établissant les patterns que le reste du monde suivrait.":
        "China wurde zum Labor von TikTok Shop und setzte die Muster, denen der Rest der Welt folgte.",
    "🇺🇸 {0} : L'arrivée chaotique aux USA": "🇺🇸 {0}: ein holpriger Start in den USA",
    "TikTok Shop arrive finalement aux États-Unis en {0}, mais avec des obstacles politiques et réglementaires. Malgré les défis législatifs, la plateforme gagne rapidement du terrain aux USA, principalement parmi la Génération Z et les créateurs de niche.":
        "TikTok Shop kam {0} endlich in die USA, aber mit politischen und regulatorischen Hürden. Trotz der Gesetzeskämpfe legte die Plattform schnell zu, vor allem bei der Gen Z und bei Nischen-Creators.",
    "Les créateurs américains découvrent rapidement que la formule fonctionne : contenu authentique + audience engagée = ventes directes. Des créateurs de mode, beauté, fitness et bien-être dominent les premiers mois.":
        "Amerikanische Creators merkten schnell, dass die Formel aufgeht: ehrliche Inhalte + engagiertes Publikum = direkte Verkäufe. Mode, Beauty, Fitness und Wellness bestimmten die ersten Monate.",
    "🇫🇷 Fin {0} - Aujourd'hui : L'explosion française": "🇫🇷 Ende {0} bis heute: Frankreich hebt ab",
    "TikTok Shop arrive en France fin {0} et le marché explose. En {1}, la France est l'un des plus grands marchés TikTok Shop en Europe. Voici pourquoi :":
        "TikTok Shop kam Ende {0} nach Frankreich, und der Markt explodierte. {1} ist Frankreich einer der größten TikTok-Shop-Märkte Europas. Warum:",
    "Audience jeune :": "Junges Publikum:",
    "TikTok a une base d'utilisateurs énorme en France ({0}+ millions)":
        "TikTok hat in Frankreich eine riesige Nutzerbasis (über {0} Millionen)",
    "Culture créative :": "Kreative Kultur:",
    "Les Français embrassent les créateurs et les influenceurs": "Das französische Publikum nimmt Creators und Influencer an",
    "Marché de niche :": "Platz für Nischen:",
    "Les petites marques et créateurs trouvent un canal direct sans coûts publicitaires énormes":
        "Kleine Marken und Creators bekommen einen Direktkanal ohne riesige Werbebudgets",
    "Beauté et Mode :": "Beauty und Mode:",
    "Deux catégories où la France excelle": "Zwei Kategorien, in denen Frankreich stark ist",
    "💰 L'impact économique": "💰 Die wirtschaftliche Wirkung",
    "En {0}, TikTok Shop représente une part significative du e-commerce en France. Des chiffres estimés :":
        "{0} macht TikTok Shop einen spürbaren Teil des französischen E-Commerce aus. Geschätzte Zahlen:",
    "Plus de {0} créateurs vendant activement sur TikTok Shop en France":
        "Mehr als {0} Creators verkaufen in Frankreich aktiv über TikTok Shop",
    "Des transactions quotidiennes dans les milliards d'euros": "Tägliche Transaktionen im Milliardenbereich",
    "Plus de {0} PME françaises intégrées à la plateforme": "Mehr als {0} französische Kleinbetriebe auf der Plattform",
    "🔮 Qu'est-ce qui a changé ?": "🔮 Was sich wirklich geändert hat",
    "TikTok Shop n'a pas inventé le shopping social, mais c'est la plateforme qui l'a démocratisé. Avant, il fallait :":
        "TikTok Shop hat Social Shopping nicht erfunden, aber es für alle geöffnet. Vorher brauchte man:",
    "Un site e-commerce": "Einen Onlineshop",
    "Un budget marketing": "Ein Marketingbudget",
    "Une expertise technique": "Technisches Können",
    "Des infrastructures logistiques": "Logistik im Rücken",
    "Avec TikTok Shop, il te faut juste :": "Mit TikTok Shop brauchst du nur:",
    "Un téléphone": "Ein Handy",
    "Du contenu authentique": "Ehrliche Inhalte",
    "Une audience engagée": "Ein engagiertes Publikum",
    "🚀 Les leçons clés": "🚀 Die Lehren, auf die es ankommt",
    "{0}. Le contenu est roi": "{0}. Der Inhalt regiert",
    "Les meilleurs vendeurs sur TikTok Shop ne sont pas nécessairement les meilleurs marketers. Ce sont les créateurs qui font du contenu authentique et divertissant. Le produit vient en second.":
        "Die besten Verkäufer auf TikTok Shop sind nicht unbedingt die besten Marketer. Es sind die Creators, die ehrliche, unterhaltsame Inhalte machen. Das Produkt kommt danach.",
    "la promotion": "Werbung",
    "Vous ne pouvez pas \"acheter\" une audience sur TikTok Shop. Vous devez la construire. Les créateurs avec une vraie communauté vendent {0}x plus que ceux avec simplement des followers.":
        "Ein Publikum lässt sich auf TikTok Shop nicht kaufen. Man muss es aufbauen. Creators mit echter Community verkaufen {0}× mehr als solche, die bloß Follower haben.",
    "{0}. La niche c'est l'argent": "{0}. In der Nische liegt das Geld",
    "Les plus grands vendeurs se concentrent sur une niche spécifique et deviennent incontournables dans cette niche. Pas de généralistes, seulement des spécialistes.":
        "Die größten Verkäufer suchen sich eine enge Nische und werden darin unumgänglich. Keine Generalisten, nur Spezialisten.",
    "📊 Les chiffres aujourd'hui (mai {0})": "📊 Wo die Zahlen stehen (Mai {0})",
    "TikTok Shop France : ~{0} milliards € annuels estimés": "TikTok Shop Frankreich: geschätzt rund {0} Milliarden € im Jahr",
    "Créateurs gagnant {0} chiffres+ : ~{1}": "Creators mit {0} Stellen oder mehr: ~{1}",
    "Catégories dominantes : Mode, Beauté, Bien-être, Électronique, Maison":
        "Führende Kategorien: Mode, Beauty, Wellness, Elektronik, Haushalt",
    "Âge moyen des vendeurs : {0}-{1} ans": "Durchschnittsalter der Verkäufer: {0}-{1} Jahre",
    "🎯 Conclusion : Ce n'est que le début": "🎯 Zum Schluss: das ist erst der Anfang",
    "TikTok Shop ne va que croître. Les prédictions pour {0}-{1} ? Des intégrations plus profondes, plus de tools d'analyse (comme Qeerah 😉), et potentiellement le plus grand changement : les agences et les marques établies qui vont entièrement réviser leur stratégie autour de TikTok Shop.":
        "TikTok Shop wird nur größer. Prognosen für {0}-{1}? Tiefere Integrationen, mehr Analysewerkzeuge (wie Qeerah 😉) und vielleicht die größte Verschiebung überhaupt: Agenturen und etablierte Marken, die ihre gesamte Strategie um TikTok Shop herum neu bauen.",
    "L'histoire de TikTok Shop n'est qu'au chapitre {0}. Nous sommes au moment clé où les créateurs peut devenir millionnaire, où les agences peuvent scaler leurs clients, et où les marques peuvent atteindre leur audience de manière directe et authentique.":
        "Die Geschichte von TikTok Shop steht erst bei Kapitel {0}. Wir sind an dem Punkt, an dem Creators reich werden können, Agenturen ihre Kunden skalieren können und Marken ihr Publikum direkt und ehrlich erreichen.",
    "Prêt à analyser vos vidéos TikTok Shop ?": "Bereit, deine TikTok-Shop-Videos zu analysieren?",
    "Utilisez Qeerah pour comprendre exactement ce qui fonctionne dans votre contenu.":
        "Nutz Qeerah, um genau zu sehen, was in deinen Inhalten funktioniert.",
    "Commencer gratuitement →": "Kostenlos starten →",
}

T_BLOG_HISTOIRE["es"] = {
    "Histoire de TikTok Shop : De la Chine à la France - Qeerah":
        "La historia de TikTok Shop: de China a Francia - Qeerah",
    "L'histoire complète de TikTok Shop : Du lancement à la domination mondiale. Découvrez comment TikTok Shop a révolutionné le e-commerce.":
        "La historia completa de TikTok Shop, del lanzamiento al alcance mundial, y cómo puso patas arriba el comercio electrónico.",
    "L'histoire complète de TikTok Shop : de la Chine à la domination mondiale":
        "La historia completa de TikTok Shop: de China al alcance mundial",
    "Comment TikTok Shop est passé d'une expérience asiatique à une révolution mondiale du e-commerce, de {0} à aujourd'hui.":
        "Cómo TikTok Shop pasó de ser un experimento asiático a una revolución mundial del comercio electrónico, de {0} a hoy.",
    "← Retour au blog": "← Volver al blog",
    "📖 HISTOIRE": "📖 HISTORIA",
    "L'histoire complète de TikTok Shop : De la Chine à la domination mondiale":
        "La historia completa de TikTok Shop: de China al alcance mundial",
    "📅 Mis à jour mai {0}": "📅 Actualizado en mayo de {0}",
    "👤 Par l'équipe Qeerah": "👤 Por el equipo de Qeerah",
    "⏱️ {0} min": "⏱️ {0} min",
    "🌍 Prologue : L'ère du e-commerce social": "🌍 Prólogo: la era del comercio social",
    "Le e-commerce a longtemps été dominé par les marketplaces traditionnelles : Amazon, eBay, Alibaba. Mais depuis quelques années, une révolution s'opère. Le shopping social — la fusion du divertissement et du commerce — est devenu la norme. TikTok Shop en est la manifestation la plus claire et la plus puissante.":
        "Durante mucho tiempo el comercio electrónico fue cosa de los marketplaces clásicos: Amazon, eBay, Alibaba. Pero desde hace unos años algo ha cambiado. Las compras sociales —entretenimiento y comercio fundidos— se han vuelto la norma. TikTok Shop es su forma más clara y más potente.",
    "📱 {0} : Les débuts en Asie du Sud-Est": "📱 {0}: los inicios en el Sudeste Asiático",
    "ByteDance, la société mère de TikTok, lance": "ByteDance, la empresa matriz de TikTok, lanza",
    "en {0} en Thaïlande et en Indonésie. L'objectif était simple : transformer la plateforme de divertissement en machine de vente e-commerce. Les résultats ont été spectaculaires.":
        "en {0} en Tailandia e Indonesia. El objetivo era simple: convertir una plataforma de entretenimiento en una máquina de vender. Los resultados fueron espectaculares.",
    "En quelques mois, les créateurs thaïlandais et indonésiens ont généré des millions en ventes directement depuis leurs vidéos. C'était une révolution pour ces marchés — plus besoin de site e-commerce complexe, plus besoin de publicité coûteuse. Juste du contenu, et des ventes instantanées.":
        "En pocos meses, los creadores tailandeses e indonesios generaron millones en ventas directamente desde sus vídeos. Para esos mercados lo cambió todo: se acabaron las tiendas online complicadas y la publicidad cara. Solo contenido, y ventas al instante.",
    "💡 Insight :": "💡 La clave:",
    "Les premiers testeurs asiatiques ont rapidement compris que le secret n'était pas le produit, mais le contenu. Un créateur avec une audience fidèle et du contenu authentique pouvait vendre presque n'importe quoi.":
        "Los primeros en probarlo en Asia entendieron rápido que el secreto no era el producto, sino el contenido. Un creador con público fiel y contenido honesto podía vender casi cualquier cosa.",
    "🇨🇳 {0}-{1} : La domination chinoise": "🇨🇳 {0}-{1}: China toma la delantera",
    "Douyin (la version chinoise de TikTok) intègre déjà le live shopping depuis des années. ByteDance étend ces capacités à TikTok Shop sur le marché chinois. Les chiffres deviennent fous :":
        "Douyin (la versión china de TikTok) llevaba años con el live shopping. ByteDance llevó esas capacidades a TikTok Shop en el mercado chino. Las cifras se dispararon:",
    "Des centaines de milliards en GMV (Gross Merchandise Value) annuels":
        "Cientos de miles de millones de GMV (valor bruto de mercancía) al año",
    "Des millions de créateurs générant des revenus six ou sept chiffres":
        "Millones de creadores con ingresos de seis o siete cifras",
    "La naissance de la catégorie \"live shopping\" comme format dominant":
        "El nacimiento del live shopping como formato dominante",
    "La Chine devient le laboratoire d'innovation de TikTok Shop, établissant les patterns que le reste du monde suivrait.":
        "China se convirtió en el laboratorio de TikTok Shop y fijó los patrones que seguiría el resto del mundo.",
    "🇺🇸 {0} : L'arrivée chaotique aux USA": "🇺🇸 {0}: una llegada accidentada a EE. UU.",
    "TikTok Shop arrive finalement aux États-Unis en {0}, mais avec des obstacles politiques et réglementaires. Malgré les défis législatifs, la plateforme gagne rapidement du terrain aux USA, principalement parmi la Génération Z et les créateurs de niche.":
        "TikTok Shop llegó por fin a Estados Unidos en {0}, pero con obstáculos políticos y regulatorios. Pese a las batallas legislativas, la plataforma ganó terreno rápido, sobre todo entre la Generación Z y los creadores de nicho.",
    "Les créateurs américains découvrent rapidement que la formule fonctionne : contenu authentique + audience engagée = ventes directes. Des créateurs de mode, beauté, fitness et bien-être dominent les premiers mois.":
        "Los creadores estadounidenses vieron rápido que la fórmula funcionaba: contenido honesto + público implicado = ventas directas. Moda, belleza, fitness y bienestar dominaron los primeros meses.",
    "🇫🇷 Fin {0} - Aujourd'hui : L'explosion française": "🇫🇷 Finales de {0} hasta hoy: el despegue francés",
    "TikTok Shop arrive en France fin {0} et le marché explose. En {1}, la France est l'un des plus grands marchés TikTok Shop en Europe. Voici pourquoi :":
        "TikTok Shop llegó a Francia a finales de {0} y el mercado se disparó. En {1}, Francia es uno de los mayores mercados de TikTok Shop en Europa. Por esto:",
    "Audience jeune :": "Público joven:",
    "TikTok a une base d'utilisateurs énorme en France ({0}+ millions)":
        "TikTok tiene una base de usuarios enorme en Francia (más de {0} millones)",
    "Culture créative :": "Cultura creativa:",
    "Les Français embrassent les créateurs et les influenceurs": "El público francés acoge a creadores e influencers",
    "Marché de niche :": "Sitio para nichos:",
    "Les petites marques et créateurs trouvent un canal direct sans coûts publicitaires énormes":
        "Las marcas pequeñas y los creadores encuentran un canal directo sin grandes costes publicitarios",
    "Beauté et Mode :": "Belleza y moda:",
    "Deux catégories où la France excelle": "Dos categorías donde Francia destaca",
    "💰 L'impact économique": "💰 El impacto económico",
    "En {0}, TikTok Shop représente une part significative du e-commerce en France. Des chiffres estimés :":
        "En {0}, TikTok Shop supone una parte considerable del comercio electrónico francés. Cifras estimadas:",
    "Plus de {0} créateurs vendant activement sur TikTok Shop en France":
        "Más de {0} creadores vendiendo activamente en TikTok Shop en Francia",
    "Des transactions quotidiennes dans les milliards d'euros": "Transacciones diarias de miles de millones de euros",
    "Plus de {0} PME françaises intégrées à la plateforme": "Más de {0} pymes francesas integradas en la plataforma",
    "🔮 Qu'est-ce qui a changé ?": "🔮 Qué cambió de verdad",
    "TikTok Shop n'a pas inventé le shopping social, mais c'est la plateforme qui l'a démocratisé. Avant, il fallait :":
        "TikTok Shop no inventó las compras sociales, pero es la plataforma que las abrió a todo el mundo. Antes hacía falta:",
    "Un site e-commerce": "Una tienda online",
    "Un budget marketing": "Un presupuesto de marketing",
    "Une expertise technique": "Conocimientos técnicos",
    "Des infrastructures logistiques": "Una logística detrás",
    "Avec TikTok Shop, il te faut juste :": "Con TikTok Shop solo necesitas:",
    "Un téléphone": "Un teléfono",
    "Du contenu authentique": "Contenido honesto",
    "Une audience engagée": "Un público implicado",
    "🚀 Les leçons clés": "🚀 Las lecciones que cuentan",
    "{0}. Le contenu est roi": "{0}. El contenido manda",
    "Les meilleurs vendeurs sur TikTok Shop ne sont pas nécessairement les meilleurs marketers. Ce sont les créateurs qui font du contenu authentique et divertissant. Le produit vient en second.":
        "Los que más venden en TikTok Shop no son necesariamente los mejores en marketing. Son los creadores que hacen contenido honesto y entretenido. El producto va después.",
    "la promotion": "la promoción",
    "Vous ne pouvez pas \"acheter\" une audience sur TikTok Shop. Vous devez la construire. Les créateurs avec une vraie communauté vendent {0}x plus que ceux avec simplement des followers.":
        "En TikTok Shop no se puede «comprar» público. Hay que construirlo. Los creadores con comunidad real venden {0} veces más que los que solo tienen seguidores.",
    "{0}. La niche c'est l'argent": "{0}. El dinero está en el nicho",
    "Les plus grands vendeurs se concentrent sur une niche spécifique et deviennent incontournables dans cette niche. Pas de généralistes, seulement des spécialistes.":
        "Los que más venden se centran en un nicho concreto y se vuelven imprescindibles dentro de él. Nada de generalistas, solo especialistas.",
    "📊 Les chiffres aujourd'hui (mai {0})": "📊 Dónde están las cifras (mayo de {0})",
    "TikTok Shop France : ~{0} milliards € annuels estimés": "TikTok Shop Francia: unos {0} mil millones de euros al año estimados",
    "Créateurs gagnant {0} chiffres+ : ~{1}": "Creadores con {0} cifras o más: ~{1}",
    "Catégories dominantes : Mode, Beauté, Bien-être, Électronique, Maison":
        "Categorías dominantes: moda, belleza, bienestar, electrónica, hogar",
    "Âge moyen des vendeurs : {0}-{1} ans": "Edad media de los vendedores: {0}-{1} años",
    "🎯 Conclusion : Ce n'est que le début": "🎯 Para terminar: esto acaba de empezar",
    "TikTok Shop ne va que croître. Les prédictions pour {0}-{1} ? Des intégrations plus profondes, plus de tools d'analyse (comme Qeerah 😉), et potentiellement le plus grand changement : les agences et les marques établies qui vont entièrement réviser leur stratégie autour de TikTok Shop.":
        "TikTok Shop solo va a crecer. ¿Previsiones para {0}-{1}? Integraciones más profundas, más herramientas de análisis (como Qeerah 😉) y, quizá el mayor cambio de todos: agencias y marcas consolidadas rehaciendo toda su estrategia en torno a TikTok Shop.",
    "L'histoire de TikTok Shop n'est qu'au chapitre {0}. Nous sommes au moment clé où les créateurs peut devenir millionnaire, où les agences peuvent scaler leurs clients, et où les marques peuvent atteindre leur audience de manière directe et authentique.":
        "La historia de TikTok Shop va apenas por el capítulo {0}. Estamos en el momento en que los creadores pueden hacerse ricos, las agencias pueden escalar a sus clientes y las marcas pueden llegar a su público de forma directa y honesta.",
    "Prêt à analyser vos vidéos TikTok Shop ?": "¿List@ para analizar tus vídeos de TikTok Shop?",
    "Utilisez Qeerah pour comprendre exactement ce qui fonctionne dans votre contenu.":
        "Usa Qeerah para entender exactamente qué funciona en tu contenido.",
    "Commencer gratuitement →": "Empezar gratis →",
}

T_BLOG_HISTOIRE["it"] = {
    "Histoire de TikTok Shop : De la Chine à la France - Qeerah":
        "La storia di TikTok Shop: dalla Cina alla Francia - Qeerah",
    "L'histoire complète de TikTok Shop : Du lancement à la domination mondiale. Découvrez comment TikTok Shop a révolutionné le e-commerce.":
        "La storia completa di TikTok Shop, dal lancio alla portata mondiale, e come ha rivoltato l'e-commerce.",
    "L'histoire complète de TikTok Shop : de la Chine à la domination mondiale":
        "La storia completa di TikTok Shop: dalla Cina alla portata mondiale",
    "Comment TikTok Shop est passé d'une expérience asiatique à une révolution mondiale du e-commerce, de {0} à aujourd'hui.":
        "Come TikTok Shop è passato da esperimento asiatico a rivoluzione mondiale dell'e-commerce, dal {0} a oggi.",
    "← Retour au blog": "← Torna al blog",
    "📖 HISTOIRE": "📖 STORIA",
    "L'histoire complète de TikTok Shop : De la Chine à la domination mondiale":
        "La storia completa di TikTok Shop: dalla Cina alla portata mondiale",
    "📅 Mis à jour mai {0}": "📅 Aggiornato a maggio {0}",
    "👤 Par l'équipe Qeerah": "👤 Dal team Qeerah",
    "⏱️ {0} min": "⏱️ {0} min",
    "🌍 Prologue : L'ère du e-commerce social": "🌍 Prologo: l'era del social commerce",
    "Le e-commerce a longtemps été dominé par les marketplaces traditionnelles : Amazon, eBay, Alibaba. Mais depuis quelques années, une révolution s'opère. Le shopping social — la fusion du divertissement et du commerce — est devenu la norme. TikTok Shop en est la manifestation la plus claire et la plus puissante.":
        "Per anni l'e-commerce è stato dei marketplace classici: Amazon, eBay, Alibaba. Ma da qualche anno qualcosa si è spostato. Lo shopping sociale — intrattenimento e commercio fusi insieme — è diventato la norma. TikTok Shop ne è la forma più chiara e più potente.",
    "📱 {0} : Les débuts en Asie du Sud-Est": "📱 {0}: gli inizi nel Sud-est asiatico",
    "ByteDance, la société mère de TikTok, lance": "ByteDance, la società madre di TikTok, lancia",
    "en {0} en Thaïlande et en Indonésie. L'objectif était simple : transformer la plateforme de divertissement en machine de vente e-commerce. Les résultats ont été spectaculaires.":
        "nel {0} in Thailandia e Indonesia. L'obiettivo era semplice: trasformare una piattaforma di intrattenimento in una macchina da vendita. I risultati sono stati clamorosi.",
    "En quelques mois, les créateurs thaïlandais et indonésiens ont généré des millions en ventes directement depuis leurs vidéos. C'était une révolution pour ces marchés — plus besoin de site e-commerce complexe, plus besoin de publicité coûteuse. Juste du contenu, et des ventes instantanées.":
        "In pochi mesi i creator thailandesi e indonesiani hanno generato milioni di vendite direttamente dai loro video. Per quei mercati è cambiato tutto: niente più negozio online complicato, niente pubblicità costosa. Solo contenuti, e vendite immediate.",
    "💡 Insight :": "💡 L'intuizione:",
    "Les premiers testeurs asiatiques ont rapidement compris que le secret n'était pas le produit, mais le contenu. Un créateur avec une audience fidèle et du contenu authentique pouvait vendre presque n'importe quoi.":
        "I primi a provarlo in Asia hanno capito in fretta che il segreto non era il prodotto ma il contenuto. Un creator con un pubblico fedele e contenuti sinceri poteva vendere quasi qualsiasi cosa.",
    "🇨🇳 {0}-{1} : La domination chinoise": "🇨🇳 {0}-{1}: la Cina prende il comando",
    "Douyin (la version chinoise de TikTok) intègre déjà le live shopping depuis des années. ByteDance étend ces capacités à TikTok Shop sur le marché chinois. Les chiffres deviennent fous :":
        "Douyin (la versione cinese di TikTok) faceva live shopping già da anni. ByteDance ha portato quelle funzioni su TikTok Shop nel mercato cinese. I numeri sono impazziti:",
    "Des centaines de milliards en GMV (Gross Merchandise Value) annuels":
        "Centinaia di miliardi di GMV (Gross Merchandise Value) all'anno",
    "Des millions de créateurs générant des revenus six ou sept chiffres":
        "Milioni di creator con entrate a sei o sette cifre",
    "La naissance de la catégorie \"live shopping\" comme format dominant":
        "La nascita del live shopping come formato dominante",
    "La Chine devient le laboratoire d'innovation de TikTok Shop, établissant les patterns que le reste du monde suivrait.":
        "La Cina è diventata il laboratorio di TikTok Shop, fissando gli schemi che il resto del mondo avrebbe seguito.",
    "🇺🇸 {0} : L'arrivée chaotique aux USA": "🇺🇸 {0}: un arrivo accidentato negli USA",
    "TikTok Shop arrive finalement aux États-Unis en {0}, mais avec des obstacles politiques et réglementaires. Malgré les défis législatifs, la plateforme gagne rapidement du terrain aux USA, principalement parmi la Génération Z et les créateurs de niche.":
        "TikTok Shop è arrivato negli Stati Uniti nel {0}, ma con ostacoli politici e regolatori. Nonostante le battaglie legislative, la piattaforma ha guadagnato terreno in fretta, soprattutto tra la Generazione Z e i creator di nicchia.",
    "Les créateurs américains découvrent rapidement que la formule fonctionne : contenu authentique + audience engagée = ventes directes. Des créateurs de mode, beauté, fitness et bien-être dominent les premiers mois.":
        "I creator americani hanno capito subito che la formula funziona: contenuti sinceri + pubblico coinvolto = vendite dirette. Moda, bellezza, fitness e benessere hanno dominato i primi mesi.",
    "🇫🇷 Fin {0} - Aujourd'hui : L'explosion française": "🇫🇷 Fine {0} a oggi: il decollo francese",
    "TikTok Shop arrive en France fin {0} et le marché explose. En {1}, la France est l'un des plus grands marchés TikTok Shop en Europe. Voici pourquoi :":
        "TikTok Shop è arrivato in Francia a fine {0} e il mercato è esploso. Nel {1} la Francia è uno dei mercati TikTok Shop più grandi d'Europa. Ecco perché:",
    "Audience jeune :": "Pubblico giovane:",
    "TikTok a une base d'utilisateurs énorme en France ({0}+ millions)":
        "TikTok ha una base di utenti enorme in Francia (oltre {0} milioni)",
    "Culture créative :": "Cultura creativa:",
    "Les Français embrassent les créateurs et les influenceurs": "Il pubblico francese accoglie creator e influencer",
    "Marché de niche :": "Spazio per le nicchie:",
    "Les petites marques et créateurs trouvent un canal direct sans coûts publicitaires énormes":
        "Piccoli marchi e creator trovano un canale diretto senza budget pubblicitari enormi",
    "Beauté et Mode :": "Bellezza e moda:",
    "Deux catégories où la France excelle": "Due categorie in cui la Francia va forte",
    "💰 L'impact économique": "💰 L'impatto economico",
    "En {0}, TikTok Shop représente une part significative du e-commerce en France. Des chiffres estimés :":
        "Nel {0} TikTok Shop pesa in modo significativo sull'e-commerce francese. Cifre stimate:",
    "Plus de {0} créateurs vendant activement sur TikTok Shop en France":
        "Oltre {0} creator che vendono attivamente su TikTok Shop in Francia",
    "Des transactions quotidiennes dans les milliards d'euros": "Transazioni quotidiane nell'ordine dei miliardi di euro",
    "Plus de {0} PME françaises intégrées à la plateforme": "Oltre {0} piccole imprese francesi sulla piattaforma",
    "🔮 Qu'est-ce qui a changé ?": "🔮 Cosa è cambiato davvero",
    "TikTok Shop n'a pas inventé le shopping social, mais c'est la plateforme qui l'a démocratisé. Avant, il fallait :":
        "TikTok Shop non ha inventato lo shopping sociale, ma è la piattaforma che lo ha aperto a tutti. Prima servivano:",
    "Un site e-commerce": "Un negozio online",
    "Un budget marketing": "Un budget di marketing",
    "Une expertise technique": "Competenze tecniche",
    "Des infrastructures logistiques": "Una logistica alle spalle",
    "Avec TikTok Shop, il te faut juste :": "Con TikTok Shop ti serve solo:",
    "Un téléphone": "Un telefono",
    "Du contenu authentique": "Contenuti sinceri",
    "Une audience engagée": "Un pubblico coinvolto",
    "🚀 Les leçons clés": "🚀 Le lezioni che contano",
    "{0}. Le contenu est roi": "{0}. Comanda il contenuto",
    "Les meilleurs vendeurs sur TikTok Shop ne sont pas nécessairement les meilleurs marketers. Ce sont les créateurs qui font du contenu authentique et divertissant. Le produit vient en second.":
        "Chi vende di più su TikTok Shop non è per forza il migliore nel marketing. Sono i creator che fanno contenuti sinceri e divertenti. Il prodotto viene dopo.",
    "la promotion": "la promozione",
    "Vous ne pouvez pas \"acheter\" une audience sur TikTok Shop. Vous devez la construire. Les créateurs avec une vraie communauté vendent {0}x plus que ceux avec simplement des followers.":
        "Su TikTok Shop il pubblico non si compra. Va costruito. I creator con una vera community vendono {0} volte più di chi ha solo follower.",
    "{0}. La niche c'est l'argent": "{0}. I soldi stanno nella nicchia",
    "Les plus grands vendeurs se concentrent sur une niche spécifique et deviennent incontournables dans cette niche. Pas de généralistes, seulement des spécialistes.":
        "Chi vende di più si concentra su una nicchia precisa e ci diventa imprescindibile. Niente generalisti, solo specialisti.",
    "📊 Les chiffres aujourd'hui (mai {0})": "📊 Dove sono i numeri (maggio {0})",
    "TikTok Shop France : ~{0} milliards € annuels estimés": "TikTok Shop Francia: circa {0} miliardi € l'anno stimati",
    "Créateurs gagnant {0} chiffres+ : ~{1}": "Creator con {0} cifre o più: ~{1}",
    "Catégories dominantes : Mode, Beauté, Bien-être, Électronique, Maison":
        "Categorie dominanti: moda, bellezza, benessere, elettronica, casa",
    "Âge moyen des vendeurs : {0}-{1} ans": "Età media dei venditori: {0}-{1} anni",
    "🎯 Conclusion : Ce n'est que le début": "🎯 Per chiudere: è solo l'inizio",
    "TikTok Shop ne va que croître. Les prédictions pour {0}-{1} ? Des intégrations plus profondes, plus de tools d'analyse (comme Qeerah 😉), et potentiellement le plus grand changement : les agences et les marques établies qui vont entièrement réviser leur stratégie autour de TikTok Shop.":
        "TikTok Shop non farà che crescere. Previsioni per il {0}-{1}? Integrazioni più profonde, più strumenti di analisi (come Qeerah 😉) e forse il cambiamento più grosso: agenzie e marchi affermati che rifanno tutta la loro strategia attorno a TikTok Shop.",
    "L'histoire de TikTok Shop n'est qu'au chapitre {0}. Nous sommes au moment clé où les créateurs peut devenir millionnaire, où les agences peuvent scaler leurs clients, et où les marques peuvent atteindre leur audience de manière directe et authentique.":
        "La storia di TikTok Shop è appena al capitolo {0}. Siamo nel momento in cui i creator possono diventare ricchi, le agenzie possono far crescere i clienti e i marchi possono raggiungere il pubblico in modo diretto e sincero.",
    "Prêt à analyser vos vidéos TikTok Shop ?": "Pronto ad analizzare i tuoi video TikTok Shop?",
    "Utilisez Qeerah pour comprendre exactement ce qui fonctionne dans votre contenu.":
        "Usa Qeerah per capire esattamente cosa funziona nei tuoi contenuti.",
    "Commencer gratuitement →": "Inizia gratis →",
}

T_BLOG_HISTOIRE["pt-br"] = {
    "Histoire de TikTok Shop : De la Chine à la France - Qeerah":
        "A história do TikTok Shop: da China à França - Qeerah",
    "L'histoire complète de TikTok Shop : Du lancement à la domination mondiale. Découvrez comment TikTok Shop a révolutionné le e-commerce.":
        "A história completa do TikTok Shop, do lançamento ao alcance mundial, e como ele virou o e-commerce de cabeça para baixo.",
    "L'histoire complète de TikTok Shop : de la Chine à la domination mondiale":
        "A história completa do TikTok Shop: da China ao alcance mundial",
    "Comment TikTok Shop est passé d'une expérience asiatique à une révolution mondiale du e-commerce, de {0} à aujourd'hui.":
        "Como o TikTok Shop passou de experimento asiático a uma virada mundial no e-commerce, de {0} até hoje.",
    "← Retour au blog": "← Voltar ao blog",
    "📖 HISTOIRE": "📖 HISTÓRIA",
    "L'histoire complète de TikTok Shop : De la Chine à la domination mondiale":
        "A história completa do TikTok Shop: da China ao alcance mundial",
    "📅 Mis à jour mai {0}": "📅 Atualizado em maio de {0}",
    "👤 Par l'équipe Qeerah": "👤 Pelo time da Qeerah",
    "⏱️ {0} min": "⏱️ {0} min",
    "🌍 Prologue : L'ère du e-commerce social": "🌍 Prólogo: a era do comércio social",
    "Le e-commerce a longtemps été dominé par les marketplaces traditionnelles : Amazon, eBay, Alibaba. Mais depuis quelques années, une révolution s'opère. Le shopping social — la fusion du divertissement et du commerce — est devenu la norme. TikTok Shop en est la manifestation la plus claire et la plus puissante.":
        "Por muito tempo o e-commerce foi dos marketplaces clássicos: Amazon, eBay, Alibaba. Mas há alguns anos algo mudou. As compras sociais — entretenimento e comércio fundidos — viraram a norma. O TikTok Shop é a forma mais clara e mais forte disso.",
    "📱 {0} : Les débuts en Asie du Sud-Est": "📱 {0}: o começo no Sudeste Asiático",
    "ByteDance, la société mère de TikTok, lance": "A ByteDance, dona do TikTok, lança o",
    "en {0} en Thaïlande et en Indonésie. L'objectif était simple : transformer la plateforme de divertissement en machine de vente e-commerce. Les résultats ont été spectaculaires.":
        "em {0} na Tailândia e na Indonésia. O objetivo era simples: transformar uma plataforma de entretenimento numa máquina de vendas. Os resultados foram impressionantes.",
    "En quelques mois, les créateurs thaïlandais et indonésiens ont généré des millions en ventes directement depuis leurs vidéos. C'était une révolution pour ces marchés — plus besoin de site e-commerce complexe, plus besoin de publicité coûteuse. Juste du contenu, et des ventes instantanées.":
        "Em poucos meses, criadores tailandeses e indonésios geraram milhões em vendas direto dos vídeos. Para aqueles mercados mudou tudo: nada de loja online complicada, nada de publicidade cara. Só conteúdo, e venda na hora.",
    "💡 Insight :": "💡 A sacada:",
    "Les premiers testeurs asiatiques ont rapidement compris que le secret n'était pas le produit, mais le contenu. Un créateur avec une audience fidèle et du contenu authentique pouvait vendre presque n'importe quoi.":
        "Quem testou primeiro na Ásia entendeu rápido que o segredo não era o produto, e sim o conteúdo. Um criador com público fiel e conteúdo honesto conseguia vender quase qualquer coisa.",
    "🇨🇳 {0}-{1} : La domination chinoise": "🇨🇳 {0}-{1}: a China assume a dianteira",
    "Douyin (la version chinoise de TikTok) intègre déjà le live shopping depuis des années. ByteDance étend ces capacités à TikTok Shop sur le marché chinois. Les chiffres deviennent fous :":
        "O Douyin (a versão chinesa do TikTok) já fazia live shopping havia anos. A ByteDance levou esses recursos ao TikTok Shop no mercado chinês. Os números explodiram:",
    "Des centaines de milliards en GMV (Gross Merchandise Value) annuels":
        "Centenas de bilhões de GMV (valor bruto de mercadoria) por ano",
    "Des millions de créateurs générant des revenus six ou sept chiffres":
        "Milhões de criadores com receita de seis ou sete dígitos",
    "La naissance de la catégorie \"live shopping\" comme format dominant":
        "O nascimento do live shopping como formato dominante",
    "La Chine devient le laboratoire d'innovation de TikTok Shop, établissant les patterns que le reste du monde suivrait.":
        "A China virou o laboratório do TikTok Shop e definiu os padrões que o resto do mundo seguiria.",
    "🇺🇸 {0} : L'arrivée chaotique aux USA": "🇺🇸 {0}: uma chegada conturbada aos EUA",
    "TikTok Shop arrive finalement aux États-Unis en {0}, mais avec des obstacles politiques et réglementaires. Malgré les défis législatifs, la plateforme gagne rapidement du terrain aux USA, principalement parmi la Génération Z et les créateurs de niche.":
        "O TikTok Shop enfim chegou aos Estados Unidos em {0}, mas com obstáculos políticos e regulatórios. Apesar das brigas legislativas, a plataforma ganhou terreno rápido, principalmente na Geração Z e entre criadores de nicho.",
    "Les créateurs américains découvrent rapidement que la formule fonctionne : contenu authentique + audience engagée = ventes directes. Des créateurs de mode, beauté, fitness et bien-être dominent les premiers mois.":
        "Os criadores americanos viram rápido que a fórmula funciona: conteúdo honesto + público engajado = venda direta. Moda, beleza, fitness e bem-estar dominaram os primeiros meses.",
    "🇫🇷 Fin {0} - Aujourd'hui : L'explosion française": "🇫🇷 Fim de {0} até hoje: a explosão francesa",
    "TikTok Shop arrive en France fin {0} et le marché explose. En {1}, la France est l'un des plus grands marchés TikTok Shop en Europe. Voici pourquoi :":
        "O TikTok Shop chegou à França no fim de {0} e o mercado explodiu. Em {1}, a França é um dos maiores mercados do TikTok Shop na Europa. Veja por quê:",
    "Audience jeune :": "Público jovem:",
    "TikTok a une base d'utilisateurs énorme en France ({0}+ millions)":
        "O TikTok tem uma base de usuários enorme na França (mais de {0} milhões)",
    "Culture créative :": "Cultura criativa:",
    "Les Français embrassent les créateurs et les influenceurs": "O público francês abraça criadores e influenciadores",
    "Marché de niche :": "Espaço para nichos:",
    "Les petites marques et créateurs trouvent un canal direct sans coûts publicitaires énormes":
        "Marcas pequenas e criadores encontram um canal direto sem gastos enormes com publicidade",
    "Beauté et Mode :": "Beleza e moda:",
    "Deux catégories où la France excelle": "Duas categorias em que a França é forte",
    "💰 L'impact économique": "💰 O impacto econômico",
    "En {0}, TikTok Shop représente une part significative du e-commerce en France. Des chiffres estimés :":
        "Em {0}, o TikTok Shop já responde por uma fatia relevante do e-commerce francês. Números estimados:",
    "Plus de {0} créateurs vendant activement sur TikTok Shop en France":
        "Mais de {0} criadores vendendo ativamente no TikTok Shop na França",
    "Des transactions quotidiennes dans les milliards d'euros": "Transações diárias na casa dos bilhões de euros",
    "Plus de {0} PME françaises intégrées à la plateforme": "Mais de {0} pequenas empresas francesas na plataforma",
    "🔮 Qu'est-ce qui a changé ?": "🔮 O que mudou de verdade",
    "TikTok Shop n'a pas inventé le shopping social, mais c'est la plateforme qui l'a démocratisé. Avant, il fallait :":
        "O TikTok Shop não inventou as compras sociais, mas foi a plataforma que abriu isso para todo mundo. Antes era preciso:",
    "Un site e-commerce": "Uma loja online",
    "Un budget marketing": "Verba de marketing",
    "Une expertise technique": "Conhecimento técnico",
    "Des infrastructures logistiques": "Logística por trás",
    "Avec TikTok Shop, il te faut juste :": "Com o TikTok Shop, você só precisa de:",
    "Un téléphone": "Um celular",
    "Du contenu authentique": "Conteúdo honesto",
    "Une audience engagée": "Um público engajado",
    "🚀 Les leçons clés": "🚀 As lições que importam",
    "{0}. Le contenu est roi": "{0}. Quem manda é o conteúdo",
    "Les meilleurs vendeurs sur TikTok Shop ne sont pas nécessairement les meilleurs marketers. Ce sont les créateurs qui font du contenu authentique et divertissant. Le produit vient en second.":
        "Quem mais vende no TikTok Shop não é necessariamente quem é melhor de marketing. São os criadores que fazem conteúdo honesto e divertido. O produto vem depois.",
    "la promotion": "a divulgação",
    "Vous ne pouvez pas \"acheter\" une audience sur TikTok Shop. Vous devez la construire. Les créateurs avec une vraie communauté vendent {0}x plus que ceux avec simplement des followers.":
        "No TikTok Shop não dá para comprar público. Tem que construir. Criadores com comunidade de verdade vendem {0}× mais do que quem só tem seguidores.",
    "{0}. La niche c'est l'argent": "{0}. O dinheiro está no nicho",
    "Les plus grands vendeurs se concentrent sur une niche spécifique et deviennent incontournables dans cette niche. Pas de généralistes, seulement des spécialistes.":
        "Quem mais vende foca num nicho específico e vira referência ali dentro. Nada de generalistas, só especialistas.",
    "📊 Les chiffres aujourd'hui (mai {0})": "📊 Onde estão os números (maio de {0})",
    "TikTok Shop France : ~{0} milliards € annuels estimés": "TikTok Shop França: cerca de € {0} bilhões por ano, estimado",
    "Créateurs gagnant {0} chiffres+ : ~{1}": "Criadores com {0} dígitos ou mais: ~{1}",
    "Catégories dominantes : Mode, Beauté, Bien-être, Électronique, Maison":
        "Categorias dominantes: moda, beleza, bem-estar, eletrônicos, casa",
    "Âge moyen des vendeurs : {0}-{1} ans": "Idade média dos vendedores: {0}-{1} anos",
    "🎯 Conclusion : Ce n'est que le début": "🎯 Para fechar: isso é só o começo",
    "TikTok Shop ne va que croître. Les prédictions pour {0}-{1} ? Des intégrations plus profondes, plus de tools d'analyse (comme Qeerah 😉), et potentiellement le plus grand changement : les agences et les marques établies qui vont entièrement réviser leur stratégie autour de TikTok Shop.":
        "O TikTok Shop só vai crescer. Previsões para {0}-{1}? Integrações mais profundas, mais ferramentas de análise (como a Qeerah 😉) e, talvez a maior virada de todas: agências e marcas consolidadas refazendo toda a estratégia em torno do TikTok Shop.",
    "L'histoire de TikTok Shop n'est qu'au chapitre {0}. Nous sommes au moment clé où les créateurs peut devenir millionnaire, où les agences peuvent scaler leurs clients, et où les marques peuvent atteindre leur audience de manière directe et authentique.":
        "A história do TikTok Shop está só no capítulo {0}. Estamos no momento em que criadores podem ficar ricos, agências podem escalar seus clientes e marcas podem falar com o público de forma direta e honesta.",
    "Prêt à analyser vos vidéos TikTok Shop ?": "Pronto para analisar seus vídeos do TikTok Shop?",
    "Utilisez Qeerah pour comprendre exactement ce qui fonctionne dans votre contenu.":
        "Use a Qeerah para entender exatamente o que funciona no seu conteúdo.",
    "Commencer gratuitement →": "Começar de graça →",
}

T_BLOG_HISTOIRE["en-ie"] = dict(T_BLOG_HISTOIRE["en"])
T_BLOG_HISTOIRE["es-mx"] = dict(T_BLOG_HISTOIRE["es"])
