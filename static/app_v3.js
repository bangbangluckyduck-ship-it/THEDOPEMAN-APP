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
    app_title:'Qeerah', app_title_hl:'', app_sub:'by Dope Ventures',
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
    footer:'© 2026 Dope Ventures · Qeerah · Tous droits réservés',
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
<p>Contactez-nous : <a href="mailto:contact@qeerah.com">contact@qeerah.com</a></p>`,
    ios_title:'Installer sur iPhone / iPad',
    ios_s1:'Appuie sur <strong style="color:var(--text)">Partager</strong> ⎋ en bas de Safari',
    ios_s2:'Fais défiler et appuie sur <strong style="color:var(--text)">"Sur l\'écran d\'accueil"</strong>',
    ios_s3:'Appuie sur <strong style="color:var(--text)">"Ajouter"</strong> en haut à droite',
  },
  en: {
    app_title:'Qeerah', app_title_hl:'', app_sub:'by Dope Ventures',
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
    footer:'© 2026 Dope Ventures · Qeerah · All rights reserved',
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
<p>Contact us: <a href="mailto:contact@qeerah.com">contact@qeerah.com</a></p>`,
    ios_title:'Install on iPhone / iPad',
    ios_s1:'Tap <strong style="color:var(--text)">Share</strong> ⎋ at the bottom of Safari',
    ios_s2:'Scroll down and tap <strong style="color:var(--text)">"Add to Home Screen"</strong>',
    ios_s3:'Tap <strong style="color:var(--text)">"Add"</strong> in the top right corner',
  },
  'pt-br': {
    app_title:'Qeerah', app_title_hl:'', app_sub:'by Dope Ventures',
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
    footer:'© 2026 Dope Ventures · Qeerah · Todos os direitos reservados',
    tb_title:'Seus dados são seus', tb_sub:'ficam em LOCAL, nunca enviados.', tb_link:'Detalhes →',
    ck_title:'🍪 Usamos cookies', ck_body:'Seus dados de vídeo ficam SEMPRE em local. Os cookies nos ajudam a melhorar sua experiência.', ck_link:'Política de privacidade', ck_accept:'Aceitar tudo', ck_reject:'Recusar',
    pm_title:'Sua privacidade', pm_close:'Entendido! Fechar',
    footer_privacy:'Privacidade', footer_cookies:'Cookies',
    pm_content:`<h3>✅ Seus dados ficam EM LOCAL</h3><p>Todas as suas análises ficam <strong>apenas no seu dispositivo</strong>. Nunca as recuperamos em nossos servidores.</p><h3>🍪 Cookies usados</h3><ul><li>localStorage: análises, histórico, idioma</li><li>cookieConsent: sua escolha</li></ul><h3>📧 Dúvidas?</h3><p><a href="mailto:contact@qeerah.com">contact@qeerah.com</a></p>`,
    ios_title:'Instalar no iPhone / iPad',
    ios_s1:'Toque em <strong style="color:var(--text)">Compartilhar</strong> ⎋ na parte inferior do Safari',
    ios_s2:'Role para baixo e toque em <strong style="color:var(--text)">"Tela de Início"</strong>',
    ios_s3:'Toque em <strong style="color:var(--text)">"Adicionar"</strong> no canto superior direito',
  },
  es: {
    app_title:'Qeerah', app_title_hl:'', app_sub:'by Dope Ventures',
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
    footer:'© 2026 Dope Ventures · Qeerah · Todos los derechos reservados',
    tb_title:'Tus datos son tuyos', tb_sub:'se quedan EN LOCAL, nunca se envían.', tb_link:'Detalles →',
    ck_title:'🍪 Usamos cookies', ck_body:'Tus datos de vídeo siempre permanecen en local. Las cookies nos ayudan a mejorar tu experiencia.', ck_link:'Política de privacidad', ck_accept:'Aceptar todo', ck_reject:'Rechazar',
    pm_title:'Tu privacidad', pm_close:'¡Entendido! Cerrar',
    footer_privacy:'Privacidad', footer_cookies:'Cookies',
    pm_content:`<h3>✅ Tus datos EN LOCAL</h3><p>Todos tus análisis se almacenan <strong>solo en tu dispositivo</strong>. Nunca los recuperamos en nuestros servidores.</p><h3>🍪 Cookies usadas</h3><ul><li>localStorage: análisis, historial, idioma</li><li>cookieConsent: tu elección</li></ul><h3>📧 ¿Preguntas?</h3><p><a href="mailto:contact@qeerah.com">contact@qeerah.com</a></p>`,
    ios_title:'Instalar en iPhone / iPad',
    ios_s1:'Pulsa <strong style="color:var(--text)">Compartir</strong> ⎋ en la parte inferior de Safari',
    ios_s2:'Desplázate y pulsa <strong style="color:var(--text)">"En pantalla de inicio"</strong>',
    ios_s3:'Pulsa <strong style="color:var(--text)">"Añadir"</strong> arriba a la derecha',
  },
  it: {
    app_title:'Qeerah', app_title_hl:'', app_sub:'by Dope Ventures',
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
    footer:'© 2026 Dope Ventures · Qeerah · Tutti i diritti riservati',
    tb_title:'I tuoi dati sono tuoi', tb_sub:'restano IN LOCALE, mai inviati.', tb_link:'Dettagli →',
    ck_title:'🍪 Usiamo i cookie', ck_body:'I tuoi dati video restano SEMPRE in locale. I cookie ci aiutano a migliorare la tua esperienza.', ck_link:'Privacy policy', ck_accept:'Accetta tutto', ck_reject:'Rifiuta',
    pm_title:'La tua privacy', pm_close:'Capito! Chiudi',
    footer_privacy:'Privacy', footer_cookies:'Cookie',
    pm_content:`<h3>✅ I tuoi dati IN LOCALE</h3><p>Tutte le tue analisi sono memorizzate <strong>solo sul tuo dispositivo</strong>. Non le recuperiamo mai sui nostri server.</p><h3>🍪 Cookie usati</h3><ul><li>localStorage: analisi, cronologia, lingua</li><li>cookieConsent: la tua scelta</li></ul><h3>📧 Domande?</h3><p><a href="mailto:contact@qeerah.com">contact@qeerah.com</a></p>`,
    ios_title:'Installa su iPhone / iPad',
    ios_s1:'Tocca <strong style="color:var(--text)">Condividi</strong> ⎋ in fondo a Safari',
    ios_s2:'Scorri e tocca <strong style="color:var(--text)">"Aggiungi a Home"</strong>',
    ios_s3:'Tocca <strong style="color:var(--text)">"Aggiungi"</strong> in alto a destra',
  },
  de: {
    app_title:'Qeerah', app_title_hl:'', app_sub:'by Dope Ventures',
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
    footer:'© 2026 Dope Ventures · Qeerah · Alle Rechte vorbehalten',
    tb_title:'Deine Daten gehören dir', tb_sub:'bleiben LOKAL, werden nie gesendet.', tb_link:'Details →',
    ck_title:'🍪 Wir verwenden Cookies', ck_body:'Deine Videodaten bleiben IMMER lokal. Cookies helfen uns, deine Erfahrung zu verbessern.', ck_link:'Datenschutz', ck_accept:'Alle akzeptieren', ck_reject:'Ablehnen',
    pm_title:'Dein Datenschutz', pm_close:'Verstanden! Schließen',
    footer_privacy:'Datenschutz', footer_cookies:'Cookies',
    pm_content:`<h3>✅ Deine Daten LOKAL</h3><p>Alle deine Analysen werden <strong>nur auf deinem Gerät</strong> gespeichert. Wir rufen sie nie auf unseren Servern ab.</p><h3>🍪 Verwendete Cookies</h3><ul><li>localStorage: Analysen, Verlauf, Sprache</li><li>cookieConsent: deine Wahl</li></ul><h3>📧 Fragen?</h3><p><a href="mailto:contact@qeerah.com">contact@qeerah.com</a></p>`,
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
  // Fallback : si l'email n'est pas stocké mais qu'un token existe, on le décode
  // (token = base64(email).signature) → la session est bien reconnue connectée.
  if (!SESSION.email) {
    const tok = localStorage.getItem('tts_token');
    if (tok && tok.indexOf('.') > 0) {
      try { SESSION.email = atob(tok.split('.')[0]); localStorage.setItem('tts_email', SESSION.email); } catch (e) {}
    }
  }
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
  const email = (emailInput?.value || '').trim().toLowerCase();

  if (!email || !email.includes('@')) {
    showToast('❌ Entre une adresse email valide');
    return;
  }

  try {
    const response = await fetch('/api/forgot-password', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email })
    });
    const data = await response.json().catch(() => ({}));
    if (!response.ok) {
      showToast('❌ ' + (data.detail || 'Erreur'));
      return;
    }
    showToast('✅ Si un compte existe, un lien de réinitialisation vient d\'être envoyé (vérifie ta boîte + spam).');
    closeForgotPasswordModal();
    if (emailInput) emailInput.value = '';
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

/* ── Indicateur de crédits temps réel (stocké pour affichage dans le menu burger) ─ */
async function updateCreditIndicator() {
  const pill = document.getElementById('credit-pill');
  const count = document.getElementById('credit-count');
  // Toujours cacher le pill du header (les crédits sont désormais dans le menu burger).
  if (pill) pill.style.display = 'none';
  if (typeof SESSION === 'undefined' || !SESSION.email) {
    window.__creditBalance = null;
    return;
  }
  try {
    const _tok = localStorage.getItem('tts_token') || '';
    const r = await fetch('/api/credits/balance', {
      headers: _tok ? { 'Authorization': 'Bearer ' + _tok } : {}
    });
    if (!r.ok) { window.__creditBalance = null; return; }
    const d = await r.json();
    const total = (d && typeof d.total_available === 'number') ? d.total_available : 0;
    window.__creditBalance = total;
    if (count) count.textContent = total;  // garde l'élément à jour si jamais utilisé ailleurs
  } catch (e) {
    window.__creditBalance = null;
  }
}

/* ── Pricing piloté par la roadmap (feature flags serveur) ───────────────── */
function _fmtEur(n) {
  // 9.99 → "9,99 €" · 249 → "249 €"
  const hasDec = Math.round(n * 100) % 100 !== 0;
  return (hasDec ? n.toFixed(2).replace('.', ',') : String(Math.round(n))) + ' €';
}

async function initDynamicPricing() {
  let plans, prices, dates;
  try {
    const [a, p] = await Promise.all([
      fetch('/api/plans/available').then(r => r.json()),
      fetch('/api/plans/prices').then(r => r.json()),
    ]);
    plans = a.plans; dates = a.dates; prices = p.prices;
  } catch (e) {
    return; // En cas d'échec API on garde l'affichage statique (sûr).
  }
  if (!plans || !prices) return;

  // 1) Prix PRO dynamique (9,99 → 11,99 → 12,99 selon la date)
  const proEl = document.getElementById('pc-pro-month');
  if (proEl && prices.pro) {
    const cur = prices.pro.current;
    const [intPart, decPart] = cur.toFixed(2).split('.');
    const old = prices.pro.promo
      ? `<span class="pc-old">${_fmtEur(prices.pro.original)}</span>` : '';
    proEl.innerHTML = `${old}${intPart}<span style="font-size:18px">,${decPart} €</span>`;
  }

  // 2) « Tu économises X €/mois » (valeur réelle − prix actuel)
  const REAL = { pro: 120, gold: 350, agency: 800 };
  ['pro', 'gold', 'agency'].forEach(plan => {
    const s = document.getElementById('pc-save-' + plan);
    if (!s) return;
    if (plans[plan] && prices[plan]) s.textContent = `→ tu économises ~${Math.round(REAL[plan] - prices[plan].current)} €/mois`;
    else s.style.display = 'none';
  });

  // 3) Cartes non encore ouvertes → "🔜 bientôt + 🔔 me notifier"
  ['pro', 'gold', 'agency'].forEach(plan => {
    const card = document.querySelector(`.pricing-card[data-plan="${plan}"]`);
    if (!card || plans[plan]) return;
    _makeComingSoon(card, plan, dates[plan]);
  });

  // 4) Carte vedette : PRO jusqu'au 16 sept, puis GOLD (seulement si ouverte)
  let featured = plans.gold ? 'gold' : 'pro';
  if (!plans[featured]) featured = null;
  if (featured) {
    const fc = document.querySelector(`.pricing-card[data-plan="${featured}"]`);
    if (fc) {
      fc.classList.add('pricing-card-gold');
      const fb = fc.querySelector('.pc-badge');
      if (fb) { fb.textContent = '⭐ POPULAIRE · 🔥 LANCEMENT'; fb.className = 'pc-badge pc-badge-gold'; }
    }
  }

  // 5) LTD masquée jusqu'au 15 oct → bannière de capture d'email à la place
  const ltd = document.getElementById('ltd-section');
  if (ltd && !plans.ltd) _ltdComingSoon(ltd, dates.ltd);
}

function _makeComingSoon(card, plan, dateStr) {
  card.classList.add('pc-soon');
  const badge = card.querySelector('.pc-badge');
  if (badge) badge.textContent = '🔜 BIENTÔT';
  card.querySelectorAll('.pc-price, .pc-period, .pc-value, .pc-save').forEach(n => n.style.display = 'none');
  const info = document.createElement('div');
  info.className = 'pc-soon-date';
  info.innerHTML = `🔜 Disponible le<br><strong>${dateStr}</strong>`;
  const feats = card.querySelector('.pc-features');
  if (feats) card.insertBefore(info, feats); else card.appendChild(info);
  const btn = card.querySelector('.pc-btn');
  if (btn) {
    btn.textContent = '🔔 Me notifier';
    btn.disabled = false;
    btn.classList.add('pc-btn-notify');
    btn.onclick = () => notifyMe(plan);
  }
}

function _ltdComingSoon(ltd, dateStr) {
  ltd.innerHTML =
    `<div style="text-align:center">
       <span style="display:inline-block;background:var(--gold,#D4AF37);color:#1a1a1a;font-size:11px;font-weight:800;padding:3px 10px;border-radius:999px">💎 OFFRE À VIE</span>
       <h3 style="margin:8px 0 2px;font-size:18px">Accès à vie en préparation</h3>
       <p style="font-size:12px;color:var(--muted);margin:0 0 12px">Paiement unique · 50 places au total · ouverture le <strong>${dateStr}</strong></p>
       <button class="btn pc-btn pc-btn-notify" style="max-width:240px;margin:0 auto" onclick="notifyMe('ltd')">🔔 Préviens-moi de l'offre à vie</button>
     </div>`;
}

async function notifyMe(plan) {
  let email = (typeof SESSION !== 'undefined' && SESSION.email) ? SESSION.email : '';
  if (!email) email = (prompt('Ton email pour être prévenu·e du lancement 🔔') || '').trim();
  if (!email || email.indexOf('@') < 1) return;
  try {
    const r = await fetch('/api/notify-me', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, plan }),
    });
    const d = await r.json().catch(() => ({}));
    showToast(r.ok ? (d.message || 'On te préviendra 🔔') : ('❌ ' + (d.detail || 'Erreur')));
  } catch (e) {
    showToast('❌ Erreur réseau');
  }
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

  const meEmail = (typeof SESSION !== 'undefined' && SESSION && SESSION.email) || '';
  const _credits = (typeof window.__creditBalance === 'number') ? window.__creditBalance : null;
  const _creditsRow = _credits !== null
    ? `<button onclick="closeAuthMenu(); switchTab('account'); return false" style="width:100%;display:flex;align-items:center;justify-content:space-between;text-align:left;padding:13px 16px;color:var(--text);background:transparent;border:none;border-bottom:1px solid var(--border);font-size:14px;font-weight:600;cursor:pointer;transition:background .15s" onmouseover="this.style.background='var(--surface2)'" onmouseout="this.style.background='transparent'">
      <span>💎 Crédits : <strong>${_credits}</strong></span>
      <span style="font-size:12px;color:var(--accent);font-weight:700">Recharger →</span>
    </button>` : '';
  menu.innerHTML = `
    ${meEmail ? `<div style="padding:12px 16px;border-bottom:1px solid var(--border);font-size:12px;color:var(--muted);white-space:nowrap;overflow:hidden;text-overflow:ellipsis">${escapeHtml(meEmail)}</div>` : ''}
    ${_creditsRow}
    <button onclick="switchTab('account'); closeAuthMenu(); return false" style="width:100%;display:block;text-align:left;padding:13px 16px;color:var(--text);background:transparent;border:none;border-bottom:1px solid var(--border);font-size:14px;font-weight:600;cursor:pointer;transition:background .15s" onmouseover="this.style.background='var(--surface2)'" onmouseout="this.style.background='transparent'">
      👤 Mon compte
    </button>
    <button onclick="window.logout(); return false" style="width:100%;display:block;text-align:left;padding:13px 16px;color:var(--danger);background:transparent;border:none;font-size:14px;cursor:pointer;transition:background .15s" onmouseover="this.style.background='var(--surface2)'" onmouseout="this.style.background='transparent'">
      🚪 Se déconnecter
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

  // Connecté si on a un email OU un token (robuste si tts_email absent).
  if (SESSION.email || localStorage.getItem('tts_token')) {
    // User is logged in
    if (overlay) overlay.style.display = 'none';
    if (userEmailEl) userEmailEl.textContent = SESSION.name || SESSION.email;
    if (btnAuth) {
      btnAuth.textContent = '☰';
      btnAuth.title = 'Menu';
      btnAuth.setAttribute('aria-label', 'Menu');
      btnAuth.style.cssText = 'font-size:20px;line-height:1;padding:6px 14px;border-radius:10px';
      btnAuth.onclick = (e) => showAuthMenu(e);
    }
    // Fetch user tier info (appelle fetchUserInfo qui met à jour le badge)
    fetchUserInfo();
    updateCreditIndicator();
  } else {
    // User is not logged in
    const _pill = document.getElementById('credit-pill');
    if (_pill) _pill.style.display = 'none';
    if (overlay) overlay.style.display = 'flex';
    if (userEmailEl) userEmailEl.textContent = '';
    if (btnAuth) {
      btnAuth.textContent = t('btn_connect');
      btnAuth.style.cssText = '';   // reset (pas de style burger en déconnecté)
      btnAuth.removeAttribute('title');
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

// Fetch user info from server. Renvoie une Promise (résolue avec les infos plan)
// pour que les vues qui dépendent du tier puissent l'attendre (ex: Photo Slide).
function fetchUserInfo() {
  if (!SESSION.email) return Promise.resolve(null);
  const p = fetch('/api/user-info', {
    headers: {
      'Authorization': localStorage.getItem('tts_token') ? 'Bearer ' + localStorage.getItem('tts_token') : ''
    }
  })
    .then(r => r.json())
    .then(data => {
      window.__userInfo = data;
      updateTierBadge(data);
      try { renderProgressionChart(); } catch (e) {}   // re-render avec le bon tier
      // Affiche le bouton "Mes analyses" dans le header + "Lancer en arrière-
      // plan" (upload) si Pro+ (le bouton URL async est déjà dans la section
      // Pro+ donc visible directement). Les crédits sont maintenant dans le
      // menu burger (rendu par renderAuthMenu).
      try {
        const tier = (data?.tier || 'free').toLowerCase();
        const isPaid = ['pro','gold','agency','beta','admin'].includes(tier);
        const myBtn = document.getElementById('my-analyses-btn');
        if (myBtn) myBtn.style.display = isPaid ? 'inline-block' : 'none';
        const uploadAsync = document.getElementById('analyze-upload-async-btn');
        if (uploadAsync) uploadAsync.style.display = isPaid ? 'block' : 'none';
      } catch (e) {}
      return data;
    })
    .catch(() => null);
  window.__userInfoPromise = p;
  return p;
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
  initDynamicPricing();
  updateCreditIndicator();
  renderProgressionChart();

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
  ['analyze', 'pricing', 'history', 'account', 'creators', 'recherche', 'feedradar', 'photoslide', 'promptstudio', 'credits', 'hooks'].forEach(t => {
    const content = document.getElementById(`tab-${t}-content`);
    const btn     = document.getElementById(`tab-${t}`);
    if (content) content.style.display = t === tab ? 'block' : 'none';
    if (btn)     btn.classList.toggle('active', t === tab);
  });
  if (tab === 'history') renderHistory();
  if (tab === 'pricing') updatePricingCTA();
  if (tab === 'account') renderAccountPage();
  if (tab === 'creators') loadCreatorsTab();
  if (tab === 'recherche') initRechercheTab();
  if (tab === 'feedradar') loadFeedRadarTab();
  if (tab === 'photoslide') initPhotoSlideTab();
  if (tab === 'promptstudio') initPromptStudioTab();
  if (tab === 'credits') initCreditsTab();
  if (tab === 'hooks') initHooksTab();
  if (tab === 'analyze') renderProgressionChart();
}

/* ── FEATURE 1 — Banque de Hooks ─────────────────────────────────────────── */
let _hooksCategory = 'all';
let _hooksData = null;

async function initHooksTab() {
  const list = document.getElementById('hooks-list');
  if (!list) return;
  list.innerHTML = '<div style="grid-column:1/-1;text-align:center;color:var(--muted);padding:24px">⏳ Chargement…</div>';
  try {
    const tok = localStorage.getItem('tts_token') || '';
    const url = '/api/hooks' + (_hooksCategory !== 'all' ? ('?category=' + encodeURIComponent(_hooksCategory)) : '');
    const r = await fetch(url, { headers: tok ? { 'Authorization': 'Bearer ' + tok } : {} });
    _hooksData = await r.json();
  } catch (e) {
    list.innerHTML = '<div style="grid-column:1/-1;text-align:center;color:#DC2626;padding:24px">Erreur de chargement.</div>';
    return;
  }
  renderHooksFilters();
  renderHooks();
}

function renderHooksFilters() {
  const bar = document.getElementById('hooks-filters');
  if (!bar || !_hooksData) return;
  const cats = _hooksData.categories || [];
  const labels = _hooksData.category_labels || {};
  const mk = (key, label) =>
    `<button onclick="setHooksCategory('${key}')" class="hook-cat${_hooksCategory === key ? ' on' : ''}"
       style="border:1px solid ${_hooksCategory === key ? 'var(--accent)' : 'var(--border)'};background:${_hooksCategory === key ? 'rgba(37,99,235,.1)' : 'var(--surface)'};color:var(--text);border-radius:999px;padding:6px 13px;font-size:12.5px;font-weight:600;cursor:pointer">${label}</button>`;
  bar.innerHTML = mk('all', 'Toutes') + cats.map(c => mk(c, labels[c] || c)).join('');
}

function setHooksCategory(c) { _hooksCategory = c; initHooksTab(); }

function renderHooks() {
  const list = document.getElementById('hooks-list');
  if (!list || !_hooksData) return;
  const items = _hooksData.items || [];
  const isFree = (_hooksData.tier || 'free') === 'free';

  if (!items.length) {
    list.innerHTML = '<div style="grid-column:1/-1;text-align:center;color:var(--muted);padding:24px">Aucun hook dans cette catégorie pour le moment.</div>';
    return;
  }
  const labels = _hooksData.category_labels || {};
  list.innerHTML = items.map(h => {
    const catLabel = labels[h.categorie] || h.categorie || '';
    if (h.locked) {
      const why = isFree ? 'Réservé aux abonnés' : (h.required || 'Plan supérieur requis');
      return `<div style="position:relative;border:1px solid var(--border);border-radius:14px;padding:16px;background:var(--surface);overflow:hidden">
        <div style="font-size:11px;font-weight:700;color:var(--muted);text-transform:uppercase;letter-spacing:.04em;margin-bottom:10px">${escapeHtml(catLabel)}</div>
        <div style="filter:blur(5px);user-select:none;color:var(--muted);font-size:14px;line-height:1.5;pointer-events:none">Cette accroche convertit très bien pour ce type de produit, débloque-la pour la copier.</div>
        <div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:8px;background:rgba(255,255,255,.55);backdrop-filter:blur(1px)">
          <div style="font-size:22px">🔒</div>
          <div style="font-size:12.5px;font-weight:700;color:var(--text)">${escapeHtml(why)}</div>
          <button class="btn btn-primary" style="font-size:12px;padding:7px 14px" onclick="switchTab('pricing')">Débloquer 👑</button>
        </div>
      </div>`;
    }
    const vid = h.url_video
      ? `<a href="${escapeHtml(h.url_video)}" target="_blank" rel="noopener" style="display:inline-block;margin-top:10px;font-size:12px;color:var(--accent);font-weight:600;text-decoration:none">▶️ Voir la vidéo d'exemple</a>` : '';
    const enc = encodeURIComponent(h.texte || '');
    return `<div style="border:1px solid var(--border);border-radius:14px;padding:16px;background:var(--surface);display:flex;flex-direction:column">
      <div style="font-size:11px;font-weight:700;color:var(--accent);text-transform:uppercase;letter-spacing:.04em;margin-bottom:10px">${escapeHtml(catLabel)}</div>
      <div style="font-size:14px;line-height:1.5;color:var(--text);flex:1">${escapeHtml(h.texte || '')}</div>
      ${vid}
      <div style="display:flex;gap:8px;margin-top:12px">
        <button onclick="navigator.clipboard.writeText(decodeURIComponent('${enc}')).then(()=>showToast('Hook copié ✓'))" class="btn btn-secondary" style="font-size:12px;flex:1">📋 Copier</button>
        <button onclick="_downloadHook(decodeURIComponent('${enc}'))" class="btn btn-secondary" style="font-size:12px">⬇️</button>
      </div>
    </div>`;
  }).join('');
}

