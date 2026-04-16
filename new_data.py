import pandas as pd
import numpy as np

products = ["Milk", "Chips", "Bread", "Soap", "Cola"]

data = []

for day in range(1, 31):
    for product in products:
        sales = np.random.randint(10, 100)
        data.append([day, product, sales])

df = pd.DataFrame(data, columns=["day", "product", "sales"])

print(df.head())

df.to_csv("app/sales.csv", index=False)

print("✅ NEW FILE CREATED SUCCESSFULLY")