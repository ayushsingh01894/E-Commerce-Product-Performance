import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

try:
    import numpy, pandas, matplotlib
except ImportError:
    os.system("python -m pip install numpy pandas matplotlib")

# Import Dataset
ECommerceDataset = pd.read_csv(r"C:\Users\windo\Desktop\MCA Project\ecommerce_product_dataset (1).csv")
print("Columns:", ECommerceDataset.columns.tolist())

# Handle Missing Values
for col in ECommerceDataset.select_dtypes(include=[np.number]).columns:
    ECommerceDataset[col] = np.where(ECommerceDataset[col].isna(), ECommerceDataset[col].mean(), ECommerceDataset[col])

# Remove duplicate rows
ECommerceDataset = ECommerceDataset.drop_duplicates()

# Create Charts Directory
charts_dir = r"C:\Users\windo\Desktop\MCA Project\Charts"
if not os.path.exists(charts_dir):
    os.makedirs(charts_dir)
    print(f"Created directory for charts at: {charts_dir}\n")
else:
    print(f"Charts directory already exists at: {charts_dir}\n")

matplotlib.use("Agg")
plt.rcParams.update({'figure.max_open_warning': 0})

# Safe numeric conversion and basic cleaning for columns used in charts
num_cols = ["Selling_Price", "Quantity_Ordered", "Profit", "Ad_Spend", "Rating"]
for c in num_cols:
    if c in ECommerceDataset.columns:
        ECommerceDataset[c] = pd.to_numeric(ECommerceDataset[c], errors="coerce").fillna(0)

# Revenue column
if ("Selling_Price" in ECommerceDataset.columns) and ("Quantity_Ordered" in ECommerceDataset.columns):
    ECommerceDataset["Revenue"] = ECommerceDataset["Selling_Price"] * ECommerceDataset["Quantity_Ordered"]
else:
    ECommerceDataset["Revenue"] = 0

# Parse Order_Date and create month column for time-series
if "Order_Date" in ECommerceDataset.columns:
    ECommerceDataset["Order_Date"] = pd.to_datetime(ECommerceDataset["Order_Date"], errors="coerce")
    ECommerceDataset["Order_Month"] = ECommerceDataset["Order_Date"].dt.to_period("M").astype(str)
else:
    ECommerceDataset["Order_Month"] = ""

# Helper to save and report
def save_fig(fig, name):
    path = os.path.join(charts_dir, name)
    fig.savefig(path, bbox_inches="tight", dpi=150)
    plt.close(fig)
    print(f"Saved chart: {path}")

# 1) Top 10 Brands by Revenue
if "Brand" in ECommerceDataset.columns:
    top_brands = ECommerceDataset.groupby("Brand")["Revenue"].sum().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(10,6))
    top_brands.plot(kind="bar", color=["tab:blue", "tab:cyan", "tab:green", "tab:orange", "tab:red", "tab:purple", "tab:brown", "tab:pink", "tab:gray", "tab:olive"], ax=ax)
    ax.set_title("Top 10 Brands by Revenue")
    ax.set_ylabel("Revenue")
    ax.set_xlabel("Brand")
    save_fig(fig, "top_10_brands_by_revenue.png")

# 2) Revenue by Category
if "Category" in ECommerceDataset.columns:
    cat_rev = ECommerceDataset.groupby("Category")["Revenue"].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(10,6))
    cat_rev.plot(kind="bar", ax=ax, color="tab:green")
    ax.set_title("Revenue by Category")
    ax.set_ylabel("Revenue")
    ax.set_xlabel("Category")
    save_fig(fig, "revenue_by_category.png")

# 3) Top 10 Products by Quantity Sold
if "Product_Name" in ECommerceDataset.columns:
    top_products = ECommerceDataset.groupby("Product_Name")["Quantity_Ordered"].sum().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(10,6))
    top_products.plot(kind="bar", ax=ax, color=["orange", "yellow", "brown", "pink", "cyan", "green", "red", "purple", "gray", "olive"])
    ax.set_title("Top 10 Products by Quantity Sold")
    ax.set_ylabel("Quantity Sold")
    ax.set_xlabel("Product Name")
    save_fig(fig, "top_10_products_by_quantity_sold.png")

