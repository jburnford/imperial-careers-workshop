"""Build a small, curated research packet from frozen OCR and cached authorities.

Run from any directory. No network access; does not modify Tropical.
The selections and interpretations below are assistant proposals for human review.
"""
import csv
import hashlib
import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / 'research/trimen-network'
OUT.mkdir(parents=True, exist_ok=True)
(OUT / 'sources').mkdir(exist_ok=True)

def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')

def table(name, rows):
    write_json(OUT / f'{name}.json', rows)
    with (OUT / f'{name}.csv').open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

selection = [
    ('S01', '#1881-07#058'), ('S02', '#1883-07#046'),
    ('S03', '#1883-07#066'), ('S04', '#1883-07#116'),
    ('S05', '#1883-12#124'), ('S06', '#1883-12#125'),
    ('S07', '#1943-04/06#013'),
]
# Scan checks performed so far (assistant, 6 October 2026, archive.org page images at the URLs in `pages`).
VERIFICATION = {
    'S02': 'Opening page n44 visually inspected; remaining text from OCR',
    'S04': 'Whole item compared with the scan of page n83 on 2026-10-06; see ocr_differences',
}
# OCR -> scan readings. These are sentence-level OCR errors that change the meaning of the letter.
OCR_CORRECTIONS = {
    'S04': [
        ('and were now in a full condition and in flower.',
         'and were growing in a bad situation and not robust.'),
        ('I have by my prints of the leaves of some of the trees as well as the other that Mr. Moens had sent to be true Ledgerianas,',
         'I have many plants from the seed of the specimen tree as well as the others that Mr. Moens declared to be true Ledgerianas,'),
        ('It was one of several Mr. Moens saw in flower at Mahanillu estate,',
         'It was one of several Mr. Moens saw in flower at Mahanilu estate,'),
    ],
}
articles = json.loads((BASE / 'trimen-howard-search.json').read_text())
sources = {}
for sid, suffix in selection:
    matches = [a for a in articles if a['id'].endswith(suffix)]
    assert len(matches) == 1, suffix
    a = dict(matches[0])
    a['source_id'] = sid
    a['verification'] = VERIFICATION.get(sid, 'OCR read; scan URLs supplied; visual check pending')
    if sid in OCR_CORRECTIONS:
        # `text` stays as the OCR delivered it (that is what a model sees); `transcription` is the
        # scan-checked reading, and `ocr_differences` lists every change so the two can be compared.
        t = a['text']
        for wrong, right in OCR_CORRECTIONS[sid]:
            assert wrong in t, (sid, wrong)
            t = t.replace(wrong, right)
        a['transcription'] = t
        a['ocr_differences'] = [dict(ocr=w, scan=r) for w, r in OCR_CORRECTIONS[sid]]
    sources[sid] = a
    write_json(OUT / 'sources' / f'{sid}.json', a)

