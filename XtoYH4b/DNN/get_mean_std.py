import pandas as pd

df = pd.read_csv('data.csv')

means = df.mean()
stds = df.std()

for column in df.columns:
    print(f"{column}: mean = {means[column]:.4f}, std = {stds[column]:.4f}")