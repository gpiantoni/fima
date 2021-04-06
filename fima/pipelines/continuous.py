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
        lg.info('Applying baseline to continuous')
        tf_cht = apply_baseline_to_continuous(tf_cht, onsets)
    lg.info('Plotting continuous')
    divs = plot_continuous(tf_cht, onsets, events)

    html_file = parameters['paths']['output'] / 'continuous' / f'{ieeg.stem}.html'
    to_html(divs, html_file)
