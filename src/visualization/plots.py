import matplotlib.pyplot as plt

def plot_sales_trend(df):
    plt.figure(figsize=(10, 5))
    plt.plot(df["date"], df["sales"])
    plt.title("Sales Trend")
    plt.xlabel("Date")
    plt.ylabel("Sales")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("images/sales_trend.png")
    plt.show()