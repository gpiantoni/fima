"""General parameters useful for all the functions"""

from .utils import get_color_for_val


"""
    align=dict(
        time=(-1, 1.5),
        threshold=dict(
            low=0.5,
            high=3,
            ),
        ),
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
