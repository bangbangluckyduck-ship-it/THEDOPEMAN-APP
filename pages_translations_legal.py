"""Traductions des pages LÉGALES — CGU, CGV, confidentialité, mentions légales.

⚠️ CE QUI FAIT FOI RESTE LE FRANÇAIS.

Ces traductions existent pour être COMPRISES, pas pour créer sept contrats
opposables. Un client allemand doit pouvoir lire ce qu'il accepte — c'est le
sens du droit européen de la consommation — mais une nuance mal rendue dans des
CGV ne doit pas devenir la règle applicable. D'où l'avertissement `AVIS`
ci-dessous, inséré en haut de CHAQUE page légale traduite (et d'aucune page
française), juste sous le titre : là où il est lu, pas en pied de page.

Décision d'Aimeric, le 07/09/2026, à la question posée explicitement.

Deux conséquences pratiques pour qui modifiera ce fichier :

  • le texte français reste la référence. Si les deux divergent, c'est la
    traduction qu'on corrige, jamais l'inverse ;
  • les identités ne se traduisent pas : DOPE VENTURES, SASU, RCS Paris, SIREN,
    l'adresse du siège, les noms des sous-traitants (Render, Supabase, Stripe,
    Sentry, Resend) et l'adresse de contact restent tels quels. Les traduire
    rendrait le document faux.

Les mentions de textes français (article 293 B du CGI, loi Informatique et
Libertés, Code de la consommation) sont conservées et nommées comme telles :
ce sont les textes réellement applicables, les travestir en équivalent local
serait une erreur juridique.
"""
from __future__ import annotations

# ═══════════════════════════════════════════════════════════════════════════
# L'AVERTISSEMENT — inséré sous le titre des pages légales traduites
# ═══════════════════════════════════════════════════════════════════════════
_STYLE = ('style="background:#fff8e1;border:1px solid #ffd54f;border-radius:10px;'
          'padding:12px 14px;margin:0 0 20px;font-size:13.5px;line-height:1.55"')

AVIS: dict[str, str] = {
    "en": f'<div {_STYLE}><strong>Translation for information only.</strong> '
          'This is a courtesy translation of a document written in French. '
          'Only the French version is legally binding; if the two differ, the '
          'French text prevails. <a href="/terms" hreflang="fr">Read the French version</a>.</div>',
    "pt-br": f'<div {_STYLE}><strong>Tradução apenas informativa.</strong> '
             'Esta é uma tradução de cortesia de um documento redigido em francês. '
             'Só a versão francesa tem valor legal; havendo divergência, prevalece '
             'o texto francês. <a href="/terms" hreflang="fr">Ler a versão francesa</a>.</div>',
    "es": f'<div {_STYLE}><strong>Traducción solo informativa.</strong> '
          'Esta es una traducción de cortesía de un documento redactado en francés. '
          'Solo la versión francesa tiene valor legal; si ambas difieren, prevalece '
          'el texto francés. <a href="/terms" hreflang="fr">Leer la versión francesa</a>.</div>',
    "it": f'<div {_STYLE}><strong>Traduzione a solo scopo informativo.</strong> '
          'Questa è una traduzione di cortesia di un documento redatto in francese. '
          'Solo la versione francese ha valore legale; in caso di divergenza prevale '
          'il testo francese. <a href="/terms" hreflang="fr">Leggi la versione francese</a>.</div>',
    "de": f'<div {_STYLE}><strong>Übersetzung nur zur Information.</strong> '
          'Dies ist eine Übersetzung eines auf Französisch verfassten Dokuments. '
          'Rechtlich verbindlich ist allein die französische Fassung; bei '
          'Abweichungen gilt der französische Text. '
          '<a href="/terms" hreflang="fr">Zur französischen Fassung</a>.</div>',
}
AVIS["en-ie"] = AVIS["en"]
AVIS["es-mx"] = AVIS["es"]


def avis_pour(chemin_fr: str) -> dict[str, str]:
    """L'avertissement, avec son lien pointant sur la page française lue.

    Le lien doit mener à la version française DE CETTE page : renvoyer les CGV
    vers les CGU serait pire que pas de lien du tout.
    """
    # `hreflang="fr"` sur ce lien n'est pas décoratif : c'est lui qui empêche la
    # réécriture des liens internes de le faire pointer sur la traduction que le
    # visiteur est déjà en train de lire (cf. pages_i18n.liens_internes).
    return {lang: texte.replace('href="/terms"', f'href="{chemin_fr}"')
            for lang, texte in AVIS.items()}


# ═══════════════════════════════════════════════════════════════════════════
# /terms — conditions générales d'utilisation
# ═══════════════════════════════════════════════════════════════════════════
T_TERMS: dict[str, dict[str, str]] = {
    "en": {
        "Conditions d'utilisation — Qeerah": "Terms of use — Qeerah",
        "Conditions générales d'utilisation de Qeerah.": "Qeerah's general terms of use.",
        "← Retour à l'accueil": "← Back to home",
        "Conditions d'utilisation": "Terms of use",
        "Qeerah — édité par Dope Ventures · Dernière mise à jour : juin {0}":
            "Qeerah — published by Dope Ventures · Last updated: June {0}",
        "{0}. Éditeur & mentions légales": "{0}. Publisher & legal information",
        "Le site et l'application": "The website and application",
        "sont édités par :": "are published by:",
        ", Société par actions simplifiée à associé unique (SASU)":
            ", a French simplified joint-stock company with a sole shareholder (SASU)",
        "Capital social : {0} €": "Share capital: €{0}",
        "RCS Paris {0} (SIREN {1})": "Paris Trade and Companies Register {0} (SIREN {1})",
        "Siège social : {0} rue Vivienne, {1} Paris, France":
            "Registered office: {0} rue Vivienne, {1} Paris, France",
        "Directeur de la publication : Aimeric Bourgon (Président)":
            "Publication director: Aimeric Bourgon (President)",
        "Contact :": "Contact:",
        "Hébergement :": "Hosting:",
        "l'application est hébergée par Render Services, Inc. (San Francisco, CA, États-Unis) ; la base de données par Supabase. Les données sont hébergées sur des infrastructures conformes au RGPD.":
            "the application is hosted by Render Services, Inc. (San Francisco, CA, USA); the database by Supabase. Data is hosted on GDPR-compliant infrastructure.",
        "{0}. Description du service": "{0}. What the service is",
        "Qeerah est une application d'analyse de vidéos TikTok par intelligence artificielle, destinée à aider les créateurs et vendeurs à améliorer leurs contenus. Le service est fourni « tel quel », sans garantie de résultats commerciaux.":
            "Qeerah is an application that analyses TikTok videos using artificial intelligence, to help creators and sellers improve their content. The service is provided “as is”, with no guarantee of commercial results.",
        "{0}. Utilisation acceptable": "{0}. Acceptable use",
        "En utilisant ce service, vous acceptez de :": "By using this service, you agree to:",
        "n'utiliser le service qu'à des fins légales ;": "use the service for lawful purposes only;",
        "ne pas tenter de contourner les quotas ni la sécurité ;":
            "make no attempt to bypass quotas or security;",
        "respecter les droits de propriété intellectuelle et les conditions de TikTok ;":
            "respect intellectual property rights and TikTok's own terms;",
        "ne connecter que des comptes TikTok dont vous êtes le titulaire ou pour lesquels vous êtes autorisé.":
            "connect only TikTok accounts you own or are authorised to use.",
        "{0}. Connexion d'un compte TikTok": "{0}. Connecting a TikTok account",
        "La connexion d'un compte TikTok est facultative et soumise à votre consentement explicite via l'autorisation officielle TikTok. Les données récupérées sont utilisées conformément à notre":
            "Connecting a TikTok account is optional and requires your explicit consent through TikTok's official authorisation flow. The data retrieved is used in accordance with our",
        "politique de confidentialité": "privacy policy",
        ". Vous pouvez révoquer cet accès à tout moment.": ". You can revoke this access at any time.",
        "{0}. Abonnements et paiements": "{0}. Subscriptions and payments",
        "Les abonnements sont sans engagement et résiliables à tout moment depuis votre espace client. Aucun remboursement pour les périodes déjà consommées. Les paiements sont traités par":
            "Subscriptions carry no commitment and can be cancelled at any time from your account. No refunds are given for periods already used. Payments are processed by",
        "{0}. Limitation de responsabilité": "{0}. Limitation of liability",
        "Les analyses fournies par l'IA sont des estimations et ne constituent pas des conseils financiers ou commerciaux garantis. Dope Ventures ne peut être tenu responsable des décisions prises sur la base de ces analyses.":
            "The analyses produced by the AI are estimates and do not constitute guaranteed financial or commercial advice. Dope Ventures cannot be held liable for decisions taken on the basis of those analyses.",
        "{0}. Droit applicable": "{0}. Governing law",
        "Les présentes conditions sont soumises au droit français. En cas de litige, les tribunaux français sont compétents.":
            "These terms are governed by French law. In the event of a dispute, the French courts have jurisdiction.",
        "Voir la politique de confidentialité →": "See the privacy policy →",
    },
    "pt-br": {
        "Conditions d'utilisation — Qeerah": "Termos de uso — Qeerah",
        "Conditions générales d'utilisation de Qeerah.": "Termos gerais de uso da Qeerah.",
        "← Retour à l'accueil": "← Voltar ao início",
        "Conditions d'utilisation": "Termos de uso",
        "Qeerah — édité par Dope Ventures · Dernière mise à jour : juin {0}":
            "Qeerah — publicado pela Dope Ventures · Última atualização: junho de {0}",
        "{0}. Éditeur & mentions légales": "{0}. Responsável pelo site e dados legais",
        "Le site et l'application": "O site e o aplicativo",
        "sont édités par :": "são publicados por:",
        ", Société par actions simplifiée à associé unique (SASU)":
            ", sociedade por ações simplificada de sócio único de direito francês (SASU)",
        "Capital social : {0} €": "Capital social: € {0}",
        "RCS Paris {0} (SIREN {1})": "Registro comercial de Paris {0} (SIREN {1})",
        "Siège social : {0} rue Vivienne, {1} Paris, France":
            "Sede: {0} rue Vivienne, {1} Paris, França",
        "Directeur de la publication : Aimeric Bourgon (Président)":
            "Responsável pela publicação: Aimeric Bourgon (Presidente)",
        "Contact :": "Contato:",
        "Hébergement :": "Hospedagem:",
        "l'application est hébergée par Render Services, Inc. (San Francisco, CA, États-Unis) ; la base de données par Supabase. Les données sont hébergées sur des infrastructures conformes au RGPD.":
            "o aplicativo é hospedado pela Render Services, Inc. (San Francisco, CA, EUA); o banco de dados pela Supabase. Os dados ficam em infraestrutura em conformidade com o RGPD.",
        "{0}. Description du service": "{0}. O que é o serviço",
        "Qeerah est une application d'analyse de vidéos TikTok par intelligence artificielle, destinée à aider les créateurs et vendeurs à améliorer leurs contenus. Le service est fourni « tel quel », sans garantie de résultats commerciaux.":
            "A Qeerah é um aplicativo de análise de vídeos do TikTok por inteligência artificial, feito para ajudar criadores e vendedores a melhorar seus conteúdos. O serviço é fornecido “como está”, sem garantia de resultados comerciais.",
        "{0}. Utilisation acceptable": "{0}. Uso aceitável",
        "En utilisant ce service, vous acceptez de :": "Ao usar este serviço, você concorda em:",
        "n'utiliser le service qu'à des fins légales ;": "usar o serviço apenas para fins lícitos;",
        "ne pas tenter de contourner les quotas ni la sécurité ;":
            "não tentar burlar cotas nem a segurança;",
        "respecter les droits de propriété intellectuelle et les conditions de TikTok ;":
            "respeitar os direitos de propriedade intelectual e os termos do TikTok;",
        "ne connecter que des comptes TikTok dont vous êtes le titulaire ou pour lesquels vous êtes autorisé.":
            "conectar apenas contas do TikTok que sejam suas ou que você esteja autorizado a usar.",
        "{0}. Connexion d'un compte TikTok": "{0}. Conexão de uma conta do TikTok",
        "La connexion d'un compte TikTok est facultative et soumise à votre consentement explicite via l'autorisation officielle TikTok. Les données récupérées sont utilisées conformément à notre":
            "Conectar uma conta do TikTok é opcional e depende do seu consentimento explícito pela autorização oficial do TikTok. Os dados obtidos são usados conforme a nossa",
        "politique de confidentialité": "política de privacidade",
        ". Vous pouvez révoquer cet accès à tout moment.": ". Você pode revogar esse acesso quando quiser.",
        "{0}. Abonnements et paiements": "{0}. Assinaturas e pagamentos",
        "Les abonnements sont sans engagement et résiliables à tout moment depuis votre espace client. Aucun remboursement pour les périodes déjà consommées. Les paiements sont traités par":
            "As assinaturas não têm fidelidade e podem ser canceladas a qualquer momento na sua conta. Não há reembolso de períodos já usados. Os pagamentos são processados pela",
        "{0}. Limitation de responsabilité": "{0}. Limitação de responsabilidade",
        "Les analyses fournies par l'IA sont des estimations et ne constituent pas des conseils financiers ou commerciaux garantis. Dope Ventures ne peut être tenu responsable des décisions prises sur la base de ces analyses.":
            "As análises produzidas pela IA são estimativas e não constituem aconselhamento financeiro ou comercial garantido. A Dope Ventures não se responsabiliza por decisões tomadas com base nelas.",
        "{0}. Droit applicable": "{0}. Lei aplicável",
        "Les présentes conditions sont soumises au droit français. En cas de litige, les tribunaux français sont compétents.":
            "Estes termos são regidos pela lei francesa. Em caso de litígio, os tribunais franceses são competentes.",
        "Voir la politique de confidentialité →": "Ver a política de privacidade →",
    },
    "es": {
        "Conditions d'utilisation — Qeerah": "Condiciones de uso — Qeerah",
        "Conditions générales d'utilisation de Qeerah.": "Condiciones generales de uso de Qeerah.",
        "← Retour à l'accueil": "← Volver al inicio",
        "Conditions d'utilisation": "Condiciones de uso",
        "Qeerah — édité par Dope Ventures · Dernière mise à jour : juin {0}":
            "Qeerah — editado por Dope Ventures · Última actualización: junio de {0}",
        "{0}. Éditeur & mentions légales": "{0}. Editor e información legal",
        "Le site et l'application": "El sitio y la aplicación",
        "sont édités par :": "están editados por:",
        ", Société par actions simplifiée à associé unique (SASU)":
            ", sociedad por acciones simplificada unipersonal de derecho francés (SASU)",
        "Capital social : {0} €": "Capital social: {0} €",
        "RCS Paris {0} (SIREN {1})": "Registro Mercantil de París {0} (SIREN {1})",
        "Siège social : {0} rue Vivienne, {1} Paris, France":
            "Domicilio social: {0} rue Vivienne, {1} París, Francia",
        "Directeur de la publication : Aimeric Bourgon (Président)":
            "Director de la publicación: Aimeric Bourgon (Presidente)",
        "Contact :": "Contacto:",
        "Hébergement :": "Alojamiento:",
        "l'application est hébergée par Render Services, Inc. (San Francisco, CA, États-Unis) ; la base de données par Supabase. Les données sont hébergées sur des infrastructures conformes au RGPD.":
            "la aplicación está alojada por Render Services, Inc. (San Francisco, CA, EE. UU.); la base de datos por Supabase. Los datos se alojan en infraestructuras conformes al RGPD.",
        "{0}. Description du service": "{0}. Descripción del servicio",
        "Qeerah est une application d'analyse de vidéos TikTok par intelligence artificielle, destinée à aider les créateurs et vendeurs à améliorer leurs contenus. Le service est fourni « tel quel », sans garantie de résultats commerciaux.":
            "Qeerah es una aplicación de análisis de vídeos de TikTok mediante inteligencia artificial, pensada para ayudar a creadores y vendedores a mejorar sus contenidos. El servicio se presta “tal cual”, sin garantía de resultados comerciales.",
        "{0}. Utilisation acceptable": "{0}. Uso aceptable",
        "En utilisant ce service, vous acceptez de :": "Al usar este servicio, aceptas:",
        "n'utiliser le service qu'à des fins légales ;": "usar el servicio solo con fines lícitos;",
        "ne pas tenter de contourner les quotas ni la sécurité ;":
            "no intentar sortear las cuotas ni la seguridad;",
        "respecter les droits de propriété intellectuelle et les conditions de TikTok ;":
            "respetar los derechos de propiedad intelectual y las condiciones de TikTok;",
        "ne connecter que des comptes TikTok dont vous êtes le titulaire ou pour lesquels vous êtes autorisé.":
            "conectar únicamente cuentas de TikTok de las que seas titular o para las que estés autorizado.",
        "{0}. Connexion d'un compte TikTok": "{0}. Conexión de una cuenta de TikTok",
        "La connexion d'un compte TikTok est facultative et soumise à votre consentement explicite via l'autorisation officielle TikTok. Les données récupérées sont utilisées conformément à notre":
            "Conectar una cuenta de TikTok es opcional y requiere tu consentimiento explícito a través de la autorización oficial de TikTok. Los datos obtenidos se usan conforme a nuestra",
        "politique de confidentialité": "política de privacidad",
        ". Vous pouvez révoquer cet accès à tout moment.": ". Puedes revocar este acceso cuando quieras.",
        "{0}. Abonnements et paiements": "{0}. Suscripciones y pagos",
        "Les abonnements sont sans engagement et résiliables à tout moment depuis votre espace client. Aucun remboursement pour les périodes déjà consommées. Les paiements sont traités par":
            "Las suscripciones no tienen permanencia y se pueden cancelar cuando quieras desde tu cuenta. No se reembolsan los periodos ya consumidos. Los pagos los procesa",
        "{0}. Limitation de responsabilité": "{0}. Limitación de responsabilidad",
        "Les analyses fournies par l'IA sont des estimations et ne constituent pas des conseils financiers ou commerciaux garantis. Dope Ventures ne peut être tenu responsable des décisions prises sur la base de ces analyses.":
            "Los análisis que produce la IA son estimaciones y no constituyen asesoramiento financiero o comercial garantizado. Dope Ventures no se hace responsable de las decisiones tomadas a partir de ellos.",
        "{0}. Droit applicable": "{0}. Ley aplicable",
        "Les présentes conditions sont soumises au droit français. En cas de litige, les tribunaux français sont compétents.":
            "Estas condiciones se rigen por el derecho francés. En caso de litigio, los tribunales franceses son competentes.",
        "Voir la politique de confidentialité →": "Ver la política de privacidad →",
    },
    "it": {
        "Conditions d'utilisation — Qeerah": "Condizioni d'uso — Qeerah",
        "Conditions générales d'utilisation de Qeerah.": "Condizioni generali d'uso di Qeerah.",
        "← Retour à l'accueil": "← Torna alla home",
        "Conditions d'utilisation": "Condizioni d'uso",
        "Qeerah — édité par Dope Ventures · Dernière mise à jour : juin {0}":
            "Qeerah — pubblicato da Dope Ventures · Ultimo aggiornamento: giugno {0}",
        "{0}. Éditeur & mentions légales": "{0}. Editore e informazioni legali",
        "Le site et l'application": "Il sito e l'applicazione",
        "sont édités par :": "sono pubblicati da:",
        ", Société par actions simplifiée à associé unique (SASU)":
            ", società per azioni semplificata con socio unico di diritto francese (SASU)",
        "Capital social : {0} €": "Capitale sociale: {0} €",
        "RCS Paris {0} (SIREN {1})": "Registro delle imprese di Parigi {0} (SIREN {1})",
        "Siège social : {0} rue Vivienne, {1} Paris, France":
            "Sede legale: {0} rue Vivienne, {1} Parigi, Francia",
        "Directeur de la publication : Aimeric Bourgon (Président)":
            "Direttore della pubblicazione: Aimeric Bourgon (Presidente)",
        "Contact :": "Contatto:",
        "Hébergement :": "Hosting:",
        "l'application est hébergée par Render Services, Inc. (San Francisco, CA, États-Unis) ; la base de données par Supabase. Les données sont hébergées sur des infrastructures conformes au RGPD.":
            "l'applicazione è ospitata da Render Services, Inc. (San Francisco, CA, USA); il database da Supabase. I dati risiedono su infrastrutture conformi al GDPR.",
        "{0}. Description du service": "{0}. Descrizione del servizio",
        "Qeerah est une application d'analyse de vidéos TikTok par intelligence artificielle, destinée à aider les créateurs et vendeurs à améliorer leurs contenus. Le service est fourni « tel quel », sans garantie de résultats commerciaux.":
            "Qeerah è un'applicazione che analizza i video TikTok con l'intelligenza artificiale, pensata per aiutare creator e venditori a migliorare i propri contenuti. Il servizio è fornito “così com'è”, senza garanzia di risultati commerciali.",
        "{0}. Utilisation acceptable": "{0}. Uso accettabile",
        "En utilisant ce service, vous acceptez de :": "Usando questo servizio accetti di:",
        "n'utiliser le service qu'à des fins légales ;": "usare il servizio solo per scopi leciti;",
        "ne pas tenter de contourner les quotas ni la sécurité ;":
            "non tentare di aggirare le quote né la sicurezza;",
        "respecter les droits de propriété intellectuelle et les conditions de TikTok ;":
            "rispettare i diritti di proprietà intellettuale e le condizioni di TikTok;",
        "ne connecter que des comptes TikTok dont vous êtes le titulaire ou pour lesquels vous êtes autorisé.":
            "collegare solo account TikTok di cui sei titolare o per i quali sei autorizzato.",
        "{0}. Connexion d'un compte TikTok": "{0}. Collegamento di un account TikTok",
        "La connexion d'un compte TikTok est facultative et soumise à votre consentement explicite via l'autorisation officielle TikTok. Les données récupérées sont utilisées conformément à notre":
            "Collegare un account TikTok è facoltativo e richiede il tuo consenso esplicito tramite l'autorizzazione ufficiale di TikTok. I dati raccolti sono usati secondo la nostra",
        "politique de confidentialité": "informativa sulla privacy",
        ". Vous pouvez révoquer cet accès à tout moment.": ". Puoi revocare questo accesso quando vuoi.",
        "{0}. Abonnements et paiements": "{0}. Abbonamenti e pagamenti",
        "Les abonnements sont sans engagement et résiliables à tout moment depuis votre espace client. Aucun remboursement pour les périodes déjà consommées. Les paiements sont traités par":
            "Gli abbonamenti sono senza vincoli e disdicibili in qualsiasi momento dal tuo account. Nessun rimborso per i periodi già usati. I pagamenti sono gestiti da",
        "{0}. Limitation de responsabilité": "{0}. Limitazione di responsabilità",
        "Les analyses fournies par l'IA sont des estimations et ne constituent pas des conseils financiers ou commerciaux garantis. Dope Ventures ne peut être tenu responsable des décisions prises sur la base de ces analyses.":
            "Le analisi prodotte dall'IA sono stime e non costituiscono consulenza finanziaria o commerciale garantita. Dope Ventures non risponde delle decisioni prese sulla loro base.",
        "{0}. Droit applicable": "{0}. Legge applicabile",
        "Les présentes conditions sont soumises au droit français. En cas de litige, les tribunaux français sont compétents.":
            "Le presenti condizioni sono soggette al diritto francese. In caso di controversia sono competenti i tribunali francesi.",
        "Voir la politique de confidentialité →": "Vedi l'informativa sulla privacy →",
    },
    "de": {
        "Conditions d'utilisation — Qeerah": "Nutzungsbedingungen — Qeerah",
        "Conditions générales d'utilisation de Qeerah.": "Allgemeine Nutzungsbedingungen von Qeerah.",
        "← Retour à l'accueil": "← Zurück zur Startseite",
        "Conditions d'utilisation": "Nutzungsbedingungen",
        "Qeerah — édité par Dope Ventures · Dernière mise à jour : juin {0}":
            "Qeerah — herausgegeben von Dope Ventures · Zuletzt aktualisiert: Juni {0}",
        "{0}. Éditeur & mentions légales": "{0}. Herausgeber & Impressumsangaben",
        "Le site et l'application": "Website und Anwendung",
        "sont édités par :": "werden herausgegeben von:",
        ", Société par actions simplifiée à associé unique (SASU)":
            ", vereinfachte Aktiengesellschaft französischen Rechts mit einem Alleingesellschafter (SASU)",
        "Capital social : {0} €": "Stammkapital: {0} €",
        "RCS Paris {0} (SIREN {1})": "Handelsregister Paris {0} (SIREN {1})",
        "Siège social : {0} rue Vivienne, {1} Paris, France":
            "Sitz: {0} rue Vivienne, {1} Paris, Frankreich",
        "Directeur de la publication : Aimeric Bourgon (Président)":
            "Verantwortlich für den Inhalt: Aimeric Bourgon (Präsident)",
        "Contact :": "Kontakt:",
        "Hébergement :": "Hosting:",
        "l'application est hébergée par Render Services, Inc. (San Francisco, CA, États-Unis) ; la base de données par Supabase. Les données sont hébergées sur des infrastructures conformes au RGPD.":
            "Die Anwendung wird von Render Services, Inc. (San Francisco, CA, USA) gehostet, die Datenbank von Supabase. Die Daten liegen auf DSGVO-konformer Infrastruktur.",
        "{0}. Description du service": "{0}. Beschreibung des Dienstes",
        "Qeerah est une application d'analyse de vidéos TikTok par intelligence artificielle, destinée à aider les créateurs et vendeurs à améliorer leurs contenus. Le service est fourni « tel quel », sans garantie de résultats commerciaux.":
            "Qeerah ist eine Anwendung, die TikTok-Videos mit künstlicher Intelligenz analysiert, um Creators und Verkäufern zu helfen, ihre Inhalte zu verbessern. Der Dienst wird “wie besehen” bereitgestellt, ohne Zusage geschäftlicher Ergebnisse.",
        "{0}. Utilisation acceptable": "{0}. Zulässige Nutzung",
        "En utilisant ce service, vous acceptez de :": "Mit der Nutzung dieses Dienstes erklärst du dich bereit:",
        "n'utiliser le service qu'à des fins légales ;": "den Dienst nur zu rechtmäßigen Zwecken zu nutzen;",
        "ne pas tenter de contourner les quotas ni la sécurité ;":
            "weder Kontingente noch Sicherheitsmechanismen zu umgehen;",
        "respecter les droits de propriété intellectuelle et les conditions de TikTok ;":
            "geistige Eigentumsrechte und die Bedingungen von TikTok zu achten;",
        "ne connecter que des comptes TikTok dont vous êtes le titulaire ou pour lesquels vous êtes autorisé.":
            "nur TikTok-Konten zu verbinden, die dir gehören oder für die du berechtigt bist.",
        "{0}. Connexion d'un compte TikTok": "{0}. Verbinden eines TikTok-Kontos",
        "La connexion d'un compte TikTok est facultative et soumise à votre consentement explicite via l'autorisation officielle TikTok. Les données récupérées sont utilisées conformément à notre":
            "Ein TikTok-Konto zu verbinden ist freiwillig und erfordert deine ausdrückliche Einwilligung über die offizielle TikTok-Autorisierung. Die abgerufenen Daten werden gemäß unserer",
        "politique de confidentialité": "Datenschutzerklärung",
        ". Vous pouvez révoquer cet accès à tout moment.": " verwendet. Du kannst diesen Zugriff jederzeit widerrufen.",
        "{0}. Abonnements et paiements": "{0}. Abos und Zahlungen",
        "Les abonnements sont sans engagement et résiliables à tout moment depuis votre espace client. Aucun remboursement pour les périodes déjà consommées. Les paiements sont traités par":
            "Abos sind ohne Bindung und jederzeit im Kundenbereich kündbar. Für bereits genutzte Zeiträume gibt es keine Erstattung. Zahlungen werden abgewickelt von",
        "{0}. Limitation de responsabilité": "{0}. Haftungsbeschränkung",
        "Les analyses fournies par l'IA sont des estimations et ne constituent pas des conseils financiers ou commerciaux garantis. Dope Ventures ne peut être tenu responsable des décisions prises sur la base de ces analyses.":
            "Die von der KI gelieferten Analysen sind Schätzungen und stellen keine zugesicherte finanzielle oder geschäftliche Beratung dar. Dope Ventures haftet nicht für Entscheidungen, die auf ihrer Grundlage getroffen werden.",
        "{0}. Droit applicable": "{0}. Anwendbares Recht",
        "Les présentes conditions sont soumises au droit français. En cas de litige, les tribunaux français sont compétents.":
            "Diese Bedingungen unterliegen französischem Recht. Bei Streitigkeiten sind die französischen Gerichte zuständig.",
        "Voir la politique de confidentialité →": "Zur Datenschutzerklärung →",
    },
}

