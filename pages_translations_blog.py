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


# ═══════════════════════════════════════════════════════════════════════════
# /blog/guide-complet
# ═══════════════════════════════════════════════════════════════════════════
T_BLOG_GUIDE: dict[str, dict[str, str]] = {}

T_BLOG_GUIDE["en"] = {
    "Guide Complet TikTok Shop {0} - Qeerah": "The complete TikTok Shop guide for {0} - Qeerah",
    "Guide complet pour structurer votre stratégie TikTok Shop de A à Z. Positionnement, contenu, optimisation, monétisation.":
        "A complete guide to building your TikTok Shop strategy from scratch: positioning, content, optimisation, earning.",
    "Guide complet : structurer sa stratégie TikTok Shop en {0}":
        "Complete guide: building your TikTok Shop strategy in {0}",
    "Un guide étape par étape pour construire une stratégie TikTok Shop de A à Z : positionnement, contenu, optimisation, monétisation.":
        "A step-by-step guide to building a TikTok Shop strategy from scratch: positioning, content, optimisation, earning.",
    "← Retour au blog": "← Back to the blog",
    "📖 GUIDE COMPLET": "📖 COMPLETE GUIDE",
    "Guide complet : Structurer sa stratégie TikTok Shop en {0}":
        "Complete guide: building your TikTok Shop strategy in {0}",
    "Vouloir réussir sur TikTok Shop sans stratégie c'est comme naviguer sans carte. Voici un guide étape par étape pour construire une stratégie solide en {0}.":
        "Trying to do well on TikTok Shop without a strategy is like sailing without a map. Here's a step-by-step guide to building a solid one in {0}.",
    "Phase {0} : Positionnement (Semaines {1}-{2})": "Phase {0}: positioning (weeks {1}-{2})",
    "Étape {0} : Trouvez votre niche": "Step {0}: find your niche",
    "Répondez à ces questions :": "Answer these questions:",
    "Que puis-je enseigner mieux que {0}% des gens ?": "What can I teach better than {0}% of people?",
    "Qui est mon client idéal ?": "Who is my ideal customer?",
    "Quel problème je résous ?": "What problem am I solving?",
    "Votre niche ne doit pas être minuscule, mais elle doit être claire. \"Mode\" c'est trop large. \"Mode éthique pour les femmes {0}-{1} urbaines\" c'est parfait.":
        "Your niche doesn't have to be tiny, but it has to be clear. “Fashion” is too broad. “Ethical fashion for city women aged {0}-{1}” is right.",
    "Étape {0} : Analysez la concurrence": "Step {0}: study the competition",
    "Trouvez {0}-{1} créateurs qui vendent dans votre niche. Regardez :":
        "Find {0}-{1} creators selling in your niche. Look at:",
    "Quels types de contenu performent": "Which kinds of content perform",
    "Quel est leur ton/personnalité": "Their tone and personality",
    "Comment ils présentent les produits": "How they present products",
    "Leurs CTA (appels à l'action)": "Their calls to action",
    "Vous n'allez pas les copier. Vous allez apprendre leurs patterns de succès.":
        "You're not going to copy them. You're going to learn the patterns behind their results.",
    "Phase {0} : Création de contenu (Semaines {1}-{2})": "Phase {0}: making content (weeks {1}-{2})",
    "Étape {0} : Créez {1} vidéos de test": "Step {0}: make {1} test videos",
    "Avant de vendre, testez. Créez {0} vidéos explorant différents angles :":
        "Before selling, test. Make {0} videos exploring different angles:",
    "{0} vidéos \"transformation/avant-après\"": "{0} “transformation / before-and-after” videos",
    "{0} vidéos \"éducation\"": "{0} “teaching” videos",
    "{0} vidéos \"divertissement pur\"": "{0} “pure entertainment” videos",
    "{0} vidéos \"preuve sociale\"": "{0} “social proof” videos",
    "{0} vidéos \"appel à l'action\"": "{0} “call to action” videos",
    "{0} vidéos \"story personnel\"": "{0} “personal story” videos",
    "Publiez rapidement ({0}-{1} par jour). Ne vous souciez pas de la perfection. Observez ce qui fonctionne.":
        "Publish fast ({0}-{1} a day). Don't worry about perfection. Watch what works.",
    "Étape {0} : Analysez vos résultats": "Step {0}: read your results",
    "Après {0} vidéos, regardez les données :": "After {0} videos, look at the data:",
    "Quels types de vidéos donnent le plus de vues ?": "Which kinds of video get the most views?",
    "Quels hooks retiennent le plus longtemps ?": "Which hooks hold attention longest?",
    "Quel ton résonne le plus ?": "Which tone lands best?",
    "Les {0} meilleures vidéos ? Observez leurs patterns communs. Vous allez répéter ces patterns.":
        "Your {0} best videos? Look at what they share. Those are the patterns you'll repeat.",
    "Phase {0} : Optimisation (Semaines {1}-{2})": "Phase {0}: optimisation (weeks {1}-{2})",
    "Étape {0} : Double-down sur ce qui fonctionne": "Step {0}: double down on what works",
    "Créez {0} variantes des vidéos qui ont le mieux performé. Changez :":
        "Make {0} variants of your best performers. Change:",
    "Les premières {0} secondes (hook différent)": "The first {0} seconds (a different hook)",
    "Le produit montré": "The product shown",
    "L'angle de caméra": "The camera angle",
    "La musique/son": "The music or sound",
    "Le ton de votre voix": "The tone of your voice",
    "Le même concept, {0} exécutions différentes. C'est ça qui crée de la croissance exponentielle.":
        "The same idea, {0} different executions. That's what compounds.",
    "Étape {0} : Introduisez progressivement vos produits": "Step {0}: bring your products in gradually",
    "Ne commencez pas à vendre immédiatement. Voici le timing optimal :":
        "Don't start selling straight away. Here's the timing that works:",
    "Semaines {0}-{1} : Zéro mention du produit. Construction d'audience.":
        "Weeks {0}-{1}: no mention of the product. Build the audience.",
    "Semaines {0}-{1} : Mention causelle. \"Voici ce que j'utilise...\"":
        "Weeks {0}-{1}: casual mentions. “This is what I use…”",
    "Semaines {0}+ : Vente directe. Maintenant votre audience vous connaît.":
        "Week {0} onwards: sell directly. By now your audience knows you.",
    "Cet ordre = conversion {0}x plus élevée que si vous vendez dès le jour {1}.":
        "This order converts {0}× better than selling from day {1}.",
    "Phase {0} : Monétisation (Semaines {1}+)": "Phase {0}: earning (week {1} onwards)",
    "Étape {0} : Mettez en place les mécaniques de vente": "Step {0}: set up the selling machinery",
    "Une fois que votre audience vous fait confiance, activez les ventes :":
        "Once your audience trusts you, switch selling on:",
    "Ajouter le produit à la TikTok Shop": "Add the product to your TikTok Shop",
    "Créer des CTA clairs (links, codes promo)": "Write clear calls to action (links, promo codes)",
    "Tester différentes stratégies de pricing": "Test different pricing approaches",
    "Analyser les conversions avec Qeerah": "Analyse the conversions with Qeerah",
    "Étape {0} : Itérez basé sur les résultats": "Step {0}: iterate on the results",
    "Publiez, analysez, ajustez. Le cycle est :": "Publish, analyse, adjust. The loop is:",
    "Vidéo publiée": "Video published",
    "Collectez les données (vues, rétention, conversions)": "Collect the data (views, retention, conversions)",
    "Identifiez le pattern gagnant": "Spot the winning pattern",
    "Créez {0} variantes du gagnant": "Make {0} variants of the winner",
    "Publiez et répétez": "Publish and repeat",
    "🎯 Les Métriques Clés à Tracker": "🎯 The numbers worth tracking",
    "Retention Rate :": "Retention rate:",
    "% de gens qui regardent jusqu'à la fin (Cible : {0}%+)": "% of people who watch to the end (target: {0}%+)",
    "Engagement Rate :": "Engagement rate:",
    "Partages + Commentaires / Vues (Cible : {0}%+)": "Shares + comments / views (target: {0}%+)",
    "Conversion Rate :": "Conversion rate:",
    "Ventes / Clics vers produit (Cible : {0}%+)": "Sales / clicks through to the product (target: {0}%+)",
    "Cost per Acquisition :": "Cost per acquisition:",
    "Marketing spend / Nouveau client (Cible :": "Marketing spend / new customer (target:",
    "⚠️ Les Erreurs Courantes à Éviter": "⚠️ Common mistakes to avoid",
    "Vendre trop tôt :": "Selling too early:",
    "Attendez d'avoir construit la confiance": "wait until you've built trust",
    "Négliger l'analyse :": "Skipping the analysis:",
    "Les chiffres ne mentent pas": "the numbers don't lie",
    "Manque de cohérence :": "Being inconsistent:",
    "perfection": "perfection",
    "Ignorer les tendances :": "Ignoring trends:",
    "TikTok change vite. Adaptez-vous": "TikTok moves fast — move with it",
    "Trop générique :": "Being too generic:",
    "tout faire": "doing everything",
    "✅ Checklist pour Démarrer": "✅ Checklist before you start",
    "☐ Niche définie clairement": "☐ Niche clearly defined",
    "☐ Compte TikTok créé avec bio alignée à la niche": "☐ TikTok account created, bio matching the niche",
    "☐ {0} idées de vidéo écrites": "☐ {0} video ideas written down",
    "☐ Caméra/téléphone prêt": "☐ Camera or phone ready",
    "☐ Produit(s) à vendre sélectionné(s)": "☐ Product(s) to sell chosen",
    "☐ TikTok Shop configurée": "☐ TikTok Shop set up",
    "☐ Système de tracking mis en place": "☐ A way to track results in place",
    "Commencez votre stratégie maintenant": "Start your strategy now",
    "Utilisez Qeerah pour optimiser chaque vidéo selon cette stratégie.":
        "Use Qeerah to tune every video against this strategy.",
    "Démarrer →": "Get started →",
}

T_BLOG_GUIDE["de"] = {
    "Guide Complet TikTok Shop {0} - Qeerah": "Der komplette TikTok-Shop-Guide für {0} - Qeerah",
    "Guide complet pour structurer votre stratégie TikTok Shop de A à Z. Positionnement, contenu, optimisation, monétisation.":
        "Ein kompletter Guide, um deine TikTok-Shop-Strategie von Grund auf zu bauen: Positionierung, Inhalte, Feinschliff, Geldverdienen.",
    "Guide complet : structurer sa stratégie TikTok Shop en {0}":
        "Kompletter Guide: deine TikTok-Shop-Strategie {0} aufbauen",
    "Un guide étape par étape pour construire une stratégie TikTok Shop de A à Z : positionnement, contenu, optimisation, monétisation.":
        "Ein Schritt-für-Schritt-Guide, um eine TikTok-Shop-Strategie von Grund auf zu bauen: Positionierung, Inhalte, Feinschliff, Geldverdienen.",
    "← Retour au blog": "← Zurück zum Blog",
    "📖 GUIDE COMPLET": "📖 KOMPLETTER GUIDE",
    "Guide complet : Structurer sa stratégie TikTok Shop en {0}": "Kompletter Guide: deine TikTok-Shop-Strategie {0} aufbauen",
    "Vouloir réussir sur TikTok Shop sans stratégie c'est comme naviguer sans carte. Voici un guide étape par étape pour construire une stratégie solide en {0}.":
        "Auf TikTok Shop ohne Strategie weiterkommen zu wollen ist wie Segeln ohne Karte. Hier ist ein Schritt-für-Schritt-Guide für eine belastbare Strategie {0}.",
    "Phase {0} : Positionnement (Semaines {1}-{2})": "Phase {0}: Positionierung (Woche {1}-{2})",
    "Étape {0} : Trouvez votre niche": "Schritt {0}: finde deine Nische",
    "Répondez à ces questions :": "Beantworte diese Fragen:",
    "Que puis-je enseigner mieux que {0}% des gens ?": "Was kann ich besser erklären als {0} % der Leute?",
    "Qui est mon client idéal ?": "Wer ist mein idealer Kunde?",
    "Quel problème je résous ?": "Welches Problem löse ich?",
    "Votre niche ne doit pas être minuscule, mais elle doit être claire. \"Mode\" c'est trop large. \"Mode éthique pour les femmes {0}-{1} urbaines\" c'est parfait.":
        "Deine Nische muss nicht winzig sein, aber klar. „Mode“ ist zu breit. „Faire Mode für Frauen zwischen {0} und {1} in der Stadt“ passt.",
    "Étape {0} : Analysez la concurrence": "Schritt {0}: schau dir die Konkurrenz an",
    "Trouvez {0}-{1} créateurs qui vendent dans votre niche. Regardez :":
        "Such dir {0}-{1} Creators, die in deiner Nische verkaufen. Achte auf:",
    "Quels types de contenu performent": "Welche Arten von Inhalten laufen",
    "Quel est leur ton/personnalité": "Ihren Ton und ihre Persönlichkeit",
    "Comment ils présentent les produits": "Wie sie Produkte zeigen",
    "Leurs CTA (appels à l'action)": "Ihre Calls to Action",
    "Vous n'allez pas les copier. Vous allez apprendre leurs patterns de succès.":
        "Du kopierst sie nicht. Du lernst die Muster hinter ihren Ergebnissen.",
    "Phase {0} : Création de contenu (Semaines {1}-{2})": "Phase {0}: Inhalte machen (Woche {1}-{2})",
    "Étape {0} : Créez {1} vidéos de test": "Schritt {0}: mach {1} Testvideos",
    "Avant de vendre, testez. Créez {0} vidéos explorant différents angles :":
        "Bevor du verkaufst, teste. Mach {0} Videos mit verschiedenen Blickwinkeln:",
    "{0} vidéos \"transformation/avant-après\"": "{0} Videos „Verwandlung / Vorher-Nachher“",
    "{0} vidéos \"éducation\"": "{0} Videos „erklären“",
    "{0} vidéos \"divertissement pur\"": "{0} Videos „reine Unterhaltung“",
    "{0} vidéos \"preuve sociale\"": "{0} Videos „sozialer Beweis“",
    "{0} vidéos \"appel à l'action\"": "{0} Videos „Call to Action“",
    "{0} vidéos \"story personnel\"": "{0} Videos „persönliche Geschichte“",
    "Publiez rapidement ({0}-{1} par jour). Ne vous souciez pas de la perfection. Observez ce qui fonctionne.":
        "Veröffentliche schnell ({0}-{1} am Tag). Kümmer dich nicht um Perfektion. Schau, was funktioniert.",
    "Étape {0} : Analysez vos résultats": "Schritt {0}: lies deine Ergebnisse",
    "Après {0} vidéos, regardez les données :": "Nach {0} Videos schau in die Daten:",
    "Quels types de vidéos donnent le plus de vues ?": "Welche Videoarten bringen die meisten Aufrufe?",
    "Quels hooks retiennent le plus longtemps ?": "Welche Hooks halten am längsten?",
    "Quel ton résonne le plus ?": "Welcher Ton kommt am besten an?",
    "Les {0} meilleures vidéos ? Observez leurs patterns communs. Vous allez répéter ces patterns.":
        "Deine {0} besten Videos? Schau, was sie gemeinsam haben. Genau diese Muster wiederholst du.",
    "Phase {0} : Optimisation (Semaines {1}-{2})": "Phase {0}: Feinschliff (Woche {1}-{2})",
    "Étape {0} : Double-down sur ce qui fonctionne": "Schritt {0}: leg bei dem nach, was läuft",
    "Créez {0} variantes des vidéos qui ont le mieux performé. Changez :":
        "Mach {0} Varianten deiner besten Videos. Ändere:",
    "Les premières {0} secondes (hook différent)": "Die ersten {0} Sekunden (anderer Hook)",
    "Le produit montré": "Das gezeigte Produkt",
    "L'angle de caméra": "Den Kamerawinkel",
    "La musique/son": "Die Musik oder den Ton",
    "Le ton de votre voix": "Den Klang deiner Stimme",
    "Le même concept, {0} exécutions différentes. C'est ça qui crée de la croissance exponentielle.":
        "Dieselbe Idee, {0} verschiedene Umsetzungen. Genau das summiert sich.",
    "Étape {0} : Introduisez progressivement vos produits": "Schritt {0}: bring deine Produkte langsam ins Spiel",
    "Ne commencez pas à vendre immédiatement. Voici le timing optimal :":
        "Fang nicht sofort mit dem Verkaufen an. Dieses Timing funktioniert:",
    "Semaines {0}-{1} : Zéro mention du produit. Construction d'audience.":
        "Woche {0}-{1}: kein Wort über das Produkt. Publikum aufbauen.",
    "Semaines {0}-{1} : Mention causelle. \"Voici ce que j'utilise...\"":
        "Woche {0}-{1}: beiläufige Erwähnungen. „Das benutze ich …“",
    "Semaines {0}+ : Vente directe. Maintenant votre audience vous connaît.":
        "Ab Woche {0}: direkt verkaufen. Jetzt kennt dich dein Publikum.",
    "Cet ordre = conversion {0}x plus élevée que si vous vendez dès le jour {1}.":
        "Diese Reihenfolge konvertiert {0}× besser, als wenn du ab Tag {1} verkaufst.",
    "Phase {0} : Monétisation (Semaines {1}+)": "Phase {0}: Geld verdienen (ab Woche {1})",
    "Étape {0} : Mettez en place les mécaniques de vente": "Schritt {0}: bau die Verkaufsmechanik auf",
    "Une fois que votre audience vous fait confiance, activez les ventes :":
        "Sobald dein Publikum dir vertraut, schalte den Verkauf frei:",
    "Ajouter le produit à la TikTok Shop": "Das Produkt in deinen TikTok Shop stellen",
    "Créer des CTA clairs (links, codes promo)": "Klare Calls to Action schreiben (Links, Gutscheincodes)",
    "Tester différentes stratégies de pricing": "Verschiedene Preisansätze testen",
    "Analyser les conversions avec Qeerah": "Die Konversionen mit Qeerah auswerten",
    "Étape {0} : Itérez basé sur les résultats": "Schritt {0}: nachsteuern anhand der Ergebnisse",
    "Publiez, analysez, ajustez. Le cycle est :": "Veröffentlichen, auswerten, anpassen. Der Kreislauf:",
    "Vidéo publiée": "Video veröffentlicht",
    "Collectez les données (vues, rétention, conversions)": "Daten sammeln (Aufrufe, Haltequote, Konversionen)",
    "Identifiez le pattern gagnant": "Das erfolgreiche Muster erkennen",
    "Créez {0} variantes du gagnant": "{0} Varianten des Gewinners bauen",
    "Publiez et répétez": "Veröffentlichen und wiederholen",
    "🎯 Les Métriques Clés à Tracker": "🎯 Die Zahlen, die es zu verfolgen lohnt",
    "Retention Rate :": "Haltequote:",
    "% de gens qui regardent jusqu'à la fin (Cible : {0}%+)": "% der Leute, die bis zum Ende schauen (Ziel: {0} %+)",
    "Engagement Rate :": "Interaktionsrate:",
    "Partages + Commentaires / Vues (Cible : {0}%+)": "Shares + Kommentare / Aufrufe (Ziel: {0} %+)",
    "Conversion Rate :": "Konversionsrate:",
    "Ventes / Clics vers produit (Cible : {0}%+)": "Verkäufe / Klicks zum Produkt (Ziel: {0} %+)",
    "Cost per Acquisition :": "Kosten pro Neukunde:",
    "Marketing spend / Nouveau client (Cible :": "Marketingausgaben / neuer Kunde (Ziel:",
    "⚠️ Les Erreurs Courantes à Éviter": "⚠️ Häufige Fehler, die du vermeidest",
    "Vendre trop tôt :": "Zu früh verkaufen:",
    "Attendez d'avoir construit la confiance": "warte, bis Vertrauen da ist",
    "Négliger l'analyse :": "Die Auswertung überspringen:",
    "Les chiffres ne mentent pas": "Zahlen lügen nicht",
    "Manque de cohérence :": "Unbeständig sein:",
    "perfection": "Perfektion",
    "Ignorer les tendances :": "Trends ignorieren:",
    "TikTok change vite. Adaptez-vous": "TikTok dreht sich schnell — dreh dich mit",
    "Trop générique :": "Zu allgemein sein:",
    "tout faire": "alles machen",
    "✅ Checklist pour Démarrer": "✅ Checkliste vor dem Start",
    "☐ Niche définie clairement": "☐ Nische klar definiert",
    "☐ Compte TikTok créé avec bio alignée à la niche": "☐ TikTok-Konto erstellt, Bio passend zur Nische",
    "☐ {0} idées de vidéo écrites": "☐ {0} Videoideen aufgeschrieben",
    "☐ Caméra/téléphone prêt": "☐ Kamera oder Handy bereit",
    "☐ Produit(s) à vendre sélectionné(s)": "☐ Produkt(e) zum Verkaufen ausgewählt",
    "☐ TikTok Shop configurée": "☐ TikTok Shop eingerichtet",
    "☐ Système de tracking mis en place": "☐ Eine Art, Ergebnisse zu verfolgen, steht",
    "Commencez votre stratégie maintenant": "Fang jetzt mit deiner Strategie an",
    "Utilisez Qeerah pour optimiser chaque vidéo selon cette stratégie.":
        "Nutz Qeerah, um jedes Video an dieser Strategie auszurichten.",
    "Démarrer →": "Loslegen →",
}

