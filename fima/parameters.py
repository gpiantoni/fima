from pathlib import Path
from platform import node


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
SPECTRUM_DIR = RESULTS_DIR / 'spectrum_interactive/'

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
        colorscale='jet',
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
