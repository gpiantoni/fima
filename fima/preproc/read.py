from wonambi.bids.structure import BIDSEEG
from wonambi.trans import montage


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

    chans = d.channels[
        (d.channels['status'] == 'good') &
        ((d.channels['type'] == 'ECOG') |
         (d.channels['type'] == 'SEEG'))
        ]

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
