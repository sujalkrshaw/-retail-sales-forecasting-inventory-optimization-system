import pandas as pd
import numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

df = pd.read_csv("data/sales.csv")

df_grouped = df.groupby("day")["sales"].sum().reset_index()

X = df_grouped["day"].values.reshape(-1, 1)
y = df_grouped["sales"].values

model = make_pipeline(PolynomialFeatures(degree=2), LinearRegression())
model.fit(X, y)

future = np.array(range(6,11)).reshape(-1,1)
pred = model.predict(future)

print(pred)
