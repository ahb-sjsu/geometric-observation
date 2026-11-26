"""Figures for Chapters 12 to 16, 18 to 20, 22, 23 and Appendices B and G (2026-11-25).

Every measured number drawn here is printed in the chapter the figure belongs to, and the
caption carries the class the chapter gives it. Schematics restate structure the text
describes and say that they are schematics where they could be taken for data.
"""

import math

from figkit import BORDER, BOX, CRITICAL, GRID, INK, INK2, INK3, SERIES, SURFACE, Axes, Canvas, legend, reg


def _bracket(c, x1, x2, y, label, above=True, color=INK2, size=11):
    """A horizontal span with end ticks and a centred label."""
    c.line(x1, y, x2, y, color, 1.5)
    c.line(x1, y - 6, x1, y + 6, color, 1.5)
    c.line(x2, y - 6, x2, y + 6, color, 1.5)
    c.text((x1 + x2) / 2, y - 9 if above else y + 18, label, size, "middle", color)


def _hollow(c, x, y, w, h, stroke):
    """An outlined bar: a value that is drawn only as a claim, not as a measurement."""
    c.add(f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" fill="none" stroke="{stroke}" '
          f'stroke-width="1.5" stroke-dasharray="5 4"/>')


# ------------------------------------------------------------------ chapter 12
def fig_12_1():
    lam = (0.9, 0.1)

    def kappa(deg):
        a = math.radians(deg)
        return lam[0] * math.cos(a) ** 2 + lam[1] * math.sin(a) ** 2

    assert abs(kappa(0) - 0.9) < 1e-12 and abs(kappa(45) - 0.5) < 1e-12 and abs(kappa(90) - 0.1) < 1e-12
    p = reg("chapters/ch12_failure_taxonomy_and_kappa.md", "12.1",
            "The alignment κ = tr(P Σ) in two dimensions, as an illustration of the definition and not a measurement. "
            "The source has variances 0.9 and 0.1 (unit trace) and the consumer reads one direction (a rank-one read "
            "metric of unit trace) at angle φ to the high-energy axis, so κ = 0.9 cos²φ + 0.1 sin²φ. Left: the "
            "one-standard-deviation contour of the source and three read directions. Right: κ against φ. A consumer "
            "that reads the high-energy axis has κ = 0.9, the coupling end, where reconstruction-optimal coding "
            "already protects what is read. A consumer that reads the quiet axis has κ = 0.1, the end where the "
            "chapter places the flip. The figure does not draw the flip magnitude, which the chapter reports only as "
            "a retrospective [exploratory] fit and one sealed [predicted] point.",
            "## Two axes, not one")
    c = Canvas(720, 400, "The alignment κ: how much energy lies where the consumer reads")
    cx, cy, s = 180, 220, 140
    c.line(cx - 160, cy, cx + 160, cy, GRID, 1)
    c.line(cx, cy - 150, cx, cy + 150, GRID, 1)
    c.ellipse(cx, cy, s * math.sqrt(lam[0]), s * math.sqrt(lam[1]), 0, INK3, INK3, 1.5, 0.10,
              title="source, variances 0.9 and 0.1")
    c.text(cx - 128, cy + 62, "source energy", 11, "start", INK3, italic=True)
    marks = [(0, SERIES[0]), (45, SERIES[1]), (90, SERIES[2])]
    for deg, col in marks:
        a = math.radians(deg)
        x2, y2 = cx + 140 * math.cos(a), cy - 140 * math.sin(a)
        c.arrow(cx, cy, x2, y2, col, 2.5)
    c.text(cx + 146, cy - 10, "φ = 0°", 11.5, "start", INK)
    c.text(cx + 146, cy + 6, "κ = 0.9", 11.5, "start", INK2)
    c.text(cx + 108, cy - 112, "φ = 45°", 11.5, "start", INK)
    c.text(cx + 108, cy - 96, "κ = 0.5", 11.5, "start", INK2)
    c.text(cx + 10, cy - 142, "φ = 90°", 11.5, "start", INK)
    c.text(cx + 10, cy - 126, "κ = 0.1", 11.5, "start", INK2)
    c.text(cx - 160, 384, "read directions drawn as arrows", 10.5, "start", INK3, italic=True)
    ax = Axes(c, 450, 70, 230, 250, (0, 90), (0, 1), [0, 30, 60, 90], [0, 0.25, 0.5, 0.75, 1],
              "angle φ between read direction and energy, degrees", "alignment κ")
    c.polyline([(ax.X(d), ax.Y(kappa(d))) for d in range(0, 91)], INK2, 2, title="κ = 0.9 cos²φ + 0.1 sin²φ")
    for deg, col in marks:
        c.dot(ax.X(deg), ax.Y(kappa(deg)), col, 5, title=f"φ = {deg}°, κ = {kappa(deg):.1f}")
    c.text(ax.X(8), ax.Y(0.9) - 12, "coupling end: no flip", 10.5, "start", INK2, italic=True)
    c.text(ax.X(86), ax.Y(0.1) + 22, "misaligned end: flip regime", 10.5, "end", INK2, italic=True)
    c.save(p)


