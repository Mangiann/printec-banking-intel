# UniCredit Bank Romania - findings 27/08/2026

Merger with Alpha Bank Romania completed 15/08/2025. H1-2026 filed to BVB 25/08/2026.

## Headline numbers (primary)

| Metric | Value | As of | Source |
|---|---|---|---|
| Branches (Bank) | 246 (Group 249) | 30/06/2026 | H1-2026 report, BVB |
| Branches (Bank) prior | 265 (Group 268) | 31/12/2025 | H1-2026 report, BVB |
| Branches at merger | ~300 | 15/08/2025 | Merger completion PR |
| Employees (Group) | 4,261 | 30/06/2026 | H1-2026 report |
| ATM locations (locator) | 1,016 | 27/08/2026 | own marker service |
| of which deposit-capable (BNA) | 87 (8.6%) | 27/08/2026 | own marker service |
| of which Euronet-operated | 331 | 27/08/2026 | own marker service |
| Branch pins (locator) | 146 | 27/08/2026 | own marker service |
| Cashless-counter branches | 23 | 27/08/2026 | own marker service |
| Consolidated H1 net profit | RON 909.757m (+7.11%) | 30/06/2026 | H1-2026 report |
| RCC ROBOR fine exposure | RON 431m, unprovisioned | Jun-2026 | H1-2026 report |

## Signals

### UniCredit Bank S.A. (Romania) - XL / win Medium

- **Signal:** Merger by absorption of Alpha Bank Romania into UniCredit Bank S.A. legally completed 15/08/2025 (Alpha part of the group since 04/11/2024). At completion the bank stated ~300 branches, an extended network of 900 ATMs, over 4,800 employees and 11% share of assets / 13% of loans (incl. UniCredit Consumer Financing) / 11% of deposits. Alpha-issued cards ceased for payments and withdrawals on 14/08/2025 at 23:50 and for cash deposits at 17:30; replacement UniCredit cards were activated by customers at any ATM via the PIN-change option.
- **Source:** UniCredit Bank Romania press release, filed as BVB current report (issuer UCB27), 22/08/2025 - https://www.bvb.ro/infocont/infocont25/UCB27_20250822153248_RO-Anunt-finalizare-fuziune.pdf (primary)
- **Printec implication:** An ~900-unit ATM estate assembled from two different vendor fleets and two card portfolios must be harmonised onto one switch, one application load and one cash-management contract - the core Printec ATM-estate consolidation and managed-services play, with ATM-hosted card activation flows attached.
- **Follow-up:** Obtain the post-merger ATM hardware split (NCR Atleos / Diebold Nixdorf / other) and the expiry date of the incumbent ATM managed-services contract.

### UniCredit Bank S.A. (Romania) - XL / win Medium

- **Signal:** The bank's own locator marker service (crawled Romania-only on 27/08/2026) returns 1,016 ATM locations and 146 branch locations. Decoded against the bank's own published filter taxonomy (01 = ATM in branch, 02 = ATM off branch, 04/05 = Bank Note Acceptor in/off branch, 06 = BNA EUR), only 87 of the 1,016 ATM locations - 8.6% - carry any cash-deposit (bank note acceptor) capability, of which 8 accept EUR. 677 machines are off-branch and 259 in-branch. NOTE: the 146 branch pins are fewer than the 246 branches the bank reports in its H1-2026 filing, so the locator is a floor for branches, while the ATM feed is the only public machine-level source.
- **Source:** UniCredit Bank Romania branch/ATM locator marker service (getMarkersFiltered and getFilters, country=RO), 27/08/2026 - https://ro.unicreditbanking.net/branch/map?country=RO&lang=ro (primary)
- **Printec implication:** The single biggest quantified white space at this bank: roughly 929 cash-out-only ATMs with no deposit function, at a bank that has just cut a fifth of its branches. Direct Printec cash-recycler, cash-in module and deposit-automation opportunity.
- **Follow-up:** Re-pull this feed every run; a rising count of codes 04/05/06 is the leading indicator that a recycler programme has started. Establish who supplies the 87 existing BNA units.

