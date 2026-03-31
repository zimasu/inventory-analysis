PAGE_CONFIG = {
    "page_title": "Inventory ABC/XYZ Analysis",
    "page_icon": "📦",
    "layout": "wide",
}

ABC_DEFAULTS = {
    "threshold_a": 0.70,
    "threshold_b": 0.90,
}

XYZ_DEFAULTS = {
    "threshold_x": 0.30,
    "threshold_y": 0.60,
}

SLIDER_BOUNDS = {
    "abc_a": (50, 80),
    "abc_b": (81, 95),
    "xyz_x": (0.10, 0.50),
    "xyz_y": (0.51, 0.80),
}

CURRENCY_SYMBOL = "Rp"
STOCKOUT_THRESHOLD_DAYS = 30
EXPORT_FILENAME = "abcxyz_results.csv"

ABC_COLORS = {"A": "#2ecc71", "B": "#f39c12", "C": "#e74c3c"}

MONTH_COLUMNS = [
    "monthly_sales_jan", "monthly_sales_feb", "monthly_sales_mar",
    "monthly_sales_apr", "monthly_sales_may", "monthly_sales_jun",
    "monthly_sales_jul", "monthly_sales_aug", "monthly_sales_sep",
    "monthly_sales_oct", "monthly_sales_nov", "monthly_sales_dec",
]

ABCXYZ_INTERPRETATIONS = {
    "AX": "⭐ High value, stable demand — prioritize stock",
    "AY": "⭐ High value, variable demand — monitor closely",
    "AZ": "⚠️ High value, irregular demand — safety stock needed",
    "BX": "✅ Medium value, stable demand — standard replenishment",
    "BY": "✅ Medium value, variable demand — review periodically",
    "BZ": "🔶 Medium value, irregular demand — review ordering",
    "CX": "📦 Low value, stable demand — consider lean stock",
    "CY": "📦 Low value, variable demand — reduce stock",
    "CZ": "❌ Low value, irregular demand — consider discontinuing",
}

REQUIRED_COLUMNS = [
    "item_code", "item_name", "category",
    "unit_cost", "unit_price", "units_in_stock",
    "volume_m3", "order_frequency", "avg_delivery_days",
    "stockout_days_per_year", "avg_days_in_stock",
    *MONTH_COLUMNS,
]

TEXT_COLUMNS = ["item_code", "item_name", "category"]

NUMERIC_COLUMNS = [c for c in REQUIRED_COLUMNS if c not in TEXT_COLUMNS]

TABLE_COLUMNS = [
    "item_code", "item_name", "category",
    "abc_class", "xyz_class", "abcxyz_class",
    "revenue", "margin_pct", "cv",
    "avg_days_in_stock", "stockout_days_per_year",
    "interpretation",
]

PLOTLY_CONFIG = {"staticPlot": True}                           # disable all chart interactivity
PLOTLY_USE_CONTAINER_WIDTH = True                              # stretch charts to full container width