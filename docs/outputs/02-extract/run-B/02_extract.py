#!/usr/bin/env python3
"""
02_extract.py -- structured records from two Tropical Agriculturist passages (July 1883).

Sources
  S03  The Tropical Agriculturist, July 1883, p. 37  (file S03_ocr.txt)
       "DR. TRIMEN'S LEDGERIANA: MR. T. N. CHRISTIE TO THE RESCUE."
  S04  The Tropical Agriculturist, July 1883, p. 66  (file S04_ocr.txt)
       "DR. TRIMEN'S TYPICAL LEDGERIANA TREE."

Fields follow B/01_structure.md (the agreed structure).

How to run (offline, python3 only, no third-party packages):

    python3 02_extract.py [--sources DIR] [--out DIR]

  --sources DIR   directory containing S03_ocr.txt and S04_ocr.txt
                  (default: the parent of the directory this script is in)
  --out DIR       where to write 02_records.json and 02_records.csv
                  (default: the directory this script is in)

What the script does
  1. Holds the records below as data (they were read off the OCR text by hand;
     there is no model call and no network access).
  2. Validates them: unique ids, every subject/object id resolves, and -- if the
     OCR files are present -- every `quote` and every parenthetical-free
     `description_as_printed` phrase occurs verbatim in the named source file.
     Any failure is printed to stderr and the run exits non-zero.
  3. Writes 02_records.json (lists kept as arrays) and 02_records.csv
     (lists joined with " | ").
  4. Prints a short report: counts by type, records with reading_status
     "uncertain" or "failed", records with non-empty `inferred`.

Source line numbers (l.N) refer to the line numbering of the OCR files.
"""

import argparse
import csv
import json
import os
import re
import sys

FIELDS = [
    "record_id", "record_type", "label_as_printed", "variants_as_printed",
    "description_as_printed", "action_type", "subject_ids", "object_ids",
    "date_as_printed", "place_as_printed", "source_ref", "quote",
    "inferred", "reading_status", "outside_identification",
]
LIST_FIELDS = {"variants_as_printed", "description_as_printed", "subject_ids", "object_ids"}

SRC = {
    "S03": "The Tropical Agriculturist, July 1883, p. 37 (S03_ocr.txt",
    "S04": "The Tropical Agriculturist, July 1883, p. 66 (S04_ocr.txt",
}


def ref(*parts):
    """ref(('S03', 'l.5'), ('S04', 'l.3, l.17')) -> source_ref string."""
    return "; ".join(f"{SRC[s]} {lines})" for s, lines in parts)


def rec(record_id, record_type, label_as_printed, **kw):
    r = {f: ([] if f in LIST_FIELDS else "") for f in FIELDS}
    r.update(record_id=record_id, record_type=record_type, label_as_printed=label_as_printed,
             reading_status="ok")
    for k, v in kw.items():
        if k not in FIELDS:
            raise KeyError(f"{record_id}: unknown field {k}")
        r[k] = v
    return r


OUTSIDE_FLAG = ("UNVERIFIED candidate from the assistant's background knowledge, not from the "
                "source and not checked against any authority: ")

