"""Séquence e-mail de l'essai — déclenchée par le comportement, vérifiée chaque heure.

  Moment     Condition                         Message (une seule action)
  ─────────  ────────────────────────────────  ──────────────────────────────────────
  inscription toujours                         bienvenue → prochaine étape de la mission
  +24 h      n'a pas analysé SA vidéo          analyse ta dernière vidéo
  jour 3     mission non terminée              une vidéo qui vend dans son pays → analyse-la
  jour 3     mission terminée                  de l'analyse à la création (accroches)
  jour 6     essai actif, non abonné           bilan perso + « ton essai se termine demain »
  jour 7     essai expiré, non abonné          bilan + lien direct vers le paiement
  jour 10    toujours pas abonné               dernier rappel court. Ensuite, plus rien.

Règles d'écriture : une idée et UN lien par e-mail (plus la désinscription,
obligatoire), objet court en minuscules, sans « gratuit / offre / exclusif » ni
point d'exclamation, tutoiement, signé « Aimeric — Qeerah », dans la langue de
l'utilisateur (`users.lang`, français par défaut).

Garanties :
- jamais deux fois le même e-mail à la même personne : journal `email_log`
  (contrainte d'unicité), repli sur `market_cache` tant que la migration
  supabase_migrations_emails_essai_v2.sql n'est pas jouée ; le journal est écrit
  APRÈS l'envoi réussi ;
- la séquence s'arrête dès que l'utilisateur s'abonne (tier ≠ free) ;
- `marketing_opt_out` respecté immédiatement, lien de désinscription signé ;
- adresses de test exclues (réputation d'expédition, cf. fin_essai.py) ;
- MODE TEST PAR DÉFAUT : tant que ESSAI_EMAILS_ACTIFS ≠ 1, rien ne part — les
  e-mails sont écrits en entier dans les journaux, rien n'est marqué. Les textes
  doivent être relus avant activation (décision du 26/10/2026).

Fenêtres de 24 h en heures depuis le début de l'essai : un passage horaire
manqué est rattrapé au suivant, et un compte ancien n'est jamais « rattrapé »
d'un coup sur toute la séquence.
"""
from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone
from html import escape
from urllib.parse import quote

import mission
from fin_essai import adresse_envoyable

LOT_MAX = 500
TRIAL_DAYS = 7

# Fenêtre de chaque e-mail, en HEURES depuis le début de l'essai.
FENETRES = {
    "bienvenue": (0, 24),
    "h24": (24, 48),
    "j3": (72, 96),
    "j6": (144, 168),
    "j7": (168, 192),
    "j10": (216, 240),
}

# Marché du Feed Radar regardé pour chaque langue (même choix que l'accueil).
REGION_PAR_LANGUE = {"fr": "FR", "en": "US", "pt-br": "BR", "es": "ES", "es-mx": "MX",
                     "it": "IT", "de": "DE"}

SIGNATURE = "Aimeric — Qeerah"


def actif() -> bool:
    return os.getenv("ESSAI_EMAILS_ACTIFS", "0").strip() == "1"


def _parse(valeur) -> datetime | None:
    if not valeur:
        return None
    try:
        d = datetime.fromisoformat(str(valeur).replace("Z", "+00:00"))
        return d if d.tzinfo else d.replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def moment_du(trial_ends_at: datetime, maintenant: datetime) -> str | None:
    """Moment de la séquence dont la fenêtre contient `maintenant`."""
    debut = trial_ends_at - timedelta(days=TRIAL_DAYS)
    heures = (maintenant - debut).total_seconds() / 3600
    return next((k for k, (lo, hi) in FENETRES.items() if lo <= heures < hi), None)


def langue(code: str | None) -> str:
    code = (code or "fr").strip().lower()
    code = {"en-ie": "en", "en-gb": "en", "en-us": "en", "pt": "pt-br"}.get(code, code)
    return code if code in TEXTES or code == "es-mx" else "fr"


