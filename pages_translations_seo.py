"""Traductions des pages d'ATTERRISSAGE — les trois pages de contenu SEO.

⚠️ UNE RÉSERVE, ÉCRITE ICI POUR QU'ELLE NE SE PERDE PAS.

Ces trois pages ont été écrites AUTOUR DE MOTS-CLEFS FRANÇAIS : « analyser une
vidéo TikTok Shop », « produits qui vendent en France », « ma vidéo ne fait pas
de vues ». Les traduire fidèlement — ce qui a été demandé et fait — donne des
pages justes et utiles à lire, mais qui visent des requêtes que personne n'a
vérifiées sur ces marchés. Leur URL reste d'ailleurs française (/en/analyser-
une-video-tiktok-shop), puisque c'est le chemin qui porte l'historique.

Autrement dit : ce fichier rend le site cohérent dans chaque langue. Il ne
remplace pas, le jour où un marché comptera vraiment, un article écrit POUR ce
marché, avec ses propres mots-clefs et sa propre URL. C'est un travail
éditorial, pas de traduction.

La page « produits qui vendent en France » garde en plus un ancrage explicite :
ses chiffres et ses catégories sont français. La traduction dit donc clairement
de quel marché elle parle, plutôt que de laisser croire à un lecteur allemand
que ces produits sont ceux de son pays.

Mécanique : identique aux autres pages (pages_i18n.py) — la clef est le texte
français rendu, les nombres sont hors clef et réinjectés (`{0}`).
"""
from __future__ import annotations

# ═══════════════════════════════════════════════════════════════════════════
# /analyser-une-video-tiktok-shop
# ═══════════════════════════════════════════════════════════════════════════
T_LP_ANALYSER: dict[str, dict[str, str]] = {}

T_LP_ANALYSER["en"] = {
    "Analyser une vidéo TikTok Shop : la méthode complète — Qeerah":
        "How to analyse a TikTok Shop video: the full method — Qeerah",
    "Comment analyser une vidéo TikTok Shop pour comprendre pourquoi elle vend : accroche, rétention, déclencheurs, appel à l'action. Méthode manuelle et analyse automatique.":
        "How to analyse a TikTok Shop video and understand why it sells: hook, retention, triggers, call to action. The manual method, and the automatic one.",
    "Les sept dimensions à examiner sur une vidéo qui vend, et comment les reproduire sur ton produit.":
        "The seven dimensions to look at in a video that sells, and how to reproduce them with your own product.",
    "Tarifs": "Pricing",
    "Ouvrir l'app →": "Open the app →",
    "Analyser une vidéo TikTok Shop : la méthode complète":
        "How to analyse a TikTok Shop video: the full method",
    "Une vidéo qui vend n'est presque jamais un coup de chance. Elle empile des mécanismes précis, dans un ordre précis. Voici comment les repérer — à la main, puis automatiquement.":
        "A video that sells is almost never luck. It stacks precise mechanisms in a precise order. Here's how to spot them — by hand first, then automatically.",
    "Sur TikTok Shop France, ce sont les créateurs affiliés qui font tourner la boutique : ils représentent":
        "On TikTok Shop in France, affiliate creators are what keeps the shop running: they account for",
    "{0} % du chiffre d'affaires généré": "{0}% of the revenue generated",
    "dans le pays au deuxième trimestre {0}, contre {1} % pour l'onglet Shopping Mall où les marques déposent simplement leur catalogue. Autrement dit, ce n'est pas le produit qui vend, c'est la vidéo. D'où l'intérêt de savoir décortiquer celles qui fonctionnent.":
        "in the country in the second quarter of {0}, against {1}% for the Shopping Mall tab where brands simply upload their catalogue. In other words, it isn't the product that sells — it's the video. Which is why it pays to take apart the ones that work.",
    "Pourquoi analyser plutôt que copier": "Why analyse rather than copy",
    "Recopier une vidéo à l'identique ne marche pas : le produit change, l'audience change, le moment change. Ce qui se transfère, ce n'est pas le contenu, c'est la":
        "Copying a video outright doesn't work: the product changes, the audience changes, the moment changes. What transfers isn't the content, it's the",
    "structure": "structure",
    "— l'ordre dans lequel l'attention est captée, maintenue, puis convertie.":
        "— the order in which attention is caught, held, then converted.",
    "Analyser une vidéo, c'est donc répondre à trois questions : qu'est-ce qui a retenu le spectateur les trois premières secondes, qu'est-ce qui l'a gardé jusqu'à l'argument de vente, et qu'est-ce qui l'a fait cliquer. Tout le reste — la lumière, le montage, la musique — sert ces trois moments.":
        "So analysing a video means answering three questions: what held the viewer for the first three seconds, what kept them until the sales argument, and what made them click. Everything else — lighting, editing, music — serves those three moments.",
    "Les sept dimensions à examiner": "The seven dimensions to examine",
    "{0}. L'accroche": "{0}. The hook",
    "Regarde uniquement la première seconde et demie, son coupé. Le sujet est-il déjà identifiable ? Une bonne accroche nomme un problème, un résultat ou une contradiction avant que le spectateur ait le temps de décider de partir. Note le":
        "Watch only the first second and a half, sound off. Is the subject already clear? A good hook names a problem, a result or a contradiction before the viewer has time to decide to leave. Note the",
    "type": "type",
    "d'accroche : question directe, affirmation clivante, avant/après, accusation douce (« tu fais ça tous les matins et… »).":
        "of hook: direct question, divisive statement, before/after, gentle accusation (“you do this every morning and…”).",
    "{0}. La rétention": "{0}. Retention",
    "Compte les changements de plan et repère les « boucles ouvertes » : une promesse annoncée tôt et tenue plus tard, qui oblige à rester. Repère aussi le moment exact où toi, spectateur, tu as eu envie de partir. C'est presque toujours là que la courbe de rétention chute.":
        "Count the cuts and spot the “open loops”: a promise made early and kept later, which forces you to stay. Also spot the exact moment when you, as a viewer, wanted to leave. That's almost always where the retention curve drops.",
    "{0}. L'argumentaire de vente": "{0}. The sales argument",
    "Le produit est-il montré en usage réel ou en présentation statique ? Un seul bénéfice est-il martelé, ou une liste de caractéristiques est-elle récitée ? Les vidéos qui convertissent défendent généralement":
        "Is the product shown in real use, or in a static display? Is a single benefit hammered home, or is a list of features recited? Videos that convert usually defend",
    "un": "one",
    "bénéfice, très concret, illustré visuellement.": "benefit, very concrete, shown on screen.",
    "{0}. L'émotion": "{0}. Emotion",
    "Quelle émotion domine : frustration, soulagement, surprise, appartenance ? L'émotion n'est pas un supplément d'âme, c'est ce qui fixe le souvenir du produit. Une vidéo purement descriptive est oubliée en trois secondes.":
        "Which emotion dominates: frustration, relief, surprise, belonging? Emotion isn't decoration — it's what fixes the product in memory. A purely descriptive video is forgotten in three seconds.",
    "{0}. La conversion": "{0}. Conversion",
    "Où se situe l'appel à l'action, et sous quelle forme ? Dit à voix haute, écrit à l'écran, les deux ? Arrive-t-il avant ou après la chute d'attention ? Un appel à l'action placé à la quinzième seconde d'une vidéo qui perd son audience à la douzième ne sert à rien, même parfaitement formulé.":
        "Where does the call to action sit, and in what form? Spoken, on screen, both? Does it come before or after attention drops? A call to action at the fifteenth second of a video that loses its audience at the twelfth is useless, however well phrased.",
    "{0}. Les signaux algorithmiques": "{0}. Algorithm signals",
    "Format vertical plein cadre, texte à l'écran lisible sans le son, durée cohérente avec le sujet, son utilisé. Ces éléments ne font pas vendre directement, mais ils conditionnent la diffusion : une excellente vidéo mal formatée sera vue par peu de monde.":
        "Full-frame vertical format, on-screen text readable without sound, a length that fits the subject, sound actually used. None of this sells directly, but it decides how far the video travels: an excellent video, badly formatted, will be seen by few people.",
    "{0}. La cohérence d'ensemble": "{0}. Coherence overall",
    "Une fois les six points notés, une question demeure : les éléments se renforcent-ils ou se contredisent-ils ? Une accroche dramatique suivie d'une démonstration plate crée une déception qui coûte plus cher que si l'accroche avait été neutre.":
        "Once the six points are scored, one question remains: do the parts reinforce each other, or contradict each other? A dramatic hook followed by a flat demonstration creates a let-down that costs more than a neutral hook would have.",
    "La grille à remplir en dix minutes": "The grid to fill in, in ten minutes",
    "Prends une vidéo qui performe dans ta niche et note chaque dimension sur {0}. Puis fais la même chose sur ta dernière vidéo. L'écart le plus grand entre les deux, c'est ton chantier prioritaire — pas celui qui te semble le plus urgent intuitivement.":
        "Take a video that performs in your niche and score each dimension out of {0}. Then do the same on your last video. The biggest gap between the two is your first job — not the one that feels most urgent.",
    "Ce que l'analyse manuelle ne voit pas": "What manual analysis misses",
    "Cette méthode fonctionne, mais elle a deux limites. D'abord, elle est lente : dix à quinze minutes par vidéo, ce qui rend impossible l'analyse d'un volume suffisant pour dégager un motif. Ensuite, elle est biaisée : on remarque ce qu'on connaît déjà, et on passe à côté de ce qu'on n'a jamais formalisé.":
        "The method works, but it has two limits. First it's slow: ten to fifteen minutes per video, which makes it impossible to cover enough of them for a pattern to appear. Second it's biased: you notice what you already know, and miss what you've never put into words.",
    "C'est exactement ce que Qeerah automatise. L'outil analyse une vidéo à partir de son lien, image par image et bande son comprise, et rend les sept dimensions notées, les déclencheurs psychologiques détectés —":
        "That is exactly what Qeerah automates. From a link, the tool analyses a video frame by frame, sound included, and returns the seven dimensions scored, the psychological triggers it found —",
    "et ceux qui manquent": "and the ones missing",
    "—, la seconde où l'attention décroche, puis des accroches réécrites pour ton produit.":
        "—, the second where attention drops, then hooks rewritten for your product.",
    "Analyse ta première vidéo maintenant": "Analyse your first video now",
    "{0} jours d'accès complet, sans carte bancaire.": "{0} days of full access, no card required.",
    "Coller un lien TikTok": "Paste a TikTok link",
    "Trois erreurs fréquentes": "Three common mistakes",
    "Analyser des vidéos hors de sa niche.": "Analysing videos outside your niche.",
    "Les mécanismes qui vendent un accessoire de cuisine ne transposent pas tels quels sur un soin visage. Reste dans ta catégorie.":
        "What sells a kitchen gadget doesn't transfer as-is to a face cream. Stay in your category.",
    "Se fier au nombre de vues.": "Trusting the view count.",
    "Une vidéo à {0} millions de vues peut ne rien vendre. Cherche celles dont le produit est réellement écoulé, pas celles qui divertissent.":
        "A video with {0} million views can sell nothing. Look for the ones whose product actually moved, not the ones that entertain.",
    "Changer plusieurs choses à la fois.": "Changing several things at once.",
    "Si tu modifies l'accroche, le montage et l'appel à l'action en même temps, tu ne sauras jamais ce qui a produit l'effet. Une variable par test.":
        "If you change the hook, the editing and the call to action at the same time, you'll never know what caused the effect. One variable per test.",
    "Par où commencer concrètement": "Where to actually start",
    "Choisis cinq vidéos de ta niche publiées dans les trente derniers jours, dont le produit s'est visiblement vendu. Analyse-les l'une après l'autre. Tu verras apparaître deux ou trois constantes — un type d'accroche, un moment de démonstration, une formulation d'appel à l'action. Ce sont ces constantes que tu reproduis, pas les vidéos.":
        "Pick five videos from your niche published in the last thirty days, whose product visibly sold. Analyse them one after another. Two or three constants will appear — a type of hook, a moment of demonstration, a way of phrasing the call to action. Those constants are what you reproduce, not the videos.",
    "Ensuite seulement, applique-les à ton produit et publie. Compare la rétention obtenue à celle de tes vidéos précédentes. C'est le seul indicateur qui te dira si tu as compris le mécanisme ou seulement copié la surface.":
        "Only then apply them to your product and publish. Compare the retention you get with your previous videos. It's the only number that tells you whether you understood the mechanism or only copied the surface.",
    "Ma vidéo ne fait pas de vues": "My video isn't getting views",
    "Les produits qui vendent en France": "The products that sell in France",
    "Guide complet TikTok Shop": "Complete TikTok Shop guide",
    "Source des chiffres :": "Source of the figures:",
    ", données sur {0} jours arrêtées au {1} juillet {2}.": ", data over {0} days, as of {1} July {2}.",
}

T_LP_ANALYSER["de"] = {
    "Analyser une vidéo TikTok Shop : la méthode complète — Qeerah":
        "Ein TikTok-Shop-Video analysieren: die vollständige Methode — Qeerah",
    "Comment analyser une vidéo TikTok Shop pour comprendre pourquoi elle vend : accroche, rétention, déclencheurs, appel à l'action. Méthode manuelle et analyse automatique.":
        "Wie du ein TikTok-Shop-Video analysierst und verstehst, warum es verkauft: Hook, Bindung, Auslöser, Call to Action. Erst von Hand, dann automatisch.",
    "Les sept dimensions à examiner sur une vidéo qui vend, et comment les reproduire sur ton produit.":
        "Die sieben Dimensionen eines Videos, das verkauft — und wie du sie mit deinem Produkt nachbaust.",
    "Tarifs": "Preise",
    "Ouvrir l'app →": "App öffnen →",
    "Analyser une vidéo TikTok Shop : la méthode complète":
        "Ein TikTok-Shop-Video analysieren: die vollständige Methode",
    "Une vidéo qui vend n'est presque jamais un coup de chance. Elle empile des mécanismes précis, dans un ordre précis. Voici comment les repérer — à la main, puis automatiquement.":
        "Ein Video, das verkauft, ist fast nie Zufall. Es stapelt genaue Mechanismen in einer genauen Reihenfolge. So erkennst du sie — erst von Hand, dann automatisch.",
    "Sur TikTok Shop France, ce sont les créateurs affiliés qui font tourner la boutique : ils représentent":
        "Auf TikTok Shop in Frankreich halten die Affiliate-Creators den Laden am Laufen: Sie stehen für",
    "{0} % du chiffre d'affaires généré": "{0} % des erzielten Umsatzes",
    "dans le pays au deuxième trimestre {0}, contre {1} % pour l'onglet Shopping Mall où les marques déposent simplement leur catalogue. Autrement dit, ce n'est pas le produit qui vend, c'est la vidéo. D'où l'intérêt de savoir décortiquer celles qui fonctionnent.":
        "im Land im zweiten Quartal {0}, gegenüber {1} % im Reiter Shopping Mall, wo Marken einfach ihren Katalog hochladen. Anders gesagt: Nicht das Produkt verkauft, sondern das Video. Deshalb lohnt es, die auseinanderzunehmen, die funktionieren.",
    "Pourquoi analyser plutôt que copier": "Warum analysieren statt kopieren",
    "Recopier une vidéo à l'identique ne marche pas : le produit change, l'audience change, le moment change. Ce qui se transfère, ce n'est pas le contenu, c'est la":
        "Ein Video eins zu eins nachzubauen funktioniert nicht: Das Produkt ist anders, das Publikum ist anders, der Moment ist anders. Übertragbar ist nicht der Inhalt, sondern die",
    "structure": "Struktur",
    "— l'ordre dans lequel l'attention est captée, maintenue, puis convertie.":
        "— die Reihenfolge, in der Aufmerksamkeit geholt, gehalten und dann umgewandelt wird.",
    "Analyser une vidéo, c'est donc répondre à trois questions : qu'est-ce qui a retenu le spectateur les trois premières secondes, qu'est-ce qui l'a gardé jusqu'à l'argument de vente, et qu'est-ce qui l'a fait cliquer. Tout le reste — la lumière, le montage, la musique — sert ces trois moments.":
        "Ein Video zu analysieren heißt also, drei Fragen zu beantworten: Was hat den Zuschauer die ersten drei Sekunden gehalten, was hat ihn bis zum Verkaufsargument gebracht, und was hat ihn klicken lassen. Alles andere — Licht, Schnitt, Musik — dient diesen drei Momenten.",
    "Les sept dimensions à examiner": "Die sieben Dimensionen, die du prüfst",
    "{0}. L'accroche": "{0}. Der Hook",
    "Regarde uniquement la première seconde et demie, son coupé. Le sujet est-il déjà identifiable ? Une bonne accroche nomme un problème, un résultat ou une contradiction avant que le spectateur ait le temps de décider de partir. Note le":
        "Sieh dir nur die erste anderthalb Sekunden an, ohne Ton. Ist das Thema schon erkennbar? Ein guter Hook benennt ein Problem, ein Ergebnis oder einen Widerspruch, bevor der Zuschauer entscheiden kann zu gehen. Notiere den",
    "type": "Typ",
    "d'accroche : question directe, affirmation clivante, avant/après, accusation douce (« tu fais ça tous les matins et… »).":
        "des Hooks: direkte Frage, steile Behauptung, Vorher/Nachher, sanfter Vorwurf („Du machst das jeden Morgen und …“).",
    "{0}. La rétention": "{0}. Die Bindung",
    "Compte les changements de plan et repère les « boucles ouvertes » : une promesse annoncée tôt et tenue plus tard, qui oblige à rester. Repère aussi le moment exact où toi, spectateur, tu as eu envie de partir. C'est presque toujours là que la courbe de rétention chute.":
        "Zähl die Schnitte und such die „offenen Schleifen“: ein Versprechen, das früh gemacht und später eingelöst wird und zum Bleiben zwingt. Merk dir auch den genauen Moment, in dem du selbst weg wolltest. Genau dort fällt fast immer die Haltekurve ab.",
    "{0}. L'argumentaire de vente": "{0}. Das Verkaufsargument",
    "Le produit est-il montré en usage réel ou en présentation statique ? Un seul bénéfice est-il martelé, ou une liste de caractéristiques est-elle récitée ? Les vidéos qui convertissent défendent généralement":
        "Wird das Produkt im echten Einsatz gezeigt oder statisch präsentiert? Wird ein einziger Nutzen eingehämmert, oder eine Merkmalsliste heruntergebetet? Videos, die konvertieren, verteidigen meist",
    "un": "einen",
    "bénéfice, très concret, illustré visuellement.": "Nutzen, sehr konkret, im Bild gezeigt.",
    "{0}. L'émotion": "{0}. Die Emotion",
    "Quelle émotion domine : frustration, soulagement, surprise, appartenance ? L'émotion n'est pas un supplément d'âme, c'est ce qui fixe le souvenir du produit. Une vidéo purement descriptive est oubliée en trois secondes.":
        "Welche Emotion überwiegt: Frust, Erleichterung, Überraschung, Zugehörigkeit? Emotion ist kein Beiwerk — sie verankert die Erinnerung an das Produkt. Ein rein beschreibendes Video ist in drei Sekunden vergessen.",
    "{0}. La conversion": "{0}. Die Konversion",
    "Où se situe l'appel à l'action, et sous quelle forme ? Dit à voix haute, écrit à l'écran, les deux ? Arrive-t-il avant ou après la chute d'attention ? Un appel à l'action placé à la quinzième seconde d'une vidéo qui perd son audience à la douzième ne sert à rien, même parfaitement formulé.":
        "Wo sitzt der Call to Action, und in welcher Form? Gesprochen, im Bild, beides? Kommt er vor oder nach dem Aufmerksamkeitsabfall? Ein Call to Action in Sekunde fünfzehn eines Videos, das sein Publikum in Sekunde zwölf verliert, bringt nichts, so gut er auch formuliert ist.",
    "{0}. Les signaux algorithmiques": "{0}. Die Signale für den Algorithmus",
    "Format vertical plein cadre, texte à l'écran lisible sans le son, durée cohérente avec le sujet, son utilisé. Ces éléments ne font pas vendre directement, mais ils conditionnent la diffusion : une excellente vidéo mal formatée sera vue par peu de monde.":
        "Hochformat bildfüllend, Text im Bild auch ohne Ton lesbar, eine Länge, die zum Thema passt, Ton wirklich genutzt. Das verkauft nicht direkt, entscheidet aber über die Reichweite: Ein hervorragendes, schlecht formatiertes Video sehen wenige.",
    "{0}. La cohérence d'ensemble": "{0}. Die Stimmigkeit im Ganzen",
    "Une fois les six points notés, une question demeure : les éléments se renforcent-ils ou se contredisent-ils ? Une accroche dramatique suivie d'une démonstration plate crée une déception qui coûte plus cher que si l'accroche avait été neutre.":
        "Sind die sechs Punkte bewertet, bleibt eine Frage: Verstärken sich die Teile, oder widersprechen sie sich? Ein dramatischer Hook, gefolgt von einer faden Demonstration, erzeugt eine Enttäuschung, die teurer kommt als ein neutraler Hook.",
    "La grille à remplir en dix minutes": "Das Raster, in zehn Minuten ausgefüllt",
    "Prends une vidéo qui performe dans ta niche et note chaque dimension sur {0}. Puis fais la même chose sur ta dernière vidéo. L'écart le plus grand entre les deux, c'est ton chantier prioritaire — pas celui qui te semble le plus urgent intuitivement.":
        "Nimm ein Video, das in deiner Nische läuft, und bewerte jede Dimension von {0}. Dann dasselbe mit deinem letzten Video. Der größte Abstand zwischen beiden ist deine erste Baustelle — nicht die, die sich am dringendsten anfühlt.",
    "Ce que l'analyse manuelle ne voit pas": "Was die Analyse von Hand nicht sieht",
    "Cette méthode fonctionne, mais elle a deux limites. D'abord, elle est lente : dix à quinze minutes par vidéo, ce qui rend impossible l'analyse d'un volume suffisant pour dégager un motif. Ensuite, elle est biaisée : on remarque ce qu'on connaît déjà, et on passe à côté de ce qu'on n'a jamais formalisé.":
        "Die Methode funktioniert, hat aber zwei Grenzen. Erstens ist sie langsam: zehn bis fünfzehn Minuten pro Video — zu langsam, um genug davon zu sehen, damit ein Muster auftaucht. Zweitens ist sie voreingenommen: Man bemerkt, was man schon kennt, und übersieht, was man nie in Worte gefasst hat.",
    "C'est exactement ce que Qeerah automatise. L'outil analyse une vidéo à partir de son lien, image par image et bande son comprise, et rend les sept dimensions notées, les déclencheurs psychologiques détectés —":
        "Genau das automatisiert Qeerah. Aus einem Link analysiert das Werkzeug ein Video Bild für Bild samt Ton und liefert die sieben Dimensionen bewertet, die erkannten psychologischen Auslöser —",
    "et ceux qui manquent": "und die fehlenden",
    "—, la seconde où l'attention décroche, puis des accroches réécrites pour ton produit.":
        "—, die Sekunde, in der die Aufmerksamkeit abreißt, und dann Hooks, neu geschrieben für dein Produkt.",
    "Analyse ta première vidéo maintenant": "Analysiere jetzt dein erstes Video",
    "{0} jours d'accès complet, sans carte bancaire.": "{0} Tage voller Zugang, ohne Kreditkarte.",
    "Coller un lien TikTok": "TikTok-Link einfügen",
    "Trois erreurs fréquentes": "Drei häufige Fehler",
    "Analyser des vidéos hors de sa niche.": "Videos außerhalb der eigenen Nische analysieren.",
    "Les mécanismes qui vendent un accessoire de cuisine ne transposent pas tels quels sur un soin visage. Reste dans ta catégorie.":
        "Was ein Küchenhelfer verkauft, lässt sich nicht eins zu eins auf eine Gesichtspflege übertragen. Bleib in deiner Kategorie.",
    "Se fier au nombre de vues.": "Sich auf die Aufrufzahl verlassen.",
    "Une vidéo à {0} millions de vues peut ne rien vendre. Cherche celles dont le produit est réellement écoulé, pas celles qui divertissent.":
        "Ein Video mit {0} Millionen Aufrufen kann null verkaufen. Such die, deren Produkt wirklich weggegangen ist — nicht die, die unterhalten.",
    "Changer plusieurs choses à la fois.": "Mehrere Dinge gleichzeitig ändern.",
    "Si tu modifies l'accroche, le montage et l'appel à l'action en même temps, tu ne sauras jamais ce qui a produit l'effet. Une variable par test.":
        "Wenn du Hook, Schnitt und Call to Action gleichzeitig änderst, wirst du nie wissen, was gewirkt hat. Eine Variable pro Test.",
    "Par où commencer concrètement": "Wo du konkret anfängst",
    "Choisis cinq vidéos de ta niche publiées dans les trente derniers jours, dont le produit s'est visiblement vendu. Analyse-les l'une après l'autre. Tu verras apparaître deux ou trois constantes — un type d'accroche, un moment de démonstration, une formulation d'appel à l'action. Ce sont ces constantes que tu reproduis, pas les vidéos.":
        "Such dir fünf Videos aus deiner Nische, veröffentlicht in den letzten dreißig Tagen, deren Produkt sichtbar verkauft wurde. Analysiere sie nacheinander. Zwei oder drei Konstanten tauchen auf — ein Hook-Typ, ein Moment der Demonstration, eine Formulierung des Call to Action. Diese Konstanten baust du nach, nicht die Videos.",
    "Ensuite seulement, applique-les à ton produit et publie. Compare la rétention obtenue à celle de tes vidéos précédentes. C'est le seul indicateur qui te dira si tu as compris le mécanisme ou seulement copié la surface.":
        "Erst dann überträgst du sie auf dein Produkt und veröffentlichst. Vergleich die erreichte Haltequote mit deinen früheren Videos. Nur diese Zahl sagt dir, ob du den Mechanismus verstanden oder bloß die Oberfläche kopiert hast.",
    "Ma vidéo ne fait pas de vues": "Mein Video bekommt keine Aufrufe",
    "Les produits qui vendent en France": "Die Produkte, die in Frankreich verkaufen",
    "Guide complet TikTok Shop": "Vollständiger TikTok-Shop-Guide",
    "Source des chiffres :": "Quelle der Zahlen:",
    ", données sur {0} jours arrêtées au {1} juillet {2}.": ", Daten über {0} Tage, Stand {1}. Juli {2}.",
}