### UniCredit Bank S.A. (Romania) / Euronet - L / win Low

- **Signal:** 331 of the 1,016 ATM locations in the bank's own feed are titled 'ATM UniCredit Euronet' - about a third of the estate runs on Euronet's outsourced network. Every one of the 331 is coded 02 (off-branch) and none carries a bank note acceptor. The bank's April-2025 reciprocal-ATM announcement with Alpha Bank Romania explicitly excluded Euronet machines from the fee-parity arrangement.
- **Source:** UniCredit Bank Romania locator marker service; UniCredit Bank Romania press release 'UniCredit Bank and Alpha Bank Romania customers have access to an extended ATM network', 15/04/2025 - https://www.unicredit.ro/en/institutional/media-center/press-releases/UniCreditBank-and-AlphaBank-Romania-have-acces-to-an-extended-ATM-network.html (primary)
- **Printec implication:** A third of the estate is already outsourced to a direct competitor of the managed-services model Printec sells, and it is entirely cash-out-only. Two plays: compete for the outsourced tranche at renewal, and position deposit-capable recyclers as the capability the Euronet off-branch fleet cannot deliver.
- **Follow-up:** Establish the start date and term of the Euronet Romania ATM outsourcing contract with UniCredit.

### UniCredit Bank S.A. (Romania) - XL / win Medium

- **Signal:** H1-2026 report filed to the Bucharest Stock Exchange on 25/08/2026: at 30/06/2026 the Group operated 249 branches and the Bank 246 branches, against 268 and 265 respectively at 31/12/2025 - 19 bank branches closed in six months, and down from the '~300' stated at merger completion in August 2025. Group headcount fell to 4,261 at 30/06/2026 from 4,475 at 31/12/2025 (Bank: 3,940 from 4,154).
- **Source:** UniCredit Bank S.A., Half-Year Report as of 30 June 2026 (FSA Reg. no. 5/2018), BVB filing, 25/08/2026 - https://www.bvb.ro/infocont/infocont26/UCB27_20260825154550_HALF-YEAR-REPORT-30-06-2026-IN-ACCORDANCE-WITH-FSA-REGULATIO.pdf (primary)
- **Printec implication:** Branch and staff reduction at this pace against a flat ~1,000-machine footprint forces transactions to self-service. That is the classic trigger for recyclers, assisted-service devices and outsourced ATM and cash managed services - Printec's core basket.
- **Follow-up:** Track the 30/09/2026 and FY-2026 branch counts; ask whether closed branches are being replaced by self-service lobbies.

### UniCredit Bank S.A. (Romania) - L / win Medium

- **Signal:** Locator records show 128 of the 146 listed branch locations have an ATM on site, only 4 branches are flagged 'Branch with Bank Note Acceptor (BNA) EUR', and 23 branch records carry the note 'SUCURSALA CU ATM - FARA NUMERAR LA CASIERIE' (branch with ATM, no cash at the teller counter).
- **Source:** UniCredit Bank Romania branch/ATM locator marker service (country=RO), 27/08/2026 - https://ro.unicreditbanking.net/branch/map?country=RO&lang=ro (primary)
- **Printec implication:** Cashless branches are already live in Romania. Once the teller stops handling cash, the lobby machine has to both dispense and accept - each of these 23 sites is an immediate recycler / assisted-self-service candidate, and the pattern normally spreads across the network.
- **Follow-up:** Get the roadmap for converting further branches to cashless, and the device specification used in the existing 23.

### UniCredit Consumer Financing IFN S.A. / UniCredit Bank Romania - L / win Medium

