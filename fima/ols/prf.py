"""Compute PRF on the parameter estimate, not the raw data
"""
from scipy.stats import norm
from scipy.optimize import least_squares
from numpy import sqrt, Inf, arange, array, corrcoef
from json import load as json_load
from json import dump

from ..parameters import FINGERS_EXTENSION, FINGERS_FLEXION


def add_prf_estimates(json_file):
    with json_file.open() as f:
        j = json_load(f)

    compute_prf_from_parameters(j, FINGERS_EXTENSION)
    compute_prf_from_parameters(j, FINGERS_FLEXION)

    y_ext = [j[k] for k in FINGERS_EXTENSION]
    y_flex = [j[k] for k in FINGERS_FLEXION]
    j['params corr'] = corrcoef(y_ext, y_flex)[0, 1]
    j['params diff'] = (array(y_ext) - array(y_flex)).mean()

    with json_file.open('w') as f:
        dump(j, f, indent=2)


def compute_prf_from_parameters(j, finger_group):
    movement_type = finger_group[0].split()[1]
    data = [j[k] for k in finger_group]

    result = least_squares(
        gaussian,
        x0=[1, 2, 0.5],
        bounds=(
            [-Inf, -1, 0.01],
            [Inf, 5, 10]),
        args=[data, ],
        max_nfev=1e4,
        x_scale=[10, 1, 1],
        )

    j[movement_type + ' A'] = result.x[0]
    j[movement_type + ' loc'] = result.x[1]
    j[movement_type + ' scale'] = result.x[2]
    j[movement_type + ' rms'] = result.fun[0]


def gaussian(x0, y):
    A, loc, scale = x0
    y1 = A * norm.pdf(arange(5), loc=loc, scale=scale)
    return sqrt(((y - y1) ** 2).mean())
