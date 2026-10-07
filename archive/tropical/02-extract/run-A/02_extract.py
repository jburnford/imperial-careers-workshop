#!/usr/bin/env python3
"""
02_extract.py -- hand-coded extraction of people, plants/trees, samples and
actions/relationships from two OCR'd items in The Tropical Agriculturist, July 1883.

Usage:   python3 02_extract.py [SOURCE_DIR]
Offline; standard library only. Writes 02_records.json, 02_records.csv and
02_validation.txt next to this script.

Design
  * The records are written out as data below (a human reading of the OCR text).
  * printed_text holds verbatim spans of the OCR text. Several spans from the same
    source may be joined with " ... " (written as the single character sequence
    ' … '). The script checks that EVERY span occurs in the source file
    (whitespace-normalised). A record failing this check is moved to
    "failed_records" in the JSON and is not written to the CSV.
  * Stated information lives in printed_*/stated_*/verb_as_printed columns.
    Anything the text does not itself say lives in inferred_* columns.
  * outside_identification and any authority identifiers are deliberately empty;
    no Wikidata identifiers are used. Names are never expanded beyond the print.
"""
import csv, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE))
SOURCES = {
    "S04": dict(file="S04_ocr.txt", ref="The Tropical Agriculturist, July 1883, p. 66",
                item="Dr. Trimen's Typical Ledgeriana Tree (letter of Walter Agar, Lawrence, June 22nd, 1883)"),
    "S03": dict(file="S03_ocr.txt", ref="The Tropical Agriculturist, July 1883, p. 37",
                item="Dr. Trimen's Ledgeriana: Mr. T. N. Christie to the Rescue (letter, St. Andrew's, Maskeliya, 7th June 1883)"),
}
SEP = " … "

FIELDS = [
    "record_id", "record_type", "material_kind", "source_id", "source_ref", "locator",
    "printed_text", "printed_name", "role_as_printed", "place_as_printed",
    "date_or_age_as_printed", "stated_detail",
    "subject_id", "verb_as_printed", "object_id", "recipient_id", "asserted_by",
    "reading_status", "reading_note",
    "inferred_same_as", "inferred_note", "outside_identification",
]

RECORDS = []

def R(rid, rtype, src, line, text, **kw):
    rec = {f: "" for f in FIELDS}
    rec.update(record_id=f"{src}-{rid}", record_type=rtype, source_id=src,
               source_ref=SOURCES[src]["ref"], locator=f"OCR line {line}", printed_text=text,
               reading_status="clear")
    for k, v in kw.items():
        if k not in rec:
            raise KeyError(k)
        # bare ids such as "P01" are expanded to this source's ids
        if k in ("subject_id", "object_id", "recipient_id") and v:
            v = "; ".join(x if "-" in x else f"{src}-{x}" for x in re.split(r";\s*", v))
        if k == "asserted_by" and re.fullmatch(r"P\d+", v):
            v = f"{src}-{v}"
        rec[k] = v
    RECORDS.append(rec)

# ============================================================== S04 (p. 66)
s = "S04"
# ---- people
R("P01", "person", s, "1, 9", "DR. TRIMEN'S TYPICAL LEDGERIANA TREE." + SEP + "The tree, which was sketched for Dr. Trimen's work, is dead.",
  printed_name="Dr. Trimen", role_as_printed="Dr.",
  stated_detail="Named in the title; a tree was sketched for 'Dr. Trimen's work'; was with Mr. Moens when the trees were seen at Mahanillu estate.",
  asserted_by="P02", inferred_same_as="S03-P02 (probable: same surname, title and subject)")
R("P02", "person", s, "3, 5, 17", "We publish below a letter from Mr. Agar" + SEP + "Lawrence, June 22nd, 1883." + SEP + "WALTER AGAR.",
  printed_name="WALTER AGAR (signature); Mr. Agar (editorial note)", role_as_printed="a letter from Mr. Agar",
  place_as_printed="Lawrence", date_or_age_as_printed="June 22nd, 1883",
  stated_detail="Writer of the letter; full forename 'Walter' is given in the signature.",
  inferred_same_as="S03-P04 (probable: S03 prints only 'Mr. Agar', planter of the plant at Mahanilu)")
R("P03", "person", s, "3, 11", "Mr. Howard himself having given testimony to that effect after having analyzed the bark" + SEP + "to Mr. Howard, who pronounced it to be Ledgeriana bark",
  printed_name="Mr. Howard", role_as_printed="(analyst of the bark)",
  stated_detail="Analysed the bark and pronounced it Ledgeriana bark.", asserted_by="P02",
  inferred_same_as="S03-P01 (probable: S03 prints 'Mr. J. E. Howard'; S04 gives no initials)",
  inferred_note="Initials 'J. E.' are NOT supplied here because S04 does not print them.")
R("P04", "person", s, "7", "I have little to add to what Mr. Christie has written on the subject of Ledgerianas",
  printed_name="Mr. Christie", stated_detail="Has written on the subject of Ledgerianas.", asserted_by="P02",
  inferred_same_as="S03-P09 (probable: S03 is a letter on Ledgerianas signed THOS. NORTH CHRISTIE, one week to 'June 7th'; S04 does not say which item is meant)",
  inferred_note="Link to S03 rests on subject matter and date; S04 does not name the piece Mr. Christie wrote.")
