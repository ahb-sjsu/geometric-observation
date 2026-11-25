"""Draw the book's figures as SVG and embed them in the chapters.

Run from the repository root:  python tools/make_figures.py
Writes figures/chNN_figM.svg and inserts, before a named section heading of each chapter,
an image line and an italic caption. Idempotent. Every figure is drawn from a formula
or from numbers that already stand in the chapter text; a figure carries no new claim.
`tools/svgfig.py` is the small SVG chart library of the companion volume.
"""

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svgfig import Canvas, Axes, INK, INK2, INK3, GRID, SERIES, CRITICAL, legend  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG = os.path.join(ROOT, "figures")
CH = os.path.join(ROOT, "chapters")
os.makedirs(FIG, exist_ok=True)
FIGS = []  # (chapter file, label, filename, caption, heading the figure goes before)


def reg(chapter, label, caption, before):
    fname = f"ch{label.split('.')[0].zfill(2)}_fig{label.split('.')[1]}.svg"
    FIGS.append((chapter, label, fname, caption, before))
    return os.path.join(FIG, fname)


def h2(x):
    return 0.0 if x <= 0 or x >= 1 else -x * math.log2(x) - (1 - x) * math.log2(1 - x)


# ------------------------------------------------------------------ chapter 5
def fig_5_1():
    p = reg("ch05_the_read_metric_and_the_quotient.md", "5.1",
            "Two errors with the same reconstruction error, trace 2. The consumer reads the horizontal direction only, "
            "so its read metric is the rank-one matrix with a single 1 in the top left. Error A costs it 0.3 and error B "
            "costs it 1.7. The vertical direction is the kernel of the read metric: displacement along it is not read.",
            "## The read distortion")
    c = Canvas(720, 400, "Equal reconstruction error, unequal error as the consumer reads it")
    cx, cy, s = 250, 215, 95
    c.line(cx - 200, cy, cx + 200, cy, GRID, 1)
    c.line(cx, cy - 160, cx, cy + 160, GRID, 1)
    c.ellipse(cx, cy, s * math.sqrt(0.3), s * math.sqrt(1.7), 0, SERIES[0], SERIES[0], 2, 0.10,
              title="error A, covariance diag(0.3, 1.7)")
    c.ellipse(cx, cy, s * math.sqrt(1.7), s * math.sqrt(0.3), 0, SERIES[1], SERIES[1], 2, 0.10,
              title="error B, covariance diag(1.7, 0.3)")
    c.arrow(cx, cy, cx + 185, cy, INK, 2)
    c.text(cx + 190, cy + 20, "read direction", 11.5, "end", INK)
    c.line(cx, cy - 150, cx, cy + 150, INK3, 1.5, dash="5 5")
    c.text(cx + 8, cy - 146, "kernel: not read", 11.5, "start", INK2)
    x0 = 500
    c.text(x0, 96, "error A", 12, "start", INK, "600")
    c.text(x0, 116, "reconstruction error 0.3 + 1.7 = 2", 11.5, "start", INK2)
    c.text(x0, 134, "read error 0.3", 11.5, "start", INK2)
    c.text(x0, 176, "error B", 12, "start", INK, "600")
    c.text(x0, 196, "reconstruction error 1.7 + 0.3 = 2", 11.5, "start", INK2)
    c.text(x0, 214, "read error 1.7", 11.5, "start", INK2)
    c.text(x0, 262, "read error = tr(P Δ)", 11.5, "start", INK2, italic=True)
    legend(c, 16, 384, [("error A", SERIES[0]), ("error B", SERIES[1])])
    c.text(704, 384, "one-standard-deviation contours", 10.5, "end", INK3, italic=True)
    c.save(p)


