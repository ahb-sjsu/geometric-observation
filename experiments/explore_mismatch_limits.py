# Exploring the LIMITS of Appendix E (the misidentified-observer theory), driven by NEG-13:
# the omission floor holds in the READ METRIC tr(P Sigma_delta) but did not become a downstream
# softmax-KL floor on Llama. This CPU experiment maps WHEN the read-metric floor transfers to a
# downstream floor, on controlled synthetic softmax consumers where the ground truth is known.
#
#   Knob A (omitted downstream weight w_out): fraction of the consumer's read energy the coder OMITS.
#   Knob B (rate / water level): how far below the floor we push the coded directions.
#
# Predictions under test (my hypotheses):
#   H1  The downstream floor EXISTS (asymptotic misidentified KL > 0, correct KL -> 0) whenever w_out>0.
#   H2  It is OPERATIVE (KL stops improving) only at high rate AND large w_out; at small w_out the
#       reducible read-mode error dominates and KL keeps improving (the NEG-13 regime).
#   H3  At small error scale (high-resolution) the downstream metric tracks tr(P Sigma_delta), so the
#       floor binds; at large error scale the softmax saturates and departs from the quadratic metric.
# Pure numpy. MIT License.
from __future__ import annotations
import numpy as np

def _softmax(z):
    z = z - z.max(-1, keepdims=True); e = np.exp(z); return e/e.sum(-1,keepdims=True)

def _sqrtm(M):
    w,U = np.linalg.eigh((M+M.T)/2); w=np.clip(w,0,None); return U@np.diag(np.sqrt(w))@U.T

def softmax_kl(K, Kq, Q, d):
    p=_softmax(Q@K.T/np.sqrt(d)); q=_softmax(Q@Kq.T/np.sqrt(d))
    return float((p*np.log((p+1e-12)/(q+1e-12))).sum(-1).mean())

def wf_sigma(P_read, Sx, theta):
    """water-fill error cov for P_read at level theta, capped by Sx; returns (Sigma, rate_nats)."""
    Sh=_sqrtm(Sx); p,V=np.linalg.eigh((Sh@P_read@Sh+ (Sh@P_read@Sh).T)/2); p=np.clip(p,0,None)
    s=np.where(p>1e-12, np.minimum(1.0, theta/np.maximum(p,1e-300)), 1.0)
    Sig=Sh@(V@np.diag(s)@V.T)@Sh
    rate=0.5*float(np.sum(np.log(p[p>theta]/theta))) if (p>theta).any() else 0.0
    return (Sig+Sig.T)/2, rate

def build_consumer(d, r_read, w_out_frac, scale, rng):
    """A softmax consumer whose read operator P = Q^T Q has r_read strong directions; one of them
    carries a w_out_frac share of the read energy and will be the OMITTED direction. Returns
    P (true, full), the true read basis, and a query set Q realizing it. 'scale' sets |Q| (SNR)."""
    U = np.linalg.qr(rng.standard_normal((d,d)))[0]
    lam = np.zeros(d);
    # r_read read weights; direction 0 gets w_out_frac of the total, rest split the remainder
    base = np.linspace(1.0, 0.3, r_read)
    base = base/base.sum()*(1-w_out_frac); base[0]=w_out_frac
    lam[:r_read] = base * (r_read)      # scale up so energies are O(1)
    Q = (rng.standard_normal((96, d)) * np.sqrt(np.maximum(lam,0))) @ U.T * scale
    P = Q.T@Q/Q.shape[0]
    return P, U[:, :r_read], U[:, :1], Q  # P, read-subspace, the omitted dir (col 0), Q

