# nourollah.me

Personal academic website of [Amir Masoud Nourollah](https://nourollah.me), Built with [Quarto](https://quarto.org/).

## Structure

```
.
├── _quarto.yml          # Site configuration (theme, navbar, output dir)
├── index.qmd            # Home page (profile, bio, research summary)
├── about.qmd            # About page (education, experience, contact)
├── styles.css           # Custom CSS (colours, layout tweaks, icon fixes)
├── assets/              # Static assets (profile image, etc.)
├── blog/
│   ├── index.qmd        # Blog listing page (auto-populated)
│   └── posts/
│       └── hello/
│           └── index.qmd  # Example post
├── presentations/
│   ├── index.qmd        # Presentations listing
│   └── annual-review-2025/
│       └── index.qmd    # RevealJS slide deck
├── projects/
│   ├── index.qmd        # Projects listing
│   └── mlip-benchmark/
│       └── index.qmd    # Project page
└── docs/                # Generated site output (served by GitHub Pages)
```

## How It Works

Source files are written in [Quarto Markdown](https://quarto.org/docs/authoring/markdown-basics.html) (`.qmd`). Running `quarto render` compiles them into static HTML under `docs/`, which is the directory served by GitHub Pages.

The site uses the built-in Quarto `cosmo` Bootstrap theme, extended with a custom `styles.css`. Icons come from [Bootstrap Icons](https://icons.getbootstrap.com/) (bundled by Quarto). Icons not included in Bootstrap Icons (ORCID, ResearchGate) are rendered via SVG `mask-image` in `styles.css` so they inherit the site's colour scheme.

Presentation slides use the Quarto RevealJS format.

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
categories: [research, tools]   # optional — any labels you like
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

