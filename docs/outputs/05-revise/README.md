# Saved output for step 5: two real revisions

Both revisions below happened in the research projects on 6 October 2026. Neither was staged for the workshop.

## Revision 1: a safeguard that validated invented names (Tropical, person profiles)

**The problem.** Tropical's profile builder let a model supply a person's full given name and then checked that the name was "printed in the article". The check accepted an *initial* as evidence for a *full name*. Three probes run against the v1 code (tag `persons-v1-reviewed`, commit `6162893`):

| Proposed normalized name | Source text supplied | v1 result |
|---|---|---|
| James Watt | `Mr. J. Watt writes about tea.` | accepted as printed |
| Henry Trimen | `Mr. H. Trimen writes about tea.` | accepted as printed |
| John Smith | `Mr. John Smithson writes about tea.` | accepted as printed |

A diagnostic over the 2,216 expansions the documentation called "verified" found 50 whose first given name does not occur as a whole word anywhere in the article. One was `von Mueller` expanded to `Ferdinand von Mueller` in an article that prints only `Sir F. von Mueller`.

**The historian's reason.** A model that knows who "F. von Mueller" probably is has added outside knowledge to the record. That may be a correct identification, but it is not what the source says, and the two must be kept apart.

**The revision** (commit `acb5e9d`, "ner/persons v2"). The check now returns a status for the given names, and a printed initial supports only an initial:

| Proposed name | Source text | v2 result |
|---|---|---|
| James Watt | `Mr. J. Watt writes about tea.` | `initials` (J only) |
| Henry Trimen | `Mr. H. Trimen writes about tea.` | `initials` (H only) |
| John Smith | `Mr. John Smithson writes about tea.` | `none` |
| Henry Trimen | `Dr. Trimen ... HENRY TRIMEN. Royal Botanic Gardens` | `full` |

Across the corpus: 2,150 expansions are fully printed, 17 are supported only by initials, 889 are not printed at all. The 889 keep the model's identification in a separate hypothesis field. The three probes are now regression tests (`ner/persons/tests/test_persons.py`), so the defect cannot return silently.

## Revision 1b: a mixed profile is not one person (same commit)

**The problem.** The merge that produced the authority table said that a model verdict of MIXED, NONE or UNSURE leaves the Wikidata identifier empty. A later fallback filled any empty identifier from the Colonial Office List match regardless. Result in v1: `John Douglas` (P000704) and `William Taylor` (P000750), both explicitly judged by the model to combine two people, each left the pipeline with a single QID at "high" confidence.

**The historian's reason.** A valid identifier does not make a mixed profile valid. If the records belong to two people, asserting one identity is wrong for some of them, whichever identity is chosen.

**The revision.** A single identity gate (`ner/persons/identity.py`) now decides what a profile may *assert* and what stays a *candidate*. MIXED asserts nothing and is flagged for splitting; NONE and UNSURE keep the rule-based identifier as a candidate, flagged. Eight tests cover the gate, including the two v1 cases by name. Re-running the review's probe against the current output: zero rows carry a QID together with a NONE, MIXED or UNSURE verdict.

## Revision 2: an OCR reading that reversed the meaning (this workshop packet)

**The problem.** The exercise letter (S04) was marked "OCR read; visual check pending". Compared with the scan of page 66 on 6 October 2026, two sentences were wrong:

| OCR | Scan |
|---|---|
| and were now in a full condition and in flower. | and were growing in a bad situation and not robust. |
| I have by my prints of the leaves of some of the trees as well as the other that Mr. Moens had sent to be true Ledgerianas, | I have many plants from the seed of the specimen tree as well as the others that Mr. Moens declared to be true Ledgerianas, |

The first inverts the trees' condition. The second removes the fact that Agar holds seedlings from the illustrated tree, which is why he says the question "will be easy in the future to determine".

**What the model did with it.** Extraction run A flagged both sentences as uncertain readings and transcribed them as printed. It guessed that "in a full condition" might be "in full bloom" and that "by my" might be "by me". Both guesses were wrong. The flag was useful; the guesses were not. Only the page settles it.

**The revision.** The packet now keeps the OCR as delivered in `text` (that is what a model sees), adds a scan-checked `transcription`, and lists every change in `ocr_differences`, so the two can be compared. The rule that follows for the rest of the collection: an extracted record whose reading status is uncertain is not data until someone has looked at the page, and a model's guess at the intended wording is not a reading.

## Rerunning after a revision

After changing a rule, rerun the small batch and look at two things: the cases the change was meant to fix, and the previously accepted cases that changed. In the Tropical v2 rebuild, the second group was the larger one. A revision that only fixes the case in front of you has not been tested.
