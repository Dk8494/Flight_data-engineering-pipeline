-- View: Airline Performance and Pricing Analysis
CREATE OR REPLACE VIEW vw_airline_performance AS
SELECT 
    a.airline_name,
    COUNT(f.fact_id) AS total_flights,
    ROUND(AVG(f.price)::numeric, 2) AS avg_fare,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY f.price) AS median_fare,
    ROUND(AVG(f.duration)::numeric, 2) AS avg_duration,
    ROUND(AVG(f.stops)::numeric, 2) AS avg_stops,
    RANK() OVER(ORDER BY AVG(f.price) DESC) AS price_rank
FROM 
    fact_flights f
JOIN 
    dim_airline a ON f.airline_id = a.airline_id
GROUP BY 
    a.airline_name;

-- Query: Average fare by class for each airline
SELECT 
    a.airline_name,
    c.class_name,
    COUNT(f.fact_id) AS flight_volume,
    ROUND(AVG(f.price)::numeric, 2) AS avg_fare
FROM 
    fact_flights f
JOIN 
    dim_airline a ON f.airline_id = a.airline_id
JOIN
    dim_class c ON f.class_id = c.class_id
GROUP BY 
    a.airline_name, c.class_name
ORDER BY 
    a.airline_name, avg_fare DESC;
