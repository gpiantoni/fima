from wonambi import Dataset
from wonambi.datatype import Data
from wonambi.trans import montage, frequency
from numpy import arange, array, histogram, log10, empty, copy, isnan
import plotly.graph_objects as go


from .read import select_events
from ..viz import to_div
from ..parameters import P

AUTOMATIC = False

def plot_raw_overview(filename):
    event_type = 'all'

    if filename.name.startswith('sub-drouwen'):
        CHANS = [f'IH0{x + 1}' for x in range(8)]
    elif filename.name.startswith('sub-itens'):
        CHANS = [f'C0{x + 1}' for x in range(8)]
    elif filename.name.startswith('sub-lemmer'):
        CHANS = [f'IH{x + 1}' for x in range(8)]
    elif filename.name.startswith('sub-som705'):
        CHANS = [f'GA0{x + 1}' for x in range(8)]  # a bit random
    elif filename.name.startswith('sub-ommen'):
        CHANS = ['chan1', 'chan2']  # I dont 'understand why I cannot use 'chan64'
    elif filename.name.startswith('sub-vledder') or filename.name.startswith('sub-ommen'):
        CHANS = ['chan1', 'chan64']
    elif '_acq-blackrock_' in filename.name:
        CHANS = ['chan1', 'chan128']
    else:
        print('you need to specify reference channel for this test')
        return None, None

    d = Dataset(filename, bids=True)
    event_names, event_onsets = select_events(d, event_type)

    is_ecog = d.dataset.task.channels.tsv['type'] == 'ECOG'
    is_seeg = d.dataset.task.channels.tsv['type'] == 'SEEG'
    chans = array(d.header['chan_name'])[is_ecog | is_seeg]
    data = d.read_data(begtime=event_onsets[0], endtime=event_onsets[-1], chan=list(chans))
    data.data[0][isnan(data.data[0])] = 0  # ignore nan

    data = montage(data, ref_chan=CHANS)
    freq = frequency(data, taper='hann', duration=2, overlap=0.5)

    hist = make_histogram(data, max=250, step=10)
    divs = []
    fig = plot_hist(hist)
    divs.append(to_div(fig))

    bad_chans = None

    if AUTOMATIC:
        from sklearn.covariance import EllipticEnvelope

        algorithm = EllipticEnvelope(
            contamination=P['data_quality']['histogram']['contamination'])
        prediction = algorithm.fit(hist.data[0]).predict(hist.data[0])
        new_bad_chans = data.chan[0][prediction == -1]
        print('bad channels with histogram / elliptic envelope: ' + ', '.join(new_bad_chans))
        bad_chans = set(new_bad_chans)

        fig = plot_outliers(
            hist.chan[0],
            algorithm.dist_,
            prediction,
            yaxis_title='distance',
            yaxis_type='log')
        divs.append(to_div(fig))

    fig = plot_freq(freq)
    divs.append(to_div(fig))

    if AUTOMATIC:
        from sklearn.neighbors import LocalOutlierFactor

        algorithm = LocalOutlierFactor(
            n_neighbors=P['data_quality']['spectrum']['n_neighbors'])
        prediction = algorithm.fit_predict(freq.data[0])

        new_bad_chans = data.chan[0][prediction == -1]
        print('bad channels with spectrum / local outlier factor: ' + ', '.join(new_bad_chans))
        bad_chans |= set(new_bad_chans)
        fig = plot_outliers(
            freq.chan[0],
            algorithm.negative_outlier_factor_,
            prediction,
            yaxis_title='distance',
            yaxis_type='linear')
        divs.append(to_div(fig))

        # we use again the reference channel. Ref channel was handpicked but it might have a weird spectrum
        bad_chans -= set(CHANS)

    return bad_chans, divs


def plot_hist(hist):
    fig = go.Figure(
        go.Heatmap(
            y=hist.bins[0],
            z=hist(trial=0).T,
            zmin=0,
            zmax=1,
            colorscale='YlOrRd',
        ),
        layout=go.Layout(
            xaxis=dict(
                title='channels',
                tickmode='array',
                tickvals=arange(hist.number_of('chan')[0]),
                ticktext=hist.chan[0],
            ),
            yaxis=dict(
                title='voltage bins',
            ),
            ),
        )
    return fig


def plot_freq(freq):
    fig = go.Figure(
        go.Heatmap(
            y=freq.freq[0],
            z=10 * log10(freq.data[0].T),
            colorscale='jet',
        ),
        layout=go.Layout(
            xaxis=dict(
                title='channels',
                tickmode='array',
                tickvals=arange(freq.number_of('chan')[0]),
                ticktext=freq.chan[0],
            ),
            yaxis=dict(
                title='frequency (Hz)',
                type='log',
                range=(log10(1), log10(200)),
            ),
            ),
        )
    return fig


def make_histogram(data, max=250, step=10):
    output = Data()
    output.axis['chan'] = copy(data.axis['chan'])
    output.axis['bins'] = empty(data.number_of('trial'), dtype='O')
    output.data = empty(data.number_of('trial'), dtype='O')

    bins = arange(-max, max + step, step)

    X = empty((data.number_of('chan')[0], len(bins) - 1))
    for i, chan in enumerate(data.chan[0]):
        v, h = histogram(
            data(trial=0, chan=chan),
            bins=bins,
            density=True)
        X[i, :] = v * 100

    output.axis['bins'][0] = bins[:-1] + step / 2
    output.data[0] = X

    return output


def plot_outliers(chans, metric, prediction, yaxis_title, yaxis_type='linear'):
    tickvals = arange(chans.shape[0])

    fig = go.Figure([
        go.Scatter(
            x=tickvals[prediction == 1],
            y=metric[prediction == 1],
            name='inlier',
            mode='markers',
            marker=dict(
                color='black',
                ),
            ),
        go.Scatter(
            x=tickvals[prediction == -1],
            y=metric[prediction == -1],
            name='outlier',
            mode='markers',
            marker=dict(
                color='red',
                ),
            ),
        ],
        layout=go.Layout(
            xaxis=dict(
                title='channels',
                tickmode='array',
                tickvals=tickvals,
                ticktext=chans,
                range=(0, len(chans)),
                ),
            yaxis=dict(
                title=yaxis_title,
                type=yaxis_type,
                ),
            ),
        )
    return fig
