import numpy as np
from scipy.optimize import curve_fit


def fit(image):
    poly = ['0', '0']
    n = 11
    mesh = np.meshgrid(np.linspace(-1, 1, image.shape[0]), np.linspace(1, -1, image.shape[0]))
    xy = np.vstack(([m.ravel() for m in mesh]))
    image = image + image.sum()/(np.count_nonzero(image)) * (image == 0)
    fit_kof, fit_error = curve_fit(func, xy, image.ravel(), np.arange(2 * n))
    for i in [1, 0]:
        power = n
        for fit_kof_x in np.array_split(fit_kof, 2)[i]:
            power -= 1
            poly[i] += '+(' + str(fit_kof_x) + '*x**' + str(power) + ')'
    return poly, fit_kof


def func(mesh, *args):
    (x, y), (a, b) = mesh, np.array_split(args, 2)
    return np.poly1d(a)(x) * np.poly1d(b)(y)
