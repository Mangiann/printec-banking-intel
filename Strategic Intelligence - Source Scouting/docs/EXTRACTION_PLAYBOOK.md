# Getting the maximum data out of a source — the playbook

Guidance for any agent building or running a collection layer. Every method below is in production and every
number is measured on a real corpus (5 countries, ~12,000 documents, 561M characters). Written to be portable:
nothing here depends on our codebase.

**The governing idea: a source is a DIRECTION, not a document.** The URL in your registry is almost never the
thing you want. It is a press-release index, a circulars page, a tender portal. The intelligence is in what it
points at. Measured: before we followed links properly, **1,780 of 3,882 producing sources yielded exactly one
document** — the landing page and nothing else.

---

## 1. Prefer typed data over scraping — always

Before parsing any HTML, ask whether the publisher offers the same facts in machine-readable form.

- **Find the API door.** Registries are full of sources that are really APIs: `/api/`, `/rest/`, `.json`,
  `/opendata`, `/sparql`, `/datasets/`, swagger endpoints. Route by **host** to a connector.
- **Never route by the registry's own `collection_method` label.** Measured: 97.5% of 6,930 sources were
  labelled "unknown", and the one labelled "api" pointed at HTML documentation while the real API endpoint was
  labelled "unknown". The label is noise; the host is fact.
- **Match hosts exactly or by dot-suffix, never by substring.** `"diavgeia" in host` also matches
  `yperdiavgeia.gr`, `easydiavgeia.gr`, `diavgeia-ai.gr` — unrelated third-party sites.
- **Fire once per source-family per run**, not once per matching row, or you will hammer one institution
  dozens of times and earn a rate-limit at exactly the place that matters most.

**Verify every API parameter actually filters.** A filter that silently does nothing returns confident noise.
Measured: one portal's `q=` parameter is ignored — `q=POS` returned 3,135,832 of 3,135,907 records, and
`q=<gibberish>` returned all of them. The real parameter was `subject=`. **Test: query a nonsense term and
compare the total. If it matches the unfiltered total, the parameter is decoration.**

**Never use a code you have not read back from the API.** Measured: half of a hand-written CPV list was
fiction — one code meant "web page editing software", another "repair of clocks", and a third was a generic IT
code that matched 140 sterilisers and seismographs and reported them as a payments pipeline.

---

## 2. The fetch ladder — cheapest rung first, and stop at the honest limit

1. **Plain HTTP GET** with conditional headers (`ETag` / `If-Modified-Since`) — a 304 is a free "unchanged".
2. **Headless real browser** (Playwright driving the system Chrome) for JS-rendered pages and lightly-defended
   sites. Escalate here when the parse looks like a substantial JS shell, or when a challenge marker appears.
3. **A human list** for hard walls. **Do not fight CAPTCHAs or logins.** Automate a human's legitimate access
   to public data; do not impersonate a human to a system explicitly checking for one.

**Detect bot walls by positive evidence, at any page size.** Look for named markers — `sgcaptcha`,
`/cdn-cgi/challenge`, `__cf_chl`, `hcaptcha`, `recaptcha`, `_Incapsula_Resource`, `distil`, `px-captcha`.
Measured: a ministry answered **HTTP 202 with a 169-byte captcha redirect** and it was stored as a healthy
empty page while the run reported "needs_human: 0". A size threshold is right for *inferring* a wall from
emptiness, but a named marker is decisive at any size.

**Be a good citizen and it costs you nothing:** ~1 request/second per host, identify yourself in the
User-Agent, honour `robots.txt`, honour `Retry-After`. But **retry a robots.txt that fails transiently** —
measured, 116 sources were skipped for an entire month because their robots file would not load once, and we
never even asked the site for its content.

---

## 3. Follow the direction — six ways to get past the landing page

Apply all of them; they overlap little.

1. **Feeds (RSS/Atom).** The site's own dated list of what it published. Read the feed address the moment you
   discover it — not next run. Measured: 0 of 230 profiles had a stored feed address, so a "use the remembered
   one" design would have read **zero feeds** while looking fine. Fixed: 87 feeds, 12,436 items on first run.
2. **Sitemaps.** From `robots.txt`. Scope to the source's own path prefix and to entries dated newer than your
   last run — never crawl a whole domain.
3. **Open-data catalogues (DCAT).** Dispatch on *content*, not the URL: fetch once, then decide whether it is
   RSS or a catalogue.
4. **Judged link-following.** Show a model the page's links and let it pick the ones that lead to reports,
   filings, tenders, circulars, statistics — rejecting nav, careers, cookie banners, logins. Code decides what
   to do with the answer; the model only proposes.
