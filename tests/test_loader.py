import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
from src.warehouse.loader import load_dimensions, load_facts

@patch('src.warehouse.loader.execute_batch')
@patch('src.warehouse.loader.get_postgres_connection')
def test_load_dimensions(mock_get_conn, mock_execute_batch):
    mock_conn = MagicMock()
    mock_get_conn.return_value.__enter__.return_value = mock_conn
    
    df = pd.DataFrame({
        'airline': ['Indigo'],
        'route': ['Delhi-Mumbai'],
        'source_city': ['Delhi'],
        'destination_city': ['Mumbai'],
        'class': ['Economy']
    })
    
    load_dimensions(df)
    assert mock_conn.cursor.called
    assert mock_conn.commit.called
    assert mock_execute_batch.called

@patch('src.warehouse.loader.execute_batch')
@patch('src.warehouse.loader.get_postgres_connection')
def test_load_facts(mock_get_conn, mock_execute_batch):
    mock_conn = MagicMock()
    mock_get_conn.return_value.__enter__.return_value = mock_conn
    
    df = pd.DataFrame({
        'fact_id': ['abc123hash'],
        'airline': ['Indigo'],
        'route': ['Delhi-Mumbai'],
        'class': ['Economy'],
        'flight': ['IN-123'],
        'departure_time': ['Morning'],
        'arrival_time': ['Night'],
        'stops_numeric': [0],
        'duration': [2.5],
        'days_left': [10],
        'price': [5000]
    })
    
    load_facts(df)
    assert mock_conn.cursor.called
    assert mock_conn.commit.called
    assert mock_execute_batch.called
