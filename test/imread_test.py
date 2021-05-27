from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
import sys

sys.path.append('../stegano')
import read

sevilla_with_sherlock = np.asarray(Image.open('../fig/sevilla_with_sherlock_4.jpg'))
sherlock_read = read.imgread(sevilla_with_sherlock, bits=4)
plt.imshow(sherlock_read)
plt.show()

sevilla_with_sherlock = np.asarray(Image.open('../fig/sevilla_with_strawberries_4.jpg'))
strawberries_read = read.imgread(sevilla_with_sherlock, bits=4)
plt.imshow(strawberries_read)
plt.show()
