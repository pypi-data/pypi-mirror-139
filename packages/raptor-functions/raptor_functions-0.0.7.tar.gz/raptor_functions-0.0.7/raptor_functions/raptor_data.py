import pandas as pd




def load_data():
    return pd.read_csv('../data.csv', index_col=0)