T_BLOG_GUIDE["es"] = {
    "Guide Complet TikTok Shop {0} - Qeerah": "Guía completa de TikTok Shop {0} - Qeerah",
    "Guide complet pour structurer votre stratégie TikTok Shop de A à Z. Positionnement, contenu, optimisation, monétisation.":
        "Guía completa para montar tu estrategia de TikTok Shop desde cero: posicionamiento, contenido, optimización, monetización.",
    "Guide complet : structurer sa stratégie TikTok Shop en {0}": "Guía completa: montar tu estrategia de TikTok Shop en {0}",
    "Un guide étape par étape pour construire une stratégie TikTok Shop de A à Z : positionnement, contenu, optimisation, monétisation.":
        "Una guía paso a paso para construir una estrategia de TikTok Shop desde cero: posicionamiento, contenido, optimización, monetización.",
    "← Retour au blog": "← Volver al blog",
    "📖 GUIDE COMPLET": "📖 GUÍA COMPLETA",
    "Guide complet : Structurer sa stratégie TikTok Shop en {0}": "Guía completa: montar tu estrategia de TikTok Shop en {0}",
    "Vouloir réussir sur TikTok Shop sans stratégie c'est comme naviguer sans carte. Voici un guide étape par étape pour construire une stratégie solide en {0}.":
        "Querer funcionar en TikTok Shop sin estrategia es como navegar sin mapa. Aquí tienes una guía paso a paso para construir una sólida en {0}.",
    "Phase {0} : Positionnement (Semaines {1}-{2})": "Fase {0}: posicionamiento (semanas {1}-{2})",
    "Étape {0} : Trouvez votre niche": "Paso {0}: encuentra tu nicho",
    "Répondez à ces questions :": "Responde a estas preguntas:",
    "Que puis-je enseigner mieux que {0}% des gens ?": "¿Qué puedo enseñar mejor que el {0} % de la gente?",
    "Qui est mon client idéal ?": "¿Quién es mi cliente ideal?",
    "Quel problème je résous ?": "¿Qué problema resuelvo?",
    "Votre niche ne doit pas être minuscule, mais elle doit être claire. \"Mode\" c'est trop large. \"Mode éthique pour les femmes {0}-{1} urbaines\" c'est parfait.":
        "Tu nicho no tiene que ser minúsculo, pero sí claro. «Moda» es demasiado amplio. «Moda ética para mujeres de ciudad de {0} a {1}» está bien.",
    "Étape {0} : Analysez la concurrence": "Paso {0}: analiza la competencia",
    "Trouvez {0}-{1} créateurs qui vendent dans votre niche. Regardez :":
        "Busca {0}-{1} creadores que vendan en tu nicho. Fíjate en:",
    "Quels types de contenu performent": "Qué tipos de contenido funcionan",
    "Quel est leur ton/personnalité": "Su tono y su personalidad",
    "Comment ils présentent les produits": "Cómo presentan los productos",
    "Leurs CTA (appels à l'action)": "Sus llamadas a la acción",
    "Vous n'allez pas les copier. Vous allez apprendre leurs patterns de succès.":
        "No vas a copiarlos. Vas a aprender los patrones que hay detrás de sus resultados.",
    "Phase {0} : Création de contenu (Semaines {1}-{2})": "Fase {0}: creación de contenido (semanas {1}-{2})",
    "Étape {0} : Créez {1} vidéos de test": "Paso {0}: haz {1} vídeos de prueba",
    "Avant de vendre, testez. Créez {0} vidéos explorant différents angles :":
        "Antes de vender, prueba. Haz {0} vídeos explorando ángulos distintos:",
    "{0} vidéos \"transformation/avant-après\"": "{0} vídeos de «transformación / antes y después»",
    "{0} vidéos \"éducation\"": "{0} vídeos «para enseñar»",
    "{0} vidéos \"divertissement pur\"": "{0} vídeos «puro entretenimiento»",
    "{0} vidéos \"preuve sociale\"": "{0} vídeos de «prueba social»",
    "{0} vidéos \"appel à l'action\"": "{0} vídeos de «llamada a la acción»",
    "{0} vidéos \"story personnel\"": "{0} vídeos de «historia personal»",
    "Publiez rapidement ({0}-{1} par jour). Ne vous souciez pas de la perfection. Observez ce qui fonctionne.":
        "Publica rápido ({0}-{1} al día). No te preocupes por la perfección. Mira qué funciona.",
    "Étape {0} : Analysez vos résultats": "Paso {0}: lee tus resultados",
    "Après {0} vidéos, regardez les données :": "Después de {0} vídeos, mira los datos:",
    "Quels types de vidéos donnent le plus de vues ?": "¿Qué tipo de vídeo consigue más visualizaciones?",
    "Quels hooks retiennent le plus longtemps ?": "¿Qué ganchos retienen más tiempo?",
    "Quel ton résonne le plus ?": "¿Qué tono conecta mejor?",
    "Les {0} meilleures vidéos ? Observez leurs patterns communs. Vous allez répéter ces patterns.":
        "¿Tus {0} mejores vídeos? Mira qué tienen en común. Esos son los patrones que vas a repetir.",
    "Phase {0} : Optimisation (Semaines {1}-{2})": "Fase {0}: optimización (semanas {1}-{2})",
    "Étape {0} : Double-down sur ce qui fonctionne": "Paso {0}: redobla lo que funciona",
    "Créez {0} variantes des vidéos qui ont le mieux performé. Changez :":
        "Haz {0} variantes de los vídeos que mejor han ido. Cambia:",
    "Les premières {0} secondes (hook différent)": "Los primeros {0} segundos (otro gancho)",
    "Le produit montré": "El producto que enseñas",
    "L'angle de caméra": "El ángulo de cámara",
    "La musique/son": "La música o el sonido",
    "Le ton de votre voix": "El tono de tu voz",
    "Le même concept, {0} exécutions différentes. C'est ça qui crée de la croissance exponentielle.":
        "La misma idea, {0} ejecuciones distintas. Eso es lo que se acumula.",
    "Étape {0} : Introduisez progressivement vos produits": "Paso {0}: mete tus productos poco a poco",
    "Ne commencez pas à vendre immédiatement. Voici le timing optimal :":
        "No empieces a vender de inmediato. Este es el ritmo que funciona:",
    "Semaines {0}-{1} : Zéro mention du produit. Construction d'audience.":
        "Semanas {0}-{1}: ni una mención del producto. Construir público.",
    "Semaines {0}-{1} : Mention causelle. \"Voici ce que j'utilise...\"":
        "Semanas {0}-{1}: menciones casuales. «Esto es lo que uso yo…»",
    "Semaines {0}+ : Vente directe. Maintenant votre audience vous connaît.":
        "A partir de la semana {0}: venta directa. Ya te conocen.",
    "Cet ordre = conversion {0}x plus élevée que si vous vendez dès le jour {1}.":
        "Este orden convierte {0} veces mejor que vender desde el día {1}.",
    "Phase {0} : Monétisation (Semaines {1}+)": "Fase {0}: monetización (desde la semana {1})",
    "Étape {0} : Mettez en place les mécaniques de vente": "Paso {0}: monta la maquinaria de venta",
    "Une fois que votre audience vous fait confiance, activez les ventes :":
        "Cuando tu público confíe en ti, activa las ventas:",
    "Ajouter le produit à la TikTok Shop": "Añadir el producto a tu TikTok Shop",
    "Créer des CTA clairs (links, codes promo)": "Escribir llamadas a la acción claras (enlaces, códigos)",
    "Tester différentes stratégies de pricing": "Probar distintas estrategias de precio",
    "Analyser les conversions avec Qeerah": "Analizar las conversiones con Qeerah",
    "Étape {0} : Itérez basé sur les résultats": "Paso {0}: itera según los resultados",
    "Publiez, analysez, ajustez. Le cycle est :": "Publica, analiza, ajusta. El ciclo es:",
    "Vidéo publiée": "Vídeo publicado",
    "Collectez les données (vues, rétention, conversions)": "Recoge los datos (visualizaciones, retención, conversiones)",
    "Identifiez le pattern gagnant": "Identifica el patrón ganador",
    "Créez {0} variantes du gagnant": "Crea {0} variantes del ganador",
    "Publiez et répétez": "Publica y repite",
    "🎯 Les Métriques Clés à Tracker": "🎯 Las métricas que vale la pena seguir",
    "Retention Rate :": "Tasa de retención:",
    "% de gens qui regardent jusqu'à la fin (Cible : {0}%+)": "% de gente que ve hasta el final (objetivo: {0} %+)",
    "Engagement Rate :": "Tasa de interacción:",
    "Partages + Commentaires / Vues (Cible : {0}%+)": "Compartidos + comentarios / visualizaciones (objetivo: {0} %+)",
    "Conversion Rate :": "Tasa de conversión:",
    "Ventes / Clics vers produit (Cible : {0}%+)": "Ventas / clics al producto (objetivo: {0} %+)",
    "Cost per Acquisition :": "Coste por cliente nuevo:",
    "Marketing spend / Nouveau client (Cible :": "Gasto en marketing / cliente nuevo (objetivo:",
    "⚠️ Les Erreurs Courantes à Éviter": "⚠️ Errores frecuentes que evitar",
    "Vendre trop tôt :": "Vender demasiado pronto:",
    "Attendez d'avoir construit la confiance": "espera a haber construido confianza",
    "Négliger l'analyse :": "Saltarte el análisis:",
    "Les chiffres ne mentent pas": "los números no mienten",
    "Manque de cohérence :": "Falta de constancia:",
    "perfection": "perfección",
    "Ignorer les tendances :": "Ignorar las tendencias:",
    "TikTok change vite. Adaptez-vous": "TikTok cambia rápido: adáptate",
    "Trop générique :": "Ser demasiado genérico:",
    "tout faire": "hacerlo todo",
    "✅ Checklist pour Démarrer": "✅ Lista para empezar",
    "☐ Niche définie clairement": "☐ Nicho definido con claridad",
    "☐ Compte TikTok créé avec bio alignée à la niche": "☐ Cuenta de TikTok creada, con bio acorde al nicho",
    "☐ {0} idées de vidéo écrites": "☐ {0} ideas de vídeo escritas",
    "☐ Caméra/téléphone prêt": "☐ Cámara o móvil listo",
    "☐ Produit(s) à vendre sélectionné(s)": "☐ Producto(s) para vender elegido(s)",
    "☐ TikTok Shop configurée": "☐ TikTok Shop configurada",
    "☐ Système de tracking mis en place": "☐ Un sistema para medir resultados montado",
    "Commencez votre stratégie maintenant": "Empieza tu estrategia ahora",
    "Utilisez Qeerah pour optimiser chaque vidéo selon cette stratégie.":
        "Usa Qeerah para ajustar cada vídeo a esta estrategia.",
    "Démarrer →": "Empezar →",
}

T_BLOG_GUIDE["it"] = {
    "Guide Complet TikTok Shop {0} - Qeerah": "Guida completa a TikTok Shop {0} - Qeerah",
    "Guide complet pour structurer votre stratégie TikTok Shop de A à Z. Positionnement, contenu, optimisation, monétisation.":
        "Guida completa per costruire la tua strategia TikTok Shop da zero: posizionamento, contenuti, ottimizzazione, monetizzazione.",
    "Guide complet : structurer sa stratégie TikTok Shop en {0}": "Guida completa: costruire la tua strategia TikTok Shop nel {0}",
    "Un guide étape par étape pour construire une stratégie TikTok Shop de A à Z : positionnement, contenu, optimisation, monétisation.":
        "Una guida passo passo per costruire una strategia TikTok Shop da zero: posizionamento, contenuti, ottimizzazione, monetizzazione.",
    "← Retour au blog": "← Torna al blog",
    "📖 GUIDE COMPLET": "📖 GUIDA COMPLETA",
    "Guide complet : Structurer sa stratégie TikTok Shop en {0}": "Guida completa: costruire la tua strategia TikTok Shop nel {0}",
    "Vouloir réussir sur TikTok Shop sans stratégie c'est comme naviguer sans carte. Voici un guide étape par étape pour construire une stratégie solide en {0}.":
        "Voler andare bene su TikTok Shop senza una strategia è come navigare senza mappa. Ecco una guida passo passo per costruirne una solida nel {0}.",
    "Phase {0} : Positionnement (Semaines {1}-{2})": "Fase {0}: posizionamento (settimane {1}-{2})",
    "Étape {0} : Trouvez votre niche": "Passo {0}: trova la tua nicchia",
    "Répondez à ces questions :": "Rispondi a queste domande:",
    "Que puis-je enseigner mieux que {0}% des gens ?": "Cosa so spiegare meglio del {0} % delle persone?",
    "Qui est mon client idéal ?": "Chi è il mio cliente ideale?",
    "Quel problème je résous ?": "Quale problema risolvo?",
    "Votre niche ne doit pas être minuscule, mais elle doit être claire. \"Mode\" c'est trop large. \"Mode éthique pour les femmes {0}-{1} urbaines\" c'est parfait.":
        "La tua nicchia non deve essere minuscola, ma chiara. «Moda» è troppo ampio. «Moda etica per donne di città tra i {0} e i {1} anni» va bene.",
    "Étape {0} : Analysez la concurrence": "Passo {0}: studia la concorrenza",
    "Trouvez {0}-{1} créateurs qui vendent dans votre niche. Regardez :":
        "Trova {0}-{1} creator che vendono nella tua nicchia. Guarda:",
    "Quels types de contenu performent": "Quali tipi di contenuto funzionano",
    "Quel est leur ton/personnalité": "Il loro tono e la loro personalità",
    "Comment ils présentent les produits": "Come presentano i prodotti",
    "Leurs CTA (appels à l'action)": "Le loro call to action",
    "Vous n'allez pas les copier. Vous allez apprendre leurs patterns de succès.":
        "Non li copierai. Imparerai gli schemi dietro ai loro risultati.",
    "Phase {0} : Création de contenu (Semaines {1}-{2})": "Fase {0}: creazione di contenuti (settimane {1}-{2})",
    "Étape {0} : Créez {1} vidéos de test": "Passo {0}: fai {1} video di prova",
    "Avant de vendre, testez. Créez {0} vidéos explorant différents angles :":
        "Prima di vendere, prova. Fai {0} video con tagli diversi:",
    "{0} vidéos \"transformation/avant-après\"": "{0} video «trasformazione / prima-dopo»",
    "{0} vidéos \"éducation\"": "{0} video «che spiegano»",
    "{0} vidéos \"divertissement pur\"": "{0} video «puro intrattenimento»",
    "{0} vidéos \"preuve sociale\"": "{0} video «prova sociale»",
    "{0} vidéos \"appel à l'action\"": "{0} video «call to action»",
    "{0} vidéos \"story personnel\"": "{0} video «storia personale»",
    "Publiez rapidement ({0}-{1} par jour). Ne vous souciez pas de la perfection. Observez ce qui fonctionne.":
        "Pubblica in fretta ({0}-{1} al giorno). Non pensare alla perfezione. Guarda cosa funziona.",
    "Étape {0} : Analysez vos résultats": "Passo {0}: leggi i risultati",
    "Après {0} vidéos, regardez les données :": "Dopo {0} video, guarda i dati:",
    "Quels types de vidéos donnent le plus de vues ?": "Quali tipi di video fanno più visualizzazioni?",
    "Quels hooks retiennent le plus longtemps ?": "Quali hook trattengono più a lungo?",
    "Quel ton résonne le plus ?": "Quale tono funziona meglio?",
    "Les {0} meilleures vidéos ? Observez leurs patterns communs. Vous allez répéter ces patterns.":
        "I tuoi {0} video migliori? Guarda cosa hanno in comune. Sono quegli schemi che ripeterai.",
    "Phase {0} : Optimisation (Semaines {1}-{2})": "Fase {0}: ottimizzazione (settimane {1}-{2})",
    "Étape {0} : Double-down sur ce qui fonctionne": "Passo {0}: raddoppia su ciò che funziona",
    "Créez {0} variantes des vidéos qui ont le mieux performé. Changez :":
        "Fai {0} varianti dei video andati meglio. Cambia:",
    "Les premières {0} secondes (hook différent)": "I primi {0} secondi (hook diverso)",
    "Le produit montré": "Il prodotto mostrato",
    "L'angle de caméra": "L'angolo di ripresa",
    "La musique/son": "La musica o l'audio",
    "Le ton de votre voix": "Il tono della tua voce",
    "Le même concept, {0} exécutions différentes. C'est ça qui crée de la croissance exponentielle.":
        "La stessa idea, {0} esecuzioni diverse. È questo che si somma nel tempo.",
    "Étape {0} : Introduisez progressivement vos produits": "Passo {0}: inserisci i prodotti poco alla volta",
    "Ne commencez pas à vendre immédiatement. Voici le timing optimal :":
        "Non iniziare subito a vendere. Questo è il ritmo che funziona:",
    "Semaines {0}-{1} : Zéro mention du produit. Construction d'audience.":
        "Settimane {0}-{1}: nessun accenno al prodotto. Costruisci il pubblico.",
    "Semaines {0}-{1} : Mention causelle. \"Voici ce que j'utilise...\"":
        "Settimane {0}-{1}: accenni casuali. «Questo è quello che uso io…»",
    "Semaines {0}+ : Vente directe. Maintenant votre audience vous connaît.":
        "Dalla settimana {0}: vendita diretta. Ormai il pubblico ti conosce.",
    "Cet ordre = conversion {0}x plus élevée que si vous vendez dès le jour {1}.":
        "Quest'ordine converte {0} volte meglio del vendere dal giorno {1}.",
    "Phase {0} : Monétisation (Semaines {1}+)": "Fase {0}: monetizzazione (dalla settimana {1})",
    "Étape {0} : Mettez en place les mécaniques de vente": "Passo {0}: monta la macchina di vendita",
    "Une fois que votre audience vous fait confiance, activez les ventes :":
        "Quando il pubblico si fida di te, accendi le vendite:",
    "Ajouter le produit à la TikTok Shop": "Aggiungere il prodotto al tuo TikTok Shop",
    "Créer des CTA clairs (links, codes promo)": "Scrivere call to action chiare (link, codici sconto)",
    "Tester différentes stratégies de pricing": "Provare diverse strategie di prezzo",
    "Analyser les conversions avec Qeerah": "Analizzare le conversioni con Qeerah",
    "Étape {0} : Itérez basé sur les résultats": "Passo {0}: correggi in base ai risultati",
    "Publiez, analysez, ajustez. Le cycle est :": "Pubblica, analizza, correggi. Il ciclo è:",
    "Vidéo publiée": "Video pubblicato",
    "Collectez les données (vues, rétention, conversions)": "Raccogli i dati (visualizzazioni, ritenzione, conversioni)",
    "Identifiez le pattern gagnant": "Individua lo schema vincente",
    "Créez {0} variantes du gagnant": "Crea {0} varianti del vincente",
    "Publiez et répétez": "Pubblica e ripeti",
    "🎯 Les Métriques Clés à Tracker": "🎯 I numeri che vale la pena seguire",
    "Retention Rate :": "Tasso di ritenzione:",
    "% de gens qui regardent jusqu'à la fin (Cible : {0}%+)": "% di persone che guardano fino in fondo (obiettivo: {0} %+)",
    "Engagement Rate :": "Tasso di interazione:",
    "Partages + Commentaires / Vues (Cible : {0}%+)": "Condivisioni + commenti / visualizzazioni (obiettivo: {0} %+)",
    "Conversion Rate :": "Tasso di conversione:",
    "Ventes / Clics vers produit (Cible : {0}%+)": "Vendite / clic sul prodotto (obiettivo: {0} %+)",
    "Cost per Acquisition :": "Costo per nuovo cliente:",
    "Marketing spend / Nouveau client (Cible :": "Spesa in marketing / nuovo cliente (obiettivo:",
    "⚠️ Les Erreurs Courantes à Éviter": "⚠️ Errori comuni da evitare",
    "Vendre trop tôt :": "Vendere troppo presto:",
    "Attendez d'avoir construit la confiance": "aspetta di aver costruito fiducia",
    "Négliger l'analyse :": "Saltare l'analisi:",
    "Les chiffres ne mentent pas": "i numeri non mentono",
    "Manque de cohérence :": "Essere incostanti:",
    "perfection": "perfezione",
    "Ignorer les tendances :": "Ignorare le tendenze:",
    "TikTok change vite. Adaptez-vous": "TikTok cambia in fretta: adattati",
    "Trop générique :": "Essere troppo generici:",
    "tout faire": "fare tutto",
    "✅ Checklist pour Démarrer": "✅ Checklist prima di partire",
    "☐ Niche définie clairement": "☐ Nicchia definita con chiarezza",
    "☐ Compte TikTok créé avec bio alignée à la niche": "☐ Account TikTok creato, bio in linea con la nicchia",
    "☐ {0} idées de vidéo écrites": "☐ {0} idee di video scritte",
    "☐ Caméra/téléphone prêt": "☐ Fotocamera o telefono pronti",
    "☐ Produit(s) à vendre sélectionné(s)": "☐ Prodotto/i da vendere scelti",
    "☐ TikTok Shop configurée": "☐ TikTok Shop configurato",
    "☐ Système de tracking mis en place": "☐ Un modo per misurare i risultati impostato",
    "Commencez votre stratégie maintenant": "Inizia subito la tua strategia",
    "Utilisez Qeerah pour optimiser chaque vidéo selon cette stratégie.":
        "Usa Qeerah per calibrare ogni video su questa strategia.",
    "Démarrer →": "Comincia →",
}

