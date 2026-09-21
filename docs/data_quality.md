# Data Quality Report

## Validation Rules
The pipeline enforces the following strict data quality rules:
1. **Schema Adherence**: The incoming dataset must have all required columns. Missing columns result in an immediate pipeline `DataQualityError`.
2. **Non-Null Critical Fields**: Records with missing critical fields are dropped (WARNING).
3. **Logical Numerical Bounds**:
   - `price > 0`: Fares cannot be free or negative.
   - `duration > 0`: Journey times must be positive.
   - `days_left >= 0`: You cannot book a flight in the past.
4. **Deduplication**: Exact duplicate signatures (calculated using `fact_id`) are consolidated to prevent analytics inflation.

## Handling Failures
- Critical failures (e.g. missing CSV, missing columns) will trigger an Airflow task failure (`DataQualityError`, `DataExtractionError`).
- Soft failures (e.g. dropped rows due to missing values or logical bounds) are logged as `WARNING` via the Python `logging` framework.

## Quality Metrics
Metrics such as extraction count and validation drop counts are tracked in the Airflow task logs for observability.
