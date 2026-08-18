# HerNext Network

**Creating Opportunity. Building Legacy.**

The institutional website and online application platform for HerNext Network, a
Pan-African institution creating pathways of opportunity that advance women's
economic transformation through leadership, entrepreneurship, innovation,
strategic partnerships and sustainable development.

Plain HTML, CSS and JavaScript. No framework, no build step, no dependencies.
The contents of `docs/` are the deployed site exactly as written.

---

## Contents

- [Quick start](#quick-start)
- [Project structure](#project-structure)
- [Design system](#design-system)
- [Connect the forms](#connect-the-forms)
- [Images](#images)
- [SEO and crawling](#seo-and-crawling)
- [Legal pages](#legal-pages)
- [Editing the copy](#editing-the-copy)
- [Deploying to GitHub Pages](#deploying-to-github-pages)
- [Adding the custom domain](#adding-the-custom-domain)
- [Before launch](#before-launch)
- [Browser support and accessibility](#browser-support-and-accessibility)

---

## Quick start

There is nothing to install and nothing to compile. Serve the `docs/` folder
with any static server:

```bash
python -m http.server 8123 --directory docs
```

Then open `http://localhost:8123`.

Opening the HTML files directly from the file system also works, though the
fonts load from Google Fonts and therefore need a network connection.

---

## Project structure

```
docs/                      the published site, this is the deploy root
  index.html               Home
  about.html               About HerNext, story, foundation, values, vision
  opportunities.html       Strategic pillars, signature initiatives, sectors
  impact.html              Opportunity gap, approach, outcomes, SDG alignment
  partners.html            Partnership philosophy, partner types, principles
  apply.html               Four-step interest registration
  contact.html             Contact details and enquiry form
  privacy.html             Privacy policy
  terms.html               Terms of use
  accessibility.html       Accessibility statement
  404.html                 Not found, noindex
  robots.txt               permissive, points at the sitemap
  sitemap.xml              all ten indexable pages
  llms.txt                 structured summary for assistants and answer engines
  .nojekyll                tells GitHub Pages to serve the files as they are
  css/style.css            the entire design system, one file
  js/main.js               navigation, scroll reveal, header state, year
  js/forms.js              validation, the four-step flow, submission
  assets/images/           logos, favicon, image placeholders

CONTENT.md                 the copy deck, every line of text on the site
README.md                  this file
```

The source PDFs and the original logo folder sit at the repository root,
outside `docs/`, so they are never published with the site.

---

## Design system

Everything is driven by custom properties at the top of `docs/css/style.css`.
Change a token there and it updates across all seven pages.

### Colour

The palette was sampled from the brand logo. `HNN Logo Light Background.svg`
contains exactly four fills, and their usage frequency sets the hierarchy:
`#3e2557` appears 51 times, `#d4af37` 7 times, `#6b1fad` once, plus white.

| Token | Value | Role |
|---|---|---|
| `--white` | `#ffffff` | Page ground, cards, form fields |
| `--plum` | `#3e2557` | Core brand. Headings, dark bands |
| `--plum-deep` | `#2a1a3c` | Footer |
| `--plum-soft` | `#786190` | Meta text and captions |
| `--plum-tint` | `#f6f3f9` | Alternating section bands |
| `--gold` | `#d4af37` | Decorative only: rules, numerals, borders |
| `--gold-text` | `#806515` | Gold text on light grounds |
| `--violet` | `#6b1fad` | The logo sparkle accent, used sparingly |
| `--ink` | `#1c1420` | Body copy |

Colour is allocated on a 50:30:20 basis measured across a full page scroll:
50 per cent white, 30 per cent plum, 20 per cent gold.

Two rules worth keeping if you extend the site:

1. **`--gold` never carries text.** At `#d4af37` on white it measures 2.1:1,
   well under the WCAG minimum. Use `--gold-text` (`#806515`, 5.54:1) whenever
   gold needs to be readable. Gold on plum measures 6.25:1 and is safe, which
   is why gold text appears inside the dark bands.
2. **No gradients.** Flat fills and hairline rules only. The gradient inside
   the logo artwork itself is left untouched.

### Typography

Cormorant Garamond for display and headings, Inter for body, UI and labels,
both loaded from Google Fonts. The type scale is fluid, built on `clamp()`, so
sizes interpolate smoothly between mobile and desktop rather than jumping at
breakpoints.

Two recurring patterns:

- **Micro-label.** `<p class="label">Signature initiatives</p>` renders small,
  uppercase and letter-spaced, preceded by a short gold rule.
- **Emphasis word.** A single `<em>` inside a heading renders in Cormorant
  italic in gold, for example
  `<h2>Turning vision into <em>action</em></h2>`.

### Motion

Section content reveals on scroll in a stagger. Put `data-reveal` on any
container and its direct children animate in sequence; `main.js` assigns the
`--i` index, and the CSS turns that into a `transition-delay`. Use
`data-reveal="self"` to animate the element itself instead of its children.

Timing is set by three tokens: `--reveal-duration` at 1100ms,
`--reveal-stagger` at 115ms between siblings, and `--reveal-shift` at 32px of
travel. The curve is `--ease-reveal`, a near-exponential ease out that spends
most of its time decelerating, which is what makes the movement read as
unhurried rather than as a slide.

The reveal is driven by a direct geometry check rather than
`IntersectionObserver`, which keeps it deterministic across browsers. Two
safeguards mean content can never be left invisible:

- The hiding rules are scoped to `.js`, a class added by a one-line inline
  script in the document head. If scripting fails, nothing is ever hidden.
- `prefers-reduced-motion: reduce` disables all transitions, delays and smooth
  scrolling, and shows every section immediately.

---

## Connect the forms

**This is the one step required before launch.** GitHub Pages serves static
files and cannot receive a form submission, so both forms post to
[Formspree](https://formspree.io). Until you supply an ID they are inert, and
submitting shows a message saying so rather than failing silently.

1. Create a free Formspree account and add two forms, one for applications and
   one for general enquiries. Each gets an ID that looks like `xayzbqwe`.
2. Set the delivery address for each to the relevant HerNext inbox.
3. Replace `REPLACE_ME` in both files:

   | File | Attribute |
   |---|---|
   | `docs/apply.html` | `<form id="apply-form" data-endpoint="https://formspree.io/f/REPLACE_ME">` |
   | `docs/contact.html` | `<form id="contact-form" data-endpoint="https://formspree.io/f/REPLACE_ME">` |

4. Submit each form once from the live site. Formspree asks you to confirm the
   destination address the first time.

Submissions arrive by email and are listed in the Formspree dashboard, where
they can be exported. The free tier allows 50 submissions per month across all
forms, so consider a paid plan before an application round opens.

Field names are already human-readable, so an application arrives as
`Full name`, `Email`, `Sector`, `Initiative` and so on rather than as terse
input names.

### Using something else

`forms.js` performs a single `fetch` POST with a `FormData` body and an
`Accept: application/json` header, and treats any `response.ok` as success.
Any endpoint meeting that contract works without further changes: Getform,
Basin, Netlify Forms or your own handler. Only the `data-endpoint` value needs
to change.

---

## Images

Photographs are served as WebP at three widths each, chosen by the browser
through `srcset`. On a 375 pixel phone at 2x the hero loads the 1000 wide file
at 75 KB rather than the 1600 wide file at 164 KB.

| Slot | Files | Page |
|---|---|---|
| Hero, full bleed | `hnn-presentation-{700,1000,1600}.webp` | Home |
| Our story | `hnn-office-{600,900,1400}.webp` | About |
| Social preview | `og-image.jpg`, 1200 x 630 | all pages |

The untouched PNG originals are in `source-images/` at the repository root,
which is gitignored. They stay out of `docs/` so a 2 MB file can never be
served to a visitor by accident.

### Adding a new photograph

```bash
python - <<'PY'
from PIL import Image
im = Image.open("source-images/your-photo.png").convert("RGB")
for w in (1600, 1000, 700):
    h = round(im.height * w / im.width)
    im.resize((w, h), Image.LANCZOS).save(
        f"docs/assets/images/your-photo-{w}.webp", "WEBP", quality=82, method=6)
PY
```

Then reference all three in one `<img>`, and keep `width` and `height` on the
tag so the page does not shift as it loads:

```html
<img src="assets/images/your-photo-1600.webp"
     srcset="assets/images/your-photo-700.webp 700w,
             assets/images/your-photo-1000.webp 1000w,
             assets/images/your-photo-1600.webp 1600w"
     sizes="100vw" alt="Describe what is happening in the photograph"
     width="1600" height="900" decoding="async">
```

Use `sizes="100vw"` for full width images and `sizes="(max-width: 900px) 100vw, 45vw"`
for one sitting in a two column split.

### Remaining placeholders

Seven flat SVG placeholders are still in use, each labelled with its slot and
recommended size: three initiative cards, the partners banner, the impact
section, the contact page and the closing call to action. Replace the file,
keep the name, and no markup changes.

### Assets you are replacing

| File | Note |
|---|---|
| `logo-mark.svg`, `logo-light.svg`, `logo-dark.svg` | Derived from the supplied SVG. Regenerate all three when the redrawn logo lands |
| `favicon.svg` | Currently the emblem cropped from the same source |
| `og-image.jpg` | Interim, cropped from the presentation photograph |
| `apple-touch-icon.png` | Not present. Add a 180 x 180 PNG, then uncomment the line in the `<head>` |

---

## SEO and crawling

Every page carries a unique title under 60 characters, a description under 160,
a canonical URL, Open Graph and Twitter card tags, and JSON-LD. The home page
declares `Organization` and `WebSite`; every other page declares `Organization`
and a `BreadcrumbList`. The 404 page is `noindex` and carries no structured
data.

Three files support crawling:

- **`robots.txt`** allows everything and names the sitemap. It also names the
  major assistant crawlers explicitly, so answer engines can read and cite the
  site.
- **`sitemap.xml`** lists the ten indexable pages with priorities.
- **`llms.txt`** is a structured plain-language summary following the
  llmstxt.org convention. Its final section tells a summarising model what
  *not* to claim: that programmes are not open, that no impact figures exist,
  and that no fee is ever charged.

### The origin is defined in one place

Canonicals, `og:url`, JSON-LD and the sitemap all need an absolute URL. That
lives in `BASE` at the top of the page builder, and is currently the live
GitHub Pages address. It is deliberately not the future custom domain, because
a canonical pointing at a site that does not answer yet will get the pages
dropped from the index.

When the domain is live, update it everywhere in one pass:

```bash
grep -rl "luishowin.github.io/hernext-network-website/" docs/ | xargs sed -i 's#https://luishowin.github.io/hernext-network-website/#https://www.hernextnetwork.org/#g'
```

Then submit `sitemap.xml` in Google Search Console and Bing Webmaster Tools.

---

## Legal pages

Three pages sit in the footer: `privacy.html`, `terms.html` and
`accessibility.html`.

**These are drafts written to match what the site actually does, not legal
advice.** Have them reviewed by a qualified adviser in the jurisdictions
HerNext operates in. Four placeholders must be filled in first, and they are
marked in the text:

- `[registered entity name]`
- `[registered address]`
- `[governing jurisdiction]`, in both the privacy policy and the terms

```bash
grep -rn "\[registered entity name\]\|\[registered address\]\|\[governing jurisdiction\]" docs/
```

The privacy policy names the three third parties that actually see visitor
data: Formspree, GitHub Pages and Google Fonts. If you drop Google Fonts in
favour of self-hosting, or add analytics, that section has to change with it.

### Why the application flow says "register your interest"

The site previously said applications were open and promised a reply within
fifteen working days. For a pre-funding organisation whose programmes are still
in development, that is a representation that would be hard to defend, and the
people it would let down are the exact audience HerNext exists to serve.

The flow now collects the same information through the same four steps, but it
is framed as registering interest, states plainly that programmes are in
development, and commits to no timeline. The terms page carries the same
statement, and adds that no fee is ever charged and how to report anyone
soliciting payment in the organisation's name.

If real programmes open later, the copy to revisit is the page hero and the
notice in `apply.html`, the confirmation text, and the shared call to action.

---

## Editing the copy

All text lives in the HTML, and `CONTENT.md` mirrors it as a plain document
organised by page and section. Copy can be reviewed and revised there, then
applied to the matching page.

Two conventions to preserve:

- **No em dashes anywhere.** Use a comma, a colon, or the word *and*. The
  house style is checked at the end of this file.
- **One `<em>` per heading.** The italic gold emphasis reads as a deliberate
  accent only while it stays rare.

### Contact details

The Institutional Profile lists contact details as "to be inserted", so the
site carries placeholders. Replace these everywhere before launch:

| Placeholder | Appears in |
|---|---|
| `info@hernextnetwork.org` | footer on all pages, contact page |
| `apply@hernextnetwork.org` | contact page, form error message in `forms.js` |
| `+00 000 000 000` | footer on all pages, contact page |
| `https://www.linkedin.com` | footer on all pages, contact page |

A quick way to find every occurrence:

```bash
grep -rn "hernextnetwork.org\|+00 000 000 000" docs/
```

### The figures on the home page

The statistics band shows structural counts drawn from the Institutional
Profile: nine strategic pillars, six signature initiatives, eleven priority
sectors and five Sustainable Development Goals. These are accurate today and
need no disclaimer. When real impact metrics exist, that band in
`docs/index.html` is where they belong.

---

## Deploying to GitHub Pages

The site is configured to publish from the `docs/` folder on the default
branch, so deployment is a push.

1. Push to `main`.
2. In the repository, open **Settings**, then **Pages**.
3. Under **Build and deployment**, set **Source** to *Deploy from a branch*.
4. Choose branch `main` and folder `/docs`, then **Save**.

The site appears at `https://<username>.github.io/<repository>/` within a
minute or two.

Two details make this work and are worth preserving:

- **`docs/.nojekyll`** stops GitHub from running the files through Jekyll,
  which would otherwise ignore anything beginning with an underscore.
- **Every internal link is relative and has no leading slash**, for example
  `about.html` and `assets/images/logo-mark.svg`, never `/about.html`. This is
  what lets the identical build work from a subdirectory today and from a
  custom domain later without a single edit. Keep it that way when adding
  pages.

---

## Adding the custom domain

Once the domain is registered:

1. Create a file named `CNAME` inside `docs/`, containing only the domain and
   nothing else:

   ```
   www.hernextnetwork.org
   ```

2. At your DNS provider, add a `CNAME` record pointing `www` to
   `<username>.github.io`. To serve the apex domain as well, add four `A`
   records pointing at `185.199.108.153`, `185.199.109.153`,
   `185.199.110.153` and `185.199.111.153`.
3. Back in **Settings**, then **Pages**, enter the domain and tick
   **Enforce HTTPS** once the certificate has been issued, which usually takes
   a few minutes and occasionally up to a day.

Then set the social sharing tags, which need absolute URLs. Add a 1200 x 630
PNG at `docs/assets/images/og-image.png`, and uncomment the `og:url` and
`og:image` block in the `<head>` of each page, replacing the domain with the
real one.

---

## Before launch

- [ ] Formspree IDs added to `apply.html` and `contact.html`, both tested live
- [ ] Real email address and telephone number in place, LinkedIn URL confirmed
- [ ] Legal placeholders filled in: entity name, address, governing jurisdiction
- [ ] Privacy policy and terms reviewed by a qualified adviser
- [ ] Redrawn logo dropped in, and all three logo files plus the favicon regenerated
- [ ] Final social preview image replacing the interim `og-image.jpg`
- [ ] `apple-touch-icon.png` added and the line in the `<head>` uncommented
- [ ] Remaining seven placeholder images replaced, with alt text reviewed
- [ ] `CNAME` added, HTTPS enforced, and the origin swap run across `docs/`
- [ ] `sitemap.xml` submitted to Google Search Console
- [ ] Copy signed off against `CONTENT.md`

---

## Browser support and accessibility

Targets the current versions of Chrome, Edge, Firefox and Safari, desktop and
mobile. The layout uses CSS Grid, custom properties, `clamp()` and `:has()`,
all of which have been broadly supported since 2023. There is no build step and
no polyfill.

Accessibility work already in place:

- Skip link, semantic landmarks, and `aria-current="page"` on the active nav
- A visible focus ring on every interactive element
- Every form control has a bound label, errors are wired through
  `aria-describedby`, and step changes and submission results are announced
  through `aria-live`
- Heading order never skips a level on any page
- Touch targets meet the 44 pixel minimum
- `prefers-reduced-motion` is fully honoured
- Text contrast meets WCAG AA throughout

Verified across the site: no horizontal scrolling at 375, 768 or 1280 pixels,
no console errors, no broken links, and no em dashes.

---

## Credits

Design and development by [Beben Design](https://beben.design).
Content adapted from the HerNext Network Institutional Profile, First Edition,
2026.

Copyright HerNext Network. All rights reserved.
