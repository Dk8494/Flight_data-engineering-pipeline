-- View: Route Performance
CREATE OR REPLACE VIEW vw_route_performance AS
SELECT 
    r.route,
    r.source_city,
    r.destination_city,
    COUNT(f.fact_id) AS total_flights,
    ROUND(AVG(f.price)::numeric, 2) AS avg_fare,
    MIN(f.price) AS min_fare,
    MAX(f.price) AS max_fare
FROM 
    fact_flights f
JOIN 
    dim_route r ON f.route_id = r.route_id
GROUP BY 
    r.route, r.source_city, r.destination_city;

-- Query: Top 10 Expensive Routes
SELECT 
    route, 
    total_flights, 
    avg_fare 
FROM 
    vw_route_performance
WHERE 
    total_flights > 50  -- Filtering out routes with very few flights for statistical significance
ORDER BY 
    avg_fare DESC
LIMIT 10;

-- Query: Top 10 Cheapest Routes
SELECT 
    route, 
    total_flights, 
    avg_fare 
FROM 
    vw_route_performance
WHERE 
    total_flights > 50
ORDER BY 
    avg_fare ASC
LIMIT 10;
