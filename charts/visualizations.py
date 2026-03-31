import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# ── helpers ──────────────────────────────────────────────────────────────────

def _quadrant(row):
    """Map ABC/XYZ to 2x2 quadrant."""
    high_value = row["abc_class"] in ["A", "B"]
    stable     = row["xyz_class"] in ["X", "Y"]
    if high_value and stable:
        return "⭐ GOLD", 1, 1
    elif high_value and not stable:
        return "⚠️ RISKY", 1, 0
    elif not high_value and stable:
        return "📦 SAFE", 0, 1
    else:
        return "❌ DEAD WEIGHT", 0, 0


# ── 1. HERO 2x2 ──────────────────────────────────────────────────────────────

def chart_hero_2x2(df: pd.DataFrame):
    """
    Interactive 2x2 matrix.
    - Default: count + label per quadrant
    - Click: item names appear
    - Hover: revenue bubble size
    """
    df = df.copy()
    df[["quadrant", "qx", "qy"]] = df.apply(
        _quadrant, axis=1, result_type="expand"
    )

    # Jitter positions so bubbles don't overlap
    rng = np.random.default_rng(42)
    df["jx"] = df["qx"] + rng.uniform(-0.35, 0.35, len(df))
    df["jy"] = df["qy"] + rng.uniform(-0.35, 0.35, len(df))

    color_map = {
        "⭐ GOLD":        "#2ecc71",
        "⚠️ RISKY":       "#e74c3c",
        "📦 SAFE":        "#3498db",
        "❌ DEAD WEIGHT": "#95a5a6",
    }

    fig = px.scatter(
        df,
        x="jx", y="jy",
        color="quadrant",
        size="revenue",
        hover_name="item_name",
        hover_data={
            "jx": False, "jy": False,
            "quadrant": False,
            "abcxyz_class": True,
            "revenue": ":,.0f",
            "margin_pct": True,
            "avg_days_in_stock": True,
        },
        color_discrete_map=color_map,
        size_max=40,
        title="Inventory Health Matrix",
    )

    # Quadrant background shading
    for (x0, x1, y0, y1, color, label) in [
        (-0.5, 0.5, 0.5, 1.5, "rgba(231,76,60,0.07)",  "⚠️ RISKY\nHigh value · Unpredictable"),
        ( 0.5, 1.5, 0.5, 1.5, "rgba(46,204,113,0.07)", "⭐ GOLD\nHigh value · Stable"),
        (-0.5, 0.5,-0.5, 0.5, "rgba(149,165,166,0.07)","❌ DEAD WEIGHT\nLow value · Unpredictable"),
        ( 0.5, 1.5,-0.5, 0.5, "rgba(52,152,219,0.07)", "📦 SAFE\nLow value · Stable"),
    ]:
        fig.add_shape(type="rect", x0=x0, x1=x1, y0=y0, y1=y1,
                      fillcolor=color, line_width=0, layer="below")
        fig.add_annotation(
            x=(x0+x1)/2, y=(y0+y1)/2,
            text=label.replace("\n", "<br>"),
            showarrow=False,
            font=dict(size=11, color="#555"),
            opacity=0.5
        )

    fig.update_layout(
        xaxis=dict(
            tickvals=[0, 1],
            ticktext=["Unpredictable demand", "Stable demand"],
            range=[-0.5, 1.5], showgrid=False, zeroline=False
        ),
        yaxis=dict(
            tickvals=[0, 1],
            ticktext=["Low value", "High value"],
            range=[-0.5, 1.5], showgrid=False, zeroline=False
        ),
        legend_title="Quadrant",
        height=520,
    )

    # Divider lines
    fig.add_shape(type="line", x0=0.5, x1=0.5, y0=-0.5, y1=1.5,
                  line=dict(color="#ccc", width=1, dash="dash"))
    fig.add_shape(type="line", x0=-0.5, x1=1.5, y0=0.5, y1=0.5,
                  line=dict(color="#ccc", width=1, dash="dash"))

    return fig


# ── 2. ABC/XYZ 3x3 heatmap ───────────────────────────────────────────────────

