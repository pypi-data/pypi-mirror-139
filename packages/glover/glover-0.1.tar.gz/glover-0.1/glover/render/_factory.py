from vispy import scene

def scene_component(visual, argument_factory, post_init=None):
    def factory(view):
        # Get the visual component
        component_cls = getattr(scene.visuals, visual)
        # Produce the (keyword) arguments from the argument factory
        args, kwargs = argument_factory(scene, view)
        # Declare the component to the scene
        component = component_cls(*args, **kwargs)
        if post_init is not None:
            post_init(component)

    return factory
