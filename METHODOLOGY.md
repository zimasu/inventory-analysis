# ABC/XYZ Classification Methodology

This document details the classification logic and parameter tuning. All threshold adjustments are handled in `config.py`.

## 1. ABC Analysis (Revenue Impact)
We rank items by total revenue contribution to distinguish between high-value drivers and long-tail items.

* **Method:** Sort items by revenue $\to$ Calculate cumulative % share $\to$ Assign classes based on thresholds.

| Class | Cumulative Revenue Share |
| :--- | :--- |
| **A** | 0 – 70% |
| **B** | 70 – 90% |
| **C** | 90 – 100% |

* **Configuration:** `ABC_DEFAULTS` in `config.py`.
* **Core Logic:** `analysis/abc.py`.

---

## 2. XYZ Analysis (Demand Stability)
We use the **Coefficient of Variation (CV)** to measure demand unpredictability.

* **Formula:** $CV = \frac{\sigma}{\mu}$ (Standard Deviation / Mean)

| Class | CV Range | Demand Profile |
| :--- | :--- | :--- |
| **X** | 0.00 – 0.30 | Stable |
| **Y** | 0.30 – 0.60 | Variable |
| **Z** | > 0.60 | Irregular |

* **Configuration:** `XYZ_DEFAULTS` in `config.py`.
* **Core Logic:** `analysis/xyz.py`.

---

## 3. Classification Matrix
Items are assigned a combined class (e.g., "AX", "BZ") to determine replenishment priority.

| | X (Stable) | Y (Variable) | Z (Irregular) |
| :--- | :--- | :--- | :--- |
| **A (High Value)** | AX | AY | AZ |
| **B (Mid Value)** | BX | BY | BZ |
| **C (Low Value)** | CX | CY | CZ |

* **Configuration:** `ABCXYZ_INTERPRETATIONS` in `config.py`.
* **Pipeline:** `analysis/combined.py` merges both metrics.

---

## Interactive Controls
The Streamlit app allows dynamic threshold adjustments.
* **Slider Ranges:** Defined by `SLIDER_BOUNDS` in `config.py`. Adjust these if you need to test boundary values outside the current range.
