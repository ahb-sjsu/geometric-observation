# Novelty sweep — partial (2026-09-06)

**Scope and honest limitation.** This is a delineation analysis plus targeted
record checks, NOT a live literature crawl: the web-search budget was exhausted
this session, so the open-ended "is there a 2024-2026 paper that pre-empts the
augmented region" question is left as owner search items below, with exact
queries. What was done: (1) audited the manuscript's own prior-art delineation,
(2) fetched and characterized the closest flagged preprint, (3) identified one
literature line the paper does not engage.

## 1. The manuscript's existing delineation is strong

The paper already carries a theorem-level "nearest prior" comparison table and a
Related Work section that positions against the correct core line: Gray's
conditional RDF (`gray1972tr,gray1973`, the `tau^2 -> 0` anchor), Steinberg's
common-reconstruction functional (`steinberg2009`, which `min I(X;\hat X | S)`
equals), the Lapidoth-Malar-Wigger augmentation device (`lapidoth2014`, Remark 8,
credited for the encoder-pair-access idea), Wyner-Ziv (`wynerziv1976`, proof
device only), Kaspi (`kaspi1994`), Heegard-Berger (`heegardberger1985`), Ahmadi
et al. (`ahmadi2013`), the Xiao-Luo / Lapidoth-Tinguely / Nayak / Stylianou floor
line, Gaussian IB (`chechik2005`), and the Landauer thermodynamic line. This is
more thorough than most T-IT submissions and is a genuine strength; the claimed
deltas (exact Gaussian closed form of the AUGMENTED functional; the 2-D
rate-content region with two water levels; the misalignment dichotomy; the
non-determination corollary) are stated against named priors.

## 2. Verified by direct fetch: Chen et al. is not a core competitor

`chen2026` = arXiv:2607.09545, Chen, Gao, Shi, Wu, Caire, Poor, Zhang (2026),
"On the Gaussian-Quadratic Rate-Distortion Function for Vector Sources with
Individual Distortion Constraints." It is vector Gaussian RDF under per-component
distortion constraints (Hadamard-bound tightness), with no conditional content,
side information, common reconstruction, or encoder-observed context. The
manuscript cites it correctly, for the vector/floor comparison only (near
Theorem 24), not the core. Status: still an arXiv preprint (submitted 2026-07-10),
so no IEEE Xplore record yet -> keep the "to be published"/arXiv citation. This
closes the README checklist item "Chen et al. re-check for an Xplore record"
(answer: none yet).

## 3. THE GAP: the rate-distortion-equivocation / secure-source-coding line

The paper's priced quantity is `L = H(M | S^n)/n`, the conditional entropy of the
stored description given a third party's noisy copy `S = V + U`. The manuscript
motivates this thermodynamically (Landauer erasure work) and positions it only
through Steinberg's common-reconstruction tradition. But mathematically
`H(M | S)` is the **equivocation of the transmitted description at a party holding
noisy side information**, and there is an entire information-theoretic-security
line on rate-distortion-equivocation and secure source coding with side
information at an eavesdropper that the manuscript does not cite. A T-IT referee
from that community will recognize `H(M|S)` as equivocation and expect it engaged.
Currently the manuscript contains no reference to it (grep: no equivocation,
secrecy, secure, wiretap, eavesdropper, Yamamoto, Villard, Piantanida, Schieler,
Cuff, Prabhakaran; one incidental "no-leakage condition" at a technical step).

**Assessment: likely a delineation gap, not a scoop** — those results typically
price equivocation of the SOURCE `H(X^n | Z, M)` and maximize secrecy, whereas
this paper prices the DESCRIPTION's entropy `H(M|S)` and minimizes it as an
erasure cost, with the encoder observing the clean context and an exact Gaussian
region as the deliverable. That distinction is real and defensible, but it must
be drawn explicitly. I could not confirm the closest secrecy paper's exact region
by fetch (wrong arXiv ID on the one attempt; no search budget to find the right
one), so a low-but-nonzero scoop risk on the Gaussian region remains until the
owner checks the papers named below.

