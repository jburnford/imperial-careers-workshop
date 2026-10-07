"""Build review/cases.json for the browser exercise from the saved Imperial Careers outputs.

No network. Each case shows a source passage, a proposed record or link, the evidence for and against, and
asks for accept / reject / unresolved with a reason. The file carries a fingerprint (sha256 of the case
content) that the page stores with every decision, so answers cannot be attached to a different version.
"""
import json, hashlib
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
ex = {e['person_id']: e for e in json.loads((BASE / 'outputs/structure/audit-examples.json').read_text())}
bios = json.loads((BASE / 'outputs/ground-test/bios.json').read_text())
price = [b for b in bios if b['bio_id'] == 'col1905-p697b20'][0]['text']
brewster = json.loads((BASE / 'outputs/ground/brewster.json').read_text())['bio']['raw_text']
GH = 'https://github.com/jburnford/col_matching'

cases = [
 dict(id='R1', kind='record', title='Blakely: does the structured record stand?',
      source_label='Colonial Office List 1905, Record of Services (OCR as delivered)',
      source_quote=ex['kgp_col1905-p614b11']['source'],
      source_url=f'{GH}/blob/master/docs/STRUCT_ERROR_CATALOG.md',
      proposal='Structured record: birth_year 1898; one event "Clk., atty.-gen.\'s officer", place "B. Honduras", year_start null.',
      evidence_for=['The record was produced by the production prompt, which says: birth_year only if explicitly printed; NEVER infer from the earliest career date.',
                    'The place and the position are present and recognisable.'],
      evidence_against=['The entry prints no "B." clause. The only date is the appointment, "Apl., 1898".',
                        '"off." is office, not officer.', 'The event has no year, and the year that was there went into the wrong field.'],
      question='Accept the record as data?'),
 dict(id='R2', kind='record', title='Balmer: the last posting\'s place',
      source_label='Colonial Office List 1936, Record of Services (OCR as delivered)',
      source_quote=ex['kgp_col1936-p832b11']['source'],
      source_url=f'{GH}/blob/master/docs/STRUCT_ERROR_CATALOG.md',
      proposal='Event 4: position "senior deputy P.M.G.", place "do.", year 1935, place_inherited true.',
      evidence_for=['That is what the clause prints.', 'The record flags the place as inherited, so a downstream pass could resolve it.'],
      evidence_against=['The prompt says a clause with no place carries over the previous clause\'s place. "do." is the printed form of exactly that; the model copied the abbreviation instead of applying the rule.',
                        'Grounding "do." finds nothing; the event stays off the map unless someone resolves it.'],
      question='Accept the event with place "do."?'),
 dict(id='R3', kind='identity', title='ABERY and CARBERY: one person?',
      source_label='Dedup cluster from the Record of Services, 1886 and 1897 editions',
      source_quote='ABERY, Joseph; hon: M.B.C.M; career: 1867 Ceylon Assistant colonial surgeon (1897 edition only)\nCARBERY, Joseph; hon: M.B.C.M; career: 1867 Ceylon Assistant colonial surgeon (1886, 1889, 1890, 1894, 1896, 1897 editions)',
      source_url=f'{GH}/blob/master/docs/DEDUP_LLM_METHOD.md',
      proposal='Merge the two biographies into one person.',
      evidence_for=['Same forename, same qualification, one identical dated event (1867, Ceylon, assistant colonial surgeon).',
                    'ABERY is a plausible OCR garble of CARBERY (two characters lost at a line start).', 'ABERY appears in one edition; CARBERY in six, including that one.'],
      evidence_against=['The surnames differ.', 'A single shared event is thin evidence for two men with a common forename.'],
      question='Accept the merge?'),
 dict(id='R4', kind='identity', title="A'BECKETT and BECKETT: one person?",
      source_label='Dedup cluster from the Record of Services, 1909–1918 and 1948–1949 editions',
      source_quote="A'BECKETT, THOMAS; b.1836; hon: KNT. BACH/1909; career: 1859 called to the Bar, Lincoln's Inn | 1860 to Victorian Bar | 1886 Victoria puisne judge\nBECKETT, Thomas Rumbold; b.1898; ed. Judd Sch., Tonbridge and Faraday House, Lond.; hon: A.M.I.E.E; career: 1924 Nigeria asst. tel. engnr. | 1940 Nigeria div. engnr | 1948 Nigeria asst. engnr.-in-ch., posts & tels",
      source_url=f'{GH}/blob/master/docs/DEDUP_LLM_METHOD.md',
      proposal='Merge the two biographies into one person.',
      evidence_for=['Same forename Thomas; surname suffix matches; the apostrophe could be OCR noise.'],
      evidence_against=['Birth years differ by 62 years, and the careers also conflict. The decision does not rest on a birth-year discrepancy alone.',
                        'A Victorian judge knighted in 1909 and a Nigerian telegraph engineer of 1948 share no event, place, honour or education.'],
      question='Accept the merge?'),
 dict(id='R5', kind='place', title='"Union of S. Africa" is Q5155572?',
      source_label='Place-grounding cache, Colonial Office List graph (rows for the surface "Union of S. Africa", "S. Africa", "S.A.")',
      source_quote='place: "Union of S. Africa"; query: "South Africa"; match_type: manifest (containment); qid: Q5155572; count: 1,062 events',
      source_url=f'{GH}/blob/master/docs/REVIEW_2026-09-03.md',
      proposal='Ground the surfaces "Union of S. Africa", "S. Africa" and "S.A." to Q5155572.',
      evidence_for=['The manifest join matched the string "South Africa" inside the item\'s name.', 'The label looked right in the table.'],
      evidence_against=['Q5155572 is the British South Africa Company\'s territory, which is Rhodesia; its seat is Harare.',
                        'Q193619, Union of South Africa (1910–1961), exists and is what the surface names.', 'On the atlas, 960 events and 572 arcs sat at Harare.'],
      question='Accept the grounding?'),
 dict(id='R6', kind='place', title='Brewster\'s "Victoria" is the Colony of Victoria?',
      source_label='Colonial Office List 1918, Record of Services (OCR as delivered)',
      source_quote=brewster,
      source_url=f'{GH}/blob/master/KG_FIXES_TODO.md',
      proposal='Ground "Victoria" in "defeated by Sir Richard McBride, in Victoria, 1912" (graph events: legislative ass. for Victoria, 1912 and 1916) to Q56850459, Victoria (Colony), Australia, as the cache does for the bare surface.',
      evidence_for=['Most occurrences of the bare surface "Victoria" in the corpus are the Australian colony, and the cache is keyed on the surface string.'],
      evidence_against=['Every other clause in the entry is British Columbia: Alberni, "removed to B. Columbia", premier of B. Columbia.',
                        'Victoria is the capital of British Columbia and an electoral district; McBride was its premier.',
                        'The atlas showed a British Columbia premier with a seat in Melbourne.'],
      question='Accept the grounding for this mention?'),
 dict(id='R7', kind='identity', title='Ferdinando Hamlyn Price is Q123279571?',
      source_label='Colonial Office List 1905, Record of Services (OCR as delivered); Wikidata item read 7 October 2026',
      source_quote=price,
      source_url='https://www.wikidata.org/wiki/Q123279571',
      proposal='Link the person to Q123279571, "Ferdinando Hamblyn Price", alias "Ferdinando Hamlyn Price", born 25 May 1855, died 10 February 1942, described (in Tamil only) as a Sri Lankan politician. No career statements on the item.',
      evidence_for=['The name is rare and matches, with the alias covering the spelling.', 'Born 1855 fits an open scholarship in 1875 and a Ceylon writership in 1878.',
                    '"Sri Lankan politician" fits three terms as mayor of Colombo.'],
      evidence_against=['The item has no statements beyond dates; nothing on it says Ceylon, Colombo or mayor.', 'The pipeline\'s conservative matching gate rejected the match because the name spelling differed.'],
      question='Accept the identity?'),
]
# Hold this case back until the final exercise. Evidence checked with wbgetentities.
cases.append(dict(
    id='R8', kind='identity', title="Harris: a supported identity with a disputed birth year?",
    source_label='Colonial Office List 1927, entry col1927-p935b5; retrieved candidate checked 7 October 2026',
    source_quote="HARRIS, SIR CHARLES ALEXANDER ... B. 1858; scholar, prizeman, and Porteus medallist of Christ's Coll., Camb.; ... gov. and c. in c., Newfoundland, 1st Nov., 1917; assumed govt., 17th Dec., 1917; ret., 1922. [Excerpt from the OCR; omissions marked.]",
    source_url='../outputs/ground-test/harris-evidence.json',
    proposal="Link the entry to the retrieved Charles Alexander Harris item, Q5075044. Keep birth_year_as_printed: 1858, record the item's 1855 separately, and flag the disagreement for review.",
    evidence_for=["The full name, Christ's College and the office of Governor of Newfoundland agree.",
                  "The proposal preserves the source reading and records the conflict instead of silently choosing a birth year."],
    evidence_against=["The birth years differ by three years. The OCR excerpt cannot establish whether the discrepancy began in scanning, printing or the external record.",
                      "The item and this entry may share an underlying source; agreement is not necessarily independent corroboration."],
    question='Accept the identity link while leaving the birth year disputed?'))
PRINCIPLE = {'R1': 'Structure', 'R2': 'Structure', 'R3': 'Clean', 'R4': 'Clean', 'R5': 'Ground', 'R6': 'Ground', 'R7': 'Ground', 'R8': 'Ground and source criticism'}
for c in cases:
    c['principle'] = PRINCIPLE[c['id']]
    c['optional'] = c['id'] not in {'R1', 'R3', 'R8'}
# Two familiar decisions, then one fresh case; retain the rest for further practice.
cases.sort(key=lambda c: ['R1', 'R3', 'R8', 'R2', 'R4', 'R5', 'R6', 'R7'].index(c['id']))
payload = json.dumps(cases, ensure_ascii=False, sort_keys=True).encode()
out = {'title': 'Three decisions, then further practice: Imperial Careers', 'built': '2026-10-07', 'cases': cases, 'fingerprint': hashlib.sha256(payload).hexdigest()[:12]}
(BASE / 'review/cases.json').write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n')
print('wrote', len(cases), 'cases, fingerprint', out['fingerprint'])
