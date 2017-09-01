#!/usr/bin/env python
# encoding: utf-8

"""

babylondreams - bd_collect_texturelocators_command

Release Notes:

V0.1 Initial Release - 2017-09-01

"""

import lx

import babylondreams
from bd_tools import bd_collect_texturelocators

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
        arguments = self.commander_args()

        reload(bd_collect_texturelocators)
        bd_collect_texturelocators.main()


lx.bless(CommandClass, 'bd.collect_texturelocators')
