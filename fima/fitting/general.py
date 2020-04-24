from scipy.optimize import least_squares
from numpy import r_, array
from multiprocessing import Pool
from functools import partial
from wonambi.trans import math

from .utils import rms, r2, make_struct
from .design_matrix import make_design_matrix


def get_trialdata(data):
    data = math(data, operator_name='mean', axis='time')
    return [data(trial=0, chan=chan) for chan in data.chan[0]]


def fit_data(model, data, names):

    y = get_trialdata(data)

    with Pool() as p:
        x = p.map(
            partial(fitting, model=model, names=names),
            y)

    return array(x)[:, 0]


def fitting(y, model, names):
    seed = [x['seed'] for x in model['parameters'].values()]
    bound_low = [x['bounds'][0] for x in model['parameters'].values()]
    bound_high = [x['bounds'][1] for x in model['parameters'].values()]
    X = make_design_matrix(names, model['design_matrix'])

    result = least_squares(
        to_minimize,
        x0=seed,
        bounds=(bound_low, bound_high),
        args=[
            model['function'],
            X,
            y,
            ],
        max_nfev=1e5,
        )

    est = estimate(model, names, result.x)
    rsquared = r2(est, y)

    return make_struct(r_[result.x, rsquared], list(model['parameters']) + ['rsquared', ])


def estimate(model, names, x0):

    X = make_design_matrix(names, model['design_matrix'])
    return model['function'](x0.view('<f8'), X)


def to_minimize(x0, fun, X, y, to_optimize='rms'):
    """Function to minimize

    Parameters
    ----------
    fun : function
        function to minimize
    X : (n_datapoints, n_betas) array
        design matrix
    y : (n_datapoints, ) array
        raw data
    to_optimize : str
        'rms' or 'r2'

    Returns
    -------
    float
        value to minimize
    """
    est = fun(x0, X)

    if to_optimize == 'rms':
        return rms(est, y)

    elif to_optimize == 'r2':
        return 1 - r2(est, y)
