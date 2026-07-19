"""Paper IV figures, drawn from the real held-out sweep numbers (ledger / results JSONs).
No synthetic or illustrative data -- every value traces to a sealed row.
Outputs fig1_dissociation.pdf, fig2_sweep.pdf, fig3_identifiability.pdf next to this file.
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

HERE = os.path.dirname(os.path.abspath(__file__))
plt.rcParams.update({
    "font.family": "serif", "font.size": 9, "axes.linewidth": 0.7,
    "axes.edgecolor": "#555", "xtick.color": "#333", "ytick.color": "#333",
    "axes.labelcolor": "#222", "figure.dpi": 200,
})
R_COL, O_COL = "#2f6f9f", "#d1873b"           # read-preserving / recon-optimal (CVD-safe pair)
TIER = {"sealed": "#2f7d5b", "partial": "#c79127", "null": "#9a5a5a", "verdict": "#4b6cc9"}


def wilson(k, n, z=1.96):
    if n == 0:
        return 0, 0, 0
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return p, max(0, c - h), min(1, c + h)


# ---------------------------------------------------------------- Fig 1: the flip
def fig1():
    doms = ["Legal retrieval\n(virgin split)", "Whale coda\ndialect"]
    dn_R = [0.796, 0.934]; dn_O = [0.780, 0.883]      # downstream AUROC (R wins)
    rc_O = [0.223, 0.431]; rc_R = [0.561, 0.889]      # reconstruction rel-MSE (O wins)
    x = np.arange(len(doms)); w = 0.34
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.6, 2.9))

    a1.bar(x - w/2, dn_R, w, color=R_COL, label="read-preserving (R)")
    a1.bar(x + w/2, dn_O, w, color=O_COL, label="recon-optimal (O)")
    for xi, r, o in zip(x, dn_R, dn_O):
        a1.text(xi - w/2, r + .004, f"{r:.3f}", ha="center", va="bottom", fontsize=7.5, color=R_COL)
        a1.text(xi + w/2, o + .004, f"{o:.3f}", ha="center", va="bottom", fontsize=7.5, color=O_COL)
    a1.set_ylim(0.72, 0.98); a1.set_ylabel("downstream task (AUROC $\\uparrow$)")
    a1.set_title("Downstream: R wins", fontsize=9.5)
    a1.set_xticks(x); a1.set_xticklabels(doms, fontsize=8)
    a1.legend(frameon=False, fontsize=7.5, loc="upper left")

    a2.bar(x - w/2, rc_R, w, color=R_COL); a2.bar(x + w/2, rc_O, w, color=O_COL)
    for xi, r, o in zip(x, rc_R, rc_O):
        a2.text(xi - w/2, r + .01, f"{r:.3f}", ha="center", va="bottom", fontsize=7.5, color=R_COL)
        a2.text(xi + w/2, o + .01, f"{o:.3f}", ha="center", va="bottom", fontsize=7.5, color=O_COL)
    a2.set_ylim(0, 1.02); a2.set_ylabel("reconstruction (rel-MSE $\\downarrow$)")
    a2.set_title("Reconstruction: O wins", fontsize=9.5)
    a2.set_xticks(x); a2.set_xticklabels(doms, fontsize=8)
    for ax in (a1, a2):
        ax.spines[["top", "right"]].set_visible(False)
    fig.suptitle("The flip: at matched bits the two fidelities move oppositely", fontsize=10, y=1.02)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "fig1_dissociation.pdf"), bbox_inches="tight")
    plt.close(fig)


# ---------------------------------------------------------------- Fig 2: domain sweep
def fig2():
    # (label, physics, k, n, tier) -- held-out flip fraction; A2 keys = worse-arm 16/16
    rows = [
        ("Synthetic ULA", "synthetic", 6, 6, "sealed"),
        ("LLM keys (Llama-3.2)", "neural", 16, 16, "sealed"),
        ("LOCATA acoustic", "acoustic", 11, 13, "sealed"),
        ("AV16.3 acoustic", "acoustic", 148, 201, "sealed"),
        ("PDAR seismic", "seismic", 13, 17, "sealed"),
        ("Legal retrieval", "retrieval", 200, 200, "sealed"),
        ("Whale codas", "bioacoustic", 300, 300, "sealed"),
        ("RaDICaL radar", "EM/radar", 25, 25, "partial"),
        ("Gradient optim.", "optimization", 82, 300, "null"),
    ]
    rows = rows[::-1]
    fig, ax = plt.subplots(figsize=(6.6, 3.8))
    for i, (lab, phys, k, n, tier) in enumerate(rows):
        p, lo, hi = wilson(k, n)
        ax.plot([lo, hi], [i, i], color=TIER[tier], lw=1.6, zorder=1, solid_capstyle="round")
        ax.scatter([p], [i], s=34, color=TIER[tier], zorder=3, edgecolor="white", linewidth=.6)
        ax.text(1.015, i, f"{k}/{n}", va="center", fontsize=7.3, color="#555")
        ax.text(-0.02, i, f"{lab}  ", va="center", ha="right", fontsize=8.2)
        ax.text(hi + 0.0, i + 0.28, phys, va="center", fontsize=6.3, color="#999", style="italic")
    ax.axvline(0.5, color="#bbb", ls=":", lw=0.8, zorder=0)
    ax.text(0.5, len(rows) - 0.3, "chance", fontsize=6.5, color="#999", ha="center")
    ax.set_xlim(0, 1.14); ax.set_ylim(-0.7, len(rows) - 0.2)
    ax.set_yticks([]); ax.set_xlabel("held-out flip fraction (Wilson 95% CI)")
    ax.set_xticks([0, .25, .5, .75, 1.0])
    ax.spines[["top", "right", "left"]].set_visible(False)
    leg = [Patch(color=TIER["sealed"], label="sealed confirmation"),
           Patch(color=TIER["partial"], label="partial (data-limited)"),
           Patch(color=TIER["null"], label="sealed null (coupling)")]
    ax.legend(handles=leg, frameon=False, fontsize=7.6, loc="upper left", bbox_to_anchor=(0.0, 0.62))
    ax.set_title("The flip across nine pre-registered domains", fontsize=10)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "fig2_sweep.pdf"), bbox_inches="tight")
    plt.close(fig)


# ------------------------------------------------------ Fig 3: identifiability (legal)
def fig3():
    stages = ["035\nestimated read op\n(MISS)", "036\nblind probe\n(same held-out)", "039\nblind probe\n(virgin split)"]
    R = [0.757, 0.779, 0.796]; O = [0.773, 0.771, 0.780]
    x = np.arange(3)
    fig, ax = plt.subplots(figsize=(4.7, 3.0))
    ax.plot(x, R, "-o", color=R_COL, lw=1.8, ms=6, label="read-preserving (R)")
    ax.plot(x, O, "-s", color=O_COL, lw=1.8, ms=5.5, label="recon-optimal (O)")
    for xi, r, o in zip(x, R, O):
        ax.annotate(f"{r:.3f}", (xi, r), textcoords="offset points", xytext=(0, 7), ha="center", fontsize=7.3, color=R_COL)
        ax.annotate(f"{o:.3f}", (xi, o), textcoords="offset points", xytext=(0, -12), ha="center", fontsize=7.3, color=O_COL)
    ax.axvspan(-0.4, 0.4, color="#f2e3e3", zorder=0)   # miss region
    ax.text(0, 0.744, "O beats R\n(overfit read op)", ha="center", fontsize=6.8, color="#9a5a5a")
    ax.set_xticks(x); ax.set_xticklabels(stages, fontsize=7.6)
    ax.set_ylim(0.74, 0.80); ax.set_ylabel("held-out AUROC")
    ax.set_title("Recovering the read operator makes the flip transfer", fontsize=9.5)
    ax.legend(frameon=False, fontsize=7.8, loc="lower right")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "fig3_identifiability.pdf"), bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    fig1(); fig2(); fig3()
    print("wrote fig1_dissociation.pdf, fig2_sweep.pdf, fig3_identifiability.pdf")
