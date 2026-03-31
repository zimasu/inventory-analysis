import pandas as pd
import pytest
from analysis.abc import calculate_abc


def make_items(revenues: list[float]) -> pd.DataFrame:
    return pd.DataFrame({"revenue": revenues})


def test_highest_revenue_item_is_class_A():
    # top item = 700/1000 = 70% of revenue — lands in A bucket
    df = calculate_abc(make_items([700, 200, 100]))
    assert df.iloc[0]["abc_class"] == "A"


def test_lowest_revenue_item_is_class_C():
    df = calculate_abc(make_items([1000, 100, 1]))
    assert df.iloc[-1]["abc_class"] == "C"


def test_cumulative_revenue_pct_reaches_100():
    df = calculate_abc(make_items([500, 300, 200]))
    assert df["cumulative_revenue_pct"].iloc[-1] == 100.0


def test_revenue_pct_sums_to_100():
    df = calculate_abc(make_items([400, 300, 200, 100]))
    assert round(df["revenue_pct"].sum(), 1) == 100.0


def test_custom_thresholds_are_respected():
    # With threshold_a=0.50, the first item (50% of revenue) should be A
    df = calculate_abc(make_items([500, 500]), threshold_a=0.50, threshold_b=0.75)
    assert df.iloc[0]["abc_class"] == "A"


def test_single_item_has_100pct_cumulative_revenue():
    # A single item represents 100% of revenue — cumulative % is always 100
    df = calculate_abc(make_items([999]))
    assert df.iloc[0]["cumulative_revenue_pct"] == 100.0


def test_output_is_sorted_by_revenue_descending():
    df = calculate_abc(make_items([10, 500, 200]))
    assert df["revenue"].iloc[0] == 500
    assert df["revenue"].iloc[-1] == 10


def test_output_contains_all_expected_columns():
    df = calculate_abc(make_items([100, 50]))
    for col in ["cumulative_revenue", "cumulative_revenue_pct", "revenue_pct", "abc_class"]:
        assert col in df.columns