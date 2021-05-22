import numpy as np

from typing import Union
from warnings import warn

from utils import lsb, data_to_str
from hamming import decode


def imgread(img: np.ndarray, bits: int = 4, random: bool = True) -> Union[bool, np.ndarray]:
    if not isinstance(img, np.ndarray):
        warn('Incompatible data type, numpy.ndarray is required.')
        return False

    return (lsb(img, bits) << bits) + (np.random.randint(0, 15, size=img.size).reshape(img.shape) if random else 0)


def strread(img: np.ndarray, bits: int = 4, hamming: bool = False, n: int = 2) -> str:
    """

    :param img:
    :param bits:
    :param hamming:
    :return:
    """

    blocks = np.tile(img.flatten(order='F'), bits).reshape(bits, -1)
    blocks = np.array([blocks[i] & (1 << bits - 1 - i) >> bits - 1 - i for i in range(bits)])
    if hamming:
        data = decode(blocks.reshape(-1, 1 << (n << 1)), n)
    else:
        data = blocks.reshape(-1, 8)
    return data_to_str(data)
