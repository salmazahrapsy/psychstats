"""Emotion in Indonesian product reviews: clothing vs other categories.

Reproduces every number on https://salmazahrapsy.github.io/business-behaviour/

Data: PRDECT-ID (Sutoyo et al., 2022, Data in Brief 44, 108554,
doi:10.1016/j.dib.2022.108554), stored in data/raw/.

Run from the repository root:
    python analysis/prdect_case_study.py
Writes analysis/output/prdect_case_study.json and prints a summary.

Limitations: the dataset was balanced by label when built, so shares describe
this sample only. Themes use keyword matching on Indonesian text (a manual
check of 16 matches found about 12 relevant). No brand-level data is included.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parent.parent
DATA = (ROOT / "data/raw/Product Reviews Dataset for Emotions Classification Tasks"
        " - Indonesian (PRDECT-ID) Dataset/PRDECT-ID Dataset.csv")
OUT = ROOT / "analysis/output"

FASHION = ["Kids and Baby Fashion", "Muslim Fashion", "Men's Fashion", "Women's Fashion"]

# Indonesian keyword patterns, including common informal spellings (ga, gak, tdk, gk).
THEMES = {
    "not_as_described": r"tidak sesuai|ga sesuai|gak sesuai|nggak sesuai|tdk sesuai|gk sesuai|beda|foto|gambar",
    "fabric": r"bahan|kain|tipis|tebal|adem|panas|gerah|nyaman",
    "colour": r"warna",
    "size_fit": r"ukuran|size|kekecilan|kebesaran|kecil|besar|longgar|sempit|pas di badan|ngepas",
    "delivery": r"kirim|pengiriman|kurir|ekspedisi|telat|lama",
    "seller_response": r"respon|seller|penjual|admin|balas",
    "packaging": r"packing|kemas|packaging|bubble",
    "stitching_defect": r"jahit|benang|sobek|robek|cacat|rusak|luntur",
}


def main() -> dict:
    df = pd.read_csv(DATA)
    df["fashion"] = df["Category"].isin(FASHION)
    text = df["Customer Review"].str.lower()
    res: dict = {"n_reviews": len(df), "n_categories": int(df["Category"].nunique())}

    # 1. Rating by emotion
    res["rating_by_emotion"] = (df.groupby("Emotion")["Customer Rating"].mean().round(2).to_dict())
    groups = [g["Customer Rating"].values for _, g in df.groupby("Emotion")]
    kw = stats.kruskal(*groups)
    res["kruskal_rating_emotion"] = {"H": round(float(kw.statistic), 1), "p": float(kw.pvalue)}

    # 2. Price quartile vs negative sentiment
    df["price_q"] = pd.qcut(df["Price"], 4, labels=["Q1", "Q2", "Q3", "Q4"])
    ct = pd.crosstab(df["price_q"], df["Sentiment"])
    chi2, p, dof, _ = stats.chi2_contingency(ct)
    res["negative_share_by_price_quartile"] = (
        df.groupby("price_q", observed=True)["Sentiment"].apply(lambda s: round((s == "Negative").mean(), 3)).to_dict())
    res["chi2_price_sentiment"] = {"chi2": round(float(chi2), 1), "dof": int(dof), "p": float(p),
                                   "cramers_v": round(float(np.sqrt(chi2 / (ct.values.sum() * (min(ct.shape) - 1)))), 3)}

    # 3. Themes in negative reviews: clothing vs other categories
    neg = df["Sentiment"] == "Negative"
    res["n_negative_fashion"] = int((neg & df["fashion"]).sum())
    res["n_negative_other"] = int((neg & ~df["fashion"]).sum())
    themes = {}
    for name, pattern in THEMES.items():
        hit = text.str.contains(pattern, regex=True)
        a = hit[neg & df["fashion"]]
        b = hit[neg & ~df["fashion"]]
        _, p = stats.fisher_exact([[a.sum(), len(a) - a.sum()], [b.sum(), len(b) - b.sum()]])
        themes[name] = {"fashion_pct": round(100 * a.mean(), 1), "other_pct": round(100 * b.mean(), 1), "fisher_p": float(p)}
    res["themes_in_negative_reviews"] = themes

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "prdect_case_study.json").write_text(json.dumps(res, indent=2))
    return res


if __name__ == "__main__":
    r = main()
    print(f"{r['n_reviews']} reviews, {r['n_categories']} categories")
    print("Mean rating by emotion:", r["rating_by_emotion"])
    for k, v in r["themes_in_negative_reviews"].items():
        print(f"{k:18s} clothing {v['fashion_pct']:5.1f}%  other {v['other_pct']:5.1f}%  p={v['fisher_p']:.2g}")
