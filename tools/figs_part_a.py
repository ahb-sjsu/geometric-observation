"""Figures for Chapters 1 to 4, 6 and 9 to 11 (Parts I, II and IV, and the third shadow).

Chapters 5, 7 and 8 have their figures in figs_core.py. Every figure here is a schematic of a
structure the chapter states, a curve computed from a formula the chapter states, or a plot of
numbers printed in the chapter.
"""

import math

from figkit import Axes, BORDER, BOX, Canvas, CRITICAL, GRID, INK, INK2, INK3, SERIES, legend, reg


def _canvas(w, h, title):
    assert len(title) <= 68, (len(title), title)
    return Canvas(w, h, title)


def _dash(c, pts, stroke, width=1.5, dash="5 5"):
    for (x1, y1), (x2, y2) in zip(pts[:-1], pts[1:]):
        c.line(x1, y1, x2, y2, stroke, width, dash=dash)


# ------------------------------------------------------------------ chapter 1
def fig_1_1():
    p = reg("chapters/ch01_why_observation_needs_a_theory.md", "1.1",
            "A schematic of the two places a code can be scored. Reconstruction error compares the object x with its "
            "reconstruction and stops there, so it names no consumer. The read distortion scores the same coding error "
            "after weighting it by the read metric, the output metric G pulled back through the consumer's Jacobian J. "
            "The consumer, the output metric and the budget together are the observer.",
            "## One object, three shadows")
    c = _canvas(720, 400, "The same coding error, scored in two places")
    y, h = 128, 54
    boxes = [(24, 100, "object x", None), (164, 110, "compressor", "spends budget B"),
             (314, 110, "reconstruction x̂", "x plus error δ"), (464, 110, "consumer C", "Jacobian J"),
             (614, 90, "output", "scored by G")]
    for x, w, lab, sub in boxes:
        c.box(x, y, w, h, lab, sub)
    for (x, w, _, _), (x2, _, _, _) in zip(boxes[:-1], boxes[1:]):
        c.arrow(x + w + 3, y + h / 2, x2 - 3, y + h / 2, INK2, 1.5)
    # the observer: consumer, output metric, budget
    c.line(464, 104, 704, 104, INK3, 1.5)
    c.line(464, 104, 464, 112, INK3, 1.5)
    c.line(704, 104, 704, 112, INK3, 1.5)
    c.text(584, 94, "observer O = (C, G, B)", 11.5, "middle", INK)
    # reconstruction error: object to reconstruction
    xa, xb, xc = 74, 369, 659
    yb = 214
    c.line(xa, yb, xb, yb, SERIES[1], 2)
    c.line(xa, yb - 7, xa, yb + 7, SERIES[1], 2)
    c.line(xb, yb - 7, xb, yb + 7, SERIES[1], 2)
    c.text((xa + xb) / 2, yb + 22, "reconstruction error  tr(Σ)", 12, "middle", INK, "600")
    c.text((xa + xb) / 2, yb + 40, "compares x with x̂; names no consumer", 11, "middle", INK2)
    # read distortion: object to scored output
    yr = 296
    c.line(xa, yr, xc, yr, SERIES[0], 2)
    c.line(xa, yr - 7, xa, yr + 7, SERIES[0], 2)
    c.line(xc, yr - 7, xc, yr + 7, SERIES[0], 2)
    c.text((xa + xc) / 2, yr + 22, "read distortion  tr(P Σ),  with read metric P = JᵀGJ", 12, "middle", INK, "600")
    c.text((xa + xc) / 2, yr + 40, "the same error, counted where the consumer looks", 11, "middle", INK2)
    c.text(16, 390, "Σ is the covariance of the coding error δ; schematic", 10.5, "start", INK3, italic=True)
    c.save(p)