T_LP_ANALYSER["es"] = {
    "Analyser une vidéo TikTok Shop : la méthode complète — Qeerah":
        "Analizar un vídeo de TikTok Shop: el método completo — Qeerah",
    "Comment analyser une vidéo TikTok Shop pour comprendre pourquoi elle vend : accroche, rétention, déclencheurs, appel à l'action. Méthode manuelle et analyse automatique.":
        "Cómo analizar un vídeo de TikTok Shop para entender por qué vende: gancho, retención, disparadores, llamada a la acción. Método manual y análisis automático.",
    "Les sept dimensions à examiner sur une vidéo qui vend, et comment les reproduire sur ton produit.":
        "Las siete dimensiones que hay que mirar en un vídeo que vende, y cómo reproducirlas con tu producto.",
    "Tarifs": "Precios",
    "Ouvrir l'app →": "Abrir la app →",
    "Analyser une vidéo TikTok Shop : la méthode complète":
        "Analizar un vídeo de TikTok Shop: el método completo",
    "Une vidéo qui vend n'est presque jamais un coup de chance. Elle empile des mécanismes précis, dans un ordre précis. Voici comment les repérer — à la main, puis automatiquement.":
        "Un vídeo que vende casi nunca es suerte. Apila mecanismos precisos, en un orden preciso. Así se detectan: primero a mano, luego de forma automática.",
    "Sur TikTok Shop France, ce sont les créateurs affiliés qui font tourner la boutique : ils représentent":
        "En TikTok Shop Francia son los creadores afiliados los que mueven la tienda: representan el",
    "{0} % du chiffre d'affaires généré": "{0} % de la facturación generada",
    "dans le pays au deuxième trimestre {0}, contre {1} % pour l'onglet Shopping Mall où les marques déposent simplement leur catalogue. Autrement dit, ce n'est pas le produit qui vend, c'est la vidéo. D'où l'intérêt de savoir décortiquer celles qui fonctionnent.":
        "en el país en el segundo trimestre de {0}, frente al {1} % de la pestaña Shopping Mall, donde las marcas se limitan a subir su catálogo. Dicho de otro modo: no vende el producto, vende el vídeo. De ahí el interés de saber desmontar los que funcionan.",
    "Pourquoi analyser plutôt que copier": "Por qué analizar en lugar de copiar",
    "Recopier une vidéo à l'identique ne marche pas : le produit change, l'audience change, le moment change. Ce qui se transfère, ce n'est pas le contenu, c'est la":
        "Copiar un vídeo tal cual no funciona: cambia el producto, cambia el público, cambia el momento. Lo que se transfiere no es el contenido, es la",
    "structure": "estructura",
    "— l'ordre dans lequel l'attention est captée, maintenue, puis convertie.":
        "— el orden en el que la atención se capta, se mantiene y luego se convierte.",
    "Analyser une vidéo, c'est donc répondre à trois questions : qu'est-ce qui a retenu le spectateur les trois premières secondes, qu'est-ce qui l'a gardé jusqu'à l'argument de vente, et qu'est-ce qui l'a fait cliquer. Tout le reste — la lumière, le montage, la musique — sert ces trois moments.":
        "Analizar un vídeo es responder a tres preguntas: qué retuvo al espectador los tres primeros segundos, qué lo mantuvo hasta el argumento de venta y qué le hizo hacer clic. Todo lo demás —la luz, el montaje, la música— está al servicio de esos tres momentos.",
    "Les sept dimensions à examiner": "Las siete dimensiones que hay que examinar",
    "{0}. L'accroche": "{0}. El gancho",
    "Regarde uniquement la première seconde et demie, son coupé. Le sujet est-il déjà identifiable ? Une bonne accroche nomme un problème, un résultat ou une contradiction avant que le spectateur ait le temps de décider de partir. Note le":
        "Mira solo el primer segundo y medio, sin sonido. ¿Se identifica ya el tema? Un buen gancho nombra un problema, un resultado o una contradicción antes de que el espectador tenga tiempo de decidir irse. Anota el",
    "type": "tipo",
    "d'accroche : question directe, affirmation clivante, avant/après, accusation douce (« tu fais ça tous les matins et… »).":
        "de gancho: pregunta directa, afirmación polémica, antes/después, acusación suave («haces esto todas las mañanas y…»).",
    "{0}. La rétention": "{0}. La retención",
    "Compte les changements de plan et repère les « boucles ouvertes » : une promesse annoncée tôt et tenue plus tard, qui oblige à rester. Repère aussi le moment exact où toi, spectateur, tu as eu envie de partir. C'est presque toujours là que la courbe de rétention chute.":
        "Cuenta los cambios de plano y busca los «bucles abiertos»: una promesa lanzada pronto y cumplida más tarde, que obliga a quedarse. Localiza también el momento exacto en el que tú, como espectador, quisiste irte. Casi siempre es ahí donde cae la curva de retención.",
    "{0}. L'argumentaire de vente": "{0}. El argumento de venta",
    "Le produit est-il montré en usage réel ou en présentation statique ? Un seul bénéfice est-il martelé, ou une liste de caractéristiques est-elle récitée ? Les vidéos qui convertissent défendent généralement":
        "¿El producto se muestra en uso real o en presentación estática? ¿Se martillea un solo beneficio o se recita una lista de características? Los vídeos que convierten suelen defender",
    "un": "un",
    "bénéfice, très concret, illustré visuellement.": "beneficio, muy concreto, mostrado en pantalla.",
    "{0}. L'émotion": "{0}. La emoción",
    "Quelle émotion domine : frustration, soulagement, surprise, appartenance ? L'émotion n'est pas un supplément d'âme, c'est ce qui fixe le souvenir du produit. Une vidéo purement descriptive est oubliée en trois secondes.":
        "¿Qué emoción domina: frustración, alivio, sorpresa, pertenencia? La emoción no es un adorno: es lo que fija el recuerdo del producto. Un vídeo puramente descriptivo se olvida en tres segundos.",
    "{0}. La conversion": "{0}. La conversión",
    "Où se situe l'appel à l'action, et sous quelle forme ? Dit à voix haute, écrit à l'écran, les deux ? Arrive-t-il avant ou après la chute d'attention ? Un appel à l'action placé à la quinzième seconde d'une vidéo qui perd son audience à la douzième ne sert à rien, même parfaitement formulé.":
        "¿Dónde está la llamada a la acción y en qué forma? ¿Dicha en voz alta, escrita en pantalla, las dos? ¿Llega antes o después de la caída de atención? Una llamada a la acción en el segundo quince de un vídeo que pierde a su público en el doce no sirve de nada, por muy bien formulada que esté.",
    "{0}. Les signaux algorithmiques": "{0}. Las señales para el algoritmo",
    "Format vertical plein cadre, texte à l'écran lisible sans le son, durée cohérente avec le sujet, son utilisé. Ces éléments ne font pas vendre directement, mais ils conditionnent la diffusion : une excellente vidéo mal formatée sera vue par peu de monde.":
        "Formato vertical a pantalla completa, texto legible sin sonido, duración coherente con el tema, sonido aprovechado. Nada de esto vende directamente, pero condiciona la difusión: un vídeo excelente mal formateado lo verá poca gente.",
    "{0}. La cohérence d'ensemble": "{0}. La coherencia del conjunto",
    "Une fois les six points notés, une question demeure : les éléments se renforcent-ils ou se contredisent-ils ? Une accroche dramatique suivie d'une démonstration plate crée une déception qui coûte plus cher que si l'accroche avait été neutre.":
        "Una vez puntuados los seis puntos, queda una pregunta: ¿los elementos se refuerzan o se contradicen? Un gancho dramático seguido de una demostración plana crea una decepción que sale más cara que si el gancho hubiera sido neutro.",
    "La grille à remplir en dix minutes": "La plantilla que se rellena en diez minutos",
    "Prends une vidéo qui performe dans ta niche et note chaque dimension sur {0}. Puis fais la même chose sur ta dernière vidéo. L'écart le plus grand entre les deux, c'est ton chantier prioritaire — pas celui qui te semble le plus urgent intuitivement.":
        "Coge un vídeo que funcione en tu nicho y puntúa cada dimensión sobre {0}. Luego haz lo mismo con tu último vídeo. La mayor diferencia entre ambos es tu prioridad, no la que te parece más urgente por intuición.",
    "Ce que l'analyse manuelle ne voit pas": "Lo que el análisis manual no ve",
    "Cette méthode fonctionne, mais elle a deux limites. D'abord, elle est lente : dix à quinze minutes par vidéo, ce qui rend impossible l'analyse d'un volume suffisant pour dégager un motif. Ensuite, elle est biaisée : on remarque ce qu'on connaît déjà, et on passe à côté de ce qu'on n'a jamais formalisé.":
        "Este método funciona, pero tiene dos límites. Primero es lento: de diez a quince minutos por vídeo, lo que hace imposible analizar el volumen necesario para que aparezca un patrón. Segundo está sesgado: uno se fija en lo que ya conoce y se le escapa lo que nunca ha puesto en palabras.",
    "C'est exactement ce que Qeerah automatise. L'outil analyse une vidéo à partir de son lien, image par image et bande son comprise, et rend les sept dimensions notées, les déclencheurs psychologiques détectés —":
        "Eso es exactamente lo que Qeerah automatiza. A partir de un enlace, la herramienta analiza el vídeo imagen por imagen, sonido incluido, y devuelve las siete dimensiones puntuadas, los disparadores psicológicos detectados",
    "et ceux qui manquent": "y los que faltan",
    "—, la seconde où l'attention décroche, puis des accroches réécrites pour ton produit.":
        "—, el segundo en el que se pierde la atención y, después, ganchos reescritos para tu producto.",
    "Analyse ta première vidéo maintenant": "Analiza tu primer vídeo ahora",
    "{0} jours d'accès complet, sans carte bancaire.": "{0} días de acceso completo, sin tarjeta.",
    "Coller un lien TikTok": "Pegar un enlace de TikTok",
    "Trois erreurs fréquentes": "Tres errores frecuentes",
    "Analyser des vidéos hors de sa niche.": "Analizar vídeos fuera de tu nicho.",
    "Les mécanismes qui vendent un accessoire de cuisine ne transposent pas tels quels sur un soin visage. Reste dans ta catégorie.":
        "Lo que vende un accesorio de cocina no se traslada tal cual a un tratamiento facial. Quédate en tu categoría.",
    "Se fier au nombre de vues.": "Fiarte del número de visualizaciones.",
    "Une vidéo à {0} millions de vues peut ne rien vendre. Cherche celles dont le produit est réellement écoulé, pas celles qui divertissent.":
        "Un vídeo con {0} millones de visualizaciones puede no vender nada. Busca aquellos cuyo producto se ha vendido de verdad, no los que entretienen.",
    "Changer plusieurs choses à la fois.": "Cambiar varias cosas a la vez.",
    "Si tu modifies l'accroche, le montage et l'appel à l'action en même temps, tu ne sauras jamais ce qui a produit l'effet. Une variable par test.":
        "Si cambias el gancho, el montaje y la llamada a la acción a la vez, nunca sabrás qué produjo el efecto. Una variable por prueba.",
    "Par où commencer concrètement": "Por dónde empezar en concreto",
    "Choisis cinq vidéos de ta niche publiées dans les trente derniers jours, dont le produit s'est visiblement vendu. Analyse-les l'une après l'autre. Tu verras apparaître deux ou trois constantes — un type d'accroche, un moment de démonstration, une formulation d'appel à l'action. Ce sont ces constantes que tu reproduis, pas les vidéos.":
        "Elige cinco vídeos de tu nicho publicados en los últimos treinta días cuyo producto se haya vendido claramente. Analízalos uno tras otro. Verás aparecer dos o tres constantes: un tipo de gancho, un momento de demostración, una forma de llamar a la acción. Son esas constantes lo que reproduces, no los vídeos.",
    "Ensuite seulement, applique-les à ton produit et publie. Compare la rétention obtenue à celle de tes vidéos précédentes. C'est le seul indicateur qui te dira si tu as compris le mécanisme ou seulement copié la surface.":
        "Solo después aplícalas a tu producto y publica. Compara la retención obtenida con la de tus vídeos anteriores. Es el único indicador que te dirá si has entendido el mecanismo o si solo has copiado la superficie.",
    "Ma vidéo ne fait pas de vues": "Mi vídeo no tiene visualizaciones",
    "Les produits qui vendent en France": "Los productos que venden en Francia",
    "Guide complet TikTok Shop": "Guía completa de TikTok Shop",
    "Source des chiffres :": "Fuente de las cifras:",
    ", données sur {0} jours arrêtées au {1} juillet {2}.": ", datos de {0} días a fecha de {1} de julio de {2}.",
}

