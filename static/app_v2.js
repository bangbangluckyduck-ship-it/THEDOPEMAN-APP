/* ============================================================
   TikTok Shop Vidéo Analyzer — app_v2.js
   by Dope Ventures
   ============================================================ */

'use strict';

// ── CONSTANTES ────────────────────────────────────────────────
const STORAGE_KEY   = 'dv_history';
const USAGE_KEY     = 'dv_usage';
const USER_KEY      = 'dv_user';
const MAX_HISTORY   = 20;
const FREE_LIMIT    = 999; // limite levée pendant la beta

// ── I18N ─────────────────────────────────────────────────────
const LANG_KEY = 'dv_lang';
let currentLanguage = 'fr';

const TRANSLATIONS = {
  fr: {
    app_title:'TikTok Shop', app_title_hl:'Analyzer', app_sub:'by Dope Ventures',
    btn_connect:'Se connecter', btn_account:'Mon compte',
    server_waking:'⏳ Réveil du serveur en cours… (~30 sec)',
    pwa_title:'Ajouter à l\'écran d\'accueil', pwa_desc:'Accède à l\'application depuis ton téléphone', pwa_install:'Installer',
    freemium_title:'🎁 Gratuit jusqu\'au lancement officiel', freemium_count:'Analyses utilisées :',
    tab_analyze:'🎬 Analyser', tab_history:'📋 Historique',
    upload_title:'📹 Analyse ta vidéo TikTok Shop', upload_sub:'Importe ta vidéo',
    upload_hint:'Clique ici ou glisse ta vidéo', upload_fmt:'MP4, MOV',
    btn_analyze:'🚀 Analyser avec l\'IA',
    loading_extract:'🎬 Extraction des images et de l\'audio…', loading_server:'⏳ Réveil du serveur…', loading_ai:'🤖 Analyse IA en cours…',
    sec_quality:'🎯 Scores de qualité', sec_detection:'🔍 Détection automatique', viral_label:'Potentiel viral / 100',
    sec_forts:'✅ Points forts', sec_ameliorer:'⚠️ À améliorer',
    sec_advice:'💡 Conseils personnalisés', hook_best:'📌 Meilleure accroche pour ce produit', hook_ex:'3 exemples à tester :',
    advice_actions:'🎬 Actions prioritaires',
    sec_transcript:'🎤 Transcription audio', sec_verdict:'🏆 Verdict',
    sec_structure:'🔄 Structure de vente', sv_score_lbl:'📊 Score Structure Global', sv_improv:'💡 Améliorer le flux de vente',
    sec_conversion:'💰 Potentiel de conversion', pc_price_lbl:'Prix détecté', pc_cat_lbl:'Catégorie', pc_timing_lbl:'Évaluer à',
    score_accroche:'🎯 Accroche', score_discours:'🗣️ Discours', score_qualite_visuelle:'🎥 Qualité visuelle',
    score_visibilite_produit:'📦 Produit', score_call_to_action:'📢 Appel à l\'action',
    score_energie_dynamisme:'⚡ Énergie', score_credibilite_confiance:'🤝 Crédibilité',
    det_produit:'📦 Produit', det_prix:'💶 Prix estimé', det_hook_type:'🎯 Type d\'accroche', det_hook_force:'⚡ Force accroche',
    det_rentable:' ✓ rentable', det_optimiser:' — à optimiser',
    cat_economique:'🟢 Économique', cat_moyen:'🟡 Moyen', cat_premium:'🔴 Premium', cat_inconnu:'— Inconnu',
    delai_j7:'Jour 7', delai_j30:'Jour 30',
    cta_title:'🔄 Refais ta vidéo et reviens l\'analyser',
    cta_desc:'Applique les recommandations IA, re-filme, et analyse à nouveau pour mesurer tes progrès.',
    cta_btn:'Nouvelle analyse ➜',
    sec_export:'📥 Exporter', btn_pdf:'📄 Télécharger PDF', btn_save:'💾 Sauvegarder',
    hist_title:'📋 Historique des analyses', hist_empty:'📋 Aucune analyse pour l\'instant.',
    hist_clear:'Tout effacer', hist_confirm:'Effacer tout l\'historique ?',
    auth_title:'Se connecter', auth_email_lbl:'Adresse e-mail', auth_email_ph:'toi@exemple.com',
    auth_submit:'Continuer', auth_note:'Lien de connexion par e-mail — disponible lors du lancement.',
    score_global_lbl:'Score global',
    sv_accroche:'Accroche', sv_probleme:'Problème', sv_solution:'Solution', sv_produit:'Produit', sv_cta:'Appel action',
    err_timeout:'❌ Délai dépassé. Réessaie avec une vidéo plus courte.',
    saved_ok:'Sauvegardé !',
    footer:'© 2026 Dope Ventures · TTS Analyzer · Tous droits réservés',
    tb_title:'Vos données vous appartiennent', tb_sub:'restent EN LOCAL, jamais envoyées.', tb_link:'Détails →',
    ck_title:'🍪 Nous utilisons des cookies',
    ck_body:'Vos données vidéo restent TOUJOURS en local. Les cookies nous aident à améliorer votre expérience.',
    ck_link:'Politique de confidentialité', ck_accept:'Accepter tout', ck_reject:'Refuser tout',
    pm_title:'Votre confidentialité', pm_close:'Compris ! Fermer',
    footer_privacy:'Confidentialité', footer_cookies:'Cookies',
    pm_content:`<h3>✅ Vos données restent EN LOCAL</h3>
<p>Toutes vos analyses (scores, résultats, historique) sont stockées <strong>uniquement sur votre appareil</strong> via localStorage. Nous ne les récupérons jamais sur nos serveurs.</p>
<h3>🤖 Ce qui est envoyé à l'IA</h3>
<p>Lors d'une analyse, les <strong>images extraites</strong> de votre vidéo et l'<strong>audio transcrit</strong> sont transmis à Mistral AI pour générer les scores. Aucune donnée personnelle n'est incluse.</p>
<h3>🍪 Cookies utilisés</h3>
<ul>
  <li><strong>localStorage</strong> : vos analyses, historique, préférences de langue</li>
  <li><strong>cookieConsent</strong> : votre choix de consentement</li>
  <li><strong>Analytiques</strong> : trafic général (optionnel, anonyme)</li>
</ul>
<h3>📤 Export & suppression</h3>
<p>Vous pouvez exporter vos analyses en PDF à tout moment. Pour supprimer toutes vos données, effacez les données de site dans les réglages de votre navigateur.</p>
<h3>📧 Questions ?</h3>
<p>Contactez-nous : <a href="mailto:dopeventure44@gmail.com">dopeventure44@gmail.com</a></p>`,
    ios_title:'Installer sur iPhone / iPad',
    ios_s1:'Appuie sur <strong style="color:var(--text)">Partager</strong> ⎋ en bas de Safari',
    ios_s2:'Fais défiler et appuie sur <strong style="color:var(--text)">"Sur l\'écran d\'accueil"</strong>',
    ios_s3:'Appuie sur <strong style="color:var(--text)">"Ajouter"</strong> en haut à droite',
  },
  en: {
    app_title:'TikTok Shop', app_title_hl:'Analyzer', app_sub:'by Dope Ventures',
    btn_connect:'Sign in', btn_account:'My account',
    server_waking:'⏳ Server waking up… (~30 sec)',
    pwa_title:'Add to home screen', pwa_desc:'Access the app directly from your phone', pwa_install:'Install',
    freemium_title:'🎁 Free until official launch', freemium_count:'Analyses used:',
    tab_analyze:'🎬 Analyze', tab_history:'📋 History',
    upload_title:'📹 Analyze your TikTok Shop video', upload_sub:'Upload your video',
    upload_hint:'Click here or drag your video', upload_fmt:'MP4, MOV',
    btn_analyze:'🚀 Analyze with AI',
    loading_extract:'🎬 Extracting frames and audio…', loading_server:'⏳ Waking up server…', loading_ai:'🤖 AI analysis in progress…',
    sec_quality:'🎯 Quality scores', sec_detection:'🔍 Auto detection', viral_label:'Viral potential / 100',
    sec_forts:'✅ Strengths', sec_ameliorer:'⚠️ To improve',
    sec_advice:'💡 Personalized tips', hook_best:'📌 Best hook for this product', hook_ex:'3 examples to test:',
    advice_actions:'🎬 Priority actions',
    sec_transcript:'🎤 Audio transcript', sec_verdict:'🏆 Verdict',
    sec_structure:'🔄 Sales structure', sv_score_lbl:'📊 Overall Structure Score', sv_improv:'💡 Improve the sales flow',
    sec_conversion:'💰 Conversion potential', pc_price_lbl:'Detected price', pc_cat_lbl:'Category', pc_timing_lbl:'Evaluate at',
    score_accroche:'🎯 Hook', score_discours:'🗣️ Speech', score_qualite_visuelle:'🎥 Visual quality',
    score_visibilite_produit:'📦 Product', score_call_to_action:'📢 Call to action',
    score_energie_dynamisme:'⚡ Energy', score_credibilite_confiance:'🤝 Credibility',
    det_produit:'📦 Product', det_prix:'💶 Est. price', det_hook_type:'🎯 Hook type', det_hook_force:'⚡ Hook strength',
    det_rentable:' ✓ profitable', det_optimiser:' — to optimize',
    cat_economique:'🟢 Budget', cat_moyen:'🟡 Mid-range', cat_premium:'🔴 Premium', cat_inconnu:'— Unknown',
    delai_j7:'Day 7', delai_j30:'Day 30',
    cta_title:'🔄 Redo your video and come back to analyze',
    cta_desc:'Apply the AI recommendations, re-shoot, and analyze again to measure your progress.',
    cta_btn:'New analysis ➜',
    sec_export:'📥 Export', btn_pdf:'📄 Download PDF', btn_save:'💾 Save',
    hist_title:'📋 Analysis history', hist_empty:'📋 No analyses yet.',
    hist_clear:'Clear all', hist_confirm:'Clear all history?',
    auth_title:'Sign in', auth_email_lbl:'Email address', auth_email_ph:'you@example.com',
    auth_submit:'Continue', auth_note:'Magic link by email — available at launch.',
    score_global_lbl:'Overall score',
    sv_accroche:'Hook', sv_probleme:'Problem', sv_solution:'Solution', sv_produit:'Product', sv_cta:'Call to action',
    err_timeout:'❌ Timeout. Try again with a shorter video.',
    saved_ok:'Saved!',
    footer:'© 2026 Dope Ventures · TTS Analyzer · All rights reserved',
    tb_title:'Your data belongs to you', tb_sub:'stays LOCAL, never sent.', tb_link:'Details →',
    ck_title:'🍪 We use cookies',
    ck_body:'Your video data always stays local. Cookies help us improve your experience.',
    ck_link:'Privacy policy', ck_accept:'Accept all', ck_reject:'Decline',
    pm_title:'Your privacy', pm_close:'Got it! Close',
    footer_privacy:'Privacy', footer_cookies:'Cookies',
    pm_content:`<h3>✅ Your data stays LOCAL</h3>
<p>All your analyses (scores, results, history) are stored <strong>only on your device</strong> via localStorage. We never retrieve them on our servers.</p>
<h3>🤖 What is sent to the AI</h3>
<p>During an analysis, the <strong>extracted frames</strong> from your video and the <strong>transcribed audio</strong> are sent to Mistral AI to generate scores. No personal data is included.</p>
<h3>🍪 Cookies used</h3>
<ul>
  <li><strong>localStorage</strong>: your analyses, history, language preferences</li>
  <li><strong>cookieConsent</strong>: your consent choice</li>
  <li><strong>Analytics</strong>: general traffic (optional, anonymous)</li>
</ul>
<h3>📤 Export & deletion</h3>
<p>You can export your analyses as PDF at any time. To delete all your data, clear site data in your browser settings.</p>
<h3>📧 Questions?</h3>
<p>Contact us: <a href="mailto:dopeventure44@gmail.com">dopeventure44@gmail.com</a></p>`,
    ios_title:'Install on iPhone / iPad',
    ios_s1:'Tap <strong style="color:var(--text)">Share</strong> ⎋ at the bottom of Safari',
    ios_s2:'Scroll down and tap <strong style="color:var(--text)">"Add to Home Screen"</strong>',
    ios_s3:'Tap <strong style="color:var(--text)">"Add"</strong> in the top right corner',
  },
  'pt-br': {
    app_title:'TikTok Shop', app_title_hl:'Analyzer', app_sub:'by Dope Ventures',
    btn_connect:'Entrar', btn_account:'Minha conta',
    server_waking:'⏳ Servidor acordando… (~30 seg)',
    pwa_title:'Adicionar à tela inicial', pwa_desc:'Acesse o app do seu celular', pwa_install:'Instalar',
    freemium_title:'🎁 Gratuito até o lançamento oficial', freemium_count:'Análises usadas:',
    tab_analyze:'🎬 Analisar', tab_history:'📋 Histórico',
    upload_title:'📹 Analise seu vídeo TikTok Shop', upload_sub:'Envie seu vídeo',
    upload_hint:'Clique aqui ou arraste seu vídeo', upload_fmt:'MP4, MOV',
    btn_analyze:'🚀 Analisar com IA',
    loading_extract:'🎬 Extraindo imagens e áudio…', loading_server:'⏳ Iniciando servidor…', loading_ai:'🤖 Análise de IA em andamento…',
    sec_quality:'🎯 Pontuações de qualidade', sec_detection:'🔍 Detecção automática', viral_label:'Potencial viral / 100',
    sec_forts:'✅ Pontos fortes', sec_ameliorer:'⚠️ A melhorar',
    sec_advice:'💡 Dicas personalizadas', hook_best:'📌 Melhor gancho para este produto', hook_ex:'3 exemplos para testar:',
    advice_actions:'🎬 Ações prioritárias',
    sec_transcript:'🎤 Transcrição de áudio', sec_verdict:'🏆 Veredicto',
    sec_structure:'🔄 Estrutura de vendas', sv_score_lbl:'📊 Pontuação Global da Estrutura', sv_improv:'💡 Melhorar o fluxo de vendas',
    sec_conversion:'💰 Potencial de conversão', pc_price_lbl:'Preço detectado', pc_cat_lbl:'Categoria', pc_timing_lbl:'Avaliar em',
    score_accroche:'🎯 Gancho', score_discours:'🗣️ Discurso', score_qualite_visuelle:'🎥 Qualidade visual',
    score_visibilite_produit:'📦 Produto', score_call_to_action:'📢 Chamada para ação',
    score_energie_dynamisme:'⚡ Energia', score_credibilite_confiance:'🤝 Credibilidade',
    det_produit:'📦 Produto', det_prix:'💶 Preço est.', det_hook_type:'🎯 Tipo de gancho', det_hook_force:'⚡ Força do gancho',
    det_rentable:' ✓ rentável', det_optimiser:' — a otimizar',
    cat_economique:'🟢 Econômico', cat_moyen:'🟡 Médio', cat_premium:'🔴 Premium', cat_inconnu:'— Desconhecido',
    delai_j7:'Dia 7', delai_j30:'Dia 30',
    cta_title:'🔄 Refaça seu vídeo e volte para analisar',
    cta_desc:'Aplique as recomendações de IA, regrave e analise novamente para medir seu progresso.',
    cta_btn:'Nova análise ➜',
    sec_export:'📥 Exportar', btn_pdf:'📄 Baixar PDF', btn_save:'💾 Salvar',
    hist_title:'📋 Histórico de análises', hist_empty:'📋 Nenhuma análise ainda.',
    hist_clear:'Limpar tudo', hist_confirm:'Limpar todo o histórico?',
    auth_title:'Entrar', auth_email_lbl:'E-mail', auth_email_ph:'voce@exemplo.com',
    auth_submit:'Continuar', auth_note:'Link mágico por e-mail — disponível no lançamento.',
    score_global_lbl:'Pontuação geral',
    sv_accroche:'Gancho', sv_probleme:'Problema', sv_solution:'Solução', sv_produit:'Produto', sv_cta:'Chamada',
    err_timeout:'❌ Tempo esgotado. Tente com um vídeo mais curto.',
    saved_ok:'Salvo!',
    footer:'© 2026 Dope Ventures · TTS Analyzer · Todos os direitos reservados',
    tb_title:'Seus dados são seus', tb_sub:'ficam em LOCAL, nunca enviados.', tb_link:'Detalhes →',
    ck_title:'🍪 Usamos cookies', ck_body:'Seus dados de vídeo ficam SEMPRE em local. Os cookies nos ajudam a melhorar sua experiência.', ck_link:'Política de privacidade', ck_accept:'Aceitar tudo', ck_reject:'Recusar',
    pm_title:'Sua privacidade', pm_close:'Entendido! Fechar',
    footer_privacy:'Privacidade', footer_cookies:'Cookies',
    pm_content:`<h3>✅ Seus dados ficam EM LOCAL</h3><p>Todas as suas análises ficam <strong>apenas no seu dispositivo</strong>. Nunca as recuperamos em nossos servidores.</p><h3>🍪 Cookies usados</h3><ul><li>localStorage: análises, histórico, idioma</li><li>cookieConsent: sua escolha</li></ul><h3>📧 Dúvidas?</h3><p><a href="mailto:dopeventure44@gmail.com">dopeventure44@gmail.com</a></p>`,
    ios_title:'Instalar no iPhone / iPad',
    ios_s1:'Toque em <strong style="color:var(--text)">Compartilhar</strong> ⎋ na parte inferior do Safari',
    ios_s2:'Role para baixo e toque em <strong style="color:var(--text)">"Tela de Início"</strong>',
    ios_s3:'Toque em <strong style="color:var(--text)">"Adicionar"</strong> no canto superior direito',
  },
  es: {
    app_title:'TikTok Shop', app_title_hl:'Analyzer', app_sub:'by Dope Ventures',
    btn_connect:'Iniciar sesión', btn_account:'Mi cuenta',
    server_waking:'⏳ Iniciando servidor… (~30 seg)',
    pwa_title:'Añadir a pantalla de inicio', pwa_desc:'Accede a la app desde tu teléfono', pwa_install:'Instalar',
    freemium_title:'🎁 Gratuito hasta el lanzamiento oficial', freemium_count:'Análisis utilizados:',
    tab_analyze:'🎬 Analizar', tab_history:'📋 Historial',
    upload_title:'📹 Analiza tu vídeo TikTok Shop', upload_sub:'Sube tu vídeo',
    upload_hint:'Haz clic aquí o arrastra tu vídeo', upload_fmt:'MP4, MOV',
    btn_analyze:'🚀 Analizar con IA',
    loading_extract:'🎬 Extrayendo imágenes y audio…', loading_server:'⏳ Iniciando servidor…', loading_ai:'🤖 Análisis de IA en curso…',
    sec_quality:'🎯 Puntuaciones de calidad', sec_detection:'🔍 Detección automática', viral_label:'Potencial viral / 100',
    sec_forts:'✅ Puntos fuertes', sec_ameliorer:'⚠️ A mejorar',
    sec_advice:'💡 Consejos personalizados', hook_best:'📌 Mejor gancho para este producto', hook_ex:'3 ejemplos para probar:',
    advice_actions:'🎬 Acciones prioritarias',
    sec_transcript:'🎤 Transcripción de audio', sec_verdict:'🏆 Veredicto',
    sec_structure:'🔄 Estructura de venta', sv_score_lbl:'📊 Puntuación Global Estructura', sv_improv:'💡 Mejorar el flujo de ventas',
    sec_conversion:'💰 Potencial de conversión', pc_price_lbl:'Precio detectado', pc_cat_lbl:'Categoría', pc_timing_lbl:'Evaluar en',
    score_accroche:'🎯 Gancho', score_discours:'🗣️ Discurso', score_qualite_visuelle:'🎥 Calidad visual',
    score_visibilite_produit:'📦 Producto', score_call_to_action:'📢 Llamada a la acción',
    score_energie_dynamisme:'⚡ Energía', score_credibilite_confiance:'🤝 Credibilidad',
    det_produit:'📦 Producto', det_prix:'💶 Precio est.', det_hook_type:'🎯 Tipo de gancho', det_hook_force:'⚡ Fuerza del gancho',
    det_rentable:' ✓ rentable', det_optimiser:' — a optimizar',
    cat_economique:'🟢 Económico', cat_moyen:'🟡 Medio', cat_premium:'🔴 Premium', cat_inconnu:'— Desconocido',
    delai_j7:'Día 7', delai_j30:'Día 30',
    cta_title:'🔄 Rehaz tu vídeo y vuelve a analizarlo',
    cta_desc:'Aplica las recomendaciones de IA, vuelve a grabar y analiza de nuevo para medir tu progreso.',
    cta_btn:'Nuevo análisis ➜',
    sec_export:'📥 Exportar', btn_pdf:'📄 Descargar PDF', btn_save:'💾 Guardar',
    hist_title:'📋 Historial de análisis', hist_empty:'📋 Ningún análisis todavía.',
    hist_clear:'Borrar todo', hist_confirm:'¿Borrar todo el historial?',
    auth_title:'Iniciar sesión', auth_email_lbl:'Correo electrónico', auth_email_ph:'tu@ejemplo.com',
    auth_submit:'Continuar', auth_note:'Enlace mágico por correo — disponible en el lanzamiento.',
    score_global_lbl:'Puntuación global',
    sv_accroche:'Gancho', sv_probleme:'Problema', sv_solution:'Solución', sv_produit:'Producto', sv_cta:'Llamada',
    err_timeout:'❌ Tiempo agotado. Intenta con un vídeo más corto.',
    saved_ok:'¡Guardado!',
    footer:'© 2026 Dope Ventures · TTS Analyzer · Todos los derechos reservados',
    tb_title:'Tus datos son tuyos', tb_sub:'se quedan EN LOCAL, nunca se envían.', tb_link:'Detalles →',
    ck_title:'🍪 Usamos cookies', ck_body:'Tus datos de vídeo siempre permanecen en local. Las cookies nos ayudan a mejorar tu experiencia.', ck_link:'Política de privacidad', ck_accept:'Aceptar todo', ck_reject:'Rechazar',
    pm_title:'Tu privacidad', pm_close:'¡Entendido! Cerrar',
    footer_privacy:'Privacidad', footer_cookies:'Cookies',
    pm_content:`<h3>✅ Tus datos EN LOCAL</h3><p>Todos tus análisis se almacenan <strong>solo en tu dispositivo</strong>. Nunca los recuperamos en nuestros servidores.</p><h3>🍪 Cookies usadas</h3><ul><li>localStorage: análisis, historial, idioma</li><li>cookieConsent: tu elección</li></ul><h3>📧 ¿Preguntas?</h3><p><a href="mailto:dopeventure44@gmail.com">dopeventure44@gmail.com</a></p>`,
    ios_title:'Instalar en iPhone / iPad',
    ios_s1:'Pulsa <strong style="color:var(--text)">Compartir</strong> ⎋ en la parte inferior de Safari',
    ios_s2:'Desplázate y pulsa <strong style="color:var(--text)">"En pantalla de inicio"</strong>',
    ios_s3:'Pulsa <strong style="color:var(--text)">"Añadir"</strong> arriba a la derecha',
  },
  it: {
    app_title:'TikTok Shop', app_title_hl:'Analyzer', app_sub:'by Dope Ventures',
    btn_connect:'Accedi', btn_account:'Il mio account',
    server_waking:'⏳ Avvio del server… (~30 sec)',
    pwa_title:'Aggiungi alla schermata iniziale', pwa_desc:'Accedi all\'app dal tuo telefono', pwa_install:'Installa',
    freemium_title:'🎁 Gratuito fino al lancio ufficiale', freemium_count:'Analisi utilizzate:',
    tab_analyze:'🎬 Analizza', tab_history:'📋 Cronologia',
    upload_title:'📹 Analizza il tuo video TikTok Shop', upload_sub:'Carica il tuo video',
    upload_hint:'Clicca qui o trascina il tuo video', upload_fmt:'MP4, MOV',
    btn_analyze:'🚀 Analizza con l\'IA',
    loading_extract:'🎬 Estrazione immagini e audio…', loading_server:'⏳ Avvio server…', loading_ai:'🤖 Analisi IA in corso…',
    sec_quality:'🎯 Punteggi di qualità', sec_detection:'🔍 Rilevamento automatico', viral_label:'Potenziale virale / 100',
    sec_forts:'✅ Punti di forza', sec_ameliorer:'⚠️ Da migliorare',
    sec_advice:'💡 Consigli personalizzati', hook_best:'📌 Miglior gancio per questo prodotto', hook_ex:'3 esempi da testare:',
    advice_actions:'🎬 Azioni prioritarie',
    sec_transcript:'🎤 Trascrizione audio', sec_verdict:'🏆 Verdetto',
    sec_structure:'🔄 Struttura di vendita', sv_score_lbl:'📊 Punteggio Globale Struttura', sv_improv:'💡 Migliorare il flusso di vendita',
    sec_conversion:'💰 Potenziale di conversione', pc_price_lbl:'Prezzo rilevato', pc_cat_lbl:'Categoria', pc_timing_lbl:'Valutare a',
    score_accroche:'🎯 Gancio', score_discours:'🗣️ Discorso', score_qualite_visuelle:'🎥 Qualità visiva',
    score_visibilite_produit:'📦 Prodotto', score_call_to_action:'📢 Chiamata all\'azione',
    score_energie_dynamisme:'⚡ Energia', score_credibilite_confiance:'🤝 Credibilità',
    det_produit:'📦 Prodotto', det_prix:'💶 Prezzo est.', det_hook_type:'🎯 Tipo di gancio', det_hook_force:'⚡ Forza gancio',
    det_rentable:' ✓ redditizio', det_optimiser:' — da ottimizzare',
    cat_economique:'🟢 Economico', cat_moyen:'🟡 Medio', cat_premium:'🔴 Premium', cat_inconnu:'— Sconosciuto',
    delai_j7:'Giorno 7', delai_j30:'Giorno 30',
    cta_title:'🔄 Rifai il tuo video e torna ad analizzarlo',
    cta_desc:'Applica i consigli dell\'IA, riprendi e analizza di nuovo per misurare i tuoi progressi.',
    cta_btn:'Nuova analisi ➜',
    sec_export:'📥 Esporta', btn_pdf:'📄 Scarica PDF', btn_save:'💾 Salva',
    hist_title:'📋 Cronologia delle analisi', hist_empty:'📋 Nessuna analisi per ora.',
    hist_clear:'Cancella tutto', hist_confirm:'Cancellare tutta la cronologia?',
    auth_title:'Accedi', auth_email_lbl:'Indirizzo email', auth_email_ph:'tu@esempio.com',
    auth_submit:'Continua', auth_note:'Link magico via email — disponibile al lancio.',
    score_global_lbl:'Punteggio globale',
    sv_accroche:'Gancio', sv_probleme:'Problema', sv_solution:'Soluzione', sv_produit:'Prodotto', sv_cta:'Azione',
    err_timeout:'❌ Timeout. Riprova con un video più breve.',
    saved_ok:'Salvato!',
    footer:'© 2026 Dope Ventures · TTS Analyzer · Tutti i diritti riservati',
    tb_title:'I tuoi dati sono tuoi', tb_sub:'restano IN LOCALE, mai inviati.', tb_link:'Dettagli →',
    ck_title:'🍪 Usiamo i cookie', ck_body:'I tuoi dati video restano SEMPRE in locale. I cookie ci aiutano a migliorare la tua esperienza.', ck_link:'Privacy policy', ck_accept:'Accetta tutto', ck_reject:'Rifiuta',
    pm_title:'La tua privacy', pm_close:'Capito! Chiudi',
    footer_privacy:'Privacy', footer_cookies:'Cookie',
    pm_content:`<h3>✅ I tuoi dati IN LOCALE</h3><p>Tutte le tue analisi sono memorizzate <strong>solo sul tuo dispositivo</strong>. Non le recuperiamo mai sui nostri server.</p><h3>🍪 Cookie usati</h3><ul><li>localStorage: analisi, cronologia, lingua</li><li>cookieConsent: la tua scelta</li></ul><h3>📧 Domande?</h3><p><a href="mailto:dopeventure44@gmail.com">dopeventure44@gmail.com</a></p>`,
    ios_title:'Installa su iPhone / iPad',
    ios_s1:'Tocca <strong style="color:var(--text)">Condividi</strong> ⎋ in fondo a Safari',
    ios_s2:'Scorri e tocca <strong style="color:var(--text)">"Aggiungi a Home"</strong>',
    ios_s3:'Tocca <strong style="color:var(--text)">"Aggiungi"</strong> in alto a destra',
  },
  de: {
    app_title:'TikTok Shop', app_title_hl:'Analyzer', app_sub:'by Dope Ventures',
    btn_connect:'Anmelden', btn_account:'Mein Konto',
    server_waking:'⏳ Server wird gestartet… (~30 Sek)',
    pwa_title:'Zum Startbildschirm hinzufügen', pwa_desc:'Greife direkt vom Telefon auf die App zu', pwa_install:'Installieren',
    freemium_title:'🎁 Kostenlos bis zum offiziellen Launch', freemium_count:'Analysen verwendet:',
    tab_analyze:'🎬 Analysieren', tab_history:'📋 Verlauf',
    upload_title:'📹 Analysiere dein TikTok Shop Video', upload_sub:'Lade dein Video hoch',
    upload_hint:'Klick hier oder ziehe dein Video rein', upload_fmt:'MP4, MOV',
    btn_analyze:'🚀 Mit KI analysieren',
    loading_extract:'🎬 Bilder und Audio werden extrahiert…', loading_server:'⏳ Server wird gestartet…', loading_ai:'🤖 KI-Analyse läuft…',
    sec_quality:'🎯 Qualitätsbewertungen', sec_detection:'🔍 Automatische Erkennung', viral_label:'Virales Potenzial / 100',
    sec_forts:'✅ Stärken', sec_ameliorer:'⚠️ Zu verbessern',
    sec_advice:'💡 Persönliche Tipps', hook_best:'📌 Bester Hook für dieses Produkt', hook_ex:'3 Beispiele zum Testen:',
    advice_actions:'🎬 Prioritätsaktionen',
    sec_transcript:'🎤 Audio-Transkription', sec_verdict:'🏆 Fazit',
    sec_structure:'🔄 Verkaufsstruktur', sv_score_lbl:'📊 Gesamtpunktzahl Struktur', sv_improv:'💡 Verkaufsfluss verbessern',
    sec_conversion:'💰 Konversionspotenzial', pc_price_lbl:'Erkannter Preis', pc_cat_lbl:'Kategorie', pc_timing_lbl:'Auswerten am',
    score_accroche:'🎯 Hook', score_discours:'🗣️ Sprache', score_qualite_visuelle:'🎥 Bildqualität',
    score_visibilite_produit:'📦 Produkt', score_call_to_action:'📢 Handlungsaufforderung',
    score_energie_dynamisme:'⚡ Energie', score_credibilite_confiance:'🤝 Glaubwürdigkeit',
    det_produit:'📦 Produkt', det_prix:'💶 Geschätzter Preis', det_hook_type:'🎯 Hook-Typ', det_hook_force:'⚡ Hook-Stärke',
    det_rentable:' ✓ rentabel', det_optimiser:' — zu optimieren',
    cat_economique:'🟢 Günstig', cat_moyen:'🟡 Mittelklasse', cat_premium:'🔴 Premium', cat_inconnu:'— Unbekannt',
    delai_j7:'Tag 7', delai_j30:'Tag 30',
    cta_title:'🔄 Drehe dein Video neu und analysiere es erneut',
    cta_desc:'Wende die KI-Empfehlungen an, drehe neu und analysiere wieder, um deinen Fortschritt zu messen.',
    cta_btn:'Neue Analyse ➜',
    sec_export:'📥 Exportieren', btn_pdf:'📄 PDF herunterladen', btn_save:'💾 Speichern',
    hist_title:'📋 Analyseverlauf', hist_empty:'📋 Noch keine Analysen.',
    hist_clear:'Alles löschen', hist_confirm:'Gesamten Verlauf löschen?',
    auth_title:'Anmelden', auth_email_lbl:'E-Mail-Adresse', auth_email_ph:'du@beispiel.de',
    auth_submit:'Weiter', auth_note:'Magic Link per E-Mail — beim Launch verfügbar.',
    score_global_lbl:'Gesamtpunktzahl',
    sv_accroche:'Hook', sv_probleme:'Problem', sv_solution:'Lösung', sv_produit:'Produkt', sv_cta:'Aktion',
    err_timeout:'❌ Zeitüberschreitung. Versuche mit einem kürzeren Video.',
    saved_ok:'Gespeichert!',
    footer:'© 2026 Dope Ventures · TTS Analyzer · Alle Rechte vorbehalten',
    tb_title:'Deine Daten gehören dir', tb_sub:'bleiben LOKAL, werden nie gesendet.', tb_link:'Details →',
    ck_title:'🍪 Wir verwenden Cookies', ck_body:'Deine Videodaten bleiben IMMER lokal. Cookies helfen uns, deine Erfahrung zu verbessern.', ck_link:'Datenschutz', ck_accept:'Alle akzeptieren', ck_reject:'Ablehnen',
    pm_title:'Dein Datenschutz', pm_close:'Verstanden! Schließen',
    footer_privacy:'Datenschutz', footer_cookies:'Cookies',
    pm_content:`<h3>✅ Deine Daten LOKAL</h3><p>Alle deine Analysen werden <strong>nur auf deinem Gerät</strong> gespeichert. Wir rufen sie nie auf unseren Servern ab.</p><h3>🍪 Verwendete Cookies</h3><ul><li>localStorage: Analysen, Verlauf, Sprache</li><li>cookieConsent: deine Wahl</li></ul><h3>📧 Fragen?</h3><p><a href="mailto:dopeventure44@gmail.com">dopeventure44@gmail.com</a></p>`,
    ios_title:'Auf iPhone / iPad installieren',
    ios_s1:'Tippe auf <strong style="color:var(--text)">Teilen</strong> ⎋ unten in Safari',
    ios_s2:'Scrolle und tippe auf <strong style="color:var(--text)">"Zum Home-Bildschirm"</strong>',
    ios_s3:'Tippe oben rechts auf <strong style="color:var(--text)">"Hinzufügen"</strong>',
  },
};