T_BLOG_GUIDE["pt-br"] = {
    "Guide Complet TikTok Shop {0} - Qeerah": "Guia completo do TikTok Shop {0} - Qeerah",
    "Guide complet pour structurer votre stratégie TikTok Shop de A à Z. Positionnement, contenu, optimisation, monétisation.":
        "Guia completo para montar sua estratégia de TikTok Shop do zero: posicionamento, conteúdo, otimização, monetização.",
    "Guide complet : structurer sa stratégie TikTok Shop en {0}": "Guia completo: montar sua estratégia de TikTok Shop em {0}",
    "Un guide étape par étape pour construire une stratégie TikTok Shop de A à Z : positionnement, contenu, optimisation, monétisation.":
        "Um guia passo a passo para construir uma estratégia de TikTok Shop do zero: posicionamento, conteúdo, otimização, monetização.",
    "← Retour au blog": "← Voltar ao blog",
    "📖 GUIDE COMPLET": "📖 GUIA COMPLETO",
    "Guide complet : Structurer sa stratégie TikTok Shop en {0}": "Guia completo: montar sua estratégia de TikTok Shop em {0}",
    "Vouloir réussir sur TikTok Shop sans stratégie c'est comme naviguer sans carte. Voici un guide étape par étape pour construire une stratégie solide en {0}.":
        "Querer ir bem no TikTok Shop sem estratégia é como navegar sem mapa. Aqui vai um guia passo a passo para montar uma estratégia sólida em {0}.",
    "Phase {0} : Positionnement (Semaines {1}-{2})": "Fase {0}: posicionamento (semanas {1}-{2})",
    "Étape {0} : Trouvez votre niche": "Passo {0}: ache seu nicho",
    "Répondez à ces questions :": "Responda a estas perguntas:",
    "Que puis-je enseigner mieux que {0}% des gens ?": "O que eu ensino melhor do que {0} % das pessoas?",
    "Qui est mon client idéal ?": "Quem é meu cliente ideal?",
    "Quel problème je résous ?": "Que problema eu resolvo?",
    "Votre niche ne doit pas être minuscule, mais elle doit être claire. \"Mode\" c'est trop large. \"Mode éthique pour les femmes {0}-{1} urbaines\" c'est parfait.":
        "Seu nicho não precisa ser minúsculo, mas precisa ser claro. “Moda” é amplo demais. “Moda ética para mulheres de cidade entre {0} e {1} anos” já serve.",
    "Étape {0} : Analysez la concurrence": "Passo {0}: estude a concorrência",
    "Trouvez {0}-{1} créateurs qui vendent dans votre niche. Regardez :":
        "Ache {0}-{1} criadores que vendem no seu nicho. Repare em:",
    "Quels types de contenu performent": "Que tipos de conteúdo funcionam",
    "Quel est leur ton/personnalité": "O tom e a personalidade deles",
    "Comment ils présentent les produits": "Como eles mostram os produtos",
    "Leurs CTA (appels à l'action)": "As chamadas para ação deles",
    "Vous n'allez pas les copier. Vous allez apprendre leurs patterns de succès.":
        "Você não vai copiar. Vai aprender os padrões por trás dos resultados deles.",
    "Phase {0} : Création de contenu (Semaines {1}-{2})": "Fase {0}: criação de conteúdo (semanas {1}-{2})",
    "Étape {0} : Créez {1} vidéos de test": "Passo {0}: faça {1} vídeos de teste",
    "Avant de vendre, testez. Créez {0} vidéos explorant différents angles :":
        "Antes de vender, teste. Faça {0} vídeos explorando ângulos diferentes:",
    "{0} vidéos \"transformation/avant-après\"": "{0} vídeos de “transformação / antes e depois”",
    "{0} vidéos \"éducation\"": "{0} vídeos “para ensinar”",
    "{0} vidéos \"divertissement pur\"": "{0} vídeos “puro entretenimento”",
    "{0} vidéos \"preuve sociale\"": "{0} vídeos de “prova social”",
    "{0} vidéos \"appel à l'action\"": "{0} vídeos de “chamada para ação”",
    "{0} vidéos \"story personnel\"": "{0} vídeos de “história pessoal”",
    "Publiez rapidement ({0}-{1} par jour). Ne vous souciez pas de la perfection. Observez ce qui fonctionne.":
        "Publique rápido ({0}-{1} por dia). Não se prenda à perfeição. Observe o que funciona.",
    "Étape {0} : Analysez vos résultats": "Passo {0}: leia seus resultados",
    "Après {0} vidéos, regardez les données :": "Depois de {0} vídeos, olhe os dados:",
    "Quels types de vidéos donnent le plus de vues ?": "Que tipo de vídeo dá mais visualizações?",
    "Quels hooks retiennent le plus longtemps ?": "Que ganchos seguram por mais tempo?",
    "Quel ton résonne le plus ?": "Que tom conecta melhor?",
    "Les {0} meilleures vidéos ? Observez leurs patterns communs. Vous allez répéter ces patterns.":
        "Seus {0} melhores vídeos? Veja o que eles têm em comum. São esses padrões que você vai repetir.",
    "Phase {0} : Optimisation (Semaines {1}-{2})": "Fase {0}: otimização (semanas {1}-{2})",
    "Étape {0} : Double-down sur ce qui fonctionne": "Passo {0}: dobre a aposta no que funciona",
    "Créez {0} variantes des vidéos qui ont le mieux performé. Changez :":
        "Faça {0} variações dos vídeos que foram melhor. Mude:",
    "Les premières {0} secondes (hook différent)": "Os primeiros {0} segundos (outro gancho)",
    "Le produit montré": "O produto mostrado",
    "L'angle de caméra": "O ângulo da câmera",
    "La musique/son": "A música ou o som",
    "Le ton de votre voix": "O tom da sua voz",
    "Le même concept, {0} exécutions différentes. C'est ça qui crée de la croissance exponentielle.":
        "A mesma ideia, {0} execuções diferentes. É isso que acumula.",
    "Étape {0} : Introduisez progressivement vos produits": "Passo {0}: traga seus produtos aos poucos",
    "Ne commencez pas à vendre immédiatement. Voici le timing optimal :":
        "Não comece a vender de cara. Este é o ritmo que funciona:",
    "Semaines {0}-{1} : Zéro mention du produit. Construction d'audience.":
        "Semanas {0}-{1}: nenhuma menção ao produto. Construir público.",
    "Semaines {0}-{1} : Mention causelle. \"Voici ce que j'utilise...\"":
        "Semanas {0}-{1}: menções casuais. “Isso aqui é o que eu uso…”",
    "Semaines {0}+ : Vente directe. Maintenant votre audience vous connaît.":
        "A partir da semana {0}: venda direta. Agora seu público te conhece.",
    "Cet ordre = conversion {0}x plus élevée que si vous vendez dès le jour {1}.":
        "Essa ordem converte {0}× melhor do que vender já no dia {1}.",
    "Phase {0} : Monétisation (Semaines {1}+)": "Fase {0}: monetização (a partir da semana {1})",
    "Étape {0} : Mettez en place les mécaniques de vente": "Passo {0}: monte a mecânica de venda",
    "Une fois que votre audience vous fait confiance, activez les ventes :":
        "Quando seu público confiar em você, ligue as vendas:",
    "Ajouter le produit à la TikTok Shop": "Colocar o produto no seu TikTok Shop",
    "Créer des CTA clairs (links, codes promo)": "Escrever chamadas para ação claras (links, cupons)",
    "Tester différentes stratégies de pricing": "Testar estratégias de preço diferentes",
    "Analyser les conversions avec Qeerah": "Analisar as conversões com a Qeerah",
    "Étape {0} : Itérez basé sur les résultats": "Passo {0}: ajuste com base nos resultados",
    "Publiez, analysez, ajustez. Le cycle est :": "Publique, analise, ajuste. O ciclo é:",
    "Vidéo publiée": "Vídeo publicado",
    "Collectez les données (vues, rétention, conversions)": "Colete os dados (visualizações, retenção, conversões)",
    "Identifiez le pattern gagnant": "Identifique o padrão vencedor",
    "Créez {0} variantes du gagnant": "Crie {0} variações do vencedor",
    "Publiez et répétez": "Publique e repita",
    "🎯 Les Métriques Clés à Tracker": "🎯 Os números que vale a pena acompanhar",
    "Retention Rate :": "Taxa de retenção:",
    "% de gens qui regardent jusqu'à la fin (Cible : {0}%+)": "% de gente que assiste até o fim (meta: {0} %+)",
    "Engagement Rate :": "Taxa de engajamento:",
    "Partages + Commentaires / Vues (Cible : {0}%+)": "Compartilhamentos + comentários / visualizações (meta: {0} %+)",
    "Conversion Rate :": "Taxa de conversão:",
    "Ventes / Clics vers produit (Cible : {0}%+)": "Vendas / cliques no produto (meta: {0} %+)",
    "Cost per Acquisition :": "Custo por cliente novo:",
    "Marketing spend / Nouveau client (Cible :": "Gasto em marketing / cliente novo (meta:",
    "⚠️ Les Erreurs Courantes à Éviter": "⚠️ Erros comuns que dá para evitar",
    "Vendre trop tôt :": "Vender cedo demais:",
    "Attendez d'avoir construit la confiance": "espere ter construído confiança",
    "Négliger l'analyse :": "Pular a análise:",
    "Les chiffres ne mentent pas": "os números não mentem",
    "Manque de cohérence :": "Falta de constância:",
    "perfection": "perfeição",
    "Ignorer les tendances :": "Ignorar as tendências:",
    "TikTok change vite. Adaptez-vous": "o TikTok muda rápido: acompanhe",
    "Trop générique :": "Ser genérico demais:",
    "tout faire": "fazer tudo",
    "✅ Checklist pour Démarrer": "✅ Checklist para começar",
    "☐ Niche définie clairement": "☐ Nicho definido com clareza",
    "☐ Compte TikTok créé avec bio alignée à la niche": "☐ Conta no TikTok criada, com bio alinhada ao nicho",
    "☐ {0} idées de vidéo écrites": "☐ {0} ideias de vídeo escritas",
    "☐ Caméra/téléphone prêt": "☐ Câmera ou celular prontos",
    "☐ Produit(s) à vendre sélectionné(s)": "☐ Produto(s) para vender escolhido(s)",
    "☐ TikTok Shop configurée": "☐ TikTok Shop configurada",
    "☐ Système de tracking mis en place": "☐ Um jeito de medir resultados montado",
    "Commencez votre stratégie maintenant": "Comece sua estratégia agora",
    "Utilisez Qeerah pour optimiser chaque vidéo selon cette stratégie.":
        "Use a Qeerah para ajustar cada vídeo a essa estratégia.",
    "Démarrer →": "Começar →",
}

T_BLOG_GUIDE["en-ie"] = dict(T_BLOG_GUIDE["en"])
T_BLOG_GUIDE["es-mx"] = dict(T_BLOG_GUIDE["es"])


# ═══════════════════════════════════════════════════════════════════════════
# /blog/expansion-mondiale-tiktok-shop
# ⚠️ LES TITRES DES SOURCES NE SONT PAS TRADUITS. Ce sont des citations : le
# titre d'un article de ContentGrip ou de Forbes doit rester tel qu'il a été
# publié, sinon la référence devient invérifiable. Seuls les noms de PAYS et le
# texte rédactionnel sont traduits.
# ═══════════════════════════════════════════════════════════════════════════
T_BLOG_EXPANSION: dict[str, dict[str, str]] = {}

