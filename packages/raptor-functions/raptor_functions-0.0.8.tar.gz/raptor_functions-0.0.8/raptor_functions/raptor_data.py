import pandas as pd




def load_validated_breath_dataset():
    return pd.read_csv('../data.csv', index_col=0)