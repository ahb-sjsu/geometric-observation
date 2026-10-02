"""ot_boundary.py: the boundary of the two-observer flip, pre-registered in two stages (2026-10-02).

Theory (Gaussian model). The leakage of a quantized projection's index decreases in R2(Z; S), a Rayleigh quotient of
the pencil (Sigma_T - Sigma_{T|S}, Sigma_T). With slack, the aware code beats the principal code exactly when some
direction within the budget is more predictable from S than the principal read b_R. Classes of b_R in that pencil:
  top            -> no flip at any slack
  not-eigenvector -> flip with first-order onset (this is the misalignment condition of Theorem misalign)
  eigenvector    -> flip only at finite slack (second order), e.g. a view uncorrelated with b_R.
Stage "predict" uses training halves only and writes boundary_predictions.json (committed and pushed before
"measure" runs). Stage "measure" evaluates the same frozen directions on held-out halves with real 3-bit codes and
the best of three adversaries, with bootstrap standard errors.
Reuses the loaders and helpers of ot_figures/ot_figures.ipynb verbatim.
"""
import matplotlib; matplotlib.use("Agg")
import io, math, zipfile, urllib.request, warnings
import numpy as np, pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.linalg import eigh
from scipy.optimize import brentq
from sklearn.datasets import fetch_california_housing, load_diabetes
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import HistGradientBoostingClassifier
warnings.filterwarnings("ignore")
plt.rcParams.update({"font.family": "serif", "font.size": 10, "figure.dpi": 110, "savefig.dpi": 300})
LN2 = math.log(2)
rng = np.random.default_rng(20261001)
print("numpy", np.__version__, "| matplotlib", matplotlib.__version__)

def msqrt(M, inv=False):
    w, U = np.linalg.eigh(M); w = np.clip(w, 1e-300 if inv else 0, None)
    return U @ np.diag(w ** (-0.5 if inv else 0.5)) @ U.T

def Phi(A):   # reverse water-filling at level one on the spectrum of A (Theorem tilted)
    w, E = np.linalg.eigh(0.5 * (A + A.T))
    return E @ np.diag([1.0 if l <= 1 else 1.0 / l for l in w]) @ E.T

def costs(S, J, Se0):   # rate and leakage in bits (Proposition posterior)
    K = np.linalg.inv(np.linalg.inv(S) + J); Se = np.linalg.inv(np.linalg.inv(Se0) + J)
    ld = lambda M: np.linalg.slogdet(M)[1] / LN2
    return 0.5 * (ld(S) - ld(Se0)), 0.5 * (ld(K) - ld(Se))

def frontier_point(S, Q, H, SU, D, alpha, iters=400):   # Proposition mm: monotone water-filling iteration
    Sh = msqrt(S); Qt = Sh @ Q @ Sh; Ht = H @ Sh; X = np.eye(S.shape[0])
    for _ in range(iters):
        T = (1 - alpha) * Ht.T @ np.linalg.inv(Ht @ X @ Ht.T + SU) @ Ht
        nu = math.exp(brentq(lambda l: np.trace(Qt @ Phi(2 * math.exp(l) * Qt + T)) - D, -40, 40))
        Xn = Phi(2 * nu * Qt + T)
        if np.linalg.norm(Xn - X) < 1e-12: X = Xn; break
        X = Xn
    return Sh @ X @ Sh

def gstar(rho2, tau2, D):   # Corollary scalar
    s = 1 + tau2; a = D * s; b = -(D + s - rho2); c = 1 - rho2
    return (-b + math.sqrt(b * b - 4 * a * c)) / (2 * a)

def onedim_direction(S, Q, J, F, D):   # Theorem onedim: top generalized eigenvector of (A(Delta), K)
    K = np.linalg.inv(np.linalg.inv(S) + J); Delta = np.trace(Q @ S) - D
    w, V = eigh(S @ Q @ S - Delta * S, K); b = V[:, -1]
    e = F @ S @ b; return math.degrees(math.atan2(e[1], e[0])) % 180

def coupled():
    u = np.array([math.cos(math.radians(50)), math.sin(math.radians(50))])
    S = np.zeros((3, 3)); S[:2, :2] = np.diag([1.0, 0.4]); S[:2, 2] = S[2, :2] = 0.6 * u; S[2, 2] = 1.0
    F = np.zeros((2, 3)); F[:, :2] = np.eye(2); H = np.array([[0.0, 0.0, 1.0]]); SU = np.array([[0.05]])
    return S, F, F.T @ F, H, SU, H.T @ np.linalg.inv(SU) @ H

