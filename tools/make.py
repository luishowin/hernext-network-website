"""Rebuild every page in docs/ from the shared partials.

Run from anywhere:   python tools/make.py

The built pages in docs/ are outputs. Edit tools/partials/ instead, or your
change will be overwritten the next time this runs.
"""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build import build, redirect, ROOT

D = "docs/"
PAGES = [
 # out, body, nav-active, title, description, cta, crumb
 (D+"index.html", "_index_main.html", "",
  "HerNext Network | Creating Opportunity. Building Legacy.",
  "A Pan-African institution creating pathways of opportunity that advance women's economic transformation across Africa. Creating Opportunity. Building Legacy.",
  True, "Home", "Creating Opportunity. Building Legacy."),

 (D+"about.html", "_about.html", "about.html",
  "About Us | HerNext Network",
  "The story behind HerNext Network, our vision, mission and eight core values, and the Africa we are working to help build.",
  True, "About", "About HerNext Network"),

 (D+"our-work.html", "_our_work.html", "our-work.html",
  "Our Work | HerNext Network",
  "Six interconnected areas of work, the pathway from listening to scale, six signature initiatives in development and nine priority sectors across Africa.",
  True, "Our Work", "Our Work"),

 (D+"impact.html", "_impact.html", "impact.html",
  "Our Impact | HerNext Network",
  "What impact means to HerNext, the eight-step model from listening to scale, the Kiambu Chapter baseline work, and the indicators we measure against.",
  True, "Impact", "Our Impact"),

 (D+"partners.html", "_partners.html", "partners.html",
  "Partners and Collaboration | HerNext Network",
  "The eight kinds of partner we work with, the seven forms collaboration takes, how a HerNext partnership begins, and the five principles behind every one.",
  False, "Partners", "Partners and Collaboration"),

 (D+"contact.html", "_contact.html", "contact.html",
  "Contact Us | HerNext Network",
  "Register your interest, or contact HerNext Network about partnerships, market and trade connections, media requests and research collaboration.",
  False, "Contact", "Contact"),

 (D+"privacy.html", "_privacy.html", "",
  "Privacy Policy | HerNext Network",
  "How HerNext Network collects, uses, shares and protects the information you provide through this website.",
  False, "Privacy", "Privacy Policy"),

 (D+"terms.html", "_terms.html", "",
  "Terms of Use | HerNext Network",
  "The terms on which HerNext Network makes this website available, including the status of our programmes and our policy of never charging a fee.",
  False, "Terms", "Terms of Use"),

 (D+"accessibility.html", "_accessibility.html", "",
  "Accessibility Statement | HerNext Network",
  "What HerNext Network has done to make this website usable by everyone, the limitations we know about, and how to report a barrier.",
  False, "Accessibility", "Accessibility Statement"),
]

for out, body, active, title, desc, cta, og, crumb in PAGES:
    build(out, body, active, title, desc, cta, og_title=og, crumb=crumb)

# The 404 page is excluded from the index and carries no canonical value.
build(D+"404.html", "_404.html", "", "Page Not Found | HerNext Network",
      "The page you were looking for could not be found. Return to the HerNext Network home page.",
      False, og_title="Page not found", noindex=True)


# Addresses that have moved keep a stub, so a link already shared still lands
# on the right page rather than on the 404.
redirect(D+"opportunities.html", "our-work.html", "Opportunities is now Our Work",
         "This page was renamed. Everything that was here, and a good deal more, "
         "now lives on Our Work.")
redirect(D+"apply.html", "contact.html", "Registering your interest moved",
         "Registration now goes through the contact form. Choose "
         "\u201cRegister your interest\u201d as the subject and tell us what you are building.")


# The contact page carries the only form on the site and needs forms.js.
# Appending it here keeps the rebuild to a single command with no follow-up edit.
SCRIPT_TAG = '<script src="js/main.js" defer></script>'
FORMS_TAG = '<script src="js/forms.js" defer></script>'

path = os.path.join(ROOT, "docs", "contact.html")
html = io.open(path, encoding="utf-8").read()
if "forms.js" not in html:
    html = html.replace(SCRIPT_TAG, SCRIPT_TAG + chr(10) + FORMS_TAG)
    io.open(path, "w", encoding="utf-8", newline=chr(10)).write(html)
    print("wired forms.js into contact.html")