# A checked authority record is not a human-approved historical mention match.
# QIDs map names/concepts, never automatically every occurrence of a string.
seed = [
('henry','person','Henry Trimen','Q2462643','S05;S06;letters','Full signature, botany, Peradeniya; distinguish Roland.'),
('howard','person','John Eliot Howard','Q3181423','S01;S05;S06','Full signature in S01; quinology context. Initial/name variants still require mention review.'),
('markham','person','Clements R. Markham','Q507802','S01;S07','Full name and cinchona history; retrospective publication is not event date.'),
('moens','person','J. C. Bernelot Moens','Q21340893','S02;S04;S06','Java cinchona context; authority given names disagree across languages. Preserve initials.'),
('mcivor','person','McIvor','Q21520254','S01;S03;S06','William Graham McIvor candidate from cinchona context; printed surname alone.'),
('ledger','person','Ledger','Q963818','S03;S05;S06','Charles Ledger candidate from seed history; do not assign all collecting work to him.'),
('weddell','person','Weddell','Q983408','S06','Hugh Algernon Weddell candidate; botanical publications and nomenclature.'),
('hooker','person','J. D. Hooker','Q157501','S05;S06','Joseph Dalton Hooker; distinguish other Hookers.'),
('fitch','person','Fitch','Q1102060','S06','Walter Hood Fitch candidate from botanical illustration context.'),
('spruce','person','Dr. Spruce','Q1349394','S07','Richard Spruce candidate from cinchona collecting context.'),
('roland','person','Roland Trimen','Q932702','letters','Explicit creator in supplied catalogue; distinct from Henry.'),
('dyer','person','Sir William Thiselton-Dyer','Q2065240','letters','Catalogue recipient; name and dates compatible with botanist.'),
('morris','person','Daniel Morris','Q20733957','letters','Catalogue recipient; botanist candidate, not the American politician.'),
('christie','person','Thomas North Christie','','S03;S06','Signature THOS. NORTH CHRISTIE; no suitable QID established. Distinguish Thomas Christy.'),
('agar','person','Walter Agar','','S04','Full signature; no suitable QID established.'),
('campbell','person','Mr. Campbell / J. A. Campbell','','S03;S04','Same-person link between initials and surname is provisional.'),
('unnamed_assistant','person','Ledger’s unnamed servant','','S06','Source gives no personal name; preserve this participation without inventing an identity.'),
('howards','organization','Howards and Sons','Q123413890','external:ACC/1037','User supplied; pharmaceutical firm. Archive catalogue connects firm to Stratford; not identical to Howard the person.'),
('peradeniya_garden','place','Royal Botanic Gardens, Peradeniya','Q3119056','S05','Explicit address in Trimen cover letter, 21 November 1883.'),
('peradeniya','place','Peradeniya','Q489744','S06;letters','Town/locality; a bare place name does not by itself identify the garden.'),
('hakgala_garden','place','Hakgala Botanical Garden','Q5640444','S07','Garden; bare Hakgala in correspondence needs separate locality record.'),
('hakgala_locality','place','Hakgala','','letters','Catalogue origin 15 April 1894; garden identity is possible but not explicit.'),
('kew_site','place','Kew Gardens','Q188617','S05','Garden site candidate for seed routing; distinguish institutional actor.'),
('kew_institution','organization','Royal Botanic Gardens, Kew','Q18748726','letters;S05','Institution candidate; catalogue herbarium code K and seed-routing role require scope review.'),
('java','place','Java','Q3757','S05;S06','Island; no modern administrative relations projected backwards.'),
('nilgiris','place','Neilgherry','Q10094','S07','Nilgiri Mountains candidate for historical regional name.'),
('ceylon','place','Ceylon','','S06;S07;letters','Island and colonial polity are not interchangeable; scope unresolved per mention.'),
('british_ceylon','historical_polity','British Ceylon','Q918153','context','Candidate only when source means colonial polity, not every Ceylon occurrence.'),
('stratford','place','Stratford','Q676136','external:ACC/1037','District candidate for factory location. Modern Newham administrative claims are not imported.'),
('west_ham_borough','historical_polity','West Ham local government district','Q5177625','user-supplied;authority qualifiers','Item explicitly includes local board of health, 1856–1886, as well as later borough forms. Retain QID with period-specific label. County-borough start qualifier says 1899: apparent discrepancy to investigate, not silently repair.'),
('standrews','place','St. Andrew’s estate, Maskeliya','','S03;S06','Local estate entity; no coordinates or QID established.'),
('mahanillu','place','Mahanillu / Mahanilu estate','','S03;S04','Spelling variants provisionally grouped by tree narrative; check scans.'),
('yarrow','place','Yarrow estate','','S03;S05;S06','Local estate entity; do not match unrelated modern Yarrow places.'),
('lordsmeade','place','Lord’s Meade','','S01','Howard letter address; no exact location match established here.'),
('lancaster','place','5 Lancaster Street, [London]','','letters','Roland letter address as catalogued; exact building not grounded.'),
('cinchona','taxon_name','Cinchona','Q160090','S01;S06','Genus; not bark product or chemical.'),
('ledgeriana','taxon_name','Cinchona ledgeriana','Q5120189','S03;S04;S06','Historical species/variety usage contested; name grounding does not identify specimen.'),
('calisaya','taxon_name','Cinchona calisaya','Q15399753','S01;S06','Preserve variety names separately; no automatic historical specimen assignment.'),
('micrantha','taxon_name','Cinchona micrantha','Q15400875','S06','Species-name authority; var. calisayoides is a narrower historical designation.'),
('officinalis','taxon_name','Cinchona officinalis','Q3091779','S01;S06','Name-level candidate; retain OCR Officialis separately when transcribing.'),
('succirubra','taxon_name','Cinchona succirubra','Q50830790','S01;S05;S07','Historical name retained even where current authority treats it as a synonym.'),
('pubescens','taxon_name','Cinchona pubescens','Q164574','S01','Authority name; NOT automatic match for rejected C. pubescens How. usage.'),
('pubescens_how','historical_name_usage','C. pubescens How.','','S01','Howard explicitly disclaims new species; describes hybrid usage distinct from established C. pubescens.'),
('micrantha_var','historical_name_usage','C. micrantha var. calisayoides','','S06','Preserve disputed infraspecific identification; no exact QID established.'),
('bark','plant_product','Cinchona bark','Q3133417','S01;S04;S06','Product; not taxon or purified quinine.'),
('alkaloids','chemical_class','Cinchona alkaloids','Q21662767','S04;S06','Class, distinct from individual compounds.'),
('quinine','chemical','quinine','Q189522','S04;S06','Pure quinine distinct from sulphate of quinine; reported percentages cannot be silently equated.'),
('illustrated_tree','specimen','Tree figured for Trimen’s description','','S03;S04;S06','Local individual tree; do not assert botanical type status. Dead by Agar letter date.'),
('neighbour_trees','specimen_group','Other trees at Mahanillu','','S04;S06','Sampled bark from some neighbouring trees is not necessarily from the illustrated tree.'),
]
entities = []
for eid, kind, label, qid, src, note in seed:
    authority = {}
    path = OUT / 'raw' / f'{qid}.json'
    if qid and path.exists():
        authority = json.loads(path.read_text())['response']['entities'][qid]
    entities.append(dict(entity_id=eid, kind=kind, historical_label=label, candidate_qid=qid,
                         authority_label=authority.get('labels',{}).get('en',authority.get('labels',{}).get('mul',{})).get('value',''),
                         authority_status='record_checked' if authority else 'local_only',
                         human_review='pending', sources=src, rationale=note,
                         authority_url=f'https://www.wikidata.org/wiki/{qid}' if qid else ''))
