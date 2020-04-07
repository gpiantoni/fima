from pathlib import Path
from platform import node

if node() == 'archxps':
    PROJ_DIR = Path('/home/gio/projects/finger_mapping')
else:
    PROJ_DIR = Path('/Fridge/users/giovanni/projects/finger_mapping')
BIDS_DIR = PROJ_DIR / 'subjects'
FREESURFER_DIR = PROJ_DIR / 'freesurfer/'

RESULTS_DIR = PROJ_DIR / 'results'
DATAGLOVE_DIR = RESULTS_DIR / 'dataglove'
OVERVIEW_DIR = RESULTS_DIR / 'data_quality'
SPECTRUM_DIR = RESULTS_DIR / 'spectrum_interactive/'


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
            time=(-0.4, -0.1),
            ),
        select=dict(
            freq=(60, 200),
            time=(0.4, 0.8),
            ),
        ),
    )
