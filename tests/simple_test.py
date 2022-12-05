import numpy as np

import rpad.visualize_3d.plots as vpl


def test_pc():
    pc = np.random.random((1000, 3))
    vpl.pointcloud_fig(pc)


def test_seg():
    pc = np.random.random((1000, 3))
    labels = np.random.randint(4, size=(1000,))
    labelmap = {0: "this", 1: "is", 2: "a", 3: "label"}
    vpl.segmentation_fig(pc, labels, labelmap=labelmap)


def test_flow():
    pc = np.random.random((1000, 3))
    flows = np.random.random((1000, 3))
    vpl.flow_fig(pc, flows, flowscale=0.1)
