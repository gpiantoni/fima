from numpy import mean, std, log10, moveaxis, concatenate, nanmean, nanstd
from wonambi.trans import select


def apply_baseline_to_continuous(tf, onsets, baseline='zscore'):

    v = []
    for on in onsets:
        x = select(tf, time=on + P['spectrum']['baseline']['time'])
        v.append(x.data[0])

    A = concatenate(v, axis=1)
    bline_m = nanmean(A, axis=1)[:, :, None]
    bline_sd = nanstd(A, axis=1)[:, :, None]

    if baseline == 'zscore':
        tf.data[0] = (tf.data[0] - bline_m) / bline_sd
    elif baseline == 'dB':
        tf.data[0] = 10 * log10(tf.data[0] / bline_m)

    return tf


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
