from tempfile import mkdtemp
from subprocess import run
from pathlib import Path

from ..read import load
from ..names import name


MATLAB_TEMPLATE = """\
addpath('/Fridge/users/giovanni/projects/finger_mapping/scripts/fima/matlab')
thicken_pial('{ribbon}', 'l', [3, 3], 0.1)
thicken_pial('{ribbon}', 'r', [3, 3], 0.1)
"""

def make_pial_thick(parameters, ieeg_file):
    fs = load('freesurfer', parameters, ieeg_file)
    output_dir = name(parameters, 'surface_dir', ieeg_file)

    ribbon_mgz = fs.dir / 'mri' / 'ribbon.mgz'
    ribbon_nii = Path(mkdtemp()) / 'ribbon.nii'

    run([
        'mri_convert',
        ribbon_mgz,
        ribbon_nii
    ])

    script_file = (output_dir / 'temp.m')
    with script_file.open('w') as f:
        f.write(MATLAB_TEMPLATE.format(ribbon=str(ribbon_nii)))

    run([
        'matlab',
        '-batch',
        "temp",
        ],
        cwd=output_dir
        )

    ribbon_nii.unlink()
    script_file.unlink()
