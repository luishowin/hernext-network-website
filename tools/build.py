"""Author-time page assembler for the HerNext Network site.

Stitches the shared head, header, optional closing call to action and footer
around a per-page body file, and generates the per-page canonical URL, social
tags and JSON-LD. Output is plain static HTML with no runtime dependency on
this script; it exists only so the pages cannot drift apart from one another.

BASE is the single place the live origin is defined. When the custom domain is
connected, change it here and rebuild, or run the sed command documented in the
README under "Adding the custom domain".
"""
import io, json, os

TOOLS = os.path.dirname(os.path.abspath(__file__))
PARTIALS = os.path.join(TOOLS, "partials")
ROOT = os.path.dirname(TOOLS)

# The single place the live origin is defined. Everything that needs an
# absolute URL reads it from here: canonicals, og:url, JSON-LD and the sitemap.
BASE = "https://luishowin.github.io/hernext-network-website/"

ORG = {
    "@type": "Organization",
    "@id": BASE + "#organisation",
    "name": "HerNext Network",
    "alternateName": "HNN",
    "url": BASE,
    "logo": BASE + "assets/images/logo-light.svg",
    "image": BASE + "assets/images/og-image.jpg",
    "slogan": "Creating Opportunity. Building Legacy.",
    "description": (
        "HerNext Network is a women-centred Pan-African institution advancing "
        "women's economic transformation through practical, evidence-driven "
        "interventions that expand access to markets, finance, skills, "
        "strategic partnerships and sustainable livelihood opportunities."
    ),
    "areaServed": {"@type": "Place", "name": "Africa"},
    "knowsAbout": [
        "Women's economic empowerment", "Enterprise and livelihood development",
        "Markets and trade", "Finance and investment",
        "Skills, leadership and enterprise capability",
        "Innovation, technology and sustainability",
        "Partnerships and economic ecosystems",
        "Monitoring, evaluation and impact measurement",
    ],
    "sameAs": ["https://www.instagram.com/hernextnetworkltd/"],
    "email": "info@hernextnetwork.com",
    "telephone": "+254780528551",
    "contactPoint": [
        {
            "@type": "ContactPoint",
            "contactType": "general enquiries",
            "email": "info@hernextnetwork.com",
            "telephone": "+254780528551",
            "availableLanguage": ["English"],
        },
        {
            "@type": "ContactPoint",
            "contactType": "programmes and partnerships",
            "email": "hernextnetwork@gmail.com",
            "telephone": "+254734806637",
            "availableLanguage": ["English"],
        },
    ],
}


# ---------------------------------------------------------------------------
# Navigation, single source of truth.
#
# The header nav (desktop dropdown + mobile menu), the footer Explore list
# and the sitemap all read from here, so adding a future programme or page
# means editing one list, not multiple templates.
#
# Programme destinations are temporary: no dedicated programme routes exist
# yet, so every programme points at our-work.html and carries a slug in
# data-programme for clean rewiring later. Do not invent programme pages.
# ---------------------------------------------------------------------------
PROGRAMMES = [
    {"title": "Women &amp; Enterprise Development",
     "href": "our-work.html", "slug": "women-enterprise-development"},
    {"title": "Youth Skills &amp; Employability",
     "href": "our-work.html", "slug": "youth-skills-employability"},
    {"title": "Skills, TVET &amp; Industry Partnerships",
     "href": "our-work.html", "slug": "skills-tvet-industry-partnerships"},
    {"title": "Agriculture &amp; Farmer Development",
     "href": "our-work.html", "slug": "agriculture-farmer-development"},
    {"title": "Animal Nutrition &amp; Feed Systems",
     "href": "our-work.html", "slug": "animal-nutrition-feed-systems"},
    {"title": "Trade &amp; Market Access",
     "href": "our-work.html", "slug": "trade-market-access"},
]

# Top-level nav in display order. "Our Programmes" links to the programmes
# overview section on Home until a dedicated landing route exists; its
# children come from PROGRAMMES above.
NAV = [
    {"title": "About", "href": "about.html"},
    {"title": "Our Work", "href": "our-work.html"},
    {"title": "Our Programmes", "href": "index.html#programmes",
     "children": PROGRAMMES},
    {"title": "Impact", "href": "impact.html"},
    {"title": "Partners", "href": "partners.html"},
    {"title": "Opportunities", "href": "our-work.html#current-opportunities"},
    {"title": "Resources", "href": "resources.html"},
    {"title": "Contact", "href": "contact.html"},
]

PARTNER_FORM = "contact.html?subject=partnership#contact-form"


