# Item Priority — Inventory ABC/XYZ Analysis

A Streamlit app for classifying inventory items by value and demand stability, helping businesses focus their stock management effort where it matters most.

---

## What it does

Uploads a CSV of inventory data and classifies each item across two dimensions:

- **ABC** — how much revenue does this item contribute?
- **XYZ** — how predictable is its demand?

Combined, each item gets a label like `AX` (high value, stable) or `CZ` (low value, irregular), with a plain-language interpretation to guide stock decisions.

---

## Running the app

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## Input data format

Upload a CSV file with the following columns:

| Column                                    | Type   | Description                    |
| ----------------------------------------- | ------ | ------------------------------ |
| `item_code`                               | text   | Unique item identifier         |
| `item_name`                               | text   | Item name                      |
| `category`                                | text   | Item category                  |
| `unit_cost`                               | number | Cost per unit                  |
| `unit_price`                              | number | Selling price per unit         |
| `units_in_stock`                          | number | Current stock level            |
| `volume_m3`                               | number | Volume per unit (cubic metres) |
| `order_frequency`                         | number | How often the item is ordered  |
| `avg_delivery_days`                       | number | Average supplier lead time     |
| `stockout_days_per_year`                  | number | Days out of stock per year     |
| `avg_days_in_stock`                       | number | Average days held in stock     |
| `monthly_sales_jan` … `monthly_sales_dec` | number | Units sold each month          |

A sample file is included: `inventory_sample.csv`

---

## Output

The app adds the following columns to the data:

| Column                   | Description                                      |
| ------------------------ | ------------------------------------------------ |
| `abc_class`              | A, B, or C — revenue contribution tier           |
| `xyz_class`              | X, Y, or Z — demand variability tier             |
| `abcxyz_class`           | Combined label e.g. AX, BZ, CY                   |
| `interpretation`         | Plain-language description of the classification |
| `revenue_pct`            | This item's % of total revenue                   |
| `cumulative_revenue_pct` | Running cumulative % (used for ABC cutoff)       |
| `cv`                     | Coefficient of variation (used for XYZ cutoff)   |

Results can be exported as `abcxyz_results.csv`.

---

## Running the tests

```bash
pip install pytest
pytest tests/
```

---

## Project structure

```
analysis/       — classification logic (ABC, XYZ, combined)
charts/         — chart components
ui/             — Streamlit layout and components
utils/          — data loading and formatting helpers
config.py       — thresholds, column names, labels
app.py          — entry point
```

See `LOGIC.md` for a plain-language explanation of the classification formulas and where to find the thresholds.
