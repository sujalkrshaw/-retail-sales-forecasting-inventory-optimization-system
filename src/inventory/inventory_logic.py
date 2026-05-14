def calculate_inventory_metrics(avg_daily_demand, lead_time, safety_stock, current_stock):
    reorder_point = (avg_daily_demand * lead_time) + safety_stock
    reorder_quantity = max(0, reorder_point - current_stock)

    return {
        "reorder_point": reorder_point,
        "reorder_quantity": reorder_quantity
    }