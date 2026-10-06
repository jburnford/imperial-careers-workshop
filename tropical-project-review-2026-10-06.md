# Tropical project review — 6 October 2026

Tropical is a substantial working research pipeline with unusually useful evidence for a workshop about delegation and human judgment. It has already completed extraction, profile building, three kinds of external matching, and a model adjudication pass. **The pending RA task is an evaluation of those results, not unfinished extraction.** The main remaining weakness is that the software prepares human review but does not yet complete the return path from human decisions to evaluated and corrected outputs.

This was a read-only review of a local checkout of the Tropical Agriculturist repository at commit `61628939a0682c99b6c2926436da04c6472bf28e`. The tracked working tree was clean before and after inspection. I inspected documentation, scripts, compressed outputs, the generated review page, and matching/adjudication tables; counted records and reproduced a small evidence-check defect using the existing function in isolation. I did not perform the RA's judgments, rebuild the corpus or profiles, change Tropical, query external services, or run GPU/model pipelines. The browser interface was inspected as source and embedded data, not through an interactive browser session. Claims below concern this local snapshot, not an independently checked live deployment.

## Current state and the RA handoff

| Component | State observed |
|---|---|
| Article corpus | 54,764 records in the per-year files, of which 53,501 are canonical. This agrees with `articles/README.md`, not the root README's older count. |
| Extraction | Documentation reports 53,053 processed articles, 1,054,564 extracted entity records and three chunk errors. The person table contains 150,754 records with unique `(article, idx)` pairs. |
| Person profiles | 38,590 profiles: 30,541 named and 8,049 surname pools. These are proposed groupings, not 38,590 verified historical individuals. |
| Wikidata first pass | 1,860 profiles with at least ten extracted person records: 199 auto, 552 review, 1,109 none. |
| Model adjudication | 690 profiles reviewed by models: 230 LINK, 380 NONE, 49 MIXED, 31 UNSURE. These are not human verdicts. |
| Colonial Office List | 314 auto and 167 review matches. |
| Planters registry | 157 link and 142 review matches. |
| Combined output | 470 profile rows have QIDs. Thirty-nine rows share a QID with another row, across 19 QIDs; two rows are flagged as nonhuman items. |
| RA sample | 100 profiles, stratified by original Wikidata decision: 35 auto, 35 review, 30 none; four sampled records per profile, 400 total. All tracked verdict fields are blank. |

The human-facing artifact is the generated person review page (`ner/persons/gold/review/index.html`). Its instructions ask the RA to assess whether a profile combines one or several people, find or verify the Wikidata identity, and assess each sampled record. It saves answers in browser local storage and exports a TSV to send to Jim. At the page's stated three to five minutes per profile, this is approximately five to eight hours of review, potentially longer for difficult cases. See instructions and export behavior (`ner/persons/gold/review_template.html:69`).

The generated page's proposed QIDs agree with the current `persons.tsv` for all 100 sampled profiles. That is a useful consistency check. Blank tracked fields establish that results have not been incorporated here; they do not establish whether the RA has already saved work in their browser or elsewhere.

The intended sequence is:

`extracted records → profiles → candidate matching/model adjudication → RA sample → measured errors → reviewed corrections and revised rules → fresh validation`

The last three steps need an explicit implementation and protocol.

## Priority findings

### 1. Confirmed: the merge assigns identities to profiles marked mixed

The merge's stated rule (`ner/persons/combine.py:8`) says adjudicated NONE, UNSURE and MIXED leave the QID empty. However, the Colonial Office fallback (`ner/persons/combine.py:85`) fills any empty QID, regardless of the adjudication decision. It adds conflict flags for NONE/MIXED but not UNSURE.

This affects current output, not just a hypothetical branch:

- John Douglas, P000704 (`ner/persons/out/persons.tsv:705`): the model explicitly identifies a mixed profile, but the final row has Q3181373 with `high` confidence.
- William Taylor, P000750 (`ner/persons/out/persons.tsv:751`): explicitly mixed, but the final row has Q16466628 with `high` confidence, plus Colonial Office and planter links.
- E. B. Denham, P000175 (`ner/persons/out/persons.tsv:176`): UNSURE becomes a high-confidence Colonial Office QID without a conflict flag. This may be a defensible proposed match, but the override policy contradicts the stated rule.

**Recommendation:** make profile purity a gate for all asserted identity links. Preserve candidate links on mixed profiles, but do not treat the entire profile as one external person. Require an explicit resolution rule or human decision before overriding negative/uncertain decisions, recording the change and its evidence. Fix this in a new version after preserving the RA's current evaluation snapshot. A valid QID does not make a mixed profile valid.