def nav_html(active):
    """Render the primary nav from NAV, marking the current page."""
    parts = ['<nav class="nav" id="primary-nav" aria-label="Primary">']
    for item in NAV:
        children = item.get("children")
        if children:
            parts.append('      <div class="nav__item">')
            parts.append(
                '        <a class="nav__link" href="%s">%s</a>'
                % (item["href"], item["title"]))
            parts.append(
                '        <button class="nav__caret" type="button" '
                'aria-expanded="false" aria-controls="nav-programmes" '
                'aria-label="Show Our Programmes submenu"></button>')
            parts.append(
                '        <ul class="nav__dropdown" id="nav-programmes" '
                'aria-label="Our Programmes">')
            for child in children:
                # Children share a temporary destination, so they never take
                # aria-current; the top-level link carries it instead.
                parts.append(
                    '          <li><a class="nav__dropdown-link" href="%s" '
                    'data-programme="%s">%s</a></li>'
                    % (child["href"], child["slug"], child["title"]))
            parts.append('        </ul>')
            parts.append('      </div>')
        else:
            current = (' aria-current="page"'
                       if item["href"] == active else "")
            parts.append(
                '      <a class="nav__link" href="%s"%s>%s</a>'
                % (item["href"], current, item["title"]))
    parts.append('    </nav>')
    return "\n".join(parts)


def footer_nav_html(active):
    """Footer Explore list, same order and destinations as the header."""
    parts = []
    for item in NAV:
        current = (' aria-current="page"'
                   if item["href"] == active else "")
        parts.append(
            '          <li><a href="%s"%s>%s</a></li>'
            % (item["href"], current, item["title"]))
    return "\n".join(parts)


def jsonld(slug, title):
    """Organization plus WebSite on the home page, breadcrumbs elsewhere."""
    if slug in ("", "index.html"):
        graph = [ORG, {
            "@type": "WebSite",
            "@id": BASE + "#website",
            "url": BASE,
            "name": "HerNext Network",
            "inLanguage": "en-GB",
            "publisher": {"@id": BASE + "#organisation"},
        }]
    else:
        graph = [ORG, {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE},
                {"@type": "ListItem", "position": 2, "name": title,
                 "item": BASE + slug},
            ],
        }]
    body = json.dumps({"@context": "https://schema.org", "@graph": graph},
                      indent=2, ensure_ascii=False)
    return '\n<script type="application/ld+json">\n%s\n</script>' % body


def read(name):
    with io.open(os.path.join(PARTIALS, name), encoding="utf-8") as f:
        return f.read()


def build(out_path, body_file, active, title, desc, with_cta,
          slug=None, og_title=None, crumb=None, noindex=False):
    slug = slug if slug is not None else os.path.basename(out_path)
    canonical = BASE if slug in ("index.html", "") else BASE + slug

    head = read("_head.html")
    head = (head.replace("@@TITLE@@", title)
                .replace("@@OGTITLE@@", og_title or title)
                .replace("@@DESC@@", desc)
                .replace("@@CANONICAL@@", canonical)
                .replace("@@BASE@@", BASE)
                .replace("@@NAV@@", nav_html(active))
                .replace("@@JSONLD@@", "" if noindex else jsonld(slug, crumb or title)))

    if noindex:
        head = head.replace(
            '<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">',
            '<meta name="robots" content="noindex, follow">')

    parts = [head, read(body_file)]
    if with_cta:
        parts.append(read("_cta.html"))
    footer = read("_footer.html").replace("@@FOOTER_NAV@@",
                                          footer_nav_html(active))
    parts.append(footer)

    with io.open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write("".join(parts))
    print("built %-22s %6d bytes" % (os.path.basename(out_path),
                                     os.path.getsize(out_path)))


def redirect(out_path, target, title, note):
    """Write a stub at an address that has moved.

    GitHub Pages serves static files and cannot issue a 301, so the stub does
    the three things a redirect would: it tells crawlers where the content
    really lives, keeps itself out of the index, and moves the visitor along.
    The visible link is the fallback for anyone whose browser blocks refreshes.
    A target fragment is kept for the visitor but stripped from the canonical.
    """
    html = """<!DOCTYPE html>
<!-- Generated file. This address moved; see tools/make.py. -->
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(title)s</title>
<link rel="canonical" href="%(canonical)s">
<meta name="robots" content="noindex, follow">
<meta http-equiv="refresh" content="0; url=%(target)s">
<link rel="icon" href="assets/images/favicon.ico" sizes="32x32">
<link rel="stylesheet" href="css/style.css">
</head>
<body>
<main id="main">
  <section class="page-hero">
    <div class="container">
      <div class="stack">
        <p class="label">This page has moved</p>
        <h1 class="page-hero__title">%(title)s</h1>
        <p class="lead">%(note)s</p>
        <p><a class="btn btn--primary" href="%(target)s">Continue <span class="btn__arrow" aria-hidden="true">&#8599;</span></a></p>
      </div>
    </div>
  </section>
</main>
</body>
</html>
""" % {"title": title, "target": target, "note": note,
        "canonical": BASE + target.split("#")[0]}

    with io.open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    print("redirect %-22s -> %s" % (os.path.basename(out_path), target))
