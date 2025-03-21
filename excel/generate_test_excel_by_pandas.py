import os

import pandas as pd
import openpyxl

df = pd.DataFrame([[11, 21, 31], [12, 22, 32], [31, 32, 33]],
                  index=['one', 'two', 'three'], columns=['a', 'b', 'c'])

print(df)
cur_path = os.path.dirname(os.path.realpath(__file__))
print(cur_path)

data_path = os.path.join(os.path.dirname(cur_path), 'data')
print(data_path)

df.to_excel(data_path + '/generate_test_excel_by_pandas.xlsx', sheet_name='test_pandas')