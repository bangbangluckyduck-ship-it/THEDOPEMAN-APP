/* Lecteur officiel TikTok (Embed Player) à la place des miniatures.
 *
 * Depuis octobre 2026, l'oEmbed TikTok ne renvoie plus de thumbnail_url : toutes
 * les vignettes du Feed Radar retombaient sur l'image grise. TikTok recommande
 * son lecteur officiel (https://developers.tiktok.com/docs/en/embed-player) :
 * il affiche la couverture de la vidéo et se lit dans la carte.
 *
 * Usage : une boîte <div class="tt-lecteur" data-tt-player="<video_id>"> qui
 * contient son repli (image grise + bouton lecture). ttLecteurs.observer(conteneur)
 * charge le lecteur quand la boîte arrive à l'écran.
 *
 * Un lecteur est lourd : 18 chargés d'un coup figeaient la page (testé le
 * 28/10/2026 sur une grille de 24). D'où : au plus CHARGES_MAX chargements
 * simultanés, et un lecteur sorti de l'écran est déchargé (sauf s'il joue).
 *
 * Messages du lecteur (testés dans Chrome) : onPlayerError dès le chargement
 * pour une vidéo invalide → on remet le repli ; onStateChange 1 quand une vidéo
 * démarre → on met les autres en pause.
 */
(function () {
  var ORIGINE = 'https://www.tiktok.com';
  var PARAMS = 'autoplay=0&music_info=0&description=0&rel=0&native_context_menu=0&closed_caption=0';
  var CHARGES_MAX = 2;          // chargements simultanés
  var DELAI_CHARGE = 8000;      // libère la place même si « load » n'arrive pas
  var file = [];
  var enCours = 0;
  var observateur = null;

  function style() {
    if (document.getElementById('tt-lecteur-style')) return;
    var s = document.createElement('style');
    s.id = 'tt-lecteur-style';
    s.textContent =
      '.tt-lecteur{position:relative;width:100%;aspect-ratio:9/16;background:#000;overflow:hidden}' +
      '.tt-lecteur>iframe{position:absolute;inset:0;width:100%;height:100%;border:0;z-index:1}' +
      '.tt-lecteur>.tt-lecteur-repli{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}';
    document.head.appendChild(s);
  }

  function suivant() {
    while (enCours < CHARGES_MAX && file.length) {
      var boite = file.shift();
      // sortie de l'écran entre-temps, ou grille redessinée
      if (boite.dataset.ttEtat !== 'attente' || !boite.isConnected) continue;
      charger(boite);
    }
  }

  function charger(boite) {
    boite.dataset.ttEtat = 'charge';
    enCours++;
    var libere = false;
    var liberer = function () { if (libere) return; libere = true; enCours--; suivant(); };
    var f = document.createElement('iframe');
    f.src = ORIGINE + '/player/v1/' + encodeURIComponent(boite.dataset.ttPlayer) + '?' + PARAMS;
    f.title = boite.dataset.ttTitre || 'Vidéo TikTok';
    f.allow = 'encrypted-media; fullscreen; picture-in-picture';
    f.setAttribute('allowfullscreen', '');
    f.addEventListener('load', function () { setTimeout(liberer, 300); });
    setTimeout(liberer, DELAI_CHARGE);
    boite.appendChild(f);
  }

  function decharger(boite) {
    var f = boite.querySelector('iframe');
    if (f) f.remove();
    delete boite.dataset.ttEtat;
  }

  function boiteDe(source) {
    var cadres = document.querySelectorAll('.tt-lecteur > iframe');
    for (var i = 0; i < cadres.length; i++) {
      if (cadres[i].contentWindow === source) return cadres[i].parentNode;
    }
    return null;
  }

  function commande(boite, type) {
    var f = boite.querySelector('iframe');
    if (f && f.contentWindow) f.contentWindow.postMessage({ 'x-tiktok-player': true, type: type, value: null }, ORIGINE);
  }

  window.addEventListener('message', function (e) {
    if (e.origin !== ORIGINE) return;
    var d = e.data;
    if (typeof d === 'string') { try { d = JSON.parse(d); } catch (_) { return; } }
    if (!d || !d['x-tiktok-player']) return;
    var boite = boiteDe(e.source);
    if (!boite) return;
    if (d.type === 'onPlayerError') {
      // Vidéo supprimée, privée, ou lecteur limité par TikTok : on remet la carte d'avant.
      var f = boite.querySelector('iframe');
      if (f) f.remove();
      boite.dataset.ttEtat = 'echec';
    } else if (d.type === 'onStateChange' && d.value === 1) {
      boite.dataset.ttEtat = 'lecture';
      var autres = document.querySelectorAll('.tt-lecteur[data-tt-etat="lecture"]');
      for (var i = 0; i < autres.length; i++) {
        if (autres[i] !== boite) { commande(autres[i], 'pause'); autres[i].dataset.ttEtat = 'charge'; }
      }
    }
  });

  function surVisibilite(entrees) {
    entrees.forEach(function (en) {
      var boite = en.target;
      var etat = boite.dataset.ttEtat;
      if (en.isIntersecting) {
        if (!etat) { boite.dataset.ttEtat = 'attente'; file.push(boite); }
      } else if (etat === 'attente') {
        delete boite.dataset.ttEtat;
      } else if (etat === 'charge') {
        decharger(boite);          // hors écran : on rend la mémoire (une vidéo qui joue est gardée)
      }
    });
    suivant();
  }

  window.ttLecteurs = {
    observer: function (conteneur) {
      if (!conteneur) return;
      style();
      var boites = conteneur.querySelectorAll('.tt-lecteur[data-tt-player]');
      if (!('IntersectionObserver' in window)) return;   // le repli reste affiché
      if (!observateur) observateur = new IntersectionObserver(surVisibilite, { rootMargin: '150px 0px' });
      for (var j = 0; j < boites.length; j++) observateur.observe(boites[j]);
    }
  };
})();
