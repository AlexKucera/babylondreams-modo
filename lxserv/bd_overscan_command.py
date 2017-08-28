#!/usr/bin/env python
# encoding: utf-8

"""

babylondreams - bd_overscan_command

Release Notes:

V0.1 Initial Release - 2017-08-28

"""

import babylondreams
import lx

import modo

from bd_tools import bd_overscan
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

    _state = False

    def commander_arguments(self):
       return [
           {
               'name': 'mode',
               'label': "Overscan Mode",
               'datatype': 'string',
               'default': "resolution",
               'values_list_type': 'popup',
               'values_list': [('resolution', 'Resolution'), ('scale', 'Scale')]
           },
           {
               'name': 'newsize',
               'label': "Overscan Size",
               'datatype': 'string',
               'default': '2016x1134',
               'values_list_type': 'sPresetText',
               'values_list': ['1920x1080', '1.05']
           }
       ]

    def commander_execute(self, msg, flags):
        arguments = self.commander_args()

        reload(bd_overscan)
        bd_overscan.main(
            mode=arguments['mode'],
            newsize=arguments['newsize']
                         )


lx.bless(CommandClass, 'bd.overscan')
