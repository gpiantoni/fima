"""Read the data, based on event type and onset time"""
from numpy import genfromtxt, isin, isnan
from bidso.objects import Electrodes
from wonambi.attr import Freesurfer

from .preproc import read_data
from .dataglove.read_dataglove import read_physio
from .parameters import BIDS_DIR, SCRIPTS_DIR, FREESURFER_DIR
from .preproc.elec import read_surf
from .align.maxmin import main_func


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
      - 'continuous' returns: ChanTime, event_names, events_onsets
      - 'data' returns: ChanTime, event_names
      - 'aligned' returns: ChanTime, event_names
      - 'events' returns: ndarray
      - 'dataglove' returns: ndarray
      - 'movements' returns: ndarray
      - 'electrodes'
      - 'surface'
      - 'freesurfer'

    EVENT_TYPE:
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

    if what in ('continuous', 'data', 'aligned'):
        pattern = f'sub-{subject}_*_acq-{acq}_run-{run}_ieeg.eeg'
        folder = BIDS_DIR

    elif what == 'events':
        pattern = f'sub-{subject}_*_run-{run}_events.tsv'
        folder = BIDS_DIR

    elif what == 'electrodes':
        pattern = f'sub-{subject}_*_acq-{acq}_run-{run}_electrodes.tsv'
        folder = BIDS_DIR

    elif what in ('surface', 'freesurfer'):
        pattern = subject
        folder = FREESURFER_DIR

    elif what == 'dataglove':
        pattern = f'sub-{subject}_*_rec-dataglove_run-{run}_physio.tsv.gz'
        folder = BIDS_DIR

    elif what == 'movements':
        pattern = f'{subject}_run-{run}_dataglove.tsv'
        folder = SCRIPTS_DIR / 'movements'

    else:
        raise ValueError(f'Unrecognize "{what}" selection')

    found = list(folder.rglob(pattern))

    if len(found) == 0:
        raise FileNotFoundError('Could not find any file')
    elif len(found) > 1:
        raise ValueError('You need to specify more parameters')
    filename = found[0]

    if what in ('continuous', 'data', 'aligned'):
        events, onsets = select_events(subject, run, event_type)

        if what == 'continuous':
            data = read_data(filename, event_onsets=onsets, continuous=True)
            return data, events, onsets

        if what == 'aligned':
            data = read_data(filename, event_onsets=onsets)
            offsets = main_func(data, events)
            onsets = onsets + offsets['t_peak']

        data = read_data(filename, event_onsets=onsets)
        return data, events

    elif what == 'dataglove':
        return read_physio(filename)

    elif what == 'electrodes':
        elec = Electrodes(filename)
        return elec.electrodes.tsv[['name', 'x', 'y', 'z']]

    elif what == 'surface':
        elec = load('electrodes', subject, run, acq)
        right_or_left = (elec['x'] > 0).sum() / elec.shape[0]
        return read_surf(filename, right_or_left)

    elif what == 'freesurfer':
        return Freesurfer(filename)

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
            ('response_time', 'float'),  # if -1, it means that we can reject trial
            ('value', 'int')
            ]
        return genfromtxt(filename, delimiter='\t', skip_header=1, dtype=dtypes)


def select_events(subject, run, t):
    """Select events for one subject / run

    Parameters
    ----------
    subject : str
        subject code
    run : str
        number of the run of interest
    t : str
        event type used to identify the trials (one of 'cues', 'open', 'close',
        'movements', 'extension', 'flexion')

    Returns
    -------
    ndarray
        (N, ) vector of onset times (float)
    ndarray
        (N, ) vector of events (str)
    """
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
    else:
        raise ValueError(f'Unknown event_type "{t}"')

    events = load(to_load, subject, run)
    if to_load == 'events':
        # get rid of "palm open" etc
        events['trial_type'] = [' '.join(x.split(' ')[:2]) for x in events['trial_type']]

    i_evt = isin(events['trial_type'], trial_types) & isnan(events['response_time'])
    event_onsets = events['onset'][i_evt]
    event_types = events['trial_type'][i_evt]
    return event_types, event_onsets
