from ..read import load
from ..spectrum import compute_timefreq, get_chantime
from ..spectrum.baseline import apply_baseline_to_continuous
from ..parameters import CONTINUOUS_DIR, SUBJECTS, P
from ..viz import to_html
from ..viz.continuous import plot_continuous


def pipeline_continuous_all(event_type='cues', baseline=False):
    for subject, runs in SUBJECTS.items():
        for run in runs:
            print(f'{subject} / {run}')
            try:
                pipeline_continuous(subject, run, event_type, baseline)
            except Exception as err:
                print(err)


def pipeline_continuous(subject, run, event_type='cues', baseline=False):
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
    if baseline:
        tf_cht = apply_baseline_to_continuous(tf_cht, onsets)
        baseline_name = '_' + P['spectrum']['baseline']['type']
    else:
        baseline_name = ''

    divs = plot_continuous(tf_cht, onsets, events)

    html_file = CONTINUOUS_DIR / event_type / f'{subject}_run-{run}_{event_type}{baseline_name}.html'
    to_html(divs, html_file)
