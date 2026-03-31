# utils/formatters.py
# ─────────────────────────────────────────────────────
# Formatters — display helpers for numbers and labels
# ─────────────────────────────────────────────────────


def format_currency(value: float, prefix: str = "Rp") -> str:
    """Format a number as currency. e.g. 1500000 → 'Rp 1,500,000'"""
    return f"{prefix} {value:,.0f}"


def format_pct(value: float, decimals: int = 1) -> str:
    """Format a number as percentage. e.g. 0.75 → '75.0%'"""
    return f"{value:.{decimals}f}%"


def format_cv(value: float) -> str:
    """Format coefficient of variation. e.g. 0.3456 → '0.35'"""
    return f"{value:.2f}"