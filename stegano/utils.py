from PIL import Image
import numpy as np


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
    :param array:
    :param bits: number of lsb
    :return: The least significant bits stored in numpy.ndarray, in string datatype
    """
    return msb(array << bits)


def resize(info: np.ndarray, size=None, target: np.ndarray = None, interp=Image.BILINEAR) -> np.ndarray:
    """
    Resize the info image into the size specified. The image is firstly converted into Pillow.Image type, then the
    builtin resize function is invoked.
    Be REALLY CAREFUL about the different convention of dimension in Pillow and NumPy

    :param info: The image to be resized.
    :param size: The size specified, in form of NumPy style (height, width), the priority of which is higher than target
    :param target: The target image.
    :param interp: The interpolation method, BILINEAR by default
    :return: The resized info image, in numpy.ndarray type.
    """

    if size is None:
        size = target.shape[:2][::-1]
    else:
        size = size[::-1]

    return np.array(Image.fromarray(info).resize(size, interp))


def str_to_data(info: str) -> np.ndarray:
    return np.array([[ord(char) & 1 << 7 - i > 0 for i in range(8)] for char in info], dtype=np.uint8)


def data_to_str(data: np.ndarray) -> str:
    _data = np.append(data, np.zeros(data.size % 8, dtype=np.uint8)).reshape(-1, 8)

    return ''.join([chr(char) for char in
                    np.sum(np.fromfunction(lambda x, y: 1 << 7 - y, (data.size >> 3, 1 << 3),
                                           dtype=np.uint8) * _data, axis=1, dtype=np.uint8)])
