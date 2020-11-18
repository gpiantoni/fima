"""General parameters useful for all the functions"""

from pathlib import Path
from platform import node
from .utils import get_color_for_val


NYU_DIR = Path('/Fridge/R01_BAIR/data/nyu/scitran/bair/nyu')

if node() == 'archxps':
    PROJ_DIR = Path('/home/gio/projects/finger_mapping')
else:
    PROJ_DIR = Path('/Fridge/users/giovanni/projects/finger_mapping')

SCRIPTS_DIR = PROJ_DIR / 'scripts'
BIDS_DIR = PROJ_DIR / 'subjects2'
FREESURFER_DIR = PROJ_DIR / 'freesurfer/'

RESULTS_DIR = PROJ_DIR / 'results'
DATAGLOVE_DIR = RESULTS_DIR / 'dataglove'
CONTINUOUS_DIR = RESULTS_DIR / 'continuous'
OVERVIEW_DIR = RESULTS_DIR / 'data_quality'
SPECTRUM_DIR = RESULTS_DIR / 'spectrum'
FINGERS_DIR = RESULTS_DIR / 'fingers'
FINGERBARS_DIR = RESULTS_DIR / 'finger_bars'
FINGERCORR_DIR = RESULTS_DIR / 'finger_corr'
FINGERCORREACH_DIR = RESULTS_DIR / 'finger_correach'
FITTING_DIR = RESULTS_DIR / 'fitting'

P = dict(
    read=dict(
        pre=2,
        post=2,
        ),
    data_quality=dict(
        histogram=dict(
            contamination=0.04,
            ),
        spectrum=dict(
            n_neighbors=20,
            ),
        ),
    align=dict(
        time=(-1, 1.5),
        threshold=dict(
            low=0.5,
            high=3,
            ),
        ),
    viz=dict(
        colorscale='Jet',
        tfr=dict(
            max=10,
            ),
        tfr_mean=dict(
            max=5,
            ),
        ),
    spectrum=dict(
        method='spectrogram',  # spectrogram or morlet
        window_size=0.3,
        baseline=dict(
            time=(-1, -0.5),
            common=True,  # use the same, common baseline for all the trials
            type='zscore',  # dB or zscore or percent or relchange
            ),
        select=dict(
            freq=(100, 140),  # (60, 200)
            timeinterval=0.3,  # fima/utils.py
            ),
        ),
    )


SUBJECTS = {
    'drouwen': {
        '1': [],
        },
    'duiven': {
        '1': [
            (237, 243),
            ],
        '2': [],
        },
    'franeker': {
        '1': [],
        '2': [],
        },
    'heek': {
        '1': [
            (190, 194),
            ],
        '2': [
            (21, 28),
            ],
        },
    'intraop008': {
        '1': [
            (85, 86),
            (112.5, 113),
            (345, 346),
            ],
        },
    'intraop013': {
        '1': [
            (36, 37),
            (63.5, 64.5),
            ],
        '2': [
            (27.5, 29.5),
            (33.5, 40),
            (247.5, 249),
            (257, 261),
            ],
        },
    'intraop016': {
        '1': [],
        },
    'itens': {
        '1': [
            (215, 216),
            ],
        '2': [],
        '3': [],
        },
    'lemmer': {
        '1': [],
        '2': [],
        },
    'ommen': {
        '1': [],
        '2': [],
        },
    'veere': {
        '1': [],
        },
    'vledder': {
        '2': [],
        '3': [],
        },
    'warmond': {
        '1': [],
        '2': [],
        },
    'som705': {
        '01': [],
        },
    }

MOVEMENT_SYMBOL_DATA = {
    'open': 'circle-open',
    'close': 'circle',
    }

MOVEMENT_SYMBOL_MODEL = {
    'open': 'diamond-open',
    'close': 'diamond',
    }

MOVEMENT_LINE = {
    'open': 'dot',
    'close': 'solid',
    }

FINGER_COLOR = {
    'thumb': get_color_for_val(4, P['viz']['colorscale'], -1, 5),
    'index': get_color_for_val(3, P['viz']['colorscale'], -1, 5),
    'middle': get_color_for_val(2, P['viz']['colorscale'], -1, 5),
    'ring': get_color_for_val(1, P['viz']['colorscale'], -1, 5),
    'little': get_color_for_val(0, P['viz']['colorscale'], -1, 5),
}

FINGERS = list(FINGER_COLOR)


EVENTS = []
for action in MOVEMENT_LINE:
    for f in FINGERS:
        EVENTS.append(f'{f} {action}')
