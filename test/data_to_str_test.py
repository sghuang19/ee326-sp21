import numpy as np
from utils import data_to_str, str_to_data

data1 = str_to_data('a')
str1 = data_to_str(data1)
print(data1, str1)

data2 = str_to_data('aaaa')
str2 = data_to_str(data2)
print(data2, str2)

with open("../stegano/zen.txt", 'r') as f:
    zen = f.read()

data3 = str_to_data(zen)
str3 = data_to_str(data3)
print(str3)
