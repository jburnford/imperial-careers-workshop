# Claude Opus 5.5 with web retrieval, 7 October 2026: the twenty entries

Jim Clifford gave the twenty entries from `bios.md` to Claude Opus 5.5 in a chat with web search. The response is reproduced verbatim below. Scoring is in `opus-scoring.md`.

---

I got through the 20 subjects, most of the people named in the bios, and seven of the schools before hitting my tool limit. I haven't grounded any places yet. Every QID below comes from a Wikidata item page (or, in one case, a Wikisource author page) that turned up in search, not from memory.

**The 20 subjects (16 found, 4 not found)**

| # | Person | QID | Notes |
|---|---|---|---|
| 1 | Sir Alfred Sharpe | Q459640 | |
| 2 | Sir Ralph Champneys Williams | Q7287329 | |
| 3 | Ferdinando Hamlyn Price | Q123279571 | Item label spells it "Hamblyn" |
| 4 | Sir Geoffrey Francis Archer | Q5534618 | |
| 5 | Elwood D'Arcy Tibbits | — | No item found |
| 6 | Sir Edmond Howard Lacam Gorges | Q121494224 | **Trap:** Q5586263 is "Gorges Edmond Howard", an 18th-century Irish lawyer |
| 7 | Sir George Chardin Denton | Q19059378 | |
| 8 | Richard James Wilkinson | Q4120852 | |
| 9 | Edward Ernest Prince | Q47891631 | |
| 10 | Herbert Plumer, 1st Viscount Plumer | Q336040 | |
| 11 | Charles Stewart Vaughan | — | No item found |
| 12 | Sir Charles Alexander Harris | Q5075044 | Bio says born 1858; the item and Wikipedia say 1855. Same man (Christ's, Newfoundland) |
| 13 | Robert Norman Bland | Q20036709 | Q75659861 redirects here |
| 14 | T. T. R. Dyer | — | No item found |
| 15 | Sir Henry Francis Wilson | Q20725021 | From his Wikisource author page; I didn't see the item page itself |
| 16 | George Bartlet Anderson | — | No item found |
| 17 | Thomas Joshua Alldridge | Q16933745 | |
| 18 | Sir Edward Marsh | Q1292947 | |
| 19 | Sir Charles Frederic Belcher | Q5077823 | |
| 20 | Sir Cecil Clementi | Q839225 | **Trap:** Q5056012 is his uncle, Cecil Clementi Smith, also a Straits governor |

"No item found" means one or two searches turned up nothing. It doesn't prove no item exists. Price (Q123279571) only has an item because a Wikipedia article was written recently, so absence from older snapshots is plausible.

**Other people named in the bios**

| Mention (bio #) | Person | QID |
|---|---|---|
| J. Chamberlain / Mr. Chamberlain (15, 18) | Joseph Chamberlain | Q315999 |
| Mr. Winston Churchill (18) | Winston Churchill | Q8016 |
| Mr. Asquith (18) | H. H. Asquith | Q166714 |
| Mr. Lyttelton (18) | Alfred Lyttelton | Q3395941 |
| Mr. Buxton, M.P. (12) | Sydney Buxton, later 1st Earl Buxton | Q1645717 |
| Earl of Selborne (12) | William Palmer, 2nd Earl of Selborne | Q3643409 |
| Duke of Devonshire (18) | Victor Cavendish, 9th Duke | Q2411883 |
| Mr. J. H. Thomas (18) | James Henry Thomas | Q338294 |

I haven't retrieved QIDs for these:
- Sir F. Cardew (17), who has an English Wikipedia article.
- King George V (1, 10) and Edward VII (10).
- Empress Zauditu, i.e. Zewditu (4).
- "the Mullah", i.e. Mohammed Abdullah Hassan (4).
- "Major Gwynn" (4). My guess is Charles William Gwynn, but I haven't confirmed that.

**Schools (7 of about 21 grounded)**

| Mention (bio #) | Institution | QID |
|---|---|---|
| Rossall (2, 3) | Rossall School | Q5493652 |
| Queen's Coll., Camb. (3) | Queens' College, Cambridge | Q765642 |
| Trin. Coll., Camb. (8, 11, 15, 18) | Trinity College, Cambridge | Q332342 |
| Harrow (11) | Harrow School | Q1247373 |
| Christ's Coll., Camb. (12) | Christ's College, Cambridge | Q714717 |
| Linc.'s Inn / Lincoln's Inn (12, 15) | Lincoln's Inn | Q69482 |
| Gray's Inn (19) | Gray's Inn | Q157412 |

These are still to do:
- St Paul's School (13, 20)
- Cheltenham College (13)
- Trinity College Dublin (13)
- Rugby School (15)
- Robert Gordon's College, for "Gordon's Coll., Aberdeen" (16)
- Westminster School (18)
- Geelong Grammar School and Trinity College, Melbourne (19)
- Magdalen College, Oxford (20)
- Leeds Modern School, St Andrews, Edinburgh, and the Glasgow Royal Infirmary medical school (9)
- University of Cambridge (9, 18)
- University of Hong Kong (20)

Several of the subjects' Wikidata items already list some of these schools under "educated at", so those links can be cross-checked.

**Places: not started.** That's roughly 80 mentions, many abbreviated or misspelled by the OCR. These need normalising before lookup:
- "Sabaragamuva" is Sabaragamuwa; "Trincomalie" is Trincomalee; "Kegalla" is Kegalle.
- "Sunjei Ujong" is Sungei Ujong; "P.W." is Province Wellesley; "S. Settlers." / "S. Stts." is the Straits Settlements; "N. Sembilan" is Negeri Sembilan.
- "Terra del Fuego" is Tierra del Fuego; "Kwang Si" is Guangxi.

Two other OCR errors are worth recording:
- "Cuthbert Peak Grant" in bio 4 should be the Cuthbert Peek Award.
- "hurricane relic offr." in bio 14 should be "relief".

Bio 8 also has an impossible date range in the source ("May to Apr., 1896").

For your scoring, note that bios 6 and 20 each have a real, plausible wrong-person item next to the right one. A no-tools chatbot would most likely produce a "wrong QID" answer on exactly those two.

Do you want me to continue with the places and remaining schools in a follow-up and package everything as a JSON or CSV file keyed by entry ID?
