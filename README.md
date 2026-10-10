# Sun-circle cipher telegram, 1916: an unfinished source audit

**Status: stalled, partly identified, and open for independent checking.** This repository records a reproducible investigation of JACAR **B03050089100**, original cipher frames **0076–0078** (PDF pages 17–19), with contemporary analysts' worksheets **0079–0081** (pages 20–22). It is associated with the 20 May 1916 telegram in the Sun Yat-sen circle. It does not offer a completed plaintext or a newly recovered key.

The most solid result is an independent **1916 printed parallel for the opening 107 Chinese characters**, including the ten-person signature block: *護國軍紀事*, issue 5, “軍政府歡迎黃克強電”, 對內文告 p.14 (PDF p.26). This is identification of an already published plaintext and comparison with the intercepted copy, not first decipherment. Seven previously unsupported glyph occurrences are now supported by the print: 歡、躍、逾、恆、堯、碌、碌.

The later military passage remains unresolved. Pencil annotations are an analyst's guesses on the target itself; they are **not independent sender plaintext**. Contemporary codebook checks and a reply from Huang Xing provide constraints and thematic context, but no complete independent parallel has been confirmed for that passage.

“Sun” is a convenient corpus nickname. Association with Sun Yat-sen's circle does **not** establish Sun as this telegram's sender. The opening print has multiple signatories; the later six-slot signature interpretation has unresolved identities and assumptions.

## Reproduce the bounded checks

Python 3.10+ and its standard library suffice; no network, API key, model call or paid service is required.

```sh
python3 scripts/verify_package.py
python3 scripts/reproduce_primary.py
python3 scripts/reproduce_round3_retractions.py
```

These verify pinned files, literal-stream coverage, formula round trips, the 107-character diagnostic alignment, the preserved eight-signature-word comparison and its shuffled controls, and two retracted round3 claims. The first script checks published-file SHA256 hashes. The latter scripts write only to ignored `outputs/` or stdout. They do not overwrite input data.

Expected diagnostic results: 107 printed glyphs, 593 expected Roman letters versus 591 literal source positions, edit distance 63, 73 exactly aligned words; eight signature words give five exact Roman matches and six worksheet-code matches. These are **not accuracy percentages**, and the minimum-edit path does not certify historical copying errors. The prefix was exposed during calibration and is not an independent holdout for later correction rules.

## Read the evidence

- [Evidence layers and coordinate conventions](docs/EVIDENCE.md)
- [Chronology, failed paths, and retractions](docs/CHRONOLOGY.md)
- [Frozen hypotheses and remaining ambiguities](docs/HYPOTHESES.md)
- [Bounded round4 archive search and negative findings](docs/ROUND4.md)
- [Sources, attribution, rights and retrieval](docs/SOURCES.md)
- [Reproduction limits and excluded material](docs/REPRODUCTION.md)

The work used AI-assisted transcription, programming and adversarial audits (Codex and a separate Claude review). Model agreement is not independent historical evidence. Older claims are retained as dated provenance and corrected explicitly; the original local lab reports and data were not rewritten for this publication.

## Useful contributions

The most helpful new evidence would be a second independent copy of the later passage, or a separately established same-key telegram with known plaintext and confirmed signatory order. Please identify the archive reference, original page/frame, exact raw letters, all proposed changes, and the independence of the witness. A fluent reconstructed story or a semantic match alone will not close the remaining gaps.
