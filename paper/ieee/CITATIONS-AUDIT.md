# Citations audit — OT applied-instance papers (2026-08-23)

Submission-readiness pass over the bibliographies of the radio, databases, and
ZooKeeper papers. Status per reference; corrections applied inline to the `.bib`.

## Verified this pass (web-checked)
- **Sampath, Kumar, Holtzman, "On Setting Reverse Link Target SIR in a CDMA
  System"** — confirmed *Proc. IEEE 47th VTC*, Phoenix, AZ, 1997, **pp. 929–933**.
  FIXED: added pages + venue detail (`ot-radio-freshness.bib`).
- **Wen, Shih, Jin, "Deep Learning for Massive MIMO CSI Feedback"** — confirmed
  *IEEE Wireless Comm. Letters* **7(5), 748–751, Oct 2018**. Entry correct.
- **Hoydis et al., "Sionna: An Open-Source Library…"** — confirmed
  **arXiv:2203.11854, Mar 2022**. FIXED: author list had two fabricated names
  (Nimier-David, Maggi — Sionna-RT contributors, not on the whitepaper) and
  omitted Binder; corrected to Hoydis, Cammerer, Ait Aoudia, Vem, Binder,
  Marcus, Keller (`ot-radio-freshness.bib`).

## High-confidence standard references (confirm exact pages/DOI at submission)
These are well-known, correctly attributed by author/venue/year; only exact page
ranges / DOIs remain to be filled before final submission:
- Kaul, Yates, Gruteser, "Real-Time Status…" — IEEE INFOCOM 2012.
- Bailis et al., "Probabilistically Bounded Staleness…" — PVLDB 5(8), 2012.
- Corbett et al., "Spanner…" — USENIX OSDI 2012.
- Terry et al., "Session Guarantees for Weakly Consistent Replicated Data" — PDIS 1994.
- Shapiro, Preguiça, Baquero, Zawirski, "Conflict-Free Replicated Data Types" — SSS 2011.
- Hunt, Konar, Junqueira, Reed, "ZooKeeper…" — USENIX ATC 2010.
- Junqueira, Reed, Serafini, "Zab…" — IEEE/IFIP DSN 2011.
- Cooper et al., "Benchmarking Cloud Serving Systems with YCSB" — ACM SoCC 2010.
- Gilbert, Lynch, "Brewer's Conjecture…" — ACM SIGACT News 33(2), 2002.
- Abadi, "Consistency Tradeoffs…" — IEEE Computer 45(2), 2012.
- 3GPP TS 38.214 / TS 38.212 / TR 38.901 / TS 38.213 — cite the exact release
  (e.g., Rel-17) and version at submission.
- RFC 4271 / 7854 / 6811 / 2439 (routing paper) — IETF RFCs, stable.

## Author's own works — finalize at submission
- `bond_ot` (Observation Theory, submitted to IEEE TIT), `bond_turboquant`
  (TurboQuant, repo/DOI), `bond_prereg` (program repo). Update with final
  venues / Zenodo DOIs when assigned.

## Note
No web database was queried for the "high-confidence" block this pass; those
entries are asserted from knowledge and should get a DOI/page check against IEEE
Xplore / ACM DL / DBLP before camera-ready. The three highest-risk entries (a
1997 conference paper, a 2018 letter, an arXiv whitepaper) were web-verified;
one carried a real author-list error, now fixed.
