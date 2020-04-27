from wonambi.attr import Freesurfer


def read_surf(filename, right_or_left):

    fs = Freesurfer(filename)
    ras_shift = fs.surface_ras_shift

    if right_or_left > 0.5:
        hemi = 'rh'
    else:
        hemi = 'lh'

    pial = getattr(fs.read_brain(), hemi)
    if 'som' not in filename.name:
        pial.vert[:, 0] += ras_shift[0]
        pial.vert[:, 1] += ras_shift[1]
        pial.vert[:, 2] += ras_shift[2]

    return pial