# ------------------------------------------------------------------ chapter 7
def fig_7_1():
    gam = [4.0, 2.0, 1.0, 0.5, 0.25]
    theta = 0.75
    d = sum(min(g, theta) for g in gam)
    rate = 0.5 * sum(math.log2(g / theta) for g in gam if g > theta)
    assert abs(d - 3.0) < 1e-12
    p = reg("ch07_cost.md", "7.1",
            f"Reverse water-filling on five modes with weighted variances 4, 2, 1, 0.5 and 0.25, at distortion D = 3. "
            f"The water level is 0.75. Each mode keeps an error equal to the smaller of its variance and the level, and "
            f"only the part above the level is described. Three modes are described, at a total of {rate:.2f} bits, and "
            f"the two modes below the level receive no bits. For a consumer the modes are those of the source weighted by "
            f"the read metric, so a direction the consumer does not read has variance 0 here and is never described.",
            "## Two observers: the rate region and refinability")
    c = Canvas(720, 400, "Reverse water-filling: describe only what stands above the level")
    ax = Axes(c, 70, 52, 560, 280, (0, 5), (0, 4.4), [], [0, 1, 2, 3, 4], "", "weighted variance of the mode")
    for i, g in enumerate(gam):
        x = ax.X(i + 0.5) - 26
        kept = min(g, theta)
        if g > theta:
            c.rect(x, ax.Y(g), 52, ax.Y(theta) - ax.Y(g), SERIES[0], 4,
                   title=f"mode {i + 1}: described part {g - theta:.2f}, {0.5 * math.log2(g / theta):.2f} bits")
            c.text(x + 26, ax.Y(g) - 6, f"{0.5 * math.log2(g / theta):.2f} bits", 10.5, "middle", INK)
        c.rect(x, ax.Y(kept), 52, ax.Y(0) - ax.Y(kept), SERIES[1], 0, title=f"mode {i + 1}: error kept {kept:.2f}",
               opacity=0.55)
        if g <= theta:
            c.text(x + 26, ax.Y(g) - 6, "0 bits", 10.5, "middle", INK)
        c.text(x + 26, ax.Y(0) + 16, f"mode {i + 1}", 11, "middle", INK2)
    y = ax.Y(theta)
    c.line(ax.x0, y, ax.x0 + ax.w, y, INK, 1.5, dash="6 4")
    c.text(ax.x0 + ax.w + 6, y + 4, "level 0.75", 11, "start", INK)
    legend(c, 70, 40, [("described", SERIES[0]), ("error kept", "#f3a585")])
    c.text(16, 390, f"error kept sums to {d:.0f}, the distortion; rate {rate:.2f} bits", 10.5, "start", INK3, italic=True)
    c.save(p)


# ------------------------------------------------------------------ chapter 8
def fig_8_1():
    p = reg("ch08_value.md", "8.1",
            "The flip in its smallest form. Descriptions A and B are the two errors of Figure 5.1, with equal "
            "reconstruction error 2. A consumer that reads the horizontal direction ranks A first (0.3 against 1.7). A "
            "consumer that reads the vertical direction ranks B first. Reconstruction error cannot rank them at all. "
            "This is an illustration of the mechanism, not a measurement; the measured cases are in the text.",
            "## The flip is a property of observation, not of a domain")
    c = Canvas(720, 400, "Two descriptions, two consumers, opposite verdicts")
    ax = Axes(c, 70, 52, 560, 280, (0, 3), (0, 2.2), [], [0, 0.5, 1, 1.5, 2], "", "error as measured")
    groups = [("reconstruction error", 2.0, 2.0), ("consumer 1 (reads horizontal)", 0.3, 1.7),
              ("consumer 2 (reads vertical)", 1.7, 0.3)]
    for i, (name, a, b) in enumerate(groups):
        xm = ax.X(i + 0.5)
        for j, v in enumerate((a, b)):
            x = xm - 26 + j * 28
            c.rect(x, ax.Y(v), 24, ax.Y(0) - ax.Y(v), SERIES[j], 4, title=f"{name}: description {'AB'[j]} = {v}")
            c.text(x + 12, ax.Y(v) - 6, f"{v:g}", 10.5, "middle", INK)
        c.text(xm, ax.Y(0) + 16, name, 11, "middle", INK2)
    legend(c, 70, 40, [("description A", SERIES[0]), ("description B", SERIES[1])])
    c.text(16, 390, "lower is better; the two consumers disagree and reconstruction error is tied", 10.5, "start", INK3,
           italic=True)
    c.save(p)


