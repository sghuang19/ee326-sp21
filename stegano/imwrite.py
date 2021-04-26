from PIL import Image
import numpy as np

lena512 = Image.read('../../img/lena512.tiff')


def imwrite(info, img=lena512, mode='hamming'):
    """
    Encrypt info into an image.
    """
    if isinstance(info, str):
        return img
