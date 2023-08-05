import pandas as pd

def max_value(data: pd.DataFrame):
    if not data["value"].dropna().empty:
        return max(data["value"].dropna())
    else: return "Undefinded"

def min_value(data: pd.DataFrame):
    if not data["value"].dropna().empty:
        return min(data["value"].dropna())
    else: return "Undefinded"

def stats(data: pd.DataFrame):

    return max_value(data), min_value(data)