function _downloadHook(text) {
  const blob = new Blob([text], { type: 'text/plain;charset=utf-8' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'hook-qeerah.txt';
  document.body.appendChild(a); a.click(); a.remove();
  URL.revokeObjectURL(a.href);
}

/* ── NOTIFICATIONS — opt-in Web Push (PWA) ───────────────────────────────── */
let _vapidKey = null;

function _b64ToUint8(base64) {
  const pad = '='.repeat((4 - base64.length % 4) % 4);
  const b64 = (base64 + pad).replace(/-/g, '+').replace(/_/g, '/');
  const raw = atob(b64);
  return Uint8Array.from([...raw].map(c => c.charCodeAt(0)));
}

async function initPushUI() {
  const card = document.getElementById('push-card');
  if (!card) return;
  // Support navigateur
  if (!('serviceWorker' in navigator) || !('PushManager' in window) || !('Notification' in window)) return;
  // Le serveur a-t-il les clés VAPID ?
  try {
    const r = await fetch('/api/push/public-key').then(x => x.json());
    if (!r.enabled || !r.key) return;     // pas configuré → on n'affiche rien
    _vapidKey = r.key;
  } catch (e) { return; }
  card.style.display = 'block';
  // État courant
  try {
    const reg = await navigator.serviceWorker.ready;
    const sub = await reg.pushManager.getSubscription();
    _setPushBtn(!!sub);
  } catch (e) { _setPushBtn(false); }
}

function _setPushBtn(active) {
  const btn = document.getElementById('push-btn');
  const desc = document.getElementById('push-desc');
  if (!btn) return;
  if (Notification.permission === 'denied') {
    btn.textContent = '🔕 Notifications bloquées (navigateur)';
    btn.disabled = true;
    if (desc) desc.textContent = 'Tu as refusé les notifications. Réactive-les dans les réglages du navigateur.';
    return;
  }
  btn.disabled = false;
  btn.textContent = active ? '🔕 Désactiver les notifications' : '🔔 Activer les notifications';
  btn.dataset.active = active ? '1' : '';
}

async function togglePush() {
  const btn = document.getElementById('push-btn');
  if (!btn) return;
  if (btn.dataset.active) return disablePush();
  return enablePush();
}

async function enablePush() {
  try {
    if (!('serviceWorker' in navigator) || !('PushManager' in window) || !('Notification' in window)) {
      showToast("Ton navigateur ne gère pas les notifications. Ouvre le site dans Chrome (ou installe l'app sur l'écran d'accueil)."); return;
    }
    if (!_vapidKey) { showToast('Configuration notifications indisponible, réessaie.'); return; }
    const perm = await Notification.requestPermission();
    if (perm !== 'granted') {
      _setPushBtn(false);
      showToast(perm === 'denied' ? '🔕 Autorisation refusée (réactive-la dans les réglages du navigateur).' : 'Autorisation non accordée.');
      return;
    }
    const reg = await navigator.serviceWorker.ready;
    let sub = await reg.pushManager.getSubscription();
    if (!sub) {
      sub = await reg.pushManager.subscribe({
        userVisibleOnly: true,
        applicationServerKey: _b64ToUint8(_vapidKey),
      });
    }
    const tok = localStorage.getItem('tts_token') || '';
    const res = await fetch('/api/push/subscribe', {
      method: 'POST',
      headers: Object.assign({ 'Content-Type': 'application/json' }, tok ? { 'Authorization': 'Bearer ' + tok } : {}),
      body: JSON.stringify({ subscription: sub.toJSON() }),
    });
    if (!res.ok) { showToast("Enregistrement serveur échoué — réessaie."); return; }
    _setPushBtn(true);
    showToast('🔔 Notifications activées');
  } catch (e) {
    // Message réel pour diagnostiquer (souvent : navigateur intégré / Custom Tab qui bloque le push).
    showToast('Notif impossible : ' + ((e && e.message) ? e.message : 'erreur inconnue'));
  }
}

async function disablePush() {
  try {
    const reg = await navigator.serviceWorker.ready;
    const sub = await reg.pushManager.getSubscription();
    if (sub) {
      await fetch('/api/push/unsubscribe', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ endpoint: sub.endpoint }),
      });
      await sub.unsubscribe();
    }
    _setPushBtn(false);
    showToast('🔕 Notifications désactivées');
  } catch (e) { showToast('Erreur.'); }
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
  // Active aussi le bouton async si user Pro+ (sinon il reste caché)
  const asyncBtn = document.getElementById('analyze-upload-async-btn');
  if (asyncBtn) asyncBtn.disabled = false;
}

// Rôle choisi par l'utilisateur (Affilié/Vendeur) — lu à chaque analyse, jamais mémorisé.
function getUserRole() {
  const sel = document.getElementById('user-role-select');
  return sel ? sel.value : null;
}

document.getElementById('analyze-btn').addEventListener('click', analyzeVideo);

// Analyse par liens TikTok (Pro / Gold / Agency)
const _urlsBtn = document.getElementById('analyze-urls-btn');
if (_urlsBtn) _urlsBtn.addEventListener('click', analyzeUrls);
const _urlSingleBtn = document.getElementById('analyze-url-single-btn');
if (_urlSingleBtn) _urlSingleBtn.addEventListener('click', analyzeSingleUrl);

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
  document.getElementById('analysis-preview')?.remove();   // reset aperçu progressif
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
    // Annonce d'attente affichée IMMÉDIATEMENT (avant l'upload du fichier qui
    // peut prendre 5-15s sur connexion lente) → l'utilisateur sait à quoi
    // s'attendre dès la 1re seconde.
    setLoadingInfo("L'analyse Pro prend généralement 30 à 60 secondes — on traite ta vidéo (image + audio + détection CTA) pour une analyse fiable.");
    const fd = new FormData();
    fd.append('frames', JSON.stringify(frames));
    if (audioBlob) fd.append('audio', audioBlob, 'audio.wav');
    // Envoie aussi la vidéo entière — le backend basculera sur le pipeline
    // Pro+ (Gemini Pro natif) si l'utilisateur est éligible. Sinon, fallback
    // automatique sur le pipeline frames+audio (ancien).
    if (selectedFile) fd.append('video', selectedFile, selectedFile.name || 'video.mp4');

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
    fd.append('user_role', getUserRole());

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
        // Info "sticky" : reste affichée tant qu'on ne l'efface pas (un nouveau
        // progress event SANS info ne l'écrase pas, contrairement au texte du
        // spinner). Permet d'annoncer "L'analyse Pro prend 1-2 min" au début
        // et que ça reste visible pendant download + downscale + vision.
        if (eventData.info) setLoadingInfo(eventData.info);
        console.log('[STREAM] Progress:', eventData.message);
      } else if (eventType === 'partial') {
        renderAnalysisPreview(eventData);   // aperçu vision avant la synthèse finale
      } else if (eventType === 'warning') {
        console.warn('[STREAM] Warning:', eventData.message);
      } else if (eventType === 'complete') {
        completeData = eventData;
        setLoadingText('✅ Analyse terminée!');
        setLoadingInfo(null);  // efface l'info sticky une fois fini
        console.log('[STREAM] Analysis complete');
      } else if (eventType === 'error') {
        setLoadingInfo(null);
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
// Analyse 1 lien TikTok en SSE (affichage dynamique : download → vision → synthèse).
async function analyzeSingleUrl() {
  const input = document.getElementById('tiktok-url-single');
  const url = input ? input.value.trim() : '';
  if (!url) { showError('Colle un lien TikTok.'); input && input.focus(); return; }
  if (!/tiktok\.com|vt\.tiktok|vm\.tiktok/i.test(url)) { showError('Lien TikTok invalide.'); input && input.focus(); return; }

  const tier  = window.__userInfo?.tier || 'free';
  const token = localStorage.getItem('tts_token');
  if (!token || tier === 'free') {
    switchTab('pricing');
    showToast("Passez au plan Pro (9,99€) pour analyser des liens TikTok directement !");
    return;
  }

  // Champs DÉDIÉS au bloc « 1 lien » (nom produit + prix obligatoires).
  const productInput = document.getElementById('single-product');
  const product = (productInput && productInput.value.trim()) ? productInput.value.trim() : null;
  const priceInput = document.getElementById('single-price');
  const price = (priceInput && priceInput.value.trim()) ? priceInput.value.trim() : null;
  if (!product) { showError('⭐ Indique le nom/description du produit (obligatoire pour le lien).'); productInput && productInput.focus(); return; }
  if (!price)   { showError('⭐ Indique le prix du produit (obligatoire pour le lien).'); priceInput && priceInput.focus(); return; }

  document.getElementById('error-box').style.display      = 'none';
  document.getElementById('upload-section').style.display  = 'none';
  document.getElementById('loading-section').style.display = 'block';
  setLoadingText('🔗 Analyse du lien…');
  setLoadingInfo("L'analyse Pro prend généralement 30 à 60 secondes — on traite ta vidéo (image + audio + détection CTA) pour une analyse fiable.");

  try {
    const res = await fetch('/analyze-url/stream', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token },
      body: JSON.stringify({ url, product, price, user_role: getUserRole() }),
    });
    if (!res.ok) {
      let m = 'Erreur serveur';
      try { m = (await res.json()).detail || m; } catch (_) {}
      if (res.status === 403) switchTab('pricing');
      throw new Error(m);
    }

    const reader = res.body.getReader(), dec = new TextDecoder();
    let buf = '', completeData = null;
    const handle = (ev, dstr) => {
      let o; try { o = JSON.parse(dstr); } catch (_) { return; }
      if (ev === 'progress') {
        setLoadingText(o.message || '🔄 En cours…');
        if (o.info) setLoadingInfo(o.info);
      }
      else if (ev === 'partial') renderAnalysisPreview(o);
      else if (ev === 'complete') { completeData = o; setLoadingText('✅ Analyse terminée!'); setLoadingInfo(null); }
      else if (ev === 'error') { setLoadingInfo(null); throw new Error(o.error || 'Erreur analyse'); }
    };
    const proc = (block) => {
      let ev = 'message'; const dl = [];
      for (const raw of block.split('\n')) {
        const l = raw.replace(/\r$/, ''); if (!l) continue;
        if (l.startsWith('event:')) ev = l.slice(6).trim();
        else if (l.startsWith('data:')) dl.push(l.slice(5).trim());
      }
      if (dl.length) handle(ev, dl.join('\n'));
    };
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      buf += dec.decode(value, { stream: true });
      let i; while ((i = buf.indexOf('\n\n')) !== -1) { const b = buf.slice(0, i); buf = buf.slice(i + 2); if (b.trim()) proc(b); }
    }
    if (buf.trim()) proc(buf);
    if (!completeData) throw new Error('Pas de données reçues');

    currentData = completeData; currentFilename = url;
    if (completeData.usage?.used !== undefined) {
      localStorage.setItem(USAGE_KEY, completeData.usage.used);
      window.__usage = completeData.usage; updateUsageCounter(); updateUsageBadge(completeData.usage);
    }
    saveToHistory(completeData, url);
    showResults(completeData);
    if (completeData.donnees_marche && (tier === 'gold' || tier === 'agency' || tier === 'beta')) {
      renderMarketSection(completeData.donnees_marche);
      const ms = document.getElementById('market-section'); if (ms) ms.style.display = 'block';
    }
  } catch (e) {
    document.getElementById('loading-section').style.display = 'none';
    document.getElementById('upload-section').style.display  = 'block';
    showError(e.name === 'AbortError' ? t('err_timeout') : '❌ ' + e.message);
  }
}

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
    showToast("Passez au plan Pro (9,99€) pour analyser des liens TikTok directement sans rien télécharger !");
    return;
  }

  // ── BLOCAGE 2 : PRO + plusieurs liens → upsell Gold ──
  if (tier === 'pro' && urls.length > 1) {
    switchTab('pricing');
    showToast("Votre plan Pro permet d'analyser 1 lien à la fois. Passez au plan Gold pour analyser plusieurs vidéos en masse !");
    return;
  }

  // Multi-liens = analyse de PATTERNS sur plusieurs vidéos → produit/prix NON requis
  // (souvent des vidéos/produits différents). On les transmet seulement s'ils sont saisis.
  const productInput = document.getElementById('product-input');
  const product = (productInput && productInput.value.trim()) ? productInput.value.trim() : null;
  const priceInput = document.getElementById('price-input');
  const price = (priceInput && priceInput.value.trim()) ? priceInput.value.trim() : null;

  // ── UI : passe en mode chargement ──
  document.getElementById('error-box').style.display      = 'none';
  document.getElementById('upload-section').style.display  = 'none';
  document.getElementById('loading-section').style.display = 'block';

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
    const _canPatterns = results.length >= 2 && ['gold', 'agency', 'beta', 'admin'].includes(tier);
    const _note = failed.length ? ` (${failed.length} échec${failed.length > 1 ? 's' : ''} : vidéo${failed.length > 1 ? 's' : ''} ${failed.join(', ')})` : '';
    if (total === 1 || !_canPatterns) {
      // Analyse simple (ou pas assez de vidéos réussies pour des patterns) → rapport complet.
      showResults(lastData);
      if (lastData.donnees_marche && ['gold', 'agency', 'beta'].includes(tier)) {
        renderMarketSection(lastData.donnees_marche);
        document.getElementById('market-section').style.display = 'block';
      }
      if (total > 1) showToast(`✅ ${okCount}/${total} vidéos analysées${_note}. (Les patterns nécessitent ≥ 2 vidéos réussies.)`);
    } else {
      // MULTI-liens → on n'affiche QUE les patterns personnels (pas l'analyse de chaque vidéo).
      document.getElementById('results-section').style.display = 'none';
      document.getElementById('market-section') && (document.getElementById('market-section').style.display = 'none');
      document.getElementById('upload-section').style.display = 'none';
      showToast(`✅ ${okCount}/${total} vidéos analysées${_note}.`);
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
  const el = document.getElementById('loading-text');
  if (!el) return;
  el.style.whiteSpace = 'pre-line';  // permet les sauts de ligne via \n
  el.textContent = txt;
}

// Info "sticky" sous le spinner : reste affichée tant qu'on ne l'efface pas
// explicitement. Permet d'annoncer "L'analyse Pro prend 1-2 min" au début et
// que ça reste visible pendant tout le download + downscale + vision.
function setLoadingInfo(info) {
  const parent = document.getElementById('loading-text');
  if (!parent) return;
  let el = document.getElementById('loading-info-sticky');
  if (!info) {
    if (el) el.remove();
    return;
  }
  if (!el) {
    el = document.createElement('div');
    el.id = 'loading-info-sticky';
    el.style.cssText = 'margin-top:12px;padding:10px 14px;background:rgba(212,175,55,0.1);border:1px solid rgba(212,175,55,0.35);border-radius:10px;color:#d4af37;font-size:13px;line-height:1.5;max-width:480px;';
    parent.parentNode.insertBefore(el, parent.nextSibling);
  }
  el.textContent = '💡 ' + info;
}

