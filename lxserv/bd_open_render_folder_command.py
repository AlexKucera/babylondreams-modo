#!/usr/bin/env python
# encoding: utf-8

"""

babylondreams - bd_open_render_folder_command

Release Notes:

V0.1 Initial Release - 2017-04-10

"""
import subprocess

import babylondreams
import lx
import modo

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
        path = modo.Scene().selected[-1:][0].channel(lx.symbol.sICHAN_RENDEROUTPUT_FILENAME).get()

        if path:
            path = os.path.dirname(path)
            subprocess.call(['open', path])
        else:
            modo.dialogs.alert(
                "Warning",
                "This render output has no location set yet.",
                dtype="info"
            )

lx.bless(CommandClass, 'bd.open_render_folder')
