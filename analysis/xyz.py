import pandas as pd                                            # data processing library
import numpy as np                                             # numerical operations
from config import MONTH_COLUMNS                               # list of 12 monthly sales columns


def calculate_xyz(
    df: pd.DataFrame,
    threshold_x: float = 0.30,
    threshold_y: float = 0.60,
) -> pd.DataFrame:
    df = df.copy()

    monthly = df[MONTH_COLUMNS]
    df["sales_std"]  = monthly.std(axis=1).round(2)           # standard deviation across 12 months
    df["sales_mean"] = monthly.mean(axis=1).round(2)          # average across 12 months

    df["cv"] = (
        df["sales_std"] / df["sales_mean"].replace(0, np.nan) # avoid dividing by zero
    ).round(4).fillna(np.inf)                                  # zero sales items → infinity → Z class

    df["xyz_class"] = pd.cut(
        df["cv"],
        bins=[0, threshold_x, threshold_y, np.inf],           # bucket by threshold
        labels=["X", "Y", "Z"],
        include_lowest=True,
    )

    return df