# ------------------------------------------------------------------ chapter 13
def fig_13_1():
    groups = [
        ("D1 radar, electromagnetic", "partial: registered miss", [(25, 25), (25, 25), None]),
        ("D2 AV16.3, acoustic, n = 201", "confirmed", [(148, 201), (201, 201), (152, 201)]),
        ("D3 PDAR, elastic, n = 17", "confirmed", [(13, 17), (17, 17), (13, 17)]),
    ]
    assert round(100 * 148 / 201) == 74 and round(100 * 13 / 17) == 76
    d1_anti, d1_bar = 0.60, 0.70
    p = reg("chapters/ch13_the_domain_generality_sweep.md", "13.1",
            "The three criteria of a flip on held-out data, in three wave physics (registration GO-P-2026-034). Bars "
            "are fractions of held-out cases: the read-preserving arm wins downstream (flip), the "
            "reconstruction-optimal arm reconstructs better (the trade), and the arm with the read direction destroyed "
            "is worst (the control). D2 and D3 are [demonstrated] on disjoint held-out recordings and events. D1 is "
            "[predicted → partial, registered miss]: its control is 60% against a sealed bar of 70%, and its split is "
            "within one recording because the disjoint set could not be downloaded. The sealed bar is drawn for D1 "
            "only, since that is the one the chapter prints.",
            "## The non-physical confirmations")
    c = Canvas(720, 400, "The flip in three wave physics: two confirmed, one partial")
    ax = Axes(c, 70, 62, 620, 250, (0, 3), (0, 1.12), [], [0, 0.25, 0.5, 0.75, 1], "", "fraction of held-out cases")
    names = ["flip", "reconstruction trade", "anti control"]
    for i, (name, verdict, vals) in enumerate(groups):
        cx = ax.X(i + 0.5)
        for j, v in enumerate(vals):
            x = cx - 69 + 46 * j + 11
            if v is None:
                frac, lab = d1_anti, "60%"
            else:
                frac, lab = v[0] / v[1], f"{v[0]}/{v[1]}"
            c.rect(x, ax.Y(frac), 24, ax.Y(0) - ax.Y(frac), SERIES[j], 4, title=f"{name}: {names[j]} {lab}")
            c.text(x + 12, ax.Y(frac) - 6, lab, 10.5, "middle", INK)
            if v is None:
                yb = ax.Y(d1_bar)
                c.line(x - 8, yb, x + 32, yb, INK, 1.5, dash="4 3")
                c.text(x + 37, yb + 4, "sealed 70%", 10.5, "start", INK)
        c.text(cx, ax.Y(0) + 17, name, 11, "middle", INK2)
        c.text(cx, ax.Y(0) + 33, verdict, 11, "middle", INK, "600")
    legend(c, 70, 46, [(n, SERIES[j]) for j, n in enumerate(names)])
    c.text(16, 390, "D1: 25 held-out frames of one recording; its anti control is printed as a percentage only", 10.5,
           "start", INK3, italic=True)
    c.save(p)


# ------------------------------------------------------------------ chapter 14
def fig_14_1():
    p = reg("chapters/ch14_the_falsifiable_core.md", "14.1",
            "A schematic of the six class tags and the two promotions the chapter states. The top row is ordered by "
            "how much each class demands. An [exploratory] finding reaches [demonstrated] only through a fresh sealed "
            "prereg and a run on held-out data (rule R-IND-6), never by a replay of the set it was first seen on. "
            "[proved] needs three things together. [refuted] is a bet lost, and it stays in print. The diagram "
            "restates the definitions; it reports no result.",
            "## The six")
    c = Canvas(720, 420, "How a claim earns its class")
    c.text(30, 66, "ordered by how much each class demands", 11, "start", INK3, italic=True)
    c.arrow(250, 62, 690, 62, INK3, 1)
    c.box(30, 84, 180, 56, "[predicted]", "sealed, gate stated")
    c.box(270, 84, 180, 56, "[demonstrated]", "passed its bar, governed run")
    c.box(510, 84, 180, 56, "[replicated]", "second independent instance")
    c.arrow(210, 112, 268, 112, INK2, 1.5)
    c.arrow(450, 112, 508, 112, INK2, 1.5)
    c.text(480, 160, "reproduced", 10.5, "middle", INK2, italic=True)
    c.box(30, 250, 180, 56, "[exploratory]", "numerical check only")
    c.text(120, 326, "may not support an umbrella claim", 10.5, "middle", INK2, italic=True)
    c.arrow(210, 262, 328, 144, INK2, 1.5)
    c.text(290, 200, "R-IND-6: a fresh sealed prereg", 11, "start", INK)
    c.text(290, 216, "and a run on held-out data", 11, "start", INK)
    c.box(510, 250, 180, 56, "[proved]", "all three of:")
    for k, s in enumerate(("a written proof", "a committed falsification harness", "a fresh-context re-derivation")):
        c.text(600, 326 + 16 * k, s, 10.5, "middle", INK2)
    c.box(270, 320, 180, 56, "[refuted]", "a bet lost, kept in print")
    c.save(p)


