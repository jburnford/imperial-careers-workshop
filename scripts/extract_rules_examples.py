"""Save what the project's real rule-based parser did with four printed entries, plus its coverage.

Imperial Careers read every printed biography in each Colonial Office List edition with a
258-line rule-based parser (col_match/services/rules_parse.py, called from col_match/volume/bios.py).
Entries it could not parse were refused whole and read by Qwen. This script copies the parser's
saved output for the workshop's examples and counts, per edition, which reader produced each
biography. It needs a checkout of the Imperial Careers repository.

    python3 scripts/extract_rules_examples.py --col-matching ~/col_matching
"""
import argparse
import collections
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'outputs/structure/rules-parser-examples.json'
EXAMPLES = [('col1936', 'BALMER'), ('col1940', 'CONNOLLY'), ('col1867', 'WODEHOUSE')]


def find(path, prefix):
    for line in path.open(encoding='utf-8'):
        bio = json.loads(line)
        if bio.get('raw_text', '').startswith(prefix):
            return bio
    raise SystemExit(f'{prefix} not found in {path}')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--col-matching', type=Path, default=Path.home() / 'col_matching')
    repo = ap.parse_args().col_matching
    volume = repo / 'data/volume'

    examples = []
    for edition, surname in EXAMPLES:
        bio = find(volume / edition / 'bios.jsonl', surname)
        examples.append({
            'edition': edition, 'bio_id': bio.get('bio_id'), 'parser': bio.get('parser'),
            'flags': bio.get('flags'), 'raw_text': bio['raw_text'],
            'events': [{k: e.get(k) for k in ('position', 'place', 'year_start', 'year_end')}
                       for e in bio.get('events', [])]})

    editions, total = {}, collections.Counter()
    for path in sorted(volume.glob('col*/bios.jsonl')):
        counts = collections.Counter(json.loads(l).get('parser') for l in path.open(encoding='utf-8'))
        total.update(counts)
        read = counts['rules'] + counts['qwen'] + counts['unparsed']
        if read:
            editions[path.parent.name] = {'rules': counts['rules'], 'qwen': counts['qwen'],
                                          'unparsed': counts['unparsed'],
                                          'rules_share': round(counts['rules'] / read, 3)}
    read = total['rules'] + total['qwen'] + total['unparsed']
    OUT.write_text(json.dumps({
        'source': 'Imperial Careers data/volume/col*/bios.jsonl; parser col_match/services/rules_parse.py',
        'note': 'parser = rules: accepted by the rule-based parser; qwen: refused by the rules '
                '(flag rules_failed) and read by Qwen. Accepted output is not necessarily correct.',
        'totals': {'editions': len(editions), 'biographies_read': read, 'rules': total['rules'],
                   'qwen': total['qwen'], 'unparsed': total['unparsed'],
                   'not_a_bio': total['not_a_bio'], 'rules_share': round(total['rules'] / read, 3)},
        'editions': editions, 'examples': examples}, ensure_ascii=False, indent=1) + '\n')

    print(f"{len(editions)} editions: rules {total['rules']:,} of {read:,} biographies "
          f"({total['rules'] / read:.1%}); Qwen {total['qwen']:,}")
    for ed in ('col1888', 'col1960'):
        print(ed, editions[ed]['rules_share'])
    for ex in examples:
        print(ex['edition'], ex['parser'], [(e['place'], e['year_start']) for e in ex['events']][-3:])


if __name__ == '__main__':
    main()
