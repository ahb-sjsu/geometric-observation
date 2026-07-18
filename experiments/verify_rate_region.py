# Numerical falsification harness for the FULL two-stage (and k-stage) rate REGION
# of successive refinement across observers -- the extension of the two-observer
# theorem (paper/ieee, sec. "Successive refinement across observers").  numpy only.
#
# Region (task A):
#   R(D1,D2) = { (R1,R2) : exists Sigma_f <= Sigma_b <= Sx,
#                          tr(P1 Sigma_b) <= D1,  tr(P2 Sigma_f) <= D2,
#                          R1      >= 1/2 log det(Sx)/det(Sigma_b),
#                          R1 + R2 >= 1/2 log det(Sx)/det(Sigma_f) }.
# CONVERSE uses ONLY: Lemma 1 (cond. mean serves every observer, incl. the PAIR
#   -conditional mean for observer 2), law of total covariance (=> nesting, NO
#   Markov), Lemma 2 (info bound).  NOT Lemma 3 (Markov), NOT Lemma 4 (uniqueness).
# ACHIEVABILITY: nested-Gaussian test channels realizing any feasible chain
#   Sigma_k <= ... <= Sigma_1 <= Sx.  The clean, provably-correct k-stage realization
#   is INDEPENDENT FISHER INCREMENTS: Z_i = Delta_i^{1/2} X + M_i (M_i iid N(0,I)),
#   Delta_i = Lambda_i - Lambda_{i-1} >= 0, Lambda_i = Sigma_i^{-1} - Sx^{-1}; then
#   Fisher info ADDS so Cov(X | Z_1..Z_i) = (Sx^{-1}+Lambda_i)^{-1} = Sigma_i exactly.
#   [FINDING: naively CHAINING the paper's 2-stage K-map -- Y_i = K_i^{1/2} Y_{i+1}+...,
#    K_i = Lam_{i+1}^{+1/2} Lam_i Lam_{i+1}^{+1/2} -- does NOT preserve Fisher info for
#    k>=3: B_{i+1}^T B_{i+1}=Lam_{i+1} only up to a rotation Q (B_{i+1}=Q Lam_{i+1}^{1/2}),
#    so the next contraction lands on Q Lam^{1/2}, not Lam^{1/2}, and Fisher(Y_i) != Lam_i.
#    Test [1b] confirms the K-map IS exact for the single 2-stage contraction the paper
#    actually uses.  The k>=3 sufficiency proof should say "chain physically-degraded
#    Gaussian channels" (independent increments), NOT "iterate the K-map verbatim".]
# Thm 5 (refinable iff Sig2*<=Sig1*) and Thm 6 (loss L=1/2 log detSig2*/detSig_o) are the
#   min-sum-rate corner; uniqueness (Lemma 4) re-enters ONLY there.  MIT License.
import numpy as np
rng = np.random.default_rng(20260717)

def spd(n):
    A = rng.standard_normal((n, n)); return A @ A.T + 0.5*np.eye(n)

def sqrtm_sym(M):
    w, U = np.linalg.eigh((M+M.T)/2); return U @ np.diag(np.sqrt(np.maximum(w,0))) @ U.T

def mineig(M): return float(np.linalg.eigvalsh((M+M.T)/2).min())

def logdet(M): return float(np.linalg.slogdet((M+M.T)/2)[1])

def sigma_star(P, D, Cap):
    """argmax{ logdet Sigma : 0<=Sigma<=Cap, tr(P Sigma)<=D }  (reverse water-filling in
    the Cap^{1/2}-whitened basis; the Sigma<=Cap cap binds on ker P).  Cap = Sx gives the
    single-stage optimum; Cap = Sigma1* gives the Thm-6 constrained optimum Sigma_o."""
    Ch = sqrtm_sym(Cap)
    p, V = np.linalg.eigh((Ch @ P @ Ch)); p = np.maximum(p, 0.0)
    if D >= float(np.sum(p)):
        e = np.ones_like(p)
    else:
        lo, hi = 0.0, max(p.max(), 1e-9)
        for _ in range(200):
            mid = 0.5*(lo+hi)
            if float(np.sum(np.minimum(p, mid))) < D: lo = mid
            else: hi = mid
        theta = 0.5*(lo+hi)
        e = np.minimum(1.0, np.where(p > 0, theta/np.where(p>0,p,1.0), 1.0))
    return Ch @ (V @ np.diag(e) @ V.T) @ Ch

