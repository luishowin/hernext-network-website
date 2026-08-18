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
- [Replacing the placeholder images](#replacing-the-placeholder-images)
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
  apply.html               Four-step application
  contact.html             Contact details and enquiry form
  404.html                 Not found
  robots.txt
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

## Replacing the placeholder images

Every image slot holds a flat SVG placeholder labelled with its purpose and its
recommended pixel size. To use a real photograph, **replace the file and keep
the existing name**, and no markup has to change.

| File | Slot | Recommended size |
|---|---|---|
| `placeholder-hero.svg` | Home hero portrait | 800 x 1000 |
| `placeholder-story.svg` | About, our story | 1200 x 800 |
| `placeholder-initiative-1.svg` | Leadership Academy | 900 x 600 |
| `placeholder-initiative-2.svg` | Opportunity Hub | 900 x 600 |
| `placeholder-initiative-3.svg` | Trade and Investment | 900 x 600 |
| `placeholder-partners.svg` | Partners banner | 1600 x 700 |
| `placeholder-impact.svg` | Impact section | 1200 x 800 |
| `placeholder-contact.svg` | Contact page | 1000 x 667 |
| `placeholder-apply.svg` | Closing call to action | 900 x 1125 |

If you switch to `.jpg` or `.webp`, update the `src` and the `width` and
`height` attributes on that `<img>`. Keeping `width` and `height` accurate is
what stops the page from shifting as images load.

Alt text is already written for each slot on the assumption that a real
photograph will replace the placeholder. Review it once the final images are
chosen so it describes what is actually shown.

### About the logo files

The supplied logo SVGs were 156 KB each, mostly a 257-stop gradient
interpolating two colours plus the tagline set as outlines. Three lighter
assets were derived for the web:

- `logo-mark.svg` (22 KB), the emblem alone, used in the header and favicon
- `logo-light.svg` (61 KB), emblem and wordmark on light backgrounds
- `logo-dark.svg` (61 KB), the same for dark backgrounds, used in the footer

The originals are untouched in `HNN Logo C/` for print and other uses.

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
| `https://www.instagram.com` | footer on all pages, contact page |

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
- [ ] Real email addresses, telephone number and social links in place
- [ ] Real photographs replacing the nine placeholders, with alt text reviewed
- [ ] `CNAME` added and HTTPS enforced
- [ ] Social sharing image added and the `og:` block uncommented
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