T_BLOG_EXPANSION["en"] = {
    "TikTok Shop : c'est quoi et peut-on gagner de l'argent avec ? - Qeerah":
        "TikTok Shop: what is it, and can you make money with it? - Qeerah",
    "TikTok Shop, c'est quoi et comment ça marche ? Peut-on vraiment gagner de l'argent avec ? Pays disponibles, chiffres de GMV et créateurs devenus millionnaires, avec sources vérifiées.":
        "What TikTok Shop is and how it works. Can you really make money with it? Countries covered, GMV figures and creators who got rich, with checked sources.",
    "TikTok Shop : c'est quoi et peut-on gagner de l'argent avec ?":
        "TikTok Shop: what is it, and can you make money with it?",
    "Ce qu'est TikTok Shop, comment ça marche, dans quels pays c'est disponible, et si on peut vraiment en vivre. Chiffres et créateurs millionnaires, sources à l'appui.":
        "What TikTok Shop is, how it works, which countries have it, and whether you can live off it. Figures and millionaire creators, with sources.",
    "← Retour au blog": "← Back to the blog",
    "💡 GUIDE TIKTOK SHOP": "💡 TIKTOK SHOP GUIDE",
    "TikTok Shop : c'est quoi, et peut-on vraiment gagner de l'argent avec ?":
        "TikTok Shop: what is it, and can you really make money with it?",
    "📅 Juillet {0}": "📅 July {0}",
    "👤 Par l'équipe Qeerah": "👤 By the Qeerah team",
    "⏱️ {0} min de lecture": "⏱️ {0} min read",
    "🇬🇧 Read in English": "🇬🇧 Read in English",
    "🔎 En bref :": "🔎 In short:",
    "TikTok Shop est la fonctionnalité e-commerce intégrée à TikTok qui permet d'acheter directement depuis l'app, via vidéos, lives ou vitrine boutique. Lancée en {0}, elle est aujourd'hui disponible dans une vingtaine de pays et a généré {1} milliards de dollars de ventes en {2}.":
        "TikTok Shop is the e-commerce layer built into TikTok, letting people buy straight from the app through videos, live streams or a shop front. Launched in {0}, it now runs in around twenty countries and generated ${1} billion in sales in {2}.",
    "Oui, on peut gagner de l'argent avec": "Yes, you can make money with it",
    "— en tant que créateur affilié (commissions) ou en tant que vendeur — mais la réalité est à deux vitesses : le créateur médian touche environ {0} $/mois, quand une minorité de top créateurs ou marques génèrent plusieurs millions.":
        "— as an affiliate creator (commissions) or as a seller — but it's a two-speed reality: the median creator makes around ${0} a month, while a small group of top creators and brands pull in millions.",
    "En un peu moins de quatre ans, TikTok Shop est passé d'un test discret en Asie du Sud-Est à l'une des plus grosses machines de social commerce au monde. Voici, chiffres et sources à l'appui, ce qu'est réellement TikTok Shop, comment ça fonctionne, dans quels pays c'est disponible, et qui sont les créateurs américains qui en ont déjà fait des fortunes.":
        "In just under four years, TikTok Shop went from a quiet test in Southeast Asia to one of the biggest social commerce machines in the world. Here, with figures and sources, is what TikTok Shop actually is, how it works, which countries have it, and which American creators have already made fortunes on it.",
    "📊 Les chiffres qui résument l'explosion": "📊 The figures that sum up the boom",
    "Le GMV (volume de marchandises vendues) mondial de TikTok Shop a atteint":
        "TikTok Shop's global GMV (gross merchandise value) reached",
    "{0} milliards de dollars en {1}": "${0} billion in {1}",
    ", en hausse de {0} % sur un an, réparti sur une quinzaine de marchés actifs cette année-là (":
        ", up {0}% year on year, across the fifteen or so markets active that year (",
    "). Pour donner une idée de la vitesse : il a fallu {0} ans à Amazon pour atteindre {1} milliards de dollars de GMV annuel ; TikTok Shop est en passe de franchir ce seuil dès sa quatrième année pleine (":
        "). For a sense of the pace: it took Amazon {0} years to reach ${1} billion in annual GMV; TikTok Shop is on course to pass that in its fourth full year (",
    "{0} Md$": "${0}B",
    "GMV mondial {0} (+{1}%)": "Global GMV {0} (+{1}%)",
    "GMV mondial projeté {0}": "Projected global GMV {0}",
    "GMV USA {0} (+{1}%)": "US GMV {0} (+{1}%)",
    "GMV Asie du Sud-Est {0}": "Southeast Asia GMV {0}",
    "Sources :": "Sources:",
    "Aux États-Unis, TikTok Shop captait déjà": "In the United States, TikTok Shop was already taking",
    "{0} % de toutes les ventes de social commerce en {1}": "{0}% of all social commerce sales in {1}",
    "). Certaines projections à long terme évoquent même une plateforme capable de peser près de {0} milliards de dollars de ventes d'ici {1}, ce qui en ferait un top {2} mondial du commerce en ligne derrière Amazon (":
        "). Some long-range projections even put the platform near ${0} billion in sales by {1}, which would make it a global top {2} in online commerce behind Amazon (",
    "🗓️ La timeline de l'expansion internationale": "🗓️ A timeline of the international rollout",
    "TikTok Shop n'a pas explosé partout en même temps. Son ouverture s'est faite marché par marché, sur un rythme qui s'est nettement accéléré depuis {0}.":
        "TikTok Shop didn't take off everywhere at once. It opened market by market, at a pace that has picked up sharply since {0}.",
    "Premiers tests d'e-commerce intégré, dont un partenariat pilote avec Shopify qui ne prendra finalement pas (":
        "First tests of built-in e-commerce, including a pilot partnership with Shopify that ultimately went nowhere (",
    "{0} avril {1} —": "{0} April {1} —",
    "Lancement officiel du e-commerce transfrontalier dans quatre pays d'Asie du Sud-Est : Thaïlande, Vietnam, Malaisie et Philippines (":
        "Official launch of cross-border e-commerce in four Southeast Asian countries: Thailand, Vietnam, Malaysia and the Philippines (",
    "Novembre {0} —": "November {0} —",
    "Début des tests beta au Royaume-Uni, en parallèle de plusieurs marchés d'Asie du Sud-Est (":
        "Beta testing begins in the United Kingdom, alongside several Southeast Asian markets (",
    "Fin {0} —": "Late {0} —",
    "TikTok Shop est actif dans six pays d'Asie (Chine, Indonésie compris) et au Royaume-Uni (":
        "TikTok Shop is live in six Asian countries (including China and Indonesia) and in the UK (",
    "{0} septembre {1} —": "{0} September {1} —",
    "Lancement officiel aux États-Unis, l'ouverture qui fera basculer TikTok Shop dans une autre dimension (":
        "Official launch in the United States — the opening that would take TikTok Shop to another scale (",
    "Consolidation en Asie du Sud-Est (Singapour, Japon) et premières ouvertures en Amérique latine, au Mexique et au Brésil.":
        "Consolidation in Southeast Asia (Singapore, Japan) and first openings in Latin America, in Mexico and Brazil.",
    "Vague européenne : France, Allemagne, Espagne, Italie, Irlande et Royaume-Uni s'établissent comme marchés matures.":
        "The European wave: France, Germany, Spain, Italy, Ireland and the UK settle in as mature markets.",
    "{0} juin {1} —": "{0} June {1} —",
    "L'Autriche, la Belgique, les Pays-Bas et la Pologne rejoignent l'Europe TikTok Shop, avec un nouvel outil « Sell Across Europe » qui permet à un vendeur de couvrir plusieurs pays européens avec une seule inscription (":
        "Austria, Belgium, the Netherlands and Poland join TikTok Shop's Europe, with a new “Sell Across Europe” tool that lets one seller cover several European countries from a single registration (",
    "🗺️ Les marchés ouverts aujourd'hui, région par région": "🗺️ The markets open today, region by region",
    "Mi-{0}, TikTok Shop Seller Center est officiellement actif dans une vingtaine de marchés répartis sur trois continents (":
        "As of mid-{0}, TikTok Shop Seller Center is officially live in around twenty markets across three continents (",
    "🌎 Amériques": "🌎 Americas",
    "États-Unis": "United States",
    "Mexique": "Mexico",
    "Brésil": "Brazil",
    "🇪🇺 Europe": "🇪🇺 Europe",
    "Royaume-Uni": "United Kingdom",
    "France": "France",
    "Allemagne": "Germany",
    "Espagne": "Spain",
    "Italie": "Italy",
    "Irlande": "Ireland",
    "Autriche": "Austria",
    "(juin {0})": "(June {0})",
    "Belgique": "Belgium",
    "Pays-Bas": "Netherlands",
    "Pologne": "Poland",
    "🌏 Asie-Pacifique": "🌏 Asia-Pacific",
    "Indonésie": "Indonesia",
    "Thaïlande": "Thailand",
    "Vietnam": "Vietnam",
    "Malaisie": "Malaysia",
    "Philippines": "Philippines",
    "Singapour": "Singapore",
    "Japon": "Japan",
    "Pas encore ouvert :": "Not open yet:",
    "l'Australie n'a toujours pas accès à TikTok Shop Seller Center mi-{0}, et malgré des rumeurs récurrentes, aucun lancement natif n'est confirmé dans le Golfe (Arabie saoudite, Émirats) à cette date (":
        "Australia still has no access to TikTok Shop Seller Center as of mid-{0}, and despite recurring rumours, no native launch is confirmed in the Gulf (Saudi Arabia, UAE) at that date (",
    "🇮🇩 L'Indonésie, nouveau rival direct des États-Unis": "🇮🇩 Indonesia, now a direct rival to the US",
    "C'est l'un des faits les plus frappants de {0} : sur le premier semestre, l'": "One of the most striking facts of {0}: over the first half of the year,",
    "Indonésie a dépassé les États-Unis": "Indonesia overtook the United States",
    "comme premier marché de TikTok Shop, avec {0} milliards de dollars de GMV contre {1} milliards pour les USA (":
        "as TikTok Shop's largest market, with ${0} billion in GMV against ${1} billion for the US (",
    "). Sur l'année {0} complète, les États-Unis reprennent la tête ({1} Md$ contre {2} Md$ pour l'Indonésie), mais l'Indonésie reste le deuxième marché mondial de la plateforme, et toute la région Asie du Sud-Est a doublé son GMV en un an pour atteindre {3} milliards de dollars (":
        "). Over the full year {0}, the United States takes the lead back (${1}B against ${2}B for Indonesia), but Indonesia remains the platform's second market worldwide, and the whole Southeast Asia region doubled its GMV in a year to ${3} billion (",
    "💰 Les créateurs américains devenus millionnaires grâce à TikTok Shop":
        "💰 The American creators who got rich on TikTok Shop",
    "Derrière les chiffres macro, il y a des histoires individuelles très concrètes. Voici trois créateurs américains dont la réussite sur TikTok Shop est documentée dans la presse.":
        "Behind the macro figures are very concrete individual stories. Here are three American creators whose TikTok Shop results are documented in the press.",
    "Stormi Steele — Canvas Beauty (Body Glaze)": "Stormi Steele — Canvas Beauty (Body Glaze)",
    "{0}M$": "${0}M",
    "en un seul live ({0} juin {1})": "in a single live stream ({0} June {1})",
    "en une journée (Black Friday)": "in one day (Black Friday)",
    "de ventes mensuelles visées": "in monthly sales, the target",
    "Fondatrice de Canvas Beauty et de sa gamme Body Glaze (huile de soin corporel), Stormi Steele est devenue la première créatrice à dépasser {0} million de dollars de ventes lors d'un seul live TikTok Shop, le {1} juin {2} (":
        "Founder of Canvas Beauty and its Body Glaze line (body care oil), Stormi Steele became the first creator to pass ${0} million in sales during a single TikTok Shop live stream, on {1} June {2} (",
    "). Lors du Black Friday, sa marque a généré {0} millions de dollars de ventes en une journée, dont {1} millions via un « mega live » de {2} heures organisé depuis son entrepôt en Alabama (":
        "). On Black Friday, her brand generated ${0} million in sales in one day, ${1} million of it through a {2}-hour “mega live” run from her warehouse in Alabama (",
    "). Canvas Beauty a depuis été désignée marque n°{0} en ventes sur TikTok Shop aux États-Unis, avec une trajectoire vers {1} millions de dollars de ventes mensuelles (":
        "). Canvas Beauty has since been named the #{0} brand by sales on TikTok Shop in the United States, on a path towards ${1} million in monthly sales (",
    "Logan Walter — Beauté & self-care masculin": "Logan Walter — men's beauty and self-care",
    "{0} ans": "{0} years old",
    "au moment de devenir millionnaire": "when he became a millionaire",
    "pour atteindre ce statut": "to get there",
    "{0} chiffres": "{0} figures",
    "de revenu mensuel": "in monthly income",
    "Logan Walter a quitté l'université à {0} ans pour se consacrer à TikTok Shop, où il s'est imposé comme l'un des rares hommes affiliés dans le créneau beauté/self-care, en vendant des marques comme Medicube ou Neutrogena. Sa première vidéo virale lui a fait gagner plus de {1} dollars en un mois ; deux ans après ses débuts, il touchait un revenu mensuel à sept chiffres (":
        "Logan Walter dropped out of university at {0} to go all in on TikTok Shop, where he became one of the few male affiliates in the beauty and self-care lane, selling brands like Medicube and Neutrogena. His first viral video earned him more than ${1} in a month; two years after starting, he was making a seven-figure monthly income (",
    "Katrina Dimiele — Mode en direct (try-on livestreams)": "Katrina Dimiele — fashion live streams (try-on hauls)",
    "cumulés en {0} ans": "over {0} years",
    "heures de vente en direct": "hours of live selling",
    "Créatrice mode spécialisée dans les « try-on hauls » en direct, Katrina Dimiele a cumulé {0} millions de dollars de ventes en neuf ans via ses lives sur TikTok Shop et Facebook (":
        "A fashion creator who specialises in live try-on hauls, Katrina Dimiele has done ${0} million in sales over nine years through her live streams on TikTok Shop and Facebook (",
    "). Son parcours illustre une réalité importante : la plupart des plus gros succès viennent de créateurs qui ont accumulé des milliers d'heures de pratique avant d'exploser, pas d'un coup de chance isolé.":
        "). Her path shows something worth noting: most of the biggest successes come from creators who put in thousands of hours before breaking through, not from one lucky moment.",
    "🔑 À retenir :": "🔑 Worth keeping:",
    "ces trois parcours partagent un point commun — le live shopping. C'est le format qui génère les pics de revenus les plus spectaculaires sur TikTok Shop, bien plus que les vidéos courtes seules.":
        "all three paths share one thing — live shopping. It's the format that produces the most spectacular revenue spikes on TikTok Shop, far more than short videos alone.",
    "📉 Et pour un créateur « normal » ?": "📉 And for an ordinary creator?",
    "Ces histoires sont réelles, mais elles ne représentent pas la moyenne. Selon les données de monétisation {0}, le créateur médian sur TikTok gagne environ {1} dollars par mois toutes sources confondues, tandis que les {2} % les plus performants combinent plusieurs revenus pour atteindre {3} à {4} dollars par mois (":
        "These stories are real, but they aren't the average. According to {0} monetisation data, the median TikTok creator makes around ${1} a month across all sources, while the top {2}% combine several income streams to reach ${3} to ${4} a month (",
    "). Les millions de Stormi Steele, Logan Walter ou Katrina Dimiele sont le sommet visible d'une pyramide beaucoup plus large.":
        "). The millions made by Stormi Steele, Logan Walter or Katrina Dimiele are the visible top of a much wider pyramid.",
    "🔮 Ce qui s'annonce ensuite": "🔮 What's coming next",
    "Le rythme d'expansion ne ralentit pas : après la vague européenne de juin {0}, TikTok Shop teste déjà des abonnements payants qui rappellent le modèle Amazon Prime (":
        "The pace isn't slowing: after the European wave of June {0}, TikTok Shop is already testing paid subscriptions that look a lot like Amazon Prime (",
    "), et des enseignes historiques comme Ulta Beauty ont rejoint la plateforme aux États-Unis en misant sur sa capacité à transformer la découverte en achat (":
        "), and long-established retailers like Ulta Beauty have joined the platform in the United States, betting on its ability to turn discovery into purchase (",
    "❓ Questions fréquentes": "❓ Frequently asked questions",
    "Qu'est-ce que TikTok Shop ?": "What is TikTok Shop?",
    "TikTok Shop est la fonctionnalité e-commerce intégrée à TikTok qui permet d'acheter des produits directement depuis l'application, via des vidéos courtes, des lives shopping ou une vitrine boutique. Lancée en {0}, elle est disponible mi-{1} dans une vingtaine de pays dont les États-Unis, le Royaume-Uni, la France, l'Allemagne, l'Espagne, l'Italie, l'Irlande, l'Indonésie, la Thaïlande, le Vietnam, la Malaisie, les Philippines, Singapour, le Japon, le Mexique et le Brésil.":
        "TikTok Shop is the e-commerce layer built into TikTok, letting people buy products straight from the app through short videos, live shopping or a shop front. Launched in {0}, as of mid-{1} it is available in around twenty countries including the United States, the United Kingdom, France, Germany, Spain, Italy, Ireland, Indonesia, Thailand, Vietnam, Malaysia, the Philippines, Singapore, Japan, Mexico and Brazil.",
    "Peut-on vraiment gagner de l'argent avec TikTok Shop ?": "Can you really make money with TikTok Shop?",
    "Oui : les créateurs peuvent toucher des commissions d'affiliation en recommandant des produits, et les vendeurs peuvent gérer leur propre boutique. Certains créateurs comme Stormi Steele (Canvas Beauty) ou Logan Walter sont devenus millionnaires grâce à TikTok Shop. Mais la réalité reste à deux vitesses : le créateur médian gagne environ {0} dollars par mois, et seule une minorité de top créateurs atteint des revenus à sept chiffres.":
        "Yes: creators can earn affiliate commissions by recommending products, and sellers can run their own shop. Some creators, like Stormi Steele (Canvas Beauty) or Logan Walter, have become millionaires through TikTok Shop. But it stays a two-speed reality: the median creator makes around ${0} a month, and only a small minority of top creators reach seven figures.",
    "Dans quels pays TikTok Shop est-il disponible ?": "Which countries have TikTok Shop?",
    "Mi-{0}, TikTok Shop est actif dans une vingtaine de marchés : aux Amériques (États-Unis, Mexique, Brésil), en Europe (Royaume-Uni, France, Allemagne, Espagne, Italie, Irlande, et depuis juin {1} l'Autriche, la Belgique, les Pays-Bas et la Pologne), et en Asie-Pacifique (Indonésie, Thaïlande, Vietnam, Malaisie, Philippines, Singapour, Japon). L'Australie et les pays du Golfe n'ont pas encore de lancement officiel.":
        "As of mid-{0}, TikTok Shop is live in around twenty markets: in the Americas (United States, Mexico, Brazil), in Europe (United Kingdom, France, Germany, Spain, Italy, Ireland, and since June {1} Austria, Belgium, the Netherlands and Poland), and in Asia-Pacific (Indonesia, Thailand, Vietnam, Malaysia, the Philippines, Singapore, Japan). Australia and the Gulf states have no official launch yet.",
    "Vous voulez percer sur TikTok Shop ?": "Want to break through on TikTok Shop?",
    "Utilisez Qeerah pour analyser vos vidéos et copier ce qui fonctionne vraiment chez les créateurs qui cartonnent.":
        "Use Qeerah to analyse your videos and copy what actually works for the creators who are winning.",
    "Analyser mes vidéos →": "Analyse my videos →",
    "📚 Sources": "📚 Sources",
    "interview vidéo, TikTok Shop Millionaire": "video interview, TikTok Shop Millionaire",
    "TikTok Shop Millionaire — ${0}M in {1} Years Selling Fashion On Livestreams (interview vidéo)":
        "TikTok Shop Millionaire — ${0}M in {1} Years Selling Fashion On Livestreams (video interview)",
}