// Aperçu progressif vidéo : carte « premier coup d'œil » affichée après la passe
// vision, AVANT la synthèse finale (produit détecté + scores visuels préliminaires).
function renderAnalysisPreview(p) {
  const host = document.getElementById('loading-section');
  if (!host || !p) return;
  let card = document.getElementById('analysis-preview');
  if (!card) {
    card = document.createElement('div');
    card.id = 'analysis-preview';
    card.style.cssText = 'max-width:420px;margin:18px auto 0;text-align:left;background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:14px;animation:fadeIn .3s ease';
    host.appendChild(card);
  }
  const sc = (v) => (v == null ? '—' : Math.round(v));
  const bar = (label, v) => {
    const val = (v == null ? 0 : Math.max(0, Math.min(100, v)));
    const col = val >= 70 ? '#059669' : (val >= 45 ? '#D97706' : '#DC2626');
    return `<div style="margin-top:8px">
      <div style="display:flex;justify-content:space-between;font-size:12px;color:var(--muted)"><span>${label}</span><span style="font-weight:700;color:${col}">${sc(v)}</span></div>
      <div style="height:6px;background:var(--border);border-radius:4px;margin-top:3px;overflow:hidden"><div style="height:100%;width:${val}%;background:${col}"></div></div>
    </div>`;
  };
  card.innerHTML = `
    <div style="font-size:11px;font-weight:700;color:var(--primary);text-transform:uppercase;letter-spacing:.04em">👁️ Premier aperçu</div>
    ${p.produit ? `<div style="font-size:14px;font-weight:700;margin-top:4px">${escapeHtml(p.produit)}</div>` : ''}
    ${p.description_visuelle ? `<div style="font-size:12px;color:var(--muted);margin-top:4px;line-height:1.4">${escapeHtml(p.description_visuelle)}</div>` : ''}
    ${bar('Qualité visuelle', p.qualite_visuelle_score)}
    ${bar('Format', p.format_visuel_score)}
    ${bar('Hook visuel', p.hook_visuel_score)}
    <div style="font-size:11px;color:var(--muted);margin-top:10px;text-align:center">🤖 Rédaction des conseils détaillés en cours…</div>`;
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

// ── MODÉRATION + SCRIPT RÉÉCRIT + TIMELINE INTERACTIVE (marqueurs rouges) ──
let _timelineVideoUrl = null;

function _formatMmSs(seconds) {
  const s = Math.max(0, Math.round(seconds));
  return `${Math.floor(s / 60)}:${String(s % 60).padStart(2, '0')}`;
}

function renderModerationAndScript(d) {
  const banner = document.getElementById('moderation-banner');
  const scriptSection = document.getElementById('script-optimise-section');
  if (d.is_safe === false) {
    banner.style.display = 'block';
    document.getElementById('moderation-reason').textContent =
      d.moderation_reason || "Cette vidéo ne respecte pas les règles TikTok Shop — analyse bloquée.";
    scriptSection.style.display = 'none';
    return;
  }
  banner.style.display = 'none';
  if (d.script_optimise) {
    scriptSection.style.display = 'block';
    document.getElementById('script-optimise-box').textContent = d.script_optimise;
    document.getElementById('directive-tournage-box').textContent = d.directive_tournage || '—';
  } else {
    scriptSection.style.display = 'none';
  }
}

function renderErrorTimeline(d) {
  const section   = document.getElementById('video-timeline-section');
  const playerWrap = document.getElementById('video-timeline-player-wrap');
  const player    = document.getElementById('analysis-video-player');
  const track     = document.getElementById('video-timeline-track');
  const list      = document.getElementById('video-timeline-list');
  const noVideoNote = document.getElementById('video-timeline-novideo-note');

  const moments = Array.isArray(d.moments_erreurs) ? d.moments_erreurs.filter(m => m && m.diagnostic) : [];

  if (d.is_safe === false || !moments.length) {
    section.style.display = 'none';
    return;
  }
  section.style.display = 'block';

  const GRAVITE_COLOR = { critique: '#e74c3c', moyen: '#e67e22', faible: '#f1c40f' };

  // Nettoyage de la précédente URL locale (évite les fuites mémoire entre 2 analyses)
  if (_timelineVideoUrl) { URL.revokeObjectURL(_timelineVideoUrl); _timelineVideoUrl = null; }
  track.innerHTML = '';

  // Aperçu vidéo local UNIQUEMENT possible pour une analyse par upload (le
  // fichier vient du disque de l'utilisateur) — une analyse par lien TikTok
  // n'a pas de vidéo à rejouer côté navigateur (jamais renvoyée par le backend).
  const hasLocalVideo = !!selectedFile && (d.source === 'upload' || !d.source_url);

  if (hasLocalVideo) {
    _timelineVideoUrl = URL.createObjectURL(selectedFile);
    player.src = _timelineVideoUrl;
    playerWrap.style.display = 'block';
    track.style.display = 'block';
    noVideoNote.style.display = 'none';

    const placeMarkers = () => {
      const dur = player.duration;
      if (!dur || !isFinite(dur)) return;
      track.innerHTML = '';
      moments.forEach(m => {
        if (typeof m.timestamp_seconds !== 'number') return;
        const dot = document.createElement('div');
        const pct = Math.min(100, Math.max(0, (m.timestamp_seconds / dur) * 100));
        dot.title = `${_formatMmSs(m.timestamp_seconds)} — ${m.pilier || ''} : ${m.diagnostic}`;
        dot.style.cssText = `position:absolute;top:-3px;left:${pct}%;width:14px;height:14px;margin-left:-7px;
          border-radius:50%;background:${GRAVITE_COLOR[m.gravite] || '#e74c3c'};border:2px solid var(--surface);cursor:pointer`;
        dot.addEventListener('click', () => { player.currentTime = m.timestamp_seconds; player.play(); });
        track.appendChild(dot);
      });
    };
    player.addEventListener('loadedmetadata', placeMarkers, { once: true });
  } else {
    playerWrap.style.display = 'none';
    track.style.display = 'none';
    noVideoNote.style.display = 'block';
  }

  list.innerHTML = moments.map(m => {
    const hasTs = typeof m.timestamp_seconds === 'number';
    const tsLabel = hasTs ? _formatMmSs(m.timestamp_seconds) : '—';
    const color = GRAVITE_COLOR[m.gravite] || '#e74c3c';
    return `
      <div class="${hasTs && hasLocalVideo ? 'timeline-item-clickable' : ''}"
           ${hasTs && hasLocalVideo ? `onclick="document.getElementById('analysis-video-player').currentTime=${m.timestamp_seconds};document.getElementById('analysis-video-player').play();window.scrollTo({top:document.getElementById('video-timeline-section').offsetTop-10,behavior:'smooth'})"` : ''}
           style="display:flex;gap:10px;align-items:flex-start;padding:10px 12px;background:var(--surface2);border-left:3px solid ${color};border-radius:6px;${hasTs && hasLocalVideo ? 'cursor:pointer' : ''}">
        <strong style="color:${color};min-width:44px">${tsLabel}</strong>
        <span style="font-size:13px"><strong>${m.pilier || ''}</strong> — ${m.diagnostic}</span>
      </div>`;
  }).join('');
}

// ── SHOW RESULTS (Core rendering function - keep as is) ────────
function showResults(d) {
  console.log('[DEBUG] showResults called with data:', d);
  window._lastAnalysis = d;   // pour le partage du score (Feature 4)
  renderModerationAndScript(d);
  renderErrorTimeline(d);
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

  // COACHING : pour FREE/PRO on garde le teaser verrouillé (upsell). Pour les plans
  // premium, l'ancien encart "🤖 Coach IA" faisait DOUBLON avec les autres volets
  // (conseils déjà couverts par points à améliorer / structure / stratégie) → retiré.
  const userTierForCoaching = window.__userInfo?.tier || 'free';
  const isFreemium = userTierForCoaching === 'free' || userTierForCoaching === 'pro';
  document.getElementById('coaching-section')?.remove();   // nettoie un éventuel encart obsolète
  if (isFreemium && d.conseils_concrets?.length > 0) {
    showLockedCoachingSection(d.conseils_concrets[0]);
  }

  // 👑 STRATÉGIE DE CONVERSION (PREMIUM) — Gold / Agency / Beta uniquement.
  // La donnée n'est générée côté serveur QUE pour ces plans ; sinon on affiche
  // un composant d'upsell pour pousser vers Gold.
  renderPremiumStrategy(d);

  // 🏆 Structures gagnantes (Gold / Agency) : affiché quand le serveur a renvoyé
  // un payload structures_gagnantes (score < 75 + plan habilité).
  renderWinningStructures(d);

  // 🔥 Reco marché auto : créateurs + produits qui cartonnent dans la catégorie
  // détectée (Gold/Agency complet, free/pro flouté). Placeholder synchrone puis
  // remplissage async (pour être inclus dans le slider).
  // 👑 Créateurs gagnants DE LA CATÉGORIE (chaîne top produits → leurs créateurs).
  renderCategoryCreators(d);

  renderMarketForCategory(d);

  // 🛍️ Produits similaires en tendance (recherche temps-réel par mot-clé produit).
  renderSimilarProducts(d);

  // 🔥 Populaire chez nos utilisateurs (mémoire produits maison, se bonifie avec le temps).
  renderPopularProducts(d);

  // 🏆 Carte verdict en tête : récap (verdict + 3 forces / 3 axes) juste après les
  // scores. Évite le doublon en masquant les sections verdict + forts/faibles.
  renderVerdictHero(d);

  // 🧬 8 dimensions de persuasion en cartes visuelles (donnée analyse_8_dimensions).
  renderDimensions(d);

  // Plan Free : on garde la notation visible, on floute le reste + CTA conversion.
  applyFreemiumBlur();

  // 🧱 Vue VERTICALE (remplace l'ancien slider horizontal) : les sections se
  // suivent de haut en bas, lecture naturelle. On aplatit tout slider résiduel
  // et on masque les sections visibles mais vides (anti-carte blanche).
  layoutAnalysisVertical();

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

// 🏆 Carte « verdict » récapitulative, insérée juste après la section des scores.
// Reprend verdict + top 3 forces / top 3 axes, et masque les sections doublons.
function renderVerdictHero(d) {
  const results = document.getElementById('results-section');
  if (!results) return;
  document.getElementById('verdict-hero')?.remove();
  const ff = document.getElementById('points-forts')?.closest('.section');
  const vs = document.getElementById('verdict-section');
  if (ff) ff.style.display = '';        // reset (au cas où masqué à l'analyse précédente)

  const forts = (d.points_forts || []).slice(0, 3);
  const axes  = (d.points_ameliorer || []).slice(0, 3);
  if (!d.verdict && !forts.length && !axes.length) return;

  const hero = document.createElement('div');
  hero.id = 'verdict-hero';
  hero.className = 'section';
  hero.setAttribute('data-free-lock', '1');     // cohérence avec le flou freemium
  hero.style.borderLeft = '4px solid var(--primary)';
  const li = (arr) => arr.length ? arr.map(x => `<li>${escapeHtml(String(x))}</li>`).join('') : '<li>—</li>';
  hero.innerHTML = `
    <h2 style="margin-bottom:10px">🏆 Verdict</h2>
    ${d.verdict ? `<p style="font-size:14px;line-height:1.55;margin:0 0 14px">${escapeHtml(d.verdict)}</p>` : ''}
    <div class="two-column">
      <div><h3 style="color:#059669;margin-bottom:6px">✅ Forces clés</h3><ul class="points-list">${li(forts)}</ul></div>
      <div><h3 style="color:#D97706;margin-bottom:6px">⚠️ Axes prioritaires</h3><ul class="points-list neg">${li(axes)}</ul></div>
    </div>`;

  const scoresSection = document.getElementById('scores-grid')?.closest('.section');
  if (scoresSection && scoresSection.parentNode === results) scoresSection.after(hero);
  else results.insertBefore(hero, results.firstChild);

  if (vs) vs.style.display = 'none';    // masque le verdict autonome (doublon)
  if (ff) ff.style.display = 'none';    // masque forts/faibles autonome (doublon)
}

// 🧬 8 dimensions de persuasion en cartes (icône + score + barre + feedback).
function renderDimensions(d) {
  const results = document.getElementById('results-section');
  if (!results) return;
  document.getElementById('dimensions-section')?.remove();
  const dim = d.analyse_8_dimensions;
  if (!dim || typeof dim !== 'object') return;

  const MAP = [
    ['hook', '🎣', 'Hook'],
    ['retention', '⏳', 'Rétention'],
    ['mecanismes_vente', '🧠', 'Mécanismes de vente'],
    ['positionnement', '🎯', 'Positionnement'],
    ['format_visuel', '🎬', 'Format visuel'],
    ['emotion_dominante', '❤️', 'Émotion'],
    ['conversion_shop', '🛒', 'Conversion Shop'],
    ['algorithme', '🚀', 'Algorithme'],
  ];
  const col = (v) => { v = Number(v) || 0; return v >= 70 ? '#059669' : (v >= 45 ? '#D97706' : '#DC2626'); };
  const cards = MAP.map(([k, ic, lbl]) => {
    const o = dim[k];
    if (!o || typeof o !== 'object') return '';
    const sc = Number(o.score) || 0;
    const fb = o.feedback || '';
    return `<div style="background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:12px">
      <div style="display:flex;justify-content:space-between;align-items:center">
        <span style="font-size:13px;font-weight:700">${ic} ${lbl}</span>
        <span style="font-size:14px;font-weight:800;color:${col(sc)}">${Math.round(sc)}<span style="font-size:10px;color:var(--muted)">/100</span></span>
      </div>
      <div style="height:6px;background:var(--border);border-radius:4px;margin:8px 0;overflow:hidden"><div style="height:100%;width:${Math.max(0, Math.min(100, sc))}%;background:${col(sc)}"></div></div>
      ${fb ? `<div style="font-size:12px;color:var(--muted);line-height:1.45">${escapeHtml(String(fb))}</div>` : ''}
    </div>`;
  }).join('');
  if (!cards.trim()) return;

  const sec = document.createElement('div');
  sec.id = 'dimensions-section';
  sec.className = 'section';
  sec.setAttribute('data-free-lock', '1');
  const g = dim.score_persuasion_global;
  sec.innerHTML = `<h2 style="margin-bottom:4px">🧬 8 dimensions de persuasion${g != null ? ` <span style="font-size:13px;color:var(--muted);font-weight:600">· global ${Math.round(g)}/100</span>` : ''}</h2>
    <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:10px;margin-top:10px">${cards}</div>`;

  const anchor = document.getElementById('verdict-hero') || document.getElementById('scores-grid')?.closest('.section');
  if (anchor && anchor.parentNode === results) anchor.after(sec);
  else results.appendChild(sec);
}

// 🧱 Vue verticale : aplatit tout slider existant + masque les sections vides.
// (Remplace buildAnalysisSlider dans le flux. Les fonctions slider restent
// définies plus bas mais ne sont plus appelées — window.__slider reste indéfini.)
function layoutAnalysisVertical() {
  const results = document.getElementById('results-section');
  if (!results) return;
  unwrapAnalysisSlider();
  window.__slider = null;
  // Coach IA (premium) en dernière position s'il existe encore (legacy), et footer
  // (CTA nouvelle analyse + export) toujours tout en bas.
  Array.from(results.children).forEach(el => {
    if (window.getComputedStyle(el).display === 'none') return;
    const hasText = (el.textContent || '').trim().length > 0;
    const hasMedia = el.querySelector('img, canvas, svg, video, button, input, select');
    if (!hasText && !hasMedia) { el.style.display = 'none'; }  // anti-carte blanche
  });
  results.querySelectorAll('[data-slider-footer]').forEach(el => results.appendChild(el));
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
  const _asyncBtn = document.getElementById('analyze-upload-async-btn');
  if (_asyncBtn) _asyncBtn.disabled = true;
  document.getElementById('transcript-section').style.display       = 'none';
  document.getElementById('verdict-section').style.display           = 'none';
  document.getElementById('structure-vente-section').style.display   = 'none';
  document.getElementById('prix-conversion-section').style.display   = 'none';
  document.getElementById('error-box').style.display                = 'none';
  document.getElementById('premium-strategy-section')?.remove();
  document.getElementById('gold-upsell-section')?.remove();
  document.getElementById('winning-structures-section')?.remove();
  document.getElementById('topcreators-multi-section')?.remove();
  document.getElementById('market-category-section')?.remove();
  document.getElementById('similar-products-section')?.remove();
  document.getElementById('popular-products-section')?.remove();
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
  // (Le bouton btn-auth est géré par updateSessionUI → menu burger ; on n'y touche plus ici.)
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
  maybeAskTestimonial(entries.length);
  try { renderProgressionChart(); } catch (e) {}
}

/* Relance avis : après 5 analyses, on invite (1 seule fois) à laisser un avis.
   Envoi email géré côté serveur (anti-doublon par compte). */
function maybeAskTestimonial(count) {
  try {
    if (count < 5) return;
    if (localStorage.getItem('tts_testimonial_asked')) return;
    if (typeof SESSION === 'undefined' || !SESSION.email) return;  // besoin d'un compte pour l'email
    localStorage.setItem('tts_testimonial_asked', '1');
    const tok = localStorage.getItem('tts_token') || '';
    fetch('/api/request-testimonial-email', {
      method: 'POST',
      headers: tok ? { 'Authorization': 'Bearer ' + tok } : {},
    }).catch(() => {});
  } catch (e) {}
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
  const container = document.getElementById('tab-account-content') || document.getElementById('account-content');
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
        <div id="tiktok-data" style="margin-top:14px"></div>

        <div style="border-top:1px solid var(--border);margin:16px 0 12px"></div>
        <div style="font-size:13px;font-weight:600;color:var(--text);margin-bottom:6px">📊 Statistiques d'audience</div>
        <div id="tiktok-biz-status" style="font-size:12px;color:var(--muted);line-height:1.5;margin-bottom:10px">Connecte ton compte pour voir la démographie de ton audience (âge, genre, pays).</div>
        <button class="btn btn-secondary" id="tiktok-biz-btn" onclick="connectTikTokBusiness()" style="width:100%">📈 Connecter mes statistiques d'audience</button>
        <div id="tiktok-insights" style="margin-top:14px"></div>
      </div>`;

  // 💎 Crédits (AI Prompt Studio) — balance + achat
  html += `
      <div style="background:var(--bg);border-radius:12px;padding:16px;margin-bottom:16px;border:1px solid var(--border)">
        <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;margin-bottom:10px">
          <div style="font-size:13px;font-weight:600;color:var(--text)">💎 Crédits AI Prompt Studio</div>
          <div style="font-size:13px"><strong id="acc-credit-total">—</strong> dispo <span id="acc-credit-detail" style="font-size:11px;color:var(--muted)"></span></div>
        </div>
        <div id="acc-credits-packs" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:10px"></div>
      </div>`;

  // 🔔 Notifications (opt-in Web Push)
  html += `
      <div id="push-card" style="display:none;background:var(--bg);border-radius:12px;padding:16px;margin-bottom:16px;border:1px solid var(--border)">
        <div style="font-size:13px;font-weight:600;color:var(--text);margin-bottom:6px">🔔 Notifications</div>
        <div id="push-desc" style="font-size:12.5px;color:var(--muted);margin-bottom:10px">Reçois une alerte pour les nouveautés et les rappels utiles.</div>
        <button id="push-btn" class="btn btn-primary" style="font-size:13px" onclick="togglePush()">🔔 Activer les notifications</button>
      </div>`;

  // Historique des analyses : déplacé vers "📊 Mes analyses" (DB Supabase
  // cross-device). L'ancien bloc localStorage n'est plus rendu ici.

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
  initPushUI();              // opt-in notifications
  renderAccountCredits();    // balance + packs crédits
}

/* ── FEATURE 3 — Graphe de progression (client-side, depuis localStorage) ── */
function renderProgressionChart() {
  const box = document.getElementById('progression-chart');
  const card = document.getElementById('progression-card');
  if (!box) return;
  const showCard = () => { if (card) card.style.display = ''; };
  const hideCard = () => { if (card) card.style.display = 'none'; };
  const tier = (window.__userInfo?.tier || 'free').toLowerCase();
  const isPaid = ['pro', 'gold', 'agency', 'beta', 'admin'].includes(tier) || window.__userInfo?.is_admin;

  // Données : derniers scores, du plus ancien au plus récent (max 15)
  const pts = getHistory()
    .filter(e => typeof e.score_global === 'number')
    .slice(0, 15).reverse()
    .map(e => ({ v: e.score_global, d: e.date }));

  // Masquage propre : pas de carte vide qui encombre le haut de l'onglet.
  if (isPaid && pts.length < 2) { hideCard(); return; }
  if (!isPaid && pts.length < 1) { hideCard(); return; }
  showCard();

  if (!isPaid) {
    // Aperçu flou + incitation upgrade (pas un message d'erreur sec)
    box.innerHTML =
      `<div style="position:relative">
         <div style="filter:blur(5px);pointer-events:none">${_chartSVG([62, 55, 68, 71, 65, 78, 74, 83])}</div>
         <div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:8px;background:rgba(255,255,255,.45)">
           <div style="font-size:22px">🔒</div>
           <div style="font-size:13px;font-weight:700">Suis ta progression dans le temps</div>
           <button class="btn btn-primary" style="font-size:12px;padding:7px 14px" onclick="switchTab('pricing')">Débloquer avec PRO 👑</button>
         </div>
       </div>`;
    return;
  }
  if (pts.length < 2) {
    box.innerHTML = `<div style="text-align:center;color:var(--muted);font-size:13px;padding:18px">Analyse au moins 2 vidéos pour visualiser ta progression 📊</div>`;
    return;
  }
  const vals = pts.map(p => p.v);
  const avg = Math.round(vals.reduce((a, b) => a + b, 0) / vals.length);
  const last = vals[vals.length - 1], first = vals[0];
  const trend = last - first;
  const trendTxt = trend > 0 ? `📈 +${trend} pts depuis le début` : trend < 0 ? `📉 ${trend} pts` : '➡️ stable';
  box.innerHTML = _chartSVG(vals) +
    `<div style="display:flex;justify-content:space-between;font-size:12px;color:var(--muted);margin-top:8px">
       <span>${pts.length} analyses · moyenne <strong style="color:var(--text)">${avg}/100</strong></span>
       <span style="font-weight:600;color:${trend >= 0 ? '#16A34A' : '#DC2626'}">${trendTxt}</span>
     </div>`;
}

/* ── FEATURE 4 — Partage du score en story TikTok (9:16) ─────────────────── */
function _scoreCardCanvas(score, productName) {
  const W = 1080, H = 1920;
  const cv = document.createElement('canvas');
  cv.width = W; cv.height = H;
  const c = cv.getContext('2d');

  // Fond dégradé brand
  const g = c.createLinearGradient(0, 0, 0, H);
  g.addColorStop(0, '#1F3A70'); g.addColorStop(1, '#0C1730');
  c.fillStyle = g; c.fillRect(0, 0, W, H);

  c.textAlign = 'center';

  // Marque
  c.fillStyle = '#FFFFFF';
  c.font = '700 56px -apple-system, Segoe UI, sans-serif';
  c.fillText('Qeerah', W / 2, 220);
  c.fillStyle = 'rgba(255,255,255,.6)';
  c.font = '400 32px -apple-system, Segoe UI, sans-serif';
  c.fillText('Analyse TikTok Shop par l\'IA', W / 2, 280);

  // Anneau de score
  const cx = W / 2, cy = 820, r = 300;
  const col = score >= 75 ? '#22C55E' : score >= 50 ? '#D4AF37' : '#EF4444';
  c.lineWidth = 46;
  c.strokeStyle = 'rgba(255,255,255,.12)';
  c.beginPath(); c.arc(cx, cy, r, 0, Math.PI * 2); c.stroke();
  c.strokeStyle = col;
  c.lineCap = 'round';
  c.beginPath();
  c.arc(cx, cy, r, -Math.PI / 2, -Math.PI / 2 + (Math.PI * 2 * (Math.max(0, Math.min(100, score)) / 100)));
  c.stroke();

  // Score chiffre
  c.fillStyle = '#FFFFFF';
  c.font = '800 260px -apple-system, Segoe UI, sans-serif';
  c.fillText(String(score), cx, cy + 70);
  c.fillStyle = 'rgba(255,255,255,.55)';
  c.font = '600 64px -apple-system, Segoe UI, sans-serif';
  c.fillText('/ 100', cx, cy + 200);

  // Label
  c.fillStyle = col;
  c.font = '700 44px -apple-system, Segoe UI, sans-serif';
  c.fillText('SCORE DE PERSUASION', cx, 480);

  // Produit (optionnel)
  if (productName) {
    c.fillStyle = 'rgba(255,255,255,.9)';
    c.font = '600 42px -apple-system, Segoe UI, sans-serif';
    let p = String(productName);
    if (p.length > 34) p = p.slice(0, 33) + '…';
    c.fillText('📦 ' + p, cx, 1280);
  }

  // CTA / site
  c.fillStyle = 'rgba(255,255,255,.95)';
  c.font = '700 46px -apple-system, Segoe UI, sans-serif';
  c.fillText('Analyse ta vidéo gratuitement', cx, 1640);
  c.fillStyle = '#D4AF37';
  c.font = '700 50px -apple-system, Segoe UI, sans-serif';
  c.fillText('qeerah.com', cx, 1720);

  return cv;
}

async function shareScoreCard(mode) {
  const d = window._lastAnalysis;
  const score = d && typeof d.score_global === 'number' ? d.score_global : parseInt(document.getElementById('score-global')?.textContent) || 0;
  if (!score) { showToast('Lance une analyse d\'abord.'); return; }
  const product = (d && d.detection && d.detection.produit) ? d.detection.produit : null;
  const cv = _scoreCardCanvas(score, product);

  const blob = await new Promise(res => cv.toBlob(res, 'image/png', 0.92));
  if (!blob) { showToast('Génération impossible.'); return; }
  const file = new File([blob], 'mon-score-tts.png', { type: 'image/png' });

  if (mode === 'share' && navigator.canShare && navigator.canShare({ files: [file] })) {
    try {
      await navigator.share({
        files: [file],
        title: 'Mon score Qeerah',
        text: `Mon score de persuasion : ${score}/100 — analysé sur qeerah.com`,
      });
      return;
    } catch (e) {
      if (e && e.name === 'AbortError') return;   // l'utilisateur a annulé
    }
  }
  // Fallback universel : téléchargement
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'mon-score-tts.png';
  document.body.appendChild(a); a.click(); a.remove();
  URL.revokeObjectURL(a.href);
  if (mode === 'share') showToast('Visuel téléchargé — partage-le en story TikTok 📲');
  else showToast('Visuel téléchargé ✓');
}

function _chartSVG(vals) {
  const W = 320, H = 150, pad = 24;
  const n = vals.length;
  const max = 100, min = 0;
  const x = i => pad + (n === 1 ? 0 : (i * (W - 2 * pad) / (n - 1)));
  const y = v => H - pad - ((v - min) / (max - min)) * (H - 2 * pad);
  const avg = vals.reduce((a, b) => a + b, 0) / n;
  const linePts = vals.map((v, i) => `${x(i).toFixed(1)},${y(v).toFixed(1)}`).join(' ');
  const area = `${pad},${H - pad} ${linePts} ${x(n - 1).toFixed(1)},${H - pad}`;
  const dots = vals.map((v, i) => `<circle cx="${x(i).toFixed(1)}" cy="${y(v).toFixed(1)}" r="3" fill="#2563EB"/>`).join('');
  const grid = [0, 25, 50, 75, 100].map(g =>
    `<line x1="${pad}" y1="${y(g).toFixed(1)}" x2="${W - pad}" y2="${y(g).toFixed(1)}" stroke="#E5E7EB" stroke-width="1"/>` +
    `<text x="2" y="${(y(g) + 3).toFixed(1)}" font-size="9" fill="#9CA3AF">${g}</text>`).join('');
  return `<svg viewBox="0 0 ${W} ${H}" width="100%" style="display:block">
    ${grid}
    <line x1="${pad}" y1="${y(avg).toFixed(1)}" x2="${W - pad}" y2="${y(avg).toFixed(1)}" stroke="#D4AF37" stroke-width="1.5" stroke-dasharray="4 3"/>
    <polygon points="${area}" fill="rgba(37,99,235,.08)"/>
    <polyline points="${linePts}" fill="none" stroke="#2563EB" stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round"/>
    ${dots}
  </svg>`;
}

// Crédits dans la page compte : balance + packs (achat stubé tant que Stripe off).
async function renderAccountCredits() {
  loadVpBalance();   // met aussi à jour acc-credit-total / acc-credit-detail
  const token = localStorage.getItem('tts_token');
  try {
    const res = await fetch('/api/credits/packs', { headers: token ? { 'Authorization': 'Bearer ' + token } : {} });
    const data = await res.json();
    const box = document.getElementById('acc-credits-packs');
    if (!box || !data.packs) return;
    box.innerHTML = Object.entries(data.packs).map(([k, p]) => `
      <div style="background:var(--surface);border:1px solid ${p.best ? '#D4AF37' : 'var(--border)'};border-radius:10px;padding:12px;text-align:center">
        ${p.best ? '<div style="font-size:10px;color:#D4AF37;font-weight:700">⭐ BEST</div>' : ''}
        <div style="font-size:13px;font-weight:700">${escapeHtml(p.label)}</div>
        <div style="font-size:12px;color:var(--muted)">${p.credits} crédits</div>
        <div style="font-size:18px;font-weight:800;margin:6px 0;color:var(--primary)">${p.price}€</div>
        <button class="btn btn-primary" style="width:100%;font-size:12px" onclick="buyCredits('${k}')">Acheter</button>
      </div>`).join('');
  } catch (e) {}
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
    const providers = data.providers || {};

    // Provider display (vidéos + perfs)
    if (providers.display?.connected) {
      statusEl.innerHTML = `✅ Compte TikTok connecté${providers.display.seller_name ? ' — <strong>' + escapeHtml(providers.display.seller_name) + '</strong>' : ''}.`;
      if (btn) btn.textContent = '🔄 Reconnecter mon compte TikTok';
      loadTikTokData();
    } else {
      statusEl.textContent = 'Aucun compte TikTok connecté pour le moment.';
    }

    // Provider business (audience)
    const bizStatus = document.getElementById('tiktok-biz-status');
    const bizBtn = document.getElementById('tiktok-biz-btn');
    if (providers.business?.connected) {
      if (bizStatus) bizStatus.innerHTML = '✅ Statistiques d\'audience connectées.';
      if (bizBtn) bizBtn.textContent = '🔄 Reconnecter mes statistiques';
      loadTikTokInsights();
    }
  } catch (e) {
    statusEl.textContent = 'Aucun compte TikTok connecté pour le moment.';
  }
}

// Récupère et affiche le profil + les vidéos (avec métriques réelles) du compte TikTok.
async function loadTikTokData() {
  const box = document.getElementById('tiktok-data');
  if (!box) return;
  const token = localStorage.getItem('tts_token');
  if (!token) return;
  box.innerHTML = '<div style="font-size:13px;color:var(--muted)">Chargement de tes données TikTok…</div>';
  try {
    const res = await fetch('/api/tiktok/me', { headers: { 'Authorization': 'Bearer ' + token } });
    const data = await res.json();
    if (!data.connected) { box.innerHTML = ''; return; }
    const p = data.profile || {};
    const videos = data.videos || [];

    const fmt = (n) => {
      n = Number(n) || 0;
      if (n >= 1e6) return (n / 1e6).toFixed(1).replace('.0', '') + 'M';
      if (n >= 1e3) return (n / 1e3).toFixed(1).replace('.0', '') + 'k';
      return String(n);
    };

    let html = '';
    // Profil
    html += `
      <div style="display:flex;align-items:center;gap:12px;background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:12px;margin-bottom:12px">
        ${p.avatar_url ? `<img src="${escapeHtml(p.avatar_url)}" alt="" style="width:48px;height:48px;border-radius:50%;object-fit:cover">` : ''}
        <div style="flex:1;min-width:0">
          <div style="font-weight:700;color:var(--text)">${escapeHtml(p.display_name || 'Mon compte TikTok')}</div>
          <div style="font-size:12px;color:var(--muted)">
            ${fmt(p.follower_count)} abonnés · ${fmt(p.likes_count)} likes · ${fmt(p.video_count)} vidéos
          </div>
        </div>
      </div>`;

    // Vidéos
    if (videos.length) {
      html += `<div style="font-size:12px;font-weight:600;color:var(--text);margin-bottom:8px">📹 Tes vidéos récentes (performances réelles)</div>`;
      html += '<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(120px,1fr));gap:10px">';
      videos.forEach(v => {
        const cover = v.cover_image_url || '';
        const title = v.title || v.video_description || 'Vidéo';
        html += `
          <div style="background:var(--surface);border:1px solid var(--border);border-radius:10px;overflow:hidden">
            ${cover ? `<div style="aspect-ratio:9/16;background:#000 url('${escapeHtml(cover)}') center/cover"></div>` : ''}
            <div style="padding:8px">
              <div style="font-size:11px;color:var(--text);line-height:1.3;max-height:2.6em;overflow:hidden">${escapeHtml(title)}</div>
              <div style="font-size:11px;color:var(--muted);margin-top:6px;display:flex;flex-wrap:wrap;gap:6px">
                <span>👁 ${fmt(v.view_count)}</span>
                <span>❤️ ${fmt(v.like_count)}</span>
                <span>💬 ${fmt(v.comment_count)}</span>
              </div>
            </div>
          </div>`;
      });
      html += '</div>';
    } else {
      html += `<div style="font-size:12px;color:var(--muted)">Aucune vidéo récupérée (compte sans vidéos publiques ou autorisation limitée).</div>`;
    }
    box.innerHTML = html;
  } catch (e) {
    box.innerHTML = '<div style="font-size:12px;color:var(--muted)">Impossible de charger les données TikTok pour le moment.</div>';
  }
}

async function startTikTokConnect(provider) {
  const token = localStorage.getItem('tts_token');
  if (!token) { showToast('Connecte-toi d\'abord.'); return; }
  try {
    const res = await fetch('/api/auth/tiktok/login?provider=' + encodeURIComponent(provider), {
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
function connectTikTokShop()     { return startTikTokConnect('display'); }
function connectTikTokBusiness() { return startTikTokConnect('business'); }

// Récupère et affiche les insights d'audience (provider business).
async function loadTikTokInsights() {
  const box = document.getElementById('tiktok-insights');
  if (!box) return;
  const token = localStorage.getItem('tts_token');
  if (!token) return;
  box.innerHTML = '<div style="font-size:12px;color:var(--muted)">Chargement de ton audience…</div>';
  try {
    const res = await fetch('/api/tiktok/insights', { headers: { 'Authorization': 'Bearer ' + token } });
    const data = await res.json();
    if (!data.connected || !data.insights) { box.innerHTML = ''; return; }
    const ins = data.insights;

    const renderBreakdown = (title, arr, labelKey) => {
      if (!Array.isArray(arr) || !arr.length) return '';
      const total = arr.reduce((s, x) => s + (Number(x.percentage ?? x.value ?? 0) || 0), 0) || 1;
      const rows = arr.slice(0, 6).map(x => {
        const label = x[labelKey] ?? x.name ?? x.label ?? '—';
        const val = Number(x.percentage ?? x.value ?? 0) || 0;
        const pct = Math.round((val / total) * 100);
        return `
          <div style="margin:4px 0">
            <div style="display:flex;justify-content:space-between;font-size:11px;color:var(--text)">
              <span>${escapeHtml(String(label))}</span><span>${pct}%</span>
            </div>
            <div style="height:6px;background:var(--border);border-radius:4px;overflow:hidden">
              <div style="height:100%;width:${pct}%;background:var(--accent)"></div>
            </div>
          </div>`;
      }).join('');
      return `<div style="margin-bottom:12px"><div style="font-size:12px;font-weight:600;color:var(--text);margin-bottom:4px">${title}</div>${rows}</div>`;
    };

    let html = '<div style="background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:14px">';
    html += renderBreakdown('👥 Genre', ins.audience_genders, 'gender');
    html += renderBreakdown('🎂 Âge', ins.audience_ages, 'age');
    html += renderBreakdown('🌍 Pays', ins.audience_countries, 'country');
    if (!ins.audience_genders && !ins.audience_ages && !ins.audience_countries) {
      html += '<div style="font-size:12px;color:var(--muted)">Données d\'audience pas encore disponibles (compte récent ou volume insuffisant côté TikTok).</div>';
    }
    html += '</div>';
    box.innerHTML = html;
  } catch (e) {
    box.innerHTML = '<div style="font-size:12px;color:var(--muted)">Impossible de charger l\'audience pour le moment.</div>';
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

// ── 🔥 RECO MARCHÉ AUTO (post-analyse) : créateurs + produits de la catégorie ──
// Catégorie marché : on privilégie celle classée par l'IA d'analyse
// (detection.categorie_marche), sinon repli sur la détection par mots-clés.
function getAnalysisCategory(d) {
  const valid = ['beaute', 'mode', 'tech', 'fitness', 'sante', 'maison'];
  const ai = String((d && d.detection && d.detection.categorie_marche) || '').toLowerCase().trim();
  if (valid.includes(ai)) return ai;
  try { return detectProductCategory((d && d.detection && d.detection.produit) || ''); } catch (e) { return null; }
}

// ── 🌍 Pays marché (TikTok Shop) ─────────────────────────────────────────────
const MARKET_COUNTRIES = [
  { code: 'US', flag: '🇺🇸', name: 'États-Unis' },
  { code: 'GB', flag: '🇬🇧', name: 'Royaume-Uni' },
  { code: 'BR', flag: '🇧🇷', name: 'Brésil' },
  { code: 'DE', flag: '🇩🇪', name: 'Allemagne' },
  { code: 'FR', flag: '🇫🇷', name: 'France' },
  { code: 'ES', flag: '🇪🇸', name: 'Espagne' },
  { code: 'IT', flag: '🇮🇹', name: 'Italie' },
  { code: 'ID', flag: '🇮🇩', name: 'Indonésie' },
  { code: 'MY', flag: '🇲🇾', name: 'Malaisie' },
];
function _userRegion() {
  const lang = (document.documentElement.lang || navigator.language || 'fr').slice(0, 2).toLowerCase();
  return ({ fr: 'FR', en: 'US', pt: 'BR', es: 'ES', it: 'IT', de: 'DE', id: 'ID', ms: 'MY' })[lang] || 'US';
}
function _orderedCountries() {
  const ur = _userRegion();
  const found = MARKET_COUNTRIES.find(c => c.code === ur);
  const rest = MARKET_COUNTRIES.filter(c => c.code !== ur);
  return found ? [found, ...rest] : MARKET_COUNTRIES.slice();
}

// 👑 Analyse : « Créateurs gagnants de la catégorie » (chaîne produits → créateurs).
function renderCategoryCreators(d) {
  const results = document.getElementById('results-section');
  if (!results) return;
  document.getElementById('topcreators-multi-section')?.remove();

  const category = getAnalysisCategory(d);
  const catLabels = { beaute:'Beauté', fashion:'Mode', mode:'Mode', tech:'Tech & Gadgets', fitness:'Fitness', sante:'Santé', complement_sante:'Santé', electromenager:'Maison', maison:'Maison' };
  const catLabel = category ? (catLabels[category] || category) : null;

  const sec = document.createElement('section');
  sec.id = 'topcreators-multi-section';
  sec.className = 'section';
  sec.setAttribute('data-free-lock', '1');
  sec.innerHTML = `<h2>👑 Créateurs gagnants${catLabel ? ` en « ${escapeHtml(catLabel)} »` : ''}</h2>
    <p style="font-size:12px;color:var(--muted);margin:4px 0 10px">📅 30 derniers jours — créateurs actifs sur les best-sellers de la catégorie.</p>
    <div id="tcm-body" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:10px">⏳ Chargement…</div>`;
  results.appendChild(sec);

  (async () => {
    const token = localStorage.getItem('tts_token');
    const headers = token ? { 'Authorization': 'Bearer ' + token } : {};
    try {
      const res = await fetch('/api/market/category-creators?region=' + _userRegion() + '&category=' + encodeURIComponent(category || ''), { headers });
      const data = await res.json();
      if (!data.ok || !data.creators || !data.creators.length) { sec.remove(); return; }
      const preview = data.preview;
      let html = '';
      data.creators.forEach((c, i) => {
        const locked = preview && i >= 1;
        const blur = locked ? 'filter:blur(4px);pointer-events:none' : '';
        const link = locked ? '#' : (c.profile_url || '#');
        html += `<a href="${escapeHtml(link)}" ${locked ? '' : 'target="_blank" rel="noopener"'} style="text-decoration:none;color:inherit;${blur}">
          <div style="background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:12px;text-align:center">
            <div style="margin:0 auto 8px;width:54px">${_avatarBadge(c.nickname, 54)}</div>
            <div style="font-size:12px;font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">${escapeHtml((c.nickname || '').slice(0, 22))}</div>
            <div style="font-size:10px;color:var(--muted);margin-top:4px">👥 ${_cfmt(c.followers)} · 👁 ${_cfmt(c.views)}</div>
          </div></a>`;
      });
      document.getElementById('tcm-body').innerHTML = html;
    } catch (e) {
      sec.remove();
    }
  })();
}

// 👑 (legacy) top 3 créateurs sur 3 pays aléatoires — conservé, non appelé.
function renderTopCreatorsMultiCountry(d) {
  const results = document.getElementById('results-section');
  if (!results) return;
  document.getElementById('topcreators-multi-section')?.remove();

  const pool = MARKET_COUNTRIES.slice();
  for (let i = pool.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [pool[i], pool[j]] = [pool[j], pool[i]]; }
  const picks = pool.slice(0, 3);
  let category = null;
  try { category = detectProductCategory((d.detection && d.detection.produit) || ''); } catch (e) { category = null; }

  const sec = document.createElement('section');
  sec.id = 'topcreators-multi-section';
  sec.className = 'section';
  sec.setAttribute('data-free-lock', '1');
  sec.innerHTML = `<h2>👑 Top créateurs dans le monde</h2>
    <p style="font-size:12px;color:var(--muted);margin:4px 0 10px">📅 30 derniers jours · 3 marchés au hasard — les créateurs qui vendent le plus.</p>
    <div id="tcm-body" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:14px">⏳ Chargement…</div>`;
  results.appendChild(sec);

  (async () => {
    const token = localStorage.getItem('tts_token');
    const headers = token ? { 'Authorization': 'Bearer ' + token } : {};
    const datas = await Promise.all(picks.map(c =>
      fetch(`/api/market/creators?region=${c.code}&category=${encodeURIComponent(category || '')}`, { headers })
        .then(r => r.json()).catch(() => null)));
    let html = ''; let any = false;
    datas.forEach((data, idx) => {
      const c = picks[idx];
      if (!data || !data.ok || !data.creators || !data.creators.length) return;
      any = true;
      const preview = data.preview;
      const rows = data.creators.slice(0, 3).map((cr, i) => {
        const locked = preview && i >= 1;
        const blur = locked ? 'filter:blur(4px);pointer-events:none' : '';
        const link = locked ? '#' : (cr.profile_url || '#');
        return `<a href="${escapeHtml(link)}" ${locked ? '' : 'target="_blank" rel="noopener"'} style="display:flex;align-items:center;gap:8px;padding:5px 4px;text-decoration:none;color:inherit;${blur}">
          ${_avatarBadge(cr.unique_id, 34)}
          <div style="min-width:0">
            <div style="font-size:12px;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">@${escapeHtml(cr.unique_id || '')}</div>
            <div style="font-size:10px;color:var(--muted)">📦 ${_cfmt(cr.sales)} · 👥 ${_cfmt(cr.followers)}</div>
          </div></a>`;
      }).join('');
      html += `<div style="background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:12px">
        <div style="font-size:13px;font-weight:700;margin-bottom:8px">${c.flag} ${escapeHtml(c.name)}</div>${rows}</div>`;
    });
    if (!any) { sec.remove(); return; }
    document.getElementById('tcm-body').innerHTML = html;
  })();
}

function renderMarketForCategory(d) {
  const results = document.getElementById('results-section');
  if (!results) return;
  document.getElementById('market-category-section')?.remove();

  const category = getAnalysisCategory(d);

  // Pas de catégorie détectée → on n'affiche PAS un top global (produits sans
  // rapport avec la vidéo). La pertinence produit est assurée par « Produits
  // similaires en tendance » (recherche par nom de produit).
  if (!category) return;
  const catLabels = { beaute:'Beauté', fashion:'Mode', mode:'Mode', tech:'Tech & Gadgets', fitness:'Fitness', sante:'Santé', complement_sante:'Santé', electromenager:'Maison', maison:'Maison' };
  const catLabel = catLabels[category] || category;
  const titleHtml = `🔥 Top produits en « ${escapeHtml(catLabel)} »`;

  const sec = document.createElement('section');
  sec.id = 'market-category-section';
  sec.className = 'section';
  sec.innerHTML = `<h2>${titleHtml}</h2>
    <div id="market-cat-body" style="font-size:13px;color:var(--muted)">⏳ Chargement du marché…</div>`;
  results.appendChild(sec);

  (async () => {
    const body = document.getElementById('market-cat-body');
    const token = localStorage.getItem('tts_token');
    try {
      // Produits ciblés sur la RÉGION de l'utilisateur (un produit US n'est pas
      // achetable en FR) — les créateurs, eux, restent multi-pays.
      const res = await fetch('/api/market/category?region=' + _userRegion() + '&category=' + encodeURIComponent(category || ''), {
        headers: token ? { 'Authorization': 'Bearer ' + token } : {}
      });
      const data = await res.json();
      // Les créateurs sont désormais affichés par le bloc « Top créateurs (3 pays) ».
      // Ici on ne garde que les PRODUITS qui se vendent.
      if (!data.ok || !data.products?.length) {
        sec.remove(); return;
      }
      const preview = data.preview;
      let html = '';

      if (data.products?.length) {
        html += `<div style="font-size:13px;font-weight:700;color:var(--text);margin:4px 0 8px">🛍️ Top produits — 30 derniers jours</div>`;
        html += '<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:10px">';
        data.products.forEach((p, i) => {
          const locked = preview && i >= 1;
          const blur = locked ? 'filter:blur(5px);pointer-events:none' : '';
          const link = locked ? '#' : (p.url || '#');
          html += `<a href="${escapeHtml(link)}" ${locked?'':'target="_blank" rel="noopener"'} style="text-decoration:none;color:inherit;${blur}">
            <div style="background:var(--surface);border:1px solid var(--border);border-radius:10px;overflow:hidden">
              ${p.image ? `<img src="${escapeHtml(_imgProxy(p.image))}" alt="" loading="lazy" referrerpolicy="no-referrer" onerror="this.style.display='none'" style="width:100%;height:110px;object-fit:cover">` : ''}
              <div style="padding:8px">
                <div style="font-size:11px;line-height:1.3;max-height:2.6em;overflow:hidden">${escapeHtml(p.name||'Produit')}</div>
                <div style="font-size:12px;color:var(--primary);font-weight:700;margin-top:3px">$${escapeHtml(String(p.price||'—'))}</div>
                <div style="font-size:10px;color:#059669">📦 ${_cfmt(p.sales)} ventes</div>
              </div>
            </div></a>`;
        });
        html += '</div>';
      }

      if (preview) {
        html += `<div style="margin-top:14px;background:rgba(255,215,0,.10);border:1px dashed rgba(255,200,40,.6);border-radius:10px;padding:12px;text-align:center">
          <strong style="color:#d4a017">Passe au plan Gold</strong> pour voir tous les créateurs et produits gagnants de cette catégorie.
          <div style="margin-top:8px"><button class="btn btn-primary" onclick="switchTab('pricing')" style="font-size:13px">Débloquer Gold 👑</button></div>
        </div>`;
      } else {
        html += `<div style="margin-top:12px;text-align:center"><button class="btn btn-secondary" onclick="switchTab('creators')" style="font-size:13px">Voir tous les créateurs gagnants →</button></div>`;
      }

      body.innerHTML = html;
      if (window.__slider) { try { updateSliderHeight(window.__slider.index); } catch (e) {} }
    } catch (e) {
      sec.remove();
    }
  })();
}

// ── 🛍️ PRODUITS SIMILAIRES EN TENDANCE (realtime product/search) ─────────────
function renderSimilarProducts(d) {
  const results = document.getElementById('results-section');
  if (!results) return;
  document.getElementById('similar-products-section')?.remove();

  const productName = (d.detection && d.detection.produit) || '';
  if (!productName || productName.length < 3) return;  // pas de mot-clé exploitable

  const sec = document.createElement('section');
  sec.id = 'similar-products-section';
  sec.className = 'section';
  sec.innerHTML = `<h2>🛍️ Produits similaires en tendance</h2>
    <div id="similar-products-body" style="font-size:13px;color:var(--muted)">⏳ Recherche des best-sellers…</div>`;
  results.appendChild(sec);

  (async () => {
    const body = document.getElementById('similar-products-body');
    const token = localStorage.getItem('tts_token');
    const headers = token ? { 'Authorization': 'Bearer ' + token } : {};
    const fetchSearch = (region) => fetch('/api/market/products/search?region=' + region + '&keyword=' + encodeURIComponent(productName), { headers }).then(r => r.json()).catch(() => null);
    try {
      // Région utilisateur d'abord ; si le catalogue local est vide (fréquent hors US),
      // on retombe sur US pour avoir des produits similaires en inspiration.
      let data = await fetchSearch(_userRegion());
      if ((!data || !data.ok || !data.products || !data.products.length) && _userRegion() !== 'US') {
        data = await fetchSearch('US');
      }
      if (!data || !data.ok || !data.products || !data.products.length) { sec.remove(); return; }
      const preview = data.preview;
      let html = '<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:10px">';
      data.products.forEach((p, i) => {
        const locked = preview && i >= 1;
        const blur = locked ? 'filter:blur(5px);pointer-events:none' : '';
        const link = locked ? '#' : (p.url || '#');
        const price = p.price ? `${escapeHtml(String(p.price))}` : '—';
        html += `<a href="${escapeHtml(link)}" ${locked?'':'target="_blank" rel="noopener"'} style="text-decoration:none;color:inherit;${blur}">
          <div style="background:var(--surface);border:1px solid var(--border);border-radius:10px;overflow:hidden">
            ${p.image ? `<img src="${escapeHtml(_imgProxy(p.image))}" alt="" loading="lazy" referrerpolicy="no-referrer" onerror="this.style.display='none'" style="width:100%;height:110px;object-fit:cover">` : ''}
            <div style="padding:8px">
              <div style="font-size:11px;line-height:1.3;max-height:2.6em;overflow:hidden">${escapeHtml(p.name||'Produit')}</div>
              <div style="font-size:12px;color:var(--primary);font-weight:700;margin-top:3px">${price}</div>
              <div style="font-size:10px;color:#059669">⭐ ${escapeHtml(String(p.rating||'—'))} · 📦 ${_cfmt(p.sales)}</div>
            </div>
          </div></a>`;
      });
      html += '</div>';
      if (preview) {
        html += `<div style="margin-top:14px;background:rgba(255,215,0,.10);border:1px dashed rgba(255,200,40,.6);border-radius:10px;padding:12px;text-align:center">
          <strong style="color:#d4a017">Passe au plan Gold</strong> pour voir tous les produits gagnants similaires.
          <div style="margin-top:8px"><button class="btn btn-primary" onclick="switchTab('pricing')" style="font-size:13px">Débloquer Gold 👑</button></div>
        </div>`;
      }
      body.innerHTML = html;
      if (window.__slider) { try { updateSliderHeight(window.__slider.index); } catch (e) {} }
    } catch (e) {
      sec.remove();
    }
  })();
}

// ── 📸 PHOTO SLIDE COACH (Gold/Agency) ───────────────────────────────────────
let _psImageB64 = null;   // image produit en base64 (sans préfixe data:)

const PS_PREMIUM_TIERS = ['gold', 'agency', 'beta', 'admin'];

async function initPhotoSlideTab() {
  // L'info plan est chargée en asynchrone → on l'attend avant de décider du gate,
  // sinon un beta/admin verrait à tort « Débloquer Gold » au 1er affichage.
  if (!window.__userInfo) {
    try { await (window.__userInfoPromise || fetchUserInfo()); } catch (e) {}
  }
  const tier = (window.__userInfo?.tier || 'free').toLowerCase();
  const premium = PS_PREMIUM_TIERS.includes(tier) || window.__userInfo?.is_admin;
  const gate = document.getElementById('ps-gate');
  const form = document.getElementById('ps-form');
  if (gate) gate.style.display = premium ? 'none' : 'block';
  if (form) form.style.display = premium ? 'block' : 'none';
  if (!premium) return;

  // Branchement upload (une seule fois)
  const drop = document.getElementById('ps-drop');
  const file = document.getElementById('ps-file');
  if (drop && !drop.dataset.bound) {
    drop.dataset.bound = '1';
    drop.addEventListener('click', () => file.click());
    drop.addEventListener('dragover', e => { e.preventDefault(); drop.style.borderColor = '#D4AF37'; });
    drop.addEventListener('dragleave', () => { drop.style.borderColor = 'var(--border)'; });
    drop.addEventListener('drop', e => {
      e.preventDefault(); drop.style.borderColor = 'var(--border)';
      if (e.dataTransfer.files[0]) _psHandleFile(e.dataTransfer.files[0]);
    });
    file.addEventListener('change', e => { if (e.target.files[0]) _psHandleFile(e.target.files[0]); });
  }
}

function _psHandleFile(f) {
  if (!/^image\/(png|jpe?g|webp)$/i.test(f.type)) { showToast('Format image non supporté.'); return; }
  if (f.size > 10 * 1024 * 1024) { showToast('Image trop lourde (max 10 Mo).'); return; }
  const reader = new FileReader();
  reader.onload = () => {
    // Downscale à max 1024px (canvas) → upload léger + pixtral bien plus rapide.
    const img = new Image();
    img.onload = () => {
      const MAX = 1024;
      let { width: w, height: h } = img;
      if (w > MAX || h > MAX) {
        if (w >= h) { h = Math.round(h * MAX / w); w = MAX; }
        else        { w = Math.round(w * MAX / h); h = MAX; }
      }
      let dataUrl;
      try {
        const cv = document.createElement('canvas');
        cv.width = w; cv.height = h;
        cv.getContext('2d').drawImage(img, 0, 0, w, h);
        dataUrl = cv.toDataURL('image/jpeg', 0.85);
      } catch (e) {
        dataUrl = reader.result;   // fallback : image d'origine
      }
      _psImageB64 = String(dataUrl).split(',')[1] || null;
      const prev = document.getElementById('ps-preview');
      const empty = document.getElementById('ps-drop-empty');
      if (prev) { prev.src = dataUrl; prev.style.display = 'block'; }
      if (empty) empty.style.display = 'none';
      const btn = document.getElementById('ps-generate');
      if (btn) btn.disabled = false;
    };
    img.onerror = () => { showToast("Image illisible."); };
    img.src = reader.result;
  };
  reader.readAsDataURL(f);
}

let _psData = {};      // données cumulées (stratégie + contenu) pour rendu progressif
let _psTimerId = null;

function _psStartTimer(msg) {
  const out = document.getElementById('ps-result');
  if (!out) return;
  const t0 = Date.now();
  out.innerHTML = `<div id="ps-loader" style="text-align:center;padding:20px;color:var(--muted)">
    <div style="font-size:14px">${msg}</div>
    <div style="font-size:12px;margin-top:6px">⏱️ <span id="ps-elapsed">0</span>s <span style="opacity:.7">· estimation ~20-40s</span></div></div>`;
  _psStopTimer();
  _psTimerId = setInterval(() => {
    const el = document.getElementById('ps-elapsed');
    if (el) el.textContent = Math.round((Date.now() - t0) / 1000);
  }, 1000);
}
function _psStopTimer() { if (_psTimerId) { clearInterval(_psTimerId); _psTimerId = null; } }
function _psSetLoaderMsg(msg) {
  const l = document.getElementById('ps-loader');
  if (l) { const d = l.querySelector('div'); if (d) d.innerHTML = msg; }
}

async function generatePhotoSlide() {
  if (!_psImageB64) { showToast('Ajoute une image produit.'); return; }
  const btn = document.getElementById('ps-generate');
  const out = document.getElementById('ps-result');
  const token = localStorage.getItem('tts_token');
  btn.disabled = true; btn.textContent = '⏳ Génération…';
  _psData = {};
  _psStartTimer("👁️ L'IA analyse ton image produit…");

  const fd = new FormData();
  fd.append('image', _psImageB64);
  fd.append('product_name', document.getElementById('ps-name')?.value || '');
  fd.append('description', document.getElementById('ps-desc')?.value || '');
  fd.append('price', document.getElementById('ps-price')?.value || '');
  fd.append('currency', document.getElementById('ps-currency')?.value || 'EUR');
  fd.append('niche', document.getElementById('ps-niche')?.value || '');
  fd.append('preferred_style', document.getElementById('ps-style')?.value || 'auto');

  try {
    const res = await fetch('/api/photo-slide/generate', {
      method: 'POST',
      headers: token ? { 'Authorization': 'Bearer ' + token } : {},
      body: fd,
    });
    if (!res.ok) {
      let msg = 'Erreur de génération.';
      try { msg = (await res.json()).detail || msg; } catch (e) {}
      _psStopTimer(); out.innerHTML = `<div style="color:#DC2626;padding:12px">${escapeHtml(msg)}</div>`;
      return;
    }

    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';

    const processBlock = (block) => {
      let evType = 'message'; const dataLines = [];
      for (const raw of block.split('\n')) {
        const line = raw.replace(/\r$/, '');
        if (line.startsWith('event:')) evType = line.slice(6).trim();
        else if (line.startsWith('data:')) dataLines.push(line.slice(5).trim());
      }
      if (!dataLines.length) return;
      let d; try { d = JSON.parse(dataLines.join('\n')); } catch (e) { return; }
      if (evType === 'progress') {
        _psSetLoaderMsg(d.message || '🔄 En cours…');
      } else if (evType === 'strategy') {
        _psStopTimer();                       // 1ʳᵉ partie arrivée → on affiche déjà
        _psData = { ..._psData, ...d };
        renderPhotoSlideResult(_psData, true);  // partiel : slides « en cours »
      } else if (evType === 'content') {
        _psData = { ..._psData, ...d };
        renderPhotoSlideResult(_psData, false);
      } else if (evType === 'error') {
        _psStopTimer(); out.innerHTML = `<div style="color:#DC2626;padding:12px">${escapeHtml(d.error || 'Erreur.')}</div>`;
      }
    };

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });
      let idx;
      while ((idx = buffer.indexOf('\n\n')) !== -1) {
        const block = buffer.slice(0, idx); buffer = buffer.slice(idx + 2);
        if (block.trim()) processBlock(block);
      }
    }
    if (buffer.trim()) processBlock(buffer);
  } catch (e) {
    _psStopTimer();
    out.innerHTML = '<div style="color:#DC2626;padding:12px">Erreur réseau. Réessaie.</div>';
  } finally {
    _psStopTimer();
    btn.disabled = false; btn.textContent = '✨ Régénérer';
    updateCreditIndicator();
  }
}

