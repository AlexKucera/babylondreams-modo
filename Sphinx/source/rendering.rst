Rendering
=========

Record GL
---------

see :doc:`animation`

Split Blends into Passes
------------------------

Still highly experimental and mostly broken.

It works in tandem with Blend Hierarchy (see :doc:`shading`). Analyzes a scene and splits it up into renderable passes/scenes.

Create Per Material RenderOutputs
---------------------------------

see :doc:`shading`


Adjust Overscan
---------------

Allows adjusting the overscan of a scene by specifying either a new resolution or a scaling factor. This will scale the render resolution and camera film back accordingly.

For a more technical explanation of Overscan Rendering see: https://www.pixelfondue.com/blog/2016/12/9/overscan-rendering

Update Render Paths
-------------------

Updates the render path of any render outputs that are enabled and have anything in the filename property (could just be "bla" or "path" as well as a valid path). The path will be updated to point at the render folder specified in the pipeline configuration file.

Headless Batch Creator
----------------------

Updates the render paths and writes all the files necessary for headless batch rendering into a folder called "_batch_ next to the scene file. It then either opens a commandline ready with the render command in the clipboard ready to go or fire off a background render.

It supports rendering with the normal bucket renderer as well as headless Preview rendering. However, at the moment headless Preview rendering does not support passes. The script will brute force turn off passes and render the plain scene.

Careful, the background render cannot be controlled once it has started. It is simply an UI-less process running in the background. Meaning no status output or any other control. If you want to kill it you need to use the OS' task manager.

Open Selected renderOutput's Folder
-----------------------------------

Select a render output and run the command and a Finder/Explorer window will open at the path the output writes to.