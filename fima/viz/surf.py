import plotly.graph_objects as go
from numpy import sign, NaN


AXIS = dict(
    title="",
    visible=False,
    zeroline=False,
    showline=False,
    showticklabels=False,
    showgrid=False,
    )


def plot_surf(parameters, data, elec, pial=None, info='activity', clim=None, colorscale=None):
    if colorscale is None:
        colorscale = parameters['viz']['colorscale']

    if info == 'finger':
        colorlim = (-1, 5)
        colorbar = dict(
            title="Main Finger",
            titleside="top",
            tickmode="array",
            tickvals=[0, 1, 2, 3, 4],
            ticktext=["Little", 'Ring', 'Middle', 'Index', 'Thumb'],
            ticks="outside"
            )

    else:
        colorbar = dict(
            title=info,
            titleside="top",
            ticks="outside"
            )

        if info == 'rsquared':
            colorlim = (0, 0.70)
            colorscale = 'Hot'

        elif info == 'open_v_close':
            colorlim = (0, 1)

        elif info == 'tstat':
            colorlim = (-10, 10)

        elif clim is not None:
            colorlim = clim

        else:
            colorlim = (
                parameters['viz']['tfr_mean']['max'] * -1,
                parameters['viz']['tfr_mean']['max'],
                )

    right_or_left = sign((elec['x'] > 0).sum() / elec.shape[0] - .5)

    traces = []
    if pial is not None:
        pial_mesh = go.Mesh3d(
            x=pial.vert[:, 0],
            y=pial.vert[:, 1],
            z=pial.vert[:, 2],
            i=pial.tri[:, 0],
            j=pial.tri[:, 1],
            k=pial.tri[:, 2],
            color='pink',
            hoverinfo='skip',
            flatshading=False,
            lighting=dict(
                ambient=0.18,
                diffuse=1,
                fresnel=0.1,
                specular=1,
                roughness=0.1,
                ),
            lightposition=dict(
                x=0,
                y=0.5,
                z=-1,
                ),
            )
        traces.append(pial_mesh)

    values = []
    labels = []
    for label in elec['name']:
        if label in data.chan[0]:
            v = data(trial=0, chan=label).tolist()
        else:
            v = NaN
        labels.append(f'{label} = {v:0.3f}')
        values.append(v)

    traces.append(
        go.Scatter3d(
            x=elec['x'], # + right_or_left,
            y=elec['y'],
            z=elec['z'], # + .5,
            text=labels,
            mode='markers',
            hoverinfo='text',
            marker=dict(
                size=5,
                color=values,
                colorscale=colorscale,
                showscale=True,
                cmin=colorlim[0],
                cmax=colorlim[1],
                colorbar=colorbar,
            ),
        )
        )

    fig = go.Figure(
        data=traces,
        layout=go.Layout(
            scene=dict(
                xaxis=AXIS,
                yaxis=AXIS,
                zaxis=AXIS,
                camera=dict(
                    eye=dict(
                        x=right_or_left,
                        y=0,
                        z=0.5,
                    ),
                    projection=dict(
                        type='orthographic',
                    ),
                    ),
                ),
            ),
        )

    return fig
