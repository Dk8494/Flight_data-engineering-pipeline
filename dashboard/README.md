# Power BI Dashboard Architecture

## Data Source
The dashboard connects directly to the PostgreSQL `flight_warehouse` database.
Instead of querying raw tables directly, Power BI consumes the curated analytical views located in `sql/analytics/`.

## Tables & Views Used
- `vw_airline_performance`
- `vw_route_performance`
- `fact_flights` (joined with dimensions for detailed drill-throughs)

## Recommended DAX Measures
Create the following DAX measures in your Power BI model for dynamic analytics:

```dax
Total Flights = COUNTROWS('fact_flights')
Average Fare = AVERAGE('fact_flights'[price])
Median Fare = MEDIAN('fact_flights'[price])
Minimum Fare = MIN('fact_flights'[price])
Maximum Fare = MAX('fact_flights'[price])
Average Duration = AVERAGE('fact_flights'[duration])
Average Stops = AVERAGE('fact_flights'[stops])
```

## Recommended Layout

### Page 1: Executive Overview
- **KPI Cards**: Total Flights, Average Fare, Median Fare, Average Duration.
- **Bar Chart**: Average Fare by Airline.
- **Donut Chart**: Flight Volume by Class.
- **Line Chart**: Average Fare by Stops.

### Page 2: Route Analysis
- **Table**: Top 10 Expensive Routes (Route, Flights, Avg Fare).
- **Table**: Top 10 Cheapest Routes.
- **Map Visual** (if lat/long added): Route volumes.

### Page 3: Pricing Analysis
- **Scatter Plot**: Fare vs Duration.
- **Line Chart**: Average Fare vs Days Left (Booking Window).

### Page 4: Airline Performance
- **Matrix**: Airline (Rows) vs Class (Columns) -> Values: Average Fare.
- **Bar Chart**: Average Duration by Airline.
