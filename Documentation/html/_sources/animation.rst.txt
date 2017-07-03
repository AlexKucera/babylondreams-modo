Animation
=========

Record GL
---------

Allows opening an OpenGL window of defined dimensions for size accurate OpenGL Previews.

It allows you fine grained control over:

* what is visible
* render sizes (always based on on the Render items' render size)
* which camera to use (defaults to the Render Camera)
* Shading Style (with a bunch of customizations on Default and AVP to make GL capture as high fidelity as possible in the capture window)
* which background style to use
* RayGL (I personally have never used it, but heck it was a simple addition)
* Performance setting for replicator visibility (also hides and shows locators since replicator visibility is linked to locator visibility)
* an option to switch all meshes in the shot from bounding box to actual meshes for the duration of the capture
* Automatic render path and file naming based on project location (optimized for our internal pipeline, but can easily be generalized)
* Custom manual naming options in case the automatic naming does not cut it
* A switch to overwrite or version up old preview files
* Render range (by default dependent on the scene range (careful, this is different then the Render Range!!!))

Transfer Animation
------------------

Copy the animation from one selected item to another. It will copy all animated channels from the first object to the second object. Any channels that are missing on the second object will be listed at the end for manual fixing.

Please make sure you have Warning dialogs enabled in modo, otherwise the user won't get a popup dialog.