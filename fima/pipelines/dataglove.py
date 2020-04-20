from ..dataglove.plot import plot_dataglove
from ..read import load
from ..viz import to_div, to_html
from ..parameters import DATAGLOVE_DIR, SUBJECTS


def pipeline_dataglove_all():
    for subject, runs in SUBJECTS.items():
        for run in runs:
            pipeline_dataglove(subject, run)


def pipeline_dataglove(subject, run):
    events = load('events', subject, run)
    try:
        tsv = load('dataglove', subject, run)
    except FileNotFoundError:
        return
    mov = load('movements', subject, run)

    fig = plot_dataglove(tsv, events, mov)
    fig_name = f'{subject}_run-{run}_dataglove.html'
    to_html([to_div(fig), ], DATAGLOVE_DIR / fig_name)
