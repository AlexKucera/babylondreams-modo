#!/usr/bin/env python
# encoding: utf-8

"""

babylondreams - bd_transfer_anim_command

Release Notes:

V0.1 Initial Release - 2017-02-21

"""

import babylondreams
import lx
import modo

from bd_tools import bd_transfer_anim

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

    def commander_execute(self, msg, flags):
        reload(bd_transfer_anim)
        bd_transfer_anim.main()


lx.bless(CommandClass, 'bd.transfer_anim_load')
