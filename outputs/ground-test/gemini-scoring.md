# Scoring Gemini 3.8 Flash on the twenty entries

**Prompt** (Jim Clifford, Gemini 3.8 Flash chat, no tools, 7 October 2026): "Parse these bios and ground the places, schools and people to Wikidata ids where possible." Full response in `gemini-response.md`. Every identifier in the response was resolved against Wikidata on 7 October 2026 (`wbgetentities`, labels and descriptions only; no disambiguation) and compared with the pipeline's tier-A grounding and the WikidataMCP lookups in `answer-key.md`.

## The subjects: the person each entry is about

| # | Entry | Pipeline or MCP | Gemini | Verdict |
|---|---|---|---|---|
| 1 | SHARPE, SIR ALFRED, K.C.M.G. (1903), C.B | Q459640 Alfred Sharpe, Commissioner and Consul-General for the Briti | Q15488812 Lepanthes oaxacana, species of plant | invented (not a person) |
| 2 | WILLIAMS, RALPH CHAMPNEYS, C.M.G. (1901) | Q7287329 Ralph Champneys Williams, Lieutenant Governor of Newfoundland (1848–192 | Q7287342 Ralph Clanton, American actor (1914-2002) | wrong person; number close to the right one |
| 3 | PRICE, FERDINANDO HAMLYN | Q123279571 Ferdinando Hamblyn Price | Q123284091 Seat support assembly, US patent 11447044 | invented (not a person); number close to the right one |
| 4 | ARCHER, SIR GEOFFREY FRANCIS, K.C.M.G. ( | Q5534618 Geoffrey Francis Archer, British ornithologist and colonial official ( | Q5534570 Geoffrey Drake, Production designer, Art director | wrong person; number close to the right one |
| 5 | TIBBITS, ELWOOD D'ARCY | — | — | declined (none found by MCP either) |
| 6 | GORGES, SIR EDMOND HOWARD LACAM, K.C.M.G | Q116445705 Edmond Howard Lacam Gorges, colonial administrator in South West Africa ( | Q1285098 Edith Mühlberghuber, Austrian politician | wrong person |
| 7 | DENTON, SIR GEORGE CHARDIN, K.C.M.G. (19 | Q19059378 George Chardin Denton, British military officer and governor of Gamb | Q1507119 Wilhelm Stollenwerk, German chemist (1891–1952) | wrong person |
| 8 | WILKINSON, RICHARD JAMES, C.M.G. (1912). | Q4120852 Richard James Wilkinson, British colonial governor (1867-1941) | Q7326830 Thoth, Egyptian deity | invented (not a person) |
| 9 | PRINCE, EDWARD ERNEST, F.R.S.C., &c | — | Q56000088 Didier Balicevic | wrong person |
| 10 | PLUMER, FIELD-MARSHAL RT. HON. VISCOUNT, | Q336040 Herbert Plumer, 1st Viscount Plumer, British Army general and High Commissioner of | Q335198 Kantarō Suzuki, 29th Prime Minister of Japan (1868-1948) | wrong person; number close to the right one |
| 11 | VAUGHAN, CHARLES STEWART | — | — | declined (none found by MCP either) |
| 12 | HARRIS, SIR CHARLES ALEXANDER, K.C.M.G.  | Q5075044 Charles Alexander Harris, British colonial administrator | Q5075037 Charles Alexander, Canadian politician | wrong person; number close to the right one |
| 13 | BLAND, ROBERT NORMAN., C.M.G. (1910) | Q20036709 Robert Norman Bland, British colonial administrator | Q110629739 MISSING | invented (no such item) |
| 14 | DYER, THOS. THEODORE RODNEY | — | — | declined (none found by MCP either) |
| 15 | WILSON, SIR HENRY FRANCIS, K.C.M.G. (190 | Q20725021 Henry Francis Wilson, British barrister-at-law (1859-1937) | Q5721528 Fulad Kola, village in Qaem Shahr County, Mazandaran Prov | invented (not a person) |
| 16 | ANDERSON, GEORGE BARTLET | — (the MCP candidate Q5536241 is a George Anderson born 1760; rejected) | — | declined (none found) |
| 17 | ALLDRIDGE, THOMAS J., F.R.G.S., F.Z.S.,  | Q16933745 T. J. Alldridge, British colonial administrator | Q64201321 Chapter 12 Bankruptcy Case Files (NAID 74627929), series in the National Archives and Records A | invented (not a person) |
| 18 | MARSH, EDWARD HOWARD, C.B., C.M.G., M.V. | Q1292947 Edward Marsh, British polymath (1872–1953) | Q1292523 Edward Henry Howard, English Catholic archbishop and cardinal (182 | wrong person; number close to the right one |
| 19 | BELCHER, CHARLES FREDERIC, O.B.E. (1923) | Q5077823 Charles Frederic Belcher, Australian lawyer, author and amateur ornitho | Q5077864 Apostolepis nigroterminata, species of reptile | invented (not a person); number close to the right one |
| 20 | CLEMENTI, SIR CECIL, K.C.M.G. (1926), C. | Q839225 Cecil Clementi, British colonial administrator (1875–1947) | Q335607 Muhammad II of Ifriqiya, Aghlabid emir of Ifriqiya | wrong person |

**Result:** 0 of 16 identifiers correct. Six resolve to things that are not people (a plant, a patent, an Egyptian deity, an Iranian village, an archive series, a reptile); the rest are other people, from a Japanese prime minister to an Aghlabid emir. 7 are within a few thousand of the right number, which is what memory of an identifier looks like: the model has seen the number near the name and reconstructs it wrongly. Four entries were declined, and for all four the MCP search also finds nothing acceptable. Declining was the right answer there. The names and descriptions Gemini wrote for the people were right in every case. It knew who; it did not know the number.

## Places, schools and other people

Gemini gave 142 distinct identifiers for places, schools and other people. Resolving each and checking whether the Wikidata label matches the name Gemini attached to it (a loose test, counting modern entities as matches):

| Kind | Label matches | Of |
|---|---|---|
| Places | 38 | 104 |
| Other People Mentioned | 2 | 14 |
| Schools | 3 | 24 |

43 of 142, after removing five the loose test let through (Geelong Grammar School resolved to a performing-arts centre, Robert Gordon's College to a French jeweller, King George V to George VI, Frederic Cardew to an American musician, the University of Cambridge to the city). The matches are the famous items with small numbers: Mumbai Q1156, Paris Q90, Canada Q16, Barbados Q244, Singapore Q334, the Ethiopian Empire, Trinity College Cambridge. The failures are everything a historian of empire needs: Nyasaland is a disambiguation page, the Straits Settlements a Danish triathlete, the Cape Colony an Austrian goalkeeper, Joseph Chamberlain a Swiss footballer, Rugby School a Russian gymnast. Where it matched a place it often matched the modern one (Penang the Malaysian state, Victoria the state), the same error the pipeline had to fix.

## What this shows

- A chatbot reads the biography correctly and names the people and places correctly. Grounding is not a reading problem.
- Identifiers are not knowledge a language model has. They are strings it has seen near names. Famous, low-numbered items survive; the rest are reconstructed.
- The failure is silent. Every line of the response looks like the pipeline's output. Nothing in the text tells you which identifiers resolve.
- Retrieval with a tool, then reading the item, then a gate: that is the pipeline. Memory is not a lookup.

The raw resolutions are in `gemini-scoring-raw.json` and `gemini-nonsubject-check.json`.