R("P05", "person", s, "11", "one of several Mr. Moens saw in flower at Mahanillu estate, Dr. Trimen was with Mr. Moens",
  printed_name="Mr. Moens", place_as_printed="Mahanillu estate",
  stated_detail="Saw several trees in flower; agreed with Dr. Trimen they were true Ledgerianas; had sent 'the other' (see S04-T03).",
  asserted_by="P02", inferred_same_as="S03-P08 (probable)")
R("P06", "person", s, "11", "sent home by Mr. Campbell for analysis to Mr. Howard",
  printed_name="Mr. Campbell", stated_detail="Sent the bark of some of the trees home for analysis.", asserted_by="P02",
  inferred_same_as="S03-P07 (probable: S03 prints 'Mr. J. A. Campbell of Lindula, Ceylon'; S04 gives only 'Mr. Campbell')")
R("P07", "person", s, "3", "—Ed.]",
  printed_name="Ed.", role_as_printed="Ed.",
  stated_detail="Editorial note introducing the letter; no personal name printed.",
  reading_status="uncertain", reading_note="Kept as an unnamed role-record (editor of the journal); it is not a personal name. Drop if only named people are wanted.",
  inferred_note="That 'Ed.' is the journal's editor is the conventional reading of the abbreviation.")
# ---- trees / plants
R("T01", "plant", s, "1, 3, 9, 11", "the tree figured by Dr. Trimen was an undoubted Ledgeriana" + SEP + "The tree, which was sketched for Dr. Trimen's work, is dead." + SEP + "It was one of several Mr. Moens saw in flower at Mahanillu estate",
  material_kind="tree", printed_name="the tree, which was sketched for Dr. Trimen's work", place_as_printed="Mahanillu estate",
  stated_detail="Called 'an undoubted Ledgeriana' (editor) and 'typical' (title); 'is dead'; one of several trees Mr. Moens saw in flower at Mahanillu estate.",
  asserted_by="P02", inferred_same_as="S03-T01 (probable: 'The plant which Dr. Trimen figured', planted on Mahanilu by Mr. Agar)",
  inferred_note="'It' in 'It was one of several...' is read as the sketched tree. 'sketched' (S04) vs 'figured' (S03) are taken as the same illustration; the texts do not say so.")
R("T02", "plant", s, "11", "The trees were only about 4½ years old from the time the plants were put out, and were now in a full condition and in flower.",
  material_kind="plant group (trees)", printed_name="these trees (the several seen in flower)", place_as_printed="Mahanillu estate",
  date_or_age_as_printed="about 4½ years old from the time the plants were put out",
  stated_detail="Agreed by Dr. Trimen and Mr. Moens to be true Ledgerianas; in flower.", asserted_by="P02",
  reading_status="uncertain", reading_note="'in a full condition' may be an OCR or printing slip (e.g. 'in full bloom'); transcribed as printed. Place 'Mahanillu estate' is stated for the first sentence and carried here by 'these trees'.")
R("T03", "plant", s, "13", "as well as the other that Mr. Moens had sent to be true Ledgerianas",
  material_kind="unclear (noun after 'the other' missing)", printed_name="the other [that Mr. Moens had sent]",
  stated_detail="Something Mr. Moens 'had sent to be true Ledgerianas', named alongside the leaf prints ('as well as the other').", asserted_by="P02",
  reading_status="uncertain", reading_note="Sentence is garbled: 'the other' lacks its noun (tree? leaves? plant?) and 'sent to be true Ledgerianas' may be missing words (e.g. 'sent, said to be'). Not interpreted.",
  inferred_note="Treated as a plant/material item only because the sentence concerns leaf prints of trees.")
# ---- samples
R("B01", "sample", s, "11", "The bark of some of these trees was sent home by Mr. Campbell for analysis to Mr. Howard, who pronounced it to be Ledgeriana bark, giving 7 per cent of pure quinine (equal I believe to 9 of sulphate) and only a trace of other alkaloids.",
  material_kind="bark", printed_name="The bark of some of these trees",
  stated_detail="Sent home by Mr. Campbell to Mr. Howard for analysis; pronounced Ledgeriana bark; '7 per cent of pure quinine'; 'only a trace of other alkaloids'; '(equal I believe to 9 of sulphate)' is the writer's belief, not a measured value.",
  asserted_by="P02", inferred_note="Which trees supplied the bark is not stated beyond 'some of these trees'; whether it includes S04-T01 is not said.")
R("B02", "sample", s, "13", "I have by my prints of the leaves of some of the trees",
  material_kind="leaf prints", printed_name="prints of the leaves of some of the trees",
  stated_detail="In the writer's keeping 'so that it will be easy in the future to determine the question'.", asserted_by="P02",
  reading_status="uncertain", reading_note="'I have by my prints' is probably 'I have by me prints' (OCR/print slip); transcribed as printed.")
