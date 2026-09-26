# Source Desk: original text, selected evidence and provenance

**8BALL 0.2.0-alpha.3. Local developer capability, not V0.3 or a production evidence vault.**

## Operator workflow

Open a case, select **Evidence & claims**, then **Source Desk**. Import a UTF-8 `.txt` or `.md` file, or paste text. Review the content hash, length and any duplicate candidates before explicitly storing the original. Select a displayed passage or highlight an exact range, collect up to 12,000 characters, preview the selected text, and commit it as **unreviewed evidence**. Source review and condition attestation remain separate steps in the existing evidence workflow.

The original is retained in full. Reading, searching, selecting, previewing and exporting do not change case facts, start inference or use a provider credential. The imported document is not an authorised model input merely because it exists. Only explicitly captured excerpts can subsequently be selected in the existing analysis flow. The model-context allowance stays unchanged; this is not a hidden larger-model prompt.

## Limits and representations

One original can contain up to **200,000 Unicode code points / 800,000 UTF-8 bytes**. A case is capped at **50 originals and 8,000,000 source bytes**, including retracted originals. A capture batch contains 1 to 12 non-overlapping passages, together no more than 12,000 characters. Evidence still uses the existing 12,000-character wire contract and 200-record case limit.

Text is preserved exactly as received. File decoding is strict UTF-8 and retains a leading byte-order mark, CRLF/lone-CR line endings, combining characters and emoji. Pasted text is the value supplied by the browser, not a claim of byte identity with an unseen original application or PDF. Binary files, PDF/DOCX parsing and OCR are not implemented. A filename is descriptive metadata, never a filesystem destination.

The reader's textarea normalises displayed line endings and uses UTF-16 selection indices. `source-model.js` maps those boundaries back to original Unicode code-point offsets and rejects a split surrogate pair. Offsets are zero-based, end-exclusive. A source passage is verified on the server using its original range and SHA-256. Captured evidence has a separate immutable parent link, including original hash, passage hash and range. An extracted quotation can be mapped through that link to the full original using `resolve-span`.

Chunk suggestions partition the text without dropping characters. They prefer line boundaries, do not split CRLF pairs and expose complete ranges. Literal search reads the whole original, not only the visible page. It reports when only the first 50 matches are returned. The reader labels partial views. Full-text export reconstructs the complete original, not the visible window. Neither search nor chunking is semantic understanding.

## Duplicate and version handling

Before import, compare SHA-256 for exact text. A second candidate hash normalises Unicode composition and whitespace for discovery only. Its matches are labelled candidates, not proven document identity, independent corroboration or the same person. No normalised text replaces the original.

A match blocks the default import. The operator may keep the existing original or explicitly record a separate source with a provenance reason. Both sources remain separate. A linked earlier version remains intact and active until separately retracted; linking versions does not overwrite text, supersede observations or establish that one account is true.

Capturing the same exact range from the same original twice is rejected. Equal text from different originals retains separate source links. Captured-character counts use the union of ranges so overlap does not inflate the displayed coverage. Coverage means captured as evidence, not read by a reviewer, analysed by a model or verified as fact. Person/entity merging, pronoun resolution, semantic deduplication and automatic deadline interpretation remain unfinished work.

## Persistence, revisions and audit

Originals and passage links are separate case-owned tables: `v2_source_documents` and `v2_source_passages`. Original text is not copied into every planning snapshot. Import, capture and retraction still create revision-checked, idempotent case events, invalidate old approvals and make queued old-revision analysis stale. Event payloads anchor immutable descriptors and content hashes. Passage links and evidence creation commit atomically.

Source-aware case exports include full originals, exact passage links and integrity results. Hashes and ranges are checked against the import/capture anchors in the case event chain. Missing originals, changed source metadata, removed links, mismatched text and altered retraction status fail those checks. Existing cases without Source Desk records preserve the exact old export format and historical audit hashes; their source origin is labelled unknown rather than fabricated.

Retracting an original is an explicit operation with a reason. In one transaction it retracts every linked evidence excerpt, invalidates approvals and recalculates the case. Observations, source bytes and history remain. A closed case reopens when that evidence no longer supports its mandatory outcome. No source or evidence is silently reinstated.

This is a local application-level chain, not independent notarisation, administrator-proof storage, immutable cloud retention or certified forensic custody. Real client use still requires the separate production security gate.

## API surface

All endpoints are authenticated and case-scoped under `/api/v2/cases/{case_id}/sources`:

- `GET /`: source inventory and passage links, without full text.
- `POST /preview` and `POST /import`: read-only import review, then explicit storage.
- `GET /{document_id}` and `GET /{document_id}/search`: bounded text pages and literal search.
- `POST /{document_id}/selection`: exact selected range and content hash, without writes.
- `POST /passages/preview` and `POST /passages`: read-only batch review, then atomic evidence capture.
- `GET /origin/{evidence_id}` and `POST /resolve-span`: exact original provenance.
- `POST /{document_id}/retract`: audited retraction of an original and its evidence.

Only import/preview routes receive the larger 1,300,000-byte JSON-body allowance. Other routes retain their existing limit. The ASGI boundary checks bytes actually received, not just a declared Content-Length. There are no automatic paid retries or implicit provider requests in Source Desk.

## Verification and next work

Run `tests/test_source_desk.py`, `tests/test_source_api.py`, all existing tests, and `tests/browser_sources.py` alongside the earlier browser suites. The source-map helper tests include CRLF, combining marks, emoji, surrogate boundaries, overlapping selections and a bounded batch. The browser journey uses the actual application and SQLite, not an invented source screen. Bridge/native results must be labelled separately.

Continue B02-14 with reviewer-safe entity/claim reconciliation and independent mixed-document tests. Continue B02-10 with ambiguity-preserving dates, explicit timezone review and source-grounded identity proposals. No requirement is removed to mark the source milestone complete.

## Native response-order correction, 26 September 2026

Typing updates a case/document-scoped query draft immediately. Refreshing the same original preserves that text and keyboard selection. New queries invalidate old results; navigation/closure invalidate in-flight results from the prior view. A late reopen cannot select a document over a newer deliberate choice. These are local UI reads only, never evidence, approvals or model requests. Run `tests/test_source_view_races.py` and `tests/browser_sources.py` with all cumulative native suites. The browser adds a controlled delay and then forwards the real index request unchanged; original search/export/lineage assertions remain.
