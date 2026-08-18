/* ==========================================================================
   HerNext Network, form behaviour

   Drives two forms with one set of rules:
     #contact-form  a single-step enquiry form
     #apply-form    a four-step application with a review screen

   Both submit to a Formspree endpoint declared on the form as
   data-endpoint. Replace REPLACE_ME with your form ID before launch.
   See the README section "Connect the forms".
   ========================================================================== */

(function () {
  "use strict";

  var EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
  var uid = 0;

  /* ------------------------------------------------------------------
     Field level helpers
     ------------------------------------------------------------------ */

  function fieldOf(el) {
    return el.closest ? el.closest(".field") : null;
  }

  function errorNode(el) {
    var field = fieldOf(el);
    return field ? field.querySelector(".field__error") : null;
  }

  function setError(el, message) {
    var field = fieldOf(el);
    var node = errorNode(el);
    if (field) field.classList.toggle("has-error", Boolean(message));
    if (!node) return;
    node.textContent = message || "";
    if (message) {
      if (!node.id) node.id = "err-" + (++uid);
      el.setAttribute("aria-invalid", "true");
      el.setAttribute("aria-describedby", node.id);
    } else {
      el.removeAttribute("aria-invalid");
      el.removeAttribute("aria-describedby");
    }
  }

  function labelFor(el) {
    var text = "";
    if (el.id) {
      var lab = document.querySelector('label[for="' + el.id + '"]');
      if (lab) text = lab.textContent;
    }
    if (!text) {
      var field = fieldOf(el);
      var own = field && field.querySelector(".field__label");
      if (own) text = own.textContent;
    }
    return text.replace("*", "").replace(/\s+/g, " ").trim();
  }

  /* Controls worth validating, with radio groups counted once. */
  function controlsIn(scope) {
    var seen = {};
    return Array.prototype.filter.call(
      scope.querySelectorAll("input, select, textarea"),
      function (el) {
        if (el.type === "hidden") return false;
        if (el.type === "radio") {
          if (seen[el.name]) return false;
          seen[el.name] = true;
        }
        return true;
      }
    );
  }

  function valueOf(el, form) {
    if (el.type === "radio") {
      var picked = form.querySelector('input[name="' + el.name + '"]:checked');
      return picked ? picked.value : "";
    }
    if (el.type === "checkbox") return el.checked ? "Yes" : "";
    return (el.value || "").trim();
  }

  function validate(el, form) {
    var value = valueOf(el, form);

    if (el.required && !value) {
      if (el.type === "radio") return "Please choose an option.";
      if (el.type === "checkbox") return "Please confirm to continue.";
      if (el.tagName === "SELECT") return "Please make a selection.";
      return "This field is required.";
    }
    if (el.type === "email" && value && !EMAIL.test(value)) {
      return "Please enter a valid email address.";
    }
    if (el.type === "url" && value && !/^https?:\/\//i.test(value)) {
      return "Please include https:// at the start of the link.";
    }
    if (el.type === "tel" && value && value.replace(/[^0-9]/g, "").length < 7) {
      return "Please enter a valid telephone number.";
    }
    return "";
  }

  function validateScope(scope, form) {
    var firstBad = null;
    controlsIn(scope).forEach(function (el) {
      var message = validate(el, form);
      setError(el, message);
      if (message && !firstBad) firstBad = el;
    });
    return firstBad;
  }

  /* ------------------------------------------------------------------
     Submission, shared by both forms
     ------------------------------------------------------------------ */

  function submit(form, onSuccess) {
    var endpoint = form.getAttribute("data-endpoint") || "";
    var status = form.querySelector(".form-status");
    var button = form.querySelector('[type="submit"]');

    function say(message, state) {
      if (!status) return;
      status.textContent = message;
      status.setAttribute("data-state", state || "");
    }

    if (endpoint.indexOf("REPLACE_ME") !== -1) {
      say("This form is not connected yet. Add your Formspree form ID to the data-endpoint attribute, as described in the README.", "error");
      return;
    }

    if (button) { button.disabled = true; }
    say("Sending, one moment.", "pending");

    fetch(endpoint, {
      method: "POST",
      body: new FormData(form),
      headers: { Accept: "application/json" }
    })
      .then(function (res) {
        if (!res.ok) throw new Error("Request failed with status " + res.status);
        say("", "");
        onSuccess();
      })
      .catch(function () {
        if (button) button.disabled = false;
        say("Your message could not be sent. Please try again, or email us directly at info@hernextnetwork.org.", "error");
      });
  }

  /* ------------------------------------------------------------------
     Contact form, single step
     ------------------------------------------------------------------ */

  function initContactForm() {
    var form = document.getElementById("contact-form");
    if (!form) return;

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var firstBad = validateScope(form, form);
      if (firstBad) { firstBad.focus(); return; }

      submit(form, function () {
        var status = form.querySelector(".form-status");
        form.reset();
        if (status) {
          status.textContent = "Thank you. Your enquiry has been sent, and we will respond shortly.";
          status.setAttribute("data-state", "success");
        }
      });
    });

    form.addEventListener("blur", function (e) {
      if (e.target.matches("input, select, textarea")) {
        setError(e.target, validate(e.target, form));
      }
    }, true);
  }

  /* ------------------------------------------------------------------
     Application form, four steps
     ------------------------------------------------------------------ */

  function initApplyForm() {
    var form = document.getElementById("apply-form");
    if (!form) return;

    var steps = Array.prototype.slice.call(form.querySelectorAll(".step"));
    var bars = Array.prototype.slice.call(form.querySelectorAll(".steps__bar"));
    var prevBtn = form.querySelector("[data-prev]");
    var nextBtn = form.querySelector("[data-next]");
    var submitBtn = form.querySelector("[data-submit]");
    var reviewBox = form.querySelector("[data-review]");
    var confirmation = document.querySelector("[data-confirmation]");
    var currentEl = form.querySelector("[data-step-current]");
    var totalEl = form.querySelector("[data-step-total]");
    var nameEl = form.querySelector("[data-step-name]");

    var index = 0;
    if (totalEl) totalEl.textContent = String(steps.length);

    function render() {
      steps.forEach(function (step, i) { step.hidden = i !== index; });
      bars.forEach(function (bar, i) { bar.classList.toggle("is-done", i <= index); });

      var last = index === steps.length - 1;
      if (prevBtn) prevBtn.hidden = index === 0;
      if (nextBtn) nextBtn.hidden = last;
      if (submitBtn) submitBtn.hidden = !last;

      if (currentEl) currentEl.textContent = String(index + 1);
      if (nameEl) nameEl.textContent = steps[index].getAttribute("data-step-label") || "";

      if (last) buildReview();
    }

    /* The review screen lists the answers from the earlier steps. The final
       step is skipped because its own fields sit directly above the review. */
    function buildReview() {
      if (!reviewBox) return;
      reviewBox.textContent = "";

      steps.slice(0, -1).forEach(function (step) {
        var rows = controlsIn(step).filter(function (el) {
          return el.type !== "checkbox";
        });
        if (!rows.length) return;

        var group = document.createElement("div");
        group.className = "review__group";

        var title = document.createElement("p");
        title.className = "review__group-title";
        title.textContent = step.getAttribute("data-step-label") || "";
        group.appendChild(title);

        rows.forEach(function (el) {
          var row = document.createElement("div");
          row.className = "review__row";

          var key = document.createElement("span");
          key.className = "review__key";
          key.textContent = labelFor(el);

          var val = document.createElement("span");
          val.className = "review__value";
          val.textContent = valueOf(el, form);

          row.appendChild(key);
          row.appendChild(val);
          group.appendChild(row);
        });

        reviewBox.appendChild(group);
      });
    }

    function goTo(next) {
      index = Math.max(0, Math.min(steps.length - 1, next));
      render();

      // Move focus to the new step heading so screen readers follow along,
      // and bring the top of the form into view.
      var legend = steps[index].querySelector(".step__legend");
      if (legend) {
        legend.setAttribute("tabindex", "-1");
        legend.focus({ preventScroll: true });
      }
      var top = form.getBoundingClientRect().top + window.scrollY - 120;
      window.scrollTo({
        top: top,
        behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth"
      });
    }

    if (nextBtn) nextBtn.addEventListener("click", function () {
      var firstBad = validateScope(steps[index], form);
      if (firstBad) { firstBad.focus(); return; }
      goTo(index + 1);
    });

    if (prevBtn) prevBtn.addEventListener("click", function () {
      goTo(index - 1); // answers are kept, nothing is cleared
    });

    form.addEventListener("blur", function (e) {
      if (e.target.matches("input, select, textarea")) {
        setError(e.target, validate(e.target, form));
      }
    }, true);

    // Enter should advance a step rather than submit an incomplete form.
    form.addEventListener("keydown", function (e) {
      if (e.key === "Enter" && e.target.tagName !== "TEXTAREA" && index < steps.length - 1) {
        e.preventDefault();
        if (nextBtn) nextBtn.click();
      }
    });

    form.addEventListener("submit", function (e) {
      e.preventDefault();

      // Validate every step, and jump back to the first one with a problem.
      for (var i = 0; i < steps.length; i++) {
        var firstBad = validateScope(steps[i], form);
        if (firstBad) {
          if (i !== index) goTo(i);
          firstBad.focus();
          return;
        }
      }

      submit(form, function () {
        form.hidden = true;
        if (confirmation) {
          confirmation.hidden = false;
          confirmation.setAttribute("tabindex", "-1");
          confirmation.focus({ preventScroll: true });
          confirmation.scrollIntoView({ block: "start", behavior: "smooth" });
        }
      });
    });

    render();
  }

  /* ------------------------------------------------------------------ */

  function init() {
    initContactForm();
    initApplyForm();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
