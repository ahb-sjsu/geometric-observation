"""Checks added after the 2026-09-17 five-referee pass. Prints, from the closed
form, the numbers quoted in the sentence after Corollary cor:notmarginal for the
within-model pair (rho^2, tau^2) = (3/5, 1/5) and (3/4, 1/2), the reduced surd
of Table tab:notmarginal, and the corrected P(g_R) expression of Appendix C
(the Lu-Xu comparison), verified symbolically.

    python check_referee_pass.py
"""
import math
import sympy as sp


def gstar(r2, t2, D):
    s = 1 + t2
    g = sp.symbols("g")
    roots = sp.solve(sp.Eq(D * s * g**2 - (D + s - r2) * g + (1 - r2), 0), g)
    return sp.radsimp(max(roots, key=lambda x: float(x)))


def main():
    ok = True
    print("within-model pair, rho_YS^2 = 1/2 in both:")
    for inst in [(sp.Rational(3, 5), sp.Rational(1, 5)), (sp.Rational(3, 4), sp.Rational(1, 2))]:
        assert inst[0] / (1 + inst[1]) == sp.Rational(1, 2)
        for D in (sp.Rational(1, 10), sp.Rational(3, 10)):
            g = gstar(*inst, D)
            L = 0.5 * math.log2(float(g))
            print(f"  (rho^2, tau^2) = {inst}, D = {D}: g* = {g}  L = {L:.4f} bits")
    expect = {(sp.Rational(3, 5), sp.Rational(1, 10)): 1.1880, (sp.Rational(3, 5), sp.Rational(3, 10)): 0.4712,
              (sp.Rational(3, 4), sp.Rational(1, 10)): 1.2105, (sp.Rational(3, 4), sp.Rational(3, 10)): 0.5228}
    for (r2, D), want in expect.items():
        t2 = sp.Rational(1, 5) if r2 == sp.Rational(3, 5) else sp.Rational(1, 2)
        got = round(0.5 * math.log2(float(gstar(r2, t2, D))), 4)
        ok &= abs(got - want) < 5e-5
    # reduced surd
    g2 = gstar(sp.Rational(3, 4), sp.Rational(1, 2), sp.Rational(3, 10))
    ok &= sp.simplify(g2 - (7 + sp.sqrt(29)) / 6) == 0
    print("  (21+sqrt(261))/18 == (7+sqrt(29))/6:", sp.simplify(g2 - (7 + sp.sqrt(29)) / 6) == 0)
    # P(g_R) in the Lu-Xu comparison
    D, r2, t2 = sp.symbols("D rho2 tau2", positive=True)
    s = 1 + t2
    P = lambda g: D * s * g**2 - (D + s - r2) * g + (1 - r2)
    DV = 1 - r2 / (1 - D)
    gR = (1 - r2) * (t2 + DV) / (s * D * DV)
    stated = r2 * t2**2 * (1 - D) * (1 - r2) / (s * (1 - D - r2) ** 2)
    ok &= sp.simplify(P(gR) - stated) == 0
    print("  P(g_R) = rho^2 tau^4 (1-D)(1-rho^2) / (s (1-D-rho^2)^2):", sp.simplify(P(gR) - stated) == 0)
    print("all checks passed" if ok else "CHECK FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
