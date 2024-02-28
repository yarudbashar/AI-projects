import pandas as pd
import sqlite3

# Replace these file paths with your own CSV file and SQLite database file
csv_file = 'sentiment_nt.csv'
sqlite_db = 'output.db'

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(csv_file, usecols=[0])  # Read only the first column

# Create a new SQLite database and connect to it
conn = sqlite3.connect(sqlite_db)

# Create a table in the database with a 'review_text' column
table_name = 'reviews'
df.columns = ['review_text']  # Rename the column to 'review_text'
df.to_sql(table_name, conn, if_exists='replace', index=False)

# Commit the changes and close the database connection
conn.commit()
conn.close()

print(f"Data from the first column of the CSV file has been copied to '{sqlite_db}' in the '{table_name}' table with a 'review_text' column.")