T_BLOG_EXPANSION["de"] = {
    "TikTok Shop : c'est quoi et peut-on gagner de l'argent avec ? - Qeerah":
        "TikTok Shop: Was ist das, und kann man damit Geld verdienen? - Qeerah",
    "TikTok Shop, c'est quoi et comment ça marche ? Peut-on vraiment gagner de l'argent avec ? Pays disponibles, chiffres de GMV et créateurs devenus millionnaires, avec sources vérifiées.":
        "Was TikTok Shop ist und wie es funktioniert. Kann man damit wirklich Geld verdienen? Verfügbare Länder, GMV-Zahlen und Creators, die reich geworden sind — mit geprüften Quellen.",
    "TikTok Shop : c'est quoi et peut-on gagner de l'argent avec ?":
        "TikTok Shop: Was ist das, und kann man damit Geld verdienen?",
    "Ce qu'est TikTok Shop, comment ça marche, dans quels pays c'est disponible, et si on peut vraiment en vivre. Chiffres et créateurs millionnaires, sources à l'appui.":
        "Was TikTok Shop ist, wie es funktioniert, in welchen Ländern es verfügbar ist und ob man davon leben kann. Zahlen und Millionen-Creators, mit Quellen.",
    "← Retour au blog": "← Zurück zum Blog",
    "💡 GUIDE TIKTOK SHOP": "💡 TIKTOK-SHOP-GUIDE",
    "TikTok Shop : c'est quoi, et peut-on vraiment gagner de l'argent avec ?":
        "TikTok Shop: Was ist das, und kann man damit wirklich Geld verdienen?",
    "📅 Juillet {0}": "📅 Juli {0}",
    "👤 Par l'équipe Qeerah": "👤 Vom Qeerah-Team",
    "⏱️ {0} min de lecture": "⏱️ {0} Min. Lesezeit",
    "🇬🇧 Read in English": "🇬🇧 Read in English",
    "🔎 En bref :": "🔎 Kurz gesagt:",
    "TikTok Shop est la fonctionnalité e-commerce intégrée à TikTok qui permet d'acheter directement depuis l'app, via vidéos, lives ou vitrine boutique. Lancée en {0}, elle est aujourd'hui disponible dans une vingtaine de pays et a généré {1} milliards de dollars de ventes en {2}.":
        "TikTok Shop ist die in TikTok eingebaute Verkaufsfunktion: Man kauft direkt in der App, über Videos, Livestreams oder eine Shop-Seite. {0} gestartet, läuft sie heute in rund zwanzig Ländern und hat {2} Verkäufe von {1} Milliarden Dollar erzeugt.",
    "Oui, on peut gagner de l'argent avec": "Ja, man kann damit Geld verdienen",
    "— en tant que créateur affilié (commissions) ou en tant que vendeur — mais la réalité est à deux vitesses : le créateur médian touche environ {0} $/mois, quand une minorité de top créateurs ou marques génèrent plusieurs millions.":
        "— als Affiliate-Creator (Provisionen) oder als Verkäufer — aber die Wirklichkeit hat zwei Geschwindigkeiten: Der mittlere Creator kommt auf etwa {0} $ im Monat, während eine kleine Gruppe von Top-Creators und Marken Millionen macht.",
    "En un peu moins de quatre ans, TikTok Shop est passé d'un test discret en Asie du Sud-Est à l'une des plus grosses machines de social commerce au monde. Voici, chiffres et sources à l'appui, ce qu'est réellement TikTok Shop, comment ça fonctionne, dans quels pays c'est disponible, et qui sont les créateurs américains qui en ont déjà fait des fortunes.":
        "In knapp vier Jahren wurde aus einem stillen Test in Südostasien eine der größten Social-Commerce-Maschinen der Welt. Hier steht, mit Zahlen und Quellen, was TikTok Shop wirklich ist, wie es funktioniert, in welchen Ländern es läuft und welche amerikanischen Creators damit schon Vermögen gemacht haben.",
    "📊 Les chiffres qui résument l'explosion": "📊 Die Zahlen, die den Boom zusammenfassen",
    "Le GMV (volume de marchandises vendues) mondial de TikTok Shop a atteint":
        "Der weltweite GMV (verkauftes Warenvolumen) von TikTok Shop erreichte",
    "{0} milliards de dollars en {1}": "{0} Milliarden Dollar im Jahr {1}",
    ", en hausse de {0} % sur un an, réparti sur une quinzaine de marchés actifs cette année-là (":
        ", ein Plus von {0} % gegenüber dem Vorjahr, verteilt auf die rund fünfzehn Märkte, die in dem Jahr aktiv waren (",
    "). Pour donner une idée de la vitesse : il a fallu {0} ans à Amazon pour atteindre {1} milliards de dollars de GMV annuel ; TikTok Shop est en passe de franchir ce seuil dès sa quatrième année pleine (":
        "). Zum Tempo: Amazon brauchte {0} Jahre für {1} Milliarden Dollar Jahres-GMV; TikTok Shop dürfte diese Schwelle schon im vierten vollen Jahr reißen (",
    "{0} Md$": "{0} Mrd. $",
    "GMV mondial {0} (+{1}%)": "Weltweiter GMV {0} (+{1} %)",
    "GMV mondial projeté {0}": "Prognostizierter weltweiter GMV {0}",
    "GMV USA {0} (+{1}%)": "GMV USA {0} (+{1} %)",
    "GMV Asie du Sud-Est {0}": "GMV Südostasien {0}",
    "Sources :": "Quellen:",
    "Aux États-Unis, TikTok Shop captait déjà": "In den USA holte TikTok Shop bereits",
    "{0} % de toutes les ventes de social commerce en {1}": "{0} % aller Social-Commerce-Verkäufe im Jahr {1}",
    "). Certaines projections à long terme évoquent même une plateforme capable de peser près de {0} milliards de dollars de ventes d'ici {1}, ce qui en ferait un top {2} mondial du commerce en ligne derrière Amazon (":
        "). Manche Langfristprognosen sehen die Plattform bis {1} sogar bei fast {0} Milliarden Dollar Umsatz — damit wäre sie weltweit in den Top {2} des Onlinehandels, hinter Amazon (",
    "🗓️ La timeline de l'expansion internationale": "🗓️ Die Zeitleiste der internationalen Ausbreitung",
    "TikTok Shop n'a pas explosé partout en même temps. Son ouverture s'est faite marché par marché, sur un rythme qui s'est nettement accéléré depuis {0}.":
        "TikTok Shop ist nicht überall gleichzeitig durchgestartet. Die Öffnung lief Markt für Markt, in einem Tempo, das sich seit {0} deutlich beschleunigt hat.",
    "Premiers tests d'e-commerce intégré, dont un partenariat pilote avec Shopify qui ne prendra finalement pas (":
        "Erste Tests mit eingebautem Handel, darunter eine Pilotpartnerschaft mit Shopify, aus der am Ende nichts wurde (",
    "{0} avril {1} —": "{0}. April {1} —",
    "Lancement officiel du e-commerce transfrontalier dans quatre pays d'Asie du Sud-Est : Thaïlande, Vietnam, Malaisie et Philippines (":
        "Offizieller Start des grenzüberschreitenden Handels in vier südostasiatischen Ländern: Thailand, Vietnam, Malaysia und den Philippinen (",
    "Novembre {0} —": "November {0} —",
    "Début des tests beta au Royaume-Uni, en parallèle de plusieurs marchés d'Asie du Sud-Est (":
        "Beginn der Beta-Tests im Vereinigten Königreich, parallel zu mehreren südostasiatischen Märkten (",
    "Fin {0} —": "Ende {0} —",
    "TikTok Shop est actif dans six pays d'Asie (Chine, Indonésie compris) et au Royaume-Uni (":
        "TikTok Shop läuft in sechs asiatischen Ländern (China und Indonesien inbegriffen) und im Vereinigten Königreich (",
    "{0} septembre {1} —": "{0}. September {1} —",
    "Lancement officiel aux États-Unis, l'ouverture qui fera basculer TikTok Shop dans une autre dimension (":
        "Offizieller Start in den USA — die Öffnung, die TikTok Shop in eine andere Größenordnung bringt (",
    "Consolidation en Asie du Sud-Est (Singapour, Japon) et premières ouvertures en Amérique latine, au Mexique et au Brésil.":
        "Festigung in Südostasien (Singapur, Japan) und erste Öffnungen in Lateinamerika, in Mexiko und Brasilien.",
    "Vague européenne : France, Allemagne, Espagne, Italie, Irlande et Royaume-Uni s'établissent comme marchés matures.":
        "Die europäische Welle: Frankreich, Deutschland, Spanien, Italien, Irland und das Vereinigte Königreich etablieren sich als reife Märkte.",
    "{0} juin {1} —": "{0}. Juni {1} —",
    "L'Autriche, la Belgique, les Pays-Bas et la Pologne rejoignent l'Europe TikTok Shop, avec un nouvel outil « Sell Across Europe » qui permet à un vendeur de couvrir plusieurs pays européens avec une seule inscription (":
        "Österreich, Belgien, die Niederlande und Polen kommen zum europäischen TikTok Shop dazu, mit dem neuen Werkzeug „Sell Across Europe“, mit dem ein Verkäufer mehrere europäische Länder über eine einzige Anmeldung bedienen kann (",
    "🗺️ Les marchés ouverts aujourd'hui, région par région": "🗺️ Die heute offenen Märkte, Region für Region",
    "Mi-{0}, TikTok Shop Seller Center est officiellement actif dans une vingtaine de marchés répartis sur trois continents (":
        "Mitte {0} ist das TikTok Shop Seller Center offiziell in rund zwanzig Märkten auf drei Kontinenten aktiv (",
    "🌎 Amériques": "🌎 Amerika",
    "États-Unis": "Vereinigte Staaten",
    "Mexique": "Mexiko",
    "Brésil": "Brasilien",
    "🇪🇺 Europe": "🇪🇺 Europa",
    "Royaume-Uni": "Vereinigtes Königreich",
    "France": "Frankreich",
    "Allemagne": "Deutschland",
    "Espagne": "Spanien",
    "Italie": "Italien",
    "Irlande": "Irland",
    "Autriche": "Österreich",
    "(juin {0})": "(Juni {0})",
    "Belgique": "Belgien",
    "Pays-Bas": "Niederlande",
    "Pologne": "Polen",
    "🌏 Asie-Pacifique": "🌏 Asien-Pazifik",
    "Indonésie": "Indonesien",
    "Thaïlande": "Thailand",
    "Vietnam": "Vietnam",
    "Malaisie": "Malaysia",
    "Philippines": "Philippinen",
    "Singapour": "Singapur",
    "Japon": "Japan",
    "Pas encore ouvert :": "Noch nicht offen:",
    "l'Australie n'a toujours pas accès à TikTok Shop Seller Center mi-{0}, et malgré des rumeurs récurrentes, aucun lancement natif n'est confirmé dans le Golfe (Arabie saoudite, Émirats) à cette date (":
        "Australien hat Mitte {0} noch immer keinen Zugang zum TikTok Shop Seller Center, und trotz wiederkehrender Gerüchte ist zu diesem Zeitpunkt kein eigener Start am Golf (Saudi-Arabien, Emirate) bestätigt (",
    "🇮🇩 L'Indonésie, nouveau rival direct des États-Unis": "🇮🇩 Indonesien, inzwischen direkter Rivale der USA",
    "C'est l'un des faits les plus frappants de {0} : sur le premier semestre, l'": "Eine der auffälligsten Tatsachen aus {0}: Im ersten Halbjahr hat",
    "Indonésie a dépassé les États-Unis": "Indonesien die Vereinigten Staaten überholt",
    "comme premier marché de TikTok Shop, avec {0} milliards de dollars de GMV contre {1} milliards pour les USA (":
        "als größter Markt von TikTok Shop, mit {0} Milliarden Dollar GMV gegenüber {1} Milliarden für die USA (",
    "). Sur l'année {0} complète, les États-Unis reprennent la tête ({1} Md$ contre {2} Md$ pour l'Indonésie), mais l'Indonésie reste le deuxième marché mondial de la plateforme, et toute la région Asie du Sud-Est a doublé son GMV en un an pour atteindre {3} milliards de dollars (":
        "). Über das gesamte Jahr {0} holen sich die USA die Spitze zurück ({1} Mrd. $ gegenüber {2} Mrd. $ für Indonesien), doch Indonesien bleibt der zweitgrößte Markt der Plattform, und ganz Südostasien hat seinen GMV binnen eines Jahres auf {3} Milliarden Dollar verdoppelt (",
    "💰 Les créateurs américains devenus millionnaires grâce à TikTok Shop":
        "💰 Die amerikanischen Creators, die mit TikTok Shop reich wurden",
    "Derrière les chiffres macro, il y a des histoires individuelles très concrètes. Voici trois créateurs américains dont la réussite sur TikTok Shop est documentée dans la presse.":
        "Hinter den großen Zahlen stehen sehr konkrete Einzelgeschichten. Hier sind drei amerikanische Creators, deren Erfolg auf TikTok Shop in der Presse belegt ist.",
    "Stormi Steele — Canvas Beauty (Body Glaze)": "Stormi Steele — Canvas Beauty (Body Glaze)",
    "{0}M$": "{0} Mio. $",
    "en un seul live ({0} juin {1})": "in einem einzigen Livestream ({0}. Juni {1})",
    "en une journée (Black Friday)": "an einem Tag (Black Friday)",
    "de ventes mensuelles visées": "angepeilter Monatsumsatz",
    "Fondatrice de Canvas Beauty et de sa gamme Body Glaze (huile de soin corporel), Stormi Steele est devenue la première créatrice à dépasser {0} million de dollars de ventes lors d'un seul live TikTok Shop, le {1} juin {2} (":
        "Als Gründerin von Canvas Beauty und der Linie Body Glaze (Körperpflegeöl) war Stormi Steele die erste Creatorin, die in einem einzigen TikTok-Shop-Livestream über {0} Million Dollar Umsatz machte, am {1}. Juni {2} (",
    "). Lors du Black Friday, sa marque a généré {0} millions de dollars de ventes en une journée, dont {1} millions via un « mega live » de {2} heures organisé depuis son entrepôt en Alabama (":
        "). Am Black Friday machte ihre Marke {0} Millionen Dollar Umsatz an einem Tag, davon {1} Millionen über einen {2}-stündigen „Mega-Live“ aus ihrem Lager in Alabama (",
    "). Canvas Beauty a depuis été désignée marque n°{0} en ventes sur TikTok Shop aux États-Unis, avec une trajectoire vers {1} millions de dollars de ventes mensuelles (":
        "). Canvas Beauty gilt seither als Marke Nr. {0} nach Umsatz auf TikTok Shop in den USA, auf dem Weg zu {1} Millionen Dollar Monatsumsatz (",
    "Logan Walter — Beauté & self-care masculin": "Logan Walter — Beauty und Selbstpflege für Männer",
    "{0} ans": "{0} Jahre alt",
    "au moment de devenir millionnaire": "als er Millionär wurde",
    "pour atteindre ce statut": "bis dahin",
    "{0} chiffres": "{0} Stellen",
    "de revenu mensuel": "Monatseinkommen",
    "Logan Walter a quitté l'université à {0} ans pour se consacrer à TikTok Shop, où il s'est imposé comme l'un des rares hommes affiliés dans le créneau beauté/self-care, en vendant des marques comme Medicube ou Neutrogena. Sa première vidéo virale lui a fait gagner plus de {1} dollars en un mois ; deux ans après ses débuts, il touchait un revenu mensuel à sept chiffres (":
        "Logan Walter brach mit {0} das Studium ab, um voll auf TikTok Shop zu setzen. Dort wurde er einer der wenigen männlichen Affiliates im Bereich Beauty und Selbstpflege und verkaufte Marken wie Medicube oder Neutrogena. Sein erstes virales Video brachte ihm in einem Monat über {1} Dollar; zwei Jahre nach dem Start lag sein Monatseinkommen im siebenstelligen Bereich (",
    "Katrina Dimiele — Mode en direct (try-on livestreams)": "Katrina Dimiele — Mode im Livestream (Try-on-Hauls)",
    "cumulés en {0} ans": "über {0} Jahre",
    "heures de vente en direct": "Stunden Live-Verkauf",
    "Créatrice mode spécialisée dans les « try-on hauls » en direct, Katrina Dimiele a cumulé {0} millions de dollars de ventes en neuf ans via ses lives sur TikTok Shop et Facebook (":
        "Als Mode-Creatorin, die auf Live-Try-on-Hauls spezialisiert ist, hat Katrina Dimiele in neun Jahren {0} Millionen Dollar Umsatz über ihre Livestreams auf TikTok Shop und Facebook gemacht (",
    "). Son parcours illustre une réalité importante : la plupart des plus gros succès viennent de créateurs qui ont accumulé des milliers d'heures de pratique avant d'exploser, pas d'un coup de chance isolé.":
        "). Ihr Weg zeigt etwas Wichtiges: Die größten Erfolge kommen meist von Creators, die tausende Stunden geübt haben, bevor es losging — nicht von einem einzelnen Glücksmoment.",
    "🔑 À retenir :": "🔑 Zum Merken:",
    "ces trois parcours partagent un point commun — le live shopping. C'est le format qui génère les pics de revenus les plus spectaculaires sur TikTok Shop, bien plus que les vidéos courtes seules.":
        "Diese drei Wege haben eines gemeinsam — Live-Shopping. Das ist das Format, das auf TikTok Shop die spektakulärsten Umsatzspitzen erzeugt, weit mehr als kurze Videos allein.",
    "📉 Et pour un créateur « normal » ?": "📉 Und für einen ganz normalen Creator?",
    "Ces histoires sont réelles, mais elles ne représentent pas la moyenne. Selon les données de monétisation {0}, le créateur médian sur TikTok gagne environ {1} dollars par mois toutes sources confondues, tandis que les {2} % les plus performants combinent plusieurs revenus pour atteindre {3} à {4} dollars par mois (":
        "Diese Geschichten sind echt, aber sie sind nicht der Durchschnitt. Nach den Monetarisierungsdaten von {0} verdient der mittlere TikTok-Creator über alle Quellen hinweg rund {1} Dollar im Monat, während die besten {2} % mehrere Einnahmequellen kombinieren und auf {3} bis {4} Dollar im Monat kommen (",
    "). Les millions de Stormi Steele, Logan Walter ou Katrina Dimiele sont le sommet visible d'une pyramide beaucoup plus large.":
        "). Die Millionen von Stormi Steele, Logan Walter oder Katrina Dimiele sind die sichtbare Spitze einer sehr viel breiteren Pyramide.",
    "🔮 Ce qui s'annonce ensuite": "🔮 Was als Nächstes kommt",
    "Le rythme d'expansion ne ralentit pas : après la vague européenne de juin {0}, TikTok Shop teste déjà des abonnements payants qui rappellent le modèle Amazon Prime (":
        "Das Tempo lässt nicht nach: Nach der europäischen Welle im Juni {0} testet TikTok Shop bereits kostenpflichtige Abos, die stark an Amazon Prime erinnern (",
    "), et des enseignes historiques comme Ulta Beauty ont rejoint la plateforme aux États-Unis en misant sur sa capacité à transformer la découverte en achat (":
        "), und altgediente Händler wie Ulta Beauty sind in den USA auf die Plattform gekommen — im Vertrauen darauf, dass sie Entdecken in Kaufen verwandelt (",
    "❓ Questions fréquentes": "❓ Häufige Fragen",
    "Qu'est-ce que TikTok Shop ?": "Was ist TikTok Shop?",
    "TikTok Shop est la fonctionnalité e-commerce intégrée à TikTok qui permet d'acheter des produits directement depuis l'application, via des vidéos courtes, des lives shopping ou une vitrine boutique. Lancée en {0}, elle est disponible mi-{1} dans une vingtaine de pays dont les États-Unis, le Royaume-Uni, la France, l'Allemagne, l'Espagne, l'Italie, l'Irlande, l'Indonésie, la Thaïlande, le Vietnam, la Malaisie, les Philippines, Singapour, le Japon, le Mexique et le Brésil.":
        "TikTok Shop ist die in TikTok eingebaute Verkaufsfunktion: Man kauft Produkte direkt in der App, über kurze Videos, Live-Shopping oder eine Shop-Seite. {0} gestartet, ist sie Mitte {1} in rund zwanzig Ländern verfügbar, darunter die USA, das Vereinigte Königreich, Frankreich, Deutschland, Spanien, Italien, Irland, Indonesien, Thailand, Vietnam, Malaysia, die Philippinen, Singapur, Japan, Mexiko und Brasilien.",
    "Peut-on vraiment gagner de l'argent avec TikTok Shop ?": "Kann man mit TikTok Shop wirklich Geld verdienen?",
    "Oui : les créateurs peuvent toucher des commissions d'affiliation en recommandant des produits, et les vendeurs peuvent gérer leur propre boutique. Certains créateurs comme Stormi Steele (Canvas Beauty) ou Logan Walter sont devenus millionnaires grâce à TikTok Shop. Mais la réalité reste à deux vitesses : le créateur médian gagne environ {0} dollars par mois, et seule une minorité de top créateurs atteint des revenus à sept chiffres.":
        "Ja: Creators können Affiliate-Provisionen verdienen, indem sie Produkte empfehlen, und Verkäufer können einen eigenen Shop führen. Manche Creators wie Stormi Steele (Canvas Beauty) oder Logan Walter sind über TikTok Shop Millionäre geworden. Aber die Wirklichkeit bleibt zweigeteilt: Der mittlere Creator verdient rund {0} Dollar im Monat, und nur eine kleine Minderheit erreicht siebenstellige Einnahmen.",
    "Dans quels pays TikTok Shop est-il disponible ?": "In welchen Ländern gibt es TikTok Shop?",
    "Mi-{0}, TikTok Shop est actif dans une vingtaine de marchés : aux Amériques (États-Unis, Mexique, Brésil), en Europe (Royaume-Uni, France, Allemagne, Espagne, Italie, Irlande, et depuis juin {1} l'Autriche, la Belgique, les Pays-Bas et la Pologne), et en Asie-Pacifique (Indonésie, Thaïlande, Vietnam, Malaisie, Philippines, Singapour, Japon). L'Australie et les pays du Golfe n'ont pas encore de lancement officiel.":
        "Mitte {0} läuft TikTok Shop in rund zwanzig Märkten: in Amerika (USA, Mexiko, Brasilien), in Europa (Vereinigtes Königreich, Frankreich, Deutschland, Spanien, Italien, Irland und seit Juni {1} Österreich, Belgien, die Niederlande und Polen) sowie in Asien-Pazifik (Indonesien, Thailand, Vietnam, Malaysia, Philippinen, Singapur, Japan). Für Australien und die Golfstaaten gibt es noch keinen offiziellen Start.",
    "Vous voulez percer sur TikTok Shop ?": "Willst du auf TikTok Shop durchstarten?",
    "Utilisez Qeerah pour analyser vos vidéos et copier ce qui fonctionne vraiment chez les créateurs qui cartonnent.":
        "Nutz Qeerah, um deine Videos zu analysieren und das nachzubauen, was bei den erfolgreichen Creators wirklich funktioniert.",
    "Analyser mes vidéos →": "Meine Videos analysieren →",
    "📚 Sources": "📚 Quellen",
    "interview vidéo, TikTok Shop Millionaire": "Videointerview, TikTok Shop Millionaire",
    "TikTok Shop Millionaire — ${0}M in {1} Years Selling Fashion On Livestreams (interview vidéo)":
        "TikTok Shop Millionaire — ${0}M in {1} Years Selling Fashion On Livestreams (Videointerview)",
}