function t(key) {
  const lang = TRANSLATIONS[currentLanguage] || TRANSLATIONS.fr;
  return lang[key] ?? TRANSLATIONS.fr[key] ?? key;
}

function detectLanguage() {
  const saved = localStorage.getItem(LANG_KEY);
  if (saved && TRANSLATIONS[saved]) { currentLanguage = saved; return; }
  const nav = (navigator.language || navigator.userLanguage || 'fr').toLowerCase();
  if (nav.startsWith('pt'))      currentLanguage = 'pt-br';
  else if (nav.startsWith('es')) currentLanguage = 'es';
  else if (nav.startsWith('it')) currentLanguage = 'it';
  else if (nav.startsWith('de')) currentLanguage = 'de';
  else if (nav.startsWith('en')) currentLanguage = 'en';
  else                           currentLanguage = 'fr';
}

function setLanguage(lang) {
  if (!TRANSLATIONS[lang]) return;
  currentLanguage = lang;
  localStorage.setItem(LANG_KEY, lang);
  applyTranslations();
  const sel = document.getElementById('lang-select');
  if (sel) sel.value = lang;
}

function applyTranslations() {
  document.querySelectorAll('[data-i18n]').forEach(el => {
    el.textContent = t(el.dataset.i18n);
  });
  document.querySelectorAll('[data-i18n-ph]').forEach(el => {
    el.placeholder = t(el.dataset.i18nPh);
  });
  // Dynamic labels that need innerHTML update
  const fTitle = document.getElementById('freemium-title');
  if (fTitle) fTitle.textContent = t('freemium_title');
  const fCount = document.getElementById('freemium-count-label');
  if (fCount) fCount.textContent = t('freemium_count');
}

