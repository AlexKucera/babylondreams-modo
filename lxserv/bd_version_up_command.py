#!/usr/bin/env python
# encoding: utf-8

"""

babylondreams - bd_version_up_command

Release Notes:

V0.1 Initial Release - 2017-08-15

"""

import babylondreams
import lx

import imp

try:
    imp.find_module('lx.symbol')
    import lx.symbol
except ImportError:
    pass

import modo

from bd_tools import bd_version_up
from bd_tools.var import *

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
        reload(bd_version_up)
        bd_version_up.main()


lx.bless(CommandClass, 'bd.version_up')
