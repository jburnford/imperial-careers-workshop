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

## What this shows

- The older OCR is noisier character by character ("Triincu" for Trimen, "Moena", "Campliell", "w:is .si nt home") and its errors are visible as errors.
- The vision-language OCR is cleaner almost everywhere on the page and, in two places, wrote fluent sentences with a different meaning. Nothing in its text signals the error. Two extraction models read the first sentence as plausible and only flagged the second as garbled.
- The two OCRs disagree exactly where the newer one is wrong. A cheap sentence-level comparison between them would have flagged both places for a human, without re-OCR.
- Chandra 2 was tested on this corpus and performs well overall. The lesson is not that it should not be used. It is that OCR is better than it was and not perfect, and that the page has to stay one click away.