# ------------------------------------------------------------------ chapter 17
def fig_17_1():
    p = reg("ch17_open_problems_and_the_keystone_theorem.md", "17.1",
            "A read kernel that moves with the point, for the consumer g(x1, x2) = x1 + sin x2. The curves are level "
            "sets of g, the fibers the consumer cannot tell apart. The short strokes are the kernel of the Jacobian, "
            "the direction along the fiber, at points of the fiber through the origin. The direction turns with x2, so "
            "no single direction is unread everywhere, and the averaged read metric has rank 2 although the consumer "
            "reads one number.",
            "## The cross-domain magnitude constant")
    c = Canvas(720, 400, "The unread direction turns from point to point")
    ax = Axes(c, 90, 48, 540, 290, (-4, 4), (-3.3, 3.3), [-4, -2, 0, 2, 4], [-3, -2, -1, 0, 1, 2, 3], "x1", "x2")
    for k, cval in enumerate([-3, -2, -1, 0, 1, 2, 3]):
        pts = []
        for i in range(0, 133):
            x2 = -3.3 + 6.6 * i / 132
            x1 = cval - math.sin(x2)
            if -4 <= x1 <= 4:
                pts.append((ax.X(x1), ax.Y(x2)))
        c.polyline(pts, SERIES[0] if cval == 0 else "#a9c8ee", 2 if cval == 0 else 1.5, title=f"g = {cval}")
    for x2 in [-2.6, -1.6, -0.6, 0.0, 0.6, 1.6, 2.6]:
        x1 = -math.sin(x2)
        # kernel of (1, cos x2) is spanned by (-cos x2, 1)
        kx, ky = -math.cos(x2), 1.0
        n = math.hypot(kx, ky)
        kx, ky = 0.42 * kx / n, 0.42 * ky / n
        c.line(ax.X(x1 - kx), ax.Y(x2 - ky), ax.X(x1 + kx), ax.Y(x2 + ky), SERIES[1], 3)
        c.dot(ax.X(x1), ax.Y(x2), INK, 2.5)
    legend(c, 90, 38, [("level sets of g", SERIES[0]), ("kernel of the Jacobian", SERIES[1])])
    c.save(p)


def fig_17_2():
    det_q = 0.5 * (1 - math.exp(-1)) ** 2
    h_u = 1.598216
    xs = [10 ** (-4 + 2 * i / 40) for i in range(41)]
    fix = [math.log(2 / d) + 0.5 * math.log(det_q) for d in xs]
    own = [h_u - 0.5 * math.log(2 * math.pi * math.e * d) for d in xs]
    c_star = math.log(2) + 0.5 * math.log(det_q) + 0.5 * math.log(2 * math.pi * math.e) - h_u
    assert abs(c_star - (-0.291379)) < 2e-6
    p = reg("ch17_open_problems_and_the_keystone_theorem.md", "17.2",
            "The price of stopping at the averaged weight, for g(x1, x2) = x1 + sin x2 with a standard Gaussian source. "
            "The upper line is the least rate of a description whose error covariance does not depend on the point, "
            "ln(2/D) + ½ ln det Q. The lower line is the Shannon lower bound on the consumer's own rate, which the note "
            "shows is tight to within ½ ln(1 + D). Both are drawn without their O(D) terms. The lines separate by "
            "½ ln(1/D) − 0.291 nats, which grows without bound as the loss D falls (ledger row T1-MK, exploratory).",
            "## The cross-domain magnitude constant")
    c = Canvas(720, 400, "Rate against consumer loss: the averaged weight pays for two directions")
    ax = Axes(c, 70, 52, 540, 280, (1e-4, 1e-2), (0, 10), [], [0, 2, 4, 6, 8, 10],
              "consumer loss D (logarithmic scale)", "rate, nats", xlog=True)
    for v, lab in ((1e-4, "0.0001"), (1e-3, "0.001"), (1e-2, "0.01")):
        c.text(ax.X(v), ax.y0 + ax.h + 16, lab, 11, "middle", INK2)
    for j, (name, ys) in enumerate([("fixed-covariance class", fix), ("consumer's own rate", own)]):
        c.polyline([(ax.X(x), ax.Y(y)) for x, y in zip(xs, ys)], SERIES[j], 2, title=name)
    for d in (1e-4, 1e-2):
        gap = 0.5 * math.log(1 / d) + c_star
        yf = math.log(2 / d) + 0.5 * math.log(det_q)
        x = ax.X(d) + (10 if d < 1e-3 else -10)
        c.line(x, ax.Y(yf), x, ax.Y(yf - gap), INK3, 1.5, dash="3 3")
        c.text(x + (6 if d < 1e-3 else -6), ax.Y(yf - gap / 2) + 4, f"{gap:.2f} nats", 11,
               "start" if d < 1e-3 else "end", INK)
    legend(c, 70, 40, [("fixed-covariance class", SERIES[0]), ("consumer's own rate", SERIES[1])])
    c.save(p)


