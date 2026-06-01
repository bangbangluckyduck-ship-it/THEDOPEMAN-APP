/* ============================================================
   TikTok Shop Vidéo Analyzer — app_v2.js (COMPLETE REBUILD)
   Clean session management with single source of truth
   ============================================================ */

'use strict';

// ── CONSTANTES ────────────────────────────────────────────────
const STORAGE_KEY   = 'dv_history';
const USAGE_KEY     = 'dv_usage';
const USER_KEY      = 'dv_user';
const MAX_HISTORY   = 20;
const FREE_LIMIT    = 999;

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
    tab_analyze:'🎬 Analyser', tab_history:'📋 Historique', tab_winning_trends:'🔥 Tendances Gagnantes',
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
    tab_analyze:'🎬 Analyze', tab_history:'📋 History', tab_winning_trends:'🔥 Winning Trends',
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
    tab_analyze:'🎬 Analisar', tab_history:'📋 Histórico', tab_winning_trends:'🔥 Tendências Vencedoras',
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
    score_energia_dinamismo:'⚡ Energia', score_credibilite_confiance:'🤝 Credibilidade',
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
    tab_analyze:'🎬 Analizar', tab_history:'📋 Historial', tab_winning_trends:'🔥 Tendencias Ganadoras',
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
    tab_analyze:'🎬 Analizza', tab_history:'📋 Cronologia', tab_winning_trends:'🔥 Tendenze Vincenti',
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
    score_energia_dinamismo:'⚡ Energia', score_credibilite_confiance:'🤝 Credibilità',
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
    tab_analyze:'🎬 Analysieren', tab_history:'📋 Verlauf', tab_winning_trends:'🔥 Gewinnende Trends',
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

// ══════════════════════════════════════════════════════════════
// SESSION MANAGEMENT — SINGLE SOURCE OF TRUTH
// ══════════════════════════════════════════════════════════════

// Session state — read from localStorage at startup, SINGLE location
let SESSION = {
  email: null,
  name: null,
};

// Load session from localStorage on module initialization
function initSessionState() {
  SESSION.email = localStorage.getItem('tts_email') || null;
  SESSION.name = localStorage.getItem('tts_name') || null;
}

// Save session to localStorage and update UI
function saveSession(email, name, token) {
  SESSION.email = email;
  SESSION.name = name;
  localStorage.setItem('tts_email', email);
  localStorage.setItem('tts_name', name);
  if (token) {
    localStorage.setItem('tts_token', token);
  }
  updateSessionUI();
  fetchUserInfo();
}

// Clear session from localStorage and redirect to home
function clearSession() {
  try {
    SESSION.email = null;
    SESSION.name = null;
    localStorage.removeItem('tts_token');
    localStorage.removeItem('tts_email');
    localStorage.removeItem('tts_name');
    localStorage.removeItem(USAGE_KEY);
  } catch (_) { /* localStorage peut être bloqué en privé sur iOS */ }
  window.location.href = '/';
}

// Expose logout in multiple scopes pour être sûr que les onclick="logout()" ou
// onclick="window.logout()" trouvent toujours la fonction (sécurité de scope).
window.logout = clearSession;
window.clearSession = clearSession;
// eslint-disable-next-line no-unused-vars
function logout() { return clearSession(); }
window.logout = window.logout || logout;

// ── TOAST & CONFIRM (in-page, no browser popups) ──────────────
function showToast(message, type) {
  try {
    if (!document.getElementById('__toast_style')) {
      const st = document.createElement('style');
      st.id = '__toast_style';
      st.textContent =
        '#__toast_wrap{position:fixed;left:50%;bottom:24px;transform:translateX(-50%);z-index:99999;display:flex;flex-direction:column;gap:8px;width:max-content;max-width:calc(100vw - 32px);pointer-events:none}' +
        '.__toast{background:#1f2937;color:#fff;padding:12px 18px;border-radius:10px;font-size:14px;line-height:1.45;box-shadow:0 8px 30px rgba(0,0,0,.25);opacity:0;transform:translateY(10px);transition:opacity .2s,transform .2s;pointer-events:auto;word-break:break-word;white-space:pre-line}' +
        '.__toast.show{opacity:1;transform:translateY(0)}' +
        '.__toast.ok{background:#065f46}.__toast.err{background:#991b1b}';
      document.head.appendChild(st);
    }
    let wrap = document.getElementById('__toast_wrap');
    if (!wrap) { wrap = document.createElement('div'); wrap.id = '__toast_wrap'; document.body.appendChild(wrap); }
    const msg = String(message == null ? '' : message);
    let cls = type || '';
    if (!cls) {
      if (msg.indexOf('❌') !== -1 || /erreur/i.test(msg)) cls = 'err';
      else if (msg.indexOf('✅') !== -1) cls = 'ok';
    }
    const el = document.createElement('div');
    el.className = '__toast ' + cls;
    el.textContent = msg;
    wrap.appendChild(el);
    requestAnimationFrame(() => el.classList.add('show'));
    const dur = Math.min(8000, Math.max(3000, msg.length * 55));
    setTimeout(() => { el.classList.remove('show'); setTimeout(() => el.remove(), 250); }, dur);
  } catch (e) { console.warn('toast failed:', message); }
}
window.showToast = showToast;

function showConfirm(message) {
  return new Promise((resolve) => {
    const ov = document.createElement('div');
    ov.style.cssText = 'position:fixed;inset:0;background:rgba(0,0,0,.55);z-index:100000;display:flex;align-items:center;justify-content:center;padding:20px';
    const box = document.createElement('div');
    box.style.cssText = 'background:var(--surface,#fff);color:var(--text,#111);border-radius:14px;padding:22px;max-width:380px;width:100%;box-shadow:0 20px 60px rgba(0,0,0,.3)';
    const txt = document.createElement('div');
    txt.style.cssText = 'font-size:15px;line-height:1.5;margin-bottom:18px;white-space:pre-line';
    txt.textContent = String(message || '');
    const row = document.createElement('div');
    row.style.cssText = 'display:flex;gap:10px;justify-content:flex-end';
    const no = document.createElement('button');
    no.textContent = 'Annuler';
    no.style.cssText = 'padding:10px 16px;border:1px solid var(--border,#ddd);background:transparent;color:var(--text,#111);border-radius:8px;cursor:pointer;font-size:14px';
    const yes = document.createElement('button');
    yes.textContent = 'Confirmer';
    yes.style.cssText = 'padding:10px 16px;border:none;background:#dc2626;color:#fff;border-radius:8px;cursor:pointer;font-size:14px;font-weight:600';
    row.appendChild(no); row.appendChild(yes);
    box.appendChild(txt); box.appendChild(row); ov.appendChild(box);
    document.body.appendChild(ov);
    const done = (v) => { ov.remove(); resolve(v); };
    yes.onclick = () => done(true);
    no.onclick = () => done(false);
    ov.onclick = (e) => { if (e.target === ov) done(false); };
  });
}
window.showConfirm = showConfirm;

// ── UTILITY FUNCTIONS ─────────────────────────────────────────
function acceptCookies() {
  localStorage.setItem('cookieConsent', 'accepted');
  const banner = document.getElementById('cookie-banner');
  if (banner) banner.style.display = 'none';
}

function rejectCookies() {
  localStorage.setItem('cookieConsent', 'rejected');
  const banner = document.getElementById('cookie-banner');
  if (banner) banner.style.display = 'none';
}

function dismissTransparencyBanner() {
  const banner = document.getElementById('transparency-banner');
  if (banner) banner.style.display = 'none';
}

function openPrivacyModal() {
  const backdrop = document.getElementById('privacy-backdrop');
  if (backdrop) backdrop.classList.add('active');
  // Populate privacy modal content based on current language
  const pmBody = document.getElementById('pm-body');
  if (pmBody) pmBody.innerHTML = t('pm_content');
}

// ── FORGOT PASSWORD FUNCTIONS ─────────────────────────────────
function openForgotPasswordModal() {
  const modal = document.getElementById('forgot-password-modal');
  if (modal) modal.style.display = 'flex';
}

function closeForgotPasswordModal() {
  const modal = document.getElementById('forgot-password-modal');
  if (modal) modal.style.display = 'none';
}

async function submitForgotPassword(event) {
  event.preventDefault();

  const emailInput = document.getElementById('forgot-email-input');
  const passwordInput = document.getElementById('forgot-password-input');
  const confirmInput = document.getElementById('forgot-password-confirm');

  const email = (emailInput?.value || '').trim().toLowerCase();
  const password = (passwordInput?.value || '').trim();
  const confirm = (confirmInput?.value || '').trim();

  // Validation
  if (!email || !password || !confirm) {
    showToast('❌ Veuillez remplir tous les champs');
    return;
  }

  if (password !== confirm) {
    showToast('❌ Les mots de passe ne correspondent pas');
    return;
  }

  if (password.length < 6) {
    showToast('❌ Min 6 caractères');
    return;
  }

  try {
    const response = await fetch('/api/forgot-password', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });

    if (!response.ok) {
      const error = await response.json();
      showToast('❌ ' + (error.detail || 'Erreur'));
      return;
    }

    // Success
    showToast('✅ Email de réinitialisation envoyé!\n\nVérifie ta boîte mail pour ton mot de passe temporaire.');
    closeForgotPasswordModal();

    // Clear form
    emailInput.value = '';
    passwordInput.value = '';
    confirmInput.value = '';

  } catch (err) {
    showToast('❌ Erreur: ' + err.message);
  }
}

// ── ADMIN PASSWORD RESET ──────────────────────────────────────
async function adminResetPassword(email, resetType) {
  if (!email) {
    showToast('❌ Email non trouvé');
    return;
  }

  const confirmMessage = resetType === 'magic_link'
    ? 'Envoyer un lien magique à ' + email + '?'
    : 'Générer et envoyer un mot de passe temporaire à ' + email + '?';

  if (!(await showConfirm(confirmMessage))) return;

  try {
    const response = await fetch('/admin/reset-user-password', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('tts_token') || ''}`
      },
      body: JSON.stringify({
        email: email.toLowerCase(),
        reset_type: resetType
      })
    });

    if (!response.ok) {
      const error = await response.json();
      showToast('❌ ' + (error.detail || 'Erreur'));
      return;
    }

    const data = await response.json();

    if (resetType === 'temporary_password') {
      // Show the temporary password
      showToast(`✅ Mot de passe temporaire généré:\n\n${data.temp_password}\n\nEmail envoyé à ${email}\n\nL'utilisateur devra changer ce mot de passe à sa première connexion.`);
    } else {
      // Magic link
      showToast(`✅ Lien magique envoyé à ${email}\n\nL'utilisateur pourra cliquer sur le lien pour créer un nouveau mot de passe.`);
    }

  } catch (err) {
    showToast('❌ Erreur: ' + err.message);
  }
}

function closePrivacyModal() {
  const backdrop = document.getElementById('privacy-backdrop');
  if (backdrop) backdrop.classList.remove('active');
}

function openCGV() {
  const overlay = document.getElementById('cgv-overlay');
  if (overlay) overlay.style.display = 'block';
}

function closeCGV() {
  const overlay = document.getElementById('cgv-overlay');
  if (overlay) overlay.style.display = 'none';
}

function installPwa() {
  if (window.deferredPrompt) {
    window.deferredPrompt.prompt();
    window.deferredPrompt.userChoice.then(() => {
      window.deferredPrompt = null;
      const banner = document.getElementById('pwa-banner');
      if (banner) banner.style.display = 'none';
    });
  }
}

// ⚠️ Passe à true une fois les produits/prix Stripe créés en production.
const CHECKOUT_ENABLED = false;

// Période de facturation choisie dans la grille tarifaire ("month" | "year")
let BILLING_PERIOD = 'month';
function setBilling(period) {
  BILLING_PERIOD = period === 'year' ? 'year' : 'month';
  document.getElementById('pricing-grid')?.setAttribute('data-billing', BILLING_PERIOD);
  document.querySelectorAll('.billing-toggle-btn').forEach(b =>
    b.classList.toggle('active', b.dataset.period === BILLING_PERIOD));
}

async function startCheckout(plan) {
  // Les abonnements automatiques ne sont pas encore ouverts : message propre.
  if (!CHECKOUT_ENABLED) {
    showToast("🚀 L'ouverture des abonnements automatiques arrive dans quelques jours ! Ton compte admin te permet déjà de tester toutes les fonctionnalités.");
    return;
  }

  const email = SESSION.email || '';
  if (!email) {
    showToast('Veuillez vous connecter d\'abord');
    const modal = document.getElementById('auth-modal');
    if (modal) modal.classList.add('active');
    return;
  }

  try {
    const res = await fetch('/create-checkout-session', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ plan, email, billing: BILLING_PERIOD })
    });

    if (!res.ok) {
      const err = await res.json();
      showToast('❌ ' + (err.detail || 'Erreur checkout'));
      return;
    }

    const data = await res.json();
    if (data.checkout_url) {
      window.location.href = data.checkout_url;
    }
  } catch (err) {
    showToast('❌ Erreur: ' + err.message);
  }
}

// Show auth menu (account dropdown)
function showAuthMenu(e) {
  e?.stopPropagation?.();

  const existing = document.getElementById('auth-menu');
  if (existing) {
    existing.remove();
    return;
  }

  const btnAuth = document.getElementById('btn-auth');
  if (!btnAuth) return;

  const menu = document.createElement('div');
  menu.id = 'auth-menu';
  menu.className = 'auth-menu';
  menu.style.cssText = `
    position: fixed;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.15);
    z-index: 2001;
    min-width: 220px;
    max-width: calc(100vw - 32px);
    overflow: hidden;
  `;

  menu.innerHTML = `
    <button onclick="switchTab('account'); closeAuthMenu(); return false" style="width:100%;display:block;text-align:left;padding:12px 16px;color:var(--text);background:transparent;border:none;border-bottom:1px solid var(--border);font-size:13px;cursor:pointer;transition:background .15s" onmouseover="this.style.background='var(--surface2)'" onmouseout="this.style.background='transparent'">
      ⚙️ Mon abonnement
    </button>
    <button onclick="window.logout(); return false" style="width:100%;display:block;text-align:left;padding:12px 16px;color:var(--danger);background:transparent;border:none;font-size:13px;cursor:pointer;transition:background .15s" onmouseover="this.style.background='var(--surface2)'" onmouseout="this.style.background='transparent'">
      🚪 Déconnexion
    </button>
  `;

  document.body.appendChild(menu);

  // Position menu relative to button — clamp right on small screens
  // to éviter que le menu déborde du viewport (bug iOS Safari).
  const rect = btnAuth.getBoundingClientRect();
  menu.style.top = (rect.bottom + 8) + 'px';
  // Ancrer au bord droit avec un padding fixe, jamais hors écran (bug iOS Safari)
  menu.style.right = '16px';
  menu.style.left = 'auto';

  // Close menu when clicking elsewhere
  function closeMenu(clickEvent) {
    if (!menu.contains(clickEvent.target) && clickEvent.target !== btnAuth) {
      menu.remove();
      document.removeEventListener('click', closeMenu);
    }
  }

  // Delay to prevent immediate closure
  setTimeout(() => {
    document.addEventListener('click', closeMenu);
  }, 50);
}

