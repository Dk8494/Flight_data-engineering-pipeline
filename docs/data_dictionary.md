# Data Dictionary

## fact_flights
| Column | Type | Description | Business Meaning |
|--------|------|-------------|------------------|
| fact_id | VARCHAR | MD5 Hash Surrogate Key | Unique ID for the observed fare |
| airline_id | INT | Foreign Key to dim_airline | Airline carrying the flight |
| route_id | INT | Foreign Key to dim_route | The path of the flight |
| class_id | INT | Foreign Key to dim_class | Ticket class |
| flight_code | VARCHAR | Source Flight ID | The specific flight code |
| departure_time | VARCHAR | Categorical | Time of day flight leaves |
| arrival_time | VARCHAR | Categorical | Time of day flight arrives |
| stops | INT | Integer | Number of layovers |
| duration | FLOAT | Decimal | Total journey time in hours |
| days_left | INT | Integer | Days between booking and travel |
| price | FLOAT | Decimal | Ticket fare |
| created_at | TIMESTAMP| Metadata | Time record was inserted |

## dim_airline
| Column | Type | Description |
|--------|------|-------------|
| airline_id | INT (PK) | Surrogate Key |
| airline_name| VARCHAR | Title-cased airline name |

## dim_route
| Column | Type | Description |
|--------|------|-------------|
| route_id | INT (PK) | Surrogate Key |
| route | VARCHAR | source-destination format |
| source_city | VARCHAR | Title-cased origin |
| destination_city| VARCHAR | Title-cased destination |

## dim_class
| Column | Type | Description |
|--------|------|-------------|
| class_id | INT (PK) | Surrogate Key |
| class_name | VARCHAR | Economy or Business |