### 2. Confirmed: the “printed in the article” check can validate invented expansions

`printed()` (`ner/persons/build_profiles.py:91`) accepts a full given name **or its initial** for every model-supplied given name, then preserves the expanded name. It also lacks adequate surname boundaries. Isolating the existing function reproduced:

| Proposed normalized name | Supplied source text | Existing result |
|---|---|---|
| James Watt | `Mr. J. Watt writes about tea.` | Accepted as printed |
| Henry Trimen | `Mr. H. Trimen writes about tea.` | Accepted as printed |
| John Smith | `Mr. John Smithson writes about tea.` | Accepted as printed |

This contradicts the documentation's description of 2,216 “verified” expansions (`ner/persons/README.md:35`). A diagnostic over the 2,216 `norm` records found 50 whose first substantial normalized-name token does not occur as a complete word anywhere in the article. This is a screening count, **not** a count of wrong identities: a correct identity can still have unsupported source wording. One concrete case is `von Mueller → Ferdinand von Mueller` in article `vol002_tropicalagricult18821883colo#1883-05#121`, which prints `Sir F. von Mueller` without “Ferdinand.”

**Recommendation:** preserve the strongest name actually supported by the source; keep expanded identities in a separate hypothesis field. Require token boundaries and evidence for each full-name expansion. Test both the positive case and the misleading-initial/prefix cases, then report which profiles and links change. This is an excellent workshop example of a plausible safeguard that still needs human scrutiny.

### 3. Confirmed workflow gap: RA exports are not yet consumed downstream

The review UI exports `person` and `mention` rows with `gid`, `pid`, article, choices, notes and timestamps (export schema (`ner/persons/gold/review_template.html:214`)). I found no corresponding importer, evaluator or human-override application in the inspected project. The merge inputs (`ner/persons/combine.py:4`) include model adjudication files, but no human-review file.

The label `adjudicated` in the current authority output means model adjudication. It should not be read as a human certification.

**Recommendation:** implement a separate, versioned import and evaluation step before using the RA results operationally. It should validate row identities, preserve the original export, distinguish unfinished from uncertain judgments, report errors by stage, and prepare proposed corrections. Keep measurement separate from application: a wrong sampled mention may require splitting a profile, not replacing its QID. Retain author, date, evidence and human/model provenance for every applied decision.

### 4. Confirmed handoff risk: changing the sample can misassociate saved answers

The page uses a fixed local-storage key, `tap_gold_v1`, and keys answers by `G001` etc. and ordinal mention index (storage code (`ner/persons/gold/review_template.html:103`)). Import uses these keys without checking the exported `pid` or article against the current data (import code (`ner/persons/gold/review_template.html:231`)). A regenerated page can therefore attach old judgments to different material. Profiles themselves receive rank-based PIDs on rebuild (assignment (`ner/persons/build_profiles.py:332`)).

Additionally, `make_gold.py` overwrites the gold TSVs and does not produce fully reproducible mention samples across ordinary Python processes: it seeds the RNG but iterates an unordered set of PIDs while shuffling (sampling (`ner/persons/gold/make_gold.py:31`)).

**Recommendation now:** freeze the page, input tables and commit while the RA works. Ask for an exported backup at each work session through the existing handoff process. For the next version, include a dataset fingerprint in exports and storage keys, reject mismatched imports, sort sampling iteration, and use stable record identifiers with the original extraction index. Do not regenerate the RA's live assignment to incorporate workshop changes.

### 5. Confirmed review limitations: source navigation and candidate provenance

The gold builder (`ner/persons/gold/make_gold.py:49`) always supplies the **first page of the article** as the scan link. In the current sample, 294 of 400 records come from multipage articles. This does not mean all 294 links are wrong, but they are article-entry links, not located evidence. Seventeen snippets explicitly say `(surface not found in text)`. Fallback matching searches the last word and highlights the original surface's length, which can highlight unrelated text (snippet code (`ner/persons/gold/make_gold.py:55`)).

The review builder also inserts any final QID missing from first-pass candidates with the description “from the Colonial Office List graph,” regardless of its actual source (candidate construction (`ner/persons/gold/make_review_site.py:40`)). Three current proposed items lack labels: John Ferguson, R. V. Norris and E. F. Smith. Colonial Office `review` matches are displayed without an explicit candidate status; C. H. Collins is a current example (display construction (`ner/persons/gold/make_review_site.py:50`)).

