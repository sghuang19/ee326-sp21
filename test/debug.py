from hamming import decode
from utils import data_to_str

import numpy as np

blocks_r = np.load('blocks_r.npy')
blocks_w = np.load('blocks_w.npy')

data_w = decode(blocks_w, n=2)
str_w = data_to_str(data_w)

data_r = decode(blocks_r, n=2)
str_r = data_to_str(data_r)
