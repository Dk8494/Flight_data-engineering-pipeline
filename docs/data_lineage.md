# Data Lineage

The data flows systematically from raw extraction to analytical views:

```mermaid
graph TD
    A[Source CSV: flights_data.csv] -->|Extract| B[Pandas DataFrame]
    B -->|Validate Schema & Bounds| C[Clean DataFrame]
    C -->|Transform: Normalize, Hash Keys, Create Route| D[Transformed DataFrame]
    
    D -->|Load Dimensions| E[(dim_airline)]
    D -->|Load Dimensions| F[(dim_route)]
    D -->|Load Dimensions| G[(dim_class)]
    
    D -->|Load Facts (UPSERT)| H[(fact_flights)]
    
    E -.-> H
    F -.-> H
    G -.-> H
    
    H -->|SQL View| I[vw_airline_performance]
    H -->|SQL View| J[vw_route_performance]
    
    I -->|BI Tools| K[Power BI Dashboard]
    J -->|BI Tools| K
```
