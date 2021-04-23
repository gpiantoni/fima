from logging import getLogger

from ..spectrum.baseline import apply_baseline_to_continuous
from ..spectrum.continuous import get_continuous_cht

from ..names import name
from ..read import load

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
    # divs = plot_continuous(parameters, tf_cht, onsets, events)

    # prepare events for export
    mov = load('events', parameters, ieeg, 'movements')
    mov_export = []
    for m in mov:
        mov_export.append({
            'name': m['trial_type'],
            'start': m['onset'] - tf_cht.time[0][0],
            'end': m['onset'] + m['duration'] - tf_cht.time[0][0],
        })

    tf_cht.s_freq = 1 / (tf_cht.time[0][1] - tf_cht.time[0][0])
    tf_cht.export(
        name(parameters, 'continuous', ieeg),
        'brainvision',
        markers=mov_export)
