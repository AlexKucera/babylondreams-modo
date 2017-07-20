#!/usr/bin/env python
# encoding: utf-8

"""

babylondreams - bd_transfer_anim_tagger_command

Release Notes:

V0.1 Initial Release - 2017-02-21

"""

import babylondreams
import lx
import modo

from bd_tools import bd_transfer_anim_tagger

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
                'name': 'mode',
                'label': "Tagging Mode",
                'datatype': 'string',
                'default': "update",
                'values_list_type': 'popup',
                'values_list': [('update', 'Update Missing Tags'),
                                ('list', 'List Untagged Animated Items'),
                                ('overwrite', 'Overwrite/Re-create Tags (CAREFUL!)'),
                                ('assign', 'Assign Tags to Hierarchy')]
            }
        ]

    def commander_execute(self, msg, flags):
        arguments = self.commander_args()

        reload(bd_transfer_anim_tagger)
        bd_transfer_anim_tagger.main(mode=arguments['mode'])


lx.bless(CommandClass, 'bd.transfer_anim_tagger')
