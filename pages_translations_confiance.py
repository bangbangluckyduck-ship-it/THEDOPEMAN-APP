"""Traductions des pages de CONFIANCE — à propos, contact, avis.

Même mécanique que pages_translations.py : la clef est le texte français rendu,
les nombres sont sortis de la clef et réinjectés (`{0}`).

Deux choses ne sont volontairement pas traduites, et n'apparaissent donc dans
aucun dictionnaire : l'adresse e-mail de contact, et la ligne de copyright, qui
porte des noms d'entreprise. Ce qui n'est pas listé reste français — c'est le
comportement voulu pour tout ce qui est un nom propre.
"""
from __future__ import annotations

# ═══════════════════════════════════════════════════════════════════════════
# /about
# ═══════════════════════════════════════════════════════════════════════════
T_ABOUT: dict[str, dict[str, str]] = {
    "en": {
        "À Propos - Qeerah by Dope Ventures": "About — Qeerah by Dope Ventures",
        "À propos de Qeerah - Créé par Dope Ventures pour aider les créateurs TikTok Shop":
            "About Qeerah — built by Dope Ventures to help TikTok Shop creators",
        "← Retour à l'accueil": "← Back to home",
        "À Propos de Qeerah": "About Qeerah",
        "est un outil créé par": "is a tool built by",
        "par des créateurs TikTok Shop qui se sont rendu compte de l'importance de pouvoir se faire aider lorsqu'on démarre TikTok Shop, mais aussi pour aider les créateurs confirmés à mieux analyser et améliorer leur contenu.":
            "by TikTok Shop creators who learned the hard way how much a bit of help matters when you're starting out — and who wanted established creators to have a better way to read and improve their own content.",
        "C'est un outil qui permet aux agences de mieux accompagner leurs créateurs et leur faire gagner du temps en leur donnant accès aux data du monde entier sans abonnement supplémentaire.":
            "It also lets agencies support their creators better and save them time, with data from every market and no extra subscription.",
        "Notre Mission": "Our mission",
        "Démocratiser l'accès à l'analyse vidéo professionelle pour que chaque créateur TikTok Shop puisse :":
            "Put professional video analysis within everyone's reach, so that every TikTok Shop creator can:",
        "Analyser": "Analyse",
        "Comprendre exactement pourquoi tes vidéos performent ou non grâce à notre IA":
            "Understand exactly why your videos land or don't, with our AI",
        "Optimiser": "Optimise",
        "Améliorer ton contenu à partir d'analyses détaillées et directement applicables":
            "Improve your content from detailed findings you can act on straight away",
        "Innover": "Innovate",
        "Rester à la pointe des tendances TikTok Shop grâce aux données globales":
            "Stay ahead of TikTok Shop trends, using data from every market",
        "Scaler": "Scale",
        "Passer de créateur à business viable avec une stratégie data-driven":
            "Go from creator to a business that stands up, with a strategy built on data",
        "Pourquoi Qeerah ?": "Why Qeerah?",
        "Créer du contenu TikTok Shop performant n'est pas une science exacte, mais ça peut s'y rapprocher. Pendant des années, les créateurs ont testé à l'aveugle, analysant leurs statistiques sans vraiment comprendre les mécanismes sous-jacents.":
            "Making TikTok Shop content that sells isn't an exact science, but it can get close. For years creators tested blind, staring at their stats without really seeing what was driving them.",
        "Qeerah change ça. En utilisant une IA entraînée sur les patterns de milliers de vidéos virales, nous pouvons vous montrer :":
            "Qeerah changes that. With an AI trained on the patterns of thousands of viral videos, we can show you:",
        "Ce que valent tes accroches": "What your hooks are worth",
        "Comment améliorer ta rétention": "How to hold attention longer",
        "Quels triggers psychologiques fonctionnent": "Which psychological triggers actually work",
        "Où placer tes appels à l'action": "Where to put your calls to action",
        "Comment adapter ton contenu à ta niche": "How to fit your content to your niche",
        "Pour les Agences": "For agencies",
        "Si tu gères plusieurs créateurs, Qeerah devient ton avantage décisif. Accède aux données du monde entier, tirez des insights sur les tendances globales, et accompagnez vos créateurs avec une stratégie basée sur les data plutôt que sur l'intuition.":
            "If you manage several creators, Qeerah becomes your edge. Reach data from every market, read global trends, and guide your creators with a strategy built on data rather than instinct.",
        "Tout cela sans surcoût pour tes clients. Pour les besoins multi-comptes, une offre sur devis est disponible.":
            "All of it at no extra cost to your clients. For multi-seat needs, a quoted plan is available.",
        "Créée par des Créateurs, Pour des Créateurs": "Built by creators, for creators",
        "L'équipe derrière Qeerah connaît TikTok Shop par expérience directe. Nous avons testé, échoué, optimisé, et réussi. Chaque feature de Qeerah a été créée parce que nous savions qu'il manquait quelque chose sur le marché.":
            "The team behind Qeerah knows TikTok Shop first-hand. We tested, failed, adjusted, and got there. Every feature exists because we felt its absence ourselves.",
        "Prêt à analyser tes vidéos ?": "Ready to analyse your videos?",
        "Teste Qeerah gratuitement : {0} jours d'accès complet, sans carte bancaire, zéro engagement.":
            "Try Qeerah free: {0} days of full access, no card, no commitment.",
        "Commencer maintenant →": "Start now →",
    },
    "pt-br": {
        "À Propos - Qeerah by Dope Ventures": "Sobre — Qeerah by Dope Ventures",
        "À propos de Qeerah - Créé par Dope Ventures pour aider les créateurs TikTok Shop":
            "Sobre a Qeerah — feita pela Dope Ventures para ajudar criadores do TikTok Shop",
        "← Retour à l'accueil": "← Voltar ao início",
        "À Propos de Qeerah": "Sobre a Qeerah",
        "est un outil créé par": "é uma ferramenta criada pela",
        "par des créateurs TikTok Shop qui se sont rendu compte de l'importance de pouvoir se faire aider lorsqu'on démarre TikTok Shop, mais aussi pour aider les créateurs confirmés à mieux analyser et améliorer leur contenu.":
            "por criadores de TikTok Shop que sentiram na pele o quanto faz diferença ter ajuda no começo — e que queriam dar a quem já é experiente uma forma melhor de ler e melhorar o próprio conteúdo.",
        "C'est un outil qui permet aux agences de mieux accompagner leurs créateurs et leur faire gagner du temps en leur donnant accès aux data du monde entier sans abonnement supplémentaire.":
            "Também serve para agências acompanharem melhor seus criadores e ganharem tempo, com dados de todos os mercados e sem assinatura extra.",
        "Notre Mission": "Nossa missão",
        "Démocratiser l'accès à l'analyse vidéo professionelle pour que chaque créateur TikTok Shop puisse :":
            "Colocar a análise de vídeo profissional ao alcance de todo mundo, para que cada criador do TikTok Shop possa:",
        "Analyser": "Analisar",
        "Comprendre exactement pourquoi tes vidéos performent ou non grâce à notre IA":
            "Entender exatamente por que seus vídeos funcionam ou não, com a nossa IA",
        "Optimiser": "Otimizar",
        "Améliorer ton contenu à partir d'analyses détaillées et directement applicables":
            "Melhorar seu conteúdo a partir de análises detalhadas e prontas para aplicar",
        "Innover": "Inovar",
        "Rester à la pointe des tendances TikTok Shop grâce aux données globales":
            "Ficar à frente das tendências do TikTok Shop, com dados de todos os mercados",
        "Scaler": "Escalar",
        "Passer de créateur à business viable avec une stratégie data-driven":
            "Sair de criador para um negócio que se sustenta, com estratégia baseada em dados",
        "Pourquoi Qeerah ?": "Por que a Qeerah?",
        "Créer du contenu TikTok Shop performant n'est pas une science exacte, mais ça peut s'y rapprocher. Pendant des années, les créateurs ont testé à l'aveugle, analysant leurs statistiques sans vraiment comprendre les mécanismes sous-jacents.":
            "Fazer conteúdo que vende no TikTok Shop não é ciência exata, mas dá para chegar perto. Durante anos os criadores testaram no escuro, olhando as métricas sem entender de verdade o que estava por trás.",
        "Qeerah change ça. En utilisant une IA entraînée sur les patterns de milliers de vidéos virales, nous pouvons vous montrer :":
            "A Qeerah muda isso. Com uma IA treinada nos padrões de milhares de vídeos virais, a gente mostra:",
        "Ce que valent tes accroches": "Quanto valem seus ganchos",
        "Comment améliorer ta rétention": "Como segurar a atenção por mais tempo",
        "Quels triggers psychologiques fonctionnent": "Quais gatilhos psicológicos realmente funcionam",
        "Où placer tes appels à l'action": "Onde colocar suas chamadas para ação",
        "Comment adapter ton contenu à ta niche": "Como adaptar seu conteúdo ao seu nicho",
        "Pour les Agences": "Para agências",
        "Si tu gères plusieurs créateurs, Qeerah devient ton avantage décisif. Accède aux données du monde entier, tirez des insights sur les tendances globales, et accompagnez vos créateurs avec une stratégie basée sur les data plutôt que sur l'intuition.":
            "Se você cuida de vários criadores, a Qeerah vira sua vantagem. Acesse dados de todos os mercados, leia as tendências globais e oriente seus criadores com estratégia baseada em dados, não em achismo.",
        "Tout cela sans surcoût pour tes clients. Pour les besoins multi-comptes, une offre sur devis est disponible.":
            "Tudo isso sem custo extra para seus clientes. Para várias contas, existe um plano sob orçamento.",
        "Créée par des Créateurs, Pour des Créateurs": "Feita por criadores, para criadores",
        "L'équipe derrière Qeerah connaît TikTok Shop par expérience directe. Nous avons testé, échoué, optimisé, et réussi. Chaque feature de Qeerah a été créée parce que nous savions qu'il manquait quelque chose sur le marché.":
            "O time por trás da Qeerah conhece o TikTok Shop na prática. A gente testou, errou, ajustou e chegou lá. Cada recurso existe porque sentimos a falta dele.",
        "Prêt à analyser tes vidéos ?": "Pronto para analisar seus vídeos?",
        "Teste Qeerah gratuitement : {0} jours d'accès complet, sans carte bancaire, zéro engagement.":
            "Teste a Qeerah de graça: {0} dias de acesso completo, sem cartão, sem compromisso.",
        "Commencer maintenant →": "Começar agora →",
    },
    "es": {
        "À Propos - Qeerah by Dope Ventures": "Quiénes somos — Qeerah by Dope Ventures",
        "À propos de Qeerah - Créé par Dope Ventures pour aider les créateurs TikTok Shop":
            "Sobre Qeerah — creada por Dope Ventures para ayudar a los creadores de TikTok Shop",
        "← Retour à l'accueil": "← Volver al inicio",
        "À Propos de Qeerah": "Sobre Qeerah",
        "est un outil créé par": "es una herramienta creada por",
        "par des créateurs TikTok Shop qui se sont rendu compte de l'importance de pouvoir se faire aider lorsqu'on démarre TikTok Shop, mais aussi pour aider les créateurs confirmés à mieux analyser et améliorer leur contenu.":
            "por creadores de TikTok Shop que descubrieron por las malas lo mucho que importa tener ayuda al empezar — y que querían dar a los creadores con experiencia una forma mejor de leer y mejorar su contenido.",
        "C'est un outil qui permet aux agences de mieux accompagner leurs créateurs et leur faire gagner du temps en leur donnant accès aux data du monde entier sans abonnement supplémentaire.":
            "También permite a las agencias acompañar mejor a sus creadores y ahorrarles tiempo, con datos de todos los mercados y sin suscripción adicional.",
        "Notre Mission": "Nuestra misión",
        "Démocratiser l'accès à l'analyse vidéo professionelle pour que chaque créateur TikTok Shop puisse :":
            "Poner el análisis de vídeo profesional al alcance de todos, para que cada creador de TikTok Shop pueda:",
        "Analyser": "Analizar",
        "Comprendre exactement pourquoi tes vidéos performent ou non grâce à notre IA":
            "Entender exactamente por qué tus vídeos funcionan o no, con nuestra IA",
        "Optimiser": "Optimizar",
        "Améliorer ton contenu à partir d'analyses détaillées et directement applicables":
            "Mejorar tu contenido a partir de análisis detallados y listos para aplicar",
        "Innover": "Innovar",
        "Rester à la pointe des tendances TikTok Shop grâce aux données globales":
            "Ir por delante de las tendencias de TikTok Shop, con datos de todos los mercados",
        "Scaler": "Escalar",
        "Passer de créateur à business viable avec une stratégie data-driven":
            "Pasar de creador a un negocio que se sostiene, con una estrategia basada en datos",
        "Pourquoi Qeerah ?": "¿Por qué Qeerah?",
        "Créer du contenu TikTok Shop performant n'est pas une science exacte, mais ça peut s'y rapprocher. Pendant des années, les créateurs ont testé à l'aveugle, analysant leurs statistiques sans vraiment comprendre les mécanismes sous-jacents.":
            "Hacer contenido que venda en TikTok Shop no es una ciencia exacta, pero puede acercarse. Durante años los creadores probaron a ciegas, mirando sus estadísticas sin entender de verdad qué había detrás.",
        "Qeerah change ça. En utilisant une IA entraînée sur les patterns de milliers de vidéos virales, nous pouvons vous montrer :":
            "Qeerah cambia eso. Con una IA entrenada con los patrones de miles de vídeos virales, te enseñamos:",
        "Ce que valent tes accroches": "Cuánto valen tus ganchos",
        "Comment améliorer ta rétention": "Cómo retener la atención más tiempo",
        "Quels triggers psychologiques fonctionnent": "Qué disparadores psicológicos funcionan de verdad",
        "Où placer tes appels à l'action": "Dónde colocar tus llamadas a la acción",
        "Comment adapter ton contenu à ta niche": "Cómo adaptar tu contenido a tu nicho",
        "Pour les Agences": "Para agencias",
        "Si tu gères plusieurs créateurs, Qeerah devient ton avantage décisif. Accède aux données du monde entier, tirez des insights sur les tendances globales, et accompagnez vos créateurs avec une stratégie basée sur les data plutôt que sur l'intuition.":
            "Si llevas a varios creadores, Qeerah se convierte en tu ventaja. Accede a datos de todos los mercados, lee las tendencias globales y acompaña a tus creadores con una estrategia basada en datos y no en intuición.",
        "Tout cela sans surcoût pour tes clients. Pour les besoins multi-comptes, une offre sur devis est disponible.":
            "Todo ello sin coste extra para tus clientes. Para varias cuentas hay un plan con presupuesto.",
        "Créée par des Créateurs, Pour des Créateurs": "Creada por creadores, para creadores",
        "L'équipe derrière Qeerah connaît TikTok Shop par expérience directe. Nous avons testé, échoué, optimisé, et réussi. Chaque feature de Qeerah a été créée parce que nous savions qu'il manquait quelque chose sur le marché.":
            "El equipo detrás de Qeerah conoce TikTok Shop de primera mano. Probamos, fallamos, ajustamos y lo conseguimos. Cada función existe porque nos hizo falta a nosotros.",
        "Prêt à analyser tes vidéos ?": "¿List@ para analizar tus vídeos?",
        "Teste Qeerah gratuitement : {0} jours d'accès complet, sans carte bancaire, zéro engagement.":
            "Prueba Qeerah gratis: {0} días de acceso completo, sin tarjeta y sin compromiso.",
        "Commencer maintenant →": "Empezar ahora →",
    },
    "it": {
        "À Propos - Qeerah by Dope Ventures": "Chi siamo — Qeerah by Dope Ventures",
        "À propos de Qeerah - Créé par Dope Ventures pour aider les créateurs TikTok Shop":
            "Su Qeerah — creata da Dope Ventures per aiutare i creator di TikTok Shop",
        "← Retour à l'accueil": "← Torna alla home",
        "À Propos de Qeerah": "Su Qeerah",
        "est un outil créé par": "è uno strumento creato da",
        "par des créateurs TikTok Shop qui se sont rendu compte de l'importance de pouvoir se faire aider lorsqu'on démarre TikTok Shop, mais aussi pour aider les créateurs confirmés à mieux analyser et améliorer leur contenu.":
            "da creator di TikTok Shop che hanno capito sulla propria pelle quanto conta essere aiutati all'inizio — e che volevano dare ai creator già esperti un modo migliore di leggere e migliorare i propri contenuti.",
        "C'est un outil qui permet aux agences de mieux accompagner leurs créateurs et leur faire gagner du temps en leur donnant accès aux data du monde entier sans abonnement supplémentaire.":
            "Serve anche alle agenzie per seguire meglio i propri creator e far loro guadagnare tempo, con dati di tutti i mercati e senza abbonamenti in più.",
        "Notre Mission": "La nostra missione",
        "Démocratiser l'accès à l'analyse vidéo professionelle pour que chaque créateur TikTok Shop puisse :":
            "Mettere l'analisi video professionale alla portata di tutti, perché ogni creator di TikTok Shop possa:",
        "Analyser": "Analizzare",
        "Comprendre exactement pourquoi tes vidéos performent ou non grâce à notre IA":
            "Capire esattamente perché i tuoi video funzionano o no, con la nostra IA",
        "Optimiser": "Ottimizzare",
        "Améliorer ton contenu à partir d'analyses détaillées et directement applicables":
            "Migliorare i contenuti partendo da analisi dettagliate e subito applicabili",
        "Innover": "Innovare",
        "Rester à la pointe des tendances TikTok Shop grâce aux données globales":
            "Stare avanti sulle tendenze di TikTok Shop, con i dati di tutti i mercati",
        "Scaler": "Crescere",
        "Passer de créateur à business viable avec une stratégie data-driven":
            "Passare da creator a un'attività che sta in piedi, con una strategia basata sui dati",
        "Pourquoi Qeerah ?": "Perché Qeerah?",
        "Créer du contenu TikTok Shop performant n'est pas une science exacte, mais ça peut s'y rapprocher. Pendant des années, les créateurs ont testé à l'aveugle, analysant leurs statistiques sans vraiment comprendre les mécanismes sous-jacents.":
            "Fare contenuti che vendono su TikTok Shop non è una scienza esatta, ma ci si può avvicinare. Per anni i creator hanno provato alla cieca, guardando le statistiche senza capire davvero cosa ci fosse sotto.",
        "Qeerah change ça. En utilisant une IA entraînée sur les patterns de milliers de vidéos virales, nous pouvons vous montrer :":
            "Qeerah cambia le cose. Con un'IA addestrata sugli schemi di migliaia di video virali, ti mostriamo:",
        "Ce que valent tes accroches": "Quanto valgono i tuoi hook",
        "Comment améliorer ta rétention": "Come tenere l'attenzione più a lungo",
        "Quels triggers psychologiques fonctionnent": "Quali leve psicologiche funzionano davvero",
        "Où placer tes appels à l'action": "Dove mettere le tue call to action",
        "Comment adapter ton contenu à ta niche": "Come adattare i contenuti alla tua nicchia",
        "Pour les Agences": "Per le agenzie",
        "Si tu gères plusieurs créateurs, Qeerah devient ton avantage décisif. Accède aux données du monde entier, tirez des insights sur les tendances globales, et accompagnez vos créateurs avec une stratégie basée sur les data plutôt que sur l'intuition.":
            "Se segui più creator, Qeerah diventa il tuo vantaggio. Accedi ai dati di tutti i mercati, leggi le tendenze globali e guida i tuoi creator con una strategia basata sui dati invece che sull'intuito.",
        "Tout cela sans surcoût pour tes clients. Pour les besoins multi-comptes, une offre sur devis est disponible.":
            "Il tutto senza costi aggiuntivi per i tuoi clienti. Per più account c'è un piano su preventivo.",
        "Créée par des Créateurs, Pour des Créateurs": "Creata da creator, per i creator",
        "L'équipe derrière Qeerah connaît TikTok Shop par expérience directe. Nous avons testé, échoué, optimisé, et réussi. Chaque feature de Qeerah a été créée parce que nous savions qu'il manquait quelque chose sur le marché.":
            "Il team dietro Qeerah conosce TikTok Shop per esperienza diretta. Abbiamo provato, sbagliato, corretto e ce l'abbiamo fatta. Ogni funzione esiste perché prima ci è mancata.",
        "Prêt à analyser tes vidéos ?": "Pronto ad analizzare i tuoi video?",
        "Teste Qeerah gratuitement : {0} jours d'accès complet, sans carte bancaire, zéro engagement.":
            "Prova Qeerah gratis: {0} giorni di accesso completo, senza carta e senza vincoli.",
        "Commencer maintenant →": "Inizia adesso →",
    },
    "de": {
        "À Propos - Qeerah by Dope Ventures": "Über uns — Qeerah by Dope Ventures",
        "À propos de Qeerah - Créé par Dope Ventures pour aider les créateurs TikTok Shop":
            "Über Qeerah — von Dope Ventures gebaut, um TikTok-Shop-Creators zu helfen",
        "← Retour à l'accueil": "← Zurück zur Startseite",
        "À Propos de Qeerah": "Über Qeerah",
        "est un outil créé par": "ist ein Werkzeug von",
        "par des créateurs TikTok Shop qui se sont rendu compte de l'importance de pouvoir se faire aider lorsqu'on démarre TikTok Shop, mais aussi pour aider les créateurs confirmés à mieux analyser et améliorer leur contenu.":
            "gebaut von TikTok-Shop-Creators, die am eigenen Leib gemerkt haben, wie viel Hilfe am Anfang ausmacht — und die erfahrenen Creators eine bessere Art geben wollten, ihre eigenen Inhalte zu lesen und zu verbessern.",
        "C'est un outil qui permet aux agences de mieux accompagner leurs créateurs et leur faire gagner du temps en leur donnant accès aux data du monde entier sans abonnement supplémentaire.":
            "Auch Agenturen betreuen damit ihre Creators besser und sparen ihnen Zeit — mit Daten aus allen Märkten und ohne zusätzliches Abo.",
        "Notre Mission": "Unser Auftrag",
        "Démocratiser l'accès à l'analyse vidéo professionelle pour que chaque créateur TikTok Shop puisse :":
            "Professionelle Videoanalyse für alle zugänglich machen, damit jeder TikTok-Shop-Creator kann:",
        "Analyser": "Analysieren",
        "Comprendre exactement pourquoi tes vidéos performent ou non grâce à notre IA":
            "Genau verstehen, warum deine Videos ankommen oder nicht — mit unserer KI",
        "Optimiser": "Optimieren",
        "Améliorer ton contenu à partir d'analyses détaillées et directement applicables":
            "Deine Inhalte verbessern, ausgehend von detaillierten und sofort umsetzbaren Befunden",
        "Innover": "Neues wagen",
        "Rester à la pointe des tendances TikTok Shop grâce aux données globales":
            "Bei TikTok-Shop-Trends vorn bleiben, mit Daten aus allen Märkten",
        "Scaler": "Skalieren",
        "Passer de créateur à business viable avec une stratégie data-driven":
            "Vom Creator zu einem Geschäft, das trägt — mit einer Strategie auf Datenbasis",
        "Pourquoi Qeerah ?": "Warum Qeerah?",
        "Créer du contenu TikTok Shop performant n'est pas une science exacte, mais ça peut s'y rapprocher. Pendant des années, les créateurs ont testé à l'aveugle, analysant leurs statistiques sans vraiment comprendre les mécanismes sous-jacents.":
            "Inhalte zu machen, die auf TikTok Shop verkaufen, ist keine exakte Wissenschaft — aber man kann nah rankommen. Jahrelang haben Creators blind getestet und auf Statistiken gestarrt, ohne wirklich zu sehen, was dahintersteckt.",
        "Qeerah change ça. En utilisant une IA entraînée sur les patterns de milliers de vidéos virales, nous pouvons vous montrer :":
            "Qeerah ändert das. Mit einer KI, die auf den Mustern tausender viraler Videos trainiert ist, zeigen wir dir:",
        "Ce que valent tes accroches": "Was deine Hooks taugen",
        "Comment améliorer ta rétention": "Wie du Aufmerksamkeit länger hältst",
        "Quels triggers psychologiques fonctionnent": "Welche psychologischen Auslöser wirklich wirken",
        "Où placer tes appels à l'action": "Wo dein Call to Action hingehört",
        "Comment adapter ton contenu à ta niche": "Wie du deine Inhalte auf deine Nische zuschneidest",
        "Pour les Agences": "Für Agenturen",
        "Si tu gères plusieurs créateurs, Qeerah devient ton avantage décisif. Accède aux données du monde entier, tirez des insights sur les tendances globales, et accompagnez vos créateurs avec une stratégie basée sur les data plutôt que sur l'intuition.":
            "Wenn du mehrere Creators betreust, wird Qeerah dein Vorsprung. Greif auf Daten aus allen Märkten zu, lies globale Trends und begleite deine Creators mit einer Strategie auf Datenbasis statt aus dem Bauch.",
        "Tout cela sans surcoût pour tes clients. Pour les besoins multi-comptes, une offre sur devis est disponible.":
            "Und das ohne Aufpreis für deine Kunden. Für mehrere Konten gibt es ein Angebot auf Anfrage.",
        "Créée par des Créateurs, Pour des Créateurs": "Von Creators gemacht, für Creators",
        "L'équipe derrière Qeerah connaît TikTok Shop par expérience directe. Nous avons testé, échoué, optimisé, et réussi. Chaque feature de Qeerah a été créée parce que nous savions qu'il manquait quelque chose sur le marché.":
            "Das Team hinter Qeerah kennt TikTok Shop aus erster Hand. Wir haben getestet, sind gescheitert, haben nachgebessert und es geschafft. Jede Funktion gibt es, weil sie uns selbst gefehlt hat.",
        "Prêt à analyser tes vidéos ?": "Bereit, deine Videos zu analysieren?",
        "Teste Qeerah gratuitement : {0} jours d'accès complet, sans carte bancaire, zéro engagement.":
            "Teste Qeerah kostenlos: {0} Tage voller Zugang, ohne Kreditkarte, ohne Bindung.",
        "Commencer maintenant →": "Jetzt loslegen →",
    },
}


