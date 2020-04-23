from wonambi.trans import apply_baseline, timefrequency, concatenate, math, select

from ..parameters import P


def compute_timefreq(data, method='spectrogram', baseline=True, mean=True):

    tf = timefrequency(
        data,
        'spectrogram',
        duration=0.3,
        overlap=0.9,
        taper='dpss',
        halfbandwidth=10)

    if baseline:
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


def get_chantime(tf, freq=None):
    if freq is None:
        freq = P['spectrum']['select']['freq']
    return math(
        select(tf, freq=freq),
        operator_name='mean',
        axis='freq')


def get_chan(tf, freq=None, time=None):
    if time is None:
        time = P['spectrum']['select']['time']
    tf = get_chantime(tf, freq=freq)
    return math(
        select(
            tf,
            time=time,
            ),
        operator_name='mean',
        axis='time')
