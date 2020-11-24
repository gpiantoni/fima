from logging import getLogger

from .compute import compute_timefreq, get_chantime
from ..read import load
from ..parameters import SUBJECTS

lg = getLogger(__name__)


def get_continuous_cht(subject, run, event_type='cues'):

    lg.info(f'{subject:<10}/ {run} Loading data for events: {event_type}')
    data, events, onsets = load('continuous', subject, run, event_type=event_type)

    lg.info(f'{subject:<10}/ {run} Computing timefreq (baseline=False, mean=False)')
    tf = compute_timefreq(data, artifacts=SUBJECTS[subject][run], baseline=False, mean=False)

    lg.info(f'{subject:<10}/ {run} Selecting frequency')
    tf_cht = get_chantime(tf)

    return tf_cht, events, onsets
