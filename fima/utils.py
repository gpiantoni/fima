"""Miscellaneous functions that might be useful across modules"""
from bidso import file_Core
from numpy import argmax, unravel_index, zeros, std, sqrt, median, moveaxis
from ast import literal_eval
from numpy import arange, array, clip, where
from plotly.colors import sequential, cyclical, diverging
from scipy.stats import ttest_1samp
from os import nice


def make_name(filename, event_type, ext='.html'):
    """Create name based on the data file name

    Parameters
    ----------
    filename : str
        filename of the dataset of interest
    event_type : str
        event type used to identify the trials (one of 'cues', 'open', 'close',
        'movements', 'extension', 'flexion')
    ext : str
        extension of the file

    Returns
    -------
    str
        file name specific to this filename and event type
    """
    f = file_Core(filename)
    if f.acquisition is None:
        acq = ''
    else:
        acq = '_{f.acquisition}'
    return f'{f.subject}_run-{f.run}{acq}_{event_type}{ext}'


def get_events(names):
    """Get events, but order by finger

    Parameters
    ----------
    names : list of str
        all the events in the dataset

    Returns
    -------
    list of str
        list of events (thumb, index etc)
    """
    from .parameters import FINGERS_CLOSED, FINGERS_OPEN, FINGERS_FLEXION, FINGERS_EXTENSION
    events = []
    if 'thumb close' in names:
        events.extend(FINGERS_CLOSED)
    if 'thumb open' in names:
        events.extend(FINGERS_OPEN)
    if 'thumb flexion' in names:
        events.extend(FINGERS_FLEXION)
    if 'thumb extension' in names:
        events.extend(FINGERS_EXTENSION)

    return events


def find_max_point(parameters, tf_cht):
    """Take the channel with the highest value and the interval containing that
    point

    Parameters
    ----------
    tf_cht : instance of ChanTime

    Returns
    -------
    str
        channel with largest activity
    tuple of float
        interval centered around largest activity
    """
    INTERVAL = parameters['spectrum']['select']['timeinterval']
    if parameters['spectrum']['select']['peak'] == 'positive':
        gain = 1
    elif parameters['spectrum']['select']['peak'] == 'negative':
        gain = -1
    ind = unravel_index(argmax(gain * tf_cht.data[0], axis=None), tf_cht.data[0].shape)
    max_chan = tf_cht.chan[0][ind[0]]
    max_timeinterval = (
        tf_cht.time[0][ind[1]] - INTERVAL / 2,
        tf_cht.time[0][ind[1]] + INTERVAL / 2,
        )

    return max_chan, max_timeinterval


def get_color_for_val(value, colorscale, vmin=0, vmax=1):
    """Return RGB value for plotly

    Parameters
    ----------
    value : float
        value of interest (between vmin and vmax)
    colorscale : str
        name of the color scale
    vmin : float
        minimal value (lowest value on the color scale)
    vmax : float
        maximal value (highest value on the color scale)

    Returns
    -------
    str
        RGB color in plotly format
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


def group_per_condition(data, names, operator='mean'):
    from .parameters import EVENTS

    dat = []
    for ev in EVENTS:
        i = create_bool(names, ev)
        y = data.data[0][..., i]
        if operator == 'mean':
            dat.append(y.mean(axis=-1))
        elif operator == 'median':
            dat.append(median(y, axis=-1))
        elif operator == 'std':
            dat.append(std(y, axis=-1))
        elif operator == 'sem':
            dat.append(std(y, axis=-1) / sqrt(y.shape[-1]))
        elif operator == 'tstat':
            res = ttest_1samp(y, 0, axis=-1)
            dat.append(res.statistic)
    out = data._copy()
    out.data[0] = moveaxis(array(dat), 0, -1)
    out.axis.pop('trial_axis')
    out.axis['event'] = array((1, ), dtype='O')
    out.axis['event'][0] = array(EVENTS)

    return out, array(EVENTS)


def create_bool(events, to_select):
    i_finger = zeros(len(events), dtype='bool')
    for i, evt in enumerate(events):
        if evt.startswith(to_select):
            i_finger[i] = True
    return i_finger


def be_nice():
    nice(10)