T_LP_ANALYSER["it"] = {
    "Analyser une vidéo TikTok Shop : la méthode complète — Qeerah":
        "Analizzare un video TikTok Shop: il metodo completo — Qeerah",
    "Comment analyser une vidéo TikTok Shop pour comprendre pourquoi elle vend : accroche, rétention, déclencheurs, appel à l'action. Méthode manuelle et analyse automatique.":
        "Come analizzare un video TikTok Shop per capire perché vende: hook, ritenzione, leve, call to action. Metodo manuale e analisi automatica.",
    "Les sept dimensions à examiner sur une vidéo qui vend, et comment les reproduire sur ton produit.":
        "Le sette dimensioni da guardare in un video che vende, e come rifarle sul tuo prodotto.",
    "Tarifs": "Prezzi",
    "Ouvrir l'app →": "Apri l'app →",
    "Analyser une vidéo TikTok Shop : la méthode complète":
        "Analizzare un video TikTok Shop: il metodo completo",
    "Une vidéo qui vend n'est presque jamais un coup de chance. Elle empile des mécanismes précis, dans un ordre précis. Voici comment les repérer — à la main, puis automatiquement.":
        "Un video che vende non è quasi mai fortuna. Impila meccanismi precisi, in un ordine preciso. Ecco come individuarli: prima a mano, poi in automatico.",
    "Sur TikTok Shop France, ce sont les créateurs affiliés qui font tourner la boutique : ils représentent":
        "Su TikTok Shop in Francia sono i creator affiliati a far girare il negozio: valgono il",
    "{0} % du chiffre d'affaires généré": "{0} % del fatturato generato",
    "dans le pays au deuxième trimestre {0}, contre {1} % pour l'onglet Shopping Mall où les marques déposent simplement leur catalogue. Autrement dit, ce n'est pas le produit qui vend, c'est la vidéo. D'où l'intérêt de savoir décortiquer celles qui fonctionnent.":
        "nel paese nel secondo trimestre {0}, contro il {1} % della scheda Shopping Mall, dove i marchi si limitano a caricare il catalogo. In altre parole: non vende il prodotto, vende il video. Ecco perché conviene saper smontare quelli che funzionano.",
    "Pourquoi analyser plutôt que copier": "Perché analizzare invece di copiare",
    "Recopier une vidéo à l'identique ne marche pas : le produit change, l'audience change, le moment change. Ce qui se transfère, ce n'est pas le contenu, c'est la":
        "Ricopiare un video pari pari non funziona: cambia il prodotto, cambia il pubblico, cambia il momento. Quello che si trasferisce non è il contenuto, è la",
    "structure": "struttura",
    "— l'ordre dans lequel l'attention est captée, maintenue, puis convertie.":
        "— l'ordine in cui l'attenzione viene catturata, tenuta e poi convertita.",
    "Analyser une vidéo, c'est donc répondre à trois questions : qu'est-ce qui a retenu le spectateur les trois premières secondes, qu'est-ce qui l'a gardé jusqu'à l'argument de vente, et qu'est-ce qui l'a fait cliquer. Tout le reste — la lumière, le montage, la musique — sert ces trois moments.":
        "Analizzare un video vuol dire quindi rispondere a tre domande: cosa ha trattenuto lo spettatore nei primi tre secondi, cosa lo ha tenuto fino all'argomento di vendita e cosa lo ha fatto cliccare. Tutto il resto — luce, montaggio, musica — serve a questi tre momenti.",
    "Les sept dimensions à examiner": "Le sette dimensioni da esaminare",
    "{0}. L'accroche": "{0}. L'hook",
    "Regarde uniquement la première seconde et demie, son coupé. Le sujet est-il déjà identifiable ? Une bonne accroche nomme un problème, un résultat ou une contradiction avant que le spectateur ait le temps de décider de partir. Note le":
        "Guarda solo il primo secondo e mezzo, senza audio. L'argomento è già riconoscibile? Un buon hook nomina un problema, un risultato o una contraddizione prima che lo spettatore faccia in tempo a decidere di andarsene. Annota il",
    "type": "tipo",
    "d'accroche : question directe, affirmation clivante, avant/après, accusation douce (« tu fais ça tous les matins et… »).":
        "di hook: domanda diretta, affermazione divisiva, prima/dopo, accusa gentile («lo fai ogni mattina e…»).",
    "{0}. La rétention": "{0}. La ritenzione",
    "Compte les changements de plan et repère les « boucles ouvertes » : une promesse annoncée tôt et tenue plus tard, qui oblige à rester. Repère aussi le moment exact où toi, spectateur, tu as eu envie de partir. C'est presque toujours là que la courbe de rétention chute.":
        "Conta i cambi di inquadratura e cerca i «loop aperti»: una promessa fatta presto e mantenuta dopo, che obbliga a restare. Individua anche il momento esatto in cui tu, spettatore, hai avuto voglia di andartene. Quasi sempre è lì che crolla la curva di ritenzione.",
    "{0}. L'argumentaire de vente": "{0}. L'argomento di vendita",
    "Le produit est-il montré en usage réel ou en présentation statique ? Un seul bénéfice est-il martelé, ou une liste de caractéristiques est-elle récitée ? Les vidéos qui convertissent défendent généralement":
        "Il prodotto è mostrato in uso reale o in presentazione statica? Viene martellato un solo beneficio o recitata una lista di caratteristiche? I video che convertono di solito difendono",
    "un": "un",
    "bénéfice, très concret, illustré visuellement.": "beneficio, molto concreto, mostrato a schermo.",
    "{0}. L'émotion": "{0}. L'emozione",
    "Quelle émotion domine : frustration, soulagement, surprise, appartenance ? L'émotion n'est pas un supplément d'âme, c'est ce qui fixe le souvenir du produit. Une vidéo purement descriptive est oubliée en trois secondes.":
        "Quale emozione domina: frustrazione, sollievo, sorpresa, appartenenza? L'emozione non è un ornamento: è ciò che fissa il ricordo del prodotto. Un video puramente descrittivo si dimentica in tre secondi.",
    "{0}. La conversion": "{0}. La conversione",
    "Où se situe l'appel à l'action, et sous quelle forme ? Dit à voix haute, écrit à l'écran, les deux ? Arrive-t-il avant ou après la chute d'attention ? Un appel à l'action placé à la quinzième seconde d'une vidéo qui perd son audience à la douzième ne sert à rien, même parfaitement formulé.":
        "Dove si trova la call to action, e in che forma? Detta a voce, scritta a schermo, entrambe? Arriva prima o dopo il calo di attenzione? Una call to action al quindicesimo secondo di un video che perde il pubblico al dodicesimo non serve a nulla, per quanto ben scritta.",
    "{0}. Les signaux algorithmiques": "{0}. I segnali per l'algoritmo",
    "Format vertical plein cadre, texte à l'écran lisible sans le son, durée cohérente avec le sujet, son utilisé. Ces éléments ne font pas vendre directement, mais ils conditionnent la diffusion : une excellente vidéo mal formatée sera vue par peu de monde.":
        "Formato verticale a tutto schermo, testo leggibile senza audio, durata coerente con l'argomento, audio davvero usato. Nulla di tutto questo vende direttamente, ma decide la diffusione: un ottimo video formattato male lo vedranno in pochi.",
    "{0}. La cohérence d'ensemble": "{0}. La coerenza d'insieme",
    "Une fois les six points notés, une question demeure : les éléments se renforcent-ils ou se contredisent-ils ? Une accroche dramatique suivie d'une démonstration plate crée une déception qui coûte plus cher que si l'accroche avait été neutre.":
        "Una volta valutati i sei punti resta una domanda: gli elementi si rafforzano o si contraddicono? Un hook drammatico seguito da una dimostrazione piatta crea una delusione che costa più di un hook neutro.",
    "La grille à remplir en dix minutes": "La griglia da compilare in dieci minuti",
    "Prends une vidéo qui performe dans ta niche et note chaque dimension sur {0}. Puis fais la même chose sur ta dernière vidéo. L'écart le plus grand entre les deux, c'est ton chantier prioritaire — pas celui qui te semble le plus urgent intuitivement.":
        "Prendi un video che va forte nella tua nicchia e dai un voto su {0} a ogni dimensione. Poi fai lo stesso con il tuo ultimo video. Il divario più ampio è il tuo cantiere prioritario, non quello che d'istinto ti sembra più urgente.",
    "Ce que l'analyse manuelle ne voit pas": "Cosa non vede l'analisi manuale",
    "Cette méthode fonctionne, mais elle a deux limites. D'abord, elle est lente : dix à quinze minutes par vidéo, ce qui rend impossible l'analyse d'un volume suffisant pour dégager un motif. Ensuite, elle est biaisée : on remarque ce qu'on connaît déjà, et on passe à côté de ce qu'on n'a jamais formalisé.":
        "Il metodo funziona, ma ha due limiti. Primo, è lento: dieci-quindici minuti a video, troppo per analizzarne abbastanza da far emergere uno schema. Secondo, è di parte: si nota ciò che si conosce già e sfugge ciò che non si è mai messo in parole.",
    "C'est exactement ce que Qeerah automatise. L'outil analyse une vidéo à partir de son lien, image par image et bande son comprise, et rend les sept dimensions notées, les déclencheurs psychologiques détectés —":
        "È esattamente ciò che Qeerah automatizza. Da un link lo strumento analizza il video fotogramma per fotogramma, audio compreso, e restituisce le sette dimensioni valutate, le leve psicologiche rilevate —",
    "et ceux qui manquent": "e quelle che mancano",
    "—, la seconde où l'attention décroche, puis des accroches réécrites pour ton produit.":
        "—, il secondo in cui l'attenzione cade, e poi hook riscritti per il tuo prodotto.",
    "Analyse ta première vidéo maintenant": "Analizza subito il tuo primo video",
    "{0} jours d'accès complet, sans carte bancaire.": "{0} giorni di accesso completo, senza carta.",
    "Coller un lien TikTok": "Incolla un link TikTok",
    "Trois erreurs fréquentes": "Tre errori frequenti",
    "Analyser des vidéos hors de sa niche.": "Analizzare video fuori dalla propria nicchia.",
    "Les mécanismes qui vendent un accessoire de cuisine ne transposent pas tels quels sur un soin visage. Reste dans ta catégorie.":
        "Ciò che vende un accessorio da cucina non si trasferisce tale e quale a una crema viso. Resta nella tua categoria.",
    "Se fier au nombre de vues.": "Fidarsi del numero di visualizzazioni.",
    "Une vidéo à {0} millions de vues peut ne rien vendre. Cherche celles dont le produit est réellement écoulé, pas celles qui divertissent.":
        "Un video da {0} milioni di visualizzazioni può non vendere nulla. Cerca quelli il cui prodotto è davvero andato via, non quelli che intrattengono.",
    "Changer plusieurs choses à la fois.": "Cambiare più cose insieme.",
    "Si tu modifies l'accroche, le montage et l'appel à l'action en même temps, tu ne sauras jamais ce qui a produit l'effet. Une variable par test.":
        "Se cambi hook, montaggio e call to action nello stesso momento, non saprai mai cosa ha prodotto l'effetto. Una variabile per test.",
    "Par où commencer concrètement": "Da dove iniziare concretamente",
    "Choisis cinq vidéos de ta niche publiées dans les trente derniers jours, dont le produit s'est visiblement vendu. Analyse-les l'une après l'autre. Tu verras apparaître deux ou trois constantes — un type d'accroche, un moment de démonstration, une formulation d'appel à l'action. Ce sont ces constantes que tu reproduis, pas les vidéos.":
        "Scegli cinque video della tua nicchia pubblicati negli ultimi trenta giorni, il cui prodotto è chiaramente stato venduto. Analizzali uno dopo l'altro. Vedrai emergere due o tre costanti: un tipo di hook, un momento di dimostrazione, un modo di formulare la call to action. Sono quelle costanti che rifai, non i video.",
    "Ensuite seulement, applique-les à ton produit et publie. Compare la rétention obtenue à celle de tes vidéos précédentes. C'est le seul indicateur qui te dira si tu as compris le mécanisme ou seulement copié la surface.":
        "Solo dopo applicale al tuo prodotto e pubblica. Confronta la ritenzione ottenuta con quella dei tuoi video precedenti. È l'unico indicatore che ti dirà se hai capito il meccanismo o se hai solo copiato la superficie.",
    "Ma vidéo ne fait pas de vues": "Il mio video non fa visualizzazioni",
    "Les produits qui vendent en France": "I prodotti che vendono in Francia",
    "Guide complet TikTok Shop": "Guida completa a TikTok Shop",
    "Source des chiffres :": "Fonte dei dati:",
    ", données sur {0} jours arrêtées au {1} juillet {2}.": ", dati su {0} giorni aggiornati al {1} luglio {2}.",
}

T_LP_ANALYSER["pt-br"] = {
    "Analyser une vidéo TikTok Shop : la méthode complète — Qeerah":
        "Analisar um vídeo do TikTok Shop: o método completo — Qeerah",
    "Comment analyser une vidéo TikTok Shop pour comprendre pourquoi elle vend : accroche, rétention, déclencheurs, appel à l'action. Méthode manuelle et analyse automatique.":
        "Como analisar um vídeo do TikTok Shop para entender por que ele vende: gancho, retenção, gatilhos, chamada para ação. Método manual e análise automática.",
    "Les sept dimensions à examiner sur une vidéo qui vend, et comment les reproduire sur ton produit.":
        "As sete dimensões que você olha num vídeo que vende, e como repetir isso no seu produto.",
    "Tarifs": "Preços",
    "Ouvrir l'app →": "Abrir o app →",
    "Analyser une vidéo TikTok Shop : la méthode complète":
        "Analisar um vídeo do TikTok Shop: o método completo",
    "Une vidéo qui vend n'est presque jamais un coup de chance. Elle empile des mécanismes précis, dans un ordre précis. Voici comment les repérer — à la main, puis automatiquement.":
        "Um vídeo que vende quase nunca é sorte. Ele empilha mecanismos precisos, numa ordem precisa. Veja como identificá-los: primeiro na mão, depois no automático.",
    "Sur TikTok Shop France, ce sont les créateurs affiliés qui font tourner la boutique : ils représentent":
        "No TikTok Shop da França, são os criadores afiliados que fazem a loja girar: eles representam",
    "{0} % du chiffre d'affaires généré": "{0} % do faturamento gerado",
    "dans le pays au deuxième trimestre {0}, contre {1} % pour l'onglet Shopping Mall où les marques déposent simplement leur catalogue. Autrement dit, ce n'est pas le produit qui vend, c'est la vidéo. D'où l'intérêt de savoir décortiquer celles qui fonctionnent.":
        "no país no segundo trimestre de {0}, contra {1} % da aba Shopping Mall, onde as marcas só sobem o catálogo. Ou seja: não é o produto que vende, é o vídeo. Daí o interesse em saber desmontar os que funcionam.",
    "Pourquoi analyser plutôt que copier": "Por que analisar em vez de copiar",
    "Recopier une vidéo à l'identique ne marche pas : le produit change, l'audience change, le moment change. Ce qui se transfère, ce n'est pas le contenu, c'est la":
        "Copiar um vídeo igualzinho não funciona: o produto muda, o público muda, o momento muda. O que se transfere não é o conteúdo, é a",
    "structure": "estrutura",
    "— l'ordre dans lequel l'attention est captée, maintenue, puis convertie.":
        "— a ordem em que a atenção é capturada, mantida e depois convertida.",
    "Analyser une vidéo, c'est donc répondre à trois questions : qu'est-ce qui a retenu le spectateur les trois premières secondes, qu'est-ce qui l'a gardé jusqu'à l'argument de vente, et qu'est-ce qui l'a fait cliquer. Tout le reste — la lumière, le montage, la musique — sert ces trois moments.":
        "Analisar um vídeo é responder a três perguntas: o que segurou o espectador nos três primeiros segundos, o que o manteve até o argumento de venda e o que o fez clicar. Todo o resto — luz, montagem, música — está a serviço desses três momentos.",
    "Les sept dimensions à examiner": "As sete dimensões que você examina",
    "{0}. L'accroche": "{0}. O gancho",
    "Regarde uniquement la première seconde et demie, son coupé. Le sujet est-il déjà identifiable ? Une bonne accroche nomme un problème, un résultat ou une contradiction avant que le spectateur ait le temps de décider de partir. Note le":
        "Olhe só o primeiro segundo e meio, sem som. Dá pra saber do que se trata? Um bom gancho nomeia um problema, um resultado ou uma contradição antes de o espectador ter tempo de decidir sair. Anote o",
    "type": "tipo",
    "d'accroche : question directe, affirmation clivante, avant/après, accusation douce (« tu fais ça tous les matins et… »).":
        "de gancho: pergunta direta, afirmação polêmica, antes/depois, acusação leve (“você faz isso toda manhã e…”).",
    "{0}. La rétention": "{0}. A retenção",
    "Compte les changements de plan et repère les « boucles ouvertes » : une promesse annoncée tôt et tenue plus tard, qui oblige à rester. Repère aussi le moment exact où toi, spectateur, tu as eu envie de partir. C'est presque toujours là que la courbe de rétention chute.":
        "Conte os cortes e procure os “loops abertos”: uma promessa feita cedo e cumprida depois, que obriga a ficar. Marque também o momento exato em que você, como espectador, quis sair. É quase sempre ali que a curva de retenção cai.",
    "{0}. L'argumentaire de vente": "{0}. O argumento de venda",
    "Le produit est-il montré en usage réel ou en présentation statique ? Un seul bénéfice est-il martelé, ou une liste de caractéristiques est-elle récitée ? Les vidéos qui convertissent défendent généralement":
        "O produto aparece em uso real ou numa apresentação parada? Um único benefício é martelado ou uma lista de características é recitada? Os vídeos que convertem geralmente defendem",
    "un": "um",
    "bénéfice, très concret, illustré visuellement.": "benefício, bem concreto, mostrado na tela.",
    "{0}. L'émotion": "{0}. A emoção",
    "Quelle émotion domine : frustration, soulagement, surprise, appartenance ? L'émotion n'est pas un supplément d'âme, c'est ce qui fixe le souvenir du produit. Une vidéo purement descriptive est oubliée en trois secondes.":
        "Qual emoção domina: frustração, alívio, surpresa, pertencimento? Emoção não é enfeite — é o que fixa a lembrança do produto. Um vídeo só descritivo é esquecido em três segundos.",
    "{0}. La conversion": "{0}. A conversão",
    "Où se situe l'appel à l'action, et sous quelle forme ? Dit à voix haute, écrit à l'écran, les deux ? Arrive-t-il avant ou après la chute d'attention ? Un appel à l'action placé à la quinzième seconde d'une vidéo qui perd son audience à la douzième ne sert à rien, même parfaitement formulé.":
        "Onde está a chamada para ação, e em que forma? Falada, escrita na tela, as duas? Vem antes ou depois da queda de atenção? Uma chamada no segundo quinze de um vídeo que perde o público no doze não serve de nada, por melhor que seja a frase.",
    "{0}. Les signaux algorithmiques": "{0}. Os sinais para o algoritmo",
    "Format vertical plein cadre, texte à l'écran lisible sans le son, durée cohérente avec le sujet, son utilisé. Ces éléments ne font pas vendre directement, mais ils conditionnent la diffusion : une excellente vidéo mal formatée sera vue par peu de monde.":
        "Formato vertical em tela cheia, texto legível sem som, duração coerente com o assunto, som aproveitado. Nada disso vende direto, mas decide o alcance: um ótimo vídeo mal formatado será visto por pouca gente.",
    "{0}. La cohérence d'ensemble": "{0}. A coerência do conjunto",
    "Une fois les six points notés, une question demeure : les éléments se renforcent-ils ou se contredisent-ils ? Une accroche dramatique suivie d'une démonstration plate crée une déception qui coûte plus cher que si l'accroche avait été neutre.":
        "Com os seis pontos avaliados, resta uma pergunta: os elementos se reforçam ou se contradizem? Um gancho dramático seguido de uma demonstração morna cria uma decepção que custa mais caro do que um gancho neutro.",
    "La grille à remplir en dix minutes": "A grade que se preenche em dez minutos",
    "Prends une vidéo qui performe dans ta niche et note chaque dimension sur {0}. Puis fais la même chose sur ta dernière vidéo. L'écart le plus grand entre les deux, c'est ton chantier prioritaire — pas celui qui te semble le plus urgent intuitivement.":
        "Pegue um vídeo que vai bem no seu nicho e dê nota de {0} a cada dimensão. Depois faça o mesmo com o seu último vídeo. A maior diferença entre os dois é a sua prioridade — não a que parece mais urgente na intuição.",
    "Ce que l'analyse manuelle ne voit pas": "O que a análise manual não vê",
    "Cette méthode fonctionne, mais elle a deux limites. D'abord, elle est lente : dix à quinze minutes par vidéo, ce qui rend impossible l'analyse d'un volume suffisant pour dégager un motif. Ensuite, elle est biaisée : on remarque ce qu'on connaît déjà, et on passe à côté de ce qu'on n'a jamais formalisé.":
        "O método funciona, mas tem dois limites. Primeiro, é lento: dez a quinze minutos por vídeo, o que impede analisar volume suficiente para um padrão aparecer. Segundo, é enviesado: a gente nota o que já conhece e passa batido pelo que nunca colocou em palavras.",
    "C'est exactement ce que Qeerah automatise. L'outil analyse une vidéo à partir de son lien, image par image et bande son comprise, et rend les sept dimensions notées, les déclencheurs psychologiques détectés —":
        "É exatamente isso que a Qeerah automatiza. A partir de um link, a ferramenta analisa o vídeo quadro a quadro, com som, e devolve as sete dimensões com nota, os gatilhos psicológicos detectados —",
    "et ceux qui manquent": "e os que faltam",
    "—, la seconde où l'attention décroche, puis des accroches réécrites pour ton produit.":
        "—, o segundo em que a atenção cai e, depois, ganchos reescritos para o seu produto.",
    "Analyse ta première vidéo maintenant": "Analise seu primeiro vídeo agora",
    "{0} jours d'accès complet, sans carte bancaire.": "{0} dias de acesso completo, sem cartão.",
    "Coller un lien TikTok": "Colar um link do TikTok",
    "Trois erreurs fréquentes": "Três erros comuns",
    "Analyser des vidéos hors de sa niche.": "Analisar vídeos fora do seu nicho.",
    "Les mécanismes qui vendent un accessoire de cuisine ne transposent pas tels quels sur un soin visage. Reste dans ta catégorie.":
        "O que vende um acessório de cozinha não se transfere igual para um creme facial. Fique na sua categoria.",
    "Se fier au nombre de vues.": "Confiar no número de visualizações.",
    "Une vidéo à {0} millions de vues peut ne rien vendre. Cherche celles dont le produit est réellement écoulé, pas celles qui divertissent.":
        "Um vídeo com {0} milhões de visualizações pode não vender nada. Procure aqueles cujo produto realmente saiu, não os que entretêm.",
    "Changer plusieurs choses à la fois.": "Mudar várias coisas de uma vez.",
    "Si tu modifies l'accroche, le montage et l'appel à l'action en même temps, tu ne sauras jamais ce qui a produit l'effet. Une variable par test.":
        "Se você muda gancho, montagem e chamada para ação ao mesmo tempo, nunca vai saber o que causou o efeito. Uma variável por teste.",
    "Par où commencer concrètement": "Por onde começar na prática",
    "Choisis cinq vidéos de ta niche publiées dans les trente derniers jours, dont le produit s'est visiblement vendu. Analyse-les l'une après l'autre. Tu verras apparaître deux ou trois constantes — un type d'accroche, un moment de démonstration, une formulation d'appel à l'action. Ce sont ces constantes que tu reproduis, pas les vidéos.":
        "Escolha cinco vídeos do seu nicho publicados nos últimos trinta dias cujo produto visivelmente vendeu. Analise um depois do outro. Vão aparecer duas ou três constantes: um tipo de gancho, um momento de demonstração, um jeito de chamar para a ação. São essas constantes que você repete, não os vídeos.",
    "Ensuite seulement, applique-les à ton produit et publie. Compare la rétention obtenue à celle de tes vidéos précédentes. C'est le seul indicateur qui te dira si tu as compris le mécanisme ou seulement copié la surface.":
        "Só então aplique no seu produto e publique. Compare a retenção obtida com a dos seus vídeos anteriores. É o único indicador que diz se você entendeu o mecanismo ou só copiou a superfície.",
    "Ma vidéo ne fait pas de vues": "Meu vídeo não tem visualizações",
    "Les produits qui vendent en France": "Os produtos que vendem na França",
    "Guide complet TikTok Shop": "Guia completo do TikTok Shop",
    "Source des chiffres :": "Fonte dos números:",
    ", données sur {0} jours arrêtées au {1} juillet {2}.": ", dados de {0} dias com corte em {1} de julho de {2}.",
}

T_LP_ANALYSER["en-ie"] = dict(T_LP_ANALYSER["en"])
T_LP_ANALYSER["es-mx"] = dict(T_LP_ANALYSER["es"])


# ═══════════════════════════════════════════════════════════════════════════
# /produits-qui-vendent-tiktok-shop-france
# Page explicitement ancrée sur le marché FRANÇAIS. Les traductions le disent
# clairement plutôt que de laisser un lecteur allemand croire que ces chiffres
# et ces catégories sont ceux de son pays.
# ═══════════════════════════════════════════════════════════════════════════
T_LP_PRODUITS: dict[str, dict[str, str]] = {}

