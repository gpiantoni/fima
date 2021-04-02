from logging import getLogger

from ..spectrum.baseline import apply_baseline_to_continuous
from ..viz import to_html
from ..viz.continuous import plot_continuous
from ..spectrum.continuous import get_continuous_cht

lg = getLogger(__name__)


def pipeline_continuous(parameters, ieeg):
    """Run pipeline to compute power spectrum on one participant, one run

    Parameters
    ----------
    parameters : dict
    """
    tf_cht, events, onsets = get_continuous_cht(parameters, ieeg)

    if parameters['spectrum']['baseline']['apply']:
        lg.info(f'Applying baseline to continuous')
        tf_cht = apply_baseline_to_continuous(tf_cht, onsets)
    lg.info(f'{subject:<10}/ {run} Plotting continuous')
    divs = plot_continuous(tf_cht, onsets, events)

    html_file = RESULTS_DIR / 'continuous' / event_type / f'{subject}_run-{run}_{event_type}.html'
    to_html(divs, html_file)
