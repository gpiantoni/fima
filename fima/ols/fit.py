from numpy import arange, c_, array, reshape, argmax
from pandas import DataFrame
from statsmodels.regression.linear_model import OLS
from statsmodels.api import add_constant
from functools import partial
from multiprocessing import Pool
from itertools import product

from .regressors import make_regressors
from ..utils import be_nice


def fit_one_channel(parameters, t, x, names):

    matrix_values, out_dim = compute_param_matrix(parameters, t)

    func = partial(get_rsquared, parameters=parameters, t=t, x=x, names=names)

    with Pool(initializer=be_nice) as p:
        results = p.map(func, matrix_values)

    return reshape(array(results), out_dim)


def get_max(parameters, t, x, names, MAT):

    val_mat = compute_param_matrix(parameters, t)[0]
    max_values = list(val_mat)[argmax(MAT)]

    regressors = make_regressors(parameters, names, t, max_values)
    results = fit_ols(regressors, x)

    out = {
        'tdiff': t[1] - t[0],
        'loc': max_values[0],
        'scale': max_values[1],
        'rsquared': results.rsquared,
        }
    out.update(dict(results.params))
    if parameters['ols']['window']['method'] == 'gamma':
        out['a'] = max_values[2]

    return out, results


def get_rsquared(params, parameters, t, x, names):
    regressors = make_regressors(parameters, names, t, params)
    results = fit_ols(regressors, x)
    return results.rsquared


def fit_ols(regressors, x):
    X = c_[list(regressors.values())].T
    X1 = DataFrame(X, columns=regressors.keys())
    X1 = add_constant(X1)

    model = OLS(x, X1, missing='drop')
    return model.fit()


def compute_param_matrix(parameters, t):
    """Calculate all the possible parameters for a set of search values

    Parameters
    ----------
    t : nd vector
        time vector from the data

    Returns
    -------
    generator
        each iter returns a tuple of 2 (gaussian) or 3 (gamma) values
    tuple of 2 or 3 int
        shape of the parameters used

    Notes
    -----
    For Gaussian and Gamma, it uses P['ols']['window']['loc'] for the time delay (
    negative is before onset and positive is after onset). Also P['ols']['window']['scale']
    is the width of the curve.
    For Gamma only, there is an additional parameter P['ols']['window']['a'] which
    encodes skewness (roughly speaking)
    """
    t_diff = t[1] - t[0]

    loc = parameters['ols']['window']['loc']
    if len(loc) == 2:
        loc.append(t_diff)

    scale = parameters['ols']['window']['scale']
    if len(scale) == 2:
        scale.append(t_diff)

    a_loc = arange(*loc)
    a_scale = arange(*scale)

    if parameters['ols']['window']['method'] == 'gaussian':
        matrix_values = product(a_loc, a_scale)
        out_dim = (len(a_loc), len(a_scale))

    elif parameters['ols']['window']['method'] == 'gamma':
        a_a = arange(*parameters['ols']['window']['a'])
        matrix_values = product(a_loc, a_scale, a_a)
        out_dim = (len(a_loc), len(a_scale), len(a_a))

    return matrix_values, out_dim