def _zip(url):
    return zipfile.ZipFile(io.BytesIO(urllib.request.urlopen(url, timeout=120).read()))

def pack(name, Y, V, S_cols, ycols, vcols):
    T = np.column_stack([Y, V]).astype(float); cols = list(ycols) + list(vcols); m = Y.shape[1] if Y.ndim > 1 else 1
    s_idx = [cols.index(c) for c in S_cols]
    # rank guard: drop context columns (never targets or the second party's columns) that are numerically dependent
    keep = list(range(T.shape[1])); Ts = (T - T.mean(0)) / T.std(0)
    for j in range(T.shape[1] - 1, m - 1, -1):
        if j in s_idx: continue
        trial = [k for k in keep if k != j]
        if np.linalg.matrix_rank(Ts[:, keep], tol=1e-8) == np.linalg.matrix_rank(Ts[:, trial], tol=1e-8):
            keep = trial
    T = T[:, keep]; cols = [cols[k] for k in keep]; s_idx = [cols.index(c) for c in S_cols]
    return dict(name=name, T=T, m=m, s_idx=s_idx, cols=cols)

def load_energy():
    z = _zip("https://archive.ics.uci.edu/static/public/242/energy+efficiency.zip")
    df = pd.read_excel(z.open([n for n in z.namelist() if n.endswith(".xlsx")][0])).dropna(axis=1, how="all").dropna()
    X = df.iloc[:, :8].to_numpy(float)
    V = np.delete(X, 1, axis=1)   # surface area = wall + 2 roof exactly
    return pack("Energy", df.iloc[:, 8:10].to_numpy(float), V, ["height", "glazing"], ["heating", "cooling"],
                ["compactness", "wall", "roof", "height", "orientation", "glazing", "glazing dist."])

def load_housing():
    d = fetch_california_housing(); X = d.data
    return pack("Housing", np.column_stack([d.target, X[:, 0]]), X[:, 1:], ["Latitude", "Longitude"],
                ["value", "income"], list(d.feature_names[1:]))

def load_parkinsons():
    df = pd.read_csv(_zip("https://archive.ics.uci.edu/static/public/189/parkinsons+telemonitoring.zip").open("parkinsons_updrs.data"))
    vcols = [c for c in df.columns if c not in ("subject#", "motor_UPDRS", "total_UPDRS")]
    return pack("Parkinsons", df[["motor_UPDRS", "total_UPDRS"]].to_numpy(float), df[vcols].to_numpy(float),
                ["age", "sex"], ["motor UPDRS", "total UPDRS"], vcols)

def load_bike():
    df = pd.read_csv(_zip("https://archive.ics.uci.edu/static/public/275/bike+sharing+dataset.zip").open("hour.csv"))
    vcols = ["season", "yr", "mnth", "hr", "holiday", "weekday", "workingday", "weathersit", "temp", "atemp", "hum", "windspeed"]
    return pack("Bike", df[["casual", "registered"]].to_numpy(float), df[vcols].to_numpy(float),
                ["season", "weathersit"], ["casual", "registered"], vcols)

def load_student():
    inner = zipfile.ZipFile(_zip("https://archive.ics.uci.edu/static/public/320/student+performance.zip").open("student.zip"))
    df = pd.read_csv(inner.open("student-por.csv"), sep=";")
    df["sex_F"] = (df["sex"] == "F").astype(float); df["urban"] = (df["address"] == "U").astype(float)
    vcols = ["age", "sex_F", "urban", "Medu", "Fedu", "traveltime", "studytime", "failures", "famrel", "freetime",
             "goout", "Dalc", "Walc", "health", "absences", "G1"]
    return pack("Student", df[["G2", "G3"]].to_numpy(float), df[vcols].to_numpy(float),
                ["age", "sex_F", "urban"], ["G2", "G3"], vcols)

def load_wine():
    df = pd.read_csv(_zip("https://archive.ics.uci.edu/static/public/186/wine+quality.zip").open("winequality-white.csv"), sep=";")
    vcols = [c for c in df.columns if c != "quality"]
    return pack("Wine", df[["quality"]].to_numpy(float), df[vcols].to_numpy(float), ["alcohol"], ["quality"], vcols)

