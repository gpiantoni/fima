from scipy.optimize import least_squares

from .utils import rms, r2, make_struct
from .design_matrix import make_design_matrix


def fitting(model, names, y):
    print(model['doc'])
    seed = [x[0] for x in model['parameters'].values()]
    bound_low = [x[1][0] for x in model['parameters'].values()]
    bound_high = [x[1][1] for x in model['parameters'].values()]
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
    print(result)
    return make_struct(result.x, model['parameters'])


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
