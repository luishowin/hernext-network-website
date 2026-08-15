# HerNext Network — Official Website

**Creating Opportunity. Building Legacy.**

A multi-page static website for HerNext Network, a Pan-African institution committed to advancing women's economic transformation through leadership, entrepreneurship, innovation, and strategic partnerships.

## Pages

| Page | Description |
|---|---|
| **Home** | Introduction, purpose, vision, signature initiatives |
| **About** | Institutional story, mission, vision, core values |
| **Opportunities** | Strategic pillars, signature initiatives, priority sectors |
| **Impact** | Approach, opportunity gap analysis, SDG alignment |
| **Partners** | Partnership philosophy, partner categories |
| **Apply** | Multi-step application form with validation |
| **Contact** | Contact information and enquiry form |

## Tech Stack

- **HTML5** — Semantic, accessible markup
- **CSS3** — Custom design system with gold/amber brand colors, responsive grid, dark theme
- **Vanilla JavaScript** — Multi-step form navigation, mobile menu toggle, form validation

## Design System

| Token | Value |
|---|---|
| Primary Gold | `#C8963E` |
| Light Gold | `#E8D48B` |
| Dark Gold | `#8B6914` |
| Background | `#0D0D0D` |
| Surface | `#1A1A1A` |
| Text Primary | `#F5F0E8` |

## Local Development

```bash
# Serve the site locally
python -m http.server 8123 --directory docs

# Open in browser
# http://localhost:8123
```

## Deployment

The site is built as static HTML in the `docs/` directory. Deploy to any static host:

- **GitHub Pages**: Point to `docs/` folder on main branch
- **Netlify / Vercel**: Set publish directory to `docs/`

## Project Structure

```
.
├── docs/
│   ├── index.html          # Home page
│   ├── about.html          # About HerNext
│   ├── opportunities.html  # Programmes & initiatives
│   ├── impact.html         # Impact & approach
│   ├── partners.html       # Partnership information
│   ├── apply.html          # Multi-step application
│   ├── contact.html        # Contact form
│   ├── css/
│   │   └── style.css       # Full design system
│   ├── js/
│   │   └── app.js          # Form logic & navigation
│   └── assets/
│       └── images/         # Brand logos (SVG)
├── opencode.json           # OpenCode AI config
└── README.md
```

## License

© 2026 HerNext Network. All rights reserved.
