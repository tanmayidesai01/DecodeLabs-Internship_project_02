
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel(
    r"C:\Users\hp\Downloads\decode\Dataset_for_Data_Analytics.xlsx"
)

print("Dataset Shape:", df.shape)
print(df.head())
print("--- Dataset Overview ---")
print("Dataset Shape:", df.shape)
print("\nColumn Names:")
print(df.columns.tolist())

# 2. Missing Values
print("\n--- Missing Values ---")
print(df.isnull().sum())

# 3. Basic Statistics
numeric_columns = [
    "Quantity", "UnitPrice", "ItemsInCart", "TotalPrice"
]

print("\n--- Basic Statistics ---")
print(df[numeric_columns].describe())

print("\nCount:")
print(df[numeric_columns].count())

print("\nMean:")
print(df[numeric_columns].mean())

print("\nMedian:")
print(df[numeric_columns].median())

# 4. Outlier Analysis using IQR
print("\n--- Outlier Analysis ---")

for col in numeric_columns:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1

    lower_limit = Q1 - 1.5 * IQR
    upper_limit = Q3 + 1.5 * IQR

    outliers = df[
        (df[col] < lower_limit) |
        (df[col] > upper_limit)
    ]

    print(f"\n{col}:")
    print("Q1:", Q1)
    print("Q3:", Q3)
    print("IQR:", IQR)
    print("Lower Limit:", lower_limit)
    print("Upper Limit:", upper_limit)
    print("Number of Outliers:", len(outliers))

# 5. TotalPrice Outliers
print("\n--- TotalPrice Outliers ---")

Q1 = df["TotalPrice"].quantile(0.25)
Q3 = df["TotalPrice"].quantile(0.75)
IQR = Q3 - Q1

lower_limit = Q1 - 1.5 * IQR
upper_limit = Q3 + 1.5 * IQR

totalprice_outliers = df[
    (df["TotalPrice"] < lower_limit) |
    (df["TotalPrice"] > upper_limit)
]

print(totalprice_outliers[
    ["OrderID", "Product", "Quantity",
     "UnitPrice", "TotalPrice"]
])

# 6. Date and Yearly Order Trend
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df["Year"] = df["Date"].dt.year

yearly_orders = df.groupby("Year")["OrderID"].nunique()

print("\n--- Yearly Order Trend ---")
print(yearly_orders)

plt.figure(figsize=(8, 5))
plt.bar(yearly_orders.index.astype(str), yearly_orders.values)
plt.title("Number of Orders by Year")
plt.xlabel("Year")
plt.ylabel("Number of Orders")
plt.tight_layout()
plt.savefig("yearly_orders.png")
plt.show()

# 7. Product Order Analysis
print("\n--- Product Order Analysis ---")

product_orders = df.groupby("Product")["OrderID"].nunique()
product_orders = product_orders.sort_values(ascending=False)

print(product_orders)

plt.figure(figsize=(10, 5))
plt.bar(product_orders.index.astype(str), product_orders.values)
plt.title("Number of Orders by Product")
plt.xlabel("Product")
plt.ylabel("Number of Orders")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("product_orders.png")
plt.show()

# 8. Payment Method Analysis
print("\n--- Payment Method Analysis ---")

payment_counts = df["PaymentMethod"].value_counts()
print(payment_counts)

plt.figure(figsize=(8, 5))
plt.bar(payment_counts.index.astype(str), payment_counts.values)
plt.title("Orders by Payment Method")
plt.xlabel("Payment Method")
plt.ylabel("Number of Records")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("payment_methods.png")
plt.show()

# 9. Order Status Analysis
print("\n--- Order Status Analysis ---")

status_counts = df["OrderStatus"].value_counts()
print(status_counts)

plt.figure(figsize=(8, 5))
plt.bar(status_counts.index.astype(str), status_counts.values)
plt.title("Orders by Order Status")
plt.xlabel("Order Status")
plt.ylabel("Number of Records")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("order_status.png")
plt.show()

# 10. Total Sales Analysis
print("\n--- Total Sales Analysis ---")

total_sales = df["TotalPrice"].sum()
average_order_value = df["TotalPrice"].mean()

print("Total Sales:", total_sales)
print("Average Record Value:", average_order_value)

# 11. Distribution Analysis
print("\n--- Distribution Analysis ---")

for col in numeric_columns:
    plt.figure(figsize=(8, 5))
    plt.hist(df[col].dropna(), bins=20, edgecolor="black")
    plt.title(f"Distribution of {col}")
    plt.xlabel(col)
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(f"{col}_distribution.png")
    plt.show()

# 12. Correlation Analysis
print("\n--- Correlation Analysis ---")

correlation_matrix = df[numeric_columns].corr()
print(correlation_matrix)

plt.figure(figsize=(8, 6))
plt.imshow(correlation_matrix, cmap="coolwarm", vmin=-1, vmax=1)
plt.colorbar()

plt.xticks(
    range(len(correlation_matrix.columns)),
    correlation_matrix.columns,
    rotation=45
)
plt.yticks(
    range(len(correlation_matrix.columns)),
    correlation_matrix.columns
)

plt.title("Correlation Matrix")
plt.tight_layout()
plt.savefig("correlation_matrix.png")
plt.show()

# 13. Key Observations
print("\n--- Key Observations ---")

highest_product = product_orders.idxmax()
lowest_product = product_orders.idxmin()
highest_payment = payment_counts.idxmax()
highest_status = status_counts.idxmax()

print("Most Ordered Product:", highest_product)
print("Least Ordered Product:", lowest_product)
print("Most Used Payment Method:", highest_payment)
print("Most Common Order Status:", highest_status)

if not yearly_orders.empty:
    print("Year with Highest Orders:", yearly_orders.idxmax())
    print("Year with Lowest Orders:", yearly_orders.idxmin())

print("Total Sales:", total_sales)
print("Average Record Value:", average_order_value)

print("\nEDA Completed Successfully!")