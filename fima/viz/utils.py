from plotly.offline import plot, get_plotlyjs

from ..parameters import P, MOVEMENT_SYMBOL_DATA, MOVEMENT_SYMBOL_MODEL
from ..utils import get_color_for_val


FINGER_COLOR = {
    'thumb': get_color_for_val(4, P['viz']['colorscale'], -1, 5),
    'index': get_color_for_val(3, P['viz']['colorscale'], -1, 5),
    'middle': get_color_for_val(2, P['viz']['colorscale'], -1, 5),
    'ring': get_color_for_val(1, P['viz']['colorscale'], -1, 5),
    'little': get_color_for_val(0, P['viz']['colorscale'], -1, 5),
}


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

    with open(filename, 'w') as f:
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
