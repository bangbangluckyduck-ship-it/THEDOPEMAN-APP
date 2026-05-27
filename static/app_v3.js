/**
 * TikTok Shop Analyzer - Frontend v3
 *
 * Progressive streaming analysis with cache support
 * Features:
 * - Server-Sent Events (SSE) for real-time analysis streaming
 * - Cache detection and optimized display
 * - Progressive section rendering with animations
 * - Error handling with reconnection logic
 * - Mobile-responsive design
 */

// ── STATE MANAGEMENT ──────────────────────────────────────────────────────────
const AppState = {
    currentLanguage: localStorage.getItem('language') || 'en',
    userTier: 'free',
    userEmail: null,
    isAnalyzing: false,
    analysisResults: null,
    currentTab: 'analyze',
    videoUrl: null,
};

// ── TRANSLATIONS ──────────────────────────────────────────────────────────────
const translations = {
    en: {
        analyzing: 'Analyzing...',
        cache_hit: 'Analysis found in cache ✨',
        analyzing_live: 'Analyzing in progress... 🔄',
        complete: 'Analysis complete ✅',
        error_occurred: 'An error occurred',
        connection_lost: 'Connection lost. Reconnecting...',
        reconnect_failed: 'Failed to reconnect. Please try again.',
        section_titles: {
            hook_type: 'Best Hook Type',
            retention_type: 'Retention Strategy',
            vente_points: 'Selling Points',
            positionnement: 'Positioning',
            format_visuel: 'Visual Format',
            emotion: 'Emotional Tone',
            conversion_strategy: 'Conversion Strategy',
            algorithme: 'Algorithm Boost',
            plan_reproduction: 'Implementation Plan',
            score_global: 'Overall Score',
        }
    },
    fr: {
        analyzing: 'Analyse en cours...',
        cache_hit: 'Analyse trouvée en cache ✨',
        analyzing_live: 'Analyse en direct... 🔄',
        complete: 'Analyse complète ✅',
        error_occurred: 'Une erreur est survenue',
        connection_lost: 'Connexion perdue. Reconnexion...',
        reconnect_failed: 'Impossible de se reconnecter. Veuillez réessayer.',
        section_titles: {
            hook_type: 'Meilleure accroche',
            retention_type: 'Stratégie de rétention',
            vente_points: 'Points de vente',
            positionnement: 'Positionnement produit',
            format_visuel: 'Format visuel optimal',
            emotion: 'Ton émotionnel',
            conversion_strategy: 'Stratégie de conversion',
            algorithme: 'Boost algorithme',
            plan_reproduction: 'Plan de reproduction',
            score_global: 'Score global',
        }
    }
};

// ── UTILITY FUNCTIONS ─────────────────────────────────────────────────────────
function t(key, category = null) {
    const lang = translations[AppState.currentLanguage] || translations.en;

    if (category === 'section_titles') {
        return lang.section_titles[key] || key;
    }

    return lang[key] || key;
}

function showLoader(message = null) {
    const loader = document.getElementById('analysis-loader');
    if (loader) {
        loader.innerHTML = `
            <div class="loader-content">
                <div class="spinner"></div>
                <p class="loader-text">${message || t('analyzing')}</p>
            </div>
        `;
        loader.style.display = 'flex';
    }
}

function hideLoader() {
    const loader = document.getElementById('analysis-loader');
    if (loader) {
        loader.style.display = 'none';
    }
}

function clearAnalysisDisplay() {
    const container = document.getElementById('analysis-container');
    if (container) {
        container.innerHTML = '';
    }
}

// ── ANALYSIS DISPLAY ──────────────────────────────────────────────────────────
function displayAnalysisSection(name, data) {
    const container = document.getElementById('analysis-container');
    if (!container) return;

    const sectionDiv = document.createElement('div');
    sectionDiv.className = 'analysis-section section-animation';
    sectionDiv.id = `section-${name}`;

    const title = t(name, 'section_titles');
    let content = '';

    if (typeof data === 'object') {
        content = `<div class="section-content">${formatAnalysisData(data)}</div>`;
    } else {
        content = `<div class="section-content"><p>${data}</p></div>`;
    }

    sectionDiv.innerHTML = `
        <div class="section-header">
            <h3>${title}</h3>
            <span class="section-icon">📊</span>
        </div>
        ${content}
    `;

    container.appendChild(sectionDiv);

    // Trigger animation
    setTimeout(() => {
        sectionDiv.classList.add('visible');
    }, 10);
}

function formatAnalysisData(data) {
    if (typeof data === 'string') {
        return `<p>${data}</p>`;
    }

    if (typeof data === 'number') {
        return `<p class="score-value">${data}</p>`;
    }

    if (Array.isArray(data)) {
        return `<ul>${data.map(item => `<li>${item}</li>`).join('')}</ul>`;
    }

    if (typeof data === 'object') {
        return `<pre>${JSON.stringify(data, null, 2)}</pre>`;
    }

    return '';
}

function displayAnalysisComplete(duration_ms, source) {
    const container = document.getElementById('analysis-container');
    if (!container) return;

    const completeDiv = document.createElement('div');
    completeDiv.className = 'analysis-complete section-animation';

    const sourceLabel = source === 'cache' ? '⚡ (from cache)' : '🔄 (live)';

    completeDiv.innerHTML = `
        <div class="complete-header">
            <h3>${t('complete')} ${sourceLabel}</h3>
            <span class="analysis-time">${duration_ms}ms</span>
        </div>
        <p class="complete-message">Ready to optimize your TikTok Shop! 🚀</p>
    `;

    container.appendChild(completeDiv);

    setTimeout(() => {
        completeDiv.classList.add('visible');
    }, 10);
}

