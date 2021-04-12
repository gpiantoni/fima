"""Compute PRF on the parameter estimate, not the raw data
"""
from scipy.stats import norm
from scipy.optimize import least_squares
from numpy import arange, array, corrcoef, argmax
from json import load as json_load
from json import dump

from ..parameters import FINGERS_EXTENSION, FINGERS_FLEXION, FINGERS_OPEN, FINGERS_CLOSED


def add_prf_estimates(json_file):
    with json_file.open() as f:
        j = json_load(f)

    if 'index open' in j:
        columns_open = FINGERS_OPEN
        columns_closed = FINGERS_CLOSED
    else:
        columns_open = FINGERS_EXTENSION
        columns_closed = FINGERS_FLEXION

    compute_prf_from_parameters(j, columns_open)
    compute_prf_from_parameters(j, columns_closed)

    y_ext = [j[k] for k in columns_open]
    y_flex = [j[k] for k in columns_closed]
    j['params corr'] = corrcoef(y_ext, y_flex)[0, 1]
    j['params diff'] = (array(y_ext) - array(y_flex)).mean()

    with json_file.open('w') as f:
        dump(j, f, indent=2)


def compute_prf_from_parameters(j, finger_group):
    movement_type = finger_group[0].split()[1]
    data = [j[k] for k in finger_group]

    j[movement_type + ' mode'] = int(argmax(data))

    result = least_squares(
        gaussian,
        x0=[2, 0.5],
        bounds=(
            [-1, 0.01],
            [5, 10]),
        args=[data, ],
        max_nfev=1e4,
        )

    j[movement_type + ' loc'] = result.x[0]
    j[movement_type + ' scale'] = result.x[1]
    # from 1 - cc to rsquared
    j[movement_type + ' rsquared'] = (1 - result.fun[0]) ** 2


def gaussian(x0, y):
    loc, scale = x0
    y1 = norm.pdf(arange(5), loc=loc, scale=scale)
    return 1 - corrcoef(y, y1)[0, 1]
