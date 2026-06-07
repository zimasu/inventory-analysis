# Inventory ABC/XYZ Analysis

A desktop-packaged Streamlit application that classifies inventory items by revenue contribution (ABC) and demand stability (XYZ). It identifies high-value stock, volatile demand tracks, and potential dead weight.

## Core Capabilities
* **ABC/XYZ Matrix Evaluation:** Automatically segments inventory profiles based on running cumulative revenues and coefficients of variation.
* **Data Integration:** Dynamically interfaces with PrestaShop REST endpoints to synchronize product listings, stocks, and monthly distributions.
* **Local Processing:** Formatted to ingest raw CSV data sheets natively and compute classification trends locally.
* **Test Configurations:** Pytest implementation included to confirm calculation formulas against explicit data thresholds.

## Project Architecture
* `analysis/` — Mathematical classification math models (ABC/XYZ matrices)
* `charts/` — Interactive dashboard plot elements
* `ui/` — Streamlit view layers and sidebars
* `utils/` — Internal data transformers and file handling wrappers
* `tests/` — Unit test validation suite running on pytest
* `app.py` — Cached API syncing and dashboard launcher
* `config.py` — Central schemas, environment routes, and calculation cutoffs

## Running Locally

### Option 1: Standalone Windows App (No Python Required)
1. Navigate to Releases on the right sidebar.
2. Download and unzip InventoryAnalysis.zip.
3. Launch InventoryAnalysis.exe.

### Option 2: Run via CLI (Python 3.11+)
1. Install dependencies:
   pip install -r requirements.txt
2. Launch the Streamlit server:
   streamlit run app.py

## Input File Format
If running via raw data ingestion manually without the PrestaShop API hook, supply an inventory_sample.csv matching this structure:
* item_code / item_name / category (Text identifiers)
* unit_cost / unit_price / units_in_stock (Numerical metrics)
* monthly_sales_jan through monthly_sales_dec (Twelve consecutive months of sales integers)

## Testing
To execute verification points:
pytest tests/
