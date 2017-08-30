#!/usr/bin/env python
# encoding: utf-8

"""

babylondreams - bd_bake_camera_command

Release Notes:

V0.1 Initial Release - 2017-08-28

"""

import babylondreams
import lx

import modo

from bd_tools import bd_bake_camera
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

    def commander_execute(self, msg, flags):
        arguments = self.commander_args()

        reload(bd_bake_camera)
        bd_bake_camera.main()


lx.bless(CommandClass, 'bd.bake_camera')