# ------------------------------------------------------------------ chapter 2
def fig_2_1():
    a, b = (0.3, 1.7), (1.7, 0.3)          # the two error covariances of Figure 5.1, diagonal entries

    def read(err, w):                       # tr(P Sigma) for P = diag(1, w)
        return err[0] + w * err[1]

    assert abs(read(a, 1) - sum(a)) < 1e-12 and abs(read(b, 1) - sum(b)) < 1e-12 and abs(sum(a) - 2) < 1e-12
    assert all(abs(read(a, w / 10) - sum(a)) > 1e-9 for w in range(10))
    p = reg("chapters/ch02_failure_of_observer_free_measurement.md", "2.1",
            "Reconstruction error as one slice of a family. The two codes are the errors A and B of Figure 5.1, with "
            "covariances diag(0.3, 1.7) and diag(1.7, 0.3), so both have reconstruction error 2. The horizontal axis is "
            "the weight w that a consumer with read metric diag(1, w) gives the second direction, and the vertical axis "
            "is the read distortion. The two measures agree only at w = 1, where the read metric is the identity, and "
            "there the two codes tie. The values are illustrative, not measured.",
            "## What the failure looks like in the wild")
    c = _canvas(720, 400, "Reconstruction error is one slice of a family of read distortions")
    ax = Axes(c, 70, 52, 520, 280, (0, 1), (0, 2.2), [0, 0.25, 0.5, 0.75, 1], [0, 0.5, 1, 1.5, 2],
              "weight w on the second direction; read metric P = diag(1, w)", "read distortion tr(P Σ)")
    y2 = ax.Y(2)
    c.line(ax.x0, y2, ax.x0 + ax.w, y2, INK3, 1.5, dash="4 4")
    c.text(ax.x0 + 6, y2 - 7, "reconstruction error of both codes = 2", 10.5, "start", INK2, italic=True)
    for j, (name, err) in enumerate((("code A", a), ("code B", b))):
        c.polyline([(ax.X(0), ax.Y(read(err, 0))), (ax.X(1), ax.Y(read(err, 1)))], SERIES[j], 2,
                   title=f"{name}: {err[0]} + {err[1]} w")
        c.dot(ax.X(0), ax.Y(read(err, 0)), SERIES[j], 4.5, title=f"{name} at w = 0: {err[0]}")
        c.text(ax.X(0) + 10, ax.Y(read(err, 0)) + (18 if j == 0 else 18), f"{err[0]} at w = 0", 11, "start", INK)
    c.dot(ax.X(1), y2, CRITICAL, 5.5, title="P = I: read distortion equals reconstruction error")
    c.text(ax.X(1) + 12, y2 - 6, "P = I", 12, "start", INK, "600")
    c.text(ax.X(1) + 12, y2 + 10, "the slice", 11, "start", INK2)
    c.text(ax.X(1) + 12, y2 + 25, "MSE assumes", 11, "start", INK2)
    legend(c, 70, 40, [("code A, error diag(0.3, 1.7)", SERIES[0]), ("code B, error diag(1.7, 0.3)", SERIES[1])])
    c.save(p)


