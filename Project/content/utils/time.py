import pandas as pd

def to_time(x):
    return pd.to_datetime(x)

def to_hours(x):
    return x.strftime("%H:%M:%S")