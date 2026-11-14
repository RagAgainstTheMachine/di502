# Two feature branches

## 1. Document ingestion

Branch: `feature/document-ingestion` → PR base: `main`.

Contains `src/ingestion/`, shared helpers/configuration, dependency files,
reviewed Markdown, 1183 ready chunks, ingestion tests and index setup. Its tests
and dry-run validation work without the search module. It has one local commit.

## 2. Hybrid retrieval

Branch: `feature/hybrid-retrieval` → initial PR base: `feature/document-ingestion`.

Contains the first branch as its dependency, followed by one additional commit
for `src/retrieval/`, retrieval/integration tests and corresponding docs. Against
the first branch, its PR shows only retrieval additions, not the dataset again.
The default is E5 + BM25 on text + RRF; parent expansion is off.

Publish the two existing local commits when ready:

```bash
git push -u origin feature/document-ingestion
git push -u origin feature/hybrid-retrieval
```

Merge the ingestion PR first. Then update the retrieval PR base to `main`.
If the first PR was squash-merged or rebased, update the second branch's base
before retargeting so that its diff still contains only the retrieval commit.
Do not merge the second PR into the first branch if you want two separate
deliveries into main. A fresh remote fetch is needed to verify the current main.

The old combined feature branch was renamed to `feature/document-ingestion`.
`DI502-67` remains the architecture-document branch. No issue number is invented.
Two local commits were created to keep the snapshots separate; no push or PR
was made. Credentials remain ignored and Qdrant is unchanged.

After both PRs merge, future LLM work can branch from updated main as
`feature/grounded-answer-generation` and import `src.retrieval.search.search`.