# --------------------------------------------------------------------------
# PEOPLE
# --------------------------------------------------------------------------
PEOPLE = [
    rec("PER-01", "person", "Dr. Trimen",
        variants_as_printed=["DR. TRIMEN'S (S03 l.1; S04 l.1)", "Dr. Trimen (S03 l.5, l.15, l.17; S04 l.3, l.9, l.11)"],
        description_as_printed=[
            "Dr. Trimen, who has seen the Ceylon and Indian plantations, and many mature analyzed trees, knows and has figured *C. Ledgeriana* (S03 l.17)"],
        source_ref=ref(("S03", "l.1, l.5, l.15, l.17"), ("S04", "l.1, l.3, l.9, l.11")),
        quote="DR. TRIMEN'S TYPICAL LEDGERIANA TREE.",
        inferred="The 'Dr. Trimen' of S03 and of S04 are taken to be the same person (same surname, same controversy, same issue of the journal); neither passage gives a forename.",
        outside_identification=OUTSIDE_FLAG + "Henry Trimen, Director of the Royal Botanic Gardens, Peradeniya, Ceylon."),
    rec("PER-02", "person", "THOS. NORTH CHRISTIE",
        variants_as_printed=["MR. T. N. CHRISTIE (S03 l.1)", "Mr. Christie (S04 l.7)"],
        description_as_printed=[
            "after having lived for years beside mature Ledgerianas, which have given the highest analyses we have yet heard of (S03 l.13)"],
        date_as_printed="7th June 1883",
        place_as_printed="St. Andrew's, Maskeliya",
        source_ref=ref(("S03", "l.1, l.3, l.19"), ("S04", "l.7")),
        quote="THOS. NORTH CHRISTIE.",
        inferred="The expansion T. N. = Thos. North is supplied by S03 itself (title and signature of one letter). Linking the 'Mr. Christie' of S04 ('what Mr. Christie has written on the subject of Ledgerianas') to the author of S03 is my inference from the shared subject; S04 does not name him further.",
        reading_status="ok"),
    rec("PER-03", "person", "Mr. J. E. Howard, F. R. S.",
        variants_as_printed=["Mr. J. E. Howard (S03 l.5)", "Mr. Howard (S03 l.5, l.13, l.15, l.17; S04 l.3, l.11)", "Howard's (S03 l.5)"],
        description_as_printed=[
            "Mr. Howard, with the knowledge of hot-house plants and dried specimens, does not know and has not figured *C. Ledgeriana* (S03 l.17)"],
        source_ref=ref(("S03", "l.5, l.7, l.13, l.15, l.17"), ("S04", "l.3, l.11")),
        quote="part of this was communicated to Mr. J. E. Howard, F. R. S., who raised seedlings.",
        inferred="The fullest printed form ('Mr. J. E. Howard, F. R. S.') occurs inside S03's quotation from the Kew Gardens Report for 1880, not in Christie's own words. All 'Mr. Howard' mentions in S03 and S04 are taken to be this one person.",
        outside_identification=OUTSIDE_FLAG + "John Eliot Howard, quinologist, of Tottenham."),
    rec("PER-04", "person", "WALTER AGAR",
        variants_as_printed=["Mr. Agar (S04 l.3)", "Mr. Agar (S03 l.5)"],
        description_as_printed=[
            "a letter from Mr. Agar, which places beyond question the fact that the tree figured by Dr. Trimen was an undoubted Ledgeriana (S04 l.3)",
            "planted on Mahanilu by Mr. Agar (S03 l.5)"],
        date_as_printed="June 22nd, 1883",
        place_as_printed="Lawrence",
        source_ref=ref(("S04", "l.3, l.5, l.17"), ("S03", "l.5")),
        quote="WALTER AGAR.",
        inferred="Within S04 the editor's 'Mr. Agar' and the signature 'WALTER AGAR' belong to the same letter, so the expansion is given by the source. Treating the 'Mr. Agar' of S03 (who planted the figured tree on Mahanilu) as the same man is my inference from the shared subject and estate, not a statement in either passage."),
    rec("PER-05", "person", "Mr. Moens",
        variants_as_printed=["Moens (S03 l.15)", "Mr. Moens' (S03 l.13, l.15)"],
        source_ref=ref(("S03", "l.13, l.15"), ("S04", "l.11, l.13")),
        quote="It was one of several Mr. Moens saw in flower at Mahanillu estate, Dr. Trimen was with Mr. Moens, and both agreed the trees were true Ledgerianas.",
        inferred="Same person assumed across S03 and S04; no forename printed.",
        outside_identification=OUTSIDE_FLAG + "J. C. Bernelot Moens, Director of the Government cinchona plantations, Java."),
    rec("PER-06", "person", "McIvor",
        description_as_printed=["raised from McIvor's seed (S03 l.5)"],
        source_ref=ref(("S03", "l.5")),
        quote="The plant which Dr. Trimen figured was one of those raised from McIvor's seed by me, and planted on Mahanilu by Mr. Agar, and its descent from Ledger's original seed is undoubted.",
        inferred="Mentioned only as the source of seed; no title or forename printed.",
        outside_identification=OUTSIDE_FLAG + "William Graham McIvor, superintendent of the Government cinchona plantations, Nilgiris, India."),
    rec("PER-07", "person", "Ledger",
        description_as_printed=["its descent from Ledger's original seed is undoubted (S03 l.5)"],
        source_ref=ref(("S03", "l.5")),
        quote="its descent from Ledger's original seed is undoubted.",
        inferred="Only 'Ledger's original seed' refers to the person; 'the Yarrow Ledgers', 'the Ledger figured by Dr. Trimen', 'a typical Ledger' and 'not Ledgers' are read as names for trees/varieties and are recorded under plants, not here.",
        outside_identification=OUTSIDE_FLAG + "Charles Ledger, after whom Cinchona ledgeriana is named."),
    rec("PER-08", "person", "Mr. T. Christy",
        description_as_printed=["Mr. T. Christy's Bolivian calisaya seedlings (S03 l.5)", "Mr. T. Christy's Bolivian plants (S03 l.5)"],
        source_ref=ref(("S03", "l.5")),
        quote="I have some of Mr. T. Christy's Bolivian plants, 18 months old, and I most certainly say they are not Ledgers.",
        inferred="Read as a different person from the author (PER-02, 'Christie'): the spelling 'Christy' is printed consistently twice, and the author speaks of 'Mr. T. Christy's' plants in the third person while writing in the first person about his own. The spelling difference could in principle be an OCR or printer's variant, so this is flagged.",
        reading_status="uncertain",
        outside_identification=OUTSIDE_FLAG + "Thomas Christy, London drug merchant and importer of cinchona seed."),
    rec("PER-09", "person", "Mr. J. A. Campbell of Lindula, Ceylon",
        variants_as_printed=["Mr. Campbell (S03 l.13)", "Mr. Campbell (S04 l.11)"],
        description_as_printed=["who was anxious to have a perfectly authentic strain (S03 l.9)"],
        place_as_printed="Lindula, Ceylon",
        source_ref=ref(("S03", "l.9, l.13"), ("S04", "l.11")),
        quote="Three of the rooted cuttings were given to Mr. J. A. Campbell of Lindula, Ceylon, who was anxious to have a perfectly authentic strain.",
        inferred="Within S03 the link between the Kew Report's 'Mr. J. A. Campbell of Lindula' and 'Mr. Campbell himself writes to me' is made by the source. The 'Mr. Campbell' of S04 who sent bark to Mr. Howard is linked to him by my inference only."),
    rec("PER-10", "person", "Ed.",
        description_as_printed=["[We publish below a letter from Mr. Agar ... —Ed.] (S04 l.3)"],
        source_ref=ref(("S04", "l.3")),
        quote="[We publish below a letter from Mr. Agar, which places beyond question the fact that the tree figured by Dr. Trimen was an undoubted Ledgeriana, Mr. Howard himself having given testimony to that effect after having analyzed the bark.—Ed.]",
        inferred="The unnamed editor of the journal. Both letters open 'DEAR SIR'; the addressee is assumed to be this editor, which the text does not state."),
]

