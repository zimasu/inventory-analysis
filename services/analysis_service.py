import pandas as pd
from analysis.abcxyz import calculate_abcxyz


def run_analysis(config: dict) -> tuple:
    df = calculate_abcxyz(
        threshold_a=config["threshold_a"],
        threshold_b=config["threshold_b"],
        threshold_x=config["threshold_x"],
        threshold_y=config["threshold_y"],
    )

    # ── column renames ─────────────────────────────────────
    df = df.rename(
        columns={
            "name": "item_name",
            "reference": "item_code",
        }
    )

    # ── derived metrics ────────────────────────────────────
    df["margin_pct"] = (
        (df["price"] - df["wholesale_price"]) / df["price"] * 100
    ).round(1)

    df["avg_days_in_stock"] = df.apply(
        lambda r: (
            round(r["quantity"] / (r["sales_volume"] / 365), 1)
            if r["sales_volume"] > 0
            else float("inf")
        ),
        axis=1,
    )

    df["stockout_days_per_year"] = df[
        "avg_days_in_stock"
    ]  # same metric, two names used across components

    # ── placeholder for category (not in PrestaShop extractor yet) ──
    if "category" not in df.columns:
        df["category"] = "—"

    return df, []
