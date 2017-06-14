#python

import modo

scene = modo.Scene()

# Get a list of selected meshes and mesh instances.
meshes = filter(lambda i: i.type in ("meshInst", "mesh"), scene.selected)

# Pop the last one off the list; that's our top-most selection.
prototype = meshes.pop()

# We filter on just meshInst items.
for instance in filter(lambda i: i.type == "meshInst", meshes):

    # Disconnect any existing meshInst graph connections.
    for source in instance.itemGraph("meshInst").reverse():
        source.itemGraph("meshInst") << instance

    # Disconnect any existing source graph connections.
    # Note that the meshInst graph and the source graph go
    # in different directions. That's why we cache the
    # "sourceGraph" in advance.
    sourceGraph = instance.itemGraph("source")
    for source in sourceGraph.forward():
        sourceGraph << source

    # Connect new prototype. Again, notice how they go in
    # different directions.
    instance >> prototype.itemGraph("source")
    prototype >> instance.itemGraph("meshInst")
