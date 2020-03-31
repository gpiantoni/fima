from wonambi.trans import apply_baseline, timefrequency, concatenate, math, select

from ..parameters import P


def compute_timefreq(data, method='spectrogram', mean=True):

    tf = timefrequency(
        data,
        'spectrogram',
        duration=0.3,
        overlap=0.9,
        taper='dpss',
        halfbandwidth=10)

    tf = apply_baseline(
        tf,
        time=P['spectrum']['baseline']['time'],
        baseline='dB')

    tf = concatenate(
        tf,
        axis='trial')

    if mean:
        tf = math(
            tf,
            operator_name='mean',
            axis='trial_axis')

    return tf


def get_chantime(tf):
    return math(
        select(
            tf,
            freq=P['spectrum']['select']['freq'],
            ),
        operator_name='mean',
        axis='freq')


def get_chan(tf):
    tf = get_chantime(tf)
    return math(
        select(
            tf,
            time=P['spectrum']['select']['time'],
            ),
        operator_name='mean',
        axis='time')
