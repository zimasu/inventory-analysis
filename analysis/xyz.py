# analysis/xyz.py
# ─────────────────────────────────────────────────────
# XYZ Analysis — Demand Variability Classification
# ─────────────────────────────────────────────────────
# Input:  sales_history.csv
#           product_id, month (YYYY-MM), units_sold
#
# Output: xyz_results.csv
#           product_id, sales_mean, sales_std, cv, xyz_class
# ─────────────────────────────────────────────────────
import numpy as np
import pandas as pd
from config import SALES_FILE, XYZ_RESULTS_FILE


def calculate_xyz(
    df: pd.DataFrame,
    threshold_x: float = 0.30,
    threshold_y: float = 0.60,
) -> pd.DataFrame:
    """
    Classify items into X / Y / Z by demand variability (CV).

    Parameters
    ----------
    df          : DataFrame from sales_history.csv (long format)
    threshold_x : CV ≤ this → Class X  (stable,    default 0.30)
    threshold_y : CV ≤ this → Class Y  (variable,  default 0.60)
                  CV > threshold_y     → Class Z   (irregular)

    Returns
    -------
    DataFrame grouped by product_id with new columns:
        sales_mean — mean monthly units sold
        sales_std  — standard deviation of monthly units sold
        cv         — coefficient of variation (std / mean); ∞ if mean is 0
        xyz_class  — X, Y, or Z
    """
    stats = (
        df.groupby("product_id")["units_sold"]
        .agg(sales_mean="mean", sales_std="std")
        .reset_index()
    )

    stats["sales_mean"] = stats["sales_mean"].round(2)
    stats["sales_std"] = stats["sales_std"].fillna(0).round(2)

    stats["cv"] = (
        (stats["sales_std"] / stats["sales_mean"].replace(0, np.nan))
        .round(4)
        .fillna(np.inf)
    )

    stats["xyz_class"] = pd.cut(
        stats["cv"],
        bins=[0, threshold_x, threshold_y, np.inf],
        labels=["X", "Y", "Z"],
        include_lowest=True,
    )

    return stats


if __name__ == "__main__":
    df = pd.read_csv(SALES_FILE)
    result = calculate_xyz(df)
    result.to_csv(XYZ_RESULTS_FILE, index=False)
    print(f"Saved {len(result)} rows to {XYZ_RESULTS_FILE}")
    print(result["xyz_class"].value_counts().sort_index().to_string())