def lam(Sig, Sx): return np.linalg.inv(Sig) - np.linalg.inv(Sx)

def post_cov(Sx, M, Sn):
    """Cov(X | Y),  Y = M X + noise(0,Sn), jointly Gaussian."""
    Syy = M @ Sx @ M.T + Sn; Sxy = Sx @ M.T
    P = Sx - Sxy @ np.linalg.pinv((Syy+Syy.T)/2, rcond=1e-12) @ Sxy.T
    return (P+P.T)/2

def chain_realize(Sx, Sigmas):
    """Independent-Fisher-increment realization of a nested chain Sx >= Sig_1 >= ... >= Sig_k.
    Returns (covs, rates): covs[i] = Cov(X|Z_1..Z_i) computed from the JOINT covariance
    (no (Sx^{-1}+Lam_i)^{-1} shortcut assumed), rates[i] = I(X;Z_1..Z_i)."""
    d = Sx.shape[0]; Lams = [lam(S, Sx) for S in Sigmas]
    prev = np.zeros((d, d)); Bblocks = []
    for L in Lams:
        Bblocks.append(sqrtm_sym(L - prev)); prev = L           # Delta_i^{1/2}, Delta_i>=0
    covs, rates = [], []
    for i in range(len(Sigmas)):
        M = np.vstack(Bblocks[:i+1]); Sn = np.eye(M.shape[0])
        C = post_cov(Sx, M, Sn); covs.append(C)
        rates.append(0.5*(logdet(Sx) - logdet(C)))
    return covs, rates

fail = []
# =====================================================================================
print("="*76); print("[1] ACHIEVABILITY: nested-Gaussian channels reproduce every feasible (Sb,Sf)")
worst = 0.0
for d in (2, 3):
    for trial in range(80):
        Sx = spd(d); P1 = spd(d); P2 = spd(d)
        D1 = rng.uniform(0.25, 0.85)*np.trace(P1@Sx)
        D2 = rng.uniform(0.10, 0.85)*np.trace(P2@Sx)
        Sb = sigma_star(P1, D1, Sx)                              # base optimum, observer 1
        Sf = sigma_star(P2, D2, Sb)                             # fine, constrained Sf<=Sb (=Sigma_o)
        assert mineig(Sb - Sf) >= -1e-8
        covs, rates = chain_realize(Sx, [Sb, Sf])
        eb = np.linalg.norm(covs[0]-Sb); ef = np.linalg.norm(covs[1]-Sf)
        er1 = abs(rates[0]-0.5*(logdet(Sx)-logdet(Sb)))
        ert = abs(rates[1]-0.5*(logdet(Sx)-logdet(Sf)))
        tr_ok = np.trace(P1@Sb) <= D1+1e-9 and np.trace(P2@Sf) <= D2+1e-9
        worst = max(worst, eb, ef, er1, ert)
        if not (eb<1e-9 and ef<1e-9 and er1<1e-10 and ert<1e-10 and tr_ok):
            fail.append(f"achiev d={d} t={trial} eb={eb:.1e} ef={ef:.1e}")
print(f"  d in 2,3 x 80: Cov(X|Y1)=Sb, Cov(X|Y1,Y2)=Sf, rates on boundary, feasible."
      f"  worst residual = {worst:.1e}")

