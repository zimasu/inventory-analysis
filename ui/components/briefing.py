# ui/components/briefing.py
# ─────────────────────────────────────────────────────────────────────────────
# Inventory Briefing — hero section for the Overview tab.
#
# Three sections rendered top-to-bottom:
#   1. Summary sentence  — one plain-English line on inventory health
#   2. KPI grid          — rounded cards, laid out as a proper grid
#   3. Notification feed — expandable panels per issue type
#
# KPI grid layout rule:
#   n cards  →  grid shape
#   1        →  1 × 1
#   2        →  1 × 2
#   3        →  1 × 3
#   4        →  2 × 2  ← the sweet spot for a dashboard feel
#   5        →  2 × 3  (last cell empty)
#   6        →  2 × 3
#   7–9      →  3 × 3
#   10+      →  rows of 3
#
# WHY ONE BIG st.markdown() FOR THE GRID?
#   st.columns() splits the Streamlit layout tree, but HTML cards rendered
#   inside those columns via st.markdown() can lose their widths depending
#   on the Streamlit version and theme.  A single st.markdown() block that
#   renders the whole grid as an HTML table avoids that entirely — the browser
#   handles the grid, not Streamlit.  No extra packages needed.
# ─────────────────────────────────────────────────────────────────────────────

import math
import streamlit as st
from config import STOCKOUT_THRESHOLD_DAYS, CURRENCY_SYMBOL


# ── Class buckets ─────────────────────────────────────────────────────────────
DEAD_WEIGHT_CLASSES = ["CZ", "CY"]   # slow-moving, unpredictable  → cash tied up
GOLD_CLASSES        = ["AX", "AY"]   # fast-moving, predictable    → protect these
RISKY_CLASSES       = ["AZ"]         # high-value, erratic demand  → safety stock

# Shared columns shown in every notification table
BASE_COLS = ["item_code", "item_name", "category", "abcxyz_class", "interpretation"]

# How many columns per row given the total card count
# 4 cards → 2 cols (= 2×2).  Everything else follows the same logic.
_COLS_FOR_N = {1: 1, 2: 2, 3: 3, 4: 2, 5: 3, 6: 3, 7: 3, 8: 3, 9: 3}


# ── Helpers ───────────────────────────────────────────────────────────────────

def _classify(inventory):
    """
    Split inventory into the four groups we care about.
    Doing this once here means no repeated filter calls elsewhere.
    """
    return {
        "stockouts":   inventory[inventory["stockout_days_per_year"] > STOCKOUT_THRESHOLD_DAYS],
        "dead_weight": inventory[inventory["abcxyz_class"].isin(DEAD_WEIGHT_CLASSES)],
        "gold":        inventory[inventory["abcxyz_class"].isin(GOLD_CLASSES)],
        "risky":       inventory[inventory["abcxyz_class"].isin(RISKY_CLASSES)],
    }


def _summary_sentence(n_stockouts, n_dead, n_risky, n_gold, dead_weight_cash) -> str:
    """
    One plain-English sentence describing inventory health.
    Accepts pre-computed counts/values — no DataFrames — so it's easy to test.
    Priority: urgent → caution → all clear.
    """
    if n_stockouts > 0 and n_dead > 0:
        return (
            f"⚠️ Your inventory needs attention — "
            f"**{n_stockouts} items** cannot be sold right now and "
            f"**{CURRENCY_SYMBOL}{dead_weight_cash:,.0f}** is sitting in slow-moving stock."
        )
    if n_stockouts > 0:
        return (
            f"⚠️ Your inventory needs attention — "
            f"**{n_stockouts} items** are out of stock and losing you sales today."
        )
    if n_dead > 0:
        return (
            f"🟡 No stockouts right now, but "
            f"**{CURRENCY_SYMBOL}{dead_weight_cash:,.0f}** is tied up in slow-moving items — "
            f"consider clearing them."
        )
    if n_risky > 0:
        return (
            f"🟡 Inventory is mostly healthy but "
            f"**{n_risky} high-value items** have unpredictable demand — keep a safety stock."
        )
    if n_gold > 0:
        return (
            f"✅ Your inventory looks healthy — "
            f"**{n_gold} top performers** are well stocked and no urgent issues were found."
        )
    return "✅ Inventory looks healthy — no urgent issues found."


