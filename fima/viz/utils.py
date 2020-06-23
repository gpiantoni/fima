from plotly.offline import plot, get_plotlyjs


def to_div(fig):
    return plot(fig, output_type='div', show_link=False, include_plotlyjs=False)


def to_html(divs, filename):
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
    fig = fig.update_layout(width=1600, height=900)
    png_name.parent.mkdir(exist_ok=True, parents=True)
    with png_name.open('wb') as f:
        f.write(fig.to_image('png'))
