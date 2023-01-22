import os

import pandas as pd
import matplotlib.pyplot as plt

df = pd.DataFrame([[11, 21, 31], [12, 22, 32], [31, 23, 33]],
                  columns=['coding_url', 'time', 'soSize'])

print(df)
cur_path = os.path.dirname(os.path.realpath(__file__))
print(cur_path)

data_path = os.path.join(os.path.dirname(cur_path), 'data')
print(data_path)

df.to_excel(data_path + '/generate_coding_build_check_result.xlsx', sheet_name='test_pandas')

print(df['time'])

print(df.head(2))

plt.plot(df["time"], df["soSize"], label='soSize', linewidth=3, color='r', marker='o',
         markerfacecolor='blue', markersize=12)
plt.xlabel("time")
plt.ylabel('soSize')
plt.title("summy of input")
plt.legend()
plt.grid()
plt.show()
