# nourollah.me

Personal academic website of [Amir Masoud Nourollah](https://nourollah.me), Built with [Quarto](https://quarto.org/).

## Structure

```
.
├── _quarto.yml          # Site config: navbar, footer, theme, social cards
├── _theme/
│   ├── light.scss       # Navy & teal palette, light mode (fonts, colours)
│   ├── dark.scss        # Same palette, dark mode
│   └── site.html        # Shared JS: QR and slide-version popovers
├── styles.css           # Layout and components (hero, news, entries, pills, CV rows)
├── CNAME                # Custom domain; copied into docs/ on every render
├── index.qmd            # Home: intro, news, selected research, recent writing
├── about.qmd            # CV-style background, education, teaching, experience
├── assets/              # Profile photo, favicon, pre-generated QR codes (assets/qr/)
├── projects/            # "Research" page + per-project write-ups
├── _extensions/talk/    # Slide template (format: talk-revealjs): theme.scss, footer.html, logo
├── presentations/       # "Talks" page + decks; presentations/theme/showcase.qmd demos every component
├── blog/                # "Writing" listing + posts
└── docs/                # Generated site (served by GitHub Pages) — do not edit
```

## How It Works

Source files are [Quarto Markdown](https://quarto.org/docs/authoring/markdown-basics.html) (`.qmd`). `quarto render` compiles them into static HTML under `docs/`, which GitHub Pages serves.

The theme is Bootstrap `cosmo` overridden by `_theme/light.scss` and `_theme/dark.scss` (visitors get a light/dark toggle). Colours used in `styles.css` come from `--c-*` CSS variables defined in those two files, so change the palette there only.

### Adding a research entry or talk

Copy an existing `::: entry` block in `projects/index.qmd` or `presentations/index.qmd`. Action buttons are `{.pill}` links. For a QR button, generate a static SVG into `assets/qr/` (any QR tool) and add:

```html
<button type="button" class="pill" data-qr="/assets/qr/NAME.svg" data-qr-url="https://nourollah.me/..."><i class="bi bi-qr-code"></i>QR</button>
```

Only add QR codes for pages that exist.

### Making a new slide deck

Every deck uses the shared template. Front matter needs only:

```yaml
format:
  talk-revealjs:
    footer: "Short title for the footer"
```

See `presentations/theme/showcase.qmd` for every component (dividers, cards, `.key`, `.warn`, `.big-number`, `.columns .dense`, tables, closing slide). The website and slides share one palette: navy `#0B1F3A` for structure, teal `#0E6B6B` as the accent, amber `#B26B12` (slides only) for new or failing results. Add a line to **News** on the home page when something notable happens.

## Requirements

[Quarto](https://quarto.org/docs/get-started/) must be installed.

```bash
# macOS (Homebrew)
brew install quarto

# or download the installer from
# https://quarto.org/docs/get-started/
```

Verify your installation:

```bash
quarto --version
```

No other dependencies are required. There is no Node.js build step or package manager involved.

## Local Development

```bash
# Render the full site once
quarto render

# Render and serve with live reload
quarto preview
```

The preview server runs at `http://localhost:4848` by default and reloads on file changes.

## Deployment

The rendered output goes to `docs/` (set in `_quarto.yml`). GitHub Pages is configured to serve from the `docs/` folder on the `main` branch. To deploy, render and push:

```bash
quarto render
git add docs/
git commit -m "rebuild site"
git push
```

> **Note:** If GitHub creates a commit on the remote (e.g. when you update the custom domain in Pages settings), pull before pushing to avoid diverged histories:
> ```bash
> git pull --rebase
> git push
> ```

## Writing a Blog Post

Each post lives in its own folder under `blog/posts/`. The folder name becomes the URL slug.

**1. Create the post folder and file:**

```bash
mkdir -p blog/posts/my-post-title
```

**2. Create `blog/posts/my-post-title/index.qmd` with this front matter:**

```yaml
---
title: "Your Post Title"
description: "A one-sentence summary shown in the listing."
author: "Amir Masoud Nourollah"
date: "2026-05-12"
categories: [research]          # keep to 1–3 broad labels
image: "cover.jpg"               # optional thumbnail (keep under ~200 KB)
image-alt: "Describe the image"
draft: false                     # set to true to hide from listing
---

Your post content here, written in Markdown.
```

**3. Preview, render, and deploy:**

```bash
quarto preview            # live preview at localhost:4848
quarto render             # build the full site
git add blog/ docs/
git commit -m "add post: my-post-title"
git push
```

The post will appear automatically in the Blog listing — no manual index update needed.

