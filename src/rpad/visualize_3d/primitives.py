from typing import Any, Dict, Optional, Sequence, Tuple, Union

import numpy as np
import numpy.typing as npt
from plotly import graph_objects as go


def pointcloud(
    pos: npt.ArrayLike,
    downsample=5,
    colors: Optional[Union[Sequence[Tuple[int, int, int]], Sequence[str]]] = None,
    scene="scene",
    name=None,
    size=3,
    colorbar=False,
) -> go.Scatter3d:
    pos = np.array(pos)

    marker_dict: Dict[str, Any] = {"size": size}
    if colors is not None:
        if isinstance(colors[0], str):
            cs = colors
        else:
            cs = [f"rgb({r}, {g}, {b})" for r, g, b in colors]  # type: ignore
        marker_dict["color"] = cs[::downsample]

        if colorbar:
            marker_dict["colorbar"] = dict(thickness=20)

    return go.Scatter3d(
        x=pos[::downsample, 0],
        y=pos[::downsample, 1],
        z=pos[::downsample, 2],
        mode="markers",
        marker=marker_dict,
        scene=scene,
        name=name,
    )


def sphere(x, y, z, r, opacity, color, scene="scene"):
    phi = np.linspace(0, 2 * np.pi, 20)
    theta = np.linspace(-np.pi / 2, np.pi / 2, 20)
    phi, theta = np.meshgrid(phi, theta)

    xs = np.cos(theta) * np.sin(phi) * r + x
    ys = np.cos(theta) * np.cos(phi) * r + y
    zs = np.sin(theta) * r + z

    return go.Surface(
        x=xs,
        y=ys,
        z=zs,
        colorscale=[[0, color], [1, color]],
        opacity=opacity,
        showscale=False,
        scene=scene,
    )


def vector(x, y, z, u, v, w, color, scene="scene", name="vector"):
    return go.Scatter3d(
        x=[x, x + u],
        y=[y, y + v],
        z=[z, z + w],
        line=dict(color=color, width=10),
        scene=scene,
        name=name,
    )