for _d in (T_TERMS,):
    _d["en-ie"] = dict(_d["en"])
    _d["es-mx"] = dict(_d["es"])


# ═══════════════════════════════════════════════════════════════════════════
# /mentions-legales
# Les identités ne se traduisent pas : dénomination, forme sociale, RCS, SIREN,
# SIRET, code APE, adresse. Seuls les LIBELLÉS qui les introduisent le sont.
# ═══════════════════════════════════════════════════════════════════════════
T_MENTIONS: dict[str, dict[str, str]] = {
    "en": {
        "Mentions légales — Qeerah": "Legal notice — Qeerah",
        "Mentions légales de Qeerah, édité par DOPE VENTURES.":
            "Legal notice for Qeerah, published by DOPE VENTURES.",
        "← Retour à l'accueil": "← Back to home",
        "Mentions légales": "Legal notice",
        "Conformément à la loi n° {0}-{1} du {2} juin {3} pour la confiance dans l'économie numérique (LCEN).":
            "As required by French law no. {0}-{1} of {2} June {3} on confidence in the digital economy (LCEN).",
        "{0}. Éditeur du site": "{0}. Site publisher",
        "Dénomination sociale": "Company name",
        "Forme juridique": "Legal form",
        "SASU au capital de {0} €": "SASU (French simplified joint-stock company, sole shareholder) with share capital of €{0}",
        "Siège social": "Registered office",
        "{0} rue Vivienne, {1} Paris, France": "{0} rue Vivienne, {1} Paris, France",
        "Immatriculation": "Registration",
        "RCS Paris {0}": "Paris Trade and Companies Register {0}",
        "SIREN : {0}": "SIREN: {0}",
        "SIRET (siège) : {0}": "SIRET (registered office): {0}",
        "Code d'activité (APE/NAF)": "Activity code (APE/NAF)",
        "{0}Z — Programmation informatique": "{0}Z — Computer programming",
        "Taxe sur la valeur ajoutée": "Value added tax",
        "TVA non applicable, article {0} B du CGI":
            "No VAT charged — French small-business exemption, art. {0} B of the French tax code",
        "Président": "President",
        "Directeur de la publication": "Publication director",
        "Contact": "Contact",
        "{0}. Hébergeur": "{0}. Hosting provider",
        "Le site est hébergé par :": "The site is hosted by:",
        "{0} Brannan Street, Suite {1}, San Francisco, CA {2}, États-Unis":
            "{0} Brannan Street, Suite {1}, San Francisco, CA {2}, United States",
        "{0}. Propriété intellectuelle": "{0}. Intellectual property",
        "L'ensemble des éléments composant le site — structure, textes, visuels, logo, marque Qeerah, code source et bases de données — est protégé par le droit de la propriété intellectuelle et demeure la propriété exclusive de DOPE VENTURES, sauf mention contraire. Toute reproduction, représentation ou exploitation, totale ou partielle, sans autorisation écrite préalable est interdite.":
            "Everything that makes up this site — structure, text, visuals, logo, the Qeerah brand, source code and databases — is protected by intellectual property law and remains the exclusive property of DOPE VENTURES unless stated otherwise. Any reproduction, display or use, in whole or in part, without prior written permission is prohibited.",
        "Les contenus analysés par le service (vidéos, images, textes) restent la propriété de leurs auteurs respectifs. Qeerah n'en revendique aucun droit et n'en effectue aucune republication.":
            "Content analysed by the service (videos, images, text) remains the property of its respective authors. Qeerah claims no rights over it and republishes none of it.",
        "{0}. Marques de tiers": "{0}. Third-party trademarks",
        "TikTok et TikTok Shop sont des marques déposées de leurs titulaires respectifs. Qeerah est un service indépendant, sans lien, partenariat ni affiliation avec ces sociétés, et n'est ni approuvé ni sponsorisé par elles.":
            "TikTok and TikTok Shop are registered trademarks of their respective owners. Qeerah is an independent service with no connection, partnership or affiliation with those companies, and is neither endorsed nor sponsored by them.",
        "{0}. Données personnelles": "{0}. Personal data",
        "Le traitement des données personnelles est décrit dans notre":
            "How personal data is processed is described in our",
        "politique de confidentialité": "privacy policy",
        ". Conformément au Règlement (UE) {0}/{1} et à la loi Informatique et Libertés, tu disposes d'un droit d'accès, de rectification, d'effacement, de portabilité, de limitation et d'opposition, exerçable à l'adresse":
            ". Under Regulation (EU) {0}/{1} and the French Data Protection Act, you have the right to access, correct, erase, port, restrict and object to the processing of your data. To exercise those rights, write to",
        "{0}. Cookies et traceurs": "{0}. Cookies and trackers",
        "Les traceurs déposés, leur finalité et leur durée de conservation sont détaillés dans la":
            "The trackers used, what they are for and how long they are kept are set out in the",
        ". Tu peux à tout moment modifier ton choix depuis le lien « Gérer les cookies » présent en pied de page.":
            ". You can change your choice at any time from the “Manage cookies” link in the footer.",
        "{0}. Conditions de vente": "{0}. Terms of sale",
        "Les modalités d'abonnement, de facturation et de résiliation figurent dans les":
            "Subscription, billing and cancellation terms are set out in the",
        "conditions générales de vente": "general terms of sale",
        ". Les conditions d'utilisation du service sont décrites dans les":
            ". The rules for using the service are set out in the",
        "conditions générales d'utilisation": "general terms of use",
        "{0}. Médiation de la consommation": "{0}. Consumer mediation",
        "Conformément à l'article L.{0}-{1} du Code de la consommation, le consommateur peut recourir gratuitement à un médiateur de la consommation en vue de la résolution amiable d'un litige. Le médiateur désigné par DOPE VENTURES est le":
            "Under article L.{0}-{1} of the French Consumer Code, consumers may use a consumer mediator free of charge to settle a dispute amicably. The mediator appointed by DOPE VENTURES is",
        ", {0} rue Saint Jean, {1} Paris —": ", {0} rue Saint Jean, {1} Paris —",
        "{0}. Responsabilité": "{0}. Liability",
        "Les analyses produites par le service reposent sur des traitements automatisés et de l'intelligence artificielle. Elles constituent des estimations à visée indicative et ne garantissent aucun résultat commercial. DOPE VENTURES ne saurait être tenue responsable des décisions prises sur leur fondement.":
            "The analyses produced by the service rely on automated processing and artificial intelligence. They are estimates offered as guidance and guarantee no commercial result. DOPE VENTURES cannot be held liable for decisions taken on their basis.",
        "{0}. Droit applicable": "{0}. Governing law",
        "Les présentes mentions légales sont soumises au droit français. En cas de litige et à défaut de résolution amiable, les tribunaux français sont compétents.":
            "This legal notice is governed by French law. In the event of a dispute that cannot be settled amicably, the French courts have jurisdiction.",
    },
    "pt-br": {
        "Mentions légales — Qeerah": "Informações legais — Qeerah",
        "Mentions légales de Qeerah, édité par DOPE VENTURES.":
            "Informações legais da Qeerah, publicada pela DOPE VENTURES.",
        "← Retour à l'accueil": "← Voltar ao início",
        "Mentions légales": "Informações legais",
        "Conformément à la loi n° {0}-{1} du {2} juin {3} pour la confiance dans l'économie numérique (LCEN).":
            "Conforme a lei francesa nº {0}-{1}, de {2} de junho de {3}, sobre a confiança na economia digital (LCEN).",
        "{0}. Éditeur du site": "{0}. Responsável pelo site",
        "Dénomination sociale": "Razão social",
        "Forme juridique": "Forma jurídica",
        "SASU au capital de {0} €": "SASU (sociedade por ações simplificada de sócio único, direito francês) com capital de € {0}",
        "Siège social": "Sede",
        "{0} rue Vivienne, {1} Paris, France": "{0} rue Vivienne, {1} Paris, França",
        "Immatriculation": "Registro",
        "RCS Paris {0}": "Registro comercial de Paris {0}",
        "SIREN : {0}": "SIREN: {0}",
        "SIRET (siège) : {0}": "SIRET (sede): {0}",
        "Code d'activité (APE/NAF)": "Código de atividade (APE/NAF)",
        "{0}Z — Programmation informatique": "{0}Z — Programação de computadores",
        "Taxe sur la valeur ajoutée": "Imposto sobre valor agregado",
        "TVA non applicable, article {0} B du CGI":
            "Sem cobrança de IVA — isenção de microempresa francesa, art. {0} B do código tributário francês",
        "Président": "Presidente",
        "Directeur de la publication": "Responsável pela publicação",
        "Contact": "Contato",
        "{0}. Hébergeur": "{0}. Hospedagem",
        "Le site est hébergé par :": "O site é hospedado por:",
        "{0} Brannan Street, Suite {1}, San Francisco, CA {2}, États-Unis":
            "{0} Brannan Street, Suite {1}, San Francisco, CA {2}, Estados Unidos",
        "{0}. Propriété intellectuelle": "{0}. Propriedade intelectual",
        "L'ensemble des éléments composant le site — structure, textes, visuels, logo, marque Qeerah, code source et bases de données — est protégé par le droit de la propriété intellectuelle et demeure la propriété exclusive de DOPE VENTURES, sauf mention contraire. Toute reproduction, représentation ou exploitation, totale ou partielle, sans autorisation écrite préalable est interdite.":
            "Tudo o que compõe o site — estrutura, textos, imagens, logotipo, marca Qeerah, código-fonte e bancos de dados — é protegido pelo direito de propriedade intelectual e permanece propriedade exclusiva da DOPE VENTURES, salvo indicação em contrário. Qualquer reprodução, exibição ou uso, total ou parcial, sem autorização prévia por escrito é proibida.",
        "Les contenus analysés par le service (vidéos, images, textes) restent la propriété de leurs auteurs respectifs. Qeerah n'en revendique aucun droit et n'en effectue aucune republication.":
            "Os conteúdos analisados pelo serviço (vídeos, imagens, textos) continuam sendo de seus autores. A Qeerah não reivindica nenhum direito sobre eles nem os republica.",
        "{0}. Marques de tiers": "{0}. Marcas de terceiros",
        "TikTok et TikTok Shop sont des marques déposées de leurs titulaires respectifs. Qeerah est un service indépendant, sans lien, partenariat ni affiliation avec ces sociétés, et n'est ni approuvé ni sponsorisé par elles.":
            "TikTok e TikTok Shop são marcas registradas de seus respectivos titulares. A Qeerah é um serviço independente, sem vínculo, parceria ou afiliação com essas empresas, e não é aprovada nem patrocinada por elas.",
        "{0}. Données personnelles": "{0}. Dados pessoais",
        "Le traitement des données personnelles est décrit dans notre":
            "O tratamento dos dados pessoais está descrito na nossa",
        "politique de confidentialité": "política de privacidade",
        ". Conformément au Règlement (UE) {0}/{1} et à la loi Informatique et Libertés, tu disposes d'un droit d'accès, de rectification, d'effacement, de portabilité, de limitation et d'opposition, exerçable à l'adresse":
            ". Conforme o Regulamento (UE) {0}/{1} e a lei francesa de proteção de dados, você tem direito de acesso, retificação, exclusão, portabilidade, limitação e oposição, exercíveis pelo endereço",
        "{0}. Cookies et traceurs": "{0}. Cookies e rastreadores",
        "Les traceurs déposés, leur finalité et leur durée de conservation sont détaillés dans la":
            "Os rastreadores usados, para que servem e por quanto tempo ficam guardados estão detalhados na",
        ". Tu peux à tout moment modifier ton choix depuis le lien « Gérer les cookies » présent en pied de page.":
            ". Você pode mudar sua escolha quando quiser pelo link “Gerenciar cookies” no rodapé.",
        "{0}. Conditions de vente": "{0}. Condições de venda",
        "Les modalités d'abonnement, de facturation et de résiliation figurent dans les":
            "As regras de assinatura, cobrança e cancelamento estão nas",
        "conditions générales de vente": "condições gerais de venda",
        ". Les conditions d'utilisation du service sont décrites dans les":
            ". As regras de uso do serviço estão nos",
        "conditions générales d'utilisation": "termos gerais de uso",
        "{0}. Médiation de la consommation": "{0}. Mediação de consumo",
        "Conformément à l'article L.{0}-{1} du Code de la consommation, le consommateur peut recourir gratuitement à un médiateur de la consommation en vue de la résolution amiable d'un litige. Le médiateur désigné par DOPE VENTURES est le":
            "Conforme o artigo L.{0}-{1} do Código do Consumidor francês, o consumidor pode recorrer gratuitamente a um mediador de consumo para resolver um litígio de forma amigável. O mediador designado pela DOPE VENTURES é o",
        ", {0} rue Saint Jean, {1} Paris —": ", {0} rue Saint Jean, {1} Paris —",
        "{0}. Responsabilité": "{0}. Responsabilidade",
        "Les analyses produites par le service reposent sur des traitements automatisés et de l'intelligence artificielle. Elles constituent des estimations à visée indicative et ne garantissent aucun résultat commercial. DOPE VENTURES ne saurait être tenue responsable des décisions prises sur leur fondement.":
            "As análises produzidas pelo serviço vêm de processamento automatizado e de inteligência artificial. São estimativas de caráter indicativo e não garantem resultado comercial nenhum. A DOPE VENTURES não se responsabiliza por decisões tomadas com base nelas.",
        "{0}. Droit applicable": "{0}. Lei aplicável",
        "Les présentes mentions légales sont soumises au droit français. En cas de litige et à défaut de résolution amiable, les tribunaux français sont compétents.":
            "Estas informações legais são regidas pela lei francesa. Em caso de litígio sem solução amigável, os tribunais franceses são competentes.",
    },
}

T_MENTIONS["es"] = {
    "Mentions légales — Qeerah": "Aviso legal — Qeerah",
    "Mentions légales de Qeerah, édité par DOPE VENTURES.":
        "Aviso legal de Qeerah, editada por DOPE VENTURES.",
    "← Retour à l'accueil": "← Volver al inicio",
    "Mentions légales": "Aviso legal",
    "Conformément à la loi n° {0}-{1} du {2} juin {3} pour la confiance dans l'économie numérique (LCEN).":
        "Conforme a la ley francesa n.º {0}-{1}, de {2} de junio de {3}, para la confianza en la economía digital (LCEN).",
    "{0}. Éditeur du site": "{0}. Editor del sitio",
    "Dénomination sociale": "Denominación social",
    "Forme juridique": "Forma jurídica",
    "SASU au capital de {0} €": "SASU (sociedad por acciones simplificada unipersonal, derecho francés) con capital de {0} €",
    "Siège social": "Domicilio social",
    "{0} rue Vivienne, {1} Paris, France": "{0} rue Vivienne, {1} París, Francia",
    "Immatriculation": "Inscripción",
    "RCS Paris {0}": "Registro Mercantil de París {0}",
    "SIREN : {0}": "SIREN: {0}",
    "SIRET (siège) : {0}": "SIRET (domicilio): {0}",
    "Code d'activité (APE/NAF)": "Código de actividad (APE/NAF)",
    "{0}Z — Programmation informatique": "{0}Z — Programación informática",
    "Taxe sur la valeur ajoutée": "Impuesto sobre el valor añadido",
    "TVA non applicable, article {0} B du CGI":
        "Sin IVA — exención de microempresa francesa, art. {0} B del código fiscal francés",
    "Président": "Presidente",
    "Directeur de la publication": "Director de la publicación",
    "Contact": "Contacto",
    "{0}. Hébergeur": "{0}. Alojamiento",
    "Le site est hébergé par :": "El sitio está alojado por:",
    "{0} Brannan Street, Suite {1}, San Francisco, CA {2}, États-Unis":
        "{0} Brannan Street, Suite {1}, San Francisco, CA {2}, Estados Unidos",
    "{0}. Propriété intellectuelle": "{0}. Propiedad intelectual",
    "L'ensemble des éléments composant le site — structure, textes, visuels, logo, marque Qeerah, code source et bases de données — est protégé par le droit de la propriété intellectuelle et demeure la propriété exclusive de DOPE VENTURES, sauf mention contraire. Toute reproduction, représentation ou exploitation, totale ou partielle, sans autorisation écrite préalable est interdite.":
        "Todos los elementos que componen el sitio —estructura, textos, imágenes, logotipo, marca Qeerah, código fuente y bases de datos— están protegidos por el derecho de propiedad intelectual y son propiedad exclusiva de DOPE VENTURES, salvo indicación en contrario. Queda prohibida toda reproducción, representación o explotación, total o parcial, sin autorización previa por escrito.",
    "Les contenus analysés par le service (vidéos, images, textes) restent la propriété de leurs auteurs respectifs. Qeerah n'en revendique aucun droit et n'en effectue aucune republication.":
        "Los contenidos analizados por el servicio (vídeos, imágenes, textos) siguen siendo propiedad de sus autores. Qeerah no reivindica ningún derecho sobre ellos ni los republica.",
    "{0}. Marques de tiers": "{0}. Marcas de terceros",
    "TikTok et TikTok Shop sont des marques déposées de leurs titulaires respectifs. Qeerah est un service indépendant, sans lien, partenariat ni affiliation avec ces sociétés, et n'est ni approuvé ni sponsorisé par elles.":
        "TikTok y TikTok Shop son marcas registradas de sus respectivos titulares. Qeerah es un servicio independiente, sin vínculo, colaboración ni afiliación con esas empresas, y no está aprobado ni patrocinado por ellas.",
    "{0}. Données personnelles": "{0}. Datos personales",
    "Le traitement des données personnelles est décrit dans notre":
        "El tratamiento de los datos personales se describe en nuestra",
    "politique de confidentialité": "política de privacidad",
    ". Conformément au Règlement (UE) {0}/{1} et à la loi Informatique et Libertés, tu disposes d'un droit d'accès, de rectification, d'effacement, de portabilité, de limitation et d'opposition, exerçable à l'adresse":
        ". Conforme al Reglamento (UE) {0}/{1} y a la ley francesa de protección de datos, tienes derecho de acceso, rectificación, supresión, portabilidad, limitación y oposición, que puedes ejercer en la dirección",
    "{0}. Cookies et traceurs": "{0}. Cookies y rastreadores",
    "Les traceurs déposés, leur finalité et leur durée de conservation sont détaillés dans la":
        "Los rastreadores utilizados, su finalidad y su plazo de conservación se detallan en la",
    ". Tu peux à tout moment modifier ton choix depuis le lien « Gérer les cookies » présent en pied de page.":
        ". Puedes cambiar tu elección en cualquier momento desde el enlace «Gestionar cookies» del pie de página.",
    "{0}. Conditions de vente": "{0}. Condiciones de venta",
    "Les modalités d'abonnement, de facturation et de résiliation figurent dans les":
        "Las condiciones de suscripción, facturación y cancelación figuran en las",
    "conditions générales de vente": "condiciones generales de venta",
    ". Les conditions d'utilisation du service sont décrites dans les":
        ". Las normas de uso del servicio se describen en las",
    "conditions générales d'utilisation": "condiciones generales de uso",
    "{0}. Médiation de la consommation": "{0}. Mediación de consumo",
    "Conformément à l'article L.{0}-{1} du Code de la consommation, le consommateur peut recourir gratuitement à un médiateur de la consommation en vue de la résolution amiable d'un litige. Le médiateur désigné par DOPE VENTURES est le":
        "Conforme al artículo L.{0}-{1} del Código de Consumo francés, el consumidor puede recurrir gratuitamente a un mediador de consumo para resolver un litigio de forma amistosa. El mediador designado por DOPE VENTURES es el",
    ", {0} rue Saint Jean, {1} Paris —": ", {0} rue Saint Jean, {1} París —",
    "{0}. Responsabilité": "{0}. Responsabilidad",
    "Les analyses produites par le service reposent sur des traitements automatisés et de l'intelligence artificielle. Elles constituent des estimations à visée indicative et ne garantissent aucun résultat commercial. DOPE VENTURES ne saurait être tenue responsable des décisions prises sur leur fondement.":
        "Los análisis que produce el servicio se basan en tratamientos automatizados e inteligencia artificial. Son estimaciones a título indicativo y no garantizan ningún resultado comercial. DOPE VENTURES no se hace responsable de las decisiones tomadas a partir de ellos.",
    "{0}. Droit applicable": "{0}. Ley aplicable",
    "Les présentes mentions légales sont soumises au droit français. En cas de litige et à défaut de résolution amiable, les tribunaux français sont compétents.":
        "Este aviso legal se rige por el derecho francés. En caso de litigio y a falta de acuerdo amistoso, los tribunales franceses son competentes.",
}

