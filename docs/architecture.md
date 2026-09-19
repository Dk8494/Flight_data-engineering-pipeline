# Architecture

The Flight Data Engineering & Analytics Platform is built around a modern ETL/ELT paradigm with clear separation of concerns.

## Pipeline Architecture
1. **Source Data**: `flights_data.csv`
2. **Orchestration**: Apache Airflow schedules and runs the pipeline tasks.
3. **Ingestion (Python)**: Reads the raw CSV data into a Pandas DataFrame.
4. **Validation (Python)**: Enforces schema strictness, bounds checking, and null handling.
5. **Transformation (Python)**: Cleans strings, handles categorical data mappings, builds unique surrogate identifiers (fact_id) and derives analytical fields (`route`).
6. **Data Warehouse (PostgreSQL)**: Serves as the persistence and analytics layer. The data is structured using a Star Schema.
7. **Analytics**: SQL Views built on top of the warehouse tables ready for BI ingestion (e.g. Power BI).

## Data Warehouse Model: Star Schema
The PostgreSQL database `flight_warehouse` contains:

- `dim_airline`: Airline names
- `dim_route`: Source and destination relationships
- `dim_class`: Flight class (Economy, Business)
- `fact_flights`: The core transactional table.

### Grain of Fact Table
**"One row represents one observed flight fare for a given itinerary and booking window."**
This is tracked via the `fact_id`, an MD5 hash of `flight_code, source, destination, class, days_left, price`.

## Idempotency
Incremental loading is achieved via a PostgreSQL `UPSERT` statement (`ON CONFLICT (fact_id) DO UPDATE`). This guarantees that running the pipeline multiple times for the same data does not artificially duplicate rows or aggregate sums.
