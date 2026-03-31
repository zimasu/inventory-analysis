import pandas as pd
from analysis.combined import calculate_abcxyz
from config import MONTH_COLUMNS, ABCXYZ_INTERPRETATIONS


STABLE_SALES    = [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100]
IRREGULAR_SALES = [0,     0,   0, 500,   0,   0,   0,   0, 300,   0,   0,   0]


def make_full_item(revenue: float, monthly_sales: list[float]) -> dict:
    row = {"revenue": revenue}
    row.update(dict(zip(MONTH_COLUMNS, monthly_sales)))
    return row


def test_high_value_stable_item_is_AX():
    # top item = 7000/7150 ≈ 97.9%... need top item ≤ 70% of total
    df = pd.DataFrame([
        make_full_item(700, STABLE_SALES),
        make_full_item(200, STABLE_SALES),
        make_full_item(100, STABLE_SALES),
    ])
    result = calculate_abcxyz(df)
    assert result.iloc[0]["abcxyz_class"] == "AX"


def test_low_value_irregular_item_is_CZ():
    df = pd.DataFrame([
        make_full_item(10000, STABLE_SALES),
        make_full_item(100,   STABLE_SALES),
        make_full_item(1,     IRREGULAR_SALES),
    ])
    result = calculate_abcxyz(df)
    assert result.iloc[-1]["abcxyz_class"] == "CZ"


def test_all_nine_combinations_have_interpretations():
    assert set(ABCXYZ_INTERPRETATIONS.keys()) == {
        "AX", "AY", "AZ",
        "BX", "BY", "BZ",
        "CX", "CY", "CZ",
    }


def test_abcxyz_class_is_concatenation_of_abc_and_xyz():
    df = pd.DataFrame([make_full_item(1000, STABLE_SALES)])
    result = calculate_abcxyz(df)
    row = result.iloc[0]
    assert row["abcxyz_class"] == str(row["abc_class"]) + str(row["xyz_class"])


def test_interpretation_column_is_populated():
    df = pd.DataFrame([make_full_item(1000, STABLE_SALES)])
    result = calculate_abcxyz(df)
    assert result.iloc[0]["interpretation"] is not None