function getLabels() {
  return {
    accroche:              t('score_accroche'),
    discours:              t('score_discours'),
    qualite_visuelle:      t('score_qualite_visuelle'),
    visibilite_produit:    t('score_visibilite_produit'),
    call_to_action:        t('score_call_to_action'),
    energie_dynamisme:     t('score_energie_dynamisme'),
    credibilite_confiance: t('score_credibilite_confiance'),
  };
}

// ── ÉTAT GLOBAL ───────────────────────────────────────────────
let selectedFile   = null;
let serverReady    = false;
let currentData    = null;
let currentFilename = '';
let deferredPrompt = null;

// ── INIT ──────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  detectLanguage();
  applyTranslations();
  wakeServer();
  updateUsageCounter();
  updateHistoryBadge();
  restoreUser();

  // Sélecteur de langue
  const sel = document.getElementById('lang-select');
  if (sel) {
    sel.value = currentLanguage;
    sel.addEventListener('change', e => setLanguage(e.target.value));
  }

  // PWA
  if ('serviceWorker' in navigator) navigator.serviceWorker.register('/static/sw.js');
  window.addEventListener('beforeinstallprompt', e => {
    e.preventDefault(); deferredPrompt = e;
    document.getElementById('pwa-banner').style.display = 'flex';
  });

  // Détection iOS : afficher guide d'installation si pas déjà installé
  const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent) ||
    (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
  const isStandalone = window.navigator.standalone === true ||
    window.matchMedia('(display-mode: standalone)').matches;
  const iosBannerDismissed = localStorage.getItem('ios_banner_dismissed');

  if (isIOS && !isStandalone && !iosBannerDismissed) {
    const banner = document.getElementById('ios-banner');
    if (banner) {
      // Mettre à jour les textes avec la langue courante
      document.getElementById('ios-banner-title').textContent = t('ios_title');
      const steps = document.getElementById('ios-banner-steps');
      steps.innerHTML = `<li>${t('ios_s1')}</li><li>${t('ios_s2')}</li><li>${t('ios_s3')}</li>`;
      banner.style.display = 'block';
      // Fermeture mémorisée
      banner.querySelector('button').addEventListener('click', () => {
        localStorage.setItem('ios_banner_dismissed', '1');
      });
    }
  }
});

