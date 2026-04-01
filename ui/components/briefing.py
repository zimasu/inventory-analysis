import streamlit as st
from config import CURRENCY_SYMBOL, STOCKOUT_THRESHOLD_DAYS
from ui.i18n import t


def _language_toggle() -> str:
    if "lang" not in st.session_state:
        st.session_state.lang = "en"

    col1, col2, col3, _ = st.columns([1, 1, 1, 6])
    with col1:
        if st.button("🇬🇧 EN"):
            st.session_state.lang = "en"
    with col2:
        if st.button("🇮🇩 ID"):
            st.session_state.lang = "id"
    with col3:
        if st.button("🇩🇪 DE"):
            st.session_state.lang = "de"

    return st.session_state.lang


def _headline(inventory, lang) -> str:
    low_stock = inventory[inventory["avg_days_in_stock"] < STOCKOUT_THRESHOLD_DAYS]
    dead = inventory[inventory["abcxyz_class"].isin(["CZ", "CY"])]
    risky = inventory[inventory["abcxyz_class"] == "AZ"]
    gold = inventory[inventory["abcxyz_class"].isin(["AX", "AY"])]

    if len(low_stock) > 0:
        return t("headline_low_stock", lang, n=len(low_stock))
    if len(dead) > 0:
        cash = (dead["wholesale_price"] * dead["quantity"]).sum()
        return t("headline_dead", lang, currency=CURRENCY_SYMBOL, cash=f"{cash:,.0f}")
    if len(risky) > 0:
        return t("headline_risky", lang, n=len(risky))
    if len(gold) > 0:
        return t("headline_gold", lang, n=len(gold))
    return t("headline_ok", lang)


def _kpi_cards(inventory, lang):
    low_stock = inventory[inventory["avg_days_in_stock"] < STOCKOUT_THRESHOLD_DAYS]
    total_revenue = inventory["revenue"].sum()
    top_items = inventory[inventory["abc_class"] == "A"]

    cards = [
        ("📦", t("kpi_total", lang), str(len(inventory)), "rgba(52,152,219,0.12)"),
        (
            "💰",
            t("kpi_revenue", lang),
            f"{CURRENCY_SYMBOL} {total_revenue:,.0f}",
            "rgba(46,204,113,0.12)",
        ),
        ("⭐", t("kpi_top", lang), str(len(top_items)), "rgba(241,196,15,0.12)"),
        ("⚠️", t("kpi_lowstock", lang), str(len(low_stock)), "rgba(231,76,60,0.12)"),
    ]

    cols = st.columns(4)
    for col, (emoji, label, value, bg) in zip(cols, cards):
        col.markdown(
            f"""
            <div style="
                background:{bg};
                border-radius:14px;
                padding:1.2rem 1rem;
                text-align:center;
            ">
                <div style="font-size:1.6rem">{emoji}</div>
                <div style="font-size:1.5rem;font-weight:800;margin:0.3rem 0;line-height:1.2">{value}</div>
                <div style="font-size:0.8rem;color:grey">{label}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("<div style='margin-bottom:1rem'></div>", unsafe_allow_html=True)


def render_briefing(inventory):
    if inventory.empty:
        st.warning("No inventory data available.")
        return

    lang = _language_toggle()

    low_stock = inventory[inventory["avg_days_in_stock"] < STOCKOUT_THRESHOLD_DAYS]
    dead = inventory[inventory["abcxyz_class"].isin(["CZ", "CY"])]
    risky = inventory[inventory["abcxyz_class"] == "AZ"]
    gold = inventory[inventory["abcxyz_class"].isin(["AX", "AY"])]

    # ── 1. Headline ───────────────────────────────────────
    st.markdown(
        f"<div style='font-size:1.1rem;padding:0.75rem 1rem;"
        f"border-radius:0.5rem;background:rgba(128,128,128,0.1);"
        f"margin-bottom:1rem'>{_headline(inventory, lang)}</div>",
        unsafe_allow_html=True,
    )

    # ── 2. KPI cards ──────────────────────────────────────
    _kpi_cards(inventory, lang)
    st.markdown("---")

    # ── 3. Expandable panels ──────────────────────────────
    st.markdown(t("attention", lang))

    if len(low_stock) > 0:
        with st.expander(t("low_stock_exp", lang, n=len(low_stock)), expanded=True):
            st.caption(t("low_stock_cap", lang))
            st.dataframe(
                low_stock[
                    [
                        "item_code",
                        "item_name",
                        "abcxyz_class",
                        "quantity",
                        "avg_days_in_stock",
                    ]
                ].rename(
                    columns={
                        "item_code": "Code",
                        "item_name": "Item",
                        "abcxyz_class": "Class",
                        "quantity": "In Stock",
                        "avg_days_in_stock": "Days Left",
                    }
                ),
                use_container_width=True,
                hide_index=True,
            )
    else:
        st.success(t("no_low_stock", lang))

    if len(dead) > 0:
        cash = (dead["wholesale_price"] * dead["quantity"]).sum()
        with st.expander(
            t(
                "dead_exp",
                lang,
                n=len(dead),
                currency=CURRENCY_SYMBOL,
                cash=f"{cash:,.0f}",
            )
        ):
            st.caption(t("dead_cap", lang))
            st.dataframe(
                dead[
                    [
                        "item_code",
                        "item_name",
                        "abcxyz_class",
                        "quantity",
                        "interpretation",
                    ]
                ].rename(
                    columns={
                        "item_code": "Code",
                        "item_name": "Item",
                        "abcxyz_class": "Class",
                        "quantity": "In Stock",
                        "interpretation": "Status",
                    }
                ),
                use_container_width=True,
                hide_index=True,
            )
    else:
        st.success(t("no_dead", lang))

    if len(risky) > 0:
        with st.expander(t("risky_exp", lang, n=len(risky))):
            st.caption(t("risky_cap", lang))
            st.dataframe(
                risky[
                    ["item_code", "item_name", "abcxyz_class", "quantity", "cv"]
                ].rename(
                    columns={
                        "item_code": "Code",
                        "item_name": "Item",
                        "abcxyz_class": "Class",
                        "quantity": "In Stock",
                        "cv": "Variability (CV)",
                    }
                ),
                use_container_width=True,
                hide_index=True,
            )
    else:
        st.success(t("no_risky", lang))

    if len(gold) > 0:
        with st.expander(t("gold_exp", lang, n=len(gold))):
            st.caption(t("gold_cap", lang))
            st.dataframe(
                gold[
                    ["item_code", "item_name", "abcxyz_class", "revenue", "quantity"]
                ].rename(
                    columns={
                        "item_code": "Code",
                        "item_name": "Item",
                        "abcxyz_class": "Class",
                        "revenue": "Revenue",
                        "quantity": "In Stock",
                    }
                ),
                use_container_width=True,
                hide_index=True,
            )
    else:
        st.success(t("no_gold", lang))