# ------------------------------------------------------------------ chapter 24
def fig_24_1():
    p = reg("ch24_the_holder.md", "24.1",
            "The three parties of the rate-leakage-distortion series. The encoder sees the source and writes a message. "
            "The decoder has the message only and must reproduce a linear part of the source within distortion D. The "
            "holder has the message and its own noisy observation S of the source, and reconstructs nothing. The rate "
            "counts the message. The leakage counts what the message tells the holder beyond S.",
            "## Paper I: reverse water-filling on a tilted weight")
    c = Canvas(720, 400, "Encoder, decoder, and a holder that learns without decoding")
    c.box(40, 150, 120, 56, "source", "X, Gaussian")
    c.box(230, 150, 120, 56, "encoder", "sees X")
    c.box(520, 80, 150, 56, "decoder", "reproduces Y = FX")
    c.box(520, 250, 150, 56, "holder", "has M and S")
    c.arrow(160, 178, 228, 178, INK2, 1.5)
    c.line(350, 178, 430, 178, INK2, 1.5)
    c.text(390, 170, "message M", 11.5, "middle", INK)
    c.text(390, 196, "rate R", 11, "middle", INK2, italic=True)
    c.arrow(430, 178, 518, 112, INK2, 1.5)
    c.arrow(430, 178, 518, 274, INK2, 1.5)
    c.line(100, 206, 100, 330, INK3, 1.5, dash="5 5")
    c.line(100, 330, 595, 330, INK3, 1.5, dash="5 5")
    c.arrow(595, 330, 595, 308, INK3, 1.5)
    c.text(330, 348, "S = HX + U, the holder's own observation", 11.5, "middle", INK2)
    c.text(595, 66, "distortion at most D", 11, "middle", INK2, italic=True)
    c.text(595, 236, "leakage L = I(X; M | S) per symbol", 11, "middle", INK2, italic=True)
    c.save(p)


