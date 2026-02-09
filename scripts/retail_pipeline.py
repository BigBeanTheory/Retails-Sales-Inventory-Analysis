import pandas as pd
import mysql.connector
import time

# === Database Connection ===
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="",
            user="",               
            password="",  
            database="retail_db",
            raise_on_warnings=True
        )
        print("Connected to MySQL successfully!")
        return conn
    except mysql.connector.Error as err:
        print(f"Connection error: {err}")
        exit(1)

# === Load and lightly clean the CSV ===
def load_clean_csv(file_path):
    print(f"Loading CSV from: {file_path}")
    df = pd.read_csv(file_path)
    
    # Quick inspection (helpful for debugging)
    print("\nFirst 3 rows of CSV:")
    print(df.head(3))
    print("\nColumns in CSV:", df.columns.tolist())
    print(f"Total rows in CSV: {len(df)}")
    
    # Convert date column (format is YYYY-MM-DD)
    df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d', errors='coerce')
    
    # Drop rows with invalid dates (NaT values)
    rows_before = len(df)
    df = df.dropna(subset=['Date'])
    rows_after = len(df)
    if rows_before != rows_after:
        print(f"\nWarning: Dropped {rows_before - rows_after} rows with invalid dates")
    
    # Ensure boolean conversion (0/1 → True/False)
    if 'Holiday/Promotion' in df.columns:
        df['Holiday/Promotion'] = df['Holiday/Promotion'].astype(bool)
    
    # Fill any rare missing values
    df.fillna({
        'Weather Condition': 'Unknown',
        'Discount': 0.0,
        'Competitor Pricing': df['Price'].mean() if 'Price' in df else 0.0
    }, inplace=True)
    
    print(f"\nFinal cleaned dataset: {len(df)} rows ready for insertion")
    
    return df

# === Insert data in batches (safe for ~73,000 rows) ===
def insert_data_to_mysql(df, batch_size=5000):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    start_time = time.time()
    inserted_count = 0
    
    insert_query = """
    INSERT INTO sales_transactions 
    (date, store_id, product_id, category, region, inventory_level, units_sold, 
     units_ordered, demand_forecast, price, discount, weather_condition, 
     holiday_promotion, competitor_pricing, seasonality)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    for i in range(0, len(df), batch_size):
        batch = df.iloc[i:i + batch_size]
        batch_data = []
        
        for _, row in batch.iterrows():
            values = (
                row['Date'],
                row['Store ID'],
                row['Product ID'],
                row['Category'],
                row['Region'],
                int(row['Inventory Level']),
                int(row['Units Sold']),
                int(row['Units Ordered']),
                float(row['Demand Forecast']),
                float(row['Price']),
                float(row['Discount']),
                row['Weather Condition'],
                int(row['Holiday/Promotion']),          # 0 or 1
                float(row['Competitor Pricing']),
                row['Seasonality']
            )
            batch_data.append(values)
        
        cursor.executemany(insert_query, batch_data)
        conn.commit()
        
        inserted_count += len(batch)
        print(f"Inserted {inserted_count:,} rows so far...")
    
    end_time = time.time()
    print(f"\nSuccess! Inserted {inserted_count:,} rows in {end_time - start_time:.2f} seconds.")
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    csv_path = r"C:\ProgramData\MySQL\MySQL Server 8.0\Uploads\retail_store_inventory.csv"   
    
    df_clean = load_clean_csv(csv_path)
    insert_data_to_mysql(df_clean)