# --------------------------------------------------------------------------
# PLANTS / TREES
# --------------------------------------------------------------------------
PLANTS = [
    rec("PLT-01", "plant", "The tree, which was sketched for Dr. Trimen's work",
        variants_as_printed=["The plant which Dr. Trimen figured (S03 l.5)", "the Ledger figured by Dr. Trimen (S03 l.5)",
                             "his figured type (S03 l.5)", "Dr. Trimen's plant (S03 l.15)", "the tree figured by Dr. Trimen (S04 l.3)",
                             "DR. TRIMEN'S TYPICAL LEDGERIANA TREE (S04 l.1)"],
        description_as_printed=[
            "is dead (S04 l.9)",
            "one of those raised from McIvor's seed by me, and planted on Mahanilu by Mr. Agar, and its descent from Ledger's original seed is undoubted (S03 l.5)",
            "It was one of several Mr. Moens saw in flower at Mahanillu estate (S04 l.11)",
            "an undoubted Ledgeriana (S04 l.3)"],
        place_as_printed="Mahanilu (S03 l.5); Mahanillu estate (S04 l.11)",
        source_ref=ref(("S03", "l.5, l.15"), ("S04", "l.1, l.3, l.9, l.11, l.15")),
        quote="The tree, which was sketched for Dr. Trimen's work, is dead.",
        inferred="The plant Christie says Trimen 'figured' (S03) and the tree Agar says was 'sketched for Dr. Trimen's work' (S04) are treated as one tree; both are placed at Mahanil(l)u. The two spellings Mahanilu/Mahanillu are kept as printed."),
    rec("PLT-02", "plant", "Other plants, exactly similar in blossom, raised from the same pinch of seed",
        description_as_printed=["have given over 12, 13 and 14 per cent sulphate of quinine (S03 l.5)"],
        source_ref=ref(("S03", "l.5")),
        quote="Other plants, exactly similar in blossom, raised from the same pinch of seed, have given over 12, 13 and 14 per cent sulphate of quinine;",
        inferred="Probably the same trees as the 'mature Ledgerianas, which have given the highest analyses we have yet heard of' beside which Christie says he has lived (S03 l.13); the text does not make this identification explicit. Location not stated (Christie raised them; S03 is written from St. Andrew's, Maskeliya)."),
    rec("PLT-03", "plant", "the Yarrow Ledgers",
        description_as_printed=[
            "the very trees which Mr. Howard called in to help him, the Yarrow Ledgers, have the same blossom, and came out of the same nursery bed as the Ledger figured by Dr. Trimen! (S03 l.5)"],
        source_ref=ref(("S03", "l.5")),
        quote="the very trees which Mr. Howard called in to help him, the Yarrow Ledgers, have the same blossom, and came out of the same nursery bed as the Ledger figured by Dr. Trimen!",
        inferred="'Yarrow' is presumably an estate name, but the text gives it only as part of the trees' name, so it is not entered as a place."),
    rec("PLT-04", "plant", "a tree here",
        description_as_printed=["as being botanically a typical Ledger (S03 l.5)",
                                "the analysis of that very tree arrived from England and showed 11.29 S. (S03 l.5)"],
        place_as_printed="here",
        source_ref=ref(("S03", "l.5")),
        quote="Before the least doubt had been thrown upon his figured type, Dr. Trimen selected a tree here for specimens, as being botanically a typical Ledger, and his selection was well borne out, when, on the following day, the analysis of that very tree arrived from England and showed 11.29 S.",
        inferred="'here' is read as the place of writing, St. Andrew's, Maskeliya (S03 l.3). '11.29 S.' is read as 11.29 per cent sulphate of quinine by analogy with 'per cent sulphate of quinine' earlier in the same paragraph; the abbreviation is not explained in the text.",
        reading_status="uncertain"),
    rec("PLT-05", "plant", "Mr. T. Christy's Bolivian calisaya seedlings",
        variants_as_printed=["Mr. T. Christy's Bolivian plants, 18 months old (S03 l.5)"],
        description_as_printed=["I most certainly say they are not Ledgers. They seem to be Calisayas of some kind, but are as protean in appearance as they have been in name. (S03 l.5)"],
        date_as_printed="18 months old",
        source_ref=ref(("S03", "l.5")),
        quote="When Mr. Howard goes on to identify by these characteristics Mr. T. Christy's Bolivian calisaya seedlings as true Ledgerianas, his bases are as reliable as those by which a gipsy foretells your fortune.",
        inferred="The seedlings Howard identified and the 18-month-old plants Christie holds are treated as the same stock; the text implies but does not state this."),
    rec("PLT-06", "plant", "the Annfield and Emelina Calisayas",
        description_as_printed=["most of these Calisayas seemed exactly similar to Mr. Howard's figured \"Ledgeriana\" (S03 l.5)"],
        date_as_printed="some two years ago",
        source_ref=ref(("S03", "l.5")),
        quote="We all remember the misunderstanding which arose about the Annfield and Emelina Calisayas, some two years ago, due chiefly to the fact that most of these Calisayas seemed exactly similar to Mr. Howard's figured \"Ledgeriana\";",
        inferred="Annfield and Emelina are presumably estate names; not entered as places because the text uses them only as part of the plants' name. 'some two years ago' relative to June 1883 would be c. 1881."),
    rec("PLT-07", "plant", "Mr. Howard's figured \"Ledgeriana\"",
        variants_as_printed=["the figured plant (S03 l.5)", "the figured (S03 l.9, in the Kew Report quotation)"],
        description_as_printed=["where the figured plant is far from being a typical Ledgeriana, if indeed it is one at all (S03 l.5, quoting the Dikoya essay)"],
        source_ref=ref(("S03", "l.5, l.9")),
        quote="a contrast to that given in Howard's great work, where the figured plant is far from being a typical Ledgeriana, if indeed it is one at all.",
        inferred="The Kew Report's 'cuttings both of the figured and of another selected plant' is read as referring to this same figured plant of Howard's; the report quotation does not say so in as many words."),
    rec("PLT-08", "plant", "some seed was received at Kew from Java",
        variants_as_printed=["the first seed received at Kew (S03 l.15)", "the same authentic strain (S03 l.11)"],
        description_as_printed=["Mr. J. E. Howard, F. R. S., who raised seedlings. He carefully selected the most promising of these (S03 l.7)"],
        date_as_printed="In 1876",
        place_as_printed="Kew; Java",
        source_ref=ref(("S03", "l.7, l.9, l.11, l.15")),
        quote="In 1876, some seed was received at Kew from Java, and part of this was communicated to Mr. J. E. Howard, F. R. S., who raised seedlings.",
        inferred="The 1876 Java seed, Howard's seedlings from it, and 'the first seed received at Kew' (S03 l.15) are treated as one lot; the identification of the l.15 phrase with the 1876 seed is mine."),
    rec("PLT-09", "plant", "Three of the rooted cuttings",
        variants_as_printed=["those \"authentic\" cuttings, which I have seen in the Waltrim clearing (S03 l.13)",
                             "the trees I have (raised from cuttings received from Mr. Howard) (S03 l.13)"],
        description_as_printed=[
            "Two of them are very shrubby in their growth, and with hard shiny leaves. The other is a Calisaya of the broad-leaved variety, very much like what I believe is called in Java *Calisaya Anglica*. (S03 l.13)",
            "are not Ledgerianas at all (S03 l.13)"],
        place_as_printed="the Waltrim clearing",
        source_ref=ref(("S03", "l.9, l.13")),
        quote="Three of the rooted cuttings were given to Mr. J. A. Campbell of Lindula, Ceylon, who was anxious to have a perfectly authentic strain.",
        inferred="The three Kew cuttings given to Campbell (Kew Report), the trees Christie saw in the Waltrim clearing, and the trees Campbell describes in his letter are treated as the same three plants; Christie's wording ('those \"authentic\" cuttings') supports but does not explicitly state the chain. That Waltrim is at or near Lindula is not stated."),
    rec("PLT-10", "plant", "another plant that Mr. Howard kindly gave me",
        description_as_printed=["which I understood him to say had been raised from Ledgeriana seed received from Java (S03 l.13)",
                                "This is the best, so far as appearance goes, but I should not call it a Ledgeriana. (S03 l.13)"],
        source_ref=ref(("S03", "l.13")),
        quote="I have also another plant that Mr. Howard kindly gave me which I understood him to say had been raised from Ledgeriana seed received from Java.",
        inferred="Spoken by Campbell in the letter quoted by Christie ('me' = Campbell)."),
    rec("PLT-11", "plant", "Three other plants, imported at Kew from the same authentic strain",
        description_as_printed=["were sent to Jamaica (S03 l.11)"],
        place_as_printed="Kew; Jamaica",
        source_ref=ref(("S03", "l.11")),
        quote="\"*Indonesia*.—Three other plants, imported at Kew from the same authentic strain were sent to Jamaica.\"",
        inferred="",
        reading_status="uncertain"),
    rec("PLT-12", "plant", "several Mr. Moens saw in flower at Mahanillu estate",
        variants_as_printed=["the trees (S04 l.11)", "some of the trees (S04 l.13)"],
        description_as_printed=[
            "both agreed the trees were true Ledgerianas (S04 l.11)",
            "The trees were only about 4½ years old from the time the plants were put out, and were now in a full condition and in flower. (S04 l.11)"],
        date_as_printed="about 4½ years old from the time the plants were put out",
        place_as_printed="Mahanillu estate",
        source_ref=ref(("S04", "l.11, l.13")),
        quote="The trees were only about 4½ years old from the time the plants were put out, and were now in a full condition and in flower.",
        inferred="This group includes PLT-01 ('It was one of several'). 'were now' presumably refers to the time of Moens' visit, which is not dated."),
    rec("PLT-13", "plant", "the other that Mr. Moens had sent to be true Ledgerianas",
        source_ref=ref(("S04", "l.13")),
        quote="I have by my prints of the leaves of some of the trees as well as the other that Mr. Moens had sent to be true Ledgerianas, so that it will be easy in the future to determine the question.",
        inferred="The sentence as printed/OCR'd does not parse ('the other that Mr. Moens had sent to be'); it may mean 'the others that Mr. Moens had said to be true Ledgerianas', i.e. further trees Moens identified, but I cannot tell from the text what plants are meant.",
        reading_status="failed"),
    rec("PLT-14", "plant", "other seed forwarded to him by Mr. Moens as true Ledgeriana",
        description_as_printed=["turned out to be nothing of the kind (S03 l.15)"],
        source_ref=ref(("S03", "l.15")),
        quote="he asserts that other seed forwarded to him by Mr. Moens as true Ledgeriana turned out to be nothing of the kind.",
        inferred="'him' = Mr. Howard (the subject of the sentence)."),
    rec("PLT-15", "plant", "several cinchonias in cultivation in Ceylon (and I suspect in Jamaica also) under the name of Ledgeriana, which are not that plant",
        place_as_printed="Ceylon; Jamaica",
        source_ref=ref(("S03", "l.13")),
        quote="That there are several cinchonias in cultivation in Ceylon (and I suspect in Jamaica also) under the name of Ledgeriana, which are not that plant, is to a great extent due to Mr. Howard himself.",
        inferred="A class of plants, not an individual tree. 'cinchonias' is kept as printed (possibly for 'cinchonas')."),
]

