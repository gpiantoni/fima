from ..preproc.data_quality import plot_raw_overview
from ..utils import make_name
from ..viz import to_html
from ..parameters import BIDS_DIR, OVERVIEW_DIR


def pipeline_dataquality():
    for filename in BIDS_DIR.rglob('*_ieeg.eeg'):
        print(filename.stem)

        divs = plot_raw_overview(filename)[1]
        fig_name = make_name(filename, 'dataquality')
        to_html(divs, OVERVIEW_DIR / fig_name)
