import plotly.graph_objs as go


from ..parameters import P


def plot():
    divs = []
    for i_chan, chan in enumerate(tf_cht.chan[0]):
        fig = plot_single_trials_per_cond(t, X[i_chan, :, :], chan)
        divs.append(to_div(fig))

    to_html(divs, Path('/home/gio/projects/finger_mapping/results/example.html'))


def plot_single_trials_per_cond(t, X, chan=''):
    """Plot single traces for all the trials in one condition

    Parameters
    ----------
    t : (n, ) array
        vector with time information
    X : (n, trl) array
        vector with data (time X trials)
    chan : str
        name of channel

    Returns
    -------
    instance of Figure
    """
    n_trl = X.shape[1]

    traces = []
    for i_trl in range(n_trl):
        traces.append(
            go.Scatter(
                x=t,
                y=X[:, i_trl],
                line=dict(
                    color='black'),
            )
        )

    fig = go.Figure(
        data=traces,
        layout=go.Layout(
            showlegend=False,
            title=dict(
                text=chan,
            ),
            xaxis=dict(
                title='time (s)',
            ),
            yaxis=dict(
                title='change from baseline ({})'.format(P['spectrum']['baseline']['type']),
                range=(
                    -1 * P['viz']['tfr_mean']['max'],
                    P['viz']['tfr_mean']['max'],
                    ),
            ))
        )

    return fig


def plot_mean_and_slope(t, X_mean_chan, est):
    """Plot mean across electrodes and the slope used for estimation
    """
    t0 = t[est['i_zero']:est['i_max']]
    x0 = t0 * est['b'] + est['a']

    fig = go.Figure(data=[
        go.Scatter(
            x=t,
            y=X_mean_chan,
            line=dict(
                color='black'),
            ),
        go.Scatter(
            x=t0,
            y=x0,
            mode='lines+markers',
            line=dict(
                color='red'),
            )
        ],
        layout=go.Layout(
            showlegend=False,
            title=dict(
                text=est['chan'],
                ),
            xaxis=dict(
                title='time (s)',
                ),
            yaxis=dict(
                title='change from baseline ({})'.format(P['spectrum']['baseline']['type']),
                range=(
                    -1 * P['viz']['tfr_mean']['max'],
                    P['viz']['tfr_mean']['max'],
                    ),
                ))
        )

    return fig