// ── SERVER WAKE ───────────────────────────────────────────────
async function wakeServer() {
  const status = document.getElementById('server-status');
  try {
    const res = await fetch('/health', { signal: AbortSignal.timeout(5000) });
    if (res.ok) { serverReady = true; return; }
  } catch {}
  status.style.display = 'block';
  for (let i = 0; i < 20; i++) {
    await new Promise(r => setTimeout(r, 3000));
    try {
      const res = await fetch('/health', { signal: AbortSignal.timeout(5000) });
      if (res.ok) { serverReady = true; status.style.display = 'none'; return; }
    } catch {}
  }
  status.textContent = '❌ Serveur indisponible. Rafraîchis la page.';
}

// ── TABS ──────────────────────────────────────────────────────
function switchTab(tab) {
  document.getElementById('tab-analyze-content').style.display  = tab === 'analyze'  ? 'block' : 'none';
  document.getElementById('tab-history-content').style.display  = tab === 'history'  ? 'block' : 'none';
  document.getElementById('tab-analyze').classList.toggle('active',  tab === 'analyze');
  document.getElementById('tab-history').classList.toggle('active',  tab === 'history');
  if (tab === 'history') renderHistory();
}

// ── UPLOAD ────────────────────────────────────────────────────
const uploadArea = document.getElementById('upload-area');
const fileInput  = document.getElementById('video-file');

