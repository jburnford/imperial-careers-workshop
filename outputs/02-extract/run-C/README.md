# Run C: Qwen3.8-27B-FP8, the model you would use at scale

Same two prompts, same two passages (S04 and S03 OCR text), sent to Qwen3.8-27B-FP8 served by vLLM on the University of Saskatchewan's Plato cluster (one 3g.40gb MIG slice of an A100), 6 October 2026. This is the model the Tropical project used to extract entities from 53,000 articles; the frontier models in runs A and B are too expensive for that.

Two differences from runs A and B, both recorded in `02_extract.py`:

- The model is not a coding agent. It cannot write or run a script, so the second prompt carries a one-sentence addition asking for the records as JSON followed by a notes section. The script is the "saved code".
- Temperature 0. Two variants: `nothink/` with the model's reasoning mode off (the setting a production run would use, for cost), and `think/` with it on.

| Variant | Records | Tokens out (turn 1 + 2) | Time |
|---|---|---|---|
| nothink | 13: 8 people, 5 activities | 1,473 + 3,304 | 57 s + 129 s |
| think | none: output cut off at the 24,000-token cap, all of it reasoning | 6,477 + 24,000 | 249 s + 955 s |

## The reasoning-mode run produced nothing

With reasoning on, the first turn (the structure proposal) took 6,477 output tokens and four minutes. The second turn spent the whole 24,000-token budget, sixteen minutes on the GPU slice, deliberating about the output format, whether the notes section might also contain code, and whether a letter signed "WALTER AGAR" allows "Mr. Agar" to be expanded, and never reached the records. The transcript is in `think/02_response.md` and `think/02_reasoning.txt`. That is why production runs turn reasoning off, and it is a fair warning about asking a mid-sized model to follow a long instruction and reason at the same time: the budget goes on the instruction.

## What the no-thinking run did (read against the page)

**It attributed the editor's claim to Agar.** Record P02 says Agar "confirms the tree sketched for Dr. Trimen was an undoubted Ledgeriana". That sentence is the editor's headnote. Agar's letter does not say it. The same record says Agar "saw the tree in flower at Mahanillu estate with Mr. Moens and Dr. Trimen"; the letter says Moens saw the trees and Trimen was with Moens. Agar's own presence is not stated.

**It did not notice the OCR errors.** Record A02 reports the trees "were now in a full condition and in flower" as fact. Its notes list name spellings and quinine percentages under uncertain readings, not the two damaged sentences. Runs A and B both flagged them.

**It dropped the hedges.** "equal I believe to 9 of sulphate" became "equal to 9 of sulphate". The bark "of some of these trees" became "bark from trees at Mahanillu estate".

**It kept Christy and Christie apart**, with a sensible note, and did not expand names beyond what the sources print.

**Thirteen records against 85 and 71.** The structure it proposed has six fields and one row per person or activity, with the whole of a person's doings in one prose cell. That is a reasonable table for reading; it is a poor one for checking, because there is no quote per claim to hold against the page.

## Why this matters for the hour

The careful behaviour in runs A and B is what a frontier model does on two passages. Run C is what the affordable model does on the same passages, and it made the structure error (the editor's claim as Agar's), missed the cleaning error (the OCR accepted as fact), and softened the evidence. None of this is visible in its output, which reads well. The review step exists for run C, not for run A.

The remedy is not a better model for every chunk. It is the pipeline shape in the Tropical project: the frontier model, as agent, writes the script and the checks; the cheap model reads the collection inside it; quotes are kept per claim so that the historian can check a sample against the page; and corrections become rules and tests.
