from logging import getLogger
from numpy import r_

from ..read import load
from ..parameters import RESULTS_DIR

lg = getLogger(__name__)


def pipeline_brainregions(subject, run):
    """Run pipeline to compute power spectrum on one participant, one run

    Parameters
    ----------
    subject : str
        subject code
    run : str
        number of the run of interest
    """
    elec = load('electrodes', subject, run)
    fs = load('freesurfer', subject, run)

    out_dir = RESULTS_DIR / 'brainregions'
    out_dir.mkdir(exist_ok=True, parents=True)

    for template in ('aparc.a2009s', 'aparc.DKTatlas'):
        tsv_file = out_dir / f'{subject}_{run}_regions_{template[6:]}.tsv'
        find_brainregions(fs, elec, tsv_file, template)


def find_brainregions(fs, elec, tsv_file, template):

    with tsv_file.open('w') as f:
        f.write('name\tx\ty\tz\tregion\tapprox\n')

        for el in elec:
            pos = r_[el['x'], el['y'], el['z']]

            region, approx = fs.find_brain_region(
                pos, template, max_approx=4,
                exclude_regions=['Unknown', 'Right-Cerebral-White-Matter', 'Left-Cerebral-White-Matter'])

            if template == 'aparc.DKTatlas':
                region = region.split('-')[2]
            elif template == 'aparc.a2009s':
                region = '_'.join(region.split('_')[2:])
            f.write(f"{el['name']}\t{el['x']}\t{el['y']}\t{el['z']}\t{region}\t{approx}\n")
