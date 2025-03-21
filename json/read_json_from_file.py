import json
import os

cur_path = os.path.dirname(os.path.realpath(__file__))
print(cur_path)

json_path = os.path.join(os.path.dirname(cur_path), 'json')
print(json_path)

# 读取json文件内容,返回字典格式
with open(json_path + "/version.json", 'r', encoding='utf8') as file:
    # loads() :将json字符串转换成字典格式
    json_data = json.load(file)
    print('json数据：', json_data)
    for key, value in json_data.items():
        print(key, ":", value)
