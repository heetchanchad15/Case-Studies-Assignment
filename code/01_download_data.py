"""
Individual Task 1 - Part 1.2 / 1.3
Download the two public datasets used in this case study.

Dataset A: Davidson et al. (2017) Hate Speech and Offensive Language
           https://github.com/t-davidson/hate-speech-and-offensive-language
Dataset B: Wulczyn et al. (2017) Wikipedia Talk Labels: Toxicity
           https://figshare.com/articles/dataset/Wikipedia_Talk_Labels_Toxicity/4563973

Both are public and require no account. Run from the repo root:
    python code/01_download_data.py
"""

import json
import os
import ssl
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "data")
os.makedirs(DATA, exist_ok=True)

UA = {"User-Agent": "Mozilla/5.0 (research; RMIT COSC2669 coursework)"}
CTX = ssl.create_default_context()

DAVIDSON_URL = (
    "https://raw.githubusercontent.com/t-davidson/"
    "hate-speech-and-offensive-language/master/data/labeled_data.csv"
)
FIGSHARE_ARTICLE = "https://api.figshare.com/v2/articles/4563973"


def fetch(url, dest):
    if os.path.exists(dest) and os.path.getsize(dest) > 0:
        print(f"  cached  {os.path.basename(dest)} ({os.path.getsize(dest):,} bytes)")
        return dest
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=120, context=CTX) as r, open(dest, "wb") as f:
        f.write(r.read())
    print(f"  saved   {os.path.basename(dest)} ({os.path.getsize(dest):,} bytes)")
    return dest


def main():
    print("Dataset A - Davidson et al. hate speech corpus")
    fetch(DAVIDSON_URL, os.path.join(DATA, "davidson_labeled_data.csv"))

    print("Dataset B - Wulczyn et al. Wikipedia Talk toxicity corpus")
    req = urllib.request.Request(FIGSHARE_ARTICLE, headers=UA)
    with urllib.request.urlopen(req, timeout=60, context=CTX) as r:
        meta = json.load(r)

    # We need the comment text and the per-annotator toxicity ratings.
    wanted = {
        "toxicity_annotated_comments.tsv": "wiki_toxicity_comments.tsv",
        "toxicity_annotations.tsv": "wiki_toxicity_annotations.tsv",
    }
    found = {f["name"]: f for f in meta["files"]}
    print("  files advertised by Figshare:", ", ".join(sorted(found)))
    for remote, local in wanted.items():
        if remote not in found:
            raise SystemExit(f"Figshare no longer exposes {remote}")
        fetch(found[remote]["download_url"], os.path.join(DATA, local))

    print("\nDone. Files in", DATA)
    for f in sorted(os.listdir(DATA)):
        print(f"  {f:40s} {os.path.getsize(os.path.join(DATA, f)):>12,} bytes")


if __name__ == "__main__":
    main()
