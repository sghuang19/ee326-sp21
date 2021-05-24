from matplotlib import pyplot as plt

from write import strwrite
from read import strread

with open("../stegano/zen.txt", 'r') as f:
    zen = f.read()

print(zen)
print('==========')
# zen = 'a'
img1 = strwrite(zen, bits=4, hamming=True)
# plt.imshow(img1)
# plt.show()

str1 = strread(img1, bits=4, hamming=True)
# print('decoded info:\n', string)
str2 = strread(strwrite('hello world!'))
