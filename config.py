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

# ─────────────────────────────────────────────────────
# PrestaShop API
# ─────────────────────────────────────────────────────
PRESTASHOP_BASE_URL = "http://localhost:8080/api"
PRESTASHOP_API_KEY = "99YUV7ASUZTY75YCCMAUEAXR966XX5PG"

# ─────────────────────────────────────────────────────
# File paths
# ─────────────────────────────────────────────────────
INVENTORY_FILE = "data/inventory.csv"
SALES_FILE = "data/sales_history.csv"
ABC_RESULTS_FILE = "results/abc_results.csv"
XYZ_RESULTS_FILE = "results/xyz_results.csv"
ABCXYZ_RESULTS_FILE = "results/abcxyz_results.csv"

# ─────────────────────────────────────────────────────
# Display
# ─────────────────────────────────────────────────────
CURRENCY_SYMBOL = "Rp"
STOCKOUT_THRESHOLD_DAYS = 30
EXPORT_FILENAME = "abcxyz_results.csv"

ABC_COLORS = {"A": "#2ecc71", "B": "#f39c12", "C": "#e74c3c"}

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

TABLE_COLUMNS = [
    "id",
    "name",
    "reference",
    "abc_class",
    "xyz_class",
    "abcxyz_class",
    "revenue",
    "cv",
    "interpretation",
]

PLOTLY_CONFIG = {"staticPlot": True}
PLOTLY_USE_CONTAINER_WIDTH = True
