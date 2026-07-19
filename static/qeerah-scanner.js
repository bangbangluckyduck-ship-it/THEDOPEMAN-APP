/* ============================================================================
 * QeerahScanner — animation "scanner" pendant l'analyse d'une vidéo.
 *
 * Autonome : aucune dépendance, styles auto-injectés, couleurs héritées des
 * tokens du site (var(--accent), var(--primary)…). Se monte dans #loading-section
 * à la place du spinner texte, et rend la main au rapport réel (#results-section)
 * une fois la réponse serveur reçue.
 *
 * API :
 *   QeerahScanner.start()                 → monte + lance le balayage
 *   QeerahScanner.setThumbFromFile(file)  → miniature = 1re frame d'un fichier vidéo
 *   QeerahScanner.setThumbUrl(url)        → miniature depuis une URL (ex : /api/tt-thumb)
 *   QeerahScanner.setStatus(txt)          → reflète le texte de progression réel
 *   QeerahScanner.finish(score, done)     → clôture animée (compteur de score) puis done()
 *   QeerahScanner.stop()                  → arrêt propre (annule le rAF, nettoie)
 *   QeerahScanner.active                  → booléen
 *
 * Robustesse : un MutationObserver arrête le scanner dès que #loading-section
 * repasse en display:none (couvre TOUS les chemins d'erreur sans y toucher).
 * ==========================================================================*/
