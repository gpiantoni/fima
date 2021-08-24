"""Compute PRF on the parameter estimate, not the raw data
"""
from scipy.optimize import least_squares
from scipy.stats import linregress
from numpy import arange, array, corrcoef, argmax, exp, Inf
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
        penalty,
        x0=[0, 1, 2, 0.5],
        bounds=(
            [-Inf, 0, -1, 0.01],
            [Inf, Inf, 5, 5],
        ),
        args=[data, ],
        method='trf',
        loss='soft_l1',
        )

    j[movement_type + ' const'] = result.x[0]
    j[movement_type + ' ampl'] = result.x[1]
    j[movement_type + ' loc'] = result.x[2]
    j[movement_type + ' scale'] = result.x[3]
    j[movement_type + ' rsquared'] = linregress(data, gaussian(result.x))[2] ** 2


def penalty(x0, y):
    return gaussian(x0) - y


def gaussian(x0):
    const, ampl, loc, scale = x0
    x = arange(5)
    # y1 = norm.pdf(x, loc=loc, scale=scale)
    y1 = exp(-(x - loc) ** 2. / (2 * scale ** 2.))
    return y1 * ampl + const