def load_concrete():
    df = pd.read_excel(_zip("https://archive.ics.uci.edu/static/public/165/concrete+compressive+strength.zip").open("Concrete_Data.xls"))
    X = df.to_numpy(float); vcols = ["cement", "slag", "fly ash", "water", "superplasticizer", "coarse agg", "fine agg", "age"]
    return pack("Concrete", X[:, 8:9], X[:, :8], ["age"], ["strength"], vcols)

def load_diabetes_():
    d = load_diabetes()
    return pack("Diabetes", d.target[:, None], d.data, ["age", "sex", "bmi"], ["progression"], list(d.feature_names))

def load_abalone():
    df = pd.read_csv(_zip("https://archive.ics.uci.edu/static/public/1/abalone.zip").open("abalone.data"), header=None)
    df.columns = ["sex", "length", "diameter", "height", "whole", "shucked", "viscera", "shell", "rings"]
    df["male"] = (df["sex"] == "M").astype(float); df["female"] = (df["sex"] == "F").astype(float)   # infant is the base
    vcols = ["male", "female", "length", "diameter", "height", "whole", "shucked", "viscera", "shell"]
    return pack("Abalone", df[["rings"]].to_numpy(float), df[vcols].to_numpy(float), ["male", "female", "length"], ["rings"], vcols)

def load_autompg():
    raw = _zip("https://archive.ics.uci.edu/static/public/9/auto+mpg.zip").open("auto-mpg.data").read().decode()
    rows = [l.split('"')[0].split() for l in raw.strip().splitlines()]
    df = pd.DataFrame([r for r in rows if "?" not in r], columns=["mpg", "cylinders", "displacement", "horsepower",
                                                                 "weight", "acceleration", "year", "origin"]).astype(float)
    vcols = ["cylinders", "displacement", "horsepower", "weight", "acceleration", "year", "origin"]
    return pack("AutoMPG", df[["mpg"]].to_numpy(float), df[vcols].to_numpy(float), ["cylinders", "year"], ["mpg"], vcols)

ZOO = "https://raw.githubusercontent.com/ahb-sjsu/routing-silence-artifact/a5bb5a84811321dfa46ef1db4f1cc45da6c93ff9/results/"
def load_zoo():
    a = pd.read_csv(ZOO + "E6/zoo-resilience-atlas.csv"); e9 = pd.read_csv(ZOO + "E9/E9-summary.csv")
    sp = pd.read_csv(ZOO + "E6/zoo-consumer-spectrum.csv")
    df = a.merge(e9[["name", "rtt0"]], on="name").merge(sp[["name", "V_lat0"]], on="name")
    vcols = ["N", "E", "L", "lam_ht", "bridges", "density", "diameter", "rtt0", "V_lat0"]
    return pack("Zoo", df[["V1", "V2"]].to_numpy(float), df[vcols].to_numpy(float), ["N", "E"], ["V1", "V2"], vcols)

DATA = [f() for f in (load_energy, load_housing, load_parkinsons, load_bike, load_student, load_wine,
                      load_concrete, load_diabetes_, load_abalone, load_autompg, load_zoo)]
for d in DATA:
    print(f"{d['name']:10s} {d['T'].shape}  Y={d['cols'][:d['m']]}  S={[d['cols'][i] for i in d['s_idx']]}")

def lloyd_max(K, iters=500):
    c = norm.ppf((np.arange(K) + 0.5) / K)
    for _ in range(iters):
        a = np.concatenate([[-np.inf], (c[:-1] + c[1:]) / 2, [np.inf]])
        p = norm.cdf(a[1:]) - norm.cdf(a[:-1]); c = (norm.pdf(a[:-1]) - norm.pdf(a[1:])) / p
    return c
BITS = 3; CB = lloyd_max(2 ** BITS); BND = (CB[:-1] + CB[1:]) / 2
GAIN = float(np.sum((norm.cdf(np.r_[BND, np.inf]) - norm.cdf(np.r_[-np.inf, BND])) * CB ** 2))
TAU2 = 0.1

