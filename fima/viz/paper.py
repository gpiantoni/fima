from pathlib import Path

from ..names import name
from ..read import load
from .utils import LAYOUT, merge
from .dataglove import plot_dataglove


def plot_papers(parameters):
    plot_dir = name(parameters, 'paper')

    fig = paper_plot_dataglove(parameters)
    fig.write_image(str(plot_dir / 'dataglove.svg'))


def paper_plot_dataglove(parameters):
    ieeg_file = Path('/Fridge/users/giovanni/projects/finger_mapping/subjects/sub-drouwen/ses-iemu1/ieeg/sub-drouwen_ses-iemu1_task-fingermapping_acq-clinical_run-1_ieeg.eeg')

    events = load('events', parameters, ieeg_file, 'cues')
    tsv = load('dataglove', parameters, ieeg_file)
    mov = load('events', parameters, ieeg_file, 'movements')

    fig = plot_dataglove(tsv, events, mov)

    layout = dict(
        width=300,
        height=200,
        xaxis=dict(
            showgrid=False,
            showline=False,
            zerolinewidth=0.5,
            title=dict(
                text='time (s)',
                standoff=4,
                ),
            range=(
                60,
                130,)
            ),
        yaxis=dict(
            showgrid=False,
            showline=False,
            zeroline=False,
            ),
    )

    return fig.update_layout(merge(LAYOUT, layout))
