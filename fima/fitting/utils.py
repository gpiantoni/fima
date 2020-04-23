from scipy.stats import pearsonr


def make_2d(x):
    return x.view('<f8').reshape(x.shape[0], -1)


def rms(est, y):
    return ((est - y) ** 2).mean() ** .5


def r2(est, y):
    return pearsonr(est, y)[0] ** 2


def pvalue(est, y):
    return pearsonr(est, y)[1]
