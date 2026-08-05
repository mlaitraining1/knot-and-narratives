# The Knot & Narratives — Wedding Photography & Choreography Website

A complete, production-ready static website for a wedding photography + choreography
studio. Plain HTML/CSS/JS (no build step, no framework) so it's easy to hand off,
edit, and deploy.

## What's included

- **9 pages**: Home, Portfolio, Stories (journal), a single Story detail page
  (template for future posts), About, Services, Pricing, Contact, Client Gallery
  — plus a custom 404.
- **Responsive design** — mobile nav, fluid type scale, grids that collapse to
  single-column on small screens. Tested at 1440px and 390px widths.
- **Animations** — scroll-triggered reveals, a signature hand-drawn "thread" line
  motif, hero entrance choreography, testimonial slider, FAQ accordion, portfolio
  filter + lightbox. Everything respects `prefers-reduced-motion`.
- **SEO** — per-page titles/descriptions, Open Graph + Twitter cards, canonical
  tags, JSON-LD (LocalBusiness + ContactPage schema), `sitemap.xml`, `robots.txt`.
- **Vercel deployment config** — `vercel.json` with cache headers for static
  assets and basic security headers. Zero-config deploy (see below).

## Before you launch — replace these placeholders

This is a fully designed, fully functional site, but it ships with placeholder
business details and placeholder imagery that **must** be swapped before it goes
live:

| What | Where | Replace with |
|---|---|---|
| Phone number `+91 99000 00000` | footer (all pages), `contact.html` | Real studio number |
| Email `hello@knotandnarratives.com` | footer (all pages), `contact.html` | Real studio email |
| Address (Indiranagar, Bengaluru) | footer, `contact.html` | Real studio address |
| Map embed query | `contact.html` (`iframe src`) | Your real address in the `q=` parameter |
| Founder name "Kabir Anand" + team names | `about.html` | Real names |
| Instagram/Pinterest/YouTube/WhatsApp links | footer (all pages) | Real profile URLs |
| `SITE_URL` (`knotandnarratives.com`) | `/build/build.py`, `vercel.json`, `robots.txt`, `sitemap.xml` | Your real domain, then re-run the build (see below) or find-and-replace in the shipped HTML |
| All photography in `/images/gallery/` | every page | **Your real portfolio photos.** See note below. |

### About the images

Every image in `/images/gallery/` is an **original, generated abstract
composition** (soft gradients + bokeh, in the site's own colour palette) — not a
photograph of any real wedding, and not a stock photo. This was a deliberate
choice: hotlinking unrelated stock photography would have looked inauthentic on
a *photographer's own site*, and any real "sample" photos would misrepresent
someone else's work as his. They're production-safe (no copyright issues, no
broken-link risk) but they are placeholders. Swap them 1:1 for the photographer's
actual edited wedding photography — same filenames will slot right in, or update
the `src` attributes to new filenames.

### About the content

Story details (couple names, cities, choreography anecdotes) are illustrative
sample copy showing how the journal/portfolio *pattern* works. Replace with real
client stories (with permission) before launch.

### The contact form and client gallery are demos

- **Contact form** (`contact.html`): validates client-side and shows a success
  message, but doesn't actually send anywhere yet. Wire it up to one of:
  - [Formspree](https://formspree.io) or [Getform](https://getform.io) (form
    endpoint, no backend needed — swap the `<form>` action/JS fetch call)
  - A Vercel [serverless function](https://vercel.com/docs/functions) at
    `/api/contact` that emails you or writes to a database/CRM
- **Client Gallery** (`gallery.html`): the "enter your code" unlock is a
  front-end-only demo (code `DEMO2026`) for layout purposes — it is **not**
  secure authentication. For a real launch, either connect it to a gallery host
  (Pixieset, Pic-Time, ShootProof — most offer embeddable client galleries) or
  replace it with a proper backend-authenticated gallery.

## Local preview

```bash
npm run dev
# or: npx serve .
```

Then open `http://localhost:3000`.

## Deploying to Vercel

**Option A — Vercel dashboard (easiest):**
1. Push this folder to a GitHub repo.
2. Go to [vercel.com/new](https://vercel.com/new), import the repo.
3. Framework preset: "Other" (it's static — no build command needed).
4. Deploy. Done.

**Option B — Vercel CLI:**
```bash
npm i -g vercel
vercel        # preview deploy
vercel --prod # production deploy
```

Once deployed, add your custom domain in the Vercel dashboard, then update
`SITE_URL` everywhere listed in the placeholder table above so canonical URLs,
sitemap, and Open Graph tags point to the real domain.

## Editing content

There's no CMS — content lives directly in the HTML files, which is intentional
for a small business site like this (nothing to break, nothing to pay for).
Each page is self-contained; the shared header/footer are duplicated across
pages rather than templated at runtime, so search-and-replace across all `.html`
files when changing sitewide details (phone, email, social links).

If you'd rather edit from source templates: the `/build` folder (not part of the
deployed site) contains the original Jinja2 templates and `build.py` used to
generate these pages. Edit a template, run `python3 build.py`, and the HTML
regenerates. This is optional — editing the shipped HTML directly works fine too.

## Adding a new Stories post

Duplicate `story-single.html`, edit the content, and add a card for it on
`stories.html` linking to the new file. Add the new URL to `sitemap.xml`.

## File structure

```
/
├── index.html, portfolio.html, stories.html, story-single.html,
│   about.html, services.html, pricing.html, contact.html, gallery.html, 404.html
├── css/
│   ├── style.css        — design tokens, typography, base components
│   ├── components.css   — page-specific patterns (hero, pricing cards, etc.)
│   └── animations.css   — keyframes + the signature "thread" motif
├── js/
│   └── main.js           — nav, scroll reveals, sliders, filters, lightbox, forms
├── images/
│   ├── gallery/           — placeholder photography (see note above)
│   ├── favicon.svg, apple-touch-icon.png
├── manifest.json, robots.txt, sitemap.xml, vercel.json, package.json
└── build/                 — Jinja2 source templates + build script (optional, not deployed)
```

## Browser support

Modern evergreen browsers (Chrome, Safari, Firefox, Edge — last 2 versions).
Uses CSS Grid, `clamp()`, IntersectionObserver, and CSS custom properties, none
of which need polyfills for current browsers.