R("B03", "sample", s, "15", "I have also in my possession the bark from the tree itself, but taken when it was dying.",
  material_kind="bark", printed_name="the bark from the tree itself",
  stated_detail="Bark taken when the tree was dying; in the writer's possession.", asserted_by="P02",
  inferred_same_as="S04-T01 is the tree (probable: 'the tree itself' follows the discussion of the sketched tree)",
  inferred_note="'the tree itself' is read as the sketched tree of S04-T01, not one of the other trees.")
# ---- actions / relationships
R("A01", "action", s, "3", "We publish below a letter from Mr. Agar", subject_id="P07", verb_as_printed="publish", object_id="P02",
  stated_detail="The editor publishes a letter from Mr. Agar.", asserted_by="P07")
R("A02", "action", s, "3", "which places beyond question the fact that the tree figured by Dr. Trimen was an undoubted Ledgeriana",
  subject_id="", verb_as_printed="places beyond question the fact that ... was an undoubted Ledgeriana", object_id="T01",
  stated_detail="Editor's claim about the letter's effect; subject is the letter itself.", asserted_by="P07",
  inferred_note="subject_id left blank because the grammatical subject is the letter, not a person.")
R("A03", "action", s, "7", "I have little to add to what Mr. Christie has written on the subject of Ledgerianas",
  subject_id="P02", verb_as_printed="have little to add to what ... has written", object_id="P04", asserted_by="P02")
R("A04", "action", s, "9", "The tree, which was sketched for Dr. Trimen's work",
  subject_id="T01", verb_as_printed="was sketched for", object_id="P01",
  stated_detail="Object is 'Dr. Trimen's work' (a publication), recorded against Dr. Trimen; the person who sketched it is not named.", asserted_by="P02",
  inferred_note="The work is not named or described beyond 'Dr. Trimen's work'; S03 mentions 'Dr. Trimen's description and figure of C. ledgeriana' but the link is not stated.")
R("A05", "action", s, "11", "several Mr. Moens saw in flower at Mahanillu estate", subject_id="P05", verb_as_printed="saw in flower",
  object_id="T02", place_as_printed="Mahanillu estate", asserted_by="P02")
R("A06", "action", s, "11", "It was one of several Mr. Moens saw in flower", subject_id="T01", verb_as_printed="was one of several",
  object_id="T02", place_as_printed="Mahanillu estate", asserted_by="P02")
R("A07", "action", s, "11", "Dr. Trimen was with Mr. Moens", subject_id="P01", verb_as_printed="was with", object_id="P05", asserted_by="P02")
R("A08", "action", s, "11", "both agreed the trees were true Ledgerianas", subject_id="P01; P05", verb_as_printed="agreed ... were true Ledgerianas",
  object_id="T02", asserted_by="P02")
R("A09", "action", s, "11", "The bark of some of these trees was sent home by Mr. Campbell for analysis to Mr. Howard",
  subject_id="P06", verb_as_printed="sent home ... for analysis", object_id="B01", recipient_id="P03", asserted_by="P02")
R("A10", "action", s, "11", "Mr. Howard, who pronounced it to be Ledgeriana bark", subject_id="P03", verb_as_printed="pronounced it to be Ledgeriana bark",
  object_id="B01", asserted_by="P02")
R("A11", "action", s, "3", "Mr. Howard himself having given testimony to that effect after having analyzed the bark",
  subject_id="P03", verb_as_printed="having given testimony ... after having analyzed", object_id="B01", asserted_by="P07")
R("A12", "action", s, "13", "the other that Mr. Moens had sent to be true Ledgerianas", subject_id="P05", verb_as_printed="had sent to be true Ledgerianas",
  object_id="T03", asserted_by="P02", reading_status="uncertain", reading_note="See S04-T03; sentence garbled.")
R("A13", "action", s, "13", "I have by my prints of the leaves of some of the trees", subject_id="P02", verb_as_printed="have by my",
  object_id="B02", asserted_by="P02", reading_status="uncertain", reading_note="See S04-B02.")
R("A14", "action", s, "15", "I have also in my possession the bark from the tree itself", subject_id="P02", verb_as_printed="have ... in my possession",
  object_id="B03", asserted_by="P02")

# ============================================================== S03 (p. 37)
s = "S03"
# ---- people
R("P01", "person", s, "5, 7, 17", "Were the question raised by Mr. J. E. Howard purely technical" + SEP + "communicated to Mr. J. E. Howard, F. R. S., who raised seedlings",
  printed_name="Mr. J. E. Howard", role_as_printed="F. R. S.", asserted_by="P09",
  stated_detail="Raised the question; raised seedlings from Java seed (Kew report); author of 'Mr. Howard's latest paper' and 'Howard's great work'; characterised by the writer as having 'the knowledge of hot-house plants and dried specimens'.",
  inferred_same_as="S04-P03 (probable)")
R("P02", "person", s, "5, 17", "Dr. Trimen's description and figure of *C. ledgeriana*" + SEP + "Dr. Trimen, who has seen the Ceylon and Indian plantations, and many mature analyzed trees, knows and has figured *C. Ledgeriana*",
  printed_name="Dr. Trimen", role_as_printed="Dr.", asserted_by="P09",
  stated_detail="Described and figured C. ledgeriana; selected a tree for specimens; has 'seen the Ceylon and Indian plantations, and many mature analyzed trees'.",
  inferred_same_as="S04-P01 (probable)")