def prepare(d, seed=0):
    r = np.random.default_rng(seed); T = d["T"]; n = len(T); perm = r.permutation(n)
    tr, te = perm[: n // 2], perm[n // 2:]
    mu, sd = T[tr].mean(0), T[tr].std(0); sd[sd == 0] = 1; Ts = (T - mu) / sd
    Sig = np.cov(Ts[tr].T) + 1e-9 * np.eye(T.shape[1])
    return dict(Ts=Ts, tr=tr, te=te, Sig=Sig, rng=r)

def holder(P, s_idx):
    Ts = P["Ts"]; p = Ts.shape[1]
    H = np.zeros((len(s_idx), p)); H[np.arange(len(s_idx)), s_idx] = 1
    S = Ts[:, s_idx] + math.sqrt(TAU2) * P["rng"].normal(size=(len(Ts), len(s_idx)))
    return H, S

def encode(P, b, idx):
    z_tr = P["Ts"][P["tr"]] @ b; z = (P["Ts"][idx] @ b - z_tr.mean()) / z_tr.std()
    return np.searchsorted(BND, z)

ADVERSARIES = {"logistic": lambda: LogisticRegression(max_iter=3000),
               "knn": lambda: KNeighborsClassifier(n_neighbors=50),
               "boosting": lambda: HistGradientBoostingClassifier(max_iter=150, early_stopping=False)}

def leakage_bits(Mtr, Mte, S, P):
    best = math.inf
    for mk in ADVERSARIES.values():
        clf = mk().fit(S[P["tr"]], Mtr); Pr = clf.predict_proba(S[P["te"]]); cols = list(clf.classes_)
        pm = np.array([Pr[i, cols.index(k)] if k in cols else 1e-9 for i, k in enumerate(Mte)])
        best = min(best, float(-np.mean(np.log2(np.clip(pm, 1e-9, 1)))))
    return best

def evaluate(P, b, m, S=None, whole_from=0):
    Ts, tr, te = P["Ts"], P["tr"], P["te"]; K = 2 ** BITS
    Mtr, Mte = encode(P, b, tr), encode(P, b, te)
    means = np.array([Ts[tr][Mtr == k].mean(0) if (Mtr == k).any() else np.zeros(Ts.shape[1]) for k in range(K)])
    err = Ts[te] - means[Mte]
    out = dict(mseT=float(np.mean(np.sum(err[:, whole_from:] ** 2, 1))), distY=float(np.mean(np.sum(err[:, :m] ** 2, 1))))
    pk = np.bincount(Mte, minlength=K) / len(te); out["HM"] = float(-np.sum(pk[pk > 0] * np.log2(pk[pk > 0])))
    if S is not None: out["leak"] = leakage_bits(Mtr, Mte, S, P)
    return out

def consumer_read(Sig, m):
    p = Sig.shape[0]; F = np.zeros((m, p)); F[:, :m] = np.eye(m); Q = F.T @ F
    return F, Q, eigh(Sig @ Q @ Sig, Sig)[1][:, -1]

# ----------------------------------------------------------------------------------------------------------
# The boundary of the two-observer flip (Flip B). Stage "predict" uses training halves only and writes
# boundary_predictions.json; stage "measure" reads it and measures the same codes on the held-out halves.
# ----------------------------------------------------------------------------------------------------------
import json, sys, argparse

FRACS = (0.05, 0.15, 0.4)
MIX_PHIS = (5, 15, 30, 60)
GH_X, GH_W = np.polynomial.hermite_e.hermegauss(80)

def h_gauss(R2):
    """Gaussian-model leakage H(q(Z)|S) in bits of the 3-bit index of a standardized projection Z whose squared
    multiple correlation with the second party's view is R2 (E[Z|S] ~ N(0, R2), Var(Z|S) = 1 - R2)."""
    a = np.concatenate([[-np.inf], BND, [np.inf]]); sz = math.sqrt(max(1 - R2, 1e-12)); r = math.sqrt(max(R2, 0.0))
    H = 0.0
    for x, w in zip(GH_X, GH_W):
        q = norm.cdf((a[1:] - r * x) / sz) - norm.cdf((a[:-1] - r * x) / sz); q = q[q > 1e-300]
        H += w * float(-np.sum(q * np.log2(q)))
    return H / math.sqrt(2 * math.pi)

def rayleigh(M, Sig, b): return float(b @ M @ b) / float(b @ Sig @ b)

def top_gen(M, Sig):
    w, V = eigh(0.5 * (M + M.T), Sig); return w[-1], V[:, -1]

def exact_aware(AS, B, Sig, need):
    """Maximize R2(b) = b'AS b / b'Sig b subject to b'B b / b'Sig b >= need (one-parameter generalized eigenproblem)."""
    lam_top, b0 = top_gen(AS, Sig)
    if rayleigh(B, Sig, b0) >= need: return b0
    lo, hi = 0.0, 1.0
    while rayleigh(B, Sig, top_gen(AS + hi * B, Sig)[1]) < need: hi *= 2
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if rayleigh(B, Sig, top_gen(AS + mid * B, Sig)[1]) < need: lo = mid
        else: hi = mid
    return top_gen(AS + hi * B, Sig)[1]

def views_for(d):
    p = d["T"].shape[1]; out = []
    for j in range(d["m"], p):
        row = np.zeros(p); row[j] = 1.0; out.append((d["cols"][j], row[None, :]))
    out.append(("principal-copy", None))     # filled per split: a noisy copy of the decoder's principal read
    for phi in MIX_PHIS:                      # crosses the boundary: rotate the view away from the principal read
        out.append((f"mix{phi}", ("mix", phi)))
    return out

def synth(name, Sig, m, n, seed):
    r = np.random.default_rng(seed); T = r.multivariate_normal(np.zeros(len(Sig)), Sig, size=n)
    cols = [f"y{i}" for i in range(m)] + [f"v{i}" for i in range(len(Sig) - m)]
    return dict(name=name, T=T, m=m, s_idx=[], cols=cols)

def synthetic_sets():
    u = np.array([math.cos(math.radians(50)), math.sin(math.radians(50))])
    S1 = np.zeros((3, 3)); S1[:2, :2] = np.diag([1.0, 0.4]); S1[:2, 2] = S1[2, :2] = 0.6 * u; S1[2, 2] = 1.0
    r = np.random.default_rng(99); G = r.normal(size=(8, 8)); S2 = G @ G.T / 8 + 0.3 * np.eye(8)
    return [synth("GaussCoupled", S1, 2, 20000, 1), synth("Gauss8", S2, 2, 20000, 2)]

def setup(d, view_rows):
    P = prepare(d); Sig = P["Sig"]; m = d["m"]; p = Sig.shape[0]
    F = np.zeros((m, p)); F[:, :m] = np.eye(m); B = Sig @ F.T @ F @ Sig
    b_R = eigh(B, Sig)[1][:, -1]
    zR = b_R / math.sqrt(b_R @ Sig @ b_R)
    if view_rows is None:
        Hm = zR[None, :]
    elif isinstance(view_rows, tuple):
        # S = cos(phi) Z_R + sin(phi) X_j, X_j the context column least correlated with Z_R (training covariance)
        phi = math.radians(view_rows[1]); ctx = list(range(m, p))
        corr = [abs(float(zR @ Sig[:, j]) / math.sqrt(Sig[j, j])) for j in ctx]; j = ctx[int(np.argmin(corr))]
        e = np.zeros(p); e[j] = 1.0 / math.sqrt(Sig[j, j]); Hm = (math.cos(phi) * zR + math.sin(phi) * e)[None, :]
    else:
        Hm = view_rows
    SS = Hm @ Sig @ Hm.T + TAU2 * np.eye(Hm.shape[0]); AS = Sig @ Hm.T @ np.linalg.inv(SS) @ Hm @ Sig
    return P, Sig, m, F, B, b_R, Hm, AS

def predict(out_path):
    rows = []
    for d in DATA + synthetic_sets():
        for vname, vrows in views_for(d):
            P, Sig, m, F, B, b_R, Hm, AS = setup(d, vrows)
            w, V = eigh(AS, Sig); R2max = float(w[-1]); R2R = rayleigh(AS, Sig, b_R)
            resid = AS @ b_R - R2R * (Sig @ b_R)
            mis = float(np.linalg.norm(resid) / max(np.linalg.norm(AS @ b_R), 1e-15))
            is_top = (R2max - R2R) < 1e-9
            cls = "top" if is_top else ("eigenvector" if mis < 1e-6 else "not-eigenvector")
            trY = float(np.trace(F @ Sig @ F.T)); DR = trY - GAIN * rayleigh(B, Sig, b_R)
            for f in FRACS:
                D0 = DR + f * (trY - DR); need = (trY - D0) / GAIN
                b_aw = exact_aware(AS, B, Sig, need); R2aw = rayleigh(AS, Sig, b_aw)
                rows.append(dict(dataset=d["name"], view=vname, f=f, cls=cls, R2_principal=R2R, R2_max=R2max,
                                 misalignment=mis, R2_aware=R2aw, pred_removed=h_gauss(R2R) - h_gauss(R2aw),
                                 b_aware=[float(x) for x in b_aw]))
        print(d["name"], "done", flush=True)
    criteria = {
        "C1": "Among cases with predicted removal >= 0.10 bit: measured removal > 0 in at least 80 percent, and the "
              "Spearman correlation of predicted and measured removal over all cases is at least 0.6.",
        "C2": "Among cases with predicted removal < 0.05 bit, excluding the principal-copy views: |measured removal| <= 2 bootstrap "
              "standard errors in at least 80 percent.",
        "consistency": "Principal-copy views (the second party sees a noisy copy of the decoder's principal read) are the top "
                       "class; the exact aware direction equals the principal read, so their measured removal is zero by "
                       "construction. Reported, not counted.",
        "C3": "Synthetic Gaussian sources (GaussCoupled, Gauss8): measured within 2 standard errors of predicted in at least 80 percent.",
        "C4": "Wine and Zoo are reported separately against the same predictions.",
        "C5": "Within the mix families (phi = 5, 15, 30, 60 degrees), measured removal tracks predicted removal: Spearman "
              "correlation of predicted and measured removal over all mix cases at least 0.6.",
        "amended_before_measurement": "C2 threshold raised from 0.02 to 0.05 bit and C5 changed from monotone-in-phi to "
              "tracks-prediction after inspecting the training-half predictions only (0.02 admitted 3 cases; the theory "
              "predicts removal non-monotone in phi at small slack). No outcome had been measured."}
    json.dump(dict(fracs=FRACS, tau2=TAU2, bits=BITS, criteria=criteria, rows=rows), open(out_path, "w"), indent=1)
    print("wrote", out_path, len(rows), "cases")

def leak_with_se(Mtr, Mte, S, P, nboot=200):
    best = (math.inf, None)
    for mk in ADVERSARIES.values():
        clf = mk().fit(S[P["tr"]], Mtr); Pr = clf.predict_proba(S[P["te"]]); cols = list(clf.classes_)
        pm = np.array([Pr[i, cols.index(k)] if k in cols else 1e-9 for i, k in enumerate(Mte)])
        ll = -np.log2(np.clip(pm, 1e-9, 1))
        if ll.mean() < best[0]: best = (float(ll.mean()), ll)
    r = np.random.default_rng(0); n = len(best[1])
    se = float(np.std([best[1][r.integers(0, n, n)].mean() for _ in range(nboot)]))
    return best[0], se

def measure(pred_path, out_path):
    pred = json.load(open(pred_path)); results = []
    sets = {d["name"]: d for d in DATA + synthetic_sets()}
    cache = {}
    for row in pred["rows"]:
        d = sets[row["dataset"]]; vrows = dict(views_for(d))[row["view"]]
        P, Sig, m, F, B, b_R, Hm, AS = setup(d, vrows)
        S = P["Ts"] @ Hm.T + math.sqrt(TAU2) * np.random.default_rng(5).normal(size=(len(P["Ts"]), Hm.shape[0]))
        key = (row["dataset"], row["view"])
        if key not in cache:
            Mtr, Mte = encode(P, b_R, P["tr"]), encode(P, b_R, P["te"]); cache[key] = leak_with_se(Mtr, Mte, S, P)
        lR, seR = cache[key]
        b = np.array(row["b_aware"]); Mtr, Mte = encode(P, b, P["tr"]), encode(P, b, P["te"])
        lA, seA = leak_with_se(Mtr, Mte, S, P)
        results.append(dict(row, measured_removed=lR - lA, se=math.sqrt(seR ** 2 + seA ** 2), leak_principal=lR, leak_aware=lA))
        print(f"{row['dataset']:12s} {row['view']:>16s} f={row['f']:.2f} {row['cls']:>15s} pred {row['pred_removed']:+.3f}  "
              f"meas {lR - lA:+.3f} +- {math.sqrt(seR**2+seA**2):.3f}", flush=True)
    json.dump(results, open(out_path, "w"), indent=1); print("wrote", out_path)

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("stage", choices=["predict", "measure"])
    ap.add_argument("--pred", default="boundary_predictions.json"); ap.add_argument("--out", default="boundary_measured.json")
    a = ap.parse_args()
    predict(a.pred) if a.stage == "predict" else measure(a.pred, a.out)
