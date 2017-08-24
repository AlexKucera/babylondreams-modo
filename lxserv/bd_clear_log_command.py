#!/usr/bin/env python
# encoding: utf-8

"""

babylondreams - bd_clear_log_command

Release Notes:

V0.1 Initial Release - 2017-08-24

"""

import babylondreams
import lx

import imp

try:
    imp.find_module('lx.symbol')
    import lx.symbol
except ImportError:
    pass

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
        lx.eval("!log.masterClear")

lx.bless(CommandClass, 'bd.clear_log')
