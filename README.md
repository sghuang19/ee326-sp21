# Self-Correction in Image Steganography Project Report

This repo is intended for project of course Digital Image Processing at SUSTech, in 2021 Spring Semester. This project is focused on steganography in digital images.

[toc]

## Background

### Steganography

### Self-Correction

## Methodology

### Hamming Encoding and Decoding of Digital

---

## Implementation

### Image Steganography

In our work, we use LSB algorithm to implement digital image steganography.

#### Extracting the Bits

The basic functions for obtaining the most significant bits and the least significant bits are required. Therefore, we defined `utils.msb()` and `utils.lsb()`.

The most intuitive way for conducting such operation is first converting the intensity value to binary string expression, then do string cropping and concatenating.

- Function `bin()` converts a number into form of `0bxxxx`, therefore, the prefix `0b` should be removed.
- In which, `xxxx` is the binary expression of the number, and may not be exactly `8` digits for `uint8` type, therefore, zero-padding may be needed.

The code based on such method is shown below.

```python
def msb(array: np.ndarray, bits: int = 4) -> np.ndarray:
    row, col, ch = array.shape
    return np.array([
        bin(array[i, j, k])[2:].zfill(8)[:bits]
        for i in range(row)
        for j in range(col)
        for k in range(ch)]).reshape(row, col, ch)


def lsb(array: np.ndarray, bits: int = 4) -> np.ndarray:
    row, col, ch = array.shape
    return np.array([
        bin(array[i, j, k])[2:].zfill(8)[8 - bits:]
        for i in range(row)
        for j in range(col)
        for k in range(ch)]).reshape(row, col, ch)
```

However, `Python` provides a variety of flexible bit operation, and `NumPy` offers `frompyfunc()` function to conduct an operation over the total array. In such case, we may directly utilizing bit shifting operators.

For obtaining the most significant bits, simply do bit right shift.

```python
def msb(array: np.ndarray, bits: int = 4) -> np.ndarray:
    """
    Extract the most significant bits from the array
    :param array:
    :param bits: number of msb
    :return: The most significant bits stored in numpy.ndarray, in int datatype
    """
    return np.frompyfunc(lambda x: x >> bits, 1, 1)(array).astype(np.uint8)
```

For obtaining the least significant bits, we may first obtain its most significant bits, then left shift and subtract it from the array.

```python
def lsb(array: np.ndarray, bits: int = 4) -> np.ndarray:
    """
    Remove the least significant bits from the array
    :param array:
    :param bits: number of lsb
    :return: The least significant bits stored in numpy.ndarray, in int datatype
    """
    return array - np.frompyfunc(lambda x: x << bits, 1, 1)(msb(array, bits)).astype(np.uint8)
```

The performance is greatly improved, and the code is extraordinarily simplified.

>Note that, the returned `ufunc` always returns `PyObject` arrays, so datatype casting to `numpy.uint8` is required otherwise `Pillow` will not be able to save the array as file.

#### Resizing the Images

In our implementation, the information image encoded into the target image must have compatible dimensions. If not so, image resize is automatically taken.

```python
def resize(info: np.ndarray, size=None, target: np.ndarray = None, interp=Image.BILINEAR) -> np.ndarray:
    """
    Resize the info image into the size specified. The image is firstly converted into Pillow.Image mode, then the
    builtin resize function is invoked.
    Be REALLY CAREFUL about the different convention of dimension in Pillow and NumPy

    :param info: The image to be resized.
    :param size: The size specified, in form of NumPy style (height, width), the priority of which is higher than target
    :param target: The target image.
    :param interp: The interpolation method, BILINEAR by default
    :return: The resized info image, in numpy.ndarray mode.
    """

    if size is None:
        size = target.shape[:2][::-1]
    else:
        size = size[::-1]

    return np.array(Image.fromarray(info).resize(size, interp))
```

Be careful that, the dimension conventions in `NumPy` and `Pillow` are different. `NumPy` uses array-like row major convention, instead in `Pillow` image-like width-height-channel is adapted.

