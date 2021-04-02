from logging import getLogger

from .compute import compute_timefreq, get_chantime
from ..read import load
from ..parameters import SUBJECTS, P

lg = getLogger(__name__)


def get_continuous_cht(parameters, ieeg_file):

    lg.info(f'Loading data for events: {event_type}')
    data, events, onsets = load('continuous', ieeg_file)

    lg.info(f'Computing timefreq (baseline=False, mean=False)')
    tf = compute_timefreq(data, baseline=False, mean=False)

    if parameters['spectrum']['method'] != 'hilbert':
        lg.info(f'Selecting frequency')
        tf = get_chantime(tf)

    return tf, events, onsets
