#!/usr/bin/env python
# encoding: utf-8

"""

babylondreams - bd_fix_orphans

Release Notes:

V0.1 Initial Release - 2017-02-22

"""

import babylondreams
import lx
import modo

from bd_tools import bd_fix_orphans

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

    #def commander_arguments(self):
    #    return [
    #         arg_commander 
    #    ]

    def commander_execute(self, msg, flags):
        # dish1 = self.commander_arg_value(0)
        # dish2 = self.commander_arg_value(1)

        # modo.dialogs.alert("breakfast", ' and '.join([dish1, dish2]))

        reload(bd_fix_orphans)
        bd_fix_orphans.main()


lx.bless(CommandClass, 'bd.fix_orphans')