T_LP_PRODUITS["en"] = {
    "Les produits qui vendent sur TikTok Shop France en {0} — Qeerah":
        "The products that sell on TikTok Shop France in {0} — Qeerah",
    "Quelles catégories vendent vraiment sur TikTok Shop France : chiffres du marché, produits qui fonctionnent, et comment repérer un produit porteur avant les autres.":
        "Which categories really sell on TikTok Shop France: market figures, products that work, and how to spot a winner before everyone else.",
    "Les catégories qui dominent le marché français, et la méthode pour repérer un produit porteur avant qu'il ne sature.":
        "The categories that dominate the French market, and the method for spotting a strong product before it saturates.",
    "Tarifs": "Pricing",
    "Ouvrir l'app →": "Open the app →",
    "Les produits qui vendent sur TikTok Shop France en {0}":
        "The products that sell on TikTok Shop France in {0}",
    "Le marché français a passé le cap des {0} millions d'euros par trimestre. Voici ce qui s'y vend réellement, et comment repérer un produit porteur avant qu'il ne sature.":
        "The French market has passed €{0} million per quarter. Here's what actually sells there, and how to spot a strong product before it saturates.",
    "Où en est le marché français": "Where the French market stands",
    "TikTok Shop a ouvert en France le": "TikTok Shop opened in France on",
    "{0} mars {1}": "{0} March {1}",
    ", en même temps que l'Allemagne et l'Italie. Un peu plus d'un an plus tard, au deuxième trimestre {0}, le marché français a généré":
        ", at the same time as Germany and Italy. Just over a year later, in the second quarter of {0}, the French market generated",
    "{0} millions d'euros": "€{0} million",
    "de chiffre d'affaires, soit {0} % du total des quatre marchés européens mesurés — France, Allemagne, Espagne, Italie — qui pèsent ensemble près de {1} millions d'euros.":
        "in revenue, or {0}% of the total across the four European markets measured — France, Germany, Spain, Italy — which together come to nearly €{1} million.",
    "Le chiffre le plus important pour un créateur n'est pas celui-là. C'est celui-ci :":
        "That isn't the number that matters most to a creator. This one is:",
    "{0} % de ce chiffre d'affaires passe par les créateurs affiliés":
        "{0}% of that revenue goes through affiliate creators",
    "en France. Les marques qui déposent leur catalogue dans l'onglet Shopping Mall n'en captent que {0} %, et la vente en direct par les marques {1} %. La France est, sur ce point, plus dépendante des créateurs que la moyenne européenne, qui se situe à {2} %.":
        "in France. Brands that upload their catalogue to the Shopping Mall tab capture only {0}%, and brands selling live {1}%. On this point France leans on creators more than the European average, which sits at {2}%.",
    "Les catégories qui dominent": "The categories that dominate",
    "Catégorie": "Category",
    "Part du chiffre d'affaires français": "Share of French revenue",
    "Beauté et soins personnels": "Beauty and personal care",
    "Électroménager et appareils": "Home appliances and devices",
    "La beauté domine, ce qui n'a rien d'un hasard : c'est la catégorie où la démonstration visuelle est la plus convaincante. Un fond de teint qui s'applique à l'écran, une texture qui pénètre, un avant/après — la vidéo courte est le format naturel de ces produits.":
        "Beauty dominates, and that's no accident: it's the category where a visual demonstration convinces best. Foundation going on, a texture sinking in, a before/after — short video is the natural format for these products.",
    "L'électroménager en deuxième position surprend davantage. Il s'agit rarement de gros appareils, mais de petits objets qui règlent un problème visible en dix secondes : ustensiles de cuisine, appareils de nettoyage, accessoires de rangement. Le point commun avec la beauté est le même :":
        "Appliances in second place is more surprising. These are rarely big machines, but small objects that solve a visible problem in ten seconds: kitchen tools, cleaning devices, storage accessories. What they share with beauty is the same thing:",
    "le bénéfice se démontre à l'image": "the benefit can be shown on screen",
    "Le critère qui compte vraiment": "The criterion that really counts",
    "Avant de choisir un produit, pose-toi une seule question :": "Before choosing a product, ask yourself one question:",
    "est-ce que je peux montrer le bénéfice en moins de dix secondes, sans l'expliquer ?":
        "can I show the benefit in under ten seconds, without explaining it?",
    "Si la réponse est non, le produit peut être excellent, il sera difficile à vendre sur ce format. C'est ce critère, plus que la catégorie, qui sépare les produits qui fonctionnent des autres.":
        "If the answer is no, the product may be excellent but it will be hard to sell in this format. That criterion, more than the category, separates the products that work from the rest.",
    "Pourquoi les listes de « produits gagnants » vieillissent mal":
        "Why lists of “winning products” age badly",
    "Les articles qui listent dix produits à vendre ont un défaut structurel : au moment où tu les lis, ces produits sont déjà travaillés par des centaines de créateurs. La marge s'écrase, l'audience sature, et l'algorithme met en avant les vidéos les plus anciennes qui ont déjà accumulé de l'engagement.":
        "Articles listing ten products to sell have a built-in flaw: by the time you read them, hundreds of creators are already working those products. Margins get crushed, the audience saturates, and the algorithm favours the older videos that have already banked engagement.",
    "Ce qui reste utile, ce n'est pas la liste, c'est la": "What stays useful isn't the list, it's the",
    "méthode pour repérer un produit avant qu'il ne soit sur la liste":
        "method for spotting a product before it makes the list",
    ". Elle tient en trois signaux :": ". It comes down to three signals:",
    "Un produit qui apparaît chez plusieurs créateurs en même temps":
        "A product showing up with several creators at once",
    ", sans que ce soit une campagne payée visible. C'est souvent le signe qu'un fournisseur pousse et que le produit convertit.":
        ", with no visible paid campaign behind it. That's often a sign a supplier is pushing and the product converts.",
    "Un rapport vues/ventes anormalement bon.": "An unusually good views-to-sales ratio.",
    "Une vidéo à {0} vues qui écoule autant qu'une à {1} vues indique un produit qui déclenche l'achat, pas seulement la curiosité.":
        "A video with {0} views that shifts as much as one with {1} views points to a product that triggers a purchase, not just curiosity.",
    "Une catégorie en croissance mais pas encore encombrée.": "A category that's growing but not yet crowded.",
    "Surveiller les catégories secondaires plutôt que la beauté, déjà très concurrentielle.":
        "Watch the secondary categories rather than beauty, which is already fiercely contested.",
    "Comment repérer ces signaux sans y passer ses journées": "How to spot those signals without spending your days on it",
    "Les surveiller à la main suppose de parcourir des dizaines de vidéos par jour et de tenir un tableau. C'est précisément ce que le":
        "Watching them by hand means going through dozens of videos a day and keeping a spreadsheet. That is exactly what Qeerah's",
    "de Qeerah automatise : il remonte les vidéos TikTok Shop qui performent en ce moment, avec leur chiffre d'affaires estimé, sur neuf régions dont la France.":
        "automates: it surfaces the TikTok Shop videos performing right now, with their estimated revenue, across nine regions including France.",
    "Et une fois un produit repéré, l'étape suivante n'est pas de le copier, mais de comprendre":
        "And once a product is spotted, the next step isn't to copy it but to understand",
    "pourquoi": "why",
    "la vidéo qui le vend fonctionne — accroche, rétention, déclencheurs, appel à l'action. C'est l'objet de l'analyse vidéo.":
        "the video selling it works — hook, retention, triggers, call to action. That's what video analysis is for.",
    "Repère les produits qui décollent, et comprends pourquoi": "Spot the products taking off, and understand why",
    "{0} jours d'accès complet, sans carte bancaire.": "{0} days of full access, no card required.",
    "Essayer Qeerah": "Try Qeerah",
    "Trois pièges à éviter": "Three traps to avoid",
    "Choisir un produit parce qu'il te plaît.": "Choosing a product because you like it.",
    "Ton goût n'est pas un indicateur de marché. Le seul test valable est la démonstrabilité en dix secondes.":
        "Your taste is not a market indicator. The only valid test is whether it can be demonstrated in ten seconds.",
    "Arriver en fin de cycle.": "Arriving at the end of the cycle.",
    "Si un produit tourne depuis six semaines dans ton fil, la fenêtre est probablement fermée. Mieux vaut la catégorie voisine.":
        "If a product has been circling your feed for six weeks, the window is probably shut. The neighbouring category is a better bet.",
    "Négliger la marge.": "Ignoring the margin.",
    "Un produit à forte rotation mais à marge faible te fait travailler pour la plateforme. Calcule avant de tourner, pas après.":
        "A fast-moving product with a thin margin makes you work for the platform. Do the maths before filming, not after.",
    "Ce qu'il faut retenir": "What to take away",
    "Le marché français est jeune — un an d'existence — et largement porté par les créateurs, davantage que ses voisins européens. Cela signifie que la place est encore prenable, mais que la qualité de la vidéo compte plus que le catalogue : c'est elle qui fait {0} % du chiffre d'affaires.":
        "The French market is young — one year old — and carried by creators far more than its European neighbours. That means there's still room to take, but the quality of the video counts more than the catalogue: it's what drives {0}% of revenue.",
    "Concentre-toi sur des produits dont le bénéfice se voit, repère-les tôt, et travaille la structure de tes vidéos plutôt que d'accumuler les références.":
        "Focus on products whose benefit can be seen, spot them early, and work on the structure of your videos rather than piling up references.",
    "Analyser une vidéo TikTok Shop": "Analysing a TikTok Shop video",
    "Ma vidéo ne fait pas de vues": "My video isn't getting views",
    "TikTok Shop dans le monde": "TikTok Shop around the world",
    "Source des chiffres :": "Source of the figures:",
    ", mesure sur {0} jours arrêtée au {1} juillet {2}, portant sur la France, l'Allemagne, l'Espagne et l'Italie.":
        ", measured over {0} days as of {1} July {2}, covering France, Germany, Spain and Italy.",
}

T_LP_PRODUITS["de"] = {
    "Les produits qui vendent sur TikTok Shop France en {0} — Qeerah":
        "Die Produkte, die {0} auf TikTok Shop Frankreich verkaufen — Qeerah",
    "Quelles catégories vendent vraiment sur TikTok Shop France : chiffres du marché, produits qui fonctionnent, et comment repérer un produit porteur avant les autres.":
        "Welche Kategorien auf TikTok Shop Frankreich wirklich verkaufen: Marktzahlen, Produkte, die funktionieren, und wie du ein starkes Produkt vor allen anderen erkennst.",
    "Les catégories qui dominent le marché français, et la méthode pour repérer un produit porteur avant qu'il ne sature.":
        "Die Kategorien, die den französischen Markt bestimmen, und die Methode, ein starkes Produkt zu erkennen, bevor es gesättigt ist.",
    "Tarifs": "Preise",
    "Ouvrir l'app →": "App öffnen →",
    "Les produits qui vendent sur TikTok Shop France en {0}":
        "Die Produkte, die {0} auf TikTok Shop Frankreich verkaufen",
    "Le marché français a passé le cap des {0} millions d'euros par trimestre. Voici ce qui s'y vend réellement, et comment repérer un produit porteur avant qu'il ne sature.":
        "Der französische Markt hat die Marke von {0} Millionen Euro pro Quartal überschritten. Das verkauft sich dort wirklich — und so erkennst du ein starkes Produkt, bevor es gesättigt ist.",
    "Où en est le marché français": "Wo der französische Markt steht",
    "TikTok Shop a ouvert en France le": "TikTok Shop startete in Frankreich am",
    "{0} mars {1}": "{0}. März {1}",
    ", en même temps que l'Allemagne et l'Italie. Un peu plus d'un an plus tard, au deuxième trimestre {0}, le marché français a généré":
        ", zeitgleich mit Deutschland und Italien. Gut ein Jahr später, im zweiten Quartal {0}, erzielte der französische Markt",
    "{0} millions d'euros": "{0} Millionen Euro",
    "de chiffre d'affaires, soit {0} % du total des quatre marchés européens mesurés — France, Allemagne, Espagne, Italie — qui pèsent ensemble près de {1} millions d'euros.":
        "Umsatz, also {0} % der vier gemessenen europäischen Märkte — Frankreich, Deutschland, Spanien, Italien —, die zusammen knapp {1} Millionen Euro ausmachen.",
    "Le chiffre le plus important pour un créateur n'est pas celui-là. C'est celui-ci :":
        "Für einen Creator ist das nicht die wichtigste Zahl. Diese ist es:",
    "{0} % de ce chiffre d'affaires passe par les créateurs affiliés":
        "{0} % dieses Umsatzes laufen über Affiliate-Creators",
    "en France. Les marques qui déposent leur catalogue dans l'onglet Shopping Mall n'en captent que {0} %, et la vente en direct par les marques {1} %. La France est, sur ce point, plus dépendante des créateurs que la moyenne européenne, qui se situe à {2} %.":
        "in Frankreich. Marken, die ihren Katalog im Reiter Shopping Mall hochladen, holen nur {0} %, der Direktverkauf durch Marken {1} %. Frankreich hängt damit stärker an den Creators als der europäische Durchschnitt, der bei {2} % liegt.",
    "Les catégories qui dominent": "Die Kategorien, die dominieren",
    "Catégorie": "Kategorie",
    "Part du chiffre d'affaires français": "Anteil am französischen Umsatz",
    "Beauté et soins personnels": "Beauty und Körperpflege",
    "Électroménager et appareils": "Haushaltsgeräte und Geräte",
    "La beauté domine, ce qui n'a rien d'un hasard : c'est la catégorie où la démonstration visuelle est la plus convaincante. Un fond de teint qui s'applique à l'écran, une texture qui pénètre, un avant/après — la vidéo courte est le format naturel de ces produits.":
        "Beauty dominiert, und das ist kein Zufall: Hier überzeugt die Demonstration im Bild am stärksten. Eine Foundation, die aufgetragen wird, eine Textur, die einzieht, ein Vorher/Nachher — das kurze Video ist das natürliche Format dieser Produkte.",
    "L'électroménager en deuxième position surprend davantage. Il s'agit rarement de gros appareils, mais de petits objets qui règlent un problème visible en dix secondes : ustensiles de cuisine, appareils de nettoyage, accessoires de rangement. Le point commun avec la beauté est le même :":
        "Haushaltsgeräte auf Platz zwei überraschen mehr. Es geht selten um große Maschinen, sondern um kleine Dinge, die ein sichtbares Problem in zehn Sekunden lösen: Küchenhelfer, Reinigungsgeräte, Ordnungshelfer. Die Gemeinsamkeit mit Beauty ist dieselbe:",
    "le bénéfice se démontre à l'image": "der Nutzen lässt sich im Bild zeigen",
    "Le critère qui compte vraiment": "Das Kriterium, auf das es wirklich ankommt",
    "Avant de choisir un produit, pose-toi une seule question :": "Bevor du ein Produkt wählst, stell dir eine einzige Frage:",
    "est-ce que je peux montrer le bénéfice en moins de dix secondes, sans l'expliquer ?":
        "Kann ich den Nutzen in weniger als zehn Sekunden zeigen, ohne ihn zu erklären?",
    "Si la réponse est non, le produit peut être excellent, il sera difficile à vendre sur ce format. C'est ce critère, plus que la catégorie, qui sépare les produits qui fonctionnent des autres.":
        "Lautet die Antwort nein, mag das Produkt hervorragend sein — in diesem Format wird es schwer zu verkaufen. Dieses Kriterium trennt, mehr als die Kategorie, die Produkte, die funktionieren, von den anderen.",
    "Pourquoi les listes de « produits gagnants » vieillissent mal":
        "Warum Listen mit „Gewinnerprodukten“ schlecht altern",
    "Les articles qui listent dix produits à vendre ont un défaut structurel : au moment où tu les lis, ces produits sont déjà travaillés par des centaines de créateurs. La marge s'écrase, l'audience sature, et l'algorithme met en avant les vidéos les plus anciennes qui ont déjà accumulé de l'engagement.":
        "Artikel mit zehn Produkten zum Verkaufen haben einen eingebauten Fehler: Wenn du sie liest, bearbeiten hunderte Creators diese Produkte längst. Die Marge bricht ein, das Publikum ist gesättigt, und der Algorithmus schiebt die älteren Videos nach vorn, die schon Interaktionen gesammelt haben.",
    "Ce qui reste utile, ce n'est pas la liste, c'est la": "Nützlich bleibt nicht die Liste, sondern die",
    "méthode pour repérer un produit avant qu'il ne soit sur la liste":
        "Methode, ein Produkt zu erkennen, bevor es auf der Liste steht",
    ". Elle tient en trois signaux :": ". Sie besteht aus drei Signalen:",
    "Un produit qui apparaît chez plusieurs créateurs en même temps":
        "Ein Produkt, das bei mehreren Creators gleichzeitig auftaucht",
    ", sans que ce soit une campagne payée visible. C'est souvent le signe qu'un fournisseur pousse et que le produit convertit.":
        ", ohne erkennbare bezahlte Kampagne. Oft ein Zeichen, dass ein Lieferant pusht und das Produkt konvertiert.",
    "Un rapport vues/ventes anormalement bon.": "Ein auffällig gutes Verhältnis von Aufrufen zu Verkäufen.",
    "Une vidéo à {0} vues qui écoule autant qu'une à {1} vues indique un produit qui déclenche l'achat, pas seulement la curiosité.":
        "Ein Video mit {0} Aufrufen, das genauso viel absetzt wie eins mit {1}, deutet auf ein Produkt hin, das den Kauf auslöst und nicht nur Neugier.",
    "Une catégorie en croissance mais pas encore encombrée.": "Eine Kategorie, die wächst, aber noch nicht überfüllt ist.",
    "Surveiller les catégories secondaires plutôt que la beauté, déjà très concurrentielle.":
        "Beobachte die Nebenkategorien statt Beauty, wo der Wettbewerb schon hart ist.",
    "Comment repérer ces signaux sans y passer ses journées": "Wie du diese Signale erkennst, ohne Tage damit zu verbringen",
    "Les surveiller à la main suppose de parcourir des dizaines de vidéos par jour et de tenir un tableau. C'est précisément ce que le":
        "Von Hand hieße das, täglich Dutzende Videos durchzugehen und eine Tabelle zu pflegen. Genau das automatisiert der",
    "de Qeerah automatise : il remonte les vidéos TikTok Shop qui performent en ce moment, avec leur chiffre d'affaires estimé, sur neuf régions dont la France.":
        "von Qeerah: Er holt die TikTok-Shop-Videos hoch, die gerade laufen, mit geschätztem Umsatz, aus neun Regionen, Frankreich inklusive.",
    "Et une fois un produit repéré, l'étape suivante n'est pas de le copier, mais de comprendre":
        "Und ist ein Produkt erkannt, besteht der nächste Schritt nicht darin, es zu kopieren, sondern zu verstehen,",
    "pourquoi": "warum",
    "la vidéo qui le vend fonctionne — accroche, rétention, déclencheurs, appel à l'action. C'est l'objet de l'analyse vidéo.":
        "das Video, das es verkauft, funktioniert — Hook, Bindung, Auslöser, Call to Action. Genau dafür ist die Videoanalyse da.",
    "Repère les produits qui décollent, et comprends pourquoi": "Erkenne die Produkte, die durchstarten — und verstehe, warum",
    "{0} jours d'accès complet, sans carte bancaire.": "{0} Tage voller Zugang, ohne Kreditkarte.",
    "Essayer Qeerah": "Qeerah ausprobieren",
    "Trois pièges à éviter": "Drei Fallen, die du vermeidest",
    "Choisir un produit parce qu'il te plaît.": "Ein Produkt wählen, weil es dir gefällt.",
    "Ton goût n'est pas un indicateur de marché. Le seul test valable est la démonstrabilité en dix secondes.":
        "Dein Geschmack ist kein Marktindikator. Der einzig gültige Test ist, ob es sich in zehn Sekunden zeigen lässt.",
    "Arriver en fin de cycle.": "Am Ende des Zyklus ankommen.",
    "Si un produit tourne depuis six semaines dans ton fil, la fenêtre est probablement fermée. Mieux vaut la catégorie voisine.":
        "Wenn ein Produkt seit sechs Wochen durch deinen Feed läuft, ist das Fenster wahrscheinlich zu. Die Nachbarkategorie ist die bessere Wahl.",
    "Négliger la marge.": "Die Marge übersehen.",
    "Un produit à forte rotation mais à marge faible te fait travailler pour la plateforme. Calcule avant de tourner, pas après.":
        "Ein Produkt mit hohem Umschlag und dünner Marge lässt dich für die Plattform arbeiten. Rechne vor dem Dreh, nicht danach.",
    "Ce qu'il faut retenir": "Was du mitnimmst",
    "Le marché français est jeune — un an d'existence — et largement porté par les créateurs, davantage que ses voisins européens. Cela signifie que la place est encore prenable, mais que la qualité de la vidéo compte plus que le catalogue : c'est elle qui fait {0} % du chiffre d'affaires.":
        "Der französische Markt ist jung — ein Jahr alt — und wird stärker von Creators getragen als seine europäischen Nachbarn. Heißt: Der Platz ist noch zu holen, aber die Qualität des Videos zählt mehr als der Katalog — sie macht {0} % des Umsatzes.",
    "Concentre-toi sur des produits dont le bénéfice se voit, repère-les tôt, et travaille la structure de tes vidéos plutôt que d'accumuler les références.":
        "Konzentrier dich auf Produkte, deren Nutzen man sieht, erkenne sie früh, und arbeite an der Struktur deiner Videos, statt Artikel anzuhäufen.",
    "Analyser une vidéo TikTok Shop": "Ein TikTok-Shop-Video analysieren",
    "Ma vidéo ne fait pas de vues": "Mein Video bekommt keine Aufrufe",
    "TikTok Shop dans le monde": "TikTok Shop weltweit",
    "Source des chiffres :": "Quelle der Zahlen:",
    ", mesure sur {0} jours arrêtée au {1} juillet {2}, portant sur la France, l'Allemagne, l'Espagne et l'Italie.":
        ", gemessen über {0} Tage, Stand {1}. Juli {2}, für Frankreich, Deutschland, Spanien und Italien.",
}

