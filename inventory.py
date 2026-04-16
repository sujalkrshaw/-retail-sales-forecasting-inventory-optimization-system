import pandas as pd

df = pd.read_csv("app/sales.csv")

avg_sales = df.groupby("product")["sales"].mean()

lead_time = 5
safety_stock = 20

inventory = []

# Assume current stock
current_stock = {
    "Milk": 200,
    "Chips": 300,
    "Bread": 250,
    "Soap": 400,
    "Cola": 150
}

for product in avg_sales.index:
    avg = avg_sales[product]
    reorder_point = (avg * lead_time) + safety_stock
    
    stock = current_stock[product]
    
    if stock < reorder_point:
        status = "⚠️ Reorder Needed"
    else:
        status = "✅ Stock OK"
    
    inventory.append([product, avg, reorder_point, stock, status])

inventory_df = pd.DataFrame(
    inventory,
    columns=["Product", "Avg Sales", "Reorder Point", "Current Stock", "Status"]
)

print(inventory_df)