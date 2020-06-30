from wonambi.trans import select, math
from numpy import c_
from ..spectrum.compute import compute_timefreq, get_chantime, get_chan
from ..read import load
from ..utils import find_max_point, group_per_condition, create_bool
from ..parameters import FINGERS


def find_activity_per_finger(subject, run, event_type='cues'):
    """
    TODO
    ----
    this function could be rewritten using preexisting code
    """
    data, events = load('data', subject, run, event_type=event_type)
    tf = compute_timefreq(data, mean=True)
    tf = get_chantime(tf)
    best_time = find_max_point(tf)[1]

    tf = compute_timefreq(data, mean=False)
    tf = get_chan(tf, time=best_time)

    values = {}
    for f in FINGERS:
        i_finger = create_bool(events, f)
        tf_finger = select(tf, trial_axis=i_finger)
        tf_finger_chan = math(tf_finger, operator_name='mean', axis='trial_axis')
        values[f] = tf_finger_chan(trial=0)

    v = c_[values['thumb'], values['index'], values['middle'], values['ring'], values['little']]
    return v, tf.chan[0]


def find_tstat_per_finger(subject, run, event_type='cues'):
    """Get tstat for each finger

    TODO
    ----
    this function can be merged with the one above
    """
    data, names = load('data', subject, run, event_type=event_type)
    tf = compute_timefreq(data, mean=False)

    tf_m = math(tf, operator_name='mean', axis='trial_axis')
    tf_cht = get_chantime(tf_m)

    best_chan, best_time = find_max_point(tf_cht)

    tf_ch = get_chan(tf, time=best_time)
    t, events = group_per_condition(tf_ch, names, 'tstat')

    return t, events
