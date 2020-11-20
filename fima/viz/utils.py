from logging import getLogger

from numpy import isnan, array, where
from plotly.offline import plot, get_plotlyjs
from scipy.stats import ttest_rel
from wonambi.trans import select

from ..parameters import FINGER_COLOR, MOVEMENT_SYMBOL_DATA, MOVEMENT_SYMBOL_MODEL

lg = getLogger(__name__)


def get_color_symbol(names):
    """Get the appropriate color and symbol for each condition

    Parameters
    ----------
    names : list of str
        list of conditions

    Returns
    -------
    list of str
        list of colors
    list of str
        list of symbols for the data
    list of str
        list of symbols for the model estimates
    """
    color = []
    symbol_data = []
    symbol_model = []

    for m in names:
        finger, action = m.split()
        color.append(FINGER_COLOR[finger])
        symbol_data.append(MOVEMENT_SYMBOL_DATA[action])
        symbol_model.append(MOVEMENT_SYMBOL_MODEL[action])

    return color, symbol_data, symbol_model


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
             <script type="text/javascript">{plotlyjs}</script>
         </head>
         <body>
            {div}
         </body>
     </html>
    '''.format(plotlyjs=get_plotlyjs(), div='\n'.join(divs))

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


def select_significant_channels(data, onsets, threshold=0.05):
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

    i_significant = (res.pvalue <= 0.05)
    significant_chan = data.chan[0][i_significant]

    out = []
    for i in where(i_significant)[0]:
        out.append(f'{data.chan[0][i]:<6}:{res.pvalue[i]: .3f}')
    lg.debug('; '.join(out))

    return significant_chan
