from logging import getLogger

from ..read import load
from ..spectrum import compute_timefreq, get_chantime
from ..spectrum.baseline import apply_baseline_to_continuous
from ..parameters import RESULTS_DIR, SUBJECTS, P
from ..viz import to_html
from ..viz.continuous import plot_continuous

lg = getLogger(__name__)


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
    lg.debug(f'Loading data for {subject} / {run} (events: {event_type})')
    data, events, onsets = load('continuous', subject, run, event_type=event_type)

    lg.debug('Computing timefreq (baseline=False, mean=False)')
    tf = compute_timefreq(data, artifacts=SUBJECTS[subject][run], baseline=False, mean=False)

    lg.debug('Selecting frequency')
    tf_cht = get_chantime(tf)

    if baseline:
        lg.debug('Applying baseline to continuous')
        tf_cht = apply_baseline_to_continuous(tf_cht, onsets)
        baseline_name = '_' + P['spectrum']['baseline']['type']
    else:
        baseline_name = ''

    lg.debug('Plotting continuous')
    divs = plot_continuous(tf_cht, onsets, events)

    html_file = RESULTS_DIR / 'continuous' / event_type / f'{subject}_run-{run}_{event_type}{baseline_name}.html'
    to_html(divs, html_file)