# ── Les textes ─────────────────────────────────────────────────────────────
# Chaque e-mail : objet, paragraphes, bouton. `{bilan}` et `{video}` sont remplis
# au moment de l'envoi ; `{etape}` est le titre de la prochaine étape de mission.
TEXTES: dict[str, dict] = {
    "fr": {
        "salut": "Salut,",
        "etapes": {1: "analyse une vidéo qui vend", 2: "analyse ta dernière vidéo",
                   3: "génère 3 accroches pour ton produit"},
        "bienvenue": {"objet": "ton compte qeerah est prêt",
                      "corps": ["Ton compte est prêt. Ta mission tient en 3 étapes et te montre, en quelques minutes, ce qui sépare ta vidéo d'une vidéo qui vend.",
                                "Prochaine étape : {etape}."],
                      "bouton": "Continuer ma mission"},
        "h24": {"objet": "où tes spectateurs décrochent",
                "corps": ["Analyse ta dernière vidéo : tu vas voir à quelle seconde les gens décrochent, et ce qui la sépare d'une vidéo qui vend."],
                "bouton": "Analyser ma dernière vidéo"},
        "j3_radar": {"objet": "une vidéo qui vend en ce moment",
                     "corps": ["Cette vidéo de {auteur} vend en ce moment ({vues} vues).",
                               "Analyse-la : tu vas comprendre pourquoi elle marche, et ce que tu peux reproduire dans la tienne."],
                     "bouton": "Analyser cette vidéo"},
        "j3_feed": {"objet": "ce qui vend en ce moment",
                    "corps": ["Ouvre le Feed Radar, choisis une vidéo qui vend en ce moment et analyse-la : tu vas comprendre pourquoi elle marche, et ce que tu peux reproduire dans la tienne."],
                    "bouton": "Voir ce qui vend"},
        "j3_creation": {"objet": "de l'analyse à ta prochaine vidéo",
                        "corps": ["Tu as terminé ta mission : tu sais ce qui sépare ta vidéo d'une vidéo qui vend.",
                                  "Prochaine étape : en faire ta prochaine vidéo. Prends un produit, génère plusieurs angles, et teste deux accroches différentes cette semaine."],
                        "bouton": "Écrire mes prochaines accroches"},
        "j6": {"objet": "ton essai se termine demain",
               "corps": ["{bilan}", "Ton essai se termine demain. Tes analyses restent accessibles ensuite."],
               "corps_vide": ["Ton essai se termine demain. Il te reste le temps d'analyser une vidéo qui vend, puis la tienne."],
               "bouton": "Ouvrir mon espace"},
        "j7": {"objet": "ton essai en chiffres",
               "corps": ["{bilan}", "Ton essai est terminé. Pour continuer à comprendre ce qui vend chaque mois, continue avec Qeerah Pro : 29,99 € par mois, sans engagement."],
               "corps_vide": ["Ton essai est terminé. Avec Qeerah Pro, tu comprends chaque mois pourquoi les vidéos TikTok Shop vendent, et quoi reproduire dans les tiennes : 29,99 € par mois, sans engagement."],
               "bouton": "Continuer avec Qeerah Pro"},
        "j10": {"objet": "une dernière chose",
                "corps": ["C'est mon dernier message à ce sujet. Si tu veux reprendre là où tu t'es arrêté, ton compte et tes analyses t'attendent."],
                "bouton": "Reprendre avec Qeerah Pro"},
        "bilan": {"intro": "Pendant ton essai, tu as ", "et": " et ",
                  "videos": ("analysé 1 vidéo", "analysé {n} vidéos"),
                  "leviers": ("identifié 1 levier de vente", "identifié {n} leviers de vente"),
                  "accroches": ("généré 1 accroche", "généré {n} accroches"),
                  "meilleur": "Ta meilleure vidéo : {n}/100."},
        "pied": "Tu reçois cet e-mail parce que tu as un compte Qeerah. ",
        "desinscription": "Ne plus recevoir ces e-mails",
    },
    "en": {
        "salut": "Hi,",
        "etapes": {1: "analyse a video that sells", 2: "analyse your latest video",
                   3: "write 3 hooks for your product"},
        "bienvenue": {"objet": "your qeerah account is ready",
                      "corps": ["Your account is ready. Your mission takes 3 steps and shows you, in a few minutes, what separates your video from a video that sells.",
                                "Next step: {etape}."],
                      "bouton": "Continue my mission"},
        "h24": {"objet": "where your viewers drop off",
                "corps": ["Analyse your latest video: you will see the exact second people drop off, and what separates it from a video that sells."],
                "bouton": "Analyse my latest video"},
        "j3_radar": {"objet": "a video that is selling right now",
                     "corps": ["This video by {auteur} is selling right now ({vues} views).",
                               "Analyse it: you will understand why it works, and what you can reproduce in yours."],
                     "bouton": "Analyse this video"},
        "j3_feed": {"objet": "what is selling right now",
                    "corps": ["Open the Feed Radar, pick a video that is selling right now and analyse it: you will understand why it works, and what you can reproduce in yours."],
                    "bouton": "See what is selling"},
        "j3_creation": {"objet": "from analysis to your next video",
                        "corps": ["You finished your mission: you know what separates your video from a video that sells.",
                                  "Next step: turn it into a video. Pick a product, write several angles, and test two different hooks this week."],
                        "bouton": "Write my next hooks"},
        "j6": {"objet": "your trial ends tomorrow",
               "corps": ["{bilan}", "Your trial ends tomorrow. Your analyses stay available afterwards."],
               "corps_vide": ["Your trial ends tomorrow. You still have time to analyse a video that sells, then yours."],
               "bouton": "Open my space"},
        "j7": {"objet": "your trial in numbers",
               "corps": ["{bilan}", "Your trial has ended. To keep understanding what sells every month, continue with Qeerah Pro: €29.99 a month, no commitment."],
               "corps_vide": ["Your trial has ended. With Qeerah Pro, you understand every month why TikTok Shop videos sell, and what to reproduce in yours: €29.99 a month, no commitment."],
               "bouton": "Continue with Qeerah Pro"},
        "j10": {"objet": "one last thing",
                "corps": ["This is my last message about it. If you want to pick up where you left off, your account and your analyses are waiting for you."],
                "bouton": "Pick up with Qeerah Pro"},
        "bilan": {"intro": "During your trial, you ", "et": " and ",
                  "videos": ("analysed 1 video", "analysed {n} videos"),
                  "leviers": ("identified 1 selling lever", "identified {n} selling levers"),
                  "accroches": ("wrote 1 hook", "wrote {n} hooks"),
                  "meilleur": "Your best video: {n}/100."},
        "pied": "You are receiving this email because you have a Qeerah account. ",
        "desinscription": "Stop receiving these emails",
    },
    "pt-br": {
        "salut": "Oi,",
        "etapes": {1: "analise um vídeo que vende", 2: "analise o seu último vídeo",
                   3: "crie 3 ganchos para o seu produto"},
        "bienvenue": {"objet": "sua conta qeerah está pronta",
                      "corps": ["Sua conta está pronta. Sua missão tem 3 etapas e mostra, em poucos minutos, o que separa o seu vídeo de um vídeo que vende.",
                                "Próximo passo: {etape}."],
                      "bouton": "Continuar minha missão"},
        "h24": {"objet": "onde seus espectadores desistem",
                "corps": ["Analise o seu último vídeo: você vai ver em que segundo as pessoas desistem, e o que o separa de um vídeo que vende."],
                "bouton": "Analisar meu último vídeo"},
        "j3_radar": {"objet": "um vídeo que está vendendo agora",
                     "corps": ["Este vídeo de {auteur} está vendendo agora ({vues} visualizações).",
                               "Analise: você vai entender por que ele funciona, e o que pode reproduzir no seu."],
                     "bouton": "Analisar este vídeo"},
        "j3_feed": {"objet": "o que está vendendo agora",
                    "corps": ["Abra o Feed Radar, escolha um vídeo que está vendendo agora e analise: você vai entender por que ele funciona, e o que pode reproduzir no seu."],
                    "bouton": "Ver o que está vendendo"},
        "j3_creation": {"objet": "da análise ao seu próximo vídeo",
                        "corps": ["Você concluiu sua missão: sabe o que separa o seu vídeo de um vídeo que vende.",
                                  "Próximo passo: transformar isso em vídeo. Escolha um produto, crie vários ângulos e teste dois ganchos diferentes esta semana."],
                        "bouton": "Criar meus próximos ganchos"},
        "j6": {"objet": "seu teste termina amanhã",
               "corps": ["{bilan}", "Seu teste termina amanhã. Suas análises continuam disponíveis depois."],
               "corps_vide": ["Seu teste termina amanhã. Ainda dá tempo de analisar um vídeo que vende, e depois o seu."],
               "bouton": "Abrir meu espaço"},
        "j7": {"objet": "seu teste em números",
               "corps": ["{bilan}", "Seu teste terminou. Para continuar entendendo o que vende todo mês, continue com o Qeerah Pro: 29,99 € por mês, sem fidelidade."],
               "corps_vide": ["Seu teste terminou. Com o Qeerah Pro, você entende todo mês por que os vídeos do TikTok Shop vendem e o que reproduzir nos seus: 29,99 € por mês, sem fidelidade."],
               "bouton": "Continuar com o Qeerah Pro"},
        "j10": {"objet": "uma última coisa",
                "corps": ["Esta é minha última mensagem sobre isso. Se quiser retomar de onde parou, sua conta e suas análises estão te esperando."],
                "bouton": "Retomar com o Qeerah Pro"},
        "bilan": {"intro": "Durante o seu teste, você ", "et": " e ",
                  "videos": ("analisou 1 vídeo", "analisou {n} vídeos"),
                  "leviers": ("identificou 1 alavanca de venda", "identificou {n} alavancas de venda"),
                  "accroches": ("criou 1 gancho", "criou {n} ganchos"),
                  "meilleur": "Seu melhor vídeo: {n}/100."},
        "pied": "Você recebe este e-mail porque tem uma conta Qeerah. ",
        "desinscription": "Não receber mais estes e-mails",
    },
    "es": {
        "salut": "Hola,",
        "etapes": {1: "analiza un vídeo que vende", 2: "analiza tu último vídeo",
                   3: "crea 3 ganchos para tu producto"},
        "bienvenue": {"objet": "tu cuenta de qeerah está lista",
                      "corps": ["Tu cuenta está lista. Tu misión tiene 3 pasos y te muestra, en pocos minutos, qué separa tu vídeo de un vídeo que vende.",
                                "Siguiente paso: {etape}."],
                      "bouton": "Seguir con mi misión"},
        "h24": {"objet": "dónde dejan de mirar tus espectadores",
                "corps": ["Analiza tu último vídeo: vas a ver en qué segundo la gente deja de mirar, y qué lo separa de un vídeo que vende."],
                "bouton": "Analizar mi último vídeo"},
        "j3_radar": {"objet": "un vídeo que vende ahora mismo",
                     "corps": ["Este vídeo de {auteur} vende ahora mismo ({vues} visualizaciones).",
                               "Analízalo: vas a entender por qué funciona, y qué puedes reproducir en el tuyo."],
                     "bouton": "Analizar este vídeo"},
        "j3_feed": {"objet": "lo que se vende ahora mismo",
                    "corps": ["Abre el Feed Radar, elige un vídeo que vende ahora mismo y analízalo: vas a entender por qué funciona, y qué puedes reproducir en el tuyo."],
                    "bouton": "Ver lo que se vende"},
        "j3_creation": {"objet": "del análisis a tu próximo vídeo",
                        "corps": ["Has terminado tu misión: sabes qué separa tu vídeo de un vídeo que vende.",
                                  "Siguiente paso: convertirlo en vídeo. Elige un producto, crea varios ángulos y prueba dos ganchos distintos esta semana."],
                        "bouton": "Escribir mis próximos ganchos"},
        "j6": {"objet": "tu prueba termina mañana",
               "corps": ["{bilan}", "Tu prueba termina mañana. Tus análisis siguen disponibles después."],
               "corps_vide": ["Tu prueba termina mañana. Todavía tienes tiempo de analizar un vídeo que vende, y luego el tuyo."],
               "bouton": "Abrir mi espacio"},
        "j7": {"objet": "tu prueba en cifras",
               "corps": ["{bilan}", "Tu prueba ha terminado. Para seguir entendiendo lo que vende cada mes, continúa con Qeerah Pro: 29,99 € al mes, sin permanencia."],
               "corps_vide": ["Tu prueba ha terminado. Con Qeerah Pro entiendes cada mes por qué venden los vídeos de TikTok Shop y qué reproducir en los tuyos: 29,99 € al mes, sin permanencia."],
               "bouton": "Continuar con Qeerah Pro"},
        "j10": {"objet": "una última cosa",
                "corps": ["Es mi último mensaje sobre esto. Si quieres retomar donde lo dejaste, tu cuenta y tus análisis te esperan."],
                "bouton": "Retomar con Qeerah Pro"},
        "bilan": {"intro": "Durante tu prueba, ", "et": " y ",
                  "videos": ("analizaste 1 vídeo", "analizaste {n} vídeos"),
                  "leviers": ("identificaste 1 palanca de venta", "identificaste {n} palancas de venta"),
                  "accroches": ("creaste 1 gancho", "creaste {n} ganchos"),
                  "meilleur": "Tu mejor vídeo: {n}/100."},
        "pied": "Recibes este correo porque tienes una cuenta de Qeerah. ",
        "desinscription": "No recibir más estos correos",
    },
    "it": {
        "salut": "Ciao,",
        "etapes": {1: "analizza un video che vende", 2: "analizza il tuo ultimo video",
                   3: "crea 3 ganci per il tuo prodotto"},
        "bienvenue": {"objet": "il tuo account qeerah è pronto",
                      "corps": ["Il tuo account è pronto. La tua missione ha 3 passaggi e ti mostra, in pochi minuti, cosa separa il tuo video da un video che vende.",
                                "Prossimo passo: {etape}."],
                      "bouton": "Continua la mia missione"},
        "h24": {"objet": "dove i tuoi spettatori smettono di guardare",
                "corps": ["Analizza il tuo ultimo video: vedrai in quale secondo le persone smettono di guardare, e cosa lo separa da un video che vende."],
                "bouton": "Analizza il mio ultimo video"},
        "j3_radar": {"objet": "un video che vende in questo momento",
                     "corps": ["Questo video di {auteur} vende in questo momento ({vues} visualizzazioni).",
                               "Analizzalo: capirai perché funziona, e cosa puoi riprodurre nel tuo."],
                     "bouton": "Analizza questo video"},
        "j3_feed": {"objet": "cosa vende in questo momento",
                    "corps": ["Apri il Feed Radar, scegli un video che vende in questo momento e analizzalo: capirai perché funziona, e cosa puoi riprodurre nel tuo."],
                    "bouton": "Vedi cosa vende"},
        "j3_creation": {"objet": "dall'analisi al tuo prossimo video",
                        "corps": ["Hai completato la tua missione: sai cosa separa il tuo video da un video che vende.",
                                  "Prossimo passo: trasformalo in un video. Scegli un prodotto, crea più angoli e prova due ganci diversi questa settimana."],
                        "bouton": "Scrivi i miei prossimi ganci"},
        "j6": {"objet": "la tua prova finisce domani",
               "corps": ["{bilan}", "La tua prova finisce domani. Le tue analisi restano disponibili anche dopo."],
               "corps_vide": ["La tua prova finisce domani. Hai ancora il tempo di analizzare un video che vende, e poi il tuo."],
               "bouton": "Apri il mio spazio"},
        "j7": {"objet": "la tua prova in cifre",
               "corps": ["{bilan}", "La tua prova è finita. Per continuare a capire cosa vende ogni mese, continua con Qeerah Pro: 29,99 € al mese, senza vincoli."],
               "corps_vide": ["La tua prova è finita. Con Qeerah Pro capisci ogni mese perché i video di TikTok Shop vendono e cosa riprodurre nei tuoi: 29,99 € al mese, senza vincoli."],
               "bouton": "Continua con Qeerah Pro"},
        "j10": {"objet": "un'ultima cosa",
                "corps": ["È il mio ultimo messaggio su questo. Se vuoi riprendere da dove avevi lasciato, il tuo account e le tue analisi ti aspettano."],
                "bouton": "Riprendi con Qeerah Pro"},
        "bilan": {"intro": "Durante la tua prova hai ", "et": " e ",
                  "videos": ("analizzato 1 video", "analizzato {n} video"),
                  "leviers": ("individuato 1 leva di vendita", "individuato {n} leve di vendita"),
                  "accroches": ("creato 1 gancio", "creato {n} ganci"),
                  "meilleur": "Il tuo video migliore: {n}/100."},
        "pied": "Ricevi questa email perché hai un account Qeerah. ",
        "desinscription": "Non ricevere più queste email",
    },
    "de": {
        "salut": "Hallo,",
        "etapes": {1: "analysiere ein Video, das verkauft", 2: "analysiere dein letztes Video",
                   3: "schreib 3 Hooks für dein Produkt"},
        "bienvenue": {"objet": "dein qeerah-konto ist bereit",
                      "corps": ["Dein Konto ist bereit. Deine Mission hat 3 Schritte und zeigt dir in wenigen Minuten, was dein Video von einem Video unterscheidet, das verkauft.",
                                "Nächster Schritt: {etape}."],
                      "bouton": "Meine Mission fortsetzen"},
        "h24": {"objet": "wo deine zuschauer abspringen",
                "corps": ["Analysiere dein letztes Video: Du siehst, in welcher Sekunde die Leute abspringen, und was es von einem Video unterscheidet, das verkauft."],
                "bouton": "Mein letztes Video analysieren"},
        "j3_radar": {"objet": "ein video, das gerade verkauft",
                     "corps": ["Dieses Video von {auteur} verkauft gerade ({vues} Aufrufe).",
                               "Analysiere es: Du verstehst, warum es funktioniert, und was du in deinem übernehmen kannst."],
                     "bouton": "Dieses Video analysieren"},
        "j3_feed": {"objet": "was gerade verkauft",
                    "corps": ["Öffne den Feed Radar, wähle ein Video, das gerade verkauft, und analysiere es: Du verstehst, warum es funktioniert, und was du in deinem übernehmen kannst."],
                    "bouton": "Sehen, was verkauft"},
        "j3_creation": {"objet": "von der analyse zu deinem nächsten video",
                        "corps": ["Du hast deine Mission abgeschlossen: Du weißt, was dein Video von einem Video unterscheidet, das verkauft.",
                                  "Nächster Schritt: Mach ein Video daraus. Nimm ein Produkt, erstelle mehrere Blickwinkel und teste diese Woche zwei verschiedene Hooks."],
                        "bouton": "Meine nächsten Hooks schreiben"},
        "j6": {"objet": "dein test endet morgen",
               "corps": ["{bilan}", "Dein Test endet morgen. Deine Analysen bleiben danach verfügbar."],
               "corps_vide": ["Dein Test endet morgen. Du hast noch Zeit, ein Video zu analysieren, das verkauft, und danach dein eigenes."],
               "bouton": "Meinen Bereich öffnen"},
        "j7": {"objet": "dein test in zahlen",
               "corps": ["{bilan}", "Dein Test ist vorbei. Um jeden Monat weiter zu verstehen, was verkauft, mach mit Qeerah Pro weiter: 29,99 € im Monat, ohne Bindung."],
               "corps_vide": ["Dein Test ist vorbei. Mit Qeerah Pro verstehst du jeden Monat, warum TikTok-Shop-Videos verkaufen und was du in deinen übernehmen kannst: 29,99 € im Monat, ohne Bindung."],
               "bouton": "Mit Qeerah Pro weitermachen"},
        "j10": {"objet": "eine letzte sache",
                "corps": ["Das ist meine letzte Nachricht dazu. Wenn du dort weitermachen willst, wo du aufgehört hast, warten dein Konto und deine Analysen auf dich."],
                "bouton": "Mit Qeerah Pro weitermachen"},
        "bilan": {"intro": "Während deines Tests hast du ", "et": " und ",
                  "videos": ("1 Video analysiert", "{n} Videos analysiert"),
                  "leviers": ("1 Verkaufshebel erkannt", "{n} Verkaufshebel erkannt"),
                  "accroches": ("1 Hook erstellt", "{n} Hooks erstellt"),
                  "meilleur": "Dein bestes Video: {n}/100."},
        "pied": "Du bekommst diese E-Mail, weil du ein Qeerah-Konto hast. ",
        "desinscription": "Diese E-Mails nicht mehr erhalten",
    },
}
TEXTES["es-mx"] = TEXTES["es"]