uploadArea.addEventListener('click', () => fileInput.click());
fileInput.addEventListener('change', e => { if (e.target.files[0]) setFile(e.target.files[0]); });
uploadArea.addEventListener('dragover',  e => { e.preventDefault(); uploadArea.classList.add('active'); });
uploadArea.addEventListener('dragleave', () => uploadArea.classList.remove('active'));
uploadArea.addEventListener('drop', e => {
  e.preventDefault(); uploadArea.classList.remove('active');
  const f = e.dataTransfer.files[0];
  if (f && f.type.startsWith('video/')) setFile(f);
});

function setFile(f) {
  selectedFile = f;
  document.getElementById('error-box').style.display = 'none';
  const tag = document.getElementById('file-tag');
  tag.textContent = `📎 ${f.name} (${(f.size / 1024 / 1024).toFixed(1)} Mo)`;
  tag.style.display = 'block';
  document.getElementById('analyze-btn').disabled = false;
}

document.getElementById('analyze-btn').addEventListener('click', analyzeVideo);

// ── FRAME EXTRACTION ──────────────────────────────────────────
async function extractFrames(file, numFrames = 6) {
  return new Promise((resolve, reject) => {
    const video = document.createElement('video');
    video.muted = true; video.playsInline = true;
    const url = URL.createObjectURL(file);
    video.src = url;
    video.onloadedmetadata = async () => {
      const dur = video.duration;
      const W = 480;
      const H = Math.round(W * video.videoHeight / Math.max(video.videoWidth, 1)) || W;
      const canvas = document.createElement('canvas');
      canvas.width = W; canvas.height = H;
      const ctx = canvas.getContext('2d');
      // 1re image : aléatoire entre 1-3s
      const first = 1 + Math.random() * Math.min(2, Math.max(0, dur - 1.1));
      const ts = [first];
      for (let i = 1; i < numFrames; i++)
        ts.push(Math.random() * Math.max(dur - 0.1, 0.1));
      ts.sort((a, b) => a - b);
      const frames = [];
      for (const t of ts) {
        await new Promise(r => {
          video.currentTime = t;
          video.onseeked = () => {
            ctx.drawImage(video, 0, 0, W, H);
            frames.push(canvas.toDataURL('image/jpeg', 0.8).split(',')[1]);
            r();
          };
        });
      }
      URL.revokeObjectURL(url);
      resolve(frames);
    };
    video.onerror = () => { URL.revokeObjectURL(url); reject(new Error('Vidéo illisible sur ce navigateur')); };
  });
}

