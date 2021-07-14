from logging import getLogger

from numpy import isnan, array, where
from plotly.offline import plot
from scipy.stats import ttest_rel
from wonambi.trans import select
from copy import deepcopy
from collections import Mapping


lg = getLogger(__name__)

FONT = dict(
    family='verdana',
    size=9.34,
    color='#000',
    )

TICKFONT = dict(
    family='verdana',
    size=9.34,
    color='#000',
    )

LIGHT_COLOR = 'lightGray'

LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    margin=dict(
        l=0,
        t=0,
        b=0,
        r=0,
        pad=0,
        ),
    title=dict(
        font=FONT,
        ),
    legend=dict(
        font=TICKFONT,
        ),
    xaxis=dict(
        title=dict(
            font=FONT,
            ),
        zerolinecolor='black',
        linecolor='black',
        gridcolor=LIGHT_COLOR,
        tickfont=TICKFONT,
        ),
    yaxis=dict(
        title=dict(
            font=FONT,
            ),
        zerolinecolor='black',
        linecolor='black',
        gridcolor=LIGHT_COLOR,
        tickfont=TICKFONT
        ),
    )


def to_div(fig):
    """Convert plotly FIG into an HTML div

    Parameters
    ----------
    fig : instance of plotly.Figure
        figure to convert

    Returns
    -------
    str
        html div, containing the figure as dynamic javascript plot
    """
    return plot(fig, output_type='div', show_link=False, include_plotlyjs=False)


def to_html(divs, filename):
    """Convert DIVs, obtained from 'to_div', into one HTML file

    Parameters
    ----------
    divs : list of divs
        list of the output of 'to_div'
    filename : path
        path of the file to write (extension should be .html). It overwrites if
        it exists
    """
    filename.parent.mkdir(exist_ok=True, parents=True)
    lg.debug(f'Saving {len(divs)} plots to {filename}')

    html = '''
        <html>
         <head>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
         </head>
         <body>
            {div}
         </body>
     </html>
    '''.format(div='\n'.join(divs))

    with filename.open('w') as f:
        f.write(html)


def to_png(fig, png_name):
    """Convert image to png directly

    Parameters
    ----------
    fig : instance of plotly.Figure
        figure to convert
    png_name : path
        path of the file to write (extension should be .png). It overwrites if
        it exists

    Notes
    -----
    It crashes easily, especially if it's called multiple times, because it relies
    on plotly calling an external function to do the actual plotting (orca)
    """
    fig = fig.update_layout(width=1600, height=900)
    png_name.parent.mkdir(exist_ok=True, parents=True)
    with png_name.open('wb') as f:
        f.write(fig.to_image('png'))


def select_significant_channels(data, onsets, threshold=0.0005):
    assert NotImplementedError
    """Select channels that show a significant difference between the period
    before onset and the period after the onset.

    Parameters
    ----------
    data : instance of wonambi.data
        continuous data (already converted to z-score or dB)
    onsets : array
        array of
    threshold : float
        p-value to consider it significant

    Returns
    -------
    list of str
        list of significant array
    """
    PRESTIM = 1
    POSTSTIM = 1
    v_pre = []
    v_post = []
    for on in onsets:
        d = select(data, time=(on - PRESTIM, on))
        v_pre.append(d(trial=0, trial_axis='trial000000').mean(axis=1))
        d = select(data, time=(on, on + POSTSTIM))
        v_post.append(d(trial=0, trial_axis='trial000000').mean(axis=1))

    v_pre = array(v_pre)
    v_post = array(v_post)

    artifact = isnan(v_pre[:, 0]) | isnan(v_post[:, 0])
    res = ttest_rel(v_post[~artifact, :], v_pre[~artifact, :], axis=0)

    i_significant = (res.pvalue <= threshold)
    significant_chan = data.chan[0][i_significant]

    out = []
    for i in where(i_significant)[0]:
        out.append(f'{data.chan[0][i]:<6}:{res.pvalue[i]: .3f}')
    lg.info('; '.join(out))

    return significant_chan


def merge(dict1, dict2):
    """Return a new dictionary by merging two dictionaries recursively.

    https://stackoverflow.com/a/43228384
    """
    result = deepcopy(dict1)

    for key, value in dict2.items():
        if isinstance(value, Mapping):
            result[key] = merge(result.get(key, {}), value)
        else:
            result[key] = deepcopy(dict2[key])

    return result
