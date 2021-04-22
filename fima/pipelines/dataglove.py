from logging import getLogger

from ..viz.dataglove import plot_dataglove
from ..read import load
from ..viz import to_div, to_html
from ..names import name

lg = getLogger(__name__)


def pipeline_dataglove(parameters, ieeg_file):
    try:
        events = load('events', parameters, ieeg_file, 'cues')
    except FileNotFoundError:
        lg.warning(f'{ieeg_file.stem} No events')
        return

    try:
        tsv = load('dataglove', parameters, ieeg_file)
    except FileNotFoundError:
        lg.warning(f'{ieeg_file.stem} No dataglove file')
        return

    try:
        mov = load('events', parameters, ieeg_file, 'movements')
    except FileNotFoundError:
        mov = None
        lg.warning(f'{ieeg_file.stem} You need to mark the movements')

    lg.info(f'{ieeg_file.stem} Plotting dataglove data')
    fig = plot_dataglove(tsv, events, mov)
    html_file = name(parameters, 'dataglove') / (ieeg_file.stem + '.html')
    to_html([to_div(fig), ], html_file)