// ── AUDIO EXTRACTION ─────────────────────────────────────────
async function extractAudio(file) {
  try {
    const arrayBuffer = await file.arrayBuffer();
    const tmpCtx = new (window.AudioContext || window.webkitAudioContext)();
    const audioBuffer = await tmpCtx.decodeAudioData(arrayBuffer);
    await tmpCtx.close();
    const SR = 16000;
    const offline = new OfflineAudioContext(1, Math.ceil(audioBuffer.duration * SR), SR);
    const src = offline.createBufferSource();
    src.buffer = audioBuffer; src.connect(offline.destination); src.start();
    const rendered = await offline.startRendering();
    const samples  = rendered.getChannelData(0);
    const buf = new ArrayBuffer(44 + samples.length * 2);
    const v   = new DataView(buf);
    const str = (o, s) => { for (let i = 0; i < s.length; i++) v.setUint8(o + i, s.charCodeAt(i)); };
    str(0,'RIFF'); v.setUint32(4, 36 + samples.length * 2, true);
    str(8,'WAVE'); str(12,'fmt '); v.setUint32(16,16,true);
    v.setUint16(20,1,true); v.setUint16(22,1,true);
    v.setUint32(24,SR,true); v.setUint32(28,SR*2,true);
    v.setUint16(32,2,true); v.setUint16(34,16,true);
    str(36,'data'); v.setUint32(40, samples.length * 2, true);
    for (let i = 0; i < samples.length; i++) {
      const s = Math.max(-1, Math.min(1, samples[i]));
      v.setInt16(44 + i * 2, s < 0 ? s * 0x8000 : s * 0x7FFF, true);
    }
    return new Blob([buf], { type: 'audio/wav' });
  } catch { return null; }
}

// ── MAIN FLOW ────────────────────────────────────────────────
async function analyzeVideo() {
  if (!selectedFile) return;

  document.getElementById('error-box').style.display      = 'none';
  document.getElementById('upload-section').style.display  = 'none';
  document.getElementById('loading-section').style.display = 'block';
  setLoadingText(t('loading_extract'));

  if (!serverReady) {
    setLoadingText(t('loading_server'));
    for (let i = 0; i < 15 && !serverReady; i++)
      await new Promise(r => setTimeout(r, 2000));
  }

  try {
    const [frames, audioBlob] = await Promise.all([
      extractFrames(selectedFile, 6),
      extractAudio(selectedFile),
    ]);

    setLoadingText(t('loading_ai'));
    const fd = new FormData();
    fd.append('frames', JSON.stringify(frames));
    if (audioBlob) fd.append('audio', audioBlob, 'audio.wav');

    const ctrl    = new AbortController();
    const timer   = setTimeout(() => ctrl.abort(), 100000);
    const headers = {};
    const email   = localStorage.getItem(USER_KEY);
    if (email) headers['Authorization'] = `Bearer ${email}`;
    const res = await fetch('/analyze', { method: 'POST', body: fd, signal: ctrl.signal, headers });
    clearTimeout(timer);

    if (!res.ok) throw new Error((await res.json()).detail || 'Erreur serveur');

    const data = await res.json();
    currentData     = data;
    currentFilename = selectedFile.name;

    // Sync le compteur avec la réponse serveur si disponible
    if (data.usage?.used !== undefined) {
      localStorage.setItem(USAGE_KEY, data.usage.used);
      updateUsageCounter();
    } else {
      incrementUsage();
    }
    saveToHistory(data, currentFilename);
    showResults(data);

  } catch (e) {
    document.getElementById('loading-section').style.display = 'none';
    document.getElementById('upload-section').style.display  = 'block';
    showError(e.name === 'AbortError' ? t('err_timeout') : '❌ ' + e.message);
  }
}

function setLoadingText(txt) {
  document.getElementById('loading-text').textContent = txt;
}
function showError(msg) {
  const eb = document.getElementById('error-box');
  eb.textContent = msg; eb.style.display = 'block';
}

// ── SCORE COLORS ─────────────────────────────────────────────
function scoreColor(n) {
  if (n >= 7) return '#00e5a0';
  if (n >= 5) return '#ffc107';
  return '#ff4757';
}

