# Flight Data Engineering & Analytics Platform

## Overview
This repository contains a professional, end-to-end Data Engineering pipeline designed to orchestrate, validate, transform, and load flight pricing data into a robust Data Warehouse for Business Intelligence and Analytics.

The initial machine learning experimental notebook has been preserved in `notebooks/optional_analysis.ipynb`. The current focus is entirely on solid Data Engineering principles: Correctness, Data Quality, Reproducibility, and Observability.

## Business Problem
Airlines and dynamic pricing systems generate massive amounts of flight scheduling and pricing data. To derive business insights (e.g., optimizing booking windows, comparing route competitiveness, and tracking competitor airline fares), this raw data must be structurally warehoused and cleanly modeled into a Star Schema.

## Architecture
The platform is orchestrated via **Apache Airflow**. The ETL pipeline comprises Python scripts to process data and PostgreSQL to serve as the analytical data warehouse. Power BI acts as the BI presentation layer.

1. **Extraction**: Raw data is pulled and parsed by Pandas.
2. **Validation**: Quality checks enforce schema compliance, non-null fields, and mathematical bounds (e.g., `price > 0`).
3. **Transformation**: String normalization, route calculation, and MD5 surrogate key generation for idempotency.
4. **Loading**: Data is loaded incrementally via UPSERT into a PostgreSQL Star Schema.
5. **Analytics**: Pre-computed SQL views fuel BI dashboards.

## Data Source
The pipeline processes the `flights_data.csv` dataset, which includes attributes like:
`airline`, `flight`, `source_city`, `departure_time`, `stops`, `arrival_time`, `destination_city`, `class`, `duration`, `days_left`, `price`.

## Data Warehouse & Star Schema
The PostgreSQL database `flight_warehouse` implements a Star Schema:
- **Dimensions**: `dim_airline`, `dim_route`, `dim_class`
- **Fact**: `fact_flights` (Grain: One row per observed flight fare itinerary)

## Incremental Loading
The data loader leverages an idempotent approach. A unique `fact_id` is generated as an MD5 hash of natural keys. The PostgreSQL `ON CONFLICT DO UPDATE` clause ensures that rerunning the pipeline will update records instead of duplicating them.

## Technology Stack
- **Python 3.10**: Primary language.
- **Pandas**: Data transformation and validation.
- **Apache Airflow**: Workflow orchestration.
- **PostgreSQL**: Data Warehouse.
- **Docker & Docker Compose**: Containerization.
- **Pytest**: Unit testing.
- **GitHub Actions**: CI pipeline.
- **Power BI**: Analytics dashboards.

## Project Structure
```text
Flight-Data-Engineering/
├── data/raw/             # Source data (flights_data.csv)
├── dags/                 # Airflow DAGs
├── src/                  # Python ETL modules
│   ├── ingestion/
│   ├── validation/
│   ├── transformation/
│   ├── warehouse/
│   └── utils/
├── sql/                  # DDL and Analytics queries
├── tests/                # Pytest suites
├── docs/                 # Architecture, Lineage, Data Quality
├── dashboard/            # Power BI instructions
├── notebooks/            # Preserved ML Notebooks
├── docker/               # PostgreSQL init scripts
└── .github/workflows/    # CI Pipeline
```

## Local Setup & Running the Pipeline
To run the platform locally, ensure you have Docker installed.

1. **Start Services**
```bash
docker compose up -d --build
```
2. **Access Airflow**
Navigate to `http://localhost:8080`.
Username: `airflow`
Password: `airflow`
3. **Run Pipeline**
Trigger the `flight_data_pipeline` DAG manually from the Airflow UI.

## Running Tests
Tests are executed using `pytest`.
```bash
pip install -r requirements.txt
pytest tests/ -v
```

## Limitations & Future Improvements
- **Data Source Limitation**: The dataset is relatively static. Real incremental loading relies on the MD5 hash of facts; if a true time-series delta API were provided, the extraction layer would filter by delta timestamps.
- **Cloud Extension**: Currently localized via Docker. A future iteration could deploy Airflow to AWS MWAA, use S3 for raw staging, and Amazon Redshift for the Data Warehouse.