table('entities', entities)

claims = []
def claim(cid, subject, relation, obj, speaker, sid, date, quote, note=''):
    assert quote in sources[sid]['text'], (cid, quote)
    claims.append(dict(claim_id=cid, subject=subject, relation=relation, object=obj,
                       attributed_to=speaker, source_id=sid, date_as_stated=date,
                       evidence=quote, interpretation_note=note, human_review='pending'))

claim('C01','henry','sent_reply_from','peradeniya_garden','henry','S05','1883-11-21',
      'Royal Botanic Gardens, Peradeniya, 21st Nov. 1883.')
claim('C02','henry','replied_to_published_argument_by','howard','henry','S05','1883-11-21',
      'in reply to the letter of Mr. J. E. Howard on "*Cinchona Ledgeriana*" published in that periodical.',
      'Reply addressed to editor; not evidence of a private letter sent directly to Howard.')
claim('C03','illustrated_tree','identified_as','ledgeriana','henry','S06','1883-10-29',
      'the tree, apart from its stunted growth, was considered by Mr. Moens as a very characteristic example of the species.',
      'Trimen’s account of Moens’s identification, endorsed in Trimen’s argument; does not resolve modern classification.')
claim('C04','illustrated_tree','identified_as','micrantha_var','howard via Trimen','S06','1883-10-29',
      '(1) The plant figured by me = *C. micrantha*, var. *calisayoides* (probably);',
      'Trimen reports Howard’s qualified identification, not an uncontested species assignment.')
claim('C05','moens','showed_diagnostic_characters_to','henry','henry','S06','1880-09',
      'Mr. Moens visited Ceylon in September 1880, and it is to him that I am indebted for having first pointed out to me that the plant had good definite characters.')
claim('C06','christie','raised','illustrated_tree','christie','S03','1883-06-07',
      "The plant which Dr. Trimen figured was one of those raised from McIvor's seed by me, and planted on Mahanilu by Mr. Agar, and its descent from Ledger's original seed is undoubted.",
      'Christie’s asserted provenance; not independently demonstrated chain of custody.')
claim('C07','agar','planted','illustrated_tree','christie','S03','1883-06-07',
      'planted on Mahanilu by Mr. Agar')
claim('C08','illustrated_tree','grew_at','mahanillu','agar','S04','1883-06-22',
      'It was one of several Mr. Moens saw in flower at Mahanillu estate, Dr. Trimen was with Mr. Moens, and both agreed the trees were true Ledgerianas.')
claim('C09','campbell','sent_neighbouring_bark_to','howard','agar','S04','1883-06-22',
      'The bark of some of these trees was sent home by Mr. Campbell for analysis to Mr. Howard,',
      'From some trees in group; do not substitute illustrated tree as sample source.')
claim('C10','howard','analysed_bark_from','neighbour_trees','agar','S04','1883-06-22',
      'who pronounced it to be Ledgeriana bark, giving 7 per cent of pure quinine (equal I believe to 9 of sulphate) and only a trace of other alkaloids.',
      'Historical reported assay, with narrator’s qualified conversion; not independently validated measurement.')
claim('C11','agar','held_bark_from','illustrated_tree','agar','S04','1883-06-22',
      'I have also in my possession the bark from the tree itself, but taken when it was dying.')
claim('C12','howard','disclaimed_species_authorship_for','pubescens_how','howard','S01','1881-04-29',
      'I find that I am credited with having created a new species of Cinchona, the "*C. pubescens* How."',
      'Following sentences explicitly reject this attribution; preserve rejected name as historical usage.')
