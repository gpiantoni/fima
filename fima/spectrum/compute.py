from numpy import arange, zeros
from wonambi.trans import apply_baseline, timefrequency, concatenate, math, select

from ..parameters import P
from .baseline import apply_common_baseline
from ..utils import hide_artifacts


def compute_timefreq(data, artifacts=None, baseline=True, mean=True):

    if P['spectrum']['method'] == 'spectrogram':
        tf = timefrequency(
            data,
            'spectrogram',
            duration=P['spectrum']['window_size'],
            step=0.01,
            taper='dpss',
            halfbandwidth=5)
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

    tf = concatenate(
        tf,
        axis='trial')

    if artifacts is not None:
        tf = hide_artifacts(tf, artifacts)

    if baseline:
        if P['spectrum']['baseline']['common']:
            tf = apply_common_baseline(
                tf,
                time=P['spectrum']['baseline']['time'],
                baseline=P['spectrum']['baseline']['type'])

        else:
            tf = apply_baseline(
                tf,
                time=P['spectrum']['baseline']['time'],
                baseline=P['spectrum']['baseline']['type'])

    if mean:
        tf = math(
            tf,
            operator_name='mean',
            axis='trial_axis')

    return tf


def get_chantime(tf, freq=None, baseline=False):
    if freq is None:
        freq = P['spectrum']['select']['freq']
    out = math(
        select(tf, freq=freq),
        operator_name='mean',
        axis='freq')

    if baseline:
        if P['spectrum']['baseline']['common']:
            out = apply_common_baseline(
                out,
                time=P['spectrum']['baseline']['time'],
                baseline=P['spectrum']['baseline']['type'])

        else:
            out = apply_baseline(
                out,
                time=P['spectrum']['baseline']['time'],
                baseline=P['spectrum']['baseline']['type'])

    return out


def get_chan(tf, freq=None, baseline=False, time=None, operator_name='mean'):
    if time is None:
        time = P['spectrum']['select']['time']
    tf = get_chantime(tf, freq=freq, baseline=baseline)
    return math(
        select(
            tf,
            time=time,
            ),
        operator_name=operator_name,
        axis='time')
