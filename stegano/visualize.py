import numpy as np
from matplotlib import pyplot as plt

benchmark = np.load('benchmark.npy')

# %% n=2, bits=4
acc = benchmark[:, 3, 0]
acc_hamming = benchmark[:, 3, 2]
d = np.linspace(0, 1, num=101)

plt.figure(figsize=(6.4, 9.6))
plt.title('The accuracy of the decoded string with noise introduced\nbits=4, n=2')

plt.plot(d, acc_hamming, label='enabled')
plt.plot(d, acc, label='disabled')
plt.xlabel('The noise density (probability)')
plt.ylabel('The accuracy of the decoded string')

plt.legend()
plt.grid()
plt.show()

# %% n=2, bits=4
import numpy as np


plt.scatter(benchmark, cmap='Blues')  #绘制散点图
# ax1.plot3D(x,y,z,'gray')    #绘制空间曲线
plt.show()