# ------------------------------------------------------------------ chapter 3
def fig_3_1():
    p = reg("chapters/ch03_historical_precursors.md", "3.1",
            "A schematic of the lineage the chapter sets out. Each of four older subjects supplies one part of the "
            "read metric, named under it. The book claims none of the parts. What it adds is the load placed on the "
            "operator, shown on the right.",
            "## The lineage, in one sentence")
    c = _canvas(720, 420, "Four older subjects each own part of the read metric")
    src = [("Shannon, rate-distortion theory", "the purpose: compress to a fidelity"),
           ("Perceptual and weighted coding", "the fidelity measure is a free variable"),
           ("Čencov and Amari", "the algebra: the pullback metric"),
           ("von Luxburg, Radl, Hein; Ng, Jordan, Weiss", "the puzzle: the collapse and its resolution")]
    x0, w0, h0 = 20, 290, 56
    mx, my, mw, mh = 372, 187, 130, 62
    for i, (lab, sub) in enumerate(src):
        y = 62 + 84 * i
        c.box(x0, y, w0, h0, lab, sub)
        ty = my + mh * (i + 1) / 5
        c.arrow(x0 + w0 + 3, y + h0 / 2, mx - 4, ty, INK2, 1.5)
    c.add(f'<rect x="{mx}" y="{my}" width="{mw}" height="{mh}" rx="6" fill="{BOX}" stroke="{SERIES[0]}" stroke-width="2"/>')
    c.text(mx + mw / 2, my + 27, "read metric", 13, "middle", INK, "600")
    c.text(mx + mw / 2, my + 46, "P = JᵀGJ", 12, "middle", INK2)
    rx, ry, rw, rh = 544, 150, 160, 136
    c.arrow(mx + mw + 3, my + mh / 2, rx - 4, my + mh / 2, INK2, 1.5)
    c.add(f'<rect x="{rx}" y="{ry}" width="{rw}" height="{rh}" rx="6" fill="{BOX}" stroke="{BORDER}" stroke-width="1"/>')
    c.text(rx + rw / 2, ry + 24, "the load it is asked to bear", 11.5, "middle", INK, "600")
    for i, s in enumerate(("one operator for lossy", "representation across", "compression, embedding", "and physical estimation,",
                           "stated so it can fail")):
        c.text(rx + rw / 2, ry + 46 + 17 * i, s, 11, "middle", INK2)
    c.text(x0 + w0 / 2, 404, "the components: old, and not claimed", 10.5, "middle", INK3, italic=True)
    c.text(rx + rw / 2, 404, "the claim of the book", 10.5, "middle", INK3, italic=True)
    c.save(p)


# ------------------------------------------------------------------ chapter 4
def fig_4_1():
    ang = math.radians(30)
    v = (math.cos(ang), math.sin(ang))           # read direction; P = v v^T
    k = (-math.sin(ang), math.cos(ang))          # kernel of P
    classes = [(-1.5, (0.8, -1.0)), (-0.3, (1.4, -0.4, -1.5)), (0.9, (0.3,)), (1.7, (1.0, -0.9))]
    for s, ts in classes:                        # differences inside a class lie in the kernel: v . delta = 0
        pts = [(s * v[0] + t * k[0], s * v[1] + t * k[1]) for t in ts]
        for q in pts[1:]:
            assert abs((q[0] - pts[0][0]) * v[0] + (q[1] - pts[0][1]) * v[1]) < 1e-12
    p = reg("chapters/ch04_the_observer_triple.md", "4.1",
            "The quotient for a consumer that reads one direction of a plane, drawn at 30 degrees. Left: eight inputs. "
            "Inputs joined by a dashed line differ only along the kernel of the read metric, so the consumer cannot "
            "tell them apart. Right: the quotient, in which each dashed line has become a single point, and the eight "
            "inputs are four. The read metric says how finely the read direction is resolved, and the quotient is the "
            "world the observer acts on. The points are illustrative.",
            "## The consumer table")
    c = _canvas(720, 400, "The quotient: inputs the consumer cannot tell apart become one")
    cx, cy, sc = 200, 222, 56

    def scr(x, y):
        return cx + sc * x, cy - sc * y

    c.line(cx - 150, cy, cx + 150, cy, GRID, 1)
    c.line(cx, cy - 150, cx, cy + 150, GRID, 1)
    x1, y1 = scr(-2.45 * v[0], -2.45 * v[1])
    x2, y2 = scr(2.6 * v[0], 2.6 * v[1])
    c.arrow(x1, y1, x2, y2, INK, 2)
    c.text(x2 + 6, y2 - 6, "read direction", 11.5, "start", INK)
    qx0, qx1, qy = 452, 690, 222
    c.arrow(qx0, qy, qx1, qy, INK, 2)
    for j, (s, ts) in enumerate(classes):
        col = SERIES[j]
        lo, hi = min(ts) - 0.35, max(ts) + 0.35
        ax_, ay_ = scr(s * v[0] + lo * k[0], s * v[1] + lo * k[1])
        bx_, by_ = scr(s * v[0] + hi * k[0], s * v[1] + hi * k[1])
        c.line(ax_, ay_, bx_, by_, col, 1.5, dash="5 5", opacity=0.8)
        for t in ts:
            px, py = scr(s * v[0] + t * k[0], s * v[1] + t * k[1])
            c.dot(px, py, col, 5, title=f"input with read coordinate {s}")
        qx = qx0 + 16 + (qx1 - qx0 - 44) * (s + 1.5) / 3.2
        c.dot(qx, qy, col, 6.5, title=f"class of {len(ts)} input(s), read coordinate {s}")
        c.text(qx, qy - 16, f"{len(ts)} input" + ("s" if len(ts) > 1 else ""), 10.5, "middle", INK2)
    kx, ky = scr(-0.3 * v[0] + 1.75 * k[0], -0.3 * v[1] + 1.75 * k[1])
    c.text(kx - 8, ky - 4, "kernel direction: not read", 11, "middle", INK2)
    c.text(cx, 372, "the space of inputs X", 11.5, "middle", INK, "600")
    c.text((qx0 + qx1) / 2, qy + 34, "the quotient of X by the kernel", 11.5, "middle", INK, "600")
    c.text((qx0 + qx1) / 2, qy + 52, "one coordinate is left: the one read", 11, "middle", INK2)
    c.arrow(368, 306, 436, 306, INK3, 1.5)
    c.text(402, 296, "identify", 11, "middle", INK2)
    c.save(p)


