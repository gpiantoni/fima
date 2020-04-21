from ..fingers.max_activity import find_activity_per_finger
from ..viz.finger_channels import plot_finger_chan
from ..viz import to_div, to_html
from ..parameters import FINGERS_DIR, SUBJECTS


def pipeline_fingers_all(event_type='cues'):

    for subject, runs in SUBJECTS.items():
        for run in runs:
            print(f'{subject} / {run}')
            try:
                pipeline_fingers(subject, run, event_type)
            except Exception as err:
                print(err)


def pipeline_fingers(subject, run, event_type='cues'):
    v, chans = find_activity_per_finger(subject, run)
    fig = plot_finger_chan(v, chans)

    divs = [to_div(fig), ]

    html_file = FINGERS_DIR / event_type / f'{subject}_run-{run}_{event_type}.html'
    to_html(divs, html_file)
