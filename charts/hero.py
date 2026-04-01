import pandas as pd
import plotly.express as px
import numpy as np


QUADRANT_COLORS = {
    "⭐ GOLD": "#2ecc71",
    "⚠️ RISKY": "#e74c3c",
    "📦 SAFE": "#3498db",
    "❌ DEAD WEIGHT": "#95a5a6",
}

QUADRANT_SHADING = [
    (
        -0.5,
        0.5,
        0.5,
        1.5,
        "rgba(231,76,60,0.10)",
        "⚠️ RISKY<br>High value · Unpredictable",
    ),
    (0.5, 1.5, 0.5, 1.5, "rgba(46,204,113,0.10)", "⭐ GOLD<br>High value · Stable"),
    (
        -0.5,
        0.5,
        -0.5,
        0.5,
        "rgba(149,165,166,0.10)",
        "❌ DEAD WEIGHT<br>Low value · Unpredictable",
    ),
    (0.5, 1.5, -0.5, 0.5, "rgba(52,152,219,0.10)", "📦 SAFE<br>Low value · Stable"),
]


def _assign_quadrant(row):
    high_value = row["abc_class"] in ["A", "B"]
    stable = row["xyz_class"] in ["X", "Y"]
    if high_value and stable:
        return "⭐ GOLD", 1, 1
    elif high_value and not stable:
        return "⚠️ RISKY", 0, 1
    elif not high_value and stable:
        return "📦 SAFE", 1, 0
    else:
        return "❌ DEAD WEIGHT", 0, 0


def chart_hero_2x2(inventory: pd.DataFrame):
    inventory = inventory.copy()
    inventory["abc_class"] = inventory["abc_class"].astype(str)
    inventory["xyz_class"] = inventory["xyz_class"].astype(str)

    inventory[["quadrant", "qx", "qy"]] = inventory.apply(
        _assign_quadrant, axis=1, result_type="expand"
    )

    rng = np.random.default_rng(42)
    inventory["demand_stability"] = inventory["qx"] + rng.uniform(
        -0.35, 0.35, len(inventory)
    )
    inventory["value_tier"] = inventory["qy"] + rng.uniform(-0.35, 0.35, len(inventory))

    fig = px.scatter(
        inventory,
        x="demand_stability",
        y="value_tier",
        color="quadrant",
        size="revenue",
        hover_name="item_name",
        hover_data={
            "demand_stability": False,
            "value_tier": False,
            "quadrant": False,
            "abcxyz_class": True,
            "revenue": ":,.0f",
            "margin_pct": ":.1f",
            "avg_days_in_stock": ":.1f",
        },
        color_discrete_map=QUADRANT_COLORS,
        size_max=40,
        title="Inventory Health Matrix",
    )

    fig.update_layout(
        xaxis=dict(
            tickvals=[0, 1],
            ticktext=["Unpredictable demand", "Stable demand"],
            range=[-0.5, 1.5],
            showgrid=False,
            zeroline=False,
        ),
        yaxis=dict(
            tickvals=[0, 1],
            ticktext=["Low value", "High value"],
            range=[-0.5, 1.5],
            showgrid=False,
            zeroline=False,
        ),
        legend_title="Quadrant",
        height=520,
    )

    for x0, x1, y0, y1, color, label in QUADRANT_SHADING:
        fig.add_shape(
            type="rect",
            x0=x0,
            x1=x1,
            y0=y0,
            y1=y1,
            fillcolor=color,
            line_width=0,
            layer="below",
        )
        fig.add_annotation(
            x=(x0 + x1) / 2,
            y=(y0 + y1) / 2,
            text=label,
            showarrow=False,
            font=dict(size=11, color="#aaa"),
            opacity=0.6,
        )

    fig.add_shape(
        type="line",
        x0=0.5,
        x1=0.5,
        y0=-0.5,
        y1=1.5,
        line=dict(color="#444", width=1, dash="dash"),
    )
    fig.add_shape(
        type="line",
        x0=-0.5,
        x1=1.5,
        y0=0.5,
        y1=0.5,
        line=dict(color="#444", width=1, dash="dash"),
    )

    # ── Top 3 labels per quadrant ─────────────────────────
    for quadrant_name in inventory["quadrant"].unique():
        top3 = inventory[inventory["quadrant"] == quadrant_name].nlargest(3, "revenue")
        for _, row in top3.iterrows():
            words = row["item_name"].split()
            if len(words) <= 3:
                label = " ".join(words)
            else:
                label = f"{words[0]} {words[1]}, {words[-1]}"
            fig.add_annotation(
                x=row["demand_stability"],
                y=row["value_tier"],
                text=label,
                showarrow=False,
                font=dict(size=12, color="#ffffff"),
                yshift=18,
                bgcolor="rgba(0,0,0,0.5)",
                bordercolor="rgba(0,0,0,0.5)",
                borderwidth=1,
                borderpad=4,
            )

    return fig
