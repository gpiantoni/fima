from numpy import Inf
from scipy.stats import norm

from .utils import make_2d


def linear_gaussian_per_finger(x0, X):
    A, loc, scale = x0
    pdf = norm.pdf([0, 1, 2, 3, 4], loc=loc, scale=scale)

    return A * (make_2d(X) * pdf).sum(axis=1)


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
    }