**Recommendation:** give the RA a route to the complete article and all its page images; identify the exact passage/page where available and clearly label missing or approximate matches. Show actual candidate provenance and status. Preserve the already-issued snapshot and issue any clarifying instructions separately until its version is settled.

## What the RA evaluation can establish

The sample is useful for finding errors and estimating first-pass auto-link precision in the high-frequency tranche. Its design has limits:

- The 35/35/30 strata deliberately oversample auto/review cases relative to the 199/552/1,109 population. An unweighted percentage across all 100 is not overall pipeline accuracy. Report separate strata and uncertainty; use population weights only for a clearly defined aggregate estimand.
- The sample excludes profiles below ten records and people never extracted or left unassigned. It cannot estimate extraction recall or validate the entire authority file. Colonial Office matching reaches three-record profiles and planters matching two-record profiles, so these lower-frequency links need separate coverage.
- The four records deliberately favor different inference methods. They are a diagnostic sample, not a random sample of all mentions. Four correct examples cannot establish that hundreds of records in a large profile all refer to one person.
- The page hides the original decision bucket but shows a highlighted proposed answer. That is assisted verification, not fully blinded independent identification. A small second-reviewer subset or source-first pass would help measure ambiguity and anchoring without duplicating the whole assignment.
- The first-pass, model-adjudicated and final merged decisions differ. Evaluate these separately against the RA answers; do not attribute improvements to the wrong stage.
- “Not in Wikidata (I searched)” should be interpreted as no supported match found through the recorded search, not proof of absence. Keep “can't tell” separate from rejection and record useful search evidence.

After using this sample to revise rules, treat it as development evidence and check a fresh held-out sample before claiming improved general accuracy.

## Other methodological and reproducibility points

**“Mentions” are not occurrence counts.** The extraction prompt (`ner/extract_entities.py:17`) asks for one representative surface per distinct entity per chunk, even when repeated many times. The 150,754 person records and profile frequencies therefore measure chunk-level extracted presence, not every printed occurrence. Chunk size differs for table-heavy text, and failed chunks can be subdivided. Explain this before making frequency comparisons or presenting the corpus as having found “every person named.” Prefer article prevalence when that matches the research question, and label the unit precisely.

**Co-occurrence is not a historical relation.** The profile's places and estates aggregate all such entities in each article (profile construction (`ner/persons/build_profiles.py:282`)). These are useful search clues but do not establish residence, employment, ownership or travel. The review UI's “Places nearby” wording helps, but subsequent claims must still require local evidence.

**Wikidata checks need bounded claims.** The pipeline usefully separates candidate search from statement reads and uses dates, names and occupations. However, the retrieved fields (`ner/persons/wd/ground_wikidata.py:145`) use simplified values: minimum birth/death years, English labels/aliases, occupations and a sampled sex value, without statement references, ranks or qualifiers. Candidate retrieval can miss aliases before checking because the label must contain the surname. A “none” outcome can be a search limitation. Cached data are valuable for a workshop, but a reproducible release should record retrieval time, query/service versions and evidence identifiers.

**Agreement between data sources is supporting evidence, not independent ground truth.** Sixteen shared auto matches agree between Wikidata and the Colonial Office KG, but the latter already contains Wikidata links. Verify source-specific evidence and upstream provenance; do not report their agreement as an independent accuracy estimate.

**Stable IDs need stable lineage.** The registry (`ner/persons/combine.py:54`) inherits identifiers by surname and article-set Jaccard overlap. That is helpful continuity machinery but cannot by itself represent a split, merger or changed historical identity. Both article IDs and profile PIDs are build-local. Before rebuilding after review, preserve old-to-new mappings and explicit split/merge decisions. `same_qid_as` should remain a review flag: an incorrect shared QID can create false duplicates.

**Documentation needs a short current-state entry point.** Root README says the corpus is absent and later says it is backed up there; it reports 54,259 canonical articles, while the current files contain 53,501 (root README (`README.md:6`), article documentation (`articles/README.md:8`)). The person README says 1,869 high-frequency profiles; current output has 1,860. `ner/README.md` still says the gazetteers have not been used, and `RERUN_PLAN.md` is historical despite its opening “Nothing below has been done yet.” Also, `parse.py`'s “test cases” print examples without assertions (test block (`ner/persons/parse.py:264`)); successful execution is not a regression-test pass.

## Recommended next steps

