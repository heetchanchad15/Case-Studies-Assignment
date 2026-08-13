"""
Profile both corpora so Part 1.2 quotes exact sizes, attributes and class balance
rather than approximations.
"""

import os
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "data")


def rule(t):
    print("\n" + "=" * 72)
    print(t)
    print("=" * 72)


rule("DATASET A - Davidson et al. (2017), labeled_data.csv")
dav = pd.read_csv(os.path.join(DATA, "davidson_labeled_data.csv"), index_col=0)
print(f"shape: {dav.shape[0]:,} rows x {dav.shape[1]} columns")
print("columns:", list(dav.columns))
print("\ndtypes:\n", dav.dtypes.to_string())
print("\nclass codes: 0 = hate speech, 1 = offensive language, 2 = neither")
print(dav["class"].value_counts().sort_index().to_string())
print("\nclass proportions:")
print((dav["class"].value_counts(normalize=True).sort_index() * 100).round(2).to_string())
print(f"\nannotators per tweet (count): min={dav['count'].min()}, "
      f"median={dav['count'].median()}, max={dav['count'].max()}")
print(f"missing tweets: {dav['tweet'].isna().sum()}")
print(f"mean characters per tweet: {dav['tweet'].str.len().mean():.1f}")
print("\nsample rows:")
print(dav[["count", "hate_speech", "offensive_language", "neither", "class"]].head(3).to_string())

rule("DATASET B - Wulczyn et al. (2017), Wikipedia Talk Labels: Toxicity")
com = pd.read_csv(os.path.join(DATA, "wiki_toxicity_comments.tsv"), sep="\t")
ann = pd.read_csv(os.path.join(DATA, "wiki_toxicity_annotations.tsv"), sep="\t")
print(f"comments file: {com.shape[0]:,} rows x {com.shape[1]} columns")
print("columns:", list(com.columns))
print(f"\nannotations file: {ann.shape[0]:,} rows x {ann.shape[1]} columns")
print("columns:", list(ann.columns))
print(f"\nunique comments annotated: {ann['rev_id'].nunique():,}")
print(f"unique annotators: {ann['worker_id'].nunique():,}")
print(f"mean annotations per comment: {ann.groupby('rev_id').size().mean():.2f}")

# Wulczyn et al. define a comment as toxic when the majority of annotators say so.
maj = ann.groupby("rev_id")["toxicity"].mean()
com = com.merge(maj.rename("toxicity_frac"), left_on="rev_id", right_index=True)
com["toxic"] = (com["toxicity_frac"] > 0.5).astype(int)
print(f"\nmerged frame: {com.shape[0]:,} rows")
print("toxic label balance:")
print(com["toxic"].value_counts().to_string())
print(f"positive rate: {com['toxic'].mean() * 100:.2f}%")
print("\nsplit column (the corpus ships its own train/dev/test split):")
print(com["split"].value_counts().to_string())
print("\nnamespace:")
print(com["ns"].value_counts().to_string())
print(f"\nmean characters per comment: {com['comment'].str.len().mean():.1f}")
print("\nsample:")
print(com[["rev_id", "year", "logged_in", "ns", "split", "toxicity_frac", "toxic"]].head(3).to_string())

rule("SUMMARY FOR PART 1.2")
print(f"Davidson : {dav.shape[0]:,} tweets, {dav.shape[1]} attributes, "
      f"{(dav['class'] == 0).mean() * 100:.2f}% hate speech, "
      f"{(dav['class'] == 1).mean() * 100:.2f}% offensive, "
      f"{(dav['class'] == 2).mean() * 100:.2f}% neither")
print(f"Wikipedia: {com.shape[0]:,} comments, {com.shape[1] - 2} native attributes, "
      f"{com['toxic'].mean() * 100:.2f}% toxic, "
      f"{ann.shape[0]:,} crowd judgements from {ann['worker_id'].nunique():,} annotators")
