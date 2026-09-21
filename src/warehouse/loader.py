import pandas as pd
from psycopg2.extras import execute_batch
from src.warehouse.connection import get_postgres_connection
from src.utils.config import logger

def execute_ddl(ddl_path: str):
    """Execute SQL DDL scripts to set up schemas."""
    try:
        with open(ddl_path, 'r') as f:
            sql_script = f.read()
        
        with get_postgres_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql_script)
            conn.commit()
        logger.info(f"Successfully executed DDL from {ddl_path}")
    except Exception as e:
        logger.error(f"Error executing DDL {ddl_path}: {e}")
        raise

def load_dimensions(df: pd.DataFrame):
    """Load distinct dimensions incrementally."""
    logger.info("Loading dimension tables...")
    
    airlines = df[['airline']].drop_duplicates().rename(columns={'airline': 'airline_name'})
    routes = df[['route', 'source_city', 'destination_city']].drop_duplicates()
    classes = df[['class']].drop_duplicates().rename(columns={'class': 'class_name'})
    
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            # Load Dim_Airline
            execute_batch(cur, """
                INSERT INTO dim_airline (airline_name) 
                VALUES (%s) ON CONFLICT (airline_name) DO NOTHING;
            """, airlines.values.tolist())
            
            # Load Dim_Route
            execute_batch(cur, """
                INSERT INTO dim_route (route, source_city, destination_city) 
                VALUES (%s, %s, %s) ON CONFLICT (route) DO NOTHING;
            """, routes.values.tolist())
            
            # Load Dim_Class
            execute_batch(cur, """
                INSERT INTO dim_class (class_name) 
                VALUES (%s) ON CONFLICT (class_name) DO NOTHING;
            """, classes.values.tolist())
            
        conn.commit()
    logger.info("Dimension tables loaded successfully.")

def load_facts(df: pd.DataFrame):
    """Load fact table incrementally using UPSERT."""
    logger.info("Loading fact table...")
    
    # We need to map dimension natural keys to surrogate keys
    # To keep it efficient, we load the data and let PostgreSQL look up the keys in the INSERT statement
    
    insert_sql = """
        INSERT INTO fact_flights (
            fact_id, airline_id, route_id, class_id, flight_code, 
            departure_time, arrival_time, stops, duration, days_left, price
        )
        SELECT 
            %s,
            (SELECT airline_id FROM dim_airline WHERE airline_name = %s),
            (SELECT route_id FROM dim_route WHERE route = %s),
            (SELECT class_id FROM dim_class WHERE class_name = %s),
            %s, %s, %s, %s, %s, %s, %s
        ON CONFLICT (fact_id) DO UPDATE SET
            price = EXCLUDED.price,
            duration = EXCLUDED.duration;
    """
    
    records = df[[
        'fact_id', 'airline', 'route', 'class', 'flight',
        'departure_time', 'arrival_time', 'stops_numeric', 'duration', 'days_left', 'price'
    ]].values.tolist()
    
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            execute_batch(cur, insert_sql, records, page_size=1000)
        conn.commit()
        
    logger.info(f"Fact table loaded successfully with {len(records)} records.")

def load_data(df: pd.DataFrame):
    """Main loader orchestration."""
    load_dimensions(df)
    load_facts(df)
