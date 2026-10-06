# Saved output for step 2: two cold extraction runs

Two coding-agent runs, 6 October 2026, each given only the OCR text of S04 (Agar's letter, p. 66) and S03 (Christie's letter, p. 37) and the two prompts below, verbatim. No hints about what to look for, no access to the scans, no network. Each run wrote its proposal, a script that regenerates its records offline, the records, and notes on failures and inferences. Nothing in either folder has been edited.

| Run | Agent and model | Records | Failed | Uncertain | Folder |
|---|---|---|---|---|---|
| A | Claude Code, model alias `sonnet` (Claude Sonnet 5.5) | 85: 16 persons, 20 plants, 4 samples, 45 actions | 0 | 8 | `run-A/` |
| B | Claude Code, session default model (Claude Fable 5.1) | 71: 10 persons, 15 plants, 4 bark samples, 2 specimens, 40 actions | 1 | 9 | `run-B/` |

The structure proposals (prompt 1) are in `../01-structure/`.

## The prompts

Prompt 1, structure:

> Read these Tropical Agriculturist passages. Propose a small table for studying the people and activities mentioned. Show two example records before processing the rest. Preserve the printed wording and source references. Keep inferred information separate from what the text states. Use local record identifiers and do not add Wikidata identifiers yet.

Prompt 2, extraction:

> Use the agreed fields to process this sample. Save the code, instructions, and output so we can inspect and rerun the work. Report failed records and uncertain readings. Do not expand a person's name unless the source provides the expansion; record any outside identification separately.

## Rerunning

```bash
python3 outputs/02-extract/run-A/02_extract.py source-pack            # writes next to the script
python3 outputs/02-extract/run-B/02_extract.py --sources source-pack --out /tmp/runB
```

Both scripts hold the records as data and check that every quoted span occurs verbatim in the source text and that every link resolves. They check quotation, not interpretation.

## What to look at in the room

**The editor versus the letter (case R2).** Neither run made the conflation the editor's headnote invites. Run A recorded the editor's "analyzed the bark" as the editor's statement (`S04-A11`, asserted by the editor) and wrote on the bark sample that which trees supplied it "is not stated beyond 'some of these trees'". Run B attached the editor's phrase to the bark-of-some-trees action as a variant (`ACT-10`) and noted on the editor's affirmation (`ACT-40`) that Agar himself only says the figured tree was "one of several". So the saved runs do not supply a wrong record to correct. They supply something more useful: a careful record whose correctness you have to confirm by reading, which is the review task in its ordinary form.

**The garbled sentences (case R3).** Both runs noticed that two sentences in S04 did not read well, kept the printed wording, and guessed at the intended reading in their notes: run A "in full bloom" and "by me"; run B "by me" and "the others that Mr. Moens had said to be". Every guess is wrong. The scan reads "growing in a bad situation and not robust" and "I have many plants from the seed of the specimen tree". A model can detect that OCR is damaged; it cannot repair it from the text alone.

**Outside knowledge, two ways.** Run A left `outside_identification` empty on every row. Run B filled it for six people with candidates "from the assistant's background knowledge", each prefixed UNVERIFIED and kept out of every other field. Both are acceptable responses to the instruction. Run B's candidates happen to agree with the retrieved ones in step 3 for Trimen, Howard, Moens, McIvor and Ledger; that agreement is not verification, and the retrieval step exists so that it does not have to be.

**Mahanilu / Mahanillu.** Both runs kept the two spellings as printed and marked them as probably one estate. The scan of p. 66 reads "Mahanilu"; the second "l" is an OCR error.

**What neither run did.** Neither expanded "Mr. Howard" to "J. E. Howard" within S04, since only S03 prints the initials. Neither merged "Mr. T. Christy" with the author Christie. Both read "11.29 S." as sulphate of quinine and said so.