# ------------------------------------------------------------------ chapter 15
def fig_15_1():
    p = reg("chapters/ch15_registration_first.md", "15.1",
            "A schematic of seal before measure. The prereg, with its pass/fail bar, is hashed and committed to git, "
            "and that commit is the binding timestamp (REG-1). The sealed state is anchored outside the repository in "
            "a DOI deposit (REG-3). Only then is the first governed measurement made, so the bar is written before the "
            "number that has to clear it is known. A missed bar stays a miss. Later corrections are appended after "
            "the sealed text as dated amendments (REG-2). Spacing along the time axis is not to scale.",
            "## Independent verification: the R-IND rules")
    c = Canvas(720, 400, "Seal before measure: the bar is fixed before the number exists")
    y = 220
    c.arrow(40, y, 690, y, INK3, 1.5)
    c.text(690, y + 18, "time", 10.5, "end", INK3, italic=True)
    xs = {"draft": 100, "seal": 250, "doi": 370, "run": 490, "out": 620}
    c.line(xs["seal"], 134, xs["seal"], 300, CRITICAL, 1.5, dash="5 4")
    c.text(40, 66, "no governed number exists yet", 10.5, "start", INK3, italic=True)
    c.text(690, 66, "measured only after the seal commit exists", 10.5, "end", INK3, italic=True)
    for k in ("draft", "doi", "run", "out"):
        c.dot(xs[k], y, SERIES[0], 5)
    c.dot(xs["seal"], y, CRITICAL, 6, title="seal: hash and git commit")
    c.text(40, 158, "prereg written", 12, "start", INK, "600")
    c.text(40, 174, "claim, arms, sample size,", 10.5, "start", INK2)
    c.text(40, 190, "pass/fail bar", 10.5, "start", INK2)
    c.text(xs["seal"], 108, "hashed and git-committed", 12, "middle", INK, "600")
    c.text(xs["seal"], 124, "the binding timestamp (REG-1)", 10.5, "middle", INK2)
    c.text(xs["doi"], y + 26, "DOI deposit", 12, "middle", INK, "600")
    c.text(xs["doi"], y + 42, "external anchor (REG-3)", 10.5, "middle", INK2)
    c.text(xs["run"], 174, "first governed", 12, "middle", INK, "600")
    c.text(xs["run"], 190, "measurement", 12, "middle", INK, "600")
    c.text(xs["out"], 174, "outcome: pass or miss", 12, "middle", INK, "600")
    c.text(xs["out"], 190, "the sealed bar is not relaxed", 10.5, "middle", INK2)
    _bracket(c, xs["seal"], 680, 312, "amendments are appended after the sealed text, dated, with the reason (REG-2)",
             above=False)
    c.text(465, 350, "the sealed text is never edited; CI checks that the hash still verifies", 10.5, "middle", INK3,
           italic=True)
    c.save(p)


# ------------------------------------------------------------------ chapter 16
def fig_16_1():
    p = reg("chapters/ch16_honest_negatives.md", "16.1",
            "A schematic of the KV-key ladder, NEG-5 to NEG-9. Each box is a sealed proxy or test that was refuted, "
            "with what the refutation showed. Each miss located the next hypothesis, and the sequence ends at the "
            "direct trace, which gets the discriminating flip right 12 of 12 times and is still not a complete rank "
            "statistic. NEG-5 refutes the registered test and not claim GO-2.",
            "## The four kinds of boundary")
    c = Canvas(720, 440, "Five refuted proxies, each locating the next")
    rungs = [
        ("NEG-5: the test as first registered", "missed 2 of 4 bars: a matched-bits confound"),
        ("NEG-6: demeaned error norm", "fails to order the arms: magnitude is not it"),
        ("NEG-7: a score of the compressor alone", "at fixed reconstruction, ranking flips with consumer"),
        ("NEG-8: variance-ratio proxy", "Spearman 0.80 only: a noisy estimate of the trace"),
        ("NEG-9: the direct trace tr(P_C Σ_δ)", "flip 12/12, yet it misorders a middle pair"),
    ]
    for i, (lab, sub) in enumerate(rungs):
        x, y = 30 + 95 * i, 56 + 70 * i
        c.box(x, y, 300, 52, lab, sub)
        if i < len(rungs) - 1:
            c.line(x + 45, y + 52, x + 45, y + 96, INK2, 1.5)
            c.arrow(x + 45, y + 96, x + 93, y + 96, INK2, 1.5)
    c.text(450, 78, "[refuted], all five;", 11, "start", INK2, italic=True)
    c.text(450, 94, "each miss carried in the ledger", 11, "start", INK2, italic=True)
    c.text(30, 396, "ends at a statistic that is load-bearing", 11, "start", INK2, italic=True)
    c.text(30, 412, "but bounded", 11, "start", INK2, italic=True)
    c.save(p)


