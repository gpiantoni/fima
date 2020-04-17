from numpy import genfromtxt, isin

from .preproc import read_data
from .dataglove.read_dataglove import read_physio
from .parameters import BIDS_DIR, SCRIPTS_DIR


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


FINGERS_FLEXION = [
    'thumb flexion',
    'index flexion',
    'middle flexion',
    'ring flexion',
    'little flexion',
    ]

FINGERS_EXTENSION = [
    'thumb extension',
    'index extension',
    'middle extension',
    'ring extension',
    'little extension',
    ]


def load(what, subject, run=None, acq=None, event_type=None):
    """
    WHAT:
      - 'data' returns: ChanTime, event_names
      - 'events' returns: ndarray
      - 'dataglove' returns: ndarray
      - 'movements' returns: ndarray

    EVENT_TYPE
      - cues : all cues (to open and close)
      - open : cues to open fingers
      - close : cues to close fingers
      - movements : all actual movements (from dataglove)
      - extension : actual extension of all fingers
      - flexion : actual flexion of all fingers
    """
    if run is None:
        run = '*'
    else:
        run = str(run)

    if acq is None:
        acq = '*'

    if what == 'data':
        pattern = f'sub-{subject}_*_acq-{acq}_run-{run}_ieeg.eeg'
        folder = BIDS_DIR

    elif what == 'events':
        pattern = f'sub-{subject}_*_run-{run}_events.tsv'
        folder = BIDS_DIR

    elif what == 'dataglove':
        pattern = f'sub-{subject}_*_rec-dataglove_run-{run}_physio.tsv.gz'
        folder = BIDS_DIR

    elif what == 'movements':
        pattern = f'{subject}_run-{run}_dataglove.tsv'
        folder = SCRIPTS_DIR / 'movements'

    found = list(folder.rglob(pattern))

    if len(found) == 0:
        raise FileNotFoundError('Could not find any file')
    elif len(found) > 1:
        raise ValueError('You need to specify more parameters')
    filename = found[0]

    if what == 'data':
        events, onsets = select_events(subject, run, event_type)
        return read_data(filename, event_onsets=onsets), events

    elif what == 'dataglove':
        return read_physio(filename)

    elif what == 'movements':
        dtypes = [
            ('onset', 'float'),
            ('duration', 'float'),
            ('trial_type', 'U4096'),
            ]
        return genfromtxt(filename, delimiter='\t', skip_header=1, dtype=dtypes)

    elif what == 'events':
        dtypes = [
            ('onset', 'float'),
            ('duration', 'float'),
            ('trial_type', 'U4096'),
            ('response_time', 'float'),
            ('value', 'int')
            ]
        return genfromtxt(filename, delimiter='\t', skip_header=1, dtype=dtypes)


def select_events(subject, run, t):

    if t == 'cues':
        trial_types = FINGERS_OPEN + FINGERS_CLOSED
        to_load = 'events'
    elif t == 'open':
        trial_types = FINGERS_OPEN
        to_load = 'events'
    elif t == 'close':
        trial_types = FINGERS_CLOSED
        to_load = 'events'
    elif t == 'movements':
        trial_types = FINGERS_EXTENSION + FINGERS_FLEXION
        to_load = 'movements'
    elif t == 'flexion':
        trial_types = FINGERS_FLEXION
        to_load = 'movements'
    elif t == 'extension':
        trial_types = FINGERS_EXTENSION
        to_load = 'movements'

    events = load(to_load, subject, run)
    if to_load == 'events':
        # get rid of "palm open" etc
        events['trial_type'] = [' '.join(x.split(' ')[:2]) for x in events['trial_type']]

    i_evt = isin(events['trial_type'], trial_types)
    event_onsets = events['onset'][i_evt]
    event_types = events['trial_type'][i_evt]
    return event_types, event_onsets
