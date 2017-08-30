Scripting
=========

Version Up Scene
----------------

Versions up the scene file. Tries to be smart about detecting the numbering. But generally it looks for a version of `_v000`, so an underscore, a *v* and some number.

If it cannot find a version string it will offer to start versioning the file.

For example::

    my_great_shot_v010.lxo becomes my_great_shot_v011.lxo
    my_great_shot.lxo becomes my_great_shot_v01.lxo
    my_great_shot_v4.lxo becomes my_great_shot_v5.lxo

Version Up Scene with Comment
-----------------------------

Same as version up, but asks for a short file comment. This will be appended to the file name.

The comment is sanitized (turns spaces into underscores, all letters into lowercase and keeps only letters and digits) so there are no invalid strings in the file name.

For example::

    my_great_shot_v010.lxo becomes my_great_shot_v010_awesome_comment.lxo

Clear Log
---------

Clears the Event Log witout any warning messages. Useful for development.

Fix Orphans
-----------
see :doc:`shading`

Docs
----

Opens this documentation.