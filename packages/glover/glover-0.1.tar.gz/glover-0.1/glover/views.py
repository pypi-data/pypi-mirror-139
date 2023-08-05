from vispy import scene

def network_view():
    canvas = scene.SceneCanvas(keys='interactive', show=True,bgcolor='black')
    view = canvas.central_widget.add_view()
    view.camera = 'fly'
    return view

def morphology_view():
    canvas = scene.SceneCanvas(keys='interactive', show=True,bgcolor='black')
    view = canvas.central_widget.add_view()
    view.camera = 'fly'

    return view

def voxelset_view():
    canvas = scene.SceneCanvas(keys='interactive', show=True,bgcolor='black')
    view = canvas.central_widget.add_view()
    view.camera = 'fly'

    return view
