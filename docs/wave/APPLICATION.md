# Stellar Wave application

Updated 9 November 2026 for the [Stellar Wave program](https://www.drips.network/wave/stellar). This replaces the 9 October draft, which predated the public release.

## Project description

**soroindex** ([Soroban-CII/soroindex](https://github.com/Soroban-CII/soroindex)) is a public index of Soroban smart contracts. It records the SEPs each contract declares, the interfaces it matches, and how both change across upgrades. SEP-47 metadata can be read one contract at a time. The index answers network-wide questions: which contracts declare SEP-41, which actually match its typed interface, and how those facts change across observed upgrades, including CAP-85 executable references.

The dated 7 October 2026 census covered 156,173 mainnet contracts. 13 of 2,178 live Wasm hashes (0.60%) declared any SEP. 120 hashes (1,141 contracts) matched SEP-41, and 109 matching hashes declared nothing.

Go parsers inspect Wasm without executing it, SQLite stores versioned claims, and a read-only HTTP API and CLI expose the results. Declarations and interface matches carry separate trust tiers. A verified tier is reserved for future testnet conformance work and is not a security audit.

## Built and planned

**Built and tested on `main`:**
- bounded SEP-47 metadata and spec parsing (four fuzz targets);
- versioned SEP-41 interface matching;
- the Phase 0 census and report;
- idempotent seeding;
- incremental ledger sync, including Protocol 30 ledgers, with retention-gap detection;
- CAP-85 reference fan-out, archival handling and history;
- a read-only API with pagination and rate limits;
- the CLI: `query` (including CSV export), `gap`, `contract`, `wasm` (naming missing and mismatched functions), `stats` (with an optional `--lag` sync check), `serve` and `sync`;
- a non-root static Docker image, measured at 27,772,533 bytes;
- a tag-triggered release workflow that drafts releases and pushes a GHCR image.

**Published:**
- the [v0.1.0 release](https://github.com/Soroban-CII/soroindex/releases/tag/v0.1.0) on 9 November 2026: four static archives with `SHA256SUMS` and `BUILD.json`, built from `3abe5a3`;
- the [documentation site](https://soroban-cii.github.io/soroindex/), on GitHub Pages.

**Not claimed:**
- No container image is published yet. The release workflow can push one on request.
- No hosted API.
- No demo video yet.
- The verified tier is deferred, because measured declaration adoption is below the 1% gate in CLAUDE.md.
- The deployed-fixture upgrade check was waived by the operator. Offline tests cover upgrades.

## Links checklist

| Item | Link | Status on 9 November 2026 |
| --- | --- | --- |
| Repository | [Soroban-CII/soroindex](https://github.com/Soroban-CII/soroindex) | Public. CI (`lint`, `test`, `fuzz-smoke`, `build`), security and docs workflows green on `main`. |
| Docs | [soroban-cii.github.io/soroindex](https://soroban-cii.github.io/soroindex/) | Deployed by the `docs` workflow. |
| Release | [v0.1.0](https://github.com/Soroban-CII/soroindex/releases/tag/v0.1.0) | Published. Asset digests match the local build. |
| Adoption report | [report/ADOPTION.md](https://github.com/Soroban-CII/soroindex/blob/main/report/ADOPTION.md) | Census of 7 October 2026. |
| Issues | [Stellar Wave issues](https://github.com/Soroban-CII/soroindex/issues?q=is%3Aopen+label%3A%22Stellar+Wave%22) | 145 open issues worth 25,000 points. 21 issues were closed between 8 and 9 November 2026, each with evidence. |
| Docker image | `ghcr.io/soroban-cii/soroindex:v0.1.0` | Not yet published. Actions → release → Run workflow with `v0.1.0`, then make the package public. |
| Demo video | none yet | The operator records [the demo](DEMO.md). |
| Live API | none | Hosting is optional and absent. |

## Planned issues

Generated from [`scripts/wave-issues.json`](https://github.com/Soroban-CII/soroindex/blob/main/scripts/wave-issues.json), the list `scripts/create-issues.sh` validates. All 145 issues are open on GitHub with the `Stellar Wave` label, a `complexity:*` label that sets their points, and an `area:*` label. They total **25,000 points**: 95 high × 200, 20 medium × 150 and 30 trivial × 100. Each body has a description, why it matters, checkbox acceptance criteria, implementation guidance with file pointers, and its complexity and points.

| Area | Issues | Trivial / medium / high | Points |
| --- | ---: | --- | ---: |
| api | 19 | 0 / 4 / 15 | 3,600 |
| cli | 15 | 6 / 0 / 9 | 2,400 |
| docs | 21 | 13 / 6 / 2 | 2,600 |
| parser | 18 | 5 / 2 / 11 | 3,000 |
| reports | 9 | 0 / 0 / 9 | 1,800 |
| rules | 12 | 1 / 1 / 10 | 2,250 |
| security | 6 | 0 / 0 / 6 | 1,200 |
| store | 10 | 0 / 0 / 10 | 2,000 |
| sync | 17 | 0 / 2 / 15 | 3,300 |
| tooling | 18 | 5 / 5 / 8 | 2,850 |

### api

- [#15](https://github.com/Soroban-CII/soroindex/issues/15) docs(api): publish validated OpenAPI 3.1 specification — high, 200 points
- [#40](https://github.com/Soroban-CII/soroindex/issues/40) feat(api): propose declared and inferred disagreement filters — high, 200 points
- [#41](https://github.com/Soroban-CII/soroindex/issues/41) feat(api): propose historical ledger query filters — high, 200 points
- [#42](https://github.com/Soroban-CII/soroindex/issues/42) test(api): exercise concurrent WAL readers during sync — medium, 150 points
- [#101](https://github.com/Soroban-CII/soroindex/issues/101) feat(api): serve several networks from one process — high, 200 points
- [#104](https://github.com/Soroban-CII/soroindex/issues/104) feat(api): ETag and If-None-Match on every GET endpoint — high, 200 points
- [#105](https://github.com/Soroban-CII/soroindex/issues/105) feat(api): request IDs, access logs and a Prometheus-text /metrics endpoint — high, 200 points
- [#106](https://github.com/Soroban-CII/soroindex/issues/106) test(api): fuzz every query-parameter parser — high, 200 points
- [#107](https://github.com/Soroban-CII/soroindex/issues/107) feat(api): versioned, tamper-evident cursors with stable ordering during sync — high, 200 points
- [#108](https://github.com/Soroban-CII/soroindex/issues/108) feat(api): archived and executable-reference filters for /v1/contracts — high, 200 points
- [#109](https://github.com/Soroban-CII/soroindex/issues/109) feat(api): Server-Sent Events stream of contract upgrades — high, 200 points
- [#111](https://github.com/Soroban-CII/soroindex/issues/111) feat(pkg): typed Go client for the /v1 API — high, 200 points
- [#112](https://github.com/Soroban-CII/soroindex/issues/112) test(api): golden response snapshots for every endpoint — high, 200 points
- [#113](https://github.com/Soroban-CII/soroindex/issues/113) feat(api): toolchain statistics endpoint — high, 200 points
- [#114](https://github.com/Soroban-CII/soroindex/issues/114) feat(api): bulk contract lookup — high, 200 points
- [#144](https://github.com/Soroban-CII/soroindex/issues/144) test(e2e): offline end-to-end test of sync, serve and every endpoint — high, 200 points
- [#148](https://github.com/Soroban-CII/soroindex/issues/148) feat(api): configurable CORS allowed origins — medium, 150 points
- [#150](https://github.com/Soroban-CII/soroindex/issues/150) feat(api): gzip response compression — medium, 150 points
- [#151](https://github.com/Soroban-CII/soroindex/issues/151) feat(api): rate-limit response headers — medium, 150 points

### cli

- [#17](https://github.com/Soroban-CII/soroindex/issues/17) feat(cli): decide and implement query exit codes for empty results — trivial, 100 points
- [#43](https://github.com/Soroban-CII/soroindex/issues/43) feat(cli): show interface evidence in contract output — trivial, 100 points
- [#115](https://github.com/Soroban-CII/soroindex/issues/115) feat(cli): inspect a local Wasm file without a database — high, 200 points
- [#116](https://github.com/Soroban-CII/soroindex/issues/116) feat(cli): doctor command for index and environment checks — high, 200 points
- [#117](https://github.com/Soroban-CII/soroindex/issues/117) feat(cli): export the index as a CSV bundle with a manifest — high, 200 points
- [#118](https://github.com/Soroban-CII/soroindex/issues/118) feat(cli): diff two Wasm hashes — high, 200 points
- [#119](https://github.com/Soroban-CII/soroindex/issues/119) feat(cli): configuration file support for every command — high, 200 points
- [#120](https://github.com/Soroban-CII/soroindex/issues/120) feat(cli): a GitHub Action that checks a contract's declared SEPs — high, 200 points
- [#121](https://github.com/Soroban-CII/soroindex/issues/121) feat(cli): machine-readable errors and a documented error catalog — high, 200 points
- [#122](https://github.com/Soroban-CII/soroindex/issues/122) feat(cli): outreach report for undeclared interfaces — high, 200 points
- [#123](https://github.com/Soroban-CII/soroindex/issues/123) feat(cli): validate a seed file against the RPC before syncing — high, 200 points
- [#155](https://github.com/Soroban-CII/soroindex/issues/155) feat(cli): version --json — trivial, 100 points
- [#159](https://github.com/Soroban-CII/soroindex/issues/159) test(config): every flag overrides its environment variable — trivial, 100 points
- [#164](https://github.com/Soroban-CII/soroindex/issues/164) feat(cli): --version flag as an alias for version — trivial, 100 points
- [#176](https://github.com/Soroban-CII/soroindex/issues/176) test(cli): every command accepts -h — trivial, 100 points

### docs

- [#30](https://github.com/Soroban-CII/soroindex/issues/30) docs(phase0): chart declared versus inferred adoption — medium, 150 points
- [#31](https://github.com/Soroban-CII/soroindex/issues/31) feat(phase0): retain dated adoption snapshots and trends — medium, 150 points
- [#47](https://github.com/Soroban-CII/soroindex/issues/47) docs(api): add a typed Python client example — trivial, 100 points
- [#48](https://github.com/Soroban-CII/soroindex/issues/48) docs(api): add a browser client with pagination and tier labels — medium, 150 points
- [#142](https://github.com/Soroban-CII/soroindex/issues/142) docs: end-to-end tutorial "find every SEP-41 token" — high, 200 points
- [#143](https://github.com/Soroban-CII/soroindex/issues/143) docs: troubleshooting guide for every error — high, 200 points
- [#146](https://github.com/Soroban-CII/soroindex/issues/146) docs: architecture page with diagrams — medium, 150 points
- [#149](https://github.com/Soroban-CII/soroindex/issues/149) docs(api): /v1 compatibility and deprecation policy — medium, 150 points
- [#152](https://github.com/Soroban-CII/soroindex/issues/152) docs(self-hosting): systemd units for sync and serve — medium, 150 points
- [#153](https://github.com/Soroban-CII/soroindex/issues/153) docs(changelog): add Unreleased entries for post-release features — trivial, 100 points
- [#154](https://github.com/Soroban-CII/soroindex/issues/154) docs(repo): move internal stage reports to docs/archive — trivial, 100 points
- [#157](https://github.com/Soroban-CII/soroindex/issues/157) chore(repo): add CITATION.cff — trivial, 100 points
- [#163](https://github.com/Soroban-CII/soroindex/issues/163) docs(api): error code table — trivial, 100 points
- [#165](https://github.com/Soroban-CII/soroindex/issues/165) docs: FAQ page — trivial, 100 points
- [#169](https://github.com/Soroban-CII/soroindex/issues/169) docs(contributing): document the release workflow for maintainers — trivial, 100 points
- [#170](https://github.com/Soroban-CII/soroindex/issues/170) docs(cli): capture a real stats --lag run — trivial, 100 points
- [#171](https://github.com/Soroban-CII/soroindex/issues/171) docs(mkdocs): add the changelog to the docs site — trivial, 100 points
- [#172](https://github.com/Soroban-CII/soroindex/issues/172) docs(api): capture real error responses — trivial, 100 points
- [#175](https://github.com/Soroban-CII/soroindex/issues/175) docs(contract-authors): multi-crate projects — trivial, 100 points
- [#177](https://github.com/Soroban-CII/soroindex/issues/177) docs(api): document cursor lifetime — trivial, 100 points
- [#178](https://github.com/Soroban-CII/soroindex/issues/178) docs(trust-tiers): worked example of the undeclared gap — trivial, 100 points

### parser

- [#23](https://github.com/Soroban-CII/soroindex/issues/23) test(sepmeta): add Unicode whitespace boundary vectors — trivial, 100 points
- [#24](https://github.com/Soroban-CII/soroindex/issues/24) test(sepmeta): seed fuzzing with real mainnet custom sections — medium, 150 points
- [#39](https://github.com/Soroban-CII/soroindex/issues/39) test(sepmeta): add nested UDT and union spec vectors — medium, 150 points
- [#59](https://github.com/Soroban-CII/soroindex/issues/59) feat(sepmeta): decode contract event specs and expose Events() — high, 200 points
- [#60](https://github.com/Soroban-CII/soroindex/issues/60) feat(sepmeta): resolve user-defined types into a type table — high, 200 points
- [#61](https://github.com/Soroban-CII/soroindex/issues/61) feat(sepmeta): decode contractenvmetav0 and record each Wasm's interface version — high, 200 points
- [#62](https://github.com/Soroban-CII/soroindex/issues/62) feat(sepmeta): read custom sections from an io.ReaderAt with bounded memory — high, 200 points
- [#63](https://github.com/Soroban-CII/soroindex/issues/63) test(sepmeta): cross-implementation conformance suite against stellar-cli and py-stellar-sdk — high, 200 points
- [#64](https://github.com/Soroban-CII/soroindex/issues/64) test(sepmeta): structure-aware fuzzing for SCMetaEntry and ScSpecEntry streams — high, 200 points
- [#65](https://github.com/Soroban-CII/soroindex/issues/65) perf(sepmeta): benchmark suite with allocation budgets enforced in CI — high, 200 points
- [#66](https://github.com/Soroban-CII/soroindex/issues/66) test(fixtures): add a SEP-40 oracle consumer fixture contract — high, 200 points
- [#67](https://github.com/Soroban-CII/soroindex/issues/67) test(fixtures): add a SEP-50 non-fungible token fixture contract — high, 200 points
- [#68](https://github.com/Soroban-CII/soroindex/issues/68) test(fixtures): add a SEP-56 tokenized vault fixture contract — high, 200 points
- [#69](https://github.com/Soroban-CII/soroindex/issues/69) test(fixtures): add negative token fixtures for matcher edge cases — high, 200 points
- [#160](https://github.com/Soroban-CII/soroindex/issues/160) test(sepmeta): runnable example for Functions — trivial, 100 points
- [#161](https://github.com/Soroban-CII/soroindex/issues/161) test(sepmeta): runnable example for handling ErrLimit — trivial, 100 points
- [#166](https://github.com/Soroban-CII/soroindex/issues/166) test(sepmeta): vectors for ASCII control whitespace around tokens — trivial, 100 points
- [#167](https://github.com/Soroban-CII/soroindex/issues/167) test(sepmeta): vectors for the six-digit boundary — trivial, 100 points

### reports

- [#124](https://github.com/Soroban-CII/soroindex/issues/124) feat(phase0): toolchain census and declaration rate by SDK version — high, 200 points
- [#125](https://github.com/Soroban-CII/soroindex/issues/125) feat(phase0): factory deployment analysis — high, 200 points
- [#126](https://github.com/Soroban-CII/soroindex/issues/126) feat(phase0): declared-versus-inferred disagreement section — high, 200 points
- [#127](https://github.com/Soroban-CII/soroindex/issues/127) feat(phase0): automate the Hubble census with a cost guard — high, 200 points
- [#128](https://github.com/Soroban-CII/soroindex/issues/128) feat(phase0): full testnet census across the retention window — high, 200 points
- [#129](https://github.com/Soroban-CII/soroindex/issues/129) feat(docs): static adoption page generated from an index — high, 200 points
- [#130](https://github.com/Soroban-CII/soroindex/issues/130) feat(phase0): Wasm age cohorts — high, 200 points
- [#131](https://github.com/Soroban-CII/soroindex/issues/131) feat(phase0): CAP-85 executable-reference report — high, 200 points
- [#132](https://github.com/Soroban-CII/soroindex/issues/132) ci(phase0): monthly adoption report automation — high, 200 points

### rules

- [#20](https://github.com/Soroban-CII/soroindex/issues/20) feat(rules): add reviewed SEP-40 oracle consumer rules — high, 200 points
- [#21](https://github.com/Soroban-CII/soroindex/issues/21) feat(rules): add reviewed SEP-50 non-fungible tokens rules — high, 200 points
- [#22](https://github.com/Soroban-CII/soroindex/issues/22) feat(rules): add reviewed SEP-56 tokenized vaults rules — high, 200 points
- [#71](https://github.com/Soroban-CII/soroindex/issues/71) feat(rules): match event specs in rule files, starting with SEP-41 — high, 200 points
- [#72](https://github.com/Soroban-CII/soroindex/issues/72) feat(match): structural matching for user-defined types — high, 200 points
- [#73](https://github.com/Soroban-CII/soroindex/issues/73) feat(match): composite rules — a SEP-56 vault requires a SEP-41 share interface — high, 200 points
- [#74](https://github.com/Soroban-CII/soroindex/issues/74) test(match): property and fuzz tests for the matcher — high, 200 points
- [#75](https://github.com/Soroban-CII/soroindex/issues/75) feat(rules): draft a rule file from a SEP's Rust trait definition — high, 200 points
- [#77](https://github.com/Soroban-CII/soroindex/issues/77) feat(match): report extra functions and interface coverage per Wasm — high, 200 points
- [#78](https://github.com/Soroban-CII/soroindex/issues/78) feat(rules): keep historical SEP-41 rulesets and report which version a Wasm matches — high, 200 points
- [#145](https://github.com/Soroban-CII/soroindex/issues/145) docs(rules): calibrate the partial threshold from census data — medium, 150 points
- [#162](https://github.com/Soroban-CII/soroindex/issues/162) test(match): runnable example for Match — trivial, 100 points

### security

- [#82](https://github.com/Soroban-CII/soroindex/issues/82) feat(ingest): verify fetched code against its ledger key hash — high, 200 points
- [#95](https://github.com/Soroban-CII/soroindex/issues/95) feat(rpc): authenticated RPC providers without logging secrets — high, 200 points
- [#110](https://github.com/Soroban-CII/soroindex/issues/110) feat(api): HTTP server hardening with timeouts, header limits and slow-client tests — high, 200 points
- [#139](https://github.com/Soroban-CII/soroindex/issues/139) feat(security): configurable Wasm and XDR limits with validated bounds — high, 200 points
- [#140](https://github.com/Soroban-CII/soroindex/issues/140) test(security): bound RPC response sizes and JSON decoding — high, 200 points
- [#141](https://github.com/Soroban-CII/soroindex/issues/141) docs(security): threat model — high, 200 points

### store

- [#76](https://github.com/Soroban-CII/soroindex/issues/76) feat(store): record each rule file's SHA-256 with every interface match — high, 200 points
- [#84](https://github.com/Soroban-CII/soroindex/issues/84) test(store): fault-injection harness that fails every write point — high, 200 points
- [#93](https://github.com/Soroban-CII/soroindex/issues/93) feat(store): track live_until_ledger and expose entries close to archival — high, 200 points
- [#96](https://github.com/Soroban-CII/soroindex/issues/96) feat(cli): migration status and dry run with checksums — high, 200 points
- [#97](https://github.com/Soroban-CII/soroindex/issues/97) test(store): upgrade-path harness across every historical migration — high, 200 points
- [#98](https://github.com/Soroban-CII/soroindex/issues/98) test(store): query-plan regression tests for every API query — high, 200 points
- [#99](https://github.com/Soroban-CII/soroindex/issues/99) perf(store): 10M-claim benchmark and materialization decision record — high, 200 points
- [#100](https://github.com/Soroban-CII/soroindex/issues/100) feat(cli): maintenance command for ANALYZE, vacuum and integrity checks — high, 200 points
- [#102](https://github.com/Soroban-CII/soroindex/issues/102) feat(store): data-quality checker against the RPC — high, 200 points
- [#103](https://github.com/Soroban-CII/soroindex/issues/103) feat(store): publish nightly read-only database snapshots — high, 200 points

### sync

- [#28](https://github.com/Soroban-CII/soroindex/issues/28) feat(ingest): implement data-lake BackfillSource — high, 200 points
- [#29](https://github.com/Soroban-CII/soroindex/issues/29) feat(rpc): fail over across network-verified providers — high, 200 points
- [#44](https://github.com/Soroban-CII/soroindex/issues/44) feat(store): add a consistent online backup command — medium, 150 points
- [#45](https://github.com/Soroban-CII/soroindex/issues/45) feat(sync): expose throughput and RPC retry metrics — medium, 150 points
- [#46](https://github.com/Soroban-CII/soroindex/issues/46) feat(ingest): stream large seed CSV inputs in bounded batches — high, 200 points
- [#79](https://github.com/Soroban-CII/soroindex/issues/79) feat(sync): detect a testnet reset and refuse to continue — high, 200 points
- [#80](https://github.com/Soroban-CII/soroindex/issues/80) feat(sync): record ledger protocol versions and fail clearly on unknown XDR — high, 200 points
- [#81](https://github.com/Soroban-CII/soroindex/issues/81) feat(ingest): fetch Wasm in parallel with a bounded worker pool and ordered commits — high, 200 points
- [#83](https://github.com/Soroban-CII/soroindex/issues/83) test(sync): property-based replay over random fact sequences — high, 200 points
- [#86](https://github.com/Soroban-CII/soroindex/issues/86) feat(config): futurenet network support — high, 200 points
- [#87](https://github.com/Soroban-CII/soroindex/issues/87) perf(sync): throughput benchmark on a recorded ledger corpus — high, 200 points
- [#88](https://github.com/Soroban-CII/soroindex/issues/88) test(ingest): record a corpus of real testnet ledgers covering every change type — high, 200 points
- [#89](https://github.com/Soroban-CII/soroindex/issues/89) test(ingest): fuzz change extraction over mutated LedgerCloseMeta — high, 200 points
- [#90](https://github.com/Soroban-CII/soroindex/issues/90) feat(ingest): retry queue for Wasm whose fetch failed — high, 200 points
- [#91](https://github.com/Soroban-CII/soroindex/issues/91) feat(sync): optional cross-provider ledger-hash verification — high, 200 points
- [#92](https://github.com/Soroban-CII/soroindex/issues/92) feat(sync): --stop-ledger for bounded, reproducible replays — high, 200 points
- [#94](https://github.com/Soroban-CII/soroindex/issues/94) feat(ingest): record transaction provenance for creations and upgrades — high, 200 points

### tooling

- [#49](https://github.com/Soroban-CII/soroindex/issues/49) ci(repo): produce release SBOM and signed provenance — medium, 150 points
- [#50](https://github.com/Soroban-CII/soroindex/issues/50) ci(repo): build and smoke-test arm64 container images — medium, 150 points
- [#51](https://github.com/Soroban-CII/soroindex/issues/51) ci(repo): test the declared Go language floor — medium, 150 points
- [#52](https://github.com/Soroban-CII/soroindex/issues/52) ci(repo): propose reviewed dependency patch automation — medium, 150 points
- [#70](https://github.com/Soroban-CII/soroindex/issues/70) ci(fixtures): verify golden Wasm reproduce from their Rust sources — high, 200 points
- [#85](https://github.com/Soroban-CII/soroindex/issues/85) ci(sync): nightly read-only mainnet follow job — high, 200 points
- [#133](https://github.com/Soroban-CII/soroindex/issues/133) ci(repo): verify tagged release builds are reproducible — high, 200 points
- [#134](https://github.com/Soroban-CII/soroindex/issues/134) ci(repo): nightly long fuzz runs with corpus caching — high, 200 points
- [#135](https://github.com/Soroban-CII/soroindex/issues/135) ci(repo): coverage reporting with per-package thresholds — high, 200 points
- [#136](https://github.com/Soroban-CII/soroindex/issues/136) ci(repo): OpenSSF Scorecard and fixes for its findings — high, 200 points
- [#137](https://github.com/Soroban-CII/soroindex/issues/137) feat(deploy): docker-compose stack for sync and serve — high, 200 points
- [#138](https://github.com/Soroban-CII/soroindex/issues/138) test(sync): 24-hour testnet soak run with lag and memory limits — high, 200 points
- [#147](https://github.com/Soroban-CII/soroindex/issues/147) ci(release): preflight GHCR permissions and document package setup — medium, 150 points
- [#156](https://github.com/Soroban-CII/soroindex/issues/156) build(make): add a make check target — trivial, 100 points
- [#158](https://github.com/Soroban-CII/soroindex/issues/158) chore(repo): add .editorconfig — trivial, 100 points
- [#168](https://github.com/Soroban-CII/soroindex/issues/168) build(make): add a make vuln target — trivial, 100 points
- [#173](https://github.com/Soroban-CII/soroindex/issues/173) chore(repo): add CODEOWNERS for rules and migrations — trivial, 100 points
- [#174](https://github.com/Soroban-CII/soroindex/issues/174) chore(repo): add .gitattributes for binary fixtures and generated reports — trivial, 100 points

## Operator checklist

Done on 9 November 2026:
- The Wave backlog was published: 145 issues (#15–#178 range) worth 25,000 points, created and re-styled on 16 November 2026.
- `main` is protected.
- Topics and the website are set.

Remaining:
1. Confirm private vulnerability reporting is enabled: https://github.com/Soroban-CII/soroindex/security/advisories/new should show a report form.
2. Publish the image: Actions → release → Run workflow with `v0.1.0`, then set the GHCR package to public.
3. Record the demo from [DEMO.md](DEMO.md) and add its public URL above.
4. Recheck the approved-repository list, then submit from the operator's account. The agent does not submit or operate that account.
