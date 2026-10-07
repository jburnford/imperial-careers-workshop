# Notes on 02_extract.py output

Run: `python3 02_extract.py [SOURCE_DIR]` (default source directory is the parent of this folder, holding `S04_ocr.txt` and `S03_ocr.txt`). It needs only the standard library and works offline. It writes `02_records.json`, `02_records.csv` and `02_validation.txt`.

The records are hand-read and entered as data in the script. The script then checks that every `printed_text` span occurs verbatim in the source file and that every `subject_id`, `object_id` and `recipient_id` points to an existing record.

Result of the last run: 85 records (16 persons, 20 plants/seeds, 4 samples, 45 actions); 0 failed records; 8 uncertain readings. Failed records would appear under `failed_records` in the JSON and in `02_validation.txt`.

## Failed records
None failed the automated checks. The checks confirm quotation and id links only; they do not confirm that the interpretation is correct.

## Uncertain readings
- S04-P07: "Ed." kept as a role-only record (no personal name). Drop if only named people are wanted.
- S04-T02: "in a full condition" may be a slip for something like "in full bloom"; transcribed as printed.
- S04-T03 and S04-A12: "the other that Mr. Moens had sent to be true Ledgerianas" is garbled ("the other" has no noun; "sent to be true" may be missing words). Not interpreted.
- S04-B02 and S04-A13: "I have by my prints of the leaves" is probably "by me"; transcribed as printed.
- S03-T11 and S03-A21: the quoted Kew paragraph is headed "*Indonesia*" but says the plants went to Jamaica. Probably a misprint or OCR error; the heading was not corrected.
- S03-T13 is a trimmed mid-sentence excerpt of Mr. Campbell's quoted letter (marked as a note, not an error).

## Things inferred, not read (all in `inferred_*` columns)
- Cross-passage identity of people and plants (S04 to S03) is marked "probable" only, based on surname, title and subject. S04-P04 "Mr. Christie" is linked to S03's signed writer "THOS. NORTH CHRISTIE" without the text confirming that S03 is the piece meant. S03 "Mr. T. Christy" (spelled with a y) is kept as a different person.
- Names are not expanded: S04 "Mr. Howard" has no initials (S03 prints "Mr. J. E. Howard"); "Walter" for Agar appears in the signature and so is source-provided; McIvor and Ledger have no forenames or titles in print. No outside identifications (for example, of Dr. Trimen, Mr. Moens or the cinchona taxa) were made; `outside_identification` is empty on every row. No Wikidata ids are used.
- "I", "me", "my" in S03 are read as the signer, Christie, except inside Mr. Campbell's quoted letter, where they are Campbell. In S04 they are Agar.
- S03 "here" is read as St. Andrew's, Maskeliya (the dateline). "S." in "11.29 S." is read as sulphate (of quinine) and its unit is not printed. "Last year" in the Kew report is relative to the Report; no calendar year is supplied.
- S03-A09: the agent who "put forward" the "satin gloss and hairy margin" statement is not named; Mr. Howard is a probable reading from context and is only in `inferred_same_as`.
- S03-A20 and S03-A16/A17/A21: the giver ("Kew") is not a person record; subject is left blank.
- S03-T12 ("authentic" cuttings in the Waltrim clearing) is linked to S03-T10 (cuttings given to Campbell) as probable; the text does not say the clearing is Campbell's.
- S04-B03 "the tree itself" is read as the sketched tree S04-T01.
- Page numbers (p. 66 for S04, p. 37 for S03) and the "July 1883" issue come from the task description, not from the OCR text.

## Not captured
- Publications mentioned (Dr. Trimen's work and "description and figure", Howard's "latest paper" and "great work", the Dikoya essay, the Kew Gardens Report for 1880 p. 12) are not separate records; they appear in `stated_detail` or `asserted_by`.
- Places (Mahanillu/Mahanilu, Lawrence, Maskeliya, Lindula, Kew, Java, Jamaica, Waltrim clearing, Yarrow) appear only as printed in `place_as_printed`, not as records. "Mahanillu" (S04) and "Mahanilu" (S03) are kept as printed.
- General statements without a specific entity (for example, "the highest analyses we have yet heard of", "the veriest tyro in cinchona cultivation") and the unnamed addressee ("Dear Sir") are omitted.
- Opinions about leaf characteristics ("satin gloss", "hairy margin") are recorded only within the actions where they appear.
- The S03 percentage figures (over 12, 13 and 14 per cent sulphate of quinine) are kept in the plant group record S03-T02 rather than as separate sample records, because the text does not link each figure to an individual plant.
