# Fresh-context symbolic verification of tit-cr-context.tex Secs IV, V, VII.
# Written independently from the manuscript text alone.
import sympy as sp

rho, tau, D, g, n, a, b = sp.symbols('rho tau D g n a b', real=True)
s = 1 + tau**2

fails = []
def check(name, cond):
    ok = bool(cond)
    print(("PASS" if ok else "FAIL"), name)
    if not ok: fails.append(name)

# ---------------- Sec IV scaffolding ----------------
SigT  = sp.Matrix([[1, rho],[rho, 1]])
SigTS = sp.Matrix([rho, 1])
SigTcS = sp.simplify(SigT - SigTS*SigTS.T/s)

check("Sigma_{T|S} entries (line ~660)",
      sp.simplify(SigTcS - sp.Matrix([[1-rho**2/s, rho*tau**2/s],
                                      [rho*tau**2/s, tau**2/s]])) == sp.zeros(2,2))
check("det Sigma_{T|S} = tau^2(1-rho^2)/s",
      sp.simplify(SigTcS.det() - tau**2*(1-rho**2)/s) == 0)

Q0 = a**2 + b**2 + 2*a*b*rho
Q1 = Q0 - (a*rho+b)**2/s
Q1_direct = (sp.Matrix([[a,b]])*SigTcS*sp.Matrix([a,b]))[0,0]
check("Q1 = A Sigma_{T|S} A^T = Q0-(a rho+b)^2/s (line ~669)",
      sp.simplify(Q1_direct - Q1) == 0)

h = (1-a)**2 - 2*(1-a)*b*rho + b**2
check("distortion identity h = 1-2(a+b rho)+Q0 (eq:distortion)",
      sp.simplify((1 - 2*(a+b*rho) + Q0) - h) == 0)

# full moment-level covariance of (Y,V,Yhat,S); Yhat = aY+bV+N', Cov(N',T)=0, Cov(N',S)=0
# order: T=(Y,V), then (Yhat,S)
M  = sp.Matrix([[Q0+n, a*rho+b],[a*rho+b, s]])
J  = sp.Matrix([[a+b*rho, rho],[a*rho+b, 1]])
check("det M = s(Q1+n) (line ~675)", sp.simplify(M.det() - s*(Q1+n)) == 0)

Sig_e = sp.simplify(SigT - J*M.inv()*J.T)
check("det Sigma_e = n det Sigma_{T|S}/(Q1+n) (eq:scalar-detid)",
      sp.simplify(Sig_e.det() - n*SigTcS.det()/(Q1+n)) == 0)
check("det Sigma_{T|S}/det Sigma_e = (Q1+n)/n",
      sp.simplify(SigTcS.det()/Sig_e.det() - (Q1+n)/n) == 0)

# full 4x4 det K = det Sigma_S det Sigma_{T|S} det Sigma_N  (Step 2 of lem:gauss, scalar case)
K = sp.Matrix([
 [1,       rho,     a+b*rho,  rho],
 [rho,     1,       a*rho+b,  1  ],
 [a+b*rho, a*rho+b, Q0+n,     a*rho+b],
 [rho,     1,       a*rho+b,  s  ]])
check("det K = s * det Sigma_{T|S} * n", sp.simplify(K.det() - s*SigTcS.det()*n) == 0)
check("det K = det M * det Sigma_e", sp.simplify(K.det() - M.det()*Sig_e.det()) == 0)

# rank-one determinant identity used in thm:region's rate identity
chat = SigT*sp.Matrix([a,b])
v = Q0 + n
Sig_e0 = sp.simplify(SigT - chat*chat.T/v)
check("det Sigma_e0 = det Sigma_T * n/(Q0+n) (thm:region rate identity)",
      sp.simplify(Sig_e0.det() - SigT.det()*n/(Q0+n)) == 0)
check("chat^T SigT^{-1} chat = Q0", sp.simplify((chat.T*SigT.inv()*chat)[0,0] - Q0) == 0)

# ---------------- thm:function: gradient identities ----------------
mu = (a*rho+b)/s
gi = {
 "d_a(Q0-h)=2":            sp.diff(Q0-h, a) - 2,
 "d_b(Q0-h)=2rho":         sp.diff(Q0-h, b) - 2*rho,
 "d_a(Q1-h)=2(1-rho*mu)":  sp.diff(Q1-h, a) - 2*(1-rho*mu),
 "d_b(Q1-h)=2(rho-mu)":    sp.diff(Q1-h, b) - 2*(rho-mu),
 "d_a h = 2(a+b rho-1)":   sp.diff(h, a) - 2*(a+b*rho-1),
 "d_b h = 2(a rho+b-rho)": sp.diff(h, b) - 2*(a*rho+b-rho),
}
for nm, e in gi.items():
    check("grad id " + nm, sp.simplify(e) == 0)

