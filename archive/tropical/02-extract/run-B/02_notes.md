# Notes on the extraction (02_records.json / 02_records.csv)

## How to rerun

```
cd <this directory>
python3 02_extract.py                 # sources expected in the parent directory (S03_ocr.txt, S04_ocr.txt)
python3 02_extract.py --sources /path/to/ocr --out /path/to/output
```

No third-party packages, no network. The script holds the records as data, checks that every
`quote` and every tagged `variants_as_printed` / `description_as_printed` phrase occurs verbatim in
the cited OCR file, checks that all `subject_ids` / `object_ids` resolve, then writes the JSON and CSV
and prints a summary. If a check fails it prints the problems and exits with status 1 without writing.

Last run: 71 records (person 10, plant 15, bark_sample 4, specimen 2, action 40); all verbatim checks passed.

## Failed records

| id | problem |
|----|---------|
| PLT-13 | S04 l.13: "I have by my prints of the leaves of some of the trees as well as the other that Mr. Moens had sent to be true Ledgerianas". The clause "the other that Mr. Moens had sent to be" does not parse. It may be an OCR or printer's error for something like "the others that Mr. Moens had said to be true Ledgerianas" (further trees Moens identified). I could not tell from the text which plants are meant, so the record is kept with the printed wording only and marked `failed`. SPC-01 and ACT-33 (Agar's leaf prints) depend on the same sentence and are marked `uncertain`. |

## Uncertain readings

| id(s) | reading | why uncertain |
|-------|---------|---------------|
| PLT-11, ACT-23 | Kew Report extract headed `"*Indonesia*.—Three other plants, imported at Kew from the same authentic strain were sent to Jamaica."` | The heading "Indonesia" sits oddly with a sentence about Jamaica in an 1880 Kew report (the preceding extract is headed "Ceylon"). Likely an OCR or transcription error for the heading, possibly "Jamaica". "imported at Kew" may also be a misreading (e.g. "propagated at Kew"). Recorded exactly as printed. |
| PLT-04, BRK-03, ACT-15 | "showed 11.29 S." | "S." is not explained; I read it as per cent sulphate of quinine, by analogy with "per cent sulphate of quinine" earlier in the same paragraph. |
| PER-08 | "Mr. T. Christy" vs the author "Christie" | Treated as two different people: the spelling "Christy" is printed twice, and the author refers to "Mr. T. Christy's" plants in the third person. A spelling variant for one person cannot be absolutely excluded from the text alone. |
| PLT-01, ACT-05, ACT-06 | "Mahanilu" (S03) / "Mahanillu estate" (S04) | Two spellings of what is evidently one estate; both kept as printed, not normalised. |
| SPC-01 | "I have by my prints of the leaves" | Probably "I have by me prints"; kept as printed. |
| PLT-15 | "cinchonias" | Probably "cinchonas"; kept as printed. |
| S03 l.5 | "DEAR SIR." (S03) vs "DEAR SIR,—" (S04) | Punctuation differences kept; not material to any record. |
| BRK-01 | "7 per cent of pure quinine (equal I believe to 9 of sulphate)" | The "9 of sulphate" is Agar's own conversion ("I believe"), not part of Howard's report. |
| BRK-03, BRK-04 | bark samples | These two records exist only because yields/analyses are reported; the text never mentions the samples themselves (see "Inferred" below). |

## Inferred rather than read

Everything below is in the `inferred` field of the relevant record and nowhere else in that record.

**Identity links across the two passages (not stated by either text):**

