# Maintaining this series

`data/papers.json` is the source for the seven papers, their original English abstracts, Chinese translations, links, and sourced academic records.

Run `python scripts/build.py` to regenerate `index.html`, both README files, and the seven existing Markdown reading pages. The static homepage shares the [LLM Paper Series](https://yukunzhang1.github.io/research/llm-paper-series/) visual language: a warm off-white background, muted rose typography, a compact introduction, and paper rows with a research figure on the left and the title, academic records, full abstract, and links on the right. On small phones each row becomes one column.

All abstracts remain visible without expanding panels or visiting detail pages. English and image links work without JavaScript. The script adds the language toggle (preserving the `ge-language` preference) and a keyboard-accessible figure dialog. Header links connect the personal homepage, AI Agent Economics, and LLM Paper Series. Existing paper and research-theme anchors remain valid.

## Research figures

`data/figures.json` records one existing research figure per paper, its accessible description, original dimensions, and source provenance. Figures are extracted from research posters already in this repository; each record includes the source file's Git blob SHA, PDF page, and image xref. The files in `site-assets/images/` preserve each complete figure, with WebP compression only. Do not generate or redraw research results. The figure dialog links to the associated paper; it does not claim that the image was extracted from the current arXiv PDF.

## Awards and academic activities

The `recognition` array on each paper holds an award, conference activity, or publication record. Each record includes `kind`, a supported date and bilingual `date_label`, concise `en` and `zh` labels, bilingual `detail`, a source `url`, and a bilingual `source_label`. An optional `links` array provides additional supporting material. A year-only date is permitted when a more precise date has not been verified.

The homepage and both READMEs integrate short award, conference, and publication links immediately below each relevant paper title, before its abstract. There is no separate awards section or navigation item. The individual reading pages preserve full details. Add records only when a specific source supports them, and distinguish an award, a conference programme listing, and a formal publication. Keep a different conference presentation title explicit instead of implying that it is the arXiv title.

`proceedings_url` adds a verified conference proceedings link alongside a paper's PDF and arXiv links. Original English abstracts must remain faithful to the source; label Chinese text as a translation.

## Publishing

The public page uses `site-assets/ai-economics.css` and `site-assets/ai-economics.js`. There is no package installation or framework build. GitHub Pages can publish the `main` branch's root directory; `.nojekyll` keeps the HTML and assets unchanged. Configure that publishing source in the repository's Pages settings if it has not yet been enabled. GitHub's README renderer does not apply the website stylesheet.

The generator adds content hashes to the stylesheet and script URLs so that published changes refresh browser caches automatically. Run the generator after editing CSS, JavaScript, figures, or paper data.

Poster and citation-download links are intentionally absent from the website, READMEs, and reading pages. Original material files remain at their existing paths.