# ═══════════════════════════════════════════════════════════════════════════
# /contact
# L'adresse e-mail n'est pas listée : ce n'est pas du texte, c'est une adresse.
# ═══════════════════════════════════════════════════════════════════════════
T_CONTACT: dict[str, dict[str, str]] = {
    "en": {
        "Contact - Qeerah by Dope Ventures": "Contact — Qeerah by Dope Ventures",
        "Contactez Qeerah - Dope Ventures pour toute question ou partenariat":
            "Get in touch with Qeerah — Dope Ventures, for any question or partnership",
        "← Retour à l'accueil": "← Back to home",
        "Nous contacter": "Contact us",
        "Des questions ou envie de discuter d'un partenariat ?":
            "A question, or want to talk about working together?",
        "Contact Direct": "Direct contact",
        "N'hésitez pas à nous envoyer un email pour toute question, suggestion ou partenariat.":
            "Write to us about anything — a question, an idea, a partnership.",
        "Email Principal": "Main email",
        "Partenariats": "Partnerships",
        "Tu es une agence, un créateur ou un influenceur ? Contacte-nous pour discuter des opportunités de collaboration.":
            "Agency, creator or influencer? Get in touch and let's talk about working together.",
        "Réponse généralement sous {0}-{1}h pendant les jours ouvrables.":
            "We usually reply within {0}-{1} hours on working days.",
        "Suivez-nous": "Follow us",
        "Rejoignez notre communauté pour rester informé des derniers updates et news TikTok Shop.":
            "Join the community and keep up with what's new on Qeerah and on TikTok Shop.",
        "Voir notre TikTok →": "See our TikTok →",
    },
    "pt-br": {
        "Contact - Qeerah by Dope Ventures": "Contato — Qeerah by Dope Ventures",
        "Contactez Qeerah - Dope Ventures pour toute question ou partenariat":
            "Fale com a Qeerah — Dope Ventures, para qualquer dúvida ou parceria",
        "← Retour à l'accueil": "← Voltar ao início",
        "Nous contacter": "Fale com a gente",
        "Des questions ou envie de discuter d'un partenariat ?":
            "Tem uma dúvida ou quer falar sobre parceria?",
        "Contact Direct": "Contato direto",
        "N'hésitez pas à nous envoyer un email pour toute question, suggestion ou partenariat.":
            "Escreva pra gente sobre qualquer coisa — dúvida, sugestão ou parceria.",
        "Email Principal": "E-mail principal",
        "Partenariats": "Parcerias",
        "Tu es une agence, un créateur ou un influenceur ? Contacte-nous pour discuter des opportunités de collaboration.":
            "É agência, criador ou influenciador? Fale com a gente pra conversar sobre colaboração.",
        "Réponse généralement sous {0}-{1}h pendant les jours ouvrables.":
            "Normalmente respondemos em {0}-{1} horas nos dias úteis.",
        "Suivez-nous": "Siga a gente",
        "Rejoignez notre communauté pour rester informé des derniers updates et news TikTok Shop.":
            "Entre na comunidade e fique por dentro das novidades da Qeerah e do TikTok Shop.",
        "Voir notre TikTok →": "Ver nosso TikTok →",
    },
    "es": {
        "Contact - Qeerah by Dope Ventures": "Contacto — Qeerah by Dope Ventures",
        "Contactez Qeerah - Dope Ventures pour toute question ou partenariat":
            "Contacta con Qeerah — Dope Ventures, para cualquier duda o colaboración",
        "← Retour à l'accueil": "← Volver al inicio",
        "Nous contacter": "Contactar",
        "Des questions ou envie de discuter d'un partenariat ?":
            "¿Tienes una duda o quieres hablar de una colaboración?",
        "Contact Direct": "Contacto directo",
        "N'hésitez pas à nous envoyer un email pour toute question, suggestion ou partenariat.":
            "Escríbenos por lo que sea: una duda, una idea o una colaboración.",
        "Email Principal": "Correo principal",
        "Partenariats": "Colaboraciones",
        "Tu es une agence, un créateur ou un influenceur ? Contacte-nous pour discuter des opportunités de collaboration.":
            "¿Eres agencia, creador o influencer? Escríbenos y hablamos de colaborar.",
        "Réponse généralement sous {0}-{1}h pendant les jours ouvrables.":
            "Solemos responder en {0}-{1} horas los días laborables.",
        "Suivez-nous": "Síguenos",
        "Rejoignez notre communauté pour rester informé des derniers updates et news TikTok Shop.":
            "Únete a la comunidad y entérate de las novedades de Qeerah y de TikTok Shop.",
        "Voir notre TikTok →": "Ver nuestro TikTok →",
    },
    "it": {
        "Contact - Qeerah by Dope Ventures": "Contatti — Qeerah by Dope Ventures",
        "Contactez Qeerah - Dope Ventures pour toute question ou partenariat":
            "Contatta Qeerah — Dope Ventures, per qualsiasi domanda o collaborazione",
        "← Retour à l'accueil": "← Torna alla home",
        "Nous contacter": "Contattaci",
        "Des questions ou envie de discuter d'un partenariat ?":
            "Hai una domanda o vuoi parlare di una collaborazione?",
        "Contact Direct": "Contatto diretto",
        "N'hésitez pas à nous envoyer un email pour toute question, suggestion ou partenariat.":
            "Scrivici per qualsiasi cosa: una domanda, un'idea, una collaborazione.",
        "Email Principal": "Email principale",
        "Partenariats": "Collaborazioni",
        "Tu es une agence, un créateur ou un influenceur ? Contacte-nous pour discuter des opportunités de collaboration.":
            "Sei un'agenzia, un creator o un influencer? Scrivici e parliamo di collaborare.",
        "Réponse généralement sous {0}-{1}h pendant les jours ouvrables.":
            "Di solito rispondiamo entro {0}-{1} ore nei giorni lavorativi.",
        "Suivez-nous": "Seguici",
        "Rejoignez notre communauté pour rester informé des derniers updates et news TikTok Shop.":
            "Entra nella community e resta aggiornato su Qeerah e su TikTok Shop.",
        "Voir notre TikTok →": "Guarda il nostro TikTok →",
    },
    "de": {
        "Contact - Qeerah by Dope Ventures": "Kontakt — Qeerah by Dope Ventures",
        "Contactez Qeerah - Dope Ventures pour toute question ou partenariat":
            "Kontakt zu Qeerah — Dope Ventures, für Fragen und Partnerschaften",
        "← Retour à l'accueil": "← Zurück zur Startseite",
        "Nous contacter": "Kontakt aufnehmen",
        "Des questions ou envie de discuter d'un partenariat ?":
            "Eine Frage, oder Lust über eine Zusammenarbeit zu sprechen?",
        "Contact Direct": "Direkter Kontakt",
        "N'hésitez pas à nous envoyer un email pour toute question, suggestion ou partenariat.":
            "Schreib uns einfach — bei Fragen, Ideen oder Partnerschaften.",
        "Email Principal": "Haupt-E-Mail",
        "Partenariats": "Partnerschaften",
        "Tu es une agence, un créateur ou un influenceur ? Contacte-nous pour discuter des opportunités de collaboration.":
            "Agentur, Creator oder Influencer? Melde dich, dann reden wir über eine Zusammenarbeit.",
        "Réponse généralement sous {0}-{1}h pendant les jours ouvrables.":
            "Wir antworten an Werktagen meist innerhalb von {0}-{1} Stunden.",
        "Suivez-nous": "Folge uns",
        "Rejoignez notre communauté pour rester informé des derniers updates et news TikTok Shop.":
            "Komm in die Community und bleib bei Qeerah und TikTok Shop auf dem Laufenden.",
        "Voir notre TikTok →": "Unser TikTok ansehen →",
    },
}


