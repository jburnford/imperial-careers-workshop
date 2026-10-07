# Scoring Claude Opus 5.5 with retrieval on the twenty entries

Jim Clifford gave the same twenty entries to Claude Opus 5.5 in a chat with web search, 7 October 2026. The model fetched Wikidata item pages (and one Wikisource author page) and reported only identifiers it had seen on a page. It stopped at its tool limit after the twenty subjects, eight other people and seven schools; places were not attempted. Its response is in `opus-response.md`. Every identifier was resolved with `wbgetentities` on 7 October 2026 (`opus-scoring-raw.json`).

## The subjects

| # | Entry | Answer key | Opus | Verdict |
|---|---|---|---|---|
| 1 | Sharpe | Q459640 | Q459640 | correct |
| 2 | Williams | Q7287329 | Q7287329 | correct |
| 3 | Price | Q123279571 | Q123279571 | correct; noted the "Hamblyn" spelling |
| 4 | Archer | Q5534618 | Q5534618 | correct |
| 5 | Tibbits | none found | declined | agrees |
| 6 | Gorges | Q116445705 (pipeline) | Q121494224 | **a Wikidata duplicate**: "Edmond Gorges, South African politician (1872–1924)" and "Edmond Howard Lacam Gorges, colonial administrator in South West Africa (1872–1924)" are two items for one man. Opus also flagged the trap item Q5586263, an 18th-century Irish lawyer called Gorges Edmond Howard |
| 7 | Denton | Q19059378 | Q19059378 | correct |
| 8 | Wilkinson | Q4120852 | Q4120852 | correct |
| 9 | Prince | none found by vector search | Q47891631 Edward Ernest Prince, Canadian fisheries biologist, 1858–1936 | **correct, and new**: birth year and F.R.S.C. match; the MCP search had not surfaced it |
| 10 | Plumer | Q336040 | Q336040 | correct |
| 11 | Vaughan | none found | declined | agrees |
| 12 | Harris | Q5075044 | Q5075044 | correct; noted the entry's birth year (1858) disagrees with the item (1855) and resolved it on Christ's College and Newfoundland |
| 13 | Bland | Q20036709 | Q20036709 | correct; noted a redirect |
| 14 | Dyer | none found | declined | agrees |
| 15 | Wilson | Q20725021 | Q20725021 | correct; from a Wikisource author page, flagged as such |
| 16 | Anderson | none found | declined | agrees |
| 17 | Alldridge | Q16933745 | Q16933745 | correct |
| 18 | Marsh | Q1292947 | Q1292947 | correct |
| 19 | Belcher | Q5077823 | Q5077823 | correct |
| 20 | Clementi | Q839225 | Q839225 | correct; flagged the trap Q5056012, his uncle Cecil Clementi Smith, also a Straits governor |

**Result:** 16 of 16 identifiers resolve to the right person (one via a duplicate item). The four declines are the four the MCP search also finds nothing for. It added one correct identification the pipeline lacked (Prince), caught two near-miss traps, and flagged three OCR errors in the entries ("Cuthbert Peak Grant" for the Cuthbert Peek Award; "hurricane relic offr." for relief; an impossible "May to Apr., 1896").

## Other people and schools

All eight other people (Chamberlain, Churchill, Asquith, Lyttelton, Buxton, Selborne, Devonshire, J. H. Thomas) and all seven schools (Rossall, Queens' Cambridge, Trinity Cambridge, Harrow, Christ's Cambridge, Lincoln's Inn, Gray's Inn) resolve to the right items. Compare Gemini without tools on the same names: Chamberlain a Swiss footballer, Rossall a motocross rider, Lincoln's Inn a Spanish municipality.

## What this shows, set beside the other two columns

| | Gemini 3.8 Flash, no tools | Pipeline: vector search + gates | Opus 5.5 with retrieval |
|---|---|---|---|
| Person identifiers correct | 0 of 16 | 12 of 12 given; 8 left ungrounded, of which 4 have items | 16 of 16 given |
| Declined | 4 | 8 | 4 |
| Found that the others missed | | | Prince; a duplicate item for Gorges |
| Cost per entry | lowest | low, scales to 100,000 | highest; stopped at its tool limit before the places |

- The difference between zero and sixteen is not the model's reading of the biography. Both named the people correctly. It is whether the identifier came from a page or from memory.
- Retrieval with a strong model and a human-style search is the most accurate and the most expensive. The pipeline's gate is conservative by design (ties resolve to no link) and misses real items (Price, Wilson, Alldridge, Prince); those are what a review queue is for.
- Even retrieval needs the historian: Gorges has two items, and someone has to decide which to use and whether to merge them on Wikidata. Harris's birth year disagrees between the source and the item, and someone decided the match on the college and the colony.