def phrase_bilan(b: dict, lang: str) -> str:
    """« Pendant ton essai, tu as analysé 8 vidéos, identifié 14 leviers de vente
    et généré 9 accroches. Ta meilleure vidéo : 74/100. » — données réelles seules."""
    tb = TEXTES[langue(lang)]["bilan"]
    morceaux = []
    for cle in ("videos", "leviers", "accroches"):
        n = int(b.get(cle) or 0)
        if n:
            un, plusieurs = tb[cle]
            morceaux.append(un if n == 1 else plusieurs.format(n=n))
    phrase = ""
    if morceaux:
        liste = morceaux[0] if len(morceaux) == 1 else ", ".join(morceaux[:-1]) + tb["et"] + morceaux[-1]
        phrase = tb["intro"] + liste + "."
    if b.get("meilleur"):
        phrase = (phrase + " " if phrase else "") + tb["meilleur"].format(n=int(b["meilleur"]))
    return phrase


def _vues(n) -> str:
    try:
        return f"{int(n):,}".replace(",", " ")
    except (TypeError, ValueError):
        return "—"


def video_du_pays(supabase, lang: str) -> dict | None:
    """La vidéo la plus vue du Feed Radar dans le pays de l'utilisateur, ou None.
    Jamais celle d'un autre pays : l'e-mail promet « dans ton pays »."""
    region = REGION_PAR_LANGUE.get(langue(lang), "FR")
    try:
        r = (supabase.table("feed_radar_videos").select("video_url,oembed_author_name,views")
             .eq("region", region).order("views", desc=True).limit(1).execute())
        v = (r.data or [None])[0]
        if v and v.get("video_url"):
            v["video_url"] = v["video_url"].split("?", 1)[0]
            return v
    except Exception as e:
        print(f"[essai_emails] Feed Radar {region} : {e}")
    return None


