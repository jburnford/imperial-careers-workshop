"""Run one reasonable regular expression over three printed entries and save what it returns.

A first attempt at a rule-based parser: split the career on semicolons, then read each clause as
"position, place, [month.] year". The point is to show, with real output, where a fixed pattern
works and where the source's wording defeats it. No model or network is needed.

    python3 scripts/demo_regex_limits.py
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'outputs/structure/regex-limits.json'

ENTRIES = {
    'BALMER': ('Colonial Office List 1936, p. 614',
               "BALMER, F. E.—Dep. chief acctnt., G.P.O., E. Africa Prot., Mar., 1919; ch. acctnt., G.P.O., "
               "Kenya, Oct., 1919; ch. acctnt., Kenya-Uganda-Tanganyika post and tel. service, 1933; senr. dep. "
               "P.M.G., do., 1935."),
    'WODEHOUSE': ('Colonial Office List 1867',
                  "WODEHOUSE, SIR PHILIP E., K.C.B. (Creat. 1862.)—Entered the Ceylon civil service as a writer, "
                  "May, 1828; promoted to be assistant colonial secretary and clerk of the executive and legislative "
                  "councils, Oct. 1833; district judge of Kandy, 1840; government agent for the western province, "
                  "1843; was appointed superintendent of Honduras, 1851; in Feb. 1854, governor of British Guiana; "
                  "was employed in 1858 on a special mission to the government of Venezuela; and in 1861 was "
                  "appointed governor of the Cape of Good Hope; is also high commissioner in South Africa."),
    'CONNOLLY': ('Colonial Office List 1940',
                 "CONNOLLY, HON. SIR JAMES DANIEL, KT. BACH. (1920). —B. 1870; ed. Warwick Pub. Schl. and Catholic "
                 "Schl.; M.L.C., Western Australia, 1902; col. sec. and min. of com. and lab., 1906; col. sec. and "
                 "min. of pub. health, 1910; leader of leg. coun. from 1906 to 1911; M.L.A. for Perth, 1914; agt. "
                 "genl. in London for Western Australia, 1917-23; agt. gen. in London for Malta, 1930."),
}

HEADER = re.compile(r'^(?P<head>[^—]+?)\s*—(?P<body>.*)$')
CLAUSE = re.compile(r'^(?P<position>.+?),\s*(?P<place>[^,]+),\s*(?:(?P<month>[A-Z][a-z]{2,4})\.,?\s*)?'
                    r'(?P<year>1[89]\d\d)(?:-(?P<end>\d{2,4}))?\.?$')
HONOUR = re.compile(r'\b(?P<award>[A-Z]{2,5})\.(?:\s*\((?P<year>\d{4})\))?')
BORN = re.compile(r'^B\.\s*(?P<year>1[89]\d\d)$')
EDUCATION = re.compile(r'^ed\.\s')


def parse(text):
    m = HEADER.match(text)
    head, body = m['head'], m['body'].strip().rstrip('.')
    honours = [{'award': h['award'], 'year': h['year']} for h in HONOUR.finditer(head.split(',', 1)[1])]
    clauses = []
    for clause in [c.strip() for c in body.split(';') if c.strip()]:
        born = BORN.match(clause)
        if born:
            clauses.append({'clause': clause, 'birth_year': born['year']})
            continue
        if EDUCATION.match(clause):
            clauses.append({'clause': clause, 'education': clause})
            continue
        c = CLAUSE.match(clause)
        clauses.append({'clause': clause, 'match': None if c is None else
                        {k: v for k, v in c.groupdict().items() if v}})
    return {'honours': honours, 'clauses': clauses}


def main():
    results = {}
    for name, (source, text) in ENTRIES.items():
        r = parse(text)
        career = [c for c in r['clauses'] if 'match' in c]
        r.update(source=source, text=text,
                 clauses_matched=sum(c['match'] is not None for c in career), clauses_total=len(career))
        results[name] = r
    OUT.write_text(json.dumps({
        'pattern': {'clause': CLAUSE.pattern, 'honour': HONOUR.pattern, 'born': BORN.pattern,
                    'education': EDUCATION.pattern},
        'note': 'One reasonable first-attempt pattern. "Matched" means the pattern returned fields, '
                'not that the fields are right; see the slide for which are wrong.',
        'entries': results}, ensure_ascii=False, indent=1) + '\n')
    for name, r in results.items():
        print(f"{name}: {r['clauses_matched']} of {r['clauses_total']} career clauses matched; honours {r['honours']}")
        for c in r['clauses']:
            shown = c.get('match') or ('BORN ' + c['birth_year'] if 'birth_year' in c else
                                       'EDUCATION' if 'education' in c else 'NO MATCH')
            print('   ', shown, '<-', c['clause'][:70])


if __name__ == '__main__':
    main()
