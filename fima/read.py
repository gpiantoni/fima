from numpy import genfromtxt

from .preproc import read_data
from .dataglove.read_dataglove import read_physio
from .parameters import BIDS_DIR, SCRIPTS_DIR


def load(what, subject, run=None, acq=None, event=None):
    """
    WHAT:
      - 'data' returns: ChanTime, event_names
      - 'events' returns: ndarray
      - 'dataglove' returns: ndarray
      - 'movements' returns: ndarray

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
        return read_data(filename, event=event)

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
