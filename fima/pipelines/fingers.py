from ..fingers.max_activity import find_activity_per_finger, find_tstat_per_finger
from ..viz.finger_channels import plot_finger_chan
from ..fingers.viz import plot_fingerbars
from ..viz import to_div, to_html
from ..parameters import FINGERS_DIR, SUBJECTS, FINGERBARS_DIR, FINGERCORR_DIR
from ..fingers.correlation import plot_correlation

from numpy import corrcoef


def pipeline_fingers_all(event_type='cues', bars=False, corr=False):

    for subject, runs in SUBJECTS.items():
        for run in runs:
            print(f'{subject} / {run}')
            try:
                if bars:
                    pipeline_fingerbars(subject, run, event_type)
                elif corr:
                    pipeline_finger_correlations(subject, run, event_type)
                else:
                    pipeline_fingers(subject, run, event_type)
            except Exception as err:
                print(err)


def pipeline_fingers(subject, run, event_type='cues'):
    v, chans = find_activity_per_finger(subject, run)
    fig = plot_finger_chan(v, chans)

    divs = [to_div(fig), ]

    html_file = FINGERS_DIR / event_type / f'{subject}_run-{run}_{event_type}.html'
    to_html(divs, html_file)


def pipeline_fingerbars(subject, run, event_type='cues'):
    t, events = find_tstat_per_finger(subject, run, event_type)
    fig = plot_fingerbars(t, events)
    divs = [to_div(fig), ]

    html_file = FINGERBARS_DIR / event_type / f'{subject}_run-{run}_{event_type}.html'
    to_html(divs, html_file)


def pipeline_finger_correlations(subject, run, event_type, threshold=5):
    t, events = find_tstat_per_finger(subject, run, event_type)
    X = t.data[0]
    i_active = (X > threshold).any(axis=1)
    X1 = X[i_active]

    dat = corrcoef(X1.T)

    fig = plot_correlation(dat, events)
    divs = [to_div(fig), ]

    html_file = FINGERCORR_DIR / event_type / f'{subject}_run-{run}_{event_type}.html'
    to_html(divs, html_file)