function closeAuthMenu() {
  const menu = document.getElementById('auth-menu');
  if (menu) menu.remove();
}

// Update UI to match session state
function updateSessionUI() {
  const overlay = document.getElementById('login-overlay');
  const userEmailEl = document.getElementById('user-email');
  const btnAuth = document.getElementById('btn-auth');

  if (SESSION.email) {
    // User is logged in
    if (overlay) overlay.style.display = 'none';
    if (userEmailEl) userEmailEl.textContent = SESSION.name || SESSION.email;
    if (btnAuth) {
      btnAuth.textContent = '⚙️ Mon compte';
      btnAuth.onclick = (e) => showAuthMenu(e);
    }
    // Fetch user tier info (appelle fetchUserInfo qui met à jour le badge)
    fetchUserInfo();
  } else {
    // User is not logged in
    if (overlay) overlay.style.display = 'flex';
    if (userEmailEl) userEmailEl.textContent = '';
    if (btnAuth) {
      btnAuth.textContent = t('btn_connect');
      btnAuth.onclick = (e) => {
        e?.preventDefault?.();
        const modal = document.getElementById('auth-modal');
        if (modal) modal.classList.add('active');
      };
    }
    // Masquer le badge du tier si pas connecté
    const tierBadge = document.getElementById('user-tier-badge');
    if (tierBadge) tierBadge.style.display = 'none';
  }
}

// Fetch user info from server
function fetchUserInfo() {
  if (!SESSION.email) return;
  fetch('/api/user-info', {
    headers: {
      'Authorization': localStorage.getItem('tts_token') ? 'Bearer ' + localStorage.getItem('tts_token') : ''
    }
  })
    .then(r => r.json())
    .then(data => {
      window.__userInfo = data;
      updateTierBadge(data);
    })
    .catch(() => {});
}

function updateTierBadge(data) {
  const tierBadge = document.getElementById('user-tier-badge');
  if (!tierBadge || !data || !data.tier) return;

  const labels = { free: 'FREE', pro: 'PRO', gold: 'GOLD ⭐', agency: 'AGENCY', beta: 'BETA 🎁', admin: 'ADMIN' };
  const colors = { free: '#6B7280', pro: '#2563EB', gold: '#D97706', agency: '#7C3AED', beta: '#059669', admin: '#DC2626' };

  tierBadge.textContent = labels[data.tier] || data.tier.toUpperCase();
  tierBadge.style.background = colors[data.tier] || '#6B7280';
  tierBadge.style.display = 'inline-block';
  // NB : le back-office admin est désormais isolé sur /dope-admin
  // (plus aucun onglet admin exposé dans l'espace client).
}

// ══════════════════════════════════════════════════════════════
// APP STATE (rest of the application state)
// ══════════════════════════════════════════════════════════════
let selectedFile   = null;
let serverReady    = false;
let currentData    = null;
let currentFilename = '';
let deferredPrompt = null;

// ── INITIALIZATION ────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  // Initialize session from localStorage
  initSessionState();

  // Set up UI to match session state
  updateSessionUI();

  detectLanguage();
  applyTranslations();
  wakeServer();
  updateUsageCounter();
  updateHistoryBadge();
  handleCheckoutReturn();

  // Language selector
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

  // iOS installation guide
  const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent) ||
    (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
  const isStandalone = window.navigator.standalone === true ||
    window.matchMedia('(display-mode: standalone)').matches;
  const iosBannerDismissed = localStorage.getItem('ios_banner_dismissed');

  if (isIOS && !isStandalone && !iosBannerDismissed) {
    const banner = document.getElementById('ios-banner');
    if (banner) {
      document.getElementById('ios-banner-title').textContent = t('ios_title');
      const steps = document.getElementById('ios-banner-steps');
      steps.innerHTML = `<li>${t('ios_s1')}</li><li>${t('ios_s2')}</li><li>${t('ios_s3')}</li>`;
      banner.style.display = 'block';
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

// ── CUSTOMER PORTAL ──────────────────────────────────────────
async function openCustomerPortal() {
  const email       = SESSION.email || '';
  const customer_id = (window.__usage || {}).customer_id || '';
  try {
    const res = await fetch('/customer-portal', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, customer_id }),
    });
    if (!res.ok) { showToast('❌ Portail indisponible.'); return; }
    const { url } = await res.json();
    window.location.href = url;
  } catch { showToast('❌ Erreur réseau.'); }
}

// ── TABS ──────────────────────────────────────────────────────
function switchTab(tab) {
  ['analyze', 'pricing', 'history', 'winning-trends', 'account'].forEach(t => {
    const content = document.getElementById(`tab-${t}-content`);
    const btn     = document.getElementById(`tab-${t}`);
    if (content) content.style.display = t === tab ? 'block' : 'none';
    if (btn)     btn.classList.toggle('active', t === tab);
  });
  if (tab === 'history') renderHistory();
  if (tab === 'pricing') updatePricingCTA();
  if (tab === 'winning-trends') loadWinningTrendsTab();
  if (tab === 'account') renderAccountPage();
}

// ── UPLOAD ────────────────────────────────────────────────────
const uploadArea = document.getElementById('upload-area');
const fileInput  = document.getElementById('video-file');

if (uploadArea) {
  uploadArea.addEventListener('click', () => fileInput.click());
  uploadArea.addEventListener('dragover',  e => { e.preventDefault(); uploadArea.classList.add('active'); });
  uploadArea.addEventListener('dragleave', () => uploadArea.classList.remove('active'));
  uploadArea.addEventListener('drop', e => {
    e.preventDefault(); uploadArea.classList.remove('active');
    const f = e.dataTransfer.files[0];
    if (f && f.type.startsWith('video/')) setFile(f);
  });
}

fileInput.addEventListener('change', e => { if (e.target.files[0]) setFile(e.target.files[0]); });

function setFile(f) {
  selectedFile = f;
  document.getElementById('error-box').style.display = 'none';
  const tag = document.getElementById('file-tag');
  tag.textContent = `📎 ${f.name} (${(f.size / 1024 / 1024).toFixed(1)} Mo)`;
  tag.style.display = 'block';
  document.getElementById('analyze-btn').disabled = false;
}

document.getElementById('analyze-btn').addEventListener('click', analyzeVideo);

// Analyse par liens TikTok (Pro / Gold / Agency)
const _urlsBtn = document.getElementById('analyze-urls-btn');
if (_urlsBtn) _urlsBtn.addEventListener('click', analyzeUrls);

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

// ── MAIN ANALYSIS FLOW ────────────────────────────────────────
async function analyzeVideo() {
  if (!selectedFile) return;

  // ── "Aha! Moment" gate : 1 essai libre, puis création de compte ──
  const token = localStorage.getItem('tts_token');
  const localUsage = parseInt(localStorage.getItem(USAGE_KEY) || '0', 10);

  // Si pas de compte ET qu'il a déjà fait 1 essai
  if (!token && localUsage >= 1) {
    const authModal = document.getElementById('auth-modal');
    if (authModal) authModal.classList.add('active');
    showError("🎉 Impressionnant, non ? Crée un compte gratuit pour débloquer tes prochaines analyses !");
    window.scrollTo({ top: 0, behavior: 'smooth' });
    return; // On stoppe l'analyse
  }

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

    // Ajouter le produit optionnel si l'utilisateur l'a entré
    const productInput = document.getElementById('product-input');
    if (productInput && productInput.value.trim()) {
      fd.append('product', productInput.value.trim());
    }
    // Ajouter le prix saisi manuellement (facilite l'analyse de conversion)
    const priceInput = document.getElementById('price-input');
    if (priceInput && priceInput.value.trim()) {
      fd.append('price', priceInput.value.trim());
    }

    const ctrl    = new AbortController();
    const timer   = setTimeout(() => ctrl.abort(), 100000);
    const headers = {};
    const _token = localStorage.getItem('tts_token');
    if (_token) {
      headers['Authorization'] = 'Bearer ' + _token;
    }
    // Use streaming SSE instead of waiting for full response
    const res = await fetch('/analyze', { method: 'POST', body: fd, signal: ctrl.signal, headers });
    clearTimeout(timer);

    if (!res.ok) {
      try {
        const errData = await res.json();
        throw new Error(errData.detail || 'Erreur serveur');
      } catch (e) {
        throw new Error('Erreur serveur');
      }
    }

    // Handle Server-Sent Events streaming (robust parser)
    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let completeData = null;
    let buffer = '';

    const handleEvent = (eventType, dataStr) => {
      if (!eventType || !dataStr) return;
      let eventData;
      try { eventData = JSON.parse(dataStr); } catch (e) {
        console.warn('[STREAM] Invalid JSON:', dataStr.slice(0, 100));
        return;
      }
      if (eventType === 'start') {
        console.log('[STREAM] Analysis started');
      } else if (eventType === 'progress') {
        setLoadingText(eventData.message || '🔄 En cours...');
        console.log('[STREAM] Progress:', eventData.message);
      } else if (eventType === 'warning') {
        console.warn('[STREAM] Warning:', eventData.message);
      } else if (eventType === 'complete') {
        completeData = eventData;
        setLoadingText('✅ Analyse terminée!');
        console.log('[STREAM] Analysis complete');
      } else if (eventType === 'error') {
        throw new Error(eventData.error || 'Erreur analyse');
      }
    };

    // SSE blocks are separated by a blank line. Each block has event:/data: lines.
    const processBlock = (block) => {
      let evType = 'message';
      const dataLines = [];
      for (const raw of block.split('\n')) {
        const line = raw.replace(/\r$/, '');
        if (!line) continue;
        if (line.startsWith('event:')) evType = line.slice(6).trim();
        else if (line.startsWith('data:')) dataLines.push(line.slice(5).trim());
      }
      if (dataLines.length) handleEvent(evType, dataLines.join('\n'));
    };

    try {
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true });
        // Split on event boundaries (\n\n)
        let idx;
        while ((idx = buffer.indexOf('\n\n')) !== -1) {
          const block = buffer.slice(0, idx);
          buffer = buffer.slice(idx + 2);
          if (block.trim()) processBlock(block);
        }
      }
      // Flush remaining
      if (buffer.trim()) processBlock(buffer);

      if (!completeData) throw new Error('Pas de données reçues');

      const data = completeData;
      console.log('[DEBUG] Analysis response:', data);
      currentData     = data;
      currentFilename = selectedFile.name;

      if (data.usage?.used !== undefined) {
        localStorage.setItem(USAGE_KEY, data.usage.used);
        window.__usage = data.usage;
        updateUsageCounter();
        updateUsageBadge(data.usage);
      } else {
        incrementUsage();
      }

      saveToHistory(data, currentFilename);
      console.log('[DEBUG] About to call showResults');
      showResults(data);

      if (data.donnees_marche && (window.__userInfo?.tier === 'gold' || window.__userInfo?.tier === 'agency' || window.__userInfo?.tier === 'beta')) {
        renderMarketSection(data.donnees_marche);
        document.getElementById('market-section').style.display = 'block';
      }

    } catch (parseErr) {
      console.error('[STREAM] Parse error:', parseErr);
      throw parseErr;
    }

  } catch (e) {
    document.getElementById('loading-section').style.display = 'none';
    document.getElementById('upload-section').style.display  = 'block';
    showError(e.name === 'AbortError' ? t('err_timeout') : '❌ ' + e.message);
  }
}

