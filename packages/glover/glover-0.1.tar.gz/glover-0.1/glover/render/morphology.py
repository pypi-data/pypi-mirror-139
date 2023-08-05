from ._factory import scene_component
from vispy.color import ColorArray
import numpy as np
import trimesh
from vispy.util.transforms import rotate

def render_morphology(morphology, **kwargs):
    mesh = morphology_to_mesh(morphology)
    arguments = _make_argument_factory(mesh)
    component = scene_component("Mesh", arguments)
    return [component]

def _make_argument_factory(mesh):
    def arguments(scene, view):
        return (), dict(
            vertices=mesh.vertices,
            faces=mesh.faces,
            parent=view.scene,
        )

    return arguments

def make_branch_mesh(points, radius=2.0, tube_points=4, vertex_colors=None, color='black'):
    # TODO: change segments to be a dictionary mapped on the type of segments
    # we're considering

    tangents, normals, binormals = _frenet_frames(points)
    segments = len(points) - 1
    # If single radius is given, convert it to list of radii
    try:
        itr = iter(radius)
    except TypeError:
        radius = [radius] * len(points)
    else:
        radius = [*radius]
    if len(radius) != len(points):
        raise ValueError('Length of radii list must match points.')

    # Get the positions of each vertex
    v = np.arange(tube_points, dtype=float) / tube_points * 2 * np.pi
    #verts = np.zeros((len(points), tube_points, 3))
    verts = np.array([p + (-1. * r * np.cos(v))[:, np.newaxis] * n
                    + (r * np.sin(v))[:, np.newaxis] * b
                    for p, n, b, r in zip(points, normals, binormals, radius)])

    # construct the mesh
    first_ind_set = [[i*tube_points + j, (i+1)*tube_points + j, i*tube_points + ((j+1) % tube_points)] for i in range(segments) for j in range(tube_points)]
    second_ind_set =[[(i+1)*tube_points + j, (i+1)*tube_points + ((j+1) % tube_points), i*tube_points + ((j+1) % tube_points)] for i in range(segments) for j in range(tube_points)]
    indices = [id_set for id_pair in zip(first_ind_set, second_ind_set) for id_set in id_pair]

    i = np.arange(segments, dtype=int)
    j = np.arange(tube_points, dtype=int)

    color = ColorArray(color)
    if vertex_colors is None:
        point_colors = np.resize(color.rgba,
                                 (len(points), 4))
        vertex_colors = np.repeat(point_colors, tube_points, axis=0)

    vertices = verts.reshape(verts.shape[0]*verts.shape[1], 3)
    indices = np.array(indices, dtype=np.uint32)

    return vertices, indices, vertex_colors


def _frenet_frames(points, closed=True):
    """Calculates and returns the tangents, normals and binormals for
    the tube.
    """
    tangents = np.zeros((len(points), 3))
    normals = np.zeros((len(points), 3))

    epsilon = 0.0001

    # Compute tangent vectors for each segment
    tangents = np.roll(points, -1, axis=0) - np.roll(points, 1, axis=0)
    tangents += epsilon
    if not closed:
        tangents[0] = points[1] - points[0]
        tangents[-1] = points[-1] - points[-2]
    mags = np.sqrt(np.sum(tangents * tangents, axis=1))
    tangents /= mags[:, np.newaxis]

    # Get initial normal and binormal
    t = np.abs(tangents[0])

    smallest = np.argmin(t)
    normal = np.zeros(3)
    normal[smallest] = 1.

    vec = np.cross(tangents[0], normal)
    normals[0] = np.cross(tangents[0], vec)

    # Compute normal and binormal vectors along the path
    for i in range(1, len(points)):
        normals[i] = normals[i-1]

        vec = np.cross(tangents[i-1], tangents[i])
        if np.linalg.norm(vec) > epsilon:
            vec /= np.linalg.norm(vec)
            theta = np.arccos(np.clip(tangents[i-1].dot(tangents[i]), -1, 1))
            normals[i] = rotate(-np.degrees(theta),
                                vec)[:3, :3].dot(normals[i])

    if closed:
        theta = np.arccos(np.clip(normals[0].dot(normals[-1]), -1, 1))
        theta /= len(points) - 1

        if tangents[0].dot(np.cross(normals[0], normals[-1])) > 0:
            theta *= -1.

        for i in range(1, len(points)):
            normals[i] = rotate(-np.degrees(theta*i),
                                tangents[i])[:3, :3].dot(normals[i])

    binormals = np.cross(tangents, normals)

    return tangents, normals, binormals



def morphology_to_mesh(morphology,
                       reduce_branches = False,
                       segment_radius = 1.0,
                       color="black",
                       soma_radius = None,
                       soma_opacity = 1.0,
                       use_last_soma_comp = 1.0,
                       offset = None):
    branches = morphology.get_branches()
    vertice_list = []
    faces_list = []
    for branch in branches:
        # Extracting the branch vertices and faces
        v,f, _ = make_branch_mesh(branch.as_matrix(with_radius=False), radius=branch.radii)

        # Merging the various branches submeshes in a whole neuron mesh
        vertice_list.append(v)
        faces_list.append(f)
        faces_offset = np.cumsum([v.shape[0] for v in vertice_list])
        faces_offset = np.insert(faces_offset, 0, 0)[:-1]

        vertices = np.vstack(vertice_list)
        faces = np.vstack([face + offset for face, offset in zip(faces_list, faces_offset)])
        mesh = trimesh.Trimesh(vertices, faces)

    return mesh
