# analysis/abc.py
# ─────────────────────────────────────────────────────
# ABC Analysis — Revenue Contribution Classification
# ─────────────────────────────────────────────────────
# What it does: ranks items by cumulative revenue share
# Input:  DataFrame with column [revenue]
# Output: same DataFrame + columns:
#           [cumulative_revenue, cumulative_revenue_pct,
#            revenue_pct, abc_class]
# Formula: cumulative % of sorted revenue → threshold buckets
# ─────────────────────────────────────────────────────
import pandas as pd


def calculate_abc(
    df: pd.DataFrame,
    threshold_a: float = 0.70,
    threshold_b: float = 0.90,
) -> pd.DataFrame:
    """
    Classify items into A / B / C by cumulative revenue share.

    Parameters
    ----------
    df          : DataFrame — must have 'revenue' column
    threshold_a : top share of revenue = Class A  (default 70%)
    threshold_b : top share of revenue = Class B  (default 90%)

    Returns
    -------
    DataFrame with new columns:
        cumulative_revenue      — running total of revenue
        cumulative_revenue_pct  — running % of total revenue
        revenue_pct             — this item's % of total revenue
        abc_class               — A, B, or C
    """
    df = df.copy()
    df = df.sort_values("revenue", ascending=False).reset_index(drop=True)

    total = df["revenue"].sum()
    df["cumulative_revenue"]     = df["revenue"].cumsum()
    df["cumulative_revenue_pct"] = (df["cumulative_revenue"] / total * 100).round(2)
    df["revenue_pct"]            = (df["revenue"] / total * 100).round(2)

    df["abc_class"] = pd.cut(
        df["cumulative_revenue_pct"],
        bins=[0, threshold_a * 100, threshold_b * 100, 100],
        labels=["A", "B", "C"],
        include_lowest=True,
    )

    return df