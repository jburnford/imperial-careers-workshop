# Trimen, cinchona, and the expansion of a research question

Working research packet, 6 October 2026. Prepared for the AI and History workshop. This is a separate, assistant-curated draft for Jim's review; it does not update Tropical's production identities or the RA's decisions.

The starting question is concrete: who is Henry Trimen connected to in *The Tropical Agriculturist*, and what can we establish about those connections? The answer leads from a dispute with John Eliot Howard to planters, seed suppliers, botanical gardens, pharmaceutical manufacturing, and correspondence. Shared identifiers help connect the records, but the historical claims need their own evidence.

## The passages to use

Seven frozen article records are in `sources/`. Each retains the Tropical article ID, OCR text, page links, and source segments. The July 1883 opening on scan n44 has been visually inspected. Other passages have been read in OCR and still need comparison with their scans before presenting a final transcription. The parent search file contains 72 articles with both surnames; that is a discovery set, not 72 verified relationships between Henry Trimen and John Eliot Howard.

| Source | Passage | Why it matters |
|---|---|---|
| S01 | [“Mr. Eliot Howard Extinguishing C. Pubescentis How.”, July 1881, pp. 114–115](https://archive.org/details/tropicalagricult1188ceyl/page/n139/mode/1up) | Howard disclaims having created a species under this name. The editorial also criticizes Clements Markham's account of hybrid parentage. |
| S02 | [“The Wars of the Quinologists”, July 1883, pp. 27–28](https://archive.org/details/tropicalagricult18831884colo/page/n44/mode/1up) | The journal explicitly presents a dispute among Howard, Trimen, and Moens. A short opening for the workshop. |
| S03 | [“Dr. Trimen's Ledgeriana: Mr. T. N. Christie to the Rescue”, p. 37](https://archive.org/details/tropicalagricult18831884colo/page/n54/mode/1up) | Christie's letter of 7 June 1883 traces the illustrated plant through McIvor's seed, his nursery, and Agar's planting. This is Christie's asserted provenance. |
| S04 | [“Dr. Trimen's Typical Ledgeriana Tree”, p. 66](https://archive.org/details/tropicalagricult18831884colo/page/n83/mode/1up) | Agar's letter of 22 June 1883 distinguishes the illustrated tree from other trees whose bark Campbell sent to Howard. Excellent material for checking a model's proposed relationship. |
| S05 | [“The Cinchona Calisaya (or Ledgeriana) Discussion”, December 1883, p. 453](https://archive.org/details/tropicalagricult18831884colo/page/n470/mode/1up) | Howard's quoted letter and Trimen's cover letter connect people, publications and places. Trimen writes from Royal Botanic Gardens, Peradeniya on 21 November. |
| S06 | [“The Botany of Cinchona Ledgeriana”, December 1883, pp. 453–455](https://archive.org/details/tropicalagricult18831884colo/page/n470/mode/1up) | Trimen's argument, dated 29 October, reports competing identifications and distinguishes botanical characters from chemical yield. |
| S07 | [“History of Cinchona Culture in Ceylon”, April–June 1943, beginning p. 91](https://archive.org/details/tropical-agriculturist_april-june-1943_99_2/page/n34/mode/1up) | A retrospective account brings in Markham, Spruce, plant movements, Peradeniya and Hakgala. Publication date must remain separate from the events described. |

The direct Trimen–Howard connection is a published disagreement, not merely article co-occurrence. Trimen's reply goes to the editor of the *Pharmaceutical Journal* and is forwarded for publication in Ceylon; it should not be recoded as a private letter addressed to Howard.

## Grounding people, plants and places

`entities.csv` and `entities.json` contain 49 local entities, with candidate QIDs where authority records have been checked. `record_checked` means that the Wikidata item was retrieved and examined. It does not mean that every historical occurrence of that name has been matched, that every statement on the item is trustworthy, or that a human has approved the proposal. Every human-review field remains pending.

The people include Henry Trimen (Q2462643), John Eliot Howard (Q3181423), Clements Markham (Q507802), Moens (Q21340893), McIvor (Q21520254), Charles Ledger (Q963818), Weddell (Q983408), Joseph Dalton Hooker (Q157501), Fitch (Q1102060), and Richard Spruce (Q1349394). The correspondence adds Roland Trimen (Q932702), Thiselton-Dyer (Q2065240), and Daniel Morris (Q20733957). Surname-only assignments remain proposals supported by context.

Thomas North Christie and Walter Agar retain local identifiers. No suitable Wikidata match was established in the searches performed. Absence from those results does not demonstrate that an item does not exist. Christie must not be merged with Thomas Christy on spelling similarity. Moens's cached authority labels and aliases disagree about his given name, so the packet retains initials. Trimen's account also mentions an unnamed servant of Ledger; keeping a local record prevents that person's involvement from disappearing merely because the source supplies no personal name.

Royal Botanic Gardens, Peradeniya (Q3119056) is explicit in the 1883 cover letter. Peradeniya as a locality has a separate candidate, Q489744. Likewise, Kew's garden site and the research institution have distinct items. The bare word Hakgala in a catalogue address does not establish that the sender was inside the botanical garden. Estates such as St. Andrew's, Mahanillu and Yarrow remain local records without invented coordinates.

Howards and Sons (Q123413890) provides a possible industrial branch. The archive catalogue for collection ACC/1037 describes the firm's pharmaceutical business and its Stratford headquarters before the move to Ilford. This is external contextual evidence, kept distinct from the Tropical passages. [Howards and Sons archive catalogue](https://atom.aim25.com/index.php/howards-and-sons-chemists?sf_culture=en)

**West Ham is a useful correction to a model's reasoning.** The label “County Borough of West Ham” initially suggested that Q5177625 would be too late for the 1883 setting. Jim pointed out that the item includes the local board of health. Its statements explicitly cover that form from 1856 to 1886. The packet therefore retains the QID for West Ham local government, with the appropriate period and label. The county-borough start qualifier currently says 1 April 1899, while the municipal-borough end says 31 March 1889; these unreferenced statements require investigation. Accepting an identity link does not require accepting all attached dates. [Wikidata record](https://www.wikidata.org/wiki/Q5177625)

## Historical classification is part of the evidence

Some historical identifications may have been wrong. The data must preserve enough detail to examine that question: who identified which plant, under what name, when, and on what evidence? Trimen's claim that several differently named plants were botanically identical belongs in the dataset as his argument, rather than as an automatic correction to all earlier records.

`claims.csv` and `claims.json` contain 14 proposed relationships with exact OCR evidence, attribution and review notes. The illustrated tree and its neighbouring trees have separate local IDs. Agar says that bark from some trees went to Howard, while bark from the illustrated tree remained in his possession. An extraction that says Howard analysed the illustrated tree would overstate the evidence. The source's word “typical” also does not by itself establish nomenclatural type status.

There are three separate questions to retain:

1. Which name did a historical actor use?
2. Which specimen or group of plants did that actor identify with that name?
3. How does a current authority treat the name?

Kew's Plants of the World Online currently treats *Cinchona ledgeriana* as a synonym of *C. calisaya*, and *C. succirubra* as a synonym of *C. pubescens*. These treatments are recorded separately in `taxonomy.csv`; they do not settle whether Howard or Trimen correctly identified a particular historical tree. [Ledgeriana record](https://powo.science.kew.org/taxon/urn:lsid:ipni.org:names:746808-1), [succirubra record](https://powo.science.kew.org/taxon/urn:lsid:ipni.org:names:746904-1)

The 1881 Howard letter makes an especially useful case. It distinguishes a hybrid that people were calling “C. pubescens How.” from an already established species with different characters. Mapping both occurrences directly to Q164574 would erase the issue the letter discusses. A separate local historical-name record preserves it.

Bark, cinchona alkaloids and quinine also have separate records. Pure quinine and sulphate of quinine are not interchangeable measurements. The packet includes only a selection of the plant names Jim supplied; unexamined species, categories and taxonomy templates have not been inserted as if they were all participants in this dispute.

## Correspondence as the next research branch

`letters.csv` and `letters.json` transcribe 25 distinct catalogue entries supplied by Jim, spanning 1893–1896. Repeated display titles in the pasted list have been collapsed. There are 24 letters attributed to Henry: 23 to Thiselton-Dyer and one to Daniel Morris. One is attributed to Roland Trimen, writing to Thiselton-Dyer from 5 Lancaster Street on 31 December 1896.

These records establish catalogue-described correspondence, dates, origins, folios, and page/image counts. They do not establish what the letters discuss. The list is a selection, not a complete correspondence census. Repository URLs for individual entries have not yet been matched.

Jim also supplied [kdcas1413](https://plants.jstor.org/stable/10.5555/al.ap.visual.kdcas1413) and [kdcas1411](https://plants.jstor.org/stable/10.5555/al.ap.visual.kdcas1411). These are retained separately in `archival-leads.csv`. The records could not be retrieved during this check; their subjects and correspondence dates remain unverified. No association has been inferred from their sequential identifiers.

For the workshop, show this branch briefly as the next question opened by the research. Reading a whole correspondence collection belongs in the follow-up materials, not the hour's core exercise.

## Reuse and remaining preparation

Run `python3 scripts/build_trimen_workshop.py` from the workshop repository to rebuild the CSV and JSON files. It validates exact evidence strings, referenced local entities, unique correspondence IDs, and the presence of cached candidate authority records. `manifest.json` records the hash of the frozen search input. The public retrieval helper, `scripts/ground_trimen.py`, caches full Wikidata responses under `raw/`, including qualifiers, references and retrieval timestamps.

Before presenting, compare the selected exercise passage with its scan, review the proposed identities and claims, and attach a small Colonial Office List excerpt for Henry's career. Keep the broader research packet available on GitHub, but limit the participant exercise to a short passage and a few decisions. The packet is saved locally; this workspace is not yet a Git repository and nothing has been published.