def run():
    rng = np.random.default_rng(0)
    d, r_read = 24, 6
    Sx = None  # set per instance
    print("="*96)
    print("Knob sweep: omitted downstream-weight fraction w_out x error scale; read-metric floor vs softmax-KL floor")
    print("="*96)
    print(f"{'w_out':>6} {'scale':>6} | {'readD@hi/floor':>15} {'KL@mid':>8} {'KL@hi':>8} {'KL_asym':>8} "
          f"{'KLcorr_asym':>11} | {'read floors':>11} {'KL floors':>9} {'KL floor>0':>10}")
    for w_out in (0.15, 0.35, 0.6, 0.85):
        for scale in (0.3, 1.0, 2.5):
            rng2 = np.random.default_rng(hash((int(w_out*100),int(scale*100))) % (2**31))
            K = rng2.standard_normal((256, d))
            P, Vread, vout, Q = build_consumer(d, r_read, w_out, scale, rng2)
            Sx = np.cov(K, rowvar=False) + 1e-6*np.eye(d)
            # MISIDENTIFIED operator: reads the r_read subspace EXCEPT the omitted top direction
            Vhat = Vread[:, 1:]                      # omits column 0 (the w_out-weighted dir)
            P_hat = Vhat @ Vhat.T                    # rank r_read-1 projector (the coder's read subspace)
            # floor (read metric): tr(P~ Pi), Pi = whitened kernel of P_hat
            Sh=_sqrtm(Sx); Pht=Sh@P_hat@Sh; w,Vk=np.linalg.eigh((Pht+Pht.T)/2)
            Pi = Vk[:, w<=1e-9*max(w.max(),1)] @ Vk[:, w<=1e-9*max(w.max(),1)].T
            D_floor = float(np.trace((Sh@P@Sh)@Pi))
            # rate sweep for the misidentified coder
            pmax=float(np.clip(np.linalg.eigvalsh(Sh@P_hat@Sh),0,None).max() or 1.0)
            thetas=pmax*np.geomspace(0.5, 1e-5, 12)
            reads=[]; kls=[]
            for th in thetas:
                Sig,_=wf_sigma(P_hat, Sx, th); Ss=_sqrtm(Sig)
                reads.append(float(np.trace(P@Sig)))
                kls.append(np.mean([softmax_kl(K, K+rng2.standard_normal(K.shape)@Ss.T, Q, d) for _ in range(3)]))
            # asymptotic (infinite rate): error confined to the floor covariance Sh Pi Sh
            Sig_asym = Sh@Pi@Sh; Ss=_sqrtm(Sig_asym)
            kl_asym=np.mean([softmax_kl(K, K+rng2.standard_normal(K.shape)@Ss.T, Q, d) for _ in range(6)])
            # correct-operator asymptotic (reads all of P's subspace): error -> 0 in read subspace
            Sig_corr,_=wf_sigma(P, Sx, pmax*1e-5); Ss=_sqrtm(Sig_corr)
            kl_corr_asym=np.mean([softmax_kl(K, K+rng2.standard_normal(K.shape)@Ss.T, Q, d) for _ in range(6)])
            read_floors = abs(reads[-1]-D_floor) <= 0.5*max(D_floor,1e-9)
            kl_mid, kl_hi = kls[len(kls)//2], kls[-1]
            kl_improve = (kl_mid-kl_hi)/(kl_mid+1e-12)
            kl_floors = kl_improve < 0.20
            kl_floor_positive = kl_asym > 3*kl_corr_asym and kl_asym > 1e-4
            print(f"{w_out:>6.2f} {scale:>6.2f} | {reads[-1]/max(D_floor,1e-9):>14.2f}x {kl_mid:>8.1e} {kl_hi:>8.1e} "
                  f"{kl_asym:>8.1e} {kl_corr_asym:>11.1e} | {str(read_floors):>11} {str(kl_floors):>9} {str(kl_floor_positive):>10}")
    print("="*96)
    print("Reading: 'read floors'=read metric hit tr(P~Pi); 'KL floors'=softmax-KL stopped improving (<20%) in swept range;")
    print("         'KL floor>0'=asymptotic misidentified KL exceeds correct-operator asymptotic (a genuine downstream floor exists).")

if __name__ == "__main__":
    run()
