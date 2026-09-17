import os
import pandas as pd
import matplotlib.pyplot as plt

DATA_PATH = "data/sales_data.csv"
OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load data
df = pd.read_csv(DATA_PATH)
df["Order_Date"] = pd.to_datetime(df["Order_Date"])

# Data quality
print("DATASET SHAPE:", df.shape)
print("\nMISSING VALUES:\n", df.isna().sum())
print("\nDUPLICATE ROWS:", df.duplicated().sum())

# Overall KPIs
total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
profit_margin = total_profit / total_sales * 100
avg_order_value = df["Sales"].mean()

print("\nOVERALL PERFORMANCE")
print(f"Total sales: ${total_sales:,.2f}")
print(f"Total profit: ${total_profit:,.2f}")
print(f"Profit margin: {profit_margin:.2f}%")
print(f"Average order value: ${avg_order_value:,.2f}")

# Category analysis
category_summary = (
    df.groupby("Category")[["Sales", "Profit"]]
    .sum()
    .sort_values("Sales", ascending=False)
)
print("\nCATEGORY PERFORMANCE\n", category_summary)

category_summary["Sales"].plot(kind="bar", title="Sales by Category")
plt.ylabel("Sales ($)")
plt.xlabel("Category")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/sales_by_category.png")
plt.close()

# Regional analysis
region_summary = (
    df.groupby("Region")[["Sales", "Profit"]]
    .sum()
    .sort_values("Sales", ascending=False)
)
print("\nREGIONAL PERFORMANCE\n", region_summary)

region_summary["Sales"].plot(kind="bar", title="Sales by Region")
plt.ylabel("Sales ($)")
plt.xlabel("Region")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/sales_by_region.png")
plt.close()

# Monthly trend
monthly_sales = df.set_index("Order_Date").resample("ME")["Sales"].sum()
print("\nMONTHLY SALES\n", monthly_sales)

monthly_sales.plot(kind="line", marker="o", title="Monthly Sales Trend")
plt.ylabel("Sales ($)")
plt.xlabel("Month")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/monthly_sales.png")
plt.close()

# Discount vs profit
print("\nDISCOUNT / PROFIT CORRELATION:", round(df["Discount"].corr(df["Profit"]), 3))

df.plot.scatter(x="Discount", y="Profit", title="Discount vs Profit")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/discount_vs_profit.png")
plt.close()

print("\nAnalysis complete. Charts saved in the outputs/ folder.")
