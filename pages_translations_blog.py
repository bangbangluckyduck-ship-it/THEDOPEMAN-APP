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
