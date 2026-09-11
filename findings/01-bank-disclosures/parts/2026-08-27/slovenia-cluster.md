# Slovenia cluster — 2026-08-27 (complete)

Fresh run. WebSearch budget was fully exhausted (200/200) before this bank; all sourcing via curl (desktop UA) + local pdfminer.six on primary IR/press PDFs.

## Signals

1. **NLB Group — branch network / cash-light / CDS** (H1-2026 interim report, 06/08/2026). NLB d.d. 371 branches at 30/06/2026 (from 386 Jun-25, 381 Dec-25). Opened 3 new "cash-light" branches; one fitted with a Cash Deposit System (CDS) for legal-entity daily cash. Card+ATM net fee income EUR 71.965m H1 (+6%). → Cash automation/recyclers, self-service, managed services. **L / Medium.**

2. **NLB Group — POS / acquiring modernisation** (same report). Online paperless ordering of any POS terminal type (traditional/mobile/web) via Rekono eID; new Merchant Portal analytics; completed a major single-terminal multi-activity POS project for a large merchant; micro-merchant acquiring via fiscal cash-register partners. → POS/acquiring, digital onboarding/eKYC, TMS. **L / Medium.**

3. **NLB — Strategy 2030** (1H-2026 presentation, 06/08/2026). Payments pillar = "accelerate cash transition across SEE"; digital penetration 65%→>80%; full microservices tech transformation by 2030; STP >80% SI (95% group). Ambition >EUR 50bn assets, >EUR 2bn revenue, >EUR 1bn profit. → Group-wide self-service/recycler + eKYC + managed-services demand across SEE. **XL / Low.**

4. **OTP Skupina Slovenija — H1-2026 results** (press release, 05/08/2026). Net profit EUR 128m; ROE 13.9% grp / 14.0% bank; assets EUR 15.7bn; gross loans +6.7% to EUR 8.3bn; deposits EUR 12.6bn; LTD 65%; TCR 20.1%; LCR 349%; NIM 3.04%. OTP Skladi (AM) integration completed; new "Value Streams" operating model; Euromoney Best Bank in Slovenia. Post-merger (SKB + Nova KBM) fleet still consolidating. → ATM/self-service, cash automation, POS, managed services. **L / Medium.**

5. **OTP banka — ATM skimming wave** (security notice, 06/08/2026). Cluster of skimming fraud (mag-stripe copiers + hidden cameras/overlay keypads). → Anti-skimming, HSM/security, transaction monitoring, AML. **M / Medium.**

6. **Bankart — national processor incumbency** (site, 27/08/2026). Leading SI payment processor: ATM+POS acquiring processing, ATM/POS network management (TMS), card issuing/CMS, instant-payment/SEPA clearing & settlement, fraud prevention; exports instant-payment infra to central banks (Eurozone deployments). 17 agile teams. → Structural barrier to Printec POS/TMS/monitoring in SI, but potential hardware/partner channel. **M / Low.**

7. **Intesa Sanpaolo Bank Slovenija — data gap.** Only ISP Group (Italy) 1H26 (29/07/2026) found; no Slovenia-specific fleet disclosure. Unscoped; needs local report/AJPES. **is_new=false.**

## Access issues
- WebSearch 200/200 consumed before this bank — curl/pdfminer only.
- NLB locator is AEM SPA; branchsearch.search.json = 403 anonymous, needs browser session/CSRF → escalate to Claude-in-Chrome for ATM/deposit-capable counts.
- Bankart /en/news/ = HTTP 500 (WordPress error).
