Release Notes
=============

1.1.0 - 2017-08-30
------------------
New:

* Added Camera Bake and Export to FBX
* Added Overscan Rendering
* Added Create Material Outputs
* Added Clear Master Log
* Added Version Up
* Added Version Up with Comment
* Added Headless Batch Creator options (Preview, etc.)

Fixed:

* Animation Transfer:
    * Don't use item names as IDs anymore as they were causing unicode issues with JSON export
    * Fixed JSON save path for windows

1.0.9 - 2017-08-01
------------------

New:

* GL Recording now has toggles for AVP Shadows and AVP Ambient Occlusion
* Deinstanced Meshes now have their BBox turned off
* Animation Tagging, Save and Load workflow

1.0.8 - 2017-07-03
------------------
New:

* Debugging routines and a snazzy runtime clock
* First stab at Blend Hierarchy Split Passes
* Update Render Paths
* Open Render Output Folder
* Added Headless Batch Creator
* Added batch event logger

Fixed:

* GL Capture was trying to save JPGs, but modo hardcodes TGA files resulting in seeminlgy corrupted image sequences (they just had the wrong file extension). This has been fixed now.
* Fixed GL Capture shading style not being applied correctly
* GL Capture now uses scene range instead of render range
* Instance re-route works again for newer versions of modo

1.0.7 - 2017-03-08
------------------

New:

* Added auto-naming, scene range and overwrite to gl capture
* bd_pipeline integration
* Added Instance BBox toggler

1.0.6 - 2017-03-03
------------------

Added:

* Disable BBox during GL Capture
* Added bunch of display defaults to GL Recording
* Added Replicator switch to GL Recording
* Added RayGL to GL Recording
* Added GL BG Style switch to GL Recording

1.0.5 - 2017-03-02
------------------

Added:

* GL Capture

Fixed:

* Major refactoring of the instance center script. Removes all cruft and makes it as fast as possible with the TD SDK
* GL Recording now respects animated render camera

1.0.4 - 2017-02-27
------------------

Added:

* Instance source dropdown shows actual names now
* Re-route instances version check. Since the script only work in modo < 10.2v1 we now check the version and pop up a warning if the script runs on an unsupported version.
* Instance Source Center Adjust. Seems to work well on fresh CAD imports. Does not seem to work at all on manually created instance hierarchies. Bummer.

Fixed:

* No more initial key on the blend tools
* Only one warning instead of one per item when creating a blend
* Fixed Blend Preference Default

1.0.3 - 2017-02-24
------------------

Added:

* First working verison of instance swapper. Only works in 10.2v1 for now. newer versions break the way this works. Already bugged it.

1.0.2 - 2017-02-22
------------------

Added:

* Added Dissolve Type Preference
* Fix orphans

Fixed:

* De-instance fixed. Now uses lx.eval to restore the proper un-instanced type instead of simply disconnecting the source item.


1.0.1 - 2017-02-21
------------------

Fixed version limit in CFG

1.0.0 - 2017-02-21
------------------

Added:

* GL Capture from old kit for now
* De-Instance
* Dissolve Hierarchy
* Per Item Transfer Anim

Initial Commit - 2017-02-15
---------------------------

Initial Commit based on a fresh Good Kitty setup.

https://github.com/adamohern/good_kitty


