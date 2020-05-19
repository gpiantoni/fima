from numpy import Inf, arange, r_
from scipy.stats import norm

from .utils import make_2d


def linear_gaussian_per_finger(x0, X, n_points=None):
    A, loc, scale = x0
    pdf = norm.pdf(arange(5), loc=loc, scale=scale)

    return A * (make_2d(X) * pdf).sum(axis=1)


def linear_gaussian_per_finger_open_v_close(x0, X, n_points=None):
    A, loc, scale, openclose = x0
    pdf = norm.pdf(arange(5), loc=loc, scale=scale)
    pdf = r_[pdf * openclose, pdf * (1 - openclose)]

    return A * (make_2d(X) * pdf).sum(axis=1)


def linear_separate_gaussians_per_finger(x0, X, n_points=None):
    open_A, open_loc, open_scale, close_A, close_loc, close_scale = x0
    pdf = norm.pdf([0, 1, 2, 3, 4], loc=open_loc, scale=open_scale)
    open_y = open_A * (make_2d(X)[:, :5] * pdf).sum(axis=1)
    pdf = norm.pdf([0, 1, 2, 3, 4], loc=close_loc, scale=close_scale)
    close_y = close_A * (make_2d(X)[:, 5:] * pdf).sum(axis=1)
    return open_y + close_y


MODELS = {
    'linear_gaussian_per_finger': {
        'type': 'trial-based',
        'doc': 'One Gaussian across fingers, no distinction between flexion and extension',
        'function': linear_gaussian_per_finger,
        'design_matrix': 'fingers',
        'parameters': {
            'amplitude': {
                'seed': 1,
                'bounds': (-Inf, Inf),
                'to_plot': False,
                },
            'center_finger': {
                'seed': 2,
                'bounds': (-1, 5),
                'to_plot': True,
                },
            'std_finger': {
                'seed': 1,
                'bounds': (0.01, 10),
                'to_plot': False,
                },
            },
        },
    'linear_gaussian_per_finger_open_v_close': {
        'type': 'trial-based',
        'doc': 'The same Gaussian across fingers, with different weights for flexion and extension',
        'function': linear_gaussian_per_finger_open_v_close,
        'design_matrix': 'cues',
        'parameters': {
            'amplitude': {
                'seed': 1,
                'bounds': (-Inf, Inf),
                'to_plot': False,
                },
            'center_finger': {
                'seed': 2,
                'bounds': (-1, 5),
                'to_plot': True,
                },
            'std_finger': {
                'seed': 1,
                'bounds': (0.01, 10),
                'to_plot': False,
                },
            'open_v_close': {
                'seed': 0.5,
                'bounds': (0, 1),
                'to_plot': True,
                },
            },
        },
    'linear_separate_gaussians_per_finger': {
        'type': 'trial-based',
        'doc': 'Two independent Gaussians across fingers, one for flexion and one for extension',
        'function': linear_separate_gaussians_per_finger,
        'design_matrix': 'cues',
        'parameters': {
            'open_amplitude': {
                'seed': 1,
                'bounds': (-Inf, Inf),
                'to_plot': False,
                },
            'open_center': {
                'seed': 2,
                'bounds': (-1, 5),
                'to_plot': True,
                },
            'open_std': {
                'seed': 1,
                'bounds': (0.01, 10),
                'to_plot': False,
                },
            'close_amplitude': {
                'seed': 1,
                'bounds': (-Inf, Inf),
                'to_plot': False,
                },
            'close_center': {
                'seed': 2,
                'bounds': (-1, 5),
                'to_plot': True,
                },
            'close_std': {
                'seed': 1,
                'bounds': (0.01, 10),
                'to_plot': False,
                },
            },
        },
    }