T_LP_PRODUITS["es"] = {
    "Les produits qui vendent sur TikTok Shop France en {0} — Qeerah":
        "Los productos que venden en TikTok Shop Francia en {0} — Qeerah",
    "Quelles catégories vendent vraiment sur TikTok Shop France : chiffres du marché, produits qui fonctionnent, et comment repérer un produit porteur avant les autres.":
        "Qué categorías venden de verdad en TikTok Shop Francia: cifras del mercado, productos que funcionan y cómo detectar un producto ganador antes que los demás.",
    "Les catégories qui dominent le marché français, et la méthode pour repérer un produit porteur avant qu'il ne sature.":
        "Las categorías que dominan el mercado francés y el método para detectar un producto con recorrido antes de que se sature.",
    "Tarifs": "Precios",
    "Ouvrir l'app →": "Abrir la app →",
    "Les produits qui vendent sur TikTok Shop France en {0}":
        "Los productos que venden en TikTok Shop Francia en {0}",
    "Le marché français a passé le cap des {0} millions d'euros par trimestre. Voici ce qui s'y vend réellement, et comment repérer un produit porteur avant qu'il ne sature.":
        "El mercado francés ha superado los {0} millones de euros por trimestre. Esto es lo que se vende de verdad allí, y cómo detectar un producto con recorrido antes de que se sature.",
    "Où en est le marché français": "Cómo está el mercado francés",
    "TikTok Shop a ouvert en France le": "TikTok Shop abrió en Francia el",
    "{0} mars {1}": "{0} de marzo de {1}",
    ", en même temps que l'Allemagne et l'Italie. Un peu plus d'un an plus tard, au deuxième trimestre {0}, le marché français a généré":
        ", a la vez que Alemania e Italia. Poco más de un año después, en el segundo trimestre de {0}, el mercado francés generó",
    "{0} millions d'euros": "{0} millones de euros",
    "de chiffre d'affaires, soit {0} % du total des quatre marchés européens mesurés — France, Allemagne, Espagne, Italie — qui pèsent ensemble près de {1} millions d'euros.":
        "de facturación, o sea el {0} % del total de los cuatro mercados europeos medidos —Francia, Alemania, España, Italia—, que suman cerca de {1} millones de euros.",
    "Le chiffre le plus important pour un créateur n'est pas celui-là. C'est celui-ci :":
        "Para un creador, esa no es la cifra más importante. Esta sí:",
    "{0} % de ce chiffre d'affaires passe par les créateurs affiliés":
        "el {0} % de esa facturación pasa por los creadores afiliados",
    "en France. Les marques qui déposent leur catalogue dans l'onglet Shopping Mall n'en captent que {0} %, et la vente en direct par les marques {1} %. La France est, sur ce point, plus dépendante des créateurs que la moyenne européenne, qui se situe à {2} %.":
        "en Francia. Las marcas que suben su catálogo a la pestaña Shopping Mall solo captan el {0} %, y la venta directa de las marcas el {1} %. En esto, Francia depende de los creadores más que la media europea, que está en el {2} %.",
    "Les catégories qui dominent": "Las categorías que dominan",
    "Catégorie": "Categoría",
    "Part du chiffre d'affaires français": "Parte de la facturación francesa",
    "Beauté et soins personnels": "Belleza y cuidado personal",
    "Électroménager et appareils": "Electrodomésticos y aparatos",
    "La beauté domine, ce qui n'a rien d'un hasard : c'est la catégorie où la démonstration visuelle est la plus convaincante. Un fond de teint qui s'applique à l'écran, une texture qui pénètre, un avant/après — la vidéo courte est le format naturel de ces produits.":
        "La belleza domina, y no es casualidad: es la categoría donde la demostración visual convence más. Una base que se aplica en pantalla, una textura que penetra, un antes/después: el vídeo corto es el formato natural de estos productos.",
    "L'électroménager en deuxième position surprend davantage. Il s'agit rarement de gros appareils, mais de petits objets qui règlent un problème visible en dix secondes : ustensiles de cuisine, appareils de nettoyage, accessoires de rangement. Le point commun avec la beauté est le même :":
        "Los electrodomésticos en segundo lugar sorprenden más. Rara vez son grandes aparatos, sino objetos pequeños que resuelven un problema visible en diez segundos: utensilios de cocina, aparatos de limpieza, accesorios de orden. Lo que comparten con la belleza es lo mismo:",
    "le bénéfice se démontre à l'image": "el beneficio se demuestra en imagen",
    "Le critère qui compte vraiment": "El criterio que de verdad cuenta",
    "Avant de choisir un produit, pose-toi une seule question :": "Antes de elegir un producto, hazte una sola pregunta:",
    "est-ce que je peux montrer le bénéfice en moins de dix secondes, sans l'expliquer ?":
        "¿puedo mostrar el beneficio en menos de diez segundos, sin explicarlo?",
    "Si la réponse est non, le produit peut être excellent, il sera difficile à vendre sur ce format. C'est ce critère, plus que la catégorie, qui sépare les produits qui fonctionnent des autres.":
        "Si la respuesta es no, el producto puede ser excelente, pero será difícil de vender en este formato. Ese criterio, más que la categoría, separa los productos que funcionan del resto.",
    "Pourquoi les listes de « produits gagnants » vieillissent mal":
        "Por qué las listas de «productos ganadores» envejecen mal",
    "Les articles qui listent dix produits à vendre ont un défaut structurel : au moment où tu les lis, ces produits sont déjà travaillés par des centaines de créateurs. La marge s'écrase, l'audience sature, et l'algorithme met en avant les vidéos les plus anciennes qui ont déjà accumulé de l'engagement.":
        "Los artículos que enumeran diez productos para vender tienen un fallo de origen: cuando los lees, cientos de creadores ya están trabajando esos productos. El margen se hunde, el público se satura y el algoritmo saca adelante los vídeos más antiguos, que ya han acumulado interacción.",
    "Ce qui reste utile, ce n'est pas la liste, c'est la": "Lo que sigue siendo útil no es la lista, es el",
    "méthode pour repérer un produit avant qu'il ne soit sur la liste":
        "método para detectar un producto antes de que llegue a la lista",
    ". Elle tient en trois signaux :": ". Se resume en tres señales:",
    "Un produit qui apparaît chez plusieurs créateurs en même temps":
        "Un producto que aparece en varios creadores a la vez",
    ", sans que ce soit une campagne payée visible. C'est souvent le signe qu'un fournisseur pousse et que le produit convertit.":
        ", sin que se vea una campaña pagada detrás. Suele ser señal de que un proveedor empuja y de que el producto convierte.",
    "Un rapport vues/ventes anormalement bon.": "Una relación visualizaciones/ventas anormalmente buena.",
    "Une vidéo à {0} vues qui écoule autant qu'une à {1} vues indique un produit qui déclenche l'achat, pas seulement la curiosité.":
        "Un vídeo con {0} visualizaciones que vende tanto como uno con {1} indica un producto que dispara la compra, no solo la curiosidad.",
    "Une catégorie en croissance mais pas encore encombrée.": "Una categoría que crece pero aún no está saturada.",
    "Surveiller les catégories secondaires plutôt que la beauté, déjà très concurrentielle.":
        "Vigila las categorías secundarias en lugar de la belleza, ya muy competida.",
    "Comment repérer ces signaux sans y passer ses journées": "Cómo detectar estas señales sin dedicarle el día entero",
    "Les surveiller à la main suppose de parcourir des dizaines de vidéos par jour et de tenir un tableau. C'est précisément ce que le":
        "Vigilarlas a mano supone repasar decenas de vídeos al día y llevar una hoja de cálculo. Eso es justo lo que automatiza el",
    "de Qeerah automatise : il remonte les vidéos TikTok Shop qui performent en ce moment, avec leur chiffre d'affaires estimé, sur neuf régions dont la France.":
        "de Qeerah: saca a la superficie los vídeos de TikTok Shop que están funcionando ahora, con su facturación estimada, en nueve regiones, Francia incluida.",
    "Et une fois un produit repéré, l'étape suivante n'est pas de le copier, mais de comprendre":
        "Y una vez detectado un producto, el siguiente paso no es copiarlo, sino entender",
    "pourquoi": "por qué",
    "la vidéo qui le vend fonctionne — accroche, rétention, déclencheurs, appel à l'action. C'est l'objet de l'analyse vidéo.":
        "funciona el vídeo que lo vende: gancho, retención, disparadores, llamada a la acción. De eso trata el análisis de vídeo.",
    "Repère les produits qui décollent, et comprends pourquoi": "Detecta los productos que despegan y entiende por qué",
    "{0} jours d'accès complet, sans carte bancaire.": "{0} días de acceso completo, sin tarjeta.",
    "Essayer Qeerah": "Probar Qeerah",
    "Trois pièges à éviter": "Tres trampas que evitar",
    "Choisir un produit parce qu'il te plaît.": "Elegir un producto porque te gusta.",
    "Ton goût n'est pas un indicateur de marché. Le seul test valable est la démonstrabilité en dix secondes.":
        "Tu gusto no es un indicador de mercado. La única prueba válida es si se puede demostrar en diez segundos.",
    "Arriver en fin de cycle.": "Llegar al final del ciclo.",
    "Si un produit tourne depuis six semaines dans ton fil, la fenêtre est probablement fermée. Mieux vaut la catégorie voisine.":
        "Si un producto lleva seis semanas dando vueltas en tu feed, la ventana probablemente esté cerrada. Mejor la categoría vecina.",
    "Négliger la marge.": "Descuidar el margen.",
    "Un produit à forte rotation mais à marge faible te fait travailler pour la plateforme. Calcule avant de tourner, pas après.":
        "Un producto de mucha rotación pero poco margen te hace trabajar para la plataforma. Haz las cuentas antes de grabar, no después.",
    "Ce qu'il faut retenir": "Lo que hay que retener",
    "Le marché français est jeune — un an d'existence — et largement porté par les créateurs, davantage que ses voisins européens. Cela signifie que la place est encore prenable, mais que la qualité de la vidéo compte plus que le catalogue : c'est elle qui fait {0} % du chiffre d'affaires.":
        "El mercado francés es joven —un año de vida— y se apoya en los creadores más que sus vecinos europeos. Significa que aún hay sitio que ganar, pero que la calidad del vídeo pesa más que el catálogo: es ella la que hace el {0} % de la facturación.",
    "Concentre-toi sur des produits dont le bénéfice se voit, repère-les tôt, et travaille la structure de tes vidéos plutôt que d'accumuler les références.":
        "Céntrate en productos cuyo beneficio se ve, detéctalos pronto y trabaja la estructura de tus vídeos en lugar de acumular referencias.",
    "Analyser une vidéo TikTok Shop": "Analizar un vídeo de TikTok Shop",
    "Ma vidéo ne fait pas de vues": "Mi vídeo no tiene visualizaciones",
    "TikTok Shop dans le monde": "TikTok Shop en el mundo",
    "Source des chiffres :": "Fuente de las cifras:",
    ", mesure sur {0} jours arrêtée au {1} juillet {2}, portant sur la France, l'Allemagne, l'Espagne et l'Italie.":
        ", medición de {0} días a fecha de {1} de julio de {2}, sobre Francia, Alemania, España e Italia.",
}

T_LP_PRODUITS["it"] = {
    "Les produits qui vendent sur TikTok Shop France en {0} — Qeerah":
        "I prodotti che vendono su TikTok Shop Francia nel {0} — Qeerah",
    "Quelles catégories vendent vraiment sur TikTok Shop France : chiffres du marché, produits qui fonctionnent, et comment repérer un produit porteur avant les autres.":
        "Quali categorie vendono davvero su TikTok Shop Francia: numeri del mercato, prodotti che funzionano e come individuare un prodotto vincente prima degli altri.",
    "Les catégories qui dominent le marché français, et la méthode pour repérer un produit porteur avant qu'il ne sature.":
        "Le categorie che dominano il mercato francese e il metodo per individuare un prodotto valido prima che si saturi.",
    "Tarifs": "Prezzi",
    "Ouvrir l'app →": "Apri l'app →",
    "Les produits qui vendent sur TikTok Shop France en {0}":
        "I prodotti che vendono su TikTok Shop Francia nel {0}",
    "Le marché français a passé le cap des {0} millions d'euros par trimestre. Voici ce qui s'y vend réellement, et comment repérer un produit porteur avant qu'il ne sature.":
        "Il mercato francese ha superato i {0} milioni di euro a trimestre. Ecco cosa ci si vende davvero e come individuare un prodotto valido prima che si saturi.",
    "Où en est le marché français": "A che punto è il mercato francese",
    "TikTok Shop a ouvert en France le": "TikTok Shop è partito in Francia il",
    "{0} mars {1}": "{0} marzo {1}",
    ", en même temps que l'Allemagne et l'Italie. Un peu plus d'un an plus tard, au deuxième trimestre {0}, le marché français a généré":
        ", insieme a Germania e Italia. Poco più di un anno dopo, nel secondo trimestre {0}, il mercato francese ha generato",
    "{0} millions d'euros": "{0} milioni di euro",
    "de chiffre d'affaires, soit {0} % du total des quatre marchés européens mesurés — France, Allemagne, Espagne, Italie — qui pèsent ensemble près de {1} millions d'euros.":
        "di fatturato, cioè il {0} % del totale dei quattro mercati europei misurati — Francia, Germania, Spagna, Italia — che insieme valgono quasi {1} milioni di euro.",
    "Le chiffre le plus important pour un créateur n'est pas celui-là. C'est celui-ci :":
        "Per un creator il numero più importante non è quello. È questo:",
    "{0} % de ce chiffre d'affaires passe par les créateurs affiliés":
        "il {0} % di quel fatturato passa dai creator affiliati",
    "en France. Les marques qui déposent leur catalogue dans l'onglet Shopping Mall n'en captent que {0} %, et la vente en direct par les marques {1} %. La France est, sur ce point, plus dépendante des créateurs que la moyenne européenne, qui se situe à {2} %.":
        "in Francia. I marchi che caricano il catalogo nella scheda Shopping Mall ne prendono solo il {0} %, e la vendita diretta dei marchi il {1} %. Su questo la Francia dipende dai creator più della media europea, ferma al {2} %.",
    "Les catégories qui dominent": "Le categorie che dominano",
    "Catégorie": "Categoria",
    "Part du chiffre d'affaires français": "Quota del fatturato francese",
    "Beauté et soins personnels": "Bellezza e cura della persona",
    "Électroménager et appareils": "Elettrodomestici e dispositivi",
    "La beauté domine, ce qui n'a rien d'un hasard : c'est la catégorie où la démonstration visuelle est la plus convaincante. Un fond de teint qui s'applique à l'écran, une texture qui pénètre, un avant/après — la vidéo courte est le format naturel de ces produits.":
        "La bellezza domina, e non è un caso: è la categoria in cui la dimostrazione visiva convince di più. Un fondotinta che si stende a schermo, una texture che si assorbe, un prima/dopo — il video breve è il formato naturale di questi prodotti.",
    "L'électroménager en deuxième position surprend davantage. Il s'agit rarement de gros appareils, mais de petits objets qui règlent un problème visible en dix secondes : ustensiles de cuisine, appareils de nettoyage, accessoires de rangement. Le point commun avec la beauté est le même :":
        "Gli elettrodomestici al secondo posto sorprendono di più. Raramente si tratta di grandi apparecchi, ma di piccoli oggetti che risolvono un problema visibile in dieci secondi: utensili da cucina, apparecchi per la pulizia, accessori per l'ordine. Ciò che li accomuna alla bellezza è lo stesso:",
    "le bénéfice se démontre à l'image": "il beneficio si dimostra a schermo",
    "Le critère qui compte vraiment": "Il criterio che conta davvero",
    "Avant de choisir un produit, pose-toi une seule question :": "Prima di scegliere un prodotto, fatti una sola domanda:",
    "est-ce que je peux montrer le bénéfice en moins de dix secondes, sans l'expliquer ?":
        "posso mostrare il beneficio in meno di dieci secondi, senza spiegarlo?",
    "Si la réponse est non, le produit peut être excellent, il sera difficile à vendre sur ce format. C'est ce critère, plus que la catégorie, qui sépare les produits qui fonctionnent des autres.":
        "Se la risposta è no, il prodotto può essere ottimo ma sarà difficile da vendere in questo formato. È questo criterio, più della categoria, a separare i prodotti che funzionano dagli altri.",
    "Pourquoi les listes de « produits gagnants » vieillissent mal":
        "Perché le liste di «prodotti vincenti» invecchiano male",
    "Les articles qui listent dix produits à vendre ont un défaut structurel : au moment où tu les lis, ces produits sont déjà travaillés par des centaines de créateurs. La marge s'écrase, l'audience sature, et l'algorithme met en avant les vidéos les plus anciennes qui ont déjà accumulé de l'engagement.":
        "Gli articoli che elencano dieci prodotti da vendere hanno un difetto di fondo: quando li leggi, centinaia di creator ci stanno già lavorando. Il margine crolla, il pubblico si satura e l'algoritmo spinge i video più vecchi, che hanno già accumulato interazioni.",
    "Ce qui reste utile, ce n'est pas la liste, c'est la": "Quel che resta utile non è la lista, è il",
    "méthode pour repérer un produit avant qu'il ne soit sur la liste":
        "metodo per individuare un prodotto prima che finisca in lista",
    ". Elle tient en trois signaux :": ". Si riduce a tre segnali:",
    "Un produit qui apparaît chez plusieurs créateurs en même temps":
        "Un prodotto che compare da più creator nello stesso momento",
    ", sans que ce soit une campagne payée visible. C'est souvent le signe qu'un fournisseur pousse et que le produit convertit.":
        ", senza una campagna a pagamento visibile. Spesso è il segno che un fornitore sta spingendo e che il prodotto converte.",
    "Un rapport vues/ventes anormalement bon.": "Un rapporto visualizzazioni/vendite insolitamente buono.",
    "Une vidéo à {0} vues qui écoule autant qu'une à {1} vues indique un produit qui déclenche l'achat, pas seulement la curiosité.":
        "Un video da {0} visualizzazioni che vende quanto uno da {1} indica un prodotto che innesca l'acquisto, non solo la curiosità.",
    "Une catégorie en croissance mais pas encore encombrée.": "Una categoria in crescita ma non ancora affollata.",
    "Surveiller les catégories secondaires plutôt que la beauté, déjà très concurrentielle.":
        "Tieni d'occhio le categorie secondarie invece della bellezza, già molto competitiva.",
    "Comment repérer ces signaux sans y passer ses journées": "Come cogliere questi segnali senza passarci le giornate",
    "Les surveiller à la main suppose de parcourir des dizaines de vidéos par jour et de tenir un tableau. C'est précisément ce que le":
        "Seguirli a mano vuol dire scorrere decine di video al giorno e tenere un foglio di calcolo. È esattamente ciò che automatizza il",
    "de Qeerah automatise : il remonte les vidéos TikTok Shop qui performent en ce moment, avec leur chiffre d'affaires estimé, sur neuf régions dont la France.":
        "di Qeerah: fa emergere i video TikTok Shop che stanno andando forte adesso, con il fatturato stimato, su nove regioni tra cui la Francia.",
    "Et une fois un produit repéré, l'étape suivante n'est pas de le copier, mais de comprendre":
        "E una volta individuato un prodotto, il passo successivo non è copiarlo ma capire",
    "pourquoi": "perché",
    "la vidéo qui le vend fonctionne — accroche, rétention, déclencheurs, appel à l'action. C'est l'objet de l'analyse vidéo.":
        "il video che lo vende funziona — hook, ritenzione, leve, call to action. È a questo che serve l'analisi video.",
    "Repère les produits qui décollent, et comprends pourquoi": "Individua i prodotti che decollano e capisci perché",
    "{0} jours d'accès complet, sans carte bancaire.": "{0} giorni di accesso completo, senza carta.",
    "Essayer Qeerah": "Prova Qeerah",
    "Trois pièges à éviter": "Tre trappole da evitare",
    "Choisir un produit parce qu'il te plaît.": "Scegliere un prodotto perché piace a te.",
    "Ton goût n'est pas un indicateur de marché. Le seul test valable est la démonstrabilité en dix secondes.":
        "Il tuo gusto non è un indicatore di mercato. L'unico test valido è se si può dimostrare in dieci secondi.",
    "Arriver en fin de cycle.": "Arrivare a fine ciclo.",
    "Si un produit tourne depuis six semaines dans ton fil, la fenêtre est probablement fermée. Mieux vaut la catégorie voisine.":
        "Se un prodotto gira nel tuo feed da sei settimane, la finestra è probabilmente chiusa. Meglio la categoria vicina.",
    "Négliger la marge.": "Trascurare il margine.",
    "Un produit à forte rotation mais à marge faible te fait travailler pour la plateforme. Calcule avant de tourner, pas après.":
        "Un prodotto ad alta rotazione ma con margine basso ti fa lavorare per la piattaforma. Fai i conti prima di girare, non dopo.",
    "Ce qu'il faut retenir": "Cosa portarsi a casa",
    "Le marché français est jeune — un an d'existence — et largement porté par les créateurs, davantage que ses voisins européens. Cela signifie que la place est encore prenable, mais que la qualité de la vidéo compte plus que le catalogue : c'est elle qui fait {0} % du chiffre d'affaires.":
        "Il mercato francese è giovane — un anno di vita — e si regge sui creator più dei vicini europei. Vuol dire che lo spazio è ancora conquistabile, ma che la qualità del video conta più del catalogo: è lei a fare il {0} % del fatturato.",
    "Concentre-toi sur des produits dont le bénéfice se voit, repère-les tôt, et travaille la structure de tes vidéos plutôt que d'accumuler les références.":
        "Concentrati su prodotti il cui beneficio si vede, individuali presto e lavora sulla struttura dei tuoi video invece di accumulare referenze.",
    "Analyser une vidéo TikTok Shop": "Analizzare un video TikTok Shop",
    "Ma vidéo ne fait pas de vues": "Il mio video non fa visualizzazioni",
    "TikTok Shop dans le monde": "TikTok Shop nel mondo",
    "Source des chiffres :": "Fonte dei dati:",
    ", mesure sur {0} jours arrêtée au {1} juillet {2}, portant sur la France, l'Allemagne, l'Espagne et l'Italie.":
        ", rilevazione su {0} giorni al {1} luglio {2}, su Francia, Germania, Spagna e Italia.",
}