**While waiting for the RA:** preserve the current evaluation snapshot and review exports; document what the RA is assessing and how uncertain/mixed cases should be recorded; prepare the importer and evaluation specifications; reproduce the two confirmed identity/evidence defects in isolated regression tests; select workshop cases from a separate frozen copy. Keep model decisions and RA decisions explicitly distinct.

**When the RA returns results:** validate the export against the frozen dataset; summarize original decisions and errors by stratum and resolution method; discuss ambiguous cases with the RA; implement documented corrections and rule changes in a new version; rebuild affected downstream outputs with lineage retained; evaluate on fresh cases. Do not silently convert MIXED into a single-identity override.

**For the conference workshop:** this project is ready to supply realistic post-OCR material and a model-assisted workflow. Use three to five small, self-contained cases: a supported match, a plausible wrong candidate, a name expansion unsupported by the text, and a mixed/unresolved profile. Show the agent performing extraction, candidate retrieval and evidence-table preparation; let participants identify a consequential error; then show how that judgment changes processing and a fresh result. Keep saved model/tool outputs beside live demonstrations. The full RA assignment is too large for the workshop and should remain a research evaluation, not a classroom completion task.

The workshop repository should be small and independent: selected OCR text, source/page references, cached candidate evidence, prompts, original/revised outputs, a short review exercise and worked answers. The local Tropical repository has roughly 738 MB of Git history and 898 MB in `output_v6` alone, so requiring a full clone would add avoidable friction. No ontology conversion or CIDOC-CRM is needed to demonstrate the central lesson: models can do substantial work, but evidence interpretation and the rules for accepting identities remain research decisions.

## Reproducing the two confirmed defects without rebuilding

Run from the root of a Tropical checkout at the reviewed commit. This reads existing data and executes only the isolated `printed()` function; `-B` disables bytecode writes. It does not import or run the profile-building pipeline.

```bash
python3 -B - <<'PY'
import ast, csv, pathlib, re, sys
p = pathlib.Path('ner/persons')
with (p / 'out/persons.tsv').open() as f:
    for r in csv.DictReader(f, delimiter='\t', quoting=csv.QUOTE_NONE):
        if r['wikidata_qid'] and re.search(r'adjudicated (NONE|MIXED|UNSURE)', r['note']):
            print(r['pid'], r['display'], r['wikidata_qid'], r['qid_confidence'], r['flags'])
sys.path.insert(0, str(p))
from parse import parse
tree = ast.parse((p / 'build_profiles.py').read_text())
fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'printed')
scope = {'re': re}
exec(compile(ast.Module(body=[fn], type_ignores=[]), '<isolated printed>', 'exec'), scope)
for name, source in [
    ('James Watt', 'Mr. J. Watt writes about tea.'),
    ('Henry Trimen', 'Mr. H. Trimen writes about tea.'),
    ('John Smith', 'Mr. John Smithson writes about tea.'),
]:
    print(name, repr(source), scope['printed'](parse(name), source))
PY
```

Expected in this snapshot: the three rows identified above, followed by `True` for all three source-evidence probes.

## Postscript, later on 6 October 2026

Tropical moved three commits past the snapshot reviewed above (`61628939`, now tagged `persons-v1-reviewed`). The findings stand as a record of v1; the state they describe has changed:

- `acb5e9d` (ner/persons v2) fixes findings 1 and 2. A printed initial no longer validates a full-name expansion (2,150 full / 17 initials only / 889 not printed, against v1's "2,216 verified"); a new identity gate (`identity.py`) ensures MIXED, NONE and UNSURE never become an asserted QID, and MIXED also withholds Colonial Office List and planter ids. The review's three probes are regression tests; 59 tests pass. Re-running the probe in this document against the new output finds no row with a QID and a NONE/MIXED/UNSURE verdict.
- The same commit addresses findings 3, 4 and 5: `score_gold.py` validates an RA export against a dataset fingerprint before scoring, preserves the export, and reports by stage and stratum with Wilson intervals; gold sampling iterates in sorted order with per-profile seeds; scan links go to the located page (386 exact, 12 loose, 2 surname-only of 400); candidate provenance is shown as recorded.
- `7e48d98` freezes the RA gold set (fingerprint `14a933f83ec5`, sampled at `acb5e9d`) and its review page.
- `ecef23b` changes the per-record rating from yes / no / can't tell to a 1–5 certainty scale, after the freeze. If the RA received the earlier page, confirm which version they are using before they begin; the fingerprint check will correctly reject an export from a different version.

The workshop materials use these commits as the "revise the process" example: a real before and after with tests, rather than a hypothetical.
