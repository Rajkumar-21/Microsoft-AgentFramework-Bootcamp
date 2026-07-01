# Agent Framework Bootcamp — Site

A simple, self-contained static site (plain **HTML + CSS + JS**, no build step) for the
Microsoft Agent Framework Bootcamp. Designed to deploy to **GitHub Pages** as-is.

## Preview locally

Just open `index.html` in a browser — no server or install required.

Optionally, serve it (so relative paths behave exactly like Pages):

```bash
# from the repo root
python -m http.server 8080 --directory site
# then visit http://localhost:8080
```

## Structure

```
site/
  index.html            # landing page
  <lesson>.html         # one file per lesson (flat — links are just "<id>.html")
  assets/
    styles.css          # design system (light/dark, layout, components)
    app.js              # injects navbar/sidebar/TOC/pager + theme, search, copy, mermaid, hljs
  .nojekyll             # tell Pages to serve files verbatim
```

External libraries load from CDN: [highlight.js](https://highlightjs.org/) (code) and
[mermaid](https://mermaid.js.org/) (diagrams). The dark/light theme is remembered in
`localStorage` and applied before paint to avoid a flash.

## Add a lesson

1. Add an entry to the `NAV` manifest in `assets/app.js` (id + title under the right section).
2. Create `site/<id>.html` using the same `<head>`/script boilerplate as an existing lesson,
   with empty `#navbar`, `#sidebar`, `#toc` mount points and your content inside
   `<article id="doc" class="prose">`.

The navbar, sidebar, right-hand table of contents, and prev/next pager are generated
automatically from the manifest.

## Deploy to GitHub Pages

A workflow at `.github/workflows/pages.yml` publishes the `site/` folder on every push to
`main`. **One-time setup:** in the repo, go to **Settings → Pages → Build and deployment**
and set **Source = GitHub Actions**. After the next push, the site is live at
`https://<owner>.github.io/<repo>/`.
