# region 1. Data Preprocessing
# %% 
# (Your standard scientific cell code goes here)
import pandas as pd
df = pd.read_csv("data.csv")

# endregion

# region 2. Model Training
# %%
from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier()

# endregion