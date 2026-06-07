# System Architecture

![System Data Flow](./architecture.svg)

This system uses a **Functional Core, Imperative Shell** paradigm, implemented as a deterministic data pipeline.

## Architectural Boundaries

* **Functional Core (`analysis/`):** Contains pure, side-effect-free math for ABC/XYZ classification. It accepts standard DataFrames, executes vectorized NumPy/Pandas operations, and returns matrix results. It is fully decoupled from the UI and I/O, allowing for 100% test coverage via `pytest`.
* **Imperative Shell (`services/`, `utils/`, `ui/`):** Handles the "messy" real-world operations—fetching external data from the PrestaShop REST API, parsing local CSV files, and managing the Streamlit dashboard state.
