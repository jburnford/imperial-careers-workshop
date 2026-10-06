"""Build the candidate-evidence tables for the workshop from the cached Wikidata responses.

Reads only research/trimen-network/raw/*.json (full Wikidata entity dumps and WikidataMCP vector-search
results cached by scripts/ground_trimen.py). No network access. Writes outputs/03-candidates/.

A row here is retrieved evidence, not a decision. Every QID shown was fetched from Wikidata and the
retrieval timestamp is recorded; nothing is supplied from model memory.
"""
import json, csv, re
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
RAW = BASE / 'research/trimen-network/raw'
OUT = BASE / 'outputs/03-candidates'
OUT.mkdir(parents=True, exist_ok=True)

def load_entity(qid):
    d = json.loads((RAW / f'{qid}.json').read_text())
    e = d['response']['entities'][qid]
    def vals(p):
        return [c['mainsnak'].get('datavalue', {}).get('value') for c in e.get('claims', {}).get(p, [])]
    def year(p):
        ys = [v['time'][1:5] for v in vals(p) if isinstance(v, dict) and 'time' in v]
        return ys[0] if ys else ''
    def items(p):
        return [v['id'] for v in vals(p) if isinstance(v, dict) and 'id' in v]
    return {
        'qid': qid,
        'label': e.get('labels', {}).get('en', e.get('labels', {}).get('mul', {})).get('value', ''),
        'label_language': 'en' if 'en' in e.get('labels', {}) else ('mul' if 'mul' in e.get('labels', {}) else ''),
        'description': e.get('descriptions', {}).get('en', {}).get('value', ''),
        'aliases': [a['value'] for a in e.get('aliases', {}).get('en', [])],
        'instance_of': items('P31'),
        'birth': year('P569'), 'death': year('P570'),
        'occupation_qids': items('P106'),
        'retrieved_at': d['retrieved_at'],
        'url': f'https://www.wikidata.org/wiki/{qid}',
    }

def load_search(slug):
    d = json.loads((RAW / f'search-{slug}.json').read_text())
    text = d['response']['result']['content'][0]['text']
    rows = []
    for line in text.splitlines():
        m = re.match(r'(Q\d+): (.*?) — (.*)$', line)
        if m:
            rows.append({'qid': m.group(1), 'label': m.group(2), 'description': m.group(3)})
    return {'query': d['query'], 'retrieved_at': d['retrieved_at'], 'top': rows[:10]}

# The people in the participant exercise, with the evidence printed in the sources.
PEOPLE = [
    dict(entity_id='henry', printed='Dr. Trimen; signed "HENRY TRIMEN", Royal Botanic Gardens, Peradeniya',
         sources='S04 (p. 66), S05 (p. 453), S06 (pp. 453-455)', candidate='Q2462643',
         colonial_office='TRIMEN, HENRY, M.B. (Lond.), F.L.S.: director Royal Botanical Gardens, Ceylon, Feb. 1880 (editions 1883-1896)'),
    dict(entity_id='howard', printed='Mr. Howard; Mr. J. E. Howard; signed "JOHN ELIOT HOWARD" (S01)',
         sources='S01 (pp. 114-115), S04 (p. 66), S05, S06', candidate='Q3181423', colonial_office=''),
    dict(entity_id='moens', printed='Mr. Moens', sources='S02, S04, S06', candidate='Q21340893', colonial_office=''),
    dict(entity_id='mcivor', printed="McIvor ('McIvor's seed')", sources='S03 (p. 37)', candidate='Q21520254', colonial_office=''),
    dict(entity_id='ledger', printed="Ledger ('Ledger's original seed')", sources='S03, S06', candidate='Q963818', colonial_office=''),
    dict(entity_id='agar', printed='Mr. Agar; signed "WALTER AGAR", Lawrence, June 22nd, 1883', sources='S03, S04', candidate='',
         searches=['walter-agar', 'walter-agar-ceylon-planter'], colonial_office=''),
    dict(entity_id='christie', printed='Mr. Christie; signed "THOS. NORTH CHRISTIE", St. Andrew\'s, Maskeliya, 7th June 1883',
         sources='S03, S04', candidate='', searches=['thomas-north-christie', 'thomas-north-christie-ceylon-planter', 'thomas-christy'],
         colonial_office=''),
    dict(entity_id='campbell', printed='Mr. Campbell', sources='S04', candidate='', searches=[], colonial_office=''),
]

rows = []
for p in PEOPLE:
    rec = dict(p)
    rec['searches'] = [load_search(s) for s in p.get('searches', [])]
    rec['entity'] = load_entity(p['candidate']) if p['candidate'] else None
    rows.append(rec)

(OUT / 'candidates.json').write_text(json.dumps(rows, indent=2, ensure_ascii=False) + '\n')

with (OUT / 'candidates.csv').open('w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['entity_id', 'printed_in_source', 'sources', 'candidate_qid', 'wikidata_label', 'wikidata_description',
                'birth', 'death', 'retrieved_at', 'colonial_office_list', 'search_queries_run', 'top_search_hits'])
    for r in rows:
        e = r['entity'] or {}
        hits = ' | '.join(f"{h['qid']} {h['label']} ({h['description']})" for s in r['searches'] for h in s['top'][:3])
        w.writerow([r['entity_id'], r['printed'], r['sources'], r['candidate'], e.get('label', ''), e.get('description', ''),
                    e.get('birth', ''), e.get('death', ''), e.get('retrieved_at', ''), r['colonial_office'],
                    '; '.join(s['query'] for s in r['searches']), hits])

md = ['# Candidate identities retrieved for the exercise people', '',
      'Generated by `scripts/build_candidates.py` from cached Wikidata responses in `research/trimen-network/raw/`.',
      'A candidate is retrieved evidence, not a decision. Click through to read the full statements.', '']
for r in rows:
    md.append(f"## {r['entity_id']}: {r['printed']}")
    md.append('')
    md.append(f"Printed in: {r['sources']}  ")
    if r['colonial_office']:
        md.append(f"Colonial Office List: {r['colonial_office']}  ")
    e = r['entity']
    if e:
        md.append(f"Candidate: [{e['qid']}]({e['url']}) {e['label']}, {e['description'] or 'no English description'}; born {e['birth'] or '?'}, died {e['death'] or '?'}; aliases: {', '.join(e['aliases']) or 'none'}; retrieved {e['retrieved_at'][:10]}.")
    else:
        md.append('Candidate: none established.')
    for s in r['searches']:
        md.append('')
        md.append(f"Vector search `{s['query']}` ({s['retrieved_at'][:10]}), top hits:")
        md.append('')
        for h in s['top'][:6]:
            md.append(f"- {h['qid']} {h['label']} ({h['description'] or 'no description'})")
    md.append('')
(OUT / 'candidates.md').write_text('\n'.join(md) + '\n')
print('wrote', OUT, len(rows), 'people')
