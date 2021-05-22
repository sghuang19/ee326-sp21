from matplotlib import pyplot as plt

from write import strwrite
from read import strread

with open("../stegano/zen.txt", 'r') as f:
    zen = f.read()

print(zen)
print('==========')

img = strwrite(zen)
plt.imshow(img)
plt.show()

string = strread(img)
print('decoded info:\n', string)