# ------------------------------------------------------------------ chapter 25
def fig_25_1():
    d = 0.15
    ts = [d * i / 60 for i in range(61)]
    pts = [(2 - h2(t) - h2(2 * d - t), 1 - h2(2 * d - t)) for t in ts]
    assert abs(pts[0][0] - 1.1187) < 1e-4 and abs(pts[0][1] - 0.1187) < 1e-4
    assert abs(pts[-1][0] - 0.7803) < 1e-4 and abs(pts[-1][1] - 0.3902) < 1e-4
    p = reg("ch25_the_reset.md", "25.1",
            "The lower boundary of the rate and reset-content region for two fair bits (A, B) with the reset agent "
            "holding A, at average Hamming distortion D = 0.15 (Proposition 2). Moving along the curve shifts the "
            "allowed error from B to A. The endpoint at the lower right puts all error on B, the bit the reset agent "
            "does not know, and has the least content, 0.1187 bits, at rate 1.1187. The endpoint at the upper left "
            "splits the error evenly and has the least rate, 0.7803 bits, at content 0.3902. Rate and reset content "
            "trade against each other.",
            "## Gaussian sources")
    c = Canvas(720, 400, "Rate against reset content: the two-bit boundary at D = 0.15")
    ax = Axes(c, 70, 52, 540, 280, (0.7, 1.2), (0, 0.45), [0.7, 0.8, 0.9, 1.0, 1.1, 1.2], [0, 0.1, 0.2, 0.3, 0.4],
              "description rate R, bits per symbol", "reset content L, bits")
    poly = [(ax.X(r), ax.Y(l)) for r, l in pts]
    c.polyline(poly, SERIES[0], 2, title="lower boundary")
    for (r, l), lab, anchor, dx, dy in ((pts[0], "all error on B: (1.1187, 0.1187)", "end", 0, 24),
                                        (pts[-1], "error split evenly: (0.7803, 0.3902)", "start", 10, -10)):
        c.dot(ax.X(r), ax.Y(l), SERIES[0], 4.5, title=lab)
        c.text(ax.X(r) + dx, ax.Y(l) + dy, lab, 11, anchor, INK)
    c.text(ax.X(1.0), ax.Y(0.36), "achievable side", 11, "middle", INK3, italic=True)
    c.save(p)


def fig_25_2():
    pflip = 0.05
    ts = list(range(0, 65))
    ls = [h2(0.5 * (1 - (1 - 2 * pflip) ** t)) for t in ts]
    p = reg("ch25_the_reset.md", "25.2",
            "Reset content against the age of the side information, for a record of one fair bit that flips with "
            "probability 0.05 per step (Proposition 6). At age 0 the reset agent knows the bit and the content is 0. "
            "As the side information ages the content rises toward 1 bit, and the predictive information, the "
            "complement, falls toward 0. The curve is the formula of the text, not a measurement; the measured "
            "thresholds are under GO-8 below.",
            "## What is machine-checked")
    c = Canvas(720, 400, "What the reset agent no longer knows, it must pay to erase")
    ax = Axes(c, 70, 52, 540, 280, (0, 64), (0, 1.05), [0, 8, 16, 24, 32, 40, 48, 56, 64], [0, 0.25, 0.5, 0.75, 1],
              "age of the side information, steps", "bits")
    c.polyline([(ax.X(t), ax.Y(v)) for t, v in zip(ts, ls)], SERIES[0], 2, title="reset content")
    c.polyline([(ax.X(t), ax.Y(1 - v)) for t, v in zip(ts, ls)], SERIES[1], 2, title="predictive information")
    legend(c, 70, 40, [("reset content", SERIES[0]), ("predictive information", SERIES[1])])
    c.save(p)


# ------------------------------------------------------------------ chapter 26
def fig_26_1():
    p = reg("ch26_the_complementarity_tax.md", "26.1",
            "The rate floor for one description that serves two reads. Each curve is the set of distortion pairs at "
            "which the floor is met with equality at the stated rate, drawn for a read plane with kappa = 1 (two "
            "orthogonal reads of unit variance). Below a curve the pair cannot be reached at that rate. Lowering one "
            "consumer's distortion at a fixed rate raises the other's. In this case the floor is the joint "
            "rate-distortion function on the whole square shown, since the exactness condition is that both "
            "distortions are at most 1.",
            "## The work floor and the discount")
    c = Canvas(720, 400, "One description, two reads: the floor on the product of distortions")
    ax = Axes(c, 90, 52, 480, 280, (0, 1), (0, 1), [0, 0.25, 0.5, 0.75, 1], [0, 0.25, 0.5, 0.75, 1],
              "distortion of consumer A", "distortion of consumer B")
    for j, r in enumerate([0.5, 1.0, 2.0]):
        k = 2 ** (-2 * r)
        pts = []
        for i in range(0, 201):
            da = k + (1 - k) * i / 200
            pts.append((ax.X(da), ax.Y(k / da)))
        c.polyline(pts, SERIES[j], 2, title=f"R = {r} bits, product {k:g}")
        mid = math.sqrt(k)
        c.text(ax.X(mid) + 8, ax.Y(mid) - 8, f"R = {r:g} bits", 11, "start", INK)
    c.text(ax.X(0.06), ax.Y(0.04), "unreachable", 10.5, "start", INK3, italic=True)
    c.text(600, 120, "product of the two", 11, "start", INK2)
    c.text(600, 136, "distortions at least", 11, "start", INK2)
    c.text(600, 152, "kappa × 2^(−2R)", 11, "start", INK2)
    c.save(p)


