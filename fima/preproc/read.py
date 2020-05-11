from wonambi.bids.structure import BIDSEEG
from wonambi.trans import montage


def read_data(filename, event_onsets):

    d = BIDSEEG(filename)
    chans = d.channels[
        (d.channels['status'] == 'good') &
        ((d.channels['type'] == 'ECOG') |
         (d.channels['type'] == 'SEEG'))
        ]

    data = d.read_data(events=event_onsets, pre=0.5, post=2, chan=list(chans['name']))
    data = montage(data, ref_to_avg=True)

    return data