def _kpi_grid(cards: list):
    """
    Render KPI cards as a proper HTML grid inside a single st.markdown() call.

    Why not st.columns() + individual st.markdown() per card?
      When you put an HTML block inside a Streamlit column, the column width
      isn't always passed into the HTML context correctly — cards can collapse
      to full-width stacks.  By rendering the ENTIRE grid as one HTML table,
      the browser owns the layout and the cards always line up correctly.

    Grid shape (n_cols is looked up from _COLS_FOR_N):
      4 cards → 2 cols → 2 × 2
      6 cards → 3 cols → 2 × 3
      9 cards → 3 cols → 3 × 3
      etc.

    Each card:
      ┌─────────────────────────┐
      │                         │
      │   Rp 879,359,500        │  ← big bold number, centred
      │   Total Revenue         │  ← small grey label below
      │                         │
      └─────────────────────────┘

    Args:
        cards: list of (label, value) tuples in display order.
    """
    n      = len(cards)
    n_cols = _COLS_FOR_N.get(n, 3)          # columns per row
    n_rows = math.ceil(n / n_cols)          # rows needed

    # Card cell style — same look as before but defined once here
    cell_style = (
        "background:rgba(128,128,128,0.08);"
        "border:1px solid rgba(128,128,128,0.2);"
        "border-radius:14px;"
        "padding:1.4rem 1rem;"
        "text-align:center;"
        "width:{pct}%;"                     # filled in below per row
    )

    col_pct = 100 // n_cols                 # each column takes an equal share

    # Build the HTML table row by row
    rows_html = []
    card_idx  = 0

    for _ in range(n_rows):
        row_cards = cards[card_idx : card_idx + n_cols]
        cells     = []

        for label, value in row_cards:
            style = cell_style.format(pct=col_pct)
            cells.append(
                f"<td style='{style}'>"
                f"  <div style='font-size:1.9rem;font-weight:700;line-height:1.2'>{value}</div>"
                f"  <div style='font-size:0.82rem;color:grey;margin-top:0.4rem'>{label}</div>"
                f"</td>"
            )

        rows_html.append(f"<tr>{''.join(cells)}</tr>")
        card_idx += n_cols

    table_html = (
        "<table style='width:100%;border-collapse:separate;border-spacing:12px 12px;'>"
        + "".join(rows_html)
        + "</table>"
    )

    st.markdown(table_html, unsafe_allow_html=True)


def _notification_table(df, extra_cols: list, rename_map: dict):
    """Render a dataframe with the shared base columns plus section-specific extras."""
    st.dataframe(
        df[BASE_COLS + extra_cols].rename(columns=rename_map),
        use_container_width=True,
        hide_index=True,
    )


# ── Public entry point ────────────────────────────────────────────────────────

