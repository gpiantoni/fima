from numpy import arange, zeros, median, diff, pad, NaN
from wonambi.trans import apply_baseline, timefrequency, concatenate, math, select, filter_

from .baseline import apply_common_baseline


def compute_timefreq(parameters, data, baseline=True, mean=True):

    if parameters['spectrum']['method'] == 'spectrogram':
        tf = timefrequency(
            data,
            'spectrogram',
            duration=parameters['spectrum']['window_size'],
            step=0.01,
            taper=parameters['spectrum']['taper'],
            halfbandwidth=5)

    elif parameters['spectrum']['method'] == 'wavelet':
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

    elif parameters['spectrum']['method'] == 'hilbert':
        f = filter_(data, low_cut=60, high_cut=200)
        tf = math(f, operator_name='hilbert', axis='time')
        tf = math(tf, operator_name='abs')

    tf = concatenate(
        tf,
        axis='trial')

    if baseline:
        if parameters['spectrum']['baseline']['common']:
            tf = apply_common_baseline(
                tf,
                time=parameters['spectrum']['baseline']['time'],
                baseline=parameters['spectrum']['baseline']['type'])

        else:
            tf = apply_baseline(
                tf,
                time=parameters['spectrum']['baseline']['time'],
                baseline=parameters['spectrum']['baseline']['type'])

    if mean:
        tf = math(
            tf,
            operator_name='nanmean',
            axis='trial_axis')

    return tf


def get_chantime(parameters, tf, freq=None, baseline=False, freq_operator='nanmean'):
    """
    freq_operator : nanmean or nanmax
    """
    if freq is None:
        freq = parameters['spectrum']['select']['freq']
    out = math(
        select(tf, freq=freq),
        operator_name=freq_operator,
        axis='freq')

    if parameters['artifacts']['remove'] == "chantime":
        out = hide_artifacts(parameters, out)

    if baseline:
        if parameters['spectrum']['baseline']['common']:
            out = apply_common_baseline(
                out,
                time=parameters['spectrum']['baseline']['time'],
                baseline=parameters['spectrum']['baseline']['type'])

        else:
            out = apply_baseline(
                out,
                time=parameters['spectrum']['baseline']['time'],
                baseline=parameters['spectrum']['baseline']['type'])

    return out


def get_chan(parameters, tf, freq=None, baseline=False, time=None, operator_name='nanmean'):
    if time is None:
        time = parameters['spectrum']['select']['time']
    tf = get_chantime(parameters, tf, freq=freq, baseline=baseline)
    return math(
        select(
            tf,
            time=time,
            ),
        operator_name=operator_name,
        axis='time')


def hide_artifacts(parameters, tf):
    t = tf.time[0]
    bad_smp = int(round((parameters['artifacts']['window'] / 2) / median(diff(t))))

    i_bad = tf.data[0] >= parameters['artifacts']['threshold']

    padded_bad = i_bad.copy()
    for i_roll in range(1, bad_smp):
        padded_bad |= pad(i_bad, ((0, 0), (i_roll, 0), (0, 0), ), mode='constant', constant_values=False)[:, :-i_roll, :]

    # after
    for i_roll in range(bad_smp):
        padded_bad |= pad(i_bad, ((0, 0), (0, i_roll), (0, 0), ), mode='constant', constant_values=False)[:, i_roll:, :]

    tf.data[0][padded_bad] = NaN

    return tf
