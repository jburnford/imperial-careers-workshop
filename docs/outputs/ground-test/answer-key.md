# Answer key: what the pipeline holds

`grounded` means the Imperial Careers person-grounding stage (vector search plus the zero-false-positive verification gates, tier A) linked this person. `not grounded` means the gates did not accept a link; it does not mean no Wikidata item exists. The MCP column is to be filled from a live lookup.

| # | Entry | Person id | Pipeline | QID | Wikidata label | MCP lookup (7 Oct 2026) |
|---|---|---|---|---|---|---|
| 1 | SHARPE, SIR ALFRED, K.C.M.G. (1903), C.B. (1897) | `kgp_col1928-p1170b6` | grounded | Q459640 |  | Q459640 read: Alfred Sharpe, b. 19 May 1853, d. 1935, governor, K.C.M.G. Confirmed. |
| 2 | WILLIAMS, RALPH CHAMPNEYS, C.M.G. (1901) | `kgp_col1917-p886b4` | grounded | Q7287329 |  | |
| 3 | PRICE, FERDINANDO HAMLYN | `kgp_col1913-p766b16` | not grounded |  |  | Vector search "Ferdinando Hamlyn Price ..." → Q123279571 Ferdinando Hamblyn Price (alias Hamlyn), b. 1855, d. 1942, description in Tamil only. A real item the pipeline missed (spelling). |
| 4 | ARCHER, SIR GEOFFREY FRANCIS, K.C.M.G. (1920), C.M.G. (1913) | `kgp_col1928-p986b18` | grounded | Q5534618 |  | |
| 5 | TIBBITS, ELWOOD D'ARCY | `kgp_col1931-p1151b5` | not grounded |  |  | Vector search: no plausible item in the top 50. |
| 6 | GORGES, SIR EDMOND HOWARD LACAM, K.C.M.G. (1919), C.M.G. (19 | `kgp_col1922-p805b16` | grounded | Q116445705 |  | |
| 7 | DENTON, SIR GEORGE CHARDIN, K.C.M.G. (1900), C.M.G. (1891) | `kgp_col1909-p700b19` | grounded | Q19059378 |  | |
| 8 | WILKINSON, RICHARD JAMES, C.M.G. (1912).  | `kgp_col1919-p898b10` | grounded | Q4120852 |  | |
| 9 | PRINCE, EDWARD ERNEST, F.R.S.C., &c | `kgp_col1917-p840b6` | not grounded |  |  | Vector search: no plausible item in the top 50 (one search). |
| 10 | PLUMER, FIELD-MARSHAL RT. HON. VISCOUNT, HERBERT CHARLES ONS | `kgp_col1919-p850b8` | grounded | Q336040 |  | |
| 11 | VAUGHAN, CHARLES STEWART | `kgp_col1921-p954b6` | not grounded |  |  | Vector search: no plausible item in the top 50. |
| 12 | HARRIS, SIR CHARLES ALEXANDER, K.C.M.G. (1917); C.B. (1904); | `kgp_col1927-p935b5` | grounded | Q5075044 |  | |
| 13 | BLAND, ROBERT NORMAN., C.M.G. (1910) | `kgp_col1920-p767b16` | grounded | Q20036709 |  | |
| 14 | DYER, THOS. THEODORE RODNEY | `kgp_col1913-p675b17` | not grounded |  |  | Vector search: no plausible item in the top 50. |
| 15 | WILSON, SIR HENRY FRANCIS, K.C.M.G. (1908), C.M.G. (1902).  | `kgp_col1932-p1075b5` | not grounded |  |  | Vector search → Q20725021 Henry Francis Wilson, barrister-at-law (1859–1937). Birth year matches (1859). A real item the pipeline missed. |
| 16 | ANDERSON, GEORGE BARTLET | `kgp_col1918-p677b9` | not grounded |  |  | Vector search → Q5536241 George Anderson, "accountant-general from England", but born 1760: rejected. No plausible item. |
| 17 | ALLDRIDGE, THOMAS J., F.R.G.S., F.Z.S., &c | `kgp_col1900-p513b22` | not grounded |  |  | Vector search → Q16933745 T. J. Alldridge, British colonial administrator, b. 1847. Supported. |
| 18 | MARSH, EDWARD HOWARD, C.B., C.M.G., M.V.O | `kgp_col1940-p999b18` | grounded | Q1292947 |  | |
| 19 | BELCHER, CHARLES FREDERIC, O.B.E. (1923), M.B.E. (1919), M.A | `kgp_col1948-p415b12` | grounded | Q5077823 |  | |
| 20 | CLEMENTI, SIR CECIL, K.C.M.G. (1926), C.M.G. (1916) | `kgp_col1931-p982b10` | grounded | Q839225 |  | |


Gemini 3.8 Flash, given the same twenty entries without tools, is scored in `gemini-scoring.md`: none of its sixteen person identifiers was correct. Claude Opus 5.5 with web retrieval is scored in `opus-scoring.md`: all sixteen correct, plus Prince.
