import numpy as np
from PIL import Image
from matplotlib import pyplot as plt

import utils
import write
import read

with open('zen.txt', 'r') as f:
    zen = f.read()
lena = np.asarray(Image.open('../img/lena512color.tiff'))


def benchmark(bits: int = 2, hamming: bool = False, n: int = 2, density: float = 1 / 16) -> float:
    img = write.strwrite(zen, lena, bits=bits, hamming=hamming, n=n)
    img_n = utils.noise(img, density=density)

    string = read.strread(img_n, bits=bits, hamming=hamming, n=n)
    sim = utils.similarity(zen, string, hamming=hamming)
    return sim


# %% Hamming encoding enabled
print(benchmark(hamming=True))

# %% Hamming encoding disabled
print(benchmark(hamming=False))

# %% benchmark

# result = np.zeros((101, 4, 5))
# for i in range(101):  # noise density
#     d = 0 + 0.01 * i
#     print('Test for noise density {}'.format(d))
#     for bits in range(1, 5):  # bits = 1~4
#         result[i, bits - 1, 0] = benchmark(hamming=False, bits=bits)
#         for n in range(1, 5):  # hamming size = 1~4
#             result[i, bits - 1, n] = benchmark(bits=bits, hamming=True, n=n)
#
# with open('benchmark.npy', 'wb') as f:
#     np.save(f, result)

# %%
# result = np.zeros((21, 4, 5))
# for i in range(21):  # noise density
#     d = 0 + 0.05 * i
#     print('Test for noise density {}'.format(d))
#     for bits in range(1, 5):  # bits = 1~4
#         result[i, bits - 1, 0] = benchmark(hamming=False, bits=bits)
#         for n in range(1, 5):  # hamming size = 1~4
#             result[i, bits - 1, n] = benchmark(bits=bits, hamming=True, n=n)
#
# with open('benchmark.npy', 'wb') as f:
#     np.save(f, result)

acc = np.array([benchmark(bits=4, hamming=False, density=i * 0.01) for i in range(101)])
acc_hamming = np.array([benchmark(bits=4, hamming=True, n=2, density=i * 0.01) for i in range(101)])
boost = np.array(acc_hamming) - np.array(acc)
d = np.linspace(0, 1, num=101) * 100

plt.title('The accuracy of the decoded string with noise introduced\nbits=4, n=2')
plt.plot(d, acc_hamming, label='enabled')
plt.plot(d, acc, label='disabled')
plt.xlabel('The noise density (probability)')
plt.ylabel('The accuracy of the decoded string')

plt.legend()
plt.grid()
plt.show()

# %%
# acc_hamming_1 = [benchmark(bits=4, hamming=True, n=1, density=i * 0.01) for i in range(101)]

fig, ax1 = plt.subplots(figsize=(6.4 * 1.1, 4.8 * 1))
ax2 = ax1.twinx()
plt.title('The Accuracy of the Decoded String \nwith noise introduced, bits=4, n=2', fontsize=16)

l1 = ax1.plot(d[:40], (np.array(acc_hamming[:40])) * 100, label='enabled', linewidth=3)
l2 = ax1.plot(d[:40], np.array(acc[:40]) * 100, label='disabled', linewidth=3)
l3 = ax2.plot(d[:40], boost[:40] * 100, 'g:', label='boost', linewidth=3)

ax1.set_xlabel(r'Noise Density (Probability) / percent', fontsize=16)
ax1.set_ylabel(r'Accuracy / percent', fontsize=16)
ax2.set_ylabel(r'Accuracy Boost / percent', fontsize=16)

ls = [*l1, *l2, *l3]
labels = [l.get_label() for l in ls]
plt.legend(ls, labels, fontsize=16)
ax1.tick_params(labelsize=12)
ax2.tick_params(labelsize=12)
ax1.grid()
plt.savefig('acc.svg', transparent=True, dpi=600, format='svg')
plt.show()

plt.show()