T_LP_PRODUITS["pt-br"] = {
    "Les produits qui vendent sur TikTok Shop France en {0} — Qeerah":
        "Os produtos que vendem no TikTok Shop da França em {0} — Qeerah",
    "Quelles catégories vendent vraiment sur TikTok Shop France : chiffres du marché, produits qui fonctionnent, et comment repérer un produit porteur avant les autres.":
        "Quais categorias vendem de verdade no TikTok Shop da França: números do mercado, produtos que funcionam e como achar um produto forte antes dos outros.",
    "Les catégories qui dominent le marché français, et la méthode pour repérer un produit porteur avant qu'il ne sature.":
        "As categorias que dominam o mercado francês e o método para achar um produto forte antes que ele sature.",
    "Tarifs": "Preços",
    "Ouvrir l'app →": "Abrir o app →",
    "Les produits qui vendent sur TikTok Shop France en {0}":
        "Os produtos que vendem no TikTok Shop da França em {0}",
    "Le marché français a passé le cap des {0} millions d'euros par trimestre. Voici ce qui s'y vend réellement, et comment repérer un produit porteur avant qu'il ne sature.":
        "O mercado francês passou dos {0} milhões de euros por trimestre. Veja o que realmente vende lá e como achar um produto forte antes que ele sature.",
    "Où en est le marché français": "Como está o mercado francês",
    "TikTok Shop a ouvert en France le": "O TikTok Shop abriu na França em",
    "{0} mars {1}": "{0} de março de {1}",
    ", en même temps que l'Allemagne et l'Italie. Un peu plus d'un an plus tard, au deuxième trimestre {0}, le marché français a généré":
        ", junto com Alemanha e Itália. Pouco mais de um ano depois, no segundo trimestre de {0}, o mercado francês gerou",
    "{0} millions d'euros": "{0} milhões de euros",
    "de chiffre d'affaires, soit {0} % du total des quatre marchés européens mesurés — France, Allemagne, Espagne, Italie — qui pèsent ensemble près de {1} millions d'euros.":
        "de faturamento, ou seja {0} % do total dos quatro mercados europeus medidos — França, Alemanha, Espanha, Itália —, que juntos somam quase {1} milhões de euros.",
    "Le chiffre le plus important pour un créateur n'est pas celui-là. C'est celui-ci :":
        "Para um criador, o número mais importante não é esse. É este:",
    "{0} % de ce chiffre d'affaires passe par les créateurs affiliés":
        "{0} % desse faturamento passa pelos criadores afiliados",
    "en France. Les marques qui déposent leur catalogue dans l'onglet Shopping Mall n'en captent que {0} %, et la vente en direct par les marques {1} %. La France est, sur ce point, plus dépendante des créateurs que la moyenne européenne, qui se situe à {2} %.":
        "na França. As marcas que sobem o catálogo na aba Shopping Mall ficam com só {0} %, e a venda direta das marcas com {1} %. Nesse ponto a França depende mais dos criadores do que a média europeia, que está em {2} %.",
    "Les catégories qui dominent": "As categorias que dominam",
    "Catégorie": "Categoria",
    "Part du chiffre d'affaires français": "Fatia do faturamento francês",
    "Beauté et soins personnels": "Beleza e cuidados pessoais",
    "Électroménager et appareils": "Eletrodomésticos e aparelhos",
    "La beauté domine, ce qui n'a rien d'un hasard : c'est la catégorie où la démonstration visuelle est la plus convaincante. Un fond de teint qui s'applique à l'écran, une texture qui pénètre, un avant/après — la vidéo courte est le format naturel de ces produits.":
        "A beleza domina, e não é por acaso: é a categoria em que a demonstração visual convence mais. Uma base sendo aplicada na tela, uma textura que absorve, um antes/depois — o vídeo curto é o formato natural desses produtos.",
    "L'électroménager en deuxième position surprend davantage. Il s'agit rarement de gros appareils, mais de petits objets qui règlent un problème visible en dix secondes : ustensiles de cuisine, appareils de nettoyage, accessoires de rangement. Le point commun avec la beauté est le même :":
        "Os eletrodomésticos em segundo lugar surpreendem mais. Raramente são aparelhos grandes, e sim objetos pequenos que resolvem um problema visível em dez segundos: utensílios de cozinha, aparelhos de limpeza, acessórios de organização. O que eles têm em comum com a beleza é o mesmo:",
    "le bénéfice se démontre à l'image": "o benefício se mostra na imagem",
    "Le critère qui compte vraiment": "O critério que realmente conta",
    "Avant de choisir un produit, pose-toi une seule question :": "Antes de escolher um produto, faça uma única pergunta:",
    "est-ce que je peux montrer le bénéfice en moins de dix secondes, sans l'expliquer ?":
        "consigo mostrar o benefício em menos de dez segundos, sem explicar?",
    "Si la réponse est non, le produit peut être excellent, il sera difficile à vendre sur ce format. C'est ce critère, plus que la catégorie, qui sépare les produits qui fonctionnent des autres.":
        "Se a resposta for não, o produto pode ser ótimo, mas vai ser difícil de vender nesse formato. É esse critério, mais do que a categoria, que separa os produtos que funcionam dos outros.",
    "Pourquoi les listes de « produits gagnants » vieillissent mal":
        "Por que as listas de “produtos vencedores” envelhecem mal",
    "Les articles qui listent dix produits à vendre ont un défaut structurel : au moment où tu les lis, ces produits sont déjà travaillés par des centaines de créateurs. La marge s'écrase, l'audience sature, et l'algorithme met en avant les vidéos les plus anciennes qui ont déjà accumulé de l'engagement.":
        "Os artigos que listam dez produtos para vender têm um defeito de origem: quando você lê, centenas de criadores já estão em cima desses produtos. A margem despenca, o público satura e o algoritmo empurra os vídeos mais antigos, que já acumularam engajamento.",
    "Ce qui reste utile, ce n'est pas la liste, c'est la": "O que continua útil não é a lista, é o",
    "méthode pour repérer un produit avant qu'il ne soit sur la liste":
        "método para achar um produto antes de ele entrar na lista",
    ". Elle tient en trois signaux :": ". Resume-se a três sinais:",
    "Un produit qui apparaît chez plusieurs créateurs en même temps":
        "Um produto que aparece em vários criadores ao mesmo tempo",
    ", sans que ce soit une campagne payée visible. C'est souvent le signe qu'un fournisseur pousse et que le produit convertit.":
        ", sem campanha paga visível por trás. Costuma ser sinal de que um fornecedor está empurrando e de que o produto converte.",
    "Un rapport vues/ventes anormalement bon.": "Uma relação visualizações/vendas fora do normal.",
    "Une vidéo à {0} vues qui écoule autant qu'une à {1} vues indique un produit qui déclenche l'achat, pas seulement la curiosité.":
        "Um vídeo com {0} visualizações que vende tanto quanto um de {1} indica um produto que dispara a compra, não só a curiosidade.",
    "Une catégorie en croissance mais pas encore encombrée.": "Uma categoria crescendo mas ainda não lotada.",
    "Surveiller les catégories secondaires plutôt que la beauté, déjà très concurrentielle.":
        "Fique de olho nas categorias secundárias em vez da beleza, já muito disputada.",
    "Comment repérer ces signaux sans y passer ses journées": "Como achar esses sinais sem passar o dia nisso",
    "Les surveiller à la main suppose de parcourir des dizaines de vidéos par jour et de tenir un tableau. C'est précisément ce que le":
        "Acompanhar na mão significa ver dezenas de vídeos por dia e manter uma planilha. É exatamente isso que o",
    "de Qeerah automatise : il remonte les vidéos TikTok Shop qui performent en ce moment, avec leur chiffre d'affaires estimé, sur neuf régions dont la France.":
        "da Qeerah automatiza: ele traz os vídeos do TikTok Shop que estão indo bem agora, com o faturamento estimado, em nove regiões, incluindo a França.",
    "Et une fois un produit repéré, l'étape suivante n'est pas de le copier, mais de comprendre":
        "E, achado o produto, o passo seguinte não é copiá-lo, e sim entender",
    "pourquoi": "por que",
    "la vidéo qui le vend fonctionne — accroche, rétention, déclencheurs, appel à l'action. C'est l'objet de l'analyse vidéo.":
        "o vídeo que o vende funciona — gancho, retenção, gatilhos, chamada para ação. É disso que trata a análise de vídeo.",
    "Repère les produits qui décollent, et comprends pourquoi": "Ache os produtos que estão decolando e entenda por quê",
    "{0} jours d'accès complet, sans carte bancaire.": "{0} dias de acesso completo, sem cartão.",
    "Essayer Qeerah": "Testar a Qeerah",
    "Trois pièges à éviter": "Três armadilhas para evitar",
    "Choisir un produit parce qu'il te plaît.": "Escolher um produto porque você gosta dele.",
    "Ton goût n'est pas un indicateur de marché. Le seul test valable est la démonstrabilité en dix secondes.":
        "Seu gosto não é indicador de mercado. O único teste válido é conseguir demonstrar em dez segundos.",
    "Arriver en fin de cycle.": "Chegar no fim do ciclo.",
    "Si un produit tourne depuis six semaines dans ton fil, la fenêtre est probablement fermée. Mieux vaut la catégorie voisine.":
        "Se um produto está rodando há seis semanas no seu feed, a janela provavelmente fechou. Melhor a categoria vizinha.",
    "Négliger la marge.": "Ignorar a margem.",
    "Un produit à forte rotation mais à marge faible te fait travailler pour la plateforme. Calcule avant de tourner, pas après.":
        "Um produto de giro alto com margem baixa faz você trabalhar para a plataforma. Faça a conta antes de gravar, não depois.",
    "Ce qu'il faut retenir": "O que ficar",
    "Le marché français est jeune — un an d'existence — et largement porté par les créateurs, davantage que ses voisins européens. Cela signifie que la place est encore prenable, mais que la qualité de la vidéo compte plus que le catalogue : c'est elle qui fait {0} % du chiffre d'affaires.":
        "O mercado francês é jovem — um ano de vida — e se apoia nos criadores mais do que os vizinhos europeus. Isso quer dizer que ainda dá para pegar espaço, mas que a qualidade do vídeo pesa mais que o catálogo: é ela que faz {0} % do faturamento.",
    "Concentre-toi sur des produits dont le bénéfice se voit, repère-les tôt, et travaille la structure de tes vidéos plutôt que d'accumuler les références.":
        "Foque em produtos cujo benefício aparece, ache-os cedo e trabalhe a estrutura dos seus vídeos em vez de acumular referências.",
    "Analyser une vidéo TikTok Shop": "Analisar um vídeo do TikTok Shop",
    "Ma vidéo ne fait pas de vues": "Meu vídeo não tem visualizações",
    "TikTok Shop dans le monde": "TikTok Shop no mundo",
    "Source des chiffres :": "Fonte dos números:",
    ", mesure sur {0} jours arrêtée au {1} juillet {2}, portant sur la France, l'Allemagne, l'Espagne et l'Italie.":
        ", medição de {0} dias com corte em {1} de julho de {2}, cobrindo França, Alemanha, Espanha e Itália.",
}

T_LP_PRODUITS["en-ie"] = dict(T_LP_PRODUITS["en"])
T_LP_PRODUITS["es-mx"] = dict(T_LP_PRODUITS["es"])


# ═══════════════════════════════════════════════════════════════════════════
# /pourquoi-ma-video-tiktok-shop-ne-fait-pas-de-vues
# ═══════════════════════════════════════════════════════════════════════════
T_LP_VUES: dict[str, dict[str, str]] = {}

T_LP_VUES["en"] = {
    "Pourquoi ma vidéo TikTok Shop ne fait pas de vues — Qeerah":
        "Why my TikTok Shop video isn't getting views — Qeerah",
    "Ta vidéo stagne à quelques centaines de vues ? Les causes réelles, dans l'ordre où il faut les vérifier, et comment savoir laquelle te concerne.":
        "Your video stuck at a few hundred views? The real causes, in the order you should check them, and how to tell which one is yours.",
    "Les causes réelles, dans l'ordre où il faut les vérifier.": "The real causes, in the order you should check them.",
    "Tarifs": "Pricing",
    "Ouvrir l'app →": "Open the app →",
    "Pourquoi ma vidéo TikTok Shop ne fait pas de vues": "Why my TikTok Shop video isn't getting views",
    "Avant d'accuser l'algorithme ou de soupçonner un compte bridé, il y a cinq causes à vérifier — dans cet ordre. Neuf fois sur dix, la réponse est dans les trois premières secondes.":
        "Before blaming the algorithm or suspecting a throttled account, there are five causes to check — in this order. Nine times out of ten, the answer is in the first three seconds.",
    "C'est la question la plus fréquente chez les créateurs TikTok Shop, et celle où l'on se trompe le plus souvent de diagnostic. On soupçonne une sanction, un problème de compte, une malchance. La cause est presque toujours plus simple, et surtout : elle est mesurable.":
        "It's the most common question among TikTok Shop creators, and the one where the diagnosis goes wrong most often. People suspect a penalty, an account problem, bad luck. The cause is almost always simpler — and, above all, measurable.",
    "La règle de base : ta vidéo est testée avant d'être diffusée":
        "The basic rule: your video is tested before it's distributed",
    "TikTok ne montre pas immédiatement une vidéo à des centaines de milliers de personnes. Elle est d'abord proposée à un petit échantillon. Selon le comportement de cet échantillon — combien restent, combien reviennent en arrière, combien interagissent — la diffusion s'élargit ou s'arrête.":
        "TikTok doesn't put a video in front of hundreds of thousands of people straight away. It first goes to a small sample. Depending on how that sample behaves — how many stay, how many rewind, how many interact — distribution widens or stops.",
    "Cela a une conséquence directe :": "That has a direct consequence:",
    "quelques centaines de vues ne signifient pas que personne ne t'a vu, mais que le test s'est mal passé":
        "a few hundred views doesn't mean nobody saw you, it means the test went badly",
    ". Ce n'est pas une punition, c'est un résultat. Et un résultat, ça se corrige.":
        ". That's not a punishment, it's a result. And a result can be fixed.",
    "Les cinq causes, dans l'ordre où il faut les vérifier": "The five causes, in the order to check them",
    "{0}. L'accroche laisse partir avant la troisième seconde": "{0}. The hook lets people leave before the third second",
    "C'est la cause la plus fréquente, et de loin. Si ton ouverture met en place un décor, se présente, ou annonce ce qu'elle va dire au lieu de le dire, tu perds l'échantillon avant qu'il ait vu ton produit.":
        "This is by far the most common cause. If your opening sets a scene, introduces itself, or announces what it's about to say instead of saying it, you lose the sample before it has seen your product.",
    "Comment vérifier :": "How to check:",
    "regarde ta propre vidéo son coupé, et arrête-toi à {0} seconde. Si tu ne sais pas encore de quoi ça parle, l'accroche est en cause.":
        "watch your own video with the sound off and stop at {0} second. If you still don't know what it's about, the hook is the problem.",
    "{0}. L'attention décroche au milieu": "{0}. Attention drops in the middle",
    "Le début tient, mais la vidéo s'installe : un plan trop long, une explication qui traîne, une transition molle. Le spectateur ne part pas brutalement, il glisse.":
        "The opening holds, but the video settles in: a shot that runs long, an explanation that drags, a limp transition. The viewer doesn't leave abruptly, they slide away.",
    "repère le moment où toi-même tu as envie d'accélérer. C'est presque toujours là que la courbe chute.":
        "find the moment where you yourself want to skip ahead. That's almost always where the curve drops.",
    "{0}. Le format contredit les codes actuels": "{0}. The format goes against current conventions",
    "Vidéo non verticale, bandes noires, texte illisible sans le son, sous-titres absents, durée qui ne correspond pas au sujet. Ces éléments ne rendent pas la vidéo mauvaise, mais ils la desservent auprès d'une audience qui regarde en mobilité, souvent sans le son.":
        "Video not vertical, black bars, text unreadable without sound, no captions, a length that doesn't match the subject. None of this makes the video bad, but it works against you with an audience watching on the move, often with the sound off.",
    "ouvre ta vidéo sur ton téléphone, son coupé, en plein soleil. Si tu ne peux pas la suivre, l'algorithme n'est pas ton problème.":
        "open your video on your phone, sound off, in bright sunlight. If you can't follow it, the algorithm isn't your problem.",
    "{0}. Le sujet ne correspond pas à ton audience habituelle": "{0}. The subject doesn't match your usual audience",
    "Un changement brusque de thème désoriente la diffusion : la vidéo est proposée à ton audience existante, qui ne réagit pas, et le test échoue. Ce n'est pas un bridage, c'est un décalage.":
        "A sudden change of topic throws distribution off: the video goes to your existing audience, which doesn't react, and the test fails. That's not throttling, it's a mismatch.",
    "compare le sujet de la vidéo qui stagne à celui de tes trois dernières vidéos qui ont fonctionné.":
        "compare the topic of the stalled video with your last three videos that worked.",
    "{0}. Le produit n'est pas démontrable en vidéo courte": "{0}. The product can't be demonstrated in a short video",
    "Certains produits se vendent mal sur ce format, non parce qu'ils sont mauvais, mais parce que leur bénéfice ne se voit pas. Un complément alimentaire, un service, un produit dont l'effet met des semaines : rien à montrer en dix secondes.":
        "Some products sell badly in this format, not because they're bad but because their benefit can't be seen. A supplement, a service, a product whose effect takes weeks: nothing to show in ten seconds.",
    "demande-toi si tu peux prouver le bénéfice à l'image, sans l'expliquer. Si non, le problème est le choix du produit, pas la vidéo.":
        "ask yourself whether you can prove the benefit on screen, without explaining it. If not, the problem is the choice of product, not the video.",
    "Ce qu'il ne faut pas faire": "What not to do",
    "Supprimer la vidéo.": "Deleting the video.",
    "Cela ne « relance » rien et te prive de la donnée qui t'aurait permis de comprendre.":
        "It “restarts” nothing and robs you of the data that would have let you understand.",
    "Republier à l'identique.": "Reposting it unchanged.",
    "Si le test a échoué une fois, il échouera de la même manière.": "If the test failed once, it will fail the same way.",
    "Tout changer d'un coup.": "Changing everything at once.",
    "Accroche, montage, produit et légende modifiés simultanément : quel que soit le résultat, tu n'auras rien appris.":
        "Hook, edit, product and caption changed at the same time: whatever the result, you'll have learned nothing.",
    "Acheter des vues.": "Buying views.",
    "Un engagement artificiel dégrade le signal que la plateforme utilise pour te qualifier.":
        "Artificial engagement degrades the signal the platform uses to size you up.",
    "La méthode qui fait gagner du temps": "The method that saves time",
    "Plutôt que de deviner laquelle des cinq causes te concerne, compare. Prends une vidéo de ta niche qui a fonctionné récemment, et la tienne qui a stagné. Note les deux sur les mêmes critères : accroche, rétention, argumentaire, émotion, appel à l'action, format. L'écart le plus large désigne ton chantier.":
        "Rather than guessing which of the five causes is yours, compare. Take a video from your niche that worked recently, and your own that stalled. Score both on the same criteria: hook, retention, sales argument, emotion, call to action, format. The widest gap points to your job.",
    "C'est exactement ce que fait Qeerah, à partir d'un simple lien : l'analyse rend les sept dimensions notées, indique la seconde où l'attention décroche, liste les déclencheurs présents":
        "That's exactly what Qeerah does, from a single link: the analysis returns the seven dimensions scored, points to the second where attention drops, lists the triggers present",
    "et manquants": "and missing",
    ", puis propose des accroches réécrites pour ton produit. En mode « explique-moi simplement », chaque note est accompagnée de l'action concrète à mener.":
        ", then suggests hooks rewritten for your product. In “explain it simply” mode, every score comes with the concrete thing to do about it.",
    "Comprends ce qui bloque sur ta vidéo": "Understand what's holding your video back",
    "{0} jours d'accès complet, sans carte bancaire.": "{0} days of full access, no card required.",
    "Analyser ma vidéo": "Analyse my video",
    "Et si tout est correct mais que ça ne vend toujours pas ?": "And if everything's right but it still doesn't sell?",
    "Vues et ventes sont deux problèmes distincts. Une vidéo peut très bien être diffusée largement et ne rien écouler : cela signifie qu'elle divertit sans donner envie d'acheter. Dans ce cas, ce n'est pas la rétention qu'il faut travailler, mais l'argumentaire et l'appel à l'action.":
        "Views and sales are two different problems. A video can travel far and shift nothing: that means it entertains without making anyone want to buy. In that case the thing to work on isn't retention, it's the sales argument and the call to action.",
    "Le rapport à surveiller n'est donc pas le nombre de vues, mais le nombre de ventes rapporté aux vues. Sur le marché français, où":
        "So the ratio to watch isn't the view count, it's sales relative to views. On the French market, where",
    "{0} % du chiffre d'affaires de TikTok Shop passe par les créateurs affiliés":
        "{0}% of TikTok Shop revenue goes through affiliate creators",
    ", c'est ce rapport qui sépare un compte qui grossit d'un compte qui gagne de l'argent.":
        ", that ratio is what separates an account that grows from an account that earns.",
    "Analyser une vidéo TikTok Shop": "Analysing a TikTok Shop video",
    "Les produits qui vendent en France": "The products that sell in France",
    "Guide complet TikTok Shop": "Complete TikTok Shop guide",
    "Source du chiffre cité :": "Source of the figure quoted:",
    ". Le fonctionnement de la diffusion décrit ici repose sur des observations largement partagées par les créateurs ; TikTok ne publie pas le détail de son système de recommandation.":
        ". How distribution works, as described here, rests on observations widely shared among creators; TikTok does not publish the details of its recommendation system.",
}

