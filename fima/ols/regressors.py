from numpy import unique, where, abs, argmin
from scipy.signal import unit_impulse, convolve
from scipy.signal.windows import gaussian


def make_regressors_from_indices(indices, shape, canonical_resp, delay=0):

    regressors = {}
    for k, v in indices.items():
        r = unit_impulse(shape, [x + delay for x in v])
        regressors[k] = convolve(r, canonical_resp, mode='same')

    return regressors


def find_movement_indices(mov, t):
    reg_idx = {}

    for event in unique(mov['trial_type']):

        indices = []
        for idx in where(mov['trial_type'] == event)[0]:
            i = argmin(abs(t - mov['onset'][idx]))
            indices.append(i)

        reg_idx[event] = indices

    return reg_idx


def model_brain_response(shape='gaussian', coef=1):
    N_POINTS = 102 * 3  # roughly one second

    if shape == 'gaussian':
        return gaussian(N_POINTS, coef)