// ════════════════════════════════════════════════════════════════════════════
// ANALYSE PAR LIENS TIKTOK — Pro = 1 lien, Gold/Agency = batch séquentiel
// ════════════════════════════════════════════════════════════════════════════
async function analyzeUrls() {
  const ta = document.getElementById('tiktok-urls');
  if (!ta) return;

  const urls = ta.value.split('\n').map(u => u.trim()).filter(Boolean);
  if (!urls.length) {
    showError('Colle au moins un lien TikTok (un par ligne).');
    return;
  }

  const tier  = window.__userInfo?.tier || 'free';
  const token = localStorage.getItem('tts_token');

  // ── BLOCAGE 1 : anonyme ou FREE → upsell Pro ──
  if (!token || tier === 'free') {
    switchTab('pricing');
    showToast("Passez au plan Pro (19,90€) pour analyser des liens TikTok directement sans rien télécharger !");
    return;
  }

  // ── BLOCAGE 2 : PRO + plusieurs liens → upsell Gold ──
  if (tier === 'pro' && urls.length > 1) {
    switchTab('pricing');
    showToast("Votre plan Pro permet d'analyser 1 lien à la fois. Passez au plan Gold pour analyser plusieurs vidéos en masse !");
    return;
  }

  // ── UI : passe en mode chargement ──
  document.getElementById('error-box').style.display      = 'none';
  document.getElementById('upload-section').style.display  = 'none';
  document.getElementById('loading-section').style.display = 'block';

  const productInput = document.getElementById('product-input');
  const product = (productInput && productInput.value.trim()) ? productInput.value.trim() : null;
  const priceInput = document.getElementById('price-input');
  const price = (priceInput && priceInput.value.trim()) ? priceInput.value.trim() : null;

  const total = urls.length;
  let lastData = null;
  let okCount  = 0;
  const failed  = [];
  const results = [];   // toutes les analyses réussies (pour la méta-synthèse)

  // Une requête /analyze-url, avec timeout + 1 retry automatique sur erreur réseau
  // ("Failed to fetch" = worker recyclé/OOM sur Render → on laisse respirer puis on réessaie).
  async function _analyzeOne(url, attempt = 1) {
    const ctrl  = new AbortController();
    const timer = setTimeout(() => ctrl.abort(), 180000); // 3 min max par vidéo
    try {
      const res = await fetch('/analyze-url', {
        method: 'POST',
        headers: {
          'Content-Type':  'application/json',
          'Authorization': 'Bearer ' + token,
        },
        body: JSON.stringify({ url, product, price }),
        signal: ctrl.signal,
      });
      if (!res.ok) {
        let msg = 'Erreur serveur';
        try { const e = await res.json(); msg = e.detail || msg; } catch (_) {}
        if (res.status === 403) switchTab('pricing');
        const err = new Error(msg);
        err.httpStatus = res.status;
        throw err;
      }
      return await res.json();
    } catch (e) {
      // Erreur réseau (connexion tombée / worker recyclé) → 1 seul retry après pause
      const isNetwork = (e instanceof TypeError) || e.name === 'AbortError';
      if (isNetwork && attempt === 1) {
        setLoadingText('⏳ Le serveur récupère, nouvelle tentative...');
        await new Promise(r => setTimeout(r, 4000));
        return _analyzeOne(url, 2);
      }
      throw e;
    } finally {
      clearTimeout(timer);
    }
  }

  // ── BATCH SÉQUENTIEL : on attend la fin de la vidéo N avant la N+1 (protège la RAM serveur) ──
  for (let i = 0; i < total; i++) {
    setLoadingText(`🔗 Analyse de la vidéo ${i + 1}/${total}...`);
    try {
      const data = await _analyzeOne(urls[i]);
      lastData        = data;
      currentData     = data;
      currentFilename = urls[i];
      okCount++;

      if (data.usage?.used !== undefined) {
        localStorage.setItem(USAGE_KEY, data.usage.used);
        window.__usage = data.usage;
        updateUsageCounter();
        updateUsageBadge(data.usage);
      }
      saveToHistory(data, urls[i]);
      results.push(data);
    } catch (e) {
      // Une vidéo qui échoue ne casse plus tout le lot : on note et on continue
      console.error('[BATCH] Échec vidéo', i + 1, e);
      failed.push(i + 1);
    }

    // Petite pause entre 2 vidéos pour laisser le serveur libérer la mémoire
    if (i < total - 1) await new Promise(r => setTimeout(r, 1500));
  }

  // ── Bilan ──
  document.getElementById('loading-section').style.display = 'none';
  if (lastData) {
    showResults(lastData);
    if (lastData.donnees_marche && ['gold', 'agency', 'beta'].includes(tier)) {
      renderMarketSection(lastData.donnees_marche);
      document.getElementById('market-section').style.display = 'block';
    }
    if (total > 1) {
      const note = failed.length ? ` (${failed.length} échec${failed.length > 1 ? 's' : ''} : vidéo${failed.length > 1 ? 's' : ''} ${failed.join(', ')})` : '';
      showToast(`✅ ${okCount}/${total} vidéos analysées${note}. Voici le dernier rapport.`);
    }

    // ── Méta-synthèse cross-vidéos : détection des patterns gagnants/perdants ──
    // Réservé aux tiers gold/agency/beta/admin et nécessite ≥2 analyses réussies.
    if (results.length >= 2 && ['gold', 'agency', 'beta', 'admin'].includes(tier)) {
      try {
        const patternsSection = document.getElementById('batch-patterns-section');
        if (patternsSection) {
          patternsSection.style.display = 'block';
          patternsSection.innerHTML = '<div style="text-align:center;padding:24px;color:#8b8ba7;">🧠 Détection de tes patterns gagnants en cours...</div>';
        }
        const token = localStorage.getItem('tts_token');
        const headers = { 'Content-Type': 'application/json' };
        if (token) headers['Authorization'] = `Bearer ${token}`;
        const resp = await fetch('/analyze-batch-patterns', {
          method: 'POST',
          headers,
          body: JSON.stringify({
            analyses: results,
            performances: results.map(r => r.performance || null),
          }),
        });
        if (resp.ok) {
          const patternsData = await resp.json();
          renderBatchPatterns(patternsData);
        } else {
          if (patternsSection) patternsSection.style.display = 'none';
          console.warn('[batch-patterns] échec', resp.status);
        }
      } catch (err) {
        const patternsSection = document.getElementById('batch-patterns-section');
        if (patternsSection) patternsSection.style.display = 'none';
        console.warn('[batch-patterns] erreur', err);
      }
    }
  } else {
    document.getElementById('upload-section').style.display = 'block';
    showError('❌ Aucune vidéo n\'a pu être analysée. Vérifie les liens et réessaie.');
  }
}

