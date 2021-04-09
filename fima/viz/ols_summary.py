import plotly.graph_objects as go

from numpy import arange, sqrt


from ..utils import get_color_for_val


def plot_ols_params(df, param, region_type, yaxis_name=''):

    SUMMARY = {}
    for region in sorted(df['channel'][region_type].unique()):
        if region == 'unknown':
            continue
        x = df[param[0]][param[1]][df['channel'][region_type] == region]
        SUMMARY[region] = [x.mean(), x.std() / sqrt(len(x))]

    fig = go.Figure([
        go.Scatter(
            mode='markers',
            y=[x[0] for x in SUMMARY.values()],
            marker=dict(
                color='black'),
            error_y=dict(
                type='data',
                array=[x[1] for x in SUMMARY.values()],
            )
        )],
        layout=go.Layout(
            title=dict(
                text=' / '.join(param),
                ),
            xaxis=dict(
                title=dict(
                    text='brain region',
                    ),
                tickmode='array',
                tickvals=arange(len(SUMMARY)),
                ticktext=list(SUMMARY.keys()),
                ),
            yaxis=dict(
                title=dict(
                    text=yaxis_name)
                ),
            )
        )

    return fig

def plot_ols_rsquared(df, region_type):

    rsquared_levels = arange(0, 1, .1)
    BARS = {}
    for region in sorted(df['channel'][region_type].unique()):

        vals = []
        for i in rsquared_levels:
            vals.append(
                len(df[(df['channel'][region_type] == region) & (i <= df['estimate']['rsquared']) & (df['estimate']['rsquared'] <= (i + 0.1))]))
        BARS[region] = vals

    n_levels = len(BARS[df['channel'][region_type][0]])
    bar_plots = []
    for i in range(n_levels):
        bar_plots.append(
            go.Bar(
                x=list(BARS.keys()),
                y=[x[i] for x in BARS.values()],
                name=f'{rsquared_levels[i]:0.1f} - {rsquared_levels[i]+0.1:0.1f}',
                marker=dict(
                    color=get_color_for_val(i, 'Hot', 0, n_levels - 3),
                ),
            ),
        )

    fig = go.Figure(
        bar_plots,
        layout=go.Layout(
            barmode='stack',
            title=dict(
                text='R-Squares'
                ),
            xaxis=dict(
                title=dict(
                    text='brain region',)
                ),
            yaxis=dict(
                title=dict(
                    text='# channels',)
                ),
        ))

    return fig
