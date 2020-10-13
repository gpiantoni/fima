from wonambi.bids.structure import BIDSEEG
from wonambi.trans import montage

from ..parameters import P


def read_data(filename, event_onsets):

    d = BIDSEEG(filename)
    chans = d.channels[
        (d.channels['status'] == 'good') &
        ((d.channels['type'] == 'ECOG') |
         (d.channels['type'] == 'SEEG'))
        ]

    data = d.read_data(events=event_onsets, pre=P['read']['pre'], post=P['read']['post'], chan=list(chans['name']))
    data = montage(data, ref_to_avg=True)

    return data