T_BLOG_EXPANSION["es"] = {
    "TikTok Shop : c'est quoi et peut-on gagner de l'argent avec ? - Qeerah":
        "TikTok Shop: qué es y si se puede ganar dinero con ello - Qeerah",
    "TikTok Shop, c'est quoi et comment ça marche ? Peut-on vraiment gagner de l'argent avec ? Pays disponibles, chiffres de GMV et créateurs devenus millionnaires, avec sources vérifiées.":
        "Qué es TikTok Shop y cómo funciona. ¿De verdad se puede ganar dinero? Países disponibles, cifras de GMV y creadores que se hicieron millonarios, con fuentes verificadas.",
    "TikTok Shop : c'est quoi et peut-on gagner de l'argent avec ?":
        "TikTok Shop: qué es y si se puede ganar dinero con ello",
    "Ce qu'est TikTok Shop, comment ça marche, dans quels pays c'est disponible, et si on peut vraiment en vivre. Chiffres et créateurs millionnaires, sources à l'appui.":
        "Qué es TikTok Shop, cómo funciona, en qué países está disponible y si se puede vivir de ello. Cifras y creadores millonarios, con fuentes.",
    "← Retour au blog": "← Volver al blog",
    "💡 GUIDE TIKTOK SHOP": "💡 GUÍA DE TIKTOK SHOP",
    "TikTok Shop : c'est quoi, et peut-on vraiment gagner de l'argent avec ?":
        "TikTok Shop: qué es y si de verdad se puede ganar dinero con ello",
    "📅 Juillet {0}": "📅 Julio de {0}",
    "👤 Par l'équipe Qeerah": "👤 Por el equipo de Qeerah",
    "⏱️ {0} min de lecture": "⏱️ {0} min de lectura",
    "🇬🇧 Read in English": "🇬🇧 Read in English",
    "🔎 En bref :": "🔎 En resumen:",
    "TikTok Shop est la fonctionnalité e-commerce intégrée à TikTok qui permet d'acheter directement depuis l'app, via vidéos, lives ou vitrine boutique. Lancée en {0}, elle est aujourd'hui disponible dans une vingtaine de pays et a généré {1} milliards de dollars de ventes en {2}.":
        "TikTok Shop es la función de comercio integrada en TikTok que permite comprar directamente desde la app, a través de vídeos, directos o un escaparate de tienda. Lanzada en {0}, hoy está disponible en una veintena de países y generó {1} mil millones de dólares en ventas en {2}.",
    "Oui, on peut gagner de l'argent avec": "Sí, se puede ganar dinero con ello",
    "— en tant que créateur affilié (commissions) ou en tant que vendeur — mais la réalité est à deux vitesses : le créateur médian touche environ {0} $/mois, quand une minorité de top créateurs ou marques génèrent plusieurs millions.":
        "—como creador afiliado (comisiones) o como vendedor—, pero la realidad va a dos velocidades: el creador mediano ingresa unos {0} $ al mes, mientras que una minoría de creadores y marcas top genera varios millones.",
    "En un peu moins de quatre ans, TikTok Shop est passé d'un test discret en Asie du Sud-Est à l'une des plus grosses machines de social commerce au monde. Voici, chiffres et sources à l'appui, ce qu'est réellement TikTok Shop, comment ça fonctionne, dans quels pays c'est disponible, et qui sont les créateurs américains qui en ont déjà fait des fortunes.":
        "En poco menos de cuatro años, TikTok Shop pasó de ser una prueba discreta en el Sudeste Asiático a una de las mayores máquinas de comercio social del mundo. Aquí tienes, con cifras y fuentes, qué es realmente TikTok Shop, cómo funciona, en qué países está disponible y quiénes son los creadores estadounidenses que ya han hecho fortunas con ello.",
    "📊 Les chiffres qui résument l'explosion": "📊 Las cifras que resumen la explosión",
    "Le GMV (volume de marchandises vendues) mondial de TikTok Shop a atteint":
        "El GMV (volumen de mercancía vendida) mundial de TikTok Shop alcanzó",
    "{0} milliards de dollars en {1}": "{0} mil millones de dólares en {1}",
    ", en hausse de {0} % sur un an, réparti sur une quinzaine de marchés actifs cette année-là (":
        ", un {0} % más que el año anterior, repartido entre la quincena de mercados activos ese año (",
    "). Pour donner une idée de la vitesse : il a fallu {0} ans à Amazon pour atteindre {1} milliards de dollars de GMV annuel ; TikTok Shop est en passe de franchir ce seuil dès sa quatrième année pleine (":
        "). Para hacerse una idea de la velocidad: Amazon tardó {0} años en llegar a {1} mil millones de dólares de GMV anual; TikTok Shop va camino de cruzar ese umbral ya en su cuarto año completo (",
    "{0} Md$": "{0} MM$",
    "GMV mondial {0} (+{1}%)": "GMV mundial {0} (+{1} %)",
    "GMV mondial projeté {0}": "GMV mundial previsto {0}",
    "GMV USA {0} (+{1}%)": "GMV EE. UU. {0} (+{1} %)",
    "GMV Asie du Sud-Est {0}": "GMV Sudeste Asiático {0}",
    "Sources :": "Fuentes:",
    "Aux États-Unis, TikTok Shop captait déjà": "En Estados Unidos, TikTok Shop ya se llevaba",
    "{0} % de toutes les ventes de social commerce en {1}": "el {0} % de todas las ventas de comercio social en {1}",
    "). Certaines projections à long terme évoquent même une plateforme capable de peser près de {0} milliards de dollars de ventes d'ici {1}, ce qui en ferait un top {2} mondial du commerce en ligne derrière Amazon (":
        "). Algunas previsiones a largo plazo hablan incluso de una plataforma capaz de mover cerca de {0} mil millones de dólares en ventas para {1}, lo que la situaría entre los {2} primeros del comercio online mundial, por detrás de Amazon (",
    "🗓️ La timeline de l'expansion internationale": "🗓️ La cronología de la expansión internacional",
    "TikTok Shop n'a pas explosé partout en même temps. Son ouverture s'est faite marché par marché, sur un rythme qui s'est nettement accéléré depuis {0}.":
        "TikTok Shop no explotó en todas partes a la vez. Se abrió mercado a mercado, a un ritmo que se ha acelerado claramente desde {0}.",
    "Premiers tests d'e-commerce intégré, dont un partenariat pilote avec Shopify qui ne prendra finalement pas (":
        "Primeras pruebas de comercio integrado, incluida una alianza piloto con Shopify que al final no cuajó (",
    "{0} avril {1} —": "{0} de abril de {1} —",
    "Lancement officiel du e-commerce transfrontalier dans quatre pays d'Asie du Sud-Est : Thaïlande, Vietnam, Malaisie et Philippines (":
        "Lanzamiento oficial del comercio transfronterizo en cuatro países del Sudeste Asiático: Tailandia, Vietnam, Malasia y Filipinas (",
    "Novembre {0} —": "Noviembre de {0} —",
    "Début des tests beta au Royaume-Uni, en parallèle de plusieurs marchés d'Asie du Sud-Est (":
        "Comienzan las pruebas beta en el Reino Unido, en paralelo a varios mercados del Sudeste Asiático (",
    "Fin {0} —": "Finales de {0} —",
    "TikTok Shop est actif dans six pays d'Asie (Chine, Indonésie compris) et au Royaume-Uni (":
        "TikTok Shop está activo en seis países de Asia (China e Indonesia incluidas) y en el Reino Unido (",
    "{0} septembre {1} —": "{0} de septiembre de {1} —",
    "Lancement officiel aux États-Unis, l'ouverture qui fera basculer TikTok Shop dans une autre dimension (":
        "Lanzamiento oficial en Estados Unidos, la apertura que lleva a TikTok Shop a otra escala (",
    "Consolidation en Asie du Sud-Est (Singapour, Japon) et premières ouvertures en Amérique latine, au Mexique et au Brésil.":
        "Consolidación en el Sudeste Asiático (Singapur, Japón) y primeras aperturas en América Latina, en México y Brasil.",
    "Vague européenne : France, Allemagne, Espagne, Italie, Irlande et Royaume-Uni s'établissent comme marchés matures.":
        "Ola europea: Francia, Alemania, España, Italia, Irlanda y el Reino Unido se consolidan como mercados maduros.",
    "{0} juin {1} —": "{0} de junio de {1} —",
    "L'Autriche, la Belgique, les Pays-Bas et la Pologne rejoignent l'Europe TikTok Shop, avec un nouvel outil « Sell Across Europe » qui permet à un vendeur de couvrir plusieurs pays européens avec une seule inscription (":
        "Austria, Bélgica, Países Bajos y Polonia se suman a la Europa de TikTok Shop, con una nueva herramienta «Sell Across Europe» que permite a un vendedor cubrir varios países europeos con un solo registro (",
    "🗺️ Les marchés ouverts aujourd'hui, région par région": "🗺️ Los mercados abiertos hoy, región por región",
    "Mi-{0}, TikTok Shop Seller Center est officiellement actif dans une vingtaine de marchés répartis sur trois continents (":
        "A mediados de {0}, TikTok Shop Seller Center está oficialmente activo en una veintena de mercados repartidos en tres continentes (",
    "🌎 Amériques": "🌎 América",
    "États-Unis": "Estados Unidos",
    "Mexique": "México",
    "Brésil": "Brasil",
    "🇪🇺 Europe": "🇪🇺 Europa",
    "Royaume-Uni": "Reino Unido",
    "France": "Francia",
    "Allemagne": "Alemania",
    "Espagne": "España",
    "Italie": "Italia",
    "Irlande": "Irlanda",
    "Autriche": "Austria",
    "(juin {0})": "(junio de {0})",
    "Belgique": "Bélgica",
    "Pays-Bas": "Países Bajos",
    "Pologne": "Polonia",
    "🌏 Asie-Pacifique": "🌏 Asia-Pacífico",
    "Indonésie": "Indonesia",
    "Thaïlande": "Tailandia",
    "Vietnam": "Vietnam",
    "Malaisie": "Malasia",
    "Philippines": "Filipinas",
    "Singapour": "Singapur",
    "Japon": "Japón",
    "Pas encore ouvert :": "Todavía sin abrir:",
    "l'Australie n'a toujours pas accès à TikTok Shop Seller Center mi-{0}, et malgré des rumeurs récurrentes, aucun lancement natif n'est confirmé dans le Golfe (Arabie saoudite, Émirats) à cette date (":
        "Australia sigue sin acceso a TikTok Shop Seller Center a mediados de {0} y, pese a los rumores recurrentes, no hay ningún lanzamiento propio confirmado en el Golfo (Arabia Saudí, Emiratos) en esa fecha (",
    "🇮🇩 L'Indonésie, nouveau rival direct des États-Unis": "🇮🇩 Indonesia, nuevo rival directo de Estados Unidos",
    "C'est l'un des faits les plus frappants de {0} : sur le premier semestre, l'": "Es uno de los datos más llamativos de {0}: en el primer semestre,",
    "Indonésie a dépassé les États-Unis": "Indonesia superó a Estados Unidos",
    "comme premier marché de TikTok Shop, avec {0} milliards de dollars de GMV contre {1} milliards pour les USA (":
        "como primer mercado de TikTok Shop, con {0} mil millones de dólares de GMV frente a {1} mil millones de EE. UU. (",
    "). Sur l'année {0} complète, les États-Unis reprennent la tête ({1} Md$ contre {2} Md$ pour l'Indonésie), mais l'Indonésie reste le deuxième marché mondial de la plateforme, et toute la région Asie du Sud-Est a doublé son GMV en un an pour atteindre {3} milliards de dollars (":
        "). En el conjunto de {0}, Estados Unidos recupera la delantera ({1} MM$ frente a {2} MM$ de Indonesia), pero Indonesia sigue siendo el segundo mercado mundial de la plataforma, y todo el Sudeste Asiático duplicó su GMV en un año hasta {3} mil millones de dólares (",
    "💰 Les créateurs américains devenus millionnaires grâce à TikTok Shop":
        "💰 Los creadores estadounidenses que se hicieron millonarios con TikTok Shop",
    "Derrière les chiffres macro, il y a des histoires individuelles très concrètes. Voici trois créateurs américains dont la réussite sur TikTok Shop est documentée dans la presse.":
        "Detrás de las cifras macro hay historias individuales muy concretas. Estos son tres creadores estadounidenses cuyos resultados en TikTok Shop están documentados en prensa.",
    "Stormi Steele — Canvas Beauty (Body Glaze)": "Stormi Steele — Canvas Beauty (Body Glaze)",
    "{0}M$": "{0} M$",
    "en un seul live ({0} juin {1})": "en un solo directo ({0} de junio de {1})",
    "en une journée (Black Friday)": "en un día (Black Friday)",
    "de ventes mensuelles visées": "de ventas mensuales como objetivo",
    "Fondatrice de Canvas Beauty et de sa gamme Body Glaze (huile de soin corporel), Stormi Steele est devenue la première créatrice à dépasser {0} million de dollars de ventes lors d'un seul live TikTok Shop, le {1} juin {2} (":
        "Fundadora de Canvas Beauty y de su línea Body Glaze (aceite corporal), Stormi Steele fue la primera creadora en superar {0} millón de dólares en ventas durante un solo directo de TikTok Shop, el {1} de junio de {2} (",
    "). Lors du Black Friday, sa marque a généré {0} millions de dollars de ventes en une journée, dont {1} millions via un « mega live » de {2} heures organisé depuis son entrepôt en Alabama (":
        "). En Black Friday, su marca generó {0} millones de dólares en ventas en un día, {1} millones de ellos en un «mega directo» de {2} horas desde su almacén de Alabama (",
    "). Canvas Beauty a depuis été désignée marque n°{0} en ventes sur TikTok Shop aux États-Unis, avec une trajectoire vers {1} millions de dollars de ventes mensuelles (":
        "). Canvas Beauty ha sido designada desde entonces marca n.º {0} en ventas en TikTok Shop en Estados Unidos, camino de {1} millones de dólares en ventas mensuales (",
    "Logan Walter — Beauté & self-care masculin": "Logan Walter — belleza y autocuidado masculino",
    "{0} ans": "{0} años",
    "au moment de devenir millionnaire": "al hacerse millonario",
    "pour atteindre ce statut": "para llegar ahí",
    "{0} chiffres": "{0} cifras",
    "de revenu mensuel": "de ingresos mensuales",
    "Logan Walter a quitté l'université à {0} ans pour se consacrer à TikTok Shop, où il s'est imposé comme l'un des rares hommes affiliés dans le créneau beauté/self-care, en vendant des marques comme Medicube ou Neutrogena. Sa première vidéo virale lui a fait gagner plus de {1} dollars en un mois ; deux ans après ses débuts, il touchait un revenu mensuel à sept chiffres (":
        "Logan Walter dejó la universidad a los {0} años para volcarse en TikTok Shop, donde se hizo un hueco como uno de los pocos hombres afiliados en el nicho de belleza y autocuidado, vendiendo marcas como Medicube o Neutrogena. Su primer vídeo viral le hizo ganar más de {1} dólares en un mes; dos años después de empezar, ingresaba siete cifras al mes (",
    "Katrina Dimiele — Mode en direct (try-on livestreams)": "Katrina Dimiele — moda en directo (try-on hauls)",
    "cumulés en {0} ans": "acumulados en {0} años",
    "heures de vente en direct": "horas de venta en directo",
    "Créatrice mode spécialisée dans les « try-on hauls » en direct, Katrina Dimiele a cumulé {0} millions de dollars de ventes en neuf ans via ses lives sur TikTok Shop et Facebook (":
        "Creadora de moda especializada en «try-on hauls» en directo, Katrina Dimiele acumula {0} millones de dólares en ventas en nueve años a través de sus directos en TikTok Shop y Facebook (",
    "). Son parcours illustre une réalité importante : la plupart des plus gros succès viennent de créateurs qui ont accumulé des milliers d'heures de pratique avant d'exploser, pas d'un coup de chance isolé.":
        "). Su recorrido enseña algo importante: la mayoría de los grandes éxitos vienen de creadores que acumularon miles de horas de práctica antes de despegar, no de un golpe de suerte aislado.",
    "🔑 À retenir :": "🔑 Para quedarse con esto:",
    "ces trois parcours partagent un point commun — le live shopping. C'est le format qui génère les pics de revenus les plus spectaculaires sur TikTok Shop, bien plus que les vidéos courtes seules.":
        "los tres recorridos comparten una cosa: el live shopping. Es el formato que genera los picos de ingresos más espectaculares en TikTok Shop, mucho más que los vídeos cortos por sí solos.",
    "📉 Et pour un créateur « normal » ?": "📉 ¿Y para un creador normal?",
    "Ces histoires sont réelles, mais elles ne représentent pas la moyenne. Selon les données de monétisation {0}, le créateur médian sur TikTok gagne environ {1} dollars par mois toutes sources confondues, tandis que les {2} % les plus performants combinent plusieurs revenus pour atteindre {3} à {4} dollars par mois (":
        "Estas historias son reales, pero no son la media. Según los datos de monetización de {0}, el creador mediano en TikTok gana unos {1} dólares al mes sumando todas las fuentes, mientras que el {2} % con mejores resultados combina varios ingresos para llegar a entre {3} y {4} dólares al mes (",
    "). Les millions de Stormi Steele, Logan Walter ou Katrina Dimiele sont le sommet visible d'une pyramide beaucoup plus large.":
        "). Los millones de Stormi Steele, Logan Walter o Katrina Dimiele son la punta visible de una pirámide mucho más ancha.",
    "🔮 Ce qui s'annonce ensuite": "🔮 Lo que viene después",
    "Le rythme d'expansion ne ralentit pas : après la vague européenne de juin {0}, TikTok Shop teste déjà des abonnements payants qui rappellent le modèle Amazon Prime (":
        "El ritmo de expansión no afloja: tras la ola europea de junio de {0}, TikTok Shop ya prueba suscripciones de pago que recuerdan al modelo de Amazon Prime (",
    "), et des enseignes historiques comme Ulta Beauty ont rejoint la plateforme aux États-Unis en misant sur sa capacité à transformer la découverte en achat (":
        "), y cadenas históricas como Ulta Beauty se han sumado a la plataforma en Estados Unidos apostando por su capacidad de convertir el descubrimiento en compra (",
    "❓ Questions fréquentes": "❓ Preguntas frecuentes",
    "Qu'est-ce que TikTok Shop ?": "¿Qué es TikTok Shop?",
    "TikTok Shop est la fonctionnalité e-commerce intégrée à TikTok qui permet d'acheter des produits directement depuis l'application, via des vidéos courtes, des lives shopping ou une vitrine boutique. Lancée en {0}, elle est disponible mi-{1} dans une vingtaine de pays dont les États-Unis, le Royaume-Uni, la France, l'Allemagne, l'Espagne, l'Italie, l'Irlande, l'Indonésie, la Thaïlande, le Vietnam, la Malaisie, les Philippines, Singapour, le Japon, le Mexique et le Brésil.":
        "TikTok Shop es la función de comercio integrada en TikTok que permite comprar productos directamente desde la aplicación, a través de vídeos cortos, directos de compras o un escaparate de tienda. Lanzada en {0}, a mediados de {1} está disponible en una veintena de países, entre ellos Estados Unidos, Reino Unido, Francia, Alemania, España, Italia, Irlanda, Indonesia, Tailandia, Vietnam, Malasia, Filipinas, Singapur, Japón, México y Brasil.",
    "Peut-on vraiment gagner de l'argent avec TikTok Shop ?": "¿De verdad se puede ganar dinero con TikTok Shop?",
    "Oui : les créateurs peuvent toucher des commissions d'affiliation en recommandant des produits, et les vendeurs peuvent gérer leur propre boutique. Certains créateurs comme Stormi Steele (Canvas Beauty) ou Logan Walter sont devenus millionnaires grâce à TikTok Shop. Mais la réalité reste à deux vitesses : le créateur médian gagne environ {0} dollars par mois, et seule une minorité de top créateurs atteint des revenus à sept chiffres.":
        "Sí: los creadores pueden cobrar comisiones de afiliación recomendando productos, y los vendedores pueden llevar su propia tienda. Algunos creadores como Stormi Steele (Canvas Beauty) o Logan Walter se han hecho millonarios con TikTok Shop. Pero la realidad sigue yendo a dos velocidades: el creador mediano gana unos {0} dólares al mes, y solo una minoría de creadores top llega a ingresos de siete cifras.",
    "Dans quels pays TikTok Shop est-il disponible ?": "¿En qué países está disponible TikTok Shop?",
    "Mi-{0}, TikTok Shop est actif dans une vingtaine de marchés : aux Amériques (États-Unis, Mexique, Brésil), en Europe (Royaume-Uni, France, Allemagne, Espagne, Italie, Irlande, et depuis juin {1} l'Autriche, la Belgique, les Pays-Bas et la Pologne), et en Asie-Pacifique (Indonésie, Thaïlande, Vietnam, Malaisie, Philippines, Singapour, Japon). L'Australie et les pays du Golfe n'ont pas encore de lancement officiel.":
        "A mediados de {0}, TikTok Shop está activo en una veintena de mercados: en América (Estados Unidos, México, Brasil), en Europa (Reino Unido, Francia, Alemania, España, Italia, Irlanda y, desde junio de {1}, Austria, Bélgica, Países Bajos y Polonia) y en Asia-Pacífico (Indonesia, Tailandia, Vietnam, Malasia, Filipinas, Singapur, Japón). Australia y los países del Golfo aún no tienen lanzamiento oficial.",
    "Vous voulez percer sur TikTok Shop ?": "¿Quieres despegar en TikTok Shop?",
    "Utilisez Qeerah pour analyser vos vidéos et copier ce qui fonctionne vraiment chez les créateurs qui cartonnent.":
        "Usa Qeerah para analizar tus vídeos y copiar lo que de verdad funciona en los creadores que arrasan.",
    "Analyser mes vidéos →": "Analizar mis vídeos →",
    "📚 Sources": "📚 Fuentes",
    "interview vidéo, TikTok Shop Millionaire": "entrevista en vídeo, TikTok Shop Millionaire",
    "TikTok Shop Millionaire — ${0}M in {1} Years Selling Fashion On Livestreams (interview vidéo)":
        "TikTok Shop Millionaire — ${0}M in {1} Years Selling Fashion On Livestreams (entrevista en vídeo)",
}

