from logging import getLogger

from .compute import compute_timefreq, get_chantime
from ..read import load

lg = getLogger(__name__)


def get_continuous_cht(parameters, ieeg_file):

    event_type = parameters['continuous']['read']['event_type']
    data, events, onsets = load('continuous', parameters, ieeg_file, event_type)

    lg.info('Computing timefreq (baseline=False, mean=False)')
    tf = compute_timefreq(parameters, data, baseline=False, mean=False)

    if parameters['spectrum']['method'] != 'hilbert':
        lg.info('Selecting frequency')
        tf = get_chantime(parameters, tf)

    return tf, events, onsets