- **Signal:** H1-2026 report discloses that UniCredit Consumer Financing introduced 'a new video identification and digital onboarding solution', virtual credit cards, personal loans via Mobile Banking for non-UniCredit customers and a 'Scan to Credit' sales channel; automation within the lending process reached 82% for personal loans and 97% for point-of-sale loans. The Bank separately introduced personalised product offers inside the digital onboarding journey and launched a chat service in Mobile Banking and on the website.
- **Source:** UniCredit Bank S.A., Half-Year Report as of 30 June 2026 (FSA Reg. no. 5/2018), BVB filing, 25/08/2026 - https://www.bvb.ro/infocont/infocont26/UCB27_20260825154550_HALF-YEAR-REPORT-30-06-2026-IN-ACCORDANCE-WITH-FSA-REGULATIO.pdf (primary)
- **Printec implication:** A live, funded video-KYC and remote onboarding programme - squarely Printec's digital onboarding/eKYC line, plus the liveness and document-verification and AML screening that must sit behind it. 97% automation on point-of-sale loans also signals merchant POS credit volume worth POS/acquiring attention.
- **Follow-up:** Identify the vendor of the new video-identification solution and whether the Bank (not only UCFIN) will adopt it.

### UniCredit Bank S.A. (Romania) / Romanian Competition Council - M / win Low

- **Signal:** In June 2026 the Romanian Competition Council Plenum decided fines against all credit institutions in the ROBOR/ROBID benchmark investigation, of which approximately RON 431 million applies to UniCredit Bank Romania. The RCC preliminary report (1Q2026) concluded the banks exchanged confidential strategic non-public information on ROBOR quotes from November 2018. No IAS 37 provision has been booked; the bank will challenge the decision at the Court of Appeal within 30 days of the reasoned decision and seek suspension of payment and enforcement. Maximum exposure RON 431m excluding interest and penalties.
- **Source:** UniCredit Bank S.A., Half-Year Report as of 30 June 2026, contingencies note (BVB filing); related BVB current reports of 08/04/2026 and 08/06/2026, 25/08/2026 - https://www.bvb.ro/infocont/infocont26/UCB27_20260825154550_HALF-YEAR-REPORT-30-06-2026-IN-ACCORDANCE-WITH-FSA-REGULATIO.pdf (primary)
- **Printec implication:** A RON 431m conduct fine reliably pulls forward spend on compliance surveillance, market-conduct and communications monitoring and demonstrable audit trails - adjacent to Printec's AML/compliance and transaction-monitoring line, and it raises board-level appetite for provable controls.
- **Follow-up:** Watch for the reasoned decision text and any RCC-imposed compliance-programme obligations; the 30-day appeal clock starts on its communication.

### UniCredit Bank S.A. (Romania) - L / win Medium

- **Signal:** H1-2026 consolidated net profit RON 909.757m (+7.11% year on year) on consolidated operating income of RON 2,459.861m (+31.67%, helped by the Alpha Bank Romania integration). Operating expenses rose 39.87% to RON 1,066.238m, mainly because of the Romanian turnover tax, applied at 4% of turnover for H2-2025 and H1-2026. Tangible and intangible assets were roughly flat at RON 1,255.298m (31/12/2025: RON 1,275.116m).
- **Source:** UniCredit Bank S.A., Half-Year Report as of 30 June 2026 (FSA Reg. no. 5/2018), BVB filing, 25/08/2026 - https://www.bvb.ro/infocont/infocont26/UCB27_20260825154550_HALF-YEAR-REPORT-30-06-2026-IN-ACCORDANCE-WITH-FSA-REGULATIO.pdf (primary)
- **Printec implication:** A 4% turnover tax that hits revenue rather than profit is a structural cost shock, and flat fixed-asset investment says the bank is not buying its way out with capex. That is the exact profile that favours opex-based managed services and device-as-a-service over outright ATM purchase - Printec's managed-services model.
- **Follow-up:** Confirm whether the turnover tax is extended beyond H1-2026, and pitch opex/managed-service commercial models accordingly.