T_BLOG_EXPANSION["it"] = {
    "TikTok Shop : c'est quoi et peut-on gagner de l'argent avec ? - Qeerah":
        "TikTok Shop: cos'è e ci si può guadagnare? - Qeerah",
    "TikTok Shop, c'est quoi et comment ça marche ? Peut-on vraiment gagner de l'argent avec ? Pays disponibles, chiffres de GMV et créateurs devenus millionnaires, avec sources vérifiées.":
        "Cos'è TikTok Shop e come funziona. Ci si può davvero guadagnare? Paesi disponibili, numeri di GMV e creator diventati milionari, con fonti verificate.",
    "TikTok Shop : c'est quoi et peut-on gagner de l'argent avec ?": "TikTok Shop: cos'è e ci si può guadagnare?",
    "Ce qu'est TikTok Shop, comment ça marche, dans quels pays c'est disponible, et si on peut vraiment en vivre. Chiffres et créateurs millionnaires, sources à l'appui.":
        "Cos'è TikTok Shop, come funziona, in quali paesi è disponibile e se ci si può vivere. Numeri e creator milionari, con le fonti.",
    "← Retour au blog": "← Torna al blog",
    "💡 GUIDE TIKTOK SHOP": "💡 GUIDA A TIKTOK SHOP",
    "TikTok Shop : c'est quoi, et peut-on vraiment gagner de l'argent avec ?":
        "TikTok Shop: cos'è e ci si può davvero guadagnare?",
    "📅 Juillet {0}": "📅 Luglio {0}",
    "👤 Par l'équipe Qeerah": "👤 Dal team Qeerah",
    "⏱️ {0} min de lecture": "⏱️ {0} min di lettura",
    "🇬🇧 Read in English": "🇬🇧 Read in English",
    "🔎 En bref :": "🔎 In breve:",
    "TikTok Shop est la fonctionnalité e-commerce intégrée à TikTok qui permet d'acheter directement depuis l'app, via vidéos, lives ou vitrine boutique. Lancée en {0}, elle est aujourd'hui disponible dans une vingtaine de pays et a généré {1} milliards de dollars de ventes en {2}.":
        "TikTok Shop è la funzione di commercio integrata in TikTok che permette di comprare direttamente dall'app, tramite video, dirette o una vetrina negozio. Lanciata nel {0}, oggi è disponibile in una ventina di paesi e ha generato {1} miliardi di dollari di vendite nel {2}.",
    "Oui, on peut gagner de l'argent avec": "Sì, ci si può guadagnare",
    "— en tant que créateur affilié (commissions) ou en tant que vendeur — mais la réalité est à deux vitesses : le créateur médian touche environ {0} $/mois, quand une minorité de top créateurs ou marques génèrent plusieurs millions.":
        "— come creator affiliato (provvigioni) o come venditore — ma la realtà va a due velocità: il creator mediano incassa circa {0} $ al mese, mentre una minoranza di top creator e marchi genera diversi milioni.",
    "En un peu moins de quatre ans, TikTok Shop est passé d'un test discret en Asie du Sud-Est à l'une des plus grosses machines de social commerce au monde. Voici, chiffres et sources à l'appui, ce qu'est réellement TikTok Shop, comment ça fonctionne, dans quels pays c'est disponible, et qui sont les créateurs américains qui en ont déjà fait des fortunes.":
        "In poco meno di quattro anni TikTok Shop è passato da test silenzioso nel Sud-est asiatico a una delle più grandi macchine di social commerce al mondo. Ecco, numeri e fonti alla mano, cos'è davvero TikTok Shop, come funziona, in quali paesi è disponibile e chi sono i creator americani che ci hanno già fatto fortune.",
    "📊 Les chiffres qui résument l'explosion": "📊 I numeri che riassumono il boom",
    "Le GMV (volume de marchandises vendues) mondial de TikTok Shop a atteint":
        "Il GMV (volume di merce venduta) mondiale di TikTok Shop ha raggiunto",
    "{0} milliards de dollars en {1}": "{0} miliardi di dollari nel {1}",
    ", en hausse de {0} % sur un an, réparti sur une quinzaine de marchés actifs cette année-là (":
        ", in crescita del {0} % su base annua, distribuito sulla quindicina di mercati attivi quell'anno (",
    "). Pour donner une idée de la vitesse : il a fallu {0} ans à Amazon pour atteindre {1} milliards de dollars de GMV annuel ; TikTok Shop est en passe de franchir ce seuil dès sa quatrième année pleine (":
        "). Per dare un'idea della velocità: ad Amazon sono serviti {0} anni per arrivare a {1} miliardi di dollari di GMV annuo; TikTok Shop è sul punto di superare quella soglia già al quarto anno pieno (",
    "{0} Md$": "{0} mld $",
    "GMV mondial {0} (+{1}%)": "GMV mondiale {0} (+{1} %)",
    "GMV mondial projeté {0}": "GMV mondiale previsto {0}",
    "GMV USA {0} (+{1}%)": "GMV USA {0} (+{1} %)",
    "GMV Asie du Sud-Est {0}": "GMV Sud-est asiatico {0}",
    "Sources :": "Fonti:",
    "Aux États-Unis, TikTok Shop captait déjà": "Negli Stati Uniti TikTok Shop si prendeva già",
    "{0} % de toutes les ventes de social commerce en {1}": "il {0} % di tutte le vendite di social commerce nel {1}",
    "). Certaines projections à long terme évoquent même une plateforme capable de peser près de {0} milliards de dollars de ventes d'ici {1}, ce qui en ferait un top {2} mondial du commerce en ligne derrière Amazon (":
        "). Alcune proiezioni di lungo periodo parlano perfino di una piattaforma capace di valere quasi {0} miliardi di dollari di vendite entro il {1}, il che la metterebbe tra i primi {2} al mondo nel commercio online, dietro ad Amazon (",
    "🗓️ La timeline de l'expansion internationale": "🗓️ La cronologia dell'espansione internazionale",
    "TikTok Shop n'a pas explosé partout en même temps. Son ouverture s'est faite marché par marché, sur un rythme qui s'est nettement accéléré depuis {0}.":
        "TikTok Shop non è esploso ovunque nello stesso momento. L'apertura è avvenuta mercato per mercato, a un ritmo che dal {0} si è chiaramente accelerato.",
    "Premiers tests d'e-commerce intégré, dont un partenariat pilote avec Shopify qui ne prendra finalement pas (":
        "Primi test di commercio integrato, inclusa una partnership pilota con Shopify che alla fine non decolla (",
    "{0} avril {1} —": "{0} aprile {1} —",
    "Lancement officiel du e-commerce transfrontalier dans quatre pays d'Asie du Sud-Est : Thaïlande, Vietnam, Malaisie et Philippines (":
        "Lancio ufficiale del commercio transfrontaliero in quattro paesi del Sud-est asiatico: Thailandia, Vietnam, Malaysia e Filippine (",
    "Novembre {0} —": "Novembre {0} —",
    "Début des tests beta au Royaume-Uni, en parallèle de plusieurs marchés d'Asie du Sud-Est (":
        "Iniziano i test beta nel Regno Unito, in parallelo a diversi mercati del Sud-est asiatico (",
    "Fin {0} —": "Fine {0} —",
    "TikTok Shop est actif dans six pays d'Asie (Chine, Indonésie compris) et au Royaume-Uni (":
        "TikTok Shop è attivo in sei paesi asiatici (Cina e Indonesia comprese) e nel Regno Unito (",
    "{0} septembre {1} —": "{0} settembre {1} —",
    "Lancement officiel aux États-Unis, l'ouverture qui fera basculer TikTok Shop dans une autre dimension (":
        "Lancio ufficiale negli Stati Uniti, l'apertura che porta TikTok Shop su un altro piano (",
    "Consolidation en Asie du Sud-Est (Singapour, Japon) et premières ouvertures en Amérique latine, au Mexique et au Brésil.":
        "Consolidamento nel Sud-est asiatico (Singapore, Giappone) e prime aperture in America Latina, in Messico e Brasile.",
    "Vague européenne : France, Allemagne, Espagne, Italie, Irlande et Royaume-Uni s'établissent comme marchés matures.":
        "Ondata europea: Francia, Germania, Spagna, Italia, Irlanda e Regno Unito si affermano come mercati maturi.",
    "{0} juin {1} —": "{0} giugno {1} —",
    "L'Autriche, la Belgique, les Pays-Bas et la Pologne rejoignent l'Europe TikTok Shop, avec un nouvel outil « Sell Across Europe » qui permet à un vendeur de couvrir plusieurs pays européens avec une seule inscription (":
        "Austria, Belgio, Paesi Bassi e Polonia entrano nell'Europa di TikTok Shop, con il nuovo strumento «Sell Across Europe» che permette a un venditore di coprire più paesi europei con una sola iscrizione (",
    "🗺️ Les marchés ouverts aujourd'hui, région par région": "🗺️ I mercati aperti oggi, regione per regione",
    "Mi-{0}, TikTok Shop Seller Center est officiellement actif dans une vingtaine de marchés répartis sur trois continents (":
        "A metà {0} il TikTok Shop Seller Center è ufficialmente attivo in una ventina di mercati su tre continenti (",
    "🌎 Amériques": "🌎 Americhe",
    "États-Unis": "Stati Uniti",
    "Mexique": "Messico",
    "Brésil": "Brasile",
    "🇪🇺 Europe": "🇪🇺 Europa",
    "Royaume-Uni": "Regno Unito",
    "France": "Francia",
    "Allemagne": "Germania",
    "Espagne": "Spagna",
    "Italie": "Italia",
    "Irlande": "Irlanda",
    "Autriche": "Austria",
    "(juin {0})": "(giugno {0})",
    "Belgique": "Belgio",
    "Pays-Bas": "Paesi Bassi",
    "Pologne": "Polonia",
    "🌏 Asie-Pacifique": "🌏 Asia-Pacifico",
    "Indonésie": "Indonesia",
    "Thaïlande": "Thailandia",
    "Vietnam": "Vietnam",
    "Malaisie": "Malaysia",
    "Philippines": "Filippine",
    "Singapour": "Singapore",
    "Japon": "Giappone",
    "Pas encore ouvert :": "Non ancora aperto:",
    "l'Australie n'a toujours pas accès à TikTok Shop Seller Center mi-{0}, et malgré des rumeurs récurrentes, aucun lancement natif n'est confirmé dans le Golfe (Arabie saoudite, Émirats) à cette date (":
        "l'Australia a metà {0} non ha ancora accesso al TikTok Shop Seller Center e, nonostante le voci ricorrenti, a quella data non è confermato alcun lancio nativo nel Golfo (Arabia Saudita, Emirati) (",
    "🇮🇩 L'Indonésie, nouveau rival direct des États-Unis": "🇮🇩 L'Indonesia, nuova rivale diretta degli Stati Uniti",
    "C'est l'un des faits les plus frappants de {0} : sur le premier semestre, l'": "È uno dei dati più sorprendenti del {0}: nel primo semestre",
    "Indonésie a dépassé les États-Unis": "l'Indonesia ha superato gli Stati Uniti",
    "comme premier marché de TikTok Shop, avec {0} milliards de dollars de GMV contre {1} milliards pour les USA (":
        "come primo mercato di TikTok Shop, con {0} miliardi di dollari di GMV contro i {1} miliardi degli USA (",
    "). Sur l'année {0} complète, les États-Unis reprennent la tête ({1} Md$ contre {2} Md$ pour l'Indonésie), mais l'Indonésie reste le deuxième marché mondial de la plateforme, et toute la région Asie du Sud-Est a doublé son GMV en un an pour atteindre {3} milliards de dollars (":
        "). Sull'intero {0} gli Stati Uniti si riprendono la testa ({1} mld $ contro {2} mld $ dell'Indonesia), ma l'Indonesia resta il secondo mercato mondiale della piattaforma, e tutto il Sud-est asiatico ha raddoppiato il GMV in un anno arrivando a {3} miliardi di dollari (",
    "💰 Les créateurs américains devenus millionnaires grâce à TikTok Shop":
        "💰 I creator americani diventati milionari con TikTok Shop",
    "Derrière les chiffres macro, il y a des histoires individuelles très concrètes. Voici trois créateurs américains dont la réussite sur TikTok Shop est documentée dans la presse.":
        "Dietro ai numeri grandi ci sono storie individuali molto concrete. Ecco tre creator americani i cui risultati su TikTok Shop sono documentati dalla stampa.",
    "Stormi Steele — Canvas Beauty (Body Glaze)": "Stormi Steele — Canvas Beauty (Body Glaze)",
    "{0}M$": "{0} mln $",
    "en un seul live ({0} juin {1})": "in una sola diretta ({0} giugno {1})",
    "en une journée (Black Friday)": "in un giorno (Black Friday)",
    "de ventes mensuelles visées": "di vendite mensili come obiettivo",
    "Fondatrice de Canvas Beauty et de sa gamme Body Glaze (huile de soin corporel), Stormi Steele est devenue la première créatrice à dépasser {0} million de dollars de ventes lors d'un seul live TikTok Shop, le {1} juin {2} (":
        "Fondatrice di Canvas Beauty e della linea Body Glaze (olio corpo), Stormi Steele è stata la prima creator a superare {0} milione di dollari di vendite in una sola diretta TikTok Shop, il {1} giugno {2} (",
    "). Lors du Black Friday, sa marque a généré {0} millions de dollars de ventes en une journée, dont {1} millions via un « mega live » de {2} heures organisé depuis son entrepôt en Alabama (":
        "). Al Black Friday il suo marchio ha generato {0} milioni di dollari di vendite in un giorno, {1} milioni dei quali con un «mega live» di {2} ore dal suo magazzino in Alabama (",
    "). Canvas Beauty a depuis été désignée marque n°{0} en ventes sur TikTok Shop aux États-Unis, avec une trajectoire vers {1} millions de dollars de ventes mensuelles (":
        "). Da allora Canvas Beauty è indicato come marchio n. {0} per vendite su TikTok Shop negli Stati Uniti, con una traiettoria verso {1} milioni di dollari di vendite mensili (",
    "Logan Walter — Beauté & self-care masculin": "Logan Walter — bellezza e cura di sé al maschile",
    "{0} ans": "{0} anni",
    "au moment de devenir millionnaire": "quando è diventato milionario",
    "pour atteindre ce statut": "per arrivarci",
    "{0} chiffres": "{0} cifre",
    "de revenu mensuel": "di reddito mensile",
    "Logan Walter a quitté l'université à {0} ans pour se consacrer à TikTok Shop, où il s'est imposé comme l'un des rares hommes affiliés dans le créneau beauté/self-care, en vendant des marques comme Medicube ou Neutrogena. Sa première vidéo virale lui a fait gagner plus de {1} dollars en un mois ; deux ans après ses débuts, il touchait un revenu mensuel à sept chiffres (":
        "Logan Walter ha lasciato l'università a {0} anni per dedicarsi a TikTok Shop, dove si è imposto come uno dei pochi affiliati uomini nel settore bellezza e cura di sé, vendendo marchi come Medicube o Neutrogena. Il suo primo video virale gli ha fatto guadagnare oltre {1} dollari in un mese; due anni dopo l'inizio, incassava un reddito mensile a sette cifre (",
    "Katrina Dimiele — Mode en direct (try-on livestreams)": "Katrina Dimiele — moda in diretta (try-on haul)",
    "cumulés en {0} ans": "accumulati in {0} anni",
    "heures de vente en direct": "ore di vendita in diretta",
    "Créatrice mode spécialisée dans les « try-on hauls » en direct, Katrina Dimiele a cumulé {0} millions de dollars de ventes en neuf ans via ses lives sur TikTok Shop et Facebook (":
        "Creator di moda specializzata nei «try-on haul» in diretta, Katrina Dimiele ha accumulato {0} milioni di dollari di vendite in nove anni con le sue dirette su TikTok Shop e Facebook (",
    "). Son parcours illustre une réalité importante : la plupart des plus gros succès viennent de créateurs qui ont accumulé des milliers d'heures de pratique avant d'exploser, pas d'un coup de chance isolé.":
        "). Il suo percorso dice una cosa importante: i successi più grossi vengono quasi sempre da creator che hanno accumulato migliaia di ore di pratica prima di esplodere, non da un colpo di fortuna isolato.",
    "🔑 À retenir :": "🔑 Da tenere a mente:",
    "ces trois parcours partagent un point commun — le live shopping. C'est le format qui génère les pics de revenus les plus spectaculaires sur TikTok Shop, bien plus que les vidéos courtes seules.":
        "questi tre percorsi hanno una cosa in comune: il live shopping. È il formato che genera i picchi di guadagno più clamorosi su TikTok Shop, molto più dei soli video brevi.",
    "📉 Et pour un créateur « normal » ?": "📉 E per un creator normale?",
    "Ces histoires sont réelles, mais elles ne représentent pas la moyenne. Selon les données de monétisation {0}, le créateur médian sur TikTok gagne environ {1} dollars par mois toutes sources confondues, tandis que les {2} % les plus performants combinent plusieurs revenus pour atteindre {3} à {4} dollars par mois (":
        "Queste storie sono vere, ma non sono la media. Secondo i dati di monetizzazione del {0}, il creator mediano su TikTok guadagna circa {1} dollari al mese sommando tutte le fonti, mentre il {2} % più performante combina più entrate arrivando a {3}-{4} dollari al mese (",
    "). Les millions de Stormi Steele, Logan Walter ou Katrina Dimiele sont le sommet visible d'une pyramide beaucoup plus large.":
        "). I milioni di Stormi Steele, Logan Walter o Katrina Dimiele sono la punta visibile di una piramide molto più larga.",
    "🔮 Ce qui s'annonce ensuite": "🔮 Cosa arriva adesso",
    "Le rythme d'expansion ne ralentit pas : après la vague européenne de juin {0}, TikTok Shop teste déjà des abonnements payants qui rappellent le modèle Amazon Prime (":
        "Il ritmo dell'espansione non rallenta: dopo l'ondata europea di giugno {0}, TikTok Shop sta già testando abbonamenti a pagamento che ricordano il modello Amazon Prime (",
    "), et des enseignes historiques comme Ulta Beauty ont rejoint la plateforme aux États-Unis en misant sur sa capacité à transformer la découverte en achat (":
        "), e catene storiche come Ulta Beauty sono entrate sulla piattaforma negli Stati Uniti, scommettendo sulla sua capacità di trasformare la scoperta in acquisto (",
    "❓ Questions fréquentes": "❓ Domande frequenti",
    "Qu'est-ce que TikTok Shop ?": "Cos'è TikTok Shop?",
    "TikTok Shop est la fonctionnalité e-commerce intégrée à TikTok qui permet d'acheter des produits directement depuis l'application, via des vidéos courtes, des lives shopping ou une vitrine boutique. Lancée en {0}, elle est disponible mi-{1} dans une vingtaine de pays dont les États-Unis, le Royaume-Uni, la France, l'Allemagne, l'Espagne, l'Italie, l'Irlande, l'Indonésie, la Thaïlande, le Vietnam, la Malaisie, les Philippines, Singapour, le Japon, le Mexique et le Brésil.":
        "TikTok Shop è la funzione di commercio integrata in TikTok che permette di comprare prodotti direttamente dall'app, tramite video brevi, dirette shopping o una vetrina negozio. Lanciata nel {0}, a metà {1} è disponibile in una ventina di paesi tra cui Stati Uniti, Regno Unito, Francia, Germania, Spagna, Italia, Irlanda, Indonesia, Thailandia, Vietnam, Malaysia, Filippine, Singapore, Giappone, Messico e Brasile.",
    "Peut-on vraiment gagner de l'argent avec TikTok Shop ?": "Si può davvero guadagnare con TikTok Shop?",
    "Oui : les créateurs peuvent toucher des commissions d'affiliation en recommandant des produits, et les vendeurs peuvent gérer leur propre boutique. Certains créateurs comme Stormi Steele (Canvas Beauty) ou Logan Walter sont devenus millionnaires grâce à TikTok Shop. Mais la réalité reste à deux vitesses : le créateur médian gagne environ {0} dollars par mois, et seule une minorité de top créateurs atteint des revenus à sept chiffres.":
        "Sì: i creator possono incassare provvigioni di affiliazione consigliando prodotti, e i venditori possono gestire un proprio negozio. Alcuni creator come Stormi Steele (Canvas Beauty) o Logan Walter sono diventati milionari con TikTok Shop. Ma la realtà resta a due velocità: il creator mediano guadagna circa {0} dollari al mese, e solo una minoranza di top creator arriva a entrate a sette cifre.",
    "Dans quels pays TikTok Shop est-il disponible ?": "In quali paesi è disponibile TikTok Shop?",
    "Mi-{0}, TikTok Shop est actif dans une vingtaine de marchés : aux Amériques (États-Unis, Mexique, Brésil), en Europe (Royaume-Uni, France, Allemagne, Espagne, Italie, Irlande, et depuis juin {1} l'Autriche, la Belgique, les Pays-Bas et la Pologne), et en Asie-Pacifique (Indonésie, Thaïlande, Vietnam, Malaisie, Philippines, Singapour, Japon). L'Australie et les pays du Golfe n'ont pas encore de lancement officiel.":
        "A metà {0} TikTok Shop è attivo in una ventina di mercati: nelle Americhe (Stati Uniti, Messico, Brasile), in Europa (Regno Unito, Francia, Germania, Spagna, Italia, Irlanda e, da giugno {1}, Austria, Belgio, Paesi Bassi e Polonia) e in Asia-Pacifico (Indonesia, Thailandia, Vietnam, Malaysia, Filippine, Singapore, Giappone). Australia e paesi del Golfo non hanno ancora un lancio ufficiale.",
    "Vous voulez percer sur TikTok Shop ?": "Vuoi sfondare su TikTok Shop?",
    "Utilisez Qeerah pour analyser vos vidéos et copier ce qui fonctionne vraiment chez les créateurs qui cartonnent.":
        "Usa Qeerah per analizzare i tuoi video e rifare ciò che funziona davvero nei creator che stanno spaccando.",
    "Analyser mes vidéos →": "Analizza i miei video →",
    "📚 Sources": "📚 Fonti",
    "interview vidéo, TikTok Shop Millionaire": "intervista video, TikTok Shop Millionaire",
    "TikTok Shop Millionaire — ${0}M in {1} Years Selling Fashion On Livestreams (interview vidéo)":
        "TikTok Shop Millionaire — ${0}M in {1} Years Selling Fashion On Livestreams (intervista video)",
}