function _psCopyBtn(text) {
  const enc = encodeURIComponent(text || '');
  return `<button onclick="navigator.clipboard.writeText(decodeURIComponent('${enc}')).then(()=>showToast('Copié ✓'))" style="font-size:11px;padding:3px 8px;border:1px solid var(--border);border-radius:6px;background:var(--surface);color:var(--text);cursor:pointer">📋 Copier</button>`;
}

function renderPhotoSlideResult(r, partial) {
  const out = document.getElementById('ps-result');
  if (!out) return;
  const st = r.type_slide || {};
  const card = (inner) => `<div style="background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:14px;margin-bottom:12px">${inner}</div>`;

  let html = '';
  if (r._fallback) {
    html += `<div style="font-size:11px;color:#d4a017;background:rgba(212,175,55,.1);border-radius:8px;padding:8px;margin-bottom:12px">⚠️ Exemple de démonstration (l'IA n'a pas pu analyser l'image — réessaie).</div>`;
  }

  // 1. Stratégie / type de slide
  html += card(`<div style="font-size:12px;font-weight:700;color:#d4a017;text-transform:uppercase;letter-spacing:.5px">Type de slide recommandé</div>
    <div style="font-size:16px;font-weight:700;margin:4px 0">${escapeHtml(st.label || st.style || '—')}</div>
    <div style="font-size:13px;color:var(--muted)">${escapeHtml(st.justification || '')}</div>`);

  // 2. Hook
  html += card(`<div style="font-size:12px;font-weight:700;color:var(--text)">📌 Hook (1ʳᵉ slide) ${_psCopyBtn(r.hook)}</div>
    <div style="font-size:15px;margin-top:6px">${escapeHtml(r.hook || '')}</div>`);

  // 3. Titre du carrousel + variantes
  let variantes = (r.titre_variantes || []).map(v => `<div style="font-size:13px;color:var(--muted);margin-top:4px">↳ ${escapeHtml(v)}</div>`).join('');
  html += card(`<div style="font-size:12px;font-weight:700;color:var(--text)">🏷️ Titre du carrousel ${_psCopyBtn(r.titre_carrousel)}</div>
    <div style="font-size:15px;font-weight:600;margin-top:6px">${escapeHtml(r.titre_carrousel || '')}</div>${variantes}`);

  // Pendant l'étape 2 : indicateur « rédaction des slides en cours »
  if (partial && !(Array.isArray(r.slides) && r.slides.length)) {
    html += `<div style="text-align:center;padding:14px;color:var(--muted);font-size:13px;background:var(--surface);border:1px dashed var(--border);border-radius:12px">
      ✍️ Rédaction des slides, du CTA et de la description… <span id="ps-elapsed2">⏳</span></div>`;
  }

  // 4. Slides (avec type de photo à prendre)
  if (Array.isArray(r.slides) && r.slides.length) {
    let slidesHtml = r.slides.map(s => {
      const badge = { hook: '#2563EB', value: '#059669', cta: '#D4AF37' }[s.type] || '#6B7280';
      return `<div style="border-left:3px solid ${badge};padding:8px 0 8px 12px;margin-bottom:10px">
        <div style="font-size:11px;font-weight:700;color:${badge};text-transform:uppercase">Slide ${s.numero} · ${escapeHtml(s.type || '')}</div>
        <div style="font-size:14px;font-weight:600;margin-top:3px">${escapeHtml(s.texte || '')}</div>
        ${s.sous_texte ? `<div style="font-size:12px;color:var(--muted)">${escapeHtml(s.sous_texte)}</div>` : ''}
        <div style="font-size:12px;color:var(--text);margin-top:6px">📷 <strong>Photo à prendre :</strong> ${escapeHtml(s.photo_a_prendre || '')}</div>
        ${s.emotion ? `<div style="font-size:11px;color:var(--muted);margin-top:2px">💗 ${escapeHtml(s.emotion)} · 📍 ${escapeHtml(s.position_texte || 'center')}</div>` : ''}
      </div>`;
    }).join('');
    html += card(`<div style="font-size:12px;font-weight:700;color:var(--text);margin-bottom:8px">🎬 Plan slide par slide</div>${slidesHtml}`);
  }

  // 5. CTA
  html += card(`<div style="font-size:12px;font-weight:700;color:var(--text)">🛒 CTA (dernière slide) ${_psCopyBtn(r.cta)}</div>
    <div style="font-size:14px;margin-top:6px">${escapeHtml(r.cta || '')}</div>`);

  // 6. Description optimisée
  html += card(`<div style="font-size:12px;font-weight:700;color:var(--text)">📝 Description optimisée ${_psCopyBtn(r.description_optimisee)}</div>
    <div style="font-size:13px;white-space:pre-wrap;margin-top:6px;color:var(--text)">${escapeHtml(r.description_optimisee || '')}</div>`);

  // 7. Hashtags
  if (Array.isArray(r.hashtags) && r.hashtags.length) {
    const tags = r.hashtags.map(t => '#' + String(t).replace(/^#/, '')).join(' ');
    html += card(`<div style="font-size:12px;font-weight:700;color:var(--text)">#️⃣ Hashtags ${_psCopyBtn(tags)}</div>
      <div style="font-size:13px;color:var(--primary);margin-top:6px">${escapeHtml(tags)}</div>`);
  }

  // 8. Conseils saves
  if (Array.isArray(r.conseils_saves) && r.conseils_saves.length) {
    const tips = r.conseils_saves.map(t => `<li style="margin-bottom:4px">${escapeHtml(t)}</li>`).join('');
    html += card(`<div style="font-size:12px;font-weight:700;color:var(--text)">💾 Maximiser les sauvegardes</div>
      <ul style="font-size:13px;color:var(--muted);margin:6px 0 0;padding-left:18px">${tips}</ul>`);
  }

  out.innerHTML = html;
}

// 🔥 « Populaire chez nos utilisateurs » — reco maison basée sur la mémoire produits.
// Ne s'affiche que s'il y a un vrai signal (≥ 3 produits récurrents dans la catégorie).
function renderPopularProducts(d) {
  const results = document.getElementById('results-section');
  if (!results) return;
  document.getElementById('popular-products-section')?.remove();
  const category = getAnalysisCategory(d);

  (async () => {
    const token = localStorage.getItem('tts_token');
    const headers = token ? { 'Authorization': 'Bearer ' + token } : {};
    let data;
    try {
      const res = await fetch('/api/market/popular?category=' + encodeURIComponent(category || ''), { headers });
      data = await res.json();
    } catch (e) { return; }
    if (!data || !data.ok || !data.products || data.products.length < 3) return;  // pas assez de signal

    const sec = document.createElement('section');
    sec.id = 'popular-products-section';
    sec.className = 'section';
    sec.setAttribute('data-free-lock', '1');
    let html = `<h2>🔥 Populaire chez nos utilisateurs</h2>
      <p style="font-size:12px;color:var(--muted);margin:4px 0 10px">Produits les plus analysés sur l'app${category ? ` en « ${escapeHtml(category)} »` : ''} — un signal qui s'affine avec le temps.</p>
      <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:10px">`;
    data.products.forEach(p => {
      html += `<a href="${escapeHtml(p.url || '#')}" target="_blank" rel="noopener" style="text-decoration:none;color:inherit">
        <div style="background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:12px">
          <div style="font-size:12px;font-weight:600;line-height:1.3;max-height:3.9em;overflow:hidden">${escapeHtml((p.name || 'Produit').slice(0, 80))}</div>
          <div style="font-size:11px;color:var(--primary);font-weight:700;margin-top:6px">🔁 analysé ${_cfmt(p.times_seen)}×</div>
        </div></a>`;
    });
    html += '</div>';
    sec.innerHTML = html;
    results.appendChild(sec);
  })();
}

// ════════════════════════════════════════════════════════════════════════════
// 🎬 AI VIDEO PROMPT STUDIO + 💳 CRÉDITS
// ════════════════════════════════════════════════════════════════════════════
const VP_PREMIUM = ['pro', 'gold', 'agency', 'beta', 'admin'];
const VP_LEVELS = [
  { n: 1, name: 'Simple', cost: 1, desc: '3-5s · B-roll, hook, transition' },
  { n: 2, name: 'Intermédiaire', cost: 2, desc: '5-10s · démo, avant/après' },
  { n: 3, name: 'Complexe', cost: 3, desc: '10-20s · mini-pub narrative' },
  { n: 4, name: 'Vidéo Qeerah', cost: 5, desc: '15-30s · prête à publier ⭐', popular: true },
  { n: 5, name: 'Multi-clips', cost: 10, desc: '30-60s · séquence 3-5 plans' },
];
const VP_PLATFORMS = [
  { id: 'sora2', label: 'Sora 2' }, { id: 'veo3', label: 'Veo 3' }, { id: 'runway', label: 'Runway' },
  { id: 'kling', label: 'Kling' }, { id: 'pika', label: 'Pika' }, { id: 'hailuo', label: 'Hailuo' },
  { id: 'all', label: 'Toutes (+50%)' },
];
const VP_STYLE_GROUPS = [
  { key: 'visual_style', label: 'Style', opts: ['Cinematic', 'Premium/Luxe', 'Minimaliste', 'Lifestyle', 'Naturel', 'Fun/Dynamique', 'Mystérieux'] },
  { key: 'mood', label: 'Ambiance', opts: ['Premium', 'Énergique', 'Calme/Zen', 'Aspirationnel', 'Quotidien', 'Mystérieux'] },
  { key: 'emotion_target', label: 'Émotion', opts: ['Curiosité', 'Désir', 'Aspiration', 'Urgence', 'Validation', 'Frustration→Soulagement'] },
  { key: 'color_tone', label: 'Couleurs', opts: ['Or/Doré', 'Pastel doux', 'Couleurs vives', 'N&B dramatique', 'Naturel/Terreux'] },
];
let _vpLevel = 4, _vpPlatform = 'sora2', _vpImageB64 = null, _vpStyle = {}, _vpLast = null;

function _vpCost() {
  const lvl = VP_LEVELS.find(l => l.n === _vpLevel);
  let c = lvl ? lvl.cost : 1;
  if (_vpPlatform === 'all') c = Math.round(c * 1.5);
  return c;
}
function _vpVal(id) { return document.getElementById(id)?.value || ''; }

async function initPromptStudioTab() {
  if (!window.__userInfo) { try { await (window.__userInfoPromise || fetchUserInfo()); } catch (e) {} }
  const tier = (window.__userInfo?.tier || 'free').toLowerCase();
  const premium = VP_PREMIUM.includes(tier) || window.__userInfo?.is_admin;
  const gate = document.getElementById('vp-gate'), form = document.getElementById('vp-form');
  if (gate) gate.style.display = premium ? 'none' : 'block';
  if (form) form.style.display = premium ? 'block' : 'none';
  if (!premium) return;

  renderVpLevels(); renderVpPlatforms(); renderVpStyles(); updateVpCost();
  loadVpBalance();

  const drop = document.getElementById('vp-drop'), file = document.getElementById('vp-file');
  if (drop && !drop.dataset.bound) {
    drop.dataset.bound = '1';
    drop.addEventListener('click', () => file.click());
    drop.addEventListener('dragover', e => { e.preventDefault(); drop.style.borderColor = '#D4AF37'; });
    drop.addEventListener('dragleave', () => { drop.style.borderColor = 'var(--border)'; });
    drop.addEventListener('drop', e => { e.preventDefault(); drop.style.borderColor = 'var(--border)'; if (e.dataTransfer.files[0]) _vpHandleFile(e.dataTransfer.files[0]); });
    file.addEventListener('change', e => { if (e.target.files[0]) _vpHandleFile(e.target.files[0]); });
  }
}

function renderVpLevels() {
  const box = document.getElementById('vp-levels'); if (!box) return;
  box.innerHTML = VP_LEVELS.map(l => {
    const sel = l.n === _vpLevel;
    return `<div onclick="_vpPick('level',${l.n})" style="cursor:pointer;border:2px solid ${sel ? 'var(--primary)' : 'var(--border)'};background:${sel ? 'rgba(37,99,235,.06)' : 'var(--surface)'};border-radius:10px;padding:10px">
      <div style="font-size:13px;font-weight:700">${escapeHtml(l.name)}${l.popular ? ' <span style="color:#D4AF37">⭐</span>' : ''}</div>
      <div style="font-size:10px;color:var(--muted);margin-top:2px">${escapeHtml(l.desc)}</div>
      <div style="font-size:11px;color:var(--primary);font-weight:700;margin-top:4px">${l.cost} crédit${l.cost > 1 ? 's' : ''}</div>
    </div>`;
  }).join('');
}
function renderVpPlatforms() {
  const box = document.getElementById('vp-platforms'); if (!box) return;
  box.innerHTML = VP_PLATFORMS.map(p => {
    const sel = p.id === _vpPlatform;
    return `<button type="button" onclick="_vpPick('platform','${p.id}')" style="cursor:pointer;border:1px solid ${sel ? 'var(--primary)' : 'var(--border)'};background:${sel ? 'var(--primary)' : 'var(--surface)'};color:${sel ? '#fff' : 'var(--text)'};border-radius:999px;padding:6px 12px;font-size:12px">${escapeHtml(p.label)}</button>`;
  }).join('');
}
function renderVpStyles() {
  const box = document.getElementById('vp-styles'); if (!box) return;
  box.innerHTML = VP_STYLE_GROUPS.map(g => `
    <div style="margin-bottom:10px"><div style="font-size:11px;color:var(--muted);margin-bottom:5px">${escapeHtml(g.label)}</div>
    <div style="display:flex;flex-wrap:wrap;gap:6px">${g.opts.map(o => {
      const sel = _vpStyle[g.key] === o;
      return `<button type="button" onclick="_vpPickStyle('${g.key}','${escapeHtml(o).replace(/'/g, '')}')" style="cursor:pointer;border:1px solid ${sel ? 'var(--primary)' : 'var(--border)'};background:${sel ? 'var(--primary)' : 'var(--surface)'};color:${sel ? '#fff' : 'var(--text)'};border-radius:999px;padding:5px 10px;font-size:11px">${escapeHtml(o)}</button>`;
    }).join('')}</div></div>`).join('');
}
function _vpPick(kind, val) {
  if (kind === 'level') { _vpLevel = val; renderVpLevels(); }
  else { _vpPlatform = val; renderVpPlatforms(); }
  updateVpCost();
}
function _vpPickStyle(key, val) { _vpStyle[key] = (_vpStyle[key] === val ? '' : val); renderVpStyles(); }
function updateVpCost() {
  const b = document.getElementById('vp-cost-badge');
  if (b) b.textContent = `(${_vpCost()} crédit${_vpCost() > 1 ? 's' : ''})`;
}

function _vpHandleFile(f) {
  if (!/^image\/(png|jpe?g|webp)$/i.test(f.type)) { showToast('Format image non supporté.'); return; }
  if (f.size > 10 * 1024 * 1024) { showToast('Image trop lourde (max 10 Mo).'); return; }
  const reader = new FileReader();
  reader.onload = () => {
    const img = new Image();
    img.onload = () => {
      const MAX = 1024; let { width: w, height: h } = img;
      if (w > MAX || h > MAX) { if (w >= h) { h = Math.round(h * MAX / w); w = MAX; } else { w = Math.round(w * MAX / h); h = MAX; } }
      let dataUrl;
      try { const cv = document.createElement('canvas'); cv.width = w; cv.height = h; cv.getContext('2d').drawImage(img, 0, 0, w, h); dataUrl = cv.toDataURL('image/jpeg', 0.85); }
      catch (e) { dataUrl = reader.result; }
      _vpImageB64 = String(dataUrl).split(',')[1] || null;
      const prev = document.getElementById('vp-preview'), empty = document.getElementById('vp-drop-empty');
      if (prev) { prev.src = dataUrl; prev.style.display = 'block'; }
      if (empty) empty.style.display = 'none';
    };
    img.onerror = () => showToast('Image illisible.');
    img.src = reader.result;
  };
  reader.readAsDataURL(f);
}

function applyVpBalance(bal) {
  if (!bal) return;
  const total = bal.total_available ?? '—';
  const sub = bal.subscription || {}, pur = bal.purchased || {};
  const detail = `(abo ${sub.remaining ?? 0}/${sub.total ?? 0}${pur.remaining ? ` + ${pur.remaining} achetés` : ''})`;
  [['vp-credit-total', 'vp-credit-detail'], ['credits-total', 'credits-detail'], ['acc-credit-total', 'acc-credit-detail']].forEach(([t, d]) => {
    const te = document.getElementById(t), de = document.getElementById(d);
    if (te) te.textContent = total;
    if (de) de.textContent = detail;
  });
}
async function loadVpBalance() {
  const token = localStorage.getItem('tts_token');
  try {
    const res = await fetch('/api/credits/balance', { headers: token ? { 'Authorization': 'Bearer ' + token } : {} });
    const data = await res.json();
    if (data.ok) applyVpBalance(data);
  } catch (e) {}
}

function _vpRegion() {
  // Pays de l'utilisateur (fuseau horaire > langue) → région TikTok Shop à essayer en 1er.
  try {
    const TZ = {'Europe/Paris':'FR','Europe/Brussels':'BE','Europe/Luxembourg':'LU','Europe/Zurich':'CH',
      'Europe/London':'GB','Europe/Dublin':'IE','Europe/Madrid':'ES','Europe/Rome':'IT','Europe/Berlin':'DE',
      'Europe/Amsterdam':'NL','Europe/Lisbon':'PT','America/New_York':'US','America/Los_Angeles':'US',
      'America/Chicago':'US','America/Toronto':'CA','Asia/Bangkok':'TH','Asia/Ho_Chi_Minh':'VN',
      'Asia/Singapore':'SG','Asia/Kuala_Lumpur':'MY','Asia/Jakarta':'ID','Asia/Manila':'PH'};
    const tz = (Intl.DateTimeFormat().resolvedOptions().timeZone) || '';
    if (TZ[tz]) return TZ[tz];
    for (const l of (navigator.languages || [navigator.language || ''])) {
      const m = /[-_]([A-Za-z]{2})$/.exec(l || ''); if (m) return m[1].toUpperCase();
    }
    return {fr:'FR',en:'GB',de:'DE',es:'ES',it:'IT',nl:'NL',pt:'PT'}[(navigator.language||'').slice(0,2).toLowerCase()] || '';
  } catch (e) { return ''; }
}

async function generateVideoPrompt() {
  const out = document.getElementById('vp-result'), btn = document.getElementById('vp-generate');
  const token = localStorage.getItem('tts_token');
  // Champs obligatoires : lien TikTok Shop, image, nom, description.
  const vpUrl = _vpVal('vp-url');
  if (!vpUrl) { alert('⭐ Le lien du produit TikTok Shop est obligatoire'); document.getElementById('vp-url')?.focus(); return; }
  if (!/tiktok\.com|tiktokshop|vt\.tiktok|vm\.tiktok/i.test(vpUrl)) { alert('Colle un lien TikTok Shop valide (ex: https://www.tiktok.com/view/product/...)'); document.getElementById('vp-url')?.focus(); return; }
  if (!_vpImageB64) { alert('⭐ L\'image du produit est obligatoire'); document.getElementById('vp-drop')?.scrollIntoView({behavior:'smooth',block:'center'}); return; }
  if (!_vpVal('vp-name')) { alert('⭐ Le nom du produit est obligatoire'); document.getElementById('vp-name')?.focus(); return; }
  if (!_vpVal('vp-desc')) { alert('⭐ La description courte est obligatoire — elle guide l\'IA pour un prompt précis'); document.getElementById('vp-desc')?.focus(); return; }
  const oldHtml = btn.innerHTML;
  btn.disabled = true; btn.textContent = '⏳ Génération…';
  out.innerHTML = '<div style="text-align:center;padding:20px;color:var(--muted)">🎬 Génération du prompt vidéo…</div>';

  const fd = new FormData();
  fd.append('level', _vpLevel); fd.append('platform', _vpPlatform);
  if (_vpImageB64) fd.append('image', _vpImageB64);
  fd.append('product_url', vpUrl); fd.append('user_region', _vpRegion());
  fd.append('product_name', _vpVal('vp-name')); fd.append('description', _vpVal('vp-desc'));
  fd.append('price', _vpVal('vp-price')); fd.append('niche', _vpVal('vp-niche'));
  fd.append('visual_style', _vpStyle.visual_style || ''); fd.append('mood', _vpStyle.mood || '');
  fd.append('emotion_target', _vpStyle.emotion_target || ''); fd.append('color_tone', _vpStyle.color_tone || '');
  // Unicité : on transmet ce qui vient d'être généré pour interdire la répétition.
  if (_vpLast) {
    const av = [_vpLast.post_production_text?.hook, _vpLast.main_prompt, (_vpLast.variants || []).map(v => v.name).join(', ')]
      .filter(Boolean).join(' || ').slice(0, 700);
    if (av) fd.append('avoid', av);
  }

  try {
    const res = await fetch('/api/video-prompt/generate', { method: 'POST', headers: token ? { 'Authorization': 'Bearer ' + token } : {}, body: fd });
    if (res.status === 402) {
      const j = await res.json();
      out.innerHTML = `<div style="text-align:center;padding:18px;background:rgba(255,215,0,.10);border:1px dashed rgba(255,200,40,.6);border-radius:12px">
        <strong style="color:#d4a017">Crédits insuffisants</strong>
        <div style="font-size:13px;color:var(--muted);margin:6px 0 12px">Coût : ${j.cost} · Disponible : ${j.available}</div>
        <button class="btn btn-primary" onclick="switchTab('account')">Acheter des crédits 💳</button></div>`;
      return;
    }
    if (!res.ok) { let m = 'Erreur.'; try { m = (await res.json()).detail || m; } catch (e) {} out.innerHTML = `<div style="color:#DC2626;padding:12px">${escapeHtml(m)}</div>`; return; }

    const reader = res.body.getReader(), dec = new TextDecoder(); let buf = '';
    const handle = (ev, dstr) => {
      let o; try { o = JSON.parse(dstr); } catch (e) { return; }
      if (ev === 'complete') { renderVideoPromptResult(o.result); applyVpBalance(o.balance); }
      else if (ev === 'error') { out.innerHTML = `<div style="color:#DC2626;padding:12px">${escapeHtml(o.error || 'Erreur')}</div>`; }
    };
    const proc = (block) => { let ev = 'message'; const dl = []; for (const raw of block.split('\n')) { const l = raw.replace(/\r$/, ''); if (l.startsWith('event:')) ev = l.slice(6).trim(); else if (l.startsWith('data:')) dl.push(l.slice(5).trim()); } if (dl.length) handle(ev, dl.join('\n')); };
    while (true) { const { done, value } = await reader.read(); if (done) break; buf += dec.decode(value, { stream: true }); let i; while ((i = buf.indexOf('\n\n')) !== -1) { const b = buf.slice(0, i); buf = buf.slice(i + 2); if (b.trim()) proc(b); } }
    if (buf.trim()) proc(buf);
  } catch (e) { out.innerHTML = '<div style="color:#DC2626;padding:12px">Erreur réseau. Réessaie.</div>'; }
  finally { btn.disabled = false; btn.innerHTML = oldHtml; updateVpCost(); updateCreditIndicator(); }
}

let _vpCopyId = 0;
function _vpBlock(title, text, mono) {
  if (!text) return '';
  const id = 'vpc-' + (++_vpCopyId);
  return `<div style="margin-top:14px">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px">
      <div style="font-size:12px;font-weight:700;color:var(--text)">${escapeHtml(title)}</div>
      <button class="btn btn-secondary" style="font-size:11px;padding:3px 8px" onclick="_vpCopy('${id}',this)">Copier</button>
    </div>
    <div id="${id}" style="font-size:12px;line-height:1.5;background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:10px;white-space:pre-wrap;${mono ? 'font-family:ui-monospace,Menlo,monospace' : ''}">${escapeHtml(text)}</div>
  </div>`;
}
function _vpCopy(id, btn) {
  const el = document.getElementById(id); if (!el) return;
  navigator.clipboard.writeText(el.textContent || '').then(() => { const o = btn.textContent; btn.textContent = '✓ Copié'; setTimeout(() => btn.textContent = o, 1200); }).catch(() => {});
}

function renderVideoPromptResult(r) {
  const out = document.getElementById('vp-result'); if (!out || !r) return;
  _vpLast = r;   // mémorise pour interdire la répétition à la régénération
  const t = r.technical_settings || {}, pp = r.post_production_text || {}, mu = r.music_suggestions || {}, comp = r.tiktok_shop_compliance || {};
  let html = `<div class="section" style="border-left:4px solid var(--primary)">
    <h3 style="margin:0 0 2px">🎬 Ton prompt vidéo</h3>
    <div style="font-size:11px;color:var(--muted)">${escapeHtml((r.product_name || '') + '')} · ${escapeHtml((VP_PLATFORMS.find(p=>p.id===r.platform)?.label)||r.platform||'')} · niveau ${escapeHtml(String(r.level||''))}${r._fallback ? ' · <span style="color:#d4a017">exemple démo</span>' : ''}</div>`;

  html += _vpBlock('📝 Prompt principal', r.main_prompt, true);
  html += _vpBlock('🚫 Prompt négatif', r.negative_prompt, true);

  const tech = [t.resolution, t.frame_rate, t.duration, t.aspect_ratio].filter(Boolean).join(' · ');
  if (tech) html += `<div style="margin-top:12px;font-size:12px;color:var(--muted)">⚙️ ${escapeHtml(tech)}</div>`;

  // 🎬 Plan séquence (timeline 3s) suivant le tunnel de vente
  if (Array.isArray(r.timeline) && r.timeline.length) {
    const phaseColor = { 'Accroche': '#2563EB', 'Problème': '#DC2626', 'Probleme': '#DC2626', 'Solution': '#D97706', 'Produit': '#7C3AED', 'CTA': '#059669' };
    const fullPlanId = 'vptl-all-' + (++_vpCopyId);
    const fullPlan = r.timeline.map(s => [
      `${s.time || ''} — ${s.phase || ''}`.trim(),
      s.scene || '',
      s.camera ? 'Caméra : ' + s.camera : '',
      s.texte_ecran ? 'Texte à l\'écran : « ' + s.texte_ecran + ' »' : ''
    ].filter(Boolean).join('\n')).join('\n\n');
    html += `<div style="margin-top:16px;display:flex;justify-content:space-between;align-items:center;gap:8px">
        <div style="font-size:12px;font-weight:700">🎬 Plan séquence (Accroche → Problème → Solution → Produit → CTA)</div>
        <button class="btn btn-secondary" style="font-size:11px;padding:3px 8px;flex-shrink:0" onclick="_vpCopy('${fullPlanId}',this)">Copier tout</button>
      </div>
      <div id="${fullPlanId}" style="display:none">${escapeHtml(fullPlan)}</div>
      <div style="margin-top:8px;display:flex;flex-direction:column;gap:8px">`;
    r.timeline.forEach((s, idx) => {
      const col = phaseColor[s.phase] || 'var(--primary)';
      const sid = 'vptl-' + (++_vpCopyId);
      const copyText = [
        s.scene || '',
        s.camera ? 'Caméra : ' + s.camera : '',
        s.texte_ecran ? 'Texte à l\'écran : « ' + s.texte_ecran + ' »' : ''
      ].filter(Boolean).join('\n');
      html += `<div style="display:flex;gap:10px;background:var(--surface);border:1px solid var(--border);border-left:3px solid ${col};border-radius:8px;padding:8px 10px">
        <div style="flex-shrink:0;text-align:center;min-width:48px">
          <div style="font-size:11px;font-weight:800">${escapeHtml(s.time || '')}</div>
          <div style="font-size:9px;color:${col};font-weight:700;text-transform:uppercase">${escapeHtml(s.phase || '')}</div>
        </div>
        <div style="flex:1;min-width:0">
          <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:8px">
            <div style="font-size:12px;line-height:1.4">${escapeHtml(s.scene || '')}</div>
            <button class="btn btn-secondary" style="font-size:10px;padding:2px 7px;flex-shrink:0" onclick="_vpCopy('${sid}',this)">Copier</button>
          </div>
          <div style="font-size:10px;color:var(--muted);margin-top:3px">${s.camera ? '🎥 ' + escapeHtml(s.camera) : ''}${s.texte_ecran ? ' · 💬 « ' + escapeHtml(s.texte_ecran) + ' »' : ''}</div>
          <div id="${sid}" style="display:none">${escapeHtml(copyText)}</div>
        </div>
      </div>`;
    });
    html += `</div>`;
  }

  if (pp.hook || pp.middle || pp.cta) {
    html += `<div style="margin-top:14px;font-size:12px;font-weight:700">✍️ Textes à ajouter (post-prod)</div>`;
    html += _vpBlock('Hook (0-3s)', pp.hook, false);
    html += _vpBlock('Texte central', pp.middle, false);
    html += _vpBlock('CTA', pp.cta, false);
  }
  if (mu.type) html += `<div style="margin-top:12px;font-size:12px;color:var(--muted)">🎵 ${escapeHtml(mu.type)}${mu.tempo_bpm ? ' · ' + escapeHtml(mu.tempo_bpm) + ' BPM' : ''}</div>`;
  if (Array.isArray(comp.checks) && comp.checks.length) {
    html += `<div style="margin-top:12px;font-size:12px;font-weight:700">✅ Conformité TikTok Shop</div><ul style="font-size:12px;color:var(--muted);margin:4px 0;padding-left:18px">${comp.checks.map(c => `<li>${escapeHtml(c)}</li>`).join('')}</ul>`;
  }
  if (Array.isArray(r.export_steps) && r.export_steps.length) {
    html += `<div style="margin-top:12px;font-size:12px;font-weight:700">📦 Assemblage</div><ul style="font-size:12px;color:var(--muted);margin:4px 0;padding-left:18px">${r.export_steps.map(s => `<li>${escapeHtml(s)}</li>`).join('')}</ul>`;
  }
  if (Array.isArray(r.variants) && r.variants.length) {
    html += `<div style="margin-top:14px;font-size:12px;font-weight:700">🔀 Variantes</div>`;
    r.variants.forEach(v => { if (v && v.prompt && v.prompt !== '…') html += _vpBlock('▸ ' + (v.name || 'Variante'), v.prompt, true); });
  }
  if (Array.isArray(r.why_it_works) && r.why_it_works.length) {
    html += `<div style="margin-top:12px;font-size:12px;font-weight:700">💡 Pourquoi ça marche</div><ul style="font-size:12px;color:var(--muted);margin:4px 0;padding-left:18px">${r.why_it_works.map(s => `<li>${escapeHtml(s)}</li>`).join('')}</ul>`;
  }
  html += `<div style="margin-top:16px;text-align:center"><button class="btn btn-primary" onclick="generateVideoPrompt()" style="font-size:13px">🔄 Régénérer (nouvelle variante) ${escapeHtml('(' + _vpCost() + ' crédit' + (_vpCost() > 1 ? 's' : '') + ')')}</button></div>`;
  html += `</div>`;
  out.innerHTML = html;
}

// 💳 Onglet achat de crédits
async function initCreditsTab() {
  if (!window.__userInfo) { try { await (window.__userInfoPromise || fetchUserInfo()); } catch (e) {} }
  loadVpBalance();
  const token = localStorage.getItem('tts_token');
  try {
    const res = await fetch('/api/credits/packs', { headers: token ? { 'Authorization': 'Bearer ' + token } : {} });
    const data = await res.json();
    const box = document.getElementById('credits-packs');
    if (!box || !data.packs) return;
    box.innerHTML = Object.entries(data.packs).map(([k, p]) => `
      <div style="background:var(--surface);border:1px solid ${p.best ? '#D4AF37' : 'var(--border)'};border-radius:12px;padding:16px;text-align:center">
        ${p.best ? '<div style="font-size:11px;color:#D4AF37;font-weight:700">⭐ BEST VALUE</div>' : '<div style="height:15px"></div>'}
        <div style="font-size:15px;font-weight:800;margin-top:2px">${escapeHtml(p.label)}</div>
        <div style="font-size:13px;color:var(--muted)">${p.credits} crédits</div>
        <div style="font-size:22px;font-weight:800;margin:8px 0;color:var(--primary)">${p.price}€</div>
        <button class="btn btn-primary" style="width:100%;font-size:13px" onclick="buyCredits('${k}')">Acheter</button>
      </div>`).join('');
  } catch (e) {}
}
function buyCredits(pack) {
  showToast("💳 L'achat de crédits sera disponible très bientôt (paiement en cours d'activation).");
}

// ── 🔥 CRÉATEURS GAGNANTS (marché KeyAPI, Gold/Agency) ───────────────────────
function _cfmt(n) {
  n = Number(n) || 0;
  if (n >= 1e6) return (n / 1e6).toFixed(1).replace('.0', '') + 'M';
  if (n >= 1e3) return (n / 1e3).toFixed(1).replace('.0', '') + 'k';
  return String(Math.round(n));
}
// Les miniatures TikTok sont en .heic (non lues par Chrome) → on tente le .jpeg
function _ttImg(url) {
  if (!url) return url;
  return url.replace(/\.heic(\?|$)/i, '.jpeg$1');
}
// Proxy serveur pour contourner la protection hotlink/signature du CDN TikTok.
// (avatars, covers, images produits) → renvoie une URL servie par notre backend.
function _imgProxy(url) {
  if (!url) return '';
  return '/api/img-proxy?url=' + encodeURIComponent(_ttImg(url));
}
// Avatars créateurs : le host KeyAPI (echosell) est un bucket PRIVÉ (403). Les URLs
// ne sont pas affichables → on génère une pastille « initiale » colorée déterministe.
function _shuffle(arr) {
  const a = (arr || []).slice();
  for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; }
  return a;
}
function _avatarBadge(name, size) {
  const s = String(name || '?').trim().replace(/^@/, '');
  const init = (s[0] || '?').toUpperCase();
  let h = 0; for (let i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) & 0xffffff;
  const bg = `hsl(${h % 360} 52% 45%)`;
  const fs = Math.round(size * 0.42);
  return `<div style="width:${size}px;height:${size}px;border-radius:50%;flex-shrink:0;display:flex;align-items:center;justify-content:center;font-size:${fs}px;font-weight:800;color:#fff;background:${bg}">${escapeHtml(init)}</div>`;
}

/* ── RECHERCHE DE PROFIL TIKTOK (GMV réel 30j + meilleures ventes) ────────── */
function initRechercheTab() {
  const tier = (window.__userInfo?.tier || 'free').toLowerCase();
  const locked = document.getElementById('recherche-locked');
  const result = document.getElementById('recherche-result');
  const quotaLabel = document.getElementById('recherche-quota-label');
  if (!locked || !result) return;
  if (tier === 'free') {
    locked.style.display = 'block';
    result.style.display = 'none';
    quotaLabel.textContent = '';
    locked.innerHTML = `
      <div style="background:var(--surface2);border-radius:12px;padding:20px;text-align:center">
        <div style="font-size:14px;margin-bottom:12px">🔒 La recherche de profil est réservée aux plans <strong>Pro</strong> et plus.</div>
        <button class="btn btn-primary" onclick="switchTab('pricing')">Passer Pro 👑</button>
      </div>`;
  } else {
    locked.style.display = 'none';
    result.style.display = 'block';
  }
}

async function runRechercheSearch() {
  const tier = (window.__userInfo?.tier || 'free').toLowerCase();
  if (tier === 'free') { switchTab('pricing'); return; }

  const input = document.getElementById('recherche-handle');
  const handle = (input?.value || '').trim();
  if (!handle) { showToast('Entre un @pseudo.'); return; }

  const box = document.getElementById('recherche-result');
  box.innerHTML = '<div style="text-align:center;padding:24px;color:var(--muted)">⏳ Recherche…</div>';

  const token = localStorage.getItem('tts_token');
  const headers = token ? { 'Authorization': 'Bearer ' + token } : {};

  try {
    const res = await fetch(`/api/recherche/profile?handle=${encodeURIComponent(handle)}`, { headers });
    const data = await res.json().catch(() => ({}));

    if (res.status === 401) { switchTab('pricing'); return; }
    if (res.status === 403) {
      box.innerHTML = `<div style="background:var(--surface2);border-radius:12px;padding:20px;text-align:center">
        🔒 ${escapeHtml(data.detail || 'Réservé aux plans Pro et plus.')}
        <div style="margin-top:10px"><button class="btn btn-primary" onclick="switchTab('pricing')">Passer Pro 👑</button></div>
      </div>`;
      return;
    }
    if (res.status === 429) {
      box.innerHTML = `<div style="background:var(--surface2);border-radius:12px;padding:20px;text-align:center">
        ⏳ ${escapeHtml(data.detail || 'Quota de recherches atteint.')}
        <div style="margin-top:10px"><button class="btn btn-primary" onclick="switchTab('pricing')">Passer Gold 👑</button></div>
      </div>`;
      return;
    }
    if (!res.ok || !data.ok) {
      box.innerHTML = `<div style="color:#dc2626;padding:16px;text-align:center">❌ ${escapeHtml(data.error || 'Profil introuvable.')}</div>`;
      return;
    }

    renderRechercheResult(data);
    const quotaLabel = document.getElementById('recherche-quota-label');
    if (quotaLabel) {
      quotaLabel.textContent = (data.quota && data.quota.tier === 'pro')
        ? `${data.quota.remaining_today}/${data.quota.limit} recherches restantes aujourd'hui`
        : '';
    }
  } catch (e) {
    box.innerHTML = '<div style="color:#dc2626;padding:16px;text-align:center">❌ Erreur réseau.</div>';
  }
}

function renderRechercheResult(data) {
  const p = data.profile || {};
  const gmv = data.gmv || {};
  const products = data.best_sellers || [];
  const box = document.getElementById('recherche-result');

  const productsHtml = products.length
    ? products.map(pr => `
        <div style="display:flex;gap:10px;align-items:center;background:var(--surface2);border-radius:10px;padding:10px;width:100%;min-width:0;box-sizing:border-box">
          <img src="${pr.image || ''}" onerror="this.style.display='none'" style="width:44px;height:44px;border-radius:8px;object-fit:cover;flex-shrink:0">
          <div style="flex:1;min-width:0;overflow:hidden">
            <div style="font-size:13px;font-weight:600;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">${escapeHtml(pr.name || '')}</div>
            <div style="font-size:12px;color:var(--muted);overflow:hidden;text-overflow:ellipsis;white-space:nowrap">${(pr.sales || 0).toLocaleString()} ventes · $${(pr.gmv || 0).toLocaleString()} GMV total</div>
          </div>
        </div>`).join('')
    : '<p style="color:var(--muted);font-size:13px">Aucun produit vendu détecté.</p>';

  box.innerHTML = `
    <div style="display:flex;gap:14px;align-items:center;margin-bottom:18px;max-width:100%;box-sizing:border-box">
      <img src="${p.avatar || ''}" onerror="this.style.display='none'" style="width:64px;height:64px;border-radius:50%;object-fit:cover;background:var(--surface2);flex-shrink:0">
      <div style="flex:1;min-width:0;overflow:hidden">
        <div style="font-weight:800;font-size:17px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">${escapeHtml(p.nickname || p.unique_id || '')}</div>
        <div style="color:var(--muted);font-size:13px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">@${escapeHtml(p.unique_id || '')} · ${(p.followers || 0).toLocaleString()} abonnés</div>
      </div>
    </div>
    <div style="background:var(--surface2);border-radius:14px;padding:18px;text-align:center;margin-bottom:18px">
      <div style="font-size:12px;color:var(--muted)">GMV estimé (30 derniers jours)</div>
      <div style="font-size:32px;font-weight:900">$${(gmv.gmv_30d || 0).toLocaleString()}</div>
      <div style="font-size:12px;color:var(--muted)">${(gmv.sales_30d || 0).toLocaleString()} ventes sur la période</div>
    </div>
    <h3 style="font-size:15px;margin-bottom:10px">🏆 Meilleures ventes</h3>
    <div style="display:grid;grid-template-columns:1fr;gap:8px;width:100%;min-width:0">${productsHtml}</div>`;
}

/* ── FEED RADAR — feed de vidéos virales (thumbnail oEmbed, GMV estimé) ──── */
let _tiktokEmbedJsLoaded = false;

async function loadFeedRadarTab() {
  const grid = document.getElementById('feedradar-grid');
  const loading = document.getElementById('feedradar-loading');
  const upsell = document.getElementById('feedradar-upsell');
  if (!grid) return;
  grid.innerHTML = ''; upsell.style.display = 'none'; loading.style.display = 'block';

  const token = localStorage.getItem('tts_token');
  const headers = token ? { 'Authorization': 'Bearer ' + token } : {};

  try {
    const res = await fetch(`/api/feed-radar?region=${_userRegion()}`, { headers });
    const data = await res.json().catch(() => ({}));
    loading.style.display = 'none';

    if (!res.ok || !data.ok) {
      grid.innerHTML = `<p style="color:var(--muted);grid-column:1/-1">Feed Radar indisponible pour le moment. Réessaie plus tard.</p>`;
      return;
    }
    const videos = data.videos || [];
    if (!videos.length) {
      grid.innerHTML = '<p style="color:var(--muted);grid-column:1/-1">Aucune vidéo collectée pour le moment.</p>';
      return;
    }
    grid.innerHTML = videos.map(renderFeedRadarCard).join('');

    if (data.preview) {
      upsell.style.display = 'block';
      upsell.innerHTML = `
        <div style="background:var(--surface2);border-radius:12px;padding:18px;text-align:center">
          🔒 Accès complet au Feed Radar réservé aux plans <strong>Gold</strong> et <strong>Agency</strong>.
          <div style="margin-top:10px"><button class="btn btn-primary" onclick="switchTab('pricing')">Passer Gold 👑</button></div>
        </div>`;
    }
  } catch (e) {
    loading.style.display = 'none';
    grid.innerHTML = '<p style="color:#dc2626;grid-column:1/-1">❌ Erreur réseau.</p>';
  }
}

function renderFeedRadarCard(v) {
  const gmv = v.gmv_estimated || 0;
  return `
    <div class="feedradar-card" data-video-id="${v.video_id}" onclick="hydrateFeedRadarCard('${v.video_id}', this)"
         style="cursor:pointer;border-radius:12px;overflow:hidden;background:var(--surface2);position:relative">
      <img src="${v.oembed_thumbnail_url || ''}" onerror="this.style.display='none'" style="width:100%;aspect-ratio:9/16;object-fit:cover;display:block">
      <div style="padding:8px 10px">
        <div style="font-size:12px;font-weight:700;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">@${escapeHtml(v.creator_nickname || v.creator_unique_id || '')}</div>
        <div style="font-size:11px;color:var(--muted)">${(v.views || 0).toLocaleString()} vues</div>
        <div style="font-size:11px;color:var(--muted)">💰 GMV estimé : $${gmv.toLocaleString()}</div>
      </div>
    </div>`;
}

async function hydrateFeedRadarCard(videoId, cardEl) {
  // Tap-to-hydrate : embed.js n'est JAMAIS chargé au scroll, uniquement ici,
  // et une seule fois par page quel que soit le nombre de cartes tapées.
  const token = localStorage.getItem('tts_token');
  const headers = token ? { 'Authorization': 'Bearer ' + token } : {};
  try {
    const res = await fetch(`/api/feed-radar/${encodeURIComponent(videoId)}/embed`, { headers });
    const data = await res.json().catch(() => ({}));
    if (res.status === 403) { switchTab('pricing'); return; }
    if (!res.ok || !data.ok || !data.oembed_html) { showToast('Vidéo indisponible.'); return; }

    cardEl.innerHTML = data.oembed_html;
    if (!_tiktokEmbedJsLoaded) {
      const s = document.createElement('script');
      s.src = 'https://www.tiktok.com/embed.js';
      document.body.appendChild(s);
      _tiktokEmbedJsLoaded = true;
    }
  } catch (e) {
    showToast('Erreur réseau.');
  }
}

async function loadCreatorsTab() {
  const grid = document.getElementById('creators-grid');
  const loading = document.getElementById('creators-loading');
  const upsell = document.getElementById('creators-upsell');
  const detail = document.getElementById('creator-detail');
  if (!grid) return;
  if (detail) { detail.style.display = 'none'; detail.innerHTML = ''; }
  grid.innerHTML = ''; upsell.style.display = 'none'; loading.style.display = 'block';

  const token = localStorage.getItem('tts_token');
  const headers = token ? { 'Authorization': 'Bearer ' + token } : {};
  const cat = document.getElementById('creators-category')?.value || '';
  // Pays de l'utilisateur en premier, puis les principaux marchés (top 5 par pays).
  const countries = _orderedCountries().slice(0, 5);
  try {
    const results = await Promise.all(countries.map(c =>
      fetch(`/api/market/creators?region=${c.code}&category=${encodeURIComponent(cat)}`, { headers })
        .then(r => r.json()).catch(() => null)));
    loading.style.display = 'none';
    let html = ''; let any = false; let anyPreview = false;
    results.forEach((data, idx) => {
      const c = countries[idx];
      if (!data || !data.ok || !data.creators || !data.creators.length) return;
      any = true;
      const preview = data.preview;
      if (preview) anyPreview = true;
      // Affichage aléatoire : on mélange le top du pays puis on en montre 5 (variété).
      const cards = _shuffle(data.creators).slice(0, 5).map((cr, i) => renderCreatorCard(cr, preview && i >= 1)).join('');
      html += `<div style="grid-column:1/-1;margin-top:8px">
        <h3 style="font-size:14px;margin-bottom:10px">${c.flag} Top 5 — ${escapeHtml(c.name)}</h3>
        <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:12px">${cards}</div>
      </div>`;
    });
    if (!any) {
      grid.innerHTML = '<p style="color:var(--muted);grid-column:1/-1">Aucune donnée marché pour le moment. Réessaie plus tard.</p>';
      return;
    }
    grid.innerHTML = html;
    if (anyPreview) {
      upsell.style.display = 'block';
      upsell.innerHTML = `
        <div class="gold-upsell"><div class="gold-upsell-inner">
          <div class="gold-upsell-icon">🔒</div>
          <div class="gold-upsell-text"><strong>Passe au plan Gold</strong> pour voir tous les créateurs gagnants par pays, leurs vidéos et leurs produits.</div>
          <button class="gold-upsell-btn" onclick="switchTab('pricing')">Débloquer Gold 👑</button>
        </div></div>`;
    }
  } catch (e) {
    loading.style.display = 'none';
    grid.innerHTML = '<p style="color:var(--muted);grid-column:1/-1">Erreur de chargement.</p>';
  }
}

function renderCreatorCard(c, locked) {
  const blur = locked ? 'filter:blur(5px);pointer-events:none;user-select:none' : '';
  const onclick = locked ? '' : `onclick="openCreatorDetail('${encodeURIComponent(c.unique_id)}','${encodeURIComponent(c.user_id || '')}','${escapeHtml((c.nickname||'').replace(/'/g,''))}')"`;
  return `
    <div ${onclick} style="background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:12px;text-align:center;cursor:${locked?'default':'pointer'};${blur}">
      <div style="margin:0 auto 8px;width:64px">${_avatarBadge(c.nickname || c.unique_id, 64)}</div>
      <div style="font-weight:700;font-size:13px;color:var(--text);white-space:nowrap;overflow:hidden;text-overflow:ellipsis">${escapeHtml(c.nickname || '')}</div>
      <div style="font-size:11px;color:var(--muted)">@${escapeHtml(c.unique_id || '')}</div>
      <div style="display:flex;justify-content:center;gap:8px;flex-wrap:wrap;font-size:11px;color:var(--muted);margin-top:6px">
        <span>👥 ${_cfmt(c.followers)}</span>
        <span>📦 ${_cfmt(c.sales)}</span>
      </div>
      <div style="font-size:11px;color:#059669;font-weight:700;margin-top:2px">💰 $${_cfmt(c.gmv)} GMV</div>
    </div>`;
}

async function openCreatorDetail(uniqueIdEnc, userIdEnc, nickname) {
  const uniqueId = decodeURIComponent(uniqueIdEnc);
  const userId = decodeURIComponent(userIdEnc || '');
  const box = document.getElementById('creator-detail');
  if (!box) return;
  box.style.display = 'block';
  box.innerHTML = '<div class="section"><p style="color:var(--muted)">⏳ Chargement du créateur…</p></div>';
  box.scrollIntoView({ behavior: 'smooth', block: 'start' });
  const token = localStorage.getItem('tts_token');
  try {
    const res = await fetch(`/api/market/creator/${encodeURIComponent(uniqueId)}?user_id=${encodeURIComponent(userId)}`, {
      headers: token ? { 'Authorization': 'Bearer ' + token } : {}
    });
    const d = await res.json();
    if (!d.ok) { box.innerHTML = '<div class="section"><p style="color:var(--muted)">Accès réservé Gold/Agency.</p></div>'; return; }

    const profileUrl = 'https://www.tiktok.com/@' + encodeURIComponent(uniqueId);
    let html = `<div class="section">
      <div style="display:flex;justify-content:space-between;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:12px">
        <h2 style="margin:0">@${escapeHtml(uniqueId)}</h2>
        <a href="${profileUrl}" target="_blank" rel="noopener" class="btn btn-secondary" style="font-size:13px">Voir le profil ↗</a>
      </div>`;

    // Vidéos
    const vids = d.videos || [];
    html += `<div style="font-size:13px;font-weight:700;margin:6px 0 8px">📹 Ses vidéos</div>`;
    if (vids.length) {
      html += '<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(120px,1fr));gap:10px;margin-bottom:18px">';
      vids.forEach(v => {
        html += `<a href="${escapeHtml(v.url || profileUrl)}" target="_blank" rel="noopener" style="text-decoration:none;color:inherit">
          <div style="background:var(--surface);border:1px solid var(--border);border-radius:10px;overflow:hidden">
            ${v.cover ? `<img src="${escapeHtml(_imgProxy(v.cover))}" alt="" loading="lazy" referrerpolicy="no-referrer" onerror="this.style.display='none'" style="width:100%;aspect-ratio:9/16;object-fit:cover;background:#111">` : ''}
            <div style="padding:8px;font-size:11px;color:var(--muted);display:flex;flex-wrap:wrap;gap:6px">
              <span>👁 ${_cfmt(v.views)}</span><span>❤️ ${_cfmt(v.likes)}</span><span>💬 ${_cfmt(v.comments)}</span>
            </div>
          </div></a>`;
      });
      html += '</div>';
    } else {
      html += '<p style="font-size:12px;color:var(--muted);margin-bottom:18px">Aucune vidéo récupérée.</p>';
    }

    // Produits
    const prods = d.products || [];
    html += `<div style="font-size:13px;font-weight:700;margin:6px 0 8px">🛍️ Ce qu'il vend</div>`;
    if (prods.length) {
      html += '<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:10px">';
      prods.forEach(p => {
        html += `<a href="${escapeHtml(p.url || '#')}" target="_blank" rel="noopener" style="text-decoration:none;color:inherit">
          <div style="background:var(--surface);border:1px solid var(--border);border-radius:10px;overflow:hidden">
            ${p.image ? `<img src="${escapeHtml(_imgProxy(p.image))}" alt="" loading="lazy" referrerpolicy="no-referrer" onerror="this.style.display='none'" style="width:100%;height:120px;object-fit:cover">` : ''}
            <div style="padding:8px">
              <div style="font-size:11px;color:var(--text);line-height:1.3;max-height:2.6em;overflow:hidden">${escapeHtml(p.name || 'Produit')}</div>
              <div style="font-size:12px;color:var(--primary);font-weight:700;margin-top:4px">$${escapeHtml(String(p.price || '—'))}</div>
              <div style="font-size:11px;color:#059669">📦 ${_cfmt(p.sales)} ventes</div>
            </div>
          </div></a>`;
      });
      html += '</div>';
    } else {
      html += '<p style="font-size:12px;color:var(--muted)">Aucun produit récupéré.</p>';
    }
    html += '</div>';
    box.innerHTML = html;
    box.scrollIntoView({ behavior: 'smooth', block: 'start' });
  } catch (e) {
    box.innerHTML = '<div class="section"><p style="color:var(--muted)">Erreur de chargement du créateur.</p></div>';
  }
}

function escapeHtml(text) {
  const map = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' };
  return String(text == null ? '' : text).replace(/[&<>"']/g, m => map[m]);
}


// ════════════════════════════════════════════════════════════════════════════
// ANALYSE ASYNCHRONE (Pro+) — submit, ferme l'onglet, reviens voir le résultat
// ════════════════════════════════════════════════════════════════════════════
const _AUTH_HEADER = () => ({ 'Authorization': 'Bearer ' + (localStorage.getItem('tts_token') || '') });
let _jobsPollTimer = null;

// ── Lancement async d'une analyse par URL ────────────────────────────────
async function analyzeUrlAsync() {
  const input = document.getElementById('tiktok-url-single');
  const url = input ? input.value.trim() : '';
  if (!url) { showError('Colle un lien TikTok.'); return; }
  if (!/tiktok\.com|vt\.tiktok|vm\.tiktok/i.test(url)) { showError('Lien TikTok invalide.'); return; }

  const product = (document.getElementById('single-product')?.value || '').trim();
  const price = (document.getElementById('single-price')?.value || '').trim();
  if (!product) { showError('⭐ Indique le nom du produit (obligatoire pour le lien).'); return; }
  if (!price) { showError('⭐ Indique le prix (obligatoire pour le lien).'); return; }

  const submitBtn = document.querySelector('[data-async-submit]');
  if (submitBtn) submitBtn.disabled = true;
  try {
    const res = await fetch('/api/jobs/create-url', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', ..._AUTH_HEADER() },
      body: JSON.stringify({ url, product, price, user_role: getUserRole() }),
    });
    if (!res.ok) {
      const t = await res.text();
      throw new Error(t || ('HTTP ' + res.status));
    }
    const data = await res.json();
    showJobLaunchedModal(data.job_id);
  } catch (e) {
    showError('Lancement échoué : ' + (e.message || e));
  } finally {
    if (submitBtn) submitBtn.disabled = false;
  }
}

// ── Lancement async d'une analyse par upload ─────────────────────────────
async function analyzeUploadAsync() {
  if (!selectedFile) { showError('Choisis une vidéo.'); return; }
  const product = (document.getElementById('product-input')?.value || '').trim();
  const price = (document.getElementById('price-input')?.value || '').trim();

  const fd = new FormData();
  fd.append('video', selectedFile, selectedFile.name || 'video.mp4');
  if (product) fd.append('product', product);
  if (price) fd.append('price', price);
  fd.append('user_role', getUserRole());

  const submitBtn = document.querySelector('[data-async-upload]');
  if (submitBtn) submitBtn.disabled = true;
  try {
    const res = await fetch('/api/jobs/create-upload', {
      method: 'POST',
      headers: _AUTH_HEADER(),  // pas de Content-Type — FormData s'en charge
      body: fd,
    });
    if (!res.ok) {
      const t = await res.text();
      throw new Error(t || ('HTTP ' + res.status));
    }
    const data = await res.json();
    showJobLaunchedModal(data.job_id);
  } catch (e) {
    showError('Lancement échoué : ' + (e.message || e));
  } finally {
    if (submitBtn) submitBtn.disabled = false;
  }
}

// ── Modal "job lancé" : rassure l'utilisateur ────────────────────────────
function showJobLaunchedModal(jobId) {
  // Stocke le dernier job_id lancé pour pouvoir le retrouver facilement
  try { localStorage.setItem('tts_last_job_id', jobId); } catch (_) {}
  const html = `
    <div id="job-launched-overlay" style="position:fixed;inset:0;background:rgba(0,0,0,0.7);z-index:99999;display:flex;align-items:center;justify-content:center;padding:20px">
      <div style="background:#1a1a2e;color:#fff;border:1px solid rgba(212,175,55,0.4);border-radius:16px;padding:32px;max-width:480px;text-align:center">
        <div style="font-size:48px;margin-bottom:16px">✅</div>
        <h2 style="margin:0 0 12px;font-size:22px">Analyse lancée !</h2>
        <p style="margin:0 0 20px;line-height:1.6;color:rgba(255,255,255,0.85)">
          Tu peux <strong>fermer cet onglet</strong> ou continuer sur le site.<br>
          On t'avertit dès que c'est prêt dans <strong>Mes analyses</strong>.
        </p>
        <div style="display:flex;gap:10px;flex-wrap:wrap;justify-content:center">
          <button onclick="closeJobLaunchedModal();openMyAnalyses();" style="padding:12px 20px;background:#d4af37;color:#000;border:none;border-radius:10px;font-weight:700;cursor:pointer">📊 Voir Mes analyses</button>
          <button onclick="closeJobLaunchedModal()" style="padding:12px 20px;background:transparent;color:#fff;border:1px solid rgba(255,255,255,0.3);border-radius:10px;cursor:pointer">Continuer</button>
        </div>
      </div>
    </div>`;
  const div = document.createElement('div');
  div.innerHTML = html;
  document.body.appendChild(div.firstElementChild);
}

function closeJobLaunchedModal() {
  document.getElementById('job-launched-overlay')?.remove();
}

// ── Overlay "Mes analyses" : full-screen, sticky par-dessus tout l'UI ────
function openMyAnalyses() {
  // Si déjà ouvert, on rafraîchit juste
  let overlay = document.getElementById('my-analyses-overlay');
  if (overlay) {
    loadMyAnalyses();
    return;
  }
  overlay = document.createElement('div');
  overlay.id = 'my-analyses-overlay';
  overlay.style.cssText = 'position:fixed;inset:0;background:var(--bg,#0a0a0a);z-index:9998;overflow-y:auto;-webkit-overflow-scrolling:touch';
  overlay.innerHTML = `
    <div style="position:sticky;top:0;background:var(--surface);border-bottom:1px solid var(--border);padding:14px 16px;display:flex;align-items:center;justify-content:space-between;gap:10px;z-index:1">
      <h1 style="margin:0;font-size:18px;font-weight:700">📊 Mes analyses</h1>
      <button onclick="closeMyAnalyses()" type="button" style="padding:8px 14px;background:transparent;color:var(--text);border:1px solid var(--border);border-radius:8px;cursor:pointer;font-weight:600">← Retour</button>
    </div>
    <div style="padding:18px 16px;max-width:900px;margin:0 auto">
      <div id="my-analyses-list" style="min-height:120px">Chargement…</div>
    </div>`;
  document.body.appendChild(overlay);
  // Empêche le scroll du body sous l'overlay (iOS)
  document.body.style.overflow = 'hidden';
  loadMyAnalyses();
  startJobsPolling();
}

function closeMyAnalyses() {
  const overlay = document.getElementById('my-analyses-overlay');
  if (overlay) overlay.remove();
  document.body.style.overflow = '';
  stopJobsPolling();
}

async function loadMyAnalyses() {
  const container = document.getElementById('my-analyses-list');
  if (!container) return;
  try {
    const res = await fetch('/api/jobs?limit=30', { headers: _AUTH_HEADER() });
    if (!res.ok) throw new Error('HTTP ' + res.status);
    const data = await res.json();
    renderJobsList(data.jobs || []);
  } catch (e) {
    container.innerHTML = `<div style="padding:20px;border:1px solid var(--border);border-radius:10px;color:var(--muted)">Impossible de charger l'historique : ${escapeHtml(e.message || e)}</div>`;
  }
}

function renderJobsList(jobs) {
  const container = document.getElementById('my-analyses-list');
  if (!container) return;
  if (!jobs.length) {
    container.innerHTML = `<div style="padding:30px;text-align:center;color:var(--muted);border:1px dashed var(--border);border-radius:12px">Aucune analyse pour le moment.<br>Lance ta première vidéo depuis l'écran d'accueil.</div>`;
    return;
  }
  const statusBadge = (s) => {
    if (s === 'queued')  return '<span style="background:rgba(120,120,120,0.2);color:#aaa;padding:3px 10px;border-radius:999px;font-size:12px;font-weight:600">🕐 En file</span>';
    if (s === 'running') return '<span style="background:rgba(212,175,55,0.15);color:#d4af37;padding:3px 10px;border-radius:999px;font-size:12px;font-weight:600">⚙️ En cours</span>';
    if (s === 'done')    return '<span style="background:rgba(46,204,113,0.15);color:#2ecc71;padding:3px 10px;border-radius:999px;font-size:12px;font-weight:600">✅ Prête</span>';
    if (s === 'error')   return '<span style="background:rgba(231,76,60,0.15);color:#e74c3c;padding:3px 10px;border-radius:999px;font-size:12px;font-weight:600">❌ Erreur</span>';
    return '<span style="color:var(--muted)">' + escapeHtml(s) + '</span>';
  };
  const fmtDate = (s) => {
    if (!s) return '';
    try { return new Date(s).toLocaleString('fr-FR', { day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit' }); }
    catch (_) { return s; }
  };
  container.innerHTML = jobs.map(j => `
    <div style="border:1px solid var(--border);border-radius:12px;padding:14px 16px;margin-bottom:10px;background:var(--surface);display:flex;align-items:center;gap:14px;flex-wrap:wrap">
      <div style="flex:1;min-width:200px">
        <div style="font-weight:700;margin-bottom:4px">${escapeHtml(j.title || j.source_url || '(sans titre)')}</div>
        <div style="font-size:12px;color:var(--muted)">${escapeHtml(j.source || '')} · ${fmtDate(j.created_at)}${j.duration_ms ? ' · ' + Math.round(j.duration_ms/1000) + 's' : ''}</div>
        ${j.error_message ? `<div style="font-size:12px;color:#e74c3c;margin-top:4px">${escapeHtml(j.error_message)}</div>` : ''}
      </div>
      <div>${statusBadge(j.status)}</div>
      ${j.status === 'done' ? `<button onclick="openJobResult('${j.id}')" style="padding:8px 14px;background:#d4af37;color:#000;border:none;border-radius:8px;cursor:pointer;font-weight:700">Voir →</button>` : ''}
    </div>
  `).join('');
}

async function openJobResult(jobId) {
  try {
    const res = await fetch('/api/jobs/' + encodeURIComponent(jobId), { headers: _AUTH_HEADER() });
    if (!res.ok) throw new Error('HTTP ' + res.status);
    const job = await res.json();
    if (job.status !== 'done' || !job.result) {
      showError("Cette analyse n'est pas encore prête.");
      return;
    }
    closeMyAnalyses();
    // Bascule sur l'onglet Analyser, masque upload, montre les sections résultat
    try { switchTab('analyze'); } catch (_) {}
    const upSec = document.getElementById('upload-section');
    if (upSec) upSec.style.display = 'none';
    const loadSec = document.getElementById('loading-section');
    if (loadSec) loadSec.style.display = 'none';
    // Render via la fonction existante (même chemin que le flow sync)
    if (typeof showResults === 'function') {
      showResults(job.result);
      // Scroll vers le résultat
      setTimeout(() => {
        const target = document.getElementById('results-section');
        if (target && target.scrollIntoView) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }, 100);
    } else {
      const c = document.getElementById('analysis-container') || document.body;
      c.innerHTML = '<pre style="padding:20px;overflow:auto;font-size:12px">' + escapeHtml(JSON.stringify(job.result, null, 2)) + '</pre>';
    }
  } catch (e) {
    showError('Impossible de charger le résultat : ' + (e.message || e));
  }
}

function startJobsPolling() {
  stopJobsPolling();
  _jobsPollTimer = setInterval(() => {
    // Tant que l'overlay est dans le DOM, on continue de poller
    if (document.getElementById('my-analyses-overlay')) {
      loadMyAnalyses();
    } else {
      stopJobsPolling();
    }
  }, 5000);
}

function stopJobsPolling() {
  if (_jobsPollTimer) { clearInterval(_jobsPollTimer); _jobsPollTimer = null; }
}

// Expose globalement pour les onclick HTML
window.analyzeUrlAsync = analyzeUrlAsync;
window.analyzeUploadAsync = analyzeUploadAsync;
window.openMyAnalyses = openMyAnalyses;
window.closeMyAnalyses = closeMyAnalyses;
window.closeJobLaunchedModal = closeJobLaunchedModal;
window.openJobResult = openJobResult;

// ── Deep-link depuis le mail : /app?job=<id> ouvre directement le résultat ──
(function autoOpenJobFromUrl() {
  try {
    const params = new URLSearchParams(window.location.search);
    const jobId = params.get('job');
    if (!jobId) return;
    // Attend que SESSION + userInfo soient prêts (sinon openJobResult échoue
    // car le token n'est pas encore lu) — on poll toutes les 300ms, max 10s.
    let waited = 0;
    const tryOpen = () => {
      const tokenReady = !!localStorage.getItem('tts_token');
      const infoReady = !!window.__userInfo;
      if (tokenReady && infoReady) {
        // Nettoyer l'URL pour ne pas re-ouvrir au refresh
        try {
          const cleanUrl = window.location.pathname + window.location.hash;
          window.history.replaceState({}, '', cleanUrl);
        } catch (_) {}
        openJobResult(jobId);
        return;
      }
      waited += 300;
      if (waited >= 10000) return;  // abandonne après 10s (probable pas connecté)
      setTimeout(tryOpen, 300);
    };
    setTimeout(tryOpen, 500);  // léger délai initial pour laisser le boot s'amorcer
  } catch (_) {}
})();