T_MENTIONS["it"] = {
    "Mentions légales — Qeerah": "Note legali — Qeerah",
    "Mentions légales de Qeerah, édité par DOPE VENTURES.":
        "Note legali di Qeerah, pubblicata da DOPE VENTURES.",
    "← Retour à l'accueil": "← Torna alla home",
    "Mentions légales": "Note legali",
    "Conformément à la loi n° {0}-{1} du {2} juin {3} pour la confiance dans l'économie numérique (LCEN).":
        "Ai sensi della legge francese n. {0}-{1} del {2} giugno {3} sulla fiducia nell'economia digitale (LCEN).",
    "{0}. Éditeur du site": "{0}. Editore del sito",
    "Dénomination sociale": "Denominazione sociale",
    "Forme juridique": "Forma giuridica",
    "SASU au capital de {0} €": "SASU (società per azioni semplificata con socio unico, diritto francese) con capitale di {0} €",
    "Siège social": "Sede legale",
    "{0} rue Vivienne, {1} Paris, France": "{0} rue Vivienne, {1} Parigi, Francia",
    "Immatriculation": "Iscrizione",
    "RCS Paris {0}": "Registro delle imprese di Parigi {0}",
    "SIREN : {0}": "SIREN: {0}",
    "SIRET (siège) : {0}": "SIRET (sede): {0}",
    "Code d'activité (APE/NAF)": "Codice attività (APE/NAF)",
    "{0}Z — Programmation informatique": "{0}Z — Programmazione informatica",
    "Taxe sur la valeur ajoutée": "Imposta sul valore aggiunto",
    "TVA non applicable, article {0} B du CGI":
        "Nessuna IVA applicata — esenzione per microimprese francesi, art. {0} B del codice fiscale francese",
    "Président": "Presidente",
    "Directeur de la publication": "Direttore della pubblicazione",
    "Contact": "Contatto",
    "{0}. Hébergeur": "{0}. Hosting",
    "Le site est hébergé par :": "Il sito è ospitato da:",
    "{0} Brannan Street, Suite {1}, San Francisco, CA {2}, États-Unis":
        "{0} Brannan Street, Suite {1}, San Francisco, CA {2}, Stati Uniti",
    "{0}. Propriété intellectuelle": "{0}. Proprietà intellettuale",
    "L'ensemble des éléments composant le site — structure, textes, visuels, logo, marque Qeerah, code source et bases de données — est protégé par le droit de la propriété intellectuelle et demeure la propriété exclusive de DOPE VENTURES, sauf mention contraire. Toute reproduction, représentation ou exploitation, totale ou partielle, sans autorisation écrite préalable est interdite.":
        "Tutti gli elementi che compongono il sito — struttura, testi, immagini, logo, marchio Qeerah, codice sorgente e banche dati — sono protetti dal diritto di proprietà intellettuale e restano di proprietà esclusiva di DOPE VENTURES, salvo diversa indicazione. È vietata ogni riproduzione, rappresentazione o utilizzo, totale o parziale, senza autorizzazione scritta preventiva.",
    "Les contenus analysés par le service (vidéos, images, textes) restent la propriété de leurs auteurs respectifs. Qeerah n'en revendique aucun droit et n'en effectue aucune republication.":
        "I contenuti analizzati dal servizio (video, immagini, testi) restano di proprietà dei rispettivi autori. Qeerah non ne rivendica alcun diritto e non li ripubblica.",
    "{0}. Marques de tiers": "{0}. Marchi di terzi",
    "TikTok et TikTok Shop sont des marques déposées de leurs titulaires respectifs. Qeerah est un service indépendant, sans lien, partenariat ni affiliation avec ces sociétés, et n'est ni approuvé ni sponsorisé par elles.":
        "TikTok e TikTok Shop sono marchi registrati dei rispettivi titolari. Qeerah è un servizio indipendente, senza legami, partnership o affiliazioni con quelle società, e non è né approvato né sponsorizzato da esse.",
    "{0}. Données personnelles": "{0}. Dati personali",
    "Le traitement des données personnelles est décrit dans notre":
        "Il trattamento dei dati personali è descritto nella nostra",
    "politique de confidentialité": "informativa sulla privacy",
    ". Conformément au Règlement (UE) {0}/{1} et à la loi Informatique et Libertés, tu disposes d'un droit d'accès, de rectification, d'effacement, de portabilité, de limitation et d'opposition, exerçable à l'adresse":
        ". Ai sensi del Regolamento (UE) {0}/{1} e della legge francese sulla protezione dei dati, hai diritto di accesso, rettifica, cancellazione, portabilità, limitazione e opposizione, esercitabili all'indirizzo",
    "{0}. Cookies et traceurs": "{0}. Cookie e tracciatori",
    "Les traceurs déposés, leur finalité et leur durée de conservation sont détaillés dans la":
        "I tracciatori utilizzati, la loro finalità e la durata di conservazione sono descritti nell'",
    ". Tu peux à tout moment modifier ton choix depuis le lien « Gérer les cookies » présent en pied de page.":
        ". Puoi modificare la tua scelta in qualsiasi momento dal link «Gestisci i cookie» in fondo alla pagina.",
    "{0}. Conditions de vente": "{0}. Condizioni di vendita",
    "Les modalités d'abonnement, de facturation et de résiliation figurent dans les":
        "Le modalità di abbonamento, fatturazione e disdetta sono indicate nelle",
    "conditions générales de vente": "condizioni generali di vendita",
    ". Les conditions d'utilisation du service sont décrites dans les":
        ". Le regole d'uso del servizio sono descritte nelle",
    "conditions générales d'utilisation": "condizioni generali d'uso",
    "{0}. Médiation de la consommation": "{0}. Mediazione dei consumatori",
    "Conformément à l'article L.{0}-{1} du Code de la consommation, le consommateur peut recourir gratuitement à un médiateur de la consommation en vue de la résolution amiable d'un litige. Le médiateur désigné par DOPE VENTURES est le":
        "Ai sensi dell'articolo L.{0}-{1} del Codice del consumo francese, il consumatore può rivolgersi gratuitamente a un mediatore per la risoluzione amichevole di una controversia. Il mediatore designato da DOPE VENTURES è il",
    ", {0} rue Saint Jean, {1} Paris —": ", {0} rue Saint Jean, {1} Parigi —",
    "{0}. Responsabilité": "{0}. Responsabilità",
    "Les analyses produites par le service reposent sur des traitements automatisés et de l'intelligence artificielle. Elles constituent des estimations à visée indicative et ne garantissent aucun résultat commercial. DOPE VENTURES ne saurait être tenue responsable des décisions prises sur leur fondement.":
        "Le analisi prodotte dal servizio si basano su trattamenti automatizzati e sull'intelligenza artificiale. Sono stime a titolo indicativo e non garantiscono alcun risultato commerciale. DOPE VENTURES non può essere ritenuta responsabile delle decisioni prese sulla loro base.",
    "{0}. Droit applicable": "{0}. Legge applicabile",
    "Les présentes mentions légales sont soumises au droit français. En cas de litige et à défaut de résolution amiable, les tribunaux français sont compétents.":
        "Le presenti note legali sono soggette al diritto francese. In caso di controversia e in mancanza di accordo amichevole, sono competenti i tribunali francesi.",
}

T_MENTIONS["de"] = {
    "Mentions légales — Qeerah": "Impressum — Qeerah",
    "Mentions légales de Qeerah, édité par DOPE VENTURES.":
        "Impressum von Qeerah, herausgegeben von DOPE VENTURES.",
    "← Retour à l'accueil": "← Zurück zur Startseite",
    "Mentions légales": "Impressum",
    "Conformément à la loi n° {0}-{1} du {2} juin {3} pour la confiance dans l'économie numérique (LCEN).":
        "Gemäß dem französischen Gesetz Nr. {0}-{1} vom {2}. Juni {3} über das Vertrauen in die digitale Wirtschaft (LCEN).",
    "{0}. Éditeur du site": "{0}. Herausgeber der Website",
    "Dénomination sociale": "Firmenname",
    "Forme juridique": "Rechtsform",
    "SASU au capital de {0} €": "SASU (vereinfachte Aktiengesellschaft französischen Rechts mit Alleingesellschafter), Stammkapital {0} €",
    "Siège social": "Sitz",
    "{0} rue Vivienne, {1} Paris, France": "{0} rue Vivienne, {1} Paris, Frankreich",
    "Immatriculation": "Registereintrag",
    "RCS Paris {0}": "Handelsregister Paris {0}",
    "SIREN : {0}": "SIREN: {0}",
    "SIRET (siège) : {0}": "SIRET (Sitz): {0}",
    "Code d'activité (APE/NAF)": "Tätigkeitsschlüssel (APE/NAF)",
    "{0}Z — Programmation informatique": "{0}Z — Softwareentwicklung",
    "Taxe sur la valeur ajoutée": "Umsatzsteuer",
    "TVA non applicable, article {0} B du CGI":
        "Keine Mehrwertsteuer — französische Kleinunternehmerregelung, Art. {0} B des französischen Steuergesetzbuchs",
    "Président": "Präsident",
    "Directeur de la publication": "Verantwortlich für den Inhalt",
    "Contact": "Kontakt",
    "{0}. Hébergeur": "{0}. Hoster",
    "Le site est hébergé par :": "Die Website wird gehostet von:",
    "{0} Brannan Street, Suite {1}, San Francisco, CA {2}, États-Unis":
        "{0} Brannan Street, Suite {1}, San Francisco, CA {2}, USA",
    "{0}. Propriété intellectuelle": "{0}. Geistiges Eigentum",
    "L'ensemble des éléments composant le site — structure, textes, visuels, logo, marque Qeerah, code source et bases de données — est protégé par le droit de la propriété intellectuelle et demeure la propriété exclusive de DOPE VENTURES, sauf mention contraire. Toute reproduction, représentation ou exploitation, totale ou partielle, sans autorisation écrite préalable est interdite.":
        "Sämtliche Bestandteile der Website — Aufbau, Texte, Bilder, Logo, die Marke Qeerah, Quellcode und Datenbanken — sind urheber- und markenrechtlich geschützt und bleiben, sofern nicht anders angegeben, ausschließliches Eigentum von DOPE VENTURES. Jede Vervielfältigung, Wiedergabe oder Verwertung, ganz oder teilweise, ohne vorherige schriftliche Zustimmung ist untersagt.",
    "Les contenus analysés par le service (vidéos, images, textes) restent la propriété de leurs auteurs respectifs. Qeerah n'en revendique aucun droit et n'en effectue aucune republication.":
        "Die vom Dienst analysierten Inhalte (Videos, Bilder, Texte) bleiben Eigentum ihrer jeweiligen Urheber. Qeerah erhebt darauf keine Ansprüche und veröffentlicht sie nicht erneut.",
    "{0}. Marques de tiers": "{0}. Marken Dritter",
    "TikTok et TikTok Shop sont des marques déposées de leurs titulaires respectifs. Qeerah est un service indépendant, sans lien, partenariat ni affiliation avec ces sociétés, et n'est ni approuvé ni sponsorisé par elles.":
        "TikTok und TikTok Shop sind eingetragene Marken ihrer jeweiligen Inhaber. Qeerah ist ein unabhängiger Dienst ohne Verbindung, Partnerschaft oder Zugehörigkeit zu diesen Unternehmen und wird von ihnen weder unterstützt noch gesponsert.",
    "{0}. Données personnelles": "{0}. Personenbezogene Daten",
    "Le traitement des données personnelles est décrit dans notre":
        "Wie personenbezogene Daten verarbeitet werden, steht in unserer",
    "politique de confidentialité": "Datenschutzerklärung",
    ". Conformément au Règlement (UE) {0}/{1} et à la loi Informatique et Libertés, tu disposes d'un droit d'accès, de rectification, d'effacement, de portabilité, de limitation et d'opposition, exerçable à l'adresse":
        ". Nach der Verordnung (EU) {0}/{1} und dem französischen Datenschutzgesetz hast du das Recht auf Auskunft, Berichtigung, Löschung, Übertragbarkeit, Einschränkung und Widerspruch. Wende dich dafür an",
    "{0}. Cookies et traceurs": "{0}. Cookies und Tracker",
    "Les traceurs déposés, leur finalité et leur durée de conservation sont détaillés dans la":
        "Welche Tracker gesetzt werden, wozu und wie lange sie gespeichert bleiben, steht in der",
    ". Tu peux à tout moment modifier ton choix depuis le lien « Gérer les cookies » présent en pied de page.":
        ". Du kannst deine Auswahl jederzeit über den Link „Cookies verwalten“ im Seitenfuß ändern.",
    "{0}. Conditions de vente": "{0}. Verkaufsbedingungen",
    "Les modalités d'abonnement, de facturation et de résiliation figurent dans les":
        "Die Bedingungen für Abo, Abrechnung und Kündigung stehen in den",
    "conditions générales de vente": "allgemeinen Verkaufsbedingungen",
    ". Les conditions d'utilisation du service sont décrites dans les":
        ". Die Regeln für die Nutzung des Dienstes stehen in den",
    "conditions générales d'utilisation": "allgemeinen Nutzungsbedingungen",
    "{0}. Médiation de la consommation": "{0}. Verbrauchermediation",
    "Conformément à l'article L.{0}-{1} du Code de la consommation, le consommateur peut recourir gratuitement à un médiateur de la consommation en vue de la résolution amiable d'un litige. Le médiateur désigné par DOPE VENTURES est le":
        "Nach Artikel L.{0}-{1} des französischen Verbrauchergesetzbuchs können Verbraucher kostenlos eine Verbrauchermediation zur gütlichen Beilegung eines Streits in Anspruch nehmen. Die von DOPE VENTURES benannte Stelle ist die",
    ", {0} rue Saint Jean, {1} Paris —": ", {0} rue Saint Jean, {1} Paris —",
    "{0}. Responsabilité": "{0}. Haftung",
    "Les analyses produites par le service reposent sur des traitements automatisés et de l'intelligence artificielle. Elles constituent des estimations à visée indicative et ne garantissent aucun résultat commercial. DOPE VENTURES ne saurait être tenue responsable des décisions prises sur leur fondement.":
        "Die Analysen des Dienstes beruhen auf automatisierter Verarbeitung und künstlicher Intelligenz. Sie sind Schätzungen mit Orientierungscharakter und sichern kein geschäftliches Ergebnis zu. DOPE VENTURES haftet nicht für Entscheidungen, die auf ihrer Grundlage getroffen werden.",
    "{0}. Droit applicable": "{0}. Anwendbares Recht",
    "Les présentes mentions légales sont soumises au droit français. En cas de litige et à défaut de résolution amiable, les tribunaux français sont compétents.":
        "Dieses Impressum unterliegt französischem Recht. Bei Streitigkeiten, die sich nicht gütlich beilegen lassen, sind die französischen Gerichte zuständig.",
}

T_MENTIONS["en-ie"] = dict(T_MENTIONS["en"])
T_MENTIONS["es-mx"] = dict(T_MENTIONS["es"])


# ═══════════════════════════════════════════════════════════════════════════
# /cgv — conditions générales de vente
# La page la plus dense du site, et celle où une nuance mal rendue coûterait le
# plus cher : d'où l'avertissement « le français fait foi » en tête de chaque
# variante. Les délais, quotas et montants restent hors des clefs (`{0}`) — un
# tarif qui change ne doit pas décrocher sept traductions.
# ═══════════════════════════════════════════════════════════════════════════
T_CGV: dict[str, dict[str, str]] = {}

T_CGV["en"] = {
    "Conditions générales de vente — Qeerah": "General terms of sale — Qeerah",
    "Conditions générales de vente de Qeerah (DOPE VENTURES).":
        "Qeerah's general terms of sale (DOPE VENTURES).",
    "← Retour à l'accueil": "← Back to home",
    "Conditions générales de vente": "General terms of sale",
    "Qeerah — édité par DOPE VENTURES · Dernière mise à jour : août {0}":
        "Qeerah — published by DOPE VENTURES · Last updated: August {0}",
    "{0}. Vendeur": "{0}. Seller",
    "Les présentes conditions générales de vente (CGV) régissent les abonnements et achats proposés sur":
        "These general terms of sale (GTS) govern the subscriptions and purchases offered on",
    ", édité par :": ", published by:",
    ", SASU au capital de {0} €": ", a French SASU with share capital of €{0}",
    "RCS Paris {0} — Siège : {1} rue Vivienne, {2} Paris, France":
        "Paris Trade and Companies Register {0} — Registered office: {1} rue Vivienne, {2} Paris, France",
    "Représentée par son Président, Aimeric Bourgon": "Represented by its President, Aimeric Bourgon",
    "Contact :": "Contact:",
    "{0}. Objet": "{0}. Purpose",
    "Qeerah est un service en ligne (SaaS) d'analyse de vidéos et de génération de contenu assistée par intelligence artificielle, à destination des créateurs. Les présentes CGV s'appliquent à tout abonnement payant et à tout achat de crédits.":
        "Qeerah is an online service (SaaS) for analysing videos and generating content with the help of artificial intelligence, aimed at creators. These GTS apply to every paid subscription and every purchase of credits.",
    "{0}. Offre et prix": "{0}. Plan and prices",
    "Qeerah propose une": "Qeerah offers a",
    "offre d'abonnement unique, « Qeerah Pro »": "single subscription plan, “Qeerah Pro”",
    ", disponible selon deux périodicités au choix :": ", available on two billing cycles:",
    "{0} € TTC par mois": "€{0} per month, tax included",
    ", facturé mensuellement ;": ", billed monthly;",
    "{0} € TTC par an": "€{0} per year, tax included",
    ", facturé annuellement, soit l'équivalent de deux mensualités offertes par rapport au tarif mensuel.":
        ", billed yearly — the equivalent of two months free compared with the monthly rate.",
    "Les deux périodicités donnent accès aux": "Both cycles give access to the",
    "mêmes fonctionnalités, sans restriction": "same features, with no restriction",
    ", et au même quota d'analyses défini à l'article {0}. Des":
        ", and to the same analysis quota set out in article {0}. Optional",
    "packs de crédits": "credit packs",
    ", destinés aux fonctionnalités de génération d'images par intelligence artificielle, peuvent être achetés séparément et facultativement ; ils ne constituent pas un abonnement.":
        ", for the AI image-generation features, can be bought separately; they are not a subscription.",
    "TVA non applicable, article {0} B du CGI":
        "No VAT charged — French small-business exemption, art. {0} B of the French tax code",
    ": les prix affichés sont nets de taxe, aucune TVA n'est facturée ni récupérable. Le prix affiché correspond donc au montant effectivement dû. Les prix peuvent évoluer ; le prix applicable est celui affiché au moment de la commande, et toute évolution tarifaire est sans effet sur les périodes déjà payées.":
        ": the prices shown carry no tax; no VAT is charged and none can be reclaimed. The price shown is therefore the amount actually due. Prices may change; the price that applies is the one displayed at the time of the order, and any change has no effect on periods already paid for.",
    "{0}. Essai gratuit": "{0}. Free trial",
    "La création d'un compte donne accès à un": "Creating an account gives access to a",
    "essai gratuit de sept ({0}) jours": "free trial of seven ({0}) days",
    "à compter de l'inscription, sans paiement ni communication de moyen de paiement. Cet essai donne accès à l'ensemble des fonctionnalités, dans la limite de":
        "from sign-up, with no payment and no payment details required. The trial gives access to every feature, up to a limit of",
    "dix ({0}) analyses de vidéos": "ten ({0}) video analyses",
    ". À l'expiration de l'essai, en l'absence d'abonnement, les analyses déjà réalisées restent consultables mais aucune nouvelle analyse ne peut être lancée. L'essai n'est pas renouvelable et ne se transforme pas automatiquement en abonnement payant.":
        ". When the trial ends without a subscription, analyses already produced remain available to read but no new analysis can be started. The trial cannot be renewed and never turns into a paid subscription by itself.",
    "{0}. Commande et paiement": "{0}. Ordering and payment",
    "La souscription s'effectue en ligne. Le paiement est traité de manière sécurisée par notre prestataire":
        "Subscriptions are taken out online. Payment is processed securely by our provider",
    "; Qeerah n'a jamais accès aux données complètes de votre moyen de paiement. La commande est confirmée par e-mail. Les abonnements sont facturés d'avance, pour la période choisie (mensuelle ou annuelle).":
        "; Qeerah never has access to your full payment details. The order is confirmed by email. Subscriptions are billed in advance for the chosen period (monthly or yearly).",
    "{0}. Quota d'analyses": "{0}. Analysis quota",
    "L'abonnement Qeerah Pro inclut": "The Qeerah Pro subscription includes",
    "cent ({0}) analyses de vidéos par mois": "one hundred ({0}) video analyses per month",
    ". Ce quota est décompté uniquement pour les analyses menées à leur terme : une analyse ayant échoué pour une raison technique n'est pas décomptée.":
        ". Only completed analyses count against this quota: an analysis that failed for a technical reason is not deducted.",
    "Le compteur est": "The counter is",
    "remis à zéro à chaque échéance mensuelle de facturation": "reset at every monthly billing date",
    ". Pour l'abonnement annuel, le quota reste de cent analyses par mois, remises à zéro à la date anniversaire mensuelle de la souscription — et non de cent analyses pour l'année entière. Les analyses non utilisées au cours d'un mois":
        ". On the yearly plan the quota stays at one hundred analyses per month, reset on the monthly anniversary of the subscription — not one hundred analyses for the whole year. Analyses left unused in a given month",
    "ne sont pas reportables": "do not carry over",
    "sur le mois suivant et ne donnent lieu à aucun remboursement ni compensation. Une fois le quota atteint, la possibilité de lancer de nouvelles analyses est suspendue jusqu'à la remise à zéro suivante, dont la date est indiquée dans votre espace client.":
        "to the following month and give rise to no refund or compensation. Once the quota is reached, starting new analyses is paused until the next reset, whose date is shown in your account.",
    "{0}. Durée, reconduction et résiliation": "{0}. Term, renewal and cancellation",
    "Les abonnements sont": "Subscriptions carry",
    "sans engagement de durée": "no minimum term",
    "et reconduits automatiquement à chaque échéance, pour une période identique à la précédente, sauf résiliation.":
        "and renew automatically at each due date for a period identical to the previous one, unless cancelled.",
    "Vous pouvez": "You can",
    "résilier à tout moment": "cancel at any time",
    "depuis votre espace client, sans motif ni frais. La résiliation met fin à la reconduction automatique : votre accès est maintenu jusqu'au terme de la période en cours déjà payée, après quoi il prend fin. Conformément au droit applicable, aucun remboursement au prorata n'est effectué pour une période entamée. Pour l'abonnement annuel, la résiliation en cours d'année met fin à la reconduction à la date anniversaire, l'accès étant maintenu jusqu'à cette date.":
        "from your account, with no reason to give and no fee. Cancelling ends the automatic renewal: your access continues until the end of the current period already paid for, and then stops. As the applicable law allows, no pro-rata refund is made for a period already started. On the yearly plan, cancelling during the year ends the renewal at the anniversary date, and access is kept until then.",
    "Nous pouvons résilier ou suspendre un abonnement en cas de défaut de paiement persistant après relances, ou de manquement grave aux présentes conditions.":
        "We may cancel or suspend a subscription in the event of persistent non-payment after reminders, or of a serious breach of these terms.",
    "{0}. Crédits": "{0}. Credits",
    "Les crédits achetés en packs ont une": "Credits bought in packs are",
    "validité d'un ({0}) mois": "valid for one ({0}) month",
    "à compter de l'achat, ne sont pas reportables au-delà de ce délai et ne sont pas remboursables une fois la commande exécutée. L'achat de crédits est facultatif et indépendant de l'abonnement.":
        "from the purchase, do not carry over beyond that period and are not refundable once the order has been fulfilled. Buying credits is optional and separate from the subscription.",
    "{0}. Droit de rétractation": "{0}. Right of withdrawal",
    "Conformément aux articles L.{0}-{1} et suivants du Code de la consommation, vous disposez d'un délai de {2} jours pour vous rétracter. Toutefois, pour la fourniture d'un":
        "Under articles L.{0}-{1} and following of the French Consumer Code, you have {2} days to withdraw. However, for the supply of",
    "contenu numérique et de services exécutés immédiatement": "digital content and services performed immediately",
    ", vous acceptez expressément, en souscrivant, que l'exécution commence avant la fin du délai de rétractation et":
        ", by subscribing you expressly agree that performance begins before the withdrawal period ends and that you",
    "renoncez à votre droit de rétractation": "waive your right of withdrawal",
    "pour la part du service déjà consommée (analyses, crédits utilisés), conformément à l'article L.{0}-{1}.":
        "for the part of the service already used (analyses, credits spent), in accordance with article L.{0}-{1}.",
    "{0}. Disponibilité et garanties": "{0}. Availability and warranties",
    "Le service est fourni « tel quel », dans la limite des moyens techniques disponibles. Les analyses générées par l'IA sont des estimations à visée indicative et ne constituent pas une garantie de résultats commerciaux. Nous nous efforçons d'assurer la continuité du service sans pouvoir la garantir de façon absolue (maintenance, dépendances tierces).":
        "The service is provided “as is”, within the limits of the technical means available. The analyses generated by the AI are estimates offered as guidance and are no guarantee of commercial results. We work to keep the service running without being able to guarantee it absolutely (maintenance, third-party dependencies).",
    "{0}. Responsabilité": "{0}. Liability",
    "La responsabilité de DOPE VENTURES ne saurait être engagée pour les décisions prises sur la base des analyses, ni pour les dommages indirects. En tout état de cause, la responsabilité est limitée au montant payé par le client au cours des {0} derniers mois.":
        "DOPE VENTURES cannot be held liable for decisions taken on the basis of the analyses, nor for indirect damages. In any event, liability is limited to the amount paid by the customer over the last {0} months.",
    "{0}. Données personnelles": "{0}. Personal data",
    "Le traitement des données est décrit dans notre": "How data is processed is described in our",
    "politique de confidentialité": "privacy policy",
    "{0}. Service client, réclamations et médiation": "{0}. Customer service, complaints and mediation",
    "Pour toute réclamation :": "For any complaint:",
    ". Conformément à l'article L.{0}-{1} du Code de la consommation, le consommateur peut recourir gratuitement à un médiateur de la consommation en vue de la résolution amiable d'un litige. Le médiateur désigné par DOPE VENTURES est le":
        ". Under article L.{0}-{1} of the French Consumer Code, consumers may use a consumer mediator free of charge to settle a dispute amicably. The mediator appointed by DOPE VENTURES is",
    "CM{0}C — Centre de Médiation de la Consommation de Conciliateurs de Justice":
        "CM{0}C — Centre de Médiation de la Consommation de Conciliateurs de Justice",
    ", {0} rue Saint Jean, {1} Paris —": ", {0} rue Saint Jean, {1} Paris —",
    "{0}. Droit applicable": "{0}. Governing law",
    "Les présentes CGV sont soumises au droit français. À défaut de résolution amiable, les tribunaux français sont compétents.":
        "These GTS are governed by French law. Failing an amicable settlement, the French courts have jurisdiction.",
}