5. **The second hop.** When a followed child turns out to be a *listing page*, take the **files** it links to.
   Measured: zero of 12,026 documents were two steps from a source, while the pages we already held pointed at
   **15,306 unfetched files**. **Files only, never another page** — that single restriction is what keeps this
   a bounded rule instead of a web crawler.
6. **Pagination.** Listings are lists. Detect the next page by `rel="next"` first (machine-readable), then a
   next-page word in the local languages, then by incrementing a page number in the URL. Measured: one
   competition-authority decisions page advertises **1,012 pages** and had yielded exactly one document.
   Contribute *links only* so the change-detection hash stays on page 1, and refuse to leave the host or the
   listing's own directory.

---

## 4. Get the content out of the file

- **Encoding ladder:** HTTP charset → `<meta>` → BOM → UTF-8 → local codepage (e.g. cp1253) → latin-1. Flag
  `mojibake_suspected` and report it. Silent mojibake looks fine to a byte counter and is garbage.
- **HTML:** pick a content root, strip boilerplate — but **keep a rescue pass**. If stripping leaves almost
  nothing while the body was substantial, redo it stripping only scripts/styles/consent. Measured: cookie
  banners and page-wrapping `<form>` elements were deleting entire documents.
- **Consent/cookie SDKs must be destroyed at any size**, because you can *name* them. Never give them the
  "it's most of the page, so it must be content" reprieve.
- **PDFs:** run the parser in a **subprocess crash barrier** — PDF libraries can hard-kill the interpreter on a
  malformed file. Wrap each page in its own try/except so one corrupt page cannot lose a 200-page report.
- **Tables are the highest-value content and the easiest to lose.** A bank's fee schedule *is* the competitive
  intelligence. Measured: with a text-only PDF parser, tables survived in **1–2%** of documents; a
  layout-aware library found **20 tables in the first 6 pages** of one document where the other found none.
- **Spreadsheets:** parse them as data (xlsx/xls/csv), not as text.
- **Scanned documents:** OCR **only after proving the file yields no characters** — extract first, and gate on
  a measured threshold (e.g. <50 chars/page). Gate **per page**, not per document: one file had 106 pages of
  which 2 carried text.

---

## 5. Never lose what you got

- **Store the original bytes, content-addressed**, and keep the raw artifact separate from the parsed reading.
  This is what makes everything below possible.
- **Change-detect on a hash of NORMALISED TEXT**, never raw bytes (CSRF tokens and "generated at" footers
  change every fetch), and **never with a model**.
- **Version your parser and re-read stored bytes when it improves.** The round only re-parses pages that
  *changed*, so without this every improvement applies to future documents only — a permanent invisible
  ceiling. Measured: re-reading one stored file with a fixed parser recovered **9,583,289 characters**, no
  network.
- **Backfill.** After any capability improvement, recover what it *would* have collected from pages already on
  disk. Measured: 18,618 files recoverable with no page re-fetch. But **respect the judge** — only backfill
  from pages whose links were never judged, or you silently overrule the judgment layer.
- **Reconcile.** Every link chosen must end somewhere you can name: stored, recorded as undownloadable, or
  skipped as a known duplicate. Measured: 112 chosen documents vanished with no error while every counter
  looked healthy.

---

## 6. The meta-rules — these matter more than any single technique

These come from repeatedly shipping bugs that looked like success.

1. **A capability that quietly does nothing is indistinguishable from one that found nothing.** This is the
   signature failure. Every capability ships with a counter, and a zero on that counter is a question.
2. **Prove every zero.** Before reporting "none found", run a positive control that *must* return something.
   Three separate false zeros came from queries reading a field name that did not exist — returning `None`
   thousands of times and "proving" a registry was empty.
3. **Count what LANDED, not what you attempted.** Reporting attempts as results claimed 19 facts where there
   were 5.
4. **Every cap must announce what it dropped.** A silent slice cost 71,278 rows of a 91,278-row regulatory
   register (78%), and later 123 pages of competitor financials — the same bug, twice, in one day.
5. **A capability is not done when its tests pass. It is done when the routine calls it.** Guard this with a
   test that fails the build if any capability has no caller. We shipped an OCR reader that worked perfectly
   and was invoked by nothing.
6. **The country belongs in a registry, never in engine logic.** Otherwise you build a system that only works
   for the country you demoed it on.
7. **Exit code 0 is not evidence the work happened.** Verify from the data. A "successful" re-parse silently
   skipped an entire country.
8. **Report failures to a human worklist, with the reason.** Anything code cannot get — hard walls, logins,
   undownloadable files — goes on a list a person can act on, never into a counter nobody reads.
