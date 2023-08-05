import pandas as pd
import subprocess
import s3fs



def load_validated_breath_dataset():


    s3_url = 's3://raptor-engine/data.csv'

    return pd.read_csv(s3_url, index_col=0)
