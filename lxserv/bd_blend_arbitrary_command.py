#!/usr/bin/env python
# encoding: utf-8

"""

babylondreams - bd_command_blend_hierarchy

Release Notes:

    The command creates an easily animatable setup to dissolve/fade a hierarchy of items. By selecting the
    parent item and running the command a few things happen:

    1. A group with the whole item hierarchy gets created
    2. A shader setup gets created and put at the top of the shader tree
    3. The shader setup gets linked to the group

V0.1 Initial Release - 2017-02-20

"""

import babylondreams
import lx

from bd_tools import bd_blend_hierarchy


__author__ = "Alexander Kucera"
__copyright__ = "Copyright 2017, BabylonDreams - Alexander & Monika Kucera GbR"
__credits__ = ["Alexander Kucera"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Alexander Kucera"
__email__ = "a.kucera@babylondreams.de"
__status__ = "Development"


class CommandClass(babylondreams.CommanderClass):
    _commander_last_used = []

    def commander_arguments(self):
        return [
            {
                'name': 'blend_group_name',
                'datatype': 'string',
                'default': 'new_blend',
                'values_list_type': 'sPresetText'
            },
        ]

    def commander_execute(self, msg, flags):
        name = self.commander_arg_value(0)

        reload(bd_blend_hierarchy)
        bd_blend_hierarchy.main(arbitrary=True, name=name)


lx.bless(CommandClass, 'bd.blend_arbitrary')