### UniCredit Bank S.A. (Romania) - M / win Medium

- **Signal:** 'Prime by UniCredit', the group's new affluent-client service model, was launched in Romania as part of a simultaneous rollout across nine CEE markets (Romania, Bulgaria, Bosnia and Herzegovina, Croatia, Czechia, Hungary, Serbia, Slovakia, Slovenia). In Romania it was launched at a NEW branch on Calea Dorobanti (in a former OTP Bank site) housing two dedicated Prime advisory offices, with Prime corners planned in further UniCredit units. CEO Mihaela Lupu framed opening new branches as deliberately counter-trend. A 'Welcome to Prime' cashback campaign of up to RON 1,000 ran 01/07/2026-30/09/2026.
- **Source:** BankingNews (on-site report from the launch event); Forbes.ro, 16/07/2026 - https://bankingnews.ro/unicredit-prime-romania-sucursala-dorobanti.html (press)
- **Printec implication:** Affluent branches are advisory-led and low-cash, which pushes routine cash and card servicing into the lobby device: assisted self-service, recyclers, instant card issuance and queue/appointment systems. Nine-market simultaneous rollout also makes this a regional, repeatable Printec fit-out opportunity rather than a Romanian one-off.
- **Follow-up:** Get the number of branches scheduled to receive Prime corners and the standard fit-out specification, and check the Bulgarian/Croatian/Serbian equivalents.

### UniCredit S.p.A. (group, covering UniCredit Bank Romania) - L / win Low

- **Signal:** UniCredit and Google Cloud signed a Memorandum of Understanding on 12/05/2025 setting out a 10-year agreement to migrate large parts of the application landscape, including legacy systems, to Google Cloud across the bank's 13 core markets - Romania among them - with Vertex AI and Gemini as the AI platform and named use cases including financial crime prevention and operational process optimisation. The MoU also opens the door to other Google divisions such as Google Maps Platform. UniCredit Bank Romania republished this on its own Romanian site.
- **Source:** UniCredit / Google Cloud joint press release, republished on UniCredit Bank Romania's site, 12/05/2025 - https://www.unicredit.ro/en/institutional/media-center/press-releases/UniCredit-Partners-with-Google-Cloud.html (primary)
- **Printec implication:** A group-mandated cloud and AI platform decides the integration surface any Romanian vendor must meet: channel and ATM management software, monitoring and AML/fraud tooling will be expected to run cloud-native and integrate with Vertex AI. 'Financial crime prevention' being named makes the transaction-monitoring/AML line a live group-level competition. Printec should be positioning for cloud-hosted ATM management and monitoring rather than on-premise appliances.
- **Follow-up:** Establish where Romania sits in the 13-market migration sequence and whether channel/self-service management is in scope. WARNING: the Google Cloud 'UniCredit case study' page is a 2014 Google Maps geolocator story and is NOT evidence of this cloud deal - do not cite it.


## Access notes

www.unicredit.ro and www.unicreditgroup.eu return HTTP 403 to the fetch tool; both return 200 to curl with a desktop Chrome User-Agent, which is the route used throughout. The unicredit.ro press-release index and the unicreditgroup.eu press-release and results indexes are client-side rendered and yielded no links to plain HTTP fetching; /bin/querybuilder.json on unicredit.ro is 301-redirected to a non-existent page and www.unicredit.ro/sitemap.xml 404s, so press releases are only reachable at known URLs. ro.unicreditbanking.net/branch/map requires both country and lang parameters (400/500 otherwise) and the marker service silently returns an empty array unless globalFilter is set (1=branches, 2=ATMs, 3=all). PDFs were extracted locally with pdftotext rather than through the fetch tool. Session WebSearch budget (200 calls) was exhausted after three queries at the start of this task, so all subsequent discovery was done by direct URL fetching and by walking the locator application's own JavaScript to find its API - no source was silently dropped.