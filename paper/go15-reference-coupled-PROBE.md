# GO-15 probe record (reference-coupled erasure) -- opened 2026-08-06

Origin: the GO-14 R-IND-5 pass on Theorems R+C established that
records coupled to the reference noise U form a DIFFERENT coordinate
(chain rule false, up to 4.59-bit residual; corrected identity
nL_a = block + C_Delta - sum_t I(S_{>t+Delta}; Yh_t | T, S^{t+Delta},
Yh^{t-1}); exact iff U-coupling Delta-lag causal; certified feasible
general-U record at L_a(0) = 0.092864 vs U-independent family min
0.5667581 -- 84% collapse, sandwich inverted). GO-15 = that object.

## Novelty flank sweep (2026-08-06, 30 queries arXiv/Crossref/DBLP;
S2 fully rate-limited, 2/5 DBLP lost -- disclosed): CLAIMABLE

No prior claim found on: a causally-conditioned per-cell erasure
coordinate for records correlated with the eraser's reference noise;
its corrected chain rule; the Delta-lag-causal preservation
subfamily. Null sets on record per channel. KNOWN core to cite:
erasure work = H(S|O) with side information (del Rio et al.
1009.1630 -- cornerstone), Sagawa-Ueda 2009, Berta et al. 1609.06994
(conditional erasure of correlations -- closest phrase-level,
distinguish: no V+U decomposition, no causal structure). ADJACENT to
cite+distinguish: Cover-Chiang 2002 + Kaspi 1994 (two-sided STATE,
rate not work), Gelfand-Pinsker/Costa, arXiv:1507.04924
(input-NOISE-dependent state -- closest structural analog, CHANNEL
side, capacity, non-causal), Permuter-Weissman vending machine,
Ito-Sagawa 1306.2756 (causally-conditioned machinery in stochastic
thermo, never composed with reference-correlated erasure),
Cuff-Permuter-Cover coordination (the GO-9 exterior),
Perarnau-Llobet 1407.7765 (work FROM correlations, converse
direction). Note-only: certified deletion / unlearning (different
senses); "Premise-Erasure Caching" 2603.00930 is a name collision.
OWED at tex-draft time before any seal: targeted re-sweep of (a)
one-shot quantum-thermo followups to Berta 1609.06994, (b) the
Charalambous directed-info/feedback-RDF line (tracked in GO-14).

## Opening probe (2026-08-06): four-level hierarchy; the collapse is
gated by ENCODER LOOKAHEAD PAST THE ERASER'S HORIZON