print("-"*76); print("[1b] paper's exact 2-stage K-map: Y2=Lam_f^{1/2}X+N, Y1=K^{1/2}Y2+(I-K)^{1/2}N'")
wk = 0.0
for d in (2, 3):
    for _ in range(80):
        Sx = spd(d); P1 = spd(d); P2 = spd(d)
        D1 = rng.uniform(0.25,0.85)*np.trace(P1@Sx); D2 = rng.uniform(0.10,0.85)*np.trace(P2@Sx)
        Sb = sigma_star(P1, D1, Sx); Sf = sigma_star(P2, D2, Sb)
        Lb, Lf = lam(Sb, Sx), lam(Sf, Sx)                       # 0<=Lb<=Lf  (Sf<=Sb)
        Lfh = sqrtm_sym(Lf); Lfp = np.linalg.pinv(Lfh)
        K = Lfp @ Lb @ Lfp; K = (K+K.T)/2
        # Fisher(Y2)=Lf ; Fisher(Y1)=Lf^{1/2} K Lf^{1/2} should equal Lb
        covXY2 = np.linalg.inv(np.linalg.inv(Sx) + Lf)
        covXY1 = np.linalg.inv(np.linalg.inv(Sx) + Lfh @ K @ Lfh)
        wk = max(wk, np.linalg.norm(covXY2-Sf), np.linalg.norm(covXY1-Sb))
print(f"  d in 2,3 x 80: ||Cov(X|Y2)-Sf|| and ||Cov(X|Y1)-Sb||, worst = {wk:.1e}  (K-map exact for 2 stages)")
if worst > 1e-8 or wk > 1e-7: fail.append("achievability")

# =====================================================================================
print("="*76); print("[2] CONVERSE: no random admissible code beats the region boundary")
viol = 0; tested = 0
for d in (2, 3):
    Sx = spd(d); P1 = spd(d); P2 = spd(d)
    D1 = 0.6*np.trace(P1@Sx); D2 = 0.45*np.trace(P2@Sx)
    R1_D1 = 0.5*(logdet(Sx)-logdet(sigma_star(P1, D1, Sx)))     # single-stage floor obs 1
    R2_D2 = 0.5*(logdet(Sx)-logdet(sigma_star(P2, D2, Sx)))     # single-stage floor obs 2 (global min total)
    for _ in range(4000):
        m1 = rng.integers(1, d+1); m2 = rng.integers(1, d+1)
        M1 = rng.standard_normal((m1, d)); M2 = rng.standard_normal((m2, d))
        s1 = np.exp(rng.uniform(-1.,1.)); s2 = np.exp(rng.uniform(-1.,1.))
        Sb = post_cov(Sx, M1, s1*np.eye(m1))                    # Cov(X|Y1)  (base)
        Sf = post_cov(Sx, np.vstack([M1,M2]),
                      np.diag(np.r_[s1*np.ones(m1), s2*np.ones(m2)]))   # Cov(X|Y1,Y2)
        d1a = np.trace(P1@Sb); d2a = np.trace(P2@Sf)            # best-estimator distortions
        if d1a > D1+1e-9 or d2a > D2+1e-9: continue             # keep only admissible codes
        tested += 1
        R1a = 0.5*(logdet(Sx)-logdet(Sb)); Rta = 0.5*(logdet(Sx)-logdet(Sf))
        nest = mineig(Sb - Sf) >= -1e-7                         # total covariance => nesting (no Markov)
        c1 = R1a >= R1_D1 - 1e-7                                # base can't beat R1(D1)
        c2 = Rta >= R2_D2 - 1e-7                                # total can't beat R2(D2)
        c3 = Rta >= R1a - 1e-7                                  # increment R2>=0
        if not (nest and c1 and c2 and c3): viol += 1
print(f"  admissible random codes tested = {tested};  converse violations = {viol}")
if viol: fail.append(f"converse-violations={viol}")

# =====================================================================================
print("="*76); print("[3] CORNER = Thm5/Thm6 as min-sum-rate vertex (uniqueness enters here)")
Sx = np.eye(2); D1 = D2 = 0.25                                  # orthogonal observers
S1s = sigma_star(np.diag([1.,0.]), D1, Sx); S2s = sigma_star(np.diag([0.,1.]), D2, Sx)
So  = sigma_star(np.diag([0.,1.]), D2, S1s)
L   = 0.5*(logdet(S2s)-logdet(So)); nest_orth = mineig(S1s - S2s) >= -1e-6
print(f"  orthogonal: nested={nest_orth} (exp False)  L={L:.4f}  R1(D1)={0.5*np.log(1/D1):.4f}"
      f"  (L=R1(D1): {abs(L-0.5*np.log(1/D1))<1e-6})")
