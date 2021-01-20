from logging import getLogger
from numpy import r_, argmin
from numpy.linalg import norm

from ..read import load
from ..parameters import RESULTS_DIR

lg = getLogger(__name__)


def pipeline_brainregions(subject):
    """Run pipeline to compute power spectrum on one participant, one run

    Parameters
    ----------
    subject : str
        subject code
    """
    elec = load('electrodes', subject)

    aparc = {}
    for template in ('aparc.a2009s', 'aparc.DKTatlas'):
        aparc[template] = load(template, subject)

    out_dir = RESULTS_DIR / 'brainregions'
    out_dir.mkdir(exist_ok=True, parents=True)

    tsv_file = out_dir / f'{subject}_regions.tsv'
    with tsv_file.open('w') as f:
        f.write('chan\tx\ty\tz\ta2009s\tDKTatlas')

        for el in elec:
            pos = r_[el['x'], el['y'], el['z']]
            pos_surf = pos - aparc['aparc.a2009s']['ras_shift']  # ras_shift depends on T1.mgz not on aparc
            i_vert = argmin(norm(aparc['aparc.a2009s']['vert'] - pos_surf, axis=1))

            f.write(f"\n{el['name']}\t{el['x']}\t{el['y']}\t{el['z']}")
            for i_aparc in aparc.values():
                region = i_aparc['regions']['names'][i_aparc['regions']['values'][i_vert]]
                f.write(f"\t{region}")
