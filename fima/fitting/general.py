from numpy import r_, array, outer
from scipy.optimize import least_squares
from multiprocessing import Pool
from functools import partial

from .utils import rms, r2, make_struct, get_response
from .design_matrix import make_design_matrix


def get_trialdata(data):
    return [data(trial=0, chan=chan) for chan in data.chan[0]]


def fit_data(model, data, names, parallel=True):

    y = get_trialdata(data)

    if parallel:
        with Pool() as p:
            x = p.map(
                partial(fitting, model=model, names=names),
                y)
    else:
        x = [fitting(y0, model=model, names=names) for y0 in y]

    return array(x)[:, 0]


def fitting(y, model, names):
    seed = [x['seed'] for x in model['parameters'].values()]
    bound_low = [x['bounds'][0] for x in model['parameters'].values()]
    bound_high = [x['bounds'][1] for x in model['parameters'].values()]
    X = make_design_matrix(names, model['design_matrix'])

    response = get_response(model.get('response', None), y)

    result = least_squares(
        to_minimize,
        x0=seed,
        bounds=(bound_low, bound_high),
        args=[
            model['function'],
            X,
            response,
            y,
            ],
        max_nfev=1e5,
        )

    if y.ndim == 1:
        n_timepoints = None
    else:
        n_timepoints = y.shape[0]

    est = estimate(model, names, result.x, n_timepoints)
    if response is not None:
        est = outer(response, est)
    rsquared = r2(est, y)
    print(f'{rsquared:0.3f}', end=', ')

    return make_struct(r_[result.x, rsquared], list(model['parameters']) + ['rsquared', ])


def estimate(model, names, x0, n_points=None):

    X = make_design_matrix(names, model['design_matrix'])
    return model['function'](x0.view('<f8'), X, n_points)


def to_minimize(x0, fun, X, response, y, to_optimize='rms'):
    """Function to minimize

    Parameters
    ----------
    fun : function
        function to minimize
    X : (n_trials, n_betas) array
        design matrix
    response : (n_timepoints, ) array
        vector with value at each time point, for all the trials
    y : (n_trials, ) or (n_timepoints, n_trials, ) array
        raw data
    to_optimize : str
        'rms' or 'r2'

    Returns
    -------
    float
        value to minimize
    """
    if y.ndim == 1:
        n_timepoints = None
    else:
        n_timepoints = y.shape[0]
    est = fun(x0, X, n_timepoints)
    if response is not None:
        est = outer(response, est)

    if to_optimize == 'rms':
        return rms(est, y)

    elif to_optimize == 'r2':
        return 1 - r2(est, y)
