"""Read the data, based on event type and onset time"""
from numpy import genfromtxt, isin, empty, NaN
from numpy.lib.recfunctions import append_fields
from bidso.objects import Electrodes
from bidso import Task
from nibabel.freesurfer.io import read_annot
from wonambi.attr import Freesurfer, Surf

from .preproc import read_data
from .dataglove.read_dataglove import read_physio
from .preproc.elec import read_surf, read_brainregion_colors, read_brainregion_colorscale
from .names import name
from .parameters import (
    FINGERS_OPEN,
    FINGERS_CLOSED,
    FINGERS_FLEXION,
    FINGERS_EXTENSION,
    )

FS_LABELS = [
    'aparc',  # same as aparc.DKTatlas
    'aparc.a2009s',
    'aparc.DKTatlas',
    'BA_exvivo',
    'BA_exvivo.thresh',
    ]


def load(what, parameters, ieeg_file, opts=None):
    """
    WHAT:
      - 'continuous' returns: ChanTime, event_names, events_onsets
      - 'data' returns: ChanTime, event_names
      - 'events' returns: ndarray
      - 'dataglove' returns: ndarray
      - 'electrodes'
      - 'freesurfer'
      - 'pial' returns original freesurfer pial mesh
      - 'surface' returns full mesh which should better reflect brain size
      - 'aparc'
      - 'aparc.a2009s'
      - 'aparc.DKTatlas'
      - 'BA_exvivo'

    EVENT_TYPE:
      - cues : all cues (to open and close)
      - open : cues to open fingers
      - close : cues to close fingers
      - movements : all actual movements (from dataglove)
      - extension : actual extension of all fingers
      - flexion : actual flexion of all fingers
      - realigned : realigned movement
    """
    if opts in ('data', 'continuous'):
        if opts is None:
            raise ValueError('You need to specify event_type')
        if opts not in ['cues', 'open', 'close', 'movements', 'extension', 'flexion', 'realigned']:
            raise ValueError(f'"{opts}" is not one of the possible event types')

    if what in ('data', 'continuous'):
        if opts is None:
            raise ValueError('You need to specify opts which is a dict with event_type, pre, post')

    ieeg = Task(ieeg_file)

    if what in ('continuous', 'data'):
        events_tsv = load('events', parameters, ieeg_file, opts['event_type'])
        events = events_tsv['trial_type']
        onsets = events_tsv['onset']

        if what == 'continuous':
            data = read_data(parameters, ieeg_file, event_onsets=onsets, opts=opts, continuous=True)
            return data, events, onsets
        elif what == 'data':
            data = read_data(parameters, ieeg_file, event_onsets=onsets, opts=opts, continuous=False)
            return data, events

    if what == 'electrodes':
        pattern = f'sub-{ieeg.subject}_*_acq-{ieeg.acquisition}_electrodes.tsv'
        folder = parameters['paths']['input']

    elif what == 'events':
        if opts in ('cues', 'open', 'close'):
            pattern = f'sub-{ieeg.subject}_*_run-{ieeg.run}_events.tsv'
            folder = parameters['paths']['input']
        elif opts in ('movements', 'extension', 'flexion'):
            pattern = f'sub-{ieeg.subject}_*_run-{ieeg.run}_dataglove.tsv'
            folder = parameters['paths']['movements']
        elif opts in ('realigned', ):
            event_path = name(parameters, 'realign', ieeg_file)
            pattern = event_path.name
            folder = event_path.parent

    elif what == 'dataglove':
        pattern = f'sub-{ieeg.subject}_*_run-{ieeg.run}_recording-dataglove_physio.tsv.gz'
        folder = parameters['paths']['input']

    elif what in ['pial', 'freesurfer', ] + FS_LABELS:
        pattern = 'sub-' + ieeg.subject
        folder = parameters['paths']['freesurfer_subjects_dir']

    elif what == 'surface':

        elec = load('electrodes', parameters, ieeg_file)
        right_or_left = (elec['x'] > 0).sum() / elec.shape[0]
        if right_or_left > 0.5:
            pattern = 'rh.pial'
        else:
            pattern = 'lh.pial'

        folder = name(parameters, 'surface_dir', ieeg_file)

    else:
        raise ValueError(f'Unrecognize "{what}" selection')

    found = list(folder.rglob(pattern))
    if len(found) == 0:
        raise FileNotFoundError(f'Could not find any file matching {pattern} in {folder}')
    elif len(found) > 1:
        raise ValueError('You need to specify more parameters')
    filename = found[0]

    if what == 'electrodes':
        elec = Electrodes(filename)
        return elec.electrodes.tsv[['name', 'x', 'y', 'z']]

    elif what == 'events':
        with filename.open() as f:
            x = f.readline()
        n_columns = x.count('\t') + 1
        dtypes = [
            ('onset', 'float'),
            ('duration', 'float'),
            ('trial_type', 'U4096'),
            ]
        if n_columns >= 4:
            dtypes.insert(3, ('value', 'int'))
        if n_columns == 5:
            dtypes.insert(3, ('response_time', 'float'))  # if -1, it means that we can reject trial

        events = genfromtxt(filename, delimiter='\t', skip_header=1, dtype=dtypes)

        if n_columns == 4:
            x = empty(len(events), dtype='float')
            x.fill(NaN)
            events = append_fields(events, 'response_time', x, usemask=False)

        return select_events(events, opts)

    elif what == 'dataglove':
        return read_physio(filename)

    elif what == 'pial':
        elec = load('electrodes', parameters, ieeg_file)
        right_or_left = (elec['x'] > 0).sum() / elec.shape[0]
        return read_surf(filename, right_or_left)

    elif what == 'surface':
        return Surf(filename)

    elif what in FS_LABELS:
        fs = load('freesurfer', parameters, ieeg_file)
        pial = load('pial', parameters, ieeg_file)
        hemi = pial.surf_file.stem

        aparc_file = fs.dir / 'label' / f'{hemi}.{what}.annot'
        region_values, region_ctab, region_names = read_annot(aparc_file)

        out = {
            'aparc': what,
            'ras_shift': fs.surface_ras_shift,
            'vert': pial.vert,
            'regions': {
                'values': region_values,
                'names': [x.decode() for x in region_names],
                'colors': read_brainregion_colors(region_names, region_ctab),
                'colorscale': read_brainregion_colorscale(region_ctab),
                }
            }

        return out

    elif what == 'freesurfer':
        return Freesurfer(filename)


def select_events(events, t):
    """Select events for one subject / run

    Parameters
    ----------
    events : ndarray
        events with onset, duration, trial_type
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
    if t in ['cues', 'realigned']:
        trial_types = FINGERS_OPEN + FINGERS_CLOSED
    elif t == 'open':
        trial_types = FINGERS_OPEN
    elif t == 'close':
        trial_types = FINGERS_CLOSED
    elif t == 'movements':
        trial_types = FINGERS_EXTENSION + FINGERS_FLEXION
    elif t == 'flexion':
        trial_types = FINGERS_FLEXION
    elif t == 'extension':
        trial_types = FINGERS_EXTENSION
    else:
        raise ValueError(f'Unknown event_type "{t}"')

    events['trial_type'] = [' '.join(x.split(' ')[:2]) for x in events['trial_type']]
    i_evt = isin(events['trial_type'], trial_types)
    return events[i_evt]
