"""Rebuild every page in docs/ from the shared partials.

Run from anywhere:   python tools/make.py

The built pages in docs/ are outputs. Edit tools/partials/ instead, or your
change will be overwritten the next time this runs.
"""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build import build, ROOT

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

 (D+"opportunities.html", "_opps.html", "opportunities.html",
  "Opportunities and Programmes | HerNext Network",
  "Nine strategic pillars, six signature initiatives and eleven priority sectors, from leadership and enterprise to trade, investment and innovation.",
  True, "Opportunities", "Opportunities and Programmes"),

 (D+"impact.html", "_impact.html", "impact.html",
  "Our Impact and Approach | HerNext Network",
  "The six barriers limiting women's economic participation in Africa, the five principles guiding our response, and the outcomes we measure.",
  True, "Impact", "Impact and Approach"),

 (D+"partners.html", "_partners.html", "partners.html",
  "Partners and Collaboration | HerNext Network",
  "The seven kinds of partner we work with, from governments to entrepreneurs, and the five principles behind every HerNext collaboration.",
  False, "Partners", "Partners and Collaboration"),

 (D+"apply.html", "_apply.html", "apply.html",
  "Register Your Interest | HerNext Network",
  "Tell us what you are building. A short four-step registration for women across Africa who want to hear from HerNext Network as programmes open.",
  False, "Register", "Register Your Interest"),

 (D+"contact.html", "_contact.html", "contact.html",
  "Contact Us | HerNext Network",
  "Contact HerNext Network about programmes, partnership enquiries, media requests and research collaboration.",
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


# Pages carrying a form also need forms.js. Appending it here keeps the
# rebuild to a single command with no follow-up edit.
SCRIPT_TAG = '<script src="js/main.js" defer></script>'
FORMS_TAG = '<script src="js/forms.js" defer></script>'

for page in ("contact.html", "apply.html"):
    path = os.path.join(ROOT, "docs", page)
    html = io.open(path, encoding="utf-8").read()
    if "forms.js" not in html:
        html = html.replace(SCRIPT_TAG, SCRIPT_TAG + chr(10) + FORMS_TAG)
        io.open(path, "w", encoding="utf-8", newline=chr(10)).write(html)
        print("wired forms.js into %s" % page)
