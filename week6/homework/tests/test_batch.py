import batch
import pandas as pd
from pandas.testing import assert_frame_equal

from datetime import datetime

def dt(hour, minute, second=0):
    return datetime(2022, 1, 1, hour, minute, second)

def test_prep_data():
    data = [
    (None, None, dt(1, 2), dt(1, 10)),
    (1, None, dt(1, 2), dt(1, 10)),
    (1, 2, dt(2, 2), dt(2, 3)),
    (None, 1, dt(1, 2, 0), dt(1, 2, 50)),
    (2, 3, dt(1, 2, 0), dt(1, 2, 59)),
    (3, 4, dt(1, 2, 0), dt(2, 2, 1)),     
    ]

    columns = ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime']
    df = pd.DataFrame(data, columns=columns)
    df_prepped = batch.prepare_data(df, ['PULocationID', 'DOLocationID'])

    # expecting additional column
    expected_cols = columns
    expected_cols.append('duration')

    # fillna(-1) and include duration > 0 and duration < 60
    expected_data = [
    ('-1', '-1', dt(1, 2), dt(1, 10), 8),
    ('1', '-1', dt(1, 2), dt(1, 10), 8),
    ('1', '2', dt(2, 2), dt(2, 3), 1),    
    ]
    df_expected = pd.DataFrame(expected_data, columns=expected_cols)

    assert_frame_equal(df_prepped, df_expected, check_dtype=False)    