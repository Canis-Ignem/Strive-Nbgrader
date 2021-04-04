import pandas as pd
import sqlite3 as sql

con = sql.connect("/home/jon/gradebook.db")

df = pd.read_sql_query("SELECT auto_score FROM grade", con)

print(df)