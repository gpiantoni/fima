from wonambi.trans import select, math
from numpy import c_, zeros
from ..spectrum.compute import compute_timefreq, get_chantime, get_chan
from ..read import load
from ..utils import find_max_point


FINGERS = ('thumb', 'index', 'middle', 'ring', 'little')


def find_activity_per_finger(subject, run, event_type='cues'):
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


def create_bool(events, to_select):
    i_finger = zeros(len(events), dtype='bool')
    for i, evt in enumerate(events):
        if evt.startswith(to_select):
            i_finger[i] = True
    return i_finger
