"""
Render the figures used in Section 3 of the report.

Design notes
    - Two series only, coloured with an Okabe-Ito blue/vermillion pair that passes
      colour-vision-deficiency separation (worst adjacent dE 21.9 protan).
    - Identity is never carried by colour alone: each model also gets its own line
      style, so the figures survive greyscale printing.
    - Grid and axes are recessive; labels use ink colours, not series colours.
"""

import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import precision_recall_curve, roc_curve

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RES = os.path.join(ROOT, "results")
IMG = os.path.join(ROOT, "img")
os.makedirs(IMG, exist_ok=True)

MODELS = ["Linear SVM", "Neural network (MLP)"]
STYLE = {
    "Linear SVM":           {"color": "#0072B2", "ls": "-",  "lw": 2.0},
    "Neural network (MLP)": {"color": "#D55E00", "ls": "--", "lw": 2.0},
}
INK = "#1a1a1a"
MUTED = "#6b6b6b"
GRID = "#dcdcdc"

plt.rcParams.update({
    "font.size": 9,
    "axes.edgecolor": MUTED,
    "axes.labelcolor": INK,
    "text.color": INK,
    "xtick.color": MUTED,
    "ytick.color": MUTED,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.dpi": 200,
})

with open(os.path.join(RES, "results.json")) as f:
    R = json.load(f)

CORPORA = [("davidson", "Dataset A: Davidson (hate speech)"),
           ("wikipedia", "Dataset B: Wikipedia (toxicity)")]


def load_curves(corpus):
    z = np.load(os.path.join(RES, f"curves_{corpus}.npz"))
    return {m: (z[f"{m}_y"], z[f"{m}_s"]) for m in MODELS}


def tidy(ax):
    ax.grid(True, color=GRID, linewidth=0.6, alpha=0.9)
    ax.set_axisbelow(True)


# ---------------------------------------------------------------- Figure 1: PR
fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.1))
for ax, (corpus, title) in zip(axes, CORPORA):
    curves = load_curves(corpus)
    base = R["config"][f"{corpus}_pos_rate"]
    for m in MODELS:
        y, s = curves[m]
        prec, rec, _ = precision_recall_curve(y, s)
        auc = np.mean([f["pr_auc"] for f in R[corpus]["per_fold"][m]])
        ax.plot(rec, prec, label=f"{m} (PR-AUC {auc:.3f})", **STYLE[m])
    ax.axhline(base, color=MUTED, ls=":", lw=1.2)
    ax.annotate(f"base rate {base * 100:.1f}%", xy=(0.98, base), xytext=(0.98, base + 0.05),
                ha="right", fontsize=7.5, color=MUTED)
    ax.set_xlabel("Recall")
    ax.set_ylabel("Precision")
    ax.set_title(title, fontsize=9, color=INK)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.02)
    ax.legend(loc="upper right", fontsize=7.5, frameon=False)
    tidy(ax)
fig.tight_layout()
fig.savefig(os.path.join(IMG, "fig_pr_curves.pdf"), bbox_inches="tight")
plt.close(fig)
print("wrote fig_pr_curves.pdf")

# --------------------------------------------------------------- Figure 2: ROC
fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.1))
for ax, (corpus, title) in zip(axes, CORPORA):
    curves = load_curves(corpus)
    for m in MODELS:
        y, s = curves[m]
        fpr, tpr, _ = roc_curve(y, s)
        auc = np.mean([f["roc_auc"] for f in R[corpus]["per_fold"][m]])
        ax.plot(fpr, tpr, label=f"{m} (ROC-AUC {auc:.3f})", **STYLE[m])
    ax.plot([0, 1], [0, 1], color=MUTED, ls=":", lw=1.2)
    ax.annotate("random guessing", xy=(0.55, 0.5), xytext=(0.55, 0.42),
                fontsize=7.5, color=MUTED, rotation=32)
    ax.set_xlabel("False positive rate")
    ax.set_ylabel("True positive rate")
    ax.set_title(title, fontsize=9, color=INK)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.02)
    ax.legend(loc="lower right", fontsize=7.5, frameon=False)
    tidy(ax)
fig.tight_layout()
fig.savefig(os.path.join(IMG, "fig_roc_curves.pdf"), bbox_inches="tight")
plt.close(fig)
print("wrote fig_roc_curves.pdf")

# ------------------------------------------------- Figure 3: where they disagree
dis = R["disagreement"]
classes = ["hate speech", "offensive not hate", "neither"]
fig, ax = plt.subplots(figsize=(5.4, 3.0))
x = np.arange(len(classes))
width = 0.36
for i, m in enumerate(MODELS):
    vals = [next(d["flagged_rate"] for d in dis
                 if d["model"] == m and d["davidson_class"] == c) * 100
            for c in classes]
    bars = ax.bar(x + (i - 0.5) * (width + 0.02), vals, width,
                  color=STYLE[m]["color"], label=m,
                  edgecolor="white", linewidth=1.2)
    for b, v in zip(bars, vals):
        ax.annotate(f"{v:.0f}%", (b.get_x() + b.get_width() / 2, v),
                    ha="center", va="bottom", fontsize=7.5, color=INK)
ax.set_xticks(x)
ax.set_xticklabels(["Hate speech\n(should flag)", "Offensive,\nnot hate",
                    "Neither\n(should not flag)"], fontsize=8)
ax.set_ylabel("Flagged by a Wikipedia-trained model (%)")
ax.set_ylim(0, 105)
ax.legend(fontsize=7.5, frameon=False, loc="upper right")
tidy(ax)
fig.tight_layout()
fig.savefig(os.path.join(IMG, "fig_transfer.pdf"), bbox_inches="tight")
plt.close(fig)
print("wrote fig_transfer.pdf")