# ═══════════════════════════════════════════════════════════════════════════
# /avis — formulaire. Les messages posés par le script (alertes, libellé du
# bouton) passent par <script data-i18n-js>, cf. pages_i18n.traduire_script.
# ═══════════════════════════════════════════════════════════════════════════
T_AVIS: dict[str, dict[str, str]] = {
    "en": {
        "Donne ton avis — Qeerah": "Leave a review — Qeerah",
        "Partage ton avis sur Qeerah.": "Share what you think of Qeerah.",
        "Ton avis compte 🙏": "Your review matters 🙏",
        "Partage ton expérience — ça aide d'autres créateurs à se lancer. Publié après validation.":
            "Tell us how it went — it helps other creators take the plunge. Published after review.",
        "Ton nom / pseudo *": "Your name / handle *",
        "Ex: Julie K.": "e.g. Julie K.",
        "Ton profil TikTok (optionnel)": "Your TikTok profile (optional)",
        "Affiché publiquement comme lien vers ton profil.": "Shown publicly as a link to your profile.",
        "Ton témoignage *": "Your review *",
        "Ce que l'outil t'a apporté, un résultat concret…": "What the tool changed for you, a concrete result…",
        "Note (optionnel)": "Rating (optional)",
        "Envoyer mon avis →": "Send my review →",
        "Merci !": "Thank you!",
        "Ton avis a bien été envoyé. Il sera publié après une rapide validation.":
            "Your review is in. It'll be published after a quick check.",
        "Retour à l'accueil": "Back to home",
        # Messages posés par le script
        "Renseigne ton nom et un témoignage (au moins {0} caractères).":
            "Add your name and a review (at least {0} characters).",
        "Envoi…": "Sending…",
        "Connecte-toi à ton compte Qeerah pour laisser ton avis — ça prend {0} secondes.":
            "Log in to your Qeerah account to leave a review — it takes {0} seconds.",
        "Erreur réseau.": "Network error.",
        "Erreur": "Error",
    },
    "pt-br": {
        "Donne ton avis — Qeerah": "Deixe sua avaliação — Qeerah",
        "Partage ton avis sur Qeerah.": "Conte o que você acha da Qeerah.",
        "Ton avis compte 🙏": "Sua opinião importa 🙏",
        "Partage ton expérience — ça aide d'autres créateurs à se lancer. Publié après validation.":
            "Conte como foi — ajuda outros criadores a começar. Publicado após revisão.",
        "Ton nom / pseudo *": "Seu nome / @ *",
        "Ex: Julie K.": "ex.: Julie K.",
        "Ton profil TikTok (optionnel)": "Seu perfil no TikTok (opcional)",
        "Affiché publiquement comme lien vers ton profil.": "Aparece publicamente como link pro seu perfil.",
        "Ton témoignage *": "Seu depoimento *",
        "Ce que l'outil t'a apporté, un résultat concret…": "O que a ferramenta mudou pra você, um resultado concreto…",
        "Note (optionnel)": "Nota (opcional)",
        "Envoyer mon avis →": "Enviar minha avaliação →",
        "Merci !": "Obrigado!",
        "Ton avis a bien été envoyé. Il sera publié après une rapide validation.":
            "Sua avaliação chegou. Vai ser publicada depois de uma checagem rápida.",
        "Retour à l'accueil": "Voltar ao início",
        "Renseigne ton nom et un témoignage (au moins {0} caractères).":
            "Preencha seu nome e um depoimento (pelo menos {0} caracteres).",
        "Envoi…": "Enviando…",
        "Connecte-toi à ton compte Qeerah pour laisser ton avis — ça prend {0} secondes.":
            "Entre na sua conta Qeerah para avaliar — leva {0} segundos.",
        "Erreur réseau.": "Erro de rede.",
        "Erreur": "Erro",
    },
    "es": {
        "Donne ton avis — Qeerah": "Deja tu opinión — Qeerah",
        "Partage ton avis sur Qeerah.": "Cuenta qué te parece Qeerah.",
        "Ton avis compte 🙏": "Tu opinión cuenta 🙏",
        "Partage ton expérience — ça aide d'autres créateurs à se lancer. Publié après validation.":
            "Cuenta cómo te fue — ayuda a otros creadores a dar el paso. Se publica tras revisión.",
        "Ton nom / pseudo *": "Tu nombre / usuario *",
        "Ex: Julie K.": "Ej.: Julie K.",
        "Ton profil TikTok (optionnel)": "Tu perfil de TikTok (opcional)",
        "Affiché publiquement comme lien vers ton profil.": "Se muestra públicamente como enlace a tu perfil.",
        "Ton témoignage *": "Tu opinión *",
        "Ce que l'outil t'a apporté, un résultat concret…": "Qué te ha aportado la herramienta, un resultado concreto…",
        "Note (optionnel)": "Puntuación (opcional)",
        "Envoyer mon avis →": "Enviar mi opinión →",
        "Merci !": "¡Gracias!",
        "Ton avis a bien été envoyé. Il sera publié après une rapide validation.":
            "Tu opinión ha llegado. Se publicará tras una revisión rápida.",
        "Retour à l'accueil": "Volver al inicio",
        "Renseigne ton nom et un témoignage (au moins {0} caractères).":
            "Pon tu nombre y una opinión (al menos {0} caracteres).",
        "Envoi…": "Enviando…",
        "Connecte-toi à ton compte Qeerah pour laisser ton avis — ça prend {0} secondes.":
            "Entra en tu cuenta de Qeerah para dejar tu opinión — son {0} segundos.",
        "Erreur réseau.": "Error de red.",
        "Erreur": "Error",
    },
    "it": {
        "Donne ton avis — Qeerah": "Lascia la tua recensione — Qeerah",
        "Partage ton avis sur Qeerah.": "Raccontaci cosa pensi di Qeerah.",
        "Ton avis compte 🙏": "La tua opinione conta 🙏",
        "Partage ton expérience — ça aide d'autres créateurs à se lancer. Publié après validation.":
            "Racconta com'è andata — aiuta altri creator a partire. Pubblicata dopo una verifica.",
        "Ton nom / pseudo *": "Il tuo nome / nickname *",
        "Ex: Julie K.": "es.: Julie K.",
        "Ton profil TikTok (optionnel)": "Il tuo profilo TikTok (facoltativo)",
        "Affiché publiquement comme lien vers ton profil.": "Mostrato pubblicamente come link al tuo profilo.",
        "Ton témoignage *": "La tua recensione *",
        "Ce que l'outil t'a apporté, un résultat concret…": "Cosa ti ha dato lo strumento, un risultato concreto…",
        "Note (optionnel)": "Voto (facoltativo)",
        "Envoyer mon avis →": "Invia la mia recensione →",
        "Merci !": "Grazie!",
        "Ton avis a bien été envoyé. Il sera publié après une rapide validation.":
            "La tua recensione è arrivata. Sarà pubblicata dopo una verifica veloce.",
        "Retour à l'accueil": "Torna alla home",
        "Renseigne ton nom et un témoignage (au moins {0} caractères).":
            "Inserisci il tuo nome e una recensione (almeno {0} caratteri).",
        "Envoi…": "Invio…",
        "Connecte-toi à ton compte Qeerah pour laisser ton avis — ça prend {0} secondes.":
            "Accedi al tuo account Qeerah per lasciare la recensione — bastano {0} secondi.",
        "Erreur réseau.": "Errore di rete.",
        "Erreur": "Errore",
    },
    "de": {
        "Donne ton avis — Qeerah": "Bewertung abgeben — Qeerah",
        "Partage ton avis sur Qeerah.": "Sag uns, was du von Qeerah hältst.",
        "Ton avis compte 🙏": "Deine Meinung zählt 🙏",
        "Partage ton expérience — ça aide d'autres créateurs à se lancer. Publié après validation.":
            "Erzähl, wie es lief — das hilft anderen Creators beim Start. Wird nach Prüfung veröffentlicht.",
        "Ton nom / pseudo *": "Dein Name / Handle *",
        "Ex: Julie K.": "z. B. Julie K.",
        "Ton profil TikTok (optionnel)": "Dein TikTok-Profil (optional)",
        "Affiché publiquement comme lien vers ton profil.": "Wird öffentlich als Link zu deinem Profil gezeigt.",
        "Ton témoignage *": "Deine Bewertung *",
        "Ce que l'outil t'a apporté, un résultat concret…": "Was dir das Werkzeug gebracht hat, ein konkretes Ergebnis…",
        "Note (optionnel)": "Wertung (optional)",
        "Envoyer mon avis →": "Bewertung abschicken →",
        "Merci !": "Danke!",
        "Ton avis a bien été envoyé. Il sera publié après une rapide validation.":
            "Deine Bewertung ist da. Sie wird nach einer kurzen Prüfung veröffentlicht.",
        "Retour à l'accueil": "Zurück zur Startseite",
        "Renseigne ton nom et un témoignage (au moins {0} caractères).":
            "Trag deinen Namen und eine Bewertung ein (mindestens {0} Zeichen).",
        "Envoi…": "Wird gesendet…",
        "Connecte-toi à ton compte Qeerah pour laisser ton avis — ça prend {0} secondes.":
            "Melde dich bei deinem Qeerah-Konto an, um zu bewerten — dauert {0} Sekunden.",
        "Erreur réseau.": "Netzwerkfehler.",
        "Erreur": "Fehler",
    },
}


