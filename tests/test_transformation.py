import pandas as pd
from src.transformation.transform import transform_data

def test_transformation():
    df = pd.DataFrame({
        'airline': ['indigo', 'spiceJet'],
        'flight': ['IN-123', 'SG-123'],
        'source_city': ['delhi', 'Mumbai'],
        'departure_time': ['Morning', 'Afternoon'],
        'stops': ['zero', 'one'],
        'arrival_time': ['Night', 'Night'],
        'destination_city': ['mumbai', 'delhi'],
        'class': ['economy', 'business'],
        'duration': [2.5, 3.0],
        'days_left': [10, 5],
        'price': [5000, 15000]
    })
    
    transformed_df = transform_data(df)
    
    assert transformed_df.iloc[0]['airline'] == 'Indigo'
    assert transformed_df.iloc[0]['route'] == 'Delhi-Mumbai'
    assert transformed_df.iloc[0]['stops_numeric'] == 0
    assert transformed_df.iloc[1]['stops_numeric'] == 1
    assert 'fact_id' in transformed_df.columns

def test_idempotency_duplicate_removal():
    df = pd.DataFrame({
        'airline': ['indigo', 'indigo'],
        'flight': ['IN-123', 'IN-123'],
        'source_city': ['delhi', 'delhi'],
        'departure_time': ['Morning', 'Morning'],
        'stops': ['zero', 'zero'],
        'arrival_time': ['Night', 'Night'],
        'destination_city': ['mumbai', 'mumbai'],
        'class': ['economy', 'economy'],
        'duration': [2.5, 2.5],
        'days_left': [10, 10],
        'price': [5000, 5000]
    })
    transformed_df = transform_data(df)
    assert len(transformed_df) == 1
