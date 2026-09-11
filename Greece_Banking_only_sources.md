# Greece — Banking-only Sources

_Generated 2026-07-29 from `Greece - Banking & Payments Sources.xlsx`._

## Method & caveat
- The workbook's `sector` column is uniformly **`both`** for all 2,027 sources (no native banking/payments split), so this list is a **topic-based classification**, not an authoritative tag.
- **Banking** = topics/name about disclosures, lending/deposits, capital, branches, **ATM/self-service**, core banking, M&A, supervision, tenders, jobs, vendors, AML/onboarding.
- **Payments (excluded)** = cards, POS/acquiring, SEPA/instant payments, wallets, terminals, IRIS/TIPS, e-money, payment schemes.
- Sources showing **both** signals are NOT in the main list — they're flagged in a separate section so nothing banking-relevant is silently dropped.

## Counts
- **Banking (this list): 1044**
- Payments-focused (excluded): 137
- Mixed banking+payments (flagged below): 781
- Unclassified / no clear topic (flagged below): 65
- Total sources in workbook: 2027

## A1 · Corporate Disclosures — 172 banking sources

| Priority | Source | Type | Topics | URL |
|---|---|---|---|---|
| critical | ATHEX / Euronext Athens — Market Announcements feed (EL, Greek-language) | exchange_regulated_information_feed | disclosures, annual reports, press releases, earnings, corporate actions | https://athens.euronext.com/el/market-data/announcements |
| critical | ATHEX HERMES (H.E.R.ME.S) regulated-announcement dissemination system | regulated_disclosure_dissemination_platform | disclosures, press releases, regulated information, earnings, investor relations | https://athens.euronext.com/en/solutions-and-services/technology/hermes |
| critical | Alpha Bank Group — Investor Relations hub (current listed entity) | issuer_ir_site | investor relations, annual reports, earnings, press releases, disclosures | https://www.alpha.gr/en/Group/investor-relations |
| critical | Bank of Greece - Supervised Institutions Register (Εποπτευόμενα Ιδρύματα / Πιστωτικά Ιδρύματα) | regulator_register | disclosures, investor relations | https://www.bankofgreece.gr/kiries-leitourgies/epopteia/epopteyomena-idrymata |
| critical | Bank of Greece — Governor's Annual Report (Έκθεση του Διοικητή) | central_bank_annual_report | annual reports, disclosures, earnings | https://www.bankofgreece.gr/en/publications-and-research/publications/governors-annual-report |
| critical | EBA EU-wide transparency exercise (bank-by-bank data) | regulator_transparency_dataset | disclosures, earnings, capital | https://www.eba.europa.eu/eu-wide-transparency-exercise-0 |
| critical | ECB Banking Supervision - Pillar 2 requirement (individual bank P2R table) | regulator_capital_requirement_disclosure | disclosures, capital, earnings | https://www.bankingsupervision.europa.eu/activities/srep/pillar-2-requirement/html/index.en.html |
| critical | Eurobank Equities - Research | domestic_broker_research_portal | earnings, target_price, ratings, sell_side_research, valuation | https://www.eurobankequities.gr/en/research |
| critical | Eurobank — Investor Relations hub (current listed entity) | issuer_ir_site | investor relations, annual reports, earnings, press releases, disclosures | https://www.eurobank.gr/en/group/investor-relations |
| critical | Euroxx Securities - Research & Analysis | domestic_broker_research_portal | earnings, target_price, ratings, sell_side_research, sector_report | https://www.euroxx.gr/ |
| critical | Greece Officially Appointed Mechanism (OAM) — national central storage of regulated information (ATHEX) | officially_appointed_mechanism_oam | disclosures, regulated information, annual reports | https://www.athexgroup.gr/web/guest/home |
| critical | Hellenic Financial Stability Fund (HFSF / ΤΧΣ) — official website, press releases & announcements | state_body_official_website_press_releases | disclosures, press releases, investor relations, divestment, bank ownership, privatisation | https://hfsf.gr/en/ |
| critical | National Bank of Greece — Investor Relations hub | issuer_ir_site | investor relations, annual reports, earnings, press releases, disclosures | https://www.nbg.gr/en/group/investor-relations |
| critical | Optima Bank - Investor Relations (Ενημέρωση Επενδυτών) | issuer_investor_relations | disclosures, annual reports, investor relations, earnings, press releases | https://www.optimabank.gr/about-us/investor-relations/ |
| critical | Piraeus Financial Holdings — Investor Relations (listed parent, TPEIR) | issuer_ir_site | investor relations, annual reports, earnings, disclosures | https://www.piraeusholdings.gr/en/enhmerwsh-ependytwn |
| high | ATHEX company announcements portal (Greek-language) | exchange_announcements_archive | disclosures, press releases, regulated information, earnings | https://www.athexgroup.gr/el/web/guest/companies-info-announcements |
| high | ATHEX — Announcement of Regulated Information section (Law 3556/2007 / OAM central storage) | officially_appointed_mechanism_oam | disclosures, annual reports, voting rights, regulated information | https://www.athexgroup.gr/en/more-options/announcements/announcement-regulated-information-214 |
| high | ATHEX — Eurobank S.A. issuer announcements (issuer id 64) | per_issuer_announcement_stream | disclosures, annual reports, earnings, press releases, corporate actions | https://www.athexgroup.gr/en/market-data/issuers/64/announcements |
| high | ATHEX — Financial Calendar (issuer earnings / GM / dividend dates) | corporate_events_calendar | earnings, annual reports, corporate actions, disclosures | https://www.athexgroup.gr/en/market-data/financial-calendar |
| high | ATHEX — National Bank of Greece S.A. issuer page (issuer id 57) | per_issuer_announcement_stream | disclosures, annual reports, earnings, press releases, corporate actions | https://www.athexgroup.gr/en/market-data/issuers/57/announcements |
| high | ATHEX — Piraeus (Bank/Financial Holdings) issuer announcements (issuer id 63) | per_issuer_announcement_stream | disclosures, annual reports, earnings, press releases, corporate actions | https://www.athexgroup.gr/en/market-data/issuers/63/announcements |
| high | AXIA Ventures - Research (AVG Research) | investment_bank_research_portal | target_price, ratings, sell_side_research, earnings, daily_note | https://www.axiavg.com/avg-research/ |
| high | Aegean Baltic Bank - Annual Financial Statements | issuer_financial_statements | annual reports, disclosures, earnings | https://www.aegeanbalticbank.com/en/meet-abbank/financial-statements/annual-financial-statements |
| high | Alpha Bank - ESG disclosures / Sustainability Report (Alpha Services and Holdings) | issuer_esg_report_hub | disclosures, annual reports, investor relations, ESG, sustainability, non-financial statem | https://www.alpha.gr/en/Group/esg-and-sustainability/our-esg-strategy-and-goal/full-and-transparent-esg-disclosures |
| high | Alpha Finance - Research (Equity Research Division) | domestic_broker_research_portal | target_price, ratings, sell_side_research, earnings | https://www.alphafinance.gr/en/services/research |
| high | Alpha — Financial Results Presentations | results_presentations | earnings, investor presentations, disclosures | https://www.alpha.gr/en/Group/investor-relations/presentations/financial-results-presentations |
| high | Alpha — Group Results and Reporting / Financial Statements | financial_statements | annual reports, financial statements, disclosures, earnings | https://www.alpha.gr/en/Group/Investor-relations/Group-Results-and-Reporting |
| high | Athens-Macedonian News Agency (ANA-MPA) English - Economy | national_news_agency_english | press releases, earnings, disclosures | https://www.amna.gr/en/149754/Economy |
| high | BOUSSIAS Events - Conferences & Awards calendar | event_organizer_calendar | earnings, press releases, investor relations | https://calendar.boussiasevents.gr/ |
| high | Bank of Greece - Complaints handling / Conduct supervision (Καταγγελίες στην ΤτΕ) | central_bank_conduct_supervision | conduct, complaints, code_of_conduct, transparency, sanctions, payment_services | https://www.bankofgreece.gr/kiries-leitourgies/epopteia/pistwtika-idrymata/kataggelies-sthn-tte |
| high | Bank of Greece — Aggregated Balance Sheets & Income Statement of MFIs / Greek Commercial Banks | banking_statistics | earnings, disclosures | https://www.bankofgreece.gr/en/statistics/monetary-and-banking-statistics/aggregated-balance-sheets-of-mfis |
| high | Bank of Greece — Annual Report on Prudential Supervision and Resolution Activities | prudential_supervision_report | disclosures, annual reports | https://www.bankofgreece.gr/en/publications-and-research/publications/publications-list?mode=preview&categories=bankOfGreecePublications&bankOfGreecePublications=964f5097-67ca-4e96-9df3-47e1a6f80eda |
| high | Bank of Greece — Monetary Policy Report / Interim Report (Νομισματική Πολιτική) | monetary_policy_report | disclosures, annual reports | https://www.bankofgreece.gr/en/publications-and-research/publications/monetary-policy-report |
| high | Bank of Greece — Monetary and Banking Statistics | banking_statistics | disclosures, earnings | https://www.bankofgreece.gr/en/statistics/monetary-and-banking-statistics |
| high | Bank of Greece — Open Data Portal (opendata.bankofgreece.gr) | open_data_portal | disclosures | https://opendata.bankofgreece.gr/en/home |
| high | Bank of Greece — Press Office / Press Releases (Γραφείο Τύπου) | press_releases | press releases, disclosures | https://www.bankofgreece.gr/enimerosi/grafeio-typoy |
| high | Bank of Greece — Publications Search / Browse (Αναζήτηση Εκδόσεων) | publications_index | disclosures, annual reports | https://www.bankofgreece.gr/en/publications-and-research/publications/publications-list |
| high | Business Daily (businessdaily.gr) — Markets/Companies | business_news_portal | earnings, investor_relations, disclosures | https://www.businessdaily.gr/agores |
| high | Cooperative Bank of Chania - News / Press Releases | issuer_press_release | press releases, annual reports, disclosures, earnings | https://www.chaniabank.gr/en/news-press/ |
| high | Delphi Economic Forum - Agenda | policy_economic_forum | press releases, investor relations | https://delphiforum.gr/ |
| high | Diebold Nixdorf - Investor Relations & Press Releases | vendor_press_release | press releases, investor relations, disclosures, atm procurement | https://investors.dieboldnixdorf.com/news-and-events/press-releases/ |
| high | EBA Credit Institutions Register (CIR) | supervisory_register | disclosures, credit_institutions, actor_map, passporting | https://www.eba.europa.eu/risk-and-data-analysis/data/registers/credit-institutions-register |
| high | ECB Banking Supervision - Press releases feed | regulator_press_release_feed | press releases, disclosures, stress tests, capital, earnings | https://www.bankingsupervision.europa.eu/press/pr/date/2025/html/index.en.html |
| high | ECB Banking Supervision - Stress tests hub | regulator_stress_test_portal | earnings, disclosures, stress tests, capital | https://www.bankingsupervision.europa.eu/activities/stresstests/html/index.en.html |
| high | ECB Data Portal - Supervisory Banking data (SUP dataset) | regulator_data_api | earnings, disclosures, capital | https://data.ecb.europa.eu/data/datasets/SUP/data-information |
| high | ECB Supervisory Banking Statistics for significant institutions | regulator_supervisory_statistics | earnings, disclosures, capital | https://www.bankingsupervision.europa.eu/framework/statistics/html/index.en.html |
| high | ESMA Prospectus register (documents & securities) | disclosure_register | disclosures, prospectuses, issuers | https://registers.esma.europa.eu/publication/searchRegister?core=esma_registers_priii_documents |
| high | Eurobank - ESG Reporting page | issuer_esg_report_hub | disclosures, annual reports, investor relations, ESG, sustainability, non-financial statem | https://www.eurobank.gr/en/group/esg-environment-society-governance/esg-reporting |
| high | Eurobank — Career Opportunities | official_career_page | hiring_signals, job_postings, digital_payments | https://www.eurobank.gr/en/group/careers-at-eurobank/career-opportunities |
| high | Eurobank — Financial Results | results_presentations | earnings, press releases, disclosures, investor presentations | https://www.eurobank.gr/en/group/investor-relations/financial-results |
| high | Eurobank — Financial Results & Corporate Presentations | results_presentations | earnings, investor presentations, disclosures | https://www.eurobank.gr/en/group/investor-relations/presentations |
| high | Eurobank — Press Office / Corporate Announcements & Financial Calendar | press_releases | press releases, disclosures, financial calendar, earnings | https://www.eurobank.gr/en/group/grafeio-tupou |
| high | Euromoney — Awards for Excellence, Greece national winners | international_awards_body_index | awards, rankings, ESG, digital banking, SME | https://www.euromoney.com/awards/awards-for-excellence/ |
| high | Euronext Athens / ATHEX - Company Announcements | exchange_announcements | disclosures, press releases, earnings, investor relations | https://www.athexgroup.gr/en/market-data/announcements |
| high | European Single Access Point (ESAP) — ESMA-operated EU disclosure gateway | disclosure_aggregator | disclosures, annual_reports, issuers, esg | https://www.esma.europa.eu/esmas-activities/data/european-single-access-point-esap |
| high | Global Finance Magazine — Awards & Rankings hub | international_awards_body_index | awards, rankings, recognitions, digital banking, press releases | https://gfmag.com/awards-ranking/ |
| high | Greek systemic banks - IR financial calendars & event participation | issuer_ir_event_calendar | investor relations, earnings, disclosures | https://www.eurobankholdings.gr/en/investor-relations/presentations |
| high | Growthfund / National Development Fund (Υπερταμείο → Εθνικό Αναπτυξιακό Ταμείο, HCAP/EESYP) — Newsroom | state_holding_company_newsroom | press releases, state holding, privatisation, participations, disclosures | https://growthfund.gr/en/newsroom/ |
| high | HBA — Greek Banking System statistics (Στατιστικά στοιχεία) | sector_statistics | earnings, disclosures | https://www.hba.gr/En/Statistics/List?type=Brief_EN |
| high | HCMC — Announcements / Results (Ανακοινώσεις – Αποτελέσματα) | regulator_announcements_feed | press releases, disclosures, earnings | http://www.hcmc.gr/el/announcements |
| high | HCMC — Approved Prospectuses database (Επιτροπή Κεφαλαιαγοράς, Ενημερωτικά Δελτία) | regulator_prospectus_register | disclosures, prospectus, divestment, bank ownership, public offering | http://www.hcmc.gr/el/elib/deltia |
| high | HCMC — Decisions of the Commission (Αποφάσεις της Επιτροπής Κεφαλαιαγοράς) | regulator_decisions_register | disclosures, press releases | http://www.hcmc.gr/el/elib/decisions |
| high | HCMC — Major Holdings / Voting-Rights Change Notifications (Σημαντικές μεταβολές δικαιωμάτων ψήφου) | major_holdings_notifications | disclosures, investor relations | http://www.hcmc.gr/en_US/web/portal/participantcompany |
| high | HCMC — Prospectuses & Information Bulletins, last 12 months (Ενημερωτικά & Πληροφοριακά Δελτία 12μήνου) | prospectus_recent_feed | disclosures | http://www.hcmc.gr/el/deltia12minou |
| high | HCMC — Takeover Bids in Progress (Δημόσια Πρόταση / Takeover Bids) | takeover_bid_register | disclosures, press releases | http://www.hcmc.gr/en/web/portal/publicproposals |
| high | HFSF Annual Financial Reports (ετήσιες οικονομικές εκθέσεις) | audited_annual_financial_report_pdf | annual reports, disclosures, financial statements, bank ownership, divestment | https://growthfund.gr/en/reports/ |
| high | ICAP CRIF - Financial Statements database (icapcrif.com / icapb2b.gr) | commercial_financial_data_aggregator | disclosures, annual reports, earnings | https://www.icapb2b.gr/portal/web/b2b/products/financial-statements |
| high | IMH - Banking, Payments & FinTech Forum & EXPO | banking_fintech_expo | press releases, investor relations | https://banking.imhbusiness.com/ |
| high | Insider.gr — Companies/Banks (Τράπεζες) | sector_news_section | earnings, disclosures, investor_relations, press_releases | https://www.insider.gr/epiheiriseis/trapezes |
| high | Kathimerini English (ekathimerini.com) - Economy section | news_media_english_edition | earnings, annual reports, press releases, disclosures, investor relations | https://www.ekathimerini.com/economy/ |
| high | Ministry of National Economy & Finance — Press Releases (Υπουργείο Εθνικής Οικονομίας και Οικονομικών) | ministry_press_releases | press releases, divestment, privatisation, state holding, disclosures | https://minfin.gov.gr/en/press-releases/ |
| high | NBG — Financial Data & Results Presentations | results_presentations | earnings, disclosures, investor presentations | https://www.nbg.gr/en/group/investor-relations/financial-statements-annual-interim/presentations |
| high | NBG — Results Press Releases (Δελτία Τύπου Αποτελεσμάτων) | results_press_releases | earnings, press releases, disclosures | https://www.nbg.gr/en/group/investor-relations/financial-statements-annual-interim/results-announcements |
| high | NCR Atleos - Newsroom / Press Releases | vendor_press_release | press releases, disclosures, atm procurement | https://www.ncratleos.com/news |
| high | Naftemporiki English edition | financial_daily_english_edition | earnings, disclosures, investor relations, press releases | https://www.naftemporiki.gr/english/ |
| high | Natech Financial Software - Press & Media | company_newsroom | press releases, investor relations | https://natechbanking.com/press-and-media/ |
| high | National Bank of Greece (NBG) - ESG Reports and data | issuer_esg_report_hub | disclosures, annual reports, investor relations, ESG, sustainability, non-financial statem | https://www.nbg.gr/en/group/esg/vision-strategy/esg-reports-and-data |
| high | Oikonomikos Taxydromos (ot.gr) — Banks | sector_news_section | earnings, investor_relations, disclosures | https://www.ot.gr/category/epixeiriseis/trapezes/ |
| high | OpenData Γ.Ε.ΜΗ. API | official_registry_open_data_api | disclosures, annual reports, corporate actions | https://opendata.businessportal.gr/ |
| high | Optima bank - Research Department | domestic_broker_research_portal | earnings, target_price, sell_side_research, sector_report, strategy | https://www.optimabank.gr/en/individuals/services/analyseis-idiotes/ |
| high | Piraeus Financial Holdings - Sustainability Statement / ESG reports | issuer_esg_report_hub | disclosures, annual reports, investor relations, ESG, sustainability, non-financial statem | https://www.piraeusgroup.gr/en/investors/financials/annual-reports |
| high | Piraeus Group — Investor Relations hub | issuer_ir_site | investor relations, annual reports, earnings, press releases, disclosures | https://www.piraeusgroup.gr/en/investor-relations |
| high | Piraeus Group — Press Office (announcements & awards) | firm_press_release_awards | awards, recognitions, digital banking, cash management, press releases | https://www.piraeusgroup.gr/el/grafeio-typoy/anakoinwseis-kai-deltia-typou |
| high | Piraeus Securities - Equity Research | domestic_broker_research_portal | earnings, target_price, sell_side_research, sector_report | https://www.piraeus-sec.gr/en/research |
| high | Piraeus — Annual Reports | annual_reports | annual reports, disclosures, financial statements | https://www.piraeusgroup.gr/en/investor-relations/annual-reports |
| high | Piraeus — Financial Results | results_presentations | earnings, press releases, disclosures, investor presentations | https://www.piraeusgroup.gr/en/investor-relations/financial-results |
| high | Plum - company site & press | company_newsroom | press releases, investor relations | https://withplum.com/ |
| high | Reuters - Greek banks coverage (Athens desk) | international_wire | earnings, disclosures, investor relations | https://www.reuters.com/markets/ |
| high | StartUpper.gr - Fintech section | startup_media | press releases, investor relations | https://startupper.gr/fintech/ |
| high | capital.gr - Agores / Markets | financial_press_aggregator | target_price, ratings, sell_side_research, earnings | https://www.capital.gr/agores/ |
| high | mononews.gr - Agores (Aγορές) | financial_press_aggregator | target_price, ratings, sell_side_research, earnings | https://www.mononews.gr/agores |
| high | reporter.gr - Analyseis (Aναλύσεις) | financial_press_aggregator | target_price, ratings, sell_side_research, earnings | https://www.reporter.gr/analyseis |
| high | Γ.Ε.ΜΗ. One-Stop Services Portal (businessportal.gr) | registry_information_hub | disclosures, annual reports | https://www.businessportal.gr/en/home-en/ |
| medium | ATHEX / Euronext Athens Daily Price Bulletin (Ημερήσιο Δελτίο Τιμών) archive | daily_official_bulletin | disclosures, regulated information | https://athens.euronext.com/en/market-data |
| medium | ATHEX — Announcements & Press Releases (exchange-issued) | exchange_operator_press_releases | press releases, corporate actions, disclosures | https://www.athexgroup.gr/en/more-options/announcements/press-releases |
| medium | ATHEX — non-systemic / smaller bank issuer streams (Attica Bank, Optima Bank, Agricultural Bank id 858) | per_issuer_announcement_stream | disclosures, annual reports, earnings, press releases | https://athens.euronext.com/en/market-data/issuers/858/announcements |
| medium | ATHEX — per-issuer Financial Data section | per_issuer_financial_data | annual reports, earnings, disclosures | https://www.athexgroup.gr/en/market-data/financial-data |
| medium | ATHEX — per-issuer Informative Material section | per_issuer_informative_material | annual reports, disclosures, press releases | https://www.athexgroup.gr/en/market-data/issuers/63/informative-material |
| medium | Association of Greek Leasing Companies — AGLC (Ένωση Ελληνικών Εταιρειών Χρηματοδοτικής Μίσθωσης) | industry_association_portal | disclosures, annual reports | https://www.aglc.gr/ |
| medium | Bank of Greece - Financial Stability Review & Governor's Annual Report (climate/ESG sections) | central_bank_supervisory_publication | ESG, sustainability, climate risk, financial stability, disclosures | https://www.bankofgreece.gr/en/publications-research/publications/financial-stability-review |
| medium | Bank of Greece - Supervision (NCA within the SSM) | national_competent_authority | disclosures, earnings | https://www.bankofgreece.gr/kiries-leitourgies/epopteia |
| medium | Bank of Greece — Annual Accounts (Annual Financial Statements) | annual_accounts | annual reports, earnings, disclosures | https://www.bankofgreece.gr/en/publications-and-research/publications/publications-list?categories=bankOfGreecePublications&bankOfGreecePublications=3eb4d63f-d454-41a4-a59e-28e489e7cacb |
| medium | Bank of Greece — Career Opportunities | official_career_page | hiring_signals, job_postings, payment_systems_oversight, regulation | https://www.bankofgreece.gr/en/news-and-media/career-opportunities |
| medium | Bank of Greece — Economic Bulletin (Οικονομικό Δελτίο) | research_bulletin | disclosures | https://www.bankofgreece.gr/ekdoseis-ereyna/ereynitiki-drastiriotita/oikonomiko-deltio |
| medium | Bank of Greece — Financial Accounts Statistics | financial_statistics | disclosures | https://www.bankofgreece.gr/en/statistics/financial-accounts |
| medium | Bank of Greece — Financial Markets and Interest Rates Statistics (Χρηματοπιστωτικές αγορές και επιτόκια) | banking_statistics | disclosures | https://www.bankofgreece.gr/statistika/xrhmatopistwtikes-agores |
| medium | Boussias — Awards portfolio hub | awards_organizer_index | awards, recognitions, pointer | https://www.boussias.com/services/awards/ |
| medium | Capital.gr — Stock-exchange announcements feed | announcements_aggregator | disclosures, press_releases, earnings | https://www.capital.gr/xrim-anakoinoseis/ |
| medium | Cooperative Bank of Karditsa - Financial Data (Οικονομικά Στοιχεία) | issuer_financial_statements | annual reports, disclosures, earnings | https://www.bankofkarditsa.com.gr/el/trapeza/oikonomika-stoixeia |
| medium | Cooperative Bank of Thessaly (Τράπεζα Θεσσαλίας) - Press Releases | issuer_press_release | press releases, annual reports, disclosures | https://www.bankofthessaly.gr/media-center/ |
| medium | Dealnews.gr — Banks | sector_news_section | earnings, disclosures, press_releases | https://www.dealnews.gr/trapezes/ |
| medium | EBA 'Other list of institutions' (transparency, stress-test and topic-specific lists) | supervisory_list | disclosures, credit_institutions, stress_test, transparency | https://www.eba.europa.eu/risk-and-data-analysis/data/registers-and-other-list-institutions/other-list-institutions |
| medium | EBA EU-wide stress testing programme hub | regulator_stress_test_portal | stress tests, disclosures, capital | https://www.eba.europa.eu/risk-and-data-analysis/risk-analysis/eu-wide-stress-testing |
| medium | ECB Annual Report on supervisory activities | regulator_annual_report | disclosures, earnings, stress tests, capital | https://www.bankingsupervision.europa.eu/press/other-publications/annual-report/html/index.en.html |
| medium | ECB Banking Supervision - Published supervisory sanctions | regulator_sanctions_register | disclosures, press releases | https://www.bankingsupervision.europa.eu/activities/sanctions/supervisory-sanctions/html/index.en.html |
| medium | ECB Data Portal — Greece / Bank of Greece (BOG) series | statistics_aggregator | disclosures | https://data.ecb.europa.eu/data/geographical-areas/greece |
| medium | ESMA Crowdfunding service providers register (ECSPR) | supervisory_register | crowdfunding, actor_map, passporting | https://www.esma.europa.eu/esmas-activities/investors-and-issuers/investment-services-and-crowdfunding |
| medium | ESMA Financial Instruments Reference Database (FIRDS) | reference_database | disclosures, instruments, issuers | https://registers.esma.europa.eu/publication/searchRegister?core=esma_registers_firds |
| medium | ESMA MiFID II investment firms & MiFIR entities register (upreg) | supervisory_register | investment_firms, actor_map, passporting, disclosures | https://registers.esma.europa.eu/publication/searchRegister?core=esma_registers_upreg |
| medium | ESMA registered & certified Credit Rating Agencies register + European Rating Platform | supervisory_register | disclosures, credit_ratings, issuers | https://registers.esma.europa.eu/credit-rating-agencies/cra-authorisation |
| medium | Economist Impact SE Europe / Hazlis & Rivas - Greece conferences | policy_summit | press releases, investor relations | https://hazliseconomist.com/ |
| medium | Epsilon Net Group - Investor Relations / Sustainability (ESG) reports | issuer_esg_report_hub | disclosures, annual reports, investor relations, ESG, sustainability, non-financial statem | https://epsilonnet.gr/en/esg/ |
| medium | Euro2day.gr — ASE Market Announcements aggregator | announcements_aggregator | disclosures, press_releases, earnings | https://www.euro2day.gr/AseMarketAnnouncements.aspx |
| medium | Euronet - Fee-Free ATM Network Greece (euronetatms.gr) | operator_announcement | press releases, disclosures, atm procurement | https://www.euronetatms.gr/ |
| medium | Euronext Athens / ATHEX - Announcements & Greek Investment Forum | exchange_announcements | investor relations, disclosures | https://athens.euronext.com/en/more-options/announcements |
| medium | FinTech Futures - Greece region | fintech_trade_press | press releases, disclosures | https://www.fintechfutures.com/about-us |
| medium | GEMI datasets on data.gov.gr (National Open Data Portal) | national_open_data_catalogue | disclosures, corporate actions | https://data.gov.gr/data-service/rev1ko-euttop1ko-mntpwo-remh |
| medium | GlobeNewswire — Greece tag (commercial PR/disclosure wire) | pr_wire_service | press releases, regulated information, earnings | https://www.globenewswire.com/en/search/tag/greece |
| medium | Greek City Times - Business | news_media_english_diaspora | earnings, disclosures, press releases | https://greekcitytimes.com/category/business/ |
| medium | Greek financial press ΤΧΣ tag/aggregation pages (Naftemporiki, Οικονομικός Ταχυδρόμος/ot.gr, Reporter.gr, Imerisia) | financial_media_tag_feed | press releases, divestment, bank ownership, earnings, disclosures | https://www.ot.gr/tag/tameio-xrimatopistotikis-statherotitas/ |
| medium | HCMC MNRS — Electronic Transaction Notification System (Σύστημα γνωστοποίησης συναλλαγών, mnrs.hcmc.gr) | regulator_submission_portal | disclosures, investor relations | https://mnrs.hcmc.gr/_layouts/15/HCMCExtranet/SignIn.aspx?AppId=MNRS&ReturnUrl=%2f_layouts%2f15%2fAuthenticate.aspx%3fSource%3d%252F&Source=%2F |
| medium | HCMC — Annual Reports (Ετήσιες Εκθέσεις) | regulator_annual_report | annual reports, press releases | http://www.hcmc.gr/el_GR/web/portal/annualreports |
| medium | HCMC — Circulars (Εγκύκλιοι Επιτροπής Κεφαλαιαγοράς) | regulator_circulars | disclosures | http://www.hcmc.gr/el_GR/web/portal/elib/circulars |
| medium | HCMC — National Legislation (Εθνική Νομοθεσία) | regulator_legislation_index | disclosures | http://www.hcmc.gr/el_GR/web/portal/klawcatel |
| medium | HCMC — Public Consultations (Διαβουλεύσεις / consults) | regulator_consultations | disclosures, press releases | http://www.hcmc.gr/el_GR/web/portal/elib/consults |
| medium | HCMC — Recommendations / Guidelines / Announcements for Listed Companies (Συστάσεις-Οδηγίες-Ανακοινώσεις, Εισηγμένες) | regulator_issuer_guidance | disclosures, press releases | http://www.hcmc.gr/el/elib/dirseis |
| medium | Hellenic Capital Market Commission (HCMC) — regulator announcements & disclosure decisions | regulator_disclosure_archive | disclosures, regulated information | http://www.hcmc.gr/en/web/portal/home |
| medium | Hellenic Republic Asset Development Fund (HRADF / ΤΑΙΠΕΔ) | privatisation_fund_official_website | privatisation, press releases, state holding, disclosures | https://hradf.com/en/home/ |
| medium | Money Show (Athens & Thessaloniki polyconference) | economic_polyconference | press releases, investor relations | https://www.moneyshow.org/ |
| medium | NBG Securities (Ethniki Chrimatistiriaki) | domestic_broker_research_portal | sell_side_research, target_price, earnings | https://www.nbgsecurities.com/eng/ |
| medium | Natech Banking Solutions — Careers | vendor_career_page | hiring_signals, job_postings, core_banking, baas, engineering | https://natechbanking.com/ |
| medium | National Bank of Greece (NBG) — press/investor awards announcements | firm_press_release_awards | awards, recognitions, digital banking, press releases | https://www.nbg.gr/en |
| medium | National Printing House / Government Gazette search (Εθνικό Τυπογραφείο - ΦΕΚ ΤΑΕ-ΕΠΕ) | official_gazette_archive | disclosures, annual reports, corporate actions | https://search.et.gr/en/fek/ |
| medium | Pantelakis Securities - Research | domestic_broker_research_portal | sell_side_research, target_price, valuation, daily_note | https://research.pantelakis.gr/el |
| medium | Piraeus — Financial Calendar (Οικονομικό Ημερολόγιο) | financial_calendar | disclosures, earnings, financial calendar | https://www.piraeusgroup.gr/en/investor-relations/oikonomiko-hmerologio |
| medium | Protothema English - Economy | news_media_english_edition | earnings, disclosures, press releases | https://en.protothema.gr/economy/ |
| medium | QUALCO Group - ESG & Sustainability reports | issuer_esg_report_hub | disclosures, annual reports, ESG, sustainability, non-financial statement | https://qualco.group/esg-sustainability/ |
| medium | Sofokleousin.gr — Companies/Banks | sector_news_section | earnings, disclosures | https://www.sofokleousin.gr/category/trapezes |
| medium | The Recursive - Greek fintech coverage | startup_media | press releases, investor relations | https://therecursive.com/?s=greece+fintech |
| medium | Tiresias TSEK - Financial Data (ισολογισμοί & κλαδικοί δείκτες) | commercial_financial_data_aggregator | disclosures, annual reports, earnings | https://business.tiresias.gr/en/home/products-services/tsek-platform/financial-data/ |
| medium | To Vima International Edition - Finance | news_media_english_edition | earnings, disclosures, press releases | https://www.tovima.com/finance/ |
| medium | World Finance — Banking & Digital Banking Awards | international_award_program_winners | awards, digital banking, recognitions | https://www.worldfinance.com/awards/world-finance-banking-awards-2025 |
| medium | dealnews.gr - Trapezes (Tράπεζες) | financial_press_aggregator | ratings, target_price, sell_side_research | https://www.dealnews.gr/trapezes |
| medium | thebanker.gr — Greek banking sector media | specialized_banking_media | earnings, disclosures, annual_reports | https://thebanker.gr/ |
| low | Bank of Greece — Working Papers (Δοκίμια Εργασίας) | working_paper_series | disclosures | https://www.bankofgreece.gr/ekdoseis-ereyna/ereynitiki-drastiriotita |
| low | Chambers of Commerce GEMI announcements (Ανακοινώσεις Γ.Ε.ΜΗ. - ACCI/EBEA and regional chambers) | chamber_registry_announcements | disclosures, corporate actions, press releases | https://acci.gr/category/anakoinwseis-gemh-ae/ |
| low | Cyprus Mail - Greek banks (regional English) | regional_news_media_english | earnings, disclosures | https://cyprus-mail.com/ |
| low | Fortune Greece - Fintech tag | business_media | press releases, investor relations | https://www.fortunegreece.com/tag/fintech/ |
| low | Global Banking & Finance Review (GBAF) | banking_trade_press | earnings, disclosures | https://www.globalbankingandfinance.com/ |
| low | Global Banking & Finance Review — Global Banking & Finance Awards | international_award_program_winners | awards, recognitions, fintech | https://www.globalbankingandfinance.com/global-banking-finance-awards-2025-award-winners/ |
| low | Greek financial press coverage of EBA/SSM stress-test & SREP results | financial_media | stress tests, earnings, capital, press releases | https://www.capital.gr/ |
| low | Hellenic Bank Association (HBA/EET) - ATM network statistics | association_pointer | disclosures, atm procurement | https://www.hba.gr/En/Statistics/List?type=ATMSsNetwork_EN |
| low | Hellenic Bank Association - Greek Banking System Financial Data (Στατιστικά) | aggregated_statistics | earnings, disclosures | https://www.hba.gr/Statistics/List?type=GreeceResults |
| low | Hyosung TNS - Newsroom (ATM sub-vendor) | vendor_press_release | press releases, atm procurement | https://www.hyosung-tns.com/ |
| low | Liberal.gr — Banks | sector_news_section | earnings, disclosures | https://www.liberal.gr/trapezes |
| low | Moneyonline.gr — Banking news (Τραπεζικά) | sector_news_section | earnings, press_releases, disclosures | https://www.moneyonline.gr/news/trapezika/nea/trapezika |
| low | PayTech.Events - Greek banking/payments/fintech conference calendar | event_aggregator | press releases | https://paytech.events/events/ |
| low | Powergame.gr — Banks (Τράπεζες) | sector_news_section | earnings, disclosures | https://www.powergame.gr/trapezes/ |
| low | Qualco (Intelligent Finance) — Careers | vendor_career_page | hiring_signals, job_postings, fintech, engineering | https://www.qualco.finance/careers |
| low | SED (Σύνδεσμος Επενδυτών & Διαδικτύου) — announcements / press releases | investor_association | press releases, investor relations | https://sed.gr/category/%CE%B1%CE%BD%CE%B1%CE%BA%CE%BF%CE%B9%CE%BD%CF%89%CF%83%CE%B5%CE%B9%CF%83-%CF%83%CE%B5%CE%B4/ |
| low | T.C. Ziraat Bankasi - Athens Branch Announcements | foreign_branch_announcements | disclosures, press releases | https://ziraatbank.com.gr/en/announcements |
| low | Στατιστικά Γ.Ε.ΜΗ. (GEMI Statistics) | registry_statistics_dashboard | disclosures, corporate actions | https://statistics.businessportal.gr/ |

## A2 · Tenders & Procurement — 477 banking sources

| Priority | Source | Type | Topics | URL |
|---|---|---|---|---|
| critical | (Impact) BITE Awards — Business IT Excellence (BOUSSIAS/NetWeek) | industry_awards_program | IT projects, banking, insurance, fintech, digital transformation, vendor selection | https://businessitawards.boussiasevents.gr/past-winners/ |
| critical | ATHEX per-issuer announcements — Eurobank (issuer 64) & Eurobank Holdings | issuer_regulated_feed | material contracts, vendor disclosure, digital transformation, payments | https://www.athexgroup.gr/en/market-data/issuers/64 |
| critical | Bank of Greece - DORA (Digital Operational Resilience Act) supervision page | regulator_rules_page | DORA, ICT third-party, outsourcing, register of information, cyber resilience, vendor gove | https://www.bankofgreece.gr/en/main-tasks/supervision/dora-digital-operational-resilience-act-for-the-financial-sector |
| critical | Bank of Greece — Diavgeia organization page (BOGGR) | public_body_transparency_profile | Bank of Greece procurement, central bank IT contracts, awards, payments infrastructure | https://et.diavgeia.gov.gr/f/BOGGR |
| critical | Bank of Greece — Procurements / Tender announcements (English feed, category=Procurements) | issuer_tender_portal | tenders, procurement, public contracts, award notices | https://www.bankofgreece.gr/en/news-and-media/press-office/news-list?category=feefbf9a-194e-49e6-8382-722f20ca7ca7&sorting=date |
| critical | CrediaBank S.A. — ATHEX regulated announcements (issuer 50) | stock_exchange_regulated_disclosures | tenders, procurement, vendor_announcements, corporate_actions, IT_projects, payments | https://www.athexgroup.gr/en/market-data/issuers/50/announcements |
| critical | Cyber Security Awards (BOUSSIAS) — Past Winners archive | industry_awards_program | cyber security, banking, critical infrastructure, vendor selection, SIEM, cloud security | https://cybersecurityawards.boussiasevents.gr/past-winners/ |
| critical | Diebold Nixdorf — Investor Relations Press Releases | vendor_pressroom | ATM, self-service, cash recycling, contract, procurement | https://investors.dieboldnixdorf.com/news-and-events/press-releases |
| critical | EYDAP Tenders — Προκηρύξεις Έργων & Προκηρύξεις Προμηθειών | buyer_procurement_portal | tenders, procurement, public contracts, CRM and billing, payment collection, e-billing | https://www.eydap.gr/TheCompany/Contests/ |
| critical | Eurobank Holdings — Press Office regulatory announcements archive (1991→present) | issuer_ir_disclosure_archive | regulated_information, issuer_disclosures, annual_reports, corporate_announcements | https://www.eurobank.gr/en/group/grafeio-tupou?cat=%7BB2CAFCD0-EE0A-438E-9E13-4A7CBE1F39BB%7D |
| critical | Eurobank — Supplier Code of Conduct & Ethics acceptance form (Corporate Governance Principles) | supplier_onboarding_form | procurement, supplier onboarding, vendor registration, code of conduct, anti-bribery | https://www.eurobank.gr/el/omilos/poioi-eimaste/etairiki-diakubernisi/arxes-etairikis-diakubernisis-tis-eurobank/form-kodikas-ithikis-deontologias-promitheuton |
| critical | Euronext Athens — National Bank of Greece (ETE) issuer announcements feed | issuer_disclosure_feed | material contracts, vendor selection, capex, regulated information, award notices | https://athens.euronext.com/en/market-data/issuers/57/announcements |
| critical | G4S Cash Solutions S.A. (Greece) — Allied Universal, CASH360 / CIT services | vendor_corporate_site | cash_in_transit, cash_management, vaulting, atm_replenishment, smart_safe | https://www.g4s.com/el-gr/what-we-do/transportation-management-and-securities-services |
| critical | Growth Fund (ΕΕΣΥΠ) — Reports / Αναφορές hub (successor host of the HFSF archive) | official_reports_index | bank divestment, annual reports, financial statements, state holdings, IT/operational mode | https://growthfund.gr/reports/ |
| critical | Growthfund — English Procurement page | official_procurement_portal | tenders, procurement, public contracts, award notices, advisory | https://growthfund.gr/en/procurement/ |
| critical | KIMDIS / ΚΗΜΔΗΣ — Central Registry of Public Contracts (eprocurement.gov.gr portal) | central_public_contracts_registry | public contracts, procurement, contract awards, ADAM, tenders, vendor selection, IT/paymen | https://portal.eprocurement.gov.gr/ |
| critical | NBG Press Office (Γραφείο Τύπου) — press releases & announcements | corporate_pressroom | press releases, partnerships, digital transformation, payments, vendor announcements | https://www.nbg.gr/en/group/press-office |
| critical | Natech Banking Solutions — Press & Media | vendor_pressroom | core banking, banking as a service, vendor selection, IT/software contracts, neobank | https://natechbanking.com/press-and-in-the-media/ |
| critical | Natech Financial Software — customer stories / clients (Greek cooperative banks & Optima) | vendor_customer_list | core_banking, cooperative_banks, AML, cloud_core, Snappi, Optima, customer_references | https://natechbanking.com/customer-stories/ |
| critical | National Bank of Greece (NBG) — Press Office / Investor Relations regulated announcements | issuer_ir_disclosure_archive | core_banking_transformation, vendor_announcement, capex_signal, regulated_information, res | https://www.nbg.gr/en/the-group/press-office/press-releases |
| critical | National Bank of Greece (Εθνική Τράπεζα) — Press Office / Γραφείο Τύπου | bank_press_office | tenders, procurement, award notices, vendor selection, core banking, digital banking, paym | https://www.nbg.gr/el/omilos/grafeio-tupou |
| critical | NetFAX (Boussias Media) | it_trade_newsletter | tenders, procurement, public contracts, award notices, contract implementation stages, ven | https://subscriptions.boussiasmedia.gr/netfax-el.html |
| critical | Netcompany-Intrasoft Banking pressroom & case studies | vendor_pressroom_case_studies | core banking, payments, vendor references, bank clients, NPL/loan servicing | https://www.netcompany-intrasoft.com/news |
| critical | Netcompany-Intrasoft — Banking News & Announcements | vendor_press_release_feed | award notices, public contracts, core banking, payments | https://banking.netcompany-intrasoft.com/news-announcements |
| critical | Netcompany-Intrasoft — Banking case studies portal (PROFITS Core Banking) | vendor_customer_reference_page | core banking, vendor wins, migration, implementation stories, procurement | https://netcompany.com/netcompany-banking-services/ |
| critical | Netweek (Boussias Media) — enterprise IT news portal | trade_it_media | banking IT, digital transformation, vendor deals, software, IT services, core banking, AI | https://netweek.gr/ |
| critical | Piraeus Financial Holdings / Piraeus Group — Press Office (Announcements & Press Releases) | issuer_ir_disclosure_archive | cloud_transformation, vendor_announcement, ai_transformation, regulated_information, law_3 | https://www.piraeusgroup.gr/en/press-office |
| critical | QUALCO Group — Press Releases | vendor_pressroom | credit management, servicing, NPL, vendor selection, bank partnership, M&A | https://qualco.group/press-releases/ |
| critical | Snappi — Press office | company_press_office | product launch, licence, partnership, processor, BNPL, neobank | https://www.snappibank.com/en/press-office-en/ |
| critical | TED (Tenders Electronic Daily) — Bank of Greece contracting-authority notices | eu_procurement_register | tenders, procurement, public contracts, award notices | https://ted.europa.eu/en/notice/588433-2025/pdf |
| critical | TED Expert Search (query-language interface) | structured_search_interface | tenders, procurement, banking, payments | https://ted.europa.eu/en/expert-search |
| critical | TED — Greek-language portal (el) | supranational_official_procurement_journal_localized | tenders, procurement, banking, payments | https://ted.europa.eu/el/ |
| critical | Temenos Press Releases (global newsroom) | vendor_pressroom | tenders, procurement, core_banking, wins, digital_transformation | https://www.temenos.com/press-releases/ |
| critical | Temenos — Press Release Center | vendor_press_release_index | tenders, procurement, public contracts, award notices, core banking, wealth management, ve | https://www.temenos.com/press_release/ |
| critical | be24 (Be Business Exchanges SA) — Eurobank e-Auctions & e-Procurement portal | procurement_platform_subsidiary | procurement, tenders, e-auctions, vendor_selection, payments_infrastructure | https://www.be24.gr/el |
| critical | cosmoONE / marketsite.gr (sourceONE — ENTERSOFTONE eSOURCE) — private & public e-tender host | private_sector_etender_platform | tenders, procurement, private_bank_RFQ, banking, prequalification | https://www.cosmo-one.gr/lyseis/idiotikos-tomeas/ |
| critical | Δι@ύγεια OpenData REST API (luminapi search/export) | open_data_rest_api | tenders, procurement, public contracts, award notices, direct awards, payment orders, stru | https://diavgeia.gov.gr/luminapi/api/search/export?q=decisionType:%22%CE%9A%CE%91%CE%A4%CE%91%CE%9A%CE%A5%CE%A1%CE%A9%CE%A3%CE%97%22&wt=json |
| critical | Διαύγεια OpenData REST API (luminapi) | open_data_api | tenders, procurement, public contracts, award notices, direct awards, open data | https://diavgeia.gov.gr/luminapi/opendata/search |
| critical | Διαύγεια OpenData REST API (luminapi) | official_open_data_api | tenders, procurement, public contracts, award notices, direct assignment, expenditure comm | https://diavgeia.gov.gr/luminapi/opendata/search.json |
| critical | Διαύγεια — ΚτΠ Μ.Α.Ε. decisions feed (org 99220730) | government_transparency_register | award notices, public contracts, procurement, payments, decisions | https://diavgeia.gov.gr/f/ktpae |
| critical | ΕΑΔΗΣΥ / Hellenic Single Public Procurement Authority (HSPPA) — main site | regulator_authority_portal | procurement, tenders, guidance, legislation, vendor exclusion, public contracts | https://eadhsy.gr/ |
| critical | ΕΑΔΗΣΥ — Αποφάσεις Προδικαστικών Προσφυγών (Pre-litigation Appeal Decisions Database) | appeal_decisions_database | procurement, tenders, vendor selection, IT/software/services contracts, payments infrastru | https://eadhsy.gr/apofaseis/ |
| critical | ΕΣΗΔΗΣ Προμηθειών & Υπηρεσιών — Ηλεκτρονικές Διαγωνιστικές Διαδικασίες (Active Tender Search) | government_tender_search_portal | tenders, procurement, vendor selection, IT services, payments infrastructure, supplies | https://nepps-search.eprocurement.gov.gr/actSearch/faces/active_search_main.jspx |
| critical | Ελλάδα 2.0 / Greece 2.0 — National Recovery & Resilience Plan (RRF) official portal | government_rrf_portal | EU funding, RRF, Greece 2.0, digital transformation, calls, awards, projects, beneficiarie | https://greece20.gov.gr/en/ |
| critical | Ελλάδα 2.0 — Προσκλήσεις Χρηματοδότησης (Greece 2.0 RRF Funding Calls index) | funding_calls_index | tenders, procurement, funding_calls, digital_transformation, payments, rrf_pipeline | https://greece20.gov.gr/proskliseis-xrimatodotisis/ |
| critical | ΚΗΜΔΗΣ — Central Electronic Registry of Public Contracts (public-access search) | government_contracts_registry | procurement, public contracts, award notices, tenders | https://cerpp.eprocurement.gov.gr/upgkimdis |
| critical | Τράπεζα της Ελλάδος — Αναζήτηση Ενημερώσεων, κατηγορία Προκηρύξεις (EL) | tender_notice_listing | προμήθειες, διαγωνισμοί, προκηρύξεις, πληροφορική, φύλαξη, συστήματα πληρωμών | https://www.bankofgreece.gr/enimerosi/grafeio-typoy/anazhthsh-enhmerwsewn?sorting=date&category=c68cac9a-d8c5-45d1-b368-c1e68762771a |
| high | AADE 'Research of Business Registry Basic Details' (Αναζήτηση Βασικών Στοιχείων Μητρώου Επιχειρήσεων) | tax_registry_lookup | tax_registry, entity_resolution, afm_validation, api | https://www.aade.gr/en/research-business-registry-basic-details |
| high | AEPP legacy decisions portal (5518.syzefxis.gov.gr) — Αρχή Εξέτασης Προδικαστικών Προσφυγών decision PDFs | regulator_quasi_judicial_decision_archive_legacy | tenders, procurement, pre-contractual appeals, procurement disputes, IT contracts | http://www.5518.syzefxis.gov.gr/ |
| high | ATHEX / Euronext Athens — listed-company financial statements & regulated announcements | stock_exchange_disclosure_repository | listed vendor annual reports, regulated announcements, material contracts, related-party d | https://athens.euronext.com/en/trade/trading-products/trading-issuers |
| high | ATHEX Group / Euronext Athens - regulated-information announcements (listed non-systemic banks) | stock_exchange_regulated_information | award notices, material events, corporate announcements, procurement-adjacent disclosures | https://www.athexgroup.gr/en/web/guest/companies-announcements |
| high | ATHEX Issuers index (per-issuer directory) | issuer_register_index | tenders, procurement, material contracts, vendor disclosure | https://www.athexgroup.gr/en/market-data/issuers |
| high | ATHEX per-issuer announcements — Alpha Bank / Alpha Services & Holdings (issuer 278) | issuer_regulated_feed | material contracts, vendor disclosure, digital transformation | https://www.athexgroup.gr/en/market-data/issuers/278/announcements |
| high | ATHEX per-issuer announcements — Profile Systems & Software (issuer 968) | issuer_regulated_feed | material contracts, vendor disclosure, award notices, digital transformation, payments | https://www.athexgroup.gr/en/market-data/issuers/968/announcements |
| high | ATHEX per-issuer announcements — listed banking/payments IT vendors (Qualco 1526, Real Consulting 1468, Entersoft, Epsilon Net, Ilyda 976, Space Hellas, Unisystems/Quest, Byte) | vendor_issuer_feed | material contracts, vendor disclosure, award notices, digital transformation, payments | https://www.athexgroup.gr/en/market-data/issuers/1526 |
| high | Accenture Newsroom (press releases index) | vendor_pressroom_index | procurement, vendor_selection, digital_transformation, cloud, banking_it | https://newsroom.accenture.com/news |
| high | Accenture Newsroom — Greece banking press releases | consultancy_press_release | award notices, public contracts, payments, procurement | https://newsroom.accenture.com/ |
| high | Administrative Court of Appeals of Athens - suspension applications (Διοικητικό Εφετείο Αθηνών) | administrative_appeals_court_case_law | public contracts, bid protests, appeal decisions, procurement, tenders | https://www.adjustice.gr/webcenter/portal/defeteioath/apofaseis |
| high | Alpha Bank Careers portal (SuccessFactors) + LinkedIn jobs | employer_careers_portal | hiring signals, implementation projects, digital transformation, payments | https://careers.alpha.gr/ |
| high | Alpha Bank Careers portal (careers.alpha.gr) | employer_career_portal | hiring_signals, core banking, payments, IT | https://careers.alpha.gr/viewalljobs/ |
| high | Alpha Bank — Digital Procurement Platform (ESG 'Procurement Platform' page, EN) | procurement_platform_page | procurement, supplier platform, Oracle, digital transformation, ESG | https://www.alpha.gr/en/Group/esg-and-sustainability/environment/digital-transition-in-the-procurement-sector |
| high | Alpha Bank — Press Releases and Announcements (alpha.gr) | corporate_press_release_index | press releases, payments, vendor partnerships, digital transformation | https://www.alpha.gr/en/Group/media-centre/Press-Releases |
| high | Alpha Bank — entersoftONE eProcurement (Cosmo-One) supplier login portal | eprocurement_platform_operator | procurement, tenders, e_auctions, suppliers | https://www.cosmo-one.gr/en/project/alpha-bank/ |
| high | AppsRunTheWorld - Greek bank technographics / customer profiles | third_party_technographics_aggregator | vendor-to-bank mapping, core banking, software procurement intelligence, pointer index | https://www.appsruntheworld.com/customers-database/customers/view/national-bank-of-greece-greece |
| high | BRIS — Business Registers Interconnection System (European e-Justice Portal, Greece/EL) | eu_register_interconnection | subsidiaries, beneficial ownership, company register, corporate filings | https://e-justice.europa.eu/topics/registers-business-insolvency-land/business-registers-search-company-eu_en |
| high | Bank Investor-Relations regulated-announcement pages (Piraeus / Alpha Holdings / NBG / Eurobank Holdings) | issuer_ir_announcements | material contracts, vendor disclosure, digital transformation, regulated information | https://www.nbg.gr/en/the-group/investor-relations/financial-information/financial-announcements |
| high | Bank of Greece — Announcements RSS feed (legacy CMS feed) | rss_feed | tenders, procurement, public contracts, award notices | https://www.bankofgreece.gr/_layouts/15/BPC.RssFeeder/RssPage.aspx?Param=Announcements&lang=en |
| high | Bank of Greece — Authorisation page (Αδειοδότηση χρηματοδοτικών ιδρυμάτων) | regulator_licensing_page | licensing_registers, authorisation_process, regulatory_framework, AISP, PISP | https://www.bankofgreece.gr/en/main-tasks/supervision/financial-institutions/authorisation |
| high | Bank of Greece — Newsroom / Press Office (Tender Invitations, English) | buyer_press_office | tenders, procurement | https://www.bankofgreece.gr/en/news-and-media/press-office |
| high | Bank of Greece — Procurement announcements (Eurosystem NCB, banknote/cash & payment-system tenders) | central_bank_procurement_page | tenders, procurement | https://www.bankofgreece.gr/enimerosi/grafeio-typoy/anazhthsh-enhmerwsewn?category=c68cac9a-d8c5-45d1-b368-c1e68762771a |
| high | Bank of Greece — Procurements (English tender category, Newsroom) | official_procurer_tender_portal | tenders, procurement, public contracts, award notices | https://www.bankofgreece.gr/en/news-and-media/press-office/news-list/?sorting=date&category=feefbf9a-194e-49e6-8382-722f20ca7ca7 |
| high | BankingNews.gr — banking & economy news portal | banking_trade_media | banking, bank technology investment, digital banking, fintech, vendor deals | https://www.bankingnews.gr/ |
| high | Business Exchanges (be24) — e-Sourcing / e-Procurement / e-Auctions platform (Eurobank subsidiary, SAP Ariba) | e_sourcing_platform_operator | tenders, procurement, e-sourcing, e-auctions, RFP | https://www.be24.gr/el/be24 |
| high | Cashflex (Printec Cash Network A.E.) — Greek off-site ATM network | vendor_operator_site | atm, estate_transfer, contracts, self-service, fees | https://cashflex.gr/en/ |
| high | Central Register of Beneficial Owners (Κεντρικό Μητρώο Πραγματικών Δικαιούχων) | beneficial_ownership_register | beneficial_ownership, entity_resolution, control_chains, aml | https://www.gov.gr/ipiresies/epikheirematike-drasterioteta/elektronikos-phakelos-epikheireses/metroo-pragmatikon-dikaioukhon |
| high | Cepal (Resolute Cepal) — Newsroom | servicer_newsroom | e-Cepal platform, vendor partnerships, NPE servicing, real estate JV | https://resolute-cepal.com/en/news/ |
| high | Consultocracy — Vouliwatch (KIMDIS-based contract/vendor explorer) | ngo_data_tool | contract_awards, vendors, procurement, analysis | https://consultocracy.vouliwatch.gr/ |
| high | Court of Audit pre-contractual control audit reports (Εκθέσεις Ελέγχου Προσυμβατικού Ελέγχου) | audit_report | procurement, pre-contractual audit, IT contracts, banking | https://www.elsyn.gr/el/%CE%AD%CE%BB%CE%B5%CE%B3%CF%87%CE%BF%CE%B9 |
| high | CrediaBank — Investor Relations / Regulatory Announcements (Euronext Athens issuer feed) | regulatory_disclosure_feed | procurement, public_contracts, vendor_signals | https://athens.euronext.com/el/market-data/issuers/50/announcements |
| high | DEDDIE (HEDNO) Tender Notices — Διακηρύξεις Διαγωνισμών | buyer_procurement_portal | tenders, procurement, public contracts, IT and digitalization, e-billing | https://www.deddie.gr/el/tender-notice-common/ |
| high | Deloitte Greece — Banking & Capital Markets (industry hub) | advisory_firm_industry_hub | banking transformation, core banking, digital maturity, banking supervision, procurement ( | https://www.deloitte.com/gr/en/Industries/banking-capital-markets.html |
| high | Deloitte Greece — Press releases | consultancy_pressroom | banking_it, digital_transformation, vendor_selection, advisory | https://www.deloitte.com/gr/en/about/press-room/press-releases.html |
| high | Diavgeia (Δι@ύγεια) - EADHSY organization act feed | transparency_register | procurement, public contracts, award notices, transparency | https://diavgeia.gov.gr/f/eaadhsy |
| high | Diavgeia (Δι@ύγεια) — organization-scoped export API (per-buyer, e.g. TPD UID 99221150) | transparency_register_api | procurement, contract_awards, IT, payment_systems | https://diavgeia.gov.gr/luminapi/api/search/export?q=organizationUid:%2299221150%22&sort=recent&wt=xml |
| high | Diavgeia - EAADHSY transparency feed (Δι@ύγεια) | government_transparency_register | procurement, public contracts, appeal decisions, award notices, bid protests | https://et.diavgeia.gov.gr/f/eaadhsy |
| high | Diavgeia AI (diavgeia-ai.gr) — independent search/monitoring overlay | third_party_search_aggregator | procurement, direct awards, search, amount filtering, KHMDHS integration | https://diavgeia-ai.gr/en |
| high | Diavgeia bulk export endpoint (/luminapi/api/search/export) | bulk_export_endpoint | bulk download, procurement, awards, spending | https://opendata.diavgeia.gov.gr/luminapi/api/search/export?q=organizationUid:%22100054486%22&sort=recent&wt=xml |
| high | Diavgeia — Bank of Greece decisions feed (org code BOGGR) | transparency_registry_org_feed | procurement, awards, spend, contracts | https://diavgeia.gov.gr/f/BOGGR |
| high | Diebold Nixdorf Investor Relations — Press Releases | vendor_investor_pressroom | ATM, self-service, cash recyclers, vendor deployment, Piraeus Bank | https://investors.dieboldnixdorf.com/news-and-events/press-releases/default.aspx |
| high | Diebold Nixdorf — global newsroom / press releases | vendor_press_room | atm, self-service, contracts, award_notices | https://www.dieboldnixdorf.com/en-us/about-us/newsroom/ |
| high | Digital Finance (digital-finance.gr) — Greek fintech/payments trade media (Boussias) | fintech_payments_trade_media | payments, banking, vendor wins, fintech, public contracts, tenders | https://digital-finance.gr/ |
| high | EAADHSY - Single Public Procurement Authority (Ενιαία Αρχή Δημοσίων Συμβάσεων) | procurement_authority_official_site | procurement, public contracts, bid protests, appeal decisions, tenders | https://eadhsy.gr/eadisy/ |
| high | ECB Banking Supervision — List of supervised entities (SSM) | supervisory_entity_register | credit institutions register, banking supervision, participant register | https://www.bankingsupervision.europa.eu/framework/supervised-banks/html/index.en.html |
| high | ECB digital euro — progress reports & pilot hub (incl. Greek-language) | programme_progress_hub | digital euro, procurement, pilot participation, public contracts | https://www.ecb.europa.eu/euro/digital_euro/progress/html/index.el.html |
| high | EIB Group Supplier Portal & Procurement (corporate/administrative procurement) | institution_procurement_page | tenders, procurement | https://www.eib.org/en/about/procurement/index |
| high | EPANT - Hellenic Competition Commission (Επιτροπή Ανταγωνισμού) merger/concentration notices | regulator_competition_authority | tenders, procurement, public contracts, award notices, bank consolidation, M&A clearance | https://www.epant.gr/enimerosi/anakoinosi-sygkentroseon.html |
| high | EPCO — Eurosystem Procurement Coordination Office | coordination_body | tenders, procurement | https://epco.lu/ |
| high | EU Funding & Tenders Portal (SEDIA) — EU-managed procurement opportunities | official_tender_portal | procurement, tenders, awards, EU-managed contracts | https://ec.europa.eu/info/funding-tenders/opportunities/portal/screen/home |
| high | EU Funding & Tenders Portal — Procurement (single entry point for EU-institution tenders) | official_tender_publication_portal | tenders, procurement | https://ec.europa.eu/info/funding-tenders/opportunities/portal/screen/opportunities/tenders |
| high | EU e-Justice / BRIS - Business Registers Interconnection (Greece) | eu_register_interconnection | company_registry, cross_border, euid, entity_resolution, pointer | https://e-justice.europa.eu/topics/registers-business-insolvency-land/business-registers-eu-countries/el_en |
| high | EY Greece — Banking & Capital Markets (insights hub) | advisory_firm_industry_hub | banking transformation, AI in banking, regulatory outlook, open banking, agentic AI | https://www.ey.com/en_gr/industries/banking-capital-markets |
| high | EYATH Tender Procedures — Διαγωνισμοί Προμηθειών / Υπηρεσιών | buyer_procurement_portal | tenders, procurement, public contracts, billing systems, ERP, payment collection | https://www.eyath.gr/tender-procedures/ |
| high | Eurobank Holdings Investor Relations | investor_relations | IR, financial_results, digital_strategy, technology_investment | https://www.eurobankholdings.gr/en/investor-relations |
| high | Eurobank — Corporate Governance Principles (suppliers prerequisite section) | bank_first_party_supplier_gate_page | procurement, vendor onboarding, supplier code of conduct, anti-bribery | https://www.eurobank.gr/en/group/about-eurobank/corporate-governance/corporate-governance-principles |
| high | Euronext Athens — CrediaBank (ex-Attica Bank) issuer announcements feed | issuer_disclosure_feed | material contracts, vendor selection, capex, regulated information, capital raise | https://athens.euronext.com/en/market-data/issuers/50/announcements |
| high | Euronext Athens — Optima Bank issuer announcements feed | issuer_disclosure_feed | material contracts, vendor selection, capex, regulated information | https://athens.euronext.com/en/market-data/issuers/1510/announcements |
| high | Euronext Athens — Profile Systems & Software issuer announcements feed | issuer_disclosure_feed | material contracts, vendor selection, award notices, regulated information, customer wins | https://athens.euronext.com/en/market-data/issuers/968/announcements |
| high | Euronext Athens — corporate home / issuer services (post-acquisition operator of the Greek market) | exchange_operator | exchange_operator, portal_migration, issuer_services, disclosure_platform | https://athens.euronext.com/en |
| high | European Commission — Greece's Recovery and Resilience Plan (Reforms & Investments country page) | eu_plan_documentation | rrp_plan, financial_sector_reform, e_payments, milestones, annexes, eu_documentation | https://reforms-investments.ec.europa.eu/recovery-and-resilience-facility-1/country-pages/greeces-recovery-and-resilience-plan_en |
| high | FinTech Futures - Greece region feed (vendor-win news aggregator) | trade_media_aggregator | core_banking, payments, wins, implementations | https://www.fintechfutures.com/latest-news |
| high | FinTech Futures — Core Banking Technology (Greece coverage) | trade_media_aggregator | core_banking, vendor_selection, digital_banking, IT_contracts | https://www.fintechfutures.com/bankingtech/core-banking-technology |
| high | Finastra Press & Media (newsroom) | vendor_pressroom | payments, iso20022, wins, implementations | https://www.finastra.com/press-media |
| high | Finextra — fintech/payments news (National Bank of Greece & payments channels) | international_fintech_trade_press | core banking, payments, bank deals, vendor partnerships | https://www.finextra.com/company-news/2614/national-bank-of-greece |
| high | GEMI financial-statements filing (χρηματοοικονομικές καταστάσεις via businessportal.gr) | financial_statements_filing | financial_statements, contracts, entity_resolution, vendor_footprint | https://www.businessportal.gr/en/publicity/ |
| high | GRNET / EDYTE — Tenders (Διαγωνισμοί / RFPs) | state_it_agency_procurement_feed | procurement, tenders, IT infrastructure, cloud, cybersecurity, SMS gateway, data center, n | https://grnet.gr/category/rfps/ |
| high | Greece 2.0 (RRF) — Διακηρύξεις και Διαγωνισμοί (Tenders & Procurement) page | programme_procurement_listing | RRF, procurement, tenders, digital transformation, payments | https://greece20.gov.gr/diakirykseis-kai-diagwnismoi/ |
| high | Greece 2.0 — National Recovery & Resilience Plan (RRF projects hub) | funding_programme_registry | tenders, procurement | https://greece20.gov.gr/en/projects/ |
| high | Greece: OpenTender OCDS publication (OCP Data Registry) | ocds_bulk_dataset | tenders, procurement, public contracts, award notices | https://data.open-contracting.org/en/publication/55 |
| high | Growthfund (HCAP / National Development Fund) — Tenders & Calls (Προκηρύξεις) | state_holding_company_procurement_portal | procurement, tenders, IT services, cybersecurity, ERP, consulting, state holdings, banks s | https://growthfund.gr/prokirykseis/ |
| high | Growthfund — Newsroom / Τα Νέα μας (press releases & announcements) | official_press_room | award notices, divestment, governance, advisory | https://growthfund.gr/newsroom/nea/ |
| high | HCMC — Public Tender Offers information circulars (Δελτία Δημοσίων Προτάσεων) | regulator_disclosure_repository | takeover_bids, public_tender_offers, listed_companies, control_changes, bank_m&a | http://www.hcmc.gr/el/deltiaprotaseon12minou |
| high | HERMES — ATHEX central storage mechanism (OAM) for regulated information | central_storage_mechanism_oam | material contracts, vendor disclosure, regulated information | https://www.athexgroup.gr/en/solutions-and-services/technology/hermes |
| high | Hellenic Capital Market Commission (HCMC) — Transparency / Listed companies & Shareholders portal | financial_regulator | transparency_regulation, periodic_disclosure, law_3556_2007, issuer_obligations | http://www.hcmc.gr/en_US/web/portal/transparency1 |
| high | Hellenic Capital Market Commission (Επιτροπή Κεφαλαιαγοράς) — Tenders & Procurement page | regulator_procurement_page | tenders, procurement, public contracts, award notices, IT systems, market surveillance | http://www.hcmc.gr/el/elib/tenders |
| high | Hellenic Court of Audit (Ελεγκτικό Συνέδριο / ELSYN) — main site | supreme_audit_institution_site | public contracts, pre-contractual audit, award review, jurisprudence | https://www.elsyn.gr/el |
| high | Hellenic Court of Audit - pre-contractual audit (Ελεγκτικό Συνέδριο, προσυμβατικός έλεγχος) | supreme_audit_institution_preaudit | public contracts, audit findings, procurement, award notices, tenders | https://www.elsyn.gr/el/node/1523 |
| high | Hellenic Court of Audit — Pre-contractual audit results (πράξεις Κλιμακίων) | audit_results_listing | public contracts, pre-contractual audit, award review | https://www.elsyn.gr/el/%CE%BD%CE%BF%CE%BC%CE%BF%CE%BB%CE%BF%CE%B3%CE%AF%CE%B1?page=0 |
| high | Hellenic Financial Stability Fund (ΤΧΣ / HFSF) — official site (legacy/archive) | official_agency_site_legacy | procurement, advisory, divestment, bank stakes, award notices | https://growthfund.gr/en/ |
| high | Hellenic Financial Stability Fund (ΤΧΣ/HFSF) — Procurement / Προκηρύξεις page | oversight_fund_procurement_page | tenders, procurement, public contracts, advisor RFP, banking | https://hfsf.gr/en/procurement/ |
| high | IBS Intelligence — Greek bank / core-banking vendor news | trade_media_aggregator | core_banking, vendor_selection, risk_compliance, IT_contracts | https://ibsintelligence.com/news-and-analysis/ |
| high | IBS Intelligence — fintech news (vendor wins naming Greek banks) | third_party_fintech_news | procurement, award notices, risk management, core banking, digital banking | https://ibsintelligence.com/ibsi-news/greece-based-attica-bank-selects-profile-softwares-risk-management-system-riskavert/ |
| high | ICAP CRIF (business information & credit-risk data, Greece) | commercial_business_information_aggregator | company_data, credit_risk, sector_studies, group_structure, entity_resolution | https://icapcrif.com/en/our-services/business-information-credit-risk-services/business-information-services/ |
| high | ICT Plus (ictplus.gr) - Greek IT/tech trade press | it_trade_press | tenders, award notices, IT project awards, systems integrators, procurement | https://ictplus.gr/ |
| high | Infosys Finacle / EdgeVerve — Client wins (National Bank of Greece) | vendor_customer_reference_page | core banking, vendor wins, procurement, award notices | https://www.edgeverve.com/finacle/ |
| high | Kathimerini — Economy / Οικονομικά (el) and ekathimerini.com (en) | business_financial_press | tenders, procurement, public contracts, banking, payments, vendor wins | https://www.kathimerini.gr/economy/ |
| high | LinkedIn Jobs — Temenos jobs in Athens (geo+keyword permalink) | job_board_search | core banking, Temenos T24, vendor hiring, procurement | https://gr.linkedin.com/jobs/temenos-jobs-athens |
| high | List of credit institutions operating in Greece (Πίνακας Πιστωτικών Ιδρυμάτων σε λειτουργία) | regulator_register_file | credit institutions, πιστωτικά ιδρύματα, banks, register | https://www.bankofgreece.gr/RelatedDocuments/1_CreditInstitutions.xlsx |
| high | Microsoft Customer Stories (catalog, Greece/banking filterable) | vendor_case_study_index | cloud, azure, banking_it, vendor_selection, ai | https://www.microsoft.com/en/customers/search?filters=story%3Bindustry%3Abanking-and-capital-markets%3Bcountry%3Agreece |
| high | Ministry of Digital Governance (ΥΨΗΔ) — Proclamations/Tenders (Προκηρύξεις–Διαγωνισμοί) | ministry_procurement_portal | procurement, tenders, cybersecurity, digital governance, gov.gr, telecommunications, IT se | https://www.mindigital.gr/prokhryxeis |
| high | Ministry of National Economy & Finance — Legislative work page for the ΕΕΣΥΠ restructuring law (5131/2024) | government_legislation_page | governance, public contracts, procurement, divestment | https://minfin.gov.gr/ypourgeio/nomothetiko-ergo/schedio-nomou-anadiarthrosi-tis-ellinikis-etaireias-symmetochon-kai-periousias-kai-ton-thygatrikon-tis/ |
| high | My Docman - Προδικαστικές Προσφυγές case database | legal_case_aggregator | bid protests, appeal decisions, public contracts, procurement | https://www.mydocman.gr/ |
| high | NBG Business Seeds — Innovation Competition Winners (National Bank of Greece) | bank_accelerator_cohort | fintech, accelerator, vendor_discovery, payments, banking_tech | https://www.nbg.gr/el/epaggelmaties/nbg-business-seeds/nikites |
| high | NCR Atleos Investor Relations — Press Releases / Newsroom | vendor_investor_pressroom | ATM-as-a-Service, Cashzone, Epirus Bank, ATM network, outsourcing | https://investor.ncratleos.com/news-events/press-releases |
| high | NCR Atleos — Newsroom & Insights (Epirus Bank ATMaaS; Eurobank NDC migration) | vendor_press_release | ATM as a service, ATM network, Cashzone, NDC Enterprise, Epirus Bank, Eurobank, managed se | https://www.ncratleos.com/news/ |
| high | Naftemporiki - Business / Finance section (naftemporiki.gr) | financial_business_press | tenders, procurement, public contracts, award notices, bank vendor deals, payments | https://www.naftemporiki.gr/business/ |
| high | Naftemporiki — Technology & Science / Finance sections | business_daily | banking, digital transformation, payments modernization, technology, finance | https://www.naftemporiki.gr/techscience/ |
| high | Natech Banking Solutions — Customer Stories | vendor_customer_reference_index | public contracts, award notices, procurement | https://natechbanking.com/customer-stories |
| high | National Bank of Greece (NBG) Career Opportunities | employer_career_portal | hiring_signals, core banking, payments, IT | https://www.nbg.gr/el/omilos/anthrwpino-dunamiko/eukairies-karieras |
| high | National Bank of Greece (NBG) — career opportunities | employer_careers_portal | hiring_signals, procurement, payments, core_banking, IT_projects | https://www.nbg.gr/en/group/human-resources/career-opportunities |
| high | National Printing House - Company Search & ΦΕΚ (Εθνικό Τυπογραφείο, search.et.gr) | official_gazette_company_archive | company_registry, historical_acts, mergers_successors, entity_resolution, gazette | https://search.et.gr/en/search-company/ |
| high | NetFAX (Boussias Media daily IT/telecom newsletter) | it_trade_newsletter | tenders, public sector IT, telecom system tenders, procurement, bank IT projects, payments | https://www.boussias.com/portfolios/netfax/ |
| high | Netcompany — Financial Services / Banking Services (post-rebrand canonical) | vendor_solutions_and_news_page | core_banking, financial_services, project_wins, banking, payments | https://netcompany.com/private-sector/financial-services/ |
| high | Netcompany-Intrasoft - Banking / news (PROFITS core banking) | vendor_customer_and_press_page | core banking, system integration, banking IT projects, vendor customer references | https://www.netcompany-intrasoft.com/ |
| high | Netcompany-Intrasoft Banking — News & Case Studies (PROFITS Core Banking) | vendor_customer_reference | vendor selection, award notices, core banking, payments, procurement | https://banking.netcompany-intrasoft.com/case-studies |
| high | Netcompany-Intrasoft — News/press (HSBC Greece → Pancreta PROFITS migration) | vendor_news_index | core banking, migration, vendor wins, procurement, award notices | https://www.netcompany-intrasoft.com/news/ |
| high | Netcompany-Intrasoft — careers on SmartRecruiters (maker of PROFITS core banking) | vendor_careers_page | core banking, PROFITS, vendor hiring, integrator, procurement | https://careers.smartrecruiters.com/netcompanyintrasoft |
| high | OpenTender.eu — Greece (Government Transparency Institute / DIGIWHIST) | open_procurement_data_aggregator | tenders, procurement, public contracts, award notices, open data, CPV analysis | https://opentender.eu/gr |
| high | Optima Bank — official website / About & Company | bank_website | bank_profile, IR, digital_banking, vendor_signals | https://www.optimabank.gr/en/about-us/company/ |
| high | Optima bank - Newsroom & Investor Relations (Deltia Typou) | bank_press_release_ir | tenders, procurement, vendor partnership, payments technology, award notices | https://www.optimabank.gr/about-us/newsroom/ |
| high | Optima bank — Corporate site / Press & Newsroom (Ο όμιλος) | issuer_press_release | procurement, vendor_signals, award_notices | https://www.optimabank.gr/about-us/company/ |
| high | PEE 178/5/2.10.2020 - Outsourcing of activities framework (Εξωτερική ανάθεση δραστηριοτήτων) | executive_committee_act | outsourcing, εξωτερική ανάθεση, cloud, EBA guidelines, vendor governance | https://www.bankofgreece.gr/enimerosi/grafeio-typoy/anazhthsh-enhmerwsewn/enhmerwseis?announcement=b9745fd4-8b8a-41da-ae71-35d1f73995ff |
| high | Piraeus Bank Careers + LinkedIn jobs | employer_careers_portal | hiring signals, implementation projects, digital transformation, payments | https://www.linkedin.com/company/piraeus-bank/jobs |
| high | Piraeus Group — Press Office / Announcements & Press Releases | press_release_feed | partnerships, IT, payments, vendor deals, digital transformation | https://www.piraeusgroup.gr/en/press-office/news-announcements |
| high | Piraeus Group — career opportunities portal | employer_careers_portal | hiring_signals, IT_projects, payments, core_banking, procurement | https://www.piraeusgroup.gr//en/career/career-opportunities-in-piraeus-group |
| high | Powergame.gr — 'Start-ups & Digital' section (bank-fintech deal tracker) | business_media_deal_tracker | fintech deals, bank-fintech partnership, acquisitions, startups, payments, BNPL | https://www.powergame.gr/start-ups-digital/ |
| high | Profile Software (PROFILE A.E.B.E. / PROF) — investor relations & annual reports (banking-software vendor) | vendor_investor_relations_filings | banking software vendor, annual report, client/contract disclosures, revenue by segment | https://www.profilesw.com/el/ |
| high | Profile Software (Profile Systems & Software) - Press Releases | vendor_press_release_page | core banking, risk and compliance software, digital banking, vendor customer references | https://www.profilesw.com/news-events/press-releases/ |
| high | Profile Software — Industry Recognition / Press Releases | vendor_awards_pressroom | core banking, digital banking platform, vendor selection, awards | https://www.profilesw.com/about-us/industry-recognition/ |
| high | Profile Software — News & Events / Press Releases | vendor_press_release_page | core_banking, risk_compliance, regulatory_reporting, project_wins, banking, payments | https://www.profilesw.com/news-events/category/press-releases/ |
| high | Profile Software — News / Press Releases (English) | vendor_pressroom | public contracts, award notices, procurement | https://www.profilesw.com/en/news/ |
| high | Profile Software — Press Releases / News & Events (vendor customer announcements) | vendor_customer_reference | vendor_signals, award_notices, procurement | https://profilesw.com/news-events/press-releases/ |
| high | Profile Software — Press releases / News & Events (deltia typou) | vendor_pressroom | core_banking, digital_banking, vendor_selection, payments_infrastructure | https://www.profilesw.com/el/news-events/deltia-typou/ |
| high | Profile Software — Δελτία Τύπου (Greek-language press releases) | vendor_pressroom | public contracts, award notices, procurement | https://www.profilesw.com/el/news.php |
| high | PwC Greece — Financial Services publications | advisory_firm_publications_index | banking, capital markets, fintech, payments, wealth management, financial services surveys | https://www.pwc.com/gr/en/publications/financial-services.html |
| high | QUALCO Group — Corporate site (solutions & news) | vendor_pressroom | credit management software, servicing platform, BPO unit, bank JVs | https://qualco.group/ |
| high | Quest Holdings press-center & news-by-company (aggregator) | group_press_aggregator | group announcements, Uni Systems banking, Intelli Solutions, Finastra treasury/payments pa | https://www.quest.gr/en/news-by-company?cid=Uni+Systems |
| high | Register of agents of credit institutions & tied agents (Μητρώο Αντιπροσώπων ΠΙ / συνδεδεμένοι αντιπρόσωποι) | regulator_register_file | agents, αντιπρόσωποι, tied agents, distribution, register | https://www.bankofgreece.gr/RelatedDocuments/20_Commercial_Agents_of_Credit_Institutions.xlsx |
| high | SEPE.gr — Federation of Hellenic ICT Enterprises (news portal) | industry_association_news | ICT industry news, digital transformation, cybersecurity, AI, public digital projects | https://www.sepe.gr/gr/tehnologia-pliroforiki/ |
| high | Snappi Bank (neobank powered by Natech / Piraeus JV) | neobank_client_site | neobank, banking as a service, payments infrastructure, vendor selection | https://www.snappibank.com/en/ |
| high | Space Hellas News / Newsroom | vendor_pressroom | data center, SDN/ACI, bank projects, cyber security, financial results | https://www.space.gr/el/news |
| high | Space Hellas S.A. — annual financial reports (listed ICT integrator; Alpha Bank ~20% shareholder) | vendor_investor_relations_filings | vendor annual report, financial-sector projects, related-party disclosure, revenue concent | https://www.space.gr/en/investors-relations |
| high | Space Hellas — Financial Sector page (Χρηματοοικονομικός Τομέας) | vendor_banking_vertical_site | tenders, procurement, public contracts, award notices, managed services, data center, syst | https://www.space.gr/pages.php?langID=1&pageID=82 |
| high | Space Hellas — News & Publications (project news feed) | vendor_press_release_page | project_wins, data_center, networking, banking, financial_services | https://www.space.gr/pages.php/news |
| high | TAIPED / HRADF official site — tenders & calls (Προκηρύξεις – Προσκλήσεις) | procurement_index | procurement, technical/legal/financial advisers, privatization tenders | https://hradf.com/prokirixeis-proskliseis/ |
| high | TED (Tenders Electronic Daily) — Bank of Greece contracting-authority notices | eu_procurement_register | EU contract notices, contract awards, banknote paper, above-threshold procurement | https://ted.europa.eu/en/advanced-search |
| high | TED Bulk XML Download (daily/monthly notice packages) | bulk_data_archive | tenders, procurement, public contracts, award notices | https://ted.europa.eu/en/simap/xml-bulk-download |
| high | TED Bulk XML Packages (daily / monthly downloads) | bulk_data_download | tenders, procurement | https://ted.europa.eu/en/help/data-reuse |
| high | TED Developer Documentation & Portal | api_documentation | tenders, procurement, public contracts, award notices | https://docs.ted.europa.eu/home/index.html |
| high | TED Developer Portal & API (eForms / notices search API) | procurement_api | tenders, procurement | https://developer.ted.europa.eu/ |
| high | TED Open Data Service (RDF / SPARQL endpoint) | linked_open_data_sparql | tenders, procurement, banking, payments | https://data.ted.europa.eu/ |
| high | TED single-notice viewer / download (HTML/PDF/XML per notice) | single_notice_record | tenders, procurement, public contracts, award notices | https://ted.europa.eu/en/notice/301561-2025/pdfs |
| high | TED — Tenders Electronic Daily (EU) — Greek public financial-body notices | eu_procurement_journal | tenders, procurement, IT, payment_systems | https://ted.europa.eu/ |
| high | Temenos Careers — Greece/Athens roles | vendor_career_portal | hiring_signals, core banking, payments, Temenos, implementation | https://www.temenos.com/about-us/careers/ |
| high | Temenos Customer Success Stories | vendor_customer_story | core_banking, payments, implementations, wins | https://www.temenos.com/success-stories/ |
| high | Temenos — Customer Success / Case Studies hub | vendor_case_study_hub | core_banking, vendor_selection, IT_contracts, digital_banking, payments_infrastructure | https://www.temenos.com/en/customer-success/customer-case-studies/ |
| high | Temenos — Press Releases / Newsroom (news index) | vendor_pressroom | public contracts, award notices | https://www.temenos.com/news |
| high | Temenos — Success Stories / Customer References hub | vendor_customer_reference_index | public contracts, award notices, procurement | https://www.temenos.com/community/success-stories/ |
| high | TheRecursive.com — Greek/SEE startup funding coverage | startup_news_media | funding_rounds, fintech_startups, bnpl, deals, bank_partnership | https://therecursive.com/top-funding-rounds-raised-by-greek-startups-in-2025/ |
| high | Tiresias S.A. (ΤΕΙΡΕΣΙΑΣ — Τραπεζικά Συστήματα Πληροφοριών ΑΕ) — official site | shared_infrastructure_operator | credit bureau, bank-owned, credit information systems, IT suppliers, TSEK | https://www.tiresias.gr/en/about-us/ |
| high | Uni Systems — Case Studies / Projects | vendor_case_study_index | core banking, payments, public contracts, award notices, procurement | https://www.unisystems.com/case-studies |
| high | Uni Systems — News / Press | vendor_press_release_page | tenders, procurement, project_wins, framework_contracts, banking, financial_services | https://www.unisystems.com/news |
| high | Uni Systems — Newsroom | corporate_pressroom | public contracts, award notices, partnerships, treasury and payments, framework contracts | https://www.unisystems.com/news/ |
| high | Unisys — Press releases (Alpha Bank ClearPath core-banking modernization) | vendor_press_release_index | core banking, vendor wins, procurement, award notices, infrastructure | https://www.unisys.com/company/newsroom/ |
| high | Unisys — Press releases (Alpha Bank ClearPath core-banking modernization) | vendor_press_release_index | core banking, vendor wins, procurement, award notices, infrastructure | https://www.unisys.com/newsroom/ |
| high | alertdda / dda.gr — Υπηρεσία Ενημέρωσης Διαγωνισμών Δημοσίου (Investment Center / Blackbird Group) | commercial_tender_alert_aggregator | tenders, procurement, public contracts, award notices, advance notices | http://dda.gr/ |
| high | contracts.gr — Greek public procurement aggregator (per-buyer feeds) | procurement_aggregator | tenders, procurement, public contracts, award notices | https://www.contracts.gr/ |
| high | contracts.gr — Greek public procurement aggregator, CPV-indexed | third_party_aggregator | tenders, procurement, public contracts, award notices | https://www.contracts.gr/v1/cpv/code/66110000-4 |
| high | contracts.gr — third-party public-procurement aggregator | commercial_aggregator | tenders, procurement, public contracts, award notices | https://contracts.gr/ |
| high | cosmoONE / marketsite.gr — shared B2B e-procurement & e-auction platform for utilities/ΔΕΚΟ | b2b_eprocurement_platform_pointer | tenders, procurement, public contracts, e-auction | https://www.marketsite.gr/ |
| high | cosmoONE / sourceONE (SOFTONE cosmoONE) e-procurement platform — BoG e-tenders | eprocurement_platform | e-tenders, supplier registration, bid submission, vendor identity | https://www.cosmo-one.gr/en/applications/e-tenders/ |
| high | cosmoONE / sourceONE — Bank of Greece e-tender platform (Σύστημα Ηλεκτρονικών Διαγωνισμών) | eprocurement_platform_vendor | tenders, procurement | https://www.cosmo-one.gr/ |
| high | dda_alert / dda.com.gr — Public Tenders Information Service (Blackbird Group) | commercial_tender_alert_aggregator | tenders, procurement, public contracts, award notices, CPV facets | https://dda.com.gr/ |
| high | diavgeia-api — Python wrapper for the OpenData API (PyPI) | open_source_client_library | API access, collection tooling, procurement | https://pypi.org/project/diavgeia-api/ |
| high | e-ΕΦΚΑ — Διαγωνισμοί (tender index) | public_buyer_tenders_page | tenders, procurement, IT, payment_systems, pensions, contributions | https://www.e-efka.gov.gr/el/diagonismoi |
| high | egg — enter•grow•go Accelerator (Eurobank) | bank_accelerator_cohort | fintech, accelerator, vendor_discovery, payments, banking_tech | https://www.theegg.gr/en/ |
| high | eprocurement.gov.gr Act Search (Αναζήτηση Πράξεων / actSearch) | public_act_search_ui | tenders, procurement | http://www.eprocurement.gov.gr/actSearch/faces/result_search_page.jspx |
| high | et.diavgeia.gov.gr (National Printing House central Diavgeia) | mandatory_transparency_portal | tenders, procurement | https://et.diavgeia.gov.gr/search |
| high | insider.gr | business_financial_news_tech_banking | bank digital transformation, fintech, vendor selection, tech investment programmes, tender | https://www.insider.gr/ |
| high | jobfind.gr — Greek job board (IT & banking categories) | job_board_national | hiring_signals, IT_projects, banking, procurement | https://www.jobfind.gr/JobAds/it_information_technology/thessaloniki/GR/Theseis_Ergasias |
| high | netweek.gr — Banking / Finance tag (Greek IT trade media) | trade_media_topic_index | project_wins, core_banking, mobile_banking, open_banking, tenders, banking, payments | https://netweek.gr/tag/banking-finance/ |
| high | netweek.gr — Διαγωνισμοί (tenders/awards) tag | trade_press_tender_award_index | tenders, procurement, public contracts, award notices, bank IT projects, payments | https://netweek.gr/tag/%CE%B4%CE%B9%CE%B1%CE%B3%CF%89%CE%BD%CE%B9%CF%83%CE%BC%CE%BF%CE%AF/ |
| high | newmoney.gr — fintech & startups coverage (τράπεζες/deals) | financial_news_media | bank_partnership, deals, fintech_startups, funding_rounds, embedded_payments | https://www.newmoney.gr/tag/startups/ |
| high | securitymanager.gr — Greek private-security trade magazine | trade_media | market_intelligence, cash_in_transit, m_and_a, sector_news | https://www.securitymanager.gr/ |
| high | Ίδρυμα Εκτύπωσης Τραπεζογραμματίων και Αξιών (ΙΕΤΑ) — BoG Banknote Printing Works as procurer | procuring_internal_unit | tenders, procurement, public contracts, banknote handling | https://www.bankofgreece.gr/euro/nomismatokopeio-ieta/ektypwsh-trapezogrammatiwn |
| high | Α.Τ.Π.Σ.Υ.Τ. — Προκηρύξεις-Διαγωνισμοί (Bank of Greece-affiliated printing/mint entity) | affiliated_printing_mint_tender_page | tenders, procurement, public contracts, banknote printing, security printing, cash handlin | https://atpsyte.gr/el/prokiryxeis-diagonismoi |
| high | ΓΕΜΗ e-Services — Certificates & Copies of Corporate Documents (services.businessportal.gr) | official_register_document_service | corporate filings, incorporations, capital changes, subsidiaries, company register | https://services.businessportal.gr/ |
| high | Γενική Γραμματεία Εμπορίου (ΓΓΕ) — Εθνική Κεντρική Αρχή Αγορών (National Central Purchasing Authority) | central_purchasing_body_portal | central_purchasing, framework_agreements, tenders, IT_equipment, general_services | https://gge.mindev.gov.gr/tomeas-dimosion-simvaseon/ |
| high | ΔΙΑΥΓΕΙΑ — ΕΟΠΥΥ organisation feed | transparency_register_feed | public contracts, award notices, banking services, procurement, disbursement | https://app.diavgeia.gov.gr/f/eopyygov |
| high | Διαύγεια (Diavgeia) Open Data API — decision/award/payment layer | government_open_data_api | public contracts, award notices, direct awards, payments | https://diavgeia.gov.gr/api/help |
| high | Διαύγεια (Diavgeia) — Ελεγκτικό Συνέδριο / Court of Audit transparency feed | government_transparency_feed_api | procurement, pre-contractual audit, procurement disputes | https://diavgeia.gov.gr/f/elegktiko_synedrio |
| high | Ε.Β.Δ.ΔΗ.ΣΥ — Εθνική Βάση Δεδομένων Δημοσίων Συμβάσεων (National Database of Public Contracts, current portal) | national_contracts_database | procurement, statistics, contracts_data, register, monitoring | https://ppp.eadhsy.gr/ |
| high | ΕΑΔΗΣΥ / EAADHSY — Hellenic Single Public Procurement Authority (Εθνική Βάση Δεδομένων Δημοσίων Συμβάσεων) | regulator_authority_guidance | procurement, public contracts, award notices | https://eadhsy.gr/anathetouses-arches/kimdis/ |
| high | ΕΑΔΗΣΥ — Εκθέσεις (Annual reports & monitoring reports) | annual_and_monitoring_reports | procurement, statistics, monitoring, central_purchasing, trends | https://eadhsy.gr/eadisy/ektheseis/ |
| high | ΕΑΔΗΣΥ — Κατευθυντήριες Οδηγίες / announcements feed (guidance directives) | guidance_directives | procurement_rules, guidance, interpretation, legislation_changes | https://eadhsy.gr/category/eadisy/ |
| high | ΕΑΔΗΣΥ — Κατευθυντήριες Οδηγίες / Γενικές Οδηγίες (Guidelines) | regulatory_guidance | guidelines, guidance, regulation, public contracts, Law 4412 | https://eaadhsy.gr/index.php/m-foreis/m-genikes-odigies |
| high | ΕΑΔΗΣΥ — Πρότυπα Τεύχη & Υποδείγματα (standard tender templates & model documents) | standard_tender_templates | tenders, procurement_rules, templates, framework_agreements, services, supplies | https://eadhsy.gr/anathetouses-arches/protypa-tefchi-ypodeigmata/ |
| high | ΕΕΤ — Συνδεδεμένα Μέλη / HBA Associate (Connected) Members directory | association_member_directory | members, banks, actor_map, leasing, cooperative_banks | https://www.hba.gr/Association/Members?type=ConnectedMembers |
| high | ΕΟΠΥΥ — Προκηρύξεις / Διαγωνισμοί (Competitions) | public_buyer_tender_page | tenders, procurement, public contracts, award notices, payment-services, reimbursement, tr | https://eopyy.gov.gr/el/articles/competitions |
| high | ΕΣΗΔΗΣ / Προμηθεύς entry portal (esidisportal) | official_platform_home_portal | tenders, procurement, e-procurement platform, manuals, CPV | https://portal.eprocurement.gov.gr/esidisportal/ |
| high | ΕΥΔΕ-ΤΠΕ — digitalplan.gov.gr (Special Service for Management & Implementation of ICT Sector) | managing_authority_calls | tenders, funding_calls, ict, public_administration, digital_transformation | https://www.digitaltransform.gr/proskliseis-entaxeis/proskliseis/ |
| high | Ελλάδα 2.0 — Έργα (Greece 2.0 RRF Projects) | project_registry | projects, rrf_pipeline, digital_transformation, financial_infrastructure | https://greece20.gov.gr/erga/ |
| high | Ελλάδα 2.0 — Επιχειρηματική χρηματοδότηση / Δάνεια ΤΑΑ (RRF Business Financing / Loans) | programme_page | rrf_loans, banks, digital_transition, financing | https://greece20.gov.gr/en/recovery-and-resilience-facility-loans/ |
| high | Ελλάδα 2.0 — Λίστα Top 100 Τελικών Αποδεκτών (Top-100 Final Recipients of RRF Funds) | beneficiary_list | beneficiaries, rrf_recipients, transparency | https://greece20.gov.gr/en/list-of-top100-final-recipients/ |
| high | Ελληνική Αναπτυξιακή Τράπεζα (HDB) — Προκηρύξεις | public_buyer_tenders_page | tenders, procurement, IT, banking_technology | https://hdb.gr/category/prokyrikseis/ |
| high | ΗΔΙΚΑ / IDIKA (Ηλεκτρονική Διακυβέρνηση Κοινωνικής Ασφάλισης) — Διαγωνισμοί / Προμήθειες | public_it_operator_tenders_page | tenders, procurement, IT, payment_systems, pensions, contributions | https://www.idika.gr/erga/diagonismoi/ |
| high | Ημερήσια Κυκλοφορία ΦΕΚ (National Printing House — Daily Gazette feed) | gazette_daily_feed | licensing, concessions, tenders, statutory_acts | https://search.et.gr/en/daily-publications/ |
| high | ΚΗΜΔΗΣ Open Data API — Swagger UI | api_specification | tenders, procurement, public contracts | https://cerpp.eprocurement.gov.gr/khmdhs-opendata/swagger-ui/index.html |
| high | ΚΗΜΔΗΣ statistics dashboard (Central Electronic Registry contract statistics, Tableau) | statistics_dashboard | statistics, ΚΗΜΔΗΣ, public contracts, procurement data, award data | https://portal.eprocurement.gov.gr/portal_files/tableu/KHMDHS.html |
| high | ΚΗΜΔΗΣ — Κεντρικό Ηλεκτρονικό Μητρώο Δημοσίων Συμβάσεων public search (cerpp kimds2) | government_contracts_registry_search | tenders, procurement, public contracts, award notices | https://cerpp.eprocurement.gov.gr/kimds2/unprotected/searchContracts.htm?execution=e1s1 |
| high | ΚτΠ Μ.Α.Ε. — Ανακοινώσεις (Announcements / clarifications) | buyer_notice_stream | tenders, procurement, award notices, clarifications | https://www.ktpae.gr/anakoinoseis/ |
| high | Πρόγραμμα «Ψηφιακός Μετασχηματισμός» 2021-2027 (Digital Transformation Programme portal) | programme_portal | digital_transformation, espa, public_services, interoperability, funding_calls | https://www.digitaltransform.gr/ |
| high | Ταμείο Παρακαταθηκών & Δανείων (TPD/CDLF) — Προκηρύξεις / προσκλήσεις | public_buyer_tenders_page | tenders, procurement, IT, payment_systems, banking_technology | https://www.tpd.gr/prokirykseis-proskliseis/ |
| high | ΥπερΔιαύγεια (yperdiavgeia.gr) — full-text Diavgeia + KHMDIS aggregator | third_party_search_aggregator | procurement, tenders, contracts, KHMDIS cross-index, OCR full-text | https://yperdiavgeia.gr/ |
| high | Ψηφιακός Μετασχηματισμός ΜμΕ — digitalsme.gov.gr (SME digital voucher action, supplier & product registry) | vendor_product_registry | payments, e_invoicing, digital_transactions, suppliers, vendors, beneficiaries, rrf | https://digitalsme.gov.gr/ |
| medium | AADE VAT/VIES validity check (Εγκυρότητα ΑΦΜ/ΦΠΑ - VIES) | vat_validation_service | vat_validation, entity_resolution, cross_border | https://www.aade.gr/en/validity-vat-vies |
| medium | AI in Financial Services Conference (Boussias Events) | conference_sponsor_speaker_list | AI in finance, payments, banking, conference sponsors | https://aiinfinancialservices.boussiasevents.gr/ |
| medium | ATHEX Group Announcements (regulated disclosures of listed Greek IT/banking vendors) | regulated_disclosure_index | core_banking, wins, disclosures, implementations | https://www.athexgroup.gr/en/more-options/announcements |
| medium | ATHEX per-issuer announcements — Optima Bank (issuer 1510) & CrediaBank/ex-Attica Bank (issuer 50) | issuer_regulated_feed | material contracts, vendor disclosure, digital transformation | https://athens.euronext.com/en/market-data/issuers/1510 |
| medium | ATM Marketplace / Kiosk Marketplace — self-service industry trade media (Greece coverage) | trade_media | ATM deployment, vendor wins, product launches, self-service | https://www.atmmarketplace.com/ |
| medium | ATM Marketplace — Greece / bank ATM deals | trade_media | ATM, cash recycling, contract, procurement | https://www.atmmarketplace.com/topics/atm-management/ |
| medium | ATM Marketplace — vendor company showcases & Greek deal news (aggregator pointer) | trade_media_aggregator | procurement, ATM, self-service, cash-cycle | https://www.atmmarketplace.com/companies/ncr-atleos/media/ |
| medium | Aegean Baltic Bank - official site (specialist shipping-finance bank) | bank_official_site | procurement, core banking, payments, vendor selection | https://www.aegeanbalticbank.com/en |
| medium | Alpha Bank — Οι Κώδικες και οι Πολιτικές μας (Codes & Policies governance index) | governance_policy_index | corporate governance, supplier code of conduct, anti-corruption, policies | https://www.alpha.gr/el/omilos/etairiki-diakuvernisi/dioikisi/kodikes-kai-politikes |
| medium | AppsRunTheWorld - Enterprise/Fintech technology-stack customer database | technographics_aggregator_db | vendor selection, tech stack, procurement history, core banking | https://www.appsruntheworld.com/customers-database/customers/view/aegean-baltic-bank-s-a-greece |
| medium | Athens Chamber of Commerce & Industry - GEMI service (ACCI, acci.gr) | chamber_gemi_service | company_registry, announcements, chamber_membership, pointer | https://acci.gr/gemi/ |
| medium | Bank of Greece - Regulatory sandbox (FinTech) | regulator_program_page | fintech, regulatory sandbox, innovation, payments | https://www.bankofgreece.gr/en/main-tasks/supervision/regulatory-sandbox |
| medium | Bank of Greece — TARGET services / Payments in TARGET (TARGET-GR operator page) | regulator_infrastructure_operator | TARGET, TARGET-GR, RTGS, large-value payments, settlement | https://www.bankofgreece.gr/en/main-tasks/payment-systems-and-settlements/target-services |
| medium | Bank of Greece — legacy Tender Invitations archive (AllItems.aspx?Filter_by=TI) | procurement_notice_archive | tenders, procurement, IT, software, banknotes | https://www.bankofgreece.gr/Pages/el/Bank/News/TenderInvitation/AllItems.aspx?Filter_by=TI |
| medium | BusinessNews.gr — Banks section | business_financial_press | banking, payments, vendor wins | https://www.businessnews.gr/epixeiriseis/trapezes |
| medium | BusinessNews.gr — Greek business/technology trade press (Επιχειρήσεις/Τεχνολογία) | trade_press | vendor_signals, award_notices, procurement, public_contracts | https://www.businessnews.gr/epixeiriseis/texnologia |
| medium | BusinessWire — NCR Atleos / vendor press-release distribution | press_wire_distributor | ATM, deployment, public contracts, award notices | https://www.businesswire.com/ |
| medium | Byte (IDEAL Holdings) — News & Press releases | vendor_pressroom | tenders, procurement, public contracts, award notices, system integrator | https://www.byte.gr/category/news-releases-en/ |
| medium | Byte Computer — corporate site (partnerships, maintenance contracts, projects) | corporate_site_projects_partnerships | public contracts, award notices, partnerships, maintenance contracts | https://www.byte.gr/en/ |
| medium | COSMOTE Business / OTE Group — banking IT solutions & press | vendor_banking_vertical_site | tenders, procurement, award notices, managed services, data center, channels, system integ | https://www.cosmote.gr/hub/business/hubPageBusinessOptionType.jsp?businessOptionType=Bank |
| medium | Coface Greece — commercial company & financial-report provider (GEMI-sourced) | commercial_business_information_provider | financial statements, ownership, credit rating | https://www.coface.com/ |
| medium | Cooperative Bank of Chania — official website | bank_website | cooperative_bank, AML, digital_banking, payments | https://www.chaniabank.gr/ |
| medium | Credit Servicing Firms register (Εταιρείες Διαχείρισης Απαιτήσεων από Δάνεια και Πιστώσεις) | regulator_register_file | credit servicers, NPL, διαχείριση απαιτήσεων, register | https://www.bankofgreece.gr/RelatedDocuments/14_Credit_Servicing_Firms.xlsx |
| medium | DEiXTo ΚΗΜΔΗΣ Web API (eprocurement scraper) | third_party_procurement_scraper_api | tenders, procurement, public contracts, award notices | https://deixto.com/blog/2015/04/20/web-api-eprocurement-gov-gr/ |
| medium | DIGIWHIST / Datlab Tenders API (govtransparency.eu) | research_procurement_dataset_api | tenders, procurement, public contracts, award notices | https://digiwhist.docs.apiary.io/ |
| medium | Data Journalists (datajournalists.co.uk) — KIMDIS direct-awards investigations | investigative_journalism | contract_awards, vendors, direct_awards, analysis | https://www.datajournalists.co.uk/?lang=en |
| medium | Diavgeia (Δι@ύγεια) — ELTA feed | transparency_register_feed | procurement, contract_awards, payment_systems | https://diavgeia.gov.gr/f/elta |
| medium | Diavgeia AI (diavgeia-ai.gr) — independent Diavgeia + ΚΗΜΔΗΣ search/analysis tool | third_party_aggregator_search | procurement, public contracts, award notices, direct awards, contracts | https://diavgeia-ai.gr/ |
| medium | Diavgeia AI — independent ΚΗΜΔΗΣ/Diavgeia analytics search | third_party_procurement_search | public contracts, award notices, procurement | https://diavgeia-ai.gr/en/khmdhs |
| medium | EADHSY (Ενιαία Αρχή Δημοσίων Συμβάσεων) — own Procurement page (ΠΡΟΜΗΘΕΙΕΣ) | authority_procurement_page | tenders, procurement, public contracts | https://eadhsy.gr/eadisy/promitheies/ |
| medium | EBA — Registers and other lists of institutions (hub) | portal_index | registers, lists, supervision, documentation | https://www.eba.europa.eu/risk-and-data-analysis/data/registers-and-other-list-institutions |
| medium | EBRD Procurement Notices & ECEPP (Client eProcurement Portal) | institution_procurement_page | tenders, procurement | https://www.ebrd.com/work-with-us/procurement/notices.html |
| medium | ECB Electronic Tendering System (e-sourcing supplier portal) | e_tendering_platform | tenders, procurement | https://www.ecb.europa.eu/ecb/jobsproc/sourcing/html/index.en.html |
| medium | EIF — Procurement (European Investment Fund) | institution_procurement_page | tenders, procurement | https://www.eif.org/work-with-us/procurement/overview |
| medium | EOPYY cash-management / treasury RFP (ταμειακή διαχείριση) | tender_document_award | tenders, procurement | https://eopyy.gov.gr/ |
| medium | EPSILON NET Group - Epsilon Pay (embedded banking with NBG) | vendor_product_reference_page | embedded banking/payments, collections software, bank-fintech partnership, vendor customer | https://epsilonnet.gr/en/products/epsilon-pay/ |
| medium | ESPA 2021-2027 — Προσκλήσεις/Διακηρύξεις & Digital Transformation programme | programme_procurement_listing | ESPA, digital transformation, procurement, co-funded programmes | https://www.espa.gr/el/Pages/Proclamations.aspx |
| medium | EU Funding & Tenders Portal — calls for tenders (SEDIA) | eu_calls_for_tenders_portal | tenders, procurement, financial IT, payments | https://ec.europa.eu/info/funding-tenders/opportunities/portal/screen/opportunities/calls-for-tenders |
| medium | EU Public Procurement Data Space (PPDS) - dashboards | eu_procurement_analytics_platform | tenders, procurement, public contracts, award notices | https://www.public-procurement-data-space.europa.eu/en/dashboards |
| medium | EY Greece — Banking & Capital Markets insights | consultancy_insight_hub | payments, procurement, core banking | https://www.ey.com/en_gr/banking-capital-markets-transformation-growth |
| medium | Easy Diavgeia (easydiavgeia.gr) — full-text search + email alerts | third_party_search_monitoring | procurement monitoring, full-text search, alerts, tenders | https://easydiavgeia.gr/ |
| medium | Euro2day.gr — banking & technology coverage | business_daily | banking, digital banking, technology, finance, vendor deals | https://www.euro2day.gr/ |
| medium | Euronext Athens — Company Prospectuses / Informative Material (Ενημερωτικά Δελτία) | prospectus_informative_material | capex, capital raise, material contracts, regulated information | https://athens.euronext.com/en/market-data/issuers/278/informative-material |
| medium | Europe: Tenders Electronic Daily (OpenTender) OCDS publication | ocds_bulk_dataset | tenders, procurement, public contracts, award notices | https://data.open-contracting.org/en/publication/150 |
| medium | European Commission — Recovery and Resilience Scoreboard (Greece) | eu_transparency_dashboard | rrf_scoreboard, milestones, disbursements, digital, eu_data | https://ec.europa.eu/economy_finance/recovery-and-resilience-scoreboard/country_overview.html?country=Greece |
| medium | FinTech Futures — Branches & ATMs vertical | trade_press | ATM, deployment, public contracts | https://www.fintechfutures.com/bankingtech/branches-atms |
| medium | FinTech Futures — banking-technology vendor news | trade_press | vendor_signals, award_notices, procurement | https://www.fintechfutures.com/ |
| medium | Finastra — Customer Stories / Success Stories index | vendor_customer_reference_index | public contracts, award notices | https://www.finastra.com/customer-experience/success-stories |
| medium | Forbes Greece (forbesgreece.gr) | business_magazine_tech_profiles | fintech vendors, IT market moves, company profiles, neobank tech | https://www.forbesgreece.gr/ |
| medium | GSIS — Στοιχεία Νομικού Προσώπου από το ΓΕΜΗ (Taxisnet/KED web service for GEMI legal-entity data) | official_registry_api | vendor entity resolution, ownership | https://www.gsis.gr/en/public-administration/ked/web-services/gemh |
| medium | Grant Thornton Greece — Financial Services / Digital Transformation Hub | advisory_firm_industry_hub | banking, digital transformation, branch banking, finance transformation, DORA / operationa | https://www.grant-thornton.gr/en/insights/digital-transformation-hub/ |
| medium | Greek financial media re-publication of vendor announcements (Mikrometoxos / alphanews / Capital / Insider / BusinessNews) | local_media_mirror | core_banking, payments, wins, digital_transformation | https://www.mikrometoxos.gr/ |
| medium | Greek financial/business press — Cashflex / Piraeus off-site ATM sale coverage | financial_press | off-site ATM network, ATM procurement, Printec, Cashflex, Piraeus Bank, fleet size | https://www.ot.gr/2025/07/19/epixeiriseis/cashflex-neo-diktyo-atm-me-anaptyksi-se-oli-tin-ellada/ |
| medium | Growthfund / Hellenic Corporation of Assets & Participations (EESYP/Υπερταμείο) — ELTA & port holdings | state_owner_portfolio | procurement, payments, financial services, public contracts | https://growthfund.gr/sector/tachydromikes-ypiresies/elta/ |
| medium | Hellenic Bank Association (HBA) — Events / Under-the-aegis listing | association_events_patronage_index | banking, conference index, regulatory, patronage, speakers | https://www.hba.gr/events/list |
| medium | Hellenic Capital Market Commission — Investment Services Providers register (Πάροχοι Επενδυτικών Υπηρεσιών, ΑΕΠΕΥ / crowdfunding / CASP) | regulator_register_index | investment_firms, crowdfunding, crypto_asset_service_providers, authorised_institution_lis | http://www.hcmc.gr/el/parohoiepey |
| medium | Hellenic MoD (ΥΠΕΘΑ) Procurement Notices — Προκηρύξεις | buyer_procurement_portal | tenders, procurement, public contracts, banking services, treasury | https://www.mod.mil.gr/category/prokiryxeis/ |
| medium | IBS Intelligence — banking-tech trade press (vendor-win news) | trade_press_aggregator | public contracts, award notices | https://ibsintelligence.com/?s=greece+bank |
| medium | ICLG - Public Procurement Laws and Regulations: Greece | legal_guide_country_chapter | bid protests, appeal decisions, procurement, public contracts | https://iclg.com/practice-areas/public-procurement-laws-and-regulations/greece |
| medium | ITSecurityPro (Smart Press) — banking cybersecurity & DORA coverage | trade_it_media | cybersecurity, banking security, DORA, IT governance, vendor deals | https://www.itsecuritypro.gr/ |
| medium | InfoCom.gr | specialised_ict_business_news | ICT business news, bank IT projects, vendor contracts, conferences | https://infocom.gr/ |
| medium | Infosys Finacle — client references / press (NBG 'Cosmos') | vendor_customer_reference | vendor selection, core banking, award notices | https://www.finacle.com/ |
| medium | Insider.gr — ΕΕΣΥΠ / Υπερταμείο news tag | financial_news_outlet | divestment, advisory, governance, award notices | https://www.insider.gr/oikonomia |
| medium | KPMG Greece — Banking / Πιστωτικά Ιδρύματα (industry page) | advisory_firm_industry_hub | banking, financial risk management, regulatory compliance, digital transformation | https://kpmg.com/gr/el/home/industries/banking.html |
| medium | KTPAE (Information Society SA) — main site & projects index | implementing_body_index | tenders, procurement, public contracts, IT systems | https://www.ktpae.gr/ |
| medium | Marathon Venture Capital — blog (Greek funding rounds & exits) | vc_blog_funding_roundup | funding_rounds, exits, fintech_startups, investors | https://marathon.vc/blog/greek-startups-funding-rounds-and-exits-2024 |
| medium | Mercell / EU-Supply — European procurement platform (Greece coverage) | commercial_tender_platform_aggregator | tenders, procurement, public contracts, award notices | https://www.mercell.com/en/ |
| medium | Mercell — Tender Discovery / Monitoring (Greece via TED + national portals) | commercial_tender_alert_aggregator_international | tenders, procurement, CPV_filtering, EU_TED, monitoring | https://info.mercell.com/en/for-suppliers/tender-discovery/ |
| medium | NBG (Εθνική Τράπεζα) — ESG Reports index (sustainability reports; supplier/procurement chapter) | sustainability_report_index | procurement, supplier evaluation, ESG, responsible procurement | https://www.nbg.gr/el/omilos/esg |
| medium | NBG (Εθνική Τράπεζα) — ESG Reports index (sustainability reports; supplier/procurement chapter) | sustainability_report_index | procurement, supplier evaluation, ESG, responsible procurement | https://www.nbg.gr/el/omilos/esg/orama-stratigiki/esg-reports-and-data |
| medium | NETinfo — digital-banking vendor (Optima Bank Greece deployment) | vendor_customer_reference_index | public contracts, award notices | https://www.netinfo.eu/ |
| medium | National Bank of Greece (NBG) — Corporate Governance / ESG governance page | bank_first_party_governance_supplier_reference | procurement, supplier governance, ESG | https://www.nbg.gr/en/group/esg/vision-strategy |
| medium | National Bank of Greece (NBG) — ESG / Sustainability hub (supplier & responsible-procurement disclosures) | esg_procurement_disclosure_hub | procurement, suppliers, esg, governance | https://www.nbg.gr/en/group/esg |
| medium | NetFAX (netfax.gr) | specialised_it_trade_press_bulletin | IT/telecom news, exclusive scoops, bank IT deals, vendor moves | https://www.netfax.gr/ |
| medium | Netcompany-Intrasoft — careers (systems integrator) | vendor_career_page | hiring_weak_signal, vendor_staffing, bank_platform_delivery, procurement | https://netcompany.com/careers/greece/vacancies/ |
| medium | Netcompany-Intrasoft — early-careers / vacancies (Greece SI) | system_integrator_careers_portal | hiring_signals, core_banking, payments, IT_projects, vendor_management | https://www.netcompany-intrasoft.com/talent/early-careers |
| medium | Nomotelia - legal database (procurement case law) | legal_case_aggregator | bid protests, appeal decisions, audit findings, public contracts | https://www.nomotelia.gr/ |
| medium | OTE/COSMOTE — company procurement announcements (OTE Group) | buyer_corporate_site | tenders, procurement, e-billing, payment collection | https://www.cosmote.gr/ |
| medium | Oikonomikos Tachydromos (ot.gr) — banks/enterprises fintech coverage | financial_media | banks, fintech, MoUs, acquisitions, innovation, payments | https://www.ot.gr/ |
| medium | OpenCorporates - Greece (GEMI) dataset | open_company_data_aggregator | company_data, entity_resolution, cross_border, api, pointer | https://opencorporates.com/registers/88 |
| medium | Opentender.eu (DIGIWHIST / Government Transparency Institute) — TED data aggregator | aggregator_open_data | procurement, open data, awards, vendor analytics | https://opentender.eu/ |
| medium | Optima Bank — Careers (θέσεις εργασίας) | employer_career_portal | hiring_signals, core banking, payments, IT | https://www.optimabank.gr/about-us/human-resources/theseis-ergasias/ |
| medium | Optima Bank — Investor Relations & Announcements | bank_investor_relations | vendor selection, digital banking, payments, award notices | https://www.optimabank.gr/en/about-us/investor-relations |
| medium | Oracle Financial Services (FLEXCUBE) — Customer stories / press | vendor_product_customer_page | core banking, vendor wins, procurement | https://www.oracle.com/financial-services/banking/flexcube/ |
| medium | PPF — Public Participation Fund (Ταμείο Δημοσίων Συμμετοχών), Growthfund subsidiary | official_agency_subsite | procurement, tenders, public contracts, divestment | https://ppf.growthfund.gr/ |
| medium | PPP Unit (Ειδική Γραμματεία ΣΔΙΤ) — Ministry of National Economy & Finance | ppp_authority_pointer_to_gazette | PPP, concessions, procurement | https://pppunit.minfin.gov.gr/ |
| medium | PR Newswire — vendor ATM/self-service contract press releases (GR) | press_wire | contracts, award_notices, atm, self-service | https://www.prnewswire.com/ |
| medium | Performance Technologies — Company News | vendor_press_release_page | project_wins, public_sector_it, partnerships, banking, financial_services | https://www.performance.gr/category/company-news/ |
| medium | Performance Technologies — corporate site & partner case stories (Alpha Bank core banking) | corporate_site_case_stories | public contracts, core banking, cloud migration, project wins | https://www.performance.gr/ |
| medium | Piraeus Bank Coupa Supplier Portal (vendor registration/login endpoint) | supplier_portal_login | procurement, vendor registration, RFP, e-sourcing | https://supplier.coupahost.com/sessions/new |
| medium | Piraeus Financial Holdings — press office / news announcements | bank_press_room | contracts, estate_transfer, atm, self-service | https://www.piraeusholdings.gr/en/press-office/news-announcements/ |
| medium | Prevedourou.gr - academic commentary on procurement remedies (Ευγενία Πρεβεδούρου) | academic_legal_commentary | bid protests, appeal decisions, audit findings, public contracts, procurement | https://www.prevedourou.gr/ |
| medium | Printec Group - Solutions & Country (Greece) pages | vendor_solution_and_reference_page | ATM/self-service, payments software, vendor customer references, procurement outcomes | https://www.printecgroup.com/country/printec-greece-en/ |
| medium | Profile Software Newsroom (Finuevo / Acumen) | vendor_pressroom | core_banking, wealth, treasury, wins | https://www.profilesw.com/news-events/ |
| medium | Profile Software — Insights / case studies (Finuevo Core & Suite banking implementations) | vendor_case_studies | core banking, treasury, case studies, implementation wins | https://www.profilesw.com/insights/ |
| medium | Project Management Awards (PMI Greece + BOUSSIAS + NetFax/netweek) | industry_awards_program | business transformation, banking, GRC, digital modernisation, cyber security | https://projectmanagementawards.boussiasevents.gr/ |
| medium | Promitheies.gr — Greek public-tender aggregator | commercial_tender_aggregator | tender aggregation, ESIDIS, KIMDIS, Diavgeia, TED, IT, banking | https://www.promitheies.gr/branch/eprocurement-esidis-kimdis |
| medium | Public Procurement Data Space (PPDS) - data.europa.eu | procurement_data_platform | tenders, procurement, public contracts, award notices | https://data.europa.eu/en/PPDS |
| medium | Public Procurement Data Space (PPDS) — dedicated portal & dashboards | analytical_data_space_dashboards | tenders, procurement, public contracts, award notices | https://www.public-procurement-data-space.europa.eu/en |
| medium | QUALCO Group - Solutions / Credit & Loan Management | vendor_solution_and_reference_page | loan/NPL management software, credit management, vendor customer references | https://www.qualco.eu/systems |
| medium | Qualco — News (Greek bank / financial-services projects) | vendor_press_release_feed | public contracts, award notices, procurement | https://blog.qualco.eu/news |
| medium | Randstad Greece — banking jobs listings | staffing_recruiter_board | hiring_signals, banking, IT_projects, procurement | https://www.randstad.gr/theseis-ergasias/q-banking/ |
| medium | Real Consulting — Financial & Services industry page | vendor_banking_vertical_site | tenders, procurement, award notices, enterprise applications, system integrator | https://www.realconsulting.gr/industries/financial-services |
| medium | SAP Greece Newsroom (Αίθουσα Τύπου) — integrator/bank project announcements | platform_vendor_pressroom | tenders, procurement, award notices, enterprise applications, system integrator | https://news.sap.com/greece/ |
| medium | SEPE — website / news & press (sepe.gr) | industry_association_news | procurement, public contracts | https://www.sepe.gr/ |
| medium | SEV members_news - member-vendor banking announcements (aggregator) | association_member_news_aggregator | vendor announcements, banking IT projects, pointer index | https://www.sev.org.gr/enimerosi?katigories=members_news |
| medium | SEV members_news - member-vendor banking announcements (aggregator) | association_member_news_aggregator | vendor announcements, banking IT projects, pointer index | https://www.sev.org.gr/nea-melwn/ |
| medium | Space Hellas — ATHEX / stock-exchange market announcements (ΣΠΕΙΣ) | regulated_market_disclosure_aggregator | public contracts, award notices, material contract disclosures | https://www.capital.gr/finance/announcements/%CE%A3%CE%A0%CE%95%CE%99%CE%A3 |
| medium | Startupper.gr — deals & fintech news (Greek startup ecosystem tracker) | startup_media_deal_tracker | startups, fintech, bank partnership, accelerator cohorts, deals, payments | https://startupper.gr/ |
| medium | TED CSV subset dataset (data.europa.eu) | open_data_dataset | tenders, procurement | https://data.europa.eu/data/datasets/ted-csv?locale=en |
| medium | TED RSS feeds + saved-search email alerts | feed_and_alert_service | tenders, procurement, public contracts, award notices | https://ted.europa.eu/en/simap/rss-feed |
| medium | Teiresias TSEK — Balance Sheets & GEMI Announcements (business.tiresias.gr) | commercial_financial_aggregator | company financial statements, GEMI announcements, sector indices, balance sheets | https://business.tiresias.gr/home/proionta-ypiresies/tsek-platforma/financial-data/ |
| medium | Tender by D Plan (tender.dplan.gr) | commercial_tender_aggregator | tenders, procurement, public contracts, award notices | https://tender.dplan.gr/ |
| medium | TendersInfo — Greece IT & BFIS (Banking/Finance/Insurance) Tenders | commercial_tender_alert_aggregator_international | tenders, procurement, IT, banking, finance, insurance, CPV_filtering | https://www.tendersinfo.com/global-greece-tenders.php |
| medium | The Wealth Mosaic — Profile Software vendor profile & news mirror | vendor_directory_mirror | public contracts, award notices | https://www.thewealthmosaic.com/vendors/profile-software/ |
| medium | Uni Systems — careers (banking systems integrator) | vendor_career_page | hiring_weak_signal, vendor_staffing, bank_platform_delivery, digital_transformation | https://www.unisystems.com/careers |
| medium | akep.gr - Διαγωνισμοί, Προμήθειες, Προκηρύξεις Δημοσίου | commercial_tender_aggregator | tenders, procurement, public contracts | https://www.akep.gr/ |
| medium | apps.interconsult.gr — ΚΗΜΔΗΣ OpenData search (third-party front-end) | third_party_api_frontend | procurement, public contracts, award notices | https://apps.interconsult.gr/ |
| medium | bankingnews.gr — δελτία τύπου (press-release republishing) | trade_press_pointer | award notices, public contracts, payments, procurement | https://www.bankingnews.gr/deltia-typou |
| medium | biztech.gr — business technology news | business_tech_trade_press | procurement, public contracts | https://biztech.gr/ |
| medium | businessdataguide — Greece GEMI Registry API reference | third_party_api_documentation | api_spec, company_register, officials, capital, rate_limits, entity_resolution | https://www.businessdataguide.com/api-directory/greece-registry-api |
| medium | capital.gr — company news / χρηματιστηριακές ανακοινώσεις (integrators) | financial_media_aggregator | tenders, procurement, public contracts, award notices, project wins, system integrator | https://www.capital.gr/finance/news/%CE%92%CE%A5%CE%A4%CE%95 |
| medium | contracts.gr — per-buyer procurement pages (aggregator) | commercial_tender_aggregator | tenders, procurement, contract_awards | https://www.contracts.gr/v1/orgs/99221150 |
| medium | cosmoONE (SOFTONE) — e-procurement platform home / client index | vendor_client_index | e-procurement, e-tenders, supplier onboarding, tender aggregation | https://www.cosmo-one.gr/en/ |
| medium | data.europa.eu — TED public procurement notices dataset (XML) & CSV subset | open_data_portal_dataset | tenders, procurement, public contracts, award notices | https://data.europa.eu/data/datasets/ted-1?locale=en |
| medium | data.gov.gr — national open-data catalogue (public contracts datasets) | open_data_catalogue | procurement, public contracts, open data | https://data.gov.gr/dataset/ |
| medium | data.gov.gr — ΕΣΗΔΗΣ open dataset (structured public-contracts data) | open_data_dataset | open_data, e_procurement, contracts_data, statistics | https://data.gov.gr/data-service/khmahe-api |
| medium | dgMarket — Greece tenders & contract awards | commercial_tender_award_aggregator | tenders, procurement, public contracts, award notices | https://www.dgmarket.com/tenders/list.do?locationISO=gr&sub=tenders-in-Greece |
| medium | e-EFKA procurement notices (Περιλήψεις Διακηρύξεων Διαγωνισμών) | buyer_procurement_page | tenders, procurement | https://www.efka.gov.gr/el/diagonismoi/perilepseis-diakeryxeon-diagonismon |
| medium | e-dimos.gr — Νομολογία ΕΑΔΗΣΥ (πρώην ΑΕΠΠ) free jurisprudence index | third_party_jurisprudence_aggregator_free | procurement, pre-contractual appeals, procurement disputes, IT contracts | https://www.e-dimos.gr/nomologia_all.php?nomologiacatid=2 |
| medium | enaon EDA (ΕΔΑ Αττικής / ΕΔΑ ΘΕΣΣ / ΔΕΔΑ merged) — Διαγωνισμοί / gas distribution tenders | buyer_eprocurement_portal | tenders, procurement, public contracts, collection | https://www.edathess.gr/diagwnismoi/ |
| medium | energypress.gr — Greek energy-sector trade press (tender coverage) | trade_press | tenders, procurement, award notices | https://energypress.gr/ |
| medium | ergolhpths.gr — Public Procurement Monitoring (built by iSmart) | commercial_tender_alert_aggregator | tenders, procurement, CPV_filtering, competitor_analysis, IT, services | https://ergolhpths.gr/ |
| medium | et.diavgeia.gov.gr — legislation & per-organization act feeds | government_transparency_act_repository | procurement, award notices, public contracts | https://et.diavgeia.gov.gr/ |
| medium | ethosEVENTS — finance/banking events & awards portfolio (meta-pointer) | event_organizer_index | conferences, awards, meta-pointer, banking, finance | https://ethosevents.eu/en/ |
| medium | euro2day.gr — market announcements & ICT project coverage | financial_press_aggregator | public contracts, award notices, market disclosures, consortia | https://www.euro2day.gr/market_announcements/announcements.html |
| medium | gov.gr — HSPPA / national procurement help index (English + Greek) | government_gateway_index | procurement, public contracts, tenders | https://www.gov.gr/en/sdg/public-contracts/participating-in-public-tenders/national-sources-of-help-with-procurement-procedures/hellenic-single-public-procurement-authority-hsppa |
| medium | iSupplies — Electronic Tenders Platform (iSmart P.C.) | private_sector_etender_platform | tenders, procurement, private_RFQ, IT | https://isupplies.gr/ |
| medium | kratikes-promitheies.gr — Προκηρύξεις / Προμήθειες δημόσιων διαγωνισμών | commercial_tender_aggregator | tenders, procurement, public contracts, award notices | https://www.kratikes-promitheies.gr/ |
| medium | newmoney.gr — Profile Software tag / Greek business-tech news | local_financial_news_aggregator | procurement, core banking, digital banking | https://www.newmoney.gr/tag/profile-software/ |
| medium | promitheies.gr — Greek tender aggregator (TED section) | commercial_tender_aggregator | tenders, procurement, banking, payments | https://www.promitheies.gr/branch/ted |
| medium | ΓΓΠΣΨΔ / GSIS — General Secretariat of Information Systems & Digital Governance (procurement) | public_buyer_operator_own_notice_page | tenders, IT, e-government, software maintenance, payments infrastructure | https://www.gsis.gr/ |
| medium | ΓΕΜΗ Commercial Activity Codes (ΚΑΔ) checker (commercial-activity-codes.businessportal.gr) | official_classification_lookup | activity codes, company register, incorporations | https://commercial-activity-codes.businessportal.gr/ |
| medium | Γενική Γραμματεία Εμπορίου — Θεσμικό Πλαίσιο Δημοσίων Συμβάσεων | ministry_procurement_framework_hub | procurement, procurement law, public contracts, ministerial decisions | https://gge.mindev.gov.gr/tomeas-dimosion-simvaseon/thesmiko-plaisio-dimosion-symvaseon/ |
| medium | Γενική Γραμματεία Συντονισμού / RRF Coordination Agency (GSCO) — RRP Reforms | coordination_agency | reforms, rrf_governance, coordination, milestones | https://gsco.gov.gr/rrp-reforms/ |
| medium | ΔΕΔΔΗΕ (HEDNO) — Distribution System Operator procurement & bill-collection | utility_procurement_portal | tenders, procurement, public contracts | https://www.deddie.gr/ |
| medium | ΕΑΔΗΣΥ organization on data.gov.gr (open datasets) | open_data_catalog | open data, legislation monitoring, opinions, Law 4412 | https://data.gov.gr/el/organization/eadhsy |
| medium | ΕΑΔΗΣΥ — Μηχανή αναζήτησης Ν.4412/2016 (Law 4412/2016 search engine / consolidated text) | legislation_reference_tool | procurement_rules, legislation, law_4412, reference | https://eadhsy.gr/n4412/ |
| medium | ΕΕΤ — Εκδόσεις (Publications: Deltion bulletin, studies, textbooks) | association_publications | publications, bulletin, studies, banking_system_overview | https://www.hba.gr/Publications |
| medium | ΕΚΑΠΥ — Εθνική Κεντρική Αρχή Προμηθειών Υγείας (National Central Authority for Health Procurement) | central_purchasing_body | central purchasing, framework agreements, tenders, procurement, public contracts | https://ekapy.gov.gr/tenders/ |
| medium | ΕΚΑΠΥ — Εθνική Κεντρική Αρχή Προμηθειών Υγείας (National Central Health Procurement Authority) | sectoral_central_purchasing_body | central_purchasing, health_sector, framework_agreements, e_procurement_system | https://ekapy.gov.gr/ |
| medium | ΕΣΗΔΗΣ Δημόσια Έργα — public-works tender search (pwgopendata) | government_eprocurement_tender_search | tenders, procurement, public contracts, award notices | https://pwgopendata.eprocurement.gov.gr/actSearchErgwn/faces/active_search_main.jspx |
| medium | ΕΣΗΔΗΣ Προμήθειες & Υπηρεσίες — Authenticated tendering subsystem (NEPPS) | transactional_tender_system | tenders, procurement, public contracts, award notices | https://nepps.eprocurement.gov.gr/ |
| medium | ΕΣΗΔΗΣ — Στατιστικά Δημοσίων Συμβάσεων (public statistics/dashboards) | government_procurement_statistics | procurement, public contracts | https://portal.eprocurement.gov.gr/webcenter/portal/TestPortal/pages_statistics1 |
| medium | Ελληνική Αναπτυξιακή Τράπεζα (Hellenic Development Bank, HDB) — RRF/cohesion financial-instrument programmes | national_promotional_bank | financing, beneficiaries, financial inclusion, rrf, cohesion | https://hdb.gr/en/ |
| medium | Ελληνική Αστυνομία (Hellenic Police) — BoG security/cash-escort personnel tenders | co_publishing_authority | tenders, procurement, public contracts | https://www.astynomia.gr/2025/12/09/9-12-2025-prokiryxi-diagonismou-proslipsis-idioton-gia-tis-anagkes-asfaleias-i-frourisis-ton-egkatastaseon-i-choron-tis-trapezas-tis-ellados-kathos-kai-gia-ti-synodeia-chrimatapostolon-aftis/ |
| medium | ΙΣΟΚΡΑΤΗΣ / dsanet.gr — Τράπεζα Νομικών Πληροφοριών (Athens Bar legal information bank) | third_party_legal_database | procurement, pre-contractual appeals, jurisprudence, administrative court decisions | https://www.dsanet.gr/ |
| medium | ΚτΠ Μ.Α.Ε. — Δελτία Τύπου / Γραφείο Τύπου (Press releases) | buyer_press_office | procurement, e-government, programme announcements | https://www.ktpae.gr/deltia-typou/ |
| medium | Νομισματοκοπείο (Mint) of the Bank of Greece — coin/medal procurer | procuring_internal_unit | tenders, procurement, public contracts | https://www.bankofgreece.gr/trapeza/dioikisi-domi/organogramma/nomismatokopeio |
| medium | ΟΛΘ / Thessaloniki Port Authority (ThPA) — Προκηρύξεις Διαγωνισμών | buyer_eprocurement_portal | tenders, procurement, public contracts | https://www.thpa.gr/index.php?Itemid=1314&id=80&lang=el&option=com_content&view=category |
| medium | ΟΠΣ (OPS) — Integrated Information System for EU-funded programmes (ops.gr) | eu_funded_programme_management_system | procurement, financial IT, EU-funded, payments | https://ops.gr/ |
| medium | Οδηγός του Πολίτη — ΦΕΚ Τεύχος Διακηρύξεων Δημοσίων Συμβάσεων tag feed | civic_gazette_aggregator | tenders, procurement, public contracts, award notices | https://www.odigostoupoliti.eu/tag/fek-tefchos-diakirixeon-dimosion-simvaseon/ |
| medium | ΣΕΠΕ (SEPE) — Association of ICT Companies of Greece, news | industry_association_news | digital transformation, bank IT projects, vendor partnerships, procurement | https://www.sepe.gr/gr/information/news/ |
| medium | Υπουργείο Ανάπτυξης — Πράσινες / Κεντρικές Δημόσιες Συμβάσεις & συμφωνίες-πλαίσιο ΕΚΑΑ (mindev.gov.gr) | ministry_framework_agreements_index | framework agreements, central purchasing, procurement, public contracts | https://www.mindev.gov.gr/%CF%80%CF%81%CE%AC%CF%83%CE%B9%CE%BD%CE%B5%CF%82-%CE%B4%CE%B7%CE%BC%CF%8C%CF%83%CE%B9%CE%B5%CF%82-%CF%83%CF%85%CE%BC%CE%B2%CE%AC%CF%83%CE%B5%CE%B9%CF%82/ |
| medium | Υπουργείο Ψηφιακής Διακυβέρνησης (mindigital.gr) — decisions & inclusion acts | parent_ministry | e-government, procurement, payments, policy | https://www.mindigital.gr/ |
| low | Aetoliki Pisti — Credit Cooperative of Aetoloakarnania (Αιτωλική Πίστη) — site incl. News/Announcements | credit_cooperative_site | announcements, payments, services, vendor_signals | https://aitpisti.gr/ |
| low | Bank of Greece - Anti-money laundering supervision (Πρόληψη ξεπλύματος χρήματος) | regulator_rules_page | AML, ξέπλυμα χρήματος, CFT, compliance | https://www.bankofgreece.gr/kiries-leitourgies/epopteia/prolhpsh-kseplymatos-xrhmatos |
| low | Bank of Greece — Digital euro information page (national mirror of ECB programme) | national_central_bank_page | digital euro, Eurosystem, national implementation | https://www.bankofgreece.gr/euro/pshfiako-euro |
| low | Bank of Karditsa / Cooperative Bank of Central Macedonia — cooperative-bank sites | cooperative_bank_press | vendor selection, digital banking, payments | https://www.bankofkarditsa.com.gr/ |
| low | BidDetail - Greece tenders & awards | commercial_tender_aggregator | tenders, procurement, award notices | https://www.biddetail.com/greece-tenders |
| low | Byte (Byte Computer / Byte Group) - corporate site & press | vendor_corporate_and_press_page | system integration, banking IT projects, vendor references | https://www.byte.gr/ |
| low | Careerjet.gr — job aggregator (Greece) | job_meta_aggregator | hiring_signals, banking, payments | https://www.careerjet.gr/ |
| low | Corporate News (corporatenews.gr) | business_news_banks_beat | banks, corporate strategy, tech/insurance deals | https://www.corporatenews.gr/ |
| low | Crowdpolicy — banks & fintech solutions / events (ecosystem orchestrator) | vendor_ecosystem_organiser | fintech, banks, hackathons, digital transformation, Fintech Meetup, cluster | https://www.crowdpolicy.com/el/lyseis-gia-trapezes/ |
| low | Deloitte Greece — Financial Services / Banking | consultancy_insight_hub | procurement, payments | https://www.deloitte.com/gr/en/Industries/financial-services.html |
| low | Dimosioi Diagonismoi - remedies practitioner portal (Δημόσιοι Διαγωνισμοί) | procurement_practitioner_portal | bid protests, appeal decisions, procurement, tenders | https://www.dimosioidiagonismoi.gr/prodikastiki-prosphigi/ |
| low | EADHSY - Hellenic Single Public Procurement Authority (national bridge to TED) | national_procurement_authority | tenders, procurement, public contracts | https://eadhsy.gr/en/home/ |
| low | Entersoft — Investor Announcements / News | issuer_regulated_disclosure_page | project_wins, erp, corporate_actions, financial_services | https://www.entersoft.eu/financials/ |
| low | Eventora — Greek event registration platform (payments/banking event pages) | event_platform_listing | payments, conference agenda, speakers, registration platform | https://www.eventora.com/en/Events/payments360-2026 |
| low | FinancialReport.gr — Υπερταμείο tenders investigative coverage | financial_news_outlet | tenders, procurement, public contracts, award notices | https://www.financialreport.gr/ |
| low | GEETHA — Hellenic National Defence General Staff — Announcements/Tenders | buyer_procurement_notices | tenders, procurement, public contracts | https://geetha.mil.gr/prokiryxeis-diagonismoi/ |
| low | GlobalTenders — Greece IT / Financial Consultancy Tenders | commercial_tender_alert_aggregator_international | tenders, procurement, IT, financial_consultancy, CPV_filtering | https://www.globaltenders.com/gr/ |
| low | HCMC — Recommendations / Directives / Announcements for Listed Companies | regulator_guidance | regulated information, material contracts | http://www.hcmc.gr/el_GR/web/portal/elib/dirseis |
| low | ICAP CRIF - Greek business information & market intelligence | business_intelligence_enrichment | procurement, award notices | https://icapcrif.com/en/ |
| low | KPMG Greece — Banking industry page | consultancy_insight_hub | payments, procurement, core banking | https://kpmg.com/gr/en/home/industries/banking.html |
| low | Lawspot.gr — Νομοθεσία (law/PD/ministerial-decision reference) | commercial_legal_media_aggregator | statutory_acts, legislation | https://www.lawspot.gr/nomothesia/ |
| low | ManpowerGroup / Experis Greece — IT & banking staffing | staffing_agency_jobs | hiring_signals, banking, payments, IT | https://www.manpowergroup.gr/ |
| low | Ministry of Labour & Social Security — Προκηρύξεις Διαγωνισμών (EFKA supervising ministry) | supervising_ministry_tenders | tenders, procurement, IT, payment_systems, contributions | https://ypergasias.gov.gr/category/diagonismoi-diagonismoi/ |
| low | Mononews.gr | business_financial_news_banking | banks, digital banking, AI in banking, vendor signals | https://www.mononews.gr/ |
| low | Naftemporiki — Χρηματιστήριο / listed-company data & announcements | financial_press_aggregator | listed_market_data, financial_press, announcement_context | https://www.naftemporiki.gr/chrimatistirio/tablo-cha/ |
| low | National ESPD service (η-ΕΕΕΣ) via HSPPA / espd platform | espd_platform_pointer | procurement, tenders, ESPD, public contracts | https://espd.eprocurement.gov.gr/ |
| low | OJEU.com — mirror of Bank of Greece EU procurement notices | procurement_aggregator | tenders, procurement, public contracts, award notices | https://ojeu.com/ojdblnk/view-notice.php?id=3827994 |
| low | OP-TED GitHub organisation (eForms SDK, TED API docs, ontology) | technical_documentation_repository | procurement, financial IT, open data | https://github.com/OP-TED |
| low | Radar.gr (Undercover column) | insider_rumour_column | behind-the-scenes business, bank/vendor rumours, early deal signals | https://radar.gr/ |
| low | Reporter.gr | business_financial_news_banking | banks, enterprise tech, digital banking | https://www.reporter.gr/ |
| low | Space Hellas - Financial Sector solutions | vendor_solution_and_reference_page | system integration, banking IT infrastructure, cybersecurity, vendor references | https://www.space.gr/pages.php?pageID=82&langID=2 |
| low | Spend Network - global tender/contract/spend data | global_procurement_data_aggregator | tenders, procurement, public contracts, award notices | https://www.spendnetwork.com/ |
| low | StockTitan / GlobalBanking&Finance / Yahoo Finance — vendor PR mirrors | financial_news_mirror | ATM, deployment, public contracts, award notices | https://www.stocktitan.net/news/DBD/ |
| low | TEE — Public Works & Studies Tender Information System (Technical Chamber of Greece) | professional_chamber_tender_index | tenders, public_works, studies, engineering | https://web.tee.gr/tp-tee/diagwnismoi/ |
| low | Temenos — Athens office & careers (core-banking vendor) | vendor_careers_portal | core_banking, payments, IT_projects, hiring_signals | https://www.temenos.com/office/athens/ |
| low | Tender Impulse - Greece tenders | commercial_tender_aggregator | tenders, procurement | https://tenderimpulse.com/greece-tenders |
| low | TenderAlerts.eu — EU/TED CPV-filtered tender search & hourly alerts | ted_reindex_aggregator | tenders, procurement, public contracts, CPV, TED | https://tenderalerts.eu/ |
| low | TenderAlpha - global procurement & contract-award intelligence | bid_intelligence_platform | procurement, public contracts, award notices | https://www.tenderalpha.com/ |
| low | TenderDetail — CPV 66110000 Banking services (Greece) | international_tender_aggregator | tenders, banking services, CPV facets, award notices | https://www.tenderdetail.com/cpv-tenders/66110000-banking-services |
| low | TenderMetric (tendermetric.com) — TED-derived EU/Greece notices, CPV-searchable | ted_reindex_aggregator | tenders, procurement, public contracts, CPV, TED | https://tendermetric.com/ |
| low | TenderRadar (tenderradar.io) — AI tender-matching, Greece coverage | international_tender_aggregator | tenders, procurement, public contracts, AI matching | https://tenderradar.io/guides/find-tenders-greece |
| low | Tendersontime — Greece tenders & CPV code search | international_tender_aggregator | tenders, procurement, CPV facets, banking services | https://www.tendersontime.com/greece-tenders/ |
| low | contracts.gr — EAADHSY buyer profile (procurement aggregator) | commercial_procurement_aggregator | tenders, procurement, public contracts | https://www.contracts.gr/v1/orgs/55083 |
| low | dda.com.gr — public tenders information / alert service | commercial_tender_alert_service | tender alerts, procurement monitoring, IT, banking | https://dda.com.gr/en/ |
| low | diagonismoi-dimosiou.gr / promitheies.diagonismoi-dimosiou.gr — tender-alert service | commercial_tender_alert_service | tenders, procurement, public contracts | https://diagonismoi-dimosiou.gr/plhrofories |
| low | dimosioidiagonismoi.gr — ESIDIS/KIMDIS tender aggregator | commercial_aggregator | tenders, procurement, contract_awards | https://www.dimosioidiagonismoi.gr/ |
| low | e-tenders.gr — Διαγωνισμοί Δημοσίου ΕΣΗΔΗΣ (support + daily notice emails) | commercial_tender_aggregator | tenders, procurement, public contracts | https://e-tenders.gr/ |
| low | eNotices2 — TED notice submission app & public consultation | notice_submission_and_consultation_app | tenders, procurement, public contracts, award notices | https://enotices2.ted.europa.eu/consult-notices |
| low | eservices.et.gr — National Printing House digital submission portal (Υποβολή Αιτημάτων Δημοσίευσης) | gazette_submission_workflow_portal | procurement, statutory_acts, workflow | https://eservices.et.gr/ |
| low | greecetenders.com (TendersInfo/Euro India network) | commercial_tender_aggregator | tenders, procurement, award notices | https://www.greecetenders.com/ |
| low | iefimerida.gr - Oikonomia section | general_news_business_desk | core banking, bank vendor deals, payments, technology | https://www.iefimerida.gr/oikonomia |
| low | jobsinforex.com — Forex & Fintech jobs in Greece | niche_job_board | hiring_signals, payments, fintech, banking_operations | https://www.jobsinforex.com/jobs/?q=Banking+Operations&country=Greece |
| low | moneyreview.gr - Fintech coverage | business_finance_media | fintech, banking technology, payments | https://www.moneyreview.gr/ |
| low | techblog.gr | consumer_tech_portal | payments products, e-banking, ATM/POS, digital banking | https://techblog.gr/ |
| low | ΔΕΠΑ Εμπορίας / ΔΕΠΑ Υποδομών — corporate tenders (gas) | buyer_eprocurement_portal | tenders, procurement, public contracts | https://www.depa.gr/?lang=en |
| low | ΕΕΤ — Δίκτυο τραπεζών & απασχολούμενο προσωπικό / Statistics | association_statistics | statistics, branches, employees, sector_coverage | https://www.hba.gr/Statistics/List?type=BanksNetwork |
| low | Εφημερίς Δημοπρασιών & Πλειστηριασμών (dimoprasion.gr) — BoG tender republications | tender_gazette_aggregator | tenders, procurement | https://www.dimoprasion.gr/trapeza-tis-ellados-prokiryksi-diagonismou-mp-2025-03a/ |
| low | Μητρώο Επιχορηγούμενων Φορέων (mef.diavgeia.gov.gr) — Registry of Subsidised Bodies | subsidy_registry | spending decisions, public bodies, subsidies | https://mef.diavgeia.gov.gr/ |

## A3 · Regulation & Deadlines — 140 banking sources

| Priority | Source | Type | Topics | URL |
|---|---|---|---|---|
| critical | Bank of Greece - Contributions to the Resolution Fund | national_resolution_authority | contributions, resolution, deadlines, regulation | https://www.bankofgreece.gr/en/main-tasks/resolution/contributions-to-the-resolution-fund |
| critical | Bank of Greece - Resolution (national resolution authority) section, English | national_resolution_authority | regulation, supervision, resolution, contributions, deadlines | https://www.bankofgreece.gr/en/main-tasks/resolution |
| critical | Bank of Greece — Reporting / Data Submission for credit institutions (Υποβολή στοιχείων + Supervisory Reporting Calendar) | regulator_reporting_obligations | deadlines, supervision, regulation | https://www.bankofgreece.gr/kiries-leitourgies/epopteia/pistwtika-idrymata/ypovolh-stoixeiwn-pistwtikwn-idrymatwn |
| critical | DG FISMA - Consultations (banking and finance) hub | official EU consultation index (sector-scoped) | regulation, consultations, deadlines | https://finance.ec.europa.eu/regulation-and-supervision/consultations-0_en |
| critical | ECB Banking Supervision (SSM) portal | primary_supervisor_portal | regulation, supervision, consultations, deadlines | https://www.bankingsupervision.europa.eu/ |
| critical | ECB Banking Supervision - Public consultations (legal framework) | consultation_register | consultations, deadlines, regulation | https://www.bankingsupervision.europa.eu/framework/legal-framework/public-consultations/html/index.en.html |
| critical | EUR-Lex — National transposition measures (NIM) collection | transposition tracker | regulation, deadlines, supervision | https://eur-lex.europa.eu/collection/n-law/mne.html |
| critical | EUR-Lex — official portal for EU law (home) | official legal database / primary-law archive | regulation, supervision, deadlines | https://eur-lex.europa.eu/ |
| critical | European Commission — Financial services (DG FISMA policy homepage) | regulator/policy department portal | regulation, supervision, consultations, deadlines | https://finance.ec.europa.eu/ |
| critical | HBA — Codes of Banking Conduct / Ethics (Κώδικες τραπεζικής δεοντολογίας) | self_regulatory_code | regulation, consultations | https://www.hba.gr/Publications/Info/bankcodes |
| critical | HCMC — Markets in Crypto-Assets (MiCA) section | regulator_topic_hub | regulation, consultations, deadlines, supervision | http://www.hcmc.gr/en_US/web/portal/agores-kryptostoicheion |
| critical | Single Resolution Board (SRB) - MREL policy, dashboards and SRF | eu_resolution_authority | regulation, supervision, resolution, deadlines, mrel, contributions | https://www.srb.europa.eu/en/content/mrel |
| critical | ΑΑΔΕ — myDATA (Ηλεκτρονικά Βιβλία) official section | regulator_program_hub | regulation, mydata, e_invoicing, deadlines | https://www.aade.gr/mydata-ilektronika-biblia |
| critical | Βουλή των Ελλήνων — Διαρκής Επιτροπή Οικονομικών Υποθέσεων (Standing Committee on Economic Affairs) | legislature_committee_actor | regulation, supervision, deadlines | https://www.hellenicparliament.gr/Koinovouleftikes-Epitropes/CommiteeDetailView?CommitteeId=3ec562f4-82ec-45d6-9705-8858534bfabf |
| critical | Βουλή των Ελλήνων — Κατατεθέντα Σχέδια/Προτάσεις Νόμων (Submitted Bills / Law Proposals) | legislature_bill_register | regulation, deadlines, consultations | https://www.hellenicparliament.gr/Nomothetiko-Ergo/Katatethenta-Nomosxedia |
| critical | Συνήγορος του Καταναλωτή (Consumer Ombudsman) — official portal | independent_authority_ombudsman | consumer_protection, dispute_resolution, fee_transparency, payment_services, conduct_rules | https://www.synigoroskatanaloti.gr/ |
| critical | Υπουργείο Εθνικής Οικονομίας και Οικονομικών — Νομοθετικό Έργο (Ministry legislative-work section) | government_ministry_legislation_index | regulation, deadlines, consultations, supervision | https://minfin.gov.gr/ypourgeio/nomothetiko-ergo/ |
| high | 1520 / kataggelies.mindev.gov.gr — Consumer complaints portal & Μητρώα (GGE) | government_complaints_portal | consumer_protection, dispute_resolution, payment_services, fee_transparency | https://kataggelies.mindev.gov.gr/ |
| high | Bank of Greece - Εξυγίανση πιστωτικών ιδρυμάτων section, Greek | national_resolution_authority | regulation, supervision, resolution, contributions | https://www.bankofgreece.gr/kiries-leitourgies/eksygiansi-pistotikon-idrymaton |
| high | Bank of Greece — Credit Institutions supervision section (Πιστωτικά ιδρύματα) | regulator_topic_index | supervision, regulation, deadlines | https://www.bankofgreece.gr/kiries-leitourgies/epopteia/pistwtika-idrymata |
| high | Bank of Greece — DORA (Digital Operational Resilience) supervisory page | regulator_topic_page | regulation, supervision, deadlines | https://www.bankofgreece.gr/kiries-leitourgies/epopteia/dora-pshfiakh-epixeirhsiakh-anthektikothta-xrhmatooikonomikoy-tomea |
| high | Bank of Greece — EPATH Decisions (Αποφάσεις ΕΠΑΘ, Επιτροπή Πιστωτικών & Ασφαλιστικών Θεμάτων) | regulator_primary_act_register | regulation, supervision, deadlines | https://www.bankofgreece.gr/trapeza/nomiko-plaisio/apofaseis-epath |
| high | Bank of Greece — Governor's Acts (Πράξεις Διοικητή / ΠΔ/ΤΕ) | regulator_primary_act_register | regulation, supervision, deadlines | https://www.bankofgreece.gr/trapeza/nomiko-plaisio/prakseis-dioikhth |
| high | Bank of Greece — Legal Framework hub (Νομικό Πλαίσιο) | regulator_legal_index | regulation, supervision, deadlines | https://www.bankofgreece.gr/trapeza/nomiko-plaisio |
| high | Bernitsas Law - Insights (briefings, legal alerts, podcasts) | law_firm_client_alert | regulation, supervision, deadlines, banking, payments | https://bernitsaslaw.com/insights |
| high | CUBE - automated regulatory intelligence (RegAI) | regulatory_intelligence_aggregator | regulation, supervision, consultations, deadlines | https://cube.global/ |
| high | Corlytics - Regulation Library & regulatory monitoring/horizon scanning | regulatory_intelligence_aggregator | regulation, supervision, consultations, deadlines | https://www.corlytics.com/solutions/regulation-library/ |
| high | EBA - Deposit Guarantee Schemes data | eu_supervisory_aggregator | deposit_guarantee, contributions, regulation, supervision | https://www.eba.europa.eu/activities/single-rulebook/regulatory-activities/depositor-protection/deposit-guarantee-schemes-data |
| high | ECB Banking Supervision - News & publications (press releases) | press_release_feed | supervision, regulation, consultations, deadlines | https://www.bankingsupervision.europa.eu/press/html/index.en.html |
| high | ECB Banking Supervision - Supervisory policy documents & guides | supervisory_guide_library | regulation, supervision, consultations | https://www.bankingsupervision.europa.eu/framework/supervisory-policy/html/index.en.html |
| high | ECB SSM - Supervisory Review and Evaluation Process (SREP) & aggregated results | supervisory_process_results | supervision, regulation | https://www.bankingsupervision.europa.eu/activities/srep/html/index.en.html |
| high | ECB SSM Supervisory priorities (2026-28 and rolling) | supervisory_strategy | supervision, regulation, deadlines | https://www.bankingsupervision.europa.eu/framework/priorities/html/index.en.html |
| high | ECB legal framework for banking supervision (SSM Regulation & Framework Regulation) | legal_framework_hub | regulation, supervision | https://www.bankingsupervision.europa.eu/framework/legal-framework/ecb-legal/html/index.en.html |
| high | EIOPA - Consultations | EU supervisory authority consultation register | regulation, supervision, consultations, deadlines | https://www.eiopa.europa.eu/consultations_en |
| high | ESMA - Consultations list | EU supervisory authority consultation register | regulation, supervision, consultations, deadlines | https://www.esma.europa.eu/press-news/consultations |
| high | EY Greece - Tax & Law Alerts (incl. financial-services regulation) | professional_services_legal_alert | regulation, supervision, deadlines, payments | https://www.ey.com/en_gr/technical/tax/tax-alerts |
| high | European Commission — 'Have your say' better-regulation portal | rulemaking/consultation portal | consultations, regulation, deadlines | https://ec.europa.eu/info/law/better-regulation/have-your-say_en |
| high | European Commission — Consultations (banking and finance) | consultation register | consultations, regulation, supervision | https://commission.europa.eu/business-economy-euro/financial-services/regulation-supervision-and-enforcement/consultations-banking-and-finance_en |
| high | Fintech Athens (Greek Fintech Hub / NBG / AUEB-ACEin / NKUA) | industry_conference_agenda | regulation, supervision, payments, fintech, ai | https://www.fintechhub.gr/events/fintech-athens-40 |
| high | HBA — Anti-Money-Laundering activity area (Καταπολέμηση ξεπλύματος) | association_topic_feed | regulation, supervision, deadlines | https://www.hba.gr/ActivityAreas/List?type=MoneyLaundering |
| high | HBA — Legal Issues activity area (Νομικά θέματα) | association_topic_feed | regulation, consultations, deadlines | https://www.hba.gr/ActivityAreas/List?type=LegalIssues |
| high | HCMC — Announcements / Results (Ανακοινώσεις – Αποτελέσματα) | regulator_announcements_feed | regulation, supervision, deadlines | http://www.hcmc.gr/en/web/portal/announcements |
| high | HCMC — Circulars (Εγκύκλιοι Επιτροπής Κεφαλαιαγοράς) | regulator_circulars_archive | regulation, supervision, deadlines | http://www.hcmc.gr/el/elib/circulars |
| high | HCMC — MiFID II / MiFIR section | regulator_topic_hub | regulation, supervision | http://www.hcmc.gr/el_GR/web/portal/mifid-ii-mifir |
| high | HDPA — Related acts on credit/financing institutions (σχετικές πράξεις) | regulator_decisions_curated_list | decisions, supervision, regulation | https://www.dpa.gr/el/enimerwtiko/thematikes_enotites/xrimatopistotika/pistwtika_xrhmatodotika/sxetikes_prakseis_pistwtika |
| high | HDPA — Χρηματοπιστωτικά (Financial sector) thematic hub | regulator_topic_hub | regulation, supervision, guidelines, decisions | https://www.dpa.gr/el/enimerwtiko/thematikes_enotites/xrimatopistotika |
| high | Hellenic Bank Association (HBA/EET) - European Banking Union legal pages (DGSD / BRRD / SRM-SRF) | industry_association | regulation, resolution, deposit_guarantee, mrel, consultations, deadlines | https://www.hba.gr/EuropeanAssociation?sectiontype=DGSD |
| high | Hellenic Bank Association — Combating Financial Crime / national AML law list (Ελληνική Ένωση Τραπεζών) | industry_association_law_index | regulation, supervision, deadlines, consultations | https://www.hba.gr/FinancialLaw/List?type=NationalFinancialCrime |
| high | KPMG Regulatory Insight Centre + Regulatory Barometer / EU Regulatory Radar | advisory_regulatory_barometer_radar | regulation, supervision, deadlines, consultations | https://kpmg.com/xx/en/our-insights/regulatory-insights.html |
| high | Kyriakides Georgopoulos (KG Law Firm) - Newsletters / Articles & Publications | law_firm_client_alert | regulation, supervision, deadlines, banking, payments | https://kglawfirm.gr/newsletters/ |
| high | Lawspot — HDPA (Αρχή Προστασίας Δεδομένων) tag/topic page | legal_news_aggregator | decisions, regulation, supervision | https://www.lawspot.gr/etiketes/arhi-prostasias-dedomenon-prosopikoy-haraktira/ |
| high | Lexology - Greece banking/payments/fintech (law-firm contributed articles) | legal_alert_aggregator | regulation, supervision, deadlines, banking, payments | https://www.lexology.com/index/report/banking-fintech |
| high | NOMOS – Τράπεζα Νομικών Πληροφοριών (Intrasoft International / Netcompany) | commercial_legal_information_bank | regulation, supervision, deadlines, consultations | https://lawdb.intrasoftnet.com/portal/home |
| high | Official Journal of the European Union (OJ L-series via EUR-Lex) | official gazette | regulation, deadlines | https://eur-lex.europa.eu/oj/direct-access.html |
| high | OpenGov.gr — Ministry of Development public consultations (ypoian) | public_consultation_portal | consultations, regulation, deadlines, consumer_protection, payment_services | https://www.opengov.gr/mindev/ |
| high | PwC Greece - Legal News (Vizas - Grigoriadou & Partners / PwC Legal) | professional_services_legal_alert | regulation, supervision, deadlines, banking, payments | https://www.pwc.com/gr/en/newsletters/legal-news.html |
| high | Regnology - regulatory reporting & taxonomy resources | regtech_vendor_reporting_resource | regulation, supervision, deadlines | https://www.regnology.net/ |
| high | TEKE Annual Reports (Apologismos) - PDF series | annual_report | contributions, deposit_guarantee, resolution_financing, deadlines | https://www.teke.gr/pages/ABOUT/files/Annual_Report_2024_GR.pdf |
| high | Wolters Kluwer - Regulatory Change Management / OneSumX regulatory intelligence | regulatory_intelligence_aggregator | regulation, supervision, deadlines | https://www.wolterskluwer.com/en/solutions/compliance-solutions/regulatory-compliance |
| high | minfin.gov.gr — Χρηματοπιστωτικός Τομέας (Financial Sector) policy section | government_policy_section | regulation, supervision | https://minfin.gov.gr/oikonomiki-politiki/ |
| high | Βουλή των Ελλήνων — Επεξεργασία στις Επιτροπές (Committee Processing of Bills) | legislature_committee_pipeline | regulation, supervision, deadlines | https://www.hellenicparliament.gr/Nomothetiko-Ergo/Epexergasia-stis-Epitropes |
| high | Βουλή των Ελλήνων — Επιστημονική Υπηρεσία της Βουλής (Scientific Service / Έκθεση επί του Νομοσχεδίου) | legislature_legal_analysis | regulation, supervision | https://www.hellenicparliament.gr/Dioikitiki-Organosi/Ypiresies/Epistimoniki-Ypiresia/ |
| high | Βουλή των Ελλήνων — Συνεδριάσεις/Πρακτικά Κοινοβουλευτικών Επιτροπών (Committee Sessions & Minutes) | legislature_committee_minutes | regulation, supervision, deadlines | https://www.hellenicparliament.gr/Koinovouleftikes-Epitropes/Synedriaseis |
| high | Βουλή των Ελλήνων — Ψηφισθέντα Νομοσχέδια (Voted Bills) | legislature_enacted_text | regulation, deadlines | https://www.hellenicparliament.gr/Nomothetiko-Ergo/Psifisthenta-Nomoschedia |
| high | Γενική Γραμματεία Χρηματοπιστωτικού Τομέα & Διαχείρισης Ιδιωτικού Χρέους (General Secretariat of the Financial Sector & Private Debt Management) — ministry page | government_general_secretariat | regulation, supervision, deadlines | https://minfin.gov.gr/en/organisation/general-secretariats/general-secretariat-of-the-financial-sector-and-private-debt-management/ |
| high | Γραφείο Τύπου ΥΠΕΘΟ — Ministry Press Office / Press Releases | government_press_office | regulation, consultations, deadlines | https://minfin.gov.gr/grafeio-typou/ |
| high | Δι@ύγεια (Diavgeia) — ΥΠΕΘΟ transparency feed of ministerial acts | government_transparency_register | regulation, supervision, deadlines | https://diavgeia.gov.gr/f/minfin |
| high | ΕΕΤ - Βάση χρηματοοικονομικού δικαίου / Συστήματα πληρωμών (HBA payment-systems legal database) | regulatory_tracking_index | regulation, payments, deadlines, open banking | https://www.hba.gr/FinancialLaw/List?type=NationalPaymentSystems |
| high | Τράπεζα της Ελλάδος — Complaints to the Bank of Greece | supervisor_complaints_desk | dispute_resolution, supervision, consumer_protection, payment_services | https://www.bankofgreece.gr/en/main-tasks/supervision/credit-institutions/complaints-to-the-bank-of-greece |
| high | Τράπεζα της Ελλάδος — Transparency of banking transactions (Διαφάνεια τραπεζικών συναλλαγών) | central_bank_supervisor | fee_transparency, supervision, conduct_rules, payment_services | https://www.bankofgreece.gr/en/main-tasks/supervision/credit-institutions/transparency-of-banking-transactions |
| medium | Ascent (AscentAI) - obligations-mapping regtech | regulatory_intelligence_aggregator | regulation, deadlines | https://www.ascentregtech.com/ |
| medium | Bank of Greece - Supervision (NCA participating in SSM/JSTs) | national_competent_authority | supervision, regulation | https://www.bankofgreece.gr/en/main-tasks/supervision |
| medium | Bank of Greece — Credit institutions passporting into Greece, by home country (xlsx) | official_register_file | passporting, credit institutions, cross-border, registers | https://www.bankofgreece.gr/RelatedDocuments/10_CrossBorder.xlsx |
| medium | Bank of Greece — Disclosure of supervisory practices (Δημοσιοποίηση εποπτικών πρακτικών) | regulator_topic_page | supervision, regulation | https://www.bankofgreece.gr/kiries-leitourgies/epopteia/pistwtika-idrymata/dhmosiopoihsh-epoptikwn-praktikwn |
| medium | Bank of Greece — List of Microfinance Institutions (xlsx) | official_register_file | authorisation, microfinance, registers | https://www.bankofgreece.gr/RelatedDocuments/19_List_of_Microfinance_Institutions.xlsx |
| medium | Bank of Greece — List of Monetary Financial Institutions (MFI) for statistics | statistical_register_index | monetary financial institutions, statistics, registers | https://www.bankofgreece.gr/statistika/nomismatikh-kai-trapezikh-statistiki/katalogos-nxi |
| medium | Bank of Greece — Supervisory methodologies & practices (Εποπτικές μεθοδολογίες και πρακτικές) | regulator_topic_page | supervision, regulation | https://www.bankofgreece.gr/kiries-leitourgies/epopteia/pistwtika-idrymata/epoptikes-methodologies-kai-praktikes |
| medium | Bank of Greece — Transparency of banking transactions (Διαφάνεια τραπεζικών συναλλαγών, ΠΔ/ΤΕ 2501/2002) | regulator_topic_page | regulation, supervision | https://www.bankofgreece.gr/kiries-leitourgies/epopteia/pistwtika-idrymata/diafaneia-trapezikwn-synallagwn |
| medium | ComplyAdvantage - AML data & State of Financial Crime | regtech_vendor_insights | regulation, supervision | https://complyadvantage.com/ |
| medium | Complytek - AML/KYC compliance platform & glossary | regtech_vendor_obligation_reference | regulation, supervision | https://www.complytek.ai/ |
| medium | Deloitte Greece - Tax & Legal Alerts | professional_services_legal_alert | regulation, deadlines, banking | https://www.deloitte.com/gr/en/services/tax/perspectives/tax-alerts-from-greece-deloittegreece-tax-alerts-insights.html |
| medium | Delphi Economic Forum – finance/payments panels | policy_forum_agenda | regulation, supervision, payments, policy | https://def-xi.delphiforum.gr/ |
| medium | EBA - Regulatory Technical Standards / Guidelines on MREL | eu_rulemaking | mrel, resolution, regulation, deadlines | https://www.eba.europa.eu/activities/single-rulebook/regulatory-activities/recovery-resolution-and-dgs/regulatory-technical-8 |
| medium | EBA News & Press (news hub with RSS) | regulator_news_hub | regulation, supervision, consultations, deadlines | https://www.eba.europa.eu/news-press |
| medium | EBA email alerts subscription | subscription_signup | regulation, consultations, deadlines | https://www.eba.europa.eu/subscribe-to-email-alerts |
| medium | EBA news RSS feed | machine_readable_feed | regulation, consultations, deadlines | https://www.eba.europa.eu/news-press/news/rss.xml |
| medium | ECB (monetary side) - Public consultations | central-bank consultation index | regulation, consultations, deadlines | https://www.ecb.europa.eu/press/intro/cons/html/index.en.html |
| medium | ECB Governing Council decisions - other decisions feed | governing_council_decisions | regulation, supervision, deadlines | https://www.ecb.europa.eu/press/govcdec/otherdec/html/index.en.html |
| medium | ECB Supervision Newsletter (quarterly) | supervisory_newsletter | supervision, regulation, deadlines | https://www.bankingsupervision.europa.eu/press/supervisory-newsletters/html/index.en.html |
| medium | ESAs Joint Committee consultations (EBA/ESMA/EIOPA joint) | cross-authority consultation pointer | regulation, supervision, consultations, deadlines | https://www.eba.europa.eu/about-us/organisation-and-governance/governance-structure-and-decision-making/joint-committee |
| medium | EUR-Lex — Legislation summaries (LEGISSUM), Greek interface | legislation summaries | regulation, supervision | https://eur-lex.europa.eu/browse/summaries.html |
| medium | Forin.gr — Φορολογικά/Λογιστικά (decisions index + myDATA Q&A) | tax_news_aggregator | regulation, deadlines, mydata, decisions, commentary | https://www.forin.gr/ |
| medium | Forvis Mazars - Financial Services Regulatory Advisory (Group) | midtier_advisory_regulatory_hub | regulation, deadlines, supervision | https://www.forvismazars.com/group/en/industries/financial-services/financial-services-regulatory-advisory |
| medium | GSIS – Τράπεζα Νομικών Πληροφοριών (Ministry of Finance legal information bank) | government_legal_information_bank | regulation, supervision, deadlines | https://www.gsis.gr/trapeza-nomikon-pliroforion |
| medium | Grant Thornton Greece - Corporate Governance, Risk & Compliance Services + Insights | midtier_advisory_local_firm | regulation, supervision, consultations | https://www.grant-thornton.gr/en/services/assurance/sustainability-and-governance/risk-management--compliance-services/ |
| medium | HCMC — Ministerial Decisions & Laws (Υπουργικές Αποφάσεις) | regulator_legislation_index | regulation | http://www.hcmc.gr/el/elib/lawsministerial |
| medium | HCMC — Press Releases (EN) | regulator_press_release_feed | regulation, supervision | http://www.hcmc.gr/en_US/web/portal/elib/press |
| medium | HCMC — Professional Suitability Certification (Πιστοποίηση Καταλληλότητας Προσώπων) | regulator_certification_registry | regulation, supervision, deadlines | http://www.hcmc.gr/el/pistepkat |
| medium | Hellenic Bank Association (HBA/EET) - SSM section & ECB legal acts | industry_association_pointer | regulation, supervision, consultations | https://www.hba.gr/EuropeanAssociation?sectiontype=SSM |
| medium | Hellenic Bank Institute (ETI / ΕΤΙ) — training & certification arm of the HBA | training_catalogue | regulation, supervision, deadlines | https://www.hba.gr/eti/ |
| medium | Hellenic Capital Market Commission (HCMC) - resolution authority for investment firms / investor compensation | national_resolution_authority | resolution, deposit_guarantee, regulation | http://www.hcmc.gr/el_GR/web/portal/exygianse-epicheireseon-ependyseon |
| medium | KPMG Global - 2026 Financial Services Regulatory Priorities / Banking Trends | annual_regulatory_priorities | regulation, deadlines, supervision | https://kpmg.com/xx/en/our-insights/regulatory-insights/2025-financial-services-regulatory-priorities.html |
| medium | Koutalidis Law Firm - News & Insights | law_firm_client_alert | regulation, supervision, banking, payments | https://www.koutalidis.gr/category/insights/ |
| medium | Ministry of National Economy & Finance — AML/CFT policy page & National Risk Assessment | ministry_policy_page | regulation, consultations, supervision | https://minfin.gov.gr/oikonomiki-politiki/katapolemisi-nomimopoiisis-esodon-apo-egklimatikes-drastiriotites/ |
| medium | NOMIKI BIBLIOTHIKI - NB Daily / publications (Greek legal analysis) | legal_publisher_analysis | regulation, banking, payments | https://daily.nb.org/ |
| medium | POTAMITIS VEKRIS - Articles & Publications | law_firm_client_alert | regulation, supervision, banking, payments | https://www.potamitisvekris.com/insights/articles/ |
| medium | PwC Switzerland - Regulatory Radar & FS regulatory monitoring | advisory_regulatory_radar | regulation, deadlines | https://www.pwc.ch/en/industry-sectors/financial-services/fs-regulations/regulatoryradar.html |
| medium | Qualex / Νομική Βιβλιοθήκη (Nomiki Bibliothiki legal content platform) | commercial_legal_content_platform | regulation, supervision, deadlines | https://www.qualex.gr/ |
| medium | Regology - horizon scanning & law/obligation library | regulatory_intelligence_aggregator | regulation, deadlines | https://www.regology.com/ |
| medium | SAS - Regulatory Content for EBA Taxonomies | regtech_vendor_reporting_resource | regulation, supervision, deadlines | https://www.sas.com/en_my/software/regulatory-content-eba-taxonomies.html |
| medium | Sanction Scanner - AML in Greece knowledge base | regtech_vendor_country_obligation_guide | regulation, supervision | https://www.sanctionscanner.com/aml-guide/anti-money-laundering-aml-in-greece-76 |
| medium | Vouliwatch — Νόμοι & Ψηφοφορίες / Votewatch (Independent Parliamentary Monitor) | civil_society_legislation_tracker | regulation, deadlines | https://vouliwatch.gr/votewatch |
| medium | e-katanalotis.gov.gr — price & bank interest-rate transparency platform (Ministry of Development) | government_price_transparency_platform | fee_transparency, consumer_protection, payment_services | https://e-katanalotis.gov.gr/ |
| medium | e-nomothesia.gr - consolidated Greek banking law repository | legal_aggregator | regulation, deposit_guarantee, resolution | https://www.e-nomothesia.gr/kat-trapezes-pistotika-idrumata/nomos-4370-2016.html |
| medium | e-nomothesia.gr — Greek legislation database (codified AADE decisions) | legal_database | regulation, deadlines, decisions, legal_text | https://www.e-nomothesia.gr/kat-oikonomia/forologia/apophase-aade-1155-2023.html |
| medium | e-nomothesia.gr — legislation & law-news portal | legal_aggregator | regulation, deadlines | https://www.e-nomothesia.gr/law-news/allages-sten-adeiodotese-parokhou-uperesion-kryptostoixeion.html |
| medium | e-nomothesia.gr — Νομοθετική Επικαιρότητα (Law News) | legal_news_portal | regulation, deadlines, consultations | https://www.e-nomothesia.gr/law-news/ |
| medium | eΘέμις (e-Themis) – Ένωση Ελλήνων Νομικών (legislation + jurisprudence) | association_legal_aggregator | regulation, supervision | https://www.ethemis.gr/ |
| medium | nepa.gr — Government Gazette (ΦΕΚ) text republisher | gazette_mirror | regulation, deadlines | https://nepa.gr/ |
| medium | Βουλή των Ελλήνων — Όλη η Επικαιρότητα Νομοθετικού Έργου (Legislative Work News Stream) | legislature_activity_stream | regulation, deadlines | https://www.hellenicparliament.gr/Nomothetiko-Ergo/all-laws |
| medium | Βουλή των Ελλήνων — Ημερήσια Διάταξη Ολομέλειας & Εβδομαδιαίο Δελτίο (Plenary Agenda & Weekly Bulletin) | legislature_agenda_bulletin | regulation, deadlines | https://www.hellenicparliament.gr/Nomothetiko-Ergo |
| medium | Βουλή των Ελλήνων — Νομοθετικό Έργο RSS Feed | feed_rss | regulation, deadlines | https://www.hellenicparliament.gr/rss |
| medium | Βουλή των Ελλήνων — Συνεδριάσεις / Πρακτικά Ολομέλειας (Plenary Sessions & Minutes) | legislature_plenary_minutes | regulation, deadlines | https://www.hellenicparliament.gr/Praktika/Synedriaseis-Olomeleias |
| medium | ΕΓΔΙΧ / Ειδική Γραμματεία Διαχείρισης Ιδιωτικού Χρέους — keyd.gov.gr | government_special_secretariat_site | regulation, supervision, deadlines | http://www.keyd.gov.gr/ |
| medium | Ελληνική Ένωση Τραπεζών (Hellenic Bank Association) — Consumer-protection financial-law portal | industry_association_law_index_pointer | regulation, fee_transparency, payment_services, consumer_protection, dispute_resolution | https://www.hba.gr/FinancialLaw/List?type=NationalConsumerBanking |
| medium | Επιτροπή Κεφαλαιαγοράς (HCMC) - διαβουλεύσεις/προκηρύξεις (Hellenic Capital Market Commission consultations & tenders) | supervisor_procurement_page | supervision, regulation, consultations, deadlines | http://www.hcmc.gr/el/elib/consults |
| medium | ΝΟΜΟΤΕΛΕΙΑ – Ηλεκτρονική Νομική Πληροφόρηση (Nomotelia) | commercial_legal_information_bank | regulation, supervision, deadlines | https://nomotelia.gr/ |
| medium | ΤΕΚΕ - Ταμείο Εγγύησης Καταθέσεων και Επενδύσεων (Hellenic Deposit & Investment Guarantee Fund) | resolution_fund_procurement_page | supervision, regulation, deadlines | https://www.teke.gr/ |
| low | Compliance.ai - regulatory change management | regulatory_intelligence_aggregator | regulation, deadlines | https://www.compliance.ai/ |
| low | Deloitte US - 2026 Financial Services Regulatory Outlooks / Banking Outlook | annual_regulatory_outlook_report | regulation, deadlines | https://www.deloitte.com/us/en/services/consulting/articles/financial-services-regulatory-outlooks.html |
| low | European Parliament — Legislative Observatory (OEIL) procedure files | legislative observatory | regulation, deadlines | https://oeil.europarl.europa.eu/oeil/en/procedure-file?reference=2023%2F0210%28COD%29 |
| low | LawNet.gr - Greek legal news (EU financial regulation coverage) | legal_news_portal | regulation, payments, banking | https://lawnet.gr/ |
| low | Lawspot — Greek legislation & legal-news portal (banking/payments laws) | legal_news_aggregator | regulation, deadlines | https://www.lawspot.gr/nomothesia/nomos-4537-2018/ |
| low | Machas & Partners - Banking & Finance insights | law_firm_client_alert | regulation, banking, payments | https://machas-partners.com/1015_2/Banking-&-Finance |
| low | Norton Rose Fulbright 'Regulation Tomorrow' consultation tracker | third-party regulatory-consultation tracker | regulation, consultations, deadlines | https://www.regulationtomorrow.com/ |
| low | diadikasies.gov.gr – Κωδικοποιήσεις (official codifications register) | official_codification_register | regulation | https://diadikasies.gov.gr/kwdikopoihseis |
| low | e-Themis (ΕΚΤ) – Ηλεκτρονική Βάση Ελληνικής Νομοθεσίας (National Documentation Centre) | government_research_legal_database | regulation | https://www.ekt.gr/el/news/10566 |
| low | Βιβλιοθήκη της Βουλής — Κοινοβουλευτική Συλλογή / Πρακτικά Συνεδριάσεων (Parliament Library Minutes Archive) | legislature_library_archive | regulation | https://library.parliament.gr/ |
| low | Εθνική Αρχή Κυβερνοασφάλειας - Δημόσιες Διαβουλεύσεις/Διαγωνισμοί (National Cybersecurity Authority) | authority_procurement_page | regulation, supervision, consultations | https://cyber.gov.gr/ |
| low | ΙΝΚΑ — Ινστιτούτο Καταναλωτών / Γενική Ομοσπονδία Καταναλωτών Ελλάδος | consumer_association_ngo | consumer_protection, fee_transparency, payment_services | https://inka.gr/ |

## A4 · Market Statistics — 19 banking sources

| Priority | Source | Type | Topics | URL |
|---|---|---|---|---|
| critical | Eurostat Data Browser - Individuals: internet activities (isoc_ci_ac_i) | official_statistics_dataset | market statistics, payment statistics, digital banking adoption | https://ec.europa.eu/eurostat/databrowser/view/isoc_ci_ac_i/default/table?lang=en |
| high | Bank of Greece - Bank deposit and loan interest rates | interest_rate_statistics_page | market statistics | https://www.bankofgreece.gr/en/statistics/financial-markets-and-interest-rates/bank-deposit-and-loan-interest-rates |
| high | Deloitte Greece — Financial Services / Insights | consultancy_publications_hub | market statistics, payment statistics, cashless usage | https://www.deloitte.com/gr/en.html |
| high | Digital Decade DESI visualisation tool (dashboard) | policy_indicator_dashboard | market statistics, digital banking adoption, e-commerce | https://digital-decade-desi.digital-strategy.ec.europa.eu/ |
| high | EPANT Banking Deposits Sector Inquiry (Κλαδική Έρευνα Τραπεζικές Καταθέσεις) - hub & interim report | regulator_sector_inquiry | market statistics, payment statistics | https://www.epant.gr/enimerosi/deposits.html |
| high | Eurostat Data Browser - Individuals using the internet for internet banking (regional, isoc_r_iuse_i) | official_statistics_dataset | market statistics, digital banking adoption, regional statistics | https://ec.europa.eu/eurostat/databrowser/view/isoc_r_iuse_i/default/table?lang=en |
| high | Open Banking Tracker — Greece country page | market_index_aggregator_directory | open banking directory, ASPSP list, API aggregators, developer portals | https://www.openbankingtracker.com/country/greece |
| medium | Bank of Greece - Financial markets and interest rates statistics | central_bank_statistics_portal | market statistics | https://www.bankofgreece.gr/en/statistics/financial-markets-and-interest-rates |
| medium | EBA — Credit Institutions Register | eu_aggregated_credit_institution_register | credit institutions, PSP register, payments actors population | https://www.eba.europa.eu/risk-analysis-and-data/credit-institutions-register |
| medium | ECB — Use of cash by companies in the euro area (companies' cash survey, incl. 2024) | survey_report | cash usage, payment statistics | https://www.ecb.europa.eu/stats/ecb_surveys/use_of_cash_by_companies_in_the_euro_area/html/index.en.html |
| medium | EPANT acts on Diavgeia transparency portal (Δι@ύγεια) | government_transparency_feed | market statistics, payment statistics | https://app.diavgeia.gov.gr/f/epant |
| medium | EU Open Data Portal (data.europa.eu) - Individuals using the internet for internet banking | open_data_catalogue_record | market statistics, digital banking adoption, data access | https://data.europa.eu/data/datasets/ag89sjmlmna2bsmr8ov2aa?locale=en |
| medium | Enable Banking — Greece market documentation | aggregator_market_docs | ASPSP connections, auth flow, redirect SCA, AIS, PIS | https://enablebanking.com/docs/markets/gr/ |
| medium | Eurostat Data Browser - Individuals: internet use (isoc_ci_ifp_iu) | official_statistics_dataset | market statistics, digital adoption | https://ec.europa.eu/eurostat/databrowser/product/page/ISOC_CI_IFP_IU |
| medium | Eurostat Statistics Explained - Digital economy and society statistics: households and individuals | statistical_commentary | market statistics, digital banking adoption, methodology | https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Digital_economy_and_society_statistics_-_households_and_individuals |
| medium | HBA Bulletin (Δελτίο ΕΕΤ) publication series | association_periodical | market statistics, payment statistics | https://www.hba.gr/Publications/PressList |
| medium | Salt Edge — Greece bank coverage (account information) | aggregator_coverage_page | account information, bank coverage, aggregation, ASPSP list | https://www.saltedge.com/products/account_information/coverage/gr |
| medium | World Bank G20 Financial Inclusion Indicators - Greece | aggregated_financial_inclusion_dashboard | market statistics, payment statistics, cash usage | https://datatopics.worldbank.org/g20fidata/country/greece |
| low | Eurostat Data Browser - Financial accounts of households (currency & deposits, nasa_10_f) | official_statistics_dataset | cash usage, financial services, market statistics | https://ec.europa.eu/eurostat/databrowser/view/nasa_10_f_bs/default/table?lang=en |

## A5 · Early Intent & Jobs — 175 banking sources

| Priority | Source | Type | Topics | URL |
|---|---|---|---|---|
| critical | ATHEX Group – Listed Companies Announcements (athexgroup.gr) | stock_exchange_regulated_disclosure_portal | leadership moves, organization changes, board changes | https://athens.euronext.com/el/more-options/announcements/press-releases |
| critical | Business Daily (businessdaily.gr) — Τράπεζες + Επιχειρήσεις | financial_news_portal_section | leadership_moves, organization_changes, hiring, jobs | https://www.businessdaily.gr/trapezes |
| critical | Egon Zehnder Athens office | executive_search_firm_site | leadership moves, organization changes, hiring | https://www.egonzehnder.com/office/athens |
| critical | Elevate Greece — National Startup Registry: Registered Startups (Εγγεγραμμένες startups) | government_startup_registry | organization changes, jobs, hiring | https://elevategreece.gov.gr/el/eggegrammenes-startups/ |
| critical | Eurobank — Careers ATS / Θέσεις Εργασίας (careers.eurobank.gr) | ats_job_board | jobs, hiring, organization changes | https://careers.eurobank.gr/ |
| critical | GEMI - Greek General Commercial Registry (businessportal.gr) | company_registry | leadership moves, organization changes | https://www.businessportal.gr/en/i-want-to-find-information-about-a-company/ |
| critical | HR Professional (hrpro.gr) — Boussias Media monthly HR magazine | hr_trade_press | leadership moves, hiring, organization changes, jobs | https://hrpro.gr/ |
| critical | Stanton Chase Athens - office & Financial Services practice | executive_search_firm_site | jobs, hiring, leadership moves, organization changes | https://www.stantonchase.com/office/executive-search-firm-in-athens-greece |
| critical | Tiresias S.A. (Τειρεσίας) - Management / Administration (Διοίκηση) | official_governance_page | leadership moves, organization changes | https://www.tiresias.gr/el/i-etaireia/dioikisi/ |
| critical | ΟΤΟΕ - Ομοσπονδία Τραπεζοϋπαλληλικών Οργανώσεων Ελλάδας (Announcements & Press Releases) | sector_union_federation_press | restructuring, voluntary_exit_scheme, collective_dismissals, branch_closures, organization | https://www.otoe.gr/page/4-2026 |
| critical | ΣΔΑΔΕ / GPMA — Σύνδεσμος Διοίκησης Ανθρώπινου Δυναμικού Ελλάδας (Greek People Management Association) | hr_professional_association | jobs, hiring, leadership moves, organization changes | https://gpma.gr/ |
| high | ATHEX / Euronext Athens — Company Announcements & HERMES (Ανακοινώσεις εισηγμένων) | regulated-market issuer disclosure portal | leadership moves, board appointments, organization changes | https://athens.euronext.com/en/more-options/announcements-companies |
| high | Aftodioikisi.gr - Προσλήψεις (public-sector recruitment) | recruitment_news_aggregator | jobs, hiring, organization changes | https://www.aftodioikisi.gr/proslipseis/ |
| high | Alpha Services and Holdings / Alpha Bank – Governance & Announcements | issuer_investor_relations | leadership moves, board changes, organization changes | https://www.alpha.gr/en/Group/advocating-sound-governance-practices/management/board-of-directors |
| high | Amrop Hellas (Amrop Athens) | executive_search_firm_site | jobs, hiring, leadership moves, organization changes | https://www.amrop.com/global-reach/global-offices/athens |
| high | Attica Bank - Corporate / Press & Board announcements | official_press_investor_relations | leadership moves, organization changes | https://www.atticabank.gr/en/ |
| high | Bloomberg — Greece banking coverage | international_financial_press | leadership moves, organization changes | https://www.bloomberg.com/ |
| high | Boyden Greece, Cyprus & Malta | executive_search_firm_site | leadership moves, hiring, organization changes | https://www.boyden.com/greece/ |
| high | Citywire — Wealth Manager / Selector, Private Banking tag | specialist_wealth_trade_press | leadership moves, hiring, organization changes | https://citywire.com/wealth-manager/tag/private-banking |
| high | Delphi Economic Forum - speakers directory | conference_speaker_roster | leadership moves, organization changes | https://def-xi.delphiforum.gr/speakers |
| high | Developers by Kariera.gr (devs.kariera.gr) developer job board | developer_job_board | jobs, hiring, organization changes | https://devs.kariera.gr/category/jobs/ |
| high | Eurobank Holdings – Board of Directors & Corporate Governance | issuer_investor_relations | leadership moves, board changes, organization changes | https://www.eurobank.gr/en/group/about-eurobank/corporate-governance/board-of-directors/the-bod-members |
| high | Financial Times — Greece topic stream | international_financial_press | organization changes, leadership moves | https://www.ft.com/greece |
| high | GPMA / ΣΔΑΔΕ — LinkedIn company page | association_social_feed | leadership moves, hiring, organization changes | https://gr.linkedin.com/company/gpma-%CF%83%CE%B4%CE%B1%CE%B4%CE%B5 |
| high | GR.EC.A — Board of Directors (Διοικητικό Συμβούλιο) | governance_leadership_page | leadership moves, organization changes | https://www.greekecommerce.gr/about-us/dioikitiko-simboylio/ |
| high | Glassdoor — Greece Jobs listings | international_job_board | jobs, hiring | https://www.glassdoor.com/Job/greece-jobs-SRCH_IL.0,6_IN100.htm |
| high | Great Place To Work® Hellas — Best Workplaces & Certified Companies | employer_branding_award_program | jobs, hiring, organization changes, leadership moves | https://greatplacetowork.gr/best-workplaces/best-workplaces-hellas/ |
| high | HBA English site — About HBA / Chairman (Hellenic Bank Association EN) | association_governance_page | governance, leadership moves, organization changes | https://www.hba.gr/en/hba |
| high | HERMES / AXIA – ATHEX issuer disclosure system | regulated_disclosure_submission_system | leadership moves, organization changes, board changes | https://hermes.athexgroup.gr/ |
| high | HR Awards (Boussias Events) — Winners & Past Winners | hr_award_program | hiring, jobs, organization changes, leadership moves | https://hrawards.boussiasevents.gr/winners-2025/ |
| high | HR Professional (hrpro.gr) — Μετακινήσεις Στελεχών column | hr_trade_media_people_moves_column | leadership moves, hiring, organization changes, jobs | https://hrpro.gr/category/metakinhseis-stelexwn/ |
| high | HR Professional — Interviews archive | hr_trade_press_interviews | leadership moves, organization changes | https://hrpro.gr/category/interviews/ |
| high | Hunt Scanlon Media - executive-search industry trade press | industry_trade_press | leadership moves, hiring, organization changes | https://huntscanlon.com/ |
| high | ICAP Employment Solutions / ICAP Outsourcing Solutions | staffing_outsourcing_provider | jobs, hiring, organization changes | https://icap-outsourcing.com/en/ |
| high | ICAP Executive Search (ICAP People / Employment Solutions, ICAP CRIF) | executive_search_firm_site | jobs, hiring, leadership moves | https://icapcareer.com/services/executive-search-and-selection/ |
| high | IG@work (Innovative Greeks / SEV) tech job platform | curated_tech_job_aggregator | jobs, hiring, organization changes | https://www.igwork.gr/search/greece/software-engineer-jobs |
| high | J. Safra Sarasin — corporate site (locations / newsroom) | corporate_pressroom | leadership moves, hiring, organization changes | https://www.jsafrasarasin.com/ |
| high | Key GR bank/payments executive LinkedIn profiles (people pages) | linkedin_people_page | leadership moves, organization changes | https://www.linkedin.com/in/paul-mylonas-886520b7/ |
| high | LinkedIn - challenger/cooperative bank company & jobs pages | professional_network | leadership moves, jobs, hiring | https://gr.linkedin.com/company/optimabank |
| high | ManpowerGroup Greece (Manpower.gr) — staffing & Finance/Banking solutions | staffing_agency_corporate_site | jobs, hiring, organization changes | https://www.manpower.gr/en |
| high | Natech Banking Solutions careers board on Workable | employer_ats_careers_board | jobs, hiring, organization changes | https://apply.workable.com/natech/ |
| high | Natech Banking Solutions — Careers (official) | company_careers_page | jobs, hiring, organization changes | https://natechbanking.com/careers/ |
| high | Natech Banking Solutions — LinkedIn company page(s) | linkedin_company_page | hiring, jobs, leadership moves, organization changes | https://www.linkedin.com/company/natechbankingsolutions/ |
| high | National Bank of Greece — LinkedIn company page | linkedin_company_page | jobs, hiring, leadership moves, organization changes | https://www.linkedin.com/company/national-bank-of-greece |
| high | Optima Bank - Board of Directors / Corporate Governance | official_governance_leadership_page | leadership moves, organization changes | https://www.optimabank.gr/en/about-us/corporate-governance/board-of-directors/ |
| high | Optima Bank - Careers / Human Resources page | official_careers_page | jobs, hiring | https://www.optimabank.gr/en/about-us/human-resources/theseis-ergasias/ |
| high | Optima bank — LinkedIn company page | linkedin_company_page | jobs, hiring, organization changes, leadership moves | https://www.linkedin.com/company/optimabank |
| high | People Management Executive Seminar (peoplemanagement.gr) — ACG / Boussias | hr_executive_seminar | leadership moves, organization changes | https://www.peoplemanagement.gr/ |
| high | Piraeus Financial Holdings – Investor Relations / Corporate Governance | issuer_investor_relations | leadership moves, board changes, organization changes | https://www.piraeusgroup.gr/el/enhmerwsh-ependytwn/etairikh-diakyvernhsh/piraeus-bank |
| high | Piraeus Group — Careers / Σταδιοδρομία στον Όμιλο | employer_careers_portal | jobs, hiring, organization changes | https://www.piraeusgroup.gr/el/stadiodromia-ston-omilo |
| high | Plum Fintech careers board on Workable (Athens engineering hub) | employer_ats_careers_board | jobs, hiring, organization changes | https://apply.workable.com/withplum/ |
| high | Randstad Hellas — Banking sector careers & job board | staffing_agency_jobs_board | jobs, hiring, organization changes | https://www.randstad.gr/professional-kariera/trapezikos-klados/ |
| high | Reuters — Greek banks / companies coverage | international_newswire | leadership moves, organization changes, hiring | https://www.reuters.com/site-search/?query=Greek%20banks |
| high | Revelio Labs — company employee-count / headcount pages (INDIRECT, LinkedIn-derived) | workforce_data_aggregator | hiring, organization changes, leadership moves, jobs | https://www.reveliolabs.com/companies/eurobank/employees/ |
| high | Search-firm LinkedIn company pages (placement/appointment announcements) | social_media_company_page | leadership moves, hiring, jobs | https://www.linkedin.com/company/stanton-chase---executive-search-athens |
| high | Snappi (Piraeus/Natech neobank) careers board on Workable | employer_ats_careers_board | jobs, hiring, organization changes | https://apply.workable.com/snappibank/?lng=en |
| high | Snappi - Careers page | official_careers_page | jobs, hiring | https://www.snappibank.com/en/careers/ |
| high | Snappi - Meet the team (leadership) page | official_governance_leadership_page | leadership moves, organization changes | https://www.snappibank.com/en/meet-the-team/ |
| high | Tiresias - Press Office (Γραφείο Τύπου) | official_press_release_hub | organization changes, leadership moves | https://www.tiresias.gr/el/grafeio-typou/ |
| high | WealthBriefing — Global Wealth Management senior/executive moves & Greece coverage | specialist_wealth_trade_press | leadership moves, hiring, organization changes | https://www.wealthbriefing.com/ |
| high | Workforce — daily HR newsletter (Boussias Media) | hr_daily_newsletter_people_moves | leadership moves, hiring, organization changes, jobs | https://subscriptions.boussiasmedia.gr/workforce-el.html |
| high | data.gov.gr - OAED registered unemployment dataset + API | open_data_api | jobs, hiring | https://data.gov.gr/dataset/oaed_unemployment |
| high | eFinancialCareers — Greece | specialist_finance_job_board | jobs, hiring | https://www.efinancialcareers.co.uk/jobs/in-greece |
| high | epixeiro.gr — Μετακινήσεις Στελεχών column | business_media_people_moves_column | leadership moves, hiring, organization changes, jobs | https://www.epixeiro.gr/metakiniseis-stelexon |
| high | ΔΗ.ΣΥ.Ε. - Δημοκρατική Συνδικαλιστική Ενότητα (Attica Bank union faction) | enterprise_union_faction | collective_dismissals, restructuring, organization_changes, leadership_moves | https://www.dhsye.gr/ |
| high | ΔΥΠΑ - Στατιστικά στοιχεία (registered unemployment, employment flows, programme beneficiaries) | official_statistics_portal | jobs, hiring | https://www.dypa.gov.gr/statistika |
| high | ΕΕΤ — Γενική Γραμματεία / Συντονιστικές Επιτροπές (HBA Secretariat & Steering Committees) | association_governance_page | organization changes, leadership moves, governance | https://www.hba.gr/Association/Info/steeringcommittee |
| high | ΕΕΤ — Γενικός Γραμματέας / Γενικός Διευθυντής (HBA General Secretary / General Manager) | association_governance_page | leadership moves, organization changes, governance | https://www.hba.gr/association/info/generalsecretary |
| high | ΕΕΤ — Εκτελεστική Επιτροπή (HBA Executive Committee) | association_governance_page | leadership moves, organization changes, governance | https://www.hba.gr/Association/Info/executive |
| high | ΠΑ.ΣΥ.Π.Ε. - Πανελλήνιος Σύλλογος Προσωπικού Eurobank Εργασίας | enterprise_bank_union | voluntary_exit_scheme, restructuring, organization_changes, branch_closures | https://www.pansype.gr/ |
| high | ΠΣ ΕΡΓΑΝΗ ΙΙ - myergani.gov.gr (employer filing portal) | government_filing_system | jobs, hiring, org_changes | https://myergani.gov.gr/ |
| high | ΣΕΤΑΠ - Σύλλογος Εργαζομένων Τράπεζας Αγροτικής/Πειραιώς (OTOE & Κινητοποιήσεις categories) | enterprise_bank_union | collective_dismissals, branch_closures, restructuring, organization_changes | https://setap.gr/category/anakinosis/kinitopiisis/ |
| high | ΣΕΤΠ - Σύλλογος Εργαζομένων Τράπεζας Πειραιώς (announcements) | enterprise_bank_union | voluntary_exit_scheme, collective_dismissals, branch_closures, restructuring, organization | https://www.setp.gr/anakoinwseis/anakoinwseissetp |
| high | ΣΠ Alpha Bank (SAB) - Σύλλογος Προσωπικού Alpha Bank | enterprise_bank_union | voluntary_exit_scheme, restructuring, organization_changes, leadership_moves | https://sab.gr/ |
| medium | ACCA Careers — Greece Banking & Financial Services | professional_body_job_board | jobs, hiring, organization changes | https://jobs.accaglobal.com/jobs/greece/banking-and-financial-services/ |
| medium | AIMS International Greece | executive_search_firm_site | hiring, leadership moves | https://www.aimsinternational.com/ |
| medium | Actionline — Greek HR / recruitment & staffing firm | staffing_agency_corporate_site | jobs, hiring | https://www.actionline.gr/ |
| medium | Adecco Greece — job listings (banking/BPO placements) | staffing_agency_listings | jobs, hiring | https://www.adecco.gr/jobs/ |
| medium | Aegean Baltic Bank - Career Opportunities page | official_careers_page | jobs, hiring | https://www.aegeanbalticbank.com/en/meet-abbank/manpower/career-opportunities-abbank |
| medium | Aegean Baltic Bank - Workable jobs portal | ats_job_board | jobs, hiring | https://apply.workable.com/aegean-baltic-bank/ |
| medium | Alexander Hughes Greece (HR Quest) | executive_search_firm_site | hiring, leadership moves | https://www.alexanderhughes.com/office/athens/ |
| medium | Alpha Bank — Distinctions / Other recent distinctions | bank_awards_page | organization changes, hiring, leadership moves | https://www.alpha.gr/en/Group/the-company/distinctions/Other-recent-distinctions |
| medium | Alpha Bank — Management Team / Governance | corporate_governance_page | leadership moves, organization changes | https://www.alpha.gr/en/Group/advocating-sound-governance-practices/management/management |
| medium | BOUSSIAS — Human Resources hub (portfolio index) | media_portfolio_index | leadership moves, organization changes | https://www.boussias.com/human-resources/ |
| medium | BusinessDaily.gr – Stock Exchange Announcements (Χρηματιστηριακές Ανακοινώσεις) | media_regulated_announcement_mirror | leadership moves, board changes, organization changes | https://www.businessdaily.gr/hrimatistiriakes-anakoinoseis |
| medium | Central Banking (centralbanking.com) — People | central_banking_trade_press | leadership moves, organization changes | https://www.centralbanking.com/central-banks/governance/people |
| medium | Cooperative Bank of Karditsa - SmartCV careers portal | ats_job_board | jobs, hiring | https://apply.smartcv.co/bankofkarditsa/ |
| medium | Cornerstone International Group - Greece / Cornerstone SEE | executive_search_firm_site | hiring, leadership moves | https://www.cornerstone-group.com/offices/cornerstone-greece/ |
| medium | DealNews.gr — Επιχειρήσεις / fintech coverage | business_news_portal_section | organization_changes, leadership_moves | https://www.dealnews.gr/epixeiriseis/ |
| medium | Delano / Paperjam (Luxembourg) — Greek wealth-hub coverage | regional_finance_press | leadership moves, organization changes | https://delano.lu/ |
| medium | Deloitte Greece - Executive Search & Selection | professional_services_search_practice | hiring, leadership moves | https://www.deloitte.com/gr/en/services/consulting/services/executive-search-selection-deloittegreece-executive-search-selection-services.html |
| medium | Deutsche Bank — corporate media / Private Bank newsroom | corporate_pressroom | leadership moves, hiring, organization changes | https://www.db.com/news |
| medium | Diversity Charter Greece — Signatories register | diversity_charter_membership | organization changes, hiring, leadership moves | https://diversity-charter.gr/signatories/ |
| medium | Diversity, Equity & Inclusion Awards (Boussias / Diversity Charter Greece) | diversity_award_program | organization changes, hiring, leadership moves | https://www.diversityawards.gr/ |
| medium | EURES — European Job Mobility Portal (Greece) | public_job_portal | jobs, hiring | https://europa.eu/eures/portal/jv-se/home?lang=en |
| medium | Elevate Greece — Registry portal (registry.elevategreece.gov.gr) | government_registry_portal | organization changes, jobs | https://registry.elevategreece.gov.gr/ |
| medium | EuroTechJobs — Greece software/developer listings | tech_job_aggregator | jobs, hiring | https://www.eurotechjobs.com/jobs/greece |
| medium | Eurobank — Our Awards page | bank_awards_page | organization changes, hiring, leadership moves | https://www.eurobank.gr/en/group/about-eurobank/eurobank-awards |
| medium | Finloup — kariera.gr company profile & about page | job_board_company_profile | jobs, hiring | https://www.kariera.gr/en/companies/finloup |
| medium | GR.EC.A — Press Releases / News (Δελτία Τύπου) | association_press_feed | leadership moves, organization changes | https://www.greekecommerce.gr/category/news/deltia-tipou/ |
| medium | Global Finance Magazine (gfmag.com) | international_finance_magazine | leadership moves, organization changes | https://gfmag.com/ |
| medium | Great Place to Work Hellas — Best Workplaces Hellas benchmark | workplace_benchmark | organization changes, hiring | https://greatplacetowork.gr/ |
| medium | Greek Fintech Cluster — LinkedIn company page | social_media_org_page | leadership moves, hiring, organization changes | https://www.linkedin.com/company/greek-fintech-cluster |
| medium | Greek Fintech Hub — NBG events/news page | bank_ecosystem_events_page | organization changes, leadership moves | https://www.nbg.gr/en/business/business-seeds/news-events/ekdiloseis-greek-fintech-hub-karatza |
| medium | GreekReporter (greekreporter.com) — Greek Banks tag | english_diaspora_news | jobs, organization changes, leadership moves | https://greekreporter.com/tag/greek-banks/ |
| medium | HR Community Conference & Awards (hrcommunity.gr) | hr_community_platform | organization changes, leadership moves | https://hrcommunity.gr/ |
| medium | HR in Action Conference (Boussias Events) | hr_conference | leadership moves, organization changes | https://hrinaction.boussiasevents.gr/ |
| medium | HRIMA Business Awards & Digital Finance Awards (ethos / Boussias) | awards_gala_roster | leadership moves, organization changes, hiring | https://ethosevents.eu/en/event/hrima-business-awards-2025-en/ |
| medium | IMH Banking, Payments & FinTech Forum & EXPO (agenda & speakers) | conference_speaker_roster | leadership moves, organization changes | https://banking.imhbusiness.com/agenda/ |
| medium | Issuer corporate/investor-relations & 'νομιμοποιητικά έγγραφα' pages (banks & PSPs) | primary issuer disclosure (corporate governance / press) | leadership moves, board appointments, hiring, organization changes | https://www.piraeusbank.gr/el/support/katalogos-nomimopoihtikwn-eggrafwn |
| medium | J.P. Morgan Careers (Oracle Cloud) — Athens roles | corporate_careers_portal | jobs, hiring | https://jpmc.fa.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1001/jobs?location=Athens,+Attica,+Greece |
| medium | J.P. Morgan Greece — corporate 'About us' + Private Bank EMEA Greece page | corporate_pressroom | leadership moves, organization changes, jobs | https://www.jpmorgan.com/GR/en/about-us |
| medium | JobInAthens.com — English-speaking professionals in Greece | expat_job_board | jobs, hiring | https://jobinathens.com/ |
| medium | KPMG People Excellence Awards Greece | hr_award_program | organization changes, hiring, leadership moves | https://peopleexcellenceawards.kpmg.gr/ |
| medium | KiTalent - Athens executive search / banking recruitment | executive_search_firm_site | jobs, hiring, leadership moves | https://kitalent.com/athens-greece-executive-search |
| medium | Marketing Week (marketingweek.gr) — Μετακινήσεις Στελεχών tag | sector_trade_media_people_moves_column | leadership moves, hiring, organization changes | https://marketingweek.gr/tag/metakiniseis-stelechon/ |
| medium | NCR Atleos - Careers | vendor_careers_portal | jobs, hiring, organization changes | https://www.ncratleos.com/careers |
| medium | Naftemporiki conferences portal (events.naftemporiki.gr) | event_calendar_pointer | leadership moves, organization changes | https://events.naftemporiki.gr/ |
| medium | Naftemporiki – Finance / Markets (Οικονομία & Αγορές) | financial_news_media | leadership moves, organization changes, board changes | https://www.naftemporiki.gr/finance/markets/ |
| medium | Oikonomikos Tachydromos (ot.gr) - fintech tag | local_financial_media_fintech_tag | organization changes, leadership moves | https://www.ot.gr/tag/fintech/ |
| medium | PAM Insight — TheWealthNet | specialist_wealth_trade_press | leadership moves, hiring, organization changes | https://www.paminsight.com/twn/ |
| medium | Panagiotis Kriaris FinTech Newsletter (Substack) | fintech_newsletter | leadership moves, organization changes | https://pkriaris.substack.com/ |
| medium | Plum Fintech — Workable ATS / careers | ats_job_feed | jobs, hiring | https://apply.workable.com/withplum/?lng=en |
| medium | Profile Software (Profile Systems & Software) – Investor Relations | issuer_investor_relations | leadership moves, board changes, organization changes | https://www.profilesw.com/about-us/investor-relations/ |
| medium | Proson.gr - jobs & recruitment news (bank hiring) | jobs_aggregator_media | jobs, hiring | https://www.proson.gr/ |
| medium | Proson.gr - ΑΣΕΠ / Εργασία | recruitment_news_aggregator | jobs, hiring | https://www.proson.gr/ergasia/asep |
| medium | QUALCO Group — LinkedIn company page(s) | linkedin_company_page | hiring, jobs, leadership moves, organization changes | https://www.linkedin.com/company/qualco |
| medium | Randstad Employer Brand Research — Greece | employer_brand_survey | hiring, jobs, organization changes | https://www.randstad.gr/en/about-us/press-releases/press/10-most-attractive-employers-greece-according-randstads-employer/ |
| medium | Randstad Greece — banking-sector vacancies (τραπεζικός κλάδος) | staffing_agency_listings | jobs, hiring, organization changes | https://www.randstad.gr/theseis-ergasias/s-trapezikos-klados/ |
| medium | Randstad Hellas — Workmonitor / HR trends / salary guide / market insights | staffing_market_report | hiring, organization changes | https://www.randstad.gr/hr-trends/ |
| medium | Reporter.gr – Stock Exchange Announcements (Χρηματιστήριο / Ανακοινώσεις) | media_regulated_announcement_mirror | leadership moves, board changes, organization changes | https://www.reporter.gr/chrhmatisthrio/anakoinwseis |
| medium | The Banker (FT group) | banking_trade_press | leadership moves, organization changes | https://www.thebanker.com/ |
| medium | The Fintech Times | fintech_trade_press | organization changes, hiring | https://thefintechtimes.com/ |
| medium | Tiresias - Careers (Καριέρα) | official_careers_page | jobs, hiring | https://www.tiresias.gr/el/kariera/ |
| medium | Total Rewards Conference (Boussias Events) | hr_conference | organization changes, leadership moves | https://totalrewards.boussiasevents.gr/ |
| medium | UNI Europa / UNI Global Union - Finance (Greek banking coverage) | international_union_federation | restructuring, collective_dismissals, organization_changes | https://www.uni-europa.org/news/greek-banking-unions-make-key-gains-in-new-sectoral-agreement/ |
| medium | Uni Systems - Careers | integrator_careers_portal | jobs, hiring, organization changes | https://www.unisystems.com/careers/ |
| medium | Wellfound (ex-AngelList) — Athens / Greece startup tech jobs | startup_job_platform | jobs, hiring, organization changes | https://wellfound.com/location/athens-greece |
| medium | Workable public jobs board (jobs.workable.com) - vendor aggregator | ats_aggregator | jobs, hiring | https://jobs.workable.com/ |
| medium | aftodioikisi.gr - Εργασιακά (union/dismissal reporting) | national_media_labor | voluntary_exit_scheme, collective_dismissals, branch_closures, restructuring | https://www.aftodioikisi.gr/ergasiaka-asfalistika/ |
| medium | e-EFKA (Ηλεκτρονικός Εθνικός Φορέας Κοινωνικής Ασφάλισης) | public_social_security_body | jobs, hiring, organization changes | https://www.e-efka.gov.gr/el |
| medium | finews.com — international private-banking moves | specialist_wealth_trade_press | leadership moves, hiring | https://www.finews.com/ |
| medium | kariera.gr - job board (challenger-bank listings) | jobs_aggregator_media | jobs, hiring | https://www.kariera.gr/companies/attica-bank-sa |
| medium | kariera.gr — Greek job board (finance/IT filters) | job_board_aggregator | jobs, hiring | https://www.kariera.gr/en/jobs?category=FINANCE,IT |
| medium | mononews.gr — business/banking desk (fintech leadership coverage) | business_media | leadership moves, organization changes | https://www.mononews.gr/business |
| medium | netweek.gr — Μετακινήσεις Στελεχών tag | sector_trade_media_people_moves_column | leadership moves, hiring, organization changes | https://netweek.gr/tag/%CE%BC%CE%B5%CF%84%CE%B1%CE%BA%CE%B9%CE%BD%CE%AE%CF%83%CE%B5%CE%B9%CF%82-%CF%83%CF%84%CE%B5%CE%BB%CE%B5%CF%87%CF%8E%CE%BD/ |
| medium | powergame.gr — Τράπεζες section | national_financial_media | leadership moves, hiring, organization changes | https://www.powergame.gr/trapezes |
| medium | ΔΥΠΑ - News / Ανακοινώσεις (programme announcements) | government_news_feed | hiring, jobs | https://www1.dypa.gov.gr/en/news |
| medium | ΕΕΔΕ (Hellenic Management Association) & its HR institute (ΕΙΜΑΔ) | management_association_hr_institute | leadership moves, organization changes | https://www.eede.gr/ |
| medium | Εφημερίδα των Συντακτών (efsyn.gr) - Εργασιακά / Οικονομία | national_media_labor | collective_dismissals, restructuring, branch_closures, organization_changes | https://www.efsyn.gr/oikonomia/ergasiaka |
| medium | ΣΕΥΤΠΕ - Σύλλογος Εργαζομένων στις Υπηρεσίες της Τράπεζας Πειραιώς | enterprise_bank_union | restructuring, organization_changes, branch_closures | https://www.seytpe.gr/ |
| medium | ΣΥΓΤΕ - Σύλλογος Υπαλλήλων Γενικής Τράπεζας | enterprise_bank_union | branch_closures, restructuring, organization_changes | https://sygte.gr/ |
| medium | ΣΥΤΑΤΕ - Σύλλογος Εργαζομένων Εθνικής Τράπεζας | enterprise_bank_union | voluntary_exit_scheme, restructuring, organization_changes, branch_closures | https://www.sytate.gr/ |
| low | BEYOND Expo / AI Fractures Forum (Thessaloniki, Metropolitan Expo) | conference_speaker_roster | leadership moves, organization changes | https://www.beyond-expo.gr/ |
| low | Cooperative Bank of Central Macedonia - official site (cmbank.gr) | official_bank_site | organization changes, jobs | https://web.cmbank.gr/ |
| low | Euromoney (euromoney.com) | international_finance_magazine | leadership moves, organization changes | https://www.euromoney.com/ |
| low | Glassdoor - vendor jobs & office pages (Greece) | job_board_aggregator | jobs, hiring, organization changes | https://www.glassdoor.com/Jobs/Euronet-Athens-Jobs-EI_IE6640.0,7_IL.8,14_IC2580540.htm |
| low | Greek Fintech Cluster — Medium blog (GFC) | association_blog | organization changes, jobs | https://medium.com/greek-fintech-cluster-gfc |
| low | Intracom Telecom - Job Opportunities | integrator_careers_portal | jobs, hiring | https://www.intracom-telecom.com/en/career/offers.htm |
| low | JUST ONE - Recruitment & Executive Search (Athens) | recruitment_search_agency | jobs, hiring | https://www.justone.gr/ |
| low | N2Growth Greece (Rebecca Pitsika) | executive_search_firm_site | hiring, leadership moves | https://www.n2growth.com/team/rebecca-pitsika/ |
| low | National Bank of Greece — Human Resources / Our People pages | bank_hr_page | hiring, organization changes, jobs | https://www.nbg.gr/el/omilos/anthrwpino-dunamiko |
| low | Randstad Greece - Executive Search service | staffing_firm_search_practice | jobs, hiring | https://www.randstad.gr/ergodotis/ypiresies/executive-search/ |
| low | Thessaloniki HELEXPO Forum - speakers-per-panel | conference_speaker_roster | leadership moves, organization changes | https://www.thessaloniki-helexpo-forum.gr/en/speakers-per-panel |
| low | Women Empowerment Awards Greece (Boussias) | diversity_award_program | organization changes, leadership moves, hiring | https://www.womenawards.gr/ |
| low | advertising.gr — Careers / Μετακινήσεις στελεχών | sector_trade_media_people_moves_column | leadership moves, hiring | https://www.advertising.gr/careers/ |
| low | dnews.gr — 'Market Maven' business column | business_column | organization_changes, leadership_moves | https://www.dnews.gr/eidhseis/market-maven |
| low | finloup — LinkedIn company page | linkedin_company_page | hiring, jobs, organization changes | https://gr.linkedin.com/company/finloup |
| low | linq (app.linq.co) — Greek job board | general_job_board | jobs, hiring, organization changes | https://app.linq.co/el/job-board |
| low | newjobs.gr — Greek job aggregator (company pages) | job_board_aggregator | jobs, hiring | https://www.newjobs.gr/en/company/5vMoT42W6aj5iyzPi5oPLZ/jobs-at-snappi |
| low | selfservice.gr — Μετακινήσεις Στελεχών tag | sector_trade_media_people_moves_column | leadership moves, organization changes | https://selfservice.gr/tag/%CE%BC%CE%B5%CF%84%CE%B1%CE%BA%CE%B9%CE%BD%CE%AE%CF%83%CE%B5%CE%B9%CF%82-%CF%83%CF%84%CE%B5%CE%BB%CE%B5%CF%87%CF%8E%CE%BD/ |
| low | techpress.gr — Μετακινήσεις στελεχών (transfers) category | sector_trade_media_people_moves_column | leadership moves, hiring | https://www.techpress.gr/index.php/archives/category/news/transfers |
| low | voucher.gov.gr - DYPA training programmes (Recovery Fund, incl. financial-literacy/digital reskilling) | government_programme_portal | hiring, org_changes, jobs | https://voucher.gov.gr/project/view-dypa |
| low | Οικονομικός Ταχυδρόμος (ot.gr) — Τράπεζες | national_financial_media | leadership moves, organization changes | https://www.ot.gr/category/oikonomia/trapezes/ |
| low | Ριζοσπάστης (rizospastis.gr) & 902.gr - class-labour press (banking) | national_media_labor | collective_dismissals, restructuring, organization_changes | https://www.rizospastis.gr/ |

## A6 · Vendors & Competitors — 61 banking sources

| Priority | Source | Type | Topics | URL |
|---|---|---|---|---|
| critical | Alpha Services and Holdings - Group Results and Reporting | bank_investor_relations_portal | vendors, partnerships, case studies, competitors | https://www.alpha.gr/en/group/investor-relations/group-results-and-reporting |
| critical | Infosys Finacle — Newsroom / press releases (NBG 'Cosmos') | vendor_press_release | vendors, case studies, partnerships, competitors | https://www.infosys.com/newsroom/press-releases.html |
| critical | Netcompany-Intrasoft — Banking (PROFITS core, case studies) | vendor_case_study | vendors, case studies, competitors, partnerships | https://www.netcompany-intrasoft.com/banking/our-solutions/profits-core-banking |
| critical | TED — Tenders Electronic Daily (EU Official Journal Supplement) | eu_procurement_portal | vendors, competitors, case studies, partnerships | https://ted.europa.eu/en/search/ |
| high | ACI Worldwide — Newsroom / Press Releases | vendor_press_release_index | vendors, partnerships, case studies, competitors | https://www.aciworldwide.com/newsroom/press-releases |
| high | Alpha Bank - Corporate Transformation (IR programme page) | transformation_programme_disclosure | case studies, partnerships, vendors | https://www.alpha.gr/en/Group/investor-relations/corporate-transformation-2025 |
| high | Alpha Bank - Financial Statements (Bank and Group) | bank_financial_statements | vendors, case studies | https://www.alpha.gr/en/Group/investor-relations/group-results-and-reporting/Financial-Statements-Bank-and-Group |
| high | Alpha Bank Media Centre - Deltia Typou (EL) | corporate_press_room | vendors, partnerships, case studies | https://www.alpha.gr/el/omilos/Grafeio-Typou/Press-Releases |
| high | Alpha Services and Holdings - Investor Presentations archive | results_presentation_deck | vendors, partnerships, case studies | https://www.alpha.gr/en/Group/investor-relations/presentations |
| high | Athens Exchange / Euronext Athens - regulatory disclosures (Optima, CrediaBank, Profile) | regulated_disclosure_feed | vendors, partnerships, competitors | https://www.athexgroup.gr/en/optima-bank |
| high | BoG — Credit institution establishment & operation / authorisation (EN) | regulator_authorisation_framework_page | competitors, partnerships, vendors | https://www.bankofgreece.gr/en/main-tasks/supervision/credit-institutions/establishment-and-operation |
| high | Business Daily - Technology & Banks sections | business_media | vendors, partnerships, competitors, case studies | https://www.businessdaily.gr/tehnologia |
| high | CrediaBank (ex-Attica Bank / Pancreta) Newsroom & Investor Relations | bank_press_room | vendors, partnerships, competitors, case studies | https://www.crediabank.com/en/ |
| high | ECB Banking Supervision — press releases & stress-test reports | regulator_press_and_reports | competitors, case_studies | https://www.bankingsupervision.europa.eu/press/pr/html/index.en.html |
| high | Epsilon Net — FinTech Solutions (NBG open-banking partner) | vendor_website | vendors, partnerships | https://epsilonnet.gr/en/eidos-logismikou/fintech-solutions/ |
| high | European Investment Bank (EIB) — press releases & project portal (Greece) | eu_financing_body_project_register | partnerships, case_studies | https://www.eib.org/en/projects/all/ |
| high | FintechFutures — Challenger banks / funding desk | trade_media | competitors, partnerships, vendors | https://www.fintechfutures.com/bankingtech/challenger-banks |
| high | FintechFutures — core-banking technology news (Greek deals) | industry_news_aggregator | vendors, case studies, competitors, partnerships | https://www.fintechfutures.com/category/core-banking-system/ |
| high | Found.ation — FWD Greece: Innovation Pulse ecosystem map | ecosystem_map_report | competitors, partnerships, case studies | https://thefoundation.gr/innovation-platform/our-publications/fwd-greece-innovation-pulse/ |
| high | Global Finance — World's Best Digital Banks / Best Bank awards (Greece winners) | international_awards_programme | competitors, case studies | https://gfmag.com/award/winner-announcements/ |
| high | Google Play / Apple App Store - Greek bank app listings (vendor fingerprinting) | app_store_metadata | vendors, partnerships | https://play.google.com/store/apps/details?id=eu.afse.omnia.attica |
| high | Greek business/banking press (Business Daily, Capital, Banks.com.gr, Mononews, BankingNews) | financial_media | vendors, partnerships, competitors, case studies | https://www.businessdaily.gr/epiheiriseis/46638_i-profile-dimioyrgise-mia-omni-channel-platforma-gia-tin-optima-bank |
| high | Hellenic Bank Association (ΕΕΤ) — European Banking Union pages (SSM/SRM/EBA) | industry_association_legal_index | competitors, partnerships, case_studies | https://www.hba.gr/EuropeanAssociation |
| high | IBS Intelligence — case studies & IBSi news (banking tech) | industry_news_aggregator | vendors, case studies, competitors | https://ibsintelligence.com/ |
| high | NETinfo — Digital banking case studies / news | vendor_case_study | vendors, case studies, partnerships, competitors | https://netinfo.eu/latest-news/ |
| high | Natech Banking Solutions - Customers / News (core-banking vendor for cooperatives) | vendor_customer_page | vendors, case studies, partnerships | https://natechbanking.com/customers/cooperative-bank-of-karditsa/ |
| high | Open Business Portal — Γενική Γραμματεία Εμπορίου δημοσιότητα search (openbusiness-portal.mindev.gov.gr) | official_business_registry | vendors, competitors | https://openbusiness-portal.mindev.gov.gr/anazitisi-dimosiotitas-epicheirisis/ |
| high | Oracle — Financial Services Customer Stories | vendor_case_study_library | vendors, case studies, partnerships | https://www.oracle.com/industries/financial-services/customer-stories.html |
| high | Piraeus Group Press Office - Announcements & Press Releases (EN) | corporate_press_room | vendors, partnerships, case studies | https://www.piraeusgroup.gr/en/press-office/announcements-and-press-releases |
| high | Profile Software — Case Studies (Greek) | vendor_case_study | vendors, case studies, competitors, partnerships | https://www.profilesw.com/el/insight_category/case-studies-el/?_insight_category=case-studies-el |
| high | Profile Software — English clients / case studies | vendor_customer_page | vendors, case studies, partnerships | https://www.profilesw.com/en/ |
| high | banks.com.gr — Greek banking news (vendor tags) | local_business_media | vendors, case studies, competitors, partnerships | https://banks.com.gr/tag/profile-software/ |
| high | ethosEVENTS – Digital Banking Forum (event hub, sponsors & agenda) | conference_organizer_event_page | vendors, competitors, partnerships | https://ethosevents.eu/en/upcoming-events/ |
| high | ethosEVENTS – Απολογισμοί (post-event recaps) section | post_event_recap_archive | vendors, competitors, partnerships | https://ethosevents.eu/apologismoi/10th-digital-banking-forum-apologismos/ |
| medium | Advantage FSE (AFSE) - Omnia digital-banking platform (vendor) | vendor_customer_page | vendors, partnerships, case studies | https://www.afse.eu/platform/ |
| medium | Apple App Store - Greek banking/payment app ratings & reviews | app_store_reviews | vendors, competitors, case studies | https://apps.apple.com/gr/app/eurobank-mobile-app/id364587747?l=el |
| medium | Attica Bank - Investor Relations / Annual Reports | bank_annual_report | competitors, vendors, case studies | https://atticabank.gr/en/investors/useful-info/annual-reports |
| medium | BankingNews.gr - Banking News (Τραπεζικά Νέα) | sector_specialist_press | partnerships, vendors, competitors | https://www.bankingnews.gr/trapezika-nea |
| medium | Cooperative Bank of Chania (Chania Bank) - website & eBanking | bank_corporate_site | vendors, partnerships | https://www.chaniabank.gr/en/home/ |
| medium | Cooperative Bank of Karditsa - Announcements (Nea Anakoinoseis) | bank_press_room | vendors, partnerships, case studies | https://www.bankofkarditsa.com.gr/el/trapeza/nea-anakoinoseis |
| medium | EU-Startups — Greek fintech coverage & directory | trade_media | competitors, partnerships, vendors | https://www.eu-startups.com/?s=greece+fintech |
| medium | FStech | international_trade_press | vendors, partnerships, case_studies | https://www.fstech.co.uk/ |
| medium | FinTech Futures — Banking Tech Awards & PayTech Awards (winners/shortlists) | international_awards_programme | vendors, case studies, partnerships | https://www.fintechfutures.com/paytech |
| medium | FintechFutures / Retail Banker International - branches & ATMs | trade_press | vendors, partnerships, case studies | https://www.fintechfutures.com/branches-atms/greece-s-epirus-bank-partners-ncr-atleos-to-expand-atm-network |
| medium | Grant Thornton Greece — Financial Services Insider & insights | advisory_firm_publications_index | competitors, partnerships, case studies | https://www.grant-thornton.gr/en/insights/ |
| medium | IBS Intelligence - Greek core-banking/vendor news | trade_press | vendors, partnerships, case studies, competitors | https://ibsintelligence.com/?s=Greece+bank |
| medium | Indeed Greece — job aggregator | job_aggregator | vendors, competitors | https://gr.indeed.com/Banking-jobs |
| medium | ReviewIt.gr - Banks category (Τράπεζες) | consumer_review_aggregator | competitors, vendors, case studies | https://www.reviewit.gr/category/trapezes/ |
| medium | The Banker — Bank of the Year Awards (Greece) | international_awards_programme | competitors, case studies | https://www.thebanker.com/awards |
| medium | diaNEOsis — Greek financial-sector research & proposals | policy_think_tank | competitors, partnerships, case studies | https://www.dianeosis.org/en/ |
| medium | ethosEVENTS – Digital Finance Forum | conference_organizer_event_page | vendors, competitors, partnerships | http://digitalfinance.ethosevents.eu/en/home/ |
| medium | gov.gr — ΓΕΜΗ publicity data & certificates service pages | government_service_catalog | vendors | https://www.gov.gr/en/upourgeia/upourgeio-anaptuxes/anaptuxes/stoikheia-demosiotetas-emporikon-epikheireseon-eggegrammenon-sto-geme |
| medium | promitheies.gr — public-tenders aggregator (IT/banking branches) | procurement_aggregator | vendors, competitors | https://www.promitheies.gr/branch/ypiresies-pliroforikis-hlektronikon-ypologiston |
| medium | Ε.Κ.ΠΟΙ.ΖΩ. - Ένωση Καταναλωτών (Financial complaints section) | consumer_association | competitors, vendors, case studies | https://www.ekpizo.gr/%CE%BA%CE%B1%CF%84%CE%B7%CE%B3%CE%BF%CF%81%CE%AF%CE%B1-%CE%B4%CF%81%CE%AC%CF%83%CE%B7%CF%82/%CF%87%CF%81%CE%B7%CE%BC%CE%B1%CF%84%CE%BF%CE%BF%CE%B9%CE%BA%CE%BF%CE%BD%CE%BF%CE%BC%CE%B9%CE%BA%CE%AC |
| low | Boussias – Sustainable Finance Conference | conference_organizer_event_page | vendors, partnerships | https://sustainablefinance.boussiasevents.gr/ |
| low | Business Voice - Digital / Digital Transformation section | business_media | vendors, case studies, partnerships | https://businessvoice.gr/digital |
| low | Fiserv — Case Studies / Resource Center | vendor_case_study_library | vendors, case studies | https://www.fiserv.com/en/about-fiserv/resource-center/case-studies.html |
| low | SAP Fioneer — Case Studies | vendor_case_study_library | vendors, case studies | https://www.sapfioneer.com/case-studies/ |
| low | SecNews.gr - cybersecurity trade news | cybersecurity_trade_press | vendors, case studies, competitors | https://www.secnews.gr/ |
| low | Winbank / Piraeus e-banking - System Downtime & Upgrade notices | provider_status_page | vendors, case studies | https://www.ebanking.piraeusbank.gr/el/Pages/System-Downtime-Upgrade.aspx |
| low | ΙΝΚΑ - Γενική Ομοσπονδία Καταναλωτών (INKA) complaints feed | consumer_association | competitors, vendors, case studies | https://www.inka.gr/?cat=5 |

## ⚠ Mixed banking+payments & unclassified — 846 sources (review before excluding)

These touch banking but also payments (or had no clear topic). Listed name + URL only so you can pull any into the banking list.

| Class | Source | Topics | URL |
|---|---|---|---|
| both | 13 Περιφερειακά Προγράμματα ΕΣΠΑ 2021-2027 (Regional Programmes / ΠΕΠ) — e.g. ΠΕΠ Αττικής | calls, procurement, ESPA/NSRF, regional programmes, municipalities, di | https://www.pepattikis.gr/view/article-stream-prosk-apof-2021-2027 |
| both | 1η ΥΠΕ Αττικής — Διαγωνισμοί (Health Region 1) | tenders, procurement, public contracts, award notices, hospital-paymen | https://1dype.gov.gr/category/diagonismoi/ |
| both | 1η ΥΠΕ Αττικής — Διαγωνισμοί (Health Region 1) | tenders, procurement, public contracts, award notices, hospital-paymen | https://www.1dype.gov.gr/category/%CE%B4%CE%B9%CE%B1%CE%B3%CF%89%CE%BD%CE%B9%CF%83%CE%BC%CE%BF%CE%AF/ |
| both | 2η ΔΥΠΕ Πειραιώς & Αιγαίου — Διαγωνισμοί (Health Region 2) | tenders, procurement, public contracts, award notices, hospital-paymen | https://www.2dype.gov.gr/ |
| both | A&O Shearman - Financial Services Horizon Report 2026 | regulation, deadlines, consultations | https://www.aoshearman.com/en/insights/financial-services-horizon-report-2026 |
| both | AADE (IAPR) — POS / cash-register interconnection & IRIS acceptance framework | regulation, deadlines, instant_payments, supervision, consultations | https://www.aade.gr/en/diasyndesi-pos-tameiakon-systimaton/diasyndesi-0 |
| both | AADE (Independent Authority for Public Revenue) - Immediate payment services / POS-cash register interconnection | IRIS-POS interconnection, myDATA, technical specifications, compliance | https://www.aade.gr/diasyndesi-pos-tameiakon-systimaton/ypiresies-amesis-pliromis |
| both | AADE (Independent Authority for Public Revenue) — Proclamations/Contests (Προκηρύξεις–Διαγωνισμοί) | procurement, tenders, IT systems, software changes, payments, e-paymen | https://www.aade.gr/prokiryxeis-diagonismoi |
| both | AADE — Annual Accountability & Planning Report (Έκθεση Απολογισμού και Προγραμματισμού) | market statistics, payment statistics, card statistics, cash usage | https://www.aade.gr/en/final-reports |
| both | AADE — POS / Cash-Register / Router Interface: Technical Manuals & Approved Models | procurement, public contracts, POS terminals, vendor models, NSP regis | https://www.aade.gr/en/interface-pos-cash-systems/technical-manuals-pos-cash-registers-routers |
| both | AADE — POS models for which a Declaration of Conformity has been submitted by Providers | procurement, certified POS models, terminal hardware, providers, publi | https://www.aade.gr/en/interface-pos-cash-systems/what-are-my-options/pos-models-which-declaration-conformity-has-been-submitted-providers |
| both | AADE — Registry of POS Providers (Acquirers & NSPs) that submitted Compliance Declarations | acquiring, NSP, POS, provider_registry, payments_infrastructure | https://www.aade.gr/en/providers-who-have-submitted-declaration-compliance |
| both | ACI Worldwide Investor News Releases | payments, cards, emv, instant_payments, wins | https://investor.aciworldwide.com/press-releases |
| both | ASEP Informational Portal (info.asep.gr) | jobs, hiring, leadership moves, organization changes | https://info.asep.gr/ |
| both | ASEP official portal (Ανώτατο Συμβούλιο Επιλογής Προσωπικού) | jobs, hiring, organization changes | https://www.asep.gr/ |
| both | ATHEX per-issuer announcements — Austriacard Holdings (issuer 1498) | material contracts, vendor disclosure, payments, award notices | https://athens.euronext.com/en/market-data/issuers/1498/announcements |
| both | ATHEX per-issuer announcements — National Bank of Greece (issuer 57) | material contracts, vendor disclosure, digital transformation | https://athens.euronext.com/en/market-data/issuers/57 |
| both | ATHEX — payments/fintech listed-issuer announcement streams (Epsilon Net, Real Consulting, Profile, ILYDA) | disclosures, annual reports, earnings, press releases | https://www.athexgroup.gr/en/market-data/issuers/976/announcements |
| both | AUSTRIACARD HOLDINGS — Investor Relations / Press Releases newsroom | procurement, card-personalization, security-print, ID, public-sector | https://www.austriacard.com/investor-relations-ac/press-releases-ac/ |
| both | Adecco Greece — job listings (θέσεις εργασίας) | hiring_signals, banking, payments, cards, IT | https://www.adecco.com/el-gr/ypopsifioi/theseis-ergasias |
| both | Aftodioikisi.gr — local-government & ΟΤΑ news portal (pointer / weak-signal) | procurement, public contracts, tenders | https://www.aftodioikisi.gr/ |
| both | Alpha Bank - Payment Services (PSD) page | regulation, compliance, supervision | https://www.alpha.gr/el/idiotes/support-center/pliromes-stin-europi/upiresies-pliromon-psd |
| both | Alpha Bank Careers (SAP SuccessFactors portal) | tenders, procurement, hiring signals, cards, POS, core banking, ISO 20 | https://careers.alpha.gr/viewalljobs/?locale=en_GB |
| both | Alpha Bank Group API Portal (developer portal & sandbox) | open banking API, AIS, PIS, sandbox, eIDAS QSealC | https://developer.api.alphabank.eu/ |
| both | Alpha Bank — 'Αντικαθιστούμε τις Mastercard με Visa' (official scheme-migration page) | scheme migration, card issuing, co-brand, re-issue, procurement signal | https://www.alpha.gr/en/retail/cards/antikathistoume-tis-mastercard-me-visa |
| both | Alpha Bank — Careers at Alpha Bank | hiring_signals, job_postings, digital_payments | https://www.alpha.gr/en/Group/human-resources/careers-at-alpha-bank |
| both | Alpha Bank — Corporate Announcements archive (Greek) | market statistics, card statistics, payment statistics | https://www.alpha.gr/el/omilos/arxeio-alpha-services-and-holdings/arxeio-enimerosis-ependuton/anakoinoseis |
| both | Alpha Bank — LinkedIn company page & Jobs tab | jobs, hiring, leadership moves, organization changes | https://www.linkedin.com/company/alpha-bank |
| both | Alpha Bank — careers portal (careers.alpha.gr) | core banking, IT hiring, DigiTech, procurement, tech stack | https://careers.alpha.gr/go/All-Jobs/9227855/ |
| both | Alpha Services and Holdings — Investor Relations portal (Results and Reporting) | card statistics, payment statistics, market statistics, ATM POS data | https://www.alpha.gr/en/group/investor-relations |
| both | American Banker / PaymentsSource — Greek payments-market coverage (EN cross-reference) | payments, vendor wins, M&A disclosures, banking | https://www.americanbanker.com/payments |
| both | American Express Greece — Merchant/Scheme Site | disclosures, partnerships, acceptance | https://www.americanexpress.com/gr/el/merchant/welcome-to-american-express.html |
| both | Andersen Legal Greece (Pistiolis-Triantafyllos & Associates) - FinTech / Banking insights | regulation, payments, supervision | https://gr.andersenlegal.com/practices/fintech/ |
| both | Argus Advisory Research — Greece Cards & Payments Market Report | card statistics, payment statistics, market statistics, ATM POS data | https://www.argusadvisoryresearch.com/reports/country-reports/europe/greece.html |
| both | Athens Bar Association (Δικηγορικός Σύλλογος Αθηνών) - recruitment notices | jobs, hiring | https://www.dsa.gr/ |
| both | Athens International Airport (AIA / DAA) — company & parking/e-parking | procurement, payment terminals, parking, contactless payments | https://www.aia.gr/el/corporate/etaireia |
| both | Athens International Airport (AIA/DAA) — Business Tenders & Digital Procurement Platform | tenders, procurement, public contracts, payment services | https://www.aia.gr/en/business/tenders |
| both | Attica Bank - Human Resources / Careers page | jobs, hiring, organization changes | https://www.atticabank.gr/en/group/human-resources/ |
| both | Attica Bank — LinkedIn company page | organization changes, leadership moves, hiring, jobs | https://gr.linkedin.com/company/attica-bank |
| both | Attiki Odos / national motorway concessionaires — electronic toll payment systems (e-PASS, interoperability) | toll payment, electronic payment, interoperability, payment acceptance | https://www.aodos.gr/en/diodia-e-pass/ |
| both | BIS Data Portal - CPMI Red Book retail payments, currency & related indicators (Greece) | payment statistics, card statistics, market statistics, cash usage | https://data.bis.org/topics/CPMI_CT |
| both | BPC Banking Technologies - SmartVista/SmartSwitch (core switching & ATM/POS platform vendor for DIAS) | vendor signals, procurement, switching, instant payments | https://www.bpcbt.com/blog/dias |
| both | Bank of Greece - Conferences & Workshops (Ημερίδες και συνέδρια) | press releases, disclosures | https://www.bankofgreece.gr/statistika/agora-akinhtwn/hmerides-kai-synedria |
| both | Bank of Greece - IRIS information portal | disclosures | https://iris.bankofgreece.gr/ |
| both | Bank of Greece - Instant Payments (Άμεσες Πληρωμές, retail payments section) | SEPA instant credit transfer, TIPS, instant payments oversight, IPR | https://www.bankofgreece.gr/kiries-leitourgies/systhmata-plhrwmwn-diakanonismou/pliromes-lianikis/ameses-plhrwmes |
| both | Bank of Greece - Instant Payments (Άμεσες Πληρωμές, retail payments section) | SEPA instant credit transfer, TIPS, instant payments oversight, IPR | https://www.bankofgreece.gr/kiries-leitourgies/systhmata-plhrwmwn-diakanonismou/pliromes-lianikis/syxnes-erwthseis-gia-tis-ameses-plhrwmes |
| both | Bank of Greece - Transactions and card fraud statistics | card statistics, payment statistics, ATM POS data | https://www.bankofgreece.gr/en/statistics/payment-cards-transaction-statement-and-fraud |
| both | Bank of Greece — Announcements search (parent hub, all categories) | tenders, procurement, press_releases | https://www.bankofgreece.gr/enimerosi/grafeio-typoy/anazhthsh-enhmerwsewn |
| both | Bank of Greece — Digital euro national page (EN & EL) | digital euro, CBDC, Eurosystem, payments modernisation | https://www.bankofgreece.gr/en/the-euro/digital-euro |
| both | Bank of Greece — Events / Εκδηλώσεις | payments, regulatory, financial stability, central bank events | https://www.bankofgreece.gr/en/news-and-media/events-list |
| both | Bank of Greece — FinTech Innovation Hub (Κόμβος Καινοτομίας FinTech) | fintech, innovation hub, regulatory guidance, payments, supervision | https://www.bankofgreece.gr/kiries-leitourgies/epopteia/komvos-kainotomias-fintech |
| both | Bank of Greece — FinTech Innovation Hub (Κόμβος Καινοτομίας FinTech) | fintech regulation, innovation hub, early-stage actors, sandbox | https://www.bankofgreece.gr/en/main-tasks/supervision/fintech-innovation-hub |
| both | Bank of Greece — Financial Stability Review (biannual publication) | financial stability, payment systems, payment institutions, e-money, e | https://www.bankofgreece.gr/en/publications-and-research/publications/financial-stability-review |
| both | Bank of Greece — Instant Payments (retail payment systems, EN) | instant payments, TIPS, SCT Inst, IRIS, DIAS, retail payment systems | https://www.bankofgreece.gr/en/main-tasks/payment-systems-and-settlements/retail-payment-strategy/instant-payments |
| both | Bank of Greece — LinkedIn company page | hiring, jobs, leadership moves, organization changes | https://www.linkedin.com/company/bank-of-greece |
| both | Bank of Greece — MiCAR (crypto-asset markets) supervisory page | regulation, supervision, deadlines | https://www.bankofgreece.gr/kiries-leitourgies/epopteia/micar-kanonismos-ee-2023_1114-gia-tis-agores-kryptostoixeion |
| both | Bank of Greece — Open Data Portal: Payments Statistics dataset | payments statistics, open data, cards, transaction volumes, fraud | https://opendata.bankofgreece.gr/en/dataset/53 |
| both | Bank of Greece — Oversight of payment systems and payment instruments (EN) | payment systems oversight, SIPS, payment instruments, financial market | https://www.bankofgreece.gr/en/main-tasks/financial-stability/oversight-of-financial-market-infrastructures/oversight-of-payment-systems-and-payment-instruments |
| both | Bank of Greece — PSD2 Useful Information page | PSD2, national_identification_number, EBA_register, regulatory_framewo | https://www.bankofgreece.gr/en/main-tasks/supervision/psd2-info |
| both | Bank of Greece — Payment Systems & Means of Payment Oversight (Directorate of Payment & Settlement Systems) | oversight, instant payments, IRIS, SEPA, infrastructure, public contra | https://www.bankofgreece.gr/kiries-leitourgies/xrhmatopistwtikh-statherothta/epivlepsh-twn-ypodomwn-toy-xrhmatopistwtikoy-systhmatos/epivlepsh-systhmatwn-plhrwmwn-kai-meswn-plhrwmhs |
| both | Bank of Greece — Payment Systems and Settlements section (TARGET-GR, BOGS/T2S, DIAS, ACO) | public contracts, procurement | https://www.bankofgreece.gr/kiries-leitourgies/systhmata-plhrwmwn-diakanonismou |
| both | Bank of Greece — Payment systems and settlements (TARGET-GR operator page) | procurement, tenders | https://www.bankofgreece.gr/en/main-tasks/payment-systems-and-settlements |
| both | Bank of Greece — Payments Statistics | disclosures | https://www.bankofgreece.gr/en/statistics/payments-statistics |
| both | Bank of Greece — Prevention of money laundering (AML/CFT supervision) | regulation, supervision, deadlines | https://www.bankofgreece.gr/en/main-tasks/supervision/prevention-of-money-laundering |
| both | Bank of Greece — Register of Bureaux de Change (Μητρώο Ανταλλακτηρίων Συναλλάγματος) | authorised_institution_lists, bureaux_de_change, licensing_registers | https://www.bankofgreece.gr/RelatedDocuments/9_ExchangeBureaus.xls |
| both | Bank of Greece — Retail Payment Strategy page | retail payment strategy, instant payments, SCT Inst, SEPA, digital eur | https://www.bankofgreece.gr/en/main-tasks/payment-systems-and-settlements/retail-payment-strategy |
| both | Bank of Greece — Revised Payment Services Directive PSD2 (EL) | PSD2, exempted, AISP, regulatory acts, supervision | https://www.bankofgreece.gr/kiries-leitourgies/epopteia/anathewrhmenh-odhgia-gia-tis-yphresies-plhrwmwn-(psd2) |
| both | Bank of Greece — SEPA page (main-tasks) | SEPA, SCT, SDD, SCT Inst, credit transfers, direct debits | https://www.bankofgreece.gr/en/main-tasks/payment-systems-and-settlements/sepa |
| both | Bank of Greece — Supervised institutions hub (EN) | disclosures | https://www.bankofgreece.gr/en/main-tasks/supervision/supervised-institutions |
| both | Bank of Greece — Supervisory sanctions / administrative penalties (Κυρώσεις) | sanctions, enforcement, payment_institutions, emoney_institutions, sup | https://www.bankofgreece.gr/en/main-tasks/supervision/sanctions |
| both | Bank of Greece — career opportunities portal | hiring_signals, procurement, IT_projects, payments | https://www.bankofgreece.gr/en/news-and-media/career-opportunities/job |
| both | Bank of Greece — Άμεσες Πληρωμές (Instant Payments) retail-payments page | payment statistics, instant payments adoption, market statistics | https://www.bankofgreece.gr/kiries-leitourgies/systhmata-plhrwmwn-diakanonismou/strathgikh-plhrwmwn-lianikhs/ameses-plhrwmes |
| both | Banking Dive (bankingdive.com) | leadership moves, organization changes | https://www.bankingdive.com/ |
| both | Banks.com.gr — banking & payments consumer/sector portal | press_releases, disclosures | https://banks.com.gr/ |
| both | Banktech Conference & Retail Payments Summit (Mellon Group / Octopus Events) — banktech.gr | retail payments, banking technology, ATM/self-service, acquiring, conf | https://banktech.gr/ |
| both | Bloomberg - Greek banks & Viva Wallet coverage | press releases, investor relations, disclosures | https://www.bloomberg.com/europe |
| both | BoG — Financial institutions (supervision overview) | payments actors population, PSP register, financial institution catego | https://www.bankofgreece.gr/en/main-tasks/supervision/financial-institutions |
| both | BoG — Innovation in payments (Καινοτομία στις πληρωμές) | vendors, partnerships | https://www.bankofgreece.gr/kiries-leitourgies/systhmata-plhrwmwn-diakanonismou/strathgikh-plhrwmwn-lianikhs/kainotomia-kai-plhrwmes |
| both | Boussias Events – Bank Management Conference | banking management, digital transformation, open finance, cyber-resili | https://bankmanagement.boussiasevents.gr/ |
| both | Boussias Events – Payments 360° Conference | payments infrastructure, instant payments, IRIS, open banking, acquiri | https://payments360.boussiasevents.gr/ |
| both | Boussias Events — Digital Finance Awards (Greece & Cyprus) | awards, digital banking, fintech, payments, recognitions | https://digitalfinanceawards.boussiasevents.gr/ |
| both | Boussias – Unified Commerce Conference | vendors, partnerships, case studies | https://unified-commerce.boussiasevents.gr/ |
| both | Brink's Hellas (Brink's Cash & Valuable Services) — Greece | cash usage, ATM POS data, market statistics | https://brinks.gr/ |
| both | Business Daily / Greek financial press - DIAS & instant-payments coverage | partnerships, case studies, competitors | https://www.businessdaily.gr/oikonomia/178349_oi-kryfes-ypiresies-tis-dias-poy-allazoyn-topio-ton-pliromon |
| both | BusinessNews.gr | bank technology, vendor contracts, anadochos awards, fintech, IT proje | https://www.businessnews.gr/ |
| both | BusinessNews.gr — Πρόσωπα (People/appointments) section | leadership_moves, hiring, jobs | https://www.businessnews.gr/prosopa |
| both | Byte — Investor Relations Financial News (δελτία τύπου/ανακοινώσεις) | project_wins, contract_awards, banking, financial_services | https://www.byte.gr/company/investor-relations/fin-news/ |
| both | CEIC Data - Greece Payment and Cards Statistics | payment statistics, card statistics, ATM POS data, market statistics | https://www.ceicdata.com/en/country/greece |
| both | CERPP — ESIDIS Published Notices / Proclamations portal | public-procurement, tenders, e-payments, POS | https://cerpp.eprocurement.gov.gr/ |
| both | CNN.gr — Οικονομία/Επιχειρήσεις (business desk) | partnerships, procurement | https://www.cnn.gr/oikonomia/epixeiriseis |
| both | COSMOTE Payments / payzy - Terms & Framework Contract (EMI) | regulation, compliance, terms_update, supervision, licensing | https://www.cosmotepayments.gr/terms.html |
| both | Capital Link - Invest in Greece Forum | investor relations, earnings | https://capitallink.com/forums/28th-annual-capital-link-invest-in-greece-forum/ |
| both | Capital.gr - Economy | payment statistics, card statistics, market statistics | https://www.capital.gr/oikonomia |
| both | Capital.gr — Economy / Businesses / Markets sections | banking, payments, public contracts, vendor wins, tenders | https://www.capital.gr/oikonomia/ |
| both | Capital.gr — Technology & Business/Banks sections | banking technology, digital banking, fintech, embedded finance, vendor | https://www.capital.gr/technology |
| both | Capital.gr — Επιχειρήσεις (Businesses) section | leadership_moves, organization_changes, hiring, jobs | https://www.capital.gr/epixeiriseis/ |
| both | Cardlink (Worldline Group) — Press Releases / Δελτία Τύπου | POS, NSP, card acceptance, partnership, procurement | https://cardlink.gr/deltia-typou/ |
| both | Cardlink (Worldline) — About / case pages (Alpha Bank & Eurobank POS network heritage) | procurement, POS, acquiring, payments | https://cardlink.gr/en/about-us/ |
| both | Cardlink (Worldline) — Greek NSP: POS terminal supply terms & IAPR interface | POS terminals, vendor models, supply terms, maintenance, acquiring | https://cardlink.gr/terms-of-pos-supply/ |
| both | Cardlink (Worldline) — LinkedIn company / jobs | hiring signals, implementation projects, acquiring, POS, terminals, pa | https://gr.linkedin.com/company/cardlink-sa |
| both | Cardlink (a Worldline brand) - News / Press Releases (el) | press releases, pos deployment, disclosures | https://cardlink.gr/ |
| both | Cardlink (a Worldline brand) — Press Office / Γραφείο Τύπου | acquiring, network_services_provider, POS, merchant_services, payments | https://cardlink.gr/grafeio-typoy/ |
| both | Cardlink (a Worldline company) — shared card-acquiring/POS infrastructure Greece | card acquiring, POS network, processing, Worldline, systemic banks, e- | https://cardlink.gr/about-us/ |
| both | Cardlink (member of Worldline) - Careers | jobs, hiring, organization changes | https://cardlink.gr/career/ |
| both | Cardlink S.A. - Workable openings | jobs, hiring | https://apply.workable.com/cardlink-sa/ |
| both | Cardlink — LinkedIn company page (Worldline member) | hiring, jobs, organization changes, leadership moves | https://www.linkedin.com/company/cardlink-sa |
| both | Cardlink — POS–ΦΗΜ interconnection implementation pages (acquirer/vendor) | pos_cash_register_interconnection, vendor_ecosystem, deadlines | https://cardlink.gr/wp-lp/ecr-pos-integration/ |
| both | Cardlink — careers / LinkedIn job feed (POS acquiring vendor) | hiring_weak_signal, pos, acquiring, merchant_onboarding, payment_gatew | https://gr.linkedin.com/jobs/cardlink-jobs |
| both | Central Beneficial Owners Register (Κεντρικό Μητρώο Πραγματικών Δικαιούχων) — GSIS / gsis.gr | beneficial ownership, subsidiaries, company register | https://www.gsis.gr/en/citizens-businesses/businesses/real-beneficiaries-register |
| both | Chambers' GEMI Registry Publicity (businessregistry.gr) | disclosures, annual reports, corporate actions | https://www.businessregistry.gr/publicity/index |
| both | Citi Careers — Private Banker, Greek Market | jobs, hiring | https://jobs.citi.com/ |
| both | Citi — Greece country page (Citi Country Officer) | leadership moves, organization changes | https://www.citigroup.com/global/about-us/global-presence/greece |
| both | Consumer Ombudsman (Συνήγορος του Καταναλωτή) - Annual Reports | complaints, consumer_protection, annual_reports, fees_charges, payment | https://www.synigoroskatanaloti.gr/en/etisies-ektheseis |
| both | Consumer Ombudsman - Recommendations & Findings on banks (Συστάσεις/Πορίσματα) | rulings, fees_charges, cards, loans, conduct, abusive_terms | https://www.synigoroskatanaloti.gr/el/nea?field_category_target_id=3 |
| both | Cooperative Bank of Epirus (Συνεταιριστική Τράπεζα Ηπείρου / Τράπεζα Ηπείρου) — corporate site | payments, digital_banking, vendor_signals, announcements | https://www.epirusbank.com/en |
| both | Cooperative Bank of Epirus (Συνεταιριστική Τράπεζα Ηπείρου) — announcements | vendor selection, core banking, digital banking, payments | https://www.epirusbank.com/ |
| both | Cooperative Bank of Karditsa — PSD2 Developer Program | open banking API, PSD2, sandbox, cooperative bank | https://www.bankofkarditsa.com.gr/el/psifiakes-ypiresies/psd2-developer-programm |
| both | Cooperative Bank of Karditsa — official website / e-Banking | cooperative_bank, e_banking, mobile_banking, IRIS_payments, core_banki | https://www.bankofkarditsa.com.gr/el/ |
| both | Cooperative Bank of Thessaly (Συνεταιριστική Τράπεζα Θεσσαλίας) — corporate site | payments, digital_banking, vendor_signals, announcements | https://www.bankofthessaly.gr/ |
| both | Council of State (Συμβούλιο της Επικρατείας) decisions - adjustice.gr | public contracts, bid protests, appeal decisions, audit findings, proc | https://www.adjustice.gr/webcenter/portal/ste/apofaseis |
| both | CrediaBank corporate site — Press Office / Group announcements (incl. Pancreta press archive) | IT_projects, payments, partnerships, vendor_announcements, merger_inte | https://www.crediabank.com/omilos/grafeio-typou/ |
| both | CrediaBank — Press Office | press_releases, partnerships, payments, digital_transformation, vendor | https://www.crediabank.com/en/group/press-office/ |
| both | CrediaBank — available job positions | hiring_signals, IT_projects, payments, procurement | https://www.crediabank.com/omilos/anthropino-dunamiko/i-crediabank-os-ergodotis/diathesimes-theseis-ergasias/ |
| both | Crowdpolicy — Solutions for Banks / Fintech project pages | open_banking, bank_partnership, psd2, implementation_story, payments | https://www.crowdpolicy.com/en/fintech/ |
| both | DEI (PPC) eProcurement Portal — Ιστοσελίδα Διαγωνισμών και Συμβάσεων | tenders, procurement, public contracts, award notices, payment collect | https://eprocurement.dei.gr/ |
| both | DEiXTo eProcurement/ΚΗΜΔΗΣ Web API (commercial) | procurement, tenders, api | https://deixto.com/eprocurement/ |
| both | DIAS - Careers (Join our Team) | jobs, hiring | https://www.dias.com.gr/en/join-our-team/ |
| both | DIAS - Financial Statements / Annual Reports (PDF archive) | annual reports, earnings, disclosures | https://www.dias.com.gr/en/financial-statements/ |
| both | DIAS - Financial statements (Χρηματοοικονομικές καταστάσεις) | payment statistics, market statistics | https://www.dias.com.gr/el/hrimatooikonomikes-katastaseis/ |
| both | DIAS - IRIS payments service page | disclosures, press releases | https://www.dias.com.gr/en/services/iris-payments/ |
| both | DIAS - LinkedIn company page | press releases, disclosures | https://gr.linkedin.com/company/dias-interbanking-systems-sa |
| both | DIAS - Nea / Δελτία Τύπου (News Center, Greek) | press releases, disclosures | https://www.dias.com.gr/el/nea/ |
| both | DIAS - News Center (Press Releases, Announcements & Publications, EN) | press releases, disclosures, investor relations | https://www.dias.com.gr/en/news-center/ |
| both | DIAS - Statistical data section (annual transaction volumes/values) | disclosures, earnings, annual reports | https://www.dias.com.gr/en/statistics-menu/ |
| both | DIAS - Statistics hub (Στατιστικά / statistics menu) | payment statistics, market statistics, cash usage, ATM POS data, card  | https://www.dias.com.gr/el/statistika-menou/ |
| both | DIAS Interbank Systems S.A. (operator of IRIS / interbank clearing) | interbank clearing, IRIS instant payments, SEPA, DIAS credit transfer, | https://www.dias.com.gr/ |
| both | DIAS Interbanking Systems - Corporate site (About Us / Membership & Connectivity / Compliance / Services) | actor map, vendor signals, instant payments, connectivity | https://www.dias.com.gr/en/about-us/ |
| both | DIAS Interbanking Systems S.A. - Corporate Governance (Board & Committees) | leadership moves, organization changes | https://www.dias.com.gr/en/corporate-governance/ |
| both | DIAS Interbanking Systems — hiring (site + LinkedIn) | hiring_signals, job_postings, instant_payments, iris, payment_infrastr | https://www.dias.com.gr/en/ |
| both | DIAS S.A. — Membership & Connectivity (participants, ACH/CSM interlinks, technical partners) | procurement, public contracts, vendors, connectivity, SEPA, clearing | https://www.dias.com.gr/en/membership-and-connectivity/ |
| both | DIAS S.A. — Services for Payment Service Providers & IRIS / Instant Payments service pages | instant payments, IRIS, SEPA, scheme specifications, procurement | https://www.dias.com.gr/en/services/services-for-payment-services-providers/ |
| both | DIAS on LinkedIn (company page - posts, jobs, partner tags) | vendor signals, hiring, partnerships, instant payments | https://www.linkedin.com/company/dias-interbanking-systems-sa |
| both | DIAS — Instant Payments (SCT Inst / TIPS) service page | instant_payments, scheme_rules, supervision | https://www.dias.com.gr/en/services/instant-payments/ |
| both | Deloitte EMEA Centre for Regulatory Strategy (ECRS) Insights Hub | regulation, supervision, consultations, deadlines | https://www.deloitte.com/uk/en/Industries/financial-services/collections/centre-for-regulatory-strategy-emea.html |
| both | Deloitte UK Financial Services Regulatory Outlook 2026 | regulation, deadlines, consultations | https://www.deloitte.com/uk/en/Industries/financial-services/research/regulatory-outlook.html |
| both | Deloitte — Digital Banking Maturity (EMEA/global benchmark incl. Greek banks) | competitors, vendors, case studies | https://www.deloitte.com/ce/en/industries/financial-services/research/digital-banking-maturity-2024.html |
| both | Delta Executive Search — Greece-desk private-banking mandates | jobs, hiring, leadership moves | https://www.deltaexec.com/ |
| both | Diavgeia (Δι@ύγεια) transparency portal — HCAP / HFSF published acts | disclosures, state holding, decisions, bank ownership, privatisation | https://diavgeia.gov.gr/f/HCAP |
| both | Diavgeia OpenData API (opendata.diavgeia.gov.gr) — complementary award-decision channel | contract_awards, decisions, vendors | https://opendata.diavgeia.gov.gr/ |
| both | Diavgeia per-organization decision feed (Προβολή Φορέα) — /f/{org} | procurement, award notices, spending decisions, public bodies | https://diavgeia.gov.gr/f/ose |
| both | Diavgeia types-of-decisions taxonomy (τύποι πράξεων) | procurement, award notices, spending decisions, taxonomy | https://diavgeia.gov.gr/typesOfDecisions |
| both | Diebold Nixdorf - Careers (Oracle CX portal) | jobs, hiring, organization changes | https://eeug.fa.us6.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX/jobs |
| both | Digital Finance Awards (BOUSSIAS) — Past Winners archive | digital banking, payments, insurance, vendor selection, digital transf | https://digitalfinanceawards.boussiasevents.gr/past-winners/ |
| both | DimosNet (ΔήμοςNet) — legal/administrative portal for municipalities | procurement, public contracts, tenders | https://dimosnet.gr/ |
| both | Diners Club Greece (dinersclub.gr, Alpha Bank-operated) | card_schemes, partnerships, payments | http://www.dinersclub.gr/ |
| both | EADHSY - Opinions & Negotiation requests (Γνωμοδοτήσεις / Αιτήματα Διαπραγμάτευσης) | procurement, public contracts, award notices, direct award, negotiatio | https://eadhsy.gr/gnomodotiseis/aitimata/ |
| both | EADHSY General/Directive Guidelines directory (Γενικές / Κατευθυντήριες Οδηγίες) | procurement, public contracts, guidance, tenders | https://eadhsy.gr/anathetouses-arches/genikes-odigies/ |
| both | EBA Consultations (public consultation papers register) | consultations, deadlines, regulation, supervision | https://www.eba.europa.eu/publications-and-media/consultations |
| both | EBA Consumer Trends Report (European Banking Authority) | consumer_trends, complaints, payment_services, cards, fraud_security | https://www.eba.europa.eu/publications-and-media/press-releases/eba-publishes-consumer-trends-report |
| both | EBA EUCLID public register interface (unified search across EBA registers) | disclosures, actor_map, passporting, payment_institutions, credit_inst | https://euclid.eba.europa.eu/register/ |
| both | EBA Greek-language section (Ελληνικά) and translated guidelines | regulation, supervision | https://www.eba.europa.eu/ellinika |
| both | EBA Guidelines on authorisation and registration under PSD2 | regulation, supervision | https://www.eba.europa.eu/guidelines-authorisation-and-registration-under-psd2 |
| both | EBA Guidelines on fraud reporting under PSD2 (with compliance table) | regulation, supervision | https://www.eba.europa.eu/activities/single-rulebook/regulatory-activities/payment-services-and-electronic-money/guidelines-fraud-reporting-under-psd2 |
| both | EBA Guidelines on major incidents reporting under PSD2 | regulation, supervision | https://www.eba.europa.eu/activities/single-rulebook/regulatory-activities/payment-services-and-electronic-money/guidelines-major-incidents-reporting-under-psd2 |
| both | EBA Interactive Single Rulebook — PSD2 | regulation, supervision | https://www.eba.europa.eu/regulation-and-policy/single-rulebook/interactive-single-rulebook/14575 |
| both | EBA Press releases | regulation, supervision, consultations, deadlines | https://www.eba.europa.eu/publications-and-media/press-releases |
| both | EBA RTS on strong customer authentication and secure communication under PSD2 (SCA & CSC) | regulation, supervision, deadlines | https://www.eba.europa.eu/legacy/regulation-and-policy/regulatory-activities/payment-services-and-electronic-money-0 |
| both | EBA Register of Payment & E-money Institutions under PSD2 | supervision, regulation, licensing | https://www.eba.europa.eu/risk-analysis-and-data/register-payment-electronic-money-institutions-under-PSD2 |
| both | EBA Register of Payment and Electronic Money Institutions (PSD2 central register) | disclosures, payment_institutions, e_money, passporting, actor_map | https://www.eba.europa.eu/risk-and-data-analysis/data/registers/payment-institutions-register |
| both | EBA Single Rulebook Q&A tool | regulation, supervision, consultations | https://www.eba.europa.eu/single-rule-book-qa |
| both | EBA Technical Standards on the EBA Register under PSD2 | regulation, supervision | https://www.eba.europa.eu/activities/single-rulebook/regulatory-activities/payment-services-and-electronic-money/technical-standards-eba-register-under-psd2 |
| both | EBA Work Programme (annual, PSD3/PSR mandate roadmap) | regulation, consultations, deadlines | https://www.eba.europa.eu/about-us/mission-values-and-tasks/work-programme |
| both | EBA — Central Register of Payment and Electronic Money Institutions under PSD2 (incl. Greece) | disclosures | https://euclid.eba.europa.eu/register/pir/disclaimer |
| both | EBA — Credit Institutions Register (CIR) via EUCLID | credit institutions, banks, registers, supervision, PSP census | https://euclid.eba.europa.eu/register/cir/search |
| both | ECB / Euro Retail Payments Board (ERPB) - SCT Inst scheme status updates | regulation, supervision, deadlines | https://www.ecb.europa.eu/paym/groups/erpb/html/index.en.html |
| both | ECB Data Portal - Payment statistics (Greece breakdown) | payment statistics, card statistics, ATM POS data | https://data.ecb.europa.eu/data/datasets/PAY/dashboard |
| both | ECB Data Portal - Payments statistics (PAY), Greece | payment statistics, card statistics, cash usage, ATM POS data | https://data.ecb.europa.eu/data/datasets/PAY/PAY.A.GR.W0.TOTL1.1._Z.N.PN |
| both | ECB Data Portal / Statistical Data Warehouse — Payments statistics (cash withdrawals, Greece) | payment statistics, card statistics, cash usage, ATM POS data | https://data.ecb.europa.eu/data/data-categories/payment-statistics/payment-services-large-value-payment-systems-and-retail-payment-systems-new/card-based-payment-transactions-incl-cash-withdrawals |
| both | ECB Data Portal — ATM, OTC and POS terminal transactions (PTT dataset) | ATM POS data, payment statistics, cash usage | https://data.ecb.europa.eu/data/datasets/PTT |
| both | ECB Data Portal — Card payments and cash withdrawals using cards, incl. fraud (PCP dataset) | payment statistics, card statistics, cash usage, ATM POS data | https://data.ecb.europa.eu/data/datasets/PCP |
| both | ECB Data Portal — Greece geographical area hub | market statistics, payment statistics, card statistics, cash usage, AT | https://data.ecb.europa.eu/data/geographical-areas/greece?reference_area_name%5B0%5D=Greece |
| both | ECB Data Portal — Number of terminals provided by resident PSPs by type and function (PTN dataset) | ATM POS data, payment statistics, card statistics | https://data.ecb.europa.eu/data/datasets/PTN |
| both | ECB Data Portal — SDMX 2.1 REST API and bulk-download service | payment statistics, card statistics, ATM POS data, market statistics | https://data.ecb.europa.eu/help/api/overview |
| both | ECB Procurement / Electronic Tendering System (TARGET / T2 / TIPS / T2S) | payments, procurement, tenders, payment infrastructure | https://www.ecb.europa.eu/ecb/jobsproc/tenders/html/index.en.html |
| both | ECB Supervision Blog | disclosures, stress tests, capital | https://www.bankingsupervision.europa.eu/press/blog/html/index.en.html |
| both | ECB — Digital euro programme (progress, pilot, provider selection) | digital euro, procurement, providers, pilot participants, framework ag | https://www.ecb.europa.eu/euro/digital_euro/html/index.el.html |
| both | ECB — Payment services methodology page (DSD naming conventions, dataset catalogue) | payment statistics, card statistics, ATM POS data | https://data.ecb.europa.eu/methodology/payment-services-large-value-payment-systems-and-retail-payment-systems |
| both | ECB — Payments statistics press releases (half-yearly) | payment statistics, cash usage, ATM POS data | https://www.ecb.europa.eu/press/stats/paysec/html/index.en.html |
| both | ECB — TARGET Services / T2 documentation and links hub | payment infrastructure, TARGET/T2, TIPS, T2S, documentation | https://www.ecb.europa.eu/paym/target/html/index.en.html |
| both | ECB — TIPS (TARGET Instant Payment Settlement) service pages & documentation | instant payments, TIPS, payment infrastructure, settlement | https://www.ecb.europa.eu/paym/target/tips/html/index.en.html |
| both | EEDADP — News & Media | industry news, position papers, NPL policy | https://eedadp.com/en/news-and-media/ |
| both | EETT — Διαγωνισμοί προμηθειών/υπηρεσιών (postal & telecom regulator, ELTA cost-system tenders) | tenders, procurement, postal_financial | https://www.eett.gr/eett/diagonismoi-promitheion-ypiresion/ |
| both | ELSTAT Statistics Portal (Στατιστικές) - thematic catalogue | market statistics, payment statistics, card statistics, cash usage, AT | https://www.statistics.gr/en/statistics |
| both | ELTA (Hellenic Post) - Career Opportunities page | jobs, hiring, organization changes | https://www.elta.gr/eukairies-karieras |
| both | ELTA (Hellenic Post) — Procurement Declarations (Προμήθεια Υλικών / Παροχή Υπηρεσιών) | tenders, procurement, public contracts, bill payment aggregation, paym | https://www.elta.gr/declarations/parochi-ypiresion |
| both | ELTA - Board of Directors / Leadership page | leadership moves, organization changes | https://www.elta.gr/team/dioikitiko-sumboulio |
| both | EMVCo — Approved Products & Solutions database | certification, vendor-selection, standards | https://www.emvco.com/approved-products/ |
| both | EPANT (Hellenic Competition Commission) — Press releases & merger decisions | merchant_acquiring, M&A_clearance, bank_carveout, competition, vendor_ | https://www.epant.gr/en/information/press-releases.html |
| both | EPANT (Hellenic Competition Commission) — merger/decisions archive | M&A, acquiring, market structure, partnerships | https://www.epant.gr/apofaseis.html |
| both | EPANT Fintech Sector Inquiry (Κλαδική Έρευνα Fintech) - hub & reports | market statistics, payment statistics, card statistics | https://www.epant.gr/enimerosi/kladiki-erevna-stis-xrimatooikonomikes-texnologies-fintech.html |
| both | EPC — SEPA Proxy Lookup / Verification of Payee (VOP) directory & scheme | VOP, verification of payee, instant payments, SEPA, participant regist | https://www.europeanpaymentscouncil.eu/what-we-do/other-schemes/sepa-proxy-lookup |
| both | ESMA Registers portal (unified register search) | disclosures, investment_firms, issuers, actor_map | https://registers.esma.europa.eu/publication/ |
| both | EU Funding & Tenders Portal — projects & results (opportunities/projects-results) | EU funding, tenders, projects, beneficiaries, digital payments | https://ec.europa.eu/info/funding-tenders/opportunities/portal/screen/opportunities/projects-results |
| both | EU Publications Office — Public Procurement details portal (op.europa.eu) | tenders, procurement, payments, financial services | https://op.europa.eu/en/web/public-procurement/ |
| both | EUR-Lex - Interchange Fee Regulation (EU) 2015/751 (IFR) | regulation | https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32015R0751 |
| both | EUR-Lex - SEPA Regulation (EU) 260/2012 (Greek text) | regulation | https://eur-lex.europa.eu/legal-content/EL/TXT/HTML/?uri=LEGISSUM:4373224 |
| both | EUR-Lex — Legislative procedure file (per-act, e.g. 2023/0210(COD) PSR) | regulation, consultations, deadlines | https://eur-lex.europa.eu/procedure/EN/2023_210 |
| both | EVERYPAY (Skroutz Group) — corporate/press pages | procurement, partnerships, EMI license, wallet, acquiring | https://everypay.gr/ |
| both | EY EMEIA - PSD3/PSR & Instant Payments impact analyses | regulation, deadlines | https://www.ey.com/en_gl/insights/financial-services/emeia/how-psd3-and-psr-will-shape-trends-in-eu-financial-services |
| both | Electronic Payments International — Greece region archive | card issuing, acquiring, scheme partnership, co-brand, M&A, procuremen | https://www.electronicpaymentsinternational.com/region/europe/greece/ |
| both | Electronic STR Submission System (eSTR) — HFIU reporting portal | deadlines, supervision, regulation | https://estr.aml-authority.gov.gr/ |
| both | Epixeiro.gr - Innovation & Technology and Banks sections | vendors, competitors, partnerships, case studies | https://www.epixeiro.gr/innovation-technology |
| both | Epsilon Net – Investor Relations (listed fintech/business-software) | leadership moves, board changes, organization changes | https://ir.epsilonnet.gr/ |
| both | Epsilon Net — Careers (Epsilon Talent / SmartCV) | hiring_signals, job_postings, payments, pos, engineering | https://careers.epsilontalent.com/job-openings?clientID=Epsilonnet |
| both | Epsilon Net — Investor Relations / Press (POS-acquiring integration partnerships) | POS, acquiring, vendor_partnership, myDATA, merchant_services | https://ir.epsilonnet.gr/en/ |
| both | EuroPA (European Payments Alliance) & member operators - IRIS/DIAS interconnection announcements | cross-border, instant payments, interoperability, vendor signals | https://epicompany.eu/media-insights/ |
| both | Eurobank - IRIS P2B / instant-payments materials (business academy & product) | IRIS P2B, instant payments, merchant onboarding, EuroPA cross-border | https://www.eurobank.gr/ |
| both | Eurobank Developer Portal (Regulatory / PSD2 APIs) | open banking API, regulatory APIs, AIS, PIS | https://developer.eurobank.gr/ |
| both | Eurobank Holdings — Investor Relations / Financial Results hub | card statistics, payment statistics, market statistics, ATM POS data | https://www.eurobankholdings.gr/en/investor-relations/financial-results |
| both | Eurobank — LinkedIn company page & Jobs tab | jobs, hiring, leadership moves, organization changes | https://gr.linkedin.com/company/eurobank |
| both | Eurobank — Mastercard scheme-alignment announcement (all cards to Mastercard) | scheme migration, card issuing, co-brand, loyalty, procurement signal | https://www.eurobank.gr/el/retail/proionta-upiresies/proionta/kartes |
| both | Eurobank — Press Office / Δελτία Τύπου (Group announcements & IR) | vendor selection, core banking, digital banking, payments, award notic | https://www.eurobankholdings.gr/el/enimerosi-ependuton |
| both | Eurobank — careers portal (SAP SuccessFactors ATS) | hiring_weak_signal, payments_transformation, core_banking_migration, c | https://careers.eurobank.gr/go/All-Jobs-Greek/827602/ |
| both | Eurobank — careers portal (careers.eurobank.gr, SuccessFactors) | core banking, IT hiring, software engineering, tech stack | https://careers.eurobank.gr/go/All-Jobs/827502/ |
| both | Eurobank — Γραφείο Τύπου / Δελτία Τύπου (Greek Press Office) | press releases, payments, cards, POS, vendor announcements | https://www.eurobank.gr/el/omilos/grafeio-tupou |
| both | Eurofound - European Restructuring Monitor (Greece) | restructuring, voluntary_exit_scheme, collective_dismissals, branch_cl | https://apps.eurofound.europa.eu/restructuring-events/countries/Greece |
| both | Euromoney — Transaction Banking / Cash Management Awards | awards, cash management, transaction banking, payments | https://www.euromoney.com/awards |
| both | Euronet Merchant Services Greece (epay) — LinkedIn / news | partnerships, public contracts, procurement | https://gr.linkedin.com/company/epay-payment-solutions |
| both | Euronet Worldwide - EFT Segment Careers (Workable) | jobs, hiring, organization changes | https://apply.workable.com/euronet-eft/ |
| both | Euronet Worldwide - Investor News Releases (Greece ATM/POS: Citibank ATM outsourcing, Piraeus merchant acquiring) | POS data, ATM data, installed base, market statistics | https://ir.euronetworldwide.com/news-releases |
| both | Euronet Worldwide / epay Greece — announcements | merchant acquiring, ATM, card management, digital wallet, procurement | https://epayworldwide.gr/ |
| both | Euronet Worldwide / epay Greece — corporate news (CrediaBank merchant-acquiring & ATM deal) | vendor selection, payments, award notices | https://www.euronet.com/use-cases/corporate-news/ |
| both | Euronet Worldwide Inc. — SEC 10-K annual filings (EFT Processing segment) | ATM POS data, market statistics, cash usage | https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001029199&type=10-K |
| both | Euronet Worldwide Investor Relations — News Releases (epay / Piraeus acquiring) | merchant acquiring, POS terminals, epay, Piraeus Bank, Euronet Merchan | https://ir.euronetworldwide.com/press-releases |
| both | Euronet Worldwide investor relations (Greek acquiring segment) | competitors, vendors | https://ir.euronetworldwide.com/ |
| both | Euronet Worldwide — Investor Relations Press Releases (parent of epay Greece) | acquiring, M&A, merchant_services, press_release, financial_disclosure | https://ir.euronetworldwide.com/index.php/press-releases |
| both | Euronext Athens (ATHEX) — Central Company Announcements | tenders, procurement, public contracts, award notices, material contra | https://athens.euronext.com/en/market-data/announcements |
| both | Euronext Athens — Alpha Bank issuer announcements feed | material contracts, vendor selection, capex, regulated information, aw | https://athens.euronext.com/en/market-data/issuers/278/announcements |
| both | Euronext Athens — Eurobank issuer announcements feed | material contracts, vendor selection, capex, regulated information, aw | https://athens.euronext.com/en/market-data/issuers/64/announcements |
| both | Euronext Athens — Piraeus Bank / Piraeus Financial Holdings issuer announcements feed | material contracts, vendor selection, capex, regulated information, aw | https://athens.euronext.com/en/market-data/issuers/63/announcements |
| both | European Commission — Consumer finance and payments hub | regulation, deadlines, consultations | https://finance.ec.europa.eu/consumer-finance-and-payments_en |
| both | European Commission — FISMA newsroom / item feed | regulation, consultations, supervision | https://ec.europa.eu/newsroom/fisma/items |
| both | European Commission — Financial assistance to Greece / Post-Programme Surveillance | competitors, case_studies | https://economy-finance.ec.europa.eu/eu-financial-assistance/euro-area-countries/financial-assistance-greece_en |
| both | European Commission — Greece Recovery & Resilience supported-projects pages | EU-funded, e-payments, POS, digital-transformation | https://commission.europa.eu/business-economy-euro/economic-recovery/recovery-and-resilience-facility/country-pages/greeces-recovery-and-resilience-plan_en |
| both | European Investment Bank — Financed Projects database (Greece filter) | public contracts, beneficiaries, financing, digital payments, financia | https://www.eib.org/en/projects/loans/index.htm?countries=GR |
| both | European Investment Fund (EIF) — InvestEU Greece / guarantees news & country page | financing, beneficiaries, financial inclusion, digital payments, rrf | https://www.eif.org/supporting-smes/eif-near-me/greece |
| both | European Parliament — Legislative Train Schedule (FISMA files) | regulation, deadlines, consultations | https://www.europarl.europa.eu/legislative-train/ |
| both | European Payments Council (EPC) - SCT Inst & Verification of Payee schemes | partnerships, competitors | https://www.europeanpaymentscouncil.eu/what-we-do/other-schemes/verification-payee |
| both | European Payments Council - Document Library / site search | regulation, consultations, deadlines | https://www.europeanpaymentscouncil.eu/search |
| both | European Payments Council - SEPA Credit Transfer (SCT) rulebook | regulation, deadlines | https://www.europeanpaymentscouncil.eu/document-library/rulebooks/2025-sepa-credit-transfer-rulebook-version-10 |
| both | European Payments Council - SEPA Direct Debit B2B (SDD B2B) rulebook & implementation guidelines | regulation, deadlines | https://www.europeanpaymentscouncil.eu/what-we-do/epc-payment-schemes/sepa-direct-debit/sepa-direct-debit-b2b-rulebook-and-implementation |
| both | European Payments Council - SEPA Direct Debit Core (SDD Core) rulebook & implementation guidelines | regulation, deadlines | https://www.europeanpaymentscouncil.eu/what-we-do/epc-payment-schemes/sepa-direct-debit/sepa-direct-debit-core-rulebook-and-implementation |
| both | European Payments Council - SEPA Instant Credit Transfer (SCT Inst) rulebook & implementation guidelines | regulation, deadlines, supervision | https://www.europeanpaymentscouncil.eu/what-we-do/epc-payment-schemes/sepa-instant-credit-transfer/sepa-instant-credit-transfer-rulebook |
| both | European Payments Council - SEPA Request-to-Pay (SRTP) scheme rulebook | regulation, deadlines | https://www.europeanpaymentscouncil.eu/what-we-do/other-schemes/sepa-request-pay |
| both | European Payments Council - Verification of Payee (VOP) scheme rulebook | regulation, deadlines, supervision | https://www.europeanpaymentscouncil.eu/document-library/rulebooks/verification-payee-scheme-rulebook |
| both | European Payments Council — SEPA payment statistics | payment statistics, market statistics | https://www.europeanpaymentscouncil.eu/what-we-do/be-involved/sepa-payment-statistics |
| both | EveryPay (Skroutz) — Greek payment institution, press & corporate news | payment institution, EMI licence, payment gateway, SoftPOS, vendor par | https://www.everypay.gr/ |
| both | EveryPay — LinkedIn company page (Skroutz group EMI) | hiring, jobs, leadership moves, organization changes | https://gr.linkedin.com/company/everypay |
| both | Everypay (Skroutz) — Corporate press | EMI, wallet, product launch, acquisition, loyalty | https://corporate.skroutz.gr/en/press/ |
| both | Everypay (a Skroutz company) — About / Company & Blog | partnerships, procurement | https://www.everypay.gr/gr/company/about |
| both | FF News (fintech.tv / ffnews.com) | leadership moves, organization changes, hiring | https://ffnews.com/ |
| both | FIS Global Media Room (Press Releases) | payments, cards, core_banking, wins | https://www.fisglobal.com/about-us/media-room |
| both | FIS Global — Client Stories / Insights | vendors, case studies | https://www.fisglobal.com/insights/fis-client-stories |
| both | FRED (St. Louis Fed) - Greece financial-access series (IMF FAS mirror) | ATM POS data, market statistics | https://fred.stlouisfed.org/series/GRCFCAANUM |
| both | Fime — payments certification/testing consultancy (SoftPOS, EMV, 3DS) | certification, standards, vendor-selection | https://www.fime.com/ |
| both | FinTech Futures — Greece region feed | vendor deals, core banking, partnerships, acquiring, digital banking | https://www.fintechfutures.com/region/greece |
| both | FinTech Futures — Greece region feed (challenger banks / payments) | partnerships, launch, licensing, vendor procurement, funding | https://www.fintechfutures.com/us/region/greece/ |
| both | Finance Magnates - Greek fintech coverage | press releases, investor relations | https://www.financemagnates.com/fintech/ |
| both | Finextra / ffnews / bobsguide — payments deal news | merchant acquiring, POS, partnership, procurement | https://ffnews.com/?s=greece |
| both | Finextra Research — Greece / Greek-bank company news feeds | vendor deals, partnerships, payments platforms, core banking, acquirin | https://www.finextra.com/ |
| both | Finextra Research — Payments channel & company news | payments, card management, core banking, vendor-bank contracts, digita | https://www.finextra.com/channel/payments |
| both | Finloup - BNPL provider (Greece) | compliance, terms_update, regulation | https://www.finloup.com/ |
| both | Finloup — Company site / About & merchant pages | BNPL, open banking, merchant partnership, installments | https://finloup.com/en/ |
| both | Finloup — Greek BNPL / device-leasing fintech (site, ACE case study, funding press) | BNPL, open banking, device leasing, merchant integrations, credit infr | https://finloup.com/ |
| both | FinregE - regulatory horizon scanning & obligation library | regulation, consultations, deadlines | https://finreg-e.com/compliance-services/regulatory-horizon-scanning/ |
| both | Fintech Athens (NKUA + National Bank of Greece) — event site / agenda | fintech, AI in finance, payments, conference speakers, conference spon | https://fintechathens.nbgevents.gr/ |
| both | Fintech Futures — Greece region & bank tags (Banking Tech) | payments, AI in banking, merchant acquiring, vendor-bank contracts, di | https://www.fintechfutures.com/keyword/greece |
| both | Fiscal Solutions (fiscal-requirements.com) — Greece fiscalisation news (EN) | regulation, deadlines, pos_cash_register_interconnection, mydata, comm | https://www.fiscal-requirements.com/countries/24 |
| both | Forin.gr – Φορολογία / Νομοθεσία (tax & commercial law database) | regulation, deadlines | https://www.forin.gr/laws |
| both | Fortune Greece / iefimerida — Greek business media (scheme strategy coverage) | partnerships, product-launch, procurement | https://www.fortunegreece.com/ |
| both | Fraport Greece — 14 regional airports operator | procurement, payment terminals, parking, contactless payments | https://www.fraport-greece.com/el.html |
| both | Fraport Greece — Regional Airports Corporate Tenders | tenders, procurement, public contracts, payment services | https://www.fraport-greece.com/en/our-expertise/prm-assistant-services-tenders.html |
| both | GDAEE / GDDIA — General Directorate for Defence Investments & Armaments — Tenders | tenders, procurement, public contracts, payments | https://www.gdaee.mil.gr/en/tenders/ |
| both | GEMH / Business Registry (Γενικό Εμπορικό Μητρώο) - DIAS statutory filings | disclosures, annual reports, earnings | https://www.businessregistry.gr/ |
| both | GEMH / businessregistry.gr — Greek General Commercial Registry (DIAS corporate filings, GEMI 000740401000) | procurement, governance, shareholders, financial statements | https://www.businessregistry.gr/Publicity.aspx |
| both | GEMI Publicity - Greek Business Registry Financial Statements | annual reports, disclosures | https://publicity.businessportal.gr/ |
| both | GRNET / ΕΔΥΤΕ Α.Ε. — Διαγωνισμοί (RFPs) | tenders, procurement, payments, e-government, digital identity | https://grnet.gr/rfps/ |
| both | GSIS (General Secretariat for Information Systems & Digital Governance) — Competitions/Auctions | procurement, tenders, cloud (G-Cloud), databases, payments systems, in | https://www.gsis.gr/en/competitions-auctions |
| both | GSIS / ΓΓΠΣΨΔ (gsis.gr) — e-Public Procurements invoice & e-POS for public revenue | e-payments, POS, public-procurement, e-invoicing | https://www.gsis.gr/en/citizens-businesses/payments-proceeds/e-invoice |
| both | GSIS Single Payment Authority (EAP) / e-Παράβολο payment platform pages | tenders, procurement | https://www.gsis.gr/en/dimosia-dioikisi/pliromes-eispraxeis/eap |
| both | Glassdoor - Nexi Group jobs in Greece | jobs, hiring, organization changes | https://www.glassdoor.com/Job/greece-nexi-group-jobs-SRCH_IL.0,6_IN100_KO7,17.htm |
| both | Glassdoor — Greece bank/PSP jobs & employer reviews | hiring_signals, job_postings, employer_signals | https://www.glassdoor.com/Jobs/Viva-Wallet-Jobs-E1267154.htm |
| both | Glassdoor — Greece banking / vendor jobs & employer pages | hiring_signals, banking, payments, vendor_management | https://www.glassdoor.com/Job/athens-banking-jobs-SRCH_IL.0,6_IC2580540_KO7,14.htm |
| both | Glassdoor — Greek fintech employer pages | jobs, hiring, organization changes | https://www.glassdoor.com/Jobs/Viva-com-Jobs-E1267154.htm |
| both | Global Payments — NBG Pay (partnership press) | merchant acquiring, processing, partnership, procurement | https://nbgpay.globalpayments.com/en-gr/about |
| both | GlobalData — Greece Cards and Payments market report | market data, disclosures, card statistics | https://www.globaldata.com/store/report/greece-cards-and-payments-market-analysis/ |
| both | GoCardless Bank Account Data (ex-Nordigen) — European bank coverage | account information, bank coverage, AIS, aggregation | https://gocardless.com/bank-account-data/coverage/ |
| both | Google Play - Greek banking/payment app reviews (Eurobank, Piraeus, Alpha, NBG) | vendors, competitors, case studies, partnerships | https://play.google.com/store/apps/details?id=com.EurobankEFG&hl=el_GR |
| both | Google for Jobs — Greece banking/payments overlay | jobs, hiring | https://www.google.com/search?q=%CF%84%CF%81%CE%AC%CF%80%CE%B5%CE%B6%CE%B1+%CE%B8%CE%AD%CF%83%CE%B5%CE%B9%CF%82+%CE%B5%CF%81%CE%B3%CE%B1%CF%83%CE%AF%CE%B1%CF%82&ibp=htl;jobs |
| both | GovHub — Municipal Payment Platform (Πλατφόρμα Ψηφιακών Πληρωμών ΟΤΑ, mpp.govhub.gr) & docs | public contracts, procurement, tenders | https://docs.govhub.gr/mpp |
| both | GovHub — Πλατφόρμα Ψηφιακών Πληρωμών ΟΤΑ (Municipal Payment Platform / MPP) integration docs | municipal e-payment, payment platform, onboarding, actor map | https://docs.govhub.gr/el/mpp |
| both | Governet.gr — public-administration portal (municipal e-services news) | procurement, public contracts, tenders | https://governet.gr/ |
| both | Greek Consumer Ombudsman (Συνήγορος του Καταναλωτή) — Recommendations & Findings (Συστάσεις-Πορίσματα) | consumer_disputes, card_fees, card_fraud, payment_services, banking_pr | https://www.synigoroskatanaloti.gr/el/systaseis-porismata |
| both | Greek Fintech Cluster (GFC) | open banking, payments, regulation | https://fintech.net.gr/ |
| both | Greek Fintech Hub - Events (Fintech Athens) | press releases, investor relations | https://www.fintechhub.gr/events |
| both | Greek banking trade press cluster (Capital.gr, Naftemporiki, Business Daily, newmoney, insider.gr) — coop/non-systemic bank coverage | mergers, vendor_announcements, IT_projects, payments, procurement_sign | https://www.capital.gr/finance/news/credia/ |
| both | Greek business & fintech press - BNPL / wallet coverage (capital.gr, powergame.gr, news247, CNN.gr, insider.gr) | market statistics, payment statistics, card statistics | https://www.capital.gr/oikonomia/3736620/agores-me-doseis-xoris-pistotiki-to-montelo-tou-bnpl-stin-ellada/ |
| both | Greek eCommerce Association (GRECA) — Member announcements & news feed | news, partnerships, m_and_a, payments_vendors, weak_signals | https://www.greekecommerce.gr/category/news/member-announcements/ |
| both | Greek economic/financial press tag pages (Capital.gr, Business Daily, OT.gr, Euronews GR) - 'ΔΙΑΣ Διατραπεζικά Συστήματα' | instant payments, vendor signals, regulation, pricing, public sector | https://www.capital.gr/tag/dias-diatrapezika-sustimata |
| both | Greek financial press - DIAS/IRIS statistics coverage (insider.gr, naftemporiki, newmoney, powergame, capital.gr) | payment statistics, market statistics, card statistics | https://www.insider.gr/epiheiriseis/394985/dias-neo-istoriko-ypsilo-se-ogko-kai-axia-synallagon-2025 |
| both | Greek legislation databases — Law 4465/2017 (PAD) & Law 4537/2018 (PSD2) texts | regulation, fee_transparency, payment_services, consumer_protection | https://www.e-nomothesia.gr/kat-trapezes-pistotika-idrumata/nomos-4465-2017-fek-47a-4-4-2017.html |
| both | GreekReporter.com - Business/Banking | earnings, press releases, disclosures | https://greekreporter.com/category/greek-news/business-2/banking/ |
| both | HBA Annual Reports (Ετήσιοι Απολογισμοί) | market statistics, payment statistics, cash usage | https://www.hba.gr/association/info/annualreport |
| both | HBA Statistics hub — Greek banking system financial & structural data | market statistics, banking sector aggregates, ATM POS data, branch net | https://www.hba.gr/Statistics/List?type=GreeceBrief |
| both | HBA — Announcements (Ανακοινώσεις, Greek) | press releases, disclosures | https://www.hba.gr/Media/List?type=Announcements |
| both | HBA — Annual activity reports (Έκθεση Πεπραγμένων / Απολογισμός) | regulation, supervision, consultations, deadlines | https://www.hba.gr/Association/Info/annualreport |
| both | HBA — Greek Banking System Overview (periodic publication, EN) | market statistics, ATM POS data, payment statistics | https://www.hba.gr/En/Publications |
| both | HBA — News / Current affairs (Επικαιρότητα) | press releases, disclosures | https://www.hba.gr/News/Details/168 |
| both | HBA — News / Current developments feed (Επικαιρότητα) | regulation, supervision, consultations, deadlines | https://www.hba.gr/Media/List?type=News |
| both | HBA — Payment Systems activity area (Συστήματα πληρωμών) | instant payments, IRIS, open banking, payment standards, PSD2, PSD3, S | https://www.hba.gr/ActivityAreas/List?type=PaymentsSystems |
| both | HBA — Payment fraud prevention activity area (Πρόληψη της απάτης στα μέσα και συστήματα πληρωμών) | regulation, consultations, deadlines | https://www.hba.gr/ActivityAreas/List?type=Fraud |
| both | HBA — Payment systems statistics (Συστήματα πληρωμών) | earnings, disclosures | https://www.hba.gr/En/Statistics/List?type=PaymentsSystems_EN |
| both | HBA — Press Releases (English) | press releases, disclosures | https://www.hba.gr/En/Media/List?type=PressReleases_EN |
| both | HBA — Publications & Annual Reports (Εκδόσεις / Ετήσιοι Απολογισμοί) | annual reports, disclosures | https://www.hba.gr/Publications/Info/annualreports |
| both | HBA — Regulatory / Activity Areas (Ρυθμιστικά θέματα · διαβουλεύσεις) | disclosures, press releases | https://www.hba.gr/ActivityAreas/List?type=OperationAndSupervisionOfCreditInstitutions |
| both | HCMC Board Decisions & Circulars (Αποφάσεις Δ.Σ. και Εγκύκλιοι) | payment statistics, market statistics | http://www.hcmc.gr/el/apophaseis-d.s.-kai-enkyklioi |
| both | HDPA — RSS feed (news / acts) | regulation, decisions, deadlines | https://www.dpa.gr/el/rss.xml |
| both | HFSF advisor-RFP announcements (LinkedIn RFP posts + procurement notices) | procurement, advisor RFP, banking | https://www.linkedin.com/posts/hellenic-financial-stability-fund_rfp-for-the-provision-of-legal-advisory-activity-7217134940470071296-TrTm |
| both | HR Professional — LinkedIn showcase page | leadership moves, organization changes | https://gr.linkedin.com/showcase/hr-professional/ |
| both | Hellas Smart Ticket S.A. (HST) — AFC concessionaire for OASA e-ticketing | e-ticketing, contactless payments, public-private partnership, procure | https://www.hellasmarticket.gr/ |
| both | Hellenic Anti-Money Laundering Authority — main institutional site (Αρχή Καταπολέμησης της Νομιμοποίησης Εσόδων από Εγκληματικές Δραστηριότητες) | regulation, supervision, consultations, deadlines | https://www.aml-authority.gov.gr/en/ |
| both | Hellenic Association of Factoring Companies (Ελληνική Ένωση Factoring / Hellenic Factors) | disclosures, annual reports | https://www.hellenicfactors.gr/ |
| both | Hellenic Bank Association (HBA / ΕΕΤ) — Payment Systems activity area | IRIS, payment_systems, bank_coordination, e_banking, onboarding | https://www.hba.gr/ActivityAreas/List?type=OnlineBanking |
| both | Hellenic Bank Association (HBA) - Events & Speeches | press releases, investor relations | https://hba.gr/events/list |
| both | Hellenic Bank Association (HBA) - Sustainable Finance / ESG section | disclosures, ESG, sustainability, sustainable finance, regulation | https://www.hba.gr/ActivityAreas/Info/esg |
| both | Hellenic Bank Association (HBA) - payment systems publications/section | disclosures, annual reports | https://www.hba.gr/FinancialLaw/List?type=InternationalPaymentSystems |
| both | Hellenic Bank Association (HBA) — Preliminary list of PSPs joining the EPC SCT Inst scheme / SEPA hub | payment statistics, instant payments adoption, market statistics | https://hba.gr/ActivityAreas/Details/575 |
| both | Hellenic Bank Association (HBA) — payment systems / PSD2 legal section | PSD2 transposition, payment systems, legal framework, member banks | https://www.hba.gr/ActivityAreas/Details/221 |
| both | Hellenic Bank Association (HBA/EET) — Press Office & Card-Market publications | press releases, disclosures, card market, interchange, contactless | https://www.hba.gr/Media |
| both | Hellenic Bank Association (ΕΕΤ / HBA) — main site | banking association, payments, digital banking, standards, policy posi | https://www.hba.gr/en |
| both | Hellenic Bank Association (ΕΕΤ) — Studies, position papers & consultations | position_papers, studies, consultations, standards, payment_systems | https://www.hba.gr/publications/info/studies |
| both | Hellenic Bank Association (Ελληνική Ένωση Τραπεζών / ΕΕΤ) — official site (master pointer hub) | members, committees, payment systems, cards, fraud prevention, studies | https://www.hba.gr/ |
| both | Hellenic Bank Association — ATM Network statistics (Δίκτυο ΑΤΜ) | ATM POS data, market statistics, cash usage | https://www.hba.gr/Statistics/List?type=ATMSsNetwork |
| both | Hellenic Bank Association — Financial Law portal (Ελληνική Ένωση Τραπεζών, hba.gr) | regulation, supervision, consultations, deadlines | https://www.hba.gr/FinancialLaw |
| both | Hellenic Bank Association — HEBIC bank & branch code directory | bank codes, branches, payment system, member list | https://www.hba.gr/info/hebicbankcodes |
| both | Hellenic Bank — API Banking / Open Banking developer portal | open banking API, PSD2, AIS, PIS | https://www.hellenicbank.com/el/personal/api-banking |
| both | Hellenic Civil Aviation Authority (HCAA / YPA) — announcements & procurement | tenders, procurement, public contracts, payment terminals, airports | https://hcaa.gov.gr/el |
| both | Hellenic Coast Guard (LS-ELAKT) — Tenders & Procurement (Διαγωνισμοί-Προμήθειες) | tenders, procurement, public contracts, payments | https://www.hcg.gr/el/anakoinwseis/ |
| both | Hellenic Competition Commission (EPANT) - merger decisions | competitors, partnerships, vendors | https://www.epant.gr/ |
| both | Hellenic Competition Commission (EPANT) — Decisions & Opinions portal (EL) | mergers, concentrations, clearances, payments_acquiring, bank_m&a, pub | https://www.epant.gr/apofaseis-gnomodotiseis.html |
| both | Hellenic Competition Commission (EPANT) — Decisions portal (EN) | mergers, concentrations, clearances, payments_acquiring, bank_m&a | https://www.epant.gr/en/decisions.html |
| both | Hellenic Competition Commission (EPANT) — Press Releases (Δελτία Τύπου) | mergers, concentrations, clearances, bank_m&a, payments_acquiring | https://www.epant.gr/enimerosi/deltia-typou.html |
| both | Hellenic Competition Commission (Epitropi Antagonismou) - card interchange enforcement | supervision, regulation | https://www.epant.gr/en/ |
| both | Hellenic Data Protection Authority (DPA/APDPX) — Acts & Decisions (Πράξεις της Αρχής) EL | data_protection, gdpr_fines, banking, payments, mobile_banking, disput | https://www.dpa.gr/el/enimerwtiko/prakseisArxis |
| both | Hellenic Development Bank (HDB) — job vacancies | hiring_signals, procurement, IT_projects | https://hdb.gr/category/theseis-ergasias/ |
| both | Hellenic Financial Ombudsman (HOBIS / Ελληνικός Χρηματοοικονομικός Μεσολαβητής) | financial_disputes, cards, payment_services, adr, fin_net | https://hobis.gr/en/ |
| both | Hellenic Financial Ombudsman (Ελληνικός Χρηματοοικονομικός Μεσολαβητής / ΕΧΜ, ex-HOBIS) | complaints, dispute_resolution, payment_services, cards, fees_charges, | https://hobis.gr/en/category/news/publications/ |
| both | Hellenic Police (Elliniki Astynomia) — official site & procurement | procurement, public contracts, payments | https://www.astynomia.gr/ |
| both | Hellenic Train — Competitions / Διαγωνισμοί | tenders, procurement, ticketing, e-ticketing, payment acceptance | https://www.hellenictrain.gr/en/competitions |
| both | ICAP Career — recruitment listings (banking/finance/IT) | hiring signals, implementation projects, payments, IT | https://icapcareer.com/ |
| both | ICTPLUS.gr — Greek ICT trade press | tenders, procurement, public contracts, e-payments, gov wallet | https://www.ictplus.gr/ |
| both | IDIKA (ΗΔΙΚΑ - Electronic Governance for Social Security S.A.) | jobs, hiring, organization changes | https://www.idika.gr/ |
| both | IMF Financial Access Survey (FAS) - Greece | ATM POS data, market statistics, payment statistics, cash usage | https://data.imf.org/en/datasets/IMF.STA:FAS |
| both | IOBE (Foundation for Economic & Industrial Research) — Electronic Payments in Greece studies | competitors, vendors, case studies, partnerships | https://iobe.gr/en/finance-capital-markets/ |
| both | Indeed Greece (gr.indeed.com) — back-office / call-center aggregator | jobs, hiring | https://gr.indeed.com/Back-Office-jobs |
| both | Indeed Greece (gr.indeed.com) — banking & payments job listings | hiring_weak_signal, payments_transformation, core_banking_migration, p | https://gr.indeed.com/q-banking-%CE%B8%CE%AD%CF%83%CE%B5%CE%B9%CF%82-%CE%B5%CF%81%CE%B3%CE%B1%CF%83%CE%AF%CE%B1%CF%82.html |
| both | Indeed Greece (gr.indeed.com) — banking/fintech listings | hiring_signals, job_postings, fintech, banking | https://gr.indeed.com/Fintech-jobs |
| both | Indeed Greece (gr.indeed.com) — banking/payments search | hiring_signals, banking, payments, POS, SEPA instant payments, core ba | https://gr.indeed.com/ |
| both | Indeed Greece - company job pages (Nexi/Mellon) | jobs, hiring | https://gr.indeed.com/cmp/Nexi-Greece |
| both | Indeed Greece — banking jobs (gr.indeed.com) | hiring_signals, banking, IT_projects, procurement | https://gr.indeed.com/q-banking-l-%CE%91%CE%B8%CE%AE%CE%BD%CE%B1-%CE%B8%CE%AD%CF%83%CE%B5%CE%B9%CF%82-%CE%B5%CF%81%CE%B3%CE%B1%CF%83%CE%AF%CE%B1%CF%82.html |
| both | Ingenico - Careers (jobs.ingenico.com) | jobs, hiring | https://jobs.ingenico.com/ |
| both | Ingenico - Newsroom / Blogs | vendors, partnerships | https://ingenico.com/en/newsroom/blogs |
| both | Ingenico — Newsroom & Payment-Terminals product site (Axium/Move/Desk lines) | POS terminals, vendor deployment, product models | https://ingenico.com/en/newsroom/press-releases |
| both | Ingenico — payment terminals site & press | pos, vendors, terminals, partnerships | https://ingenico.com/en/ |
| both | Ingenico — payment terminals site & press | pos, vendors, terminals, partnerships | https://ingenico.com/en |
| both | Insider.gr - Epiheiriseis (Business) section (insider.gr) | bank vendor deals, payments, acquiring, POS, tender, vendor selection, | https://www.insider.gr/epiheiriseis |
| both | Insider.gr — Technology & Banks sections | banking, digital banking, fintech, technology, vendor deals | https://www.insider.gr/tehnologia |
| both | Insomnia.gr Forums - POS / payments merchant threads | vendors, competitors, partnerships, case studies | https://www.insomnia.gr/forums/ |
| both | Intelli Solutions — corporate site & Quest activity page (banking/cards/payments SI) | public contracts, partnerships, core banking, payments, digital onboar | https://intelli-corp.com/ |
| both | JobFind.gr — Banking category (Τραπεζικά / Banking) | hiring_signals, banking, payments, cards operations, treasury | https://www.jobfind.gr/JobAds/Trapezika-Banking/all/GR/Theseis_Ergasias?cnt=1 |
| both | Jobfind.gr - Greek job board | jobs, hiring | https://www.jobfind.gr/ |
| both | Jobfind.gr — Greek job board (banking/payments, Athens) | procurement, hiring signals, cards, POS, core banking | https://www.jobfind.gr/JobAds/all/Athens/GR/Theseis_Ergasias |
| both | Jobily.gr - Nexi Greece openings | jobs, hiring | https://jobily.gr/company/5f7ace3b-98f6-1187-1dfb-fac03ba6e720 |
| both | Jobs by Workable — Greece software-engineer aggregator | jobs, hiring, organization changes | https://jobs.workable.com/search/greece/software-engineer-jobs |
| both | Jooble Greece (gr.jooble.org) | jobs, hiring | https://gr.jooble.org/ |
| both | KPMG Greece - Executive Search & Selection (People Services) | hiring, leadership moves, organization changes | https://kpmg.com/gr/en/services/advisory/management-consulting/people-services/executive-search-selection.html |
| both | Karatzas & Partners - Publications / contributed banking briefs | regulation, supervision, deadlines, banking, payments | https://karatza-partners.gr/ |
| both | Lawspot.gr - Greek legal news (banking/payments legislation) | regulation, supervision, deadlines, banking, payments | https://www.lawspot.gr/ |
| both | Liberal.gr | banks, fintech, payments vendors, awards-derived vendor signals | https://www.liberal.gr/ |
| both | LinkedIn Jobs - vendor/integrator company pages (Greece) | jobs, hiring, leadership moves, organization changes | https://gr.linkedin.com/jobs/mellon-technologies-jobs |
| both | LinkedIn Jobs — Greece Payments feed | jobs, hiring, organization changes | https://gr.linkedin.com/jobs/payments-jobs |
| both | LinkedIn Jobs — Greece bank/payments/project-manager searches | hiring signals, implementation projects, procurement, vendor managemen | https://gr.linkedin.com/jobs/bank-jobs |
| both | LinkedIn Jobs — Greece banking & fintech (aggregator + company jobs tabs) | hiring_signals, job_postings, fintech, banking, actor_discovery | https://gr.linkedin.com/jobs/fintech-jobs |
| both | LinkedIn Jobs — Greece banking/procurement facets + bank company pages | tenders, procurement, hiring_signals, vendor_management, payments, cor | https://gr.linkedin.com/jobs/banking-jobs |
| both | LinkedIn — foreign-bank Greece company pages & people search | leadership moves, hiring, organization changes | https://gr.linkedin.com/company/deutsche-bank |
| both | ManpowerGroup Greece — Workable ATS + LinkedIn (banking-IT staffing) | hiring_signals, IT_projects, procurement, vendor_management, payments | https://apply.workable.com/manpowergroup-greece-1/ |
| both | Mastercard Careers - Athens, Greece | jobs, hiring | https://careers.mastercard.com/us/en/athens-greece |
| both | Mastercard Europe - Greece intracountry / domestic interchange fee schedules | regulation, deadlines | https://www.mastercard.com/europe/en/business/support/merchant-interchange-rates.html |
| both | Mastercard Newsroom — Europe (press releases) | card scheme, issuing, tokenization, partnership, agentic commerce | https://www.mastercard.com/news/europe/en/newsroom/press-releases/ |
| both | Mastercard Newsroom — global | partnerships, vendors, competitors | https://newsroom.mastercard.com/ |
| both | McKinsey & Company — Global Payments Report & FS insights | competitors, vendors, partnerships | https://www.mckinsey.com/industries/financial-services/our-insights/global-payments-report |
| both | Mellon Group / Mellon Technologies - Payment Solutions | payments software, POS/EFTPOS, card issuing and acquiring, vendor cust | https://mellongroup.com/solutions/payment-solutions |
| both | Mellon Group of Companies - Careers (Workable) | jobs, hiring, organization changes | https://apply.workable.com/mellongroup/ |
| both | Mellon Group of Companies — banking BPO, staffing & payments outsourcing | jobs, hiring, organization changes | https://mellongroup.com/services/outsourcing-services |
| both | Mellon Group — Mobile Payments / POS solutions | procurement, partnerships, public contracts | https://mellongroup.com/solutions/mobile-payments |
| both | Mellon Group — News | payments, ATM, POS, card personalization, bank managed services, vendo | https://mellongroup.com/news/ |
| both | Mellon Technologies (Greece) - General Terms of Transactions | compliance, terms_update | https://eshop.mellontechnologies.gr/genikoi-oroi-synallagon/ |
| both | Mellon Technologies — Careers / LinkedIn | hiring_signals, job_postings, pos, card_technology, bpo | https://mellongroup.com/companies/mellon-technologies |
| both | Mellon Technologies — careers (payments / next-gen branch) | hiring_weak_signal, payments_transformation, atm_pos, vendor_staffing, | https://www.kariera.gr/en/companies/mellon-technologies |
| both | Ministry of National Economy & Finance — IRIS mandate / policy announcements | instant payments, IRIS, mandate, public contracts, procurement | https://minfin.gov.gr/apo-1i-noemvriou-ameses-pliromes-iris-choris-promitheia-se-oles-tis-epicheiriseis-se-fysika-kai-ilektronika-katastimata/ |
| both | Mobile & IoT Awards / Mobile Excellence Awards (Boussias + AUEB ELTRUN) | vendors, competitors, case studies, partnerships | https://m-awards.boussiasevents.gr/past-winners/ |
| both | Moneyonline.gr - Banking news & POS guides | ATM POS data, payment statistics, card statistics | https://www.moneyonline.gr/news/trapezika/ |
| both | Mononews.gr — Banks (/category/trapezes) & Business categories | banking, payments, vendor wins, fintech, public contracts | https://www.mononews.gr/category/trapezes |
| both | NBG Pay (National Bank of Greece / Global Payments) - POS Terms | regulation, compliance, terms_update, deadlines | https://nbgpay.globalpayments.com/el-gr |
| both | NBG Pay press office (National Bank of Greece) | press releases, acquiring, partnerships | https://www.nbg.gr/en/group/press-office/nbg-pay |
| both | NBG Pay — LinkedIn company page (National Bank of Greece payments arm) | hiring, leadership moves, organization changes | https://www.linkedin.com/company/nbg-pay |
| both | NBG — Financial Statements (Annual & Interim) | annual reports, disclosures, financial statements | https://www.nbg.gr/en/group/investor-relations/financial-statements-annual-interim |
| both | NCR Atleos — Insights / Case Studies (Greek deployments) | ATM software, managed services, maintenance contracts, vendor wins, de | https://www.ncratleos.com/insights/eurobank-greece |
| both | NCR Atleos — Insights / Customer Stories | ATM, software, deployment, public contracts, award notices | https://www.ncratleos.com/insights?category=Customer+Stories |
| both | NCR Atleos — banking self-service site & customer stories | atm, self-service, software, contracts, case_studies | https://www.ncratleos.com/banking/atm-itm |
| both | NEPPS public tender search (nepps-search.eprocurement.gov.gr) | tenders, procurement, framework agreements, dynamic purchasing systems | https://nepps-search.eprocurement.gov.gr/ |
| both | NFCW — Greece country archive (payments-tech aggregator) | contactless/NFC, transit fare payments, IRIS/instant payments, digital | https://www.nfcw.com/country/greece/ |
| both | Naftemporiki (Η ΝΑΥΤΕΜΠΟΡΙΚΗ) — Finance & Business sections | tenders, procurement, public contracts, award notices, banking, paymen | https://www.naftemporiki.gr/finance/ |
| both | National Bank of Greece (NBG) Developer Portal | open banking API, AIS, PIS, confirmation of funds, premium APIs | https://developer.nbg.gr/ |
| both | National Bank of Greece (NBG) — Jobs at NBG | core banking, IT hiring, procurement, internships | https://www.nbg.gr/en/group/human-resources/career-opportunities/jobs-nbg |
| both | National Bank of Greece (NBG) — cards / scheme programme pages | card issuing, scheme migration, co-brand, tokenisation, procurement si | https://www.nbg.gr/el/idiwtes/kathimerines-sunallages/trapezikes-kartes |
| both | National Bank of Greece — Job Positions / Θέσεις Εργασίας Εθνικής Τράπεζας | jobs, hiring, organization changes | https://www.nbg.gr/el/omilos/anthrwpino-dunamiko/eukairies-karieras/theseis-ergasias-ethnikh-trapeza |
| both | Netcompany-Intrasoft / vendor company LinkedIn pages (win announcements) | procurement, award notices, core banking | https://www.linkedin.com/company/netcompany-intrasoft-sa |
| both | Netcompany-Intrasoft Banking News (PROFITS core banking) | core_banking, migrations, wins, implementations | https://banking.netcompany-intrasoft.com/ |
| both | Netcompany-Intrasoft Careers (SmartRecruiters ATS) | hiring_signals, core banking, payments, system integration, IT | https://careers.smartrecruiters.com/NetcompanyIntrasoft |
| both | Newsit.gr - Economy/Technology section | vendors, partnerships, case studies | https://www.newsit.gr/oikonomia/ |
| both | Nexi Greece / XPay - IRIS acceptance integration (developer portal & press) | instant payments, acceptance, vendor signals | https://developer.nexigroup.com/xpaygreece/en-EU/docs/iris-payments/ |
| both | Nexi Greece — LinkedIn company page (Nexi Processing Services Greece) | hiring, jobs, leadership moves, organization changes | https://www.linkedin.com/company/nexi-greece |
| both | Nexi Greece — POS terminal product catalogue (wired / wireless / SmartPOS) | POS terminals, Ingenico, Verifone, PAX, SmartPOS, acquirer deployment | https://www.nexi.gr/en/pos/ |
| both | Nexi Group - Sustainability Report (Nexi Greece parent) | disclosures, annual reports, ESG, sustainability, non-financial statem | https://www.nexigroup.com/en/esg/overview/overview/ |
| both | Nexi Group Investor Relations - financial results presentations | market statistics, card statistics, payment statistics, ATM POS data | https://www.nexigroup.com/en/investor-relations/overview/ |
| both | Nexi Group press releases archive | press releases, disclosures, partnerships, earnings | https://www.nexigroup.com/en/media-relations/press-releases/ |
| both | Nexi Group — Media Relations / News (Nexi Payments Greece) | vendor selection, payments, award notices | https://www.nexigroup.com/en/media-relations/news/ |
| both | Nexi Group — careers / job openings (Athens hub) | hiring_signals, payments, IT_projects, vendor_management | https://www.nexigroup.com/en/people/careers/job-openings/ |
| both | Nexi Payments Greece - Newsroom / Business | press releases, disclosures, pos deployment | https://www.nexi.gr/en/ |
| both | Nexi Payments Greece - Terms & Conditions / Processing | regulation, compliance, terms_update, supervision | https://www.nexi.gr/el/oroi-kai-proypotheseis/ |
| both | Nexi Payments Greece — POS terminal product pages (Ingenico / PAX models) | POS terminals, vendor models, SmartPOS, acquiring | https://www.nexi.gr/en/business/ |
| both | OASA POS card-acceptance terminals tender (Athens urban transport) | tenders, procurement | https://www.oasa.gr/blog/ |
| both | OASA — public POS-terminal tender (Athens transport) example / issuing authority | tenders, procurement, public_contracts, pos | https://www.oasa.gr/ |
| both | OSETH — Transport Authority of Thessaloniki (TheTA) | tenders, procurement, e-ticketing, contactless payments, smart card | https://oseth.com.gr/el |
| both | OTE/Cosmote Group Careers & Cosmote e-Value (BPO for banks/payments) | vendors, partnerships | https://www.cosmote.gr/static/otegroup/en/careers-home.html |
| both | Oikonomikos Tachydromos (ot.gr) - Banks / Tiresias tags | leadership moves, organization changes | https://www.ot.gr/tag/teiresias/ |
| both | Open Banking Tracker - Attica Bank / Greek providers (API & open banking) | vendors, partnerships | https://www.openbankingtracker.com/provider/atticabank-gr |
| both | OpenGov.gr (Ministry of Finance) — public consultation on PSD2 transposition / Art.14 BoG register | consultations, regulation, deadlines | https://archive.opengov.gr/minfin/?p=8090 |
| both | Optima bank – Investor Relations / Share Announcements | leadership moves, board changes, organization changes | https://www.optimabank.gr/about-us/investor-relations/stoixeia-metoxis/stoixeia-metoxis-anakoinoseis/ |
| both | PAX Global Technology - Latest News | vendors, partnerships | https://www.paxglobal.com.hk/en/latest-news/ |
| both | PAX Global Technology — Newsroom (Greece deployments via Transaction Systems) | POS terminals, vendor deployment, SmartPOS, market entry | https://www.paxglobal.com.hk/en/latest-news/pax-android-terminals-delivering-applications-for-restaurants-and-retailers-in-greece/ |
| both | PAX Technology — Blog / News (International) | POS, terminals, deployment, certification, public contracts | https://www.paxtechnology.com/blog |
| both | PAX Technology — POS terminals (deployed via GR acquirers) | pos, terminals, vendors | https://www.paxtechnology.com/ |
| both | PEE 190/2/16.6.2021 - ICT and security risk management framework (PDF) | ICT risk, τπε, cybersecurity, security risk management, vendor governa | https://www.bankofgreece.gr/RelatedDocuments/%CE%A0%CE%95%CE%95_190-%CE%98%CE%AD%CE%BC%CE%B1_2.pdf |
| both | PR Newswire — vendor payments/ATM press-release distribution | ATM, POS, deployment, public contracts, award notices | https://www.prnewswire.com/news/diebold-nixdorf/ |
| both | PYMNTS | vendors, partnerships, case_studies, competitors | https://www.pymnts.com/fintech-payments/ |
| both | PYMNTS.com — Greece bank & payments partnerships / tags | merchant acquiring, vendor-bank contracts, payments processing, M&A, r | https://www.pymnts.com/tag/evo-payments/ |
| both | PYMNTS.com — Greece payments/fintech coverage | digital payments, acquiring, partnerships, investment, litigation | https://www.pymnts.com/ |
| both | Pancreta Bank API Portal (PSD2) | open banking API, AIS, PIS, PSD2 | https://developer.crediabank.com/ |
| both | Patras Port Authority (OLPA) — Tenders / Announcements | tenders, procurement, public contracts, payment terminals, parking | https://patrasport.gr/en/tenders-announcements/ |
| both | PaymentComponents (aplonHUB / FINaplo / aplonAPI) | regulation, deadlines | https://www.paymentcomponents.com/ |
| both | Paymentology — Snappi partnership / press (issuer-processor vendor) | issuer processor, card processing, neobank infrastructure, vendor deal | https://www.paymentology.com/newsroom |
| both | Payments Dive | organization changes, leadership moves | https://www.paymentsdive.com/ |
| both | Piraeus Bank / Piraeus Financial Holdings Careers (Workable ATS) | procurement, hiring signals, cards, POS, core banking, ISO 20022 | https://apply.workable.com/piraeus-bank/?lng=en |
| both | Piraeus Bank rAPIdLink Developer Portal (PSD2) | open banking API, Berlin Group XS2A, AIS, PIS, swagger spec | https://rapidlink.piraeusbank.gr/ |
| both | Piraeus Bank — Careers (Workable ATS) | hiring_signals, job_postings, digital_payments, acquiring | https://apply.workable.com/piraeus-bank/ |
| both | Piraeus Bank — LinkedIn company page & Jobs tab | jobs, hiring, leadership moves, organization changes | https://www.linkedin.com/company/piraeus-bank |
| both | Piraeus Bank — wired/wireless POS terminal (PayCenter) product pages | POS terminals, merchant acquiring, PayCenter, wired/wireless terminals | https://www.piraeusbank.gr/el/epiheiriseis-epaggelmaties/anakalypse-ta-xrimatodotika-ergaleia-sou/lyseis-emporon/collections-eisprakseis/pos-paycenter-gia-epixeirhseis-epaggelmaties/ensurmata-termatika-pos |
| both | Piraeus Financial Holdings / Group — Relationship with Suppliers (ESG page) | procurement, Coupa, supplier management, tenders, prequalification | https://www.piraeusgroup.gr/en/esg/corporate-governance/sxeseis-me-promitheytes |
| both | Piraeus Group — Coupa supplier & procurement platform (operational tender portal) | procurement, tenders, vendor_registration, suppliers | https://piraeusbank.coupahost.com/ |
| both | Piraeus — Financial Statements & Other Information / Results Presentations (Greek + English) | card statistics, payment statistics, market statistics | https://www.piraeusgroup.gr/en/investor-relations/oikonomikes-katastaseis-loipes-plhrofories |
| both | Piraeus — Sustainability & Business Report (Annual Report) PDF | card statistics, payment statistics, market statistics | https://www.piraeusholdings.gr/en/investors/financials/annual-reports |
| both | Printec Blog (EFT-POS & ATM landscape CEE) | atm, pos, market_landscape, self-service | https://blog.printecgroup.com/ |
| both | Printec Group - Careers (Workable) | jobs, hiring, leadership moves, organization changes | https://apply.workable.com/printec/ |
| both | Printec Group - LinkedIn company page | vendors, partnerships, case studies | https://www.linkedin.com/company/printec-group-of-companies |
| both | Printec Group - Solutions, Resources & Blog (EFT-POS & ATM landscape CEE) | ATM data, POS data, installed base, market statistics | https://www.printecgroup.com/resources/ |
| both | Printec Group — Careers / Apply-for-a-job | hiring signals, implementation projects, POS, ATM, self-service, vendo | https://www.printecgroup.com/careers/apply-for-a-job/ |
| both | Printec Group — Newsroom / News | ATM software, self-service, LiveBank, Cashflex, systemic banks, POS | https://www.printecgroup.com/news/ |
| both | Printec Group — Newsroom / Printec Greece | ATM, POS, self-service, contract, procurement | https://www.printecgroup.com/country/printec-greece/ |
| both | Printec Group — careers (ATM/POS/payments vendor) | hiring_weak_signal, atm_pos, vendor_staffing, digital_onboarding, proc | https://www.printecgroup.com/careers/ |
| both | Printec Group — corporate site (NCR representative & ATM/POS integrator in Greece) | maintenance contracts, ATM deployment, POS terminals, vendor wins, sys | https://www.printecgroup.com/ |
| both | Public hospital procurement pages — δημόσιοι ανοικτοί διαγωνισμοί (e.g. Παίδων Αγία Σοφία, ΑΧΕΠΑ, ΠΓΝ Πατρών/Αλεξανδρούπολης) | tenders, procurement, public contracts | https://paidon-agiasofia.gr/diagonismoi-prokiryxeis/dimosioi-anoiktoi-diagonismoi/ |
| both | PwC Legal - Regulatory Radar / RegCORE (EU FS regulatory monitoring) | regulation, deadlines, consultations | https://legal.pwc.de/en/services/pwc-legals-eu-regulatory-compliance-operations |
| both | Pylones Hellas — News/Press (cyber-security awards) | cyber security, banking, SOC, SIEM, vendor selection | https://www.pylones.gr/ |
| both | QUALCO Group — open positions (careers) | credit tech, banking software, vendor hiring, procurement | https://qualco.group/open-positions/ |
| both | QUALCO — careers / open positions (bank tech vendor) | hiring_weak_signal, vendor_staffing, bank_platform_delivery, procureme | https://www.qualco.tech/careers/open-positions |
| both | QUBE Events — NextGen Payments & RegTech Forum, Athens (sponsors/contributors/speakers) | payments, regtech, open banking, digital euro, compliance, conference  | https://www.qubevents.com/nextgen-payments-regtech-athens |
| both | Quality & Reliability (Q&R) — corporate site / Financial Services | tenders, procurement, award notices, digital banking, POS, ATM, system | https://www.qnr.com.gr/el/ |
| both | Quest Holdings — Uni Systems (banking IT integrator) annual/consolidated financials | banking IT integrator, consolidated financial statements, subsidiary d | https://www.quest.gr/en/activities/Uni-Systems |
| both | RBR Data Services (Datos Insights) — Global ATM Intelligence & Retail Cash Automation | ATM POS data, cash usage, card statistics, payment statistics | https://datos-insights.com/what-we-offer/rbr-data-services/banking-automation/global-atm-intelligence-service/ |
| both | Randstad Greece — Banking / IT jobs (recruiter listings) | procurement, hiring signals, POS, payment terminals, core banking, acq | https://www.randstad.gr/en/jobs/q-banking/ |
| both | Randstad Greece — banking/IT job listings | hiring_signals, banking, payments, IT | https://www.randstad.gr/en/jobs/q-banking/attica/piraeus-centre/ |
| both | Recruiter LinkedIn pages posting GR bank/payments hiring (Randstad Hellas, Adecco) — INDIRECT | hiring, jobs | https://www.linkedin.com/company/randstad-hellas |
| both | Register of Electronic Money Institutions authorised in Greece (Μητρώο Ιδρυμάτων Ηλεκτρονικού Χρήματος) | e-money institutions, ηλεκτρονικό χρήμα, EMI, register | https://www.bankofgreece.gr/RelatedDocuments/7_Electronic_Money_Institutions_Register.xlsx |
| both | Register of payment institutions authorised in Greece (Μητρώο Ιδρυμάτων Πληρωμών) | payment institutions, ιδρύματα πληρωμών, PSD2, authorisation, register | https://www.bankofgreece.gr/RelatedDocuments/6_PaymentInstitutions.xls |
| both | Relational Financial Solutions — corporate site & partnerships (PROFITS/Netcompany implementation partner) | public contracts, partnerships, core banking, payments implementation | https://www.relationalfs.com/ |
| both | Reporter.gr - Technology section | vendors, competitors, partnerships | https://www.reporter.gr/eidhseis/technologia |
| both | Reporter.gr — Companies/Banks | earnings, press_releases, disclosures | https://www.reporter.gr/eidhseis/epicheirhseis/trapezes |
| both | Reuters — Greece / Greek banks coverage | bank M&A, acquiring, privatisation, deals | https://www.reuters.com/ |
| both | Revolut (Greece) - Legal Terms el-GR | regulation, compliance, terms_update, supervision | https://www.revolut.com/el-GR/legal/terms/ |
| both | Rokas International Law Firm - Banking & Finance / payments insights | regulation, supervision, payments, banking | https://rokas.com/banking-finance/ |
| both | S&P Global Ratings - Greek banks (English rating commentary) | disclosures, investor relations | https://www.spglobal.com/ratings/en |
| both | SDIT.gov.gr — Special Secretariat for Public-Private Partnerships | public-private partnership, e-ticketing, procurement, public contracts | http://sdit.gov.gr/ |
| both | SGS Greece — PCI / EMVCo / Mastercard / Visa security evaluation lab | certification, standards, vendor-selection | https://www.sgs.com/en-gr/services/pci-security-evaluation-services |
| both | SMARTEC — PAX terminal distributor in Greece (via Transaction Systems) | POS terminals, distribution, spare parts, vendor channel | https://smartec.gr/en.html |
| both | STASY S.A. (Statheres Sygkoinonies) — Tenders in force (Διαγωνισμοί σε ισχύ) | tenders, procurement, e-ticketing, contactless payments, fare collecti | https://www.stasy.gr/en/ |
| both | Shop X Conference (Greek retail-tech conference) | vendors, partnerships | https://www.shopxconference.gr/ |
| both | Sifted - Greece country page | competitors, vendors, partnerships, case_studies | https://sifted.eu/countries/greece |
| both | Skroutz corporate newsroom & Skroutz.gr blog | partnership announcements, PSP selection, acquiring, e-commerce paymen | https://corporate.skroutz.gr/press-el/ |
| both | Skywalker.gr — Greek job board | hiring_signals, job_postings, payments | https://www.skywalker.gr/elGR/categories |
| both | Skywalker.gr — Greek job board (banking/IT/payments) | procurement, hiring signals, cards, POS, core banking | https://www.skywalker.gr/en |
| both | Skywalker.gr — job board & employer profiles (staffing agencies) | jobs, hiring | https://www.skywalker.gr/ |
| both | Snappi (neobank) — LinkedIn people & company presence | leadership moves, hiring, jobs, organization changes | https://www.linkedin.com/in/navrozoglou |
| both | Snappi / Plum careers on Workable (jobs boards) | hiring signals, tech stack, payment rails, vendor procurement | https://apply.workable.com/snappibank/ |
| both | Snappi on LinkedIn (company page) — proxy newsroom | product launch, funding, partnership, hiring | https://www.linkedin.com/company/snappibank |
| both | Sofokleousin.gr - fintech / startups coverage | partnerships, vendors, competitors, case studies | https://www.sofokleousin.gr/ |
| both | Sofokleousin.gr — Τράπεζες | regulation, consultations, deadlines | https://www.sofokleousin.gr/tags/trapezes |
| both | Space Hellas - Career Opportunities | jobs, hiring, organization changes | https://www.space.gr/en/career |
| both | Statista - Greece card/POS/ATM/cash statistics pages | card statistics, payment statistics, cash usage, market statistics | https://www.statista.com/statistics/866459/number-of-pos-transactions-greece/ |
| both | Statista — Digital Payments Greece (Market Insights / Forecast) | payment statistics, market statistics, ATM POS data | https://www.statista.com/outlook/fmo/digital-payments/greece |
| both | Survey on the Use of ICT by Households and Individuals - incl. e-commerce & internet banking (Έρευνα Χρήσης ΤΠΕ από Νοικοκυριά και Άτομα) | payment statistics, card statistics, cash usage, market statistics | https://www.statistics.gr/en/statistics/-/publication/SFA20/- |
| both | TED (Tenders Electronic Daily) — Bank of Greece contracting-authority notices | tenders, procurement, public contracts, award notices, banknote printi | https://ted.europa.eu/en/search/result?scope=ALL&text=%22Bank%20of%20Greece%22 |
| both | TED CPV — Common Procurement Vocabulary (code list & browse-by-sector) | procurement, banking, payments, financial IT | https://ted.europa.eu/en/simap/cpv |
| both | TED Expert Search (query language) | tenders, procurement, public contracts, award notices | https://ted.europa.eu/en/help/search-browse |
| both | TED Search API (v3, no authentication) | procurement, tenders, awards, open data, bulk XML | https://docs.ted.europa.eu/api/latest/search.html |
| both | TED Search API (v3, unauthenticated) | tenders, procurement, banking, payments, financial IT | https://api.ted.europa.eu/v3/notices/search |
| both | TED eNotices2 — EU procurement notices submission/index (enotices2.ted.europa.eu) | tenders, award notices, procurement, public contracts, above-threshold | https://enotices2.ted.europa.eu/ |
| both | TED — Tenders Electronic Daily (EU Official Journal supplement) | public-procurement, tenders, e-payments, EU-funded, disclosures | https://ted.europa.eu/en/ |
| both | Talent.com Greece (gr.talent.com) | jobs, hiring | https://gr.talent.com/en/jobs |
| both | Taxheaven — IRIS technical-spec & regulatory news aggregator | regulation, deadlines, instant_payments, consultations | https://www.taxheaven.gr/news/72117/iris-apo-112-stis-lianikes-synallages-b2c-nees-texnikes-prodiagrafes-diasyndeshs |
| both | Taxheaven — Law 4557/2018 consolidated (codified AML law tracker) | regulation, deadlines, supervision | https://www.taxheaven.gr/law/4557/2018 |
| both | Taxheaven — codified Greek law database (banking/payments statutes) | regulation, deadlines | https://www.taxheaven.gr/law/4537/2018 |
| both | Taxheaven.gr - tax & payments professional news | IRIS instant payments, POS interconnection, technical specifications,  | https://www.taxheaven.gr/news/70924/iris-diplasiazetai-ws-to-telos-toy-etoys-to-hmerhsio-orio-synallagwn-apo-0111-ypoxrewtikh-h-enswmatwsh-toy-sta-pos |
| both | Taxheaven.gr — tax/legal news portal reproducing ΦΕΚ acts (BoG licensing acts) | licensing, payment_institutions, e_money_institutions, statutory_acts | https://www.taxheaven.gr/ |
| both | TechSaloniki — tech recruitment fair (participating companies + job openings) | vendors, competitors, partnerships | https://techsaloniki.gr/techsalonikix/job-openings/ |
| both | Teleperformance Greece (TP Greece) — contact-centre / BPO mass hiring | jobs, hiring | https://gr.linkedin.com/jobs/teleperformance-jobs |
| both | Temenos Careers (Workday) — Greece-tagged roles | procurement, hiring signals, core banking, Temenos, migration, impleme | https://temenos.wd103.myworkdayjobs.com/Temenoscareers |
| both | Tender Service M.E.P.E. (tender-service.com) — Public tenders in Greece | tenders, procurement, public contracts, award notices | https://www.tender-service.com/international/greece |
| both | ThPA S.A. / ΟΛΘ — Οργανισμός Λιμένος Θεσσαλονίκης, Διαγωνισμοί και Προμήθειες | tenders, procurement, public contracts | https://www.thpa.gr/category/news-en-gb/tenders-procurement/ |
| both | The Berlin Group - openFinance / NextGenPSD2 SEPA API standards | regulation, deadlines | https://www.berlin-group.org/open-finance |
| both | The Business of Payments (Geoffrey Barraclough) - acquirer analysis | market statistics, payment statistics, ATM POS data | https://businessofpayments.com/tag/nexi/ |
| both | The Digital Banker — Global Retail Banking / Cards & Payments Innovation Awards | vendors, competitors, case studies, partnerships | https://thedigitalbanker.com/awards/ |
| both | The Information (theinformation.com) | organization changes, leadership moves | https://www.theinformation.com/ |
| both | The Paypers - DIAS / IRIS / EuroPA payments news | instant payments, vendor signals, cross-border, product launches | https://thepaypers.com/payments/news/dias-brings-iris-across-all-physical-and-online-stores |
| both | The Paypers - Greek fintech/payments news | press releases, disclosures | https://thepaypers.com/ |
| both | The Paypers — DIAS / IRIS / EuroPA payments-industry news | instant payments, IRIS, EuroPA, partnerships, vendors | https://thepaypers.com/payments/news/iris-payments-connects-greece-with-european-europa-network |
| both | The Paypers — Payments & Fintech News (Greece coverage) | payments, merchant acquiring, vendor-bank contracts, fintech partnersh | https://thepaypers.com/news |
| both | The Paypers — payments/fintech news (Greece coverage) | payments, acquiring, bank partnerships, vendor wins, fintech deals | https://thepaypers.com/payments/news |
| both | Thessaloniki Metro (Elliniko Metro / ThessMetro) — tickets & fare systems | e-ticketing, contactless payments, smart card, fare collection hardwar | https://www.thessmetro.gr/en/tickets/ |
| both | Tink (Visa) — open banking coverage / Greece connectivity | account aggregation, payment initiation, coverage, TPP | https://tink.com/ |
| both | Top Employers Institute — Certified employers search (Greece) | hiring, organization changes, jobs | https://www.top-employers.com/search-top-employers/ |
| both | Tora Wallet (OPAP Group) - Regulatory Announcements & Terms (EMI) | regulation, licensing, supervision, compliance | https://investors.opap.gr/el-gr/results-and-news/news/regulatory-announcements |
| both | Tora Wallet (OPAP group) — e-money institution official site | e-money institution, cash-in network, bill payments, vendor partnershi | https://torawallet.gr/ |
| both | Transaction Systems - PAX master distributor (CE/SEE) | vendors, partnerships | https://www.tpspay.com/terminals |
| both | Trustpilot - viva.com / Viva Wallet reviews | vendors, competitors, case studies, partnerships | https://www.trustpilot.com/review/viva.com |
| both | Uni Systems (Quest) Banking & Finance industry section | core banking, payments, cards, treasury, AML/KYC compliance, bMASTER,  | https://www.unisystems.com/industries/banking-finance |
| both | Uni Systems — Banking & Finance / Payment solutions | tenders, procurement, award notices, payments, treasury, system integr | https://www.unisystems.com/solutions/vertical-solutions/banking-sector-solutions/payment |
| both | UnionPay International — Newsroom / Company News (Greece items) | card acceptance, card issuing, acquiring, scheme partnership | https://www.unionpayintl.com/en/mediaCenter/newsCenter/companyNews/ |
| both | Unit A — Hellenic Financial Intelligence Unit (HFIU) | regulation, supervision, deadlines | https://fiu.aml-authority.gov.gr/en/ |
| both | University of Piraeus — Dept. of Banking & Financial Management + FinTech & Quantitative Finance Laboratory (FinTechQF Lab) | fintech, payment statistics, digital transactions | https://bankfin.unipi.gr/fql/ |
| both | VIXIO Regulatory Intelligence - payments compliance platform | regulation, supervision, deadlines | https://www.vixio.com/ |
| both | Vendor award-announcement pages (Performance Technologies, Netcompany, Info Quest, Profile Software, Worldline Greece) | vendors, partnerships, case studies | https://www.performance.gr/digital-finance-awards2024/ |
| both | Vendor legal/imprint & company pages disclosing entity + ΦΕΚ/ΑΦΜ/ΓΕΜΗ (Worldline, Everypay, Nexi, Cardlink) | vendor entity resolution, licensing, ownership | https://worldline.com/el-gr/compliancy/imprint |
| both | Verifone — Newsroom | POS, terminals, deployment, public contracts | https://www.verifone.com/en/global/newsroom |
| both | Verifone — corporate site & terminal documentation (as deployed in GR) | pos, terminals, vendors | https://www.verifone.com/en/global |
| both | Visa Corporate/Global Newsroom (press releases + investor news) | card_schemes, partnerships, payments, fintech | https://usa.visa.com/about-visa/newsroom/press-releases-listing.html |
| both | Visa Europe - fees and interchange (EEA / Greece) | regulation, deadlines | https://www.visa.co.uk/about-visa/visa-in-europe/fees-and-interchange.html |
| both | Visa Europe Newsroom / Press Releases | press releases, earnings, disclosures, partnerships, contactless, toke | https://www.visaeurope.lu/en_LU/about-visa/newsroom/press-releases.html |
| both | Visa Global Careers (Greece roles) | jobs, hiring | https://corporate.visa.com/en/careers.html |
| both | Visa Global Newsroom (corporate.visa.com / usa.visa.com) | press releases, disclosures, tokenisation, partnerships | https://usa.visa.com/about-visa/newsroom.html |
| both | Visa Global Newsroom (press releases) | partnerships, certification, procurement, award notices | https://www.visa.com/about-visa/newsroom.html |
| both | Visa Greece Newsroom (Mynewsdesk press room) | card_schemes, partnerships, payments, fintech, tokenization | https://www.mynewsdesk.com/gr/visa |
| both | Visa Inc. Investor Relations — News Releases | market statistics, payment statistics | https://investor.visa.com/news/default.aspx |
| both | Visa Inc. — Investor Relations press releases (gcs-web) | partnerships, vendors, competitors | https://visa.gcs-web.com/ |
| both | Visa Perspectives — Trends & Insights (Greece country data notes) | card statistics, payment statistics, cash usage, market statistics | https://corporate.visa.com/en/sites/visa-perspectives/trends-insights.html |
| both | Visa Ready Program (certification programme page) | certification, vendor-selection | https://partner.visa.com/site/programs/visa-ready.html |
| both | Viva.com (Viva Payment Services / VivaBank) - Company & Newsroom | leadership moves, organization changes, hiring | https://www.viva.com/en-gr/about/the-company |
| both | Viva.com (Viva Wallet Group) — corporate / newsroom | product launches, market expansion, merchant deals, acquiring, banking | https://www.vivawallet.com/ |
| both | Viva.com (Viva Wallet) - Blog / Press & product | vendors, competitors, partnerships | https://www.viva.com/el-gr/blog |
| both | Viva.com (Viva Wallet) - Financial Statements & Reports page | disclosures, annual reports, ESG, sustainability, non-financial statem | https://www.viva.com/en-gr/financial-statements |
| both | Viva.com (Viva Wallet) - newsroom | press releases, investor relations, earnings | https://www.viva.com/ |
| both | Viva.com (Viva Wallet) careers board on Workable | jobs, hiring, organization changes, leadership moves | https://apply.workable.com/viva/ |
| both | Viva.com (Viva Wallet) — Jobs in Greece | hiring_signals, payments, POS, acquiring, card issuing | https://gr.linkedin.com/jobs/viva-wallet-jobs-greece |
| both | Viva.com (Viva Wallet) — careers / jobs | hiring signals, implementation projects, acquiring, POS, payments | https://gr.linkedin.com/jobs/viva-wallet-jobs |
| both | Viva.com / VIVABANK - Financial Statements & Reports | annual reports, disclosures, earnings | https://www.viva.com/el-gr/financial-statements |
| both | Viva.com / Vivabank - Terms Portal & Corporate Governance | regulation, compliance, terms_update, supervision, licensing | https://www.viva.com/el-gr/terms-portal |
| both | Viva.com / Vivabank — official site, newsroom & developer release notes | neobank, EMI, acquiring, card issuing, vendor partnerships, Tap on Any | https://www.viva.com/en-eu |
| both | Viva.com — Blog / Newsroom (Greece) | acquiring, Tap_to_Pay, SoftPOS, merchant_services, product_launch, M&A | https://www.viva.com/en-gr/blog |
| both | Viva.com — Blog / Press (newsroom) | product launch, acquiring, lending, expansion, partnership, instant pa | https://www.viva.com/en-eu/blog |
| both | Viva.com — Careers (site + Workable ATS) | hiring_signals, job_postings, acquiring, card_issuing, aml_compliance, | https://www.viva.com/en-gr/about/careers |
| both | Viva.com — LinkedIn company & jobs page | leadership moves, hiring, organization changes | https://gr.linkedin.com/company/viva-com/jobs |
| both | Viva.com — LinkedIn company page & Jobs | jobs, hiring, leadership moves, organization changes | https://gr.linkedin.com/company/viva-com |
| both | Woli Fintech — LinkedIn company page | hiring, jobs, organization changes | https://www.linkedin.com/company/woli-fintech |
| both | Woli — Greek family/teen neobank (E-money distributor) site & 'Woli for Banks' | neobank, e-money distributor, prepaid Mastercard, BaaS partner, card i | https://www.woli.io/ |
| both | Woli — Press (Τι έγραψαν για εμάς) | card issuing, youth banking, funding, expansion | https://www.woli.io/woli-press/ |
| both | Woli — kids/teen family banking fintech (site) | partnerships, vendors, competitors | https://woli.io/ |
| both | Workenter.gr - Δημόσιο/ΑΣΕΠ recruitment news | jobs, hiring, organization changes | https://workenter.gr/category/dimosio-asep |
| both | Workenter.gr — recruitment-news republisher (bank hiring rounds) | hiring_weak_signal, pointer_to_bank_careers, payments_transformation,  | https://workenter.gr/ |
| both | World Bank DataBank / WDI & data360 - Greece financial-infrastructure indicators | ATM POS data, market statistics | https://data.worldbank.org/indicator/FB.ATM.TOTL.P5?locations=GR |
| both | Worldline / Cardlink Greece - Worldline Group sustainability (non-financial) reports | disclosures, annual reports, investor relations, ESG, sustainability,  | https://investors.worldline.com/en/home |
| both | Worldline / Cardlink Greece — careers portal + LinkedIn | hiring_signals, payments, vendor_management, IT_projects | https://careers.worldline.com/en/search-jobs/Greece/35538/2/390903/39/22/50/2 |
| both | Worldline / Cardlink — Careers | hiring_signals, job_postings, acquiring, pos, a2a_payments | https://jobs.worldline.com/ |
| both | Worldline Careers - Greece jobs | jobs, hiring, organization changes | https://careers.worldline.com/en/search-jobs/Greece |
| both | Worldline Global media relations press releases | press releases, acquiring, partnerships, disclosures | https://worldline.com/en/home/top-navigation/media-relations/press-release |
| both | Worldline Greece (Worldline Ελλάδα) — vendor pressroom / support | card processing vendor, Cardlink, acquiring, POS, DIAS CSM partner | https://worldline.com/el-gr/home |
| both | Worldline Greece - Compliancy & Terms (Acquiring) | regulation, compliance, terms_update, deadlines, supervision | https://worldline.com/el-gr/compliancy |
| both | Worldline Greece - IRIS acceptance / PSP integration (press & product) | instant payments, acceptance, vendor signals, connectivity | https://worldline.com/en-gr/home/main-navigation/solutions/merchants/value-added-services/iris |
| both | Worldline Greece - LinkedIn company page | hiring, leadership moves, organization changes | https://www.linkedin.com/company/worldlineglobal/ |
| both | Worldline Greece / Cardlink - Company & News (payment network operator) | leadership moves, organization changes | https://worldline.com/en-gr/home/top-navigation/about-worldline/who-we-are |
| both | Worldline Greece — LinkedIn company page | hiring, jobs, leadership moves, organization changes | https://gr.linkedin.com/company/worldline-greece |
| both | Worldline Greece — Media Relations / Newsroom (el-gr) | acquiring, merchant_services, payments_infrastructure, bank_partnershi | https://worldline.com/el-gr/home/top-navigation/media-relations |
| both | Worldline Greece — media relations / awards press releases (winner-side pointer) | awards, payments vendors, fintech, corroboration | https://worldline.com/en-gr/home/top-navigation/media-relations/press-release/pr-2025_03_19_01 |
| both | Worldline Group — Financial Press Releases (global, Greece deals) | public contracts, partnerships, award notices | https://worldline.com/en/home/top-navigation/media-relations/financial-press-releases |
| both | Worldline Investor Relations - financial press releases & reports | market statistics, payment statistics, card statistics, ATM POS data | https://investors.worldline.com/en/home/news-events/financial-press-releases.html |
| both | Worldline Investors — Financial Press Releases index | partnerships, vendors, competitors | https://investors.worldline.com/en/home/news-events/financial-press-releases |
| both | Worldline Media Relations / Press Releases | payments, merchant_acquiring, cards, M&A, wins | https://worldline.com/en/home/top-navigation/media-relations |
| both | Worldline Ελλάδα — Media Relations (Greek newsroom) | merchant acquiring, POS, partnership, procurement | https://worldline.com/el-gr/home/top-navigation/media-relations/press-release |
| both | Zepos & Yannopoulos - Insights / Newsletters | regulation, supervision, deadlines, banking, payments | https://www.zeya.com/newsroom |
| both | Ziraat Bank Ελλάδας — Announcements / support & documentation (Athens branch site) | internet banking, PSD2/API, Berlin Group, payments, digital services | https://ziraatbank.com.gr/el/announcements |
| both | bankingnews.gr | payment statistics, market statistics | https://bankingnews.gr/ |
| both | bankingnews.gr — Δελτία Τύπου (Greek relay of scheme releases) | payment statistics, card statistics, market statistics | https://www.bankingnews.gr/deltia-typou/ |
| both | capital.gr — Επιχειρήσεις / Τράπεζες (Greek financial media) | ATM, POS, merchant acquiring, contract, procurement | https://www.capital.gr/epixeiriseis |
| both | careerjet.gr — banking job aggregator (Greece) | jobs, hiring | https://www.careerjet.gr/%CE%B8%CE%B5%CF%83%CE%B5%CE%B9%CF%82-%CE%B5%CF%81%CE%B3%CE%B1%CF%83%CE%B9%CE%B1-banking.html |
| both | data.gov.gr - Greek Open Data Catalogue | market statistics, payment statistics, ATM POS data | https://data.gov.gr/ |
| both | dda.gr / dda.com.gr — DDA alert public-tender information service | tenders, procurement, public contracts, award notices | https://dda.gr/en |
| both | dealnews.gr — Greek banking/finance trade news (ATM vendor market coverage) | ATM market, maintenance contracts, vendor market share, tender economi | http://www.dealnews.gr/roi/item/129592 |
| both | diagonismoi-dimosiou.gr / promitheies.diagonismoi-dimosiou.gr — tender information service | tenders, procurement, public contracts, award notices | https://diagonismoi-dimosiou.gr/ |
| both | diagonismoi-dimosiou.gr / promitheies.gr — tender-notice aggregators | public-procurement, tenders, e-payments | https://promitheies.diagonismoi-dimosiou.gr/ |
| both | dimosioi-diagonismoi.gr - state-procurement tenders aggregator | market statistics, payment statistics, ATM POS data | https://dimosioi-diagonismoi.gr/diagonismoi |
| both | doValue Greece — Press Releases | servicing platform, payments (IRIS), digital transformation, vendor pa | https://dovaluegreece.gr/en/press-releases |
| both | e-forologia — Φορολογική/Λογιστική/Εργατική ενημέρωση | regulation, deadlines, pos_cash_register_interconnection, mydata, comm | https://www.e-forologia.gr/ |
| both | e-volution Awards (Boussias Events) — e-Commerce & e-Business | vendors, partnerships, case studies | https://e-volutionawards.boussiasevents.gr/ |
| both | e-volution awards (BOUSSIAS/Lighthouse) — Past Winners | e-banking, electronic payments, mobile business, digital transformatio | https://e-volutionawards.boussiasevents.gr/past-winners/ |
| both | e-ΕΦΚΑ — Ηλεκτρονικές Υπηρεσίες / Πληρωμές (social-security fund contribution collection) | contribution collection, bank payments, e-payment, payment channels | https://www.e-efka.gov.gr/el/ilektronikes-ypiresies-%CE%BF |
| both | eGov-KYC — List of banks & financial institutions connected to the service (GSIS) | KYC, onboarding, procurement, licensed entities, integrations | https://www.gsis.gr/en/polites-epiheiriseis/stoiheia-politon-kai-taytopoiitika-eggrafa/kyc/egov-kyc_BANKS |
| both | emea.gr - Epixeiriseis / Bank News | bank vendor deals, payments, acquiring, M&A | https://emea.gr/epicheiriseis/bank-news/ |
| both | enikonomia.gr - Economy (payment-stats reporting) | payment statistics, card statistics, ATM POS data | https://www.enikonomia.gr/economy/ |
| both | epay (Euronet Merchant Services Greece) newsroom | press releases, acquiring, partnerships, product launches | https://epayworldwide.gr/en/ |
| both | epay (Euronet) Greece — POS / softPOS terminal offerings (PAX, Sunmi, Verifone, Ingenico) | POS terminals, softPOS, vendor models, acquiring | https://epayworldwide.gr/en/in-store-pos/ |
| both | epay, a Euronet Worldwide Company — Careers (Workable ATS) | procurement, hiring signals, acquiring platform, cards, prepaid, imple | https://apply.workable.com/epay/?lng=en |
| both | ethosEVENTS - Digital Banking Forum & financial conference series | press releases, investor relations, earnings | https://ethosevents.eu/ |
| both | ethosEVENTS – Digital Banking Forum (event series) | digital banking, fintech, payments, vendor sponsorship, digital transf | https://ethosevents.eu/en/event/13th-digital-banking-forum-en/ |
| both | finloup - Greek BNPL / open-banking installment fintech | market statistics, payment statistics | https://finloup.com/en |
| both | jobfind.gr — Τραπεζικά / Banking category | jobs, hiring, organization changes | https://www.jobfind.gr/JobAds/Trapezika-Banking/all/GR/Theseis_Ergasias |
| both | jobseeker.gr — general job board | jobs, hiring | https://www.jobseeker.gr/job-listings/ |
| both | jooble Greece — banking jobs meta-aggregator | hiring_signals, banking, IT_projects | https://gr.jooble.org/%CE%B5%CF%81%CE%B3%CE%B1%CF%83%CE%AF%CE%B1-%CF%83%CE%B5-%CF%84%CF%81%CE%AC%CF%80%CE%B5%CE%B6%CE%B1 |
| both | kariera.gr — Greek job board (bank/fintech company pages) | hiring_signals, job_postings, banking, fintech | https://www.kariera.gr/en/jobs?title=%CF%84%CF%81%CE%AC%CF%80%CE%B5%CE%B6%CE%B1 |
| both | kariera.gr — job aggregator (staffing-agency & bank listings) | jobs, hiring | https://www.kariera.gr/en/jobs/call-center-or-customer-support-jobs-in-attiki |
| both | kariera.gr — job board (banking/IT postings + company pages) | vendors, competitors, partnerships | https://www.kariera.gr/en/jobs/it-jobs |
| both | kariera.gr — job search (keyword/company filters) | tenders, procurement, public contracts, hiring_signals, core banking,  | https://www.kariera.gr/en/jobs |
| both | kariera.gr — job search by title keyword | procurement, core banking, vendor selection, IT hiring, tech stack | https://www.kariera.gr/en/jobs?title=Temenos |
| both | metaforespress.gr / athenstransport.com — transport-sector press (AFC/POS weak-signal pointer) | procurement, tenders, public contracts | https://www.metaforespress.gr/ |
| both | mononews.gr / businessdaily.gr / imerisia.gr — bank-deal reporting | merchant acquiring, ATM, POS, procurement | https://www.mononews.gr/trapezes |
| both | moved.gr — 'Απλά Ψηφιακά' Greek fintech/BNPL commentary (EL) | BNPL, wallets, consumer payments | https://www.moved.gr/ |
| both | naftemporiki.gr — vendor/bank ATM & payments coverage | ATM, merchant acquiring, POS, procurement | https://www.naftemporiki.gr/ |
| both | newmoney.gr - Palmos Oikonomias (Business Stories / Trapezes) | tenders, procurement, public contracts, award notices, bank vendor dea | https://www.newmoney.gr/palmos-oikonomias/ |
| both | newmoney.gr — Banks (Παλμός Οικονομίας/Τράπεζες) | earnings, press_releases, disclosures | https://www.newmoney.gr/category/roh/palmos-oikonomias/trapezes/ |
| both | newmoney.gr — fintech / payments business coverage (EL) | fintech deals, BNPL, payments, bank-fintech | https://www.newmoney.gr/ |
| both | newmoney.gr — Παλμός Οικονομίας / Τράπεζες | POS, ATM, merchant acquiring, procurement | https://www.newmoney.gr/roh/palmos-oikonomias/trapezes/ |
| both | promitheies.gr - public-tenders aggregator (DIAVGEIA + Eprocurement) | market statistics, payment statistics, card statistics, ATM POS data | https://www.promitheies.gr/ |
| both | pwgopendata.eprocurement.gov.gr — public-works tenders open data / search | tenders, procurement, public contracts | https://pwgopendata.eprocurement.gov.gr/ |
| both | search.et.gr — Αναζήτηση Νομοθεσίας (Legislation search by law/PD number) | regulation, deadlines | https://search.et.gr/en/search-legislation/ |
| both | search.et.gr — Σύνθετη/Έξυπνη Αναζήτηση (Advanced / semantic free-text search) | regulation, supervision, consultations, deadlines | https://search.et.gr/en/advanced-search/ |
| both | symvasi.gr - KIMDIS contracts aggregator | market statistics, payment statistics, ATM POS data | https://symvasi.gr/khmdhs/ |
| both | symvasi.gr — public-contracts / CPV & ΚΗΜΔΗΣ aggregator | tenders, procurement, public contracts, banking services, POS, cards | https://symvasi.gr/cpv/ |
| both | taxheaven.gr — Greek tax/accounting news (tender coverage) | tenders, tax payments, card acceptance, e-paravolo, policy | https://www.taxheaven.gr/news |
| both | tbi bank Greece - news/newsroom | market statistics, payment statistics | https://tbibank.gr/news/ |
| both | tbi bank Greece — LinkedIn company page | hiring, jobs, organization changes, leadership moves | https://gr.linkedin.com/company/tbibank |
| both | techpress.gr — Greek payments/tech trade coverage | POS, terminals, deployment, public contracts | https://www.techpress.gr/ |
| both | thepaypers.com / Financial IT / Fintech Futures — Greek acquiring deal coverage | partnerships, public contracts, award notices | https://thepaypers.com/payments/news/finaro-partners-everypay-to-improve-in-store-payment-acceptance |
| both | viva.com Financial Statements & Reports | disclosures, annual reports, earnings | https://www.viva.com/en-eu/financial-statements |
| both | viva.com News & Announcements (Greek) | press releases, product launches, partnerships, corporate updates | https://www.viva.com/el-gr/news-announcements |
| both | xe.gr — εργασία (jobs classifieds section) | jobs, hiring | https://www.xe.gr/%CE%B5%CF%81%CE%B3%CE%B1%CF%83%CE%AF%CE%B1/%CE%B5%CF%8D%CF%81%CE%B5%CF%83%CE%B7-%CE%B5%CF%81%CE%B3%CE%B1%CF%83%CE%AF%CE%B1%CF%82 |
| both | ΑΑΔΕ (AADE) — Proclamations & Contests (Προκηρύξεις-Διαγωνισμοί) | public-procurement, tenders, POS, card-acceptance, e-payments | https://www.aade.gr/en/prokiryxeis-diagonismoi |
| both | ΑΑΔΕ (Independent Authority for Public Revenue) — payment/card-acceptance & banking-IT tenders | vendors, competitors, partnerships | https://www.aade.gr/ |
| both | ΑΑΔΕ — Account-to-account instant payment services (IRIS) interconnection page | regulation, deadlines, mandatory_payment_acceptance, iris_instant_paym | https://www.aade.gr/en/interface-pos-cash-systems/account-account-instant-payment-services |
| both | ΑΑΔΕ — Independent Authority for Public Revenue (POS / foreign-card acceptance tenders, incl. e-POS network) | POS, card acceptance, payments, tenders, procurement, public contracts | https://www.aade.gr/sites/default/files/2025-07/diak_xenes%20kartes.pdf |
| both | ΑΑΔΕ — POS / Cash-register interconnection hub (diasyndesipos) | POS, e-payments, regulation, card-acceptance | https://www.aade.gr/en/diasyndesipos |
| both | ΑΑΔΕ — Press Releases / Announcements | regulation, deadlines, announcements, supervision | https://www.aade.gr/en/press-releases-announcements |
| both | ΑΑΔΕ — myDATA Technical specifications & versions (REST API docs) | mydata, e_invoicing, technical_specifications, regulation | https://www.aade.gr/en/mydata/technical-specifications-versions-mydata |
| both | ΑΑΔΕ — Απόφαση Α.1155/2023 (ΦΗΜ–POS interconnection decision) canonical page | regulation, deadlines, pos_cash_register_interconnection | https://www.aade.gr/egkyklioi-kai-apofaseis/1155-09-10-2023 |
| both | ΑΑΔΕ — Εγκύκλιοι και Αποφάσεις (Circulars & Decisions register) | regulation, deadlines, supervision, decisions | https://www.aade.gr/egkyklioi-kai-apofaseis |
| both | ΑΑΔΕ — Μητρώο Μέσων Πληρωμών (EFT/POS) / POS Registry page | regulation, supervision, pos_registry, mandatory_payment_acceptance | https://www.aade.gr/en/dimioyrgia-mitrooy-meson-pliromon-pos-ton-epiheiriseon |
| both | ΑΑΔΕ — Πάροχοι υπηρεσιών ηλεκτρονικής τιμολόγησης (certified e-invoicing providers list) | mydata, e_invoicing, vendor_ecosystem, regulation | https://www.aade.gr/en/mydata/e-invoicing-service-providers |
| both | Απογραφή - Human Resources Registry of the Greek State / Annual Recruitment Planning | hiring, organization changes | https://hrms.gov.gr/portal/ |
| both | Βουλή των Ελλήνων — Συζητήσεις & Ψήφιση (Plenary Debates & Voting) | regulation, deadlines | https://www.hellenicparliament.gr/Nomothetiko-Ergo/Syzitiseis-kai-Psifisi |
| both | Βραβεία Ψηφιακής Διακυβέρνησης (Digital Governance Awards) — gov.gr | vendors, partnerships, case studies | https://digitalawards.gov.gr/winners |
| both | Γ.Ν. Παπαγεωργίου — Διαγωνισμοί / Οικονομική Διεύθυνση (hospital exemplar) | tenders, procurement, public contracts, POS, banking services, cash ma | https://www.papageorgiou-hospital.gr/diagonismoi/ |
| both | ΓΓΠΣΔΔ / gsis.gr — General Secretariat of Information Systems & Digital Governance (central e-POS / card-acceptance infrastructure) | payments, POS, card acceptance, public contracts, procurement | https://gsis.gr/ |
| both | ΓΓΠΣΨΔ / GSIS - Διαγωνισμοί Γενικής Γραμματείας Πληροφοριακών Συστημάτων & Ψηφιακής Διακυβέρνησης | regulation, deadlines | https://www.gsis.gr/dimosia-dioikisi |
| both | ΓΓΠΣΨΔ / GSIS — ΕΣΗΔΗΣ management directorate & e-invoice register (gsis.gr) | e_procurement, e_invoice, system_operator, register | https://www.gsis.gr/en/directorate-management-development-and-support-national-system-electronic-public-procurement-esidis |
| both | ΓΓΠΣΨΔ / GSIS — Κέντρο Διαλειτουργικότητας (ΚΕΔ) & ηλεκτρονικές πληρωμές δημοσίου | e-payment gateway, public payments infrastructure, interoperability, e | https://www.gsis.gr/kentro-dialeitoyrgikotitas-ked-ypoyrgeioy-oikonomikon |
| both | ΓΣΕΒΕΕ — Γενική Συνομοσπονδία Επαγγελματιών Βιοτεχνών Εμπόρων Ελλάδας (GSEVEE) & ΙΜΕ ΓΣΕΒΕΕ | POS, SME digitalization, payment costs, instant payments, positions | https://www.gsevee.gr/ |
| both | Γενική Γραμματεία Εμπορίου & Προστασίας Καταναλωτή — Διεύθυνση Προστασίας Καταναλωτή | consumer_protection, fee_transparency, payment_services, conduct_rules | https://gge.mindev.gov.gr/home/dieuthinsi-prostasias-katanaloti/ |
| both | Γενική Γραμματεία Εμπορίου — Τομέας Δημοσίων Συμβάσεων / ΕΚΑΑ (General Secretariat of Commerce — National Central Purchasing Authority) | framework agreements, central purchasing, procurement, public contract | https://gge.mindev.gov.gr/tomeas-dimosion-simvaseon/diadikasies-anathesis-ekaa/ |
| both | Γενική Γραμματεία Πληροφοριακών Συστημάτων & Ψηφιακής Διακυβέρνησης (ΓΓΠΣΨΔ/GSIS) — Διαγωνισμοί/Διαβουλεύσεις | tenders, procurement, public contracts, e-payments | https://www.gsis.gr/en/list-competitions |
| both | Γενική Γραμματεία Ψηφιακής Διακυβέρνησης & Απλούστευσης Διαδικασιών — project index (secdigital.gov.gr / digitalstrategy.gov.gr) | public contracts, e-payments, gov wallet | https://digitalstrategy.gov.gr/project/govgr |
| both | ΔΕΔΔΗΕ — Διακηρύξεις Διαγωνισμών (HEDNO electricity distribution operator tenders) | tenders, procurement, services, payment collection | https://www.deddie.gr/el/tender-notice-dmpt/ |
| both | ΔΕΗ e-Money Services (PPC e-Money Services) — utility-turned-payments-issuer signal | payment services, collection, e-money, acquiring, public contracts | https://www.dei.gr/en/home/contact-support/online-payment/ |
| both | ΔΕΗ Ανανεώσιμες (PPC Renewables) eProcurement — Tenders | tenders, procurement, public contracts | https://eprocurement.ppcr.gr/tenders |
| both | ΔΕΥΑ municipal water & sewage utilities — e-payment/POS & procurement | e-payment of fees, POS, banking services, procurement | https://www.deyah.gr/tropoi-pliromis/ |
| both | ΔΕΥΑ — Δημοτικές Επιχειρήσεις Ύδρευσης Αποχέτευσης (municipal water utilities, e.g. ΔΕΥΑΗ/ΔΕΥΑΠ/ΔΕΥΑΧ/ΔΕΥΑΞ) | tenders, procurement, public contracts | https://www.deyah.gr/online-eksoflisi-logariasmou/ |
| both | ΔΥΠΑ (DYPA) — Προμήθειες / Διαγωνισμοί + Prepaid page | tenders, procurement, public contracts, award notices, prepaid-card, b | https://www.dypa.gov.gr/promitheies-diaghonismi |
| both | ΔΥΠΑ - Προγράμματα Απασχόλησης / Active Employment Policies (subsidised hiring) | hiring, jobs | https://www.dypa.gov.gr/en/active-employment-policies |
| both | Δήμος Αθηναίων (City of Athens) — tenders/procurement & e-payments | tenders, procurement, public contracts, banking services, e-payment of | https://www.cityofathens.gr/ |
| both | Δήμος Θεσσαλονίκης (City of Thessaloniki) — diakiryxeis / KIMDIS PDFs | tenders, procurement, public contracts, banking services, POS | https://thessaloniki.gr/ |
| both | Δι@ύγεια (Diavgeia) — per-entity feeds for ΚτΠ / ΗΔΙΚΑ / ΟΠΕΚΑ / ΟΠΕΚΕΠΕ + advanced search | award notices, public contracts, procurement, tenders | https://diavgeia.gov.gr/search?advanced=true |
| both | Δι@ύγεια OpenData API (opendata.diavgeia.gov.gr/luminapi) | procurement, public contracts, award notices | https://opendata.diavgeia.gov.gr/luminapi/api/search/export |
| both | Διαύγεια (Diavgeia) — AEPP/EADISY transparency feed | tenders, procurement, pre-contractual appeals, procurement disputes | https://diavgeia.gov.gr/f/aepp |
| both | Διαύγεια (Diavgeia) — Transparency Programme public-acts register | public-procurement, awards, e-payments, disclosures | https://diavgeia.gov.gr/ |
| both | Διαύγεια (Diavgeia) — per-entity transparency feeds for utility/ΔΕΚΟ buyers | award notices, public contracts, procurement, payment services | https://diavgeia.gov.gr/f/eydap |
| both | Διαύγεια (Diavgeia) — public administration decisions transparency portal | procurement decisions, award decisions, commitment decisions, banking, | https://diavgeia.gov.gr/search |
| both | Διαύγεια OpenData API — search-export endpoint (luminapi) | procurement, direct awards, expenditure commitments, payment services, | https://diavgeia.gov.gr/luminapi/api/search/export?q=organizationUid:%2250280%22&sort=recent&wt=json |
| both | Δικτυακός Τόπος Διαβουλεύσεων ΥΠΕΘΟ (OpenGov consultations sub-portal of the Ministry) | consultations, regulation, deadlines | https://www.opengov.gr/minfin/ |
| both | Ε.Α.Π. — Ελληνικό Ανοικτό Πανεπιστήμιο payments portal & ΕΛΚΕ (university buyer example) | tenders, procurement, public contracts | https://payments.eap.gr/ |
| both | Ε.Κ.ΠΟΙ.ΖΩ. — Ένωση Καταναλωτών «Η Ποιότητα της Ζωής» | consumer_protection, fee_transparency, payment_services, dispute_resol | https://www.ekpizo.gr/ |
| both | ΕΕΤ — Δελτία Τύπου / Γραφείο Τύπου (Press Releases) | press_releases, sector_positions, announcements, digital_banking | https://www.hba.gr/Media/List?type=PressReleases |
| both | ΕΕΤ — Εκδηλώσεις - Ομιλίες (Events & Speeches, incl. events under HBA auspices) | events, conferences, digital_banking, payments, speakers | https://www.hba.gr/Events/List |
| both | ΕΕΤΑΑ — Hellenic Agency for Local Development & Local Government | procurement, public contracts, tenders | https://eetaa.gr/ |
| both | ΕΚΑΠΥ — Εθνική Κεντρική Αρχή Προμηθειών Υγείας (procurement app + tenders) | tenders, procurement, public contracts, award notices, banking service | https://apps.ekapy.gov.gr/procurementsEkapy/overview |
| both | ΕΛΤΑ / Hellenic Post — Διακηρύξεις (Declarations / Tenders) | tenders, procurement, public contracts, payment services, collection | https://www.elta.gr/declarations/promitheia-ylikon |
| both | ΕΝΠΕ — Union of Regions of Greece: 'Προκηρύξεις Περιφερειών' (regional tenders index) | tenders, procurement, public contracts, award notices | https://enpe.gr/prokiryxeis-perifereion/ |
| both | ΕΟΠΥΥ — official site (Διαγωνισμοί / Προκηρύξεις) | tenders, procurement, public contracts, award notices, banking service | https://www.eopyy.gov.gr/ |
| both | ΕΣΕΕ — Ελληνική Συνομοσπονδία Εμπορίου & Επιχειρηματικότητας (Hellenic Confederation of Commerce & Entrepreneurship) | POS, merchant acquiring, interchange, bank commissions, instant paymen | https://www.esee.gr/ |
| both | ΕΣΗΔΗΣ / ΚΗΜΔΗΣ — Promitheus National e-Procurement System (eprocurement.gov.gr) | public-procurement, tenders, e-payments, POS, disclosures | https://www.eprocurement.gov.gr/ |
| both | ΕΣΗΔΗΣ / ΚΗΜΔΗΣ — Εθνικό Σύστημα Ηλεκτρονικών Δημοσίων Συμβάσεων (promitheus.gov.gr) | tenders, procurement, IT contracts, payment systems | https://www.promitheus.gov.gr/ |
| both | ΕΣΗΔΗΣ — CPV lookup tool (Κοινό Λεξιλόγιο Δημοσίων Συμβάσεων) | procurement, public contracts | https://cerpp.eprocurement.gov.gr/cpv/main/ |
| both | ΕΣΗΔΗΣ — Προκαταρκτικές Διαβουλεύσεις (eproc-deliberation searchDeliberations) | tenders, procurement, public contracts | https://cerpp.eprocurement.gov.gr/deliberation/ |
| both | ΕΥΔΑΠ — Προκηρύξεις Προμηθειών / Έργων (Athens Water Supply & Sewerage tenders) | tenders, procurement, bill collection, payment acceptance, banking ser | https://www.eydap.gr/TheCompany/Contests/ProcurementNotices/ |
| both | ΕΥΔΕ-ΤΠΕ / digitalplan.gov.gr — Digital Transformation calls & enrolled projects | tenders, procurement, public contracts, calls, OTA/municipalities, dig | https://www.digitalplan.gov.gr/ |
| both | ΕΥΔΕ-ΤΠΕ — digitalplan.gov.gr (Special Managing Authority for ICT projects, ΕΣΠΑ/RRF calls) | procurement, tenders, beneficiaries, rrf, digital payments | https://www.digitaltransform.gr/proskliseis-entaxeis/ |
| both | Εθνική Τράπεζα — Ενημέρωση Επενδυτών (Greek IR portal) | market statistics, card statistics, payment statistics | https://www.nbg.gr/el/omilos/enimerwsi-ependutwn |
| both | Εθνικό Τυπογραφείο — National Printing House (main site) | tenders, procurement, public contracts, award notices, payment institu | https://www.et.gr/ |
| both | Εθνικό Τυπογραφείο — ΦΕΚ / Government Gazette search (search.et.gr) | regulation, deadlines, supervision | https://search.et.gr/en/ |
| both | Εθνικό Τυπογραφείο — ΦΕΚ Search Portal (National Printing House Official Gazette search) | tenders, procurement, licensing, concessions, PPP, statutory_acts, pay | https://search.et.gr/ |
| both | Εθνικό Τυπογραφείο — ΦΕΚ Απλή / Έξυπνη Αναζήτηση (Gazette simple & semantic search) | licensing, corporate events, public contracts, award notices | https://search.et.gr/en/simple-search/ |
| both | Ελλάδα 2.0 (Greece 2.0) — National Recovery & Resilience Plan portal (RRF projects & calls) | RRF, EU-funded projects, digital payments, grants/calls, beneficiaries | https://greece20.gov.gr/ |
| both | Ελλάδα 2.0 / Greece 2.0 (greece20.gov.gr) — RRF project index | public contracts, e-payments, gov wallet, procurement | https://greece20.gov.gr/en/?projects=eniaia-psifiaki-pyli-pliromon |
| both | Ελληνική Ένωση Acquirers / Ελληνική Ένωση Ιδρυμάτων Αποδοχής Πράξεων Πληρωμών (Hellenic Association of Acquirers, HAACQ) | merchant acquiring, POS, instant payments, interchange, payment standa | https://www.haacq.gr/ |
| both | Ελληνική Ένωση Τραπεζών (HBA) — Financial Law index (national legislation) | procurement law, ministerial decisions, payment institution licences,  | https://www.hba.gr/FinancialLaw/List?type=NationalOnlineBanking |
| both | Ελληνική Ένωση Τραπεζών (ΕΕΤ) — Τακτικά Μέλη / HBA Regular Members directory | members, banks, actor_map, tenders, procurement | https://www.hba.gr/Association/Members?type=RegularMembers |
| both | Ελληνικός Χρηματοοικονομικός Μεσολαβητής (Hellenic Financial Ombudsman / HOBIS) | dispute_resolution, payment_services, consumer_protection, conduct_rul | https://hobis.gr/ |
| both | Ελληνικός Χρηματοοικονομικός Μεσολαβητής (Hellenic Financial Ombudsman, HOBIS) — Annual Reports | payment statistics, card statistics, market statistics, payment disput | https://hobis.gr/en/category/news/publications/annual-reports/ |
| both | Επιμελητήρια (Chambers of Commerce) — member circulars on POS/myDATA obligations | regulation, deadlines, mandatory_payment_acceptance, commentary | https://acci.gr/ |
| both | Ευρωπαϊκό Κέντρο Καταναλωτή Ελλάδας (European Consumer Centre Greece, ECC-Net) | payment disputes, card statistics | https://www.eccgreece.gr/ |
| both | ΙΝ.ΕΜ.Υ – ΕΣΕΕ (INEMY, Institute of Commerce and Services – research arm of ESEE) | electronic payments, card usage, cash usage, consumer payment behavior | https://inemy.gr/ |
| both | ΚΕ.Π.ΚΑ. — Κέντρο Προστασίας Καταναλωτών | consumer_protection, fee_transparency, payment_services | https://www.kepka.org/ |
| both | ΚΕΔΕ — Central Union of Municipalities of Greece (news & policy portal) | procurement, public contracts, tenders | https://kede.gr/ |
| both | ΚΗΜΔΗΣ - Contracts search | market statistics, payment statistics, card statistics, ATM POS data | https://cerpp.eprocurement.gov.gr/kimds2/unprotected/searchContracts.htm |
| both | ΚΗΜΔΗΣ - Notices/Proclamations search (Central Electronic Registry of Public Contracts) | market statistics, payment statistics, card statistics, ATM POS data | https://cerpp.eprocurement.gov.gr/kimds2/unprotected/searchNotice.htm |
| both | ΚΗΜΔΗΣ OpenData REST API (KIMDIS Open Data) | procurement, tenders, awards, contracts, IT services, payments infrast | https://cerpp.eprocurement.gov.gr/khmdhs-opendata/help |
| both | ΚΗΜΔΗΣ public search UI — current portal (upgkimdis/unprotected) | tenders, procurement, contract_awards, vendors | https://cerpp.eprocurement.gov.gr/upgkimdis/unprotected/home.xhtml |
| both | ΚΗΜΔΗΣ — Central Electronic Registry of Public Contracts | tenders, procurement, public contracts, award notices | https://cerpp.eprocurement.gov.gr/kimds2/protectedSearch.htm |
| both | ΚΗΜΔΗΣ — Central Electronic Registry of Public Contracts (via Promitheus) | procurement, public contracts, award notices, direct awards, banking s | https://promitheus.gov.gr/ |
| both | ΚΗΜΔΗΣ — Central Electronic Registry of Public Contracts (via gov.gr) | tenders, procurement, public contracts, award notices | https://www.gov.gr/ipiresies/epikheirematike-drasterioteta/elektronikos-phakelos-epikheireses/demosioteta-demosion-sumbaseon-kemdes |
| both | Κοινωνία της Πληροφορίας Μ.Α.Ε. (KtP AE) — Tenders (Διαγωνισμοί) | public-procurement, tenders, e-payments, digital-transformation | https://www.ktpae.gr/diagwnismoi/ |
| both | ΚτΠ Μ.Α.Ε. — Έργα (projects) index, incl. Ενιαία Ψηφιακή Πύλη Πληρωμών & gov.gr Wallet | public contracts, e-payments, gov wallet, procurement, tenders | https://www.ktpae.gr/erga/ |
| both | ΚτΠ Μ.Α.Ε. — Ανακοινώσεις (announcements) | tenders, procurement, public contracts, award notices | https://www.ktpae.gr/%CE%BD%CE%AD%CE%B1/%CE%B1%CE%BD%CE%B1%CE%BA%CE%BF%CE%B9%CE%BD%CF%8E%CF%83%CE%B5%CE%B9%CF%82/ |
| both | Ο.ΣΥ. ΜΟΝ. Α.Ε. — Διακηρύξεις Διαγωνισμών (Athens road transport operator tenders) | tenders, procurement, fare collection, contactless payment, ticketing | https://www.osy.gr/%CE%B4%CE%B9%CE%B1%CE%BA%CE%B7%CF%81%CF%8D%CE%BE%CE%B5%CE%B9%CF%82-%CE%B4%CE%B9%CE%B1%CE%B3%CF%89%CE%BD%CE%B9%CF%83%CE%BC%CF%8E%CE%BD/ |
| both | ΟΑΣΑ — Προκηρύξεις / Διακηρύξεις Διαγωνισμών (Athens Urban Transport Organisation tenders, incl. ΑΣΣΚ fare-collection) | tenders, procurement, fare collection, contactless payment, AFCS, tick | https://www.oasa.gr/%CF%80%CF%81%CE%BF%CE%BA%CE%B7%CF%81%CF%8D%CE%BE%CE%B5%CE%B9%CF%82/ |
| both | ΟΛΠ / Piraeus Port Authority (PPA) — Διαγωνισμοί σε εξέλιξη (Active Tenders) | tenders, procurement, public contracts, payment services | https://www.olp.gr/el/diagonismoi-se-ekseliksi |
| both | ΟΠΕΚΑ — Οργανισμός Προνοιακών Επιδομάτων & Κοινωνικής Αλληλεγγύης (opeka.gov.gr) | tenders, procurement, public contracts, benefits disbursement, e-payme | https://opeka.gov.gr/ |
| both | ΟΠΕΚΕΠΕ — Οργανισμός Πληρωμών & Ελέγχου Κοινοτικών Ενισχύσεων (opekepe.gr) | tenders, procurement, public contracts, benefits disbursement, e-payme | https://www.aade.gr/aade/anthropino-dynamiko/diaheirisi-anthropinoy-dynamikoy/ypiresies-tis-aade/genikes-dieythynseis/geniki-dieythynsi-eleghon |
| both | ΟΣΕΘ / ΟΑΣΘ — Thessaloniki public transport authority & operator (AFC / smart-card & POS tenders) | tenders, procurement, public contracts | https://www.oasth.gr/eisitiria/komistra/ |
| both | Οδηγός του Πολίτη - ΑΣΕΠ tag | jobs, hiring | https://www.odigostoupoliti.eu/tag/asep/ |
| both | Περιφέρεια Αττικής — Attica Region official tenders/procurement | tenders, procurement, public contracts, banking services, e-payment of | https://www.patt.gov.gr/ |
| both | Περιφέρεια Κεντρικής Μακεδονίας — Central Macedonia Region: Προκηρύξεις | tenders, procurement, public contracts, banking services, POS | https://www.pkm.gov.gr/category/proclamations/ |
| both | Περιφέρεια Στερεάς Ελλάδας — regional authority procurement (syzefxis tenders portal) [representative of 13 regions] | tenders, procurement, public contracts | http://www.2522.syzefxis.gov.gr/ |
| both | ΣΕΒ - Σύνδεσμος Επιχειρήσεων και Βιομηχανιών (SEV / Hellenic Federation of Enterprises) | regulation, consultations, deadlines, payments | https://www.sev.org.gr/ |
| both | ΣΥΕΤΕ - Σύλλογος Υπαλλήλων Εθνικής Τράπεζας Ελλάδος | voluntary_exit_scheme, restructuring, organization_changes, branch_clo | https://www.syete.gr/ |
| both | Συνήγορος του Καταναλωτή - Financial Services (Greek Consumer Ombudsman) | competitors, vendors, case studies, partnerships | https://www.synigoroskatanaloti.gr/en/financial-services |
| both | Συνήγορος του Καταναλωτή — Annual Reports (Ετήσιες Εκθέσεις) PDF archive | consumer_protection, complaint_statistics, payment_services, fee_trans | https://www.synigoroskatanaloti.gr/el/etisies-ektheseis |
| both | Ταμείο Παρακαταθηκών & Δανείων (Consignment Deposits & Loans Fund) — Procurement notices | vendors, competitors, case studies, partnerships | https://www.tpd.gr/prokirykseis-promitheion/ |
| both | Ταμείο Παρακαταθηκών & Δανείων (Deposits & Loans Fund) — treasury/payments-receipts for OTAs | banking services, cash management, municipal collections, treasury | https://www.tpd.gr/ |
| both | Τράπεζα της Ελλάδος — Κίνηση και απάτη των συναλλαγών με κάρτες πληρωμών (card transaction & fraud statistics) | card transactions, card fraud, POS, payment statistics, reporting temp | https://www.bankofgreece.gr/statistika/kinhsh-kai-apath-twn-synallagwn-me-kartes-plhrwmwn |
| both | Τράπεζα της Ελλάδος — Καινοτομία στις πληρωμές (Innovation in payments) | regulation, supervision | https://www.bankofgreece.gr/en/main-tasks/payment-systems-and-settlements/retail-payment-strategy/payment-innovation |
| both | Τράπεζα της Ελλάδος — Στατιστικές πληρωμών (EL) | στατιστικές πληρωμών, κάρτες, POS, όγκος συναλλαγών, απάτη | https://www.bankofgreece.gr/statistika/statistikes-plhrwmwn |
| both | Υπουργείο Εθνικής Οικονομίας & Οικονομικών (minfin.gov.gr) — press & procurement | e-payments, POS, regulation, public-procurement, press-releases | https://minfin.gov.gr/ |
| both | Υπουργείο Κοινωνικής Συνοχής & Οικογένειας — Προσκλήσεις/Προκηρύξεις (minscfa) | tenders, procurement, public contracts, prepaid card, disbursement, PS | https://minscfa.gov.gr/proskliseis-prokiryxeis/ |
| both | ΦΟΔΣΑ regional solid-waste bodies — procurement/tenders sections | tenders, procurement, public contracts, e-payment of fees, POS | https://fodsapel.gr/category/prokiryxeis-diagonismoi/ |
| unclassified | AADE — Average Annual Turnover per Activity Code (μέσος ετήσιος τζίρος ανά ΚΑΔ) | market statistics, payment statistics | https://www.aade.gr/en/perfomance-reports-accountability/statistics/average-annual-turnover-activity-code-kad |
| unclassified | AADE — KPIs / Open Data: monthly Tax & Customs Administration Monitoring reports | market statistics, payment statistics, cash usage | https://www.aade.gr/en/open-data/KPIs |
| unclassified | AADE — myDATA REST API technical documentation & developer portal | payment statistics, market statistics | https://www.aade.gr/en/mydata-operational-specifications |
| unclassified | AADE — myDATA statistics sub-page (under Statistics) | payment statistics, market statistics | https://www.aade.gr/en/mydata-0 |
| unclassified | Alpha Bank — press room / awards announcements | awards, recognitions, SME, press releases | https://www.alpha.gr/en |
| unclassified | Anaptyxi.gov.gr 2027 — ESPA 2021-2027 project & beneficiary database | EU funding, ESPA 2021-2027, projects, beneficiaries, open data, digita | https://2027.anaptyxi.gov.gr/ |
| unclassified | Annual National Accounts - Final Consumption (Εθνικοί Λογαριασμοί - Τελική Κατανάλωση, SEL39) | market statistics, cash usage | https://www.statistics.gr/en/statistics/-/publication/SEL39/- |
| unclassified | Athens Times - Markets (English) | ratings, target_price, sell_side_research | https://athens-times.com/ |
| unclassified | Banco de España / ECB — List of payment-statistics-relevant institutions (PSRI) for Greece | authorised_institution_lists, payment_institutions, LEI, payment_stati | https://www.bde.es/webbe/en/estadisticas/otras-clasificaciones/clasificacion-entidades/listas-instituciones-financieras/listas-instituciones-relevantes-estadisticas-pago-pais/lista-psri-gr.html |
| unclassified | Bank of Greece - Economic Bulletin | market statistics | https://www.bankofgreece.gr/en/publications-and-research/research/economic-bulletin |
| unclassified | Business Daily — banks/technology fintech coverage | banks, fintech, accelerator, neobank, payments, finalists | https://www.businessdaily.gr/ |
| unclassified | Consumer Price Index (Δείκτης Τιμών Καταναλωτή, DKT87) | market statistics | https://www.statistics.gr/en/statistics/-/publication/DKT87/- |
| unclassified | Crowdpolicy - fintech/govtech & crowdfunding | press releases | https://crowdpolicy.com/ |
| unclassified | Crunchbase / Tracxn — Greek fintech company & funding databases | actor enumeration, funding, investors, fintech | https://tracxn.com/d/explore/fintech-startups-in-greece/__qo4iDQXalIFuCA3IWeUyRD8ZX1oYvVHBI2oT-x1mxMw/companies |
| unclassified | ECB Data Portal — Payments transactions key indicators (PAY dataset) | market statistics, payment statistics | https://data.ecb.europa.eu/data/datasets/PAY |
| unclassified | ECB — List of T2 (TARGET Services) participants | payment infrastructure, participants, RTGS, TARGET/T2 | https://www.ecb.europa.eu/paym/target/t2/facts/shared/pdf/list-of-participants.en.xlsx |
| unclassified | ECB — Study on Payment Attitudes of Consumers in the Euro Area (SPACE) | cash usage, market statistics, payment statistics | https://www.ecb.europa.eu/stats/ecb_surveys/space/html/index.en.html |
| unclassified | ELSTAT Release Calendar & Press Releases (Ημερολόγιο Ανακοινώσεων / Δελτία Τύπου) | market statistics, payment statistics | https://www.statistics.gr/en/calendar |
| unclassified | EU-Startups — Greek startup/fintech coverage & lists | funding, actor enumeration, fintech, payments | https://www.eu-startups.com/2026/02/from-athens-to-thessaloniki-10-of-the-most-promising-greek-startups-to-keep-an-eye-on-in-2026/ |
| unclassified | EU-Startups — Greek startups & directory listings | directory, fintech_startups, funding_rounds, ecosystem | https://www.eu-startups.com/directory/greek-fintech-cluster/ |
| unclassified | Elevate Greece - National Startup Registry | member_directory, market_commentary | https://elevategreece.gov.gr/ |
| unclassified | Elevate Greece — Startup Database Dashboard / Analytics | organization changes | https://elevategreece.gov.gr/the-startup-database/ |
| unclassified | Elorus - fintech SaaS (invoicing/cashflow) | press releases | https://www.elorus.com/ |
| unclassified | Eurostat SDMX Dissemination API (getting started + Swagger) | market statistics, data access, programmatic collection | https://ec.europa.eu/eurostat/web/user-guides/data-browser/api-data-access/api-getting-started |
| unclassified | Evolution of Turnover of Enterprises (Εξέλιξη Κύκλου Εργασιών των Επιχειρήσεων) - quarterly value data | market statistics, payment statistics | https://www.statistics.gr/en/statistics/ind |
| unclassified | Found.ation — 'Startups in Greece' Venture Financing Report (annual) | funding rounds, investors, fintech deals, ecosystem mapping | https://thefoundation.gr/innovation-platform/our-publications/startups-in-greece/ |
| unclassified | Found.ation — Startups in Greece: Venture Financing Report (annual) | funding_rounds, fintech_startups, venture_capital, deals, ecosystem_st | https://thefoundation.gr/2024/12/12/startups-in-greece-venture-financing-report-2024-2025/ |
| unclassified | Greek Fintech Hub (Endeavor Greece + National Bank of Greece) | member_directory, events, press_releases, market_commentary | https://www.fintechhub.gr/ |
| unclassified | Group Center Hellas Security (GCHS) — regional CIT firm & exclusive G4S representative (Central Greece) | cash_in_transit, cash_management, guarding_services, regional_operator | https://www.groupcenterhellas.com/ypiresies/xrimatapostoles |
| unclassified | Hellenic Parliament — legislative work / bills on HFSF & state holdings | legislation, state holding, privatisation | https://www.hellenicparliament.gr/Nomothetiko-Ergo/Anazitisi-Nomothetikou-Ergou |
| unclassified | Household Budget Survey (Έρευνα Οικογενειακών Προϋπολογισμών, ΕΟΠ) | cash usage, market statistics, payment statistics | https://www.statistics.gr/en/statistics/pop |
| unclassified | Intrum Group — Press releases (Greece coverage) | Greece transactions, Piraeus platform, securitizations | https://www.intrum.com/press/press-releases/ |
| unclassified | KPMG Greece — Compensation & Benefits Surveys (People Services) | organization changes | https://kpmg.com/gr/en/home/services/advisory/management-consulting/people-services/compensation-benefits-surveys.html |
| unclassified | Kohesio — EU cohesion-policy projects database (beneficiaries by country) | cohesion policy, EU-funded projects, beneficiaries, digital, payments | https://kohesio.ec.europa.eu/en/ |
| unclassified | MPS Security / GIS Security — CIT (χρηματαποστολές) service provider | cash_in_transit, guarding_services, regional_operators | https://www.gis-security.gr/ |
| unclassified | NBG Business Seeds (National Bank of Greece) | market statistics, payment statistics | https://www.nbg.gr/el/epaggelmaties/nbg-business-seeds |
| unclassified | Official Diavgeia OpenData client samples (GitHub org: diavgeia) | API access, collection tooling, documentation | https://github.com/diavgeia/opendata-client-samples-python |
| unclassified | Plum — smart money app (Eurobank strategic partner) | funding, bank partnership, market expansion, consumer fintech | https://withplum.com/press/ |
| unclassified | PowerGame.gr | ICT market size, SEPE reporting, tech sector, banks | https://www.powergame.gr/ |
| unclassified | Protect Cash Solutions S.A. — Greek cash-management / CIT operator | cash_management, cash_in_transit, regional_operators | https://www.protectsolutions.gr/en |
| unclassified | Simply Wall St - Greek bank analyst forecasts | target_price, consensus, valuation | https://simplywall.st/stocks/gr/banks/ath-eurob/eurobank-shares |
| unclassified | The Banker (Financial Times Group) — Bank of the Year Awards | awards, rankings, recognitions | https://www.thebanker.com/Awards |
| unclassified | TheRecursive — SEE/Greek startup funding coverage | funding rounds, startup deals, fintech | https://therecursive.com/ |
| unclassified | Turnover Index in Wholesale Trade (Δείκτης Κύκλου Εργασιών στο Χονδρικό Εμπόριο) | market statistics | https://www.statistics.gr/en/statistics/-/publication/DKT42/- |
| unclassified | data.gov.gr - Bank of Greece organisation datasets | payment statistics, market statistics | https://data.gov.gr/organization/trapeza-tis-ellados |
| unclassified | data.gov.gr — 'gov-et-laws' dataset (Δημοσιευμένοι νόμοι από το Εθνικό Τυπογραφείο) | statutory_acts, licensing, legislation_metadata | https://data.gov.gr/dataset/dimosieymenoi-nomoi-apo-to-ethniko-typografeio-2000-2026 |
| unclassified | data.gov.gr — AADE organization page (Ανεξάρτητη Αρχή Δημοσίων Εσόδων) | market statistics, payment statistics | https://data.gov.gr/organization/aade-2026 |
| unclassified | data.gov.gr — National Open Data Portal, 'Companies & company ownership' HVD category | company register, beneficial ownership, incorporations, corporate fili | https://data.gov.gr/en/pages/hvd |
| unclassified | diaNEOsis — Research & Policy Institute (διαΝΕΟσις) | shadow economy, tax evasion, cash usage, digital transactions | https://www.dianeosis.org/research/ |
| unclassified | dikaio.ai — ΦΕΚ PDF mirror / AI legal index | statutory_acts, licensing, legislation | https://www.dikaio.ai/ |
| unclassified | e-nomothesia.gr — Τράπεζα Πληροφοριών Νομοθεσίας (legislation database mirroring ΦΕΚ) | statutory_acts, licensing, legislation | https://www.e-nomothesia.gr/ |
| unclassified | ethosEVENTS — awards & conferences portal | awards, finance, recognitions, pointer | https://ethosevents.eu/en/home/ |
| unclassified | kodiko.gr — Greek legislation search engine (ΦΕΚ-linked) | statutory_acts, legislation, circulars | https://www.kodiko.gr/ |
| unclassified | openarchives.gr — National aggregator of Greek scholarly content (EKT) | digital transactions, cash usage, shadow economy, payment statistics | https://www.openarchives.gr/ |
| unclassified | ΓΕΜΗ / Γενικό Εμπορικό Μητρώο (General Commercial Registry) — HBA statutory filings | organization changes, governance | https://www.businessportal.gr/ |
| unclassified | ΔΑΚΕ - Συνεργασία (bank-union faction) | collective_dismissals, restructuring, organization_changes | https://www.dake-synergasia.gr/ |
| unclassified | ΕΣΠΑ 2021-2027 — espa.gr (main NSRF portal) | espa, programmes, funding_calls, digital_transformation, pointer | https://www.espa.gr/ |
| unclassified | Ελλάδα 2.0 — Λίστα Ενταγμένων Έργων / Αποφάσεις ένταξης (Inclusion Decisions) | beneficiaries, award notices, public contracts, rrf | https://greece20.gov.gr/lista-entagmenwn-ergwn/ |
| unclassified | Ενωτικός Σύλλογος Εργαζομένων Τράπεζας EFG Eurobank Ergasias (ΣΕΤΕΕ) | voluntary_exit_scheme, restructuring, organization_changes | http://www.setee.gr/ |
| unclassified | Μητρώο Επιχορηγούμενων Φορέων (mef.diavgeia.gov.gr) — Open Data API | expenditure commitments, public contracts | https://mef.diavgeia.gov.gr/pages/API |
| unclassified | ΠΑΜΕ / Αγωνιστικό Μέτωπο τραπεζοϋπαλλήλων (class-oriented union front) | collective_dismissals, voluntary_exit_scheme, restructuring, organizat | https://pamehellas.gr/ |
| unclassified | Πρόγραμμα «Ψηφιακός Μετασχηματισμός» 2021-2027 (Digital Transformation Programme) — calls & awards portal | EU funding, ESPA 2021-2027, digital transformation, calls, awards, ICT | https://www.digitaltransform.gr/en/archiki-english/ |
| unclassified | Πρόταση Προοπτικής (bank-union faction blog) | collective_dismissals, restructuring, organization_changes | https://protasiprooptikis.blogspot.com/ |
| unclassified | Συσπείρωση (agonistic faction in OTOE) | collective_dismissals, restructuring, organization_changes | https://sysp.gr/ |
| unclassified | Σωματείο Εργαζομένων Union Eurobank | voluntary_exit_scheme, restructuring, organization_changes | https://unioneurobank.gr/ |

## Payments-focused — 137 sources EXCLUDED

| Source | Topics | URL |
|---|---|---|
| AADE — Annual Statistical Bulletins for Natural Persons (Ετήσια στατιστικά δελτία Φυσικών Προσώπων) | market statistics, payment statistics, cash usage | https://www.aade.gr/en/perfomance-reports-accountability/statistics/annual-statistical-reports-natural-persons |
| AADE — Report on the evolution & fluctuation of tax revenue (Έκθεση εσόδων / Revenue) | market statistics, payment statistics | https://www.aade.gr/en/perfomance-reports-accountability/statistics/reports-evolution-and-fluctuation-tax-revenue |
| AADE — Statistics hub (Στατιστικά / Σχεδιασμός–Απολογισμός) | market statistics, payment statistics, card statistics, cash usage | https://www.aade.gr/en/perfomance-reports-accountability/statistics |
| AADE — myDATA (Ηλεκτρονικά Βιβλία) live dashboard / statistics | payment statistics, market statistics, card statistics | https://www.aade.gr/en/mydata |
| AADE — Πάροχοι που έχουν υποβάλει δήλωση συμμόρφωσης (Greek-language authoritative list) | payments_companies, acquirers, nsp, pos, entity_enumeration, complianc | https://www.aade.gr/epiheiriseis/diasyndesi-pos-tameiakon-systimaton/poies-einai-oi-epiloges-moy/pos/parohoi-poy-ehoyn-ypobalei-dilosi-symmorfosis |
| Alpha Bank - Instant Transfers (SCT Inst) page | SEPA instant credit transfer, instant transfers, bank implementation | https://www.alpha.gr/en/retail/myalpha/online-transactions-and-digital-wallets/money-transfers/instant-transfers |
| Alpha Bank — Mastercard→Visa card replacement / scheme pages | issuer, scheme migration, partner selection, agentic commerce | https://www.alpha.gr/el/idiotes/kartes/xreostikes-kartes/antikathistoume-tin-alpha-bank-enter-mastercard |
| Alpha Bank — Nexi partnership / merchant POS pages (bank side of the JV) | acquiring, POS, bank_JV, merchant_services, partnership | https://www.alpha.gr/en/Business/Professionals-and-Businesses/nexi-pos-termatika-apodoxis-pliromon-me-kartes-sunergasia |
| Athens University of Economics and Business (AUEB / Οικονομικό Πανεπιστήμιο Αθηνών, ΟΠΑ) | payment statistics, card statistics, fintech, digital transactions | https://www.aueb.gr/ |
| Bank of Greece - TARGET Instant Payment Settlement (TIPS) page | TIPS, SCT Inst, settlement infrastructure | https://www.bankofgreece.gr/kiries-leitourgies/systhmata-plhrwmwn-diakanonismou/yphresies-target/tips |
| Bank of Greece Open Data Portal — home / catalog root | open data, catalog, API, payments statistics | https://opendata.bankofgreece.gr/ |
| Bank of Greece — Cross-border EEA E-Money Institutions notifying into Greece | authorised_institution_lists, emoney_institutions, passporting, cross_ | https://www.bankofgreece.gr/RelatedDocuments/13_LIST_OF_EEA__E-MONEY_INSTITUTIONS.xls |
| Bank of Greece — Cross-border Payment Institutions by home country (passporting into Greece) | authorised_institution_lists, payment_institutions, passporting, cross | https://www.bankofgreece.gr/RelatedDocuments/12_List_of_Payment_Institutions_by_country_of_origin.xls |
| Bank of Greece — Euro banknotes & coins / Cash services (Ταμειακές Υπηρεσίες) | cash usage, market statistics | https://www.bankofgreece.gr/euro/trapezogrammatia-kai-kermata-eyrw |
| Bank of Greece — Press releases / supervisory decisions (licence grants, withdrawals, special liquidation) | licence_withdrawal, special_liquidation, supervisory_decisions, paymen | https://www.bankofgreece.gr/en/news-and-media/press-office/news-list |
| Bank of Greece — Αδειοδότηση (Authorisation) page, incl. ΦΕΚ-cited Executive Committee Acts | payment institution licences, e-money authorisation, bank charters, cr | https://www.bankofgreece.gr/kiries-leitourgies/epopteia/xrhmatodotika-idrymata/adeiodothsh |
| Bank of Greece — Υπηρεσία TIPS (TARGET TIPS service) page | payment statistics, instant payments adoption | https://www.bankofgreece.gr/en/main-tasks/payment-systems-and-settlements/target-services/tips |
| Bank of Greece — Υπηρεσίες TARGET (TARGET services, national gateway page) | payments infrastructure, settlement, participant register, instant pay | https://www.bankofgreece.gr/kiries-leitourgies/systhmata-plhrwmwn-diakanonismou/yphresies-target |
| COSMOTE Payments (OTE Group EMI) corporate site | telecom payments, EMI, wallet, partnership announcements | https://www.cosmotepayments.gr/ |
| COSMOTE Payments (OTE) corporate site | product launches, acquiring | https://www.cosmotepayments.gr/en_about.html |
| COSMOTE Payments - licensed Greek e-money institution | market statistics, payment statistics | https://www.cosmotepayments.gr/about.html |
| Cardlink (a Worldline brand) — Pressroom & Banks/Financial-Institutions page | payments, POS acquiring, bank partnerships, public contracts, award no | https://cardlink.gr/en/pressroom/ |
| Cardlink official site (cardlink.gr) | acquiring, product launches, partnerships | https://cardlink.gr/en/ |
| DIAS - IRIS Payments product & scheme pages | IRIS instant payments, P2P, P2B, IRIS Commerce, participating banks | https://www.dias.com.gr/el/services/iris-payments/ |
| DIAS Interbank Systems SA (ΔΙΑΣ Α.Ε.) | interbank clearing, public payments, e-paravolo, IRIS, collections | https://www.dias.com.gr/el/i-etaireia/ |
| EBA / EU Register of Payment and Electronic Money Institutions (PSD2) | licences, payment institutions, e-money institutions, PSD2, passportin | https://euclid.eba.europa.eu/register/pir/search |
| EBA CLEARING — RT1 SCT Inst participants & addressable PSPs list | payment statistics, instant payments adoption, market statistics | https://www.ebaclearing.eu/services-instant-payments/rt1-sct-inst/participants/ |
| EBA CLEARING — STEP2 SCT participants | payment statistics, market statistics | https://www.ebaclearing.eu/services-sepa-payments/step2-sct/participants/ |
| ECB - Payments statistics press release (semi-annual) | payment statistics, card statistics | https://www.ecb.europa.eu/press/stats/paysec/html/ecb.pis2025h1~36edd636c8.en.html |
| ECB Data Portal - Payment systems dataset, DIAS transactions (PST) | payment statistics, market statistics | https://data.ecb.europa.eu/data/datasets/PST/PST.A.GR.G3.1._T._T.RPS_GR_1.N.PN.Z01 |
| ECB Data Portal — Credit transfers incl. fraud (PCT dataset, SEPA) | payment statistics, market statistics | https://data.ecb.europa.eu/data/datasets/PCT |
| ECB Data Portal — Direct debits incl. fraud (PDD dataset, SEPA) | payment statistics, market statistics | https://data.ecb.europa.eu/data/datasets/PDD |
| ECB Data Portal — E-money payment transactions incl. fraud (PEM dataset) | payment statistics, market statistics | https://data.ecb.europa.eu/data/datasets/PEM |
| ECB Data Portal — Payments statistics indicators (key figures dashboard) | market statistics, payment statistics, card statistics | https://data.ecb.europa.eu/key-figures/payments-statistics-indicators |
| ECB Data Portal — Payments statistics publication (semi-annual releases + press notes) | payment statistics, card statistics, market statistics | https://data.ecb.europa.eu/publications/payments-statistics/4062040 |
| EDPS (edps.gr) - Greek EFT/POS processor | POS data, card statistics, market statistics | https://edps.gr/product-category/pos/ |
| ELTRUN / eBusiness Lab – Οικονομικό Πανεπιστήμιο Αθηνών (AUEB e-Business & e-Commerce Research Lab) | e-commerce, electronic payments, consumer behavior, card statistics | https://eltrun.org/ |
| EMPSA — European Mobile Payment Systems Association (DIAS/IRIS membership & interoperability news) | instant payments adoption, market statistics, payment statistics | https://empsa.org/ |
| EPI Company — European Payments Initiative / Wero media-insights | European scheme, Wero, EuroPA, A2A payments, scheme competition | https://epicompany.eu/media-insights |
| ESMA list of registered Trade Repositories (EMIR/SFTR) | market_infrastructure, actor_map | https://www.esma.europa.eu/document/list-registered-trade-repositories |
| ESMA short selling / net short positions register | short_selling, issuers, market_signals | https://registers.esma.europa.eu/publication/searchRegister?core=esma_registers_mifid_shsexs |
| EU / EBA — Register of Payment and Electronic Money Institutions (data.europa.eu / Greece) | organization changes | https://data.europa.eu/data/datasets/register-of-payment-and-electronic-money-institutions?locale=el |
| Endeavor Greece — Visa Innovation Program partner blog | card_schemes, fintech, partnerships | https://www.endeavor.org.gr/blog/visa-innovation-program-europe-greece-cyprus-malta |
| EuroPA (European Payments Alliance) - IRIS cross-border interconnection | payment statistics, market statistics | https://www.europ-a.eu/ |
| Euromonitor International — Financial Cards and Payments in Greece | card statistics, payment statistics, market statistics | https://www.euromonitor.com/financial-cards-and-payments-in-greece/report |
| European Payments Council - SEPA Instant Credit Transfer (SCT Inst) scheme & rulebooks | SCT Inst rulebook, implementation guidelines, IPR, pan-European instan | https://www.europeanpaymentscouncil.eu/what-we-do/sepa-instant-credit-transfer |
| European Payments Council — Clearing and Settlement Mechanisms (CSM) scheme-compliance list | clearing and settlement, CSM, SEPA, reachability, DIAS | https://www.europeanpaymentscouncil.eu/what-we-do/epc-payment-scheme-management/clearing-and-settlement-mechanisms |
| European Payments Council — Register of Participants (SEPA schemes) | SEPA, instant payments, participant register, clearing settlement | https://www.europeanpaymentscouncil.eu/what-we-do/be-involved/register-participants |
| European Payments Council — Registers of Participants in SEPA schemes (SCT, SCT Inst, SDD Core, SDD B2B, OCT Inst) | SEPA, scheme adherents, instant payments, PSP census, participants | https://www.europeanpaymentscouncil.eu/what-we-do/be-involved/register-participants/registers-participants-sepa-payment-schemes |
| Eurostat Data Browser - E-commerce sales of enterprises (isoc_ec_eseln2 / esels / evals) | payment statistics, e-commerce, POS data | https://ec.europa.eu/eurostat/databrowser/view/isoc_ec_eseln2/default/table?lang=en |
| Eurostat Data Browser - Internet purchases by individuals / e-commerce (isoc_ec_ib* family) | payment statistics, e-commerce, card statistics | https://ec.europa.eu/eurostat/databrowser/view/isoc_ec_ibuy/default/table?lang=en |
| Everypay (Skroutz) company / about site | product launches, partnerships, acquiring | https://www.everypay.gr/en/company/about |
| Finextra — Viva Wallet / Greek payments company news | press releases, partnerships, product launches | https://www.finextra.com/company-news/5762/viva-wallet |
| Greek eCommerce Association (GR.EC.A / ΕΣΗΕ) | member_directory, policy_positions, press_releases, market_commentary | https://www.greekecommerce.gr/ |
| Greek tourism/business press relay of Visa MoU spend data (insider.gr, tornosnews, tourismtoday) | payment statistics, card statistics, market statistics | https://www.insider.gr/toyrismos/405558/i-visa-ananeonei-ti-synergasia-me-yp-toyrismoy-i-dapani-stin-ellada-2025 |
| GreekReporter.com - English-language Greek news (IRIS coverage) | IRIS instant payments, cross-border, adoption | https://greekreporter.com/2026/07/06/greece-iris-payments-system-expand-cross-border-transfers-europe/ |
| HBA — YouTube channel (webhba) | press releases | https://www.youtube.com/@webhba |
| Hellenic Bank Association (Ελληνική Ένωση Τραπεζών / HBA) - SEPA & payment-systems section | SEPA instant credit transfer, SCT Inst rulebook, IPR, VoP, mobile paym | https://www.hba.gr/info/sepa |
| IDEAS/RePEc — economics research aggregator (author & article index) | payment statistics, card statistics, tax evasion, shadow economy | https://ideas.repec.org/ |
| IOBE - Foundation for Economic & Industrial Research | market_commentary, policy_positions | https://iobe.gr/ |
| IOBE — Foundation for Economic & Industrial Research (Ίδρυμα Οικονομικών και Βιομηχανικών Ερευνών) | market statistics, payment statistics, card statistics, cash usage, sh | https://iobe.gr/en/ |
| KEPE — Centre of Planning and Economic Research (Κέντρο Προγραμματισμού και Οικονομικών Ερευνών) | market statistics, shadow economy, tax evasion, digital transactions,  | https://www.kepe.gr/ |
| MarketScreener - Greek bank analyst consensus / broker-research pages | target_price, ratings, consensus, sell_side_research | https://www.marketscreener.com/quote/stock/EUROBANK-ERGASIAS-SERVICE-1408766/consensus/ |
| Mastercard Borderless Payments Report | payment statistics, market statistics | https://www.mastercard.com/global/en/business/payments/mastercard-move/borderless-payments-report.html |
| Mastercard Economics Institute (MEI) | market statistics, card statistics, payment statistics | https://www.mastercard.com/us/en/news-and-trends/insights-report/mastercard-economic-institute.html |
| Mastercard Global Newsroom — Press | payment statistics, market statistics, card statistics | https://newsroom.mastercard.com/news/press/ |
| Mastercard Global — Newsroom / Stories (global scheme releases) | card issuing, co-brand, tokenisation, scheme partnership | https://www.mastercard.com/global/en/news-and-trends/stories.html |
| Mastercard Greece — Official Facebook (@MastercardGreece) | press releases, partnerships | https://www.facebook.com/MastercardGreece/ |
| Mastercard Greece — Official Site (mastercard.gr) | press releases, partnerships, contactless | https://www.mastercard.gr/el-gr.html |
| Mastercard Newsroom — EEMEA region press releases | partner selection, issuer, acquirer, co-brand, announcements | https://www.mastercard.com/news/eemea/en/newsroom/press-releases/ |
| Mastercard SpendingPulse / SpendingPulse Destinations | market statistics, payment statistics, card statistics | https://www.mastercard.com/us/en/business/insights-intelligence/economic-market-insights/solutions/spendingpulse.html |
| Mastercard Ελλάδα — local Greek site (mastercard.gr) | localisation, co-brand, partner selection, consumer programmes | https://www.mastercard.com/gr/el.html |
| Mellon Group of Companies newsroom | product launches, press releases | https://mellongroup.com/news |
| Mellon Technologies — POS (Ingenico) service & e-shop portal | Ingenico POS, SoftPOS, terminal maintenance, multi-acquirer, consumabl | https://pos.mellongroup.com/ |
| Ministry of National Economy and Finance — State Budget archive (Kratikos Proypologismos) & Introductory Report | market statistics, payment statistics, e-transactions, VAT revenue, ta | https://minfin.gov.gr/kratikos-proypologismos/ |
| NBG / Eurobank card pages — dual Visa+Mastercard co-badge & issuer signals | issuer, co-badging, dual scheme, product localisation | https://www.nbg.gr/el/idiwtes/kathimerines-sunallages/trapezikes-kartes/xrewstikes-kartes/visa-mastercard-debit |
| NBG Pay (National Bank of Greece x Global Payments/EVO acquiring JV) | acquiring, merchant_services, POS, bank_partnership, payments_infrastr | https://nbgpay.globalpayments.com/en-gr/ |
| Naftemporiki — Mastercard Greece country-manager briefings | card statistics, payment statistics, cash usage, market statistics | https://www.naftemporiki.gr/business/2045153/mastercard-me-rythmo-ayxisis-9-i-dieisdysi-karton-stis-pliromes/ |
| National Bank of Greece (NBG / Ethniki) — POS for professionals product page | POS terminals, merchant acquiring, NBG PAY, certified models | https://www.nbg.gr/el/epaggelmaties/proionta-upiresies/eisprakseis-plirwmes/pos |
| National Bank of Greece - SEPA Instant Payments / IPR landing page | SEPA instant credit transfer, IPR, VoP, bank implementation | https://www.nbg.gr/el/lp/sepa-instant-payments |
| Nexi Greece — News (Ελλάδα) | POS, merchant acquiring, partnership | https://www.nexi.gr/en/Resources/news/ |
| Nexi Greece — What's new / IRIS Payment | A2A payments, IRIS, wallet, acquiring, POS, partnership | https://www.nexi.gr/en/whatsnew/ |
| Nexi Greece — retailers & merchants offer / press | acquiring, merchant solutions, e-commerce, partnership announcements | https://www.nexi.gr/ |
| OKTO — digital payments fintech (gaming/leisure/entertainment) | vertical payments, gaming/leisure, wallet, product launches | https://www.hugedomains.com/domain_profile.cfm?d=oktopay.com |
| OTE Group / COSMOTE — Press Center (parent of COSMOTE Payments/payzy) | e_money, digital_wallet, product_launch, partnership, press_release | https://www.cosmote.gr/cs/otegroup/en/press_center.html |
| Oikonomikos Tachydromos (ot.gr) - Greek financial press, banks/payments desk | IRIS instant payments, EuroPA, banks, instant payments | https://www.ot.gr/2026/07/04/epixeiriseis/trapezes/iris-payments-ti-allazei-me-ti-diasyndesi-sto-europa |
| OpenGov public-consultation portal — Ministry of Finance (opengov.gr/minfin) | e-payment tax incentive, policy, legislation, e-transactions | https://opengov.gr/minfin/ |
| Piraeus Bank - IRIS Payments product & instant-payment pages | IRIS instant payments, P2B, IRIS Commerce, EuroPA cross-border, instan | https://www.piraeusbank.gr/en/individuals/banking-products-and-services/banking-services/emvasmata-idiwtwn/iris-payments |
| Piraeus Bank — Visa exclusive partnership / card-scheme migration pages | issuer, scheme migration, partner selection, co-brand, localisation | https://www.piraeusbank.gr/el/idiwtes/proionta-upiresies/kartes/apokleistiki-sunergasia-tis-trapezas-piraeus-me-ti-visa |
| Plum — Press / newsroom | funding, licence, product launch, bank partnership, investing | https://withplum.com/press |
| Quarterly National Accounts - GDP (Τριμηνιαίοι Εθνικοί Λογαριασμοί - ΑΕΠ, SEL84) | market statistics | https://www.statistics.gr/en/statistics/-/publication/SEL84/- |
| Reporters United — investigative payments reporting | acquiring, Worldline-Cardlink, merchant data | https://www.reportersunited.gr/ |
| Revolut Greece - newsroom / corporate communications | market statistics, payment statistics, card statistics | https://www.revolut.com/en-GR/news/ |
| Techmaniacs.gr — Greek tech/consumer media (card scheme-switch coverage) | scheme migration, card re-issue, co-brand | https://techmaniacs.gr/ |
| The Business of Payments (Geoffrey Barraclough) — payments analyst newsletter | payments, acquiring, PSP market, fintech deals | https://businessofpayments.com/ |
| The Nilson Report - global card issuer / merchant-acquirer rankings (Greek institutions) | card statistics, payment statistics, market statistics | https://nilsonreport.com/ |
| The Paypers - payments industry trade media (IRIS / EuroPA / SCT Inst coverage) | IRIS instant payments, EuroPA, SCT Inst, industry news | https://thepaypers.com/payments/news/greece-joins-europa-through-iris-payments |
| The Paypers — Greek PSP company news | press releases, partnerships | https://thepaypers.com/companies/latest-news-on-viva-wallet--25804 |
| The Total Business — Greek retail/e-commerce business news | retail e-commerce, merchant strategy, partnership announcements | https://www.thetotalbusiness.com/ |
| Trading Economics - Greece indicators | market statistics, payment statistics | https://tradingeconomics.com/greece/indicators |
| Transaction Systems — PAX Master Distributor for Central & SE Europe (incl. Greece) | POS, terminals, deployment, distribution, public contracts | https://tr-sys.eu/ |
| Turnover Index in Motor Trade (Δείκτης Κύκλου Εργασιών στο Εμπόριο Αυτοκινήτων) | market statistics | https://www.statistics.gr/en/statistics/-/publication/DKT45/- |
| Turnover and Volume Index in Retail Trade (Δείκτης Κύκλου Εργασιών στο Λιανικό Εμπόριο) | market statistics, cash usage, card statistics | https://www.statistics.gr/en/statistics/-/publication/DKT39/- |
| Visa Corporate Newsroom (Visa Perspectives) | payment statistics, card statistics, cash usage, market statistics | https://corporate.visa.com/en/sites/visa-perspectives/newsroom.html |
| Visa Economic Empowerment Institute (VEEI) | market statistics, cash usage, payment statistics | https://corporate.visa.com/en/sites/visa-economic-empowerment-institute.html |
| Visa Greece (visa.gr) — official Greek site | partnerships, certification, product-launch | https://www.visa.gr/ |
| Visa Innovation Program Europe (Athens hub) | press releases, partnerships, fintech | https://visainnovationprogram.com/ |
| Visa Navigate — Europe (Visa Perspectives / company news) | tokenisation, contactless, card issuing, market signals | https://corporate.visa.com/en/sites/visa-perspectives.html |
| Visa Newsroom — UK/Europe (press releases) | card issuing, co-brand, tokenisation, scheme migration, public contrac | https://www.visa.co.uk/about-visa/newsroom.html |
| Visa UK / Europe Newsroom — Press Releases | payment statistics, market statistics | https://www.visa.co.uk/about-visa/newsroom/press-releases.2991143.html |
| Visa — Newsroom / Press Releases (Europe & UK) | card scheme, issuing, tokenization, partnership, agentic commerce | https://www.visa.co.uk/about-visa/newsroom/press-releases.html |
| Viva.com (Viva Wallet) Greek blog & merchant solutions | acquiring, marketplace payments, e-commerce, partnership announcements | https://www.viva.com/el-gr/blog/ |
| Viva.com - IRIS transfers / EuroPA cross-border participant support & announcements | IRIS instant payments, EuroPA cross-border, PSP participation | https://euhelp.viva.com/en/articles/8560183-how-can-i-transfer-funds-through-iris |
| Viva.com — corporate site & newsroom (Greek market) | partnerships, acquiring, merchant signals | https://www.viva.com/el-gr |
| Viva.com — corporate site / blog (newsroom) | payments, acquiring, tech bank, card issuing, merchant financing | https://www.viva.com/en-gr |
| World Bank Global Findex Database 2025 - Greece | market statistics, payment statistics, card statistics, cash usage | https://www.worldbank.org/en/publication/globalfindex |
| Worldline Greece - Local Media Relations press releases (en-gr) | POS data, market statistics, card statistics | https://worldline.com/en-gr/home/top-navigation/media-relations/press-release |
| Worldline Greece / Cardlink — awards & news | awards, payments, fintech, recognitions | https://www.cardlink.gr/news |
| Worldline Greece Pressroom (Worldline & Cardlink) | press releases, acquiring, partnerships, product launches | https://worldline.com/en-gr/home/pressroom.html |
| eleftherostypos.gr — Δελτία Τύπου (press-release republishing section) | partnerships, product-launch, certification | https://www.eleftherostypos.gr/deltia-typou/ |
| payzy by COSMOTE (COSMOTE Payments) — product/news page | e_money, digital_wallet, ecommerce_payments, cashback, product_launch | https://www.payzy.gr/ |
| selfservice.gr (Σελφ Σέρβις) — organized food-retail trade magazine | POS in retail, acquirer selection, loyalty, self-checkout, retail paym | https://selfservice.gr/ |
| ΔΥΠΑ — Προπληρωμένη Κάρτα (Public Employment Service prepaid card page) | prepaid card, disbursement, cards, benefits, PSP, public contracts | https://www.dypa.gov.gr/prepaid |
| Δι@ύγεια luminapi decision-types taxonomy endpoint | award notices, direct awards, public contracts, payment orders, taxono | https://diavgeia.gov.gr/luminapi/opendata/types.json |
| ΕΕΤ — Ενιαίος Χώρος Πληρωμών σε Ευρώ (SEPA) information hub | SEPA, IBAN, ISO20022, SCT, SDD, interbank_standards, migration | https://www.hba.gr/Info/sepa |
| ΕΣΕΕ – Ελληνική Συνομοσπονδία Εμπορίου & Επιχειρηματικότητας (Hellenic Confederation of Commerce & Entrepreneurship) | card acceptance costs, POS fees, electronic payments, merchant interch | https://esee.gr/ |
| Εμπορικός Σύλλογος Αθηνών (ΕΣΑ, Athens Traders' Association) | POS fees, card acceptance costs, retail statistics, cash usage | https://www.esathena.gr/ |
| ΙΜΕ ΓΣΕΒΕΕ – Ινστιτούτο Μικρών Επιχειρήσεων ΓΣΕΒΕΕ (IME GSEVEE, SME research institute) | card statistics, electronic payments, SME, consumer behavior | https://imegsevee.gr/ |
| ΙΝΣΕΤΕ – Ινστιτούτο ΣΕΤΕ (INSETE, Institute of the Greek Tourism Confederation) | tourism, market statistics, cash usage, card statistics, consumer beha | https://insete.gr/ |
| Ξενοδοχειακό Επιμελητήριο Ελλάδος (Hellenic Chamber of Hotels / ΞΕΕ) | tourism, card acceptance costs, cash usage, market statistics | https://www.grhotels.gr/ |
| ΠΟΕΣΕ – Πανελλήνια Ομοσπονδία Εστιατορικών & Συναφών Επαγγελμάτων (Panhellenic Federation of Restaurants & Related Professions) | card acceptance costs, POS fees, cash usage, electronic payments, HORE | https://www.poese.gr/ |
| ΠΟΞ – Πανελλήνια Ομοσπονδία Ξενοδόχων (POX, Hellenic Hoteliers Federation) | card acceptance costs, tourism, electronic payments, merchant fees | https://www.hhf.gr/ |
| Πράξεις Εκτελεστικής Επιτροπής Τράπεζας Ελλάδος — Bank of Greece Executive Committee Acts index | licensing, payment_institutions, e_money_institutions, supervisory_act | https://www.bankofgreece.gr/trapeza/nomiko-plaisio/prakseis-ektelestikhs-epitrophs |
| Προπληρωμένη Κάρτα Παροχών — official program portal (prepaid.minscfa.gov.gr) | prepaid card, disbursement, cards, payments, benefits, PSP | https://prepaid.minscfa.gov.gr/ |
| ΣΕΛΠΕ – Σύνδεσμος Επιχειρήσεων Λιανικής Πωλήσεως Ελλάδος (SELPE, Hellenic Retail Business Association) | card statistics, electronic payments, e-commerce, consumer behavior, r | https://www.selpe.gr/ |
| ΣΕΤΕ – Σύνδεσμος Ελληνικών Τουριστικών Επιχειρήσεων (SETE, Greek Tourism Confederation) | tourism, card acceptance costs, cash usage, electronic payments | https://sete.gr/ |
| Συνήγορος του Καταναλωτή — Συστάσεις / Πορίσματα (Recommendations & Findings, case decisions) | payment disputes, card statistics | https://www.synigoroskatanaloti.gr/en/systaseis-porismata |