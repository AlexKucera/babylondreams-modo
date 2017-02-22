#!/usr/bin/env python
# encoding: utf-8

"""

babylondreams - bd_split_blend_passes_command

Release Notes:

V0.1 Initial Release - 2017-02-22

"""

import babylondreams
import lx
import modo

from bd_tools import bd_split_blend_passes

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
        reload(bd_split_blend_passes)
        bd_split_blend_passes.main()


lx.bless(CommandClass, 'bd.split_blend_passes')