R("P03", "person", s, "5", "raised from McIvor's seed by me", printed_name="McIvor", asserted_by="P09",
  stated_detail="Source of the seed from which the figured plant was raised (as printed, 'McIvor's seed'); no title or forename printed.",
  inferred_note="Printed without title or initials; not expanded.")
R("P04", "person", s, "5", "planted on Mahanilu by Mr. Agar", printed_name="Mr. Agar", place_as_printed="Mahanilu", asserted_by="P09",
  stated_detail="Planted the figured plant on Mahanilu.", inferred_same_as="S04-P02 (probable)")
R("P05", "person", s, "5", "its descent from Ledger's original seed is undoubted", printed_name="Ledger", asserted_by="P09",
  stated_detail="'Ledger's original seed' is the stated origin of the figured plant's line.",
  inferred_note="Printed as 'Ledger' only; no forename or title; not expanded. The plant name 'Ledgeriana' is, by common usage, derived from this name, but the text does not say so.")
R("P06", "person", s, "5", "Mr. T. Christy's Bolivian calisaya seedlings", printed_name="Mr. T. Christy", asserted_by="P09",
  stated_detail="Owner of 'Bolivian calisaya seedlings'; spelled 'Christy' (not 'Christie').",
  inferred_note="Spelling 'Christy' differs from 'Christie' (the letter-writer); treated as a different person; not expanded.")
R("P07", "person", s, "9, 13", "Mr. J. A. Campbell of Lindula, Ceylon, who was anxious to have a perfectly authentic strain",
  printed_name="Mr. J. A. Campbell", place_as_printed="Lindula, Ceylon", asserted_by="P09",
  stated_detail="Received three rooted cuttings; wrote to the letter-writer on 5th instant; quoted at length.",
  inferred_same_as="S04-P06 (probable)")
R("P08", "person", s, "13, 15", "according to Mr. Moens' idea of one" + SEP + "Moens' identification of Dr. Trimen's plant",
  printed_name="Mr. Moens", asserted_by="P09",
  stated_detail="Has an 'idea' of a pure-type Ledgeriana tree; identified Dr. Trimen's plant; forwarded seed to Mr. Howard; the writer asks 'why should the infallibility of Moens be relied on'.",
  inferred_same_as="S04-P05 (probable)")
R("P09", "person", s, "1, 3, 19", "MR. T. N. CHRISTIE TO THE RESCUE." + SEP + "St. Andrew's, Maskeliya, 7th June 1883." + SEP + "THOS. NORTH CHRISTIE.",
  printed_name="THOS. NORTH CHRISTIE (signature); MR. T. N. CHRISTIE (title)", place_as_printed="St. Andrew's, Maskeliya",
  date_or_age_as_printed="7th June 1883", stated_detail="Letter-writer; says he raised plants from McIvor's seed ('by me').",
  inferred_same_as="S04-P04 (probable)",
  inferred_note="First-person 'I'/'me'/'my' throughout S03 is read as this person, because the letter is signed by him.")
# ---- plants / seeds
R("T01", "plant", s, "5", "The plant which Dr. Trimen figured was one of those raised from McIvor's seed by me, and planted on Mahanilu by Mr. Agar, and its descent from Ledger's original seed is undoubted.",
  material_kind="plant (tree)", printed_name="The plant which Dr. Trimen figured", place_as_printed="Mahanilu",
  stated_detail="One of those raised from McIvor's seed by the writer; planted on Mahanilu by Mr. Agar; descent from Ledger's original seed 'undoubted'; also called 'the Ledger figured by Dr. Trimen' and 'his figured type'.",
  asserted_by="P09", inferred_same_as="S04-T01 (probable)")
R("T02", "plant", s, "5", "Other plants, exactly similar in blossom, raised from the same pinch of seed, have given over 12, 13 and 14 per cent sulphate of quinine",
  material_kind="plant group", printed_name="Other plants, exactly similar in blossom, raised from the same pinch of seed",
  stated_detail="Analyses 'over 12, 13 and 14 per cent sulphate of quinine'.", asserted_by="P09",
  inferred_note="'the same pinch of seed' is read as the seed that produced S03-T01; the three analyses are not tied to individual plants or dates.")
R("T03", "plant", s, "5", "the very trees which Mr. Howard called in to help him, the Yarrow Ledgers, have the same blossom, and came out of the same nursery bed as the Ledger figured by Dr. Trimen!",
  material_kind="tree group", printed_name="the Yarrow Ledgers", asserted_by="P09",
  stated_detail="Called in by Mr. Howard 'to help him'; 'have the same blossom'; 'came out of the same nursery bed'.",
  inferred_note="'Yarrow' appears to be a place or owner's name but the text does not say.")
R("T04", "plant", s, "5", "Dr. Trimen selected a tree here for specimens, as being botanically a typical Ledger, and his selection was well borne out, when, on the following day, the analysis of that very tree arrived from England and showed 11.29 S.",
  material_kind="tree", printed_name="a tree [selected by Dr. Trimen]", place_as_printed="here",
  stated_detail="Selected 'as being botanically a typical Ledger'; its analysis 'showed 11.29 S.' (analysis arrived the following day).", asserted_by="P09",
  inferred_note="'here' is read as the place named in the dateline (St. Andrew's, Maskeliya). 'S.' is read as sulphate of quinine; the text does not spell this out. Percentage unit not printed.")
