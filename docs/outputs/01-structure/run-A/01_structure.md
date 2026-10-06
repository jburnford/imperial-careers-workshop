# Proposed table structure: people and activities in the Tropical Agriculturist passages

One flat table, one row per record. `record_type` is `person`, `plant` (trees, seedlings, cuttings, seed, plant groups), `sample` (bark, leaf prints, analyses) or `action` (a relationship or event linking two other records). Rows link to each other by local identifiers of the form `S04-P01` (source, type letter, number): P person, T plant, B sample, A action. No Wikidata or other external identifiers are used at this stage.

## Fields

| Field | Rationale |
|---|---|
| `record_id` | Local identifier, unique across both passages (source + type letter + number). |
| `record_type` | Lets people, plants, samples and actions sit in one sortable table. |
| `material_kind` | Tree, seed, cutting, bark, leaf prints, etc., for plant and sample rows. |
| `source_id`, `source_ref` | Passage code (S03, S04) and journal reference (The Tropical Agriculturist, July 1883, page). |
| `locator` | Line of the OCR text file, so each row can be checked against the source. |
| `printed_text` | Verbatim span(s) supporting the row, OCR wording kept; the script checks each span against the text. |
| `printed_name` | Name or label exactly as printed (titles and initials kept; nothing expanded). |
| `role_as_printed` | Title or role only where printed (e.g. "Dr.", "F. R. S."). |
| `place_as_printed`, `date_or_age_as_printed` | Places, dates and ages in the printed form. |
| `stated_detail` | Short statement of what the text says about the entity or event, close to the printed wording. |
| `subject_id`, `verb_as_printed`, `object_id`, `recipient_id` | For actions: who/what, the printed verb phrase, what it acts on, and who received it. Blank when the text does not say. |
| `asserted_by` | Who makes the claim (letter-writer, quoted correspondent, or quoted report), since the passages are arguments and not neutral records. |
| `reading_status`, `reading_note` | `clear` or `uncertain`, with the reason (OCR slips, garbled sentences). |
| `inferred_same_as` | Possible identity with a record in the other passage. Kept apart from the printed name because the texts do not state it. |
| `inferred_note` | Anything supplied by the reader rather than the text (who "he" is, what "S." means, missing agents). |
| `outside_identification` | Reserved and left empty: any later identification from outside the source goes here, separately from the above. |

Rules: names are not expanded unless the source prints the expansion; the same person in two passages is two rows linked only by `inferred_same_as`; statements that belong to someone else (for example a quoted letter or report) carry that person in `asserted_by`.

## Two example records

**Example 1: a sample row** (the bark analysis, S04)

| Field | Value |
|---|---|
| record_id | S04-B01 |
| record_type | sample |
| material_kind | bark |
| source_ref | The Tropical Agriculturist, July 1883, p. 66 |
| locator | OCR line 11 |
| printed_text | The bark of some of these trees was sent home by Mr. Campbell for analysis to Mr. Howard, who pronounced it to be Ledgeriana bark, giving 7 per cent of pure quinine (equal I believe to 9 of sulphate) and only a trace of other alkaloids. |
| printed_name | The bark of some of these trees |
| stated_detail | Sent home by Mr. Campbell to Mr. Howard for analysis; pronounced Ledgeriana bark; "7 per cent of pure quinine"; "only a trace of other alkaloids"; "(equal I believe to 9 of sulphate)" is the writer's belief, not a measured value. |
| asserted_by | S04-P02 |
| reading_status | clear |
| inferred_note | Which trees supplied the bark is not stated beyond "some of these trees"; whether it includes S04-T01 is not said. |
| outside_identification | (empty) |

**Example 2: an action row** (sending the bark, S04)

| Field | Value |
|---|---|
| record_id | S04-A09 |
| record_type | action |
| source_ref | The Tropical Agriculturist, July 1883, p. 66 |
| locator | OCR line 11 |
| printed_text | The bark of some of these trees was sent home by Mr. Campbell for analysis to Mr. Howard |
| subject_id | S04-P06 (printed name "Mr. Campbell") |
| verb_as_printed | sent home ... for analysis |
| object_id | S04-B01 |
| recipient_id | S04-P03 (printed name "Mr. Howard") |
| asserted_by | S04-P02 (letter-writer, signed "WALTER AGAR") |
| reading_status | clear |
| inferred_same_as | (empty on this row; the person rows S04-P06 and S04-P03 carry "probable" links to S03-P07 and S03-P01, where fuller printed names appear: "Mr. J. A. Campbell of Lindula, Ceylon" and "Mr. J. E. Howard") |
