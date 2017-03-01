#!/usr/bin/env python
# encoding: utf-8

"""

babylondreams - bd_instance_source_center_adjust_command

Release Notes:

V0.1 Initial Release - 2017-02-27

"""

import babylondreams
import lx
import modo
from bd_tools.var import *

from bd_tools import bd_instance_source_center_adjust

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
               'name': 'center_action',
               'datatype': 'string',
               'default': 'Center to BBox',
               'values_list_type': 'popup',
               'values_list': [CENTER_BBOX, CENTER_WPLANE, CENTER_TOP, CENTER_BOTTOM, CENTER_LEFT,
                               CENTER_RIGHT, CENTER_FRONT, CENTER_BACK]
           },
       ]

    def commander_execute(self, msg, flags):
        center_action = self.commander_arg_value(0)

        if center_action == CENTER_BBOX:
            center_action = "center.bbox center"
        elif center_action == CENTER_TOP:
            center_action = "center.bbox top"
        elif center_action == CENTER_BOTTOM:
            center_action = "center.bbox bottom"
        elif center_action == CENTER_LEFT:
            center_action = "center.bbox left"
        elif center_action == CENTER_RIGHT:
            center_action = "center.bbox right"
        elif center_action == CENTER_FRONT:
            center_action = "center.bbox front"
        elif center_action == CENTER_BACK:
            center_action = "center.bbox back"
        elif center_action == CENTER_WPLANE:
            center_action = 'center.matchWorkplane pos'

        reload(bd_instance_source_center_adjust)
        bd_instance_source_center_adjust.main(center_action)


lx.bless(CommandClass, 'bd.instance_source_center_adjust')