# ---------------- thm:function: stationary family and reduction to P(g) ----------------
k  = g*s - 1
muE = rho*(g-1)/k
aE  = 1 - sp.Rational(1,1)/g
bE  = muE/g
check("mu_c consistency: (aE rho + bE)/s == rho(g-1)/k",
      sp.simplify((aE*rho+bE)/s - muE) == 0)
# FOC eq:foc
check("FOC-1: a+b rho = 1-(1-rho mu)/g",
      sp.simplify(aE + bE*rho - (1 - (1-rho*muE)/g)) == 0)
check("FOC-2: a rho+b = rho-(rho-mu)/g",
      sp.simplify(aE*rho + bE - (rho - (rho-muE)/g)) == 0)

hE  = h.subs({a:aE, b:bE})
check("h at FOC = (1-2 rho mu + mu^2)/g^2 (eq:h-at-foc)",
      sp.simplify(hE - (1-2*rho*muE+muE**2)/g**2) == 0)
Q0E = Q0.subs({a:aE, b:bE})
check("Q0 at FOC = 1-2(1-rho mu)/g + h",
      sp.simplify(Q0E - (1 - 2*(1-rho*muE)/g + hE)) == 0)
Q1E = Q1.subs({a:aE, b:bE})
check("Q1 at FOC = 1-2(1-rho mu)/g + h - s mu^2",
      sp.simplify(Q1E - (1 - 2*(1-rho*muE)/g + hE - s*muE**2)) == 0)

P = D*s*g**2 - (D + s - rho**2)*g + (1 - rho**2)
expr = (g-1)*(D - hE) - Q1E     # active constraint + def of g  <=>  expr = 0
check("(g-1)(D-h)-Q1 == (g-1) P(g)/(g k)  [quadratic reduction]",
      sp.simplify(expr - (g-1)*P/(g*k)) == 0)

check("P(1) = (D-1) tau^2", sp.simplify(P.subs(g,1) - (D-1)*tau**2) == 0)
check("P(0) = 1-rho^2", sp.simplify(P.subs(g,0) - (1-rho**2)) == 0)

gstar = ((D+s-rho**2) + sp.sqrt((D+s-rho**2)**2 - 4*D*s*(1-rho**2)))/(2*D*s)
check("g* closed form satisfies P(g*)=0", sp.simplify(P.subs(g,gstar)) == 0)

# ---------------- cor:anchors ----------------
check("anchor rho=0: P=(Dg-1)(sg-1)",
      sp.simplify(P.subs(rho,0) - (D*g-1)*(s*g-1)) == 0)
check("anchor tau=0: P=(g-1)(Dg-(1-rho^2))",
      sp.simplify(P.subs(tau,0) - (g-1)*(D*g-(1-rho**2))) == 0)
check("anchor tau=0 discriminant = (D-(1-rho^2))^2",
      sp.simplify(((D+1-rho**2)**2 - 4*D*(1-rho**2)) - (D-(1-rho**2))**2) == 0)
check("anchor rho^2=1: P=g(Dsg-(D+tau^2))",
      sp.simplify(P.subs(rho,1) - g*(D*s*g-(D+tau**2))) == 0)
check("anchor rho^2=1 (rho=-1 too)",
      sp.simplify(P.subs(rho,-1) - g*(D*s*g-(D+tau**2))) == 0)
# Steinberg value at rho_YS^2 = 1/s
r2 = 1/s
check("Steinberg margin at r2=1/s equals (tau^2+D)/(sD)",
      sp.simplify((1 - r2 + r2*D)/D - (tau**2+D)/(s*D)) == 0)
# anchor (i) channel values
check("rho=0 channel: VarN=(1-D)^2/(1/D-1)=D(1-D)",
      sp.simplify((1-D)**2/(1/D-1) - D*(1-D)) == 0)

# ---------------- Sec VI single-read floor corollary (cites eq:Pg) ----------------
gf = (s - rho**2)/(D*s)
check("P(g_f) = -rho^2 tau^2 / s (thm:floor single-read corollary)",
      sp.simplify(P.subs(g, gf) + rho**2*tau**2/s) == 0)

# ---------------- thm:region FOC algebra ----------------
alpha, g0, g1 = sp.symbols('alpha gamma0 gamma1', real=True)
# derive eq:foc-a, eq:foc-b from the weighted objective symbolically:
# n treated as D-h; phi = alpha ln(Q0+n)+(1-alpha) ln(Q1+n) - ln n
nn = D - h
phi = alpha*sp.log(Q0+nn) + (1-alpha)*sp.log(Q1+nn) - sp.log(nn)
for x, name in [(a,'a'), (b,'b')]:
    dphi = sp.diff(phi, x)
    G0 = nn/(Q0+nn); G1 = nn/(Q1+nn)
    if x == a:
        claimed = (2/nn)*(alpha*G0 + (1-alpha)*G1*(1-rho*mu) + (a+b*rho-1))
    else:
        claimed = (2/nn)*(alpha*G0*rho + (1-alpha)*G1*(rho-mu) + (a*rho+b-rho))
    check(f"region FOC in {name} matches eq:foc-{name}",
          sp.simplify(dphi - claimed) == 0)

