from typing import Union
from warnings import warn
from functools import reduce

import numpy as np


def encode(data: np.ndarray, n: int = 2) -> np.ndarray:
    """
    Encoding data into several data blocks of size n by n, with hamming redundant bits
    If the size of the data is not enough to fill the last block, zeros are padded

    :param data: the input data series
    :param n: The size of the data block is specified as 2 ** n, or 1 << n
    """

    _data_bits = data_bits(n)
    _data = data.flatten()
    if data.size % _data_bits:
        warn("Not enough data bits, zero-padding is automatically introduced.")
        _data = np.append(_data, np.zeros(_data_bits - (data.size - 1) % _data_bits - 1)
                          ).astype(np.uint8)
    _data = _data.reshape(-1, _data_bits)
    return np.array([encode_block(block) for block in _data])


def encode_block(data: np.ndarray) -> Union[np.ndarray, bool]:
    """
    Calculate the hamming redundant bits and encode which with the original data into a data block.

    :param data: The data bits in one block, the data mode of the array must be bool or 1s and 0s.
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

    block_size = 1 << (n << 1)
    if blocks.size % block_size:
        warn("Not enough bits, zero-padding is automatically introduced.")
        _blocks = np.append(blocks.flat, np.zeros(block_size - (blocks.size - 1) % block_size - 1))
    else:
        _blocks = blocks.flatten()
    _blocks = _blocks.reshape(-1, 1 << (n << 1))
    return np.array([decode_block(block) for block in _blocks])


def decode_block(block: np.ndarray) -> Union[np.ndarray, bool]:
    """
    Decode a data block with hamming parity bits.

    :param block: The data block to be decoded
    :return the decoded data bits, False if the block is invalid
    """

    if not block.size & block.size - 1 and block.size & 0x5555_5555:
        _block = np.array(block.flat)
        flip = reduce(lambda x, y: x ^ y, [i for i, bit in enumerate(_block) if bit] + [1, 1])

        if flip:
            warn("Single bit-flip at index {} corrected".format(flip))
            _block[flip] = not _block[flip]
        elif reduce(lambda x, y: x ^ y, _block):
            warn('Two or more bit-flips occur, self-correction failed.')

        return np.array([bit for i, bit in enumerate(_block) if i and i & i - 1])

    warn('Invalid block size.')
    return False


def data_bits(n: int = 2):
    """
    Calculate the data bits in one hamming data block.

    :param n: The dimension of the hamming data block is specified by 2 ** n or n << 1
    :return: The number of valid data bits carrying information in one hamming data block.
    """

    return (1 << 2 * n) - (n << 1) - 1


def str_pad(info: str, n: int = 2) -> str:
    """
    Pad a string with protective [NUL] character \x00 to avoid wraparound errors in steganography when hamming encoding
    is enabled.

    :param info: The string to be padded
    :param n: The size of the hamming block is specified by 2 ** n, or n << 1
    :return: The padded string.
    """

    return info + '\x00' * (data_bits(n) - (len(info) - 1) % data_bits(n) - 1)
