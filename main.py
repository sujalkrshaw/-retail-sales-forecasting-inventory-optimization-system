from src.data_processing.load_data import load_data
from src.data_processing.preprocess import preprocess_data
from src.features.build_features import create_features
from src.models.train_model import train_model
from src.inventory.inventory_logic import calculate_inventory_metrics
from src.visualization.plots import plot_sales_trend

def main():
    file_path = "data/retail_sales_data.csv"

    df = load_data(file_path)
    df = preprocess_data(df)
    df = create_features(df)

    plot_sales_trend(df)

    model = train_model(df)

    avg_daily_demand = df["sales"].mean()
    lead_time = 7
    safety_stock = 20
    current_stock = int(df["current_stock"].iloc[-1])

    inventory_result = calculate_inventory_metrics(
        avg_daily_demand, lead_time, safety_stock, current_stock
    )

    print("\nInventory Recommendation")
    print("Reorder Point:", round(inventory_result["reorder_point"], 2))
    print("Reorder Quantity:", round(inventory_result["reorder_quantity"], 2))

if __name__ == "__main__":
    main()