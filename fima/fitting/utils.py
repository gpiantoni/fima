from numpy import zeros
from scipy.stats import pearsonr


def make_2d(x):
    return x.view('<f8').reshape(x.shape[0], -1)


def rms(est, y):
    return ((est - y) ** 2).mean() ** .5


def r2(est, y):
    return pearsonr(est, y)[0] ** 2


def pvalue(est, y):
    return pearsonr(est, y)[1]


def make_struct(x, dtype_names):
    """There should be a numpy function to do this, but I cannot find it
    """
    DTYPES = []
    for col_name in dtype_names:
        DTYPES.append((col_name, '<f8'))
    out = zeros(1, dtype=DTYPES)
    for i, col_name in enumerate(dtype_names):
        out[col_name] = x[i]

    return out