// ── STREAMING ENDPOINT ────────────────────────────────────────────────────────
async function streamAnalysis(videoUrl, product = null) {
    if (AppState.isAnalyzing) {
        console.warn('Analysis already in progress');
        return;
    }

    AppState.isAnalyzing = true;
    AppState.videoUrl = videoUrl;

    clearAnalysisDisplay();
    showLoader(t('analyzing'));

    const params = new URLSearchParams({ video_url: videoUrl });
    if (product) {
        params.append('product', product);
    }

    const url = `/api/analyze/stream?${params}`;

    try {
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('userEmail') || 'anonymous'}`
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';
        let currentEvent = null;
        let eventData = null;

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            buffer += decoder.decode(value, { stream: true });

            // Process complete SSE messages (separated by \n\n)
            const messages = buffer.split('\n\n');

            // Keep last potentially incomplete message in buffer
            buffer = messages.pop() || '';

            for (const message of messages) {
                if (!message.trim()) continue;

                const lines = message.split('\n');
                let event = null;
                let data = null;

                for (const line of lines) {
                    if (line.startsWith('event:')) {
                        event = line.substring(6).trim();
                    } else if (line.startsWith('data:')) {
                        data = line.substring(5).trim();
                    }
                }

                if (event && data) {
                    try {
                        const parsedData = JSON.parse(data);

                        if (event === 'start') {
                            hideLoader();
                            showLoader(parsedData.message || t('analyzing'));
                        } else if (event === 'section') {
                            hideLoader();
                            displayAnalysisSection(parsedData.name, parsedData.data);
                        } else if (event === 'complete') {
                            hideLoader();
                            displayAnalysisComplete(parsedData.duration_ms || 0, parsedData.source || 'live');
                        } else if (event === 'error') {
                            hideLoader();
                            displayError(parsedData.error || parsedData.message || t('error_occurred'));
                        }
                    } catch (e) {
                        console.error(`Failed to parse ${event} event:`, e, data);
                    }
                }
            }
        }

    } catch (error) {
        console.error('Stream error:', error);
        displayError(`${t('error_occurred')}: ${error.message}`);
    } finally {
        AppState.isAnalyzing = false;
    }
}

// ── ERROR DISPLAY ─────────────────────────────────────────────────────────────
function displayError(message) {
    const container = document.getElementById('analysis-container');
    if (!container) return;

    const errorDiv = document.createElement('div');
    errorDiv.className = 'analysis-error section-animation visible';

    errorDiv.innerHTML = `
        <div class="error-header">
            <h3>⚠️ ${t('error_occurred')}</h3>
        </div>
        <p class="error-message">${message}</p>
    `;

    container.appendChild(errorDiv);
}

// ── TAB SWITCHING ─────────────────────────────────────────────────────────────
function switchTab(tabName) {
    // Hide all tab contents
    const tabContents = document.querySelectorAll('.tab-content');
    tabContents.forEach(tab => {
        tab.style.display = 'none';
    });

    // Remove active class from all buttons
    const tabButtons = document.querySelectorAll('.tab-button');
    tabButtons.forEach(btn => {
        btn.classList.remove('active');
    });

    // Show selected tab
    const selectedTab = document.getElementById(`tab-${tabName}-content`);
    if (selectedTab) {
        selectedTab.style.display = 'block';
    }

    // Add active class to clicked button
    const activeButton = document.querySelector(`[data-tab="${tabName}"]`);
    if (activeButton) {
        activeButton.classList.add('active');
    }

    AppState.currentTab = tabName;
}

// ── INITIALIZATION ────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', function() {
    console.log('App v3 initialized');

    // Get user info from storage
    const storedEmail = localStorage.getItem('userEmail');
    const storedTier = localStorage.getItem('userTier') || 'free';

    if (storedEmail) {
        AppState.userEmail = storedEmail;
        AppState.userTier = storedTier;
        updateUIForUser();
    }

    // Setup tab switches
    const tabButtons = document.querySelectorAll('.tab-button');
    tabButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const tabName = btn.getAttribute('data-tab');
            switchTab(tabName);
        });
    });

    // Setup analysis trigger
    const analyzeButton = document.getElementById('analyze-button');
    if (analyzeButton) {
        analyzeButton.addEventListener('click', handleAnalysisRequest);
    }

    // Default to analyze tab
    switchTab('analyze');
});

function updateUIForUser() {
    // Update user info display
    const userEmailEl = document.getElementById('user-email');
    const userTierEl = document.getElementById('user-tier');

    if (userEmailEl) {
        userEmailEl.textContent = AppState.userEmail;
    }

    if (userTierEl) {
        userTierEl.textContent = AppState.userTier.toUpperCase();
    }
}

function handleAnalysisRequest() {
    const videoUrlInput = document.getElementById('video-url-input');
    const videoUrl = videoUrlInput?.value?.trim();

    if (!videoUrl) {
        alert('Please enter a TikTok URL');
        return;
    }

    const productInput = document.getElementById('product-hint-input');
    const product = productInput?.value?.trim() || null;

    streamAnalysis(videoUrl, product);
}

// ── EXPORT FUNCTIONS ──────────────────────────────────────────────────────────
// Make functions globally available for HTML onclick handlers
window.streamAnalysis = streamAnalysis;
window.switchTab = switchTab;
window.handleAnalysisRequest = handleAnalysisRequest;
