"""Cache public Wikidata evidence for the Trimen workshop, without changing Tropical.

Usage: python3 scripts/ground_trimen.py entities Q2462643 Q3181423
       python3 scripts/ground_trimen.py search 'Cinchona ledgeriana'
"""
import concurrent.futures
import datetime
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1] / 'research/trimen-network'
RAW = ROOT / 'raw'
RAW.mkdir(parents=True, exist_ok=True)

def curl(url, extra=()):
    p = subprocess.run(['curl', '--fail', '--location', '--silent', '--show-error',
                        '--max-time', '45', *extra, url], capture_output=True, text=True)
    if p.returncode:
        raise RuntimeError(p.stderr.strip())
    return p.stdout

def entity(qid):
    assert re.fullmatch(r'Q\d+', qid)
    path = RAW / f'{qid}.json'
    if not path.exists():
        url = f'https://www.wikidata.org/wiki/Special:EntityData/{qid}.json'
        body = curl(url)
        data = json.loads(body)
        path.write_text(json.dumps({'retrieved_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                                    'url': url, 'response': data}, ensure_ascii=False, indent=2))
    e = json.loads(path.read_text())['response']['entities'][qid]
    claims = {}
    for key in ['P31', 'P106', 'P569', 'P570', 'P225', 'P171', 'P105', 'P1420', 'P1843',
                'P566', 'P586', 'P428', 'P4081', 'P961', 'P846', 'P17', 'P131', 'P571', 'P576', 'P625']:
        values = [r['mainsnak'].get('datavalue', {}).get('value') for r in e.get('claims', {}).get(key, [])]
        if values: claims[key] = values
    return {'qid': qid, 'label': e.get('labels', {}).get('en', e.get('labels', {}).get('mul', {})).get('value'),
            'description': e.get('descriptions', {}).get('en', {}).get('value'),
            'aliases': [a['value'] for a in e.get('aliases', {}).get('en', [])], 'claims': claims}

def search(query):
    slug = re.sub(r'[^a-z0-9]+', '-', query.lower()).strip('-')
    path = RAW / f'search-{slug}.json'
    if not path.exists():
        body = {'jsonrpc': '2.0', 'id': 1, 'method': 'tools/call',
                'params': {'name': 'search_items', 'arguments': {'query': query}}}
        request = RAW / f'search-{slug}-request.json'
        request.write_text(json.dumps(body))
        url = 'https://wd-mcp.wmcloud.org/mcp'
        raw = curl(url, ['-H', 'Content-Type: application/json', '-H', 'Accept: application/json, text/event-stream',
                         '--data-binary', '@' + str(request)])
        if raw.lstrip().startswith('event:') or raw.lstrip().startswith('data:'):
            raw = '\n'.join(l[5:].strip() for l in raw.splitlines() if l.startswith('data:'))
        data = json.loads(raw)
        path.write_text(json.dumps({'query': query, 'retrieved_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                                    'url': url, 'response': data}, ensure_ascii=False, indent=2))
    data = json.loads(path.read_text())
    response = data['response']
    result = response.get('result', {})
    content = '\n'.join(c.get('text', '') for c in result.get('content', []))
    return {'query': query, 'candidates': content.splitlines()[:8], 'error': response.get('error')}

if __name__ == '__main__':
    func = {'entities': entity, 'search': search}[sys.argv[1]]
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        for value in pool.map(func, sys.argv[2:]):
            print(json.dumps(value, ensure_ascii=False))