T_CGV["de"] = {
    "Conditions générales de vente — Qeerah": "Allgemeine Verkaufsbedingungen — Qeerah",
    "Conditions générales de vente de Qeerah (DOPE VENTURES).":
        "Allgemeine Verkaufsbedingungen von Qeerah (DOPE VENTURES).",
    "← Retour à l'accueil": "← Zurück zur Startseite",
    "Conditions générales de vente": "Allgemeine Verkaufsbedingungen",
    "Qeerah — édité par DOPE VENTURES · Dernière mise à jour : août {0}":
        "Qeerah — herausgegeben von DOPE VENTURES · Zuletzt aktualisiert: August {0}",
    "{0}. Vendeur": "{0}. Verkäufer",
    "Les présentes conditions générales de vente (CGV) régissent les abonnements et achats proposés sur":
        "Diese allgemeinen Verkaufsbedingungen (AVB) gelten für die Abos und Käufe auf",
    ", édité par :": ", herausgegeben von:",
    ", SASU au capital de {0} €": ", SASU französischen Rechts mit einem Stammkapital von {0} €",
    "RCS Paris {0} — Siège : {1} rue Vivienne, {2} Paris, France":
        "Handelsregister Paris {0} — Sitz: {1} rue Vivienne, {2} Paris, Frankreich",
    "Représentée par son Président, Aimeric Bourgon": "Vertreten durch den Präsidenten Aimeric Bourgon",
    "Contact :": "Kontakt:",
    "{0}. Objet": "{0}. Gegenstand",
    "Qeerah est un service en ligne (SaaS) d'analyse de vidéos et de génération de contenu assistée par intelligence artificielle, à destination des créateurs. Les présentes CGV s'appliquent à tout abonnement payant et à tout achat de crédits.":
        "Qeerah ist ein Online-Dienst (SaaS) zur Analyse von Videos und zur KI-gestützten Erstellung von Inhalten, gerichtet an Creators. Diese AVB gelten für jedes kostenpflichtige Abo und jeden Kauf von Guthaben.",
    "{0}. Offre et prix": "{0}. Angebot und Preise",
    "Qeerah propose une": "Qeerah bietet ein",
    "offre d'abonnement unique, « Qeerah Pro »": "einziges Abo-Angebot, „Qeerah Pro“",
    ", disponible selon deux périodicités au choix :": ", wahlweise in zwei Abrechnungszyklen:",
    "{0} € TTC par mois": "{0} € pro Monat, inkl. Steuern",
    ", facturé mensuellement ;": ", monatlich abgerechnet;",
    "{0} € TTC par an": "{0} € pro Jahr, inkl. Steuern",
    ", facturé annuellement, soit l'équivalent de deux mensualités offertes par rapport au tarif mensuel.":
        ", jährlich abgerechnet — das entspricht zwei geschenkten Monatsbeiträgen gegenüber dem Monatspreis.",
    "Les deux périodicités donnent accès aux": "Beide Zyklen geben Zugang zu den",
    "mêmes fonctionnalités, sans restriction": "gleichen Funktionen, ohne Einschränkung",
    ", et au même quota d'analyses défini à l'article {0}. Des":
        ", und zum gleichen Analysekontingent aus Artikel {0}. Optionale",
    "packs de crédits": "Guthabenpakete",
    ", destinés aux fonctionnalités de génération d'images par intelligence artificielle, peuvent être achetés séparément et facultativement ; ils ne constituent pas un abonnement.":
        " für die KI-Bildgenerierung können separat dazugekauft werden; sie sind kein Abo.",
    "TVA non applicable, article {0} B du CGI":
        "Keine Mehrwertsteuer — französische Kleinunternehmerregelung, Art. {0} B des französischen Steuergesetzbuchs",
    ": les prix affichés sont nets de taxe, aucune TVA n'est facturée ni récupérable. Le prix affiché correspond donc au montant effectivement dû. Les prix peuvent évoluer ; le prix applicable est celui affiché au moment de la commande, et toute évolution tarifaire est sans effet sur les périodes déjà payées.":
        ": Die angezeigten Preise sind ohne Steuer; es wird keine Mehrwertsteuer berechnet und keine ist abziehbar. Der angezeigte Preis ist damit der tatsächlich fällige Betrag. Preise können sich ändern; es gilt der zum Zeitpunkt der Bestellung angezeigte Preis, und eine Preisänderung berührt bereits bezahlte Zeiträume nicht.",
    "{0}. Essai gratuit": "{0}. Kostenlose Testphase",
    "La création d'un compte donne accès à un": "Wer ein Konto anlegt, erhält eine",
    "essai gratuit de sept ({0}) jours": "kostenlose Testphase von sieben ({0}) Tagen",
    "à compter de l'inscription, sans paiement ni communication de moyen de paiement. Cet essai donne accès à l'ensemble des fonctionnalités, dans la limite de":
        "ab der Anmeldung, ohne Zahlung und ohne Angabe von Zahlungsdaten. Die Testphase gibt Zugang zu allen Funktionen, begrenzt auf",
    "dix ({0}) analyses de vidéos": "zehn ({0}) Videoanalysen",
    ". À l'expiration de l'essai, en l'absence d'abonnement, les analyses déjà réalisées restent consultables mais aucune nouvelle analyse ne peut être lancée. L'essai n'est pas renouvelable et ne se transforme pas automatiquement en abonnement payant.":
        ". Läuft die Testphase ohne Abo aus, bleiben bereits erstellte Analysen lesbar, neue lassen sich aber nicht starten. Die Testphase ist nicht verlängerbar und wird nie von selbst zu einem kostenpflichtigen Abo.",
    "{0}. Commande et paiement": "{0}. Bestellung und Zahlung",
    "La souscription s'effectue en ligne. Le paiement est traité de manière sécurisée par notre prestataire":
        "Der Abschluss erfolgt online. Die Zahlung wird sicher abgewickelt von unserem Dienstleister",
    "; Qeerah n'a jamais accès aux données complètes de votre moyen de paiement. La commande est confirmée par e-mail. Les abonnements sont facturés d'avance, pour la période choisie (mensuelle ou annuelle).":
        "; Qeerah erhält nie deine vollständigen Zahlungsdaten. Die Bestellung wird per E-Mail bestätigt. Abos werden im Voraus für den gewählten Zeitraum abgerechnet (monatlich oder jährlich).",
    "{0}. Quota d'analyses": "{0}. Analysekontingent",
    "L'abonnement Qeerah Pro inclut": "Das Abo Qeerah Pro enthält",
    "cent ({0}) analyses de vidéos par mois": "einhundert ({0}) Videoanalysen pro Monat",
    ". Ce quota est décompté uniquement pour les analyses menées à leur terme : une analyse ayant échoué pour une raison technique n'est pas décomptée.":
        ". Angerechnet werden nur abgeschlossene Analysen: Eine aus technischen Gründen fehlgeschlagene Analyse wird nicht abgezogen.",
    "Le compteur est": "Der Zähler wird",
    "remis à zéro à chaque échéance mensuelle de facturation": "zu jedem monatlichen Abrechnungstermin zurückgesetzt",
    ". Pour l'abonnement annuel, le quota reste de cent analyses par mois, remises à zéro à la date anniversaire mensuelle de la souscription — et non de cent analyses pour l'année entière. Les analyses non utilisées au cours d'un mois":
        ". Beim Jahresabo bleibt das Kontingent bei einhundert Analysen pro Monat, zurückgesetzt am monatlichen Jahrestag des Abschlusses — nicht einhundert Analysen für das ganze Jahr. In einem Monat nicht genutzte Analysen",
    "ne sont pas reportables": "sind nicht übertragbar",
    "sur le mois suivant et ne donnent lieu à aucun remboursement ni compensation. Une fois le quota atteint, la possibilité de lancer de nouvelles analyses est suspendue jusqu'à la remise à zéro suivante, dont la date est indiquée dans votre espace client.":
        "auf den Folgemonat und begründen weder Erstattung noch Ausgleich. Ist das Kontingent erreicht, pausiert das Starten neuer Analysen bis zum nächsten Zurücksetzen; das Datum steht in deinem Kundenbereich.",
    "{0}. Durée, reconduction et résiliation": "{0}. Laufzeit, Verlängerung und Kündigung",
    "Les abonnements sont": "Die Abos haben",
    "sans engagement de durée": "keine Mindestlaufzeit",
    "et reconduits automatiquement à chaque échéance, pour une période identique à la précédente, sauf résiliation.":
        "und verlängern sich zu jedem Termin automatisch um einen gleich langen Zeitraum, sofern nicht gekündigt wird.",
    "Vous pouvez": "Du kannst",
    "résilier à tout moment": "jederzeit kündigen",
    "depuis votre espace client, sans motif ni frais. La résiliation met fin à la reconduction automatique : votre accès est maintenu jusqu'au terme de la période en cours déjà payée, après quoi il prend fin. Conformément au droit applicable, aucun remboursement au prorata n'est effectué pour une période entamée. Pour l'abonnement annuel, la résiliation en cours d'année met fin à la reconduction à la date anniversaire, l'accès étant maintenu jusqu'à cette date.":
        "im Kundenbereich, ohne Angabe von Gründen und ohne Gebühr. Die Kündigung beendet die automatische Verlängerung: Der Zugang bleibt bis zum Ende des bereits bezahlten laufenden Zeitraums bestehen und endet dann. Nach geltendem Recht wird für einen angebrochenen Zeitraum nicht anteilig erstattet. Beim Jahresabo beendet eine Kündigung im laufenden Jahr die Verlängerung zum Jahrestag; bis dahin bleibt der Zugang bestehen.",
    "Nous pouvons résilier ou suspendre un abonnement en cas de défaut de paiement persistant après relances, ou de manquement grave aux présentes conditions.":
        "Wir können ein Abo kündigen oder aussetzen, wenn Zahlungen trotz Mahnungen dauerhaft ausbleiben oder gegen diese Bedingungen schwer verstoßen wird.",
    "{0}. Crédits": "{0}. Guthaben",
    "Les crédits achetés en packs ont une": "In Paketen gekauftes Guthaben hat eine",
    "validité d'un ({0}) mois": "Gültigkeit von einem ({0}) Monat",
    "à compter de l'achat, ne sont pas reportables au-delà de ce délai et ne sont pas remboursables une fois la commande exécutée. L'achat de crédits est facultatif et indépendant de l'abonnement.":
        "ab Kauf, ist darüber hinaus nicht übertragbar und nach Ausführung der Bestellung nicht erstattungsfähig. Der Kauf von Guthaben ist freiwillig und unabhängig vom Abo.",
    "{0}. Droit de rétractation": "{0}. Widerrufsrecht",
    "Conformément aux articles L.{0}-{1} et suivants du Code de la consommation, vous disposez d'un délai de {2} jours pour vous rétracter. Toutefois, pour la fourniture d'un":
        "Nach den Artikeln L.{0}-{1} ff. des französischen Verbrauchergesetzbuchs hast du {2} Tage Widerrufsrecht. Für die Bereitstellung von",
    "contenu numérique et de services exécutés immédiatement": "digitalen Inhalten und sofort erbrachten Leistungen",
    ", vous acceptez expressément, en souscrivant, que l'exécution commence avant la fin du délai de rétractation et":
        " erklärst du dich mit dem Abschluss jedoch ausdrücklich damit einverstanden, dass die Ausführung vor Ablauf der Widerrufsfrist beginnt, und",
    "renoncez à votre droit de rétractation": "verzichtest auf dein Widerrufsrecht",
    "pour la part du service déjà consommée (analyses, crédits utilisés), conformément à l'article L.{0}-{1}.":
        "für den bereits genutzten Teil der Leistung (Analysen, verbrauchtes Guthaben), gemäß Artikel L.{0}-{1}.",
    "{0}. Disponibilité et garanties": "{0}. Verfügbarkeit und Gewährleistung",
    "Le service est fourni « tel quel », dans la limite des moyens techniques disponibles. Les analyses générées par l'IA sont des estimations à visée indicative et ne constituent pas une garantie de résultats commerciaux. Nous nous efforçons d'assurer la continuité du service sans pouvoir la garantir de façon absolue (maintenance, dépendances tierces).":
        "Der Dienst wird „wie besehen“ im Rahmen der verfügbaren technischen Mittel bereitgestellt. Die von der KI erzeugten Analysen sind Schätzungen mit Orientierungscharakter und keine Zusage geschäftlicher Ergebnisse. Wir bemühen uns um durchgehenden Betrieb, können ihn aber nicht absolut garantieren (Wartung, Abhängigkeiten von Dritten).",
    "{0}. Responsabilité": "{0}. Haftung",
    "La responsabilité de DOPE VENTURES ne saurait être engagée pour les décisions prises sur la base des analyses, ni pour les dommages indirects. En tout état de cause, la responsabilité est limitée au montant payé par le client au cours des {0} derniers mois.":
        "DOPE VENTURES haftet weder für Entscheidungen, die auf Grundlage der Analysen getroffen werden, noch für mittelbare Schäden. In jedem Fall ist die Haftung auf den Betrag begrenzt, den der Kunde in den letzten {0} Monaten gezahlt hat.",
    "{0}. Données personnelles": "{0}. Personenbezogene Daten",
    "Le traitement des données est décrit dans notre": "Die Verarbeitung der Daten ist beschrieben in unserer",
    "politique de confidentialité": "Datenschutzerklärung",
    "{0}. Service client, réclamations et médiation": "{0}. Kundendienst, Beschwerden und Mediation",
    "Pour toute réclamation :": "Für Beschwerden:",
    ". Conformément à l'article L.{0}-{1} du Code de la consommation, le consommateur peut recourir gratuitement à un médiateur de la consommation en vue de la résolution amiable d'un litige. Le médiateur désigné par DOPE VENTURES est le":
        ". Nach Artikel L.{0}-{1} des französischen Verbrauchergesetzbuchs können Verbraucher kostenlos eine Verbrauchermediation zur gütlichen Beilegung eines Streits in Anspruch nehmen. Die von DOPE VENTURES benannte Stelle ist die",
    "CM{0}C — Centre de Médiation de la Consommation de Conciliateurs de Justice":
        "CM{0}C — Centre de Médiation de la Consommation de Conciliateurs de Justice",
    ", {0} rue Saint Jean, {1} Paris —": ", {0} rue Saint Jean, {1} Paris —",
    "{0}. Droit applicable": "{0}. Anwendbares Recht",
    "Les présentes CGV sont soumises au droit français. À défaut de résolution amiable, les tribunaux français sont compétents.":
        "Diese AVB unterliegen französischem Recht. Kommt keine gütliche Einigung zustande, sind die französischen Gerichte zuständig.",
}