def fig_16_2():
    claimed, mc, corrected = 1.0, 1.226, 1.225
    assert abs(mc - corrected) < 0.002 and mc - claimed > 0.2
    p = reg("chapters/ch16_honest_negatives.md", "16.2",
            "NEG-18, the refuted dispersion constant, against what was measured. The claim V = (r_D/2) log² e, which "
            "counts only the modes above the water level, gives 1.0 on the test case and is drawn as a dashed outline "
            "because it is [refuted]. A Monte Carlo of the definition gives 1.226. The corrected formula, in which "
            "each mode below the level adds (γ/θ)²/2, gives 1.225. The vertical axis is the dispersion V in the units "
            "the chapter prints. What stands is the bound: the dispersion counts at most the read dimensions.",
            "## The four kinds of boundary")
    c = Canvas(720, 400, "NEG-18: the claimed dispersion constant against the measured one")
    ax = Axes(c, 70, 52, 600, 280, (0, 3), (0, 1.4), [], [0, 0.25, 0.5, 0.75, 1, 1.25], "", "dispersion V")
    rows = [("claim: active modes only", "[refuted]", claimed, None),
            ("Monte Carlo of the definition", "measured", mc, SERIES[0]),
            ("corrected formula", "below-level modes counted", corrected, SERIES[1])]
    for i, (name, sub, v, col) in enumerate(rows):
        xm = ax.X(i + 0.5)
        if col is None:
            _hollow(c, xm - 20, ax.Y(v), 40, ax.Y(0) - ax.Y(v), CRITICAL)
        else:
            c.rect(xm - 20, ax.Y(v), 40, ax.Y(0) - ax.Y(v), col, 4, title=f"{name} {v}")
        c.text(xm, ax.Y(v) - 7, f"{v:.3f}" if col else "1.0", 11.5, "middle", INK)
        c.text(xm, ax.Y(0) + 17, name, 11, "middle", INK2)
        c.text(xm, ax.Y(0) + 33, sub, 10.5, "middle", INK, "600" if col is None else "normal")
    yc = ax.Y(claimed)
    c.line(ax.X(0.5) + 20, yc, ax.x0 + ax.w, yc, INK3, 1.5, dash="4 4")
    c.text(ax.X(1), yc - 7, "the claimed value", 10.5, "middle", INK2, italic=True)
    c.save(p)


# ------------------------------------------------------------------ chapter 18
def fig_18_1():
    p = reg("chapters/ch18_the_principle.md", "18.1",
            "A schematic of the chapter's summary: one operator, four faces. Each face is a shadow of the read metric "
            "P_C, and each was a separate literature, named beneath its box. The last line under three of the faces "
            "says what happens in the slice P_C = I, the observer that reads every direction equally: the rate is "
            "Shannon's, the flip collapses because reconstruction is then optimal, and the quotient is trivial.",
            "## What the principle licenses")
    c = Canvas(720, 420, "One operator, four faces; Shannon is the slice P_C = I")
    c.box(255, 190, 210, 60, "the read metric P_C", "P_C = Jᵀ G J", fill=BOX, stroke=SERIES[0])
    faces = [
        (30, 66, "COST", "the rate–distortion function R_C(D)", "rate–distortion theory", "at P_C = I: Shannon's R(D)"),
        (480, 66, "VALUE", "the flip: preserve, not reconstruct", "task-aware compression",
         "at P_C = I: the flip collapses"),
        (30, 300, "LEGIBILITY", "the quotient X/~C", "spectral embedding", "at P_C = I: the quotient is trivial"),
        (480, 300, "IDENTIFIABILITY", "the blind probe", "probing", "from the observer's behaviour alone"),
    ]
    for x, y, lab, sub, lit, slc in faces:
        c.box(x, y, 210, 56, lab, sub)
        c.text(x + 4, y + 74, "literature: " + lit, 10.5, "start", INK2)
        c.text(x + 4, y + 90, slc, 10.5, "start", INK3, italic=True)
        bx = x + 210 if x < 300 else x
        tx = 300 if x < 300 else 420
        ty = 190 if y < 200 else 250
        c.line(bx, y + 28, tx, ty, INK3, 1.5)
    c.save(p)


