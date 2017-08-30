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

Bake Camera Hierarchy and Export as FBX
---------------------------------------

Bakes a camera animation of any complexity down to a simple camera path and exports it as FBX next to the scene file's location.

* Select any camera
* Run the command
* It will pop up two bake range requests that you can just confirm (or adjust if needed)
* After it is done baking it will export the FBX and open the folder in Explorer/Finder.

Transfer Animation (per Item)
-----------------------------

Copy the animation from one selected item to another. It will copy all animated channels from the first object to the second object. Any channels that are missing on the second object will be listed at the end for manual fixing.

Please make sure you have Warning dialogs enabled in modo, otherwise the user won't get a popup dialog.

Transfer Animation Hierarchy Workflow
-------------------------------------

This workflow consists of several steps and allows you to save out complete animation sets of a previously tagged hierarchy/rig.

* The first step is to prepare the asset for this workflow. This has to happen before any animation takes place!
* Select the asset (the topmost group or all individual items of the asset/rig).
* Run "Tag Hierarchy for Animation Transfer" with the dropdown set to "Create/Update Missing Tags"
* Import your tagged asset into your animation scenes and animate to your heart's content.
* When you want to save out your animation, select the asset's topmost folder and run "Save Animation Hierarchy". This will save out the animation to a JSON file.
* This JSON file can then be applied to the asset in another scene or to an updated asset by selecting the asset's topmost folder and and running "Load and Apply Animation Hierarchy".