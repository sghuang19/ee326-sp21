import numpy as np
import sys

sys.path.append('../stegano')
from hamming import decode, decode_block

block1 = np.array([[1, 1, 0, 1],
                   [0, 1, 0, 0],
                   [1, 1, 0, 1],
                   [1, 0, 1, 1]])
data1 = decode_block(block1)
print("data 1:\n", data1)

block2 = np.array(block1).flatten()
block2[10] = not block2[10]
data2 = decode_block(block2)
print("data 2:\n", data2)

data3 = decode(block2)
print('data3: \n', data3)

block4 = np.array([block2, ] * 2)
data4 = decode(block4)
print('data4: \n', data4)
