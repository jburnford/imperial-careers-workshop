# Timing of the grounding-test runs, 7 October 2026 (CST)

Times for the three chatbot runs are reconstructed from file modification times on Jim's machine, except the Astra start, which is Jim's estimate. Pasted results were saved within about a minute of arriving.

| Event | Time | Source |
|---|---|---|
| Twenty-entry file `bios.md` written | 08:28 | file mtime |
| Gemini 3.8 Flash (no tools) results pasted | ~08:33 | scoring file mtime 08:34 |
| Astra medium run started | ~08:35 | Jim's estimate |
| Opus 5.5 (web retrieval) first results pasted | ~08:44 | scoring file mtime 08:44 |
| Opus CSV `bios_wikidata_grounding.csv` downloaded | 08:46 | file mtime |
| Astra still running, no output | ~08:49 | Jim's report |
| Astra finished; `bios-grounded.json` downloaded | 09:02 | file mtime |

Elapsed: Gemini under 5 minutes from the earliest possible start; Opus first pass up to 16 minutes, with the CSV two minutes after that (the passes overlapped). Astra: about 27 minutes from Jim's estimated start to the downloaded file. Its own methodology block says it used public web search, Wikipedia sitelinks and web-retrieved Wikidata pages, not the API or a vector search, and did not consult the answer key. Prompt: to be recorded.