# --------------------------------------------------------------------------
# BARK SAMPLES and OTHER SPECIMENS
# --------------------------------------------------------------------------
SAMPLES = [
    rec("BRK-01", "bark_sample", "The bark of some of these trees",
        description_as_printed=["Ledgeriana bark, giving 7 per cent of pure quinine (equal I believe to 9 of sulphate) and only a trace of other alkaloids (S04 l.11)",
                                "after having analyzed the bark (S04 l.3)"],
        source_ref=ref(("S04", "l.3, l.11")),
        quote="The bark of some of these trees was sent home by Mr. Campbell for analysis to Mr. Howard, who pronounced it to be Ledgeriana bark, giving 7 per cent of pure quinine (equal I believe to 9 of sulphate) and only a trace of other alkaloids.",
        inferred="Taken from PLT-12 (the Mahanillu trees); whether the figured tree PLT-01 was among 'some of these trees' is not stated. The editor's 'the bark' (S04 l.3) is assumed to be this sample."),
    rec("BRK-02", "bark_sample", "the bark from the tree itself, but taken when it was dying",
        source_ref=ref(("S04", "l.15")),
        quote="I have also in my possession the bark from the tree itself, but taken when it was dying.",
        inferred="'the tree itself' = PLT-01. No analysis of this bark is mentioned."),
    rec("BRK-03", "bark_sample", "the analysis of that very tree arrived from England and showed 11.29 S.",
        source_ref=ref(("S03", "l.5")),
        quote="the analysis of that very tree arrived from England and showed 11.29 S.",
        inferred="RECORD IS INFERRED: the text mentions only an analysis that 'arrived from England'; that a bark sample of PLT-04 was sent to England for it is my inference. Analyst not named. '11.29 S.' read as per cent sulphate of quinine (see PLT-04).",
        reading_status="uncertain"),
    rec("BRK-04", "bark_sample", "have given over 12, 13 and 14 per cent sulphate of quinine",
        source_ref=ref(("S03", "l.5")),
        quote="have given over 12, 13 and 14 per cent sulphate of quinine;",
        inferred="RECORD IS INFERRED: yields are stated for PLT-02 but no sample, analyst, date or place is mentioned; a set of bark analyses is assumed to lie behind the figures.",
        reading_status="uncertain"),
    rec("SPC-01", "specimen", "my prints of the leaves of some of the trees",
        source_ref=ref(("S04", "l.13")),
        quote="I have by my prints of the leaves of some of the trees as well as the other that Mr. Moens had sent to be true Ledgerianas, so that it will be easy in the future to determine the question.",
        inferred="Leaf prints held by Agar, of some of PLT-12 and apparently of PLT-13 (sense of the sentence uncertain, see PLT-13). 'I have by my' is kept as printed (perhaps 'I have by me').",
        reading_status="uncertain"),
    rec("SPC-02", "specimen", "specimens",
        source_ref=ref(("S03", "l.5")),
        quote="Dr. Trimen selected a tree here for specimens, as being botanically a typical Ledger,",
        inferred="Botanical specimens from PLT-04; nature of the specimens not stated."),
]