if not (not nest_orth and abs(L-0.5*np.log(1/D1))<1e-6): fail.append("corner-orthogonal")
n=3; Sx2=spd(n); P=spd(n); dA=0.6*np.trace(P@Sx2); dB=0.2*np.trace(P@Sx2)    # refinable (P1=P2)
S1r=sigma_star(P,dA,Sx2); S2r=sigma_star(P,dB,Sx2); Sor=sigma_star(P,dB,S1r)
Lr=0.5*(logdet(S2r)-logdet(Sor))
print(f"  refinable(P1=P2,D2<D1): nested={mineig(S1r-S2r)>=-1e-7} (exp True)  L={Lr:.2e} (exp 0)"
      f"  ||Sigma_o-Sig2*||={np.linalg.norm(Sor-S2r):.1e}")
if not (mineig(S1r-S2r)>=-1e-7 and abs(Lr)<1e-7 and np.linalg.norm(Sor-S2r)<1e-7): fail.append("corner-refinable")
okL=okiff=True
for _ in range(300):
    Sx3=spd(3); Pa=spd(3); Pb=spd(3)
    da=rng.uniform(0.2,0.8)*np.trace(Pa@Sx3); db=rng.uniform(0.1,0.8)*np.trace(Pb@Sx3)
    S1=sigma_star(Pa,da,Sx3); S2=sigma_star(Pb,db,Sx3); Soo=sigma_star(Pb,db,S1)
    LL=0.5*(logdet(S2)-logdet(Soo)); okL &= LL >= -1e-7
    okiff &= ((mineig(S1-S2)>=-1e-7) == (abs(LL)<1e-6))         # L=0 <=> Sig2*<=Sig1*
print(f"  300 random: L>=0 always={okL};  (L=0 <=> Sig2*<=Sig1*)={okiff}")
if not (okL and okiff): fail.append("corner-random")

# =====================================================================================
print("="*76); print("[4] k=3 NESTED CHAIN: nested-Gaussian channels reproduce the whole chain")
w3 = 0.0
for d in (2, 3):
    for _ in range(60):
        Sx=spd(d); P1=spd(d); P2=spd(d); P3=spd(d)
        D1=rng.uniform(0.4,0.85)*np.trace(P1@Sx); D2=rng.uniform(0.25,0.85)*np.trace(P2@Sx)
        D3=rng.uniform(0.10,0.85)*np.trace(P3@Sx)
        S1=sigma_star(P1,D1,Sx); S2=sigma_star(P2,D2,S1); S3=sigma_star(P3,D3,S2)   # nested by caps
        assert mineig(S1-S2)>=-1e-8 and mineig(S2-S3)>=-1e-8 and mineig(Sx-S1)>=-1e-8
        covs, rates = chain_realize(Sx, [S1,S2,S3])
        eb = max(np.linalg.norm(covs[0]-S1), np.linalg.norm(covs[1]-S2), np.linalg.norm(covs[2]-S3))
        rb = max(abs(rates[i]-0.5*(logdet(Sx)-logdet(S))) for i,S in enumerate([S1,S2,S3]))
        tr_ok = np.trace(P1@S1)<=D1+1e-9 and np.trace(P2@S2)<=D2+1e-9 and np.trace(P3@S3)<=D3+1e-9
        w3 = max(w3, eb, rb)
        if not (eb<1e-9 and rb<1e-10 and tr_ok): fail.append(f"k3 d={d} eb={eb:.1e} rb={rb:.1e}")
print(f"  d in 2,3 x 60: Cov(X|Y1..Yi)=Si (i=1,2,3), cumulative rates on boundary."
      f"  worst residual = {w3:.1e}")

print("="*76)
print("VERDICT:", "ALL PASS" if not fail else f"FAIL: {fail}")
