import sys

sys.path.append('../stegano')

import write
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt

sherlock = np.asarray(Image.open('../img/sherlock.jpg'))
sevilla = np.asarray(Image.open('../img/sevilla.jpg'))
strawberries = np.asarray(Image.open('../img/strawberries.jpg'))

sevilla_with_sherlock = write.imgwrite(info=sherlock, bits=4)
Image.fromarray(sevilla_with_sherlock).save('../img/sevilla_with_sherlock_4.jpg')
plt.imshow(sevilla_with_sherlock)
plt.show()

sevilla_with_strawberries = write.imgwrite(info=strawberries, bits=4)
Image.fromarray(sevilla_with_strawberries).save('../img/sevilla_with_strawberries_4.jpg')
plt.imshow(sevilla_with_strawberries)
plt.show()