# ── Choix et rédaction ─────────────────────────────────────────────────────
def choisir(moment: str, etat: dict) -> str | None:
    """Clé de l'e-mail à envoyer à ce moment, ou None si rien d'utile à dire."""
    if moment == "h24":
        return None if any(e["id"] == 2 and e["fait"] for e in etat.get("etapes", [])) else "h24"
    if moment == "j3":
        return "j3_creation" if etat.get("terminee") else "j3_radar"
    return moment


def contenu(cle: str, etat: dict, lang: str, liens: dict, video: dict | None = None
            ) -> tuple[str, str, str] | None:
    """(objet, titre, corps HTML). `liens` : chemin de chaque bouton, déjà suivi."""
    from email_service import _button

    T = TEXTES[langue(lang)]
    if cle == "j3_radar" and not video:
        cle = "j3_feed"
    e = T[cle]
    bilan = phrase_bilan(etat.get("bilan") or {}, lang)
    paragraphes = e["corps_vide"] if (not bilan and "corps_vide" in e) else e["corps"]
    prochaine = etat.get("prochaine") or 1
    valeurs = {
        "bilan": bilan, "etape": T["etapes"].get(prochaine, T["etapes"][1]),
        "auteur": "@" + str((video or {}).get("oembed_author_name") or "").lstrip("@"),
        "vues": _vues((video or {}).get("views")),
    }
    corps = "".join(f"<p>{escape(p.format(**valeurs))}</p>" for p in paragraphes if p.format(**valeurs))
    html = (f"<p>{escape(T['salut'])}</p>{corps}"
            f"{_button(escape(e['bouton']), liens[cle])}"
            f"<p>{escape(SIGNATURE)}</p>")
    return e["objet"], escape(e["objet"][:1].upper() + e["objet"][1:]), html


