import numpy as np 
import pandas as pd
import sqlite3 

#open database 
conn1 = sqlite3.connect('MazakToolDat.db')
conn2 = sqlite3.connect('VC500AM_powder_tooldatabase.db')

# Read tables from the first database
tables1 = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", conn1)
print(tables1)

# Read tables from the second database
tables2 = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", conn2)
#print(tables2)

# Read one table
df1 = pd.read_sql_query("SELECT * FROM tools;", conn1)
print(df1.head())

df2 = pd.read_sql_query("SELECT * FROM tools;", conn2)
#print(df2.head())

# Close the connection
conn1.close()
conn2.close()