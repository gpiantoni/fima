from bidso import file_Core
from numpy import argmax, unravel_index
from ast import literal_eval
from numpy import arange, array, clip, where
from plotly.colors import sequential, cyclical, diverging

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


def get_color_for_val(value, colorscale, vmin=0, vmax=1):
    """Return RGB value for plotly
    """
    if colorscale in dir(sequential):
        color_values = getattr(sequential, colorscale)
    elif colorscale in dir(cyclical):
        color_values = getattr(cyclical, colorscale)
    elif colorscale in dir(diverging):
        color_values = getattr(diverging, colorscale)
    else:
        raise ValueError(f'Could not find colorscale "{colorscale}"')

    scale = arange(len(color_values)) / (len(color_values) - 1)
    colors = array([literal_eval(color[3:]) for color in color_values]) / 255

    value = clip(value, vmin, vmax)
    v = (value - vmin) / (vmax - vmin)

    v_max = where(v <= scale)[0][0]
    v_min = where(v >= scale)[0][-1]
    if v_min == v_max:
        vv = v_min
    else:
        vv = (v - scale[v_min]) / (scale[v_max] - scale[v_min])
    val_color = colors[v_min, :] + vv * (colors[v_max, :] - colors[v_min, :])

    val_color_0255 = (255 * val_color + 0.5).astype(int)
    return f'rgb{str(tuple(val_color_0255))}'