(function () {
  "use strict";

  var STYLE_ID = "qs-style";
  var CSS = [
    ".qs{--qs-mono:ui-monospace,'SF Mono','JetBrains Mono',Menlo,Consolas,monospace;",
    "--qs-scan:var(--primary,#D4AF37);--qs-pos:var(--success,#059669);--qs-warn:var(--danger,#EF4444);",
    "--qs-neu:var(--primary,#D4AF37);--qs-neu-ink:var(--primary-dk,#B8962E);--qs-prog:var(--navy,#1F3A70);",
    "--qs-text:var(--text,#1A1A1A);--qs-muted:var(--muted,#6B7280);--qs-border:var(--border,rgba(0,0,0,.08));",
    "--qs-scan-rgb:212,175,55;width:min(320px,84vw);margin:0 auto;}",
    ".qs-stage{position:relative;aspect-ratio:9/16;border-radius:18px;overflow:hidden;background:linear-gradient(160deg,#FFFFFF 0%,#FBF3DC 52%,#F1E3BE 100%);",
    "border:1px solid rgba(212,175,55,.35);box-shadow:0 12px 48px rgba(0,0,0,.12),inset 0 1px 24px rgba(212,175,55,.18);isolation:isolate;}",
    ".qs-thumb{position:absolute;inset:18px;border-radius:12px;object-fit:cover;filter:saturate(.95) contrast(1.02);box-shadow:0 6px 20px rgba(0,0,0,.22);",
    "opacity:0;transition:opacity .5s ease,filter .6s ease;}",
    ".qs-thumb.loaded{opacity:1;}",
    ".qs-veil{position:absolute;inset:18px;border-radius:12px;z-index:1;background:linear-gradient(180deg,rgba(12,17,22,.16),rgba(12,17,22,0) 26%,rgba(12,17,22,0) 74%,rgba(12,17,22,.24));}",
    ".qs-grid{position:absolute;inset:18px;border-radius:12px;overflow:hidden;z-index:2;pointer-events:none;background-image:",
    "linear-gradient(to right,rgba(var(--qs-scan-rgb),.13) 1px,transparent 1px),",
    "linear-gradient(to bottom,rgba(var(--qs-scan-rgb),.13) 1px,transparent 1px);background-size:20px 20px;",
    "opacity:0;transition:opacity .5s ease;}",
    ".qs-stage[data-phase='scanning'] .qs-grid{opacity:1;}",
    ".qs-scan{position:absolute;left:0;right:0;top:0;height:3px;z-index:4;background:var(--qs-scan);",
    "box-shadow:0 0 16px 2px rgba(var(--qs-scan-rgb),.9);will-change:transform;opacity:0;transition:opacity .5s ease;}",
    ".qs-stage[data-phase='scanning'] .qs-scan{opacity:1;}",
    ".qs-scan::before{content:'';position:absolute;left:0;right:0;bottom:3px;height:90px;",
    "background:linear-gradient(to top,rgba(var(--qs-scan-rgb),.36),rgba(var(--qs-scan-rgb),0));}",
    ".qs-scan[data-dir='up']::before{bottom:auto;top:3px;background:linear-gradient(to bottom,rgba(var(--qs-scan-rgb),.36),rgba(var(--qs-scan-rgb),0));}",
    ".qs-labels{position:absolute;left:0;right:0;top:15%;bottom:15%;z-index:3;pointer-events:none;display:flex;flex-direction:column;align-items:center;gap:8px;overflow:hidden;}",
    ".qs-label{font-family:var(--qs-mono);font-size:11.5px;font-weight:600;line-height:1;",
    "padding:4px 8px;border-radius:6px;white-space:nowrap;background:rgba(255,255,255,.94);border:1px solid;",
    "box-shadow:0 2px 8px rgba(0,0,0,.18);opacity:0;transform:translateY(4px);transition:opacity .35s ease,transform .35s ease;}",
    ".qs-label.in{opacity:1;transform:translateY(0);}.qs-label.out{opacity:0;transform:translateY(-4px);}",
    ".qs-label::before{content:'';display:inline-block;width:6px;height:6px;border-radius:50%;background:currentColor;margin-right:6px;vertical-align:middle;}",
    ".qs-label.pos{color:var(--qs-pos);border-color:rgba(5,150,105,.35);}",
    ".qs-label.warn{color:var(--qs-warn);border-color:rgba(239,68,68,.35);}",
    ".qs-label.neu{color:var(--qs-neu-ink);border-color:rgba(212,175,55,.45);}",
    ".qs-progress{position:absolute;top:12px;right:12px;z-index:5;display:inline-flex;align-items:center;gap:7px;",
    "font-family:var(--qs-mono);font-size:13px;font-weight:700;color:var(--qs-prog);font-variant-numeric:tabular-nums;",
    "padding:4px 10px;border-radius:999px;background:rgba(255,255,255,.94);box-shadow:0 2px 8px rgba(0,0,0,.18);",
    "opacity:0;transition:opacity .4s ease;}",
    ".qs-stage[data-phase='scanning'] .qs-progress{opacity:1;}",
    ".qs-progress::before{content:'';width:6px;height:6px;border-radius:50%;background:var(--qs-scan);animation:qs-pulse 1.1s ease-in-out infinite;}",
    "@keyframes qs-pulse{0%,100%{opacity:1;}50%{opacity:.2;}}",
    ".qs-status{position:absolute;left:12px;bottom:12px;z-index:5;font-family:var(--qs-mono);font-size:10.5px;",
    "letter-spacing:.04em;color:#fff;padding:3px 9px;border-radius:999px;background:rgba(12,17,22,.55);",
    "max-width:70%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;opacity:0;transition:opacity .4s ease;}",
    ".qs-stage[data-phase='scanning'] .qs-status{opacity:1;}",
    /* clôture : cercle de score doré */
    ".qs-finish{position:absolute;inset:0;z-index:6;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px;",
    "background:linear-gradient(160deg,rgba(255,255,255,.88),rgba(249,240,214,.88));backdrop-filter:blur(4px);opacity:0;transition:opacity .45s ease;}",
    ".qs-stage[data-phase='finish'] .qs-finish{opacity:1;}",
    ".qs-ring{position:relative;width:132px;height:132px;display:grid;place-items:center;animation:qs-pop .55s cubic-bezier(.22,1,.36,1) both;}",
    "@keyframes qs-pop{from{transform:scale(.84);opacity:0;}to{transform:scale(1);opacity:1;}}",
    ".qs-ring svg{position:absolute;inset:0;transform:rotate(-90deg);}",
    ".qs-ring .tk{stroke:rgba(212,175,55,.28);}",
    ".qs-ring .ar{stroke:var(--qs-neu);stroke-linecap:round;filter:drop-shadow(0 0 7px rgba(212,175,55,.55));}",
    ".qs-ring .qs-n{font-family:var(--qs-mono);font-size:38px;font-weight:700;color:var(--qs-neu-ink);font-variant-numeric:tabular-nums;line-height:1;text-shadow:0 1px 2px rgba(255,255,255,.6);}",
    ".qs-ring .qs-n span{font-size:16px;color:var(--qs-muted);}",
    ".qs-flabel{font-family:var(--qs-mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--qs-muted);}",
    /* fondu de sortie du scanner + révélation du rapport */
    ".qs.qs-bye{opacity:0;transform:translateY(-8px);transition:opacity .45s ease,transform .45s ease;}",
    "#results-section.qs-pending{opacity:0;}",
    "#results-section.qs-reveal{animation:qs-reveal .55s cubic-bezier(.22,1,.36,1) both;}",
    "@keyframes qs-reveal{from{opacity:0;transform:translateY(14px);}to{opacity:1;transform:translateY(0);}}",
    "@media (prefers-reduced-motion: reduce){.qs.qs-bye{transition:opacity .3s ease;transform:none;}",
    "#results-section.qs-reveal{animation-duration:.3s;}.qs-progress::before{animation:none;}}"
  ].join("");

  var FAKE_LABELS = [
    { t: "accroche 0-3s ✓", type: "pos" },
    { t: "rétention 41%", type: "warn" },
    { t: "CTA détecté", type: "neu" },
    { t: "prix affiché ✓", type: "pos" },
    { t: "démo produit ✓", type: "pos" },
    { t: "hook faible 2-4s", type: "warn" },
    { t: "preuve sociale", type: "neu" },
    { t: "sous-titres ✓", type: "pos" },
    { t: "silence 5-7s", type: "warn" },
    { t: "produit en main ✓", type: "pos" },
    { t: "lien bio détecté", type: "neu" },
    { t: "cut rythmé 1.1s", type: "pos" },
    { t: "pas d'urgence", type: "warn" },
    { t: "watermark détecté", type: "neu" }
  ];

  var reduced = false;
  try { reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches; } catch (e) {}

  function injectStyle() {
    if (document.getElementById(STYLE_ID)) return;
    var s = document.createElement("style");
    s.id = STYLE_ID;
    s.textContent = CSS;
    document.head.appendChild(s);
  }

  var QS = {
    active: false,
    _raf: null,
    _root: null,
    _stage: null,
    _observer: null,
    _finishing: false,

    start: function () {
      var host = document.getElementById("loading-section");
      if (!host) return;
      injectStyle();
      this.stop(true); // reset silencieux si un précédent traîne

      // masque le spinner texte historique le temps du scan
      this._hidden = [];
      var sp = document.getElementById("spinner-inline");
      var lt = document.getElementById("loading-text");
      [sp, lt].forEach(function (el) { if (el) { QS._hidden.push([el, el.style.display]); el.style.display = "none"; } });

      var root = document.createElement("div");
      root.className = "qs";
      root.id = "qs-live";
      root.innerHTML =
        '<div class="qs-stage" data-phase="scanning">' +
          '<img class="qs-thumb" alt="">' +
          '<div class="qs-veil"></div>' +
          '<div class="qs-grid"></div>' +
          '<div class="qs-labels"></div>' +
          '<div class="qs-scan" data-dir="down"></div>' +
          '<div class="qs-progress">0%</div>' +
          '<div class="qs-status"></div>' +
          '<div class="qs-finish"></div>' +
        "</div>";
      host.insertBefore(root, host.firstChild);

      this._root = root;
      this._stage = root.querySelector(".qs-stage");
      this._thumb = root.querySelector(".qs-thumb");
      this._scan = root.querySelector(".qs-scan");
      this._labelsBox = root.querySelector(".qs-labels");
      this._progressEl = root.querySelector(".qs-progress");
      this._statusEl = root.querySelector(".qs-status");
      this._finishEl = root.querySelector(".qs-finish");

      this.active = true;
      this._finishing = false;
      this._t0 = now();
      this._lastLabel = 0;
      this._labelIdx = 0;
      this._progress = 0;

      var self = this;
      this._raf = requestAnimationFrame(function (t) { self._loop(t); });

      // filet de sécurité : si loading-section se masque (erreur, reset…) → stop
      try {
        this._observer = new MutationObserver(function () {
          if (self._finishing) return;
          if (host.style.display === "none") self.stop();
        });
        this._observer.observe(host, { attributes: true, attributeFilter: ["style"] });
      } catch (e) {}
    },

    setThumbUrl: function (url) {
      if (!this._thumb || !url) return;
      var img = this._thumb;
      img.onload = function () { img.classList.add("loaded"); };
      img.onerror = function () { /* on garde le fond sombre, le scan continue */ };
      img.src = url;
    },

    setThumbFromFile: function (file) {
      if (!file) return;
      var self = this;
      try {
        var v = document.createElement("video");
        v.muted = true; v.playsInline = true; v.preload = "metadata";
        var url = URL.createObjectURL(file);
        v.src = url;
        v.onloadeddata = function () {
          try { v.currentTime = Math.min(0.1, (v.duration || 1) * 0.02); } catch (e) {}
        };
        v.onseeked = function () {
          try {
            var W = 360;
            var H = Math.round(W * v.videoHeight / Math.max(v.videoWidth, 1)) || 640;
            var c = document.createElement("canvas");
            c.width = W; c.height = H;
            c.getContext("2d").drawImage(v, 0, 0, W, H);
            self.setThumbUrl(c.toDataURL("image/jpeg", 0.82));
          } catch (e) {}
          try { URL.revokeObjectURL(url); } catch (e) {}
        };
      } catch (e) {}
    },

    setStatus: function (txt) {
      if (this._statusEl && txt) this._statusEl.textContent = String(txt).replace(/^[^\wÀ-ÿ]+/, "").trim();
    },

    _loop: function (t) {
      if (!this.active) return;
      var elapsed = t - this._t0;

      // 1) ligne de balayage — onde triangulaire haut→bas→haut
      var period = reduced ? 4200 : 2300;
      var cp = (elapsed % (period * 2)) / (period * 2);
      var y = cp < 0.5 ? cp * 2 : (1 - cp) * 2;
      var h = this._stage.clientHeight || 500;
      this._scan.style.transform = "translateY(" + (y * (h - 3)).toFixed(1) + "px)";
      this._scan.setAttribute("data-dir", cp < 0.5 ? "down" : "up");

      // 2) progression simulée — asymptote vers ~90%, ralentit en approchant
      if (!this._finishing) {
        this._progress = 90 * (1 - Math.exp(-elapsed / 6000));
        this._progressEl.textContent = Math.floor(this._progress) + "%";
      }

      // 3) étiquettes factices, une à une
      if (elapsed - this._lastLabel > 760) {
        this._lastLabel = elapsed;
        this._spawnLabel();
      }

      var self = this;
      this._raf = requestAnimationFrame(function (tt) { self._loop(tt); });
    },

    _spawnLabel: function () {
      var box = this._labelsBox;
      if (!box) return;
      var d = FAKE_LABELS[this._labelIdx % FAKE_LABELS.length];
      this._labelIdx++;
      var el = document.createElement("div");
      el.className = "qs-label " + d.type;
      el.textContent = d.t;
      box.appendChild(el);
      requestAnimationFrame(function () { el.classList.add("in"); });
      var all = box.querySelectorAll(".qs-label");
      if (all.length > 5) {
        var first = all[0];
        first.classList.add("out");
        setTimeout(function () { if (first.parentNode) first.remove(); }, 350);
      }
    },

    /* Clôture animée : compteur de score dans le cercle doré, puis done(). */
    finish: function (score, done) {
      if (!this.active) { if (typeof done === "function") done(); return; }
      this._finishing = true;
      var self = this;
      var s = parseInt(score, 10);
      if (isNaN(s)) s = null;

      // termine la progression jusqu'à 100
      this._progressEl.textContent = "100%";

      // efface les étiquettes
      if (this._labelsBox) {
        this._labelsBox.querySelectorAll(".qs-label").forEach(function (el) {
          el.classList.add("out");
          setTimeout(function () { if (el.parentNode) el.remove(); }, 350);
        });
      }

      var finishHold = 0;
      if (s !== null && this._finishEl) {
        // construit le cercle de score
        var R = 54, C = 2 * Math.PI * R;
        this._finishEl.innerHTML =
          '<div class="qs-ring">' +
            '<svg viewBox="0 0 128 128" width="128" height="128">' +
              '<circle class="tk" cx="64" cy="64" r="' + R + '" fill="none" stroke-width="6"></circle>' +
              '<circle class="ar" cx="64" cy="64" r="' + R + '" fill="none" stroke-width="6" stroke-dasharray="' + C.toFixed(1) + '" stroke-dashoffset="' + C.toFixed(1) + '"></circle>' +
            "</svg>" +
            '<div class="qs-n">0<span>/100</span></div>' +
          "</div>" +
          '<div class="qs-flabel">Note globale</div>';
        this._stage.setAttribute("data-phase", "finish");
        var arc = this._finishEl.querySelector(".ar");
        var num = this._finishEl.querySelector(".qs-n");
        this._countScore(num, arc, s, C);
        finishHold = reduced ? 600 : 1500;
      } else {
        this._stage.setAttribute("data-phase", "done");
        finishHold = 200;
      }

      // fondu de sortie du scanner puis remise de main
      setTimeout(function () {
        if (self._root) self._root.classList.add("qs-bye");
        setTimeout(function () {
          self.stop();
          if (typeof done === "function") done();
        }, reduced ? 300 : 460);
      }, finishHold);
    },

    _countScore: function (numEl, arcEl, target, C) {
      if (reduced) {
        numEl.innerHTML = target + "<span>/100</span>";
        arcEl.style.strokeDashoffset = (C * (1 - target / 100)).toFixed(1);
        return;
      }
      var start = now(), dur = 1100;
      function ease(x) { return 1 - Math.pow(1 - x, 3); }
      function tick() {
        var k = Math.min(1, (now() - start) / dur);
        var e = ease(k);
        numEl.innerHTML = Math.round(target * e) + "<span>/100</span>";
        arcEl.style.strokeDashoffset = (C * (1 - (target * e) / 100)).toFixed(1);
        if (k < 1) requestAnimationFrame(tick);
      }
      requestAnimationFrame(tick);
    },

    /* Arrêt propre : annule le rAF, retire le DOM, restaure le spinner. */
    stop: function (silent) {
      if (this._raf) { cancelAnimationFrame(this._raf); this._raf = null; }
      if (this._observer) { try { this._observer.disconnect(); } catch (e) {} this._observer = null; }
      if (this._root && this._root.parentNode) this._root.remove();
      this._root = this._stage = this._scan = this._labelsBox = this._progressEl = this._statusEl = this._finishEl = this._thumb = null;
      if (this._hidden) {
        this._hidden.forEach(function (pair) { if (pair[0]) pair[0].style.display = pair[1] || ""; });
        this._hidden = null;
      }
      this.active = false;
      this._finishing = false;
    }
  };

  function now() {
    return (window.performance && performance.now) ? performance.now() : Date.now();
  }

  window.QeerahScanner = QS;
})();
