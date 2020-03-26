from .tfr_chan import plot_tfr
from .tfr_time import plot_tfr_time
from .surf import plot_surf

from plotly.offline import plot, get_plotlyjs


def to_div(fig):
    return plot(fig, output_type='div', show_link=False, include_plotlyjs=False)


def to_html(divs, filename):
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
