from numpy import unique, where, abs, argmin, arange
from scipy.signal import unit_impulse, convolve
from scipy.stats import norm as normal
from scipy.stats import gamma


def find_movement_indices(mov, t):
    reg_idx = {}

    for event in unique(mov['trial_type']):

        indices = []
        for idx in where(mov['trial_type'] == event)[0]:
            i = argmin(abs(t - mov['onset'][idx]))
            indices.append(i)

        reg_idx[event] = indices

    return reg_idx


def make_regressors_from_indices(parameters, indices, t, params):

    canonical_resp = compute_canonical(parameters, t, params)[1]
    regressors = {}
    for k, v in indices.items():
        r = unit_impulse(t.shape, v)
        regressors[k] = convolve(r, canonical_resp, mode='same')

    return regressors


def compute_canonical(parameters, t, params):

    t_diff = t[1] - t[0]
    t_window = arange(-3, 3, t_diff)
    if parameters['ols']['window']['method'] == 'gaussian':
        canonical_resp = normal.pdf(t_window, loc=params[0], scale=params[1])
    else:
        canonical_resp = gamma.pdf(t_window, a=params[2], loc=params[0], scale=params[1])

    # TODO add this line: canonical_resp /= canonical_resp.max()

    return t_window, canonical_resp
