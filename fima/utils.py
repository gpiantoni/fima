from bidso import file_Core
from numpy import argmax, unravel_index

INTERVAL = 0.3


def make_name(filename, event_type, ext='.html'):
    f = file_Core(filename)
    if f.acquisition is None:
        acq = ''
    else:
        acq = '_{f.acquisition}'
    return f'{f.subject}_run-{f.run}{acq}_{event_type}{ext}'


def find_max_point(tf_cht):
    """Take the channel with the highest value and the interval containing that
    point
    """
    ind = unravel_index(argmax(tf_cht.data[0], axis=None), tf_cht.data[0].shape)
    max_chan = tf_cht.chan[0][ind[0]]
    max_timeinterval = (
        tf_cht.time[0][ind[1]] - INTERVAL / 2,
        tf_cht.time[0][ind[1]] + INTERVAL / 2,
        )

    return max_chan, max_timeinterval
