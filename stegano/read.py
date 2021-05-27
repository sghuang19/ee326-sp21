import numpy as np

from typing import Union
from warnings import warn

from utils import lsb, data_to_str
from hamming import decode


def imgread(img: np.ndarray, bits: int = 4, random: bool = True) -> Union[bool, np.ndarray]:
    """
    Read encrypted image.

    :param img: The image carrying the encrypted image.
    :param bits: The number of least significant bits used fro steganography.
    :param random: Fill the least significant bits of the decrypted image with random values, disabled by default
    :return: The decrypted image.
    """

    if not isinstance(img, np.ndarray):
        warn('Incompatible data mode, numpy.ndarray is required.')
        return False

    return (lsb(img, bits) << bits) + (np.random.randint(0, 15, size=img.size).reshape(img.shape) if random else 0)


def strread(img: np.ndarray, bits: int = 4, hamming: bool = False, n: int = 2) -> str:
    """
    Decrypt string from image.
    In the outermost loop, read the data from the highest bit, then the second highest bit, all the way down to the 0th
    bit.
    The pixels are flattened in Fortran style, therefore the information is firstly read along each channel, then each
    column, then each row.
    bit -> channel -> column -> row

    :param img: The image to be decoded.
    :param bits: The number of the least significant bits used for encrypting information.
    :param hamming: If True, hamming encoding is introduced, False by default.
    :param n: The dimension of the hamming data block is specified by 2 ** n, or n << 1
    :return: The decoded string.
    """

    blocks = np.tile(img.flatten(order='F'), bits).reshape(bits, -1)
    blocks = np.array([blocks[i] << 8 - bits + i >> 7 for i in range(bits)])
    if hamming:
        data = decode(blocks.reshape(-1, 1 << (n << 1)), n).reshape(-1, 8)
    else:
        data = blocks.reshape(-1, 8)
    return data_to_str(data)
