# Maintaining this series

`data/papers.json` is the source for the seven papers, their original English abstracts, Chinese translations, links, and sourced scholarly records.

Run `python scripts/build.py` to regenerate `index.html`, both README files, and the seven existing Markdown reading pages. The site is a static, single-column page. All abstracts remain visible without expanding panels or navigating to detail pages. English is readable without JavaScript; the small script only switches languages.

The public page uses `site-assets/ai-economics.css` and `site-assets/ai-economics.js`. There is no package installation or framework build. GitHub Pages can publish the `main` branch's root directory; `.nojekyll` keeps the HTML and assets unchanged. Configure that publishing source in the repository's Pages settings if it has not yet been enabled.

Paper links are limited to PDF, arXiv, and verified published versions. Poster and citation-download links are intentionally absent from the website, READMEs, and reading pages. Original material files remain available at their existing paths.

Keep original English abstracts faithful to the source. Mark Chinese text as a translation. Add publication, award, or presentation information only when a specific source supports it, and distinguish conference programmes from formal publications.
