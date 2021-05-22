from typing import Union
from warnings import warn
from functools import reduce

import numpy as np


def encode(data: np.ndarray, n: int = 2):
    """
    Encoding data into several data blocks of size n by n, with hamming redundant bits
    If the size of the data is not enough to fill the last block, zeros are padded
    :param data: the input data series
    :param n: The size of the data block is specified as 2 ** n, or 1 << n
    """

    data_bits = (1 << 2 * n) - (n << 1) - 1
    if data.size % data_bits:
        warn("Not enough data bits, zero-padding is automatically introduced.")
        _data = np.append(data.flat, [0] * ((data.size // data_bits + 1) * data_bits - data.size))
    else:
        _data = np.array(data.flat)
    return np.array([encode_block(_data[i:i + data_bits]) for i in range(0, _data.size, data_bits)])


def encode_block(data: np.ndarray) -> Union[np.ndarray, bool]:
    """
    Calculate the hamming redundant bits and encode which with the original data into a data block.

    :param data: The data bits in one block, the data type of the array must be bool or 1s and 0s.
    :return The complete data block with data bits and hamming redundant bits encoded
    """

    n = 0
    while (1 << 2 * n) - (n << 1) - 1 < data.size:
        n += 1

    if (1 << 2 * n) - (n << 1) - 1 != data.size:
        warn('Wrong number of data bits')
        return False

    parity = [0] + [1 << i for i in range(1 << n)]
    block = []
    i = 0
    for j in range(1 << 2 * n):
        if j in parity:
            block.append(0)
        else:
            block.append(data.flat[i])
            i += 1

    for p in range(n << 1):
        block[1 << p] = reduce(lambda x, y: x ^ y, [bit for i, bit in enumerate(block) if 1 << p & i])
    block[0] = reduce(lambda x, y: x ^ y, block[1:])

    return np.array(block).reshape(1 << n, 1 << n)


def decode(blocks: np.ndarray, n: int = 2) -> np.ndarray:
    """
    Decode the data blocks. Automatic zero-padding takes place when the bits are not enough.
    :param blocks: The blocks series to be decoded.
    :param n: The size of each data block is specified as 2 ** n, or 1 << n
    :return The decoded data
    """

    if blocks.size % 1 << 2 * n:
        warn("Not enough bits, zero-padding is automatically introduced.")
        _blocks = np.append(blocks.flat, [0] * (blocks.size // (1 << 2 * n) + 1) * (1 << 2 * n) - blocks.size)
    else:
        _blocks = np.array(blocks.flat)
    return np.array([decode_block(_blocks[i:i + 1 << 2 * n]) for i in range(0, _blocks.size, 1 << 2 * n)])


def decode_block(block: np.ndarray) -> Union[np.ndarray, bool]:
    """
    Decode a data block with hamming parity bits.
    :param block: The data block to be decoded
    :return the decoded data bits, False if the block is invalid
    """

    if not block.size & block.size - 1 and block.size & 0x5555_5555:
        _block = np.array(block.flat)
        flip = reduce(lambda x, y: x ^ y, [i for i, bit in enumerate(_block) if bit])

        if flip:
            warn("Single bit-flip at index {} corrected".format(flip))
            _block[flip] = not _block[flip]
        elif reduce(lambda x, y: x ^ y, _block):
            warn('Two or more bit-flips occur, self-correction failed.')

        return np.array([bit for i, bit in enumerate(_block) if i and i & i - 1])

    warn('Invalid block size.')
    return False