# ------------------------------------------------------------------ chapter 6
def fig_6_1():
    def read(e1, e2, deg):                       # tr(P Sigma), P = diag(1, 0), Sigma = R diag(e1, e2) R^T
        t = math.radians(deg)
        return e1 * math.cos(t) ** 2 + e2 * math.sin(t) ** 2

    errs = [((1.7, 0.3), "eigenvalues 1.7, 0.3"), ((1.95, 0.05), "eigenvalues 1.95, 0.05"), ((1.0, 1.0), "eigenvalues 1, 1")]
    for (e1, e2), _ in errs:
        assert abs(e1 + e2 - 2) < 1e-12          # rotation leaves the trace at 2
    p = reg("chapters/ch06_mathematical_preliminaries.md", "6.1",
            "The lemma drawn for a consumer that reads one direction of a plane. Each curve is an error covariance of "
            "fixed magnitude, trace 2, rotated through the angle on the horizontal axis; the vertical axis is the read "
            "distortion. The magnitude never changes and the read distortion does. Between the two extreme "
            "orientations it changes by a factor of 5.7 for eigenvalues (1.7, 0.3) and 39 for (1.95, 0.05), and the "
            "factor grows without limit as the error is made thinner. Only the isotropic error is indifferent to "
            "orientation. The values are illustrative.",
            "## The output metric $G$, concretely")
    c = _canvas(720, 400, "Same error magnitude, different read distortion: orientation decides")
    ax = Axes(c, 70, 52, 480, 280, (0, 90), (0, 2.2), [0, 15, 30, 45, 60, 75, 90], [0, 0.5, 1, 1.5, 2],
              "angle between the error's long axis and the read direction, degrees", "read distortion tr(P Σ)")
    y2 = ax.Y(2)
    c.line(ax.x0, y2, ax.x0 + ax.w, y2, INK3, 1.5, dash="4 4")
    c.text(ax.x0 + ax.w + 10, y2 + 4, "magnitude tr(Σ) = 2", 11, "start", INK)
    c.text(ax.x0 + ax.w + 10, y2 + 19, "at every angle", 10.5, "start", INK2)
    for j, ((e1, e2), name) in enumerate(errs):
        c.polyline([(ax.X(d), ax.Y(read(e1, e2, d))) for d in range(0, 91)], SERIES[j], 2, title=name)
        c.dot(ax.X(90), ax.Y(e2), SERIES[j], 4.5, title=f"{name}: {e2} at 90 degrees")
        if e1 != e2:
            assert abs(e1 / e2 - (5.667 if j == 0 else 39.0)) < 1e-3
            c.text(ax.X(90) + 10, ax.Y(e2) + (-3 if j == 0 else 7), f"{e2:g}, a factor of {e1 / e2:.2g} below", 10.5, "start", INK)
        else:
            c.text(ax.X(90) + 10, ax.Y(e2) + 4, "1 throughout", 10.5, "start", INK)
    legend(c, 70, 40, [(n, SERIES[j]) for j, (_, n) in enumerate(errs)])
    c.save(p)


