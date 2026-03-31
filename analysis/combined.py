# analysis/combined.py
# ─────────────────────────────────────────────────────
# Combined ABC/XYZ Analysis
# ─────────────────────────────────────────────────────
# What it does: runs ABC + XYZ then merges into one table
# Input:  DataFrame with revenue + 12 monthly sales columns
# Output: fully enriched DataFrame with abcxyz_class + interpretation
# ─────────────────────────────────────────────────────
import pandas as pd
from analysis.abc import calculate_abc
from analysis.xyz import calculate_xyz
from config import ABCXYZ_INTERPRETATIONS


def calculate_abcxyz(
    df: pd.DataFrame,
    threshold_a: float = 0.70,
    threshold_b: float = 0.90,
    threshold_x: float = 0.30,
    threshold_y: float = 0.60,
) -> pd.DataFrame:
    """
    Run the full ABC/XYZ pipeline on a DataFrame.

    Parameters
    ----------
    df            : DataFrame — must have revenue + monthly sales columns
    threshold_a/b : ABC cutoffs (see analysis/abc.py)
    threshold_x/y : XYZ cutoffs (see analysis/xyz.py)

    Returns
    -------
    Fully enriched DataFrame with all ABC, XYZ and combined columns.
    abcxyz_class combines both e.g. AX, BZ, CY etc.
    interpretation is a human readable label for each combination.
    """
    df = calculate_abc(df, threshold_a, threshold_b)
    df = calculate_xyz(df, threshold_x, threshold_y)

    df["abcxyz_class"]  = df["abc_class"].astype(str) + df["xyz_class"].astype(str)
    df["interpretation"] = df["abcxyz_class"].map(ABCXYZ_INTERPRETATIONS)

    return df