def chemin(cle: str, etat: dict, video: dict | None = None) -> str:
    """Page où mène le bouton de chaque e-mail (avant suivi du clic)."""
    if cle == "bienvenue":
        return f"/app?mission={etat.get('prochaine') or 1}"
    if cle == "h24":
        return "/app?mission=2"
    if cle == "j3_radar" and video:
        return "/app?analyser=" + quote(video["video_url"], safe="")
    if cle in ("j3_radar", "j3_feed"):
        return "/app?onglet=feedradar"
    if cle == "j3_creation":
        return "/scripts"
    if cle == "j6":
        return "/app"
    return "/abonnement/payer"           # j7, j10 : Stripe Checkout directement


def lien_suivi(app_url: str, cle: str, page: str, email: str) -> str:
    """Le clic passe par /e/<cle> (compté, sans donnée personnelle), puis la page.
    Le lien de paiement est signé : il ouvre Checkout pour CE compte uniquement."""
    if page == "/abonnement/payer":
        from auth import make_payment_token
        page = f"/abonnement/payer?e={quote(email)}&s={make_payment_token(email)}"
    return f"{app_url}/e/{cle}?r={quote(page, safe='')}"


# ── Journal ────────────────────────────────────────────────────────────────
def deja_envoye(supabase, email: str, cle: str) -> bool:
    try:
        r = supabase.table("email_log").select("id").eq("email", email).eq("cle", cle).limit(1).execute()
        return bool(r.data)
    except Exception:
        pass
    try:   # table pas encore créée : ancien marqueur
        r = (supabase.table("market_cache").select("cache_key")
             .eq("cache_key", f"mail_essai:{cle}:{email}").limit(1).execute())
        return bool(r.data)
    except Exception as e:
        # Dans le doute, on s'abstient : un message manquant vaut mieux qu'un doublon.
        print(f"[essai_emails] journal illisible ({email}) : {e} → on s'abstient")
        return True


