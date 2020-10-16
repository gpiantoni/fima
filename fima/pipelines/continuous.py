from ..read import load
from ..spectrum import compute_timefreq, get_chantime
from ..parameters import CONTINUOUS_DIR, SUBJECTS
from ..viz import to_html
from ..viz.continuous import plot_continuous


def pipeline_continuous_all(event_type='cues'):
    for subject, runs in SUBJECTS.items():
        for run in runs:
            print(f'{subject} / {run}')
            try:
                pipeline_continuous(subject, run, event_type)
            except Exception as err:
                print(err)


def pipeline_continuous(subject, run, event_type='cues'):
    """Run pipeline to compute power spectrum on one participant, one run

    Parameters
    ----------
    subject : str
        subject code
    run : str
        number of the run of interest
    event_type : str
        event type used to identify the trials (one of 'cues', 'open', 'close',
        'movements', 'extension', 'flexion')
    """
    data, events, onsets = load('continuous', subject, run, event_type=event_type)

    tf = compute_timefreq(data, baseline=False, mean=False)
    tf_cht = get_chantime(tf)

    divs = plot_continuous(tf_cht, onsets, events)

    html_file = CONTINUOUS_DIR / event_type / f'{subject}_run-{run}_{event_type}.html'
    to_html(divs, html_file)