- PER-01 "Dr. Trimen" of S03 = "Dr. Trimen" of S04.
- PER-02 "THOS. NORTH CHRISTIE" / "MR. T. N. CHRISTIE" (S03) = "Mr. Christie" (S04). The T. N. = Thos. North expansion itself is given by S03 (title and signature), so it is not an outside expansion.
- PER-03 "Mr. J. E. Howard, F. R. S." (S03, Kew Report quotation) = all other "Mr. Howard" / "Howard's" mentions in S03 and S04.
- PER-04 "WALTER AGAR" (S04 signature) = "Mr. Agar" of S04 editorial note (given by the source: same letter) = "Mr. Agar" of S03 who planted the figured tree on Mahanilu (my inference).
- PER-05 "Mr. Moens" of S03 = "Mr. Moens" of S04.
- PER-09 "Mr. J. A. Campbell of Lindula" (S03, Kew Report) = "Mr. Campbell" who "writes to me" (S03, link made by the source: "Mr. Campbell himself") = "Mr. Campbell" who sent bark to Howard (S04, my inference).
- PLT-01 the plant Trimen "figured" (S03) = the tree "sketched for Dr. Trimen's work" (S04).
- PLT-08 the 1876 Java seed at Kew = "the first seed received at Kew" (S03 l.15).
- PLT-09 the three rooted cuttings given to Campbell (Kew Report) = the "authentic" cuttings in the Waltrim clearing = the trees Campbell describes "raised from cuttings received from Mr. Howard".
- PLT-02 the 12-14 per cent trees = "mature Ledgerianas, which have given the highest analyses we have yet heard of" (ACT-38).
- PLT-07 Howard's figured "Ledgeriana" = "the figured" plant of the Kew Report's cuttings (ACT-21).

**Resolved dates and places (the text gives only relative expressions):**

- "5th instant" (ACT-25) -> 5 June 1883, from the letter date 7th June 1883.
- "in the course of last year" (ACT-21) -> 1879, from "Kew Gardens Report for 1880".
- "some two years ago" (PLT-06, ACT-36) -> c. 1881; "9 months ago" (ACT-18) -> c. September 1882; both counted from June 1883.
- "here" (PLT-04, ACT-14) -> St. Andrew's, Maskeliya, the place of writing of S03.
- "sent home" (ACT-09) -> England.
- "DEAR SIR" in both letters -> the journal's editor (PER-10).
- PLT-01 "is dead" -> dead by June 22nd, 1883 (ACT-39); date of death not stated.

**Records that exist only by inference:**

- BRK-03: a bark sample of PLT-04 sent to England, inferred from "the analysis of that very tree arrived from England".
- BRK-04: bark analyses behind "over 12, 13 and 14 per cent sulphate of quinine" for PLT-02.

**Pronoun resolution inside quoted matter:** "me" in Campbell's quoted letter = Campbell (PLT-10, ACT-26); "him" in "forwarded to him by Mr. Moens" = Howard (PLT-14); "these characteristics" = the "satin gloss and hairy margin of the leaves" (ACT-16).

## Names: expansions and outside identification

- No name was expanded beyond what the two passages print. Head forms are the fullest form the source itself gives (a signature or the Kew Report's "Mr. J. E. Howard, F. R. S.").
- `outside_identification` is filled for six people (PER-01, -03, -05, -06, -07, -08) with a candidate drawn from the assistant's general background knowledge. Each is explicitly prefixed "UNVERIFIED candidate ... not from the source and not checked against any authority". Nothing was looked up; no Wikidata or other identifiers were added. These are suggestions for the historian to verify or delete, kept out of every other field.

## Things deliberately not made into records

- Places (Kew, Java, Jamaica, Ceylon, Lindula, Waltrim, Mahanil(l)u, Lawrence, St. Andrew's/Maskeliya, Dikoya, England, "the Ceylon and Indian plantations") are kept in `place_as_printed` on the relevant records rather than as separate records, to keep the table small. They could be promoted to a `place` type later.
- Estate names that appear only inside plant names ("the Yarrow Ledgers", "the Annfield and Emelina Calisayas") are not entered as places.
- Publications ("Dr. Trimen's work", "Mr. Howard's latest paper", "Howard's great work", "the Dikoya essay", "Kew Gardens Report for 1880, p. 12") are referenced in `inferred`/`description_as_printed` but have no records of their own.
- "a gipsy", "The veriest tyro" (rhetorical figures) are not people records.
- Cross-passage links are recorded as `inferred` text on the person/plant records; no separate "same_as" action records were created.
