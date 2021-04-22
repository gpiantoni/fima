from bidso.utils import read_tsv
import plotly.graph_objects as go
from numpy import sign

from ..names import name
from ..read import load

from .surf import AXIS


def plot_brain_regions(parameters, ieeg_file, region_type):
    """
    region_type can be one of:
    'aparc.a2009s',
    'aparc.DKTatlas',
    'BA_exvivo',
    'BA_exvivo.thresh',
    """
    brainregions_file = name(parameters, 'brainregions', ieeg_file)
    electrodes = read_tsv(brainregions_file)
    pial = load('surface', parameters, ieeg_file)
    annot = load(region_type, parameters, ieeg_file)

    colors = []
    labels = []
    for elec in electrodes:
        region = elec[region_type]
        labels.append(f'{elec["name"]} = {region}')
        colors.append(annot['regions']['colors'][region])

    # to normalize plotly
    n_regions = len(annot['regions']['names'])

    right_or_left = sign((electrodes['x'] > 0).sum() / electrodes.shape[0] - .5)

    traces = [
        go.Mesh3d(
            x=pial.vert[:, 0],
            y=pial.vert[:, 1],
            z=pial.vert[:, 2],
            i=pial.tri[:, 0],
            j=pial.tri[:, 1],
            k=pial.tri[:, 2],
            intensity=annot['regions']['values'] / n_regions,
            colorscale=annot['regions']['colorscale'],
            hoverinfo='skip',
            showscale=False,
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
                y=0,
                z=-1,
                ),
            ),
        go.Scatter3d(
            x=electrodes['x'],
            y=electrodes['y'],
            z=electrodes['z'],
            text=labels,
            mode='markers',
            hoverinfo='text',
            marker=dict(
                size=5,
                color=colors,
            ),
        )
        ]

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
