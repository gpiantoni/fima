from bidso.utils import replace_underscore
from bidso.objects import Electrodes
from wonambi.attr import Freesurfer

from ..parameters import FREESURFER_DIR


def read_elec(filename):
    elec_file = replace_underscore(filename, 'electrodes.tsv')
    elec = Electrodes(elec_file)
    return elec.electrodes.tsv[['name', 'x', 'y', 'z']]


def read_surf(filename):
    elec = read_elec(filename)
    right_or_left = (elec['x'] > 0).sum() / elec.shape[0]

    fs_subj = filename.stem.split('_')[0][4:]
    fs = Freesurfer(FREESURFER_DIR / fs_subj)
    ras_shift = fs.surface_ras_shift

    if right_or_left > 0.5:
        hemi = 'rh'
    else:
        hemi = 'lh'

    pial = getattr(fs.read_brain(), hemi)
    pial.vert[:, 0] += ras_shift[0],
    pial.vert[:, 1] += ras_shift[1],
    pial.vert[:, 2] += ras_shift[2],

    return pial