R("T05", "plant", s, "5", "When Mr. Howard goes on to identify by these characteristics Mr. T. Christy's Bolivian calisaya seedlings as true Ledgerianas" + SEP + "I have some of Mr. T. Christy's Bolivian plants, 18 months old, and I most certainly say they are not Ledgers. They seem to be Calisayas of some kind",
  material_kind="seedlings / plants", printed_name="Mr. T. Christy's Bolivian calisaya seedlings", date_or_age_as_printed="18 months old",
  stated_detail="Identified by Mr. Howard as true Ledgerianas; the writer says they 'are not Ledgers' and 'seem to be Calisayas of some kind'; the writer has some.",
  asserted_by="P09",
  inferred_note="'seedlings' and 'plants' are read as the same stock (the second sentence says 'some of ... plants').")
R("T06", "plant", s, "5", "Dr. Trimen's illustration of the blossom (but not of the tree itself) is particularly good, a contrast to that given in Howard's great work, where the figured plant is far from being a typical Ledgeriana, if indeed it is one at all.",
  material_kind="figured plant (illustration)", printed_name="the figured plant [in Howard's great work]",
  date_or_age_as_printed="written '9 months ago, in the Dikoya essay'",
  stated_detail="Quoted from the writer's own earlier essay; the plant figured is 'far from being a typical Ledgeriana, if indeed it is one at all'.", asserted_by="P09",
  inferred_note="Also referred to as 'Mr. Howard's figured \"Ledgeriana\"' (line 5), read as the same figured plant. Title of Howard's 'great work' not printed.")
R("T07", "plant", s, "5", "the misunderstanding which arose about the Annfield and Emelina Calisayas, some two years ago",
  material_kind="plant group", printed_name="the Annfield and Emelina Calisayas", date_or_age_as_printed="some two years ago",
  stated_detail="Subject of a 'misunderstanding'; 'most of these Calisayas seemed exactly similar to Mr. Howard's figured \"Ledgeriana\"'.", asserted_by="P09",
  inferred_note="'Annfield' and 'Emelina' read as the names of two Calisaya stocks (or places); text does not say.")
R("T08", "plant", s, "7", "In 1876, some seed was received at Kew from Java, and part of this was communicated to Mr. J. E. Howard, F. R. S., who raised seedlings.",
  material_kind="seed", printed_name="some seed [received at Kew from Java]", place_as_printed="Kew; Java",
  date_or_age_as_printed="1876", stated_detail="Part of it communicated to Mr. J. E. Howard. Elsewhere (line 15) the writer says Mr. Howard 'wishes to believe' that 'the first seed received at Kew was genuine'.",
  asserted_by="Kew Gardens Report for 1880, p. 12 (as quoted by S03-P09)",
  inferred_same_as="'the first seed received at Kew' (line 15) (probable)")
R("T09", "plant", s, "7, 9", "who raised seedlings. He carefully selected the most promising of these," + SEP + "very kindly supplied Kew with cuttings both of the figured and of another selected plant in the course of last year.",
  material_kind="seedlings and cuttings", printed_name="the figured [plant] and another selected plant",
  date_or_age_as_printed="'in the course of last year' (relative to the 1880 Report)",
  stated_detail="Cuttings of 'both the figured and ... another selected plant' were supplied to Kew.", asserted_by="Kew Gardens Report for 1880, p. 12 (as quoted by S03-P09)",
  inferred_note="'last year' is relative to the Report, so the calendar year is not printed; it would be 1879 if the Report year is the publication year, but this is NOT stated. 'the figured' [plant] presumably = S03-T06.")
R("T10", "plant", s, "9", "Three of the rooted cuttings were given to Mr. J. A. Campbell of Lindula, Ceylon, who was anxious to have a perfectly authentic strain.",
  material_kind="rooted cuttings (3)", printed_name="Three of the rooted cuttings", place_as_printed="Lindula, Ceylon",
  stated_detail="Given to Mr. J. A. Campbell, 'anxious to have a perfectly authentic strain'.", asserted_by="Kew Gardens Report for 1880, p. 12 (as quoted by S03-P09)")
R("T11", "plant", s, "11", "Three other plants, imported at Kew from the same authentic strain were sent to Jamaica.",
  material_kind="plants (3)", printed_name="Three other plants, imported at Kew from the same authentic strain", place_as_printed="Jamaica",
  stated_detail="Sent to Jamaica.", asserted_by="Kew Gardens Report for 1880, p. 12 (as quoted by S03-P09)",
  reading_status="uncertain", reading_note="The paragraph heading is printed '*Indonesia*.—' but the content concerns Jamaica; probably a misprint or OCR error for 'Jamaica.'. Heading transcribed as printed; location taken from the sentence.")
