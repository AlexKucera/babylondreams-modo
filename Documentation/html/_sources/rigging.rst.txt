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