T_BLOG_EXPANSION["pt-br"] = {
    "TikTok Shop : c'est quoi et peut-on gagner de l'argent avec ? - Qeerah":
        "TikTok Shop: o que é e dá para ganhar dinheiro com isso? - Qeerah",
    "TikTok Shop, c'est quoi et comment ça marche ? Peut-on vraiment gagner de l'argent avec ? Pays disponibles, chiffres de GMV et créateurs devenus millionnaires, avec sources vérifiées.":
        "O que é o TikTok Shop e como funciona. Dá mesmo para ganhar dinheiro? Países disponíveis, números de GMV e criadores que ficaram milionários, com fontes verificadas.",
    "TikTok Shop : c'est quoi et peut-on gagner de l'argent avec ?": "TikTok Shop: o que é e dá para ganhar dinheiro com isso?",
    "Ce qu'est TikTok Shop, comment ça marche, dans quels pays c'est disponible, et si on peut vraiment en vivre. Chiffres et créateurs millionnaires, sources à l'appui.":
        "O que é o TikTok Shop, como funciona, em quais países está disponível e se dá para viver disso. Números e criadores milionários, com fontes.",
    "← Retour au blog": "← Voltar ao blog",
    "💡 GUIDE TIKTOK SHOP": "💡 GUIA DO TIKTOK SHOP",
    "TikTok Shop : c'est quoi, et peut-on vraiment gagner de l'argent avec ?":
        "TikTok Shop: o que é e dá mesmo para ganhar dinheiro com isso?",
    "📅 Juillet {0}": "📅 Julho de {0}",
    "👤 Par l'équipe Qeerah": "👤 Pelo time da Qeerah",
    "⏱️ {0} min de lecture": "⏱️ {0} min de leitura",
    "🇬🇧 Read in English": "🇬🇧 Read in English",
    "🔎 En bref :": "🔎 Resumindo:",
    "TikTok Shop est la fonctionnalité e-commerce intégrée à TikTok qui permet d'acheter directement depuis l'app, via vidéos, lives ou vitrine boutique. Lancée en {0}, elle est aujourd'hui disponible dans une vingtaine de pays et a généré {1} milliards de dollars de ventes en {2}.":
        "O TikTok Shop é a parte de comércio embutida no TikTok, que permite comprar direto no app por vídeos, lives ou uma vitrine de loja. Lançado em {0}, hoje está disponível em cerca de vinte países e gerou {1} bilhões de dólares em vendas em {2}.",
    "Oui, on peut gagner de l'argent avec": "Sim, dá para ganhar dinheiro com isso",
    "— en tant que créateur affilié (commissions) ou en tant que vendeur — mais la réalité est à deux vitesses : le créateur médian touche environ {0} $/mois, quand une minorité de top créateurs ou marques génèrent plusieurs millions.":
        "— como criador afiliado (comissões) ou como vendedor —, mas a realidade tem duas velocidades: o criador mediano recebe cerca de {0} $/mês, enquanto uma minoria de criadores e marcas de topo fatura vários milhões.",
    "En un peu moins de quatre ans, TikTok Shop est passé d'un test discret en Asie du Sud-Est à l'une des plus grosses machines de social commerce au monde. Voici, chiffres et sources à l'appui, ce qu'est réellement TikTok Shop, comment ça fonctionne, dans quels pays c'est disponible, et qui sont les créateurs américains qui en ont déjà fait des fortunes.":
        "Em pouco menos de quatro anos, o TikTok Shop saiu de um teste discreto no Sudeste Asiático para virar uma das maiores máquinas de comércio social do mundo. Aqui vai, com números e fontes, o que é de fato o TikTok Shop, como funciona, em quais países está disponível e quem são os criadores americanos que já fizeram fortuna com ele.",
    "📊 Les chiffres qui résument l'explosion": "📊 Os números que resumem a explosão",
    "Le GMV (volume de marchandises vendues) mondial de TikTok Shop a atteint":
        "O GMV (volume de mercadoria vendida) mundial do TikTok Shop chegou a",
    "{0} milliards de dollars en {1}": "{0} bilhões de dólares em {1}",
    ", en hausse de {0} % sur un an, réparti sur une quinzaine de marchés actifs cette année-là (":
        ", alta de {0} % em um ano, espalhado pelos cerca de quinze mercados ativos naquele ano (",
    "). Pour donner une idée de la vitesse : il a fallu {0} ans à Amazon pour atteindre {1} milliards de dollars de GMV annuel ; TikTok Shop est en passe de franchir ce seuil dès sa quatrième année pleine (":
        "). Para dar noção da velocidade: a Amazon levou {0} anos para chegar a {1} bilhões de dólares de GMV anual; o TikTok Shop está prestes a cruzar essa marca já no quarto ano completo (",
    "{0} Md$": "{0} bi $",
    "GMV mondial {0} (+{1}%)": "GMV mundial {0} (+{1} %)",
    "GMV mondial projeté {0}": "GMV mundial projetado {0}",
    "GMV USA {0} (+{1}%)": "GMV EUA {0} (+{1} %)",
    "GMV Asie du Sud-Est {0}": "GMV Sudeste Asiático {0}",
    "Sources :": "Fontes:",
    "Aux États-Unis, TikTok Shop captait déjà": "Nos Estados Unidos, o TikTok Shop já ficava com",
    "{0} % de toutes les ventes de social commerce en {1}": "{0} % de todas as vendas de comércio social em {1}",
    "). Certaines projections à long terme évoquent même une plateforme capable de peser près de {0} milliards de dollars de ventes d'ici {1}, ce qui en ferait un top {2} mondial du commerce en ligne derrière Amazon (":
        "). Algumas projeções de longo prazo falam até de uma plataforma capaz de movimentar perto de {0} bilhões de dólares em vendas até {1}, o que a colocaria entre os {2} maiores do comércio online do mundo, atrás da Amazon (",
    "🗓️ La timeline de l'expansion internationale": "🗓️ A linha do tempo da expansão internacional",
    "TikTok Shop n'a pas explosé partout en même temps. Son ouverture s'est faite marché par marché, sur un rythme qui s'est nettement accéléré depuis {0}.":
        "O TikTok Shop não explodiu em todo lugar ao mesmo tempo. A abertura veio mercado por mercado, num ritmo que acelerou bastante desde {0}.",
    "Premiers tests d'e-commerce intégré, dont un partenariat pilote avec Shopify qui ne prendra finalement pas (":
        "Primeiros testes de comércio integrado, incluindo uma parceria piloto com a Shopify que no fim não vingou (",
    "{0} avril {1} —": "{0} de abril de {1} —",
    "Lancement officiel du e-commerce transfrontalier dans quatre pays d'Asie du Sud-Est : Thaïlande, Vietnam, Malaisie et Philippines (":
        "Lançamento oficial do comércio transfronteiriço em quatro países do Sudeste Asiático: Tailândia, Vietnã, Malásia e Filipinas (",
    "Novembre {0} —": "Novembro de {0} —",
    "Début des tests beta au Royaume-Uni, en parallèle de plusieurs marchés d'Asie du Sud-Est (":
        "Começam os testes beta no Reino Unido, em paralelo a vários mercados do Sudeste Asiático (",
    "Fin {0} —": "Fim de {0} —",
    "TikTok Shop est actif dans six pays d'Asie (Chine, Indonésie compris) et au Royaume-Uni (":
        "O TikTok Shop está ativo em seis países da Ásia (China e Indonésia incluídas) e no Reino Unido (",
    "{0} septembre {1} —": "{0} de setembro de {1} —",
    "Lancement officiel aux États-Unis, l'ouverture qui fera basculer TikTok Shop dans une autre dimension (":
        "Lançamento oficial nos Estados Unidos, a abertura que joga o TikTok Shop para outro patamar (",
    "Consolidation en Asie du Sud-Est (Singapour, Japon) et premières ouvertures en Amérique latine, au Mexique et au Brésil.":
        "Consolidação no Sudeste Asiático (Singapura, Japão) e primeiras aberturas na América Latina, no México e no Brasil.",
    "Vague européenne : France, Allemagne, Espagne, Italie, Irlande et Royaume-Uni s'établissent comme marchés matures.":
        "Onda europeia: França, Alemanha, Espanha, Itália, Irlanda e Reino Unido se firmam como mercados maduros.",
    "{0} juin {1} —": "{0} de junho de {1} —",
    "L'Autriche, la Belgique, les Pays-Bas et la Pologne rejoignent l'Europe TikTok Shop, avec un nouvel outil « Sell Across Europe » qui permet à un vendeur de couvrir plusieurs pays européens avec une seule inscription (":
        "Áustria, Bélgica, Países Baixos e Polônia entram na Europa do TikTok Shop, com a nova ferramenta “Sell Across Europe”, que permite a um vendedor cobrir vários países europeus com um único cadastro (",
    "🗺️ Les marchés ouverts aujourd'hui, région par région": "🗺️ Os mercados abertos hoje, região por região",
    "Mi-{0}, TikTok Shop Seller Center est officiellement actif dans une vingtaine de marchés répartis sur trois continents (":
        "Em meados de {0}, o TikTok Shop Seller Center está oficialmente ativo em cerca de vinte mercados em três continentes (",
    "🌎 Amériques": "🌎 Américas",
    "États-Unis": "Estados Unidos",
    "Mexique": "México",
    "Brésil": "Brasil",
    "🇪🇺 Europe": "🇪🇺 Europa",
    "Royaume-Uni": "Reino Unido",
    "France": "França",
    "Allemagne": "Alemanha",
    "Espagne": "Espanha",
    "Italie": "Itália",
    "Irlande": "Irlanda",
    "Autriche": "Áustria",
    "(juin {0})": "(junho de {0})",
    "Belgique": "Bélgica",
    "Pays-Bas": "Países Baixos",
    "Pologne": "Polônia",
    "🌏 Asie-Pacifique": "🌏 Ásia-Pacífico",
    "Indonésie": "Indonésia",
    "Thaïlande": "Tailândia",
    "Vietnam": "Vietnã",
    "Malaisie": "Malásia",
    "Philippines": "Filipinas",
    "Singapour": "Singapura",
    "Japon": "Japão",
    "Pas encore ouvert :": "Ainda não aberto:",
    "l'Australie n'a toujours pas accès à TikTok Shop Seller Center mi-{0}, et malgré des rumeurs récurrentes, aucun lancement natif n'est confirmé dans le Golfe (Arabie saoudite, Émirats) à cette date (":
        "a Austrália ainda não tem acesso ao TikTok Shop Seller Center em meados de {0} e, apesar dos boatos recorrentes, nenhum lançamento próprio está confirmado no Golfo (Arábia Saudita, Emirados) nessa data (",
    "🇮🇩 L'Indonésie, nouveau rival direct des États-Unis": "🇮🇩 A Indonésia, nova rival direta dos Estados Unidos",
    "C'est l'un des faits les plus frappants de {0} : sur le premier semestre, l'": "É um dos dados mais marcantes de {0}: no primeiro semestre, a",
    "Indonésie a dépassé les États-Unis": "Indonésia passou os Estados Unidos",
    "comme premier marché de TikTok Shop, avec {0} milliards de dollars de GMV contre {1} milliards pour les USA (":
        "como maior mercado do TikTok Shop, com {0} bilhões de dólares de GMV contra {1} bilhões dos EUA (",
    "). Sur l'année {0} complète, les États-Unis reprennent la tête ({1} Md$ contre {2} Md$ pour l'Indonésie), mais l'Indonésie reste le deuxième marché mondial de la plateforme, et toute la région Asie du Sud-Est a doublé son GMV en un an pour atteindre {3} milliards de dollars (":
        "). No ano de {0} inteiro os Estados Unidos retomam a liderança ({1} bi $ contra {2} bi $ da Indonésia), mas a Indonésia segue como segundo maior mercado da plataforma, e todo o Sudeste Asiático dobrou seu GMV em um ano, chegando a {3} bilhões de dólares (",
    "💰 Les créateurs américains devenus millionnaires grâce à TikTok Shop":
        "💰 Os criadores americanos que ficaram milionários com o TikTok Shop",
    "Derrière les chiffres macro, il y a des histoires individuelles très concrètes. Voici trois créateurs américains dont la réussite sur TikTok Shop est documentée dans la presse.":
        "Por trás dos números grandes existem histórias individuais bem concretas. Aqui vão três criadores americanos cujos resultados no TikTok Shop estão documentados na imprensa.",
    "Stormi Steele — Canvas Beauty (Body Glaze)": "Stormi Steele — Canvas Beauty (Body Glaze)",
    "{0}M$": "{0} mi $",
    "en un seul live ({0} juin {1})": "em uma única live ({0} de junho de {1})",
    "en une journée (Black Friday)": "em um dia (Black Friday)",
    "de ventes mensuelles visées": "de vendas mensais como meta",
    "Fondatrice de Canvas Beauty et de sa gamme Body Glaze (huile de soin corporel), Stormi Steele est devenue la première créatrice à dépasser {0} million de dollars de ventes lors d'un seul live TikTok Shop, le {1} juin {2} (":
        "Fundadora da Canvas Beauty e da linha Body Glaze (óleo corporal), Stormi Steele foi a primeira criadora a passar de {0} milhão de dólares em vendas em uma única live do TikTok Shop, em {1} de junho de {2} (",
    "). Lors du Black Friday, sa marque a généré {0} millions de dollars de ventes en une journée, dont {1} millions via un « mega live » de {2} heures organisé depuis son entrepôt en Alabama (":
        "). Na Black Friday, a marca dela gerou {0} milhões de dólares em vendas num dia, {1} milhões deles numa “mega live” de {2} horas feita do galpão dela no Alabama (",
    "). Canvas Beauty a depuis été désignée marque n°{0} en ventes sur TikTok Shop aux États-Unis, avec une trajectoire vers {1} millions de dollars de ventes mensuelles (":
        "). Desde então a Canvas Beauty é apontada como marca n.º {0} em vendas no TikTok Shop nos Estados Unidos, a caminho de {1} milhões de dólares em vendas mensais (",
    "Logan Walter — Beauté & self-care masculin": "Logan Walter — beleza e autocuidado masculino",
    "{0} ans": "{0} anos",
    "au moment de devenir millionnaire": "quando virou milionário",
    "pour atteindre ce statut": "para chegar lá",
    "{0} chiffres": "{0} dígitos",
    "de revenu mensuel": "de renda mensal",
    "Logan Walter a quitté l'université à {0} ans pour se consacrer à TikTok Shop, où il s'est imposé comme l'un des rares hommes affiliés dans le créneau beauté/self-care, en vendant des marques comme Medicube ou Neutrogena. Sa première vidéo virale lui a fait gagner plus de {1} dollars en un mois ; deux ans après ses débuts, il touchait un revenu mensuel à sept chiffres (":
        "Logan Walter largou a faculdade aos {0} anos para se dedicar ao TikTok Shop, onde se firmou como um dos poucos homens afiliados na área de beleza e autocuidado, vendendo marcas como Medicube e Neutrogena. O primeiro vídeo viral dele rendeu mais de {1} dólares em um mês; dois anos depois de começar, tinha renda mensal de sete dígitos (",
    "Katrina Dimiele — Mode en direct (try-on livestreams)": "Katrina Dimiele — moda ao vivo (try-on hauls)",
    "cumulés en {0} ans": "acumulados em {0} anos",
    "heures de vente en direct": "horas de venda ao vivo",
    "Créatrice mode spécialisée dans les « try-on hauls » en direct, Katrina Dimiele a cumulé {0} millions de dollars de ventes en neuf ans via ses lives sur TikTok Shop et Facebook (":
        "Criadora de moda especializada em “try-on hauls” ao vivo, Katrina Dimiele acumulou {0} milhões de dólares em vendas em nove anos com suas lives no TikTok Shop e no Facebook (",
    "). Son parcours illustre une réalité importante : la plupart des plus gros succès viennent de créateurs qui ont accumulé des milliers d'heures de pratique avant d'exploser, pas d'un coup de chance isolé.":
        "). O caminho dela mostra algo importante: a maioria dos maiores sucessos vem de criadores que acumularam milhares de horas de prática antes de estourar, não de um golpe de sorte isolado.",
    "🔑 À retenir :": "🔑 Para guardar:",
    "ces trois parcours partagent un point commun — le live shopping. C'est le format qui génère les pics de revenus les plus spectaculaires sur TikTok Shop, bien plus que les vidéos courtes seules.":
        "os três caminhos têm uma coisa em comum: o live shopping. É o formato que gera os picos de receita mais espetaculares no TikTok Shop, muito mais do que só os vídeos curtos.",
    "📉 Et pour un créateur « normal » ?": "📉 E para um criador comum?",
    "Ces histoires sont réelles, mais elles ne représentent pas la moyenne. Selon les données de monétisation {0}, le créateur médian sur TikTok gagne environ {1} dollars par mois toutes sources confondues, tandis que les {2} % les plus performants combinent plusieurs revenus pour atteindre {3} à {4} dollars par mois (":
        "Essas histórias são reais, mas não são a média. Segundo os dados de monetização de {0}, o criador mediano no TikTok ganha cerca de {1} dólares por mês somando todas as fontes, enquanto os {2} % de melhor desempenho combinam várias receitas e chegam a {3}–{4} dólares por mês (",
    "). Les millions de Stormi Steele, Logan Walter ou Katrina Dimiele sont le sommet visible d'une pyramide beaucoup plus large.":
        "). Os milhões de Stormi Steele, Logan Walter ou Katrina Dimiele são o topo visível de uma pirâmide bem mais larga.",
    "🔮 Ce qui s'annonce ensuite": "🔮 O que vem a seguir",
    "Le rythme d'expansion ne ralentit pas : après la vague européenne de juin {0}, TikTok Shop teste déjà des abonnements payants qui rappellent le modèle Amazon Prime (":
        "O ritmo de expansão não afrouxa: depois da onda europeia de junho de {0}, o TikTok Shop já testa assinaturas pagas que lembram o modelo do Amazon Prime (",
    "), et des enseignes historiques comme Ulta Beauty ont rejoint la plateforme aux États-Unis en misant sur sa capacité à transformer la découverte en achat (":
        "), e redes tradicionais como a Ulta Beauty entraram na plataforma nos Estados Unidos, apostando na capacidade dela de transformar descoberta em compra (",
    "❓ Questions fréquentes": "❓ Perguntas frequentes",
    "Qu'est-ce que TikTok Shop ?": "O que é o TikTok Shop?",
    "TikTok Shop est la fonctionnalité e-commerce intégrée à TikTok qui permet d'acheter des produits directement depuis l'application, via des vidéos courtes, des lives shopping ou une vitrine boutique. Lancée en {0}, elle est disponible mi-{1} dans une vingtaine de pays dont les États-Unis, le Royaume-Uni, la France, l'Allemagne, l'Espagne, l'Italie, l'Irlande, l'Indonésie, la Thaïlande, le Vietnam, la Malaisie, les Philippines, Singapour, le Japon, le Mexique et le Brésil.":
        "O TikTok Shop é a parte de comércio embutida no TikTok, que permite comprar produtos direto no aplicativo por vídeos curtos, lives de compras ou uma vitrine de loja. Lançado em {0}, em meados de {1} está disponível em cerca de vinte países, entre eles Estados Unidos, Reino Unido, França, Alemanha, Espanha, Itália, Irlanda, Indonésia, Tailândia, Vietnã, Malásia, Filipinas, Singapura, Japão, México e Brasil.",
    "Peut-on vraiment gagner de l'argent avec TikTok Shop ?": "Dá mesmo para ganhar dinheiro com o TikTok Shop?",
    "Oui : les créateurs peuvent toucher des commissions d'affiliation en recommandant des produits, et les vendeurs peuvent gérer leur propre boutique. Certains créateurs comme Stormi Steele (Canvas Beauty) ou Logan Walter sont devenus millionnaires grâce à TikTok Shop. Mais la réalité reste à deux vitesses : le créateur médian gagne environ {0} dollars par mois, et seule une minorité de top créateurs atteint des revenus à sept chiffres.":
        "Sim: criadores podem receber comissões de afiliação recomendando produtos, e vendedores podem tocar a própria loja. Alguns criadores, como Stormi Steele (Canvas Beauty) ou Logan Walter, ficaram milionários com o TikTok Shop. Mas a realidade continua tendo duas velocidades: o criador mediano ganha cerca de {0} dólares por mês, e só uma minoria de criadores de topo chega a receitas de sete dígitos.",
    "Dans quels pays TikTok Shop est-il disponible ?": "Em quais países o TikTok Shop está disponível?",
    "Mi-{0}, TikTok Shop est actif dans une vingtaine de marchés : aux Amériques (États-Unis, Mexique, Brésil), en Europe (Royaume-Uni, France, Allemagne, Espagne, Italie, Irlande, et depuis juin {1} l'Autriche, la Belgique, les Pays-Bas et la Pologne), et en Asie-Pacifique (Indonésie, Thaïlande, Vietnam, Malaisie, Philippines, Singapour, Japon). L'Australie et les pays du Golfe n'ont pas encore de lancement officiel.":
        "Em meados de {0}, o TikTok Shop está ativo em cerca de vinte mercados: nas Américas (Estados Unidos, México, Brasil), na Europa (Reino Unido, França, Alemanha, Espanha, Itália, Irlanda e, desde junho de {1}, Áustria, Bélgica, Países Baixos e Polônia) e na Ásia-Pacífico (Indonésia, Tailândia, Vietnã, Malásia, Filipinas, Singapura, Japão). Austrália e países do Golfo ainda não têm lançamento oficial.",
    "Vous voulez percer sur TikTok Shop ?": "Quer estourar no TikTok Shop?",
    "Utilisez Qeerah pour analyser vos vidéos et copier ce qui fonctionne vraiment chez les créateurs qui cartonnent.":
        "Use a Qeerah para analisar seus vídeos e copiar o que realmente funciona nos criadores que estão bombando.",
    "Analyser mes vidéos →": "Analisar meus vídeos →",
    "📚 Sources": "📚 Fontes",
    "interview vidéo, TikTok Shop Millionaire": "entrevista em vídeo, TikTok Shop Millionaire",
    "TikTok Shop Millionaire — ${0}M in {1} Years Selling Fashion On Livestreams (interview vidéo)":
        "TikTok Shop Millionaire — ${0}M in {1} Years Selling Fashion On Livestreams (entrevista em vídeo)",
}

T_BLOG_EXPANSION["en-ie"] = dict(T_BLOG_EXPANSION["en"])
T_BLOG_EXPANSION["es-mx"] = dict(T_BLOG_EXPANSION["es"])