**Recommended action (one paragraph in Related Work): DONE 2026-09-06.** Added a
"security reading" paragraph to the Related Work section citing Yamamoto (Shannon
cipher system, `yamamoto1997`), Villard-Piantanida (secure source coding with SI
at the eavesdropper, `villard2013`), and Schieler-Cuff (rate-distortion theory
for secrecy systems, `schieler2014`), drawing the distinction: (a) `H(M|S)` is
the equivocation of the DESCRIPTION, minimized as erasure cost, not source
secrecy maximized; (b) the encoder observes clean context `V`; (c) Thm-region,
Cor-misalign, and Cor-notmarginal are, to our knowledge, new relative to this
line. Rebuild verified: 35 pp, 0 undefined, 0 overfull. **Citation details VERIFIED
2026-09-06** against DBLP (via curl; the WebFetch/DBLP-API 503'd, curl with a
normal UA worked): all three exact, `% verify` flags removed:
- Yamamoto, IEEE T-IT 43(3):827--835, 1997, doi 10.1109/18.568694.
- Villard & Piantanida, IEEE T-IT 59(6):3668--3692, 2013, doi 10.1109/TIT.2013.2245394.
- Schieler & Cuff, IEEE T-IT 60(12):7584--7605, 2014, doi 10.1109/TIT.2014.2365175.
(DOIs recorded here for provenance; not added to the bibitems, matching the
manuscript's convention of omitting DOIs on published journal entries.)
**LIVE SCOOP-CHECK RUN 2026-09-06 (external reviewer screen through 2026-09-06).**
Result: the Gaussian core survives; the BINARY endpoint (Thm 27) is unsafe.
Applied to the manuscript this session (all reviewer "immediate changes"):
- Gaussian quadratic (Thm 13), joint frontier + misalignment dichotomy (Thm 16 /
  Cor 19), non-determination (Cor 21): survive; retained. "no water-filling"
  softened to "we are unaware of a prior derivation of this coupled frontier".
- Pair sufficiency (Thm 9): recast as a distortion-preserving specialization of
  Armstrong 2026 (arXiv:2604.26744, source-side sufficiency for the IB); cited;
  intro "everything ... is new" qualified accordingly.
- BINARY (Thm 27): nearest prior is Lu, Xu, Qian, Wang, "The binary
  Heegard-Berger problem with encoder side information and common reconstruction
  constraints," WCSP 2016 (encoder SI + CR = the real overlap). Table I row
  replaced; the p.30 "nearest = decoder-SI" claim replaced with the Lu et al.
  paragraph; abstract "solve the DSBS case completely" recast to "give the joint
  rate-content frontier"; binary contribution recast around the tilt + joint
  (R,L) frontier (Remark 28), which appears to survive. Appendix app:lucompare
  added as a SCAFFOLD (relabeling X_Lu<->Y, S_enc<->V, S_dec<->S fixed; the
  formula-by-formula identification of their value with L(D) at q=0 is NOT
  asserted).
- Added: Guler-MolavianJazi-Yener ISIT 2015 (remote source coding w/ two-sided
  info) as the non-CR baseline; Meidlinger-Winkelbauer-Matz SSP 2014 (Gaussian
  IB <-> MSE RD quantization); Lu-Xu WCSP 2021 (vector Gaussian HB w/ CR) as the
  vector counterpart, limit-correspondence noted not resolved. All 5 new cites
  from DBLP canonical records. Rebuild: 36 pp, 0 undefined, 0 overfull, all cites
  + app:lucompare resolve.

**app:lucompare COMPLETED 2026-09-06 (owner supplied the PDF -> docs/).** The
primary source is Lu, Xu, Zhang, Feng, Wang, "Binary lossy coding problem with
encoder side information and common reconstruction constraint," WCSP 2016 (the
reviewer's IEEE 7752468 -- a DISTINCT paper from the Heegard-Berger companion
7752469, so that open question is resolved: yes, two Lu et al. 2016 items).
RESULT: their Theorem 1 rate $\widetilde R^{CR}(D)=\min I(X,S_1;W|S_2)$ is, under
$X\!\leftrightarrow\!Y,S_1\!\leftrightarrow\!V,S_2\!\leftrightarrow\!S,
W\!\leftrightarrow\!\hat Y,(p_1,p_2)\!\leftrightarrow\!(p,q)$, IDENTICALLY our
conditional-content functional $I((Y,V);\hat Y|S)=L$. So our binary $L(D)$
COINCIDES with their CR rate and is credited, NOT claimed new. Endpoints checked:
$q=0$ ($p_2=0$) -> Gray $h(p)-h(D)$ (their Remark 3); $q=1/2$ ($p_2=1/2$) ->
marginal $1-h(D)$; $D=0$ -> $h(p*q)$ (their Remark 1). What stays NEW: the joint
$(R,L)$ region + tilt parametrization (Remark 28) -- they price the single CR
rate only, no unconditional rate coordinate, no tradeoff. Also: same functional,
DIFFERENT operational role (their transmitted Wyner-Ziv rate vs our third-party
erasure content). Manuscript updated: abstract/intro/Table I/binary prose recast
to credit $L(D)$ and scope the binary contribution to the frontier; the appendix
now states the comparison in full; the OWNER-TODO / do-not-submit flag is
REMOVED. Build 37 pp, 0 undefined/overfull. Bibitem lu2016lossy added (page range
carries a verify flag: read from the author PDF while DBLP was in maintenance).
Only genuinely-remaining pre-submission item is the Steinberg 2009 binary
institutional read (minor, decoder-SI comparison).
Prabhakaran-Ramchandran (source coding with a helper/eavesdropper) was NOT cited
(kept the paragraph to three well-identified references); add it if the live
search shows it is closer than the three.

## 4. Secondary risk (framing, not prior art)

The nearest prior is Steinberg CR + LMW Remark 8, which already identify the
augmented functional in the abstract. A referee could frame the Gaussian closed
form as an evaluation of a known object. Mitigation is already in the paper's
structure: lead the contribution with the 2-D region (Thm 16), the misalignment
dichotomy (Cor 19), and non-determination (Cor 21), which are new phenomena, not
with the closed form alone. Keep the abstract and intro weighted that way.

## 5. Owner search items (need live search; run at submission)

Exact queries to run (Google Scholar / IEEE Xplore / arXiv):
- "rate distortion equivocation" side information eavesdropper Gaussian
- "secure source coding" "side information" eavesdropper region  (Villard Piantanida)
- "rate-distortion" secrecy systems  (Schieler Cuff 2014) — read the Gaussian case
- Yamamoto rate distortion secrecy 1997 — the scalar/Gaussian result
- conditional content OR "message equivocation" "common reconstruction" Gaussian  (2023-2026)
- "encoder observed context" OR "encoder side information" "common reconstruction" region
- Steinberg 2009 binary example — institutional read (README item, still open)
- Lu et al., WCSP 2016 — institutional read (README item, still open); resolve exact title

Goal of the sweep: confirm no existing result already gives the exact Gaussian
augmented rate-content region (Thm 16) or the misalignment dichotomy (Cor 19). If
clean, the paper's novelty stands; the only required manuscript change is the
Related Work paragraph in section 3 above.
