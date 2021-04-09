"""General parameters useful for all the functions"""

from .utils import get_color_for_val


"""
P = dict(
    data_quality=dict(
        histogram=dict(
            contamination=0.04,
            ),
        spectrum=dict(
            n_neighbors=20,
            ),
        ),
    align=dict(
        time=(-1, 1.5),
        threshold=dict(
            low=0.5,
            high=3,
            ),
        ),
    ols=dict(
        window=dict(
            method='gaussian',  # gaussian or gamma (for gamma, use a as well)
            loc=[-.8, .3, 0.05],  # [-1, +1],
            scale=[0.03, 0.5, .03],  # [0.1, 2, .1],
            a=[1.5, 8.1, 0.5],
            ),
        ),
    viz=dict(
        colorscale='Jet',
        tfr=dict(
            max=3,
            ),
        tfr_mean=dict(
            max=2,
            ),
        ),
    spectrum=dict(
        method='spectrogram',  # spectrogram or wavelet or hilbert
        window_size=0.3,
        taper='dpss',  # dpss or hanning (only for spectrogram)
        baseline=dict(
            time=(-1, -0.5),
            common=True,  # use the same, common baseline for all the trials
            type='zscore',  # dB or zscore or percent or relchange
            ),
        select=dict(
            freq=(60, 150),  # (60, 200)
            timeinterval=0.3,  # fima/utils.py
            ),
        ),
    )

"""


COLORSCALE = 'Jet'

MOVEMENT_SYMBOL_DATA = {
    'open': 'circle-open',
    'close': 'circle',
    }

MOVEMENT_SYMBOL_MODEL = {
    'open': 'diamond-open',
    'close': 'diamond',
    }

MOVEMENT_LINE = {
    'open': 'dot',
    'close': 'solid',
    }

FINGER_COLOR = {
    'thumb': get_color_for_val(4, COLORSCALE, -1, 5),
    'index': get_color_for_val(3, COLORSCALE, -1, 5),
    'middle': get_color_for_val(2, COLORSCALE, -1, 5),
    'ring': get_color_for_val(1, COLORSCALE, -1, 5),
    'little': get_color_for_val(0, COLORSCALE, -1, 5),
    }

FINGERS = list(FINGER_COLOR)


FINGERS_OPEN = []
FINGERS_CLOSED = []
FINGERS_FLEXION = []
FINGERS_EXTENSION = []
for f in FINGERS:
    FINGERS_OPEN.append(f + ' open')
    FINGERS_CLOSED.append(f + ' close')
    FINGERS_FLEXION.append(f + ' flexion')
    FINGERS_EXTENSION.append(f + ' extension')

EVENTS = FINGERS_OPEN + FINGERS_CLOSED
