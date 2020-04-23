from numpy import Inf, arange, r_
from scipy.stats import norm

from .utils import make_2d


def linear_gaussian_per_finger(x0, X):
    A, loc, scale = x0
    pdf = norm.pdf(arange(5), loc=loc, scale=scale)

    return A * (make_2d(X) * pdf).sum(axis=1)


def linear_gaussian_per_finger_open_v_close(x0, X):
    A, loc, scale, openclose = x0
    pdf = norm.pdf(arange(5), loc=loc, scale=scale)
    pdf = r_[pdf * openclose, pdf * (1 - openclose)]

    return A * (make_2d(X) * pdf).sum(axis=1)


def linear_separate_gaussians_per_finger(x0, X):
    open_A, open_loc, open_scale, close_A, close_loc, close_scale = x0
    pdf = norm.pdf([0, 1, 2, 3, 4], loc=open_loc, scale=open_scale)
    open_y = open_A * (make_2d(X)[:, :5] * pdf).sum(axis=1)
    pdf = norm.pdf([0, 1, 2, 3, 4], loc=close_loc, scale=close_scale)
    close_y = close_A * (make_2d(X)[:, 5:] * pdf).sum(axis=1)
    return open_y + close_y


MODELS = {
    'linear_gaussian_per_finger': {
        'doc': 'One Gaussian across fingers, no distinction between flexion and extension',
        'function': linear_gaussian_per_finger,
        'design_matrix': 'fingers',
        'parameters': {
            'amplitude': (1, (-Inf, Inf)),
            'center_finger': (2, (-1, 5)),
            'std_finger': (1, (0.01, 10)),
            }
        },
    'linear_gaussian_per_finger_open_v_close': {
        'doc': 'The same Gaussian across fingers, with different weights for flexion and extension',
        'function': linear_gaussian_per_finger_open_v_close,
        'design_matrix': 'cues',
        'parameters': {
            'amplitude': (1, (-Inf, Inf)),
            'center_finger': (2, (-1, 5)),
            'std_finger': (1, (0.01, 10)),
            'open_v_close': (0.5, (0, 1)),
            }
        },
    'linear_separate_gaussians_per_finger': {
        'doc': 'Two independent Gaussians across fingers, one for flexion and one for extension',
        'function': linear_separate_gaussians_per_finger,
        'design_matrix': 'cues',
        'parameters': {
            'open_amplitude': (1, (-Inf, Inf)),
            'open_center': (2, (-1, 5)),
            'open_std': (1, (0.01, 10)),
            'close_amplitude': (1, (-Inf, Inf)),
            'close_center': (2, (-1, 5)),
            'close_std': (1, (0.01, 10)),
            }
        },
    }
