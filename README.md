# Individual Task 1, Part 1 — Case Studies in Data Science (COSC2669/COSC2816)

Heet Chanchad (s4218211), RMIT University.

Content-moderation triage as a machine learning engineering problem, anchored to a live
graduate Machine Learning Engineer advertisement in TikTok's Trust & Safety Engineering
team.

## The question

A platform receives far more user-generated content each day than any moderation team can
read, and removing content automatically without recourse is unacceptable. The engineering
problem is triage: rank items by the probability they violate policy so a finite number of
human moderators spend their attention where it changes an outcome.

## Data

Both corpora are public and download without an account.

| | Dataset A | Dataset B |
|---|---|---|
| Source | [Davidson et al. (2017)](https://github.com/t-davidson/hate-speech-and-offensive-language) | [Wulczyn et al. (2017)](https://figshare.com/articles/dataset/Wikipedia_Talk_Labels_Toxicity/4563973) |
| Platform | Twitter | English Wikipedia talk pages |
| Instances | 24,783 tweets | 159,686 comments |
| Labels | 3 classes (hate / offensive / neither) | binary toxicity, ~10 annotators per comment |
| Positive class | hate speech, 5.77% | toxic, 9.62% |
| Licence | MIT | CC0 1.0 |

## Models

| Model | Why |
|---|---|
| Linear SVM (`LinearSVC`) | Strong, cheap baseline for high-dimensional sparse text |
| Neural network (`MLPClassifier`) | Learns feature interactions a linear boundary cannot |

Neither was used in Practical Data Science (decision tree, k-NN), satisfying the
assignment's "at least one model must be different" condition.

## Evaluation

Following Page, *Evaluating Machine Learning Methods*:

- stratified 5-fold cross validation, with the TF-IDF vectoriser fitted **inside** each
  fold so no test-fold vocabulary leaks into training;
- precision, recall, F1, ROC-AUC and PR-AUC rather than accuracy alone, because the
  positive class is 5.8% and 9.6% of the two corpora;
- precision over the top 1% of the ranked stream — the slice a fixed review team could
  actually process;
- a paired two-tailed *t*-test over per-fold differences to compare the two learners;
- a cross-corpus transfer test, training on one source and testing on the other.

## Running it

```bash
python -m pip install -r requirements.txt
python code/01_download_data.py    # fetch both corpora (~110 MB)
python code/02_profile_data.py     # exact sizes, attributes, class balance
python code/03_analysis.py         # cross validation, transfer, t-tests (~25 min)
python code/04_job_ad_pdf.py       # typeset the job advertisement for the appendix
python code/05_figures.py          # PR curves, ROC curves, transfer chart
```

Results are written to `results/results.json`; figures to `img/`.

## Layout

```
code/     the five pipeline scripts
data/     downloaded corpora (git-ignored)
results/  results.json, per-fold curves, run log
img/      figures and the job advertisement PDF
latex/    the report sources (ACM acmart template)
```
