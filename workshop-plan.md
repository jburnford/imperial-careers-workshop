# AI and History Workshop Plan

Working draft, 6 October 2026, revised the same evening after the participant site and saved outputs were built. Prepared for Jim Clifford and collaborators. The site is in this repository (`quarto render` builds `docs/`); see `README.md` for the layout.

This workshop will show how historians can use models and coding agents to turn existing OCR text into structured, connected research data. Models will do substantial work: propose a structure, extract records, write processing code, retrieve candidate identities, and prepare results for inspection. The historian will define what the records mean, check consequential decisions against evidence, and direct revisions before expanding the process.

The session will use a small example from *The Tropical Agriculturist*, with the Colonial Office List records in `col_matching` providing a collection to connect it to. Participants should leave understanding how to delegate this work and how to recognize where historical judgment is essential.

## Conference setting

The published session is **Cleaning and Structuring Historical Data: A Working Session**, Thursday 15 October 2026, 1:30–2:30 p.m. in Baltimore, Room 110 at the SNF Agora Institute, Johns Hopkins University. The room is listed with a capacity of 25. The conference says all sessions will stream through Zoom. The exact arrangements for receiving questions from remote participants still need to be established. [Conference program and FAQ](https://proflouishyman.github.io/ai_conference_2026/index.html)

The workshop must fit one hour and work for people with different levels of technical experience. The common activity will be inspecting evidence and making a decision. Participants who arrive with a working coding agent can also run the example. Following the session should not depend on completing software installation during it.

## Agreed scope

- Begin with existing OCR text. Other sessions cover OCR production. Page images remain available when participants need to check a reading.
- Demonstrate the amount of work models can do, including building the scripts and review tools that make a project manageable.
- Make human review part of the workflow throughout, including checking apparently successful results.
- Use Wikidata carefully as a source of shared identifiers. Preserve local records, source evidence, and uncertainty.
- Use `col_matching` as the mostly complete project and Tropical as the developing project.
- Put the workshop materials on GitHub so participants in the room and online can follow the same sequence and return to it later. Done as a Quarto site rendered to `docs/` in this repository; GitHub Pages serves from that folder.
- Reuse the Wikidata grounding and verification material from the earlier Claude Code workshop. That workshop is a separate project; its GIS exercises and LINCS conversion are not the basis of this session.
- Do not cover CIDOC-CRM, RDF conversion, or formal ontology training.

## What participants should learn

By the end of the session, participants should be able to describe a small extraction task to a model, inspect the resulting records against the source, and distinguish a candidate identity from a supported match. They should see how a correction to one result can become a better rule, check, or review process for the rest of a collection.

The practical output is a small CSV or JSON dataset with source references, proposed links, and recorded review decisions. A useful historical connection between collections will demonstrate why these steps matter.

## Projects and materials

| Resource | Role in the workshop | Preparation needed |
|---|---|---|
| Tropical article text and page references | The continuous example, beginning after OCR | Select a few short passages and preserve their source references |
| Tropical entity extraction and person profiles | Examples of model output, normalization, uncertainty, and review | Freeze a small snapshot and distinguish automated suggestions from human decisions |
| `col_matching` person and career records | An existing dataset to search and connect to Tropical | Export only the relevant candidate records and career evidence |
| Imperial Careers atlas | A brief demonstration of what structured and connected data enables | Select one relevant view or career; keep the opening demonstration short |
| Empire Evolution paper | Methodological background on verifying QIDs, historical scope, and using visualizations for review | Select one concise example if needed to explain a grounding problem |
| Earlier Claude Code workshop | Reusable grounding instructions and verification lessons | Adapt only the relevant material and check any setup instructions before reuse |

Tropical already has code for matching person profiles against the Colonial Office List graph (`ner/persons/colist/match_colist.py` in the Tropical repository). The workshop can therefore demonstrate a connection that exists in the research workflow. It does not need a new linkage project built for the event. For Henry Trimen the pipeline's current output is profile P000001 (863 extracted records, 779 articles), linked by rule to Q2462643 and to Colonial Office List person `kgp_col1889-p554b20`; see `outputs/06-connect/`.

Tropical is currently awaiting an RA's human review. Automated links and model adjudications must remain labelled as such until the corresponding human decisions are available. Workshop preparation should use a separate snapshot and preserve the RA's review material. Completing the research review is not a prerequisite for demonstrating why the review is needed.

## The worked example

Use one small Tropical example through all stages:

**Existing OCR text → proposed structure → extracted records → candidate identities → evidence review → revised processing → connection to another collection.**

Build the example around **Henry Trimen**, who appears in both collections. Begin with his career in the Colonial Office List, then ask: **who is Trimen connected to in the Tropical Agriculturist, and what evidence supports those connections?** The cinchona dispute with John Eliot Howard provides a concrete answer and opens further questions about people, plants, estates, botanical gardens, and pharmaceutical manufacturing.

The [Trimen research packet](research/trimen-network/README.md) now contains seven frozen Tropical articles, candidate authority links for people, plants and places, 14 attributed claims, and 25 correspondence catalogue records supplied by Jim. These are preparation materials, not a requirement to teach every branch. All human-review decisions remain pending.

**The exercise passage has been checked against the scan (6 October).** Two sentences of the OCR are wrong in ways that change Agar's meaning: "were now in a full condition and in flower" reads "were growing in a bad situation and not robust" on the page, and "I have by my prints of the leaves of some of the trees" reads "I have many plants from the seed of the specimen tree". The packet keeps the OCR as delivered in `text` and adds a scan-checked `transcription` with the differences listed. The exercise keeps the OCR, so that checking a reading against the page is one of the decisions.

Use “The Wars of the Quinologists” (July 1883, pp. 27–28) to introduce the published dispute. The participant exercise centres on Walter Agar's short letter, “Dr. Trimen's Typical Ledgeriana Tree” (p. 66). Ask a model to extract the people, trees, bark samples and actions. Then inspect whether it has wrongly made the illustrated tree the source of bark analysed by Howard. Agar distinguishes that tree from the group whose bark was sent for analysis. This makes the historian's intervention specific and consequential. Note that the conflation is invited by the journal's own editorial headnote, not only by the model: the review is a reading of the letter against the editor. Two cold rehearsal runs (`outputs/02-extract/`, Claude Sonnet 5.5 and Claude Fable 5.1) both avoided the conflation and both guessed wrongly at the damaged OCR sentences; the saved outputs therefore illustrate a careful record that must still be confirmed, and a flagged reading that only the page can settle.

Trimen's longer October 1883 argument, reprinted in December, supplies the disputed identifications. Preserve who classified which plants and under what name. Modern taxonomy is a separate layer: Kew currently treats C. ledgeriana as a synonym of C. calisaya, but that does not settle the identification of an individual tree in the historical debate. The 1881 letter in which Howard rejects the name “C. pubescens How.” offers an optional second exercise in why matching a name string to a QID can erase the source's meaning. Sources and current authority links are in the research packet.

Show the expansion briefly: Trimen and Howard lead to Moens, Christie, Agar, McIvor, Ledger and Markham; plants and samples move between estates, gardens and laboratories; Howards and Sons adds an industrial connection. The correspondence catalogue adds Thiselton-Dyer, Daniel Morris and Roland Trimen. Catalogue metadata supports correspondence links, while the letters' subjects remain to be read. These additional branches belong mainly in the GitHub follow-up materials.

West Ham (Q5177625, which covers the local board of health from 1856 as well as the later county borough) is a useful example of reading an item's statements rather than its label, but it does not occur in the Tropical passages. It stays in the research packet and the follow-up materials, not in the hour.

The exercise cases, selected and built (`review/cases.json`):

| Case | Decision | Teaching purpose |
|---|---|---|
| R1 | "Dr. Trimen" / "HENRY TRIMEN" is Q2462643 | A supported match: signature, Peradeniya address, Colonial Office List career, retrieved item |
| R2 | Howard analysed bark from the illustrated tree | The editor's headnote versus Agar's letter; the consequential error |
| R3 | The OCR reading "in a full condition and in flower" stands | Text versus page |
| R4 | A Wikidata item for Walter Agar | What "not found" means; keep the local record with the searches recorded |
| R5 | "C. pubescens How." is Q164574 | A name string versus what the source says about the name |
| R6 | "Mr. T. Christy" and "Thos. North Christie" are one person | Spelling distance versus the text's own distinction |

Henry and Roland Trimen stay separate; the Tropical pipeline also produced two phantom "Trimen" profiles (OCR errors for Howard and for Ledger, both confirmed against the scans) that step 6 uses to show why rare name forms deserve a look at the page. All cases are drawn from actual outputs or actual source text; none has been modified.

Keep the record structure small. The participant view needs the printed name, extracted role or activity, article date and source reference, proposed identity, supporting and conflicting evidence, and the review decision. Retain the original wording alongside normalized values.

Tropical's person-profile notes document a useful failure mode: a model can supply given names that do not appear in the article. The selected example is the name-evidence check itself, which in v1 accepted `Henry Trimen` as "printed" for a source reading `Mr. H. Trimen`, and the `Sir F. von Mueller` article whose profile carried `Ferdinand`. The v2 fix and its before/after are in `outputs/05-revise/`.

## Proposed running order

| Minutes | Activity | Purpose |
|---|---|---|
| 0–5 | Show a relevant Imperial Careers result and introduce the Tropical question | Establish the research payoff and the task |
| 5–20 | Ask the model to propose a structure, extract records, and save a reusable script and outputs | Demonstrate substantial delegation while keeping the source visible |
| 20–30 | Retrieve candidate identities from Wikidata and `col_matching`; assemble a compact review view | Make the evidence behind a proposed link inspectable |
| 30–45 | Review selected results together, identify a consequential problem, and direct a revision | Show how historical judgment changes the process and how to check the correction |
| 45–55 | Participants inspect a few fresh results and record decisions and reasons | Give both remote and in-person participants a manageable activity |
| 55–60 | Discuss questions and adapting the workflow to another collection | Leave participants with a practical next step |

Use saved outputs to keep the session moving when generation, retrieval, or troubleshooting takes too long. Every live stage needs a prepared checkpoint. If the session falls behind, shorten the opening tour and switch to a saved extraction or candidate set; protect the review and revision discussion.

## Model work and human decisions

| Stage | Work delegated to the model or code | Human contribution |
|---|---|---|
| Define the records | Read a sample and propose fields and examples | Decide what the research question requires and what the source can support |
| Extract and clean | Process text, retain source wording, normalize into separate fields, and report failures | Inspect examples for omissions, invented details, and changes of meaning |
| Propose identities | Retrieve candidates and collect relevant dates, occupations, places, and identifiers | Judge whether the proposed identity fits the historical context |
| Review | Build an evidence table or interface and identify conflicts | Accept, reject, or defer a match with a reason |
| Revise and expand | Search for related errors, update rules or prompts, and rerun a small batch | Check the repair and look for new errors before scaling up |

Also distinguish what a coding agent does from what an extraction model does. An agent can write the program that processes a collection; that program may combine ordinary code, model calls, and external lookups. Participants should be able to see which operation produced a result.

A second model can help identify problems, but its agreement is not independent historical confirmation. Review a mixture of uncertain cases and apparently successful matches. Handpicked workshop examples explain failure modes; they do not establish an accuracy rate for the full project.

## Wikidata grounding

Separate structuring from grounding. Give records local identifiers first. Add a Wikidata link only after retrieval and review provide appropriate support.

The review should distinguish three questions:

1. **Does the QID resolve to the retrieved entity?** Do not accept a Q-number supplied from model memory as a verified lookup.
2. **Is that entity the one described in this source?** Compare the name, entity type, dates, geography, and relevant activity. A real identifier can still refer to the wrong person or the wrong historical form of a place.
3. **What does the connection assert?** A shared identifier does not verify every statement about the entity. A modern political unit, geographical island, or broader historical entity may require a qualified relation or scope note rather than an exact identity claim.

Keep evidence for the match and record unresolved cases. If no suitable entity exists, retain a stable local identifier. Any later contribution to Wikidata would be separate work.

The Empire Evolution paper provides the background: coding agents proposed incorrect identifiers, visual inspection helped expose errors, and some matches needed notes explaining their historical scope. Shared identifiers allow datasets to connect while researchers retain responsibility for their own models and assertions. [Empire Evolution paper](https://working-papers-in-critical-search.github.io/paper-002-empire-evolution/)

## Draft demonstration prompts

These are starting points to rehearse against the selected sample, not tested final instructions.

**Propose a structure**

> Read these Tropical Agriculturist passages. Propose a small table for studying the people and activities mentioned. Show two example records before processing the rest. Preserve the printed wording and source references. Keep inferred information separate from what the text states. Use local record identifiers and do not add Wikidata identifiers yet.

**Build and run the extraction**

> Use the agreed fields to process this sample. Save the code, instructions, and output so we can inspect and rerun the work. Report failed records and uncertain readings. Do not expand a person's name unless the source provides the expansion; record any outside identification separately.

**Retrieve candidates**

> Look up candidate identities for these people using the configured Wikidata tools and the supplied Colonial Office List records. Save the retrieved evidence and lookup date. For each candidate, show what supports the match, what conflicts, and what is missing. Leave unresolved cases unresolved. Do not generate QIDs from memory.

**Prepare review**

> Make a review table showing each source passage, extracted record, candidate identities, and relevant evidence side by side. Provide accept, reject, and unresolved decisions with a place for the reviewer's reason. Preserve automated suggestions separately from human decisions.

**Revise the process**

> This example is wrong for the following historical reason: [explain]. Find other records that might have the same problem. Propose a correction and show which records it would affect. After we review the change, rerun a small batch and show both corrected cases and previously accepted cases that changed.

## GitHub materials and online participation

Create a dedicated workshop repository and a simple GitHub Pages site. The site is Quarto, rendered to `docs/`, matching the earlier workshop's approach. The participant pages open without a GitHub account.

The site should contain:

- A start page with the question, one-hour sequence, and clear prerequisites.
- A small downloadable source pack with citations and page links.
- Numbered steps with copyable prompts and a short explanation of the decisions involved.
- Saved outputs for every stage, including the initial mistakes and the revised results.
- A browser review exercise and a way to download participants' decisions.
- Worked answers explaining the evidence, including when more than one interpretation remains possible.
- Optional code and instructions for rerunning or extending the example after the session.
- A short guide to applying the approach to participants' own data.

The shared exercise should work from saved results without a model subscription or API key. Live model processing will run in the presenter's configured environment. Participants who want to run it themselves will need separate setup guidance, including account requirements and likely costs once the model and tools have been chosen. Public workshop files must not contain credentials.

Number the checkpoints and keep them visible during the demonstration. Give remote participants the same evidence and review task as those in the room. Confirm the Zoom question arrangement and whether someone can monitor remote questions; do not rely on being able to read the chat while presenting. Keep any recording dependent on the conference's arrangements.

## Preparation and dependencies

| Order | Work | Completion condition |
|---|---|---|
| 1 | Review Tropical's current state and pending RA task | Done 6 October: see the project review and its postscript |
| 2 | Select the historical question and cases | Done: six cases in `review/cases.json`, each with source text, scan link, candidate evidence and a worked answer |
| 3 | Freeze the teaching snapshot | Done: `research/trimen-network/manifest.json` records the source hash and scan checks; case file carries a fingerprint |
| 4 | Build the smallest complete example | Done for the saved path: two extraction runs, candidate tables, review page, revisions, connection |
| 5 | Prepare the GitHub site and fallback outputs | Built; needs Jim's review, a repository, and Pages enabled |
| 6 | Rehearse the hour | The workflow, review discussion, exercise, and questions fit the allotted time |
| 7 | Finalize and publish the workshop materials | Links, downloads, source credits, and setup guidance have been checked |

Proceed with sample selection and the teaching interface while the RA review is pending. Once the RA returns decisions, reconcile them with the relevant snapshot before presenting any examples as human-verified. If the review is still pending at the conference, label those examples as open research decisions and use separately checked teaching cases where an answer is needed.

The accompanying [Tropical project review](tropical-project-review-2026-10-06.md) informs the sample choice and preparation priorities. It is a technical and methodological review, not a replacement for the RA's historical adjudication. Its postscript records what changed in Tropical later the same day.

The current RA packet contains 100 profiles and 400 sampled mentions. Preserve that packet while the RA is working: its answer identifiers and browser storage are not protected against a regenerated sample. The project also needs a defined path for importing the downloaded answers, evaluating them against the frozen predictions, and applying reviewed corrections. Until that path exists, a completed review form does not itself update the research dataset. These are preparation dependencies, not reasons to interrupt the RA's historical assessment.

The project review found two concrete issues: the merge could attach a QID to a profile marked mixed or uncertain, and the name-evidence check accepted a full-name expansion when only initials were printed. Both were fixed in Tropical the same day (commit `acb5e9d`, "ner/persons v2", with regression tests), and the RA gold set was then frozen with a dataset fingerprint and located scan pages. The workshop uses the real before and after as its "revise the process" example rather than a hypothetical (see the review's postscript). The RA rating scale changed after the freeze; confirm which page version the RA has. Keep the full RA assignment separate from the short participant exercise.

## Decisions still to make

- Which coding agent, extraction model, and Wikidata lookup configuration will be demonstrated? (The saved runs used Claude Code with Claude Sonnet 5.5 and Claude Fable 5.1; retrieval used the WikidataMCP endpoint and Wikidata's entity-data endpoint.)
- How much live execution can the rehearsed workflow accommodate?
- Which RA-reviewed results, if any, will be available for the workshop snapshot?
- Who can monitor online questions, and how will participant decisions be discussed?
- Repository and URL: decided. `github.com/jburnford/trimen-workshop`, served by GitHub Pages from `docs/` at https://jimclifford.ca/trimen-workshop/ (first push 6 October 2026).
- Whether the exercise should show the OCR as delivered (current choice) or the corrected transcription, and whether to add a live extraction in the room on top of the saved runs.

The published description (session 10) reads:

> How to extract structured, linked open data from archival materials. Participants bring messy historical datasets — or work with provided examples — and practice cleaning source data, structuring it for reuse, and grounding entities in Wikidata so datasets can be interconnected across projects. Grounded in OCR and data-quality problems in historical archives, and new OCR tools built for a digital edition of the Encyclopaedia Britannica.

How the hour maps onto it: "provided examples" are the Trimen passages; "cleaning source data" is the OCR-versus-scan check (R3) and the name-evidence rule; "structuring it for reuse" is steps 2 and 5; "grounding entities in Wikidata so datasets can be interconnected" is steps 3 and 6. Two gaps: participants' own datasets get only the step 7 handout, and Britannica is not used. Suggested wording to offer the organizer if the description can still change:

> How to turn OCR text into structured, linked data without losing historical judgment. Working from provided examples (an 1883 dispute about a cinchona tree in *The Tropical Agriculturist*, connected to the *Colonial Office List*), participants watch a coding agent propose a structure, extract records, and retrieve candidate identities from Wikidata, then review the results against the page images, record decisions, and turn a correction into a rule. A browser exercise works in the room and on Zoom with no setup. Participants with their own messy datasets leave with a short guide to applying the same sequence.

## Reference materials

- [AHA conference listing](https://www.historians.org/event/ai-and-history-conference-2026/)
- [Conference program and online participation details](https://proflouishyman.github.io/ai_conference_2026/index.html)
- [Imperial Careers repository](https://github.com/jburnford/col_matching)
- [Tropical Agriculturist repository](https://github.com/jburnford/tropical-agriculturist)
- [Tropical article viewer](https://jimclifford.ca/tropical-agriculturist/viewer/)
- [Empire Evolution paper](https://working-papers-in-critical-search.github.io/paper-002-empire-evolution/)
- [Earlier workshop](https://jimclifford.ca/claude_code_workshop/workshop-event.html), for grounding and verification material only
