// === HerNext Network — Application JavaScript ===

// --- Mobile Navigation Toggle ---
document.addEventListener('DOMContentLoaded', function() {
  var toggle = document.getElementById('navToggle');
  var links = document.getElementById('navLinks');
  if (toggle && links) {
    toggle.addEventListener('click', function() {
      links.classList.toggle('open');
      toggle.textContent = links.classList.contains('open') ? '✕' : '☰';
    });
  }

  // Close nav when clicking a link on mobile
  var navAnchors = links ? links.querySelectorAll('a') : [];
  for (var i = 0; i < navAnchors.length; i++) {
    navAnchors[i].addEventListener('click', function() {
      links.classList.remove('open');
      if (toggle) toggle.textContent = '☰';
    });
  }
});

// --- Multi-Step Application Form ---

function showStep(stepNum) {
  // Hide all steps
  var steps = document.querySelectorAll('.form-step');
  for (var i = 0; i < steps.length; i++) {
    steps[i].classList.remove('active');
  }
  // Show target step
  var target = document.querySelector('.form-step[data-step="' + stepNum + '"]');
  if (target) target.classList.add('active');

  // Update step indicators
  var indicators = document.querySelectorAll('.form-step-indicator');
  var connectors = document.querySelectorAll('.form-step-connector');
  for (var j = 0; j < indicators.length; j++) {
    var s = parseInt(indicators[j].getAttribute('data-step'));
    indicators[j].classList.remove('active', 'done');
    if (s === stepNum) indicators[j].classList.add('active');
    if (s < stepNum) indicators[j].classList.add('done');
  }
  for (var k = 0; k < connectors.length; k++) {
    var c = parseInt(connectors[k].getAttribute('data-connector'));
    connectors[k].classList.remove('done');
    if (c < stepNum) connectors[k].classList.add('done');
  }

  // If showing step 4, populate review summary
  if (stepNum === 4) {
    populateReview();
  }

  // Scroll to top of form
  var formContainer = document.querySelector('.form-container');
  if (formContainer) formContainer.scrollIntoView({ behavior: 'smooth' });
}

function nextStep(step) {
  // Validate current step fields
  var currentStep = document.querySelector('.form-step.active');
  if (!currentStep) return;
  var currentNum = parseInt(currentStep.getAttribute('data-step'));
  var fields = currentStep.querySelectorAll('[required]');
  var valid = true;
  for (var i = 0; i < fields.length; i++) {
    if (!fields[i].value) {
      fields[i].style.borderColor = '#e74c3c';
      valid = false;
    } else {
      fields[i].style.borderColor = '';
    }
  }
  if (!valid) {
    alert('Please fill in all required fields before continuing.');
    return;
  }
  showStep(step);
}

function prevStep(step) {
  showStep(step);
}

function populateReview() {
  var summary = document.getElementById('reviewSummary');
  if (!summary) return;

  function val(id) { var el = document.getElementById(id); return el ? (el.value || '—') : '—'; }
  function label(id) { var el = document.getElementById(id); if (!el) return id; var lbl = el.parentElement.querySelector('label'); return lbl ? lbl.textContent.replace(' *', '') : id; }

  var items = [
    ['First Name', val('firstName')],
    ['Last Name', val('lastName')],
    ['Email', val('email')],
    ['Phone', val('phone')],
    ['Country', val('country')],
    ['Organisation', val('organisation')],
    ['Role', val('role')],
    ['Industry', val('industry')],
    ['Experience', val('experience')],
    ['Programme', val('programme')],
    ['Motivation', val('motivation').substring(0, 100) + (val('motivation').length > 100 ? '...' : '')],
    ['Contribution', val('contribution').substring(0, 100) + (val('contribution').length > 100 ? '...' : '')]
  ];

  var html = '';
  for (var i = 0; i < items.length; i++) {
    html += '<p style="margin-bottom:0.5rem;font-size:0.9rem;"><strong style="color:var(--text-primary);">' + items[i][0] + ':</strong> <span style="color:var(--text-secondary);">' + items[i][1] + '</span></p>';
  }
  summary.innerHTML = html;
}

function handleApplySubmit(event) {
  event.preventDefault();

  // Collect all form data
  var data = {
    firstName: document.getElementById('firstName') ? document.getElementById('firstName').value : '',
    lastName: document.getElementById('lastName') ? document.getElementById('lastName').value : '',
    email: document.getElementById('email') ? document.getElementById('email').value : '',
    phone: document.getElementById('phone') ? document.getElementById('phone').value : '',
    country: document.getElementById('country') ? document.getElementById('country').value : '',
    organisation: document.getElementById('organisation') ? document.getElementById('organisation').value : '',
    role: document.getElementById('role') ? document.getElementById('role').value : '',
    industry: document.getElementById('industry') ? document.getElementById('industry').value : '',
    experience: document.getElementById('experience') ? document.getElementById('experience').value : '',
    programme: document.getElementById('programme') ? document.getElementById('programme').value : '',
    motivation: document.getElementById('motivation') ? document.getElementById('motivation').value : '',
    contribution: document.getElementById('contribution') ? document.getElementById('contribution').value : '',
    referral: document.getElementById('referral') ? document.getElementById('referral').value : '',
    submittedAt: new Date().toISOString()
  };

  // In production, this would POST to a server endpoint
  console.log('Application submitted:', data);

  // Show success
  document.getElementById('applyForm').style.display = 'none';
  document.querySelector('.form-steps').style.display = 'none';
  var success = document.getElementById('successMessage');
  if (success) success.classList.add('show');

  // Scroll to success message
  success.scrollIntoView({ behavior: 'smooth' });
}

// --- Contact Form ---
function handleContactSubmit(event) {
  event.preventDefault();
  var form = document.getElementById('contactForm');
  var success = document.getElementById('contactSuccess');
  if (form) form.style.display = 'none';
  if (success) {
    success.style.display = 'block';
    success.scrollIntoView({ behavior: 'smooth' });
  }

  // In production, POST to server
  var contactData = {
    name: document.getElementById('contactName') ? document.getElementById('contactName').value : '',
    email: document.getElementById('contactEmail') ? document.getElementById('contactEmail').value : '',
    subject: document.getElementById('contactSubject') ? document.getElementById('contactSubject').value : '',
    message: document.getElementById('contactMessage') ? document.getElementById('contactMessage').value : '',
    submittedAt: new Date().toISOString()
  };
  console.log('Contact form submitted:', contactData);
}
