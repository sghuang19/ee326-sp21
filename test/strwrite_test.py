import numpy as np
from matplotlib import pyplot as plt
from write import strwrite

info1 = 'a'
img1 = strwrite(info1)
img2 = strwrite(info1, hamming=True)
plt.imshow(img1)
plt.show()
plt.imshow(img2)
plt.show()
