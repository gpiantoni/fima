from wonambi.bids.structure import BIDSEEG
from wonambi.trans import montage


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

    data = montage(data, ref_to_avg=True)

    return data
