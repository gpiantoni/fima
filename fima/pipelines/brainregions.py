from logging import getLogger
from numpy import r_, argmin
from numpy.linalg import norm

from bidso import Task

from ..read import load

lg = getLogger(__name__)


def pipeline_brainregions(parameters, ieeg_file):
    """Run pipeline to compute power spectrum on one participant, one run

    Parameters
    ----------
    subject : str
        subject code
    """
    elec = load('electrodes', parameters, ieeg_file)

    aparc = {}
    for template in ('aparc.a2009s', 'aparc.DKTatlas', 'BA_exvivo'):
        aparc[template] = load(template, parameters, ieeg_file)

    out_dir = parameters['paths']['output'] / 'brainregions'
    out_dir.mkdir(exist_ok=True, parents=True)

    ieeg = Task(ieeg_file)

    tsv_file = out_dir / f'sub-{ieeg.subject}_ses-{ieeg.session}_acq-{ieeg.acquisition}_brainregions.tsv'
    with tsv_file.open('w') as f:
        f.write('chan\tx\ty\tz\ta2009s\tDKTatlas\tBA')

        for el in elec:
            pos = r_[el['x'], el['y'], el['z']]
            pos_surf = pos - aparc['aparc.a2009s']['ras_shift']  # ras_shift depends on T1.mgz not on aparc
            i_vert = argmin(norm(aparc['aparc.a2009s']['vert'] - pos_surf, axis=1))

            f.write(f"\n{el['name']}\t{el['x']}\t{el['y']}\t{el['z']}")
            for name, i_aparc in aparc.items():
                region = i_aparc['regions']['names'][i_aparc['regions']['values'][i_vert]]
                if name == 'BA_exvivo':
                    region = region.split('_')[0]
                f.write(f"\t{region}")
