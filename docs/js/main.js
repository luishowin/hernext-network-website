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

  /* ------------------------------------------------------------------ */

  function init() {
    initNav();
    initHeader();
    initReveal();
    initYear();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
