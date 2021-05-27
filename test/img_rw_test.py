from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
import sys

sys.path.append('../stegano')
import write
import read

sherlock = np.asarray(Image.open('../img/sherlock.jpg'))
sevilla = np.asarray(Image.open('../img/sevilla.jpg'))
strawberries = np.asarray(Image.open('../img/strawberries.jpg'))

sevilla_with_sherlock = write.imgwrite(info=sherlock, bits=4)
Image.fromarray(sevilla_with_sherlock).save('../img/sevilla_with_sherlock_4.jpg')
plt.imshow(sevilla_with_sherlock)
plt.savefig('sevilla_with_sherlock.svg', format='svg', transparent=True)
plt.show()

sherlock_read = read.imgread(sevilla_with_sherlock, bits=4)
plt.imshow(sherlock_read)
plt.savefig('sherlock_read.svg', format='svg', transparent=True)
plt.show()