# --------------------------------------------------------------------------
# ACTIONS / RELATIONSHIPS
# --------------------------------------------------------------------------
def act(record_id, label, action_type, subj, obj, src, quote, **kw):
    return rec(record_id, "action", label, action_type=action_type, subject_ids=subj, object_ids=obj,
               source_ref=src, quote=quote, **kw)


ACTIONS = [
    act("ACT-01", "The plant which Dr. Trimen figured", "figured", ["PER-01"], ["PLT-01"],
        ref(("S03", "l.5"), ("S04", "l.3, l.9")),
        "The plant which Dr. Trimen figured was one of those raised from McIvor's seed by me, and planted on Mahanilu by Mr. Agar, and its descent from Ledger's original seed is undoubted.",
        variants_as_printed=["The tree, which was sketched for Dr. Trimen's work (S04 l.9)", "Dr. Trimen's description and figure of *C. ledgeriana* (S03 l.5)",
                             "Dr. Trimen's illustration of the blossom (but not of the tree itself) is particularly good (S03 l.5)"],
        inferred="S03's 'figured' and S04's 'sketched for Dr. Trimen's work' are treated as one act. S04 does not say who made the sketch; 'Dr. Trimen's work' is not named."),
    act("ACT-02", "raised from McIvor's seed by me", "raised_from_seed", ["PER-02"], ["PLT-01"],
        ref(("S03", "l.5")),
        "The plant which Dr. Trimen figured was one of those raised from McIvor's seed by me,",
        inferred="'me' = the letter writer, Christie (PER-02). The same seed also produced PLT-02 and PLT-03 ('the same pinch of seed', 'the same nursery bed')."),
    act("ACT-03", "McIvor's seed", "supplied_seed", ["PER-06"], ["PLT-01", "PLT-02", "PLT-03"],
        ref(("S03", "l.5")),
        "raised from McIvor's seed by me,",
        inferred="How McIvor's seed reached Christie, and when, is not stated. Objects PLT-02 and PLT-03 are included because the text says they came from 'the same pinch of seed' / 'the same nursery bed'."),
    act("ACT-04", "its descent from Ledger's original seed is undoubted", "descended_from_seed_of", ["PLT-01"], ["PER-07"],
        ref(("S03", "l.5")),
        "its descent from Ledger's original seed is undoubted.",
        inferred="A pedigree claim by Christie, not a documented transfer."),
    act("ACT-05", "planted on Mahanilu by Mr. Agar", "planted", ["PER-04"], ["PLT-01"],
        ref(("S03", "l.5")),
        "and planted on Mahanilu by Mr. Agar,",
        place_as_printed="Mahanilu",
        inferred="Date of planting not stated; S04 says the trees were 'about 4½ years old from the time the plants were put out' at the time of Moens' undated visit."),
    act("ACT-06", "several Mr. Moens saw in flower at Mahanillu estate", "saw_in_flower", ["PER-05"], ["PLT-12"],
        ref(("S04", "l.11")),
        "It was one of several Mr. Moens saw in flower at Mahanillu estate, Dr. Trimen was with Mr. Moens, and both agreed the trees were true Ledgerianas.",
        place_as_printed="Mahanillu estate",
        inferred="Visit undated."),
    act("ACT-07", "Dr. Trimen was with Mr. Moens", "accompanied", ["PER-01"], ["PER-05"],
        ref(("S04", "l.11")),
        "Dr. Trimen was with Mr. Moens,",
        place_as_printed="Mahanillu estate"),
    act("ACT-08", "both agreed the trees were true Ledgerianas", "identified_as_true_ledgeriana", ["PER-05", "PER-01"], ["PLT-12"],
        ref(("S04", "l.11"), ("S03", "l.15")),
        "and both agreed the trees were true Ledgerianas.",
        variants_as_printed=["Moens' identification of Dr. Trimen's plant (S03 l.15)"],
        place_as_printed="Mahanillu estate"),
    act("ACT-09", "sent home by Mr. Campbell for analysis to Mr. Howard", "sent_for_analysis", ["PER-09"], ["BRK-01", "PER-03"],
        ref(("S04", "l.11")),
        "The bark of some of these trees was sent home by Mr. Campbell for analysis to Mr. Howard, who pronounced it to be Ledgeriana bark, giving 7 per cent of pure quinine (equal I believe to 9 of sulphate) and only a trace of other alkaloids.",
        inferred="'Sent home' is read as sent to England (S03 speaks of an analysis that 'arrived from England'), but S04 does not name the destination. 'Mr. Campbell' here is linked to 'Mr. J. A. Campbell of Lindula' (PER-09) of S03 by inference."),
    act("ACT-10", "pronounced it to be Ledgeriana bark", "analysed_and_pronounced", ["PER-03"], ["BRK-01"],
        ref(("S04", "l.11, l.3")),
        "who pronounced it to be Ledgeriana bark, giving 7 per cent of pure quinine (equal I believe to 9 of sulphate) and only a trace of other alkaloids.",
        variants_as_printed=["Mr. Howard himself having given testimony to that effect after having analyzed the bark (S04 l.3)"],
        description_as_printed=["7 per cent of pure quinine (equal I believe to 9 of sulphate) and only a trace of other alkaloids (S04 l.11)"],
        inferred="'equal I believe to 9 of sulphate' is Agar's own conversion, not Howard's."),
    act("ACT-11", "We publish below a letter from Mr. Agar", "published_with_note", ["PER-10"], ["PER-04"],
        ref(("S04", "l.3")),
        "[We publish below a letter from Mr. Agar, which places beyond question the fact that the tree figured by Dr. Trimen was an undoubted Ledgeriana, Mr. Howard himself having given testimony to that effect after having analyzed the bark.—Ed.]"),
    act("ACT-12", "the question raised by Mr. J. E. Howard", "raised_question_about", ["PER-03"], ["PER-01", "PLT-01"],
        ref(("S03", "l.5")),
        "Were the question raised by Mr. J. E. Howard purely technical it would be presumption on my part to say anything in reply to Dr. Trimen's description and figure of *C. ledgeriana*;",
        variants_as_printed=["Mr. Howard's latest paper (S03 l.5)", "Before the least doubt had been thrown upon his figured type (S03 l.5)"],
        description_as_printed=["The statement that the \"satin gloss and hairy margin of the leaves\" was put forward as a characteristic of true Ledgerianas is almost incredible. (S03 l.5)"],
        inferred="Howard's paper is not titled or dated in the text."),
    act("ACT-13", "the very trees which Mr. Howard called in to help him, the Yarrow Ledgers", "cited_as_evidence", ["PER-03"], ["PLT-03"],
        ref(("S03", "l.5")),
        "the very trees which Mr. Howard called in to help him, the Yarrow Ledgers, have the same blossom, and came out of the same nursery bed as the Ledger figured by Dr. Trimen!"),
    act("ACT-14", "Dr. Trimen selected a tree here for specimens", "selected_for_specimens", ["PER-01"], ["PLT-04", "SPC-02"],
        ref(("S03", "l.5")),
        "Dr. Trimen selected a tree here for specimens, as being botanically a typical Ledger,",
        place_as_printed="here",
        inferred="'here' read as St. Andrew's, Maskeliya. Undated, but 'Before the least doubt had been thrown upon his figured type'."),
    act("ACT-15", "the analysis of that very tree arrived from England", "analysis_received", [], ["PLT-04", "BRK-03", "PER-02"],
        ref(("S03", "l.5")),
        "on the following day, the analysis of that very tree arrived from England and showed 11.29 S.",
        description_as_printed=["showed 11.29 S. (S03 l.5)"],
        date_as_printed="on the following day",
        place_as_printed="England",
        inferred="Agent (the analyst) unstated. Recipient taken to be Christie, who reports it. 'the following day' is relative to Trimen's undated selection (ACT-14).",
        reading_status="uncertain"),
    act("ACT-16", "Mr. Howard goes on to identify by these characteristics Mr. T. Christy's Bolivian calisaya seedlings as true Ledgerianas", "identified_as_true_ledgeriana", ["PER-03"], ["PLT-05"],
        ref(("S03", "l.5")),
        "When Mr. Howard goes on to identify by these characteristics Mr. T. Christy's Bolivian calisaya seedlings as true Ledgerianas, his bases are as reliable as those by which a gipsy foretells your fortune.",
        inferred="'these characteristics' = the 'satin gloss and hairy margin of the leaves' quoted earlier in the paragraph."),
    act("ACT-17", "I have some of Mr. T. Christy's Bolivian plants, 18 months old, and I most certainly say they are not Ledgers", "holds_and_judges_not_ledgeriana", ["PER-02"], ["PLT-05"],
        ref(("S03", "l.5")),
        "I have some of Mr. T. Christy's Bolivian plants, 18 months old, and I most certainly say they are not Ledgers.",
        date_as_printed="18 months old"),
    act("ACT-18", "what I wrote 9 months ago, in the Dikoya essay", "wrote_essay", ["PER-02"], ["PLT-01", "PLT-07"],
        ref(("S03", "l.5")),
        "here I may quote what I wrote 9 months ago, in the Dikoya essay, long before I had any idea of this controversy arising:—\"Dr. Trimen's illustration of the blossom (but not of the tree itself) is particularly good, a contrast to that given in Howard's great work, where the figured plant is far from being a typical Ledgeriana, if indeed it is one at all.\"",
        date_as_printed="9 months ago",
        inferred="'9 months ago' relative to 7th June 1883 would be c. September 1882. The 'Dikoya essay' is not otherwise identified in the text."),
    act("ACT-19", "some seed was received at Kew from Java", "seed_received", [], ["PLT-08"],
        ref(("S03", "l.7")),
        "In 1876, some seed was received at Kew from Java,",
        date_as_printed="In 1876",
        place_as_printed="Kew; Java",
        inferred="Quoted by Christie from the Kew Gardens Report for 1880, p. 12. Sender not named (Christie elsewhere attributes 'the first seed received at Kew' to 'Mr. Moens' own authority', S03 l.15)."),
    act("ACT-20", "part of this was communicated to Mr. J. E. Howard, F. R. S., who raised seedlings", "raised_seedlings", ["PER-03"], ["PLT-08"],
        ref(("S03", "l.7")),
        "part of this was communicated to Mr. J. E. Howard, F. R. S., who raised seedlings. He carefully selected the most promising of these,",
        inferred="From the Kew Report quotation. Who communicated the seed (Kew) is implied, not named."),
    act("ACT-21", "very kindly supplied Kew with cuttings both of the figured and of another selected plant", "supplied_cuttings", ["PER-03"], ["PLT-07", "PLT-08"],
        ref(("S03", "l.9")),
        "and very kindly supplied Kew with cuttings both of the figured and of another selected plant in the course of last year.",
        date_as_printed="in the course of last year",
        place_as_printed="Kew",
        inferred="'last year' relative to a report for 1880 would be 1879. That 'the figured' plant is Howard's figured \"Ledgeriana\" (PLT-07) is my reading."),
    act("ACT-22", "Three of the rooted cuttings were given to Mr. J. A. Campbell of Lindula, Ceylon", "gave_cuttings", [], ["PLT-09", "PER-09"],
        ref(("S03", "l.9")),
        "Three of the rooted cuttings were given to Mr. J. A. Campbell of Lindula, Ceylon, who was anxious to have a perfectly authentic strain.",
        inferred="Giver not named (Kew implied by the report). Campbell's own letter says 'cuttings received from Mr. Howard' (S03 l.13), which may describe the same transfer differently."),
    act("ACT-23", "Three other plants, imported at Kew from the same authentic strain were sent to Jamaica", "sent_plants", [], ["PLT-11"],
        ref(("S03", "l.11")),
        "\"*Indonesia*.—Three other plants, imported at Kew from the same authentic strain were sent to Jamaica.\"",
        place_as_printed="Kew; Jamaica",
        inferred="",
        reading_status="uncertain"),
    act("ACT-24", "those \"authentic\" cuttings, which I have seen in the Waltrim clearing, are not Ledgerianas at all", "saw_and_judged_not_ledgeriana", ["PER-02"], ["PLT-09"],
        ref(("S03", "l.13")),
        "I say that those \"authentic\" cuttings, which I have seen in the Waltrim clearing, are not Ledgerianas at all.",
        place_as_printed="the Waltrim clearing"),
    act("ACT-25", "Mr. Campbell himself writes to me on 5th instant", "wrote_to", ["PER-09"], ["PER-02", "PLT-09", "PLT-10"],
        ref(("S03", "l.13")),
        "Mr. Campbell himself writes to me on 5th instant:—\"No one who knows a Ledgeriana tree of a pure type, according to Mr. Moens' idea of one, would think of calling the trees I have (raised from cuttings received from Mr. Howard) Ledgerianas.",
        date_as_printed="5th instant",
        inferred="'5th instant' read as 5 June 1883 (the letter is dated 7th June 1883). Campbell's letter is known only through Christie's quotation."),
    act("ACT-26", "another plant that Mr. Howard kindly gave me", "gave_plant", ["PER-03"], ["PLT-10", "PER-09"],
        ref(("S03", "l.13")),
        "I have also another plant that Mr. Howard kindly gave me which I understood him to say had been raised from Ledgeriana seed received from Java.",
        inferred="'me' = Campbell, inside the quoted letter."),
    act("ACT-27", "he repudiates Moens' identification of Dr. Trimen's plant", "repudiated_identification", ["PER-03"], ["PER-05", "PLT-01"],
        ref(("S03", "l.15")),
        "he repudiates Moens' identification of Dr. Trimen's plant,"),
    act("ACT-28", "He clings to \"Mr. Moens' own authority\" ... that the first seed received at Kew was genuine", "accepted_on_authority", ["PER-03"], ["PER-05", "PLT-08"],
        ref(("S03", "l.15")),
        "He clings to \"Mr. Moens' own authority\" only so far as he himself wishes to believe, viz., that the first seed received at Kew was genuine;"),
    act("ACT-29", "other seed forwarded to him by Mr. Moens as true Ledgeriana", "forwarded_seed", ["PER-05"], ["PLT-14", "PER-03"],
        ref(("S03", "l.15")),
        "he asserts that other seed forwarded to him by Mr. Moens as true Ledgeriana turned out to be nothing of the kind.",
        inferred="Reported by Christie as Howard's assertion; undated."),
    act("ACT-30", "he asserts that other seed ... turned out to be nothing of the kind", "asserted_not_ledgeriana", ["PER-03"], ["PLT-14"],
        ref(("S03", "l.15")),
        "turned out to be nothing of the kind."),
    act("ACT-31", "letter: St. Andrew's, Maskeliya, 7th June 1883 ... THOS. NORTH CHRISTIE", "wrote_letter", ["PER-02"], ["PER-10"],
        ref(("S03", "l.3, l.19")),
        "St. Andrew's, Maskeliya, 7th June 1883.",
        date_as_printed="7th June 1883",
        place_as_printed="St. Andrew's, Maskeliya",
        inferred="Addressee 'DEAR SIR' assumed to be the editor (PER-10); published on p. 37 of the July 1883 issue."),
    act("ACT-32", "letter: Lawrence, June 22nd, 1883 ... WALTER AGAR", "wrote_letter", ["PER-04"], ["PER-10"],
        ref(("S04", "l.5, l.17")),
        "Lawrence, June 22nd, 1883.",
        date_as_printed="June 22nd, 1883",
        place_as_printed="Lawrence",
        inferred="Addressee 'DEAR SIR' assumed to be the editor (PER-10); published on p. 66 of the July 1883 issue. Agar says he is adding to 'what Mr. Christie has written', i.e. responding to S03 (my reading)."),
    act("ACT-33", "I have by my prints of the leaves of some of the trees", "holds_specimen", ["PER-04"], ["SPC-01"],
        ref(("S04", "l.13")),
        "I have by my prints of the leaves of some of the trees as well as the other that Mr. Moens had sent to be true Ledgerianas, so that it will be easy in the future to determine the question.",
        reading_status="uncertain",
        inferred="See PLT-13 and SPC-01 for the garbled clause."),
    act("ACT-34", "I have also in my possession the bark from the tree itself", "holds_bark_sample", ["PER-04"], ["BRK-02"],
        ref(("S04", "l.15")),
        "I have also in my possession the bark from the tree itself, but taken when it was dying."),
    act("ACT-35", "that given in Howard's great work, where the figured plant", "figured", ["PER-03"], ["PLT-07"],
        ref(("S03", "l.5")),
        "a contrast to that given in Howard's great work, where the figured plant is far from being a typical Ledgeriana, if indeed it is one at all.",
        inferred="'Howard's great work' is not titled in the text."),
    act("ACT-36", "the misunderstanding which arose about the Annfield and Emelina Calisayas", "misunderstanding_arose", [], ["PLT-06", "PLT-07"],
        ref(("S03", "l.5")),
        "We all remember the misunderstanding which arose about the Annfield and Emelina Calisayas, some two years ago, due chiefly to the fact that most of these Calisayas seemed exactly similar to Mr. Howard's figured \"Ledgeriana\";",
        date_as_printed="some two years ago",
        inferred="No individual agent is named ('We all remember'); the cause is attributed to resemblance to Howard's figure. c. 1881 if counted from June 1883."),
    act("ACT-37", "Dr. Trimen, who has seen the Ceylon and Indian plantations, and many mature analyzed trees", "has_seen", ["PER-01"], [],
        ref(("S03", "l.17")),
        "Dr. Trimen, who has seen the Ceylon and Indian plantations, and many mature analyzed trees, knows and has figured *C. Ledgeriana*,",
        place_as_printed="Ceylon; Indian plantations",
        inferred="No object record: the plantations are not individual plants in this table."),
    act("ACT-38", "after having lived for years beside mature Ledgerianas", "lived_beside", ["PER-02"], ["PLT-02"],
        ref(("S03", "l.13")),
        "Now, if, after having lived for years beside mature Ledgerianas, which have given the highest analyses we have yet heard of, I may presume to think that I know a Ledgeriana when I see it,",
        inferred="Link to PLT-02 (the 12-14 per cent trees) is my inference; see PLT-02."),
    act("ACT-39", "The tree, which was sketched for Dr. Trimen's work, is dead", "died", ["PLT-01"], [],
        ref(("S04", "l.9, l.15")),
        "The tree, which was sketched for Dr. Trimen's work, is dead.",
        inferred="Dead by June 22nd, 1883 (letter date); when it died is not stated. BRK-02 was 'taken when it was dying'."),
    act("ACT-40", "which places beyond question the fact that the tree figured by Dr. Trimen was an undoubted Ledgeriana", "affirmed_true_ledgeriana", ["PER-10", "PER-04"], ["PLT-01"],
        ref(("S04", "l.3")),
        "which places beyond question the fact that the tree figured by Dr. Trimen was an undoubted Ledgeriana,",
        inferred="The affirmation is the editor's summary of Agar's letter; Agar himself says the figured tree was 'one of several' that Moens and Trimen 'agreed ... were true Ledgerianas'."),
]

