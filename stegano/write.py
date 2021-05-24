from PIL import Image
import numpy as np

from typing import Union
from warnings import warn

from utils import msb, resize, str_to_data
from hamming import encode, str_pad

sevilla = np.asarray(Image.open('../img/sevilla.jpg'))
sherlock = np.asarray(Image.open('../img/sherlock.jpg'))


def imgwrite(info: np.ndarray = sherlock, target: np.ndarray = sevilla, bits: int = 4,
             interp=Image.BILINEAR) -> Union[bool, np.ndarray]:
    """
    Encrypt info into an image. If the dimension of the image to be encrypted and the target is not compatible,
    the info image is automatically stretched.

    :param info: The image to be encrypted, sherlock.jpg by default
    :param target: The image into which the info is encrypted, sevilla.jpg by default
    :param bits: The number of least significant bits chosen, 4 by default
    :param interp: The interpolation method, would be used when automatically resize takes place, BILINEAR by default
    :return: The image with encrypted information, in numpy.ndarray type, False if encryption failed
    """

    if not isinstance(info, np.ndarray) or not isinstance(target, np.ndarray):
        warn('Incompatible data type, numpy.ndarray is required.')
        return False

    _info = np.array(info)
    if info.shape != target.shape:
        warn('Incompatible dimension, image is automatically reshaped to the size of the target.')
        _info = resize(info, target=target, interp=interp)

    return (msb(target, bits) << bits) + msb(_info, bits)


def strwrite(info: str, target=sevilla, bits: int = 4, hamming=False, n: int = 2) -> np.ndarray:
    """
    Encrypt string into an image. In the outermost loop, write the data into the highest bit, then the second highest
    bit, all the way down to the 0th it. The pixels are flattened in Fortran style, therefore the information is
    firstly write along each channel, then each column, then each row. bit -> channel -> column -> row

    :param info: The information to be encoded into the target image, must be str type.
    :param target: The target image, sevilla.jpg by default.
    :param bits: The number of the least significant bits used for encrypting information.
    :param hamming: If True, hamming encoding is introduced, False by default.
    :param n: The dimension of the hamming data block is specified by 2 ** n, or n << 1
    :return The image with the information encrpyted in.
    """

    blocks = str_to_data(str_pad(info) if hamming else info)
    if hamming:
        blocks = encode(blocks, n)
    if blocks.size // bits > target.size:
        warn("The size of the target image is not enough, part of the data will not be encoded.")

    blocks = np.append(np.tile(blocks.flatten(), target.size * bits // blocks.size),
                       blocks.flat[:target.size * bits % blocks.size]).reshape(bits, target.size)
    return np.sum(np.fromfunction(lambda x, y: 1 << bits - 1 - x, (bits, target.size), dtype=np.uint8) * blocks,
                  axis=0, dtype=np.uint8).reshape(*target.shape, order='F') + (msb(target, bits) << 8 - bits)