# ------------------------------------------------------------------ chapter 19
def fig_19_1():
    k = 0.177
    phi = 100.0
    tcoh = phi / k
    assert abs(phi / tcoh - 0.177) < 1e-12
    p = reg("chapters/ch19_the_certificate_that_ages.md", "19.1",
            "A schematic of the witnessed triple on a time axis. Each bar is one certificate, a claim that the "
            "consumer's read is within tolerance, valid from its issue until it is renewed. The certificate issued at "
            "t is acted on at t + Δ, and it can be wrong for no reason other than Δ. The witness is an independent "
            "measurement of the true outcome, and it grades the claim at the time of use. The renewal interval is the "
            "refresh floor φ, drawn at 0.177 of the coherence time, the slope this chapter quotes from Chapter 21 for "
            "one 5G physical layer [demonstrated]; on another substrate the ratio may differ.",
            "## The false-clear rate")
    c = Canvas(720, 400, "A certificate is issued at one time and used at another")
    x0 = 70
    y = 250
    c.arrow(40, y, 695, y, INK3, 1.5)
    c.text(695, y + 18, "time", 10.5, "end", INK3, italic=True)
    n = 6
    for i in range(n):
        xa = x0 + phi * i
        c.add(f'<rect x="{xa + 2:.2f}" y="196" width="{phi - 4:.2f}" height="14" rx="3" fill="{SERIES[0]}" '
              f'fill-opacity="{0.9 if i == 0 else 0.45}"><title>certificate {i + 1}</title></rect>')
        c.line(xa, y - 6, xa, y + 6, INK2, 1.5)
    c.line(x0 + phi * n, y - 6, x0 + phi * n, y + 6, INK2, 1.5)
    c.text(x0, 186, "certificate, issued at t", 11.5, "start", INK)
    _bracket(c, x0 + 2 * phi, x0 + 3 * phi, 172, "refresh floor φ")
    xe = x0 + tcoh
    assert xe < 660
    _bracket(c, x0, xe, 110, "coherence time T_coh: the certified state decorrelates over this span")
    xu = x0 + 62
    c.dot(xu, y, CRITICAL, 6, title="acted on at t + Δ")
    _bracket(c, x0, xu, 278, "Δ", above=False)
    c.text(xu + 12, y + 22, "acted on at t + Δ", 11.5, "start", INK)
    c.box(250, 318, 330, 50, "witness W", "an independent measurement of the true outcome")
    c.line(250, 343, xu, 343, INK2, 1.5)
    c.arrow(xu, 343, xu, 304, INK2, 1.5)
    c.text(40, 388, "schematic; φ / T_coh drawn at 0.177", 10.5, "start", INK3, italic=True)
    c.save(p)


def fig_19_2():
    cov, fc = 0.80, 0.25
    joint = cov * fc
    assert abs(joint - 0.20) < 1e-12
    p = reg("chapters/ch19_the_certificate_that_ages.md", "19.2",
            "The false-clear rate as a conditional, drawn for illustrative values (coverage 0.80, false-clear rate "
            "0.25; these are not measurements). The square is all certificates. Its width splits them into those that "
            "clear and those that do not. Within the ones that clear, the shaded part is the fraction the witness "
            "refutes: that fraction is FC. The joint probability of clearing and being refuted is the product, 0.20. "
            "A certificate that clears everything has coverage 1, so for it the joint rate and FC are the same number.",
            "## What this Part shows")
    c = Canvas(720, 400, "The false-clear rate is conditional on the certificate clearing")
    x0, y0, s = 70, 70, 260
    wc = s * cov
    hr = s * fc
    c.add(f'<rect x="{x0}" y="{y0}" width="{wc - 2:.2f}" height="{s - hr - 2:.2f}" fill="{SERIES[0]}" '
          f'fill-opacity="0.75"><title>clears, upheld by the witness</title></rect>')
    c.add(f'<rect x="{x0}" y="{y0 + s - hr:.2f}" width="{wc - 2:.2f}" height="{hr:.2f}" fill="{CRITICAL}">'
          f'<title>clears, refuted by the witness</title></rect>')
    c.add(f'<rect x="{x0 + wc:.2f}" y="{y0}" width="{s - wc:.2f}" height="{s}" fill="{BOX}" stroke="{BORDER}" '
          f'stroke-width="1"><title>does not clear</title></rect>')
    c.text(x0 + wc / 2, y0 + (s - hr) / 2 + 4, "clears, upheld", 12, "middle", SURFACE, "600")
    c.text(x0 + wc / 2, y0 + s - hr / 2 + 4, "clears, refuted by W", 12, "middle", SURFACE, "600")
    c.text(x0 + wc + (s - wc) / 2, y0 + s / 2, "does not clear", 11, "middle", INK2, rotate=-90)
    _bracket(c, x0, x0 + wc - 2, y0 + s + 18, "coverage 0.80", above=False)
    c.line(x0 - 14, y0 + s - hr, x0 - 14, y0 + s, INK2, 1.5)
    c.line(x0 - 20, y0 + s - hr, x0 - 8, y0 + s - hr, INK2, 1.5)
    c.line(x0 - 20, y0 + s, x0 - 8, y0 + s, INK2, 1.5)
    c.text(x0 - 24, y0 + s - hr / 2, "FC 0.25", 11, "middle", INK2, rotate=-90)
    tx = 390
    c.text(tx, 106, "coverage = Pr[ certificate clears ] = 0.80", 12, "start", INK)
    c.text(tx, 146, "FC = Pr[ W refutes it | it clears ] = 0.25", 12, "start", INK, "600")
    c.text(tx, 164, "the height of the shaded part within the", 10.5, "start", INK2)
    c.text(tx, 180, "certificates that clear", 10.5, "start", INK2)
    c.text(tx, 220, "joint = Pr[ clears and refuted ]", 12, "start", INK)
    c.text(tx, 238, f"= 0.80 × 0.25 = {joint:.2f}", 12, "start", INK)
    c.text(tx, 256, "the shaded area as a share of the square", 10.5, "start", INK2)
    c.text(tx, 300, "clears everything: coverage 1,", 10.5, "start", INK3, italic=True)
    c.text(tx, 316, "so the joint rate equals FC", 10.5, "start", INK3, italic=True)
    c.text(16, 390, "illustrative values, not measurements", 10.5, "start", INK3, italic=True)
    c.save(p)


