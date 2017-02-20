#!/usr/bin/env python
# encoding: utf-8

"""

babylondreams - bd_command_dissolve_hierarchy

Release Notes:

V0.1 Initial Release - 2017-02-20

"""

import babylondreams
import lx

from bd_tools import bd_dissolve_hierarchy


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

        reload(bd_dissolve_hierarchy)

        bd_dissolve_hierarchy.main()


lx.bless(CommandClass, 'bd.dissolve_hierarchy')
