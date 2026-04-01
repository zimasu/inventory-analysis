import os
from pathlib import Path
from typing import Dict, Tuple, List, Any

# ─────────────────────────────────────────────────────
# Core Engine Configurations
# ─────────────────────────────────────────────────────
PAGE_CONFIG: Dict[str, Any] = {
    "page_title": "Inventory ABC/XYZ Analysis",
    "page_icon": "📦",
    "layout": "wide",
}

ABC_DEFAULTS: Dict[str, float] = {
    "threshold_a": 0.70,
    "threshold_b": 0.90,
}

XYZ_DEFAULTS: Dict[str, float] = {
    "threshold_x": 0.30,
    "threshold_y": 0.60,
}

SLIDER_BOUNDS: Dict[str, Tuple[Any, Any]] = {
    "abc_a": (50, 80),
    "abc_b": (81, 95),
    "xyz_x": (0.10, 0.50),
    "xyz_y": (0.51, 0.80),
}

# ─────────────────────────────────────────────────────
# PrestaShop Secure API Client Boundaries
# ─────────────────────────────────────────────────────
# Environment variables pull credentials securely, preventing hardcoded leaks.
PRESTASHOP_BASE_URL: str = os.getenv("PRESTASHOP_BASE_URL", "http://localhost:8080/api")
PRESTASHOP_API_KEY: str = os.getenv("PRESTASHOP_API_KEY", "PLACEHOLDER_TOKEN_SECURE_MIGRATION")

# ─────────────────────────────────────────────────────
# Deterministic File Paths via Pathlib
# ─────────────────────────────────────────────────────
BASE_DIR: Path = Path(__file__).resolve().parent
DATA_DIR: Path = BASE_DIR / "data"
RESULTS_DIR: Path = BASE_DIR / "results"

# Ensure runtime directories exist natively on execution initialization
DATA_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

INVENTORY_FILE: str = str(DATA_DIR / "inventory.csv")
SALES_FILE: str = str(DATA_DIR / "sales_history.csv")
ABC_RESULTS_FILE: str = str(RESULTS_DIR / "abc_results.csv")
XYZ_RESULTS_FILE: str = str(RESULTS_DIR / "xyz_results.csv")
ABCXYZ_RESULTS_FILE: str = str(RESULTS_DIR / "abcxyz_results.csv")

# ─────────────────────────────────────────────────────
# UI Metric Displays
# ─────────────────────────────────────────────────────
CURRENCY_SYMBOL: str = "Rp"
STOCKOUT_THRESHOLD_DAYS: int = 30
EXPORT_FILENAME: str = "abcxyz_results.csv"

ABC_COLORS: Dict[str, str] = {"A": "#2ecc71", "B": "#f39c12", "C": "#e74c3c"}

ABCXYZ_INTERPRETATIONS: Dict[str, str] = {
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

TABLE_COLUMNS: List[str] = [
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

PLOTLY_CONFIG: Dict[str, bool] = {"staticPlot": True}
PLOTLY_USE_CONTAINER_WIDTH: bool = True