// ── SHOW RESULTS ─────────────────────────────────────────────
function showResults(d) {
  document.getElementById('loading-section').style.display  = 'none';
  document.getElementById('results-section').style.display  = 'block';

  // Score global
  document.getElementById('score-global').textContent = d.score_global ?? '—';

  // Grille scores
  const grid = document.getElementById('scores-grid');
  grid.innerHTML = '';
  const LABELS = getLabels();
  if (d.scores) {
    Object.entries(d.scores).forEach(([k, v]) => {
      const n   = v.note ?? 0;
      const col = scoreColor(n);
      const card = document.createElement('div');
      card.className = 'score-card';
      card.innerHTML = `
        <div class="score-label">${LABELS[k] || k}</div>
        <div class="score-value" style="color:${col}">${n}<span style="font-size:16px;color:var(--muted)">/10</span></div>
        <div class="score-bar"><div class="score-bar-fill" style="width:0%;background:${col}"></div></div>
        <div class="score-comment">${v.commentaire || ''}</div>
      `;
      grid.appendChild(card);
      requestAnimationFrame(() => requestAnimationFrame(() => {
        card.querySelector('.score-bar-fill').style.width = (n * 10) + '%';
      }));
    });
  }

  // Détection
  const detGrid = document.getElementById('detection-grid');
  detGrid.innerHTML = '';
  const det = d.detection;
  if (det) {
    const items = [
      { label: t('det_produit'),    val: det.produit || '—',       cls: det.produit && det.produit !== 'non détecté' ? 'det-neu' : 'det-bad' },
      { label: t('det_prix'),       val: det.prix_estime || '—',   cls: det.prix_rentable ? 'det-ok' : 'det-neu' },
      { label: t('det_hook_type'),  val: det.hook_type || '—',     cls: 'det-neu' },
      { label: t('det_hook_force'), val: (det.hook_force ?? '—') + (det.hook_force ? '/10' : ''), cls: det.hook_force >= 7 ? 'det-ok' : det.hook_force >= 5 ? 'det-neu' : 'det-bad' },
    ];
    if (det.prix_rentable !== undefined) {
      items[1].val += det.prix_rentable ? t('det_rentable') : t('det_optimiser');
    }
    items.forEach(({ label, val, cls }) => {
      const div = document.createElement('div');
      div.className = 'detection-item';
      div.innerHTML = `<label>${label}</label><strong class="${cls}">${val}</strong>`;
      detGrid.appendChild(div);
    });
  }

  // Potentiel viral
  const vp = d.viral_potential;
  if (vp) {
    document.getElementById('viral-score').textContent      = vp.score ?? '—';
    document.getElementById('viral-prix').textContent       = vp.facteur_prix || '';
    document.getElementById('viral-explication').textContent = vp.explication || '';
  }

  // Points forts / faibles
  fillList('points-forts',  d.points_forts,     '', true);
  fillList('points-faibles',d.points_ameliorer, '', true);

  // Recommandations accroches
  const reco = d.recommendations_hooks;
  if (reco) {
    document.getElementById('hook-type-propose').textContent = reco.hook_type_propose || '—';
    document.getElementById('hook-reason').textContent       = reco.raison || '';
    const exList = document.getElementById('hook-examples');
    exList.innerHTML = (reco.exemples_concrets || []).map(e => `<li>${e}</li>`).join('');
  }

  // Conseils
  fillList('conseils-list', d.conseils_concrets, '', true);

  // Structure de vente
  const sv = d.structure_vente;
  if (sv) {
    document.getElementById('structure-vente-section').style.display = 'block';

    // Étapes du funnel
    const etapes = ['accroche', 'probleme', 'solution', 'produit', 'cta'];
    etapes.forEach(k => {
      const step = sv[k];
      if (!step) return;
      const n = step.score ?? 0;
      const el = document.getElementById(`sv-step-${k}`) || document.getElementById(`sv-${k}`);
      if (el) {
        el.classList.remove('sv-ok', 'sv-warn', 'sv-bad');
        el.classList.add(!step.present ? 'sv-bad' : n >= 7 ? 'sv-ok' : n >= 5 ? 'sv-warn' : 'sv-bad');
      }
      const scoreEl = document.getElementById(`sv-score-${k}`);
      if (scoreEl) scoreEl.textContent = step.present ? `${n}/10` : '—';
      scoreEl && (scoreEl.style.color = !step.present ? 'var(--danger)' : scoreColor(n));

      const feedEl = document.getElementById(`sv-feedback-${k}`);
      if (feedEl) feedEl.textContent = step.feedback || '';
    });

    // Score global structure
    const scoreStrEl = document.getElementById('score-structure');
    if (scoreStrEl) {
      scoreStrEl.textContent = sv.score_structure ?? '—';
      const s = sv.score_structure ?? 0;
      scoreStrEl.style.color = s >= 70 ? 'var(--primary)' : s >= 50 ? 'var(--warning)' : 'var(--danger)';
    }

    // Résumé
    const summaryEl = document.getElementById('structure-summary');
    if (summaryEl) {
      const parts = [];
      if (sv.ordre_naturel) parts.push('✅ Ordre naturel respecté');
      else parts.push('⚠️ Ordre du flux non respecté');
      if (sv.transitions === 'fluides') parts.push('✅ Transitions fluides');
      else if (sv.transitions) parts.push(`⚠️ Transitions : ${sv.transitions}`);
      if (sv.etapes_manquantes?.length) parts.push(`❌ Étapes absentes : ${sv.etapes_manquantes.join(', ')}`);
      if (sv.etapes_faibles?.length) parts.push(`⚠️ Étapes faibles : ${sv.etapes_faibles.join(', ')}`);
      summaryEl.textContent = parts.join(' · ') || 'Structure correcte ✅';
    }

    // Améliorations structure
    const amelioEl = document.getElementById('ameliorations-structure');
    if (amelioEl && d.ameliorations_structure?.length) {
      amelioEl.innerHTML = `
        <h3 style="color:var(--warning);margin-bottom:8px">💡 Améliorer le flux de vente</h3>
        <ul class="points-list neg">${(d.ameliorations_structure).map(a => `<li>${a}</li>`).join('')}</ul>`;
    }
  } else {
    document.getElementById('structure-vente-section').style.display = 'none';
  }

  // Potentiel de conversion par prix
  const pc = d.prix_conversion;
  if (pc) {
    document.getElementById('prix-conversion-section').style.display = 'block';

    document.getElementById('pc-montant').textContent =
      pc.montant ? `${pc.montant} €` : 'Non détecté';

    const catLabels = { economique: t('cat_economique'), moyen: t('cat_moyen'), premium: t('cat_premium'), inconnu: t('cat_inconnu') };
    document.getElementById('pc-categorie').textContent = catLabels[pc.categorie] || pc.categorie || '—';

    const pot = pc.potentiel_conversion || {};
    const delaiLabels = { j7: t('delai_j7'), j30: t('delai_j30'), inconnu: '—' };
    document.getElementById('pc-delai').textContent = delaiLabels[pot.temps_attendre] || pot.temps_attendre || '—';

    document.getElementById('pc-conseil').textContent = pc.conseil_prix || '—';

    document.getElementById('pc-disclaimer').textContent =
      d.disclaimer_realisme || '⚠️ Cette analyse est un guide, pas une certitude. L\'algo TikTok surprend toujours.';
  } else {
    document.getElementById('prix-conversion-section').style.display = 'none';
  }

  // Transcription
  if (d.transcript) {
    document.getElementById('transcript-section').style.display = 'block';
    document.getElementById('transcript-text').textContent = d.transcript;
  }

  // Verdict
  if (d.verdict) {
    document.getElementById('verdict-section').style.display = 'block';
    document.getElementById('verdict-text').textContent = d.verdict;
  }

  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function fillList(id, items, icon, noIcon) {
  const el = document.getElementById(id);
  if (!el) return;
  el.innerHTML = (items || []).map(t => `<li>${noIcon ? '' : icon}${t}</li>`).join('');
}

// ── RESET ────────────────────────────────────────────────────
function resetAnalysis() {
  selectedFile = null; currentData = null;
  document.getElementById('results-section').style.display    = 'none';
  document.getElementById('upload-section').style.display     = 'block';
  document.getElementById('file-tag').style.display           = 'none';
  document.getElementById('video-file').value                 = '';
  document.getElementById('analyze-btn').disabled             = true;
  document.getElementById('transcript-section').style.display       = 'none';
  document.getElementById('verdict-section').style.display           = 'none';
  document.getElementById('structure-vente-section').style.display   = 'none';
  document.getElementById('prix-conversion-section').style.display   = 'none';
  document.getElementById('error-box').style.display                = 'none';
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ── USAGE COUNTER ─────────────────────────────────────────────
function getUsage()       { return parseInt(localStorage.getItem(USAGE_KEY) || '0', 10); }
function incrementUsage() { localStorage.setItem(USAGE_KEY, getUsage() + 1); updateUsageCounter(); }
function updateUsageCounter() {
  const n = getUsage();
  const el = document.getElementById('usage-count');
  if (el) el.textContent = `${n} / ${FREE_LIMIT}`;
}

// ── HISTORY ──────────────────────────────────────────────────
function getHistory() {
  try { return JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]'); } catch { return []; }
}

function saveToHistory(data, filename) {
  const entries = getHistory();
  // Évite les doublons consécutifs
  if (entries[0]?.id === data.id) return;
  entries.unshift({
    id:                    Date.now(),
    date:                  new Date().toISOString(),
    filename:              filename || 'vidéo',
    score_global:          data.score_global,
    verdict:               data.verdict,
    scores:                data.scores,
    detection:             data.detection,
    viral_potential:       data.viral_potential,
    points_forts:          data.points_forts,
    points_ameliorer:      data.points_ameliorer,
    recommendations_hooks: data.recommendations_hooks,
    conseils_concrets:     data.conseils_concrets,
    transcript:            data.transcript,
  });
  localStorage.setItem(STORAGE_KEY, JSON.stringify(entries.slice(0, MAX_HISTORY)));
  updateHistoryBadge();
}

function updateHistoryBadge() {
  const n = getHistory().length;
  const b = document.getElementById('history-badge');
  if (b) { b.textContent = n; b.style.display = n > 0 ? 'inline-block' : 'none'; }
}

function renderHistory() {
  const entries = getHistory();
  const container = document.getElementById('history-list');
  if (!container) return;
  if (entries.length === 0) {
    container.innerHTML = `<div class="history-empty">${t('hist_empty')}</div>`;
    return;
  }
  let html = `<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px">
    <span style="font-size:13px;color:var(--muted)">${entries.length} analyse${entries.length > 1 ? 's' : ''}</span>
    <button onclick="clearHistory()" style="background:none;border:1px solid rgba(255,71,87,.3);color:#ff6b7a;border-radius:6px;padding:4px 10px;font-size:11px;cursor:pointer">${t('hist_clear')}</button>
  </div>`;
  entries.forEach((e, i) => {
    const d = new Date(e.date);
    const ds = d.toLocaleDateString('fr-FR', { day:'2-digit', month:'short' }) + ' · ' + d.toLocaleTimeString('fr-FR', { hour:'2-digit', minute:'2-digit' });
    const snippet = (e.verdict || e.filename || '').slice(0, 55) + '…';
    html += `<div class="history-entry" onclick="openHistoryEntry(${i})">
      <div class="history-score">${e.score_global ?? '—'}</div>
      <div class="history-info">
        <div class="history-date">${ds} · ${e.filename}</div>
        <div class="history-snippet">${snippet}</div>
      </div>
      <button class="history-del" onclick="deleteEntry(event,${i})">✕</button>
    </div>`;
  });
  container.innerHTML = html;
}

function openHistoryEntry(i) {
  const e = getHistory()[i];
  if (!e) return;
  currentData = e; currentFilename = e.filename;
  switchTab('analyze');
  document.getElementById('upload-section').style.display = 'none';
  showResults(e);
}

function deleteEntry(event, i) {
  event.stopPropagation();
  const entries = getHistory();
  entries.splice(i, 1);
  localStorage.setItem(STORAGE_KEY, JSON.stringify(entries));
  updateHistoryBadge(); renderHistory();
}

function clearHistory() {
  if (!confirm(t('hist_confirm'))) return;
  localStorage.removeItem(STORAGE_KEY);
  updateHistoryBadge(); renderHistory();
}

// ── EXPORT PDF ───────────────────────────────────────────────
function exportPDF() {
  if (!currentData || !window.jspdf) return;
  const { jsPDF } = window.jspdf;
  const doc = new jsPDF({ unit: 'mm', format: 'a4' });
  const GREEN = [0, 229, 160];
  const DARK  = [13, 15, 20];
  const BLUE  = [77, 159, 255];
  let y = 0;

  // En-tête
  doc.setFillColor(...DARK);
  doc.rect(0, 0, 210, 36, 'F');
  doc.setFillColor(...GREEN);
  doc.rect(0, 34, 210, 2, 'F');
  doc.setTextColor(...GREEN);
  doc.setFontSize(16); doc.setFont('helvetica', 'bold');
  doc.text('TikTok Shop Vidéo Analyzer', 105, 14, { align: 'center' });
  doc.setFontSize(9); doc.setFont('helvetica', 'normal');
  doc.setTextColor(140, 140, 140);
  doc.text('by Dope Ventures', 105, 21, { align: 'center' });
  doc.text(`${new Date().toLocaleDateString('fr-FR')} · ${currentFilename}`, 105, 28, { align: 'center' });
  y = 46;

  // Score global
  doc.setFillColor(...BLUE);
  doc.roundedRect(15, y, 180, 20, 3, 3, 'F');
  doc.setTextColor(212, 175, 55);
  doc.setFontSize(20); doc.setFont('helvetica', 'bold');
  doc.text(`Score global : ${currentData.score_global ?? '—'} / 100`, 105, y + 13, { align: 'center' });
  y += 26;

  // Verdict
  if (currentData.verdict) {
    doc.setFontSize(9); doc.setFont('helvetica', 'italic'); doc.setTextColor(100, 100, 100);
    const lines = doc.splitTextToSize(currentData.verdict, 180);
    doc.text(lines, 15, y); y += lines.length * 5 + 6;
  }

  const section = (title, col) => {
    if (y > 265) { doc.addPage(); y = 15; }
    doc.setFillColor(...col);
    doc.rect(15, y, 180, 8, 'F');
    doc.setTextColor(255, 255, 255);
    doc.setFontSize(10); doc.setFont('helvetica', 'bold');
    doc.text(title, 19, y + 5.5); y += 12;
  };

  // Scores détaillés
  section('Analyse détaillée', BLUE);
  if (currentData.scores) {
    const LABELS_PDF = { accroche:'Accroche', discours:'Discours', qualite_visuelle:'Qualité visuelle', visibilite_produit:'Produit', call_to_action:'Appel à l\'action', energie_dynamisme:'Énergie', credibilite_confiance:'Crédibilité' };
    Object.entries(currentData.scores).forEach(([k, v]) => {
      if (y > 265) { doc.addPage(); y = 15; }
      const n = v.note ?? 0;
      const col = n >= 7 ? [0,229,160] : n >= 5 ? [255,193,7] : [255,71,87];
      doc.setTextColor(40,40,40); doc.setFontSize(9); doc.setFont('helvetica', 'bold');
      doc.text(LABELS_PDF[k] || k, 15, y);
      doc.setTextColor(...col); doc.text(`${n}/10`, 195, y, { align:'right' });
      doc.setFillColor(220,220,220); doc.roundedRect(15, y+2, 180, 3, 1, 1, 'F');
      doc.setFillColor(...col); doc.roundedRect(15, y+2, 180*n/10, 3, 1, 1, 'F');
      y += 7;
      if (v.commentaire) {
        doc.setTextColor(100,100,100); doc.setFont('helvetica','normal'); doc.setFontSize(8);
        const lines = doc.splitTextToSize(v.commentaire, 176);
        doc.text(lines, 19, y); y += lines.length * 4 + 3;
      }
    });
  }

  const listSection = (title, col, items, prefix) => {
    if (!items?.length) return;
    section(title, col);
    items.forEach(p => {
      if (y > 270) { doc.addPage(); y = 15; }
      doc.setTextColor(40,40,40); doc.setFontSize(9); doc.setFont('helvetica','normal');
      const lines = doc.splitTextToSize(`${prefix} ${p}`, 176);
      doc.text(lines, 19, y); y += lines.length * 4.5 + 2;
    });
  };

  listSection('Points forts',     [34,139,34],    currentData.points_forts,     '+');
  listSection('À améliorer',      [200,100,0],    currentData.points_ameliorer, '!');
  listSection('Conseils concrets', BLUE,           currentData.conseils_concrets,'→');

  // Recommandations accroches
  const reco = currentData.recommendations_hooks;
  if (reco) {
    section('Recommandation accroche', [77,159,255]);
    doc.setTextColor(0,229,160); doc.setFontSize(10); doc.setFont('helvetica','bold');
    doc.text(reco.hook_type_propose || '', 15, y); y += 6;
    if (reco.raison) {
      doc.setTextColor(100,100,100); doc.setFont('helvetica','italic'); doc.setFontSize(8);
      const lines = doc.splitTextToSize(reco.raison, 178);
      doc.text(lines, 15, y); y += lines.length * 4 + 4;
    }
    (reco.exemples_concrets || []).forEach(e => {
      if (y > 270) { doc.addPage(); y = 15; }
      doc.setTextColor(60,60,60); doc.setFont('helvetica','normal'); doc.setFontSize(9);
      const lines = doc.splitTextToSize(`→ "${e}"`, 176);
      doc.text(lines, 19, y); y += lines.length * 4.5 + 2;
    });
  }

  if (currentData.transcript) {
    section('Transcription audio', [80,80,80]);
    doc.setTextColor(80,80,80); doc.setFontSize(8); doc.setFont('helvetica','italic');
    const lines = doc.splitTextToSize(currentData.transcript, 176);
    doc.text(lines, 19, y);
  }

  // Pied de page
  const pages = doc.getNumberOfPages();
  for (let i = 1; i <= pages; i++) {
    doc.setPage(i);
    doc.setFontSize(7); doc.setTextColor(100,100,100); doc.setFont('helvetica','normal');
    doc.text(`TikTok Shop Vidéo Analyzer · by Dope Ventures · ${i}/${pages}`, 105, 291, { align:'center' });
  }

  doc.save(`analyse-dv-${Date.now()}.pdf`);
}

// ── AUTH ─────────────────────────────────────────────────────
document.getElementById('btn-auth').addEventListener('click', () => {
  document.getElementById('auth-modal').classList.add('active');
});

function closeModal() {
  document.getElementById('auth-modal').classList.remove('active');
}

function handleAuth(event) {
  event.preventDefault();
  const email = document.getElementById('email-input').value;
  if (!email) return;
  localStorage.setItem(USER_KEY, email);
  restoreUser();
  closeModal();
}

function restoreUser() {
  const email = localStorage.getItem(USER_KEY);
  if (email) {
    document.getElementById('user-email').textContent = email;
    document.getElementById('btn-auth').textContent = t('btn_account');
    document.getElementById('btn-auth').removeAttribute('data-i18n'); // géré manuellement
  }
}

// ── PWA ──────────────────────────────────────────────────────
function installPwa() {
  if (!deferredPrompt) return;
  deferredPrompt.prompt();
  deferredPrompt.userChoice.then(() => {
    deferredPrompt = null;
    document.getElementById('pwa-banner').style.display = 'none';
  });
}

// Fermer modal en cliquant dehors
document.getElementById('auth-modal').addEventListener('click', function(e) {
  if (e.target === this) closeModal();
});

// ── COOKIES RGPD ─────────────────────────────────────────────
const CONSENT_KEY     = 'dv_cookie_consent';
const TRANSP_KEY      = 'dv_transparency_dismissed';

function initCookies() {
  const consent = localStorage.getItem(CONSENT_KEY);
  if (!consent) {
    document.getElementById('cookie-banner').style.display = 'block';
  }
  const dismissed = localStorage.getItem(TRANSP_KEY);
  if (dismissed) {
    const tb = document.getElementById('transparency-banner');
    if (tb) tb.style.display = 'none';
  }
}

function acceptCookies() {
  localStorage.setItem(CONSENT_KEY, JSON.stringify({
    essential: true, analytics: true,
    timestamp: new Date().toISOString()
  }));
  hideCookieBanner();
}

function rejectCookies() {
  localStorage.setItem(CONSENT_KEY, JSON.stringify({
    essential: true, analytics: false,
    timestamp: new Date().toISOString()
  }));
  hideCookieBanner();
}

function hideCookieBanner() {
  const el = document.getElementById('cookie-banner');
  if (!el) return;
  el.style.animation = 'fadeOut .25s ease forwards';
  setTimeout(() => el.style.display = 'none', 260);
}

function dismissTransparencyBanner() {
  localStorage.setItem(TRANSP_KEY, '1');
  const tb = document.getElementById('transparency-banner');
  if (tb) { tb.style.animation = 'fadeOut .2s ease forwards'; setTimeout(() => tb.style.display = 'none', 210); }
}

// ── PRIVACY MODAL ─────────────────────────────────────────────
function openPrivacyModal() {
  const body = document.getElementById('pm-body');
  if (body) body.innerHTML = t('pm_content') || '';
  document.getElementById('privacy-backdrop').classList.add('active');
  document.body.style.overflow = 'hidden';
}

function closePrivacyModal() {
  document.getElementById('privacy-backdrop').classList.remove('active');
  document.body.style.overflow = '';
}

// Init au chargement
document.addEventListener('DOMContentLoaded', () => { /* déjà appelé plus haut */ });
// Appel direct (DOMContentLoaded déjà bindé, on ajoute juste initCookies au flux existant)
document.addEventListener('DOMContentLoaded', initCookies);
