from sklearn.linear_model import LinearRegression
import numpy as np

def train_model(df):
    X = df["day"].values.reshape(-1, 1)
    y = df["sales"].values

    model = LinearRegression()
    model.fit(X, y)

    return model

def predict_sales(model, days):
    days = np.array(days).reshape(-1, 1)
    return model.predict(days)