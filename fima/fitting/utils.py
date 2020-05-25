from numpy import zeros
from scipy.stats import pearsonr
from ..fingers.max_activity import FINGERS, create_bool
from ..spectrum.compute import get_chantime
from numpy import moveaxis, array


EVENTS = []
for action in ('close', 'open'):
    for f in FINGERS:
        EVENTS.append(f'{f} {action}')


def make_2d(x):
    return x.view('<f8').reshape(x.shape[0], -1)


def rms(est, y):
    return ((est.ravel() - y.ravel()) ** 2).mean() ** .5


def r2(est, y):
    return pearsonr(est.ravel(), y.ravel())[0] ** 2


def pvalue(est, y):
    return pearsonr(est.ravel(), y.ravel())[1]


def make_struct(x, dtype_names):
    """There should be a numpy function to do this, but I cannot find it
    """
    DTYPES = []
    for col_name in dtype_names:
        DTYPES.append((col_name, '<f8'))
    out = zeros(1, dtype=DTYPES)
    for i, col_name in enumerate(dtype_names):
        out[col_name] = x[i]

    return out


def get_response(method, y):

    if method is None:
        response = None
    elif method == 'mean':
        response = y.mean(axis=1)

    return response


def group_per_condition(data, names):
    dat = []
    for ev in EVENTS:
        i = create_bool(names, ev)
        dat.append(data.data[0][..., i].mean(axis=-1))

    data.data[0] = moveaxis(array(dat), 0, -1)
    data.axis.pop('trial_axis');
    data.axis['event'] = array((1, ), dtype='O')
    data.axis['event'][0] = array(EVENTS)

    return data, array(EVENTS)