// 🆕 Render Méta-synthèse cross-vidéos : patterns gagnants & perdants personnels
// Affiche le résultat de /analyze-batch-patterns : recette personnelle de l'utilisateur,
// patterns à reproduire (gagnants) et patterns à corriger (risque algo TikTok Shop).
function renderBatchPatterns(data) {
  const section = document.getElementById('batch-patterns-section');
  if (!section || !data) return;

  const esc = (s) => String(s == null ? '' : s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

  const gagnants = Array.isArray(data.patterns_gagnants) ? data.patterns_gagnants : [];
  const perdants = Array.isArray(data.patterns_perdants) ? data.patterns_perdants : [];
  const recette = (data.recette_personnelle || '').trim();
  const priorite = (data.priorite_coaching || '').trim();
  const nbVideos = data.nb_videos || results?.length || 0;
  const statsReelles = !!data.stats_reelles;

  let html = '';
  html += '<div class="batch-patterns-card" style="background:linear-gradient(135deg,#1a1a2e 0%,#16213e 100%);border:1px solid #2d2d44;border-radius:16px;padding:24px;margin-top:24px;">';
  html += '<div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;">';
  html += '<span style="font-size:24px;">🧠</span>';
  html += '<h2 style="margin:0;font-size:20px;color:#fff;">Tes patterns personnels</h2>';
  html += '</div>';
  html += `<p style="color:#8b8ba7;font-size:13px;margin:0 0 20px;">Méta-synthèse croisée sur ${esc(nbVideos)} vidéos${statsReelles ? ' · pondérée par tes stats réelles' : ' · basée sur les scores d\'analyse'}.</p>`;

  if (recette) {
    html += '<div style="background:rgba(124,77,255,0.12);border-left:3px solid #7c4dff;border-radius:8px;padding:14px 16px;margin-bottom:20px;">';
    html += '<div style="font-size:12px;text-transform:uppercase;letter-spacing:1px;color:#b39ddb;margin-bottom:6px;">🎯 Ta recette personnelle</div>';
    html += `<div style="color:#e8e8f0;font-size:15px;line-height:1.5;">${esc(recette)}</div>`;
    html += '</div>';
  }

  // Patterns gagnants
  html += '<div style="margin-bottom:20px;">';
  html += '<h3 style="font-size:15px;color:#4caf50;margin:0 0 12px;">✅ Patterns gagnants — à reproduire</h3>';
  if (gagnants.length) {
    gagnants.forEach((p) => {
      html += '<div style="background:rgba(76,175,80,0.08);border:1px solid rgba(76,175,80,0.25);border-radius:10px;padding:14px;margin-bottom:10px;">';
      html += `<div style="font-weight:600;color:#fff;font-size:14px;">${esc(p.pattern || '')}`;
      if (p.occurrences) html += `<span style="color:#8b8ba7;font-weight:400;font-size:12px;"> · ${esc(p.occurrences)} vidéos</span>`;
      html += '</div>';
      if (p.preuve) html += `<div style="color:#b8c5b9;font-size:13px;margin-top:6px;">📊 ${esc(p.preuve)}</div>`;
      if (p.conseil) html += `<div style="color:#a5d6a7;font-size:13px;margin-top:6px;">💡 ${esc(p.conseil)}</div>`;
      html += '</div>';
    });
  } else {
    html += '<p style="color:#8b8ba7;font-size:13px;">Aucun pattern gagnant récurrent détecté pour l\'instant.</p>';
  }
  html += '</div>';

  // Patterns perdants
  html += '<div style="margin-bottom:8px;">';
  html += '<h3 style="font-size:15px;color:#ff7043;margin:0 0 12px;">⚠️ Patterns à corriger — risque pour l\'algo TikTok Shop</h3>';
  if (perdants.length) {
    perdants.forEach((p) => {
      html += '<div style="background:rgba(255,112,67,0.08);border:1px solid rgba(255,112,67,0.25);border-radius:10px;padding:14px;margin-bottom:10px;">';
      html += `<div style="font-weight:600;color:#fff;font-size:14px;">${esc(p.pattern || '')}`;
      if (p.occurrences) html += `<span style="color:#8b8ba7;font-weight:400;font-size:12px;"> · ${esc(p.occurrences)} vidéos</span>`;
      html += '</div>';
      if (p.risque_algo) html += `<div style="color:#ffccbc;font-size:13px;margin-top:6px;">🚨 ${esc(p.risque_algo)}</div>`;
      if (p.correction) html += `<div style="color:#ffab91;font-size:13px;margin-top:6px;">🔧 ${esc(p.correction)}</div>`;
      html += '</div>';
    });
  } else {
    html += '<p style="color:#8b8ba7;font-size:13px;">Aucun pattern pénalisant récurrent détecté. 👍</p>';
  }
  html += '</div>';

  if (priorite) {
    html += '<div style="background:rgba(255,193,7,0.1);border-left:3px solid #ffc107;border-radius:8px;padding:14px 16px;margin-top:16px;">';
    html += '<div style="font-size:12px;text-transform:uppercase;letter-spacing:1px;color:#ffd54f;margin-bottom:6px;">🏆 Priorité de coaching</div>';
    html += `<div style="color:#e8e8f0;font-size:14px;line-height:1.5;">${esc(priorite)}</div>`;
    html += '</div>';
  }

  html += '</div>';
  section.innerHTML = html;
  section.style.display = 'block';
}

// 🆕 Render Contexte Temporel (saisonnalité + événements)
// Chip discret intégré au bloc Potentiel Viral : signal saisonnier minimal,
// pas de section dédiée. Affiché uniquement si l'IA a renvoyé un signal clair
// ou si le backend a calculé un momentum non-evergreen.
function renderContexteTemporel(ct) {
  const chip = document.getElementById('viral-timing-chip');
  if (!chip) return;
  if (!ct || typeof ct !== 'object') {
    chip.style.display = 'none';
    return;
  }

  // Priorité au momentum déterministe (backend) → puis reco IA → puis statut saison
  const momentum = (ct.momentum_status || '').trim();
  const reco = (ct.recommandation_publication
                || (ct.fenetre_publication && ct.fenetre_publication.moment_optimal)
                || '').trim();
  const evt = ct.evenement_booster;

  // Ne pas afficher si purement evergreen sans event ni reco utile
  const isEvergreen = momentum.toLowerCase().includes('evergreen');
  const hasEvent = evt && evt.label && evt.dans_fenetre_optimale;
  if (isEvergreen && !hasEvent && !reco) {
    chip.style.display = 'none';
    return;
  }

  // Couleur selon le signal momentum
  let bg = 'rgba(255,255,255,.12)';
  let icon = '⏱️';
  if (momentum.includes('Pic de Saison')) { icon = '🔥'; bg = 'rgba(239,68,68,.20)'; }
  else if (momentum.includes("Phase d'Inception")) { icon = '✨'; bg = 'rgba(34,197,94,.20)'; }
  else if (momentum.includes('Fin de Tendance')) { icon = '⏳'; bg = 'rgba(245,158,11,.20)'; }
  else if (momentum.includes('Hors-Saison')) { icon = '⚠️'; bg = 'rgba(220,38,38,.22)'; }

  // Texte affiché : momentum (priorité) → sinon reco IA → sinon event proche
  let text = '';
  if (momentum && !isEvergreen) {
    // Extraire la première phrase du momentum (avant les ":" ou les "[mot-clé...")
    const cleaned = momentum.split('[')[0].trim();
    const firstSentence = cleaned.split(/[:.]/)[0].trim();
    text = firstSentence;
    const detail = cleaned.split(':')[1];
    if (detail) text += ' — ' + detail.replace(/\s*\.$/, '').trim();
  } else if (hasEvent) {
    text = `${evt.label} dans ${evt.jours_avant}j — fenêtre de publication idéale`;
  } else if (reco) {
    text = reco;
  }

  if (!text) {
    chip.style.display = 'none';
    return;
  }

  chip.style.background = bg;
  chip.style.display = 'block';
  chip.innerHTML = `<span style="margin-right:6px">${icon}</span>${escapeHtml(text)}`;
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
  if (n >= 7) return '#059669';
  if (n >= 5) return '#D97706';
  return '#DC2626';
}

// ── COACHING VERROUILLÉ ──────────────────────────────────────
function showLockedCoachingSection(firstCoachingLine) {
  const section = document.getElementById('locked-coaching-section') || document.createElement('section');
  if (!section.id) {
    section.id = 'locked-coaching-section';
    section.className = 'section';
    const resultsSection = document.getElementById('results-section');
    if (resultsSection) resultsSection.appendChild(section);
  }

  section.innerHTML = `
    <div style="background:linear-gradient(135deg,rgba(212,175,55,.1),rgba(37,99,235,.1));border:1px solid rgba(212,175,55,.3);border-radius:12px;padding:20px;position:relative">
      <div style="position:absolute;top:16px;right:16px;font-size:24px">🔐</div>
      <h3 style="margin-top:0;margin-bottom:12px;color:var(--navy)">Coach IA personnalisé</h3>
      <p style="margin:0 0 12px 0;font-size:13px;color:var(--text);line-height:1.5">"${firstCoachingLine}"</p>
      <div style="background:rgba(0,0,0,.03);border-radius:8px;padding:12px;margin:12px 0;border-left:3px solid var(--primary)">
        <div style="font-size:12px;color:var(--muted)">Cette analyse complète est réservée aux plans GOLD & AGENCY</div>
        <div style="font-size:12px;color:var(--muted);margin-top:4px">Passez à GOLD pour débloquer le coaching IA personnalisé</div>
      </div>
      <button onclick="document.getElementById('tab-pricing').click()" style="background:var(--primary);color:white;border:none;border-radius:8px;padding:10px 16px;font-weight:600;cursor:pointer;font-size:13px">Voir les plans →</button>
    </div>
  `;
  section.style.display = 'block';
}

// ── SHOW RESULTS (Core rendering function - keep as is) ────────
function showResults(d) {
  console.log('[DEBUG] showResults called with data:', d);
  document.getElementById('loading-section').style.display  = 'none';
  document.getElementById('results-section').style.display  = 'block';

  console.log('[DEBUG] score_global value:', d.score_global);
  document.getElementById('score-global').textContent = d.score_global ?? '—';

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

  // MARKET INTELLIGENCE (verrouillée pour FREE/PRO)
  const marketData = d.donnees_marche;
  const userTier = window.__userInfo?.tier || 'free';
  const isAdmin = window.__userInfo?.is_admin || false;
  const hasMarketAccess = ['gold', 'agency', 'beta'].includes(userTier) || isAdmin;

  const marketIntelligenceSection = document.getElementById('market-intelligence-section');
  if (marketIntelligenceSection && marketData) {
    marketIntelligenceSection.style.display = 'block';

    const lockOverlay = document.getElementById('market-intelligence-lock');
    const content = document.getElementById('market-intelligence-content');

    if (hasMarketAccess) {
      // DÉVERROUILLER pour GOLD+
      if (lockOverlay) lockOverlay.style.display = 'none';
      if (content) content.style.display = 'block';

      const det = d.detection;
      const detectedCategory = det?.produit || '';

      // === CONTEXTE CATÉGORIE ===
      const trendingCategories = (marketData.trending || []).map(p => p.category).filter(Boolean);
      const topCategories = (marketData.top_products || []).map(p => p.category).filter(Boolean);

      let categoryContext = '—';
      if (detectedCategory) {
        const isTrending = trendingCategories.includes(detectedCategory);
        const topCount = topCategories.filter(c => c === detectedCategory).length;

        if (isTrending) {
          categoryContext = `✅ <strong>${detectedCategory}</strong> est EN CROISSANCE rapide en ce moment. Excellente timing pour tester ce produit !`;
        } else if (topCount > 0) {
          categoryContext = `📊 <strong>${detectedCategory}</strong> a ${topCount} produit(s) dans le top. C'est une catégorie stable avec une demande constante.`;
        } else {
          categoryContext = `⚠️ <strong>${detectedCategory}</strong> n'apparaît pas dans les trending actuels. Stratégie : sois plus agressif sur le hook et le CTA.`;
        }
      }
      document.getElementById('market-category-context').innerHTML = categoryContext;

      // === TOP PRODUITS ===
      const topProdsContainer = document.getElementById('market-top-products');
      topProdsContainer.innerHTML = (marketData.top_products || []).map(p => `
        <div class="market-card">
          <div class="market-card-title">${p.title || p.name || '—'}</div>
          <div class="market-card-meta">
            <span class="market-badge hot">🔥 ${p.sold_count || '?'} ventes</span>
          </div>
          <div style="font-size:11px;color:var(--muted)">
            ${p.category || ''} ${p.current_price ? `• ${p.current_price}€` : ''}
          </div>
        </div>
      `).join('');

      // === TRENDING ===
      const trendingContainer = document.getElementById('market-trending');
      trendingContainer.innerHTML = (marketData.trending || []).map(p => `
        <div class="market-card">
          <div class="market-card-title">${p.title || p.name || '—'}</div>
          <div class="market-card-meta">
            <span class="market-badge trend">📈 +${p.growth_percent || '?'}%</span>
          </div>
          <div style="font-size:11px;color:var(--muted)">
            ${p.category || ''} ${p.current_price ? `• ${p.current_price}€` : ''}
          </div>
        </div>
      `).join('');

      // === TOP CREATORS ===
      const creatorsContainer = document.getElementById('market-creators');
      const creatorsByCategory = (marketData.top_creators || []).filter(c =>
        c.primary_category === detectedCategory || !detectedCategory
      );
      creatorsContainer.innerHTML = (creatorsByCategory.length > 0 ? creatorsByCategory : marketData.top_creators || []).map(c => `
        <div class="market-card">
          <div class="market-card-title">@${c.handle || '?'}</div>
          <div class="market-card-meta">
            <span class="market-badge">👥 ${c.followers || '?'}</span>
          </div>
          <div style="font-size:11px;color:var(--muted)">
            ${c.primary_category || '—'}
          </div>
        </div>
      `).join('');

      // === ACTIONS RECOMMANDÉES ===
      let recommendations = '—';
      if (detectedCategory) {
        const score = d.score_global || 0;
        let actions = [];

        if (score < 65) {
          actions.push('🎯 <strong>Score faible</strong> : Ta vidéo ne convainc pas encore. Examine le hook et la rétention en priorité.');
        } else if (score < 75) {
          actions.push('📊 <strong>Score moyen</strong> : Tu es sous la médiane. Focus sur améliorer 1-2 dimensions (hook ou CTA généralement).');
        } else {
          actions.push('✅ <strong>Score bon</strong> : Ta vidéo est compétitive. Test en vraie pour voir les vraies conversions.');
        }

        if (trendingCategories.includes(detectedCategory)) {
          actions.push('🚀 <strong>Trending</strong> : Cette catégorie explose. Sois agressif : publie plusieurs variations rapidement.');
        }

        if (det?.prix_estime) {
          const price = parseFloat(det.prix_estime);
          if (price < 50) {
            actions.push('💰 <strong>Prix bas</strong> : Conversion potentielle rapide (J1-J3). Focus sur volume + urgency.');
          } else if (price < 150) {
            actions.push('💰 <strong>Prix moyen</strong> : Attends J7-J30 pour vraies conclusions. Besoin de proof/testimonials.');
          } else {
            actions.push('💎 <strong>Prix premium</strong> : Très lent. Stratégie : autorité + transformation + rareté.');
          }
        }

        recommendations = actions.map((a, i) => `<div style="margin-bottom:8px;padding:10px;background:var(--surface2);border-radius:8px;border-left:3px solid var(--primary)">${a}</div>`).join('');
      }
      document.getElementById('market-recommendations').innerHTML = recommendations;
    } else {
      // VERROUILLER pour FREE/PRO
      if (lockOverlay) lockOverlay.style.display = 'flex';
      if (content) content.style.display = 'none';
    }
  }

  const vp = d.viral_potential;
  if (vp) {
    document.getElementById('viral-score').textContent      = vp.score ?? '—';
    document.getElementById('viral-prix').textContent       = vp.facteur_prix || '';
    document.getElementById('viral-explication').textContent = vp.explication || '';
    // Chip timing discret intégré au bloc viral (signal saisonnier en contexte)
    renderContexteTemporel(d.contexte_temporel);
  }

  fillList('points-forts',  d.points_forts,     '', true);
  fillList('points-faibles',d.points_ameliorer, '', true);

  const reco = d.recommendations_hooks;
  if (reco) {
    document.getElementById('hook-type-propose').textContent = reco.hook_type_propose || '—';
    document.getElementById('hook-reason').textContent       = reco.raison || '';
    const exList = document.getElementById('hook-examples');
    exList.innerHTML = (reco.exemples_concrets || []).map(e => `<li>${e}</li>`).join('');
  }

  fillList('conseils-list', d.conseils_concrets, '', true);

  const sv = d.structure_vente;
  if (sv) {
    document.getElementById('structure-vente-section').style.display = 'block';

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

    const scoreStrEl = document.getElementById('score-structure');
    if (scoreStrEl) {
      scoreStrEl.textContent = sv.score_structure ?? '—';
      const s = sv.score_structure ?? 0;
      scoreStrEl.style.color = s >= 70 ? 'var(--primary)' : s >= 50 ? 'var(--warning)' : 'var(--danger)';
    }

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

    const amelioEl = document.getElementById('ameliorations-structure');
    if (amelioEl && d.ameliorations_structure?.length) {
      amelioEl.innerHTML = `
        <h3 style="color:var(--warning);margin-bottom:8px">💡 Améliorer le flux de vente</h3>
        <ul class="points-list neg">${(d.ameliorations_structure).map(a => `<li>${a}</li>`).join('')}</ul>`;
    }
  } else {
    document.getElementById('structure-vente-section').style.display = 'none';
  }

  const pc = d.prix_conversion;
  if (pc) {
    document.getElementById('prix-conversion-section').style.display = 'block';
    const prixIdentifie = pc.prix_identifie !== false && pc.montant;
    document.getElementById('pc-montant').textContent = prixIdentifie ? `${pc.montant} €` : '❓ Non identifié';
    const catLabels = { economique: t('cat_economique'), moyen: t('cat_moyen'), premium: t('cat_premium'), inconnu: t('cat_inconnu') };
    if (!prixIdentifie) {
      document.getElementById('pc-categorie').textContent = '— (prix manquant)';
      document.getElementById('pc-categorie').style.color = 'var(--muted)';
    } else {
      document.getElementById('pc-categorie').textContent = catLabels[pc.categorie] || pc.categorie || '—';
      document.getElementById('pc-categorie').style.color = '';
    }
    const pot = pc.potentiel_conversion || {};
    const delaiLabels = { j7: t('delai_j7'), j30: t('delai_j30'), inconnu: '—' };
    document.getElementById('pc-delai').textContent = prixIdentifie
      ? (delaiLabels[pot.temps_attendre] || pot.temps_attendre || '—')
      : 'Non évaluable';
    document.getElementById('pc-conseil').textContent = pc.conseil_prix || '—';
    document.getElementById('pc-disclaimer').textContent = d.disclaimer_realisme || '⚠️ Cette analyse est un guide, pas une certitude. L\'algo TikTok surprend toujours.';
  } else {
    document.getElementById('prix-conversion-section').style.display = 'none';
  }

  if (d.transcript) {
    document.getElementById('transcript-section').style.display = 'block';
    document.getElementById('transcript-text').textContent = d.transcript;
  }

  if (d.verdict) {
    document.getElementById('verdict-section').style.display = 'block';
    document.getElementById('verdict-text').textContent = d.verdict;
  }

  // COACHING: verrouillé pour FREE/PRO, complet pour GOLD/AGENCY
  const userTierForCoaching = window.__userInfo?.tier || 'free';
  const isFreemium = userTierForCoaching === 'free' || userTierForCoaching === 'pro';
  if (isFreemium && d.conseils_concrets?.length > 0) {
    showLockedCoachingSection(d.conseils_concrets[0]);
  } else if (!isFreemium && d.conseils_concrets?.length > 0) {
    const coachSection = document.getElementById('coaching-section') || document.createElement('section');
    if (!coachSection.id) {
      coachSection.id = 'coaching-section';
      coachSection.className = 'section';
      document.getElementById('results-section').appendChild(coachSection);
    }
    coachSection.innerHTML = `
      <h2>🤖 Coach IA personnalisé</h2>
      <ul class="points-list" style="border-left:3px solid var(--primary)">
        ${(d.conseils_concrets || []).map(c => `<li>${c}</li>`).join('')}
      </ul>
    `;
    coachSection.style.display = 'block';
  }

  // 👑 STRATÉGIE DE CONVERSION (PREMIUM) — Gold / Agency / Beta uniquement.
  // La donnée n'est générée côté serveur QUE pour ces plans ; sinon on affiche
  // un composant d'upsell pour pousser vers Gold.
  renderPremiumStrategy(d);

  // 🏆 Structures gagnantes (Gold / Agency) : affiché quand le serveur a renvoyé
  // un payload structures_gagnantes (score < 75 + plan habilité).
  renderWinningStructures(d);

  // Plan Free : on garde la notation visible, on floute le reste + CTA conversion.
  applyFreemiumBlur();

  // 🎚️ Slider horizontal : chaque section devient une slide (glisser vers la
  // gauche). Le Coach IA est placé en dernière slide ; le CTA "nouvelle analyse"
  // + l'export passent SOUS le slider. Construit en tout dernier pour englober
  // les sections premium/upsell ajoutées dynamiquement ci-dessus.
  buildAnalysisSlider();

  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ── 🎚️ Slider d'analyse (carousel horizontal scroll-snap) ────────────
// Idempotent : on désassemble un slider existant avant de reconstruire, pour
// supporter les ré-analyses successives sans empiler les wrappers.
function unwrapAnalysisSlider() {
  const results = document.getElementById('results-section');
  if (!results) return;
  const slider = document.getElementById('analysis-slider');
  if (slider) {
    slider.querySelectorAll('.analysis-slide').forEach(slide => {
      while (slide.firstChild) results.appendChild(slide.firstChild);
    });
    slider.remove();
  }
  const footer = document.getElementById('slider-footer');
  if (footer) {
    while (footer.firstChild) results.appendChild(footer.firstChild);
    footer.remove();
  }
}

function buildAnalysisSlider() {
  const results = document.getElementById('results-section');
  if (!results) return;

  // 1) Repartir d'un état propre (les sections reviennent enfants directs)
  unwrapAnalysisSlider();

  // 2) Trier les enfants directs : slides (visibles) vs footer (CTA + export)
  const footerEls = [];
  const slideEls = [];
  Array.from(results.children).forEach(el => {
    if (el.id === 'analysis-slider' || el.id === 'slider-footer') return;
    if (el.hasAttribute('data-slider-footer')) { footerEls.push(el); return; }
    if (window.getComputedStyle(el).display === 'none') return;  // sections masquées
    // Anti-slide-vide : on écarte les sections visibles mais sans contenu
    // (ni texte, ni média) qui apparaîtraient comme des pages blanches.
    const hasText = (el.textContent || '').trim().length > 0;
    const hasMedia = el.querySelector('img, canvas, svg, video');
    if (!hasText && !hasMedia) return;
    slideEls.push(el);
  });

  // 3) Coach IA toujours en dernière slide
  const coachIdx = slideEls.findIndex(
    el => el.id === 'coaching-section' || el.id === 'locked-coaching-section'
  );
  if (coachIdx > -1) {
    const [coach] = slideEls.splice(coachIdx, 1);
    slideEls.push(coach);
  }

  if (slideEls.length === 0) return;

  // 4) Construire la structure du slider
  const slider = document.createElement('div');
  slider.id = 'analysis-slider';
  const viewport = document.createElement('div');
  viewport.className = 'slider-viewport';
  const track = document.createElement('div');
  track.className = 'slider-track';
  viewport.appendChild(track);
  slider.appendChild(viewport);

  const slideWrappers = [];
  slideEls.forEach(el => {
    const slide = document.createElement('div');
    slide.className = 'analysis-slide';
    slide.appendChild(el);
    track.appendChild(slide);
    slideWrappers.push(slide);
  });

  // 5) Navigation (flèches + points + compteur)
  const nav = document.createElement('div');
  nav.className = 'slider-nav';
  nav.innerHTML = `
    <button class="slider-arrow" id="slider-prev" type="button" aria-label="Précédent">‹</button>
    <div class="slider-dots" id="slider-dots"></div>
    <div class="slider-counter" id="slider-counter"></div>
    <button class="slider-arrow" id="slider-next" type="button" aria-label="Suivant">›</button>
  `;
  slider.appendChild(nav);

  const hint = document.createElement('div');
  hint.className = 'slider-hint';
  hint.textContent = '← Glissez pour naviguer dans l’analyse →';
  slider.appendChild(hint);

  // 6) Footer SOUS le slider (nouvelle analyse + export)
  const footer = document.createElement('div');
  footer.id = 'slider-footer';
  footerEls.forEach(el => footer.appendChild(el));

  results.appendChild(slider);
  if (footerEls.length) results.appendChild(footer);

  // 7) Points cliquables
  const dotsWrap = nav.querySelector('#slider-dots');
  slideEls.forEach((_, i) => {
    const dot = document.createElement('button');
    dot.type = 'button';
    dot.className = 'slider-dot' + (i === 0 ? ' active' : '');
    dot.setAttribute('aria-label', `Section ${i + 1}`);
    dot.addEventListener('click', () => sliderGoTo(i));
    dotsWrap.appendChild(dot);
  });

  // 8) État + handlers
  window.__slider = { index: 0, count: slideWrappers.length, viewport, slides: slideWrappers };
  nav.querySelector('#slider-prev').addEventListener('click', () => sliderGoTo(window.__slider.index - 1));
  nav.querySelector('#slider-next').addEventListener('click', () => sliderGoTo(window.__slider.index + 1));

  // Synchronise l'état actif lors d'un swipe / scroll manuel
  let scrollTO;
  viewport.addEventListener('scroll', () => {
    clearTimeout(scrollTO);
    scrollTO = setTimeout(() => {
      const i = Math.round(viewport.scrollLeft / viewport.clientWidth);
      sliderSetActive(i);
    }, 80);
  });

  // Recalcule la hauteur sur rotation / redimensionnement de l'écran
  if (!window.__sliderResizeBound) {
    window.__sliderResizeBound = true;
    window.addEventListener('resize', () => {
      if (window.__slider) updateSliderHeight(window.__slider.index);
    });
  }

  // La hauteur dépend du rendu final (images/polices) → on attend un frame
  requestAnimationFrame(() => sliderSetActive(0));
}

// Adapte la hauteur du viewport à la slide active : pas de grand vide blanc
// sous les sections courtes, et les sections plus hautes que l'écran défilent
// verticalement à l'intérieur de leur slide.
function updateSliderHeight(i) {
  const s = window.__slider;
  if (!s || !s.slides) return;
  const slide = s.slides[i];
  if (!slide) return;
  const maxH = Math.round(window.innerHeight * 0.74);   // garde de la place pour la nav
  const natural = slide.scrollHeight;
  const h = Math.min(natural, maxH);
  s.viewport.style.height = h + 'px';
}

function sliderGoTo(i) {
  const s = window.__slider;
  if (!s) return;
  i = Math.max(0, Math.min(i, s.count - 1));
  s.viewport.scrollTo({ left: i * s.viewport.clientWidth, behavior: 'smooth' });
  sliderSetActive(i);
}

function sliderSetActive(i) {
  const s = window.__slider;
  if (!s) return;
  i = Math.max(0, Math.min(i, s.count - 1));
  s.index = i;
  updateSliderHeight(i);
  document.querySelectorAll('#slider-dots .slider-dot')
    .forEach((d, idx) => d.classList.toggle('active', idx === i));
  const counter = document.getElementById('slider-counter');
  if (counter) counter.textContent = `${i + 1} / ${s.count}`;
  const prev = document.getElementById('slider-prev');
  const next = document.getElementById('slider-next');
  if (prev) prev.disabled = (i === 0);
  if (next) next.disabled = (i === s.count - 1);
}

// ── Flou des fonctionnalités verrouillées pour le plan Free ──────────
function applyFreemiumBlur() {
  const resultsSection = document.getElementById('results-section');
  if (!resultsSection) return;

  const locks = resultsSection.querySelectorAll('[data-free-lock]');

  // Nettoie l'état précédent (re-analyse / changement de plan)
  document.getElementById('freemium-unlock-cta')?.remove();
  locks.forEach(el => el.classList.remove('freemium-locked'));

  const tier = window.__userInfo?.tier || 'free';
  if (tier !== 'free') return;   // Pro / Gold / Agency / Beta / Admin : aucun flou

  let firstLocked = null;
  locks.forEach(el => {
    el.classList.add('freemium-locked');
    if (!firstLocked) firstLocked = el;
  });

  // Un seul bandeau de conversion, juste avant la première section floutée
  if (firstLocked) {
    const cta = document.createElement('div');
    cta.id = 'freemium-unlock-cta';
    cta.className = 'section freemium-cta';
    cta.innerHTML = `
      <div class="fc-icon">🔒</div>
      <div class="fc-title">Choisissez votre plan pour débloquer toutes les fonctionnalités</div>
      <div class="fc-sub">Conseils IA personnalisés, structure de vente, potentiel de conversion, détection produit et bien plus — passez à un plan payant pour accéder à l'analyse complète.</div>
      <button class="fc-btn" onclick="switchTab('pricing')">Voir les plans →</button>
    `;
    firstLocked.parentNode.insertBefore(cta, firstLocked);
  }
}

// ── 👑 Stratégie de Conversion (Premium) + Upsell Gold ───────────────
function renderPremiumStrategy(d) {
  const resultsSection = document.getElementById('results-section');
  if (!resultsSection) return;

  // Nettoie un éventuel rendu précédent
  document.getElementById('premium-strategy-section')?.remove();
  document.getElementById('gold-upsell-section')?.remove();

  const sp = d.strategie_conversion_premium;

  if (sp && (sp.persona || sp.script_tiktok)) {
    // → Plan habilité : on affiche la stratégie complète, style doré premium
    const persona = sp.persona || {};
    const script = sp.script_tiktok || {};
    const declencheurs = (persona.declencheurs_achat || [])
      .map(x => `<li>${escapeHtml(x)}</li>`).join('');

    const sec = document.createElement('section');
    sec.id = 'premium-strategy-section';
    sec.className = 'section premium-strategy';
    sec.innerHTML = `
      <h2 style="display:flex;align-items:center;gap:8px;">${escapeHtml(sp.titre || '👑 Stratégie de Conversion (Premium)')}</h2>
      ${sp.produit_identifie ? `<p class="premium-product">🛍️ Produit identifié : <strong>${escapeHtml(sp.produit_identifie)}</strong></p>` : ''}

      <div class="premium-block">
        <h3>🎯 Persona cible</h3>
        ${persona.profil ? `<p><strong>Profil :</strong> ${escapeHtml(persona.profil)}</p>` : ''}
        ${persona.psychologie ? `<p><strong>Psychologie :</strong> ${escapeHtml(persona.psychologie)}</p>` : ''}
        ${declencheurs ? `<p><strong>Déclencheurs d'achat :</strong></p><ul class="premium-list">${declencheurs}</ul>` : ''}
      </div>

      <div class="premium-block">
        <h3>🎬 Script TikTok clé en main</h3>
        ${script.hook_0_3s ? `<p><span class="premium-tag">Hook 0-3s</span> ${escapeHtml(script.hook_0_3s)}</p>` : ''}
        ${script.demonstration_organique ? `<p><span class="premium-tag">Démonstration</span> ${escapeHtml(script.demonstration_organique)}</p>` : ''}
        ${script.call_to_action ? `<p><span class="premium-tag">CTA Shop</span> ${escapeHtml(script.call_to_action)}</p>` : ''}
      </div>
    `;
    resultsSection.appendChild(sec);
    return;
  }

  // → Plan free / pro : composant d'upsell statique attractif
  const tier = window.__userInfo?.tier || 'free';
  if (tier === 'free' || tier === 'pro' || tier === 'basic') {
    const up = document.createElement('section');
    up.id = 'gold-upsell-section';
    up.className = 'section gold-upsell';
    up.innerHTML = `
      <div class="gold-upsell-inner">
        <div class="gold-upsell-icon">🔒</div>
        <div class="gold-upsell-text">
          <strong>Passez au plan Gold</strong> pour que notre IA identifie votre audience cible
          et rédige le script de vente parfait pour ce produit.
        </div>
        <button class="gold-upsell-btn" onclick="switchTab('pricing')">Débloquer Gold 👑</button>
      </div>
    `;
    resultsSection.appendChild(up);
  }
}

// 🏆 STRUCTURES GAGNANTES — réservé Gold / Agency. Le serveur ne renvoie le
// payload `structures_gagnantes` QUE si l'analyse < 75 et que le plan est habilité.
function renderWinningStructures(d) {
  const resultsSection = document.getElementById('results-section');
  if (!resultsSection) return;
  document.getElementById('winning-structures-section')?.remove();

  const ws = d.structures_gagnantes;
  if (!ws || !Array.isArray(ws.items) || ws.items.length === 0) return;

  const cards = ws.items.map(it => {
    const examples = (it.hook_examples || [])
      .map(x => `<li>${escapeHtml(x)}</li>`).join('');
    const s = it.script || {};
    const scriptHtml = (s.hook_0_3s || s.demonstration_organique || s.call_to_action) ? `
      <div class="winning-script">
        ${s.hook_0_3s ? `<p><span class="premium-tag">Hook 0-3s</span> ${escapeHtml(s.hook_0_3s)}</p>` : ''}
        ${s.demonstration_organique ? `<p><span class="premium-tag">Démonstration</span> ${escapeHtml(s.demonstration_organique)}</p>` : ''}
        ${s.call_to_action ? `<p><span class="premium-tag">CTA Shop</span> ${escapeHtml(s.call_to_action)}</p>` : ''}
      </div>` : '';
    const priceTxt = (it.price != null) ? ` · ${escapeHtml(String(it.price))} €` : '';
    return `
      <div class="winning-card">
        <div class="winning-card-head">
          <span class="winning-score">${escapeHtml(String(it.score ?? '?'))}/100</span>
          <span class="winning-product">${escapeHtml(it.product || 'Produit similaire')}${priceTxt}</span>
        </div>
        ${it.hook_type ? `<p class="winning-hook-type">📌 Accroche : <strong>${escapeHtml(it.hook_type)}</strong></p>` : ''}
        ${examples ? `<ul class="winning-examples">${examples}</ul>` : ''}
        ${scriptHtml}
      </div>`;
  }).join('');

  const sec = document.createElement('section');
  sec.id = 'winning-structures-section';
  sec.className = 'section winning-structures';
  sec.innerHTML = `
    <h2>${escapeHtml(ws.titre || '🏆 Les structures qui ont mieux fonctionné')}</h2>
    <p class="winning-intro">${escapeHtml(ws.intro || '')}</p>
    <div class="winning-grid">${cards}</div>
    <p class="winning-advice">💡 Refais ta vidéo en t'appuyant sur ces structures déjà éprouvées : elles ont dépassé 75 sur des produits comparables.</p>
  `;
  resultsSection.appendChild(sec);
}

function fillList(id, items, icon, noIcon) {
  const el = document.getElementById(id);
  if (!el) return;
  el.innerHTML = (items || []).map(t => `<li>${noIcon ? '' : icon}${t}</li>`).join('');
}

// ── RESET ────────────────────────────────────────────────────
function resetAnalysis() {
  selectedFile = null; currentData = null;
  unwrapAnalysisSlider();   // remet les sections à plat avant de masquer / ré-analyser
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
  document.getElementById('premium-strategy-section')?.remove();
  document.getElementById('gold-upsell-section')?.remove();
  document.getElementById('winning-structures-section')?.remove();
  document.getElementById('freemium-unlock-cta')?.remove();
  document.querySelectorAll('#results-section [data-free-lock]').forEach(el => el.classList.remove('freemium-locked'));
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ── USAGE COUNTER ─────────────────────────────────────────────
function getUsage()       { return parseInt(localStorage.getItem(USAGE_KEY) || '0', 10); }
function incrementUsage() { localStorage.setItem(USAGE_KEY, getUsage() + 1); updateUsageCounter(); }
function updateUsageCounter() {
  const n  = getUsage();
  const el = document.getElementById('usage-count');
  if (el) el.textContent = `${n} / ${FREE_LIMIT}`;
}

function updateUsageBadge(usage) {
  if (!usage) return;
  const tierLabels = { free:'FREE', pro:'PRO', gold:'GOLD ⭐', agency:'AGENCY' };
  const label = tierLabels[usage.tier] || 'FREE';
  const badge = document.getElementById('user-email');
  if (badge && usage.email) {
    badge.textContent = usage.email;
  }
  const statusEl = document.getElementById('auth-status');
  if (statusEl && usage.tier && usage.tier !== 'free') {
    statusEl.innerHTML = `<span style="color:var(--primary);font-weight:700">${label}</span>`;
  }
  const upgradeBtn = document.getElementById('btn-auth');
  if (upgradeBtn && usage.tier && usage.tier !== 'free') {
    upgradeBtn.textContent = '⚙️ Mon abonnement';
    upgradeBtn.onclick = openCustomerPortal;
  }
}

// ── ECHOTIK MARKET DATA ───────────────────────────────────────
function _productCard(p, badgeHtml) {
  const link    = p.product_url || '#';
  const img     = p.image_url   || '';
  const target  = link !== '#' ? 'target="_blank" rel="noopener"' : '';
  return `
    <a href="${link}" ${target} style="display:flex;align-items:center;gap:12px;padding:10px 12px;background:var(--surface2);border-radius:12px;text-decoration:none;color:inherit;transition:box-shadow .15s" onmouseover="this.style.boxShadow='var(--shadow)'" onmouseout="this.style.boxShadow='none'">
      ${img ? `<img src="${img}" alt="" style="width:54px;height:54px;object-fit:cover;border-radius:8px;flex-shrink:0" loading="lazy" onerror="this.style.display='none'">` : `<div style="width:54px;height:54px;border-radius:8px;background:var(--border);flex-shrink:0;display:flex;align-items:center;justify-content:center;font-size:20px">🛍️</div>`}
      <div style="flex:1;min-width:0">
        <div style="font-size:13px;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">${p.title || '—'}</div>
        <div style="font-size:11px;color:var(--muted);margin-top:3px">${p.category || ''} · ${p.current_price ? p.current_price + '€' : '—'}</div>
      </div>
      <div style="text-align:right;white-space:nowrap;flex-shrink:0">${badgeHtml}</div>
    </a>`;
}

function renderMarketSection(data) {
  const topList = document.getElementById('market-top-list');
  if (topList && data.top_products?.length) {
    topList.innerHTML = data.top_products.slice(0, 8).map(p =>
      _productCard(p, `<div style="font-size:13px;font-weight:700;color:var(--navy)">${(p.sold_count || 0).toLocaleString()}</div><div style="font-size:10px;color:var(--muted)">ventes</div>`)
    ).join('');
  }

  const trendList = document.getElementById('market-trend-list');
  if (trendList && data.trending?.length) {
    trendList.innerHTML = data.trending.slice(0, 8).map(p =>
      _productCard(p, `<div style="font-size:13px;font-weight:700;color:#059669">+${p.growth_percent || 0}%</div><div style="font-size:10px;color:var(--muted)">croissance</div>`)
    ).join('');
  }

  const creatorList = document.getElementById('market-creator-list');
  if (creatorList && data.top_creators?.length) {
    creatorList.innerHTML = data.top_creators.slice(0, 6).map(c => {
      const profileLink = c.profile_url || '#';
      const target = profileLink !== '#' ? 'target="_blank" rel="noopener"' : '';
      return `
        <a href="${profileLink}" ${target} style="display:flex;align-items:center;gap:12px;padding:10px 12px;background:var(--surface2);border-radius:12px;text-decoration:none;color:inherit;transition:box-shadow .15s" onmouseover="this.style.boxShadow='var(--shadow)'" onmouseout="this.style.boxShadow='none'">
          <div style="width:44px;height:44px;border-radius:50%;background:linear-gradient(135deg,var(--primary),var(--navy));display:flex;align-items:center;justify-content:center;font-size:18px;flex-shrink:0">🎯</div>
          <div style="flex:1;min-width:0">
            <div style="font-size:13px;font-weight:600">@${c.handle || '—'}</div>
            <div style="font-size:11px;color:var(--muted);margin-top:3px">${c.primary_category || ''}</div>
          </div>
          <div style="text-align:right;flex-shrink:0">
            <div style="font-size:13px;font-weight:700;color:var(--navy)">${c.followers ? (c.followers >= 1000000 ? (c.followers/1000000).toFixed(1)+'M' : (c.followers/1000).toFixed(0)+'k') : '—'}</div>
            <div style="font-size:10px;color:var(--muted)">followers</div>
          </div>
        </a>`;
    }).join('');
  }
}

function switchMarketTab(tab) {
  ['top', 'trend', 'creator'].forEach(t => {
    const content = document.getElementById(`market-${t}-content`);
    const btn     = document.getElementById(`market-tab-${t}`);
    if (content) content.style.display = t === tab ? 'block' : 'none';
    if (btn) {
      btn.style.background = t === tab ? 'var(--navy)' : 'var(--surface2)';
      btn.style.color      = t === tab ? '#fff' : 'var(--text)';
    }
  });
}

// ── HISTORY ──────────────────────────────────────────────────
function getHistory() {
  try { return JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]'); } catch { return []; }
}

// Map product names to categories for market trend analysis
function detectProductCategory(productName) {
  if (!productName) return null;
  const name = productName.toLowerCase();

  // Keywords organized by category with priority scoring
  const categoryKeywords = {
    'beaute': {
      high: ['maquillage', 'makeup', 'fond de teint', 'rouge à lèvres', 'mascara', 'cosmetic'],
      medium: ['sérum', 'crème', 'ombre', 'primer', 'BB cream', 'palette', 'poudre', 'blush', 'crayon', 'eyeliner']
    },
    'fashion': {
      high: ['vêtement', 'robe', 'pantalon', 'chemise', 'veste', 'chaussure', 'shoe', 'dress', 'shirt'],
      medium: ['sac', 'accessoire', 'montre', 'bijou', 'ceinture', 'pull', 'jean', 'blazer', 'sneaker']
    },
    'tech': {
      high: ['téléphone', 'phone', 'écouteur', 'earbuds', 'appareil', 'gadget', 'tech', 'watch'],
      medium: ['batterie', 'chargeur', 'charger', 'électronique', 'smart', 'ordinateur', 'laptop', 'tablette']
    },
    'fitness': {
      high: ['haltère', 'fitness', 'workout', 'gym', 'exercise', 'protéine', 'whey'],
      medium: ['tapis', 'bande', 'équipement', 'yoga', 'supplément', 'dumbbell']
    },
    'sante': {
      high: ['vitamine', 'vitamin', 'supplément', 'santé', 'health', 'wellness', 'médicament'],
      medium: ['pilule', 'complément', 'capsule', 'comprimé']
    },
    'complement_sante': {
      high: ['protéine', 'whey', 'créatine', 'collagène', 'oméga', 'bcaa', 'acides aminés'],
      medium: ['supplément', 'complément', 'poudre protéine', 'shake']
    },
    'electromenager': {
      high: ['cuisinière', 'frigo', 'aspirateur', 'lave-vaisselle', 'micro-onde', 'appliance', 'kitchen'],
      medium: ['chauffage', 'ventilateur', 'lampe', 'électroménager', 'cuiseur']
    },
  };

  // Score each category based on keyword matches
  let bestCategory = null;
  let bestScore = 0;

  for (const [category, keywords] of Object.entries(categoryKeywords)) {
    let score = 0;

    // High priority keywords = 3 points
    if (keywords.high.some(kw => name.includes(kw))) {
      score += 3;
    }

    // Medium priority keywords = 1 point
    if (keywords.medium.some(kw => name.includes(kw))) {
      score += 1;
    }

    if (score > bestScore) {
      bestScore = score;
      bestCategory = category;
    }
  }

  return bestCategory;
}

function saveToHistory(data, filename) {
  if (!data) return;
  const entries = getHistory();

  // Dédup robuste : le serveur ne renvoie PAS d'identifiant stable (data.id est
  // toujours undefined), donc l'ancien test `entries[0]?.id === data.id`
  // valait `undefined === undefined` = true et bloquait TOUTE sauvegarde.
  // On déduplique désormais sur une signature de contenu, ce qui évite aussi le
  // double enregistrement (auto-save SSE + clic « Sauvegarder »).
  const sig = `${filename || ''}|${data.score_global ?? ''}|${(data.verdict || '').slice(0, 40)}`;
  if (entries[0]?._sig === sig) return;

  // Detect product category from detected product name
  const productName = data.detection?.produit || null;
  const detectedCategory = detectProductCategory(productName);

  entries.unshift({
    id:                    Date.now(),
    _sig:                  sig,
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
    product_category:      detectedCategory,  // Add detected category
    product_name:          productName
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
    <button onclick="clearHistory()" style="background:none;border:1px solid rgba(239,68,68,.25);color:#DC2626;border-radius:6px;padding:4px 10px;font-size:11px;cursor:pointer">${t('hist_clear')}</button>
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

async function clearHistory() {
  if (!(await showConfirm(t('hist_confirm')))) return;
  localStorage.removeItem(STORAGE_KEY);
  updateHistoryBadge(); renderHistory();
}

// ── ACCOUNT PAGE ─────────────────────────────────────────────
function renderAccountPage() {
  const container = document.getElementById('account-content');
  if (!container) return;

  const userInfo = window.__userInfo || {};
  const tierLabels = { free: 'Gratuit', pro: 'Pro', gold: 'Gold ⭐', agency: 'Agency', beta: 'Beta 🎁', admin: 'Admin' };
  const tierColors = { free: '#6B7280', pro: '#2563EB', gold: '#D97706', agency: '#7C3AED', beta: '#059669', admin: '#DC2626' };
  const tierDescriptions = {
    free: '3 analyses par mois • Pas de coaching IA • Support basique',
    pro: '20 analyses par mois • Pas de coaching IA • Support par email',
    gold: '25 analyses par jour • Coaching IA complet • Tendances marché • Support prioritaire',
    agency: '125 analyses par jour • Coaching IA complet • Tendances marché • Support 24/7',
    beta: 'Accès illimité • Coaching IA complet • Tendances marché • Support VIP',
    admin: 'Accès illimité • Panneau d\'admin • Support complet'
  };

  const tier = userInfo.tier || 'free';
  const tierLabel = tierLabels[tier] || tier.toUpperCase();
  const tierColor = tierColors[tier] || '#6B7280';
  const tierDesc = tierDescriptions[tier] || '';

  let html = `
    <div class="section">
      <h2>👤 Mon compte</h2>

      <!-- User info -->
      <div style="background:var(--bg);border-radius:12px;padding:16px;margin-bottom:16px;border:1px solid var(--border)">
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">
          <div>
            <div style="font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:.05em;margin-bottom:4px">Email</div>
            <div style="font-size:15px;font-weight:600;color:var(--text)">${SESSION.email || '—'}</div>
          </div>
          <div>
            <div style="font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:.05em;margin-bottom:4px">Plan actuel</div>
            <div style="display:inline-block;background:${tierColor};color:#fff;padding:4px 12px;border-radius:20px;font-size:13px;font-weight:700">${tierLabel}</div>
          </div>
        </div>
      </div>

      <!-- Plan details -->
      <div style="background:linear-gradient(135deg,rgba(212,175,55,.07),rgba(37,99,235,.04));border:1px solid rgba(212,175,55,.22);border-radius:12px;padding:16px;margin-bottom:16px">
        <div style="font-size:13px;font-weight:600;color:var(--text);margin-bottom:8px">ℹ️ Inclusions du plan</div>
        <div style="font-size:13px;color:var(--text);line-height:1.6">${tierDesc}</div>
      </div>

      <!-- Usage -->
      <div style="background:var(--bg);border-radius:12px;padding:16px;margin-bottom:16px;border:1px solid var(--border)">
        <div style="font-size:13px;font-weight:600;color:var(--text);margin-bottom:12px">📊 Utilisation</div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">
          <div>
            <div style="font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:.05em;margin-bottom:4px">Analyses ce mois</div>
            <div style="font-size:24px;font-weight:700;color:var(--navy)">${getUsage()}</div>
          </div>
          <div>
            <div style="font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:.05em;margin-bottom:4px">Limite</div>
            <div style="font-size:24px;font-weight:700;color:${tier === 'free' || tier === 'pro' ? 'var(--warning)' : 'var(--success)'}">${tier === 'free' ? '3' : tier === 'pro' ? '20' : '∞'}</div>
          </div>
        </div>
      </div>

      <!-- Connexion compte TikTok -->
      <div style="background:var(--bg);border-radius:12px;padding:16px;margin-bottom:16px;border:1px solid var(--border)">
        <div style="font-size:13px;font-weight:600;color:var(--text);margin-bottom:8px">🎵 Mon compte TikTok</div>
        <div id="tiktok-shop-status" style="font-size:13px;color:var(--muted);line-height:1.6;margin-bottom:4px">Vérification…</div>
        <div style="font-size:12px;color:var(--muted);line-height:1.5;margin-bottom:12px">Relie ton compte créateur pour analyser tes vraies performances (vues, likes, partages) et laisser l'IA apprendre ce qui fonctionne pour toi.</div>
        <button class="btn btn-primary" id="tiktok-connect-btn" onclick="connectTikTokShop()" style="width:100%">🔗 Connecter mon compte TikTok</button>
      </div>`;

  // Buttons
  if (tier !== 'free' && tier !== 'admin') {
    html += `
      <div style="display:flex;gap:10px;flex-wrap:wrap">
        <button class="btn btn-primary" onclick="openCustomerPortal()" style="flex:1">💳 Gérer l'abonnement</button>
        <button class="btn btn-accent" onclick="window.logout()" style="flex:1">🚪 Déconnexion</button>
      </div>`;
  } else if (tier === 'free') {
    html += `
      <div style="display:flex;gap:10px;flex-wrap:wrap">
        <button class="btn btn-primary" onclick="switchTab('pricing')" style="flex:1">⭐ Passer à Pro</button>
        <button class="btn btn-accent" onclick="window.logout()" style="flex:1">🚪 Déconnexion</button>
      </div>`;
  } else {
    html += `
      <button class="btn btn-accent" onclick="window.logout()" style="width:100%">🚪 Déconnexion</button>`;
  }

  html += `</div>`;

  container.innerHTML = html;
  loadTikTokShopStatus();
}

// ── 🛍️ Connexion boutique TikTok Shop (OAuth Partner API) ────────────
async function loadTikTokShopStatus() {
  const statusEl = document.getElementById('tiktok-shop-status');
  const btn = document.getElementById('tiktok-connect-btn');
  if (!statusEl) return;
  const token = localStorage.getItem('tts_token');
  if (!token) { statusEl.textContent = 'Connecte-toi pour relier ta boutique.'; return; }
  try {
    const res = await fetch('/api/auth/tiktok/status', {
      headers: { 'Authorization': 'Bearer ' + token }
    });
    const data = await res.json();
    if (data.connected) {
      statusEl.innerHTML = `✅ Compte TikTok connecté${data.seller_name ? ' — <strong>' + escapeHtml(data.seller_name) + '</strong>' : ''}.`;
      if (btn) btn.textContent = '🔄 Reconnecter mon compte TikTok';
    } else {
      statusEl.textContent = 'Aucun compte TikTok connecté pour le moment.';
    }
  } catch (e) {
    statusEl.textContent = 'Aucun compte TikTok connecté pour le moment.';
  }
}

async function connectTikTokShop() {
  const token = localStorage.getItem('tts_token');
  if (!token) { showToast('Connecte-toi d\'abord.'); return; }
  try {
    const res = await fetch('/api/auth/tiktok/login', {
      headers: { 'Authorization': 'Bearer ' + token }
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      showToast('❌ ' + (err.detail || 'Connexion TikTok indisponible.'));
      return;
    }
    const data = await res.json();
    if (data.authorize_url) {
      window.location.href = data.authorize_url;   // redirige vers TikTok
    }
  } catch (e) {
    showToast('❌ Erreur de connexion TikTok.');
  }
}

// Retour du callback OAuth : affiche un toast selon le paramètre ?tiktok=
(function handleTikTokCallbackParam() {
  try {
    const params = new URLSearchParams(window.location.search);
    const t = params.get('tiktok');
    if (!t) return;
    const messages = {
      connected: '✅ Compte TikTok connecté !',
      warn_not_saved: '⚠️ Compte autorisé mais sauvegarde incomplète. Réessaie.',
      error: '❌ La connexion TikTok a échoué.'
    };
    const msg = messages[t] || (t.startsWith('error') ? messages.error : null);
    if (msg && typeof showToast === 'function') setTimeout(() => showToast(msg), 600);
    // Nettoie l'URL pour éviter de re-déclencher le toast au refresh.
    params.delete('tiktok'); params.delete('reason');
    const clean = window.location.pathname + (params.toString() ? '?' + params.toString() : '');
    window.history.replaceState({}, '', clean);
  } catch (e) { /* no-op */ }
})();

// ── EXPORT PDF ───────────────────────────────────────────────
function exportPDF() {
  if (!currentData || !window.jspdf) return;
  const { jsPDF } = window.jspdf;
  const doc = new jsPDF({ unit: 'mm', format: 'a4' });
  const GOLD  = [212, 175, 55];
  const NAVY  = [31, 58, 112];
  const BLUE  = [37, 99, 235];
  let y = 0;

  doc.setFillColor(...NAVY);
  doc.rect(0, 0, 210, 36, 'F');
  doc.setFillColor(...GOLD);
  doc.rect(0, 34, 210, 2, 'F');
  doc.setTextColor(...GOLD);
  doc.setFontSize(16); doc.setFont('helvetica', 'bold');
  doc.text('TikTok Shop Vidéo Analyzer', 105, 14, { align: 'center' });
  doc.setFontSize(9); doc.setFont('helvetica', 'normal');
  doc.setTextColor(200, 210, 230);
  doc.text('by Dope Ventures', 105, 21, { align: 'center' });
  doc.text(`${new Date().toLocaleDateString('fr-FR')} · ${currentFilename}`, 105, 28, { align: 'center' });
  y = 46;

  doc.setFillColor(...NAVY);
  doc.roundedRect(15, y, 180, 20, 3, 3, 'F');
  doc.setTextColor(...GOLD);
  doc.setFontSize(20); doc.setFont('helvetica', 'bold');
  doc.text(`Score global : ${currentData.score_global ?? '—'} / 100`, 105, y + 13, { align: 'center' });
  y += 26;

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

  section('Analyse détaillée', NAVY);
  if (currentData.scores) {
    const LABELS_PDF = { accroche:'Accroche', discours:'Discours', qualite_visuelle:'Qualité visuelle', visibilite_produit:'Produit', call_to_action:'Appel à l\'action', energie_dynamisme:'Énergie', credibilite_confiance:'Crédibilité' };
    Object.entries(currentData.scores).forEach(([k, v]) => {
      if (y > 265) { doc.addPage(); y = 15; }
      const n = v.note ?? 0;
      const col = n >= 7 ? [5,150,105] : n >= 5 ? [217,119,6] : [220,38,38];
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

  listSection('Points forts',     [5,150,105],   currentData.points_forts,     '+');
  listSection('À améliorer',      [217,119,6],   currentData.points_ameliorer, '!');
  listSection('Conseils concrets', BLUE,          currentData.conseils_concrets,'→');

  const reco = currentData.recommendations_hooks;
  if (reco) {
    section('Recommandation accroche', BLUE);
    doc.setTextColor(...GOLD); doc.setFontSize(10); doc.setFont('helvetica','bold');
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

  const pages = doc.getNumberOfPages();
  for (let i = 1; i <= pages; i++) {
    doc.setPage(i);
    doc.setFontSize(7); doc.setTextColor(100,100,100); doc.setFont('helvetica','normal');
    doc.text(`TikTok Shop Vidéo Analyzer · by Dope Ventures · ${i}/${pages}`, 105, 291, { align:'center' });
  }

  doc.save(`analyse-dv-${Date.now()}.pdf`);
}

// ── AUTH MODAL ────────────────────────────────────────────────
// Note: btn-auth onclick is set dynamically in updateSessionUI()
// When logged out: opens auth modal
// When logged in: shows account dropdown menu

function closeModal() {
  document.getElementById('auth-modal').classList.remove('active');
}

// ── LOGIN FORM HANDLER ────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  const authForm = document.getElementById('auth-form');
  if (authForm) {
    authForm.addEventListener('submit', handleAuthSubmit);
  }
});

async function handleAuthSubmit(event) {
  event.preventDefault();
  const emailInput = document.getElementById('email-input');
  const passwordInput = document.getElementById('password-input');
  const email = (emailInput?.value || '').trim().toLowerCase();
  const password = (passwordInput?.value || '').trim();

  if (!email || !password) {
    showToast('Veuillez remplir tous les champs');
    return;
  }

  try {
    // Jeton CAPTCHA Turnstile (présent uniquement si le widget est activé)
    const cfToken = (window.turnstile && typeof window.turnstile.getResponse === 'function')
      ? (window.turnstile.getResponse() || '')
      : '';

    // Si le widget est affiché mais pas encore validé, on évite une requête vouée
    // à l'échec : on invite l'utilisateur à attendre la coche verte.
    if (document.querySelector('.cf-turnstile') && !cfToken) {
      showToast('⏳ Vérification de sécurité en cours — attends la coche verte puis réessaie.');
      return;
    }

    // Call the /api/login endpoint
    const response = await fetch('/api/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password, cf_turnstile_token: cfToken })
    });

    if (!response.ok) {
      const error = await response.json();
      showToast('❌ ' + (error.detail || 'Erreur connexion'));
      // Réinitialise le CAPTCHA pour permettre une nouvelle tentative
      if (window.turnstile && typeof window.turnstile.reset === 'function') window.turnstile.reset();
      return;
    }

    const data = await response.json();

    // Save session (with secure auth token from backend)
    if (data.token) {
      localStorage.setItem('tts_token', data.token);
    }
    saveSession(email, email, data.token); // email for both email and name

    // Close modal
    closeModal();

    // Clear form
    if (emailInput) emailInput.value = '';
    if (passwordInput) passwordInput.value = '';
    // Connexion silencieuse : pas de popup, l'UI se met à jour directement
  } catch (err) {
    showToast('❌ Erreur: ' + err.message);
  }
}

// ── ADMIN ────────────────────────────────────────────────────
// Le back-office d'administration est désormais isolé sur la route /dope-admin
// (template templates/dope_admin.html + static/admin.js). Aucune logique admin
// n'est exposée dans l'espace client pour ne laisser aucune surface d'attaque.

// ── ECHOTIK TAB FUNCTIONS ──────────────────────────────────────────────────
async function loadWinningTrendsTab() {
  "use strict";
  const tabContent = document.getElementById('tab-winning-trends-content');
  if (!tabContent) return;

  // Récupérer la dernière analyse pour connaître la catégorie
  const history = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
  const lastAnalysis = history.length > 0 ? history[0] : null;
  const detectedCategory = lastAnalysis?.product_category
    || localStorage.getItem('tta_selected_category')
    || null;

  // Afficher la catégorie détectée
  const categoryDisplay = document.getElementById('winning-trends-detected-category');
  const detectedCatName = document.getElementById('detected-cat-name');
  if (detectedCategory) {
    detectedCatName.textContent = detectedCategory;
    categoryDisplay.style.display = 'block';
  } else {
    categoryDisplay.style.display = 'none';
  }

  // Charger les données marché RÉELLES (KeyAPI filtré par catégorie)
  const marketUrl = detectedCategory
    ? `/api/market-recommendations?category=${encodeURIComponent(detectedCategory)}`
    : '/api/market-recommendations';

  // Synchroniser le dropdown
  const selectorEl = document.getElementById('category-selector');
  if (selectorEl && detectedCategory) selectorEl.value = detectedCategory;

  const fmtNum = (n) => {
    if (!n) return '0';
    if (n >= 1e9) return (n/1e9).toFixed(1) + 'B';
    if (n >= 1e6) return (n/1e6).toFixed(1) + 'M';
    if (n >= 1e3) return (n/1e3).toFixed(0) + 'K';
    return String(n);
  };
  const placeholder = 'data:image/svg+xml;utf8,' + encodeURIComponent(
    '<svg xmlns="http://www.w3.org/2000/svg" width="200" height="140" viewBox="0 0 200 140"><rect width="200" height="140" fill="%23f3f4f6"/><text x="100" y="75" font-family="sans-serif" font-size="32" text-anchor="middle" fill="%239ca3af">📦</text></svg>'
  );

  try {
    const res = await fetch(marketUrl);
    const data = await res.json();
    console.log('[WINNING-TRENDS] Response:', data);

    if (data.market_context) {
      const mc = data.market_context;
      let html = '';

      // Top Produits (vraies images KeyAPI)
      if (mc.top_products && mc.top_products.length > 0) {
        html += '<h3 style="margin-top:16px;margin-bottom:8px">⭐ Top Produits TikTok Shop</h3>';
        html += '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px;margin-bottom:16px">';
        mc.top_products.forEach((p) => {
          const imgSrc = p.image || placeholder;
          const productLink = p.url || `https://www.tiktok.com/search?q=${encodeURIComponent(p.name || 'produit')}`;
          html += `<a href="${productLink}" target="_blank" rel="noopener" style="text-decoration:none;display:flex;flex-direction:column">
            <div style="background:var(--surface);border-radius:12px;overflow:hidden;box-shadow:var(--shadow-sm);transition:transform .2s,box-shadow .2s;cursor:pointer" onmouseover="this.style.transform='translateY(-4px)';this.style.boxShadow='var(--shadow)'" onmouseout="this.style.transform='none';this.style.boxShadow='var(--shadow-sm)'">
              <img src="${imgSrc}" alt="${escapeHtml(p.name)}" loading="lazy" onerror="this.src='${placeholder}'" style="width:100%;height:140px;object-fit:cover;background:var(--bg)">
              <div style="padding:12px">
                <div style="font-weight:600;font-size:13px;color:var(--text);margin-bottom:6px;line-height:1.4;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden">${escapeHtml(p.name || 'Produit')}</div>
                <div style="color:var(--primary);font-weight:700;font-size:14px;margin-bottom:4px">${escapeHtml(p.price || '—')}</div>
                <div style="display:flex;gap:8px;flex-wrap:wrap;font-size:11px;color:var(--muted)">
                  <span>⭐ ${p.viral_score || '—'}</span>
                  <span>📦 ${fmtNum(p.sales)}</span>
                  <span>👁️ ${fmtNum(p.views)}</span>
                </div>
              </div>
            </div>
          </a>`;
        });
        html += '</div>';
      }

      // Tendances
      if (mc.trending && mc.trending.length > 0) {
        html += '<h3 style="margin-top:16px;margin-bottom:8px">🔥 Tendances - Croissance Rapide</h3>';
        html += '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px;margin-bottom:16px">';
        mc.trending.forEach((p) => {
          const imgSrc = p.image || placeholder;
          const productLink = p.url || `https://www.tiktok.com/search?q=${encodeURIComponent(p.name || 'produit')}`;
          html += `<a href="${productLink}" target="_blank" rel="noopener" style="text-decoration:none;display:flex;flex-direction:column">
            <div style="background:var(--surface);border-radius:12px;overflow:hidden;box-shadow:var(--shadow-sm);transition:transform .2s,box-shadow .2s;cursor:pointer" onmouseover="this.style.transform='translateY(-4px)';this.style.boxShadow='var(--shadow)'" onmouseout="this.style.transform='none';this.style.boxShadow='var(--shadow-sm)'">
              <img src="${imgSrc}" alt="${escapeHtml(p.name)}" loading="lazy" onerror="this.src='${placeholder}'" style="width:100%;height:140px;object-fit:cover;background:var(--bg)">
              <div style="padding:12px">
                <div style="font-weight:600;font-size:13px;color:var(--text);margin-bottom:6px;line-height:1.4;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden">${escapeHtml(p.name || 'Produit')}</div>
                <div style="color:#EF4444;font-weight:700;font-size:13px;margin-bottom:4px">${p.trend_momentum || '🚀'}</div>
                <div style="display:flex;gap:8px;flex-wrap:wrap;font-size:11px;color:var(--muted)">
                  <span>👥 ${fmtNum(p.creator_count)} créateurs</span>
                  <span>🎥 ${fmtNum(p.video_count)}</span>
                </div>
              </div>
            </div>
          </a>`;
        });
        html += '</div>';
      }

      // Top Créateurs
      if (mc.top_creators && mc.top_creators.length > 0) {
        html += '<h3 style="margin-top:16px;margin-bottom:8px">👑 Top Produits par # de Créateurs</h3>';
        html += '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:12px">';
        mc.top_creators.forEach((c) => {
          const imgSrc = c.image || placeholder;
          const link = c.url || `https://www.tiktok.com/search/user?q=${encodeURIComponent(c.product || c.handle || '')}`;
          html += `<a href="${link}" target="_blank" rel="noopener" style="text-decoration:none;display:flex;flex-direction:column">
            <div style="background:var(--surface);border-radius:12px;padding:12px;box-shadow:var(--shadow-sm);transition:transform .2s,box-shadow .2s;cursor:pointer;text-align:center" onmouseover="this.style.transform='translateY(-4px)';this.style.boxShadow='var(--shadow)'" onmouseout="this.style.transform='none';this.style.boxShadow='var(--shadow-sm)'">
              <img src="${imgSrc}" alt="produit" loading="lazy" onerror="this.src='${placeholder}'" style="width:80px;height:80px;border-radius:50%;object-fit:cover;margin:0 auto 12px;border:2px solid var(--primary)">
              <div style="font-weight:700;font-size:12px;color:var(--text);margin-bottom:4px;word-break:break-word;line-height:1.3;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden">${escapeHtml(c.product || c.handle || '')}</div>
              <div style="color:var(--muted);font-size:11px;margin-bottom:2px">👥 ${escapeHtml(c.followers_display || '—')} portée</div>
              <div style="color:var(--muted);font-size:11px">🎥 ${fmtNum(c.video_count)} vidéos</div>
            </div>
          </a>`;
        });
        html += '</div>';
      }

      if (html.length > 0) {
        document.getElementById('market-context-content').innerHTML = html;
        document.getElementById('winning-trends-context').style.display = 'block';
        document.getElementById('winning-trends-loading').style.display = 'none';
      } else {
        console.warn('[WINNING-TRENDS] HTML est vide');
        document.getElementById('winning-trends-no-data').style.display = 'block';
        document.getElementById('winning-trends-loading').style.display = 'none';
      }
    } else {
      console.warn('[WINNING-TRENDS] Pas de market_context dans les données');
      document.getElementById('winning-trends-no-data').style.display = 'block';
      document.getElementById('winning-trends-loading').style.display = 'none';
    }
  } catch (e) {
    console.error('Erreur chargement marché:', e);
    document.getElementById('winning-trends-no-data').style.display = 'block';
    document.getElementById('winning-trends-loading').style.display = 'none';
  }

  // Charger vidéos virales EchoTik si catégorie détectée
  if (detectedCategory) {
    try {
      const viralRes = await fetch(`/api/viral-videos/${detectedCategory.toLowerCase().replace(/\s/g, '-')}`);
      const viralData = await viralRes.json();
      console.log('[VIRAL-VIDEOS] Response:', viralData);

      if (viralData.ok && viralData.videos && viralData.videos.length > 0) {
        const viralHtml = `
          <div style="margin-top: 40px;">
            <h2 style="font-size:18px;font-weight:700;color:var(--text);margin-bottom:16px">🎬 Vidéos Virales (100K+ vues)</h2>
            <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:12px">
              ${viralData.videos.map(v => `
                <a href="${v.url}" target="_blank" rel="noopener" style="text-decoration:none">
                  <div style="background:var(--surface);border-radius:12px;overflow:hidden;box-shadow:var(--shadow-sm);transition:transform .2s,box-shadow .2s" onmouseover="this.style.transform='translateY(-4px)';this.style.boxShadow='var(--shadow)'" onmouseout="this.style.transform='none';this.style.boxShadow='var(--shadow-sm)'">
                    <img src="${v.thumbnail}" alt="Vidéo viral" style="width:100%;height:120px;object-fit:cover;background:var(--bg)">
                    <div style="padding:10px">
                      <div style="font-size:11px;color:var(--primary);font-weight:700;margin-bottom:4px">@${escapeHtml(v.creator_handle)}</div>
                      <div style="font-size:11px;color:var(--muted);margin-bottom:2px">👁️ ${(v.views/1000).toFixed(0)}K vues</div>
                      <div style="font-size:11px;color:#059669;font-weight:600">📦 ${(v.sales/1000).toFixed(1)}K ventes</div>
                      ${v.hashtags && v.hashtags.length > 0 ? `<div style="font-size:10px;color:var(--accent);margin-top:4px">${v.hashtags.slice(0,2).join(' ')}</div>` : ''}
                    </div>
                  </div>
                </a>
              `).join('')}
            </div>
          </div>
        `;
        document.getElementById('winning-trends-products').insertAdjacentHTML('beforeend', viralHtml);
      }
    } catch (e) {
      console.error('Erreur vidéos virales:', e);
    }
  }

  // Charger les recommandations produits si catégorie détectée
  if (detectedCategory) {
    try {
      const res = await fetch(`/api/product-recommendations/${detectedCategory.toLowerCase().replace(/\s/g, '-')}`);
      const data = await res.json();

      if (data.ok && data.strategy) {
        const strategy = data.strategy;
        // Afficher les produits recommandés + stratégie
        const productsHtml = `
          <div style="margin-top: 40px;">
            <h2 style="font-size:18px;font-weight:700;color:var(--text);margin-bottom:16px">🛍️ Produits Recommandés pour ${escapeHtml(strategy.name)}</h2>

            <!-- Stratégie -->
            <div style="background:var(--surface2);padding:16px;border-radius:8px;margin-bottom:20px">
              <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:12px">
                <div>
                  <div style="color:var(--muted);font-size:12px;font-weight:600">📌 Hooks Efficaces</div>
                  <div style="color:var(--text);font-size:13px;margin-top:4px">${strategy.hooks.join(' • ')}</div>
                </div>
                <div>
                  <div style="color:var(--muted);font-size:12px;font-weight:600">💰 Positionnement Prix</div>
                  <div style="color:var(--primary);font-size:13px;font-weight:600;margin-top:4px">${strategy.price_positioning} (${strategy.average_price})</div>
                </div>
              </div>
              <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">
                <div>
                  <div style="color:var(--muted);font-size:12px;font-weight:600">⏱️ Timing Conversion</div>
                  <div style="color:var(--text);font-size:13px;margin-top:4px">${strategy.conversion_timing}</div>
                </div>
                <div>
                  <div style="color:var(--muted);font-size:12px;font-weight:600">📈 Multiplicateur Viral</div>
                  <div style="color:#059669;font-size:13px;font-weight:600;margin-top:4px">x${strategy.viral_multiplier}</div>
                </div>
              </div>
            </div>

            <!-- Produits Recommandés -->
            ${data.recommended_products && data.recommended_products.length > 0 ? `
              <div>
                <h3 style="font-size:14px;font-weight:700;color:var(--text);margin-bottom:12px">📊 Top Produits en Tendance</h3>
                <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:12px">
                  ${data.recommended_products.slice(0, 6).map(p => `
                    <a href="${p.url || p.tiktok_search_url || '#'}" target="_blank" rel="noopener" style="text-decoration:none">
                      <div style="background:var(--surface);border-radius:8px;overflow:hidden;box-shadow:var(--shadow-sm);transition:transform .2s,box-shadow .2s;cursor:pointer" onmouseover="this.style.transform='translateY(-2px)';this.style.boxShadow='var(--shadow)'" onmouseout="this.style.transform='none';this.style.boxShadow='var(--shadow-sm)'">
                        ${p.image
                          ? `<img src="${p.image}" alt="${escapeHtml(p.title||'Produit')}" loading="lazy" onerror="this.style.display='none'" style="width:100%;height:120px;object-fit:cover;background:var(--bg)">`
                          : `<div style="width:100%;height:120px;background:linear-gradient(135deg,var(--primary),var(--accent));display:flex;align-items:center;justify-content:center;color:white;font-weight:700;padding:8px;text-align:center;font-size:12px">${escapeHtml((p.title || 'Produit').substring(0,40))}</div>`
                        }
                        <div style="padding:8px">
                          <div style="font-size:11px;color:var(--text);font-weight:600;margin-bottom:4px;line-height:1.3;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden">${escapeHtml((p.title || 'Produit').substring(0,60))}</div>
                          <div style="font-size:11px;color:var(--primary);font-weight:700;margin-bottom:2px">💰 ${p.price ? '$' + Number(p.price).toFixed(2) : '—'}</div>
                          <div style="font-size:10px;color:var(--muted);margin-bottom:2px">👁️ ${p.views ? (p.views/1000).toFixed(0)+'K' : '—'} vues</div>
                          <div style="font-size:10px;color:#059669">📦 ${p.sales || p.video_sale_cnt || 0} ventes</div>
                        </div>
                      </div>
                    </a>
                  `).join('')}
                </div>
              </div>
            ` : ''}
          </div>
        `;
        document.getElementById('winning-trends-products').insertAdjacentHTML('beforeend', productsHtml);
        document.getElementById('winning-trends-products-loading').style.display = 'none';
      }
    } catch (e) {
      console.error('Erreur recommandations:', e);
      document.getElementById('winning-trends-products-none').style.display = 'block';
      document.getElementById('winning-trends-products-loading').style.display = 'none';
    }
  } else {
    document.getElementById('winning-trends-products-none').style.display = 'block';
    document.getElementById('winning-trends-products-loading').style.display = 'none';
  }
}