---

#### Image Encryption

#### Image Decryption

### Hamming Encoding and Decoding

#### Encode One Data Block

This function converts a series of data bits into single data block with Hamming redundant bits added, if the data bits provided does not correspond with a possible size of a $2^n$ by $2^n$ data block, the function returns false and gives warning.

First, define the function.

```python
def encode_block(data: np.ndarray) -> Union[np.ndarray, bool]:
    """
    Calculate the hamming redundant bits and encode which with the original data into a data block.

    :param data: The data bits in one block, the data mode of the array must be bool or 1s and 0s.
    :return The complete data block with data bits and hamming redundant bits encoded
    """
```

Basically, for an $2^n$ by $2^n$, $n\in N$ data block, the hamming redundant bits in which should be

$$
R = 2n + 1.
$$

In which, $n$ for row, $n$ for column and an extra bit at $(0, 0)$ position for global check. Accordingly, the number of data bits is

$$
D = \left(2^n\right)^2 - R = 2^{2n} - 2n - 1.
$$

Specifically, for $n=0$, obtains $D_0=0$ and $R_0=1$, namely no actual data can be stored. For $n=1$, $D_1=1$ and $R_1=3$, namely in a $2$ by $2$ data block, $3$ redundant bits are required and only $1$ data bit can be stored.

Therefore, we may check the size of the input data array.

```python
n = 0
while 1 << 2 * n - n << 1 - 1 < data.size:
    n += 1

if 1 << 2 * n - n << 1 - 1 != data.size:
    warn('Wrong number of data bits')
    return False
```

In row-major and 0-index notation, the positions of each parity bits in the data block in flattened pattern are

$$
\begin{cases}
    (0, 0) = 0\\
    (0, 2^i) = 2^i\\
    (2^i, 0) = 2^i \times 2^n = 2^{i + n}
\end{cases}\quad i \in \{0, 1, \dots, n - 1\}
$$

In other words, the common feature of the redundant bits is that, the binary indexes of which has only one or no zero digit. In a $2^n$ by $2^n$ data block, the indexes ranges from $0$ to $2^{2n}-1$, which can be specified with $2n$ digits of binary number. Hence, we may first insert the parity bits as $0$ to form the data block.

```python
parity = [1 << i for i in range(1 << n)]
block = [0]
i = 0
for j in range(2 << 2 * n):
    if j in parity:
        block += [0]
    else:
        block += data[i]
        i += 1
```

The parity group of each parity bit is specified by the `1` digit at certain position of its index. The most convenient way of conducting such judgment to determine whether one data bit in the block is in the parity or not is by bitwise AND operation.

Take the parity bit at index `2` in a `4` by `4` block for example, the binary index of the parity bit is `0010`, which has the single `1` at the `1` position. Therefore, to justify whether data bit at index `5` is in its parity group or not, first obtain is binary index `0101`. Then, we need to determine the digit at `1` position, and such comparison can be easily done by simply doing bitwise AND operation between `0010` and `0101`. The key point of such feasibility is listed below.

- The index of the parity bit is specifically chosen, so that it has only one `1` digit in its binary index.
- The indexes of the parity group is specifically chosen, so that the binary indexes of which all have `1` digit in the corresponding position.
- `0 and 1 = 0`, `0 and 0 = 0`, `1 and 0 = 0`, `1 and 1 = 1`

Therefore, when the data bit is not in the parity bit, the result of bitwise AND operation is zero.

#### Encode Several Data Blocks

#### Decode One Data Block

#### Decode Several Data Blocks

---

### Combining Self-Correction and Image Steganography

```python
for i in range(1, 4):
    for j, bit in enumerate(np.nditer(_target, order='F', op_flags, ['readwrite'])):
        bit += np.uint8(0)
        np.take(blocks, range(i << 2, i + 1 << 2), mode='wrap') << 3 - i
```

---

## How to Use This Package

## Useful Coding Details

### In
