import pandas as pd
import numpy as np
import pytest
from analysis.xyz import calculate_xyz
from config import MONTH_COLUMNS


def make_items_with_monthly_sales(sales_rows: list[list[float]]) -> pd.DataFrame:
    return pd.DataFrame(sales_rows, columns=MONTH_COLUMNS)


STABLE_DEMAND    = [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100]
VARIABLE_DEMAND  = [50,  80, 120,  60, 100,  90, 110,  70, 130,  40, 100,  80]
IRREGULAR_DEMAND = [0,    0,   0, 500,   0,   0,   0,   0, 300,   0,   0,   0]
ZERO_DEMAND      = [0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0]


def test_perfectly_stable_demand_is_class_X():
    df = make_items_with_monthly_sales([STABLE_DEMAND])
    result = calculate_xyz(df)
    assert result.iloc[0]["xyz_class"] == "X"


def test_moderately_variable_demand_is_class_Y():
    df = make_items_with_monthly_sales([VARIABLE_DEMAND])
    result = calculate_xyz(df)
    assert result.iloc[0]["xyz_class"] == "Y"


def test_highly_irregular_demand_is_class_Z():
    df = make_items_with_monthly_sales([IRREGULAR_DEMAND])
    result = calculate_xyz(df)
    assert result.iloc[0]["xyz_class"] == "Z"


def test_zero_demand_item_has_infinite_cv():                   # zero sales → no meaningful CV
    df = make_items_with_monthly_sales([ZERO_DEMAND])
    result = calculate_xyz(df)
    assert result.iloc[0]["cv"] == np.inf                      # infinity, not zero
    assert result.iloc[0]["xyz_class"] == "Z"                  # dead item → Z not X


def test_stable_demand_has_cv_of_zero():
    df = make_items_with_monthly_sales([STABLE_DEMAND])
    result = calculate_xyz(df)
    assert result.iloc[0]["cv"] == 0.0


def test_output_contains_all_expected_columns():
    df = make_items_with_monthly_sales([STABLE_DEMAND])
    result = calculate_xyz(df)
    for col in ["sales_std", "sales_mean", "cv", "xyz_class"]:
        assert col in result.columns


def test_custom_thresholds_are_respected():
    df = make_items_with_monthly_sales([VARIABLE_DEMAND])
    result = calculate_xyz(df, threshold_x=0.01, threshold_y=0.99)
    assert result.iloc[0]["xyz_class"] == "Y"