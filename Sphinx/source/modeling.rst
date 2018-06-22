Modeling
========

Re-Route Instances
------------------

Select as many instances as you want and execute the command. It will ask you for a new mesh source. Pick one from the dropdown or put in a new name and an empty mesh will be created as new source.

De-Instance
-----------

Select as many instances as you want and execute the command. You will get shiny new normal meshes.

Select by Size/Volume
---------------------

This command enables you to clean up a dense (CAD) scene very quickly.
Often one does not need the tiny screws that come with a car model. With this they are easily filtered out.

Allows you to select all items in a scene based on different sizing methods.

* Volume: If the mesh bounding box is smaller then the entered cubic volume.
* Area (X/Z): If the mesh bounding box  X/Y area is smaller then the entered value.
* Shortest Side: If the mesh's shortest side is smaller then the entered value.
* Longest Side: If the mesh's longest side is smaller then the entered value.

The invert checkbox simply inverts the selection, so everything that is larger then the entered value gets selected.

The instances checkbox allows you to either select or don't select instances.