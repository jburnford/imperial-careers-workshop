"""Build review/cases.json for the browser exercise from the research packet and the candidate tables.

No network. Each case shows a source passage, a proposed record or link, the evidence for and against, and
asks for accept / reject / unresolved with a reason. The file carries a fingerprint (sha256 of the case
content) that the page stores with every decision, so answers cannot be attached to a different version.
"""
import json, hashlib
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
SRC = BASE / 'research/trimen-network/sources'
S = {sid: json.loads((SRC / f'{sid}.json').read_text()) for sid in ['S01', 'S03', 'S04', 'S05']}
scan = {sid: S[sid]['pages'][0]['viewer_url'] for sid in S}

def quote(sid, text, use_transcription=False):
    body = S[sid]['transcription'] if use_transcription else S[sid]['text']
    assert text in body, (sid, text)
    return text

cases = [
 dict(id='R1', kind='identity', title='Is "Dr. Trimen" / "HENRY TRIMEN" the Wikidata item Q2462643?',
      source_label='S05, December 1883, p. 453 (Trimen\'s cover letter)',
      source_quote=quote('S05', 'Royal Botanic Gardens, Peradeniya, 21st Nov. 1883.'),
      source_url=scan['S05'],
      proposal='Link the local record `henry` to Wikidata Q2462643 (Henry Trimen, British botanist, 1843–1896) and to Colonial Office List person kgp_col1889-p554b20.',
      evidence_for=['Signed in full "HENRY TRIMEN" with the Peradeniya address (S06).',
                    'Colonial Office List 1883–1896: "director Royal Botanical Gardens, Ceylon, Feb., 1880".',
                    'Wikidata item retrieved 2026-10-06: born 1843, died 1896, occupations include botanist.'],
      evidence_against=['A brother, Roland Trimen (Q932702), appears in both collections; "Dr. Trimen" alone does not distinguish them.',
                        'The research pipeline made this link by rule; no human has recorded a decision.'],
      question='Accept the identity for the 1883 mentions signed from Peradeniya?'),
 dict(id='R2', kind='relationship', title='Did Howard analyse bark from the illustrated tree?',
      source_label='S04, July 1883, p. 66 (editor\'s note, then Agar\'s letter)',
      source_quote=quote('S04', 'Mr. Howard himself having given testimony to that effect after having analyzed the bark.—Ed.]') + '\n[...]\n' +
                   quote('S04', 'The bark of some of these trees was sent home by Mr. Campbell for analysis to Mr. Howard, who pronounced it to be Ledgeriana bark') + '\n[...]\n' +
                   quote('S04', 'I have also in my possession the bark from the tree itself, but taken when it was dying.'),
      source_url=scan['S04'],
      proposal='Extracted relationship: `howard` analysed_bark_from `illustrated_tree` (the tree sketched for Dr. Trimen\'s work).',
      evidence_for=['The editor\'s headnote says Howard analysed "the bark" of the tree Trimen figured.'],
      evidence_against=['Agar says the bark sent to Howard came from "some of these trees" at Mahanilu, a group the illustrated tree belonged to.',
                        'Agar says the bark from "the tree itself" is in his own possession, taken when it was dying.',
                        'The headnote is the editor\'s gloss; the letter is the evidence.'],
      question='Accept the relationship as extracted?'),
 dict(id='R3', kind='reading', title='Does the OCR reading of the trees\' condition stand?',
      source_label='S04, July 1883, p. 66 (OCR text as delivered)',
      source_quote=quote('S04', 'The trees were only about 4½ years old from the time the plants were put out, and were now in a full condition and in flower.'),
      source_url=scan['S04'],
      proposal='Extracted record: the trees at Mahanilu were "in a full condition and in flower" in June 1883.',
      evidence_for=['That is what the OCR text says.', 'Extraction run A kept it as printed but flagged it as an uncertain reading and guessed "in full bloom".'],
      evidence_against=['Open the scan (link above, right-hand column, last paragraph) and read the sentence.'],
      question='Accept the reading as data?'),
 dict(id='R4', kind='identity', title='Is there a Wikidata item for Walter Agar?',
      source_label='S04, July 1883, p. 66 (signature and dateline)',
      source_quote=quote('S04', 'Lawrence, June 22nd, 1883.') + ' [...] ' + quote('S04', 'WALTER AGAR.'),
      source_url=scan['S04'],
      proposal='Link `agar` to a Wikidata item.',
      evidence_for=['Vector search "Walter Agar" (2026-10-06), top hits: Q22336890 Walter Sarger, politician; Q12784009 Agar, family name; Q3568178 Wilfred Eade Agar, zoologist (1882–1951).',
                    'Vector search "Walter Agar Ceylon planter": Q31373350 Agaraelandhoor Maariyamman temple; Q177998 agar (thickening agent); Q918153 British Ceylon.'],
      evidence_against=['No hit is a Ceylon planter alive in 1883.', 'Absence from these searches does not prove no item exists.'],
      question='What should happen to the record `agar`?'),
 dict(id='R5', kind='concept', title='Is "C. pubescens How." the plant Wikidata calls Cinchona pubescens (Q164574)?',
      source_label='S01, July 1881, pp. 114–115 (Howard\'s letter)',
      source_quote=quote('S01', 'I find that I am credited with having created a new species of Cinchona, the "*C. pubescens* How."'),
      source_url=scan['S01'],
      proposal='Link every occurrence of "C. pubescens How." to Q164574 Cinchona pubescens.',
      evidence_for=['The name string matches the accepted species name.', 'Kew\'s Plants of the World Online treats C. succirubra as a synonym of C. pubescens today.'],
      evidence_against=['Howard\'s letter is a disclaimer: he says he did not create a species under this name and that the plants so called are something else.',
                        'Mapping the rejected usage to the accepted species erases what the letter is about.'],
      question='Accept the link for this usage?'),
 dict(id='R6', kind='identity', title='Are "Mr. T. Christy" and "THOS. NORTH CHRISTIE" the same person?',
      source_label='S03, July 1883, p. 37 (Christie\'s letter)',
      source_quote=quote('S03', "When Mr. Howard goes on to identify by these characteristics Mr. T. Christy's Bolivian calisaya seedlings as true Ledgerianas, his bases are as reliable as those by which a gipsy foretells your fortune."),
      source_url=scan['S03'],
      proposal='Merge the records `christie` (the letter\'s author, St. Andrew\'s, Maskeliya) and the "Mr. T. Christy" he mentions into one person.',
      evidence_for=['Same initial; the surnames differ by one letter, well within OCR error.'],
      evidence_against=['The author criticises Mr. T. Christy\'s seedlings in the third person.', 'The signature reads "THOS. NORTH CHRISTIE" and the dateline is a Ceylon estate; the Christy seedlings are "Bolivian" and come via Howard in England.',
                        'Vector searches for both names (2026-10-06) return no plausible item for either.'],
      question='Accept the merge?'),
]
PRINCIPLE = {'R3': 'Clean', 'R2': 'Structure', 'R1': 'Ground', 'R4': 'Ground', 'R5': 'Ground (extra)', 'R6': 'Ground (extra)'}
ORDER = ['R3', 'R2', 'R1', 'R4', 'R5', 'R6']
cases.sort(key=lambda c: ORDER.index(c['id']))
for c in cases:
    c['principle'] = PRINCIPLE[c['id']]
    c['optional'] = c['id'] in ('R5', 'R6')
payload = {'title': 'Trimen review exercise', 'built': '2026-10-06', 'cases': cases}
digest = hashlib.sha256(json.dumps(cases, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:12]
payload['fingerprint'] = digest
out = BASE / 'review/cases.json'
out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + '\n')
print('wrote', out, len(cases), 'cases, fingerprint', digest)
