# utils/data_loader.py
# ─────────────────────────────────────────────────────
# Data Loader — CSV ingestion and validation
# ─────────────────────────────────────────────────────
# What it does: loads a CSV, validates columns,
#               fills gaps, computes derived fields
# Input:  uploaded CSV file
# Output: (DataFrame, list of warning strings)
# ─────────────────────────────────────────────────────
import pandas as pd
from config import REQUIRED_COLUMNS, NUMERIC_COLUMNS, MONTH_COLUMNS


def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Lowercase and underscore all column names."""
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df


def _validate_columns(df: pd.DataFrame) -> None:
    """Raise ValueError if any required columns are missing."""
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")


def _fill_missing_numerics(df: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    """
    Fill missing numeric values with 0.
    Returns (df, warnings) where warnings lists which columns were affected.
    """
    warnings = []
    for col in NUMERIC_COLUMNS:
        if df[col].isnull().any():
            warnings.append(f"Column '{col}' had missing values — filled with 0")
            df[col] = df[col].fillna(0)
    return df, warnings


def _compute_derived_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add derived columns that the analysis depends on.

    Adds:
        margin_pct      — gross margin as a percentage
        total_sales     — sum of all monthly sales
        avg_monthly_sales — mean of monthly sales
        revenue         — total_sales * unit_price
    """
    df["margin_pct"]        = ((df["unit_price"] - df["unit_cost"]) / df["unit_price"] * 100).round(2)
    df["total_sales"]       = df[MONTH_COLUMNS].sum(axis=1)
    df["avg_monthly_sales"] = df[MONTH_COLUMNS].mean(axis=1).round(2)
    df["revenue"]           = df["total_sales"] * df["unit_price"]
    return df


def load_csv(file) -> tuple[pd.DataFrame, list[str]]:
    """
    Load and validate a CSV file for ABC/XYZ analysis.

    Parameters
    ----------
    file : uploaded file object (from st.file_uploader)

    Returns
    -------
    (DataFrame, list of warning strings)
    Raises ValueError if required columns are missing.
    """
    df = pd.read_csv(file)
    df = _normalize_columns(df)
    _validate_columns(df)

    df = df.dropna(how="all")
    df, warnings = _fill_missing_numerics(df)
    df = _compute_derived_columns(df)

    return df, warnings