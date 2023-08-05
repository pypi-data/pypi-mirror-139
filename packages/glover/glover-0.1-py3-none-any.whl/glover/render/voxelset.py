from ._factory import scene_component
from vispy.color import ColorArray
from vispy.visuals.transforms import MatrixTransform

def render_voxelset(voxelset, **kwargs):
    components = []
    color = (1,1,1,0)
    edge_color = 'white'
    for voxel, size in zip(
        voxelset.as_spatial_coords(copy=False),
        voxelset.get_size_matrix(copy=False),
    ):
        arguments = _make_argument_factory(size, color, edge_color)
        post_init = _make_postinit_factory(voxel)
        components.append(scene_component("Box", arguments, post_init))
    return components

def _make_argument_factory(size, color, edge_color):
    def arguments(scene, view):
        return (*size,), dict(
            parent=view.scene,
            color=color,
            edge_color=edge_color,
        )

    return arguments

def _make_postinit_factory(coords):
    def post_init(box):
        box.transform = MatrixTransform()
        print("DOING POST INIT TRANSLATION", coords)
        box.transform.translate(coords)

    return post_init