Evaluator FD-validated (7e-10; vs definitional 1.6e-14); anchors
reproduced (uind 0.5667582; trivial 0.539536; R-IND-5 record
0.0928562). VALUE TABLE (16,0): general-U **0.078685** (0.0929 was
an iteration-capped endpoint; valley floor ~0.077(1)) << 
S-constructible 0.2898 << Delta-causal 0.5224 < U-indep 0.5668.
86% collapse. STRUCTURE (universal, 24 winners): Au mass 63-93% on
the SINGLE first-beyond-horizon band s = t+Delta+1, NEGATIVE
(corr(Yh_t, U_{t+1}) = -0.245 spike) -- "reference-noise
anticipation," the GO-14 horizon mechanism transplanted from
V-cancellation to U-anticipation; needs the full cross-cell code
(a lone band on the trivial record: 0.5395 -> only 0.5316).
DECOMPOSITION at the winner: block 5.243 + C 0.673 - Dterm 5.837 =
0.0787 -- the T-conditional Dterm buys the collapse (74x the final
value); block/Dterm individually diverge at the boundary, only the
difference is physical. Delta-causal winners have Dterm = 0 to
1e-16 (preservation confirmed at optimizers) and Au ~= Av: the
Delta-causal optimum IS essentially causally-S-constructible.
DELTA-REVERSAL: general min RISES in Delta (0.079 -> 0.201 -> 0.219
at n=16), rejoining block at Delta = n -- the lag knob reverses
sign across the U-coupling boundary.
OPERATIONAL VERDICT (Q4): S-constructible captures 57% of the
collapse and already inverts the sandwich (0.29 << block_16 =
0.535); direct U-access is load-bearing for the last ~0.21 bits
(resolving S into V+U -- fictitious). THE SHARP LINE: collapse <=>
the encoder's reference window extends beyond the eraser's access
horizon (lookahead <= horizon -> 0.52-level; full lookahead ->
0.29; U-resolution -> 0.079). GO-15's object = the S-constructible
family with an encoder-lookahead parameter; general-U = the labeled
fictitious outer relaxation.
SCOPING (load-bearing): winners ride the deterministic-record
boundary (BB' eigmin 1e-13..1e-9; log-type noise singularity:
+1e-4 isotropic noise -> 0.727) -- every minimum claim MUST carry a
noise floor; FLOOR LAW (not artifact): min <= 0.0787/0.1054/0.1487/
0.3656 at floors 1e-8/1e-6/1e-4/1e-2, ALL below block_16 -- the
phenomenon survives realistic noise, the VALUE is floor-relative.
KKT degenerates at collapse winners (state distortion as boundary
geometry). NO LOWER BOUNDS exist for U-coupled families (Theorems
R/C break in both legs) -- every number is class-conditional UB
until a GO-15 LB face lands; n-scan variance is optimization-depth,
not physics (equal-depth numerics or the LB needed before any
n-trend claim).
CONJECTURE LIST for the statement tex (from the probe): Prop 1
corrected identity + vanishing-iff-Delta-causal; Conj 1 strict
four-level hierarchy (floors <= 1e-2); Conj 2 horizon-matched
anti-coupling (>= 60% mass at s = t+Delta+1, negative); Conj 3
Delta-reversal (F_U increasing, rejoins block at Delta = n; F_S
shape open); Conj 4 boundary attainment + floor-continuity (the
sigma0 -> 0 limit at fixed n open); Q5 LB face (extend Theorem R to
extended moments -- denominator leg already convex; numerator
regrouping = the prover target); Q6 Landauer face (erasure cost
against a causally-growing reference is NOT encoder-independent;
collapse gated by lookahead); Q7 process limit (blocked on
equal-depth or LB). Probe artifacts in scratchpad go15probe/
(winners4.npz, deepwin4b_16_0.npz, analyze4.out).

## LB-face prover (2026-08-07): Theorem R+ and the DC form PROVED; convexity REFUTED with a canonical counterexample; the F_Dc face CERTIFIED -- and two probe numbers CORRECTED

