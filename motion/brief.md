# Claude Motion brief: six animated explainers for the workshop deck

Claude Motion runs in claude.ai (Team and Enterprise, beta from 8 October 2026), not in Claude Code. Use it from a chat (Output → Motion) or from the Artifacts tab with a Motion template. Paste one prompt per animation, attach the listed files, then **Export → MP4**. Save each file as `media/motion/<name>.mp4` in this repository and Claude Code will place it in a draft deck for comparison with the current static slide.

Every number below is checked against the workshop pages or the Imperial Careers statistics. Ask Motion not to add any others.

## Shared style (paste at the top of every prompt)

> Audience: historians at a conference session, advanced beginners to intermediate with computational methods, in the room and on Zoom. It plays silently on a projected 16:9 slide (1280 × 720) while I talk, so no narration or audio, and no captions that duplicate my speech.
> Style: dark background #15161a; text #e9e4d8; headings #f3ead3 in Georgia or a similar serif; accent gold #c9a227; secondary blue #7fa7d6; "before" or error state #c0674f; "after" or fixed state #79a868. Flat shapes, thin rules, no gradients, no 3D, no stock imagery, no people.
> Keep on-screen text short and large enough to read from the back of a room. Use only the words and numbers I give you; do not invent figures, dates, names or identifiers. Hold the final frame for at least three seconds so it can sit on the slide while I talk.

## 1. `arc` · From printed clause to a mapped arc (about 20 s)

Replaces or precedes the slide "What one arc needs". Attach `images/atlas-wodehouse-repaired.png`.

> Animate how one printed clause becomes one arc on a map.
> Scene 1: show this source text in a serif typeface: "WODEHOUSE, SIR PHILIP E.—… governor of British Guiana; … in 1861 was appointed governor of the Cape of Good Hope." Highlight "governor of the Cape of Good Hope" and "1861" in gold.
> Scene 2: the highlighted words slide down into a small record card: Event: governor · Year: 1861.
> Scene 3: a second card attaches: Historical place: Cape Colony (a Wikidata item). Label it "checked identifier".
> Scene 4: a third card: Plotting seat: Cape Town, with the small note "a proxy, not a residence".
> Scene 5: a simple dark world outline. A blue point appears at Georgetown (British Guiana) and another at Cape Town; a thin blue arc draws from the first to the second. Final caption: "A source clause → an event → a checked place → a point → an arc."
> Use the attached atlas screenshot only as a style reference for the map colours.

## 2. `ditto` · Balmer's "do." (about 15 s)

Supports "The source", "Mark up Balmer" and "Replay a past correction".

> Animate how a printed ditto is resolved.
> Scene 1: show this entry: "BALMER, F. E.—Dep. chief acctnt., G.P.O., E. Africa Prot., Mar., 1919; ch. acctnt., G.P.O., Kenya, Oct., 1919; ch. acctnt., Kenya-Uganda-Tanganyika post and tel. service, 1933; senr. dep. P.M.G., do., 1935."
> Scene 2: highlight "do." in gold. A small label appears: "do. = ditto, 'the same as before'".
> Scene 3: a curved arrow travels back from "do." to "Kenya-Uganda-Tanganyika".
> Scene 4: below, a record card shows place: "do." in the before colour, then the value changes in place to "Kenya-Uganda-Tanganyika" in the after colour, with the line place_inherited: true staying unchanged.
> Final caption: "A reader resolves it at a glance. A program has to be told, and the change is logged."

## 3. `hybrid` · Python, Qwen, Python (about 20 s)

Replaces or precedes "Develop the hybrid with Claude Code".

> Animate a three-stage text-processing pipeline as a flow of small cards, each card standing for one biographical entry.
> Stage 1, blue box labelled "Python": regular entries pass straight through. Any entry with a dated clause the rules cannot parse is set aside whole, not half-parsed.
> Stage 2, gold box labelled "Qwen reads": set-aside entries enter one at a time; each leaves as a structured record (show a tiny card with fields: position, place, years).
> Stage 3, blue box labelled "Python checks": a few fields flash in the before colour and are dropped with the label "not in the source".
> Then a counter: "30,496 India Office entries · 8.24 hours overnight".
> Final caption: "Claude Code helped build the pipeline. Qwen read the entries."
> Do not show any other counts or percentages.

## 4. `merge` · Forty editions, one person (about 20 s)

Replaces or precedes "Clean: forty editions, one person".

> Animate record linkage across annual editions.
> Scene 1: many small entry cards scattered across the frame, with the label "199,099 printed entries, Colonial Office List".
> Scene 2: cards with matching names and a shared dated event snap together into stacks: label "strong rules".
> Scene 3: two similar cards remain apart: "ABERY, Joseph · M.B.C.M. · 1867 Ceylon, assistant colonial surgeon" and "CARBERY, Joseph · M.B.C.M. · 1867 Ceylon, assistant colonial surgeon". The letters "C" and "R" fade in faintly on ABERY to show the likely OCR loss; the two cards merge, and a small ledger line writes: "merged: same forename, qualification and dated appointment; probable OCR loss".
> Scene 4: the stacks settle into a count: "27,526 person records".
> Final caption: "Ties resolve to no merge. Every merge keeps its reason."

## 5. `victoria` · Which Victoria? (about 15 s)

Replaces or precedes "A past repair: which Victoria?".

> Animate a place-name disambiguation repair.
> Scene 1: the quotation "defeated by Sir Richard McBride, in Victoria, 1912."
> Scene 2: the word "Victoria" fans out to five labels: Colony of Victoria (Australia); Victoria, British Columbia; Victoria, Hong Kong; Victoria, Seychelles; Victoria, Labuan.
> Scene 3, labelled "Before" in the before colour: one arrow from every entry that printed "Victoria" goes to the Australian colony; a point lands in Australia.
> Scene 4, labelled "Completed fix" in the after colour: the career context appears (McBride; legislative assembly; British Columbia) and pulls the arrow to Victoria, British Columbia.
> Final caption: "Resolve the place per person, from the surrounding career."

## 6. `cost` · Where a hosted run's money goes (about 12 s)

Supports "What reading the corpus costs". Check the OpenRouter price before the session and edit the numbers in Motion if it has changed.

> Animate a simple cost breakdown.
> Scene 1: one entry card. A bar labelled "read: about 640 tokens" fills, then a second bar labelled "written: about 330 tokens".
> Scene 2: multiply to 30,496 entries: "about 19.5 million tokens read" and "about 10 million tokens written".
> Scene 3: convert to money at "Qwen3.8-27B on OpenRouter, 8 October 2026, a 50% promotion: $0.0239 read / $2.175 written per million tokens". The read bar becomes "≈ $0.47"; the written bar grows to "≈ $22".
> Final caption: "Almost all of the cost is what the model writes. Regular price: about twice."

## Judging whether Motion helps

For each export, ask: does the motion teach something the static slide does not (a sequence, a change of state, a flow), or only decorate it? Is every number still exactly as given? Can it be read from the back of the room and on a Zoom share? Does it fit the minute it replaces? Keep the static slide as the fallback if the video fails to load.
