/* ==========================================================================
   HerNext Network, shared behaviour
   Mobile navigation, staggered scroll reveal, sticky header state, footer year.
   No dependencies, no build step.
   ========================================================================== */

(function () {
  "use strict";

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ------------------------------------------------------------------
     Mobile navigation
     ------------------------------------------------------------------ */

  function initNav() {
    var toggle = document.querySelector(".nav-toggle");
    var nav = document.getElementById("primary-nav");
    if (!toggle || !nav) return;

    function close() {
      nav.classList.remove("is-open");
      toggle.setAttribute("aria-expanded", "false");
      document.body.style.removeProperty("overflow");
    }

    function open() {
      nav.classList.add("is-open");
      toggle.setAttribute("aria-expanded", "true");
      document.body.style.overflow = "hidden";
    }

    toggle.addEventListener("click", function () {
      if (toggle.getAttribute("aria-expanded") === "true") close();
      else open();
    });

    // Close on link activation, on Escape, and when the layout returns to desktop.
    nav.addEventListener("click", function (e) {
      if (e.target.closest("a")) close();
    });

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && toggle.getAttribute("aria-expanded") === "true") {
        close();
        toggle.focus();
      }
    });

    window.matchMedia("(min-width: 901px)").addEventListener("change", function (e) {
      if (e.matches) close();
    });
  }

  /* ------------------------------------------------------------------
     Sticky header hairline, shown once the page has scrolled
     ------------------------------------------------------------------ */

  function initHeader() {
    var header = document.querySelector(".site-header");
    if (!header) return;

    var ticking = false;
    function update() {
      header.classList.toggle("is-scrolled", window.scrollY > 40);
      ticking = false;
    }

    window.addEventListener("scroll", function () {
      if (!ticking) {
        window.requestAnimationFrame(update);
        ticking = true;
      }
    }, { passive: true });

    update();
  }

  /* ------------------------------------------------------------------
     Staggered reveal on scroll

     Any element carrying [data-reveal] animates its direct children in
     sequence. The delay comes from a --i custom property, which is set
     here so the markup does not have to carry an index on every child.
     [data-reveal="self"] animates the element itself instead.
     ------------------------------------------------------------------ */

  function initReveal() {
    var pending = Array.prototype.slice.call(document.querySelectorAll("[data-reveal]"));
    if (!pending.length) return;

    function revealAll() {
      pending.forEach(function (g) {
        // is-settled goes on immediately here: nothing is animating, so the
        // compositor hint would only cost memory.
        g.classList.add("is-visible", "is-settled");
      });
      pending = [];
    }

    if (reduceMotion) { revealAll(); return; }

    // Stagger comes from --i on each direct child, so the markup does not
    // have to carry an index on every element.
    pending.forEach(function (group) {
      if (group.getAttribute("data-reveal") === "self") return;
      Array.prototype.forEach.call(group.children, function (child, i) {
        if (!child.style.getPropertyValue("--i")) {
          child.style.setProperty("--i", String(i));
        }
      });
    });

    // A direct geometry check rather than IntersectionObserver. It is
    // deterministic, runs identically in every browser, and cannot leave
    // content stuck at opacity 0 if the observer never reports.
    var ticking = false;

    // How long a group needs before its last child has finished animating.
    var styles = window.getComputedStyle(document.documentElement);
    var ms = function (name, fallback) {
      var v = parseFloat(styles.getPropertyValue(name));
      return isNaN(v) ? fallback : v;
    };
    var duration = ms("--reveal-duration", 1100);
    var stagger = ms("--reveal-stagger", 115);

    function settle(group) {
      var children = group.getAttribute("data-reveal") === "self" ? 1 : group.children.length;
      window.setTimeout(function () {
        group.classList.add("is-settled"); // drops the will-change hint
      }, duration + stagger * children + 100);
    }

    function check() {
      ticking = false;
      var trigger = window.innerHeight * 0.88;
      for (var i = pending.length - 1; i >= 0; i--) {
        if (pending[i].getBoundingClientRect().top < trigger) {
          pending[i].classList.add("is-visible"); // reveal once, never re-run
          settle(pending[i]);
          pending.splice(i, 1);
        }
      }
      if (!pending.length) {
        window.removeEventListener("scroll", request);
        window.removeEventListener("resize", request);
      }
    }

    function request() {
      if (ticking) return;
      ticking = true;
      window.requestAnimationFrame(check);
    }

    window.addEventListener("scroll", request, { passive: true });
    window.addEventListener("resize", request);
    check();

    // Last resort: never leave anything hidden, whatever else happens.
    window.setTimeout(function () { if (pending.length) check(); }, 1200);
  }

  /* ------------------------------------------------------------------
     Footer year
     ------------------------------------------------------------------ */

  function initYear() {
    var el = document.querySelector("[data-year]");
    if (el) el.textContent = String(new Date().getFullYear());
  }

  /* ------------------------------------------------------------------
     Hero video

     A decorative clip layered over the hero photograph. Everything here is
     about deciding NOT to play it. The element ships with no src and no
     autoplay attribute, so until this function attaches one the browser has
     asked for nothing, and the hero is the photograph it has always been.
     That is also what happens if this script never runs at all.
     ------------------------------------------------------------------ */

  var PAUSED_KEY = "hnn-hero-paused";

  function remembered(key) {
    // Private mode and blocked site data both throw rather than return null.
    try { return window.sessionStorage.getItem(key); } catch (e) { return null; }
  }

  function remember(key, value) {
    try { window.sessionStorage.setItem(key, value); } catch (e) { /* no matter */ }
  }

  function metered() {
    var conn = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
    if (!conn) return false;
    return !!conn.saveData || /(^|-)2g$/.test(conn.effectiveType || "");
  }

  function initHeroVideo() {
    var video = document.querySelector(".hero__video");
    if (!video) return;

    var figure = video.parentNode;
    var toggle = null;

    function drop() {
      if (video.parentNode) video.parentNode.removeChild(video);
      if (toggle && toggle.parentNode) toggle.parentNode.removeChild(toggle);
      toggle = null;
    }

    // The accessibility statement says that asking for reduced motion switches
    // all animation off. A paused video would still be a downloaded video, so
    // this declines before a single byte is requested.
    if (reduceMotion) { drop(); return; }

    // Nor should a decorative loop cost a megabyte on a metered connection.
    if (metered()) { drop(); return; }

    if (!video.canPlayType ||
        !video.canPlayType('video/mp4; codecs="avc1.42E01E"')) { drop(); return; }

    var narrow = window.matchMedia("(max-width: 700px)").matches;
    var src = video.getAttribute(narrow ? "data-src-narrow" : "data-src");
    if (!src) { drop(); return; }

    function label(paused) {
      toggle.setAttribute("data-paused", paused ? "true" : "false");
      toggle.querySelector(".visually-hidden").textContent =
        paused ? "Play background video" : "Pause background video";
    }

    function addToggle() {
      if (toggle) return;
      toggle = document.createElement("button");
      toggle.className = "hero__toggle";
      toggle.type = "button";
      toggle.innerHTML =
        '<svg class="hero__toggle-pause" viewBox="0 0 16 16" aria-hidden="true" focusable="false">' +
        '<rect x="3" y="2" width="3.5" height="12"></rect>' +
        '<rect x="9.5" y="2" width="3.5" height="12"></rect></svg>' +
        '<svg class="hero__toggle-play" viewBox="0 0 16 16" aria-hidden="true" focusable="false">' +
        '<path d="M4 2l10 6-10 6z"></path></svg>' +
        '<span class="visually-hidden"></span>';
      toggle.addEventListener("click", function () {
        if (video.paused) {
          start();
          remember(PAUSED_KEY, "");
        } else {
          video.pause();
          remember(PAUSED_KEY, "1");
        }
        label(video.paused);
      });
      figure.appendChild(toggle);
      label(video.paused);
    }

    function start() {
      if (!video.getAttribute("src")) video.src = src;
      var started = video.play();
      if (started && started.catch) {
        started.catch(function () {
          // Autoplay refused by a browser policy or a battery saver, or a play
          // that raced the load it was waiting on. Neither is fatal and neither
          // is worth working around: the photograph is untouched underneath,
          // and the control is left offering to start the clip. Real decode and
          // network failures arrive on the error event below, which does drop it.
          if (toggle) label(true);
        });
      }
    }

    video.addEventListener("error", drop);
    video.addEventListener("playing", function () {
      video.classList.add("is-playing");
    });

    // The control goes in as soon as the clip is known to be eligible, not
    // when it first plays. Someone who paused it on the last page needs a way
    // to start it again, and waiting for a play that will never happen would
    // leave them without one.
    addToggle();

    // A choice to stop it survives moving between pages in one visit, and
    // costs nothing while it stands: with preload="none" and no src, the
    // browser has not been asked for a single byte.
    if (remembered(PAUSED_KEY)) label(true);

    /* The clip runs only while the hero band is actually on screen.

       This is not an optimisation bolted on afterwards, it is what Chrome
       insists on. A muted video carries no audio track, and a video-only
       element that is scrolled out of view gets stopped with "background media
       was paused to save power". The hero band sits below the fold at load, so
       an unconditional play() on DOMContentLoaded is refused every time.

       Tying playback to visibility satisfies that, and is the right behaviour
       anyway: nothing decodes while nobody is looking at it. The geometry is
       measured directly rather than through IntersectionObserver, for the same
       reason initReveal does it that way. */
    function onScreen() {
      var box = figure.getBoundingClientRect();
      var height = window.innerHeight || document.documentElement.clientHeight;
      return box.bottom > 0 && box.top < height;
    }

    function sync() {
      if (!video.parentNode) return;
      if (remembered(PAUSED_KEY)) return;   // the visitor's choice outranks this
      if (document.hidden || !onScreen()) {
        if (!video.paused) video.pause();
      } else if (video.paused) {
        start();
      }
    }

    var ticking = false;
    function request() {
      if (ticking) return;
      ticking = true;
      window.requestAnimationFrame(function () { ticking = false; sync(); });
    }

    window.addEventListener("scroll", request, { passive: true });
    window.addEventListener("resize", request);
    document.addEventListener("visibilitychange", sync);
    sync();

    // Turning reduced motion on mid-visit has to take effect at once.
    window.matchMedia("(prefers-reduced-motion: reduce)")
      .addEventListener("change", function (e) {
        if (e.matches) { video.pause(); drop(); }
      });
  }

  /* ------------------------------------------------------------------ */

  function init() {
    initNav();
    initHeader();
    initReveal();
    initYear();
    initHeroVideo();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
