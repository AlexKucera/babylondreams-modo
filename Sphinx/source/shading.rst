Shading
=======

Fix Orphans
-----------

Finds any Shader Tree items that have become unparented and parents them back to the Shader Tree.

Create Per Material RenderOutputs
---------------------------------

Adds an Alpha and a Final Color output to any selected Material Group. The outputs will be named with the name of the Material Group plus the output type, e.g.: red_metal_alpha.

Blend Hierarchy
---------------

The command creates an easily animateable setup to dissolve/fade a hierarchy of items. By selecting the parent item and running the command a few things happen:

    1. A group with the whole item hierarchy gets created
    2. A shader setup gets created and put at the top of the shader tree
    3. The shader setup gets linked to the group

To animate the blend/dissolve you open the corresponding Shader group and animate the constant's value.

Blend Arbitrary
---------------

Same as Blend Hierarchy, but allows blending of completely unrelated items in the scene.

BBox Instance Toggle
--------------------

Toggles the bounding box display of all instances of a given selection (or all instances in the scene if nothing is selected).