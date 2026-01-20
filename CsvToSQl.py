import pandas as pd
import sqlite3
# Load CSV file
df = pd.read_csv("ecommerce_product_dataset (1).csv")
# Create SQLite connection
conn = sqlite3.connect("ecommerce.db")
# Write DataFrame to SQL table
df.to_sql("products", conn, if_exists="replace", index=False)
print("Data successfully loaded into SQL database!")
# Close the connection
conn.close()

# .open "C:\\Users\\windo\\Desktop\\MCA Project\\ecommerce.db"
# .output "C:\\Users\\windo\\Desktop\\MCA Project\\export.sql"
# .dump
# .exit
