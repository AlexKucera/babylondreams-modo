Rigging
=======

Re-Route Instances
------------------

see :doc:`modeling`

De-Instance
-----------

see :doc:`modeling`

Instance Source Center Adjust
-----------------------------

Allows adjustments to the center of an object that is the source of a bunch of instances without the instances flying off in all directions.

The basic idea is to save the source world position, then adjust the center, then get the new world position and calculate the offset. Then apply this offset to the transform of all the instances.

Seems to work well on fresh CAD imports. Does not seem to work at all on manually created instance hierarchies for now. Bummer.

Parent Selection to Group
-------------------------

One more parent option that helps you to sort through and clean up dense scenes. Select a bunch of items and run this in one of two ways.

1. Select a bunch of items and as last item add the group you want to parent your items to. Then right click the group/seletion and in the Parent submenu there is a new entry "Parent Selected to Group".

2. Select a bunch of items and run the command via the button in the rigging section of this kit. It will pop up a dialog that allows you to name and create a new group all items will be parented below.

There is one option for this dialog. Parent in Place or not. Parent in Place keeps the items transforms intact, meaning your items won't jump around when they get thrown into the new group. This is potentially slower though on large scenes. If spped is more important then keeping the item locations, then untick this box and large scenes should see a speed improvement.