# two-level system consistency with the FOC (eliminations in the proof):
# subtract rho*foc_a from foc_b => b=(1-alpha) g1 mu ; then a = 1-alpha g0-(1-alpha) g1
focA = alpha*g0 + (1-alpha)*g1*(1-rho*mu) + (a+b*rho-1)
focB = alpha*g0*rho + (1-alpha)*g1*(rho-mu) + (a*rho+b-rho)
comb = sp.expand(focB - rho*focA)
check("focB - rho*focA = (1-rho^2)(b-(1-alpha) g1 mu)",
      sp.simplify(comb - (1-rho**2)*(b - (1-alpha)*g1*mu)) == 0)
# substitute b=(1-alpha) g1 mu_sym as free symbol relation, verify a-elimination:
mus = sp.symbols('mu_s', real=True)
focA2 = alpha*g0 + (1-alpha)*g1*(1-rho*mus) + (a + (1-alpha)*g1*mus*rho - 1)
check("focA with b=(1-a)g1 mu gives a = 1-alpha g0-(1-alpha) g1",
      sp.simplify(sp.solve(focA2, a)[0] - (1 - alpha*g0 - (1-alpha)*g1)) == 0)

# alpha=1 endpoint algebra: gamma0 = D
g0v = sp.symbols('g0v', positive=True)
aa = 1 - g0v
ee = sp.simplify(g0v*(1-g0v) - (D - g0v**2))   # n=gamma0*a combined with n=D-h
check("alpha=1 endpoint: gamma0=D", sp.simplify(sp.solve(ee, g0v)[0] - D) == 0)

# L(1) display in cor:misalign: b=0,a=1-D,n=D(1-D)
Q1_at = ((1-D)**2*(1-rho**2/s))
check("cor:misalign L(1) ratio = [(1-D)(1-rho^2/s)+D]/D",
      sp.simplify((Q1_at + D*(1-D))/(D*(1-D)) - ((1-D)*(1-rho**2/s)+D)/D) == 0)

# ---------------- prop:uniq determinant rewrites ----------------
c1, c2, c3, vv = sp.symbols('c1 c2 c3 v', real=True)
l1, l2, l3 = sp.symbols('l1 l2 l3', positive=True)
c = sp.Matrix([c1,c2,c3]); Lam = sp.diag(l1,l2,l3)
nO = vv - (c.T*c)[0,0]
sig = vv - (c.T*(sp.eye(3)-Lam)*c)[0,0]
check("det(I-cc^T/v) = n/v",
      sp.simplify((sp.eye(3)-c*c.T/vv).det() - nO/vv) == 0)
check("det(Lam - (Lam c)(Lam c)^T/sigma) = det(Lam) n/sigma",
      sp.simplify((Lam - (Lam*c)*(Lam*c).T/sig).det() - Lam.det()*nO/sig) == 0)
check("sigma = Q1+n  (v - c^T(I-Lam)c)",
      sp.simplify(sig - ((c.T*Lam*c)[0,0] + nO)) == 0)

# ---------------- thm:vector FOC algebra (symbolic, p=3) ----------------
y1, y2, y3 = sp.symbols('y1 y2 y3', real=True)
y0 = sp.Matrix([y1,y2,y3])
Q0v = (c.T*c)[0,0]; Q1v = (c.T*Lam*c)[0,0]; hv = ((y0-c).T*(y0-c))[0,0]
nv = D - hv
phiv = alpha*sp.log(Q0v+nv) + (1-alpha)*sp.log(Q1v+nv) - sp.log(nv)
grad = sp.Matrix([sp.diff(phiv, x) for x in (c1,c2,c3)])
G0 = nv/(Q0v+nv); G1 = nv/(Q1v+nv)
claimed = (2/nv)*(alpha*G0*y0 + (1-alpha)*G1*(Lam*c + (y0-c)) - (y0-c))
check("vector FOC matches displayed system (pre-collection)",
      sp.simplify(grad - claimed) == sp.zeros(3,1))
bracket = (1-(1-alpha)*g1)*sp.eye(3) + (1-alpha)*g1*Lam
rhs = (1 - alpha*g0 - (1-alpha)*g1)*y0
collected = alpha*g0*y0 + (1-alpha)*g1*(Lam*c) + (1-alpha)*g1*(y0-c) - (y0-c)
check("collection: FOC <=> bracket*c = rhs (eq:vecfoc)",
      sp.simplify(collected - (bracket*c - rhs)) == sp.zeros(3,1))

print()
print("FAILURES:", fails if fails else "none")
