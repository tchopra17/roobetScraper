import pandas as pd
import numpy as np
df = pd.read_csv("scraped.csv")
a = df["('Crash Point',)"].str.rstrip("x")
a = a.astype(float)
print(np.median(a))
