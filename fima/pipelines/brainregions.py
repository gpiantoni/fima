from logging import getLogger
from numpy import r_, argmin
from numpy.linalg import norm

from ..parameters import REGION_TYPES
from ..names import name
from ..read import load
from ..viz.brainregions import plot_brain_regions
from ..viz.utils import to_div, to_html
from ..matlab.pial import make_pial_thick

lg = getLogger(__name__)


def pipeline_brainregions(parameters, ieeg_file):
    """Run pipeline to compute power spectrum on one participant, one run

    Parameters
    ----------
    subject : str
        subject code
    """
    make_pial_thick(parameters, ieeg_file)

    try:
        elec = load('electrodes', parameters, ieeg_file)
    except FileNotFoundError:
        return

    aparc = {}
    for template in REGION_TYPES:
        aparc[template] = load(template, parameters, ieeg_file)

    out_dir = parameters['paths']['output'] / 'brainregions'
    out_dir.mkdir(exist_ok=True, parents=True)

    tsv_file = name(parameters, 'brainregions', ieeg_file)
    with tsv_file.open('w') as f:
        HDR = ['chan', 'x', 'y', 'z'] + REGION_TYPES
        f.write('\t'.join(HDR))

        for el in elec:
            pos = r_[el['x'], el['y'], el['z']]
            i_vert = argmin(norm(aparc['aparc.a2009s']['vert'] - pos, axis=1))

            f.write(f"\n{el['name']}\t{el['x']}\t{el['y']}\t{el['z']}")
            for region_name, i_aparc in aparc.items():
                region = i_aparc['regions']['names'][i_aparc['regions']['values'][i_vert]]
                if region_name.startswith('BA_exvivo'):
                    region = region.split('_')[0]
                f.write(f"\t{region}")

    # not very efficient because we read the surf every time but the function call is much cleaner
    divs = []
    for region_type in REGION_TYPES:
        fig = plot_brain_regions(parameters, ieeg_file, region_type)
        divs.append(to_div(fig))

    to_html(divs, name(parameters, 'brainregions_plot', ieeg_file))