# 4) Average Selling Price by Customer Segment
if ("Customer_Segment" in ECommerceDataset.columns) and ("Selling_Price" in ECommerceDataset.columns):
    seg_price = ECommerceDataset.groupby("Customer_Segment")["Selling_Price"].mean()
    fig, ax = plt.subplots(figsize=(7,7))
    seg_price.plot(kind="pie", ax=ax, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
    ax.set_title("Average Selling Price by Customer Segment")
    ax.set_ylabel("")
    save_fig(fig, "avg_selling_price_by_customer_segment.png")

# 5) Profit Margin By Category
if ("Category" in ECommerceDataset.columns) and ("Selling_Price" in ECommerceDataset.columns) and ("Profit" in ECommerceDataset.columns):
    cat_data = ECommerceDataset.groupby("Category").agg({"Selling_Price":"sum", "Profit":"sum"})
    cat_data["Profit_Margin"] = (cat_data["Profit"] / cat_data["Selling_Price"]) * 100
    fig, ax = plt.subplots(figsize=(10,6))
    cat_data["Profit_Margin"].sort_values(ascending=False).plot(kind="barh", ax=ax, color="tab:orange")
    ax.set_title("Profit Margin by Category (%)")
    ax.set_xlabel("Profit Margin (%)")
    save_fig(fig, "profit_margin_by_category.png")


# 6) Stacked Bar Chart of Delivery Status by Category
if ("Delivery_Status" in ECommerceDataset.columns) and ("Category" in ECommerceDataset.columns):
    ds_cat = ECommerceDataset.pivot_table(index="Category", columns="Delivery_Status", aggfunc="size", fill_value=0)
    fig, ax = plt.subplots(figsize=(10,6))
    ds_cat.plot(kind="bar", stacked=True, ax=ax, colormap="tab20")
    ax.set_title("Delivery Status by Category")
    ax.set_ylabel("Number of Orders")
    save_fig(fig, "delivery_status_by_category_stacked.png")

# 7) Profit by Category doguhnut
if "Profit" in ECommerceDataset.columns and "Category" in ECommerceDataset.columns:
    prof_cat = ECommerceDataset.groupby("Category")["Profit"].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(10,6))
    prof_cat.plot(kind="pie", ax=ax, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
    ax.set_title("Profit by Category")
    ax.set_ylabel("")
    save_fig(fig, "profit_by_category_doughnut.png")
    
# 8) Monthly Revenue trend
if "Order_Month" in ECommerceDataset.columns:
    monthly = ECommerceDataset.groupby("Order_Month")["Revenue"].sum().sort_index()
    if not monthly.empty:
        fig, ax = plt.subplots(figsize=(12,5))
        monthly.plot(kind="line", marker="o", ax=ax, color="tab:cyan")
        ax.set_title("Monthly Revenue Trend")
        ax.set_ylabel("Revenue")
        ax.set_xlabel("Order Month")
        plt.xticks(rotation=45)
        save_fig(fig, "monthly_revenue_trend.png")

# 9) Ad_Spend vs Profit scatter
if ("Ad_Spend" in ECommerceDataset.columns) and ("Profit" in ECommerceDataset.columns):
    scatter_df = ECommerceDataset[[ "Ad_Spend", "Profit" ]].dropna()
    if not scatter_df.empty:
        fig, ax = plt.subplots(figsize=(7,6))
        ax.scatter(scatter_df["Ad_Spend"], scatter_df["Profit"], alpha=0.6, s=20)
        ax.set_xlabel("Ad Spend")
        ax.set_ylabel("Profit")
        ax.set_title("Ad Spend vs Profit")
        save_fig(fig, "ad_spend_vs_profit.png")

# 10) Correlation heatmap (numeric columns)
numeric = ECommerceDataset.select_dtypes(include=[np.number]).copy()
if not numeric.empty:
    corr = numeric.corr()
    fig, ax = plt.subplots(figsize=(8,6))
    cax = ax.imshow(corr, cmap="RdYlBu", vmin=-1, vmax=1)
    ax.set_xticks(range(len(corr.columns)))
    ax.set_yticks(range(len(corr.index)))
    ax.set_xticklabels(corr.columns, rotation=90, fontsize=8)
    ax.set_yticklabels(corr.index, fontsize=8)
    fig.colorbar(cax, fraction=0.046, pad=0.04)
    ax.set_title("Correlation Matrix (numeric)")
    save_fig(fig, "numeric_correlation_heatmap.png")

print("\nAll charts generated (if relevant data available) and saved to Charts directory.")