R("T12", "plant", s, "13", "those \"authentic\" cuttings, which I have seen in the Waltrim clearing, are not Ledgerianas at all",
  material_kind="cuttings", printed_name="those \"authentic\" cuttings", place_as_printed="the Waltrim clearing",
  stated_detail="Writer says they 'are not Ledgerianas at all'.", asserted_by="P09",
  inferred_same_as="S03-T10 (probable: 'authentic' cuttings from Mr. Howard to Mr. Campbell)",
  inferred_note="The 'Waltrim clearing' is not said to be Mr. Campbell's, though Campbell's trees are discussed in the next sentence; ownership is inferred only.")
R("T13", "plant", s, "13", "the trees I have (raised from cuttings received from Mr. Howard) Ledgerianas. Two of them are very shrubby in their growth, and with hard shiny leaves. The other is a Calisaya of the broad-leaved variety, very much like what I believe is called in Java *Calisaya Anglica*.",
  material_kind="trees (3, from cuttings)", printed_name="the trees I have (raised from cuttings received from Mr. Howard)",
  stated_detail="Two 'very shrubby in their growth, and with hard shiny leaves'; the other 'a Calisaya of the broad-leaved variety'.",
  asserted_by="P07 (quoted letter of 5th instant, as quoted by S03-P09)",
  reading_note="Span is a trimmed excerpt that begins mid-sentence ('...would think of calling the trees I have (...) Ledgerianas.').",
  inferred_note="The count of three is inferred from 'Two of them ... The other' and from the earlier 'Three of the rooted cuttings'. 'I' in the quotation is Mr. Campbell (quoted letter), not the letter-writer.")
R("T14", "plant", s, "13", "I have also another plant that Mr. Howard kindly gave me which I understood him to say had been raised from Ledgeriana seed received from Java. This is the best, so far as appearance goes, but I should not call it a Ledgeriana.",
  material_kind="plant", printed_name="another plant that Mr. Howard kindly gave me",
  stated_detail="Said (as understood) to be raised from Ledgeriana seed received from Java; 'the best, so far as appearance goes'; 'I should not call it a Ledgeriana'.",
  asserted_by="P07 (quoted letter of 5th instant, as quoted by S03-P09)")
R("T15", "plant", s, "5", "Ledger's original seed", material_kind="seed", printed_name="Ledger's original seed", asserted_by="P09",
  stated_detail="Stated origin of the figured plant's descent.")
R("T16", "plant", s, "5", "raised from McIvor's seed by me" + SEP + "the same pinch of seed", material_kind="seed", printed_name="McIvor's seed ('the same pinch of seed')",
  asserted_by="P09", stated_detail="Seed from which the figured plant and 'other plants' were raised.",
  inferred_note="'the same pinch of seed' is read as McIvor's seed; relation of McIvor's seed to Ledger's original seed is not stated beyond 'descent'.")
R("T17", "plant", s, "15", "he asserts that other seed forwarded to him by Mr. Moens as true Ledgeriana turned out to be nothing of the kind",
  material_kind="seed", printed_name="other seed forwarded to him by Mr. Moens", stated_detail="Mr. Howard 'asserts' it was not true Ledgeriana.", asserted_by="P09")
# ---- samples
R("B01", "sample", s, "5", "the analysis of that very tree arrived from England and showed 11.29 S.",
  material_kind="analysis (sample material not stated)", printed_name="the analysis of that very tree",
  stated_detail="Arrived from England on the day after Dr. Trimen selected the tree; 'showed 11.29 S.'.", asserted_by="P09",
  inferred_note="Whether bark was analysed is not stated here. 'S.' read as sulphate of quinine (unit not spelled out).")
# ---- actions / relationships
R("A01", "action", s, "5", "raised from McIvor's seed by me", subject_id="P09", verb_as_printed="raised from McIvor's seed", object_id="T01", asserted_by="P09")
R("A02", "action", s, "5", "planted on Mahanilu by Mr. Agar", subject_id="P04", verb_as_printed="planted on Mahanilu", object_id="T01", place_as_printed="Mahanilu", asserted_by="P09")
R("A03", "action", s, "5", "its descent from Ledger's original seed is undoubted", subject_id="T01", verb_as_printed="descent from", object_id="T15", asserted_by="P09")
R("A04", "action", s, "5", "Other plants, exactly similar in blossom, raised from the same pinch of seed", subject_id="T02", verb_as_printed="raised from the same pinch of seed",
  object_id="T16", asserted_by="P09")
R("A05", "action", s, "5", "came out of the same nursery bed as the Ledger figured by Dr. Trimen", subject_id="T03", verb_as_printed="came out of the same nursery bed as", object_id="T01", asserted_by="P09")
R("A06", "action", s, "5", "the very trees which Mr. Howard called in to help him, the Yarrow Ledgers", subject_id="P01", verb_as_printed="called in to help him", object_id="T03", asserted_by="P09")
R("A07", "action", s, "5", "Dr. Trimen selected a tree here for specimens", subject_id="P02", verb_as_printed="selected ... for specimens", object_id="T04", place_as_printed="here", asserted_by="P09")
R("A08", "action", s, "5", "the analysis of that very tree arrived from England", subject_id="B01", verb_as_printed="analysis of that very tree", object_id="T04", asserted_by="P09")
R("A09", "action", s, "5", "The statement that the \"satin gloss and hairy margin of the leaves\" was put forward as a characteristic of true Ledgerianas is almost incredible.",
  subject_id="", verb_as_printed="was put forward as a characteristic of true Ledgerianas", object_id="", asserted_by="P09",
  inferred_same_as="agent probably S03-P01 (Mr. Howard)",
  inferred_note="The text does not name who put the statement forward; the next sentence discusses Mr. Howard's use of 'these characteristics' and the opening refers to 'Mr. Howard's latest paper'.")