# ------------------------------------------------------------------ chapter 20
def fig_20_1():
    rows = [("BGP", 0.351), ("IS-IS", 0.184), ("OSPF", 0.083)]
    p = reg("chapters/ch20_the_false_clear_rate.md", "20.1",
            "The routing anchor of the outline: how often the certificate \"60 seconds of quiescence means converged\" "
            "is false, for three routing protocols [replicated]. The vertical axis is the false-clear rate. The "
            "outline's reading is that opacity orders the bands and the implementation places a system within its "
            "band. The outline prints no target for these certificates, so none is drawn.",
            "## Key figures / claims (→ ledger)")
    c = Canvas(720, 400, "Sixty seconds of silence is wrong up to a third of the time")
    ax = Axes(c, 70, 52, 600, 280, (0, 3), (0, 0.4), [], [0, 0.1, 0.2, 0.3, 0.4], "",
              "false-clear rate of 60 s quiescence")
    for i, (name, v) in enumerate(rows):
        xm = ax.X(i + 0.5)
        c.rect(xm - 20, ax.Y(v), 40, ax.Y(0) - ax.Y(v), SERIES[0], 4, title=f"{name} {v}")
        c.text(xm, ax.Y(v) - 7, f"{v:.3f}", 11.5, "middle", INK)
        c.text(xm, ax.Y(0) + 18, name, 12, "middle", INK2)
    c.text(16, 390, "[replicated]; numbers as printed in the chapter outline", 10.5, "start", INK3, italic=True)
    c.save(p)