RECORDS = PEOPLE + PLANTS + SAMPLES + ACTIONS


# --------------------------------------------------------------------------
# validation, output, report
# --------------------------------------------------------------------------
def load_sources(src_dir):
    texts = {}
    for key in ("S03", "S04"):
        path = os.path.join(src_dir, f"{key}_ocr.txt")
        if os.path.exists(path):
            with open(path, encoding="utf-8") as fh:
                texts[key] = fh.read()
    return texts


def strip_tag(phrase):
    """Remove the trailing '(S0x l.N ...)' location tag from a description/variant phrase."""
    return re.sub(r"\s*\((S0[34])\b[^)]*\)\s*$", "", phrase)


def phrase_sources(phrase):
    """Return the source keys named in a phrase's trailing tag, e.g. {'S03'}."""
    m = re.search(r"\(((?:S0[34])[^)]*)\)\s*$", phrase)
    return set(re.findall(r"S0[34]", m.group(1))) if m else set()


def validate(records, texts):
    problems = []
    ids = [r["record_id"] for r in records]
    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes:
        problems.append(f"duplicate record ids: {sorted(dupes)}")
    idset = set(ids)
    for r in records:
        for f in ("subject_ids", "object_ids"):
            for i in r[f]:
                if i not in idset:
                    problems.append(f"{r['record_id']}: {f} points to unknown id {i}")
        if r["reading_status"] not in ("ok", "uncertain", "failed"):
            problems.append(f"{r['record_id']}: bad reading_status {r['reading_status']!r}")
        if r["record_type"] == "action" and not r["action_type"]:
            problems.append(f"{r['record_id']}: action without action_type")
        if not texts:
            continue
        srcs = set(re.findall(r"S0[34]", r["source_ref"]))
        # quote must occur verbatim in at least one of the cited sources
        if r["quote"] and not any(r["quote"] in texts.get(s, "") for s in srcs):
            problems.append(f"{r['record_id']}: quote not found verbatim in {sorted(srcs)}")
        # tagged phrases: the untagged text must occur in the tagged source
        for f in ("variants_as_printed", "description_as_printed"):
            for phrase in r[f]:
                core = strip_tag(phrase)
                if " ... " in core:          # elided phrase, check the pieces
                    pieces = core.split(" ... ")
                else:
                    pieces = [core]
                tag_srcs = phrase_sources(phrase) or srcs
                for piece in pieces:
                    if not any(piece in texts.get(s, "") for s in tag_srcs):
                        problems.append(f"{r['record_id']}: {f} phrase not found verbatim in {sorted(tag_srcs)}: {piece!r}")
    return problems


