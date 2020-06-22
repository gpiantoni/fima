from numpy import arange, zeros
from wonambi.trans import apply_baseline, timefrequency, concatenate, math, select

from ..parameters import P


def compute_timefreq(data, baseline=True, mean=True):

    if P['spectrum']['method'] == 'spectrogram':
        tf = timefrequency(
            data,
            'spectrogram',
            duration=0.6,
            overlap=0.9,
            taper='dpss',
            halfbandwidth=10)
    else:
        tf = timefrequency(
            data,
            'morlet',
            foi=arange(1, 200),
            ratio=7,
            dur_in_sd=3
        )
        tf = math(tf, operator_name='abs')
        t_bool = zeros(tf.time[0].shape, dtype=bool)
        t_step = t_bool.shape[0] // 100
        t_bool[20:-20:t_step] = True
        tf = select(tf, time=t_bool)

    if baseline:
        tf = apply_baseline(
            tf,
            time=P['spectrum']['baseline']['time'],
            baseline=P['spectrum']['baseline']['type'])

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