T_CGV["es"] = {
    "Conditions générales de vente — Qeerah": "Condiciones generales de venta — Qeerah",
    "Conditions générales de vente de Qeerah (DOPE VENTURES).":
        "Condiciones generales de venta de Qeerah (DOPE VENTURES).",
    "← Retour à l'accueil": "← Volver al inicio",
    "Conditions générales de vente": "Condiciones generales de venta",
    "Qeerah — édité par DOPE VENTURES · Dernière mise à jour : août {0}":
        "Qeerah — editado por DOPE VENTURES · Última actualización: agosto de {0}",
    "{0}. Vendeur": "{0}. Vendedor",
    "Les présentes conditions générales de vente (CGV) régissent les abonnements et achats proposés sur":
        "Estas condiciones generales de venta (CGV) rigen las suscripciones y compras ofrecidas en",
    ", édité par :": ", editado por:",
    ", SASU au capital de {0} €": ", SASU de derecho francés con un capital de {0} €",
    "RCS Paris {0} — Siège : {1} rue Vivienne, {2} Paris, France":
        "Registro Mercantil de París {0} — Domicilio: {1} rue Vivienne, {2} París, Francia",
    "Représentée par son Président, Aimeric Bourgon": "Representada por su Presidente, Aimeric Bourgon",
    "Contact :": "Contacto:",
    "{0}. Objet": "{0}. Objeto",
    "Qeerah est un service en ligne (SaaS) d'analyse de vidéos et de génération de contenu assistée par intelligence artificielle, à destination des créateurs. Les présentes CGV s'appliquent à tout abonnement payant et à tout achat de crédits.":
        "Qeerah es un servicio en línea (SaaS) de análisis de vídeos y de generación de contenido asistida por inteligencia artificial, dirigido a creadores. Estas CGV se aplican a toda suscripción de pago y a toda compra de créditos.",
    "{0}. Offre et prix": "{0}. Oferta y precios",
    "Qeerah propose une": "Qeerah ofrece una",
    "offre d'abonnement unique, « Qeerah Pro »": "única suscripción, «Qeerah Pro»",
    ", disponible selon deux périodicités au choix :": ", disponible con dos periodicidades a elegir:",
    "{0} € TTC par mois": "{0} € al mes, impuestos incluidos",
    ", facturé mensuellement ;": ", facturado mensualmente;",
    "{0} € TTC par an": "{0} € al año, impuestos incluidos",
    ", facturé annuellement, soit l'équivalent de deux mensualités offertes par rapport au tarif mensuel.":
        ", facturado anualmente, el equivalente a dos mensualidades gratis frente a la tarifa mensual.",
    "Les deux périodicités donnent accès aux": "Ambas periodicidades dan acceso a las",
    "mêmes fonctionnalités, sans restriction": "mismas funciones, sin restricción",
    ", et au même quota d'analyses défini à l'article {0}. Des":
        ", y a la misma cuota de análisis definida en el artículo {0}. Se pueden comprar aparte, de forma opcional,",
    "packs de crédits": "packs de créditos",
    ", destinés aux fonctionnalités de génération d'images par intelligence artificielle, peuvent être achetés séparément et facultativement ; ils ne constituent pas un abonnement.":
        " destinados a las funciones de generación de imágenes con inteligencia artificial; no constituyen una suscripción.",
    "TVA non applicable, article {0} B du CGI":
        "Sin IVA — exención de microempresa francesa, art. {0} B del código fiscal francés",
    ": les prix affichés sont nets de taxe, aucune TVA n'est facturée ni récupérable. Le prix affiché correspond donc au montant effectivement dû. Les prix peuvent évoluer ; le prix applicable est celui affiché au moment de la commande, et toute évolution tarifaire est sans effet sur les périodes déjà payées.":
        ": los precios mostrados son sin impuestos, no se factura IVA ni es recuperable. El precio mostrado es, por tanto, el importe realmente debido. Los precios pueden cambiar; el precio aplicable es el mostrado en el momento del pedido, y ningún cambio de tarifa afecta a los periodos ya pagados.",
    "{0}. Essai gratuit": "{0}. Prueba gratuita",
    "La création d'un compte donne accès à un": "Crear una cuenta da acceso a una",
    "essai gratuit de sept ({0}) jours": "prueba gratuita de siete ({0}) días",
    "à compter de l'inscription, sans paiement ni communication de moyen de paiement. Cet essai donne accès à l'ensemble des fonctionnalités, dans la limite de":
        "desde el registro, sin pago y sin facilitar ningún medio de pago. La prueba da acceso a todas las funciones, con un límite de",
    "dix ({0}) analyses de vidéos": "diez ({0}) análisis de vídeo",
    ". À l'expiration de l'essai, en l'absence d'abonnement, les analyses déjà réalisées restent consultables mais aucune nouvelle analyse ne peut être lancée. L'essai n'est pas renouvelable et ne se transforme pas automatiquement en abonnement payant.":
        ". Al terminar la prueba sin suscripción, los análisis ya realizados siguen consultables pero no se puede lanzar ninguno nuevo. La prueba no es renovable y nunca se convierte por sí sola en una suscripción de pago.",
    "{0}. Commande et paiement": "{0}. Pedido y pago",
    "La souscription s'effectue en ligne. Le paiement est traité de manière sécurisée par notre prestataire":
        "La suscripción se realiza en línea. El pago lo procesa de forma segura nuestro proveedor",
    "; Qeerah n'a jamais accès aux données complètes de votre moyen de paiement. La commande est confirmée par e-mail. Les abonnements sont facturés d'avance, pour la période choisie (mensuelle ou annuelle).":
        "; Qeerah nunca accede a los datos completos de tu medio de pago. El pedido se confirma por correo. Las suscripciones se facturan por adelantado, para el periodo elegido (mensual o anual).",
    "{0}. Quota d'analyses": "{0}. Cuota de análisis",
    "L'abonnement Qeerah Pro inclut": "La suscripción Qeerah Pro incluye",
    "cent ({0}) analyses de vidéos par mois": "cien ({0}) análisis de vídeo al mes",
    ". Ce quota est décompté uniquement pour les analyses menées à leur terme : une analyse ayant échoué pour une raison technique n'est pas décomptée.":
        ". Solo se descuentan los análisis completados: un análisis que ha fallado por un motivo técnico no se descuenta.",
    "Le compteur est": "El contador se",
    "remis à zéro à chaque échéance mensuelle de facturation": "pone a cero en cada vencimiento mensual de facturación",
    ". Pour l'abonnement annuel, le quota reste de cent analyses par mois, remises à zéro à la date anniversaire mensuelle de la souscription — et non de cent analyses pour l'année entière. Les analyses non utilisées au cours d'un mois":
        ". En la suscripción anual la cuota sigue siendo de cien análisis al mes, puestos a cero en el aniversario mensual de la suscripción, y no de cien análisis para todo el año. Los análisis no usados en un mes",
    "ne sont pas reportables": "no se acumulan",
    "sur le mois suivant et ne donnent lieu à aucun remboursement ni compensation. Une fois le quota atteint, la possibilité de lancer de nouvelles analyses est suspendue jusqu'à la remise à zéro suivante, dont la date est indiquée dans votre espace client.":
        "al mes siguiente y no dan lugar a reembolso ni compensación. Alcanzada la cuota, lanzar nuevos análisis queda suspendido hasta la siguiente puesta a cero, cuya fecha aparece en tu cuenta.",
    "{0}. Durée, reconduction et résiliation": "{0}. Duración, renovación y cancelación",
    "Les abonnements sont": "Las suscripciones son",
    "sans engagement de durée": "sin permanencia",
    "et reconduits automatiquement à chaque échéance, pour une période identique à la précédente, sauf résiliation.":
        "y se renuevan automáticamente en cada vencimiento, por un periodo idéntico al anterior, salvo cancelación.",
    "Vous pouvez": "Puedes",
    "résilier à tout moment": "cancelar cuando quieras",
    "depuis votre espace client, sans motif ni frais. La résiliation met fin à la reconduction automatique : votre accès est maintenu jusqu'au terme de la période en cours déjà payée, après quoi il prend fin. Conformément au droit applicable, aucun remboursement au prorata n'est effectué pour une période entamée. Pour l'abonnement annuel, la résiliation en cours d'année met fin à la reconduction à la date anniversaire, l'accès étant maintenu jusqu'à cette date.":
        "desde tu cuenta, sin motivo ni gastos. La cancelación pone fin a la renovación automática: tu acceso se mantiene hasta el final del periodo en curso ya pagado y termina después. Conforme al derecho aplicable, no se reembolsa la parte proporcional de un periodo empezado. En la suscripción anual, cancelar durante el año pone fin a la renovación en la fecha de aniversario, y el acceso se mantiene hasta entonces.",
    "Nous pouvons résilier ou suspendre un abonnement en cas de défaut de paiement persistant après relances, ou de manquement grave aux présentes conditions.":
        "Podemos cancelar o suspender una suscripción en caso de impago persistente tras los avisos, o de incumplimiento grave de estas condiciones.",
    "{0}. Crédits": "{0}. Créditos",
    "Les crédits achetés en packs ont une": "Los créditos comprados en packs tienen una",
    "validité d'un ({0}) mois": "validez de un ({0}) mes",
    "à compter de l'achat, ne sont pas reportables au-delà de ce délai et ne sont pas remboursables une fois la commande exécutée. L'achat de crédits est facultatif et indépendant de l'abonnement.":
        "desde la compra, no se acumulan más allá de ese plazo y no son reembolsables una vez ejecutado el pedido. Comprar créditos es opcional e independiente de la suscripción.",
    "{0}. Droit de rétractation": "{0}. Derecho de desistimiento",
    "Conformément aux articles L.{0}-{1} et suivants du Code de la consommation, vous disposez d'un délai de {2} jours pour vous rétracter. Toutefois, pour la fourniture d'un":
        "Conforme a los artículos L.{0}-{1} y siguientes del Código de Consumo francés, dispones de {2} días para desistir. No obstante, para el suministro de",
    "contenu numérique et de services exécutés immédiatement": "contenido digital y de servicios ejecutados de inmediato",
    ", vous acceptez expressément, en souscrivant, que l'exécution commence avant la fin du délai de rétractation et":
        ", al suscribirte aceptas expresamente que la ejecución empiece antes de que acabe el plazo de desistimiento y",
    "renoncez à votre droit de rétractation": "renuncias a tu derecho de desistimiento",
    "pour la part du service déjà consommée (analyses, crédits utilisés), conformément à l'article L.{0}-{1}.":
        "por la parte del servicio ya consumida (análisis, créditos usados), conforme al artículo L.{0}-{1}.",
    "{0}. Disponibilité et garanties": "{0}. Disponibilidad y garantías",
    "Le service est fourni « tel quel », dans la limite des moyens techniques disponibles. Les analyses générées par l'IA sont des estimations à visée indicative et ne constituent pas une garantie de résultats commerciaux. Nous nous efforçons d'assurer la continuité du service sans pouvoir la garantir de façon absolue (maintenance, dépendances tierces).":
        "El servicio se presta «tal cual», dentro de los medios técnicos disponibles. Los análisis generados por la IA son estimaciones a título indicativo y no garantizan resultados comerciales. Nos esforzamos por asegurar la continuidad del servicio sin poder garantizarla de forma absoluta (mantenimiento, dependencias de terceros).",
    "{0}. Responsabilité": "{0}. Responsabilidad",
    "La responsabilité de DOPE VENTURES ne saurait être engagée pour les décisions prises sur la base des analyses, ni pour les dommages indirects. En tout état de cause, la responsabilité est limitée au montant payé par le client au cours des {0} derniers mois.":
        "DOPE VENTURES no responde de las decisiones tomadas a partir de los análisis ni de los daños indirectos. En cualquier caso, la responsabilidad se limita al importe pagado por el cliente en los últimos {0} meses.",
    "{0}. Données personnelles": "{0}. Datos personales",
    "Le traitement des données est décrit dans notre": "El tratamiento de los datos se describe en nuestra",
    "politique de confidentialité": "política de privacidad",
    "{0}. Service client, réclamations et médiation": "{0}. Atención al cliente, reclamaciones y mediación",
    "Pour toute réclamation :": "Para cualquier reclamación:",
    ". Conformément à l'article L.{0}-{1} du Code de la consommation, le consommateur peut recourir gratuitement à un médiateur de la consommation en vue de la résolution amiable d'un litige. Le médiateur désigné par DOPE VENTURES est le":
        ". Conforme al artículo L.{0}-{1} del Código de Consumo francés, el consumidor puede recurrir gratuitamente a un mediador de consumo para resolver un litigio de forma amistosa. El mediador designado por DOPE VENTURES es el",
    "CM{0}C — Centre de Médiation de la Consommation de Conciliateurs de Justice":
        "CM{0}C — Centre de Médiation de la Consommation de Conciliateurs de Justice",
    ", {0} rue Saint Jean, {1} Paris —": ", {0} rue Saint Jean, {1} París —",
    "{0}. Droit applicable": "{0}. Ley aplicable",
    "Les présentes CGV sont soumises au droit français. À défaut de résolution amiable, les tribunaux français sont compétents.":
        "Estas CGV se rigen por el derecho francés. A falta de acuerdo amistoso, los tribunales franceses son competentes.",
}

T_CGV["it"] = {
    "Conditions générales de vente — Qeerah": "Condizioni generali di vendita — Qeerah",
    "Conditions générales de vente de Qeerah (DOPE VENTURES).":
        "Condizioni generali di vendita di Qeerah (DOPE VENTURES).",
    "← Retour à l'accueil": "← Torna alla home",
    "Conditions générales de vente": "Condizioni generali di vendita",
    "Qeerah — édité par DOPE VENTURES · Dernière mise à jour : août {0}":
        "Qeerah — pubblicato da DOPE VENTURES · Ultimo aggiornamento: agosto {0}",
    "{0}. Vendeur": "{0}. Venditore",
    "Les présentes conditions générales de vente (CGV) régissent les abonnements et achats proposés sur":
        "Le presenti condizioni generali di vendita (CGV) regolano gli abbonamenti e gli acquisti offerti su",
    ", édité par :": ", pubblicato da:",
    ", SASU au capital de {0} €": ", SASU di diritto francese con capitale di {0} €",
    "RCS Paris {0} — Siège : {1} rue Vivienne, {2} Paris, France":
        "Registro delle imprese di Parigi {0} — Sede: {1} rue Vivienne, {2} Parigi, Francia",
    "Représentée par son Président, Aimeric Bourgon": "Rappresentata dal suo Presidente, Aimeric Bourgon",
    "Contact :": "Contatto:",
    "{0}. Objet": "{0}. Oggetto",
    "Qeerah est un service en ligne (SaaS) d'analyse de vidéos et de génération de contenu assistée par intelligence artificielle, à destination des créateurs. Les présentes CGV s'appliquent à tout abonnement payant et à tout achat de crédits.":
        "Qeerah è un servizio online (SaaS) di analisi video e di creazione di contenuti assistita dall'intelligenza artificiale, rivolto ai creator. Le presenti CGV si applicano a ogni abbonamento a pagamento e a ogni acquisto di crediti.",
    "{0}. Offre et prix": "{0}. Offerta e prezzi",
    "Qeerah propose une": "Qeerah propone un",
    "offre d'abonnement unique, « Qeerah Pro »": "unico abbonamento, «Qeerah Pro»",
    ", disponible selon deux périodicités au choix :": ", disponibile con due periodicità a scelta:",
    "{0} € TTC par mois": "{0} € al mese, tasse incluse",
    ", facturé mensuellement ;": ", fatturato mensilmente;",
    "{0} € TTC par an": "{0} € all'anno, tasse incluse",
    ", facturé annuellement, soit l'équivalent de deux mensualités offertes par rapport au tarif mensuel.":
        ", fatturato annualmente, l'equivalente di due mensilità in omaggio rispetto alla tariffa mensile.",
    "Les deux périodicités donnent accès aux": "Entrambe le periodicità danno accesso alle",
    "mêmes fonctionnalités, sans restriction": "stesse funzioni, senza restrizioni",
    ", et au même quota d'analyses défini à l'article {0}. Des":
        ", e alla stessa quota di analisi definita all'articolo {0}. Si possono acquistare a parte, in modo facoltativo,",
    "packs de crédits": "pacchetti di crediti",
    ", destinés aux fonctionnalités de génération d'images par intelligence artificielle, peuvent être achetés séparément et facultativement ; ils ne constituent pas un abonnement.":
        " destinati alle funzioni di generazione di immagini con l'intelligenza artificiale; non costituiscono un abbonamento.",
    "TVA non applicable, article {0} B du CGI":
        "Nessuna IVA applicata — esenzione per microimprese francesi, art. {0} B del codice fiscale francese",
    ": les prix affichés sont nets de taxe, aucune TVA n'est facturée ni récupérable. Le prix affiché correspond donc au montant effectivement dû. Les prix peuvent évoluer ; le prix applicable est celui affiché au moment de la commande, et toute évolution tarifaire est sans effet sur les périodes déjà payées.":
        ": i prezzi indicati sono al netto di imposte, nessuna IVA viene fatturata né è recuperabile. Il prezzo indicato corrisponde quindi all'importo effettivamente dovuto. I prezzi possono cambiare; si applica quello indicato al momento dell'ordine, e ogni variazione non incide sui periodi già pagati.",
    "{0}. Essai gratuit": "{0}. Prova gratuita",
    "La création d'un compte donne accès à un": "Creando un account si ottiene una",
    "essai gratuit de sept ({0}) jours": "prova gratuita di sette ({0}) giorni",
    "à compter de l'inscription, sans paiement ni communication de moyen de paiement. Cet essai donne accès à l'ensemble des fonctionnalités, dans la limite de":
        "dall'iscrizione, senza pagamento né comunicazione di un metodo di pagamento. La prova dà accesso a tutte le funzioni, entro il limite di",
    "dix ({0}) analyses de vidéos": "dieci ({0}) analisi di video",
    ". À l'expiration de l'essai, en l'absence d'abonnement, les analyses déjà réalisées restent consultables mais aucune nouvelle analyse ne peut être lancée. L'essai n'est pas renouvelable et ne se transforme pas automatiquement en abonnement payant.":
        ". Alla scadenza della prova, senza abbonamento, le analisi già svolte restano consultabili ma non se ne può avviare di nuove. La prova non è rinnovabile e non si trasforma mai da sola in un abbonamento a pagamento.",
    "{0}. Commande et paiement": "{0}. Ordine e pagamento",
    "La souscription s'effectue en ligne. Le paiement est traité de manière sécurisée par notre prestataire":
        "La sottoscrizione avviene online. Il pagamento è gestito in modo sicuro dal nostro fornitore",
    "; Qeerah n'a jamais accès aux données complètes de votre moyen de paiement. La commande est confirmée par e-mail. Les abonnements sont facturés d'avance, pour la période choisie (mensuelle ou annuelle).":
        "; Qeerah non ha mai accesso ai dati completi del tuo metodo di pagamento. L'ordine è confermato via email. Gli abbonamenti sono fatturati in anticipo, per il periodo scelto (mensile o annuale).",
    "{0}. Quota d'analyses": "{0}. Quota di analisi",
    "L'abonnement Qeerah Pro inclut": "L'abbonamento Qeerah Pro include",
    "cent ({0}) analyses de vidéos par mois": "cento ({0}) analisi di video al mese",
    ". Ce quota est décompté uniquement pour les analyses menées à leur terme : une analyse ayant échoué pour une raison technique n'est pas décomptée.":
        ". Vengono conteggiate solo le analisi portate a termine: un'analisi fallita per un motivo tecnico non viene scalata.",
    "Le compteur est": "Il contatore viene",
    "remis à zéro à chaque échéance mensuelle de facturation": "azzerato a ogni scadenza mensile di fatturazione",
    ". Pour l'abonnement annuel, le quota reste de cent analyses par mois, remises à zéro à la date anniversaire mensuelle de la souscription — et non de cent analyses pour l'année entière. Les analyses non utilisées au cours d'un mois":
        ". Con l'abbonamento annuale la quota resta di cento analisi al mese, azzerate alla data mensile di anniversario della sottoscrizione — non cento analisi per tutto l'anno. Le analisi non usate in un mese",
    "ne sont pas reportables": "non sono riportabili",
    "sur le mois suivant et ne donnent lieu à aucun remboursement ni compensation. Une fois le quota atteint, la possibilité de lancer de nouvelles analyses est suspendue jusqu'à la remise à zéro suivante, dont la date est indiquée dans votre espace client.":
        "al mese successivo e non danno diritto ad alcun rimborso o compenso. Raggiunta la quota, l'avvio di nuove analisi è sospeso fino all'azzeramento successivo, la cui data è indicata nel tuo account.",
    "{0}. Durée, reconduction et résiliation": "{0}. Durata, rinnovo e disdetta",
    "Les abonnements sont": "Gli abbonamenti sono",
    "sans engagement de durée": "senza vincolo di durata",
    "et reconduits automatiquement à chaque échéance, pour une période identique à la précédente, sauf résiliation.":
        "e si rinnovano automaticamente a ogni scadenza per un periodo identico al precedente, salvo disdetta.",
    "Vous pouvez": "Puoi",
    "résilier à tout moment": "disdire in qualsiasi momento",
    "depuis votre espace client, sans motif ni frais. La résiliation met fin à la reconduction automatique : votre accès est maintenu jusqu'au terme de la période en cours déjà payée, après quoi il prend fin. Conformément au droit applicable, aucun remboursement au prorata n'est effectué pour une période entamée. Pour l'abonnement annuel, la résiliation en cours d'année met fin à la reconduction à la date anniversaire, l'accès étant maintenu jusqu'à cette date.":
        "dal tuo account, senza motivo né spese. La disdetta interrompe il rinnovo automatico: l'accesso resta fino alla fine del periodo in corso già pagato, poi termina. Secondo la legge applicabile non è previsto alcun rimborso proporzionale per un periodo iniziato. Con l'abbonamento annuale, la disdetta durante l'anno interrompe il rinnovo alla data di anniversario, mantenendo l'accesso fino a quel giorno.",
    "Nous pouvons résilier ou suspendre un abonnement en cas de défaut de paiement persistant après relances, ou de manquement grave aux présentes conditions.":
        "Possiamo disdire o sospendere un abbonamento in caso di mancato pagamento persistente dopo i solleciti, o di grave violazione delle presenti condizioni.",
    "{0}. Crédits": "{0}. Crediti",
    "Les crédits achetés en packs ont une": "I crediti acquistati in pacchetti hanno una",
    "validité d'un ({0}) mois": "validità di un ({0}) mese",
    "à compter de l'achat, ne sont pas reportables au-delà de ce délai et ne sont pas remboursables une fois la commande exécutée. L'achat de crédits est facultatif et indépendant de l'abonnement.":
        "dall'acquisto, non sono riportabili oltre tale termine e non sono rimborsabili una volta eseguito l'ordine. L'acquisto di crediti è facoltativo e indipendente dall'abbonamento.",
    "{0}. Droit de rétractation": "{0}. Diritto di recesso",
    "Conformément aux articles L.{0}-{1} et suivants du Code de la consommation, vous disposez d'un délai de {2} jours pour vous rétracter. Toutefois, pour la fourniture d'un":
        "Ai sensi degli articoli L.{0}-{1} e seguenti del Codice del consumo francese, hai {2} giorni per recedere. Tuttavia, per la fornitura di",
    "contenu numérique et de services exécutés immédiatement": "contenuti digitali e servizi eseguiti immediatamente",
    ", vous acceptez expressément, en souscrivant, que l'exécution commence avant la fin du délai de rétractation et":
        ", sottoscrivendo accetti espressamente che l'esecuzione inizi prima della fine del termine di recesso e",
    "renoncez à votre droit de rétractation": "rinunci al tuo diritto di recesso",
    "pour la part du service déjà consommée (analyses, crédits utilisés), conformément à l'article L.{0}-{1}.":
        "per la parte di servizio già usata (analisi, crediti consumati), ai sensi dell'articolo L.{0}-{1}.",
    "{0}. Disponibilité et garanties": "{0}. Disponibilità e garanzie",
    "Le service est fourni « tel quel », dans la limite des moyens techniques disponibles. Les analyses générées par l'IA sont des estimations à visée indicative et ne constituent pas une garantie de résultats commerciaux. Nous nous efforçons d'assurer la continuité du service sans pouvoir la garantir de façon absolue (maintenance, dépendances tierces).":
        "Il servizio è fornito «così com'è», nei limiti dei mezzi tecnici disponibili. Le analisi generate dall'IA sono stime a titolo indicativo e non garantiscono risultati commerciali. Ci impegniamo a garantire la continuità del servizio senza poterla assicurare in modo assoluto (manutenzione, dipendenze da terzi).",
    "{0}. Responsabilité": "{0}. Responsabilità",
    "La responsabilité de DOPE VENTURES ne saurait être engagée pour les décisions prises sur la base des analyses, ni pour les dommages indirects. En tout état de cause, la responsabilité est limitée au montant payé par le client au cours des {0} derniers mois.":
        "DOPE VENTURES non risponde delle decisioni prese sulla base delle analisi né dei danni indiretti. In ogni caso la responsabilità è limitata all'importo pagato dal cliente negli ultimi {0} mesi.",
    "{0}. Données personnelles": "{0}. Dati personali",
    "Le traitement des données est décrit dans notre": "Il trattamento dei dati è descritto nella nostra",
    "politique de confidentialité": "informativa sulla privacy",
    "{0}. Service client, réclamations et médiation": "{0}. Assistenza clienti, reclami e mediazione",
    "Pour toute réclamation :": "Per qualsiasi reclamo:",
    ". Conformément à l'article L.{0}-{1} du Code de la consommation, le consommateur peut recourir gratuitement à un médiateur de la consommation en vue de la résolution amiable d'un litige. Le médiateur désigné par DOPE VENTURES est le":
        ". Ai sensi dell'articolo L.{0}-{1} del Codice del consumo francese, il consumatore può rivolgersi gratuitamente a un mediatore per la risoluzione amichevole di una controversia. Il mediatore designato da DOPE VENTURES è il",
    "CM{0}C — Centre de Médiation de la Consommation de Conciliateurs de Justice":
        "CM{0}C — Centre de Médiation de la Consommation de Conciliateurs de Justice",
    ", {0} rue Saint Jean, {1} Paris —": ", {0} rue Saint Jean, {1} Parigi —",
    "{0}. Droit applicable": "{0}. Legge applicabile",
    "Les présentes CGV sont soumises au droit français. À défaut de résolution amiable, les tribunaux français sont compétents.":
        "Le presenti CGV sono soggette al diritto francese. In mancanza di accordo amichevole sono competenti i tribunali francesi.",
}

