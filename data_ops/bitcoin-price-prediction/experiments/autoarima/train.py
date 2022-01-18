import os
import pandas as pd
from sklearn.model_selection import TimeSeriesSplit

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'data', 'Bitcoin_071911_081921.csv')


# df = pd.read_csv(DATA_PATH)

# print(df.head(10))

tscv = TimeSeriesSplit()
print(tscv)