claim('C13','markham','was_criticised_for_hybrid_parentage_of','pubescens_how','journal editorial voice','S01','1881-07',
      "Mr. Clements Markham's mistake in putting it as a hybrid of *Calisaya* and *Officialis* was commented on.",
      'Editorial attribution of an error; not a fresh independent botanical determination.')
claim('C14','markham','collected_consignment_later_sent_to','nilgiris','Jayaweera retrospective','S07','event date not specified in excerpt',
      'The first consignment of plants was collected and brought to Bombay by Mr. Clements R. Markham. As the plants were not quite healthy they were all sent to Neilgherry instead of a few being sent here as was first intended.',
      'Publication 1943; Markham brought plants to Bombay, onward consignment sent to Nilgiris. Does not establish that he accompanied the onward leg.')
table('claims', claims)

# User-supplied catalogue entries; duplicates in the pasted display collapsed.
# No repository catalogue URL or letter contents supplied for these records.
letter_seed = [
('1896-04-12','533',4,2),('1896-07-20','538',4,2),('1896-12-31','540-541',6,4),
('1896-08-30','539',4,2),('1896-05-11','535',4,2),('1896-04-16','534',4,2),
('1896-07-05','537',4,2),('1896-03-15','532',4,2),('1896-06-03','536',2,2),
('1895-01-15','524-525',8,4),('1895-03-17','527-528',7,4),('1895-04-10','530-531',8,4),
('1895-02-27','526',4,2),('1894-11-13','521-523',12,6),('1894-07-04','515-516',8,4),
('1894-04-15','512-514',12,6),('1894-10-10','519-520',8,4),('1894-09-10','517-518',8,4),
('1894-04-03','510-511',7,4),('1894-01-15','507-509',12,6),('1893-08-29','501-502',8,4),
('1893-03-07','491-492',7,4),('1893-03-21','493-494',6,4),('1893-07-05','496-497',6,4),
('1893-06-07','495',4,2),
]
letters=[]
for date, folio, pages, images in letter_seed:
    roland=date=='1896-12-31'
    letters.append(dict(letter_id='L'+date, sender='roland' if roland else 'henry',
                        recipient='morris' if date=='1894-04-03' else 'dyer', date=date,
                        origin='lancaster' if roland else 'hakgala_locality' if date=='1894-04-15' else 'peradeniya',
                        folios=folio, pages=pages, images=images, herbarium='K',
                        source='User-supplied catalogue text, 2026-10-06', source_url='',
                        verification='catalogue_metadata_only', subject='not_read', human_review='pending'))
table('letters', letters)

table('archival-leads', [dict(lead_id=ident, url=f'https://plants.jstor.org/stable/10.5555/al.ap.visual.{ident}',
                            supplied_by='user', verification='retrieval_unavailable',
                            linked_letter_id='', note='Record contents unavailable during check; do not infer date, subject or match to pasted catalogue entries from URL sequence.')
                        for ident in ['kdcas1413','kdcas1411']])

taxonomy=[]
for name, accepted, ipni in [('ledgeriana','calisaya','746808-1'),('succirubra','pubescens','746904-1')]:
    taxonomy.append(dict(historical_name_entity=name, current_accepted_name_entity=accepted,
                         authority='Kew Plants of the World Online', status='synonym', checked='2026-10-06',
                         url=f'https://powo.science.kew.org/taxon/urn:lsid:ipni.org:names:{ipni}',
                         scope='Current name treatment only; does not adjudicate historical specimen identifications.'))
table('taxonomy', taxonomy)

ids={e['entity_id'] for e in entities}
assert len(ids)==len(entities)
for c in claims:
    assert c['subject'] in ids and c['object'] in ids
for l in letters:
    assert all(l[k] in ids for k in ['sender','recipient','origin'])
assert len(letters)==len({l['letter_id'] for l in letters})
for e in entities:
    assert not e['candidate_qid'] or e['authority_status']=='record_checked', e
manifest=dict(built_from='trimen-howard-search.json',
              source_sha256=hashlib.sha256((BASE/'trimen-howard-search.json').read_bytes()).hexdigest(),
              snapshot_note='Frozen search extract from Tropical; not a census of verified relationships. Production repository may have changed since extraction.',
              counts=dict(entities=len(entities),claims=len(claims),letters=len(letters),articles=len(sources)),
              scan_checks={sid: VERIFICATION[sid] for sid in VERIFICATION},
              review='Assistant-curated draft; all human decisions pending. No Tropical RA data changed.')
write_json(OUT/'manifest.json',manifest)
print(json.dumps(manifest['counts']))