THEOREM R+ (extended moment representation, schedule-general):
coordinates Hw = Cov(Yh,W), Hu = Cov(Yh,U) = tau^2 Au, Gamma;
cone = the LMI N := Gamma - G Pe G' >= 0 (N IS Cov(Z)), with
Pe = blkdiag(SigW^-1, tau^-2 I). Distortion is affine in (Hw,Gamma)
and INDEPENDENT OF Hu (load-bearing). Then 2ln2 n L_a = [block
bracket with Qe = F Cs^-1 F'] + [leak sum] + [sum_j ln Var(S_j | W,
S^{j-1}, Yh^{k(j)}) - ln tau^2]. Verified 300 cells against TWO
independent evaluators (worst 9.5e-9, typical 1e-14).
LEG CURVATURE: block bracket CONVEX -- it is exactly GO-14 Thm R/C
with the AUGMENTED source W+ = (W,U) (Sig_{W+} = blkdiag(SigW,
tau^2 I) since U _|_ W), so the 074 lift applies verbatim once
Re := Pe - Qe >= 0, closed form Sig_{W+}^-1 Sig_{W+|S} Sig_{W+}^-1
(eigmin -3.6e-16..-2.4e-15; lift identity 1e-9; eigmax(Z) 0.999996
< 1). Leak sum CONVEX (inf-of-affine pivots). **THE FAILING TERM is
the S-side DENOMINATOR pivot sum -- concave, entering with a +
sign.** So n L_a = L_a+ - Dterm where L_a+ is GO-14's coordinate for
the augmented source: AN EXACT DC DECOMPOSITION, both pieces convex
in closed form on a convex LMI cone. Dterm vanishes identically iff
Hu is Delta-lag-causal (0.000e+00 vs -3.20/-6.56/-6.76/-11.37 bits
dense). This ALSO REPAIRS GO-14 rem:ulegs: the EXTENDED moment form
is exact at every Au, causal or not (the recorded "2.4-3.5 bits"
failure was of the un-extended form).
CONVEXITY REFUTED. Midpoint sweeps are the WRONG instrument (4,800
pairs: ZERO violations -- the negative curvature lives in a thin
Hu-subspace). Hessian scan: indefinite at 18-26 of ~28 interior
points per (n,Delta) cell; worst rel eigmin -1.88e-1. CANONICAL
COUNTEREXAMPLE (base = the GO-14 certified F0 optimizer at (16,0);
since distortion is Hu-free, +/-eps on the U-block gives identical
distortion with the F0 optimizer as EXACT midpoint; A = the
first-beyond-horizon band, eps = 0.6): n L_a = 9.5031465571 /
8.3974861139 / midpoint 9.0681306448 vs mean 8.9503163355 ->
**JENSEN VIOLATION +1.178143e-01 bits** (+7.363e-03 per symbol),
reproduced to the last digit by the independent definitional
evaluator; all three feasible (cone slack 8.97e-2, dist-D -1.4e-8).
In words: the U-INDEPENDENT record is strictly MORE EXPENSIVE than
the average of two symmetric U-coupled records at the same
distortion. CONTROLS at the same base point, same machinery:
all-directions eigmin -3.85 (indefinite) | F0-only +0.261 (PSD --
GO-14 Thm C reproduced) | F_Dc-only +0.260 (PSD) | pure-Hu -2.358
(the whole defect). Same pattern at (8,0). Piece decomposition:
convex part contributes -4.5034, the concave -Dterm +4.6212 -- the
failing term carries the WHOLE violation. F_S also fails.
**This refutes the natural reading of Q5**: the NUMERATOR
regrouping is not the obstacle (block regroups perfectly, leak is
convex); the DENOMINATOR's S-side pivot sum is, and no regrouping
removes it.
CERTIFIED LB FACE for F_Dc (the first for any U-coupled family --
the section is LINEAR in the LMI cone and Dterm vanishes there, so
079 machinery applies): (16,0) [0.522354033, 0.522356390] w 2.36e-6;
(12,0) [0.523221769, 0.523224986]; (8,0) [0.524961127, 0.524962345];
(16,2) [0.500749120, 0.500753370]. F0 CONTROLS reproduce GO-14's
sealed brackets cold-start with an independent evaluator.
TWO STRICT SEPARATIONS NOW THEOREMS: min F_S <= 0.1698616 <
0.522354033 = LB(F_Dc) (margin 0.3525 ~ 1.5e5 bracket widths); and
min F_Dc < min F_0 at four cells (margin 0.0444 at (16,0)).
min F_U < min F_S remains CONJECTURAL (two UBs, no LB on F_S).
NOT CERTIFIABLE (honest): any value for F_U or F_S. Best LB for the
headline cell is 0 (CMI nonnegativity). All four routes vacuous:
duality needs convexity (refuted); DC decoupling gives <= -12.056;
numerator-floor minorant loses 9.966 bits/cell; the
information-inequality relaxation is ITSELF non-convex and already
negative at the winner. STRUCTURAL OBSTRUCTION: the floor-1e-6
optimum 0.1043 sits inside block 6.0817 + leak 0.5279 - Dterm
6.5053 -- a 62x CANCELLATION; every decoupling relaxation loses
~(1/2)log2(1/sigma0^2) ~ 10 bits, i.e. 100x the quantity being
bounded. No decoupled bound can work at any realistic floor.
**TWO PROBE-RECORD CORRECTIONS OWED (folded into the tex):** at
matched floor 1e-6, F_U UB = 0.1042575 (probe floor-law said
0.1054) and **F_S UB = 0.1698616, far below the probe's floorless
0.2898 -- the probe's F_S search was UNDER-CONVERGED**. So F_S
captures **85.8%** of the collapse, NOT 57%, and direct
U-resolution is load-bearing for only ~0.066 bits, not ~0.21. The
QUALITATIVE verdict (collapse <=> encoder lookahead past the
eraser's horizon) is UNTOUCHED; the quantitative split is not.
Current hierarchy anchors for F_S/F_U are optimization-depth
artefacts at the second decimal -- equal-depth matched-floor reruns
are owed BEFORE any branch-and-bound target is set.
SEALABLE NOW (three items, no value claim on the headline cell):
Theorem R+ with the DC form; the non-convexity refutation with its
canonical counterexample + three matched controls; the F_Dc
certified two-sided face with the two strict separations. NEXT RUNG
for the headline cell: spatial branch-and-bound on the Hu block over
the DC form (distortion is Hu-free, so the branching variable is
budget-unconstrained, and >=60% of optimizer Hu mass sits on one
band) -- but ONLY after the equal-depth matched-floor reruns.