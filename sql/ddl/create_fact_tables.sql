CREATE TABLE IF NOT EXISTS fact_flights (
    fact_id VARCHAR(64) PRIMARY KEY, -- MD5 hash of natural keys
    airline_id INT REFERENCES dim_airline(airline_id),
    route_id INT REFERENCES dim_route(route_id),
    class_id INT REFERENCES dim_class(class_id),
    flight_code VARCHAR(50),
    departure_time VARCHAR(50),
    arrival_time VARCHAR(50),
    stops INT CHECK (stops >= 0),
    duration FLOAT CHECK (duration > 0),
    days_left INT CHECK (days_left >= 0),
    price FLOAT CHECK (price > 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index for common analytical queries
CREATE INDEX IF NOT EXISTS idx_fact_flights_airline ON fact_flights(airline_id);
CREATE INDEX IF NOT EXISTS idx_fact_flights_route ON fact_flights(route_id);
CREATE INDEX IF NOT EXISTS idx_fact_flights_price ON fact_flights(price);
