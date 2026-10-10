# Evidence layers

All offsets in `whole_source_alignment.tsv` and `primary107_vs_raw591.tsv` are zero-based, half-open intervals in the literal concatenation of `reading_order.tsv`'s `source_group`. Literal brackets count as positions: the full stream is 1271 positions. Removing only `[` and `]` gives 1265; this second coordinate system must never be silently mixed with the first.

|Layer|File|What it establishes|
|---|---|---|
|Guided source collation|data/reading_order.tsv|126 ten-letter layout groups with original-page and group coordinates, including uncertain literal notation; guided rather than blind transcription|
|Separate Roman audit|data/roman_independent_audit.tsv|Frozen best readings, alternatives and image coordinates; a separate reading of the same manuscript, not independent historical plaintext|
|Worksheet glyph audit|data/worksheet_kana_independent_audit.tsv|Kana, ticks, pencil glosses and image coordinates from the contemporary target-analysis sheets|
|Full stream ledger|data/whole_source_alignment.tsv|Every raw interval and its distinct worksheet, formula, pencil, codebook, native-reread and hypothesis columns|
|Independent printed opening|data/primary_1916_welcome_telegram.txt|Manual transcription of the 1916 print, excluding framing narration; punctuation removed for comparison|
|Diagnostic prefix alignment|data/primary107_vs_raw591.tsv|A fixed comparison, not authorization to emend raw letters|
|Pre-located signature spans|data/independent_primary_signature.tsv|Eight source spans located before the print was found, with all three Roman exceptions retained|

The source and worksheet layers must remain separate even when one resolves a reading in the other. The full ledger is a dated research snapshot, **not a continuous verified plaintext**. Earlier table fields such as `prior_selected_anchor` reference previously published worksheet selections. Modern glyph proposals and 1926 checked glyphs do not establish a complete 1916 codebook. Missing values and illegal kana slots remain missing/illegal.

The published three-kana construction uses the ordered FIRST/SECOND/THIRD alphabets in the script, with `200*FIRST.index(k1) + 10*THIRD.index(k3) + SECOND.index(k2) + 1`. Our internally bijective inverse uses `(n-1)//200`. Tomokiyo's printed Excel formula uses `INT(n/200)+1` for the first kana, which differs at exact multiples of 200. Boundary treatment is therefore an explicit computational convention; exhaustive round trips verify software, not authentic historical behavior at every boundary value.

Roman `e`/`ye` cannot by itself distinguish エ from ヱ. The parser supports observed period variants, excludes ambiguous standalone `n`, and never licenses arbitrary sound or semantic substitutions. Exact numeric re-encoding checks the formula relation; it cannot authenticate a proposed Chinese word.
