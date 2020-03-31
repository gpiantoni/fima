from pathlib import Path

PROJ_DIR = Path('/Fridge/users/giovanni/projects/')
PROJ_DIR = Path('/home/gio/projects/')
SPECTRUM_DIR = PROJ_DIR / 'finger_mapping/results/spectrum_interactive/'
BIDS_DIR = PROJ_DIR / 'finger_mapping/subjects'
FREESURFER_DIR = PROJ_DIR / 'finger_mapping/freesurfer/'


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