# ------------------------------------------------------------------ chapter 9
def fig_9_1():
    n = 12
    th = [2 * math.pi * i / n for i in range(n)]
    rad = [1 + 0.42 * math.sin(2 * t + 0.6) for t in th]          # illustrative radii
    p = reg("chapters/ch09_legibility.md", "9.1",
            "A schematic of the polar form x = r u. Twelve embedding points are drawn with radii that vary from point "
            "to point, as the radius does when it carries degree and density. Row normalization moves each point "
            "along its ray onto the unit circle, which keeps the direction u and discards the radius r. At one point "
            "the two components of a motion are marked: the tangential part turns u and is read by the geodesic-rank "
            "consumer, and the radial part changes only r and is not. The radii are illustrative.",
            "## The exactly-solvable cases")
    c = _canvas(720, 400, "Keep the angle: row normalization drops the radius, not the angle")
    cx, cy, R = 215, 218, 98

    def scr(r, t):
        return cx + R * r * math.cos(t), cy - R * r * math.sin(t)

    c.add(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{INK3}" stroke-width="1.5"/>')
    for t, r in zip(th, rad):
        x, y = scr(r, t)
        c.line(cx, cy, *scr(max(r, 1), t), stroke=GRID, width=1)
        ux, uy = scr(1, t)
        c.line(x, y, ux, uy, INK2, 1.5, dash="3 3")
    for t, r in zip(th, rad):
        c.dot(*scr(1, t), SERIES[0], 4.5, title="direction u, on the unit circle")
        c.dot(*scr(r, t), SERIES[1], 4.5, title=f"embedding point, radius {r:.2f}")
    c.dot(cx, cy, INK3, 2)
    # components of a motion at the point on the horizontal ray
    x, y = scr(rad[0], th[0])
    c.arrow(x, y, x + 46, y, INK, 1.8)
    c.arrow(x, y, x, y - 46, INK, 1.8)
    c.dot(x, y, SERIES[1], 4.5)
    c.text(x + 54, y + 4, "radial: changes r only", 11, "start", INK)
    c.text(x + 8, y - 52, "tangential: turns u", 11, "start", INK)
    tx = 470
    c.text(tx, 96, "x = r u", 13, "start", INK, "600")
    c.text(tx, 118, "radius r: degree and density,", 11.5, "start", INK2)
    c.text(tx, 134, "the nuisance, in the kernel", 11.5, "start", INK2)
    c.text(tx, 156, "direction u: the graph geodesics,", 11.5, "start", INK2)
    c.text(tx, 172, "the coordinate that is read", 11.5, "start", INK2)
    c.text(tx, 300, "row normalization: x to u,", 11.5, "start", INK2)
    c.text(tx, 316, "along the dotted segments", 11.5, "start", INK2)
    legend(c, 16, 384, [("embedding point x", SERIES[1]), ("its direction u on the unit circle", SERIES[0])])
    c.text(704, 384, "schematic", 10.5, "end", INK3, italic=True)
    c.save(p)


# ------------------------------------------------------------------ chapter 10
def fig_10_1():
    ang = math.radians(30)
    w = (math.cos(ang), math.sin(ang))            # planted read direction

    def cons(x, y):
        return math.tanh(w[0] * x + w[1] * y)

    h = 1e-4
    grid = [-1.5, -0.5, 0.5, 1.5]
    pts = [(x, y) for x in grid for y in grid]
    gs = [((cons(x + h, y) - cons(x - h, y)) / (2 * h), (cons(x, y + h) - cons(x, y - h)) / (2 * h)) for x, y in pts]
    sxx = sum(g[0] * g[0] for g in gs) / len(gs)
    sxy = sum(g[0] * g[1] for g in gs) / len(gs)
    syy = sum(g[1] * g[1] for g in gs) / len(gs)
    tr, det = sxx + syy, sxx * syy - sxy * sxy
    l1 = tr / 2 + math.sqrt(max(tr * tr / 4 - det, 0))
    l2 = tr - l1
    e = (sxy, l1 - sxx)
    ne = math.hypot(*e)
    e = (e[0] / ne, e[1] / ne)
    overlap = abs(e[0] * w[0] + e[1] * w[1])
    assert overlap > 1 - 1e-6 and abs(l2) < 1e-6 * l1
    if e[0] * w[0] + e[1] * w[1] < 0:
        e = (-e[0], -e[1])
    p = reg("chapters/ch10_the_blind_probe.md", "10.1",
            "The probe worked on a planted consumer in a plane, C(x) = tanh(w·x) with w at 30 degrees. The thin lines "
            "are level sets of C. At sixteen operating points the gradient g is taken by finite differences of the "
            "output alone and drawn as a stroke. Every stroke points the same way, and where the consumer saturates "
            "the strokes shrink. The margin sensitivity S, the average of g gᵀ, has one nonzero eigenvalue, and its "
            "top eigenvector is the planted direction. This illustrates the mechanism and is not the GO-1 measurement.",
            "## What the probe can promise: GO-1")
    c = _canvas(720, 400, "Poke the consumer, average the gradients, read off the direction")
    ax = Axes(c, 60, 56, 286, 286, (-2, 2), (-2, 2), [-2, -1, 0, 1, 2], [-2, -1, 0, 1, 2], "x1", "x2")
    kx, ky = -w[1], w[0]
    for i in range(-5, 6):                          # level sets w.x = i/2, clipped to the square
        s = i / 2
        seg = []
        for j in range(-400, 401):
            t = j / 100
            x, y = s * w[0] + t * kx, s * w[1] + t * ky
            if abs(x) <= 2 and abs(y) <= 2:
                seg.append((ax.X(x), ax.Y(y)))
        if len(seg) > 1:
            c.line(*seg[0], *seg[-1], stroke="#3d7868", width=1.2)
    c.arrow(ax.X(0), ax.Y(0), ax.X(1.72 * e[0]), ax.Y(1.72 * e[1]), CRITICAL, 2.6)
    gmax = max(math.hypot(*g) for g in gs)
    for (x, y), g in zip(pts, gs):
        L = 30 / gmax
        c.line(ax.X(x), ax.Y(y), ax.X(x) + L * g[0], ax.Y(y) - L * g[1], SERIES[1], 3)
        c.dot(ax.X(x), ax.Y(y), INK, 2.2, title=f"g = ({g[0]:.3f}, {g[1]:.3f})")
    tx = 392
    c.text(tx, 92, "consumer  C(x) = tanh(w·x)", 12, "start", INK, "600")
    c.text(tx, 112, "queried only through its output", 11.5, "start", INK2)
    c.text(tx, 150, "margin sensitivity  S = E[g gᵀ]", 12, "start", INK, "600")
    c.text(tx, 170, f"eigenvalues {l1:.3f} and {abs(l2):.3f}", 11.5, "start", INK2)
    c.text(tx, 188, "one direction is read", 11.5, "start", INK2)
    c.text(tx, 226, "top eigenvector of S", 12, "start", INK, "600")
    c.text(tx, 246, f"overlap with the planted w: {overlap:.3f}", 11.5, "start", INK2)
    c.text(tx, 264, "no label and no oracle direction used", 11.5, "start", INK2)
    for i, (lab, col) in enumerate((("level sets of C", "#3d7868"), ("gradient g, by finite differences", SERIES[1]),
                                    ("top eigenvector of S", CRITICAL))):
        legend(c, tx, 304 + 20 * i, [(lab, col)])
    c.save(p)


def fig_10_2():
    rows = [("035", "document covariance", "[refuted]", 0.757, 0.773, 0.016, "flip failed"),
            ("036", "blind probe, same held-out data", "[demonstrated]", 0.779, 0.771, 0.008, "flip 200/200"),
            ("039", "blind probe, fresh split", "[demonstrated]", 0.796, 0.780, 0.016, "flip 200/200")]
    for _, _, _, r, o, d, _ in rows:
        assert abs(abs(r - o) - d) < 1e-9
    assert rows[0][3] < rows[0][4] and rows[1][3] > rows[1][4] and rows[2][3] > rows[2][4]
    p = reg("chapters/ch10_the_blind_probe.md", "10.2",
            "The three legal-retrieval tests, with the downstream scores printed in the text for the read-preserving "
            "code R and the reconstruction-optimal code O. In 035 the read operator was the document covariance and O "
            "beat R: the flip failed [refuted]. In 036 the operator came from the blind probe and, on the same "
            "held-out data, R beat O by 0.008 [demonstrated, GO-P-2026-036, 4/4]. In 039 the frozen recipe on a fresh "
            "opinion-disjoint split gave R over O by 0.016 [demonstrated, GO-P-2026-039]. The horizontal axis starts "
            "at 0.74, not at zero.",
            "## What the probe cannot promise")
    c = _canvas(720, 330, "The blind probe restores the flip that a covariance estimate lost")
    ax = Axes(c, 238, 62, 300, 180, (0.74, 0.81), (0, 3), [0.74, 0.76, 0.78, 0.80], [],
              "downstream score on the held-out set, as printed", "")
    for v in (0.74, 0.76, 0.78, 0.80):
        c.line(ax.X(v), ax.y0, ax.X(v), ax.y0 + ax.h, GRID, 1)
    for i, (num, how, cls, r, o, d, note) in enumerate(rows):
        y = ax.y0 + 60 * (i + 0.5)
        c.text(16, y - 6, f"{num}: {how}", 11.5, "start", INK, "600")
        c.text(16, y + 11, cls, 11, "start", INK2)
        xr, xo = ax.X(r), ax.X(o)
        c.line(xr, y, xo, y, CRITICAL if r < o else INK3, 2)
        c.dot(xr, y, SERIES[0], 5.5, title=f"{num}: R = {r:.3f}")
        c.dot(xo, y, SERIES[1], 5.5, title=f"{num}: O = {o:.3f}")
        for x, val, left in ((xr, r, r < o), (xo, o, o < r)):
            c.text(x + (-11 if left else 11), y + 4, f"{val:.3f}", 10.5, "end" if left else "start", INK)
        c.text(ax.x0 + ax.w + 22, y - 3, ("R below O by " if r < o else "R above O by ") + f"{d:.3f}", 11, "start", INK)
        c.text(ax.x0 + ax.w + 22, y + 13, note, 10.5, "start", INK2)
    legend(c, 238, 46, [("read-preserving code, R", SERIES[0]), ("reconstruction-optimal code, O", SERIES[1])])
    c.save(p)


# ------------------------------------------------------------------ chapter 11
def fig_11_1():
    lam_max = 400
    spaces = []
    # circle S^1: eigenvalue k^2, multiplicity 2 (1 at k = 0)
    spaces.append(("circle S¹", 1, [(k * k, 1 if k == 0 else 2) for k in range(0, 21)], 2.0))
    # sphere S^2: eigenvalue l(l+1), multiplicity 2l+1
    spaces.append(("sphere S²", 2, [(l * (l + 1), 2 * l + 1) for l in range(0, 20)], 1.0))
    # flat torus T^2 with unit lattice: eigenvalue a^2 + b^2
    tor = {}
    for a_ in range(-20, 21):
        for b_ in range(-20, 21):
            if a_ * a_ + b_ * b_ <= lam_max:
                tor[a_ * a_ + b_ * b_] = tor.get(a_ * a_ + b_ * b_, 0) + 1
    spaces.append(("flat torus T²", 2, sorted(tor.items()), math.pi))
    # sphere S^3: eigenvalue l(l+2), multiplicity (l+1)^2
    spaces.append(("sphere S³", 3, [(l * (l + 2), (l + 1) ** 2) for l in range(0, 20)], 1 / 3))
    assert [m for _, m in spaces[1][2][:4]] == [1, 3, 5, 7] and [m for _, m in spaces[2][2][:4]] == [1, 4, 4, 4]
    p = reg("chapters/ch11_the_recognizer.md", "11.1",
            "The Weyl law of the text on four spaces whose Laplacian spectra are known in closed form. The horizontal "
            "axis is the threshold λ and the vertical axis is the number of eigenvalues at or below it, both on "
            "logarithmic scales, so the slope of each staircase is d/2. The dashed lines are the Weyl leading terms. "
            "The sphere and the flat torus are both of dimension 2 and climb at the same slope. They differ in the "
            "constant and in the sizes of the steps, 1, 3, 5, 7 for the sphere and 1, 4, 4, 4 for the torus, which is "
            "the shape. This is an illustration from known spectra, not a measurement by the recognizer.",
            "## The certificate and its vacuity threshold (GO-3)")
    c = _canvas(720, 400, "The spectrum's growth rate gives the dimension before the shape")
    ax = Axes(c, 70, 52, 480, 280, (0.7, lam_max), (0.8, 5000), [1, 10, 100], [1, 10, 100, 1000],
              "eigenvalue threshold λ (logarithmic scale)", "eigenvalues at or below λ", xlog=True, ylog=True)
    order = [0, 1, 2, 3]
    ends = {}
    for j in order:
        name, d, spec, cw = spaces[j]
        spec = [(ev, m) for ev, m in spec if ev <= lam_max]
        _dash(c, [(ax.X(x), ax.Y(cw * x ** (d / 2))) for x in (max(1.0, (0.8 / cw) ** (2 / d)), lam_max)], INK3, 1.2, "4 4")
        pts, cnt = [], 0
        for ev, m in spec:
            if ev == 0:
                cnt = m
                pts.append((ax.X(0.7), ax.Y(cnt)))
                continue
            pts.append((ax.X(ev), ax.Y(cnt)))
            cnt += m
            pts.append((ax.X(ev), ax.Y(cnt)))
        pts.append((ax.X(lam_max), ax.Y(cnt)))
        assert abs(cnt / (cw * lam_max ** (d / 2)) - 1) < 0.15      # the staircase follows its Weyl term
        c.polyline(pts, SERIES[j], 2, title=f"{name}, d = {d}")
        ends[j] = cnt
    for j in order:
        name, d, _, _ = spaces[j]
        y = ax.Y(ends[j])
        c.text(ax.x0 + ax.w + 10, y + 4, f"{name}, d = {d}", 11.5, "start", INK)
    legend(c, 70, 40, [("counting function", INK2)])
    c.line(250, 37, 274, 37, INK3, 1.2, dash="4 4")
    c.text(282, 41, "Weyl leading term, a constant times λ^(d/2)", 11.5, "start", INK2)
    c.save(p)
