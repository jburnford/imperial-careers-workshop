# Cleaning and Structuring Historical Data: A Working Session

Materials for a one-hour workshop at the AI and History Conference, Johns Hopkins University, Thursday 15 October 2026 (1:30–2:30 p.m., Room 110, SNF Agora Institute; streamed on Zoom). Presenter: Jim Clifford, University of Saskatchewan.

The session follows one dataset from printed source to animated atlas: the *Colonial Office List* and *India Office List* as processed by the [Imperial Careers](https://github.com/jburnford/col_matching) project (46,926 officials, 305,164 dated career events, places grounded to Wikidata). It shows what a coding agent and a cheap model did at scale, where the historian had to decide something, and how the visualization became the error detector that drove fixes back through the pipeline.

**Status: draft for review.** Updated on 8 October 2026 on the Imperial Careers example; the earlier draft on *The Tropical Agriculturist* is in `archive/tropical/`. The worked atlas errors are completed corrections, with dated before evidence and a rebuilt result.

## Layout

| Path | What it is |
|---|---|
| `index.qmd`, `steps/*.qmd`, `answers.qmd`, `presenter.qmd`, `setup.qmd`, `handout.qmd` | The participant site (Quarto). Rendered to `docs/` for GitHub Pages |
| `slides.qmd` | The slide deck (reveal.js), rendered to `docs/slides.html`; speaker notes in the source |
| `media/combined-mobility.webm` | WebM playback fallback, converted from the Imperial Careers opening MP4 |
| `annotate/` | The mark-up exercise: tag positions, places, years and honours in an entry, then compare with the pipeline. Static |
| `review/` | The decision exercise: three core accept/reject/unresolved decisions with reasons, plus five further cases. Static |
| `outputs/` | Saved outputs: prompt, audit, merge rules and clusters, grounding cache rows, the twenty-entry grounding test with the Gemini control, project review, stats |
| `source-pack/` | Trimen's seven Colonial Office List entries |
| `scripts/build_review_cases.py` | Builds `review/cases.json` offline |
| `archive/tropical/` | The 6 October draft and its materials |

## Building the site

```bash
quarto render
touch docs/.nojekyll
```

Output goes to `docs/`, which GitHub Pages serves at https://jimclifford.ca/imperial-careers-workshop/ (branch `main`, folder `/docs`). `quarto render` deletes `docs/.nojekyll`; recreate it before committing.

## Sources and credits

Entries are from the *Colonial Office List* (OCR by the Imperial Careers project). Graph data, method documents, audits and grounding caches from [Imperial Careers / col_matching](https://github.com/jburnford/col_matching) (data CC0, code MIT). Wikidata evidence retrieved through the [WikidataMCP](https://wd-mcp.wmcloud.org/) server and Wikidata's `wbgetentities` API on 7 October 2026. The Gemini 3.8 Flash response in `outputs/ground-test/` was produced by Jim Clifford on 7 October 2026.

The video slide uses the public Imperial Careers MP4 with a local WebM fallback for browsers without H.264 decoding. The still image is the video poster; it must not be configured as a competing Reveal background image.