async function changeCategory() {
  "use strict";
  const selectedCategory = document.getElementById('category-selector').value;

  // Si vide, recharger avec catégorie détectée
  if (!selectedCategory) {
    loadWinningTrendsTab();
    return;
  }

  // Effacer le contenu précédent
  document.getElementById('winning-trends-products').innerHTML = '';
  document.getElementById('winning-trends-products-loading').style.display = 'block';
  document.getElementById('winning-trends-products-none').style.display = 'none';

  // Stocker la catégorie sélectionnée dans le storage pour recharger le marché
  // puis appeler loadWinningTrendsTab avec override
  const history = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
  if (history.length > 0) {
    history[0].product_category = selectedCategory;
    localStorage.setItem(STORAGE_KEY, JSON.stringify(history));
  } else {
    // Aucune analyse → stocker temporairement
    localStorage.setItem('tta_selected_category', selectedCategory);
  }
  // Recharger la tab complète (marché + produits) avec la nouvelle catégorie
  loadWinningTrendsTab();
  return;

  try {
    // Charger recommandations pour la catégorie sélectionnée
    const res = await fetch(`/api/product-recommendations/${selectedCategory}`);
    const data = await res.json();
    console.log('[CATEGORY-CHANGE] Response:', data);

    if (data.ok && data.strategy) {
      const strategy = data.strategy;
      const productsHtml = `
        <div style="margin-top: 0;">
          <h2 style="font-size:18px;font-weight:700;color:var(--text);margin-bottom:16px">🛍️ Produits Recommandés pour ${escapeHtml(strategy.name)}</h2>

          <!-- Stratégie -->
          <div style="background:var(--surface2);padding:16px;border-radius:8px;margin-bottom:20px">
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:12px">
              <div>
                <div style="color:var(--muted);font-size:12px;font-weight:600">📌 Hooks Efficaces</div>
                <div style="color:var(--text);font-size:13px;margin-top:4px">${strategy.hooks.join(' • ')}</div>
              </div>
              <div>
                <div style="color:var(--muted);font-size:12px;font-weight:600">💰 Positionnement Prix</div>
                <div style="color:var(--primary);font-size:13px;font-weight:600;margin-top:4px">${strategy.price_positioning} (${strategy.average_price})</div>
              </div>
            </div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">
              <div>
                <div style="color:var(--muted);font-size:12px;font-weight:600">⏱️ Timing Conversion</div>
                <div style="color:var(--text);font-size:13px;margin-top:4px">${strategy.conversion_timing}</div>
              </div>
              <div>
                <div style="color:var(--muted);font-size:12px;font-weight:600">📈 Multiplicateur Viral</div>
                <div style="color:#059669;font-size:13px;font-weight:600;margin-top:4px">x${strategy.viral_multiplier}</div>
              </div>
            </div>
          </div>

          <!-- Produits Recommandés -->
          ${data.recommended_products && data.recommended_products.length > 0 ? `
            <div>
              <h3 style="font-size:14px;font-weight:700;color:var(--text);margin-bottom:12px">📊 Top Produits en Tendance</h3>
              <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:12px">
                ${data.recommended_products.slice(0, 6).map(p => `
                  <a href="${p.url || p.tiktok_search_url || '#'}" target="_blank" rel="noopener" style="text-decoration:none">
                    <div style="background:var(--surface);border-radius:8px;overflow:hidden;box-shadow:var(--shadow-sm);transition:transform .2s,box-shadow .2s;cursor:pointer" onmouseover="this.style.transform='translateY(-2px)';this.style.boxShadow='var(--shadow)'" onmouseout="this.style.transform='none';this.style.boxShadow='var(--shadow-sm)'">
                      ${p.image
                        ? `<img src="${p.image}" alt="${escapeHtml(p.title||'Produit')}" loading="lazy" onerror="this.style.display='none'" style="width:100%;height:120px;object-fit:cover;background:var(--bg)">`
                        : `<div style="width:100%;height:120px;background:linear-gradient(135deg,var(--primary),var(--accent));display:flex;align-items:center;justify-content:center;color:white;font-weight:700;padding:8px;text-align:center;font-size:12px">${escapeHtml((p.title || 'Produit').substring(0,40))}</div>`
                      }
                      <div style="padding:8px">
                        <div style="font-size:11px;color:var(--text);font-weight:600;margin-bottom:4px;line-height:1.3;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden">${escapeHtml((p.title || 'Produit').substring(0,60))}</div>
                        <div style="font-size:11px;color:var(--primary);font-weight:700;margin-bottom:2px">💰 ${p.price ? '$' + Number(p.price).toFixed(2) : '—'}</div>
                        <div style="font-size:10px;color:var(--muted);margin-bottom:2px">👁️ ${p.views ? (p.views/1000).toFixed(0)+'K' : '—'} vues</div>
                        <div style="font-size:10px;color:#059669">📦 ${p.sales || p.video_sale_cnt || 0} ventes</div>
                      </div>
                    </div>
                  </a>
                `).join('')}
              </div>
            </div>
          ` : `<p style="color:var(--muted)">Aucun produit trouvé pour cette catégorie.</p>`}
        </div>
      `;
      document.getElementById('winning-trends-products').innerHTML = productsHtml;
    } else {
      document.getElementById('winning-trends-products-none').style.display = 'block';
    }
  } catch (e) {
    console.error('Erreur changement catégorie:', e);
    document.getElementById('winning-trends-products-none').style.display = 'block';
  }

  document.getElementById('winning-trends-products-loading').style.display = 'none';
}

function escapeHtml(text) {
  const map = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' };
  return text.replace(/[&<>"']/g, m => map[m]);
}
