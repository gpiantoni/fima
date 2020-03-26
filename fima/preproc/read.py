from wonambi import Dataset
from wonambi.trans import montage
from numpy import array

from .bad_chan import find_good_channels


def read_data(filename):
    d = Dataset(filename, bids=True)
    mrk = d.read_markers()
    events = [x['start'] for x in mrk if 'open' in x['name']]

    is_ecog = d.dataset.task.channels.tsv['type'] == 'ECOG'
    is_seeg = d.dataset.task.channels.tsv['type'] == 'SEEG'
    chans = array(d.header['chan_name'])[is_ecog | is_seeg]
    data = d.read_data(begtime=events[0], endtime=events[-1], chan=list(chans))
    chans = find_good_channels(data)
    print(len(chans))

    data = d.read_data(events=events, pre=0.5, post=2, chan=list(chans))
    data = montage(data, ref_to_avg=True)

    return data