T_LP_VUES["de"] = {
    "Pourquoi ma vidéo TikTok Shop ne fait pas de vues — Qeerah":
        "Warum mein TikTok-Shop-Video keine Aufrufe bekommt — Qeerah",
    "Ta vidéo stagne à quelques centaines de vues ? Les causes réelles, dans l'ordre où il faut les vérifier, et comment savoir laquelle te concerne.":
        "Dein Video hängt bei ein paar hundert Aufrufen fest? Die echten Ursachen, in der Reihenfolge, in der du sie prüfst — und wie du erkennst, welche deine ist.",
    "Les causes réelles, dans l'ordre où il faut les vérifier.": "Die echten Ursachen, in der Reihenfolge, in der du sie prüfst.",
    "Tarifs": "Preise",
    "Ouvrir l'app →": "App öffnen →",
    "Pourquoi ma vidéo TikTok Shop ne fait pas de vues": "Warum mein TikTok-Shop-Video keine Aufrufe bekommt",
    "Avant d'accuser l'algorithme ou de soupçonner un compte bridé, il y a cinq causes à vérifier — dans cet ordre. Neuf fois sur dix, la réponse est dans les trois premières secondes.":
        "Bevor du den Algorithmus beschuldigst oder ein gedrosseltes Konto vermutest: Es gibt fünf Ursachen, die du prüfst — in dieser Reihenfolge. In neun von zehn Fällen liegt die Antwort in den ersten drei Sekunden.",
    "C'est la question la plus fréquente chez les créateurs TikTok Shop, et celle où l'on se trompe le plus souvent de diagnostic. On soupçonne une sanction, un problème de compte, une malchance. La cause est presque toujours plus simple, et surtout : elle est mesurable.":
        "Das ist die häufigste Frage unter TikTok-Shop-Creators — und die, bei der die Diagnose am öftesten danebengeht. Man vermutet eine Strafe, ein Kontoproblem, Pech. Die Ursache ist fast immer einfacher und vor allem: messbar.",
    "La règle de base : ta vidéo est testée avant d'être diffusée":
        "Die Grundregel: Dein Video wird getestet, bevor es ausgespielt wird",
    "TikTok ne montre pas immédiatement une vidéo à des centaines de milliers de personnes. Elle est d'abord proposée à un petit échantillon. Selon le comportement de cet échantillon — combien restent, combien reviennent en arrière, combien interagissent — la diffusion s'élargit ou s'arrête.":
        "TikTok zeigt ein Video nicht sofort Hunderttausenden. Es geht erst an eine kleine Stichprobe. Je nachdem, wie sich diese Stichprobe verhält — wie viele bleiben, wie viele zurückspulen, wie viele reagieren —, wird die Ausspielung größer oder sie stoppt.",
    "Cela a une conséquence directe :": "Das hat eine unmittelbare Folge:",
    "quelques centaines de vues ne signifient pas que personne ne t'a vu, mais que le test s'est mal passé":
        "ein paar hundert Aufrufe heißen nicht, dass dich niemand gesehen hat, sondern dass der Test schiefging",
    ". Ce n'est pas une punition, c'est un résultat. Et un résultat, ça se corrige.":
        ". Das ist keine Strafe, das ist ein Ergebnis. Und ein Ergebnis lässt sich korrigieren.",
    "Les cinq causes, dans l'ordre où il faut les vérifier": "Die fünf Ursachen, in der Reihenfolge, in der du sie prüfst",
    "{0}. L'accroche laisse partir avant la troisième seconde": "{0}. Der Hook lässt sie vor Sekunde drei gehen",
    "C'est la cause la plus fréquente, et de loin. Si ton ouverture met en place un décor, se présente, ou annonce ce qu'elle va dire au lieu de le dire, tu perds l'échantillon avant qu'il ait vu ton produit.":
        "Das ist mit Abstand die häufigste Ursache. Wenn dein Einstieg erst eine Kulisse aufbaut, sich vorstellt oder ankündigt, was er gleich sagt, statt es zu sagen, verlierst du die Stichprobe, bevor sie dein Produkt gesehen hat.",
    "Comment vérifier :": "So prüfst du das:",
    "regarde ta propre vidéo son coupé, et arrête-toi à {0} seconde. Si tu ne sais pas encore de quoi ça parle, l'accroche est en cause.":
        "Sieh dir dein eigenes Video ohne Ton an und stopp bei Sekunde {0}. Wenn du noch nicht weißt, worum es geht, liegt es am Hook.",
    "{0}. L'attention décroche au milieu": "{0}. Die Aufmerksamkeit bricht in der Mitte ab",
    "Le début tient, mais la vidéo s'installe : un plan trop long, une explication qui traîne, une transition molle. Le spectateur ne part pas brutalement, il glisse.":
        "Der Anfang trägt, aber das Video macht es sich bequem: eine zu lange Einstellung, eine Erklärung, die sich zieht, ein schlaffer Übergang. Der Zuschauer geht nicht abrupt, er gleitet weg.",
    "repère le moment où toi-même tu as envie d'accélérer. C'est presque toujours là que la courbe chute.":
        "Finde die Stelle, an der du selbst vorspulen willst. Fast immer fällt dort die Kurve.",
    "{0}. Le format contredit les codes actuels": "{0}. Das Format passt nicht zu den aktuellen Codes",
    "Vidéo non verticale, bandes noires, texte illisible sans le son, sous-titres absents, durée qui ne correspond pas au sujet. Ces éléments ne rendent pas la vidéo mauvaise, mais ils la desservent auprès d'une audience qui regarde en mobilité, souvent sans le son.":
        "Kein Hochformat, schwarze Balken, Text ohne Ton nicht lesbar, keine Untertitel, eine Länge, die nicht zum Thema passt. Nichts davon macht das Video schlecht, aber es schadet ihm bei einem Publikum, das unterwegs schaut, oft ohne Ton.",
    "ouvre ta vidéo sur ton téléphone, son coupé, en plein soleil. Si tu ne peux pas la suivre, l'algorithme n'est pas ton problème.":
        "Öffne dein Video auf dem Handy, ohne Ton, in der prallen Sonne. Wenn du ihm nicht folgen kannst, ist nicht der Algorithmus dein Problem.",
    "{0}. Le sujet ne correspond pas à ton audience habituelle": "{0}. Das Thema passt nicht zu deinem üblichen Publikum",
    "Un changement brusque de thème désoriente la diffusion : la vidéo est proposée à ton audience existante, qui ne réagit pas, et le test échoue. Ce n'est pas un bridage, c'est un décalage.":
        "Ein abrupter Themenwechsel bringt die Ausspielung durcheinander: Das Video geht an dein bestehendes Publikum, das nicht reagiert, und der Test scheitert. Das ist keine Drosselung, das ist ein Missverhältnis.",
    "compare le sujet de la vidéo qui stagne à celui de tes trois dernières vidéos qui ont fonctionné.":
        "Vergleich das Thema des hängengebliebenen Videos mit deinen letzten drei Videos, die liefen.",
    "{0}. Le produit n'est pas démontrable en vidéo courte": "{0}. Das Produkt lässt sich im Kurzvideo nicht zeigen",
    "Certains produits se vendent mal sur ce format, non parce qu'ils sont mauvais, mais parce que leur bénéfice ne se voit pas. Un complément alimentaire, un service, un produit dont l'effet met des semaines : rien à montrer en dix secondes.":
        "Manche Produkte verkaufen sich in diesem Format schlecht — nicht weil sie schlecht sind, sondern weil man ihren Nutzen nicht sieht. Ein Nahrungsergänzungsmittel, eine Dienstleistung, ein Produkt, dessen Wirkung Wochen braucht: nichts, was man in zehn Sekunden zeigen kann.",
    "demande-toi si tu peux prouver le bénéfice à l'image, sans l'expliquer. Si non, le problème est le choix du produit, pas la vidéo.":
        "Frag dich, ob du den Nutzen im Bild beweisen kannst, ohne ihn zu erklären. Wenn nicht, liegt das Problem bei der Produktwahl, nicht beim Video.",
    "Ce qu'il ne faut pas faire": "Was du nicht tun solltest",
    "Supprimer la vidéo.": "Das Video löschen.",
    "Cela ne « relance » rien et te prive de la donnée qui t'aurait permis de comprendre.":
        "Das „startet“ nichts neu und nimmt dir die Daten, mit denen du es hättest verstehen können.",
    "Republier à l'identique.": "Unverändert erneut posten.",
    "Si le test a échoué une fois, il échouera de la même manière.": "Ist der Test einmal gescheitert, scheitert er genauso wieder.",
    "Tout changer d'un coup.": "Alles auf einmal ändern.",
    "Accroche, montage, produit et légende modifiés simultanément : quel que soit le résultat, tu n'auras rien appris.":
        "Hook, Schnitt, Produkt und Caption gleichzeitig geändert: Wie das Ergebnis auch ausfällt, du hast nichts gelernt.",
    "Acheter des vues.": "Aufrufe kaufen.",
    "Un engagement artificiel dégrade le signal que la plateforme utilise pour te qualifier.":
        "Künstliche Interaktion verdirbt genau das Signal, mit dem dich die Plattform einordnet.",
    "La méthode qui fait gagner du temps": "Die Methode, die Zeit spart",
    "Plutôt que de deviner laquelle des cinq causes te concerne, compare. Prends une vidéo de ta niche qui a fonctionné récemment, et la tienne qui a stagné. Note les deux sur les mêmes critères : accroche, rétention, argumentaire, émotion, appel à l'action, format. L'écart le plus large désigne ton chantier.":
        "Statt zu raten, welche der fünf Ursachen deine ist: vergleich. Nimm ein Video aus deiner Nische, das zuletzt lief, und dein eigenes, das hängen blieb. Bewerte beide nach denselben Kriterien: Hook, Bindung, Verkaufsargument, Emotion, Call to Action, Format. Der größte Abstand zeigt deine Baustelle.",
    "C'est exactement ce que fait Qeerah, à partir d'un simple lien : l'analyse rend les sept dimensions notées, indique la seconde où l'attention décroche, liste les déclencheurs présents":
        "Genau das macht Qeerah, aus einem einfachen Link: Die Analyse liefert die sieben Dimensionen bewertet, nennt die Sekunde, in der die Aufmerksamkeit abreißt, listet die vorhandenen Auslöser",
    "et manquants": "und die fehlenden",
    ", puis propose des accroches réécrites pour ton produit. En mode « explique-moi simplement », chaque note est accompagnée de l'action concrète à mener.":
        " und schlägt dann Hooks vor, neu geschrieben für dein Produkt. Im Modus „erklär's mir einfach“ steht zu jeder Wertung, was konkret zu tun ist.",
    "Comprends ce qui bloque sur ta vidéo": "Versteh, woran es bei deinem Video hakt",
    "{0} jours d'accès complet, sans carte bancaire.": "{0} Tage voller Zugang, ohne Kreditkarte.",
    "Analyser ma vidéo": "Mein Video analysieren",
    "Et si tout est correct mais que ça ne vend toujours pas ?": "Und wenn alles stimmt und es trotzdem nicht verkauft?",
    "Vues et ventes sont deux problèmes distincts. Une vidéo peut très bien être diffusée largement et ne rien écouler : cela signifie qu'elle divertit sans donner envie d'acheter. Dans ce cas, ce n'est pas la rétention qu'il faut travailler, mais l'argumentaire et l'appel à l'action.":
        "Aufrufe und Verkäufe sind zwei verschiedene Probleme. Ein Video kann weit laufen und trotzdem nichts absetzen: Dann unterhält es, ohne Kauflust zu wecken. In dem Fall arbeitest du nicht an der Bindung, sondern am Verkaufsargument und am Call to Action.",
    "Le rapport à surveiller n'est donc pas le nombre de vues, mais le nombre de ventes rapporté aux vues. Sur le marché français, où":
        "Die Kennzahl, die zählt, ist also nicht die Aufrufzahl, sondern Verkäufe im Verhältnis zu Aufrufen. Auf dem französischen Markt, wo",
    "{0} % du chiffre d'affaires de TikTok Shop passe par les créateurs affiliés":
        "{0} % des TikTok-Shop-Umsatzes über Affiliate-Creators laufen",
    ", c'est ce rapport qui sépare un compte qui grossit d'un compte qui gagne de l'argent.":
        ", trennt genau dieses Verhältnis ein Konto, das wächst, von einem Konto, das Geld verdient.",
    "Analyser une vidéo TikTok Shop": "Ein TikTok-Shop-Video analysieren",
    "Les produits qui vendent en France": "Die Produkte, die in Frankreich verkaufen",
    "Guide complet TikTok Shop": "Vollständiger TikTok-Shop-Guide",
    "Source du chiffre cité :": "Quelle der genannten Zahl:",
    ". Le fonctionnement de la diffusion décrit ici repose sur des observations largement partagées par les créateurs ; TikTok ne publie pas le détail de son système de recommandation.":
        ". Wie die Ausspielung hier beschrieben wird, beruht auf Beobachtungen, die unter Creators weit geteilt werden; TikTok veröffentlicht die Details seines Empfehlungssystems nicht.",
}

T_LP_VUES["es"] = {
    "Pourquoi ma vidéo TikTok Shop ne fait pas de vues — Qeerah":
        "Por qué mi vídeo de TikTok Shop no tiene visualizaciones — Qeerah",
    "Ta vidéo stagne à quelques centaines de vues ? Les causes réelles, dans l'ordre où il faut les vérifier, et comment savoir laquelle te concerne.":
        "¿Tu vídeo se queda en unos cientos de visualizaciones? Las causas reales, en el orden en que hay que revisarlas, y cómo saber cuál es la tuya.",
    "Les causes réelles, dans l'ordre où il faut les vérifier.": "Las causas reales, en el orden en que hay que revisarlas.",
    "Tarifs": "Precios",
    "Ouvrir l'app →": "Abrir la app →",
    "Pourquoi ma vidéo TikTok Shop ne fait pas de vues": "Por qué mi vídeo de TikTok Shop no tiene visualizaciones",
    "Avant d'accuser l'algorithme ou de soupçonner un compte bridé, il y a cinq causes à vérifier — dans cet ordre. Neuf fois sur dix, la réponse est dans les trois premières secondes.":
        "Antes de culpar al algoritmo o sospechar que tu cuenta está limitada, hay cinco causas que revisar, en este orden. Nueve de cada diez veces, la respuesta está en los tres primeros segundos.",
    "C'est la question la plus fréquente chez les créateurs TikTok Shop, et celle où l'on se trompe le plus souvent de diagnostic. On soupçonne une sanction, un problème de compte, une malchance. La cause est presque toujours plus simple, et surtout : elle est mesurable.":
        "Es la pregunta más frecuente entre los creadores de TikTok Shop y en la que más se falla el diagnóstico. Se sospecha una sanción, un problema de cuenta, mala suerte. La causa casi siempre es más simple y, sobre todo, medible.",
    "La règle de base : ta vidéo est testée avant d'être diffusée":
        "La regla básica: tu vídeo se prueba antes de difundirse",
    "TikTok ne montre pas immédiatement une vidéo à des centaines de milliers de personnes. Elle est d'abord proposée à un petit échantillon. Selon le comportement de cet échantillon — combien restent, combien reviennent en arrière, combien interagissent — la diffusion s'élargit ou s'arrête.":
        "TikTok no enseña un vídeo de golpe a cientos de miles de personas. Primero se lo propone a una muestra pequeña. Según cómo se comporte esa muestra —cuántos se quedan, cuántos rebobinan, cuántos interactúan—, la difusión se amplía o se detiene.",
    "Cela a une conséquence directe :": "Eso tiene una consecuencia directa:",
    "quelques centaines de vues ne signifient pas que personne ne t'a vu, mais que le test s'est mal passé":
        "unos cientos de visualizaciones no significan que nadie te haya visto, sino que la prueba salió mal",
    ". Ce n'est pas une punition, c'est un résultat. Et un résultat, ça se corrige.":
        ". No es un castigo, es un resultado. Y un resultado se corrige.",
    "Les cinq causes, dans l'ordre où il faut les vérifier": "Las cinco causas, en el orden en que hay que revisarlas",
    "{0}. L'accroche laisse partir avant la troisième seconde": "{0}. El gancho deja escapar antes del tercer segundo",
    "C'est la cause la plus fréquente, et de loin. Si ton ouverture met en place un décor, se présente, ou annonce ce qu'elle va dire au lieu de le dire, tu perds l'échantillon avant qu'il ait vu ton produit.":
        "Es con diferencia la causa más frecuente. Si tu apertura monta un decorado, se presenta o anuncia lo que va a decir en vez de decirlo, pierdes la muestra antes de que haya visto tu producto.",
    "Comment vérifier :": "Cómo comprobarlo:",
    "regarde ta propre vidéo son coupé, et arrête-toi à {0} seconde. Si tu ne sais pas encore de quoi ça parle, l'accroche est en cause.":
        "mira tu propio vídeo sin sonido y detente en el segundo {0}. Si todavía no sabes de qué va, el gancho es el problema.",
    "{0}. L'attention décroche au milieu": "{0}. La atención se cae por el medio",
    "Le début tient, mais la vidéo s'installe : un plan trop long, une explication qui traîne, une transition molle. Le spectateur ne part pas brutalement, il glisse.":
        "El principio aguanta, pero el vídeo se acomoda: un plano demasiado largo, una explicación que se alarga, una transición floja. El espectador no se va de golpe, se desliza.",
    "repère le moment où toi-même tu as envie d'accélérer. C'est presque toujours là que la courbe chute.":
        "localiza el momento en el que tú mismo quieres adelantar. Casi siempre es ahí donde cae la curva.",
    "{0}. Le format contredit les codes actuels": "{0}. El formato choca con los códigos actuales",
    "Vidéo non verticale, bandes noires, texte illisible sans le son, sous-titres absents, durée qui ne correspond pas au sujet. Ces éléments ne rendent pas la vidéo mauvaise, mais ils la desservent auprès d'une audience qui regarde en mobilité, souvent sans le son.":
        "Vídeo no vertical, bandas negras, texto ilegible sin sonido, sin subtítulos, duración que no encaja con el tema. Nada de eso hace malo el vídeo, pero le juega en contra ante un público que mira en movimiento, muchas veces sin sonido.",
    "ouvre ta vidéo sur ton téléphone, son coupé, en plein soleil. Si tu ne peux pas la suivre, l'algorithme n'est pas ton problème.":
        "abre tu vídeo en el móvil, sin sonido, a pleno sol. Si no puedes seguirlo, el algoritmo no es tu problema.",
    "{0}. Le sujet ne correspond pas à ton audience habituelle": "{0}. El tema no encaja con tu público habitual",
    "Un changement brusque de thème désoriente la diffusion : la vidéo est proposée à ton audience existante, qui ne réagit pas, et le test échoue. Ce n'est pas un bridage, c'est un décalage.":
        "Un cambio brusco de tema desorienta la difusión: el vídeo se le propone a tu público actual, que no reacciona, y la prueba falla. No es una limitación, es un desajuste.",
    "compare le sujet de la vidéo qui stagne à celui de tes trois dernières vidéos qui ont fonctionné.":
        "compara el tema del vídeo estancado con el de tus tres últimos vídeos que funcionaron.",
    "{0}. Le produit n'est pas démontrable en vidéo courte": "{0}. El producto no se puede demostrar en vídeo corto",
    "Certains produits se vendent mal sur ce format, non parce qu'ils sont mauvais, mais parce que leur bénéfice ne se voit pas. Un complément alimentaire, un service, un produit dont l'effet met des semaines : rien à montrer en dix secondes.":
        "Algunos productos se venden mal en este formato, no porque sean malos, sino porque su beneficio no se ve. Un complemento alimenticio, un servicio, un producto cuyo efecto tarda semanas: nada que enseñar en diez segundos.",
    "demande-toi si tu peux prouver le bénéfice à l'image, sans l'expliquer. Si non, le problème est le choix du produit, pas la vidéo.":
        "pregúntate si puedes probar el beneficio en imagen, sin explicarlo. Si no, el problema es la elección del producto, no el vídeo.",
    "Ce qu'il ne faut pas faire": "Lo que no hay que hacer",
    "Supprimer la vidéo.": "Borrar el vídeo.",
    "Cela ne « relance » rien et te prive de la donnée qui t'aurait permis de comprendre.":
        "No «relanza» nada y te quita el dato que te habría permitido entenderlo.",
    "Republier à l'identique.": "Volver a publicarlo igual.",
    "Si le test a échoué une fois, il échouera de la même manière.": "Si la prueba falló una vez, fallará igual.",
    "Tout changer d'un coup.": "Cambiarlo todo de golpe.",
    "Accroche, montage, produit et légende modifiés simultanément : quel que soit le résultat, tu n'auras rien appris.":
        "Gancho, montaje, producto y texto cambiados a la vez: sea cual sea el resultado, no habrás aprendido nada.",
    "Acheter des vues.": "Comprar visualizaciones.",
    "Un engagement artificiel dégrade le signal que la plateforme utilise pour te qualifier.":
        "La interacción artificial degrada la señal que la plataforma usa para calificarte.",
    "La méthode qui fait gagner du temps": "El método que ahorra tiempo",
    "Plutôt que de deviner laquelle des cinq causes te concerne, compare. Prends une vidéo de ta niche qui a fonctionné récemment, et la tienne qui a stagné. Note les deux sur les mêmes critères : accroche, rétention, argumentaire, émotion, appel à l'action, format. L'écart le plus large désigne ton chantier.":
        "En vez de adivinar cuál de las cinco causas es la tuya, compara. Coge un vídeo de tu nicho que haya funcionado hace poco y el tuyo que se ha estancado. Puntúa los dos con los mismos criterios: gancho, retención, argumento, emoción, llamada a la acción, formato. La mayor diferencia señala tu tarea.",
    "C'est exactement ce que fait Qeerah, à partir d'un simple lien : l'analyse rend les sept dimensions notées, indique la seconde où l'attention décroche, liste les déclencheurs présents":
        "Es exactamente lo que hace Qeerah a partir de un simple enlace: el análisis devuelve las siete dimensiones puntuadas, señala el segundo en el que cae la atención, enumera los disparadores presentes",
    "et manquants": "y los que faltan",
    ", puis propose des accroches réécrites pour ton produit. En mode « explique-moi simplement », chaque note est accompagnée de l'action concrète à mener.":
        " y propone ganchos reescritos para tu producto. En modo «explícamelo fácil», cada puntuación viene con la acción concreta que hay que hacer.",
    "Comprends ce qui bloque sur ta vidéo": "Entiende qué está bloqueando tu vídeo",
    "{0} jours d'accès complet, sans carte bancaire.": "{0} días de acceso completo, sin tarjeta.",
    "Analyser ma vidéo": "Analizar mi vídeo",
    "Et si tout est correct mais que ça ne vend toujours pas ?": "¿Y si todo está bien pero sigue sin vender?",
    "Vues et ventes sont deux problèmes distincts. Une vidéo peut très bien être diffusée largement et ne rien écouler : cela signifie qu'elle divertit sans donner envie d'acheter. Dans ce cas, ce n'est pas la rétention qu'il faut travailler, mais l'argumentaire et l'appel à l'action.":
        "Visualizaciones y ventas son dos problemas distintos. Un vídeo puede difundirse mucho y no vender nada: significa que entretiene sin dar ganas de comprar. En ese caso no hay que trabajar la retención, sino el argumento y la llamada a la acción.",
    "Le rapport à surveiller n'est donc pas le nombre de vues, mais le nombre de ventes rapporté aux vues. Sur le marché français, où":
        "Así que la relación a vigilar no es el número de visualizaciones, sino las ventas en proporción a las visualizaciones. En el mercado francés, donde",
    "{0} % du chiffre d'affaires de TikTok Shop passe par les créateurs affiliés":
        "el {0} % de la facturación de TikTok Shop pasa por los creadores afiliados",
    ", c'est ce rapport qui sépare un compte qui grossit d'un compte qui gagne de l'argent.":
        ", es esa relación la que separa una cuenta que crece de una cuenta que gana dinero.",
    "Analyser une vidéo TikTok Shop": "Analizar un vídeo de TikTok Shop",
    "Les produits qui vendent en France": "Los productos que venden en Francia",
    "Guide complet TikTok Shop": "Guía completa de TikTok Shop",
    "Source du chiffre cité :": "Fuente de la cifra citada:",
    ". Le fonctionnement de la diffusion décrit ici repose sur des observations largement partagées par les créateurs ; TikTok ne publie pas le détail de son système de recommandation.":
        ". El funcionamiento de la difusión descrito aquí se basa en observaciones ampliamente compartidas por los creadores; TikTok no publica el detalle de su sistema de recomendación.",
}