def render_briefing(inventory):
    """
    Main render function — call this from the Overview tab.
    Flow: guard → classify → summary sentence → KPI grid → notification feed.
    """

    if inventory.empty:
        st.warning("No inventory data available.")
        return

    # ── Classify ──────────────────────────────────────────────────────────────
    groups          = _classify(inventory)
    stockouts       = groups["stockouts"]
    dead_weight     = groups["dead_weight"]
    gold            = groups["gold"]
    risky           = groups["risky"]
    dead_weight_cash = (dead_weight["unit_cost"] * dead_weight["units_in_stock"]).sum()

    # ── 1. Summary sentence ───────────────────────────────────────────────────
    summary = _summary_sentence(
        n_stockouts      = len(stockouts),
        n_dead           = len(dead_weight),
        n_risky          = len(risky),
        n_gold           = len(gold),
        dead_weight_cash = dead_weight_cash,
    )
    st.markdown(
        f"<div style='font-size:1.1rem;padding:0.75rem 1rem;"
        f"border-radius:0.5rem;background:rgba(128,128,128,0.1);"
        f"margin-bottom:1rem'>{summary}</div>",
        unsafe_allow_html=True,
    )

    # ── 2. KPI grid ───────────────────────────────────────────────────────────
    # Add / remove / reorder tuples here — the grid reshapes automatically.
    # 4 cards → 2×2.  Add 2 more and it becomes 2×3.  Add 5 more: 3×3.
    kpi_cards = [
        ("Total Items",    str(len(inventory))),
        ("Total Revenue",  f"{CURRENCY_SYMBOL} {inventory['revenue'].sum():,.0f}"),
        ("Avg Margin",     f"{inventory['margin_pct'].mean():.1f}%"),
        ("Stockout Items", str(len(stockouts))),
    ]
    _kpi_grid(kpi_cards)

    st.markdown("---")
    st.markdown("#### What needs your attention today")

    # ── 3. Notification feed ──────────────────────────────────────────────────
    # Most urgent first.  Stockouts auto-expanded; rest collapsed.

    # 3a. Stockouts
    if len(stockouts) > 0:
        with st.expander(
            f"🔴  {len(stockouts)} items out of stock — you are losing sales right now",
            expanded=True,
        ):
            st.caption("Restock these first — they have run out too often this year.")
            _notification_table(stockouts,
                extra_cols = ["stockout_days_per_year"],
                rename_map = {
                    "item_code": "Code", "item_name": "Item", "category": "Category",
                    "abcxyz_class": "Class", "interpretation": "Status",
                    "stockout_days_per_year": "Stockout days / year",
                })
    else:
        st.success("✅  No stockout items — all items are sufficiently stocked.")

    # 3b. Dead weight
    if len(dead_weight) > 0:
        with st.expander(
            f"🟡  {len(dead_weight)} items tying up your cash"
            f" — {CURRENCY_SYMBOL} {dead_weight_cash:,.0f} sitting on the shelf",
        ):
            st.caption("These sell poorly and unpredictably. Consider discounting or discontinuing.")
            _notification_table(dead_weight,
                extra_cols = ["units_in_stock", "avg_days_in_stock"],
                rename_map = {
                    "item_code": "Code", "item_name": "Item", "category": "Category",
                    "abcxyz_class": "Class", "interpretation": "Status",
                    "units_in_stock": "Units in stock", "avg_days_in_stock": "Avg days in stock",
                })
    else:
        st.success("✅  No dead weight items found.")

    # 3c. Risky
    if len(risky) > 0:
        with st.expander(
            f"⚠️  {len(risky)} high-value items with unpredictable demand — keep a safety stock",
        ):
            st.caption("Valuable but hard to predict. Do not let these run out.")
            _notification_table(risky,
                extra_cols = ["units_in_stock", "stockout_days_per_year"],
                rename_map = {
                    "item_code": "Code", "item_name": "Item", "category": "Category",
                    "abcxyz_class": "Class", "interpretation": "Status",
                    "units_in_stock": "Units in stock", "stockout_days_per_year": "Stockout days / year",
                })
    else:
        st.success("✅  No risky items found.")

    # 3d. Gold
    if len(gold) > 0:
        with st.expander(
            f"✅  {len(gold)} top-performing items — keep these always in stock",
        ):
            st.caption("Your best sellers with stable demand. Never let these run out.")
            _notification_table(gold,
                extra_cols = ["units_in_stock", "revenue"],
                rename_map = {
                    "item_code": "Code", "item_name": "Item", "category": "Category",
                    "abcxyz_class": "Class", "interpretation": "Status",
                    "units_in_stock": "Units in stock", "revenue": "Revenue",
                })
    else:
        st.success("✅  No top-performing items found.")