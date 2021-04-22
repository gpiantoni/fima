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


def read_brainregion_colors(annot_names, annot_ctab):
    ctab = {}
    for region_name, val in zip(annot_names, annot_ctab):
        region_name = region_name.decode()
        if region_name.endswith('_exvivo'):
            region_name = region_name[:-7]
        ctab[region_name] = f'rgb({val[0]}, {val[1]}, {val[2]})'

    return ctab


def read_brainregion_colorscale(annot_ctab):
    colorscale = []
    for i, val in enumerate(annot_ctab):
        colorscale.append(
            [i , f'rgb({val[0]}, {val[1]}, {val[2]})'])
    colorscale = [[i0 / i, i1] for i0, i1 in colorscale]

    return colorscale
