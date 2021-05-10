from logging import getLogger
from numpy import NaN, pad, sum, mean, min, max, std

from wonambi.bids.structure import BIDSEEG
from wonambi.trans import montage


lg = getLogger(__name__)


def read_data(parameters, filename, event_onsets, continuous=False):

    d = BIDSEEG(filename)
    chans = d.channels[
        (d.channels['status'] == 'good')
        & (d.channels['type'] == 'ECOG')
        ]

    if continuous:
        data = d.read_data(
            begtime=event_onsets[0] - parameters['read']['pre'],
            endtime=event_onsets[-1] + parameters['read']['post'],
            chan=list(chans['name']))
    else:
        data = d.read_data(
            events=event_onsets,
            pre=parameters['read']['pre'],
            post=parameters['read']['post'],
            chan=list(chans['name']))

    if parameters['read']['artifacts']['remove']:
        data, bad_smp_per_chan = hide_artifacts(parameters, data)
        lg.info(f'{filename.stem} bad points {mean(bad_smp_per_chan):.3f}s, s.d. {std(bad_smp_per_chan):.3f}s [{min(bad_smp_per_chan):.3f}-{max(bad_smp_per_chan):.3f}s]')

    data = montage(data, ref_to_avg=True)

    return data


def hide_artifacts(parameters, data):

    data_comparison = montage(data, ref_to_avg=True, method='median')

    count_samples = []

    bad_smp = int(data.s_freq * parameters['read']['artifacts']['window'] / 2)

    for i_trl in range(data.number_of('trial')):
        i_bad = abs(data_comparison.data[i_trl]) > parameters['read']['artifacts']['threshold']

        # before
        padded_bad = i_bad.copy()
        for i_roll in range(1, bad_smp):
            padded_bad |= pad(i_bad, ((0, 0), (i_roll, 0)), mode='constant', constant_values=False)[:, :-i_roll]

        # after
        for i_roll in range(bad_smp):
            padded_bad |= pad(i_bad, ((0, 0), (0, i_roll)), mode='constant', constant_values=False)[:, i_roll:]

        data.data[i_trl][padded_bad] = NaN

        count_samples.append(padded_bad.sum(axis=1))

    bad_smp_per_chan = sum(count_samples, axis=0) / data.s_freq

    return data, bad_smp_per_chan