# ------------------------------------------------------------------ chapter 22
def fig_22_1():
    # (domain, class, naive, witnessed, naive label, witnessed label); a value is a number, a (lo, hi) range,
    # a list of points, or None with the label standing alone.
    rows = [
        ("Interdomain routing", "[replicated]", [0.083, 0.184, 0.351], None, "0.083, 0.184, 0.351 (OSPF, IS-IS, BGP)",
         "detector band; no number printed"),
        ("Replication (databases)", "[replicated]", 0.5, (0.02, 0.06), "~0.5", "~0.02–0.06"),
        ("ZooKeeper, hot footprint", "[replicated]", 0.99, 0.0, "0.99", "0"),
        ("ZooKeeper, cold footprint", "[replicated]", 0.01, 0.0, "0.01", "0"),
        ("Cellular PHY/RAN", "[demonstrated]", (0.28, 0.47), (0.05, 0.13), "0.28–0.47", "0.05–0.13"),
        ("Optical", "[predicted]", 0.40, 0.0, "~0.40", "~0 per footprint"),
        ("Power grid", "[predicted]", 0.25, 0.01, "~0.25", "~0.01"),
        ("AI evaluation", "[predicted]", None, None, "shakedown; no number printed", None),
        ("Quantum devices", "[exploratory]", (0.28, 0.43), 0.0, "0.28–0.43", "0"),
        ("Markets", "[exploratory]", 0.37, 0.003, "0.37", "0.003"),
        ("Sensing", "[refuted]", None, None, "drift real; linear recalibration only ~1.6×", None),
    ]
    p = reg("chapters/ch22_the_freshness_sweep.md", "22.1",
            "The freshness sweep of the outline's table, drawn on one axis. For each domain the upper mark is the "
            "false-clear rate of the naive certificate and the lower mark is the rate once the certificate is "
            "witnessed. A bar is a range and a single dot is one value, both as the table prints them, approximate "
            "values included. The class of each row is at the right, and rows keep their own class: routing and "
            "replication are [replicated], cellular is [demonstrated], optical, grid and AI evaluation are "
            "[predicted], quantum and markets are [exploratory]. Sensing is [refuted]: the clean template failed and "
            "no false-clear pair is printed for it. The outline does not claim that the magnitudes coincide across "
            "domains.",
            "## Narrative beats")
    c = Canvas(720, 520, "One grammar, many substrates: naive against witnessed false-clear")
    rh = 36
    ax = Axes(c, 190, 62, 360, rh * len(rows), (0, 1), (0, len(rows)), [0, 0.25, 0.5, 0.75, 1], [],
              "false-clear rate", "")
    for v in (0.25, 0.5, 0.75, 1.0):
        c.line(ax.X(v), ax.y0, ax.X(v), ax.y0 + ax.h, GRID, 1)
    c.line(ax.x0, ax.y0, ax.x0, ax.y0 + ax.h, GRID, 1)
    c.text(566, 52, "class", 10.5, "start", INK3, italic=True)

    def mark(val, yy, col, name):
        """Draw a value; return the x of its right end."""
        if isinstance(val, list):
            for v in val:
                c.dot(ax.X(v), yy, col, 4.5, title=f"{name} {v}")
            return ax.X(max(val))
        if isinstance(val, tuple):
            c.line(ax.X(val[0]), yy, ax.X(val[1]), yy, col, 9)
            return ax.X(val[1])
        c.dot(ax.X(val), yy, col, 4.5, title=f"{name} {val}")
        return ax.X(val)

    for i, (dom, cls, nv, wv, nlab, wlab) in enumerate(rows):
        y = ax.y0 + rh * (i + 0.5)
        if i:
            c.line(ax.x0, y - rh / 2, ax.x0 + ax.w, y - rh / 2, GRID, 1)
        c.text(ax.x0 - 10, y + 4, dom, 11.5, "end", INK2)
        c.text(566, y + 4, cls, 11, "start", INK, "600" if cls in ("[replicated]", "[demonstrated]", "[refuted]")
               else "normal")
        if nv is None:
            c.text(ax.x0 + 10, y + 4, nlab, 10.5, "start", INK2, italic=True)
            continue
        xr = mark(nv, y - 7, SERIES[1], dom + ", naive")
        if isinstance(nv, float) and nv > 0.8:
            c.text(ax.X(nv) - 10, y - 3.5, nlab, 10, "end", INK)
        else:
            c.text(xr + 10, y - 3.5, nlab, 10, "start", INK)
        if wv is None:
            c.text(ax.x0 + 10, y + 10.5, wlab, 10, "start", INK2, italic=True)
        else:
            xr = mark(wv, y + 7, SERIES[0], dom + ", witnessed")
            c.text(xr + 10, y + 10.5, wlab, 10, "start", INK)
    legend(c, 190, 46, [("naive certificate", SERIES[1]), ("witnessed", SERIES[0])])
    c.save(p)


# ------------------------------------------------------------------ chapter 23
def fig_23_1():
    p = reg("chapters/ch23_the_governor.md", "23.1",
            "A schematic of the governor as the outline describes it. Top: the operational loop, which observes the "
            "certificate and witness streams, measures the false-clear rate per certificate and consumer, governs, and "
            "certifies. Below: the escalation ladder that the govern step follows. It first shrinks the refresh period "
            "to the floor, then changes the mechanism when refreshing at the floor still leaves the certificate "
            "vacuous, and certifies per consumer, since the same certificate can hold for a lax consumer and be "
            "vacuous for a strict one. The diagram shows structure only; the outline calls the governor a reference "
            "implementation.",
            "## Boundary / honesty")
    c = Canvas(720, 440, "The governor: a loop that measures FC and a ladder that acts on it")
    labels = [("observe", "certificate + witness"), ("measure", "FC per consumer"), ("govern", "escalation ladder"),
              ("certify", "per consumer")]
    xs = [30, 205, 380, 555]
    for x, (lab, sub) in zip(xs, labels):
        c.box(x, 76, 135, 54, lab, sub, stroke=SERIES[0] if lab == "govern" else BORDER)
    for x in xs[:-1]:
        c.arrow(x + 135, 103, x + 173, 103, INK2, 1.5)
    c.line(622, 76, 622, 54, INK3, 1.5)
    c.line(622, 54, 97, 54, INK3, 1.5)
    c.arrow(97, 54, 97, 74, INK3, 1.5)
    c.text(360, 48, "the loop repeats", 10.5, "middle", INK3, italic=True)
    rungs = [("1. refresh faster", "vacuous, reporting above the floor: shrink the period to the floor"),
             ("2. change mechanism", "at the floor and still vacuous: add diversity, re-route, re-layout"),
             ("3. certify per consumer", "the reliability target is the read operator")]
    c.arrow(447, 130, 447, 176, SERIES[0], 1.5)
    for i, (lab, sub) in enumerate(rungs):
        x, y = 100 + 60 * i, 178 + 80 * i
        c.box(x, y, 410, 54, lab, sub)
        if i < len(rungs) - 1:
            c.line(x + 28, y + 54, x + 28, y + 107, INK2, 1.5)
            c.arrow(x + 28, y + 107, x + 58, y + 107, INK2, 1.5)
    c.text(16, 428, "schematic of the outline's structure", 10.5, "start", INK3, italic=True)
    c.save(p)