def chart_abcxyz_heatmap(df: pd.DataFrame):
    matrix = df.groupby(["abc_class", "xyz_class"])["item_code"].count().reset_index()
    matrix.columns = ["abc_class", "xyz_class", "item_count"]
    pivot = matrix.pivot(index="abc_class", columns="xyz_class", values="item_count").fillna(0)

    # Ensure correct order
    pivot = pivot.reindex(index=["A","B","C"], columns=["X","Y","Z"], fill_value=0)

    fig = go.Figure(data=go.Heatmap(
        z=pivot.values,
        x=["X — Stable", "Y — Variable", "Z — Irregular"],
        y=["A — High value", "B — Mid value", "C — Low value"],
        colorscale="RdYlGn",
        reversescale=True,
        text=pivot.values,
        texttemplate="%{text:.0f} items",
        showscale=True,
        hoverongaps=False,
    ))
    fig.update_layout(
        title="ABC / XYZ Classification Matrix",
        xaxis_title="Demand Predictability →",
        yaxis_title="← Revenue Contribution",
        height=380,
    )
    return fig


# ── 3. Treemap ────────────────────────────────────────────────────────────────

def chart_treemap(df: pd.DataFrame):
    fig = px.treemap(
        df,
        path=["category", "abc_class", "item_name"],
        values="revenue",
        color="abc_class",
        color_discrete_map={"A": "#2ecc71", "B": "#f39c12", "C": "#e74c3c"},
        title="Revenue Treemap — Category → ABC Class → Item",
        hover_data={"margin_pct": True}
    )
    fig.update_traces(textinfo="label+value+percent root")
    fig.update_layout(height=500)
    return fig


# ── 4. Ranked bar chart ───────────────────────────────────────────────────────

def chart_ranked_bar(df: pd.DataFrame, top_n: int = 20):
    top = df.nlargest(top_n, "revenue").sort_values("revenue")
    fig = px.bar(
        top,
        x="revenue",
        y="item_name",
        color="abc_class",
        orientation="h",
        color_discrete_map={"A": "#2ecc71", "B": "#f39c12", "C": "#e74c3c"},
        title=f"Top {top_n} Items by Revenue",
        text="abcxyz_class",
        hover_data=["category", "margin_pct", "abcxyz_class"]
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(
        xaxis_title="Revenue (Rp)",
        yaxis_title="",
        height=600,
        showlegend=True
    )
    return fig


# ── 5. Scatter — days in stock vs margin ─────────────────────────────────────

def chart_scatter(df: pd.DataFrame):
    fig = px.scatter(
        df,
        x="avg_days_in_stock",
        y="margin_pct",
        color="abcxyz_class",
        size="revenue",
        hover_name="item_name",
        hover_data=["category", "units_in_stock", "stockout_days_per_year"],
        title="Days in Stock vs Margin % — sized by Revenue",
        labels={
            "avg_days_in_stock": "Avg Days in Stock",
            "margin_pct": "Margin %"
        },
        size_max=40,
        height=500
    )
    fig.add_vline(x=30, line_dash="dash", line_color="gray",
                  annotation_text="30 day mark")
    fig.add_hline(y=df["margin_pct"].median(), line_dash="dash",
                  line_color="gray", annotation_text="Median margin")
    return fig


# ── 6. Pareto ─────────────────────────────────────────────────────────────────

def chart_pareto(df: pd.DataFrame):
    df_sorted = df.sort_values("revenue", ascending=False).head(20)
    fig = go.Figure()
    fig.add_bar(
        x=df_sorted["item_name"],
        y=df_sorted["revenue"],
        name="Revenue",
        marker_color="#3498db"
    )
    fig.add_scatter(
        x=df_sorted["item_name"],
        y=df_sorted["cumulative_revenue_pct"],
        name="Cumulative %",
        yaxis="y2",
        line=dict(color="#e74c3c", width=2),
        mode="lines+markers"
    )
    fig.update_layout(
        title="Pareto Chart — Top 20 Items",
        xaxis_tickangle=-45,
        yaxis=dict(title="Revenue (Rp)"),
        yaxis2=dict(title="Cumulative %", overlaying="y",
                    side="right", range=[0, 110]),
        legend=dict(x=0.01, y=0.99),
        height=450
    )
    return fig