# One page, three readings

Walter Agar's letter, *The Tropical Agriculturist*, 2 July 1883, p. 66. Scan: archive.org `tropicalagricult18831884colo`, page n83 (right column, last three paragraphs).

The two sentences that differ. The scan was read by eye on 6 October 2026.

## Sentence 1

**Scan:** The trees were only about 4½ years old from the time the plants were put out, and were growing in a bad situation and not robust.

**Chandra 2 (Tropical corpus `output_v6`, 29 September 2026):** The trees were only about 4½ years old from the time the plants were put out, and were now in a full condition and in flower.

**archive.org text layer (`tropicalagricult18831884colo_djvu.txt`, retrieved 6 October 2026):** The trees were only about 4| years old I roui the lime the plants were put out, ami were growing; in a bad situation and not robust.

## Sentence 2

**Scan:** I have many plants from the seed of the specimen tree as well as the others that Mr. Moens declared to be true Ledgerianas, so that it will be easy in the future to determine the question.

**Chandra 2:** I have by my prints of the leaves of some of the trees as well as the other that Mr. Moens had sent to be true Ledgerianas, so that it will be easy in the future to determine the question.

**archive.org text layer:** I have many plants from the seed of the specimen^ tree as well as the oiheis that Mr. Moens declared to be true Ledgerianas, so that it will be easy in the future to determine the question.

## Chandra 2 again, on the page image

On 6 October 2026 the same page was re-OCR'd with Chandra 2 three times (`scripts/plato_chandra_page66.slurm`), feeding it the archive.org page image `n83.jpg` (1940 × 2865 px) one page at a time. All three runs read both sentences correctly:

> … and were growing in a bad situation and not robust.
> I have many plants from the seed of the specimen tree as well as the others that Mr. Moens declared to be true Ledgerianas …

Full output: `S04_chandra_rerun_2026-10-06.md`. The production corpus was built from the volume PDF in batches of 28 pages with 16 concurrent sequences. The wrong sentences belong to the page image that run saw (next section), not to the model's ability to read this page.

## Chandra 2 on the production PDF page

The production corpus was not OCR'd from the JPEG scans but from archive.org's volume PDFs. Those PDFs are MRC-compressed: page 84 of this volume is a 646 × 954 colour background, an 8 KB foreground layer, and a 1-bit JBIG2 text mask at 1940 × 2865. Rendering that page at 300 dpi and giving it to Chandra 2 (`S04_chandra_pdfrender_2026-10-06.md`) reproduced the failure with a different invented text:

> The trees were only about 4½ years old from the time the plants were put out, and were in a very abnormal situation at the time. I have no doubts from the sketch and the specimen trees as well as the other that Mr. Moens intended to be true Ledgerianas, so that it will be easy in the future to determine the question.

Same page, same model, same sentences, a third reading, and again fluent. Looking at the two images side by side (`images/p66-jpeg-detail.jpg`, `images/p66-pdf-render-detail.png`) shows why: in the PDF render the two lines are mostly gone. The JBIG2 mask kept the darker lines above and below and dropped most of the glyphs in these two, which are lightly inked on the scan. The model did not misread the lines; it wrote plausible prose across lines that were nearly blank, instead of reporting them as illegible. One page is one page, but the mechanism is identified: lossy PDF text masks drop faint lines, and a vision-language OCR model fills the gap with language.

## What this shows

- The older OCR is noisier character by character ("Triincu" for Trimen, "Moena", "Campliell", "w:is .si nt home") and its errors are visible as errors.
- The vision-language OCR is cleaner almost everywhere on the page and, in two places, wrote fluent sentences with a different meaning. Nothing in its text signals the error. Two extraction models read the first sentence as plausible and only flagged the second as garbled.
- The two OCRs disagree exactly where the newer one is wrong. A cheap sentence-level comparison between them would have flagged both places for a human, without re-OCR.
- Chandra 2 was tested on this corpus and performs well overall, and it reads this page correctly when given the page image on its own. The lesson is not that it should not be used. It is that OCR output depends on the page image as well as the model, that a fluent wrong sentence can come out of a good model on a page a person reads easily, and that the page has to stay one click away. For this corpus the practical question is whether to OCR from the JPEG scans rather than the compressed PDFs; a sample of pages compared both ways would answer it.
