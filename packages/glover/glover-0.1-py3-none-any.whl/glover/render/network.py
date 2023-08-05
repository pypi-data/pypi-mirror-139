from ._factory import scene_component
from vispy.color import ColorArray

def render_network(network, **kwargs):
    components = []
    for cell_type in network.get_cell_types():
        ps = network.get_placement_set(cell_type)
        pos = ps.load_positions() / 1000
        color = "white"
        arguments = _make_argument_factory(pos, color)
        components.append(scene_component("Markers", arguments))

    return components

def _make_argument_factory(pos, color):
    def arguments(scene, view):
        return (), dict(
            pos=pos,
            size=2.5, parent=view.scene,
            edge_color=ColorArray(color),
            face_color=ColorArray(color)
        )

    return arguments
