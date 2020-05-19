from numpy import arange, outer
from scipy.stats import norm as normdistr
from functools import partial

from .trialbased import (
    MODELS,
    linear_gaussian_per_finger,
    linear_separate_gaussians_per_finger,
    )


def add_gauss(seed, X, n_points, fun):
    v = fun(seed[:-2], X)
    t = arange(n_points)
    response = normdistr.pdf(t, loc=seed[-2], scale=seed[-1])
    est = outer(response, v)
    return est


MODELS['linear_gaussian_per_finger_with_gauss'] = {
    'type': 'time-based',
    'doc': MODELS['linear_gaussian_per_finger']['doc'] + ' multiplied by a Gaussian',
    'function': partial(add_gauss, fun=linear_gaussian_per_finger),
    'design_matrix': MODELS['linear_gaussian_per_finger']['design_matrix'],
    'parameters': {
        **MODELS['linear_gaussian_per_finger']['parameters'],
        'delay': {
            'seed': 20,
            'bounds': (-5, 80),  # this depends on the number of data points
            'to_plot': True,
            },
        'spread': {
            'seed': 10,
            'bounds': (0.1, 40),  # this depends on the number of data points
            'to_plot': False,
            },
        },
    }

MODELS['linear_separate_gaussians_per_finger_with_gauss'] = {
    'type': 'time-based',
    'doc': MODELS['linear_separate_gaussians_per_finger']['doc'] + ' multiplied by a Gaussian',
    'function': partial(add_gauss, fun=linear_separate_gaussians_per_finger),
    'design_matrix': MODELS['linear_separate_gaussians_per_finger']['design_matrix'],
    'parameters': {
        **MODELS['linear_separate_gaussians_per_finger']['parameters'],
        'delay': {
            'seed': 20,
            'bounds': (-5, 80),  # this depends on the number of data points
            'to_plot': True,
            },
        'spread': {
            'seed': 10,
            'bounds': (0.1, 40),  # this depends on the number of data points
            'to_plot': False,
            },
        },
    }
