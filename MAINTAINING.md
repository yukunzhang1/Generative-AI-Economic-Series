# Maintaining this series

`data/papers.json` is the source for paper titles, arXiv identifiers, summaries, original abstracts, poster paths, and sourced recognition records. Keep the original poster filenames available to preserve existing links.

Run `python scripts/build.py` to rebuild the bilingual README, seven Markdown reading pages, and `CITATION.bib`.

To update the academic website at the same time, use:

```sh
python scripts/build.py --site-root /path/to/yukunzhang1.github.io
```

The website export creates the series overview, seven detail pages, citation download, and shared CSS/JavaScript. Commit the generated changes in both repositories. Website navigation and the homepage entry are maintained in the website repository.

Only add a publication, award, or presentation label when a specific source supports it. Conference programme listings are distinct from archival publication. Citation entries identify arXiv versions by their original posting year; publisher citations should be obtained from the publication record.

The older relationship diagrams remain available for existing links. The current overview describes thematic connections rather than formal dependencies between models. Add code or dataset download links only when the materials are publicly available.
