# Maintaining this series

`data/papers.json` is the source for the seven papers, their original English abstracts, Chinese translations, links, and sourced academic records.

Run `python scripts/build.py` to regenerate `index.html`, both README files, and the seven existing Markdown reading pages. The static homepage follows a research-thread structure inspired by the [Distill Circuits overview](https://distill.pub/2020/circuits/): a compact masthead, a title and research question, an author metadata band, a narrow reading column, and numbered paper entries separated by fine rules. The implementation and writing are specific to this series; no Distill identity or publication status is implied.

All abstracts remain visible without expanding panels or visiting detail pages. English is readable without JavaScript; the small script only switches languages. The desktop number gutter becomes an inline number on small screens. Navigation links jump directly to papers, awards and activities, or contact details.

## Awards and academic activities

The `recognition` array on each paper holds an award, conference activity, or publication record. Each record includes `kind`, a supported date and bilingual `date_label`, concise `en` and `zh` labels, bilingual `detail`, a source `url`, and a bilingual `source_label`. An optional `links` array provides additional supporting material. A year-only date is permitted when a more precise date has not been verified.

The homepage and both READMEs place a compact, three-item summary immediately after the introduction and before the papers. `recognition_highlights()` in the generator groups the award, the two UNU conference records, and the CADE publication; source links come from the original records. Update this bilingual summary when new records are added. Short records remain near each relevant paper title, and the individual reading pages preserve full details. Add records only when a specific source supports them, and distinguish an award, a conference programme listing, and a formal publication. Keep a different conference presentation title explicit instead of implying that it is the arXiv title.

`proceedings_url` adds a verified conference proceedings link alongside a paper's PDF and arXiv links. Original English abstracts must remain faithful to the source; label Chinese text as a translation.

## Publishing

The public page uses `site-assets/ai-economics.css` and `site-assets/ai-economics.js`. There is no package installation or framework build. GitHub Pages can publish the `main` branch's root directory; `.nojekyll` keeps the HTML and assets unchanged. Configure that publishing source in the repository's Pages settings if it has not yet been enabled. GitHub's README renderer does not apply the website stylesheet.

The generator adds a content hash to the stylesheet URL so that published layout changes refresh browser caches automatically. Run the generator after editing CSS as well as paper data.

Poster and citation-download links are intentionally absent from the website, READMEs, and reading pages. Original material files remain at their existing paths.
