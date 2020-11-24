from numpy import arange, c_, array, reshape, argmax, unravel_index
from pandas import DataFrame
from statsmodels.regression.linear_model import OLS
from statsmodels.api import add_constant
from functools import partial
from multiprocessing import Pool
from itertools import product

from .regressors import model_brain_response, make_regressors_from_indices, find_movement_indices
from ..utils import be_nice

DELAYS = arange(-20, 50, 2)
SIGMAS = arange(1, 50)


def fit_one_channel(x, indices):

    func = partial(get_rsquared, x=x, indices=indices)

    with Pool(initializer=be_nice) as p:
        results = p.starmap(func, product(SIGMAS, DELAYS))

    return reshape(array(results), (SIGMAS.shape[0], DELAYS.shape[0]))


def get_max(MAT, x, indices):
    i_sigma, i_delay = unravel_index(argmax(MAT), MAT.shape)

    canonical_resp = model_brain_response(coef=SIGMAS[i_sigma])
    regressors = make_regressors_from_indices(indices, x.shape, canonical_resp, delay=DELAYS[i_delay])
    results = fit_ols(regressors, x)

    out = {
        'sigma': SIGMAS[i_sigma],
        'delay': DELAYS[i_delay],
        'rsquared': results.rsquared,
        }
    return out, results


def get_rsquared(sigma, delay, x, indices):
    canonical_resp = model_brain_response(coef=sigma)
    regressors = make_regressors_from_indices(indices, x.shape, canonical_resp, delay=delay)
    results = fit_ols(regressors, x)
    return results.rsquared


def fit_ols(regressors, x):
    X = c_[list(regressors.values())].T
    X1 = DataFrame(X, columns=regressors.keys())
    X1 = add_constant(X1)

    model = OLS(x, X1, missing='drop')
    return model.fit()
