from logging import getLogger

from ..viz.dataglove import plot_dataglove
from ..read import load
from ..viz import to_div, to_html
from ..parameters import RESULTS_DIR

lg = getLogger(__name__)


def pipeline_dataglove(subject, run):
    try:
        events = load('events', subject, run)
    except FileNotFoundError:
        lg.warning(f'{subject:<10}/ {run} No events')
        return

    try:
        tsv = load('dataglove', subject, run)
    except FileNotFoundError:
        lg.warning(f'{subject:<10}/ {run} No dataglove file')
        return

    try:
        mov = load('movements', subject, run)
    except FileNotFoundError:
        mov = None
        lg.warning(f'{subject:<10}/ {run} You need to mark the movements')

    lg.info(f'{subject:<10}/ {run} Plotting dataglove data')
    fig = plot_dataglove(tsv, events, mov)
    html_file = RESULTS_DIR / 'dataglove' / f'{subject}_run-{run}_dataglove.html'
    to_html([to_div(fig), ], html_file)
