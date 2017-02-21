#!/usr/bin/env python
# encoding: utf-8

"""

A simple example of a blessed MODO command using the commander module.
https://github.com/adamohern/commander for details

"""

import babylondreams
import lx
import modo

from bd_tools import bd_gl_capture

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

        reload(bd_gl_capture)
        bd_gl_capture.main()


lx.bless(CommandClass, 'bd.gl_capture')