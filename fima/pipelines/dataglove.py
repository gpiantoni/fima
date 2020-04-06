from ..dataglove.read_dataglove import _read_physio, _read_events
from ..dataglove.plot_dataglove import _plot_dataglove

from ..utils import make_name
from ..viz import to_div, to_html
from ..parameters import BIDS_DIR, DATAGLOVE_DIR

def pipeline_dataglove():
    for physio_tsv in BIDS_DIR.rglob('*_rec-dataglove_physio.tsv.gz'):
        print(physio_tsv.stem)
        tsv = _read_physio(physio_tsv)
        events = _read_events(physio_tsv)
        fig = _plot_dataglove(tsv, events)
        fig_name = make_name(physio_tsv, 'dataglove')
        to_html([to_div(fig), ], DATAGLOVE_DIR / fig_name)
