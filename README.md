# Cleaning and Structuring Historical Data: A Working Session

Materials for a one-hour workshop at the AI and History Conference, Johns Hopkins University, Thursday 15 October 2026 (1:30–2:30 p.m., Room 110, SNF Agora Institute; streamed on Zoom). Presenter: Jim Clifford, University of Saskatchewan.

The session shows how historians can delegate substantial data work to models and coding agents (proposing a structure, extracting records, writing the processing code, retrieving candidate identities, preparing evidence for review) while keeping the decisions that require historical judgment. The worked example follows Henry Trimen, Director of the Royal Botanic Gardens at Peradeniya, from the *Colonial Office List* into an 1883 dispute in *The Tropical Agriculturist* about a cinchona tree.

**Status: draft for review.** Everything here was prepared on 6 October 2026. The scan checks and pipeline facts stated on the pages were verified; the prompts, running order and case selection are proposals.

## Layout

| Path | What it is |
|---|---|
| `index.qmd`, `steps/*.qmd`, `answers.qmd`, `presenter.qmd`, `setup.qmd`, `packet.qmd` | The participant site (Quarto). Rendered to `docs/` for GitHub Pages |
| `slides.qmd` | The slide deck (reveal.js), rendered to `docs/slides.html`; speaker notes in the source |
| `images/` | Scan crops used on the slides (archive.org, public domain) |
| `review/` | The browser exercise: `index.html` + `cases.json`. Static; no account or API key needed |
| `source-pack/` | OCR text of the six passages, the scan-checked transcription of the exercise letter, Trimen's Colonial Office List entries, citations with page links |
| `outputs/` | Saved outputs for every stage: structure proposals, extraction runs, candidate evidence, the two real revisions, Trimen across collections |
| `research/trimen-network/` | The wider research packet: 49 entities, 14 attributed claims, 25 catalogued letters, cached Wikidata responses. All human-review fields pending |
| `scripts/` | Build scripts. All run offline except `ground_trimen.py`, which fetches and caches Wikidata evidence |
| `workshop-plan.md` | The working plan for the session |
| `tropical-project-review-2026-10-06.md` | Technical review of the Tropical pipeline that informed the case selection, with a postscript on what changed the same day |

## Building the site

```bash
quarto render
```

Output goes to `docs/`, which GitHub Pages serves at https://jimclifford.ca/trimen-workshop/ (branch `main`, folder `/docs`). Commit the rendered `docs/` with the source changes. The `docs/.nojekyll` file tells GitHub to serve the files as rendered.

## Rebuilding the data

```bash
python3 scripts/build_trimen_workshop.py
python3 scripts/build_candidates.py
python3 scripts/build_source_pack.py
python3 scripts/build_review_cases.py
```

## Sources and credits

Passages are from *The Tropical Agriculturist* (Colombo), scans on archive.org (`tropicalagricult1188ceyl`, `tropicalagricult18831884colo`), OCR text from the [Tropical Agriculturist project](https://github.com/jburnford/tropical-agriculturist). Colonial Office List entries and career graph from [Imperial Careers / col_matching](https://github.com/jburnford/col_matching). Wikidata evidence retrieved through the [WikidataMCP](https://wd-mcp.wmcloud.org/) server and Wikidata's entity data endpoint. Modern plant-name treatments from Kew's Plants of the World Online.

Extraction runs in `outputs/` were produced by Claude models in Claude Code on 6 October 2026 from the prompts recorded with them; each run's folder names the model used.
