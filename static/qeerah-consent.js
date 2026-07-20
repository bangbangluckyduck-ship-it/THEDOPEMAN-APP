/* ============================================================================
 * QeerahConsent — consentement cookies conforme RGPD / ePrivacy.
 *
 * AVANT : le script Google Analytics était chargé en dur dans le <head> de
 * 20 pages, et les boutons « Accepter / Refuser » ne faisaient qu'écrire dans
 * localStorage. Refuser ne bloquait donc rien → consentement non effectif
 * (RGPD art. 4-11 et 7, directive ePrivacy art. 5-3).
 *
 * MAINTENANT : aucun traceur n'est chargé tant que l'utilisateur n'a pas
 * accepté. Le module :
 *   - ne charge Analytics QUE si le choix stocké vaut « accepted » ;
 *   - affiche un bandeau tant qu'aucun choix n'a été fait ;
 *   - réutilise le bandeau déjà présent dans la page (index.html, traduit)
 *     ou en injecte un identique sur les pages qui n'en ont pas ;
 *   - permet de RETIRER son consentement aussi facilement (revoke()), ce
 *     qu'exige l'art. 7-3 du RGPD.
 *
 * API : QeerahConsent.accept() / .reject() / .revoke() / .status()
 * ==========================================================================*/
(function () {
  "use strict";

  var GA_ID = "G-HR4QQJ52DT";
  var KEY   = "cookieConsent";

  function status() {
    try { return localStorage.getItem(KEY); } catch (e) { return null; }
  }
  function remember(v) {
    try { v ? localStorage.setItem(KEY, v) : localStorage.removeItem(KEY); } catch (e) {}
  }

  // File d'attente : un gtag() appelé avant consentement est mis en attente et
  // ne partira que si Analytics est réellement chargé plus tard.
  window.dataLayer = window.dataLayer || [];
  if (typeof window.gtag !== "function") {
    window.gtag = function () { window.dataLayer.push(arguments); };
  }

  function loadAnalytics() {
    if (window.__qsAnalyticsLoaded) return;
    window.__qsAnalyticsLoaded = true;
    var s = document.createElement("script");
    s.async = true;
    s.src = "https://www.googletagmanager.com/gtag/js?id=" + GA_ID;
    document.head.appendChild(s);
    window.gtag("js", new Date());
    window.gtag("config", GA_ID, { anonymize_ip: true });
  }

  // ── Bandeau ───────────────────────────────────────────────────────────────
  var STYLE_ID = "qs-consent-style";
  var CSS = [
    "#qs-consent{position:fixed;left:0;right:0;bottom:0;z-index:99998;",
    "background:var(--surface,#fff);border-top:1px solid var(--border,rgba(0,0,0,.10));",
    "box-shadow:0 -6px 30px rgba(0,0,0,.10);padding:16px 18px;",
    "font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;}",
    "#qs-consent .qs-c-in{max-width:900px;margin:0 auto;display:flex;gap:16px;align-items:center;",
    "justify-content:space-between;flex-wrap:wrap;}",
    "#qs-consent .qs-c-t{font-weight:700;font-size:15px;color:var(--text,#1A1A1A);margin-bottom:3px;}",
    "#qs-consent .qs-c-b{font-size:13px;color:var(--muted,#6B7280);line-height:1.5;max-width:560px;}",
    "#qs-consent .qs-c-b a{color:var(--navy,#1F3A70);}",
    "#qs-consent .qs-c-btns{display:flex;gap:9px;flex-wrap:wrap;}",
    "#qs-consent button{font-size:14px;font-weight:700;border-radius:10px;padding:11px 20px;",
    "cursor:pointer;border:1px solid transparent;min-height:44px;}",
    "#qs-consent .qs-c-ok{background:var(--primary,#D4AF37);color:#111;}",
    "#qs-consent .qs-c-no{background:transparent;color:var(--text,#1A1A1A);",
    "border-color:var(--border,rgba(0,0,0,.20));}",
    "#qs-consent button:focus-visible{outline:2px solid var(--navy,#1F3A70);outline-offset:2px;}",
    "@media(max-width:560px){#qs-consent .qs-c-in{flex-direction:column;align-items:stretch;}",
    "#qs-consent .qs-c-btns button{flex:1;}}"
  ].join("");

  function injectStyle() {
    if (document.getElementById(STYLE_ID)) return;
    var s = document.createElement("style");
    s.id = STYLE_ID; s.textContent = CSS;
    document.head.appendChild(s);
  }

  // Bandeau déjà présent dans la page (index.html : traduit via data-i18n)
  function existingBanner() { return document.getElementById("cookie-banner"); }

  function buildBanner() {
    injectStyle();
    var el = document.createElement("div");
    el.id = "qs-consent";
    el.setAttribute("role", "dialog");
    el.setAttribute("aria-label", "Consentement aux cookies");
    el.innerHTML =
      '<div class="qs-c-in">' +
        "<div>" +
          '<div class="qs-c-t">🍪 Cookies</div>' +
          '<div class="qs-c-b">On utilise des cookies de mesure d\'audience pour comprendre ce qui est utile. ' +
          'Rien n\'est déposé tant que tu n\'as pas accepté. ' +
          '<a href="/privacy">Politique de confidentialité</a></div>' +
        "</div>" +
        '<div class="qs-c-btns">' +
          '<button type="button" class="qs-c-no" id="qs-c-no">Refuser</button>' +
          '<button type="button" class="qs-c-ok" id="qs-c-ok">Accepter</button>' +
        "</div>" +
      "</div>";
    document.body.appendChild(el);
    el.querySelector("#qs-c-ok").addEventListener("click", accept);
    el.querySelector("#qs-c-no").addEventListener("click", reject);
    return el;
  }

  function showBanner() {
    var b = existingBanner();
    if (b) { b.style.display = ""; return; }          // laisse le CSS de la page gérer
    if (!document.getElementById("qs-consent")) {
      if (document.body) buildBanner();
      else document.addEventListener("DOMContentLoaded", buildBanner);
    }
  }

  function hideBanner() {
    var b = existingBanner();
    if (b) b.style.display = "none";
    var own = document.getElementById("qs-consent");
    if (own) own.remove();
  }

  // ── Actions ───────────────────────────────────────────────────────────────
  function accept() { remember("accepted"); hideBanner(); loadAnalytics(); }
  function reject() { remember("rejected"); hideBanner(); }   // aucun traceur chargé

  /** Retrait du consentement — aussi simple que de le donner (RGPD art. 7-3).
   *  Les cookies déjà posés par Analytics sont supprimés et la page rechargée
   *  pour repartir d'un état propre. */
  function revoke() {
    remember(null);
    try {
      document.cookie.split(";").forEach(function (c) {
        var name = c.split("=")[0].trim();
        if (/^_ga|^_gid|^_gat/.test(name)) {
          document.cookie = name + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/";
          document.cookie = name + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/;domain=." + location.hostname;
        }
      });
    } catch (e) {}
    location.reload();
  }

  // ── Démarrage ─────────────────────────────────────────────────────────────
  var choice = status();
  if (choice === "accepted") loadAnalytics();
  else if (choice !== "rejected") {
    if (document.readyState === "loading")
      document.addEventListener("DOMContentLoaded", showBanner);
    else showBanner();
  }

  window.QeerahConsent = {
    accept: accept, reject: reject, revoke: revoke,
    status: status, loadAnalytics: loadAnalytics
  };
  // Compat : les onclick historiques d'index.html continuent de fonctionner,
  // mais pilotent désormais réellement le chargement d'Analytics.
  window.acceptCookies = accept;
  window.rejectCookies = reject;
})();
