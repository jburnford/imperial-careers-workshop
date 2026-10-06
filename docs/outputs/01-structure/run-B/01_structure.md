# Proposed record structure: people and activities in two *Tropical Agriculturist* passages (July 1883)

Sources covered:

- **S03** — *The Tropical Agriculturist*, July 1883, p. 37: "DR. TRIMEN'S LEDGERIANA: MR. T. N. CHRISTIE TO THE RESCUE." (letter from St. Andrew's, Maskeliya, 7th June 1883, signed THOS. NORTH CHRISTIE; quotes the Kew Gardens Report for 1880 and a letter from Mr. Campbell).
- **S04** — *The Tropical Agriculturist*, July 1883, p. 66: "DR. TRIMEN'S TYPICAL LEDGERIANA TREE." (editorial note plus letter from Lawrence, June 22nd, 1883, signed WALTER AGAR).

## Design in one paragraph

One flat table, one row per record. A record is either an *entity* (person, plant/tree, bark sample, other specimen) or an *action* (something one entity did to, or said about, another). Entities carry the printed wording; actions carry a short controlled verb plus pointers to the entity records they connect. Everything the text states goes in the `*_as_printed` and `quote` fields; everything I supplied (identity links across the two passages, resolved dates, "here" = place of writing, etc.) goes in `inferred` and nowhere else. Identifiers are local (`PER-`, `PLT-`, `BRK-`, `SPC-`, `ACT-`), and the `outside_identification` field is reserved for later authority linking (Wikidata etc.) and is kept separate from the source wording.

## Fields

| # | Field | Rationale (one line) |
|---|-------|----------------------|
| 1 | `record_id` | Local, stable identifier with a type prefix (`PER-01`, `PLT-03`, `BRK-01`, `SPC-01`, `ACT-12`); no external IDs yet. |
| 2 | `record_type` | One of `person`, `plant`, `bark_sample`, `specimen`, `action`; lets a single table hold both entities and relationships. |
| 3 | `label_as_printed` | The printed form chosen as the record's head form (for people: the fullest form the source itself prints, e.g. a signature); never expanded beyond what the source gives. |
| 4 | `variants_as_printed` | Other printed forms of the same entity found in the two passages (e.g. "Mr. Agar" beside "WALTER AGAR"), each tagged with its source; list. |
| 5 | `description_as_printed` | Verbatim descriptive phrases the text attaches to the entity or action (ages, yields, judgements), so the printed wording is preserved alongside the structured fields. |
| 6 | `action_type` | Actions only: a short controlled verb (`figured`, `planted`, `sent_for_analysis`, `pronounced`, ...), so activities can be counted and filtered. |
| 7 | `subject_ids` | Actions only: list of local IDs of the actor(s); empty when the text leaves the agent unstated (e.g. "the analysis ... arrived from England"). |
| 8 | `object_ids` | Actions only: list of local IDs of the thing(s) acted on or addressed. |
| 9 | `date_as_printed` | The date expression exactly as printed ("7th June 1883", "5th instant", "some two years ago"); resolved dates go in `inferred`. |
| 10 | `place_as_printed` | Place name exactly as printed ("Mahanilu", "Mahanillu estate", "the Waltrim clearing"); OCR spelling differences are kept, not normalised. |
| 11 | `source_ref` | Journal, month/year, page, OCR file and line number(s), so every record can be checked against the page. |
| 12 | `quote` | The exact supporting sentence(s) from the OCR text; the script verifies each quote occurs verbatim in the source file. |
| 13 | `inferred` | Anything not stated in the text that I supplied to make the record usable (cross-passage identity, resolved relative dates, implied bark samples); blank when nothing was inferred. |
| 14 | `reading_status` | `ok`, `uncertain` (OCR or sense doubtful), or `failed` (could not be made into a usable record); feeds the notes file. |
| 15 | `outside_identification` | Reserved and separate from the source: any identification from outside the text (to be verified; no Wikidata QIDs yet). |

Conventions: lists are JSON arrays in `02_records.json` and ` | `-joined strings in `02_records.csv`. Quotation marks and asterisks (italics markers) in the OCR are kept as they stand.

## Two example records

### Example 1 — a person

```json
{
  "record_id": "PER-04",
  "record_type": "person",
  "label_as_printed": "WALTER AGAR",
  "variants_as_printed": ["Mr. Agar (S04 l.3)", "Mr. Agar (S03 l.5)"],
  "description_as_printed": ["a letter from Mr. Agar, which places beyond question the fact that the tree figured by Dr. Trimen was an undoubted Ledgeriana (S04 l.3)", "planted on Mahanilu by Mr. Agar (S03 l.5)"],
  "action_type": "",
  "subject_ids": [],
  "object_ids": [],
  "date_as_printed": "June 22nd, 1883",
  "place_as_printed": "Lawrence",
  "source_ref": "The Tropical Agriculturist, July 1883, p. 66 (S04_ocr.txt l.3, l.5, l.17); p. 37 (S03_ocr.txt l.5)",
  "quote": "WALTER AGAR.",
  "inferred": "Within S04 the editor's 'Mr. Agar' and the signature 'WALTER AGAR' belong to the same letter, so the expansion is given by the source. Treating the 'Mr. Agar' of S03 (who planted the figured tree on Mahanilu) as the same man is my inference from the shared subject and estate, not a statement in either passage.",
  "reading_status": "ok",
  "outside_identification": ""
}
```

### Example 2 — an action linking a person, a bark sample and another person

```json
{
  "record_id": "ACT-09",
  "record_type": "action",
  "label_as_printed": "sent home by Mr. Campbell for analysis to Mr. Howard",
  "variants_as_printed": [],
  "description_as_printed": [],
  "action_type": "sent_for_analysis",
  "subject_ids": ["PER-09"],
  "object_ids": ["BRK-01", "PER-03"],
  "date_as_printed": "",
  "place_as_printed": "",
  "source_ref": "The Tropical Agriculturist, July 1883, p. 66 (S04_ocr.txt l.11)",
  "quote": "The bark of some of these trees was sent home by Mr. Campbell for analysis to Mr. Howard, who pronounced it to be Ledgeriana bark, giving 7 per cent of pure quinine (equal I believe to 9 of sulphate) and only a trace of other alkaloids.",
  "inferred": "'Sent home' is read as sent to England (S03 speaks of an analysis that 'arrived from England'), but S04 does not name the destination. 'Mr. Campbell' here is linked to 'Mr. J. A. Campbell of Lindula' (PER-09) of S03 by inference.",
  "reading_status": "ok",
  "outside_identification": ""
}
```

If these fields are acceptable, the remaining people, plants, bark samples, specimens and actions from both passages will be processed with the same structure.