def write_outputs(records, out_dir):
    json_path = os.path.join(out_dir, "02_records.json")
    csv_path = os.path.join(out_dir, "02_records.csv")
    with open(json_path, "w", encoding="utf-8") as fh:
        json.dump(records, fh, ensure_ascii=False, indent=2)
    with open(csv_path, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader()
        for r in records:
            row = {k: (" | ".join(v) if k in LIST_FIELDS else v) for k, v in r.items()}
            w.writerow(row)
    return json_path, csv_path


def report(records, texts):
    by_type = {}
    for r in records:
        by_type[r["record_type"]] = by_type.get(r["record_type"], 0) + 1
    print("Records by type:", ", ".join(f"{k}={v}" for k, v in by_type.items()), f"(total {len(records)})")
    print("Source files found:", ", ".join(sorted(texts)) or "none (verbatim check skipped)")
    for status in ("failed", "uncertain"):
        hits = [r["record_id"] for r in records if r["reading_status"] == status]
        print(f"{status}: {len(hits)} -> {', '.join(hits) if hits else '-'}")
    inf = [r["record_id"] for r in records if r["inferred"]]
    print(f"records with inferred content: {len(inf)}")
    out = [r["record_id"] for r in records if r["outside_identification"]]
    print(f"records with outside_identification (unverified, not from source): {len(out)} -> {', '.join(out)}")


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sources", default=os.path.dirname(here))
    ap.add_argument("--out", default=here)
    a = ap.parse_args()

    texts = load_sources(a.sources)
    problems = validate(RECORDS, texts)
    if problems:
        print("VALIDATION PROBLEMS:", file=sys.stderr)
        for p in problems:
            print("  -", p, file=sys.stderr)
        sys.exit(1)
    os.makedirs(a.out, exist_ok=True)
    jp, cp = write_outputs(RECORDS, a.out)
    print("wrote", jp)
    print("wrote", cp)
    report(RECORDS, texts)


if __name__ == "__main__":
    main()