T_CGV["pt-br"] = {
    "Conditions générales de vente — Qeerah": "Condições gerais de venda — Qeerah",
    "Conditions générales de vente de Qeerah (DOPE VENTURES).":
        "Condições gerais de venda da Qeerah (DOPE VENTURES).",
    "← Retour à l'accueil": "← Voltar ao início",
    "Conditions générales de vente": "Condições gerais de venda",
    "Qeerah — édité par DOPE VENTURES · Dernière mise à jour : août {0}":
        "Qeerah — publicado pela DOPE VENTURES · Última atualização: agosto de {0}",
    "{0}. Vendeur": "{0}. Vendedor",
    "Les présentes conditions générales de vente (CGV) régissent les abonnements et achats proposés sur":
        "Estas condições gerais de venda (CGV) regem as assinaturas e compras oferecidas em",
    ", édité par :": ", publicado por:",
    ", SASU au capital de {0} €": ", SASU de direito francês com capital de € {0}",
    "RCS Paris {0} — Siège : {1} rue Vivienne, {2} Paris, France":
        "Registro comercial de Paris {0} — Sede: {1} rue Vivienne, {2} Paris, França",
    "Représentée par son Président, Aimeric Bourgon": "Representada por seu Presidente, Aimeric Bourgon",
    "Contact :": "Contato:",
    "{0}. Objet": "{0}. Objeto",
    "Qeerah est un service en ligne (SaaS) d'analyse de vidéos et de génération de contenu assistée par intelligence artificielle, à destination des créateurs. Les présentes CGV s'appliquent à tout abonnement payant et à tout achat de crédits.":
        "A Qeerah é um serviço online (SaaS) de análise de vídeos e de criação de conteúdo assistida por inteligência artificial, voltado a criadores. Estas CGV se aplicam a toda assinatura paga e a toda compra de créditos.",
    "{0}. Offre et prix": "{0}. Oferta e preços",
    "Qeerah propose une": "A Qeerah oferece uma",
    "offre d'abonnement unique, « Qeerah Pro »": "assinatura única, “Qeerah Pro”",
    ", disponible selon deux périodicités au choix :": ", disponível em duas periodicidades à escolha:",
    "{0} € TTC par mois": "€ {0} por mês, impostos incluídos",
    ", facturé mensuellement ;": ", cobrado mensalmente;",
    "{0} € TTC par an": "€ {0} por ano, impostos incluídos",
    ", facturé annuellement, soit l'équivalent de deux mensualités offertes par rapport au tarif mensuel.":
        ", cobrado anualmente — o equivalente a duas mensalidades grátis em relação à tarifa mensal.",
    "Les deux périodicités donnent accès aux": "As duas periodicidades dão acesso às",
    "mêmes fonctionnalités, sans restriction": "mesmas funcionalidades, sem restrição",
    ", et au même quota d'analyses défini à l'article {0}. Des":
        ", e à mesma cota de análises definida no artigo {0}. É possível comprar à parte, de forma opcional,",
    "packs de crédits": "pacotes de créditos",
    ", destinés aux fonctionnalités de génération d'images par intelligence artificielle, peuvent être achetés séparément et facultativement ; ils ne constituent pas un abonnement.":
        " destinados às funções de geração de imagens por inteligência artificial; eles não constituem assinatura.",
    "TVA non applicable, article {0} B du CGI":
        "Sem cobrança de IVA — isenção de microempresa francesa, art. {0} B do código tributário francês",
    ": les prix affichés sont nets de taxe, aucune TVA n'est facturée ni récupérable. Le prix affiché correspond donc au montant effectivement dû. Les prix peuvent évoluer ; le prix applicable est celui affiché au moment de la commande, et toute évolution tarifaire est sans effet sur les périodes déjà payées.":
        ": os preços exibidos são sem imposto, nenhum IVA é cobrado nem recuperável. O preço exibido é, portanto, o valor efetivamente devido. Os preços podem mudar; vale o preço exibido no momento do pedido, e qualquer mudança não afeta períodos já pagos.",
    "{0}. Essai gratuit": "{0}. Teste grátis",
    "La création d'un compte donne accès à un": "Criar uma conta dá acesso a um",
    "essai gratuit de sept ({0}) jours": "teste grátis de sete ({0}) dias",
    "à compter de l'inscription, sans paiement ni communication de moyen de paiement. Cet essai donne accès à l'ensemble des fonctionnalités, dans la limite de":
        "a partir do cadastro, sem pagamento e sem informar meio de pagamento. O teste dá acesso a todas as funcionalidades, com limite de",
    "dix ({0}) analyses de vidéos": "dez ({0}) análises de vídeo",
    ". À l'expiration de l'essai, en l'absence d'abonnement, les analyses déjà réalisées restent consultables mais aucune nouvelle analyse ne peut être lancée. L'essai n'est pas renouvelable et ne se transforme pas automatiquement en abonnement payant.":
        ". Quando o teste termina sem assinatura, as análises já feitas continuam disponíveis, mas nenhuma nova pode ser iniciada. O teste não é renovável e nunca vira uma assinatura paga sozinho.",
    "{0}. Commande et paiement": "{0}. Pedido e pagamento",
    "La souscription s'effectue en ligne. Le paiement est traité de manière sécurisée par notre prestataire":
        "A assinatura é feita online. O pagamento é processado com segurança pelo nosso prestador",
    "; Qeerah n'a jamais accès aux données complètes de votre moyen de paiement. La commande est confirmée par e-mail. Les abonnements sont facturés d'avance, pour la période choisie (mensuelle ou annuelle).":
        "; a Qeerah nunca tem acesso aos dados completos do seu meio de pagamento. O pedido é confirmado por e-mail. As assinaturas são cobradas antecipadamente, pelo período escolhido (mensal ou anual).",
    "{0}. Quota d'analyses": "{0}. Cota de análises",
    "L'abonnement Qeerah Pro inclut": "A assinatura Qeerah Pro inclui",
    "cent ({0}) analyses de vidéos par mois": "cem ({0}) análises de vídeo por mês",
    ". Ce quota est décompté uniquement pour les analyses menées à leur terme : une analyse ayant échoué pour une raison technique n'est pas décomptée.":
        ". Só contam as análises concluídas: uma análise que falhou por motivo técnico não é descontada.",
    "Le compteur est": "O contador é",
    "remis à zéro à chaque échéance mensuelle de facturation": "zerado a cada vencimento mensal da cobrança",
    ". Pour l'abonnement annuel, le quota reste de cent analyses par mois, remises à zéro à la date anniversaire mensuelle de la souscription — et non de cent analyses pour l'année entière. Les analyses non utilisées au cours d'un mois":
        ". Na assinatura anual a cota continua sendo de cem análises por mês, zeradas na data mensal de aniversário da assinatura — e não cem análises para o ano inteiro. As análises não usadas em um mês",
    "ne sont pas reportables": "não são acumuláveis",
    "sur le mois suivant et ne donnent lieu à aucun remboursement ni compensation. Une fois le quota atteint, la possibilité de lancer de nouvelles analyses est suspendue jusqu'à la remise à zéro suivante, dont la date est indiquée dans votre espace client.":
        "para o mês seguinte e não geram reembolso nem compensação. Atingida a cota, iniciar novas análises fica suspenso até a próxima zeragem, cuja data aparece na sua conta.",
    "{0}. Durée, reconduction et résiliation": "{0}. Duração, renovação e cancelamento",
    "Les abonnements sont": "As assinaturas são",
    "sans engagement de durée": "sem fidelidade",
    "et reconduits automatiquement à chaque échéance, pour une période identique à la précédente, sauf résiliation.":
        "e se renovam automaticamente a cada vencimento, por um período igual ao anterior, salvo cancelamento.",
    "Vous pouvez": "Você pode",
    "résilier à tout moment": "cancelar quando quiser",
    "depuis votre espace client, sans motif ni frais. La résiliation met fin à la reconduction automatique : votre accès est maintenu jusqu'au terme de la période en cours déjà payée, après quoi il prend fin. Conformément au droit applicable, aucun remboursement au prorata n'est effectué pour une période entamée. Pour l'abonnement annuel, la résiliation en cours d'année met fin à la reconduction à la date anniversaire, l'accès étant maintenu jusqu'à cette date.":
        "na sua conta, sem justificativa nem custo. O cancelamento encerra a renovação automática: o acesso continua até o fim do período já pago e depois termina. Conforme a lei aplicável, não há reembolso proporcional de período iniciado. Na assinatura anual, cancelar durante o ano encerra a renovação na data de aniversário, com acesso mantido até lá.",
    "Nous pouvons résilier ou suspendre un abonnement en cas de défaut de paiement persistant après relances, ou de manquement grave aux présentes conditions.":
        "Podemos cancelar ou suspender uma assinatura em caso de inadimplência persistente após avisos, ou de descumprimento grave destas condições.",
    "{0}. Crédits": "{0}. Créditos",
    "Les crédits achetés en packs ont une": "Os créditos comprados em pacotes têm",
    "validité d'un ({0}) mois": "validade de um ({0}) mês",
    "à compter de l'achat, ne sont pas reportables au-delà de ce délai et ne sont pas remboursables une fois la commande exécutée. L'achat de crédits est facultatif et indépendant de l'abonnement.":
        "a partir da compra, não são acumuláveis além desse prazo e não são reembolsáveis depois que o pedido é executado. Comprar créditos é opcional e independente da assinatura.",
    "{0}. Droit de rétractation": "{0}. Direito de arrependimento",
    "Conformément aux articles L.{0}-{1} et suivants du Code de la consommation, vous disposez d'un délai de {2} jours pour vous rétracter. Toutefois, pour la fourniture d'un":
        "Conforme os artigos L.{0}-{1} e seguintes do Código do Consumidor francês, você tem {2} dias para se arrepender. No entanto, para o fornecimento de",
    "contenu numérique et de services exécutés immédiatement": "conteúdo digital e de serviços executados de imediato",
    ", vous acceptez expressément, en souscrivant, que l'exécution commence avant la fin du délai de rétractation et":
        ", ao assinar você aceita expressamente que a execução comece antes do fim do prazo de arrependimento e",
    "renoncez à votre droit de rétractation": "renuncia ao seu direito de arrependimento",
    "pour la part du service déjà consommée (analyses, crédits utilisés), conformément à l'article L.{0}-{1}.":
        "pela parte do serviço já consumida (análises, créditos usados), conforme o artigo L.{0}-{1}.",
    "{0}. Disponibilité et garanties": "{0}. Disponibilidade e garantias",
    "Le service est fourni « tel quel », dans la limite des moyens techniques disponibles. Les analyses générées par l'IA sont des estimations à visée indicative et ne constituent pas une garantie de résultats commerciaux. Nous nous efforçons d'assurer la continuité du service sans pouvoir la garantir de façon absolue (maintenance, dépendances tierces).":
        "O serviço é fornecido “como está”, dentro dos meios técnicos disponíveis. As análises geradas pela IA são estimativas de caráter indicativo e não garantem resultados comerciais. Trabalhamos para manter o serviço no ar sem poder garanti-lo de forma absoluta (manutenção, dependências de terceiros).",
    "{0}. Responsabilité": "{0}. Responsabilidade",
    "La responsabilité de DOPE VENTURES ne saurait être engagée pour les décisions prises sur la base des analyses, ni pour les dommages indirects. En tout état de cause, la responsabilité est limitée au montant payé par le client au cours des {0} derniers mois.":
        "A DOPE VENTURES não responde por decisões tomadas com base nas análises nem por danos indiretos. Em qualquer caso, a responsabilidade se limita ao valor pago pelo cliente nos últimos {0} meses.",
    "{0}. Données personnelles": "{0}. Dados pessoais",
    "Le traitement des données est décrit dans notre": "O tratamento dos dados está descrito na nossa",
    "politique de confidentialité": "política de privacidade",
    "{0}. Service client, réclamations et médiation": "{0}. Atendimento, reclamações e mediação",
    "Pour toute réclamation :": "Para qualquer reclamação:",
    ". Conformément à l'article L.{0}-{1} du Code de la consommation, le consommateur peut recourir gratuitement à un médiateur de la consommation en vue de la résolution amiable d'un litige. Le médiateur désigné par DOPE VENTURES est le":
        ". Conforme o artigo L.{0}-{1} do Código do Consumidor francês, o consumidor pode recorrer gratuitamente a um mediador de consumo para resolver um litígio de forma amigável. O mediador designado pela DOPE VENTURES é o",
    "CM{0}C — Centre de Médiation de la Consommation de Conciliateurs de Justice":
        "CM{0}C — Centre de Médiation de la Consommation de Conciliateurs de Justice",
    ", {0} rue Saint Jean, {1} Paris —": ", {0} rue Saint Jean, {1} Paris —",
    "{0}. Droit applicable": "{0}. Lei aplicável",
    "Les présentes CGV sont soumises au droit français. À défaut de résolution amiable, les tribunaux français sont compétents.":
        "Estas CGV são regidas pela lei francesa. Não havendo solução amigável, os tribunais franceses são competentes.",
}

T_CGV["en-ie"] = dict(T_CGV["en"])
T_CGV["es-mx"] = dict(T_CGV["es"])


# ═══════════════════════════════════════════════════════════════════════════
# /privacy — politique de confidentialité
# Les noms des sous-traitants (Render, Supabase, Stripe, Resend, Sentry), les
# scopes de l'API TikTok (`user.info.basic`, `video.list`) et les noms de
# cookies (`_ga`, `_ttp`) sont des identifiants techniques : ils ne sont pas
# listés, donc jamais traduits.
# ═══════════════════════════════════════════════════════════════════════════
T_PRIVACY: dict[str, dict[str, str]] = {}

T_PRIVACY["en"] = {
    "Politique de confidentialité — Qeerah": "Privacy policy — Qeerah",
    "Politique de confidentialité de Qeerah : données collectées, usage des données TikTok, RGPD, suppression.":
        "Qeerah's privacy policy: what we collect, how TikTok data is used, GDPR, deletion.",
    "← Retour à l'accueil": "← Back to home",
    "Politique de confidentialité": "Privacy policy",
    "Qeerah — édité par Dope Ventures · Dernière mise à jour : juin {0}":
        "Qeerah — published by Dope Ventures · Last updated: June {0}",
    "{0}. Responsable du traitement": "{0}. Data controller",
    "Le responsable du traitement des données est": "The data controller is",
    ", SASU au capital de {0} €, RCS Paris {1}, siège social {2} rue Vivienne, {3} Paris, représentée par son Président Aimeric Bourgon. Pour toute question relative à vos données ou exercer vos droits (accès, rectification, suppression, portabilité, opposition) :":
        ", a French SASU with share capital of €{0}, Paris Trade and Companies Register {1}, registered office {2} rue Vivienne, {3} Paris, represented by its President Aimeric Bourgon. For any question about your data, or to exercise your rights (access, correction, deletion, portability, objection):",
    "{0}. Données que nous collectons": "{0}. What we collect",
    "Compte": "Account",
    ": votre adresse e-mail, pour identifier votre compte et gérer vos quotas.":
        ": your email address, to identify your account and manage your quotas.",
    "Analyses": "Analyses",
    ": les vidéos que vous soumettez sont analysées puis transmises à notre fournisseur d'IA. Nous ne stockons pas vos fichiers vidéo sur nos serveurs.":
        ": the videos you submit are analysed and passed to our AI provider. We do not store your video files on our servers.",
    "Données TikTok": "TikTok data",
    "(uniquement si vous connectez votre compte, voir §{0}).":
        "(only if you connect your account, see §{0}).",
    "Statistiques anonymisées": "Anonymised statistics",
    ": catégorie de produit, prix, score, type d'accroche — sans aucun lien avec votre identité.":
        ": product category, price, score, hook type — with no link to your identity.",
    "{0}. Connexion de votre compte TikTok (Login Kit / Display API)":
        "{0}. Connecting your TikTok account (Login Kit / Display API)",
    "Si vous choisissez de connecter votre compte TikTok, nous utilisons l'API officielle de TikTok (Login Kit et Display API) avec votre consentement explicite. Nous accédons alors :":
        "If you choose to connect your TikTok account, we use TikTok's official API (Login Kit and Display API) with your explicit consent. We then access:",
    "aux": "your",
    "informations de base de votre profil": "basic profile information",
    "(pseudo, photo, statistiques publiques de compte) — scope": "(handle, picture, public account statistics) — scope",
    "à la": "your",
    "liste de vos vidéos publiées": "list of published videos",
    "et à leurs métriques publiques (vues, mentions j'aime, commentaires, partages) — scope":
        "and their public metrics (views, likes, comments, shares) — scope",
    "Usage de ces données :": "How this data is used:",
    "elles servent exclusivement à vous fournir l'analyse de vos performances et à améliorer nos recommandations. Nous n'utilisons ces données qu'avec votre autorisation, nous ne les vendons jamais et ne les partageons avec aucun tiers à des fins publicitaires.":
        "solely to give you the analysis of your performance and to improve our recommendations. We use this data only with your permission, we never sell it and we share it with no third party for advertising purposes.",
    "Vous pouvez": "You can",
    "révoquer cet accès à tout moment": "revoke this access at any time",
    ", soit depuis les paramètres de votre compte TikTok, soit en nous contactant : nous supprimons alors les jetons d'accès et les données associées.":
        ", either from your TikTok account settings or by contacting us: we then delete the access tokens and the associated data.",
    "{0}. Finalités": "{0}. Purposes",
    "Fournir le service d'analyse vidéo et de recommandations.":
        "Provide the video analysis and recommendation service.",
    "Gérer votre compte, vos quotas et votre abonnement.":
        "Manage your account, your quotas and your subscription.",
    "Améliorer la qualité de nos modèles via des statistiques":
        "Improve the quality of our models using",
    "anonymisées": "anonymised",
    "et agrégées.": "and aggregated statistics.",
    "{0}. Partage des données": "{0}. Sharing your data",
    "Nous faisons appel à des sous-traitants techniques strictement nécessaires au service :":
        "We use technical subprocessors that are strictly necessary to run the service:",
    "Hébergement": "Hosting",
    "(Render Services, Inc., États-Unis) : mise à disposition du site et de l'application.":
        "(Render Services, Inc., USA): serving the website and the application.",
    "Base de données": "Database",
    "(Supabase) : stockage de votre compte et de vos analyses.":
        "(Supabase): storing your account and your analyses.",
    "Fournisseur d'IA": "AI provider",
    ": traitement des vidéos que vous soumettez, le temps de l'analyse. Vos vidéos ne sont pas conservées par ce prestataire.":
        ": processing the videos you submit, for the duration of the analysis. Your videos are not kept by this provider.",
    "(Irlande / États-Unis) : encaissement des paiements et facturation. Nous n'avons jamais accès à vos données bancaires.":
        "(Ireland / USA): taking payments and issuing invoices. We never have access to your card details.",
    "et notre service de messagerie : envoi des e-mails du service (bienvenue, résultat d'analyse, réinitialisation de mot de passe).":
        "and our mail service: sending the service's emails (welcome, analysis result, password reset).",
    "(Functional Software, Inc., États-Unis) : détection des erreurs techniques, afin de les corriger. Ce service reçoit le message d'erreur et l'endroit du code concerné. Il est configuré pour":
        "(Functional Software, Inc., USA): spotting technical errors so we can fix them. This service receives the error message and the place in the code concerned. It is configured to",
    "ne recevoir ni votre adresse e-mail, ni votre adresse IP, ni le contenu de vos requêtes":
        "receive neither your email address, nor your IP address, nor the content of your requests",
    "Certains de ces prestataires sont établis aux États-Unis. Les transferts correspondants sont encadrés par les clauses contractuelles types de la Commission européenne et, le cas échéant, par le cadre de protection des données UE–États-Unis.":
        "Some of these providers are based in the United States. Those transfers are covered by the European Commission's standard contractual clauses and, where applicable, by the EU–US Data Privacy Framework.",
    "Aucune donnée n'est vendue. Les seules données transmises à des fins publicitaires sont celles décrites à l'article {0} (mesure de nos campagnes TikTok), et uniquement si vous y avez consenti.":
        "No data is sold. The only data sent for advertising purposes is the data described in article {0} (measuring our TikTok campaigns), and only if you consented to it.",
    "{0}. Conservation": "{0}. Retention",
    "Les données de compte sont conservées tant que votre compte est actif. Les jetons TikTok sont conservés tant que la connexion est active et supprimés à la déconnexion. Les statistiques anonymisées, n'étant pas rattachées à une personne, peuvent être conservées de façon agrégée.":
        "Account data is kept for as long as your account is active. TikTok tokens are kept while the connection is active and deleted when you disconnect. Anonymised statistics, being tied to no individual, may be kept in aggregated form.",
    "{0}. Vos droits (RGPD)": "{0}. Your rights (GDPR)",
    "Vous disposez d'un droit d'accès, de rectification, d'effacement, de portabilité et d'opposition. Pour exercer ces droits, écrivez à":
        "You have the right to access, correct, erase, port and object to the processing of your data. To exercise those rights, write to",
    "{0}. Cookies et traceurs": "{0}. Cookies and trackers",
    "Les cookies techniques nécessaires au fonctionnement du site (session, préférences) sont déposés sans consentement, comme la réglementation le permet. Tous les autres traceurs sont soumis à votre accord préalable, finalité par finalité, via le bandeau affiché à votre première visite :":
        "The technical cookies needed to run the site (session, preferences) are set without consent, as the rules allow. Every other tracker requires your prior agreement, purpose by purpose, through the banner shown on your first visit:",
    "Mesure d'audience": "Audience measurement",
    "— Google Analytics, avec anonymisation de l'adresse IP. Sert à comprendre quelles pages sont utiles. Cookies":
        "— Google Analytics, with IP anonymisation. Used to understand which pages are useful. Cookies",
    "Publicité": "Advertising",
    "— pixel TikTok Ads. Sert à mesurer quelles publicités TikTok amènent des inscriptions et des abonnements. Cookie":
        "— TikTok Ads pixel. Used to measure which TikTok ads bring sign-ups and subscriptions. Cookie",
    ". Lorsqu'un abonnement est payé, la conversion est également transmise à TikTok depuis nos serveurs : votre adresse e-mail n'est alors envoyée que sous forme d'empreinte chiffrée (SHA-{0}), jamais en clair, et uniquement si vous avez accepté cette finalité.":
        ". When a subscription is paid for, the conversion is also sent to TikTok from our servers: your email address is then sent only as a hash (SHA-{0}), never in the clear, and only if you accepted this purpose.",
    "Tant que vous n'avez rien accepté, aucun de ces traceurs n'est chargé et aucune donnée ne part vers Google ou TikTok. Refuser est aussi simple qu'accepter : un seul clic, au même endroit.":
        "Until you accept, none of these trackers is loaded and no data goes to Google or TikTok. Refusing is as easy as accepting: one click, in the same place.",
    "Vous pouvez modifier ou retirer votre choix à tout moment :": "You can change or withdraw your choice at any time:",
    "rouvrir mes préférences de cookies": "reopen my cookie preferences",
    ". Le retrait supprime les cookies déjà déposés.": ". Withdrawing deletes the cookies already set.",
    "TikTok Technology Limited et Google Ireland Limited agissent en qualité de responsables de traitement indépendants pour les données collectées via ces traceurs. Leurs politiques respectives :":
        "TikTok Technology Limited and Google Ireland Limited act as independent controllers for the data collected through these trackers. Their respective policies:",
    "{0}. Contact": "{0}. Contact",
    "Voir les conditions d'utilisation →": "See the terms of use →",
}

