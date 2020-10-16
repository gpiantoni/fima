from numpy import arange, zeros, mean, std, log10, moveaxis
from wonambi.trans import apply_baseline, timefrequency, concatenate, math, select

from ..parameters import P


def compute_timefreq(data, baseline=True, mean=True):

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


def apply_common_baseline(tf, time, baseline):
    """Concatenate all the baseline periods for all the conditions. Keep it
    separate for each channel and each frequency"""

    tf_time = select(tf, time=time)

    X = moveaxis(tf_time.data[0], 1, 2)
    X = X.reshape((X.shape[0], X.shape[1], -1))

    bline_mean = mean(X, axis=-1)
    bline_std = std(X, axis=-1)

    if len(tf.list_of_axes) == 4:
        bline_m = bline_mean[:, None, :, None]
        bline_sd = bline_std[:, None, :, None]
    else:
        bline_m = bline_mean[:, None, :]
        bline_sd = bline_std[:, None, :]

    if baseline == 'zscore':
        tf.data[0] = (tf.data[0] - bline_m) / bline_sd
    elif baseline == 'dB':
        tf.data[0] = 10 * log10(tf.data[0] / bline_m)

    return tf
