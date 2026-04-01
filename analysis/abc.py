# analysis/abc.py
# ─────────────────────────────────────────────────────
# ABC Analysis — Revenue Contribution Classification
# ─────────────────────────────────────────────────────
# Input:  inventory.csv
#           id, reference, name, price,
#           wholesale_price, quantity, sales_volume
#
# Output: abc_results.csv
#           all input columns +
#           revenue, revenue_pct,
#           cumulative_revenue, cumulative_revenue_pct,
#           abc_class
# ─────────────────────────────────────────────────────
import pandas as pd
from config import INVENTORY_FILE, ABC_RESULTS_FILE


def calculate_abc(
    df: pd.DataFrame,
    threshold_a: float = 0.70,
    threshold_b: float = 0.90,
) -> pd.DataFrame:
    """
    Classify items into A / B / C by cumulative revenue share.

    Parameters
    ----------
    df          : DataFrame from inventory.csv
    threshold_a : cumulative revenue share ceiling for Class A (default 70%)
    threshold_b : cumulative revenue share ceiling for Class B (default 90%)
                  anything above → Class C

    Returns
    -------
    DataFrame sorted by revenue descending, with new columns:
        revenue                 — price × sales_volume
        revenue_pct             — this item's % of total revenue
        cumulative_revenue      — running total of revenue
        cumulative_revenue_pct  — running % of total revenue
        abc_class               — A, B, or C
    """
    df = df.copy()
    df["revenue"] = (df["price"] * df["sales_volume"]).round(2)
    df = df.sort_values("revenue", ascending=False).reset_index(drop=True)

    total = df["revenue"].sum()
    df["revenue_pct"] = (df["revenue"] / total * 100).round(2)
    df["cumulative_revenue"] = df["revenue"].cumsum().round(2)
    df["cumulative_revenue_pct"] = (df["cumulative_revenue"] / total * 100).round(2)

    df["abc_class"] = pd.cut(
        df["cumulative_revenue_pct"],
        bins=[0, threshold_a * 100, threshold_b * 100, 100],
        labels=["A", "B", "C"],
        include_lowest=True,
    )

    return df


if __name__ == "__main__":
    df = pd.read_csv(INVENTORY_FILE)
    result = calculate_abc(df)
    result.to_csv(ABC_RESULTS_FILE, index=False)
    print(f"Saved {len(result)} rows to {ABC_RESULTS_FILE}")
    print(result["abc_class"].value_counts().sort_index().to_string())
