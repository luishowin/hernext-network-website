/* ==========================================================================
   HerNext Network, form behaviour

   Drives the one form on the site:
     #contact-form  the enquiry form, which also carries registrations of
                    interest through its subject field

   It submits to a Formspree endpoint declared on the form as data-endpoint.
   Replace REPLACE_ME with your form ID before launch.
   See the README section "Connect the form".
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
     Submission
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
        say("Your message could not be sent. Please try again, or email us directly at info@hernextnetwork.com.", "error");
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

  /* ------------------------------------------------------------------ */

  function init() {
    initContactForm();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