T_LP_VUES["it"] = {
    "Pourquoi ma vidéo TikTok Shop ne fait pas de vues — Qeerah":
        "Perché il mio video TikTok Shop non fa visualizzazioni — Qeerah",
    "Ta vidéo stagne à quelques centaines de vues ? Les causes réelles, dans l'ordre où il faut les vérifier, et comment savoir laquelle te concerne.":
        "Il tuo video è fermo a qualche centinaio di visualizzazioni? Le cause vere, nell'ordine in cui vanno controllate, e come capire qual è la tua.",
    "Les causes réelles, dans l'ordre où il faut les vérifier.": "Le cause vere, nell'ordine in cui vanno controllate.",
    "Tarifs": "Prezzi",
    "Ouvrir l'app →": "Apri l'app →",
    "Pourquoi ma vidéo TikTok Shop ne fait pas de vues": "Perché il mio video TikTok Shop non fa visualizzazioni",
    "Avant d'accuser l'algorithme ou de soupçonner un compte bridé, il y a cinq causes à vérifier — dans cet ordre. Neuf fois sur dix, la réponse est dans les trois premières secondes.":
        "Prima di prendertela con l'algoritmo o sospettare un account limitato, ci sono cinque cause da controllare — in quest'ordine. Nove volte su dieci la risposta è nei primi tre secondi.",
    "C'est la question la plus fréquente chez les créateurs TikTok Shop, et celle où l'on se trompe le plus souvent de diagnostic. On soupçonne une sanction, un problème de compte, une malchance. La cause est presque toujours plus simple, et surtout : elle est mesurable.":
        "È la domanda più frequente tra i creator di TikTok Shop, e quella su cui si sbaglia più spesso diagnosi. Si sospetta una penalizzazione, un problema di account, sfortuna. La causa è quasi sempre più semplice e, soprattutto, misurabile.",
    "La règle de base : ta vidéo est testée avant d'être diffusée":
        "La regola di base: il tuo video viene testato prima di essere diffuso",
    "TikTok ne montre pas immédiatement une vidéo à des centaines de milliers de personnes. Elle est d'abord proposée à un petit échantillon. Selon le comportement de cet échantillon — combien restent, combien reviennent en arrière, combien interagissent — la diffusion s'élargit ou s'arrête.":
        "TikTok non mostra subito un video a centinaia di migliaia di persone. Prima lo propone a un piccolo campione. A seconda di come si comporta quel campione — quanti restano, quanti riavvolgono, quanti interagiscono — la diffusione si allarga o si ferma.",
    "Cela a une conséquence directe :": "Ne deriva una conseguenza diretta:",
    "quelques centaines de vues ne signifient pas que personne ne t'a vu, mais que le test s'est mal passé":
        "qualche centinaio di visualizzazioni non vuol dire che nessuno ti abbia visto, ma che il test è andato male",
    ". Ce n'est pas une punition, c'est un résultat. Et un résultat, ça se corrige.":
        ". Non è una punizione, è un risultato. E un risultato si corregge.",
    "Les cinq causes, dans l'ordre où il faut les vérifier": "Le cinque cause, nell'ordine in cui vanno controllate",
    "{0}. L'accroche laisse partir avant la troisième seconde": "{0}. L'hook li lascia andare prima del terzo secondo",
    "C'est la cause la plus fréquente, et de loin. Si ton ouverture met en place un décor, se présente, ou annonce ce qu'elle va dire au lieu de le dire, tu perds l'échantillon avant qu'il ait vu ton produit.":
        "È di gran lunga la causa più frequente. Se la tua apertura costruisce una scenografia, si presenta o annuncia quello che dirà invece di dirlo, perdi il campione prima che abbia visto il prodotto.",
    "Comment vérifier :": "Come verificare:",
    "regarde ta propre vidéo son coupé, et arrête-toi à {0} seconde. Si tu ne sais pas encore de quoi ça parle, l'accroche est en cause.":
        "guarda il tuo video senza audio e fermati al secondo {0}. Se non hai ancora capito di cosa parla, il problema è l'hook.",
    "{0}. L'attention décroche au milieu": "{0}. L'attenzione cade a metà",
    "Le début tient, mais la vidéo s'installe : un plan trop long, une explication qui traîne, une transition molle. Le spectateur ne part pas brutalement, il glisse.":
        "L'inizio tiene, ma il video si siede: un'inquadratura troppo lunga, una spiegazione che si trascina, una transizione fiacca. Lo spettatore non se ne va di colpo, scivola via.",
    "repère le moment où toi-même tu as envie d'accélérer. C'est presque toujours là que la courbe chute.":
        "individua il punto in cui tu stesso vorresti mandare avanti. Quasi sempre è lì che crolla la curva.",
    "{0}. Le format contredit les codes actuels": "{0}. Il formato va contro i codici attuali",
    "Vidéo non verticale, bandes noires, texte illisible sans le son, sous-titres absents, durée qui ne correspond pas au sujet. Ces éléments ne rendent pas la vidéo mauvaise, mais ils la desservent auprès d'une audience qui regarde en mobilité, souvent sans le son.":
        "Video non verticale, bande nere, testo illeggibile senza audio, sottotitoli assenti, durata che non corrisponde all'argomento. Nulla di tutto ciò rende il video brutto, ma lo penalizza con un pubblico che guarda in movimento, spesso senza audio.",
    "ouvre ta vidéo sur ton téléphone, son coupé, en plein soleil. Si tu ne peux pas la suivre, l'algorithme n'est pas ton problème.":
        "apri il tuo video sul telefono, senza audio, in pieno sole. Se non riesci a seguirlo, il tuo problema non è l'algoritmo.",
    "{0}. Le sujet ne correspond pas à ton audience habituelle": "{0}. L'argomento non corrisponde al tuo pubblico abituale",
    "Un changement brusque de thème désoriente la diffusion : la vidéo est proposée à ton audience existante, qui ne réagit pas, et le test échoue. Ce n'est pas un bridage, c'est un décalage.":
        "Un cambio brusco di tema disorienta la diffusione: il video viene proposto al tuo pubblico attuale, che non reagisce, e il test fallisce. Non è una limitazione, è uno scarto.",
    "compare le sujet de la vidéo qui stagne à celui de tes trois dernières vidéos qui ont fonctionné.":
        "confronta l'argomento del video fermo con quello dei tuoi ultimi tre video che hanno funzionato.",
    "{0}. Le produit n'est pas démontrable en vidéo courte": "{0}. Il prodotto non è dimostrabile in un video breve",
    "Certains produits se vendent mal sur ce format, non parce qu'ils sont mauvais, mais parce que leur bénéfice ne se voit pas. Un complément alimentaire, un service, un produit dont l'effet met des semaines : rien à montrer en dix secondes.":
        "Alcuni prodotti vendono male in questo formato, non perché siano scadenti ma perché il loro beneficio non si vede. Un integratore, un servizio, un prodotto il cui effetto richiede settimane: niente da mostrare in dieci secondi.",
    "demande-toi si tu peux prouver le bénéfice à l'image, sans l'expliquer. Si non, le problème est le choix du produit, pas la vidéo.":
        "chiediti se puoi provare il beneficio a schermo, senza spiegarlo. Se no, il problema è la scelta del prodotto, non il video.",
    "Ce qu'il ne faut pas faire": "Cosa non fare",
    "Supprimer la vidéo.": "Cancellare il video.",
    "Cela ne « relance » rien et te prive de la donnée qui t'aurait permis de comprendre.":
        "Non «rilancia» nulla e ti toglie il dato che ti avrebbe permesso di capire.",
    "Republier à l'identique.": "Ripubblicarlo uguale.",
    "Si le test a échoué une fois, il échouera de la même manière.": "Se il test è fallito una volta, fallirà allo stesso modo.",
    "Tout changer d'un coup.": "Cambiare tutto insieme.",
    "Accroche, montage, produit et légende modifiés simultanément : quel que soit le résultat, tu n'auras rien appris.":
        "Hook, montaggio, prodotto e didascalia cambiati insieme: qualunque sia il risultato, non avrai imparato nulla.",
    "Acheter des vues.": "Comprare visualizzazioni.",
    "Un engagement artificiel dégrade le signal que la plateforme utilise pour te qualifier.":
        "L'interazione artificiale rovina proprio il segnale con cui la piattaforma ti valuta.",
    "La méthode qui fait gagner du temps": "Il metodo che fa risparmiare tempo",
    "Plutôt que de deviner laquelle des cinq causes te concerne, compare. Prends une vidéo de ta niche qui a fonctionné récemment, et la tienne qui a stagné. Note les deux sur les mêmes critères : accroche, rétention, argumentaire, émotion, appel à l'action, format. L'écart le plus large désigne ton chantier.":
        "Invece di indovinare quale delle cinque cause ti riguarda, confronta. Prendi un video della tua nicchia che ha funzionato di recente e il tuo che si è fermato. Valutali con gli stessi criteri: hook, ritenzione, argomento, emozione, call to action, formato. Il divario più ampio indica il tuo cantiere.",
    "C'est exactement ce que fait Qeerah, à partir d'un simple lien : l'analyse rend les sept dimensions notées, indique la seconde où l'attention décroche, liste les déclencheurs présents":
        "È esattamente ciò che fa Qeerah, da un semplice link: l'analisi restituisce le sette dimensioni valutate, indica il secondo in cui l'attenzione cala, elenca le leve presenti",
    "et manquants": "e quelle mancanti",
    ", puis propose des accroches réécrites pour ton produit. En mode « explique-moi simplement », chaque note est accompagnée de l'action concrète à mener.":
        ", poi propone hook riscritti per il tuo prodotto. In modalità «spiegamelo semplice», ogni voto è accompagnato dall'azione concreta da fare.",
    "Comprends ce qui bloque sur ta vidéo": "Capisci cosa blocca il tuo video",
    "{0} jours d'accès complet, sans carte bancaire.": "{0} giorni di accesso completo, senza carta.",
    "Analyser ma vidéo": "Analizza il mio video",
    "Et si tout est correct mais que ça ne vend toujours pas ?": "E se è tutto a posto ma continua a non vendere?",
    "Vues et ventes sont deux problèmes distincts. Une vidéo peut très bien être diffusée largement et ne rien écouler : cela signifie qu'elle divertit sans donner envie d'acheter. Dans ce cas, ce n'est pas la rétention qu'il faut travailler, mais l'argumentaire et l'appel à l'action.":
        "Visualizzazioni e vendite sono due problemi diversi. Un video può essere diffuso tantissimo e non vendere nulla: vuol dire che intrattiene senza far venire voglia di comprare. In quel caso non si lavora sulla ritenzione, ma sull'argomento e sulla call to action.",
    "Le rapport à surveiller n'est donc pas le nombre de vues, mais le nombre de ventes rapporté aux vues. Sur le marché français, où":
        "Il rapporto da guardare non è quindi il numero di visualizzazioni, ma le vendite rapportate alle visualizzazioni. Sul mercato francese, dove",
    "{0} % du chiffre d'affaires de TikTok Shop passe par les créateurs affiliés":
        "il {0} % del fatturato di TikTok Shop passa dai creator affiliati",
    ", c'est ce rapport qui sépare un compte qui grossit d'un compte qui gagne de l'argent.":
        ", è questo rapporto a separare un account che cresce da un account che guadagna.",
    "Analyser une vidéo TikTok Shop": "Analizzare un video TikTok Shop",
    "Les produits qui vendent en France": "I prodotti che vendono in Francia",
    "Guide complet TikTok Shop": "Guida completa a TikTok Shop",
    "Source du chiffre cité :": "Fonte del dato citato:",
    ". Le fonctionnement de la diffusion décrit ici repose sur des observations largement partagées par les créateurs ; TikTok ne publie pas le détail de son système de recommandation.":
        ". Il funzionamento della diffusione descritto qui si basa su osservazioni ampiamente condivise dai creator; TikTok non pubblica il dettaglio del suo sistema di raccomandazione.",
}

T_LP_VUES["pt-br"] = {
    "Pourquoi ma vidéo TikTok Shop ne fait pas de vues — Qeerah":
        "Por que meu vídeo do TikTok Shop não tem visualizações — Qeerah",
    "Ta vidéo stagne à quelques centaines de vues ? Les causes réelles, dans l'ordre où il faut les vérifier, et comment savoir laquelle te concerne.":
        "Seu vídeo travou em algumas centenas de visualizações? As causas reais, na ordem em que se deve checar, e como saber qual é a sua.",
    "Les causes réelles, dans l'ordre où il faut les vérifier.": "As causas reais, na ordem em que se deve checar.",
    "Tarifs": "Preços",
    "Ouvrir l'app →": "Abrir o app →",
    "Pourquoi ma vidéo TikTok Shop ne fait pas de vues": "Por que meu vídeo do TikTok Shop não tem visualizações",
    "Avant d'accuser l'algorithme ou de soupçonner un compte bridé, il y a cinq causes à vérifier — dans cet ordre. Neuf fois sur dix, la réponse est dans les trois premières secondes.":
        "Antes de culpar o algoritmo ou achar que sua conta está limitada, há cinco causas para checar — nesta ordem. Nove em cada dez vezes, a resposta está nos três primeiros segundos.",
    "C'est la question la plus fréquente chez les créateurs TikTok Shop, et celle où l'on se trompe le plus souvent de diagnostic. On soupçonne une sanction, un problème de compte, une malchance. La cause est presque toujours plus simple, et surtout : elle est mesurable.":
        "É a pergunta mais comum entre criadores do TikTok Shop e aquela em que mais se erra o diagnóstico. Suspeita-se de punição, problema de conta, azar. A causa quase sempre é mais simples e, principalmente, dá para medir.",
    "La règle de base : ta vidéo est testée avant d'être diffusée":
        "A regra básica: seu vídeo é testado antes de ser distribuído",
    "TikTok ne montre pas immédiatement une vidéo à des centaines de milliers de personnes. Elle est d'abord proposée à un petit échantillon. Selon le comportement de cet échantillon — combien restent, combien reviennent en arrière, combien interagissent — la diffusion s'élargit ou s'arrête.":
        "O TikTok não mostra um vídeo de cara para centenas de milhares de pessoas. Ele primeiro vai para uma amostra pequena. Dependendo do comportamento dessa amostra — quantos ficam, quantos voltam, quantos interagem —, a distribuição aumenta ou para.",
    "Cela a une conséquence directe :": "Isso tem uma consequência direta:",
    "quelques centaines de vues ne signifient pas que personne ne t'a vu, mais que le test s'est mal passé":
        "algumas centenas de visualizações não querem dizer que ninguém viu você, e sim que o teste foi mal",
    ". Ce n'est pas une punition, c'est un résultat. Et un résultat, ça se corrige.":
        ". Não é punição, é resultado. E resultado se corrige.",
    "Les cinq causes, dans l'ordre où il faut les vérifier": "As cinco causas, na ordem em que se deve checar",
    "{0}. L'accroche laisse partir avant la troisième seconde": "{0}. O gancho deixa a pessoa sair antes do terceiro segundo",
    "C'est la cause la plus fréquente, et de loin. Si ton ouverture met en place un décor, se présente, ou annonce ce qu'elle va dire au lieu de le dire, tu perds l'échantillon avant qu'il ait vu ton produit.":
        "É de longe a causa mais comum. Se a sua abertura monta um cenário, se apresenta ou anuncia o que vai dizer em vez de dizer, você perde a amostra antes de ela ver o seu produto.",
    "Comment vérifier :": "Como checar:",
    "regarde ta propre vidéo son coupé, et arrête-toi à {0} seconde. Si tu ne sais pas encore de quoi ça parle, l'accroche est en cause.":
        "assista ao seu próprio vídeo sem som e pare no segundo {0}. Se você ainda não sabe do que se trata, o problema é o gancho.",
    "{0}. L'attention décroche au milieu": "{0}. A atenção cai no meio",
    "Le début tient, mais la vidéo s'installe : un plan trop long, une explication qui traîne, une transition molle. Le spectateur ne part pas brutalement, il glisse.":
        "O começo segura, mas o vídeo se acomoda: um plano longo demais, uma explicação que se arrasta, uma transição mole. O espectador não sai de repente, ele escorrega.",
    "repère le moment où toi-même tu as envie d'accélérer. C'est presque toujours là que la courbe chute.":
        "ache o momento em que você mesmo quer adiantar. É quase sempre ali que a curva cai.",
    "{0}. Le format contredit les codes actuels": "{0}. O formato contraria os códigos atuais",
    "Vidéo non verticale, bandes noires, texte illisible sans le son, sous-titres absents, durée qui ne correspond pas au sujet. Ces éléments ne rendent pas la vidéo mauvaise, mais ils la desservent auprès d'une audience qui regarde en mobilité, souvent sans le son.":
        "Vídeo fora do vertical, tarjas pretas, texto ilegível sem som, sem legendas, duração que não bate com o assunto. Nada disso deixa o vídeo ruim, mas atrapalha diante de um público que assiste na rua, muitas vezes sem som.",
    "ouvre ta vidéo sur ton téléphone, son coupé, en plein soleil. Si tu ne peux pas la suivre, l'algorithme n'est pas ton problème.":
        "abra seu vídeo no celular, sem som, no sol forte. Se não conseguir acompanhar, o algoritmo não é o seu problema.",
    "{0}. Le sujet ne correspond pas à ton audience habituelle": "{0}. O assunto não bate com seu público de sempre",
    "Un changement brusque de thème désoriente la diffusion : la vidéo est proposée à ton audience existante, qui ne réagit pas, et le test échoue. Ce n'est pas un bridage, c'est un décalage.":
        "Uma mudança brusca de tema desorienta a distribuição: o vídeo vai para o seu público atual, que não reage, e o teste falha. Não é limitação, é descompasso.",
    "compare le sujet de la vidéo qui stagne à celui de tes trois dernières vidéos qui ont fonctionné.":
        "compare o assunto do vídeo travado com o dos seus três últimos vídeos que funcionaram.",
    "{0}. Le produit n'est pas démontrable en vidéo courte": "{0}. O produto não dá para demonstrar em vídeo curto",
    "Certains produits se vendent mal sur ce format, non parce qu'ils sont mauvais, mais parce que leur bénéfice ne se voit pas. Un complément alimentaire, un service, un produit dont l'effet met des semaines : rien à montrer en dix secondes.":
        "Alguns produtos vendem mal nesse formato, não porque sejam ruins, mas porque o benefício não aparece. Um suplemento, um serviço, um produto cujo efeito leva semanas: nada para mostrar em dez segundos.",
    "demande-toi si tu peux prouver le bénéfice à l'image, sans l'expliquer. Si non, le problème est le choix du produit, pas la vidéo.":
        "pergunte-se se dá para provar o benefício na imagem, sem explicar. Se não, o problema é a escolha do produto, não o vídeo.",
    "Ce qu'il ne faut pas faire": "O que não fazer",
    "Supprimer la vidéo.": "Apagar o vídeo.",
    "Cela ne « relance » rien et te prive de la donnée qui t'aurait permis de comprendre.":
        "Isso não “reinicia” nada e te tira o dado que teria permitido entender.",
    "Republier à l'identique.": "Repostar igualzinho.",
    "Si le test a échoué une fois, il échouera de la même manière.": "Se o teste falhou uma vez, vai falhar do mesmo jeito.",
    "Tout changer d'un coup.": "Mudar tudo de uma vez.",
    "Accroche, montage, produit et légende modifiés simultanément : quel que soit le résultat, tu n'auras rien appris.":
        "Gancho, montagem, produto e legenda mudados ao mesmo tempo: dê no que der, você não terá aprendido nada.",
    "Acheter des vues.": "Comprar visualizações.",
    "Un engagement artificiel dégrade le signal que la plateforme utilise pour te qualifier.":
        "Engajamento artificial estraga justamente o sinal que a plataforma usa para te classificar.",
    "La méthode qui fait gagner du temps": "O método que economiza tempo",
    "Plutôt que de deviner laquelle des cinq causes te concerne, compare. Prends une vidéo de ta niche qui a fonctionné récemment, et la tienne qui a stagné. Note les deux sur les mêmes critères : accroche, rétention, argumentaire, émotion, appel à l'action, format. L'écart le plus large désigne ton chantier.":
        "Em vez de adivinhar qual das cinco causas é a sua, compare. Pegue um vídeo do seu nicho que funcionou há pouco e o seu que travou. Dê nota aos dois nos mesmos critérios: gancho, retenção, argumento, emoção, chamada para ação, formato. A maior diferença aponta o seu trabalho.",
    "C'est exactement ce que fait Qeerah, à partir d'un simple lien : l'analyse rend les sept dimensions notées, indique la seconde où l'attention décroche, liste les déclencheurs présents":
        "É exatamente o que a Qeerah faz, a partir de um simples link: a análise devolve as sete dimensões com nota, aponta o segundo em que a atenção cai, lista os gatilhos presentes",
    "et manquants": "e os que faltam",
    ", puis propose des accroches réécrites pour ton produit. En mode « explique-moi simplement », chaque note est accompagnée de l'action concrète à mener.":
        " e propõe ganchos reescritos para o seu produto. No modo “explica simples”, cada nota vem com a ação concreta a tomar.",
    "Comprends ce qui bloque sur ta vidéo": "Entenda o que está travando seu vídeo",
    "{0} jours d'accès complet, sans carte bancaire.": "{0} dias de acesso completo, sem cartão.",
    "Analyser ma vidéo": "Analisar meu vídeo",
    "Et si tout est correct mais que ça ne vend toujours pas ?": "E se estiver tudo certo e mesmo assim não vender?",
    "Vues et ventes sont deux problèmes distincts. Une vidéo peut très bien être diffusée largement et ne rien écouler : cela signifie qu'elle divertit sans donner envie d'acheter. Dans ce cas, ce n'est pas la rétention qu'il faut travailler, mais l'argumentaire et l'appel à l'action.":
        "Visualizações e vendas são dois problemas diferentes. Um vídeo pode ser distribuído bastante e não vender nada: isso quer dizer que ele entretém sem dar vontade de comprar. Nesse caso não é a retenção que se trabalha, é o argumento e a chamada para ação.",
    "Le rapport à surveiller n'est donc pas le nombre de vues, mais le nombre de ventes rapporté aux vues. Sur le marché français, où":
        "Ou seja, a relação a acompanhar não é o número de visualizações, e sim as vendas em relação às visualizações. No mercado francês, onde",
    "{0} % du chiffre d'affaires de TikTok Shop passe par les créateurs affiliés":
        "{0} % do faturamento do TikTok Shop passa pelos criadores afiliados",
    ", c'est ce rapport qui sépare un compte qui grossit d'un compte qui gagne de l'argent.":
        ", é essa relação que separa uma conta que cresce de uma conta que ganha dinheiro.",
    "Analyser une vidéo TikTok Shop": "Analisar um vídeo do TikTok Shop",
    "Les produits qui vendent en France": "Os produtos que vendem na França",
    "Guide complet TikTok Shop": "Guia completo do TikTok Shop",
    "Source du chiffre cité :": "Fonte do número citado:",
    ". Le fonctionnement de la diffusion décrit ici repose sur des observations largement partagées par les créateurs ; TikTok ne publie pas le détail de son système de recommandation.":
        ". O funcionamento da distribuição descrito aqui vem de observações amplamente compartilhadas pelos criadores; o TikTok não publica os detalhes do seu sistema de recomendação.",
}

T_LP_VUES["en-ie"] = dict(T_LP_VUES["en"])
T_LP_VUES["es-mx"] = dict(T_LP_VUES["es"])
