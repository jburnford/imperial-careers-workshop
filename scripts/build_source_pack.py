"""Assemble the participant source pack from the research packet. No network access.

Writes source-pack/: plain-text OCR for the passages used in the hour, the scan-checked transcription of
the exercise letter, the Colonial Office List entries for Henry Trimen, and a citations file with page links.
"""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
SRC = BASE / 'research/trimen-network/sources'
OUT = BASE / 'source-pack'
OUT.mkdir(exist_ok=True)

USED = ['S01', 'S02', 'S03', 'S04', 'S05', 'S06']
cites = ['# Sources used in the workshop', '',
         'All passages are from *The Tropical Agriculturist* (Colombo), digitised by archive.org. The OCR text comes from the',
         'Tropical Agriculturist project (github.com/jburnford/tropical-agriculturist). Page links open the scan.', '']
for sid in USED:
    a = json.loads((SRC / f'{sid}.json').read_text())
    (OUT / f'{sid}_ocr.txt').write_text(a['text'] + '\n')
    if 'transcription' in a:
        (OUT / f'{sid}_scan_checked.txt').write_text(a['transcription'] + '\n')
        diff = ['# OCR versus scan: ' + a['title'], '', f"Checked: {a['verification']}", '']
        for d in a['ocr_differences']:
            diff += ['OCR:  ' + d['ocr'], 'Scan: ' + d['scan'], '']
        (OUT / f'{sid}_ocr_differences.md').write_text('\n'.join(diff) + '\n')
    pages = '; '.join(f"p. {p['folio']}: {p['viewer_url']}" for p in a['pages'])
    cites.append(f"- **{sid}** \"{a['title']}\", issue {a['issue']}, {a['words']} words. Tropical article id `{a['id']}`. Scan: {pages}. Verification: {a['verification']}.")

col = json.loads((SRC / 'colonial-office-list-trimen-bios.json').read_text())
lines = ['# Henry Trimen in the Colonial Office List', '',
         'OCR blocks from the col_matching project (github.com/jburnford/col_matching). One entry per edition.', '']
for r in col:
    lines.append(f"## {r['edition']}")
    lines.append('')
    lines.append(r['raw_ocr_block']['text'])
    lines.append('')
(OUT / 'colonial-office-list-henry-trimen.md').write_text('\n'.join(lines))
cites += ['', '- **Colonial Office List** entries for Henry Trimen, editions ' + ', '.join(str(r['edition']) for r in col) + ' (`colonial-office-list-henry-trimen.md`).']
(OUT / 'CITATIONS.md').write_text('\n'.join(cites) + '\n')
print('wrote', sorted(p.name for p in OUT.iterdir()))
