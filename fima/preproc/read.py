from wonambi.bids.structure import BIDSEEG
from wonambi.trans import montage

from ..parameters import P


def read_data(filename, event_onsets, continuous=False):

    d = BIDSEEG(filename)
    chans = d.channels[
        (d.channels['status'] == 'good') &
        ((d.channels['type'] == 'ECOG') |
         (d.channels['type'] == 'SEEG'))
        ]

    if continuous:
        data = d.read_data(
            begtime=event_onsets[0] - P['read']['pre'],
            endtime=event_onsets[-1] + P['read']['post'],
            chan=list(chans['name']))
    else:
        data = d.read_data(events=event_onsets, pre=P['read']['pre'], post=P['read']['post'], chan=list(chans['name']))

    data = montage(data, ref_to_avg=True)

    return data