T_PRIVACY["de"] = {
    "Politique de confidentialité — Qeerah": "Datenschutzerklärung — Qeerah",
    "Politique de confidentialité de Qeerah : données collectées, usage des données TikTok, RGPD, suppression.":
        "Datenschutzerklärung von Qeerah: erhobene Daten, Umgang mit TikTok-Daten, DSGVO, Löschung.",
    "← Retour à l'accueil": "← Zurück zur Startseite",
    "Politique de confidentialité": "Datenschutzerklärung",
    "Qeerah — édité par Dope Ventures · Dernière mise à jour : juin {0}":
        "Qeerah — herausgegeben von Dope Ventures · Zuletzt aktualisiert: Juni {0}",
    "{0}. Responsable du traitement": "{0}. Verantwortlicher",
    "Le responsable du traitement des données est": "Verantwortlich für die Datenverarbeitung ist",
    ", SASU au capital de {0} €, RCS Paris {1}, siège social {2} rue Vivienne, {3} Paris, représentée par son Président Aimeric Bourgon. Pour toute question relative à vos données ou exercer vos droits (accès, rectification, suppression, portabilité, opposition) :":
        ", SASU französischen Rechts mit einem Stammkapital von {0} €, Handelsregister Paris {1}, Sitz {2} rue Vivienne, {3} Paris, vertreten durch den Präsidenten Aimeric Bourgon. Für Fragen zu deinen Daten oder zur Ausübung deiner Rechte (Auskunft, Berichtigung, Löschung, Übertragbarkeit, Widerspruch):",
    "{0}. Données que nous collectons": "{0}. Welche Daten wir erheben",
    "Compte": "Konto",
    ": votre adresse e-mail, pour identifier votre compte et gérer vos quotas.":
        ": deine E-Mail-Adresse, um dein Konto zu identifizieren und deine Kontingente zu verwalten.",
    "Analyses": "Analysen",
    ": les vidéos que vous soumettez sont analysées puis transmises à notre fournisseur d'IA. Nous ne stockons pas vos fichiers vidéo sur nos serveurs.":
        ": Die Videos, die du einreichst, werden analysiert und an unseren KI-Anbieter übermittelt. Wir speichern deine Videodateien nicht auf unseren Servern.",
    "Données TikTok": "TikTok-Daten",
    "(uniquement si vous connectez votre compte, voir §{0}).":
        "(nur wenn du dein Konto verbindest, siehe §{0}).",
    "Statistiques anonymisées": "Anonymisierte Statistiken",
    ": catégorie de produit, prix, score, type d'accroche — sans aucun lien avec votre identité.":
        ": Produktkategorie, Preis, Wertung, Art des Hooks — ohne jeden Bezug zu deiner Identität.",
    "{0}. Connexion de votre compte TikTok (Login Kit / Display API)":
        "{0}. Verbinden deines TikTok-Kontos (Login Kit / Display API)",
    "Si vous choisissez de connecter votre compte TikTok, nous utilisons l'API officielle de TikTok (Login Kit et Display API) avec votre consentement explicite. Nous accédons alors :":
        "Wenn du dein TikTok-Konto verbindest, nutzen wir mit deiner ausdrücklichen Einwilligung die offizielle TikTok-API (Login Kit und Display API). Wir greifen dann zu auf:",
    "aux": "die",
    "informations de base de votre profil": "Basisinformationen deines Profils",
    "(pseudo, photo, statistiques publiques de compte) — scope": "(Name, Bild, öffentliche Kontostatistiken) — Scope",
    "à la": "die",
    "liste de vos vidéos publiées": "Liste deiner veröffentlichten Videos",
    "et à leurs métriques publiques (vues, mentions j'aime, commentaires, partages) — scope":
        "und deren öffentliche Kennzahlen (Aufrufe, Likes, Kommentare, Shares) — Scope",
    "Usage de ces données :": "Wozu diese Daten dienen:",
    "elles servent exclusivement à vous fournir l'analyse de vos performances et à améliorer nos recommandations. Nous n'utilisons ces données qu'avec votre autorisation, nous ne les vendons jamais et ne les partageons avec aucun tiers à des fins publicitaires.":
        "ausschließlich dazu, dir die Analyse deiner Ergebnisse zu liefern und unsere Empfehlungen zu verbessern. Wir nutzen diese Daten nur mit deiner Erlaubnis, verkaufen sie nie und geben sie an keinen Dritten zu Werbezwecken weiter.",
    "Vous pouvez": "Du kannst",
    "révoquer cet accès à tout moment": "diesen Zugriff jederzeit widerrufen",
    ", soit depuis les paramètres de votre compte TikTok, soit en nous contactant : nous supprimons alors les jetons d'accès et les données associées.":
        " — entweder in den Einstellungen deines TikTok-Kontos oder indem du uns schreibst: Wir löschen dann die Zugriffstoken und die zugehörigen Daten.",
    "{0}. Finalités": "{0}. Zwecke",
    "Fournir le service d'analyse vidéo et de recommandations.":
        "Den Dienst zur Videoanalyse und für Empfehlungen bereitstellen.",
    "Gérer votre compte, vos quotas et votre abonnement.":
        "Dein Konto, deine Kontingente und dein Abo verwalten.",
    "Améliorer la qualité de nos modèles via des statistiques":
        "Die Qualität unserer Modelle verbessern, über",
    "anonymisées": "anonymisierte",
    "et agrégées.": "und aggregierte Statistiken.",
    "{0}. Partage des données": "{0}. Weitergabe der Daten",
    "Nous faisons appel à des sous-traitants techniques strictement nécessaires au service :":
        "Wir setzen technische Auftragsverarbeiter ein, die für den Dienst zwingend nötig sind:",
    "Hébergement": "Hosting",
    "(Render Services, Inc., États-Unis) : mise à disposition du site et de l'application.":
        "(Render Services, Inc., USA): Bereitstellung von Website und Anwendung.",
    "Base de données": "Datenbank",
    "(Supabase) : stockage de votre compte et de vos analyses.":
        "(Supabase): Speicherung deines Kontos und deiner Analysen.",
    "Fournisseur d'IA": "KI-Anbieter",
    ": traitement des vidéos que vous soumettez, le temps de l'analyse. Vos vidéos ne sont pas conservées par ce prestataire.":
        ": Verarbeitung der Videos, die du einreichst, für die Dauer der Analyse. Dieser Dienstleister bewahrt deine Videos nicht auf.",
    "(Irlande / États-Unis) : encaissement des paiements et facturation. Nous n'avons jamais accès à vos données bancaires.":
        "(Irland / USA): Zahlungsabwicklung und Rechnungsstellung. Wir haben nie Zugriff auf deine Zahlungsdaten.",
    "et notre service de messagerie : envoi des e-mails du service (bienvenue, résultat d'analyse, réinitialisation de mot de passe).":
        "und unser Mailversand: Versand der Dienst-E-Mails (Willkommen, Analyseergebnis, Passwort zurücksetzen).",
    "(Functional Software, Inc., États-Unis) : détection des erreurs techniques, afin de les corriger. Ce service reçoit le message d'erreur et l'endroit du code concerné. Il est configuré pour":
        "(Functional Software, Inc., USA): Erkennen technischer Fehler, um sie zu beheben. Dieser Dienst erhält die Fehlermeldung und die betroffene Stelle im Code. Er ist so eingestellt, dass er",
    "ne recevoir ni votre adresse e-mail, ni votre adresse IP, ni le contenu de vos requêtes":
        "weder deine E-Mail-Adresse noch deine IP-Adresse noch den Inhalt deiner Anfragen erhält",
    "Certains de ces prestataires sont établis aux États-Unis. Les transferts correspondants sont encadrés par les clauses contractuelles types de la Commission européenne et, le cas échéant, par le cadre de protection des données UE–États-Unis.":
        "Einige dieser Dienstleister sitzen in den USA. Die entsprechenden Übermittlungen stützen sich auf die Standardvertragsklauseln der Europäischen Kommission und, soweit einschlägig, auf das EU-US Data Privacy Framework.",
    "Aucune donnée n'est vendue. Les seules données transmises à des fins publicitaires sont celles décrites à l'article {0} (mesure de nos campagnes TikTok), et uniquement si vous y avez consenti.":
        "Es werden keine Daten verkauft. Die einzigen zu Werbezwecken übermittelten Daten sind die in Artikel {0} beschriebenen (Messung unserer TikTok-Kampagnen), und nur, wenn du dem zugestimmt hast.",
    "{0}. Conservation": "{0}. Speicherdauer",
    "Les données de compte sont conservées tant que votre compte est actif. Les jetons TikTok sont conservés tant que la connexion est active et supprimés à la déconnexion. Les statistiques anonymisées, n'étant pas rattachées à une personne, peuvent être conservées de façon agrégée.":
        "Kontodaten bleiben gespeichert, solange dein Konto aktiv ist. TikTok-Token bleiben gespeichert, solange die Verbindung besteht, und werden beim Trennen gelöscht. Anonymisierte Statistiken sind keiner Person zugeordnet und können in aggregierter Form aufbewahrt werden.",
    "{0}. Vos droits (RGPD)": "{0}. Deine Rechte (DSGVO)",
    "Vous disposez d'un droit d'accès, de rectification, d'effacement, de portabilité et d'opposition. Pour exercer ces droits, écrivez à":
        "Du hast das Recht auf Auskunft, Berichtigung, Löschung, Übertragbarkeit und Widerspruch. Um diese Rechte auszuüben, schreib an",
    "{0}. Cookies et traceurs": "{0}. Cookies und Tracker",
    "Les cookies techniques nécessaires au fonctionnement du site (session, préférences) sont déposés sans consentement, comme la réglementation le permet. Tous les autres traceurs sont soumis à votre accord préalable, finalité par finalité, via le bandeau affiché à votre première visite :":
        "Technisch notwendige Cookies für den Betrieb der Website (Sitzung, Einstellungen) werden ohne Einwilligung gesetzt, wie es die Vorschriften erlauben. Alle anderen Tracker brauchen deine vorherige Zustimmung, Zweck für Zweck, über das Banner beim ersten Besuch:",
    "Mesure d'audience": "Reichweitenmessung",
    "— Google Analytics, avec anonymisation de l'adresse IP. Sert à comprendre quelles pages sont utiles. Cookies":
        "— Google Analytics, mit anonymisierter IP-Adresse. Dient dazu zu verstehen, welche Seiten nützlich sind. Cookies",
    "Publicité": "Werbung",
    "— pixel TikTok Ads. Sert à mesurer quelles publicités TikTok amènent des inscriptions et des abonnements. Cookie":
        "— TikTok-Ads-Pixel. Dient dazu zu messen, welche TikTok-Anzeigen zu Anmeldungen und Abos führen. Cookie",
    ". Lorsqu'un abonnement est payé, la conversion est également transmise à TikTok depuis nos serveurs : votre adresse e-mail n'est alors envoyée que sous forme d'empreinte chiffrée (SHA-{0}), jamais en clair, et uniquement si vous avez accepté cette finalité.":
        ". Wird ein Abo bezahlt, wird die Konversion auch von unseren Servern an TikTok gemeldet: Deine E-Mail-Adresse geht dabei nur als Prüfsumme (SHA-{0}) heraus, nie im Klartext, und nur wenn du diesem Zweck zugestimmt hast.",
    "Tant que vous n'avez rien accepté, aucun de ces traceurs n'est chargé et aucune donnée ne part vers Google ou TikTok. Refuser est aussi simple qu'accepter : un seul clic, au même endroit.":
        "Solange du nichts zugestimmt hast, wird keiner dieser Tracker geladen und es gehen keine Daten an Google oder TikTok. Ablehnen ist genauso einfach wie Zustimmen: ein Klick, an derselben Stelle.",
    "Vous pouvez modifier ou retirer votre choix à tout moment :": "Du kannst deine Auswahl jederzeit ändern oder zurücknehmen:",
    "rouvrir mes préférences de cookies": "meine Cookie-Einstellungen erneut öffnen",
    ". Le retrait supprime les cookies déjà déposés.": ". Der Widerruf löscht die bereits gesetzten Cookies.",
    "TikTok Technology Limited et Google Ireland Limited agissent en qualité de responsables de traitement indépendants pour les données collectées via ces traceurs. Leurs politiques respectives :":
        "TikTok Technology Limited und Google Ireland Limited handeln für die über diese Tracker erhobenen Daten als eigenständig Verantwortliche. Ihre jeweiligen Erklärungen:",
    "{0}. Contact": "{0}. Kontakt",
    "Voir les conditions d'utilisation →": "Zu den Nutzungsbedingungen →",
}

T_PRIVACY["es"] = {
    "Politique de confidentialité — Qeerah": "Política de privacidad — Qeerah",
    "Politique de confidentialité de Qeerah : données collectées, usage des données TikTok, RGPD, suppression.":
        "Política de privacidad de Qeerah: datos recogidos, uso de los datos de TikTok, RGPD, supresión.",
    "← Retour à l'accueil": "← Volver al inicio",
    "Politique de confidentialité": "Política de privacidad",
    "Qeerah — édité par Dope Ventures · Dernière mise à jour : juin {0}":
        "Qeerah — editado por Dope Ventures · Última actualización: junio de {0}",
    "{0}. Responsable du traitement": "{0}. Responsable del tratamiento",
    "Le responsable du traitement des données est": "El responsable del tratamiento de los datos es",
    ", SASU au capital de {0} €, RCS Paris {1}, siège social {2} rue Vivienne, {3} Paris, représentée par son Président Aimeric Bourgon. Pour toute question relative à vos données ou exercer vos droits (accès, rectification, suppression, portabilité, opposition) :":
        ", SASU de derecho francés con un capital de {0} €, Registro Mercantil de París {1}, domicilio social {2} rue Vivienne, {3} París, representada por su Presidente Aimeric Bourgon. Para cualquier duda sobre tus datos o para ejercer tus derechos (acceso, rectificación, supresión, portabilidad, oposición):",
    "{0}. Données que nous collectons": "{0}. Datos que recogemos",
    "Compte": "Cuenta",
    ": votre adresse e-mail, pour identifier votre compte et gérer vos quotas.":
        ": tu dirección de correo, para identificar tu cuenta y gestionar tus cuotas.",
    "Analyses": "Análisis",
    ": les vidéos que vous soumettez sont analysées puis transmises à notre fournisseur d'IA. Nous ne stockons pas vos fichiers vidéo sur nos serveurs.":
        ": los vídeos que envías se analizan y se transmiten a nuestro proveedor de IA. No guardamos tus archivos de vídeo en nuestros servidores.",
    "Données TikTok": "Datos de TikTok",
    "(uniquement si vous connectez votre compte, voir §{0}).":
        "(solo si conectas tu cuenta, ver §{0}).",
    "Statistiques anonymisées": "Estadísticas anonimizadas",
    ": catégorie de produit, prix, score, type d'accroche — sans aucun lien avec votre identité.":
        ": categoría de producto, precio, puntuación, tipo de gancho — sin ningún vínculo con tu identidad.",
    "{0}. Connexion de votre compte TikTok (Login Kit / Display API)":
        "{0}. Conexión de tu cuenta de TikTok (Login Kit / Display API)",
    "Si vous choisissez de connecter votre compte TikTok, nous utilisons l'API officielle de TikTok (Login Kit et Display API) avec votre consentement explicite. Nous accédons alors :":
        "Si decides conectar tu cuenta de TikTok, usamos la API oficial de TikTok (Login Kit y Display API) con tu consentimiento explícito. Accedemos entonces a:",
    "aux": "la",
    "informations de base de votre profil": "información básica de tu perfil",
    "(pseudo, photo, statistiques publiques de compte) — scope": "(usuario, foto, estadísticas públicas de la cuenta) — scope",
    "à la": "la",
    "liste de vos vidéos publiées": "lista de tus vídeos publicados",
    "et à leurs métriques publiques (vues, mentions j'aime, commentaires, partages) — scope":
        "y sus métricas públicas (visualizaciones, me gusta, comentarios, veces compartido) — scope",
    "Usage de ces données :": "Uso de estos datos:",
    "elles servent exclusivement à vous fournir l'analyse de vos performances et à améliorer nos recommandations. Nous n'utilisons ces données qu'avec votre autorisation, nous ne les vendons jamais et ne les partageons avec aucun tiers à des fins publicitaires.":
        "sirven exclusivamente para darte el análisis de tus resultados y mejorar nuestras recomendaciones. Solo usamos estos datos con tu autorización, nunca los vendemos y no los compartimos con ningún tercero con fines publicitarios.",
    "Vous pouvez": "Puedes",
    "révoquer cet accès à tout moment": "revocar este acceso cuando quieras",
    ", soit depuis les paramètres de votre compte TikTok, soit en nous contactant : nous supprimons alors les jetons d'accès et les données associées.":
        ", desde los ajustes de tu cuenta de TikTok o escribiéndonos: entonces eliminamos los tokens de acceso y los datos asociados.",
    "{0}. Finalités": "{0}. Finalidades",
    "Fournir le service d'analyse vidéo et de recommandations.":
        "Prestar el servicio de análisis de vídeo y de recomendaciones.",
    "Gérer votre compte, vos quotas et votre abonnement.":
        "Gestionar tu cuenta, tus cuotas y tu suscripción.",
    "Améliorer la qualité de nos modèles via des statistiques":
        "Mejorar la calidad de nuestros modelos mediante estadísticas",
    "anonymisées": "anonimizadas",
    "et agrégées.": "y agregadas.",
    "{0}. Partage des données": "{0}. Comunicación de los datos",
    "Nous faisons appel à des sous-traitants techniques strictement nécessaires au service :":
        "Recurrimos a encargados técnicos estrictamente necesarios para el servicio:",
    "Hébergement": "Alojamiento",
    "(Render Services, Inc., États-Unis) : mise à disposition du site et de l'application.":
        "(Render Services, Inc., EE. UU.): puesta a disposición del sitio y de la aplicación.",
    "Base de données": "Base de datos",
    "(Supabase) : stockage de votre compte et de vos analyses.":
        "(Supabase): almacenamiento de tu cuenta y de tus análisis.",
    "Fournisseur d'IA": "Proveedor de IA",
    ": traitement des vidéos que vous soumettez, le temps de l'analyse. Vos vidéos ne sont pas conservées par ce prestataire.":
        ": tratamiento de los vídeos que envías, durante el análisis. Este proveedor no conserva tus vídeos.",
    "(Irlande / États-Unis) : encaissement des paiements et facturation. Nous n'avons jamais accès à vos données bancaires.":
        "(Irlanda / EE. UU.): cobro de los pagos y facturación. Nunca accedemos a tus datos bancarios.",
    "et notre service de messagerie : envoi des e-mails du service (bienvenue, résultat d'analyse, réinitialisation de mot de passe).":
        "y nuestro servicio de correo: envío de los correos del servicio (bienvenida, resultado de análisis, restablecimiento de contraseña).",
    "(Functional Software, Inc., États-Unis) : détection des erreurs techniques, afin de les corriger. Ce service reçoit le message d'erreur et l'endroit du code concerné. Il est configuré pour":
        "(Functional Software, Inc., EE. UU.): detección de errores técnicos para poder corregirlos. Este servicio recibe el mensaje de error y el punto del código afectado. Está configurado para",
    "ne recevoir ni votre adresse e-mail, ni votre adresse IP, ni le contenu de vos requêtes":
        "no recibir ni tu correo, ni tu dirección IP, ni el contenido de tus peticiones",
    "Certains de ces prestataires sont établis aux États-Unis. Les transferts correspondants sont encadrés par les clauses contractuelles types de la Commission européenne et, le cas échéant, par le cadre de protection des données UE–États-Unis.":
        "Algunos de estos proveedores están establecidos en Estados Unidos. Esas transferencias se amparan en las cláusulas contractuales tipo de la Comisión Europea y, en su caso, en el marco de protección de datos UE–EE. UU.",
    "Aucune donnée n'est vendue. Les seules données transmises à des fins publicitaires sont celles décrites à l'article {0} (mesure de nos campagnes TikTok), et uniquement si vous y avez consenti.":
        "No se vende ningún dato. Los únicos datos transmitidos con fines publicitarios son los descritos en el artículo {0} (medición de nuestras campañas de TikTok), y solo si has dado tu consentimiento.",
    "{0}. Conservation": "{0}. Conservación",
    "Les données de compte sont conservées tant que votre compte est actif. Les jetons TikTok sont conservés tant que la connexion est active et supprimés à la déconnexion. Les statistiques anonymisées, n'étant pas rattachées à une personne, peuvent être conservées de façon agrégée.":
        "Los datos de la cuenta se conservan mientras tu cuenta esté activa. Los tokens de TikTok se conservan mientras la conexión esté activa y se eliminan al desconectarla. Las estadísticas anonimizadas, al no estar vinculadas a ninguna persona, pueden conservarse de forma agregada.",
    "{0}. Vos droits (RGPD)": "{0}. Tus derechos (RGPD)",
    "Vous disposez d'un droit d'accès, de rectification, d'effacement, de portabilité et d'opposition. Pour exercer ces droits, écrivez à":
        "Tienes derecho de acceso, rectificación, supresión, portabilidad y oposición. Para ejercerlos, escribe a",
    "{0}. Cookies et traceurs": "{0}. Cookies y rastreadores",
    "Les cookies techniques nécessaires au fonctionnement du site (session, préférences) sont déposés sans consentement, comme la réglementation le permet. Tous les autres traceurs sont soumis à votre accord préalable, finalité par finalité, via le bandeau affiché à votre première visite :":
        "Las cookies técnicas necesarias para el funcionamiento del sitio (sesión, preferencias) se instalan sin consentimiento, como permite la normativa. Todos los demás rastreadores requieren tu acuerdo previo, finalidad por finalidad, mediante el banner que se muestra en tu primera visita:",
    "Mesure d'audience": "Medición de audiencia",
    "— Google Analytics, avec anonymisation de l'adresse IP. Sert à comprendre quelles pages sont utiles. Cookies":
        "— Google Analytics, con anonimización de la dirección IP. Sirve para entender qué páginas resultan útiles. Cookies",
    "Publicité": "Publicidad",
    "— pixel TikTok Ads. Sert à mesurer quelles publicités TikTok amènent des inscriptions et des abonnements. Cookie":
        "— píxel de TikTok Ads. Sirve para medir qué anuncios de TikTok traen registros y suscripciones. Cookie",
    ". Lorsqu'un abonnement est payé, la conversion est également transmise à TikTok depuis nos serveurs : votre adresse e-mail n'est alors envoyée que sous forme d'empreinte chiffrée (SHA-{0}), jamais en clair, et uniquement si vous avez accepté cette finalité.":
        ". Cuando se paga una suscripción, la conversión también se transmite a TikTok desde nuestros servidores: tu correo se envía únicamente como huella cifrada (SHA-{0}), nunca en claro, y solo si has aceptado esta finalidad.",
    "Tant que vous n'avez rien accepté, aucun de ces traceurs n'est chargé et aucune donnée ne part vers Google ou TikTok. Refuser est aussi simple qu'accepter : un seul clic, au même endroit.":
        "Mientras no aceptes nada, no se carga ninguno de estos rastreadores y no sale ningún dato hacia Google ni TikTok. Rechazar es tan fácil como aceptar: un solo clic, en el mismo sitio.",
    "Vous pouvez modifier ou retirer votre choix à tout moment :": "Puedes cambiar o retirar tu elección cuando quieras:",
    "rouvrir mes préférences de cookies": "volver a abrir mis preferencias de cookies",
    ". Le retrait supprime les cookies déjà déposés.": ". Al retirarla se eliminan las cookies ya instaladas.",
    "TikTok Technology Limited et Google Ireland Limited agissent en qualité de responsables de traitement indépendants pour les données collectées via ces traceurs. Leurs politiques respectives :":
        "TikTok Technology Limited y Google Ireland Limited actúan como responsables del tratamiento independientes de los datos recogidos mediante estos rastreadores. Sus políticas respectivas:",
    "{0}. Contact": "{0}. Contacto",
    "Voir les conditions d'utilisation →": "Ver las condiciones de uso →",
}

