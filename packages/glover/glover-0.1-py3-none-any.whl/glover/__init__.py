"""
An Open**GL** Lay**over** library built on top of vispy for plotting BSB entities.
"""

__version__ = "0.1"

import bsb.core
import bsb.morphologies
import bsb.voxels
from .render import render_morphology, render_network, render_voxelset
from .views import morphology_view, network_view, voxelset_view
from vispy import app, scene
import functools


@functools.singledispatch
def view(view, *components, **kwargs):
    for component in components:
        component(view)

    app.run()

@view.register
def _(network: bsb.core.Scaffold, **kwargs):
    components = render_network(network, **kwargs)
    _view = network_view()
    return view(_view, *components)

@view.register
def _(morphology: bsb.morphologies.Morphology, **kwargs):
    components = render_morphology(morphology, **kwargs)
    _view = morphology_view()
    return view(_view, *components)

@view.register
def _(voxelset: bsb.voxels.VoxelSet, **kwargs):
    components = render_voxelset(voxelset, **kwargs)
    _view = voxelset_view()
    return view(_view, *components)
