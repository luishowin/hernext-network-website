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
        "HerNext Network is a Pan-African institution creating pathways of "
        "opportunity that advance women's economic transformation through "
        "leadership, entrepreneurship, innovation, strategic partnerships and "
        "sustainable development."
    ),
    "areaServed": {"@type": "Place", "name": "Africa"},
    "knowsAbout": [
        "Women's economic empowerment", "Leadership development",
        "Entrepreneurship", "Trade and market access", "Investment promotion",
        "Innovation and technology", "Strategic partnerships",
        "Sustainable development in Africa",
    ],
    "sameAs": ["https://www.instagram.com/hernextnetworkltd/"],
    "contactPoint": {
        "@type": "ContactPoint",
        "contactType": "general enquiries",
        "email": "info@hernextnetwork.org",
        "availableLanguage": ["English"],
    },
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