def journaliser(supabase, email: str, cle: str) -> None:
    maintenant = datetime.now(timezone.utc)
    try:
        supabase.table("email_log").insert({"email": email, "cle": cle, "statut": "envoye",
                                            "envoye_le": maintenant.isoformat()}).execute()
        return
    except Exception:
        pass
    try:
        supabase.table("market_cache").upsert({
            "cache_key": f"mail_essai:{cle}:{email}",
            "payload": {"etape": cle, "envoye_le": maintenant.isoformat()},
            "expires_at": (maintenant + timedelta(days=3650)).isoformat(),
        }).execute()
    except Exception as e:
        print(f"⚠️  [essai_emails] {email} : envoyé mais non journalisé ({e}) — risque de doublon.")


# ── Envoi ──────────────────────────────────────────────────────────────────
def pied(email: str, lang: str, app_url: str) -> str:
    from auth import make_unsubscribe_token
    T = TEXTES[langue(lang)]
    unsub = f"{app_url}/unsubscribe?e={quote(email)}&s={make_unsubscribe_token(email)}"
    return (f'<p style="font-size:12px;color:#9a9ab0;margin-top:22px;">{escape(T["pied"])}'
            f'<a href="{unsub}" style="color:#9a9ab0;">{escape(T["desinscription"])}</a>.</p>')


