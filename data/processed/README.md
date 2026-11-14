# Selected ready chunk bundles

Seven document folders contain 1183 ready chunks and their provenance/validation
records. `chunks_review.md` is the readable chunk view; `qdrant_payloads.jsonl`
is the minimal Cloud payload projection. `chunks.jsonl` and `parents.jsonl`
retain additional preparation metadata. Manifest hashes validate content.
Only relocatable `source_path` values were adapted during migration; chunk IDs,
body text, embedding text, source references and parent groups are preserved.
`hybrid_setup.json` records the already-completed Cloud BM25 setup verification.

Doc01 retains known PDF layout issues in diagrams/split columns, especially
pages 16–17 and 41. Structural validation does not prove perfect PDF extraction.
Sources and counts are listed in [the pipeline guide](../../docs/pipeline/README.md).
