# HerNext Network

**Creating Opportunity. Building Legacy.**

The institutional website for HerNext Network, a women-centred Pan-African
institution advancing women's economic transformation through practical,
evidence-driven interventions that expand access to markets, finance, skills,
strategic partnerships and sustainable livelihood opportunities.

Plain HTML, CSS and JavaScript. No framework and no dependencies. The contents
of `docs/` are the deployed site exactly as served.

**Live at** https://luishowin.github.io/hernext-network-website/

---

## Contents

- [Status](#status)
- [What changed in the 2026 revision](#what-changed-in-the-2026-revision)
- [Quick start](#quick-start)
- [Project structure](#project-structure)
- [Regenerating the pages](#regenerating-the-pages)
- [Design system](#design-system)
- [Connect the form](#connect-the-form)
- [Images](#images)
- [SEO and crawling](#seo-and-crawling)
- [Legal pages](#legal-pages)
- [Editing the copy](#editing-the-copy)
- [Deploying to GitHub Pages](#deploying-to-github-pages)
- [Adding the custom domain](#adding-the-custom-domain)
- [Before launch](#before-launch)
- [Browser support and accessibility](#browser-support-and-accessibility)

---

## Status

The site is complete, verified and deployed. The 2026 content corrections have
been applied in full. Five things are still outstanding, and two of them block
launch.

| Outstanding | Where it goes | Blocking launch |
|---|---|---|
| Formspree form ID | `contact.html` | **Yes.** The form is inert until then, and says so rather than failing quietly |
| Legal placeholders: entity name, address, jurisdiction | `privacy.html`, `terms.html` | **Yes** |
| Redrawn logo SVG | regenerates `logo-mark`, `logo-light`, `logo-dark`, `favicon` | No, current files are derived from the supplied SVG |
| LinkedIn URL | footer and contact page | No. Email, telephone and Instagram are live |
| Final social preview image | `assets/images/` | Recut from the hero photograph |

Each has its own section below, and the full list is repeated as a checklist
under [Before launch](#before-launch).

One thing to know before reading further: **the pages in `docs/` are generated.**
Edit `tools/partials/` and run `python tools/make.py`. See
[Regenerating the pages](#regenerating-the-pages).

---

## What changed in the 2026 revision

The client returned four correction documents that rewrote most of the site's
copy. The through-line of all four is a repositioning **from aspiration to
evidence**: the site used to describe the institution by its ambitions, and now
describes it by its method.

If you knew the earlier site, these are the changes that will surprise you.

| Was | Now |
|---|---|
| `opportunities.html`, "Opportunities" in the nav | `our-work.html`, "Our Work". The old address is a redirect stub |
| `apply.html`, a four-step registration form | Folded into the contact form. The old address is a redirect stub |
| Six nav items including a gold "Register interest" button | Five: About, Our Work, Impact, Partners, Contact |
| Nine strategic pillars | Six interconnected areas of work |
| Eleven priority sectors | Nine, with leadership, governance, entrepreneurship, research and capacity development moved out into cross-cutting capabilities |
| Six initiatives including a "HerNext Partnership Forum" | Six, without it, and none described as open |
| "Each is open to applications" | A *Current opportunities* section that is empty by design and says so |
| Impact opened on the opportunity gap | Impact opens on what impact means, and carries the Kiambu Chapter as evidence in progress |
| Seven partner categories | Eight, and a new *How we partner* section |
| Partnership principle 05, "Innovation" | "Measurable impact" |
| `info@hernextnetwork.org`, `+00 000 000 000` | Real addresses and Kenyan numbers, see [Contact details](#contact-details) |

Three editorial rules came with the corrections and outlive them. They are the
reason several sections read more cautiously than a marketing site normally
would, and they should survive future edits:

1. **Nothing is described as open unless it is open.** No initiative, no
   programme, no call for applications.
2. **No result is attributed to an intervention that has not been measured.**
   The Kiambu Chapter is an example of the process, not proof of impact, and
   the figures on the home page count structure rather than outcomes.
3. **Women stay at the centre** of the institutional positioning, not at the
   edge of it.

The four source documents live outside the repository, in the client's
`Hernext` folder. `CONTENT.md` is the authoritative record of what they said.

---

## Quick start

There is nothing to install and nothing to compile. Serve the `docs/` folder:

```bash
python tools/serve.py
```

Then open `http://localhost:8123`.

`python -m http.server` also works for everything except the hero clip. It
answers every request with the whole file and never implements ranges, and a
browser's media pipeline needs ranges, so the clip hangs with no error and the
page looks broken for a reason that has nothing to do with the site.

Opening the HTML files directly from the file system also works, though the
fonts load from Google Fonts and therefore need a network connection.

To change anything on the pages, edit `tools/partials/` and rebuild:

```bash
python tools/make.py
```

That needs Python 3 and nothing else. Pillow is only required if you are
optimising new photographs, as described under [Images](#images).

---

## Project structure

```
docs/                      the published site, this is the deploy root
  index.html               Home
  about.html               About HerNext, story, foundation, values, vision
  our-work.html            Six areas of work, the pathway, initiatives, sectors
  impact.html              What impact means, the model, Kiambu, measurement
  partners.html            Philosophy, eight partner types, how we partner
  contact.html             Contact details and the site's only form
  privacy.html             Privacy policy
  terms.html               Terms of use
  accessibility.html       Accessibility statement
  404.html                 Not found, noindex
  opportunities.html       Stub, redirects to our-work.html, noindex
  apply.html               Stub, redirects to contact.html, noindex
  robots.txt               permissive, points at the sitemap
  sitemap.xml              the nine indexable pages, stubs excluded
  llms.txt                 structured summary for assistants and answer engines
  .nojekyll                tells GitHub Pages to serve the files as they are
  css/style.css            the entire design system, one file
  js/main.js               navigation, scroll reveal, header state, year, hero clip
  js/forms.js              validation and submission for the contact form
  assets/images/           logos, favicon, photography
  assets/video/            the home hero clip, absent until it is encoded

tools/
  make.py                  rebuilds every page in docs/, run this after editing
  build.py                 assembler, and the one place BASE is defined
  images.py                cuts every photograph from the originals, crops recorded
  video.py                 encodes the hero clip into its two renditions
  serve.py                 local preview, with the range support video needs
  icons.py                 cuts the favicons and logo marks from the client artwork
  partials/
    _head.html             doctype through to the opening <main>, shared
    _footer.html           footer, scripts, closing tags, shared
    _cta.html              the closing call to action, shared by four pages
    _index_main.html       the body of each page, one file per page
    _about.html            ...
    _our_work.html         ...

CONTENT.md                 the copy deck, every line of text on the site
README.md                  this file
source-media/              untouched photo originals and the raw hero clip, gitignored
```

The source PDFs and the original logo folder sit at the repository root,
outside `docs/`, so they are never published with the site. So do the photo
originals in `source-media/`, which keeps multi-megabyte files from ever being
served to a visitor.

---

## Regenerating the pages

Ten pages share one head, one header, one footer and one closing call to
action. Keeping those in step by hand is how sites drift, so the shared chrome
is assembled instead.

**The HTML files in `docs/` are outputs.** Each one opens with a comment saying
so. Edit the partial, not the page:

```bash
python tools/make.py
```

That rewrites all ten pages, regenerates canonicals, Open Graph tags and
JSON-LD from `BASE`, writes the two redirect stubs, and re-attaches `forms.js`
to the contact page. It takes about a second.

| To change | Edit |
|---|---|
| Anything in the `<head>`, or the header and navigation | `tools/partials/_head.html` |
| The footer, including contact details and legal links | `tools/partials/_footer.html` |
| The closing call to action on four pages | `tools/partials/_cta.html` |
| The body of one page | `tools/partials/_<page>.html` |
| A page title, description, or which pages get the call to action | `tools/make.py` |
| Where a moved address sends its visitors | the `redirect()` calls in `tools/make.py` |
| The live origin used by canonicals, tags, JSON-LD | `BASE` in `tools/build.py` |
| The organisation JSON-LD, including contact details | `ORG` in `tools/build.py` |

This is an authoring convenience, not a build step. Nothing is compiled,
minified or transformed. The output is the same plain HTML you would write by
hand, and the deployed site has no idea the tooling exists. You can safely
ignore it and hand-edit all ten pages instead, as long as you accept that
the shared chrome will drift.

---

## Design system

Everything is driven by custom properties at the top of `docs/css/style.css`.
Change a token there and it updates across all ten pages.

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

Three recurring patterns:

- **Micro-label.** `<p class="label">Signature initiatives</p>` renders small,
  uppercase, letter-spaced and gold, sitting flush with the left margin so it
  aligns with the heading beneath it.
- **Emphasis word.** A single `<em>` inside a heading renders in Cormorant
  italic in gold, for example
  `<h2>Turning evidence into <em>action</em></h2>`. One per heading, no more:
  the accent reads as deliberate only while it stays rare.
- **Pathway chain.** An ordered list of the steps in the HerNext method, with
  gold arrows drawn between them in CSS:

  ```html
  <ol class="pathway pathway--framed" data-reveal="self">
    <li class="pathway__step">Listen</li>
    <li class="pathway__step">Identify</li>
  </ol>
  ```

  The arrow is a `::before` on every step but the first, so a screen reader
  hears a plain ordered list rather than a string of arrow characters. The
  chain wraps freely at narrow widths, where a wrapped row simply opens with
  the arrow. `--framed` adds the hairline rules above and below. It appears on
  Home, Our Work, Impact and Partners, and the wording of the steps should not
  drift between them.

### Motion

Section content reveals on scroll in a stagger. Put `data-reveal` on any
container and its direct children animate in sequence; `main.js` assigns the
`--i` index, and the CSS turns that into a `transition-delay`. Use
`data-reveal="self"` to animate the element itself instead of its children.

The pathway chains use `data-reveal="self"` deliberately. Staggering eight
short steps at 115ms each takes almost two seconds to settle, which reads as
broken rather than considered, so the chain arrives as one unit.

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

## Connect the form

**This is the one step required before launch.** GitHub Pages serves static
files and cannot receive a form submission, so the contact form posts to
[Formspree](https://formspree.io). Until you supply an ID it is inert, and
submitting shows a message saying so rather than failing silently.

1. Create a free Formspree account and add one form. It gets an ID that looks
   like `xayzbqwe`.
2. Set the delivery address to the HerNext inbox.
3. Replace `REPLACE_ME` in the partial, not in the built page:

   | File | Attribute |
   |---|---|
   | `tools/partials/_contact.html` | `<form id="contact-form" data-endpoint="https://formspree.io/f/REPLACE_ME">` |

   Then run `python tools/make.py`.
4. Submit the form once from the live site. Formspree asks you to confirm the
   destination address the first time.

Submissions arrive by email and are listed in the Formspree dashboard, where
they can be exported. The free tier allows 50 submissions per month, so
consider a paid plan before an initiative opens and registrations arrive in
volume.

Field names are human-readable, so a submission arrives as `Full name`,
`Email`, `Organisation`, `Subject` and `Message` rather than as terse input
names. The `Subject` value is what separates a registration of interest from a
partnership enquiry, so it is worth setting up a Formspree filter on it.

### Using something else

`forms.js` performs a single `fetch` POST with a `FormData` body and an
`Accept: application/json` header, and treats any `response.ok` as success.
Any endpoint meeting that contract works without further changes: Getform,
Basin, Netlify Forms or your own handler. Only the `data-endpoint` value needs
to change.

---

## The hero clip

The home page hero carries a looping clip over its photograph. It is the
heaviest thing on the site by a wide margin, and almost all of the code around
it is about deciding not to play it.

### Adding or replacing it

```bash
sudo dnf install ffmpeg     # once. RPM Fusion is already enabled
                            # ffmpeg-free will not do, it has no libx264
```

Put the camera file in `source-media/`, then:

```bash
python tools/video.py
python tools/make.py
```

`video.py` writes two renditions into `docs/assets/video/`, 1600 wide for
desktop and 960 for narrow viewports, both ten seconds, both silent. `make.py`
then adds the `<video>` element to the home hero. It only does that when both
files exist, so a checkout without a clip ships the photograph alone and no
browser is ever sent looking for a file that is not there.

| File | Budget |
|---|---|
| `hnn-hero-1600.mp4` | 1.6 MB |
| `hnn-hero-960.mp4` | 600 KB |

Check the loop seam. A clip whose first and last frames disagree jumps visibly
every ten seconds, and no amount of encoding hides it.

The camera file stays in `source-media/` and is never committed. Git keeps
every version of a binary it is handed, permanently, and a few rounds of
re-encoding would weigh more than the entire rest of the repository.

### Why it is built the way it is

The clip does not replace the photograph, it lies over it. The `<img>` keeps
its `srcset` and its `fetchpriority`, so it is still what paints first, still
what decides the largest contentful paint, and still what carries the
alternative text. Every case where the clip does not run leaves the hero
exactly as it was.

It ships with **no `src` and no `autoplay` attribute**. `main.js` attaches a
source only after all of these pass, and each one fetches nothing when it
fails:

- **Reduced motion.** The accessibility statement says all animation is
  switched off when the system asks for it. A paused video would still be a
  downloaded video, so this declines before a byte is requested. Turning the
  setting on mid-visit removes the clip immediately.
- **A metered connection.** `saveData`, or an `effectiveType` of 2g.
- **A browser that cannot play H.264.**
- **Visibility.** The clip runs only while the hero band is on screen and the
  tab is in front. This is not only courtesy: Chrome stops a video-only element
  that is scrolled out of view with *"background media was paused to save
  power"*, so an unconditional `play()` on load is refused every time, because
  the hero band sits below the fold. Geometry is measured directly rather than
  through IntersectionObserver, for the same reason `initReveal` does.

A play and pause control is inserted by script once the clip is eligible, never
before, so it cannot appear with nothing to control. WCAG 2.1 asks for a way to
stop anything that moves by itself for more than five seconds, and the site
calls that standard a floor rather than a finish line. The choice is remembered
for the rest of the visit, and while a pause stands nothing is downloaded at
all.

There is no audio track, at all. Muting is required for autoplay anyway, and a
file with no audio stream cannot raise WCAG 1.4.2 however it is embedded.

If `play()` is refused, by a browser policy or a battery saver or a race with
its own load, that is not treated as a failure. The photograph is untouched
underneath and the control is left offering to start the clip. Only a real
decode or network error removes the element.

---

## Images

Photographs are served as WebP at three or four widths each, chosen by the
browser through `srcset`. On a 375 pixel phone at 2x the hero loads the 1000
wide file at 81 KB rather than the 1600 wide file at 169 KB.

All fourteen slots carry photography from a single HerNext Network community
gathering. The first nine file stems are slot names that predate the
photographs now in them, so `hnn-office` is not an office and `hnn-trade` is
not a trade floor: they name a position on the page, not a subject. The five
added later are named for what they show.

| Slot | Files | Page |
|---|---|---|
| Hero, full bleed, 16:9 | `hnn-presentation-{700,1000,1600}.webp` | Home |
| Our story, 16:9 | `hnn-office-{600,900,1400}.webp` | About |
| Partnership philosophy banner, 16:7 | `hnn-forum-{700,1000,1400}.webp` | Partners |
| Leadership Academy card, 3:2 | `hnn-academy-{400,800,1200}.webp` | Our Work |
| Opportunity Hub card, 3:2 | `hnn-mentoring-{400,800,1200}.webp` | Our Work |
| Global Trade card, 3:2 | `hnn-trade-{400,800,1200}.webp` | Our Work |
| Impact in action, Kiambu, 3:2 | `hnn-team-{600,900,1400}.webp` | Impact |
| Contact, 3:2 | `hnn-hall-{600,900,1400}.webp` | Contact |
| Closing call to action, 4:5 | `hnn-conversation-{400,600,800,1000}.webp` | Home, About, Our Work, Impact |
| Why we exist, 1:1 | `hnn-together-{400,700,1000}.webp` | Home |
| How we work, 1:1 | `hnn-facilitator-{400,700,1000}.webp` | Home |
| How a partnership begins, 1:1 | `hnn-welcome-{400,700,1000}.webp` | Partners |
| From data to action, 1:1 | `hnn-coordinator-{400,700,1000}.webp` | Impact |
| The Africa we envision, 3:2 | `hnn-circle-{600,900,1400}.webp` | About |
| Social preview | `og-image.jpg`, 1200 x 630, recut from the hero | all pages |

The untouched camera originals are in `source-media/` at the repository root,
which is gitignored. They stay out of `docs/` so a 7 MB file can never be
served to a visitor by accident.

### Adding or recutting a photograph

Every crop lives in one manifest, `PHOTOS` at the top of `tools/images.py`:
source file, crop box, output widths. Put the original in `source-media/`, add
a row, and run:

```bash
python tools/images.py
```

It crops, resizes with LANCZOS and writes WebP at each width. Quality is not
fixed. Each file is encoded at the highest quality that still fits a byte
ceiling derived from its pixel count, because a busy frame full of people and
plywood grain costs far more than a calm one at the same dimensions and a
single setting cannot suit both. A file that cannot reach its ceiling fails
the run rather than shipping quietly degraded.

A row may carry an optional fifth field, a multiplier on that ceiling, for a
frame the curve genuinely misjudges. The two outdoor photographs use it: a
hedge in daylight is about the most expensive thing a photograph can contain,
every leaf being an edge, and held to the ordinary budget they encode at the
quality floor, which is where artefacts start showing on skin. Use it sparingly
and say why in the manifest, or it stops being an exception.

This replaced a snippet that was pasted into a shell and never committed. The
crop boxes it used were written down nowhere, so when the originals were later
cleared off the machine the lossy WebP was all that survived and nothing could
be recut. Keeping the manifest current is what stops that happening twice.

Then reference every width in one `<img>`, and keep `width` and `height` on the
tag so the page does not shift as it loads:

```html
<img src="assets/images/your-photo-1600.webp"
     srcset="assets/images/your-photo-700.webp 700w,
             assets/images/your-photo-1000.webp 1000w,
             assets/images/your-photo-1600.webp 1600w"
     sizes="100vw" alt="Describe what is happening in the photograph"
     width="1600" height="900" decoding="async">
```

`sizes` has to describe the box the image actually lands in, or the browser
fetches the wrong file. Measure it rather than estimating: `.container` caps at
1280px, so above that width a figure stops growing and a `vw` unit stops
describing it, and `.card` adds 36px of padding on each side. The three in use:

| Layout | `sizes` |
|---|---|
| Full bleed hero | `100vw` |
| Two column split | `(max-width: 900px) 90vw, (max-width: 1280px) 35vw, 450px` |
| Three up card grid | `(max-width: 640px) 80vw, (max-width: 900px) 36vw, (max-width: 1280px) 23vw, 292px` |

The splits used to claim `45vw` where the figure renders at about `29vw`, and
the cards `30vw` where they render at `23vw`, so both pulled a file a rung
larger than they could use.

### Cropping to the slot

Every `.media` class fixes an aspect ratio in CSS and crops with
`object-fit: cover`, so a photograph whose native ratio differs will be cut by
the browser wherever it happens to land. Crop deliberately at build time
instead, then set `width` and `height` to the cropped size so the ratio in the
markup matches the ratio in the stylesheet and the page never shifts:

| Class | Ratio | Used by |
|---|---|---|
| `media--square` | 1 / 1 | four frames shot square, used at their native ratio |
| `media--portrait` | 4 / 5 | closing call to action |
| `media--landscape` | 3 / 2 | initiative cards, impact, contact |
| `media--wide` | 16 / 7 | partners banner |
| `media--169` | 16 / 9 | about, our story |

Two crops are tight on purpose and the manifest says why: `hnn-mentoring` is
cut hard to the right, and `hnn-team` is taken from the upper band of its
frame, because the fuller crop of each puts a small child in the foreground.

Consent for these photographs is understood to cover adults for public web
use. Children are excluded by crop rather than relied upon, so widening either
of those two boxes needs checking again before it ships.

### Assets you are replacing

| File | Note |
|---|---|
| `logo-mark.svg`, `logo-light.svg`, `logo-dark.svg` | Derived from the supplied SVG. Regenerate all three when the redrawn logo lands |
| `favicon.svg` | Currently the emblem cropped from the same source |
| `og-image.jpg` | Recut from the hero crop by `tools/images.py`, so the preview and the page agree |

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
lives in `BASE` near the top of `tools/build.py`, and is currently the live
GitHub Pages address. It is deliberately not the future custom domain, because
a canonical pointing at a site that does not answer yet will get the pages
dropped from the index.

When the domain is live, change `BASE`, rebuild, and regenerate the sitemap:

```bash
python tools/make.py
```

`robots.txt` and `sitemap.xml` are not generated by that script, so update the
origin in both by hand, or run:

```bash
sed -i 's#https://luishowin.github.io/hernext-network-website/#https://www.hernextnetwork.com/#g' docs/robots.txt docs/sitemap.xml docs/llms.txt
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

### Why the site says "register your interest" and never "apply"

The site once said applications were open and promised a reply within fifteen
working days. For a pre-funding organisation whose initiatives are still in
development, that is a representation that would be hard to defend, and the
people it would let down are the exact audience HerNext exists to serve.

The 2026 corrections went further and made this an editorial rule across the
whole site: do not state that an initiative is open to applications unless
applications are genuinely open, and do not present an initiative still being
developed as an established programme with completed outcomes. The Our Work
page therefore carries a *Current opportunities* section that is empty by
design, and says so.

Registering interest now goes through the contact form, framed as registering
interest, stating plainly that initiatives are in development, and committing
to no timeline. The terms page carries the same statement, and adds that no fee
is ever charged and how to report anyone soliciting payment in the
organisation's name.

**When a real opportunity opens**, the places to change are the *Current
opportunities* section of `tools/partials/_our_work.html`, which carries a
commented-out card template, and the callout above the initiative grid on the
same page. Nothing else needs to move.

---

## Editing the copy

All text lives in the partials under `tools/partials/`, and `CONTENT.md`
mirrors it as a plain document organised by page and section. Copy can be
reviewed and revised in `CONTENT.md`, applied to the matching partial, then
built with `python tools/make.py`.

Two conventions to preserve:

- **No em dashes anywhere.** Use a comma, a colon, or the word *and*. The
  house style is checked at the end of this file.
- **One `<em>` per heading.** The italic gold emphasis reads as a deliberate
  accent only while it stays rare.

### Contact details

The real details are in place. One placeholder remains.

| Detail | Value | Appears in |
|---|---|---|
| Primary email | `info@hernextnetwork.com` | footer, contact page, legal pages, JSON-LD, `llms.txt`, `forms.js` error message |
| Secondary email | `hernextnetwork@gmail.com` | footer, contact page, terms, JSON-LD, `llms.txt` |
| Telephone | `0780 528 551`, dialling `+254780528551` | footer, contact page, JSON-LD |
| Telephone | `0734 806 637`, dialling `+254734806637` | footer, contact page, JSON-LD |
| Instagram | `@hernextnetworkltd` | footer, contact page, terms, JSON-LD, `llms.txt` |
| LinkedIn | `https://www.linkedin.com` **placeholder** | footer, contact page |

Numbers display in Kenyan local format and dial in international format. Change
the display text and the `tel:` href together, or one will contradict the other.

The email address lives in four places that are easy to miss when changing it:
`ORG` in `tools/build.py` (JSON-LD), the failure message in `docs/js/forms.js`,
`docs/llms.txt`, and the official-channels sentence in section 3 of the terms.

A quick way to confirm nothing stale survives:

```bash
grep -rn "hernextnetwork.org\|+00 000 000 000\|apply@" docs/ tools/
```

### The figures on the home page

The statistics band shows structural counts: six areas of work, six signature
initiatives, nine priority sectors and five Sustainable Development Goals.
These count structure, not results, so they need no disclaimer.

**They are not a place for impact metrics yet.** The 2026 corrections are
explicit that no figure may be published before follow-up measurement supports
it. When verified programme results exist, the band in
`tools/partials/_index_main.html` is where they belong, and the Impact page
gains its before-and-after indicators at the same time.

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
   www.hernextnetwork.com
   ```

2. At your DNS provider, add a `CNAME` record pointing `www` to
   `<username>.github.io`. To serve the apex domain as well, add four `A`
   records pointing at `185.199.108.153`, `185.199.109.153`,
   `185.199.110.153` and `185.199.111.153`.
3. Back in **Settings**, then **Pages**, enter the domain and tick
   **Enforce HTTPS** once the certificate has been issued, which usually takes
   a few minutes and occasionally up to a day.

The social sharing tags need no attention here. `og:url` and `og:image` are
generated from `BASE`, so changing `BASE` and rebuilding updates them on all
ten pages and both redirect stubs at once. The steps for that are under
[The origin is defined in one place](#the-origin-is-defined-in-one-place).

---

## Before launch

- [ ] Formspree ID added to `tools/partials/_contact.html`, rebuilt and tested live
- [ ] LinkedIn URL confirmed and swapped in
- [ ] Legal placeholders filled in: entity name, address, governing jurisdiction
- [ ] Privacy policy and terms reviewed by a qualified adviser
- [ ] Redrawn logo dropped in, and all three logo files plus the favicon regenerated
- [ ] Final social preview image replacing the interim `og-image.jpg`
- [ ] Confirm photo consent covers public web use for everyone shown
- [ ] `CNAME` added, HTTPS enforced, `BASE` updated in `tools/build.py` and rebuilt,
      and the origin swapped in `robots.txt`, `sitemap.xml` and `llms.txt`
- [ ] `sitemap.xml` submitted to Google Search Console
- [ ] Copy signed off against `CONTENT.md`
- [ ] Nothing on the site claims an initiative is open, or attributes a result
      to an intervention that has not yet been measured

---

## Browser support and accessibility

Targets the current versions of Chrome, Edge, Firefox and Safari, desktop and
mobile. The layout uses CSS Grid, custom properties, `clamp()`, `:has()` and
`dvh` units, and photographs are served as WebP through `srcset`. All of these
have been broadly supported since 2023, WebP since 2020. There are no
polyfills, and nothing is transpiled.

The one place this matters in practice: `dvh` is what makes the mobile menu
fill the screen correctly as browser chrome grows and shrinks on scroll. On a
browser without it the menu falls back to filling the layout viewport, which is
slightly taller than the visible area but still usable.

Accessibility work already in place:

- Skip link, semantic landmarks, and `aria-current="page"` on the active nav
- A visible focus ring on every interactive element
- Every form control has a bound label, errors are wired through
  `aria-describedby`, and submission results are announced through `aria-live`
- The pathway chains are ordered lists. The arrows between steps are drawn in
  CSS, so a screen reader hears "Listen, Identify, Design" and not a string of
  stray arrow characters
- Heading order never skips a level on any page
- Touch targets meet the 44 pixel minimum
- `prefers-reduced-motion` is fully honoured
- Text contrast meets WCAG AA throughout

Verified across all ten pages: no horizontal scrolling at 375, 768 or 1280
pixels, no console errors, no broken links, no unused assets, no heading level
skips and no em dashes.

`accessibility.html` states this publicly, along with four limitations named
honestly rather than left for a visitor to discover: the Google Fonts
dependency, screen reader pairings not yet exhaustively tested, photography
still being replaced, and no independent audit yet. Keep that page truthful as
the site changes. An accessibility statement that overclaims is worse than
none.

---

## Credits

Design and development by [Beben Design](https://beben.design).
Content adapted from the HerNext Network Institutional Profile, First Edition,
2026, and revised in full against the 2026 correction documents for the About,
Our Work, Impact, and Partners and Collaboration pages.

Copyright HerNext Network. All rights reserved.