T_PRIVACY["it"] = {
    "Politique de confidentialité — Qeerah": "Informativa sulla privacy — Qeerah",
    "Politique de confidentialité de Qeerah : données collectées, usage des données TikTok, RGPD, suppression.":
        "Informativa sulla privacy di Qeerah: dati raccolti, uso dei dati TikTok, GDPR, cancellazione.",
    "← Retour à l'accueil": "← Torna alla home",
    "Politique de confidentialité": "Informativa sulla privacy",
    "Qeerah — édité par Dope Ventures · Dernière mise à jour : juin {0}":
        "Qeerah — pubblicato da Dope Ventures · Ultimo aggiornamento: giugno {0}",
    "{0}. Responsable du traitement": "{0}. Titolare del trattamento",
    "Le responsable du traitement des données est": "Il titolare del trattamento dei dati è",
    ", SASU au capital de {0} €, RCS Paris {1}, siège social {2} rue Vivienne, {3} Paris, représentée par son Président Aimeric Bourgon. Pour toute question relative à vos données ou exercer vos droits (accès, rectification, suppression, portabilité, opposition) :":
        ", SASU di diritto francese con capitale di {0} €, Registro delle imprese di Parigi {1}, sede legale {2} rue Vivienne, {3} Parigi, rappresentata dal suo Presidente Aimeric Bourgon. Per qualsiasi domanda sui tuoi dati o per esercitare i tuoi diritti (accesso, rettifica, cancellazione, portabilità, opposizione):",
    "{0}. Données que nous collectons": "{0}. Dati che raccogliamo",
    "Compte": "Account",
    ": votre adresse e-mail, pour identifier votre compte et gérer vos quotas.":
        ": il tuo indirizzo email, per identificare l'account e gestire le tue quote.",
    "Analyses": "Analisi",
    ": les vidéos que vous soumettez sont analysées puis transmises à notre fournisseur d'IA. Nous ne stockons pas vos fichiers vidéo sur nos serveurs.":
        ": i video che invii vengono analizzati e trasmessi al nostro fornitore di IA. Non conserviamo i tuoi file video sui nostri server.",
    "Données TikTok": "Dati TikTok",
    "(uniquement si vous connectez votre compte, voir §{0}).":
        "(solo se colleghi il tuo account, vedi §{0}).",
    "Statistiques anonymisées": "Statistiche anonimizzate",
    ": catégorie de produit, prix, score, type d'accroche — sans aucun lien avec votre identité.":
        ": categoria di prodotto, prezzo, punteggio, tipo di hook — senza alcun collegamento con la tua identità.",
    "{0}. Connexion de votre compte TikTok (Login Kit / Display API)":
        "{0}. Collegamento del tuo account TikTok (Login Kit / Display API)",
    "Si vous choisissez de connecter votre compte TikTok, nous utilisons l'API officielle de TikTok (Login Kit et Display API) avec votre consentement explicite. Nous accédons alors :":
        "Se scegli di collegare il tuo account TikTok, usiamo l'API ufficiale di TikTok (Login Kit e Display API) con il tuo consenso esplicito. Accediamo allora:",
    "aux": "alle",
    "informations de base de votre profil": "informazioni di base del tuo profilo",
    "(pseudo, photo, statistiques publiques de compte) — scope": "(nome utente, foto, statistiche pubbliche dell'account) — scope",
    "à la": "all'",
    "liste de vos vidéos publiées": "elenco dei tuoi video pubblicati",
    "et à leurs métriques publiques (vues, mentions j'aime, commentaires, partages) — scope":
        "e alle loro metriche pubbliche (visualizzazioni, «mi piace», commenti, condivisioni) — scope",
    "Usage de ces données :": "Uso di questi dati:",
    "elles servent exclusivement à vous fournir l'analyse de vos performances et à améliorer nos recommandations. Nous n'utilisons ces données qu'avec votre autorisation, nous ne les vendons jamais et ne les partageons avec aucun tiers à des fins publicitaires.":
        "servono esclusivamente a fornirti l'analisi dei tuoi risultati e a migliorare i nostri consigli. Usiamo questi dati solo con la tua autorizzazione, non li vendiamo mai e non li condividiamo con terzi a fini pubblicitari.",
    "Vous pouvez": "Puoi",
    "révoquer cet accès à tout moment": "revocare questo accesso in qualsiasi momento",
    ", soit depuis les paramètres de votre compte TikTok, soit en nous contactant : nous supprimons alors les jetons d'accès et les données associées.":
        ", dalle impostazioni del tuo account TikTok o scrivendoci: cancelliamo allora i token di accesso e i dati collegati.",
    "{0}. Finalités": "{0}. Finalità",
    "Fournir le service d'analyse vidéo et de recommandations.":
        "Fornire il servizio di analisi video e di consigli.",
    "Gérer votre compte, vos quotas et votre abonnement.":
        "Gestire il tuo account, le tue quote e il tuo abbonamento.",
    "Améliorer la qualité de nos modèles via des statistiques":
        "Migliorare la qualità dei nostri modelli tramite statistiche",
    "anonymisées": "anonimizzate",
    "et agrégées.": "e aggregate.",
    "{0}. Partage des données": "{0}. Condivisione dei dati",
    "Nous faisons appel à des sous-traitants techniques strictement nécessaires au service :":
        "Ci avvaliamo di responsabili tecnici strettamente necessari al servizio:",
    "Hébergement": "Hosting",
    "(Render Services, Inc., États-Unis) : mise à disposition du site et de l'application.":
        "(Render Services, Inc., USA): messa a disposizione del sito e dell'applicazione.",
    "Base de données": "Database",
    "(Supabase) : stockage de votre compte et de vos analyses.":
        "(Supabase): archiviazione del tuo account e delle tue analisi.",
    "Fournisseur d'IA": "Fornitore di IA",
    ": traitement des vidéos que vous soumettez, le temps de l'analyse. Vos vidéos ne sont pas conservées par ce prestataire.":
        ": trattamento dei video che invii, per la durata dell'analisi. Questo fornitore non conserva i tuoi video.",
    "(Irlande / États-Unis) : encaissement des paiements et facturation. Nous n'avons jamais accès à vos données bancaires.":
        "(Irlanda / USA): incasso dei pagamenti e fatturazione. Non abbiamo mai accesso ai tuoi dati bancari.",
    "et notre service de messagerie : envoi des e-mails du service (bienvenue, résultat d'analyse, réinitialisation de mot de passe).":
        "e il nostro servizio di posta: invio delle email del servizio (benvenuto, risultato dell'analisi, reimpostazione della password).",
    "(Functional Software, Inc., États-Unis) : détection des erreurs techniques, afin de les corriger. Ce service reçoit le message d'erreur et l'endroit du code concerné. Il est configuré pour":
        "(Functional Software, Inc., USA): rilevamento degli errori tecnici per poterli correggere. Questo servizio riceve il messaggio di errore e il punto di codice interessato. È configurato per",
    "ne recevoir ni votre adresse e-mail, ni votre adresse IP, ni le contenu de vos requêtes":
        "non ricevere né la tua email, né il tuo indirizzo IP, né il contenuto delle tue richieste",
    "Certains de ces prestataires sont établis aux États-Unis. Les transferts correspondants sont encadrés par les clauses contractuelles types de la Commission européenne et, le cas échéant, par le cadre de protection des données UE–États-Unis.":
        "Alcuni di questi fornitori hanno sede negli Stati Uniti. I relativi trasferimenti sono coperti dalle clausole contrattuali tipo della Commissione europea e, ove applicabile, dal quadro UE-USA per la protezione dei dati.",
    "Aucune donnée n'est vendue. Les seules données transmises à des fins publicitaires sont celles décrites à l'article {0} (mesure de nos campagnes TikTok), et uniquement si vous y avez consenti.":
        "Nessun dato viene venduto. Gli unici dati trasmessi a fini pubblicitari sono quelli descritti all'articolo {0} (misurazione delle nostre campagne TikTok), e solo se hai dato il consenso.",
    "{0}. Conservation": "{0}. Conservazione",
    "Les données de compte sont conservées tant que votre compte est actif. Les jetons TikTok sont conservés tant que la connexion est active et supprimés à la déconnexion. Les statistiques anonymisées, n'étant pas rattachées à une personne, peuvent être conservées de façon agrégée.":
        "I dati dell'account sono conservati finché l'account è attivo. I token TikTok restano finché il collegamento è attivo e vengono cancellati alla disconnessione. Le statistiche anonimizzate, non essendo riferite a una persona, possono essere conservate in forma aggregata.",
    "{0}. Vos droits (RGPD)": "{0}. I tuoi diritti (GDPR)",
    "Vous disposez d'un droit d'accès, de rectification, d'effacement, de portabilité et d'opposition. Pour exercer ces droits, écrivez à":
        "Hai diritto di accesso, rettifica, cancellazione, portabilità e opposizione. Per esercitarli scrivi a",
    "{0}. Cookies et traceurs": "{0}. Cookie e tracciatori",
    "Les cookies techniques nécessaires au fonctionnement du site (session, préférences) sont déposés sans consentement, comme la réglementation le permet. Tous les autres traceurs sont soumis à votre accord préalable, finalité par finalité, via le bandeau affiché à votre première visite :":
        "I cookie tecnici necessari al funzionamento del sito (sessione, preferenze) sono impostati senza consenso, come la normativa consente. Tutti gli altri tracciatori richiedono il tuo consenso preventivo, finalità per finalità, tramite il banner mostrato alla prima visita:",
    "Mesure d'audience": "Misurazione del pubblico",
    "— Google Analytics, avec anonymisation de l'adresse IP. Sert à comprendre quelles pages sont utiles. Cookies":
        "— Google Analytics, con anonimizzazione dell'indirizzo IP. Serve a capire quali pagine sono utili. Cookie",
    "Publicité": "Pubblicità",
    "— pixel TikTok Ads. Sert à mesurer quelles publicités TikTok amènent des inscriptions et des abonnements. Cookie":
        "— pixel di TikTok Ads. Serve a misurare quali annunci TikTok portano iscrizioni e abbonamenti. Cookie",
    ". Lorsqu'un abonnement est payé, la conversion est également transmise à TikTok depuis nos serveurs : votre adresse e-mail n'est alors envoyée que sous forme d'empreinte chiffrée (SHA-{0}), jamais en clair, et uniquement si vous avez accepté cette finalité.":
        ". Quando un abbonamento viene pagato, la conversione è trasmessa a TikTok anche dai nostri server: la tua email parte solo come impronta cifrata (SHA-{0}), mai in chiaro, e solo se hai accettato questa finalità.",
    "Tant que vous n'avez rien accepté, aucun de ces traceurs n'est chargé et aucune donnée ne part vers Google ou TikTok. Refuser est aussi simple qu'accepter : un seul clic, au même endroit.":
        "Finché non accetti, nessuno di questi tracciatori viene caricato e nessun dato parte verso Google o TikTok. Rifiutare è semplice quanto accettare: un solo clic, nello stesso punto.",
    "Vous pouvez modifier ou retirer votre choix à tout moment :": "Puoi modificare o ritirare la tua scelta in qualsiasi momento:",
    "rouvrir mes préférences de cookies": "riaprire le mie preferenze sui cookie",
    ". Le retrait supprime les cookies déjà déposés.": ". Il ritiro cancella i cookie già impostati.",
    "TikTok Technology Limited et Google Ireland Limited agissent en qualité de responsables de traitement indépendants pour les données collectées via ces traceurs. Leurs politiques respectives :":
        "TikTok Technology Limited e Google Ireland Limited agiscono come titolari autonomi per i dati raccolti tramite questi tracciatori. Le rispettive informative:",
    "{0}. Contact": "{0}. Contatti",
    "Voir les conditions d'utilisation →": "Vedi le condizioni d'uso →",
}

T_PRIVACY["pt-br"] = {
    "Politique de confidentialité — Qeerah": "Política de privacidade — Qeerah",
    "Politique de confidentialité de Qeerah : données collectées, usage des données TikTok, RGPD, suppression.":
        "Política de privacidade da Qeerah: dados coletados, uso dos dados do TikTok, RGPD, exclusão.",
    "← Retour à l'accueil": "← Voltar ao início",
    "Politique de confidentialité": "Política de privacidade",
    "Qeerah — édité par Dope Ventures · Dernière mise à jour : juin {0}":
        "Qeerah — publicado pela Dope Ventures · Última atualização: junho de {0}",
    "{0}. Responsable du traitement": "{0}. Controlador dos dados",
    "Le responsable du traitement des données est": "O controlador do tratamento dos dados é a",
    ", SASU au capital de {0} €, RCS Paris {1}, siège social {2} rue Vivienne, {3} Paris, représentée par son Président Aimeric Bourgon. Pour toute question relative à vos données ou exercer vos droits (accès, rectification, suppression, portabilité, opposition) :":
        ", SASU de direito francês com capital de € {0}, registro comercial de Paris {1}, sede {2} rue Vivienne, {3} Paris, representada por seu Presidente Aimeric Bourgon. Para qualquer dúvida sobre seus dados ou para exercer seus direitos (acesso, correção, exclusão, portabilidade, oposição):",
    "{0}. Données que nous collectons": "{0}. Dados que coletamos",
    "Compte": "Conta",
    ": votre adresse e-mail, pour identifier votre compte et gérer vos quotas.":
        ": seu e-mail, para identificar sua conta e gerenciar suas cotas.",
    "Analyses": "Análises",
    ": les vidéos que vous soumettez sont analysées puis transmises à notre fournisseur d'IA. Nous ne stockons pas vos fichiers vidéo sur nos serveurs.":
        ": os vídeos que você envia são analisados e transmitidos ao nosso fornecedor de IA. Não guardamos seus arquivos de vídeo nos nossos servidores.",
    "Données TikTok": "Dados do TikTok",
    "(uniquement si vous connectez votre compte, voir §{0}).":
        "(apenas se você conectar sua conta, ver §{0}).",
    "Statistiques anonymisées": "Estatísticas anonimizadas",
    ": catégorie de produit, prix, score, type d'accroche — sans aucun lien avec votre identité.":
        ": categoria de produto, preço, nota, tipo de gancho — sem nenhuma ligação com sua identidade.",
    "{0}. Connexion de votre compte TikTok (Login Kit / Display API)":
        "{0}. Conexão da sua conta do TikTok (Login Kit / Display API)",
    "Si vous choisissez de connecter votre compte TikTok, nous utilisons l'API officielle de TikTok (Login Kit et Display API) avec votre consentement explicite. Nous accédons alors :":
        "Se você escolher conectar sua conta do TikTok, usamos a API oficial do TikTok (Login Kit e Display API) com seu consentimento explícito. Acessamos então:",
    "aux": "as",
    "informations de base de votre profil": "informações básicas do seu perfil",
    "(pseudo, photo, statistiques publiques de compte) — scope": "(usuário, foto, estatísticas públicas da conta) — scope",
    "à la": "a",
    "liste de vos vidéos publiées": "lista dos seus vídeos publicados",
    "et à leurs métriques publiques (vues, mentions j'aime, commentaires, partages) — scope":
        "e as métricas públicas deles (visualizações, curtidas, comentários, compartilhamentos) — scope",
    "Usage de ces données :": "Uso desses dados:",
    "elles servent exclusivement à vous fournir l'analyse de vos performances et à améliorer nos recommandations. Nous n'utilisons ces données qu'avec votre autorisation, nous ne les vendons jamais et ne les partageons avec aucun tiers à des fins publicitaires.":
        "servem exclusivamente para entregar a análise do seu desempenho e melhorar nossas recomendações. Só usamos esses dados com sua autorização, nunca os vendemos e não os compartilhamos com terceiros para fins publicitários.",
    "Vous pouvez": "Você pode",
    "révoquer cet accès à tout moment": "revogar esse acesso quando quiser",
    ", soit depuis les paramètres de votre compte TikTok, soit en nous contactant : nous supprimons alors les jetons d'accès et les données associées.":
        ", pelas configurações da sua conta do TikTok ou falando com a gente: aí apagamos os tokens de acesso e os dados ligados a eles.",
    "{0}. Finalités": "{0}. Finalidades",
    "Fournir le service d'analyse vidéo et de recommandations.":
        "Prestar o serviço de análise de vídeo e de recomendações.",
    "Gérer votre compte, vos quotas et votre abonnement.":
        "Gerenciar sua conta, suas cotas e sua assinatura.",
    "Améliorer la qualité de nos modèles via des statistiques":
        "Melhorar a qualidade dos nossos modelos com estatísticas",
    "anonymisées": "anonimizadas",
    "et agrégées.": "e agregadas.",
    "{0}. Partage des données": "{0}. Compartilhamento dos dados",
    "Nous faisons appel à des sous-traitants techniques strictement nécessaires au service :":
        "Recorremos a operadores técnicos estritamente necessários ao serviço:",
    "Hébergement": "Hospedagem",
    "(Render Services, Inc., États-Unis) : mise à disposition du site et de l'application.":
        "(Render Services, Inc., EUA): disponibilização do site e do aplicativo.",
    "Base de données": "Banco de dados",
    "(Supabase) : stockage de votre compte et de vos analyses.":
        "(Supabase): armazenamento da sua conta e das suas análises.",
    "Fournisseur d'IA": "Fornecedor de IA",
    ": traitement des vidéos que vous soumettez, le temps de l'analyse. Vos vidéos ne sont pas conservées par ce prestataire.":
        ": tratamento dos vídeos que você envia, durante a análise. Esse fornecedor não guarda seus vídeos.",
    "(Irlande / États-Unis) : encaissement des paiements et facturation. Nous n'avons jamais accès à vos données bancaires.":
        "(Irlanda / EUA): recebimento dos pagamentos e faturamento. Nunca temos acesso aos seus dados bancários.",
    "et notre service de messagerie : envoi des e-mails du service (bienvenue, résultat d'analyse, réinitialisation de mot de passe).":
        "e nosso serviço de e-mail: envio dos e-mails do serviço (boas-vindas, resultado de análise, redefinição de senha).",
    "(Functional Software, Inc., États-Unis) : détection des erreurs techniques, afin de les corriger. Ce service reçoit le message d'erreur et l'endroit du code concerné. Il est configuré pour":
        "(Functional Software, Inc., EUA): detecção de erros técnicos, para poder corrigi-los. Esse serviço recebe a mensagem de erro e o ponto do código envolvido. Está configurado para",
    "ne recevoir ni votre adresse e-mail, ni votre adresse IP, ni le contenu de vos requêtes":
        "não receber nem seu e-mail, nem seu IP, nem o conteúdo das suas requisições",
    "Certains de ces prestataires sont établis aux États-Unis. Les transferts correspondants sont encadrés par les clauses contractuelles types de la Commission européenne et, le cas échéant, par le cadre de protection des données UE–États-Unis.":
        "Alguns desses fornecedores ficam nos Estados Unidos. As transferências correspondentes seguem as cláusulas contratuais padrão da Comissão Europeia e, quando aplicável, o marco de proteção de dados UE–EUA.",
    "Aucune donnée n'est vendue. Les seules données transmises à des fins publicitaires sont celles décrites à l'article {0} (mesure de nos campagnes TikTok), et uniquement si vous y avez consenti.":
        "Nenhum dado é vendido. Os únicos dados transmitidos para fins publicitários são os descritos no artigo {0} (medição das nossas campanhas no TikTok), e só se você tiver consentido.",
    "{0}. Conservation": "{0}. Retenção",
    "Les données de compte sont conservées tant que votre compte est actif. Les jetons TikTok sont conservés tant que la connexion est active et supprimés à la déconnexion. Les statistiques anonymisées, n'étant pas rattachées à une personne, peuvent être conservées de façon agrégée.":
        "Os dados da conta ficam guardados enquanto sua conta estiver ativa. Os tokens do TikTok ficam enquanto a conexão estiver ativa e são apagados ao desconectar. As estatísticas anonimizadas, por não estarem ligadas a uma pessoa, podem ser mantidas de forma agregada.",
    "{0}. Vos droits (RGPD)": "{0}. Seus direitos (RGPD)",
    "Vous disposez d'un droit d'accès, de rectification, d'effacement, de portabilité et d'opposition. Pour exercer ces droits, écrivez à":
        "Você tem direito de acesso, correção, exclusão, portabilidade e oposição. Para exercê-los, escreva para",
    "{0}. Cookies et traceurs": "{0}. Cookies e rastreadores",
    "Les cookies techniques nécessaires au fonctionnement du site (session, préférences) sont déposés sans consentement, comme la réglementation le permet. Tous les autres traceurs sont soumis à votre accord préalable, finalité par finalité, via le bandeau affiché à votre première visite :":
        "Os cookies técnicos necessários ao funcionamento do site (sessão, preferências) são gravados sem consentimento, como a regulamentação permite. Todos os outros rastreadores dependem do seu acordo prévio, finalidade por finalidade, pelo banner exibido na sua primeira visita:",
    "Mesure d'audience": "Medição de audiência",
    "— Google Analytics, avec anonymisation de l'adresse IP. Sert à comprendre quelles pages sont utiles. Cookies":
        "— Google Analytics, com anonimização do IP. Serve para entender quais páginas são úteis. Cookies",
    "Publicité": "Publicidade",
    "— pixel TikTok Ads. Sert à mesurer quelles publicités TikTok amènent des inscriptions et des abonnements. Cookie":
        "— pixel do TikTok Ads. Serve para medir quais anúncios do TikTok trazem cadastros e assinaturas. Cookie",
    ". Lorsqu'un abonnement est payé, la conversion est également transmise à TikTok depuis nos serveurs : votre adresse e-mail n'est alors envoyée que sous forme d'empreinte chiffrée (SHA-{0}), jamais en clair, et uniquement si vous avez accepté cette finalité.":
        ". Quando uma assinatura é paga, a conversão também é enviada ao TikTok pelos nossos servidores: seu e-mail vai apenas como hash (SHA-{0}), nunca aberto, e só se você tiver aceitado essa finalidade.",
    "Tant que vous n'avez rien accepté, aucun de ces traceurs n'est chargé et aucune donnée ne part vers Google ou TikTok. Refuser est aussi simple qu'accepter : un seul clic, au même endroit.":
        "Enquanto você não aceitar nada, nenhum desses rastreadores é carregado e nenhum dado vai para o Google ou o TikTok. Recusar é tão simples quanto aceitar: um clique, no mesmo lugar.",
    "Vous pouvez modifier ou retirer votre choix à tout moment :": "Você pode mudar ou retirar sua escolha quando quiser:",
    "rouvrir mes préférences de cookies": "reabrir minhas preferências de cookies",
    ". Le retrait supprime les cookies déjà déposés.": ". A retirada apaga os cookies já gravados.",
    "TikTok Technology Limited et Google Ireland Limited agissent en qualité de responsables de traitement indépendants pour les données collectées via ces traceurs. Leurs politiques respectives :":
        "TikTok Technology Limited e Google Ireland Limited atuam como controladores independentes dos dados coletados por esses rastreadores. As políticas de cada uma:",
    "{0}. Contact": "{0}. Contato",
    "Voir les conditions d'utilisation →": "Ver os termos de uso →",
}

T_PRIVACY["en-ie"] = dict(T_PRIVACY["en"])
T_PRIVACY["es-mx"] = dict(T_PRIVACY["es"])
