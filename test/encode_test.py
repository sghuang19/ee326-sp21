import numpy as np
from matplotlib import pyplot as plt
import sys

sys.path.append('../stegano')
from hamming import encode, encode_block

encode_block(np.array([1] * 6))
print('==========')

data1 = np.array([1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1])
print("data1: ")
print(data1)
block1 = encode_block(data1)
print("block1: ")
print(block1)
print('==========')

data2 = np.array([1] * (16 - 5))
print("data2: ")
print(data2)
block2 = encode_block(data2)
print("block2: ")
print(block2)
print('==========')

data3 = np.array([1, 1, 1])
block3 = encode(data3, 1)
print('block3: ')
print(block3)
print('==========')

block4 = encode(data1, 2)
print("block4: ")
print(block4)
