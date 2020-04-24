from pathlib import Path
from platform import node
from .utils import get_color_for_val


NYU_DIR = Path('/Fridge/R01_BAIR/data/nyu/scitran/bair/nyu')

if node() == 'archxps':
    PROJ_DIR = Path('/home/gio/projects/finger_mapping')
else:
    PROJ_DIR = Path('/Fridge/users/giovanni/projects/finger_mapping')

SCRIPTS_DIR = PROJ_DIR / 'scripts'
BIDS_DIR = PROJ_DIR / 'subjects'
FREESURFER_DIR = PROJ_DIR / 'freesurfer/'

RESULTS_DIR = PROJ_DIR / 'results'
DATAGLOVE_DIR = RESULTS_DIR / 'dataglove'
OVERVIEW_DIR = RESULTS_DIR / 'data_quality'
SPECTRUM_DIR = RESULTS_DIR / 'spectrum'
FINGERS_DIR = RESULTS_DIR / 'fingers'
FITTING_DIR = RESULTS_DIR / 'fitting'

P = dict(
    data_quality=dict(
        histogram=dict(
            contamination=0.04,
            ),
        spectrum=dict(
            n_neighbors=20,
            ),
        ),
    viz=dict(
        colorscale='Jet',
        tfr=dict(
            max=5,
            ),
        tfr_mean=dict(
            max=3,
            ),
        ),
    spectrum=dict(
        baseline=dict(
            time=(-0.6, 0.6),
            ),
        select=dict(
            freq=(60, 200),
            ),
        ),
    )


SUBJECTS = {
    'drouwen': [1, ],
    'duiven': [1, 2],
    'franeker': [1, 2],
    'heek': [1, 2],
    'intraop008': [1, ],
    'intraop013': [1, 2],
    'intraop016': [1, ],
    'itens': [1, 2, 3],
    'lemmer': [1, 2],
    'ommen': [1, 2],
    'vledder': [2, 3],
    'warmond': [1, 2],
    }

MOVEMENT_SYMBOL_DATA = {
    'open': 'circle',
    'close': 'circle-open',
    }

MOVEMENT_SYMBOL_MODEL = {
    'open': 'diamond',
    'close': 'diamond-open',
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
