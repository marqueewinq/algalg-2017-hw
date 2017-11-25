import numpy as np

def fft(X):
    length = X.shape[0]
    if length == 1:
        return X

    assert length % 2 == 0, "length = {}".format(length)

    X_even = fft(X[::2])
    X_odd = fft(X[1::2])
    factor = np.exp(2j * np.pi * np.arange(length) / length)
    return np.concatenate([X_even + factor[:length // 2] * X_odd, 
                           X_even + factor[length // 2:] * X_odd])


if __name__ == '__main__':
    coeffs = np.array(list(map(float, input().strip().split())))
    result = fft(coeffs)
    print(' '.join(f'{x.real},{x.imag}' for x in result))
