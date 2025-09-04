# Surfing the Data Pipeline

Files used to compile the web-based textbook "Surfing the Data Pipeline with Python" by Jonathan Kropko.

## Build Locally

- Create a new environment: `uv init`
- Install Jupyter Book: `uv add jupyter-book`.
- Install notebook dependencies: `uv add -r requirements.txt`.
- Build the site: `uv run jupyter-book build .` (outputs to `_build/html`).
- Publish to GitHub Pages: (FIXME - set up GitHub Actions).