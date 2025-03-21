import os

import pandas as pd
import sqlite3

cur_path = os.path.dirname(os.path.realpath(__file__))
print(cur_path)

data_path = os.path.join(os.path.dirname(cur_path), 'data')
print(data_path)

result = pd.read_excel(data_path + '/generate_test_excel_by_pandas.xlsx')
print(result)

# 查看指定前几行，默认前5行，指定行数写小括号里
print(result.head())

# 查看数据的（行数、列数）
print(result.shape)

# 查看列索引列表
print(result.columns.values)

# 查看行索引列表
print(result.index.values)

result = pd.read_excel(data_path + '/generate_test_excel_by_pandas.xlsx', 'test_pandas')
print(result)

sqlite_path = os.path.join(os.path.dirname(cur_path), 'sqlite')
print(sqlite_path)

con = sqlite3.connect(sqlite_path + "/xypolice.db")
cur = con.cursor()
# The result of a "cursor.execute" can be iterated over by row
# for row in cur.execute('SELECT * FROM imid_table;'):
#    print(row)

df = pd.read_sql_query("SELECT * from imid_table", con)
# Verify that result of SQL query is stored in the dataframe
print(df.head())

cur.close()
# Be sure to close the connection
con.close()