R("A10", "action", s, "5", "When Mr. Howard goes on to identify by these characteristics Mr. T. Christy's Bolivian calisaya seedlings as true Ledgerianas",
  subject_id="P01", verb_as_printed="identify ... as true Ledgerianas", object_id="T05", asserted_by="P09")
R("A11", "action", s, "5", "I have some of Mr. T. Christy's Bolivian plants, 18 months old, and I most certainly say they are not Ledgers.",
  subject_id="P09", verb_as_printed="have some of ...; say they are not Ledgers", object_id="T05", asserted_by="P09")
R("A12", "action", s, "5", "Mr. T. Christy's Bolivian calisaya seedlings", subject_id="P06", verb_as_printed="'s (possessive)", object_id="T05",
  asserted_by="P09", inferred_note="Ownership is read from the possessive; no verb of owning is printed.")
R("A13", "action", s, "5", "is to a great extent due to Mr. Howard himself", subject_id="P01", verb_as_printed="is to a great extent due to",
  object_id="", asserted_by="P09",
  stated_detail="Writer's claim that Ledgeriana-labelled cinchonas in Ceylon (and he suspects Jamaica) which are 'not that plant' are largely Mr. Howard's responsibility.")
R("A14", "action", s, "5", "most of these Calisayas seemed exactly similar to Mr. Howard's figured \"Ledgeriana\"", subject_id="T07",
  verb_as_printed="seemed exactly similar to", object_id="T06", asserted_by="P09")
R("A15", "action", s, "5", "here I may quote what I wrote 9 months ago, in the Dikoya essay", subject_id="P09",
  verb_as_printed="wrote ... in the Dikoya essay", object_id="P02", date_or_age_as_printed="9 months ago",
  stated_detail="Praised 'Dr. Trimen's illustration of the blossom (but not of the tree itself)'; criticised Howard's figured plant (S03-T06).",
  asserted_by="P09", inferred_note="Object recorded as Dr. Trimen because his illustration is the subject; the Dikoya essay is a publication not otherwise identified.")
R("A16", "action", s, "7", "some seed was received at Kew from Java", subject_id="", verb_as_printed="was received at Kew from Java", object_id="T08",
  place_as_printed="Kew; Java", date_or_age_as_printed="1876", asserted_by="Kew Gardens Report for 1880, p. 12 (as quoted by S03-P09)",
  inferred_note="Receiver stated only as 'Kew'; not a person record.")
R("A17", "action", s, "7", "part of this was communicated to Mr. J. E. Howard, F. R. S.", subject_id="", verb_as_printed="was communicated to", object_id="T08",
  recipient_id="P01", asserted_by="Kew Gardens Report for 1880, p. 12 (as quoted by S03-P09)")
R("A18", "action", s, "7", "who raised seedlings", subject_id="P01", verb_as_printed="raised seedlings", object_id="T09", asserted_by="Kew Gardens Report for 1880, p. 12 (as quoted by S03-P09)")
R("A19", "action", s, "7, 9", "very kindly supplied Kew with cuttings both of the figured and of another selected plant", subject_id="P01",
  verb_as_printed="supplied Kew with cuttings", object_id="T09", asserted_by="Kew Gardens Report for 1880, p. 12 (as quoted by S03-P09)",
  date_or_age_as_printed="in the course of last year",
  inferred_note="Subject 'he' (Mr. Howard) follows 'He carefully selected the most promising of these'.")
R("A20", "action", s, "9", "Three of the rooted cuttings were given to Mr. J. A. Campbell of Lindula, Ceylon", subject_id="", verb_as_printed="were given to",
  object_id="T10", recipient_id="P07", asserted_by="Kew Gardens Report for 1880, p. 12 (as quoted by S03-P09)",
  inferred_note="Giver not named; Kew is the probable giver.")
R("A21", "action", s, "11", "Three other plants, imported at Kew from the same authentic strain were sent to Jamaica.", subject_id="",
  verb_as_printed="were sent to Jamaica", object_id="T11", place_as_printed="Jamaica", asserted_by="Kew Gardens Report for 1880, p. 12 (as quoted by S03-P09)",
  reading_status="uncertain", reading_note="See S03-T11 (heading printed 'Indonesia').")
R("A22", "action", s, "13", "those \"authentic\" cuttings, which I have seen in the Waltrim clearing", subject_id="P09", verb_as_printed="have seen",
  object_id="T12", place_as_printed="the Waltrim clearing", asserted_by="P09")
R("A23", "action", s, "13", "Mr. Campbell himself writes to me on 5th instant", subject_id="P07", verb_as_printed="writes to me", object_id="P09",
  date_or_age_as_printed="5th instant", asserted_by="P09")
