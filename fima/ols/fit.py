from numpy import arange, c_, array, reshape, argmax, unravel_index
from pandas import DataFrame
from statsmodels.regression.linear_model import OLS
from statsmodels.api import add_constant
from functools import partial
from multiprocessing import Pool
from itertools import product

from ..parameters import P
from .regressors import make_regressors_from_indices
from ..utils import be_nice


def fit_one_channel(t, x, indices):
    t_diff = t[1] - t[0]

    func = partial(get_rsquared, t=t, x=x, indices=indices)

    loc = P['ols']['window']['loc']
    if len(loc) == 2:
        loc.append(t_diff)

    scale = P['ols']['window']['scale']
    if len(scale) == 2:
        scale.append(t_diff)

    a_loc = arange(*loc)
    a_scale = arange(*scale)

    if P['ols']['window']['method'] == 'gaussian':
        matrix_values = product(a_loc, a_scale)
        out_dim = (len(a_loc), len(a_scale))

    elif P['ols']['window']['method'] == 'gamma':
        a_a = arange(*P['ols']['window']['a'])
        matrix_values = product(a_loc, a_scale, a_a)
        out_dim = (len(a_loc), len(a_scale), len(a_a))

    with Pool(initializer=be_nice) as p:
        results = p.map(func, matrix_values)

    return reshape(array(results), out_dim)


def get_max(MAT, x, indices):
    i_sigma, i_delay = unravel_index(argmax(MAT), MAT.shape)

    regressors = make_regressors_from_indices(indices, x.shape, canonical_resp, delay=DELAYS[i_delay])
    results = fit_ols(regressors, x)

    out = {
        'sigma': SIGMAS[i_sigma],
        'delay': DELAYS[i_delay],
        'rsquared': results.rsquared,
        }
    return out, results


def get_rsquared(params, t, x, indices):
    regressors = make_regressors_from_indices(indices, t, params)
    results = fit_ols(regressors, x)
    return results.rsquared


def fit_ols(regressors, x):
    X = c_[list(regressors.values())].T
    X1 = DataFrame(X, columns=regressors.keys())
    X1 = add_constant(X1)

    model = OLS(x, X1, missing='drop')
    return model.fit()
