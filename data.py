import pandas as pd
import numpy as np

data = []

for i in range(30):
    sales = np.random.randint(10, 100)
    data.append(sales)

df = pd.DataFrame(data, columns=["sales"])
df.to_csv("sales.csv", index=False)

print("Data created ✅")