R("A24", "action", s, "13", "the trees I have (raised from cuttings received from Mr. Howard)", subject_id="P01", verb_as_printed="cuttings received from",
  object_id="T13", recipient_id="P07", asserted_by="P07 (quoted letter of 5th instant, as quoted by S03-P09)")
R("A25", "action", s, "13", "I have also another plant that Mr. Howard kindly gave me", subject_id="P01", verb_as_printed="kindly gave me",
  object_id="T14", recipient_id="P07", asserted_by="P07 (quoted letter of 5th instant, as quoted by S03-P09)")
R("A26", "action", s, "15", "He clings to \"Mr. Moens' own authority\" only so far as he himself wishes to believe, viz., that the first seed received at Kew was genuine",
  subject_id="P01", verb_as_printed="clings to ... authority", object_id="P08", asserted_by="P09",
  stated_detail="Writer's claim: Mr. Howard relies on Mr. Moens' authority only as to the first Kew seed being genuine (S03-T08).")
R("A27", "action", s, "15", "he repudiates Moens' identification of Dr. Trimen's plant", subject_id="P01", verb_as_printed="repudiates ... identification of",
  object_id="T01", asserted_by="P09",
  inferred_note="'Dr. Trimen's plant' is read as S03-T01; the identifier of the plant (Moens) is recorded in the text.")
R("A28", "action", s, "15", "other seed forwarded to him by Mr. Moens as true Ledgeriana", subject_id="P08", verb_as_printed="forwarded ... as true Ledgeriana",
  object_id="T17", recipient_id="P01", asserted_by="P09")
R("A29", "action", s, "15", "he asserts that other seed forwarded to him by Mr. Moens as true Ledgeriana turned out to be nothing of the kind",
  subject_id="P01", verb_as_printed="asserts ... turned out to be nothing of the kind", object_id="T17", asserted_by="P09")
R("A30", "action", s, "17", "Dr. Trimen, who has seen the Ceylon and Indian plantations, and many mature analyzed trees, knows and has figured *C. Ledgeriana*",
  subject_id="P02", verb_as_printed="knows and has figured", object_id="T01", asserted_by="P09",
  inferred_note="Object in the text is the species 'C. Ledgeriana', not the specific plant; link to S03-T01 is by context (title and first paragraph).")
R("A31", "action", s, "17", "Mr. Howard, with the knowledge of hot-house plants and dried specimens, does not know and has not figured *C. Ledgeriana*",
  subject_id="P09", verb_as_printed="concludes ... does not know and has not figured", object_id="P01", asserted_by="P09")

# ============================================================== validation
def norm(t):
    return re.sub(r"\s+", " ", t).strip()

source_text = {}
for sid, meta in SOURCES.items():
    p = os.path.join(SRC_DIR, meta["file"])
    with open(p, encoding="utf-8") as fh:
        source_text[sid] = norm(fh.read())

ids = {r["record_id"] for r in RECORDS}
good, failed = [], []
for r in RECORDS:
    problems = []
    # verbatim check
    for seg in r["printed_text"].split(SEP):
        if norm(seg) not in source_text[r["source_id"]]:
            problems.append(f"printed_text segment not found verbatim in {SOURCES[r['source_id']]['file']}: {seg[:70]!r}")
    # id references
    for fld in ("subject_id", "object_id", "recipient_id"):
        for ref in [x for x in re.split(r";\s*", r[fld]) if x]:
            if ref not in ids:
                problems.append(f"{fld} {ref!r} is not a record_id")
    if len({x["record_id"] for x in RECORDS if x["record_id"] == r["record_id"]}) and \
       sum(1 for x in RECORDS if x["record_id"] == r["record_id"]) > 1:
        problems.append("duplicate record_id")
    if problems:
        r = dict(r, validation_problems=problems)
        failed.append(r)
    else:
        good.append(r)

out = {
    "meta": {
        "sources": SOURCES, "fields": FIELDS,
        "note": "Local record identifiers only. No Wikidata or other authority identifiers. "
                "Columns beginning 'inferred_' and 'outside_identification' are NOT stated by the sources.",
        "counts": {"records_ok": len(good), "records_failed": len(failed),
                   **{t: sum(1 for r in good if r['record_type'] == t) for t in ("person", "plant", "sample", "action")},
                   "uncertain_readings": sum(1 for r in good if r["reading_status"] != "clear")},
    },
    "records": good,
    "failed_records": failed,
}
with open(os.path.join(HERE, "02_records.json"), "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=2)
with open(os.path.join(HERE, "02_records.csv"), "w", encoding="utf-8", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=FIELDS)
    w.writeheader()
    w.writerows(good)
with open(os.path.join(HERE, "02_validation.txt"), "w", encoding="utf-8") as fh:
    fh.write(json.dumps(out["meta"]["counts"], indent=2) + "\n")
    for r in failed:
        fh.write(f"FAILED {r['record_id']}: " + " | ".join(r["validation_problems"]) + "\n")
print(json.dumps(out["meta"]["counts"]))
for r in failed:
    print("FAILED", r["record_id"], r["validation_problems"])
