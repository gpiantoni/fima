from wonambi import Dataset
from wonambi.trans import montage
from numpy import array


FINGERS_OPEN = [
    'thumb open',
    'index open',
    'middle open',
    'ring open',
    'little open',
    ]


FINGERS_CLOSED = [
    'thumb close',
    'index close',
    'middle close',
    'ring close',
    'little close',
    ]


FINGERS = {
    'thumb': ['thumb open', 'thumb close'],
    'index': ['index open', 'index close'],
    'middle': ['middle open', 'middle close'],
    'ring': ['ring open', 'ring close'],
    'little': ['little open', 'little close'],
    }


def read_data(filename, event='all'):

    if event == 'all':
        event_list = FINGERS_OPEN + FINGERS_CLOSED
    elif event == 'open':
        event_list = FINGERS_OPEN
    elif event == 'closed':
        event_list = FINGERS_CLOSED
    else:
        event_list = FINGERS[event]

    d = BIDSEEG(filename)
    event_names, event_onsets = select_events(d, event_list)

    channels = d.channels[
        (self.channels['status'] == 'good') &
        ((self.channels['type'] == 'ECOG') |
         (self.channels['type'] == 'SEEG') )
        ]
    data = d.read_data(
        begtime=event_onsets[0],
        endtime=event_onsets[-1],
        chan=list(chans))
    chans = find_good_channels(data)

    data = d.read_data(events=event_onsets, pre=0.5, post=2, chan=list(chans))
    data = montage(data, ref_to_avg=True)

    return data, event_names


def select_events(d, events):

    onsets = []
    names = []
    for evt in d.read_markers():
        for event_name in events:
            if evt['name'].startswith(event_name):
                onsets.append(evt['start'])
                names.append(' '.join(evt['name'].split(' ')[:2]))

    return names, onsets
