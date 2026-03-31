# ui/components/briefing.py
# ─────────────────────────────────────────────────────
# Inventory Briefing — full hero for the Overview tab
# ─────────────────────────────────────────────────────
# Structure:
#   1. One-line summary sentence  — the subject line
#   2. KPI cards                  — 4 numbers at a glance
#   3. Notification feed          — what needs action today
# ─────────────────────────────────────────────────────
import streamlit as st
from config import STOCKOUT_THRESHOLD_DAYS, CURRENCY_SYMBOL

DEAD_WEIGHT_CLASSES = ["CZ", "CY"]
GOLD_CLASSES        = ["AX", "AY"]
RISKY_CLASSES       = ["AZ"]

BRIEFING_TABLE_COLS = ["item_code", "item_name", "category", "abcxyz_class", "interpretation"]


def _summary_sentence(stockouts, dead_weight, risky, gold) -> str:
    """
    Build a single plain-language sentence summarising the inventory state.
    Tone changes based on severity — urgent, caution, or healthy.
    """
    dead_weight_cash = (dead_weight["unit_cost"] * dead_weight["units_in_stock"]).sum()
    n_stockouts      = len(stockouts)
    n_dead           = len(dead_weight)
    n_risky          = len(risky)

    # urgent — stockouts present
    if n_stockouts > 0 and n_dead > 0:
        return (
            f"⚠️ Your inventory needs attention — "
            f"**{n_stockouts} items** cannot be sold right now and "
            f"**{CURRENCY_SYMBOL} {dead_weight_cash:,.0f}** is sitting in slow-moving stock."
        )
    if n_stockouts > 0:
        return (
            f"⚠️ Your inventory needs attention — "
            f"**{n_stockouts} items** are out of stock and losing you sales today."
        )

    # caution — no stockouts but dead weight or risky
    if n_dead > 0:
        return (
            f"🟡 No stockouts right now, but "
            f"**{CURRENCY_SYMBOL} {dead_weight_cash:,.0f}** is tied up in slow-moving items — "
            f"consider clearing them."
        )
    if n_risky > 0:
        return (
            f"🟡 Inventory is mostly healthy but "
            f"**{n_risky} high-value items** have unpredictable demand — keep a safety stock."
        )

    # all clear
    return (
        f"✅ Your inventory looks healthy — "
        f"**{len(gold)} top performers** are well stocked and no urgent issues were found."
    )


def render_briefing(inventory):
    """
    Full hero component: summary → KPI cards → notification feed.
    Replaces both render_hero and render_kpi_strip on the Overview tab.
    """

    # ── classify items ────────────────────────────────
    stockouts        = inventory[inventory["stockout_days_per_year"] > STOCKOUT_THRESHOLD_DAYS]
    dead_weight      = inventory[inventory["abcxyz_class"].isin(DEAD_WEIGHT_CLASSES)]
    gold             = inventory[inventory["abcxyz_class"].isin(GOLD_CLASSES)]
    risky            = inventory[inventory["abcxyz_class"].isin(RISKY_CLASSES)]
    dead_weight_cash = (dead_weight["unit_cost"] * dead_weight["units_in_stock"]).sum()

    # ── 1. SUMMARY SENTENCE ───────────────────────────
    st.markdown(
        f"<div style='font-size:1.1rem; padding: 0.75rem 1rem; "
        f"border-radius: 0.5rem; background-color: rgba(128,128,128,0.1); "
        f"margin-bottom: 1.25rem;'>"
        f"{_summary_sentence(stockouts, dead_weight, risky, gold)}"
        f"</div>",
        unsafe_allow_html=True,
    )

    # ── 2. KPI CARDS ─────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Items",    len(inventory))
    c2.metric("Total Revenue",  f"{CURRENCY_SYMBOL} {inventory['revenue'].sum():,.0f}")
    c3.metric("Avg Margin",     f"{inventory['margin_pct'].mean():.1f}%")
    c4.metric("Stockout Items", len(stockouts))

    st.markdown("---")
    st.markdown("#### What needs your attention today")

    # ── 3. NOTIFICATION FEED ──────────────────────────

    # stockouts — always expanded if present
    if len(stockouts) > 0:
        with st.expander(
            f"🔴  {len(stockouts)} items out of stock — you are losing sales right now",
            expanded=True,
        ):
            st.caption("Restock these first — they have run out too often this year.")
            st.dataframe(
                stockouts[BRIEFING_TABLE_COLS + ["stockout_days_per_year"]].rename(columns={
                    "item_code":              "Code",
                    "item_name":              "Item",
                    "category":               "Category",
                    "abcxyz_class":           "Class",
                    "interpretation":         "Status",
                    "stockout_days_per_year": "Stockout days / year",
                }),
                use_container_width=True,
                hide_index=True,
            )
    else:
        st.success("✅  No stockout items — all items are sufficiently stocked.")

    # dead weight — collapsed by default
    if len(dead_weight) > 0:
        with st.expander(
            f"🟡  {len(dead_weight)} items tying up your cash"
            f" — {CURRENCY_SYMBOL} {dead_weight_cash:,.0f} sitting on the shelf",
        ):
            st.caption("These sell poorly and unpredictably. Consider discounting or discontinuing.")
            st.dataframe(
                dead_weight[BRIEFING_TABLE_COLS + ["units_in_stock", "avg_days_in_stock"]].rename(columns={
                    "item_code":         "Code",
                    "item_name":         "Item",
                    "category":          "Category",
                    "abcxyz_class":      "Class",
                    "interpretation":    "Status",
                    "units_in_stock":    "Units in stock",
                    "avg_days_in_stock": "Avg days in stock",
                }),
                use_container_width=True,
                hide_index=True,
            )
    else:
        st.success("✅  No dead weight items found.")

    # risky — collapsed
    if len(risky) > 0:
        with st.expander(
            f"⚠️  {len(risky)} high-value items with unpredictable demand — keep a safety stock",
        ):
            st.caption("Valuable but hard to predict. Do not let these run out.")
            st.dataframe(
                risky[BRIEFING_TABLE_COLS + ["units_in_stock", "stockout_days_per_year"]].rename(columns={
                    "item_code":              "Code",
                    "item_name":              "Item",
                    "category":               "Category",
                    "abcxyz_class":           "Class",
                    "interpretation":         "Status",
                    "units_in_stock":         "Units in stock",
                    "stockout_days_per_year": "Stockout days / year",
                }),
                use_container_width=True,
                hide_index=True,
            )

    # gold — collapsed
    if len(gold) > 0:
        with st.expander(
            f"✅  {len(gold)} top-performing items — keep these always in stock",
        ):
            st.caption("Your best sellers with stable demand. Never let these run out.")
            st.dataframe(
                gold[BRIEFING_TABLE_COLS + ["units_in_stock", "revenue"]].rename(columns={
                    "item_code":      "Code",
                    "item_name":      "Item",
                    "category":       "Category",
                    "abcxyz_class":   "Class",
                    "interpretation": "Status",
                    "units_in_stock": "Units in stock",
                    "revenue":        "Revenue",
                }),
                use_container_width=True,
                hide_index=True,
            )