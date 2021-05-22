import write
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt

sherlock = np.asarray(Image.open('../img/sherlock.jpg'))
sevilla = np.asarray(Image.open('../img/sevilla.jpg'))

print("The size of sherlock is", sherlock.shape[:2])
print("The size of sevilla is", sevilla.shape[:2])

print('=== test applying size of target ===')
sherlock_r_1 = write.resize(sherlock, target=sevilla)
print("The size of resized sherlock is", sherlock_r_1.shape[:2])

plt.imshow(sherlock_r_1)
plt.show()

print('=== test specifying size in NumPy style (h, w) ===')
size = (800, 400)
print('Specified size is', size)
sherlock_r_2 = write.resize(sherlock, size=size)
print("The size of resized sherlock is", sherlock_r_2.shape[:2])

plt.imshow(sherlock_r_2)
plt.show()
