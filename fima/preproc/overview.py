from wonambi import Dataset
from wonambi.trans import montage, frequency
from numpy import arange, array, histogram, log10
import plotly.graph_objects as go
from pathlib import Path

from .read import select_events
from ..viz import to_div, to_html


def plot_raw_overview(filename):
    event_list = 'all'

    d = Dataset(filename, bids=True)
    event_names, event_onsets = select_events(d, event_list)

    is_ecog = d.dataset.task.channels.tsv['type'] == 'ECOG'
    is_seeg = d.dataset.task.channels.tsv['type'] == 'SEEG'
    chans = array(d.header['chan_name'])[is_ecog | is_seeg]
    data = d.read_data(begtime=event_onsets[0], endtime=event_onsets[-1], chan=list(chans))

    data = montage(data, ref_chan=['chan1', 'chan64'])  # which chans?
    freq = frequency(data, taper='hann', duration=2, overlap=0.5)

    print('*' * data.number_of('chan')[0])
    divs = []
    for one_chan in data.chan[0]:
        print('.', end='')
        fig = plot_raw_one_chan(data, freq, one_chan)
        divs.append(to_div(fig))

    to_html(divs, Path('/Fridge/users/giovanni/projects/finger_mapping/results/overview/vledder_blackrock_run-1.html'))


def plot_raw_one_chan(data, freq, chan):
    v, h = histogram(
        data(trial=0, chan=chan),
        bins=arange(-250, 250 + 10, 10),
        density=True)

    trace1 = go.Scatter(
        x=data.time[0],
        y=data(trial=0, chan=chan),
        line=dict(
            color='black',
            ),
        xaxis="x",
        yaxis="y"
        )

    trace2 = go.Bar(
        x=h + 10 / 2,
        y=v,
        xaxis="x2",
        yaxis="y2",
        marker=dict(
            color='black',
            ),
        )

    trace3 = go.Scatter(
        x=freq.freq[0],
        y=freq(trial=0, chan=chan),
        line=dict(
            color='black',
            ),
        xaxis="x3",
        yaxis="y3"
        )

    layout = go.Layout(
        title=chan,
        showlegend=False,
        xaxis=dict(
            title=dict(
                text='time (s)',
                standoff=0,
                ),
            domain=[0, 1],
            ),
        yaxis=dict(
            title='amplitude (μV)',
            range=(-250, 250),
            domain=[0.55, 1],
            ),
        xaxis2=dict(
            title='amplitude (μV)',
            domain=[0, 0.45],
            anchor='y2',
            ),
        yaxis2=dict(
            title='density',
            range=(0, 0.01),
            domain=[0, 0.45],
            anchor='x2',
            ),
        xaxis3=dict(
            title='frequency (Hz)',
            type='log',
            range=(log10(1), log10(200)),
            domain=[0.55, 1],
            anchor='y3',
            ),
        yaxis3=dict(
            title='amplitude (μV²/Hz)',
            type='log',
            range=(log10(0.01), log10(1000)),
            domain=[0, 0.45],
            anchor='x3',
            ),
        )

    fig = go.Figure(data=[trace1, trace2, trace3], layout=layout)
    return fig
