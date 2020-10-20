from scipy.stats import ttest_ind

from ..spectrum import compute_timefreq, get_chan
from ..parameters import SUBJECTS, FINGERS
from ..read import load
from ..utils import group_per_condition, create_bool


def pipeline_flexext_all(event_type='cues', subject_only=None):
    for subject, runs in SUBJECTS.items():
        if subject_only is not None and subject != subject_only:
            continue
        for run in runs:
            print(f'{subject} / {run}')
            try:
                pipeline_flexext(subject, run, event_type)
            except Exception as err:
                print(err)


def pipeline_flexext(subject, run, event_type='cues'):

    data, events = load('data', subject, run, event_type=event_type)

    tf = compute_timefreq(data, baseline=False, mean=False)

    tf_ch = get_chan(tf, baseline=True, time=(-1, 1), operator_name='amax')
    tf_m = group_per_condition(tf_ch, events, 'mean')[0]
    bool_chan = (tf_m.data[0] > 15).any(axis=1)

    for finger in FINGERS:
        print('')
        print(finger)
        ev = finger + ' open'
        select_trl = create_bool(events, ev)
        x0 = tf_ch.data[0][bool_chan, :][:, select_trl]

        ev = finger + ' close'
        select_trl = create_bool(events, ev)
        x1 = tf_ch.data[0][bool_chan, :][:, select_trl]

        t = ttest_ind(x0, x1, axis=1)

        for i, chan in enumerate(tf_ch.chan[0][bool_chan]):
            if t.pvalue[i] > 0.05:
                continue
            if t.statistic[i] > 0:
                print(f'chan "{chan}" has higher power for "extension" than "flexion"')
            else:
                print(f'chan "{chan}" has higher power for "flexion" than "extension"')
