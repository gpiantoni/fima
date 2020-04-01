from pathlib import Path

PROJ_DIR = Path('/home/gio/projects/finger_mapping')
PROJ_DIR = Path('/Fridge/users/giovanni/projects/finger_mapping')
BIDS_DIR = PROJ_DIR / 'subjects'
FREESURFER_DIR = PROJ_DIR / 'freesurfer/'

RESULTS_DIR = PROJ_DIR / 'results'
OVERVIEW_DIR = RESULTS_DIR / 'overview'
SPECTRUM_DIR = RESULTS_DIR / 'spectrum_interactive/'


P = dict(
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