# ------------------------------------------------------------------ appendix B
def fig_B_1():
    gam = [4.0, 2.0, 0.6, 0.3]
    theta = 1.0
    part = [0.5 if g > theta else 0.5 * (g / theta) ** 2 for g in gam]
    r_d = sum(1 for g in gam if g > theta)
    r = len(gam)
    v = sum(part)
    assert r_d == 2 and abs(v - 1.225) < 1e-12 and abs(v - 1.226) < 0.002
    assert r_d <= 2 * v <= r
    p = reg("chapters/appendix_b_cost_ledger.md", "B.1",
            "The corrected variance of Theorem B7 on the appendix's test case, tilted mode variances (4, 2, 0.6, 0.3) "
            "and water level 1, in nats squared. Each mode above the level contributes 1/2. Each mode below it "
            "contributes (γ/θ)²/2, here 0.18 and 0.045, which the old constant left out. The sum is 1.225; the "
            "Monte Carlo of the definition quoted in the text gives 1.226. The old constant r_D/2 = 1.0, counting "
            "active modes only, is [refuted] (NEG-18) and is drawn as a dashed line; it survives as the lower bound, "
            "and the upper bound is r/2 = 2. The corrected formula is [proved] as the variance of the tilted "
            "information (ledger row PAPER-III.b); reading it as the dispersion stays [exploratory].",
            "## Custody summary (corrected 2026-11-20 and 2026-11-21)")
    c = Canvas(720, 400, "Modes below the water level still add to the variance")
    ax = Axes(c, 70, 56, 560, 270, (0, 6), (0, 2.2), [], [0, 0.5, 1, 1.5, 2], "", "contribution to V, nats²")
    for i, (g, q) in enumerate(zip(gam, part)):
        xm = ax.X(i + 0.5)
        col = SERIES[0] if g > theta else SERIES[1]
        c.rect(xm - 20, ax.Y(q), 40, ax.Y(0) - ax.Y(q), col, 4, title=f"mode γ = {g:g}: {q:g}")
        c.text(xm, ax.Y(q) - 7, f"{q:g}", 11, "middle", INK)
        c.text(xm, ax.Y(0) + 17, f"γ = {g:g}", 11, "middle", INK2)
        c.text(xm, ax.Y(0) + 33, "above the level" if g > theta else "below the level", 10.5, "middle", INK3)
    xm = ax.X(5.0)
    acc = 0.0
    for g, q in zip(gam, part):
        col = SERIES[0] if g > theta else SERIES[1]
        ya, yb = ax.Y(acc), ax.Y(acc + q)
        c.add(f'<rect x="{xm - 20:.2f}" y="{yb + 1:.2f}" width="40" height="{max(ya - yb - 2, 0.8):.2f}" '
              f'fill="{col}"><title>γ = {g:g}: {q:g}</title></rect>')
        acc += q
    c.text(xm, ax.Y(v) - 8, f"sum {v:.3f}", 11.5, "middle", INK, "600")
    c.text(xm, ax.Y(0) + 17, "all four modes", 11, "middle", INK2)
    c.text(xm, ax.Y(0) + 33, "V, corrected", 10.5, "middle", INK3)
    c.dot(xm + 46, ax.Y(1.226), INK, 4, title="Monte Carlo 1.226")
    c.text(xm + 56, ax.Y(1.226) - 4, "Monte Carlo", 10.5, "start", INK2)
    c.text(xm + 56, ax.Y(1.226) + 10, "1.226", 10.5, "start", INK2)
    y1, y2 = ax.Y(1.0), ax.Y(2.0)
    c.line(ax.x0, y1, ax.x0 + ax.w, y1, CRITICAL, 1.5, dash="5 4")
    c.text(ax.x0 + 6, y1 - 6, "old constant r_D/2 = 1.0, active modes only: [refuted]; it is the lower bound", 10.5,
           "start", INK2, italic=True)
    c.line(ax.x0, y2, ax.x0 + ax.w, y2, INK3, 1.5, dash="4 4")
    c.text(ax.x0 + 6, y2 - 6, "upper bound r/2 = 2, met when every mode is above the level", 10.5, "start", INK2,
           italic=True)
    legend(c, 70, 42, [("mode above the level", SERIES[0]), ("mode below the level", SERIES[1])])
    c.save(p)


# ------------------------------------------------------------------ appendix G
