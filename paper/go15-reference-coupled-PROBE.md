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