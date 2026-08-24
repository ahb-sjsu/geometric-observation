# Chapter 20 — The False-Clear Rate

> **STUB [A] — draftable now.** Source: `observation-theory-campaigns` freshness
> cells + `FRESHNESS-PROGRAM.md`; ZK cell (`analysis/zk`, `ZK-USE-CASES.ipynb`);
> routing D8 (`analysis/xproto`, `analysis/d8`). House voice per Ch. 19. Every
> number resolves to a `SEALS.md` row (Appendix D/F).

## What this chapter must establish

- **FC as a first-class KPI**, not a derived afterthought: define, measure, report
  per `(certificate, consumer)`. Contrast with the conventions it replaces (a lag
  bound, a convergence timer, a confidence interval) whose *error rate* is never
  itself reported.
- **Vacuity**: a certificate whose FC exceeds its own target is vacuous for that
  consumer. The routing anchor — 60 s quiescence false at **0.351** (BGP) /
  **0.184** (IS-IS) / **0.083** (OSPF) [replicated] — opacity orders the bands,
  implementation places within band.
- **Consumer-relativity, made unavoidable**: the ZK hot/cold **99×** on one replica
  at one instant [replicated]; the database footprint certificate (~0.5 aggregate →
  ~0.02–0.06 per footprint) [replicated]. The aggregate certificate *is* the
  $P_C=I$ error with a clock (tie back to Ch. 2).
- **The two-sided cost**: false-clear (danger) vs false-refresh (waste); the
  certificate interpolates between free-and-wrong and correct-but-costly (the ZK
  `read_fresh` curve).

## Key figures / claims (→ ledger)
- FC definition box (from Ch. 19). 
- Routing vacuity bar (three protocols) [replicated].
- ZK hot-vs-cold same-replica plot [replicated].
- DB aggregate-vs-footprint table [replicated].

## Boundary
FC needs a sound witness; where none exists the claim is inference, not
certification (forward-ref Ch. 23 + the skeptic's appendix).