# ── Irlande et Mexique ──────────────────────────────────────────────────────
for _dico in (T_ABOUT, T_CONTACT, T_AVIS):
    _dico["en-ie"] = dict(_dico["en"])

_MX_ABOUT = {
    "Prêt à analyser tes vidéos ?": "¿Listo para analizar tus videos?",
    "Teste Qeerah gratuitement : {0} jours d'accès complet, sans carte bancaire, zéro engagement.":
        "Prueba Qeerah gratis: {0} días de acceso completo, sin tarjeta y sin compromiso.",
    "Comprendre exactement pourquoi tes vidéos performent ou non grâce à notre IA":
        "Entender exactamente por qué tus videos funcionan o no, con nuestra IA",
    "Démocratiser l'accès à l'analyse vidéo professionelle pour que chaque créateur TikTok Shop puisse :":
        "Poner el análisis de video profesional al alcance de todos, para que cada creador de TikTok Shop pueda:",
    "Qeerah change ça. En utilisant une IA entraînée sur les patterns de milliers de vidéos virales, nous pouvons vous montrer :":
        "Qeerah cambia eso. Con una IA entrenada con los patrones de miles de videos virales, te enseñamos:",
    "Créer du contenu TikTok Shop performant n'est pas une science exacte, mais ça peut s'y rapprocher. Pendant des années, les créateurs ont testé à l'aveugle, analysant leurs statistiques sans vraiment comprendre les mécanismes sous-jacents.":
        "Hacer contenido que venda en TikTok Shop no es una ciencia exacta, pero puede acercarse. Durante años los creadores probaron a ciegas, mirando sus estadísticas sin entender de verdad qué había detrás.",
}
_MX_AVIS = {
    "Ton témoignage *": "Tu opinión *",
    "Ce que l'outil t'a apporté, un résultat concret…": "Qué te dio la herramienta, un resultado concreto…",
    "Connecte-toi à ton compte Qeerah pour laisser ton avis — ça prend {0} secondes.":
        "Entra a tu cuenta de Qeerah para dejar tu opinión — son {0} segundos.",
}
T_ABOUT["es-mx"] = {**T_ABOUT["es"], **_MX_ABOUT}
T_CONTACT["es-mx"] = dict(T_CONTACT["es"])
T_AVIS["es-mx"] = {**T_AVIS["es"], **_MX_AVIS}
