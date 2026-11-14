/* Asefa Family Gathering: shared language choice, header and footer.
   The language is chosen once on the home page and remembered on this device.
   Load in <head> with: <script src="assets/site.js" data-root="./" data-page="home"></script>
   (data-root is "../" for pages inside Games/). */
(function () {
  'use strict';
  var KEY = 'asefa-lang', LANGS = ['en', 'am', 'om'];
  var me = document.currentScript;
  var root = (me && me.dataset.root) || './';
  var page = (me && me.dataset.page) || '';

  var storageOK = (function () { try { localStorage.setItem('asefa-test', '1'); localStorage.removeItem('asefa-test'); return true; } catch (e) { return false; } })();
  function read() { try { var v = localStorage.getItem(KEY); return LANGS.indexOf(v) >= 0 ? v : null; } catch (e) { return null; } }
  function write(v) { try { localStorage.setItem(KEY, v); } catch (e) {} }

  var chosen = read();
  /* Not chosen yet and not on the home page: choose there first, then come back. */
  if (!chosen && page !== 'home' && storageOK) {
    location.replace(root + '?next=' + encodeURIComponent(location.pathname + location.search + location.hash));
    return;
  }
  var lang = chosen || 'en';
  function apply(v) { document.documentElement.setAttribute('data-lang', v); document.documentElement.lang = v; }
  apply(lang);

  var TXT = {
    brand: { en: 'Asefa Family Gathering', am: 'የአሰፋ ቤተሰብ ስብሰባ', om: 'Walgahii Maatii Asefaa' },
    home: { en: 'Home', am: 'መነሻ', om: 'Fuula jalqabaa' },
    constitution: { en: 'Constitution', am: 'መተዳደሪያ ደንብ', om: 'Seera ittiin bulmaataa' },
    meetups: { en: 'Meetups', am: 'ስብሰባዎች', om: 'Walgahiiwwan' },
    games: { en: 'Games', am: 'ጨዋታዎች', om: 'Taphoota' },
    motto: { en: 'Three generations, one table.', am: 'ሦስት ትውልድ፣ አንድ ማዕድ።', om: 'Dhaloota sadii, maaddii tokko.' },
    when: { en: 'Every three months, first Saturday', am: 'በየሦስት ወሩ፣ የመጀመሪያ ቅዳሜ', om: "Ji'a sadii sadiin, Sanbata jalqabaa" }
  };
  function tx(k) { return TXT[k][lang]; }
  var MARK = '<svg viewBox="0 0 40 40" aria-hidden="true"><circle cx="20" cy="17" r="14" fill="#f6c453"/><g fill="#3fa66b"><circle cx="11" cy="17" r="6"/><circle cx="20" cy="12" r="7.5"/><circle cx="29" cy="17" r="6"/><circle cx="15.5" cy="19" r="6"/><circle cx="24.5" cy="19" r="6"/></g><circle cx="16" cy="13" r="1.5" fill="#c4202f"/><circle cx="25" cy="16" r="1.5" fill="#b8296e"/><circle cx="20" cy="18" r="1.3" fill="#fff6e0"/><path d="M18.4 22h3.2v12h-3.2z" fill="#7a4a2a"/><path d="M8 34.5h24" stroke="#f6c453" stroke-width="2.2" stroke-linecap="round"/></svg>';

  function header() {
    var links = [['home', ''], ['constitution', 'constitution.html'], ['meetups', 'meetups.html'], ['games', 'Games/']];
    return '<div class="tibeb"></div><header class="site-head"><div class="wrap">' +
      '<a class="brand" href="' + root + '">' + MARK + '<span>' + tx('brand') + '</span></a>' +
      '<nav class="site-nav" aria-label="Site">' + links.map(function (l) {
        return '<a href="' + root + l[1] + '"' + (page === l[0] ? ' aria-current="page"' : '') + '>' + tx(l[0]) + '</a>';
      }).join('') + '</nav></div></header>';
  }
  function footer() {
    return '<footer class="site-foot"><div class="tibeb thin"></div><div class="wrap"><b>' + tx('brand') + '</b><span>' + tx('when') + '</span><span class="motto">' + tx('motto') + '</span></div></footer>';
  }

  window.ASEFA = {
    lang: lang, root: root, storageOK: storageOK, chosen: chosen,
    setLang: function (v) { if (LANGS.indexOf(v) < 0) return; write(v); lang = v; window.ASEFA.lang = v; window.ASEFA.chosen = v; apply(v); fill(); },
    t: function (o) { return o[lang] || o.en; }
  };

  function fill() {
    var h = document.getElementById('site-head'), f = document.getElementById('site-foot');
    if (h) h.innerHTML = header();
    if (f) f.innerHTML = footer();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', fill); else fill();
})();
