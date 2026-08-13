"""
Individual Task 1 - Part 1.3
Two machine learning algorithms over two public corpora, evaluated for a
content-moderation triage case study.

Algorithms
    1. Linear Support Vector Machine  (sklearn LinearSVC)
    2. Feed-forward neural network    (sklearn MLPClassifier)

Neither was used in Practical Data Science (decision tree, k-NN), satisfying
the "at least one model must be different" condition; both are different here.

Operational target in both corpora is the same business question: *should this
item be escalated to a human moderator for removal?*
    Davidson  positive = class 0 (hate speech)
    Wikipedia positive = majority of annotators marked the comment toxic

Evaluation follows Page, "Evaluating Machine Learning Methods":
    - stratified k-fold cross validation, all preprocessing fitted inside the
      fold so no test label ever influences the vectoriser (slide 35)
    - confusion matrix, precision, recall, F1 rather than accuracy alone,
      because both corpora carry large class skew (slides 18-19)
    - ROC-AUC and PR-AUC, the latter being better suited when negatives
      dominate (slide 33)
    - paired t-test over per-fold differences to compare the two learners
      (slides 43-47)

Run:  python code/03_analysis.py
"""

import json
import os
import time

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import (
    average_precision_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import StratifiedKFold
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data")
OUT = os.path.join(ROOT, "results")
os.makedirs(OUT, exist_ok=True)

SEED = 42
N_FOLDS = 5
REVIEW_CAPACITY = 0.01  # moderators can review 1% of the daily stream

rng = np.random.RandomState(SEED)


# --------------------------------------------------------------------------
# Data loading
# --------------------------------------------------------------------------
def load_davidson():
    df = pd.read_csv(os.path.join(DATA, "davidson_labeled_data.csv"), index_col=0)
    df = df.dropna(subset=["tweet"])
    # class 0 = hate speech -> the removal-worthy class
    y = (df["class"] == 0).astype(int).to_numpy()
    return df["tweet"].astype(str).to_numpy(), y


def load_wikipedia():
    com = pd.read_csv(os.path.join(DATA, "wiki_toxicity_comments.tsv"), sep="\t")
    ann = pd.read_csv(os.path.join(DATA, "wiki_toxicity_annotations.tsv"), sep="\t")
    maj = ann.groupby("rev_id")["toxicity"].mean()
    com = com.merge(maj.rename("toxicity_frac"), left_on="rev_id", right_index=True)
    com = com.dropna(subset=["comment"])
    # Wulczyn et al. encode newlines and tabs as literal tokens
    text = (com["comment"].astype(str)
            .str.replace("NEWLINE_TOKEN", " ", regex=False)
            .str.replace("TAB_TOKEN", " ", regex=False))
    y = (com["toxicity_frac"] > 0.5).astype(int).to_numpy()
    return text.to_numpy(), y


# --------------------------------------------------------------------------
# Models
# --------------------------------------------------------------------------
def make_vectoriser():
    # Fitted inside every fold, never on the full corpus.
    return TfidfVectorizer(
        sublinear_tf=True,
        min_df=3,
        max_features=20000,
        ngram_range=(1, 2),
        strip_accents="unicode",
        lowercase=True,
    )


def make_models():
    return {
        "Linear SVM": Pipeline([
            ("tfidf", make_vectoriser()),
            ("clf", LinearSVC(C=1.0, class_weight="balanced",
                              max_iter=5000, random_state=SEED)),
        ]),
        "Neural network (MLP)": Pipeline([
            ("tfidf", make_vectoriser()),
            ("clf", MLPClassifier(hidden_layer_sizes=(64,),
                                  activation="relu", solver="adam",
                                  alpha=1e-4, batch_size=256,
                                  learning_rate_init=1e-3,
                                  max_iter=30, early_stopping=True,
                                  n_iter_no_change=3, validation_fraction=0.1,
                                  random_state=SEED)),
        ]),
    }


def scores_of(fitted, X):
    """Continuous confidence scores, whichever the estimator exposes."""
    clf = fitted.named_steps["clf"]
    if hasattr(clf, "predict_proba"):
        return fitted.predict_proba(X)[:, 1]
    return fitted.decision_function(X)


def precision_at_capacity(y_true, score, capacity=REVIEW_CAPACITY):
    """Precision over the top-scoring slice a moderation queue can actually review."""
    k = max(1, int(round(len(y_true) * capacity)))
    top = np.argsort(score)[::-1][:k]
    return float(y_true[top].mean()), k


# --------------------------------------------------------------------------
# Cross-validated evaluation
# --------------------------------------------------------------------------
def evaluate(name, X, y):
    print(f"\n{'=' * 72}\nCORPUS: {name}   n={len(y):,}  positives={y.sum():,} "
          f"({y.mean() * 100:.2f}%)\n{'=' * 72}")
    skf = StratifiedKFold(n_splits=N_FOLDS, shuffle=True, random_state=SEED)
    per_fold = {m: [] for m in make_models()}
    pooled = {m: {"y": [], "s": []} for m in make_models()}

    for fold, (tr, te) in enumerate(skf.split(X, y), 1):
        for mname, model in make_models().items():
            t0 = time.time()
            model.fit(X[tr], y[tr])
            pred = model.predict(X[te])
            score = scores_of(model, X[te])
            tn, fp, fn, tp = confusion_matrix(y[te], pred, labels=[0, 1]).ravel()
            p_at_k, k = precision_at_capacity(y[te], score)
            row = {
                "fold": fold,
                "tp": int(tp), "fp": int(fp), "fn": int(fn), "tn": int(tn),
                "accuracy": float((tp + tn) / (tp + tn + fp + fn)),
                "precision": float(precision_score(y[te], pred, zero_division=0)),
                "recall": float(recall_score(y[te], pred, zero_division=0)),
                "f1": float(f1_score(y[te], pred, zero_division=0)),
                "roc_auc": float(roc_auc_score(y[te], score)),
                "pr_auc": float(average_precision_score(y[te], score)),
                "precision_at_1pct": p_at_k,
                "queue_size": k,
                "seconds": round(time.time() - t0, 1),
            }
            per_fold[mname].append(row)
            pooled[mname]["y"].append(y[te])
            pooled[mname]["s"].append(score)
            print(f"  fold {fold} {mname:22s} "
                  f"P={row['precision']:.3f} R={row['recall']:.3f} "
                  f"F1={row['f1']:.3f} PR-AUC={row['pr_auc']:.3f} "
                  f"ROC-AUC={row['roc_auc']:.3f}  [{row['seconds']}s]")

    # Pool fold predictions for a single curve per model (Page, slide 32, approach 1)
    curves = {m: {"y": np.concatenate(pooled[m]["y"]).tolist(),
                  "s": np.concatenate(pooled[m]["s"]).tolist()}
              for m in pooled}
    return per_fold, curves


def summarise(per_fold):
    rows = []
    for mname, folds in per_fold.items():
        d = pd.DataFrame(folds)
        for metric in ["accuracy", "precision", "recall", "f1",
                       "roc_auc", "pr_auc", "precision_at_1pct"]:
            rows.append({"model": mname, "metric": metric,
                         "mean": d[metric].mean(), "std": d[metric].std(ddof=1)})
    return pd.DataFrame(rows)


def paired_test(per_fold, metric):
    """Paired two-tailed t-test on per-fold differences (Page, slides 44-47)."""
    names = list(per_fold)
    a = np.array([f[metric] for f in per_fold[names[0]]])
    b = np.array([f[metric] for f in per_fold[names[1]]])
    t, p = stats.ttest_rel(a, b)
    return {"metric": metric, "model_a": names[0], "model_b": names[1],
            "mean_a": float(a.mean()), "mean_b": float(b.mean()),
            "mean_diff": float((a - b).mean()),
            "t": float(t), "p_value": float(p),
            "significant_at_05": bool(p < 0.05)}


# --------------------------------------------------------------------------
# Cross-corpus transfer: does a model learned on one source hold on the other?
# --------------------------------------------------------------------------
def transfer(Xa, ya, Xb, yb, label_a, label_b):
    out = []
    for mname, model in make_models().items():
        model.fit(Xa, ya)
        pred = model.predict(Xb)
        score = scores_of(model, Xb)
        tn, fp, fn, tp = confusion_matrix(yb, pred, labels=[0, 1]).ravel()
        out.append({
            "model": mname, "trained_on": label_a, "tested_on": label_b,
            "tp": int(tp), "fp": int(fp), "fn": int(fn), "tn": int(tn),
            "accuracy": float((tp + tn) / len(yb)),
            "precision": float(precision_score(yb, pred, zero_division=0)),
            "recall": float(recall_score(yb, pred, zero_division=0)),
            "f1": float(f1_score(yb, pred, zero_division=0)),
            "roc_auc": float(roc_auc_score(yb, score)),
            "pr_auc": float(average_precision_score(yb, score)),
            "flag_rate": float(pred.mean()),
            "base_rate": float(yb.mean()),
        })
        print(f"  {mname:22s} {label_a} -> {label_b}: "
              f"P={out[-1]['precision']:.3f} R={out[-1]['recall']:.3f} "
              f"F1={out[-1]['f1']:.3f} PR-AUC={out[-1]['pr_auc']:.3f} "
              f"flagged={out[-1]['flag_rate'] * 100:.1f}% of stream "
              f"(true base rate {out[-1]['base_rate'] * 100:.1f}%)")
    return out


def main():
    t_start = time.time()
    Xd, yd = load_davidson()
    Xw, yw = load_wikipedia()
    print(f"Davidson : {len(yd):,} tweets,   {yd.mean() * 100:.2f}% hate speech")
    print(f"Wikipedia: {len(yw):,} comments, {yw.mean() * 100:.2f}% toxic")

    results = {"config": {"seed": SEED, "folds": N_FOLDS,
                          "review_capacity": REVIEW_CAPACITY,
                          "davidson_n": int(len(yd)),
                          "davidson_pos_rate": float(yd.mean()),
                          "wikipedia_n": int(len(yw)),
                          "wikipedia_pos_rate": float(yw.mean())}}

    for label, X, y in [("davidson", Xd, yd), ("wikipedia", Xw, yw)]:
        per_fold, curves = evaluate(label, X, y)
        results[label] = {
            "per_fold": per_fold,
            "summary": summarise(per_fold).to_dict("records"),
            "paired_tests": [paired_test(per_fold, m)
                             for m in ["f1", "pr_auc", "roc_auc", "recall", "precision"]],
        }
        np.savez_compressed(
            os.path.join(OUT, f"curves_{label}.npz"),
            **{f"{m}_{k}": np.asarray(v) for m, d in curves.items() for k, v in d.items()})
        print(f"\n  summary ({label}):")
        print(summarise(per_fold).pivot(index="metric", columns="model",
                                        values="mean").round(4).to_string())
        print(f"\n  paired t-tests ({label}):")
        for t in results[label]["paired_tests"]:
            flag = "SIGNIFICANT" if t["significant_at_05"] else "not significant"
            print(f"    {t['metric']:>10s}: diff={t['mean_diff']:+.4f} "
                  f"t={t['t']:+.3f} p={t['p_value']:.4f}  ({flag})")

    print(f"\n{'=' * 72}\nCROSS-CORPUS TRANSFER\n{'=' * 72}")
    results["transfer"] = (
        transfer(Xw, yw, Xd, yd, "wikipedia", "davidson")
        + transfer(Xd, yd, Xw, yw, "davidson", "wikipedia")
    )

    # How much of Davidson's "offensive but not hate" band does a Wikipedia-trained
    # model flag?  This is the concrete evidence of contradiction between sources.
    print(f"\n{'=' * 72}\nWHERE THE SOURCES DISAGREE\n{'=' * 72}")
    dav_raw = pd.read_csv(os.path.join(DATA, "davidson_labeled_data.csv"), index_col=0)
    dav_raw = dav_raw.dropna(subset=["tweet"])
    disagree = []
    for mname, model in make_models().items():
        model.fit(Xw, yw)
        pred = model.predict(Xd)
        for cls, cname in [(0, "hate speech"), (1, "offensive not hate"), (2, "neither")]:
            mask = (dav_raw["class"] == cls).to_numpy()
            rate = float(pred[mask].mean())
            disagree.append({"model": mname, "davidson_class": cname,
                             "n": int(mask.sum()), "flagged_rate": rate})
            print(f"  {mname:22s} flags {rate * 100:5.1f}% of Davidson "
                  f"'{cname}' (n={mask.sum():,})")
    results["disagreement"] = disagree

    with open(os.path.join(OUT, "results.json"), "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nWrote {os.path.join(OUT, 'results.json')}")
    print(f"Total runtime: {(time.time() - t_start) / 60:.1f} min")


if __name__ == "__main__":
    main()
