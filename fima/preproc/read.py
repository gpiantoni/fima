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


def select_events(d, events):

    """
    Events : str
        - cues : all cues (to open and close)
        - open : cues to open fingers
        - close : cues to close fingers
        - movements : all actual movements (from dataglove)
        - extension : actual extension of all fingers
        - flexion : actual flexion of all fingers
    """

    if event == 'all':
        event_list = FINGERS_OPEN + FINGERS_CLOSED
    elif event == 'open':
        event_list = FINGERS_OPEN
    elif event == 'closed':
        event_list = FINGERS_CLOSED
    else:
        event_list = FINGERS[event]
    onsets = []
    names = []
    for evt in d.events:
        for event_name in events:
            if evt['trial_type'].startswith(event_name):
                onsets.append(evt['onset'])
                names.append(' '.join(evt['trial_type'].split(' ')[:2]))

    return names, onsets
