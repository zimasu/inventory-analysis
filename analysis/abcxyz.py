# analysis/combined.py
# ─────────────────────────────────────────────────────
# Combined ABC/XYZ Analysis
# ─────────────────────────────────────────────────────
# Input:  inventory.csv     (from extractor.py)
#         sales_history.csv (from extractor.py)
#
# Output: abcxyz_results.csv
#           all inventory columns +
#           revenue, revenue_pct,
#           cumulative_revenue, cumulative_revenue_pct,
#           abc_class, sales_mean, sales_std, cv,
#           xyz_class, abcxyz_class, interpretation
# ─────────────────────────────────────────────────────
import pandas as pd
from analysis.abc import calculate_abc
from analysis.xyz import calculate_xyz
from config import (
    ABCXYZ_INTERPRETATIONS,
    INVENTORY_FILE,
    SALES_FILE,
    ABCXYZ_RESULTS_FILE,
)


def calculate_abcxyz(
    inventory_path: str = INVENTORY_FILE,
    sales_path: str = SALES_FILE,
    threshold_a: float = 0.70,
    threshold_b: float = 0.90,
    threshold_x: float = 0.30,
    threshold_y: float = 0.60,
) -> pd.DataFrame:
    """
    Run the full ABC/XYZ pipeline from raw extractor CSVs.

    Parameters
    ----------
    inventory_path : path to inventory.csv
    sales_path     : path to sales_history.csv
    threshold_a/b  : ABC cutoffs (see analysis/abc.py)
    threshold_x/y  : XYZ cutoffs (see analysis/xyz.py)

    Returns
    -------
    Fully enriched DataFrame merged on product_id, with columns:
        abc_class, xyz_class, abcxyz_class, interpretation
    Products with no sales history are assigned xyz_class Z (irregular).
    """
    inv = pd.read_csv(inventory_path)
    sales = pd.read_csv(sales_path)

    abc = calculate_abc(inv, threshold_a, threshold_b)
    xyz = calculate_xyz(sales, threshold_x, threshold_y)

    df = abc.merge(
        xyz[["product_id", "sales_mean", "sales_std", "cv", "xyz_class"]],
        left_on="id",
        right_on="product_id",
        how="left",
    ).drop(columns="product_id")

    if "Z" not in df["xyz_class"].cat.categories:
        df["xyz_class"] = df["xyz_class"].cat.add_categories("Z")
    df["xyz_class"] = df["xyz_class"].fillna("Z")

    df["abcxyz_class"] = df["abc_class"].astype(str) + df["xyz_class"].astype(str)
    df["interpretation"] = df["abcxyz_class"].map(ABCXYZ_INTERPRETATIONS)

    return df


if __name__ == "__main__":
    result = calculate_abcxyz()
    result.to_csv(ABCXYZ_RESULTS_FILE, index=False)
    print(f"Saved {len(result)} rows to {ABCXYZ_RESULTS_FILE}")
    print(result["abcxyz_class"].value_counts().sort_index().to_string())
