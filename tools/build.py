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
                .replace("@@JSONLD@@", "" if noindex else jsonld(slug, crumb or title)))

    if noindex:
        head = head.replace(
            '<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">',
            '<meta name="robots" content="noindex, follow">')

    if active:
        needle = 'class="nav__link" href="%s"' % active
        head = head.replace(needle, needle + ' aria-current="page"')

    parts = [head, read(body_file)]
    if with_cta:
        parts.append(read("_cta.html"))
    parts.append(read("_footer.html"))

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
    """
    html = """<!DOCTYPE html>
<!-- Generated file. This address moved; see tools/make.py. -->
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(title)s</title>
<link rel="canonical" href="%(base)s%(target)s">
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
""" % {"title": title, "target": target, "note": note, "base": BASE}

    with io.open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    print("redirect %-22s -> %s" % (os.path.basename(out_path), target))
