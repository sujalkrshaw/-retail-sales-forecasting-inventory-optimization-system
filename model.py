import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

# Load data
df = pd.read_csv("app/sales.csv")

# Prepare data
df_grouped = df.groupby("day")["sales"].sum().reset_index()

X = df_grouped["day"].values.reshape(-1, 1)
y = df_grouped["sales"].values

# Train model
model = LinearRegression()
model.fit(X, y)

# Predict next 7 days
future_days = np.array(range(31, 38)).reshape(-1, 1)
predictions = model.predict(future_days)

print("Future Sales Prediction:")
for i, val in enumerate(predictions):
    print(f"Day {31+i}: {int(val)}")