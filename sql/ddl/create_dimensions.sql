CREATE TABLE IF NOT EXISTS dim_airline (
    airline_id SERIAL PRIMARY KEY,
    airline_name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_route (
    route_id SERIAL PRIMARY KEY,
    route VARCHAR(255) UNIQUE NOT NULL,
    source_city VARCHAR(100) NOT NULL,
    destination_city VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_class (
    class_id SERIAL PRIMARY KEY,
    class_name VARCHAR(50) UNIQUE NOT NULL
);
