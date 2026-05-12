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
