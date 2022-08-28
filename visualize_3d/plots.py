from typing import Dict, Optional, Sequence

import numpy as np
import numpy.typing as npt
import plotly.colors as pc
import plotly.graph_objects as go

from visualize_3d.primitives import pointcloud


def _3d_scene(data: npt.ArrayLike) -> Dict:
    """Create a plotly 3D scene dictionary that gives you a big cube, so aspect ratio is preserved"""
    # Create a 3D scene which is a cube w/ equal aspect ratio and fits all the data.
    data = np.array(data)

    assert data.shape[1] == 3
    # Find the ranges for visualizing.
    mean = data.mean(axis=0)
    max_x = np.abs(data[:, 0] - mean[0]).max()
    max_y = np.abs(data[:, 1] - mean[1]).max()
    max_z = np.abs(data[:, 2] - mean[2]).max()
    all_max = max(max(max_x, max_y), max_z)
    scene = dict(
        xaxis=dict(nticks=10, range=[mean[0] - all_max, mean[0] + all_max]),
        yaxis=dict(nticks=10, range=[mean[1] - all_max, mean[1] + all_max]),
        zaxis=dict(nticks=10, range=[mean[2] - all_max, mean[2] + all_max]),
        aspectratio=dict(x=1, y=1, z=1),
    )
    return scene


def _segmentation_traces(
    data: npt.ArrayLike,
    labels: npt.ArrayLike,
    labelmap=None,
    scene="scene",
    sizes=None,
):
    data = np.array(data)
    labels = np.array(labels)

    # Colormap.
    colors = np.array(pc.qualitative.Alphabet)

    # Keep track of all the traces.
    traces = []

    for label in np.unique(labels):
        subset = data[np.where(labels == label)]
        color = colors[label % len(colors)]
        if sizes is None:
            subset_sizes = 4
        else:
            subset_sizes = sizes[np.where(labels == label)]
        if labelmap is not None:
            legend = labelmap[label]
        else:
            legend = str(label)
        traces.append(
            go.Scatter3d(
                mode="markers",
                marker={"size": subset_sizes, "color": color, "line": {"width": 0}},
                x=subset[:, 0],
                y=subset[:, 1],
                z=subset[:, 2],
                name=legend,
                scene=scene,
            )
        )
    return traces


def _flow_traces(
    start: npt.ArrayLike,
    flows: npt.ArrayLike,
    flowscale=0.05,
    scene="scene",
    flowcolor="red",
    name="flow",
):
    start = np.array(start)
    flows = np.array(flows)

    x_lines = list()
    y_lines = list()
    z_lines = list()

    # normalize flows:
    nonzero_flows = (flows == 0.0).all(axis=-1)
    nz_start = start[~nonzero_flows]
    nz_flows = flows[~nonzero_flows]

    nz_end = nz_start + nz_flows * flowscale

    # Evil hacky line segments in 3D.
    for i in range(len(nz_start)):
        x_lines.append(nz_start[i][0])
        y_lines.append(nz_start[i][1])
        z_lines.append(nz_start[i][2])
        x_lines.append(nz_end[i][0])
        y_lines.append(nz_end[i][1])
        z_lines.append(nz_end[i][2])
        x_lines.append(None)
        y_lines.append(None)
        z_lines.append(None)
    lines_trace = go.Scatter3d(
        x=x_lines,
        y=y_lines,
        z=z_lines,
        mode="lines",
        scene=scene,
        line=dict(color=flowcolor, width=10),
        name=name,
    )

    head_trace = go.Scatter3d(
        x=nz_end[:, 0],
        y=nz_end[:, 1],
        z=nz_end[:, 2],
        mode="markers",
        marker={"size": 3, "color": "darkred"},
        scene=scene,
        showlegend=False,
    )

    return [lines_trace, head_trace]


def pointcloud_fig(
    data: npt.ArrayLike, downsample=5, colors=None, size=3, colorbar=False
):
    """A simple point cloud figure. Nothing special."""
    fig = go.Figure()
    fig.add_trace(
        pointcloud(
            data, downsample, colors, scene="scene1", size=size, colorbar=colorbar
        )
    )
    fig.update_layout(scene1=_3d_scene(data), showlegend=False)
    return fig


def segmentation_fig(
    data: npt.ArrayLike,
    labels: npt.ArrayLike,
    labelmap: Optional[Dict[int, str]] = None,
    sizes: Optional[Sequence[int]] = None,
    fig: Optional[go.Figure] = None,
):
    """Creates a segmentation figure."""
    # Create a figure.
    if fig is None:
        fig = go.Figure()

    fig.add_traces(_segmentation_traces(data, labels, labelmap, "scene1", sizes))

    fig.update_layout(
        scene1=_3d_scene(data),
        showlegend=True,
        margin=dict(l=0, r=0, b=0, t=40),
        legend=dict(x=1.0, y=0.75),
    )

    return fig


def flow_fig(pos: npt.ArrayLike, flows: npt.ArrayLike, flowscale: float = 0.05):
    """Create a flow figure, which plots a point cloud, and then flow at each point."""
    f = go.Figure()
    f.add_trace(pointcloud(pos, downsample=1, scene="scene1"))
    ts = _flow_traces(pos, flows, flowscale=flowscale, scene="scene1")
    for t in ts:
        f.add_trace(t)
    f.update_layout(scene1=_3d_scene(pos))
    return f
