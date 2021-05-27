from PIL import Image
import numpy as np

from hamming import str_pad

"""
Functions that may be useful.
"""


def msb(array: np.ndarray, bits: int = 4) -> np.ndarray:
    """
    Extract the most significant bits from the array

    :param array:
    :param bits: number of msb
    :return: The most significant bits stored in numpy.ndarray, in string datatype
    """

    return array >> bits


def lsb(array: np.ndarray, bits: int = 4) -> np.ndarray:
    """
    Extract the least significant bits from the array

    :param array: The array from which the least significant bits are extracted.
    :param bits: Number of the least significant bits to be extracted.
    :return: The least significant bits stored in numpy.ndarray, in string datatype
    """

    return msb(array << bits)


def resize(info: np.ndarray, size=None, target: np.ndarray = None, interp=Image.BILINEAR) -> np.ndarray:
    """
    Resize the info image into the size specified. The image is firstly converted into Pillow.Image mode, then the
    builtin resize function is invoked.
    Be REALLY CAREFUL about the different convention of dimension in Pillow and NumPy

    :param info: The image to be resized.
    :param size: The size specified, in form of NumPy style (height, width), the priority of which is higher than target
    :param target: The target image.
    :param interp: The interpolation method, BILINEAR by default
    :return: The resized info image, in numpy.ndarray mode.
    """

    if size is None:
        size = target.shape[:2][::-1]
    else:
        size = size[::-1]

    return np.array(Image.fromarray(info).resize(size, interp))


def str_to_data(info: str) -> np.ndarray:
    """
    Convert string into binary ASCII data

    :param info: The string to be converted.
    :return: The converted binary ASCII data.
    """

    return np.array([[ord(char) & 1 << 7 - i > 0 for i in range(8)] for char in info], dtype=np.uint8)


def data_to_str(data: np.ndarray) -> str:
    """
    Convert binary ASCII data into string.

    :param data: The binary ASCII data.
    :return: The converted string.
    """

    _data = np.append(data, np.zeros(8 - (data.size - 1) % 8 - 1, dtype=np.uint8)).reshape(-1, 8)
    return ''.join([chr(char) for char in
                    np.sum(np.fromfunction(lambda x, y: 1 << 7 - y, (_data.size >> 3, 8),
                                           dtype=np.uint8) * _data, axis=1, dtype=np.uint8)])


def capacity(target: np.ndarray, bits: int = 4, hamming: bool = False, n: int = 2) -> int:
    """
    Calculate the capacity of an image for storing string info.

    :param target: The target image.
    :param bits: The number of least significant bits used for storing information.
    :param hamming: Hamming encoding is disabled by default.
    :param n: The dimension of Hamming block is specified by 2 ** n, or n << 1
    :return: The length of string that can be stored in the image.
    """

    return int(target.size * bits * (1 - ((n << 1) + 1) / (1 << (n << 1))) if hamming else 1 >> 3)


def str_tile(raw: str, length: int) -> str:
    """
    Tile the string to conform with the length.

    :param raw: The string to be tiled
    :param length: The target length.
    :return: The tiled string.
    """

    return raw * (length // len(raw)) + raw[:length % len(raw)]


def noise(img: np.ndarray, density: float) -> np.ndarray:
    """
    The input image must in dimension of (height, width, channel)

    :param img:
    :param density:
    :param mode:
    :return:
    """

    row, col, _ = img.shape
    noise_array = np.frompyfunc(lambda x: 255 if np.random.rand() < density else x, 1, 1)(np.zeros((row, col)))
    return np.clip(np.array([noise_array for i in range(3)]).transpose() + img, 0, 255).astype(np.uint8)


def similarity(raw: str, target: str, hamming=False) -> float:
    """
    Compare the similarity of the two strings. The raw string is tiled to conform with the length of the target string.
    If Hamming encoding is enabled, the protective characters are padded to the raw string first.

    :param raw: The raw string.
    :param target: The target string, for example, the string decoded from the image.
    :param hamming: If Hamming encoding is enabled, the protective bits are padded to the raw string.
    :return: The similarity of the two strings.
    """

    if hamming:
        raw = str_pad(raw)
    raw = str_tile(raw, len(target))

    return sum([raw[i] is target[i] for i in range(len(raw))]) / len(raw)