# ------------------------------------------------------------------ chapter 27
def fig_27_1():
    p = reg("ch27_access_width.md", "27.1",
            "Three kinds of access the eraser can have to its observation path, with the record made at the marked "
            "time. With path access it holds every sample, and delay alone costs nothing. With prefix access it holds "
            "every sample up to a horizon. With slice access it holds a single sample at a distance Delta from the "
            "record, and the cost rises with Delta. What ages a context is how little of the path is held, not the "
            "delay.",
            "## The dynamic complementarity tax (GO-13)")
    c = Canvas(720, 400, "Access width: which samples of the context the eraser holds")
    x0, x1, n = 150, 650, 21
    rec = 8
    rows = [("path", lambda i: True), ("prefix", lambda i: i <= rec + 5), ("slice", lambda i: i == rec + 5)]
    for r, (name, held) in enumerate(rows):
        y = 110 + 90 * r
        c.line(x0, y, x1, y, GRID, 1)
        c.text(40, y + 4, name + " access", 12, "start", INK, "600")
        for i in range(n):
            x = x0 + (x1 - x0) * i / (n - 1)
            if held(i):
                c.dot(x, y, SERIES[0], 5, title=f"{name}: sample held")
            else:
                c.add(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="4" fill="none" stroke="{INK3}" stroke-width="1"/>')
    xr = x0 + (x1 - x0) * rec / (n - 1)
    xs = x0 + (x1 - x0) * (rec + 5) / (n - 1)
    c.line(xr, 70, xr, 320, CRITICAL, 1.5, dash="5 4")
    c.text(xr, 62, "record made here", 11, "middle", INK)
    c.line(xr, 340, xs, 340, INK2, 1.5)
    c.line(xr, 334, xr, 346, INK2, 1.5)
    c.line(xs, 334, xs, 346, INK2, 1.5)
    c.text((xr + xs) / 2, 358, "distance Delta", 11, "middle", INK2)
    c.arrow(x0, 384, x1, 384, INK3, 1)
    c.text(x1, 378, "time", 10.5, "end", INK3, italic=True)
    legend(c, 150, 40, [("sample held by the eraser", SERIES[0])])
    c.save(p)


# ------------------------------------------------------------------ chapter 28
def fig_28_1():
    mu = [5.0, 3.0, 2.0, 1.0]
    s2 = [10.0, 0.1, 0.1, 0.1]
    lam, k = 1.0, 2

    def j_of(t):
        v = lam * k * t
        for m, s in zip(mu, s2):
            if lam * m < s:
                v += lam * max(m - t, 0.0)
            else:
                v += s * max(1 - t / m, 0.0)
        return v

    assert abs(j_of(0) - 5.3) < 1e-12
    ts = [5.5 * i / 220 for i in range(221)]
    p = reg("ch28_the_adversarial_observer.md", "28.1",
            "The function J(t) of the corrected Theorem 3 on the instance that refuted the sealed statement: weights "
            "(5, 3, 2, 1), value weights (10, 0.1, 0.1, 0.1), price 1, attention budget 2. J is convex and piecewise "
            "linear, and here it rises from t = 0, so the attention water level is 0. The sealed statement placed the "
            "level at one of the weights, marked on the curve, and J is larger at every one of them than its value "
            "5.3 at 0. This is the blackout case the sealed statement missed.",
            "## The discrete twin and Theorems 4 to 6")
    c = Canvas(720, 400, "The level can be zero: J(t) on the refuting instance")
    ax = Axes(c, 70, 52, 540, 280, (0, 5.5), (0, 12), [0, 1, 2, 3, 4, 5], [0, 2, 4, 6, 8, 10, 12],
              "water level t", "J(t)")
    c.polyline([(ax.X(t), ax.Y(j_of(t))) for t in ts], SERIES[0], 2, title="J(t)")
    c.dot(ax.X(0), ax.Y(j_of(0)), CRITICAL, 5, title="minimum, J(0) = 5.3")
    c.text(ax.X(0) + 10, ax.Y(j_of(0)) + 20, "minimum: J(0) = 5.3", 11, "start", INK)
    for m in mu:
        c.dot(ax.X(m), ax.Y(j_of(m)), SERIES[1], 4.5, title=f"t = {m:g}, J = {j_of(m):.3f}")
        c.text(ax.X(m), ax.Y(j_of(m)) - 12, f"{j_of(m):.2f}", 10.5, "middle", INK)
    legend(c, 70, 40, [("J(t)", SERIES[0]), ("J at the weights", SERIES[1])])
    c.save(p)


# ------------------------------------------------------------------ chapter 29
def fig_29_1():
    ang = [0, 30, 60, 90]
    val = [1.000, 1.037, 1.123, 1.149]
    p = reg("ch29_estimation_and_control.md", "29.1",
            "The measured tax for serving two consumers with one sensor schedule, against the principal angle between "
            "their read operators (ledger row GO-EC-6, predicted). The ratio compares the best shared schedule, judged by "
            "the worse-served consumer, with each consumer served alone. It is 1.000 when the two geometries coincide and "
            "1.149 when they are orthogonal. Synthetic systems and planted consumers, one governed run.",
            "## Closed loop at matched control effort")
    c = Canvas(720, 400, "Sharing is free when the consumers agree and costs most when they are orthogonal")
    ax = Axes(c, 70, 52, 540, 280, (-8, 98), (0.95, 1.2), ang, [1.0, 1.05, 1.1, 1.15, 1.2],
              "angle between the two consumers, degrees", "shared over separate")
    pts = [(ax.X(a), ax.Y(v)) for a, v in zip(ang, val)]
    c.polyline(pts, SERIES[0], 2, title="measured ratio")
    for (x, y), v in zip(pts, val):
        c.dot(x, y, SERIES[0], 4.5, title=f"{v:.3f}")
        c.text(x, y - 12, f"{v:.3f}", 11, "middle", INK)
    y1 = ax.Y(1.0)
    c.line(ax.x0, y1, ax.x0 + ax.w, y1, INK3, 1.5, dash="4 4")
    c.text(ax.x0 + ax.w, y1 + 14, "no tax", 10.5, "end", INK2, italic=True)
    c.save(p)


# ------------------------------------------------------------------ embed
def embed():
    for chapter, label, fname, caption, before in FIGS:
        path = os.path.join(CH, chapter)
        with open(path, encoding="utf-8", newline="") as f:
            s = f.read()
        if fname in s:
            continue
        nl = "\r\n" if "\r\n" in s else "\n"
        key = nl + before + nl
        if s.count(key) != 1:
            raise SystemExit(f"{chapter}: heading not found exactly once: {before}")
        block = f"![Figure {label}](figures/{fname}){nl}{nl}*Figure {label}. {caption}*{nl}"
        s = s.replace(key, nl + block + nl + before + nl)
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(s)
        print("embedded", label, "in", chapter)


if __name__ == "__main__":
    for fn in (fig_5_1, fig_7_1, fig_8_1, fig_17_1, fig_17_2, fig_24_1, fig_25_1, fig_25_2, fig_26_1, fig_27_1,
               fig_28_1, fig_29_1):
        fn()
    embed()
    print(len(FIGS), "figures written to", FIG)
