import plotly.graph_objects as go

from numpy import arange, sqrt, abs, max, linspace, isnan, histogram, zeros, corrcoef

from .utils import to_div

from ..ols.summary import import_df_ols
from ..utils import get_color_for_val
from ..parameters import FINGERS


REGIONS = (
    'G_precentral',
    'G_postcentral',
    'G_parietal_sup',
    'G_parietal_inf-Supramar',
    )


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


def plot_ols_prf(df, region_type, param):

    i = (df['estimate']['rsquared'] >= 0.1)
    df1 = df[i]
    region_type = 'brainregion'

    x = df1['flexext']['diff']
    absmax = max(abs(x))
    bins = linspace(-absmax, absmax, 30)

    divs = []
    for region in REGIONS:
        df_roi = df1.loc[df['channel'][region_type] == region]
        i_ext = (df_roi['estimate']['rsquared'] >= 0.1) & (df_roi['extension']['rsquared'] >= 0.9)
        i_flex = (df_roi['estimate']['rsquared'] >= 0.1) & (df_roi['flexion']['rsquared'] >= 0.9)

        if param == 'finger':
            bins = linspace(-1.5, 5.5, 15)
        elif param == 'spread':
            bins = linspace(0, 5, 20)

        fig = go.Figure(data=[
            make_bars(df_roi[i_ext]['extension'][param], bins, 'extension'),
            make_bars(df_roi[i_flex]['flexion'][param], bins, 'flexion'),
            ],
            layout=go.Layout(
                title=dict(
                    text=region),
            ))
        divs.append(to_div(fig))

    return divs


def plot_ols_flexext(df, region_type):

    i = (df['estimate']['rsquared'] >= 0.1)
    df1 = df[i]
    region_type = 'brainregion'

    x = df1['flexext']['diff']
    absmax = max(abs(x))
    bins = linspace(-absmax, absmax, 30)

    divs = []
    for region in REGIONS:
        df_roi = df1.loc[df['channel'][region_type] == region]
        fig = go.Figure(
            data=[
                make_bars(df_roi['flexext']['diff'], bins),
                ],
            layout=go.Layout(
                title=dict(
                    text=region),
                bargap=0,
            ))
        divs.append(to_div(fig))

    return divs


def make_bars(x, bins, name=''):
    x = x[~isnan(x)]
    [hist, edges] = histogram(x, bins=bins)

    trace = go.Bar(
        x=edges[:-1] + (edges[1] - edges[0]) / 2,
        y=hist,
        name=name,
        )
    return trace


def plot_fingerfriends(parameters):

    df_ols = import_df_ols(parameters)
    i = df_ols['rsquared'] > 0.2
    df = df_ols[i]

    divs = []
    for region in REGIONS:
        for MOVEMENT in ('flexion', 'extension'):

            cc = zeros((5, 5))
            for i0, f0 in enumerate(FINGERS):
                for i1, f1 in enumerate(FINGERS):
                    cc[i0, i1] = corrcoef(df[f'{f0} {MOVEMENT}'], df[f'{f1} {MOVEMENT}'])[0, 1]
                    fig = go.Figure(
                        data=[
                            go.Heatmap(
                                z=cc,
                                zmin=0,
                                zmax=1,
                                colorscale='Hot',
                            ),
                        ],
                        layout=go.Layout(
                            title=dict(
                                text=region + ' ' + MOVEMENT),
                            yaxis=dict(
                                autorange='reversed')))

            divs.append(to_div(fig))

    return divs
