# Scoring GPT Astra 6 (medium) with web retrieval on the twenty entries

Jim Clifford gave the twenty entries (`bios.md`) to OpenAI's GPT Astra 6, a frontier model released in late summer 2026, at the medium setting, on 7 October 2026, starting about 08:35; the output file `bios-grounded.json` was downloaded at 09:02, so about 27 minutes. Prompt, the same as for the other two runs: "Parse these bios and ground the places, schools and people to Wikidata ids where possible." The file's own methodology block says: public web search, Wikipedia sitelinks and web-retrieved Wikidata pages, not the API or a vector search; the answer key was not consulted; birth years only where printed. The file is saved as `astra-grounding.json`; every identifier in it was resolved with `wbgetentities` on 7 October (`astra-grounding-check.json`).

## What it produced

A structured dataset rather than a list: 180 entities, 301 mentions with character offsets into the source text, 396 clauses, and for each entity a status (`matched`, `unresolved`, `candidate`, `geographic_proxy`), a confidence, a `match_relation` (same entity, geographic correspondence only, region only, historical phase of entity), rejected candidates with reasons, and the evidence URL with the date checked.

| | |
|---|---|
| Subject identifiers given | 16 (4 declined, the same four as the MCP search and Opus) |
| Subjects correct | 16 (Gorges on the duplicate item Q121494224, as Opus) |
| Entities with an identifier | 155 |
| Whose Wikidata label or alias matches the name | 155 |
| Unresolved, with a reason | 15 |
| Modern items recorded as proxies only, not matches | 9 |

By type: 30 people, 1 award eponym, 20 schools and inns, 31 historical polities, 64 places, 9 regions, all consistent.

## Where it was better than the pipeline

The Imperial Careers pipeline's known place errors (step 6 of the workshop) are modern-collapse errors: Penang grounded to the Malaysian state, the Union of South Africa joined to the British South Africa Company, "Victoria" resolved once for everyone. Astra's file handles those cases the way the fixes did:

- Ceylon → Q918153 British Ceylon, the same item the pipeline uses. Straits Settlements → Q376178, the pipeline's manifest entity. Union of South Africa → Q193619, the corrected row. Transvaal Colony, Orange River Colony, Lagos Colony, Gambia Colony and Protectorate, British Guiana, Dominion of Newfoundland, Crown Colony of Malta: all the period polities.
- Penang, Malacca, Singapore, Barbados, Grenada, Saint Lucia, Dominica, Seberang Perai and Guangxi carry only a `geographic_qid` marked "geographic correspondence only", with a note that the modern item is not the colonial jurisdiction. Penang Q188096 is exactly the identifier the pipeline had wrongly used as a match.
- Zanzibar is marked "historical phase of entity"; East Africa "region only"; "Mende country" refused a people-QID as a place; "Sherbro district" refused Sherbro Island; four sub-island judicial districts left unresolved; "British sphere north of the Zambezi" left as a relational extent rather than the later protectorate.
- Rejected candidates are recorded with reasons: the Glasgow Royal Infirmary hospital is not its medical college; Shimbiris mountain is not the Shimber Berris forts; the trans-African Sudan belt is too broad for the 1884 expedition; modern Seremban is not the historical Sungai Ujong luak.

One modern collapse remains: "Victoria, Australia" for Belcher's postings → Q36687, the state, where the pipeline's manifest uses Q56850459, the Colony of Victoria. And "Malay States" → Q2658454 "Monarchies of Malaysia" as a collective term is a stretch.

## What this shows

- Retrieval with a careful model and enough time produces the dataset a historian would want: period entities, modern proxies labelled as such, refusals with reasons, evidence with dates. Twenty-seven minutes for twenty entries.
- That is about 80 seconds an entry. The Colonial Office List has 27,526 people; at this rate the grounding alone is 25 days of continuous model time, before the India Office List, and it would have to be audited anyway. The pipeline's vector search plus gates runs the same lookups in seconds per surface and reaches 131,343 placed events; its failures were caught on the map.
- The right use of this column is the review queue and the gold standard: run it on the hard cases and the sample, use what it decides to write the rules, measure the pipeline against it.

Four runs, one table:

| | Gemini 3.8 Flash, no tools | Pipeline: vector search + gates | Claude Opus 5.5, retrieval | GPT Astra 6 (medium), retrieval |
|---|---|---|---|---|
| Person identifiers correct | 0 of 16 | 12 of 12 given; 8 ungrounded, 4 have items | 16 of 16 | 16 of 16 |
| Places | 38 of 104 labels match; modern items | 3,207 surfaces over the corpus; modern-collapse errors fixed later from the map | 17 of 138, then stopped | 104, period entities, 9 modern proxies labelled |
| Time | under 5 min | overnight for the corpus | ~20 min, two passes | ~27 min |
