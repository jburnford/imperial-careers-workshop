---
description: Live grounding demo — search WikidataMCP for an official from the Colonial Office List, read the candidates' statements against the printed entry, and decide supported / unresolved / wrong
argument-hint: trimen | price | tibbits | <any name and context>
---

You are running a short, live demonstration for historians at the AI and History conference. Work visibly and briefly: the audience is watching the screen.

The person to ground: **$ARGUMENTS**

If the argument is `trimen`, `price` or `tibbits`, use the matching printed entry below. Otherwise treat the argument as a name with context and ask no questions; work from what is given.

**trimen** — *Colonial Office List*, 1889:
> TRIMEN, HENRY, M.B. (Lond.), F.R.S., F.L.S. —Formerly lecturer on botany at St. Mary's Hospital, London, 1867 to 1875; was senior assistant to department of botany, British Museum, 1869 to 1879; director Royal Botanical Gardens, Ceylon, Feb., 1880; author of numerous works and papers on pure and applied botany.

**price** — *Colonial Office List*, 1905 (record kgp_col1913-p766b16):
> PRICE, FERDINANDO HAMLYN.—Ed. at Rossall, and Queen's Coll., Camb.; open scholarship, 1875; writer to the govt. of Ceylon, Mar., 1878; … ag. chmn. mun. coun. and mayor, Colombo, Sept. to Dec., 1889; … chmn. mun. coun., and mayor, Colombo, June, 1896; sent on special duty to Bombay, Feb., 1897; ag. govt. agt., Sabaragamuva, Apr., 1898; again mayor, Colombo, Oct., 1898; spec. serv. as asst. govt. agt., W. prov., Nov., 1900; govt. agt., prov. of Uva, Oct., 1901.

**tibbits** — *Colonial Office List*, 1913 (record kgp_col1931-p1151b5):
> TIBBITS, ELWOOD D'ARCY.—B. 1880; ag. 4th clk., col. sec.'s off., Antigua, Jan., 1899, to Nov., 1900 …; ag. clk. to administr. and clk. to exec. coun., Dominica, 2nd Aug., 1905, to 5th Apr., 1906; 3rd clk., col. sec.'s off., Antigua, 23rd Sept., 1906; 2nd clk., clk. to exec. and legis. couns., and supt. of govt. printing off., Antigua, 11th Oct., 1911; … ag. ch. clk. on abolition of off. of asst. col. sec., 20th June, 1912.

Steps:

1. **Retrieve.** Call `mcp__wikidata__search_items` once with the name plus two or three career words (for example "Henry Trimen botanist Ceylon Peradeniya"). Show the top five results as a short list.
2. **Read.** For the one or two plausible candidates, call `mcp__wikidata__get_statements`. Show only the statements that bear on identity: instance of, birth and death dates, occupation, positions held, education, places.
3. **Decide.** Compare them with the printed entry in a small table: evidence that agrees, evidence that conflicts, evidence missing. Then give one verdict:
   - **Supported** — the whole biography agrees; record the QID with the evidence and today's date.
   - **Unresolved** — nothing plausible, or too little to decide; keep the local record and say what search was run. Do not claim that no item exists.
   - **Wrong** — name a plausible-looking candidate that is not this person and say why.
   Where it helps the audience, point out a near miss in the results (for example a different botanist born the same year).

Rules: never write a QID from memory; every identifier must come from a tool result in this session. OCR can misread names and dates, so a single spelling or date discrepancy does not by itself rule a candidate out; conflicting careers do. Keep the whole answer short enough to read on a projected screen. If the MCP tools fail, say so and stop; the saved answer key is at `outputs/ground-test/answer-key.md`.