async def envoyer(supabase, email: str, cle: str, lang: str, etat: dict,
                  video: dict | None = None, simulation: bool | None = None) -> str:
    """Rédige et envoie (ou simule) UN e-mail. Renvoie envoye | simule | echec | deja."""
    from email_service import email_service, _wrap

    if deja_envoye(supabase, email, cle):
        return "deja"
    simulation = (not actif()) if simulation is None else simulation
    app_url = os.getenv("APP_PUBLIC_URL", "https://www.qeerah.com").rstrip("/")
    cle_effective = "j3_feed" if (cle == "j3_radar" and not video) else cle
    liens = {cle_effective: lien_suivi(app_url, cle, chemin(cle_effective, etat, video), email)}
    objet, titre, corps = contenu(cle_effective, etat, lang, liens, video)
    html = _wrap(titre, corps + pied(email, lang, app_url), lang=langue(lang))

    if simulation:
        # Mode test : l'e-mail entier dans les journaux, rien ne part, rien n'est marqué.
        print(f"[essai_emails] SIMULATION {cle} ({langue(lang)}) → {email} : « {objet} »\n{corps}")
        return "simule"
    if await email_service._send(email, objet, html):
        journaliser(supabase, email, cle)
        try:
            import entonnoir
            entonnoir.enregistrer(supabase, "email_envoye", detail=cle, lang=langue(lang))
        except Exception:
            pass
        return "envoye"
    return "echec"


