import pandas as pd

df = pd.read_csv('raw_data.csv', index_col=None)
df.to_csv('annotated_data.csv', index=False)
df = df[:200]
df.to_csv('sample_annotated_data.csv', index=False)
