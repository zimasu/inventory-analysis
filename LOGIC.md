# Business Logic — ABC/XYZ Classification

This document explains how the classification works and where to find the numbers if you want to adjust them. Written for someone who understands inventory management but not necessarily the code.

---

## ABC Analysis — Revenue Contribution

**The idea:** not all items deserve the same attention. A items drive most of the revenue, so they get priority treatment.

**How it works:**

1. Items are ranked by total revenue (highest first)
2. We calculate each item's running cumulative share of total revenue
3. Items are bucketed based on where that cumulative % crosses the thresholds

| Class | Cumulative revenue share | Meaning               |
| ----- | ------------------------ | --------------------- |
| A     | 0 – 70%                  | Top revenue drivers   |
| B     | 70 – 90%                 | Mid-tier contributors |
| C     | 90 – 100%                | Long tail             |

**Where to change the thresholds:** `config.py` → `ABC_DEFAULTS`

```python
ABC_DEFAULTS = {
    "threshold_a": 0.70,   # ← top 70% of revenue = Class A
    "threshold_b": 0.90,   # ← top 90% of revenue = Class B (rest is C)
}
```

The logic itself is in `analysis/abc.py`.

---

## XYZ Analysis — Demand Variability

**The idea:** stable demand is easy to plan for. Irregular demand needs safety stock or a different replenishment strategy.

**How it works:**

1. For each item, we calculate the standard deviation and mean of monthly sales across the year
2. We compute the **Coefficient of Variation (CV)** — a standardised measure of variability:

```
CV = standard deviation of monthly sales / mean monthly sales
```

A CV of 0 means perfectly stable (same sales every month). A CV above 0.60 means highly unpredictable.

| Class | CV range    | Meaning                     |
| ----- | ----------- | --------------------------- |
| X     | 0.00 – 0.30 | Stable, predictable demand  |
| Y     | 0.30 – 0.60 | Variable but manageable     |
| Z     | above 0.60  | Irregular, hard to forecast |

**Where to change the thresholds:** `config.py` → `XYZ_DEFAULTS`

```python
XYZ_DEFAULTS = {
    "threshold_x": 0.30,   # ← CV ≤ 0.30 = Class X
    "threshold_y": 0.60,   # ← CV ≤ 0.60 = Class Y (above = Z)
}
```

The logic itself is in `analysis/xyz.py`.

---

## Combined ABC/XYZ Matrix

Each item ends up with a two-letter label combining both dimensions. This gives 9 possible classes:

|                    | X (stable) | Y (variable) | Z (irregular) |
| ------------------ | ---------- | ------------ | ------------- |
| **A (high value)** | AX ⭐      | AY ⭐        | AZ ⚠️         |
| **B (mid value)**  | BX ✅      | BY ✅        | BZ 🔶         |
| **C (low value)**  | CX 📦      | CY 📦        | CZ ❌         |

**Where to change the interpretation labels:** `config.py` → `ABCXYZ_INTERPRETATIONS`

The pipeline that runs both analyses and combines them is in `analysis/combined.py`.

---

## Adjusting thresholds in the app

The app includes sliders to adjust thresholds interactively. The slider bounds (minimum and maximum values the user can set) are defined in:

```
config.py → SLIDER_BOUNDS
```

If the default slider range doesn't cover a threshold value you want to test, adjust the bounds there.