def _comptes(supabase, borne: str) -> list[dict]:
    """Comptes en essai (ou essai fini depuis peu). `lang` facultative (migration)."""
    for cols in ("email,tier,marketing_opt_out,trial_ends_at,lang",
                 "email,tier,marketing_opt_out,trial_ends_at"):
        try:
            r = (supabase.table("users").select(cols)
                 .eq("tier", "free").gte("trial_ends_at", borne).limit(LOT_MAX).execute())
            return r.data or []
        except Exception as e:
            print(f"[essai_emails] lecture des comptes ({cols}) : {e}")
    raise RuntimeError("lecture des comptes impossible")


async def run(supabase, maintenant: datetime | None = None) -> dict:
    """Passage horaire : envoie (ou simule) les e-mails dus. Ne lève jamais."""
    if not supabase:
        return {"ok": False, "reason": "supabase indisponible", "sent": 0}

    maintenant = maintenant or datetime.now(timezone.utc)
    simulation = not actif()
    compte = {"ok": True, "simulation": simulation, "sent": 0, "skipped": 0, "failed": 0,
              "par_email": {}}
    # Fin d'essai jusqu'à 3 jours après la fin (j10 = jour 10 depuis le début).
    borne = (maintenant - timedelta(days=4)).isoformat()
    try:
        rows = _comptes(supabase, borne)
    except Exception as ex:
        return {**compte, "ok": False, "error": str(ex)}

    videos: dict[str, dict | None] = {}
    for u in rows:
        email = (u.get("email") or "").strip().lower()
        fin = _parse(u.get("trial_ends_at"))
        envoyable, _motif = adresse_envoyable(email)
        if not email or not fin or u.get("marketing_opt_out") or not envoyable:
            compte["skipped"] += 1
            continue
        moment = moment_du(fin, maintenant)
        if not moment:
            compte["skipped"] += 1
            continue
        etat = mission.etat(supabase, email)
        cle = choisir(moment, etat)
        if not cle:
            compte["skipped"] += 1
            continue
        lang = langue(u.get("lang"))
        video = None
        if cle == "j3_radar":
            if lang not in videos:
                videos[lang] = video_du_pays(supabase, lang)
            video = videos[lang]
        statut = await envoyer(supabase, email, cle, lang, etat, video, simulation)
        if statut in ("envoye", "simule"):
            compte["sent" if statut == "envoye" else "skipped"] += 1
            compte["par_email"][cle] = compte["par_email"].get(cle, 0) + 1
        elif statut == "echec":
            compte["failed"] += 1
        else:
            compte["skipped"] += 1
    return compte


async def bienvenue(supabase, email: str, lang: str) -> str:
    """À l'inscription. Mode test → l'e-mail de bienvenue historique part comme
    avant (rien ne change en production tant que la séquence n'est pas activée)."""
    if not actif():
        from email_service import email_service
        await email_service.send_welcome_email(email)
        return "historique"
    return await envoyer(supabase, email, "bienvenue", lang, mission.etat(supabase, email))
