from logging import getLogger

from ..spectrum.baseline import apply_baseline_to_continuous
from ..viz import to_html
from ..viz.continuous import plot_continuous
from ..spectrum.continuous import get_continuous_cht

from ..names import name

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
        tf_cht = apply_baseline_to_continuous(parameters, tf_cht, onsets)
    lg.info('Plotting continuous')
    divs = plot_continuous(parameters, tf_cht, onsets, events)

    to_html(divs, name(parameters, 'continuous', ieeg))
