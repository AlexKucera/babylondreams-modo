#!/usr/bin/env python
# encoding: utf-8

"""

babylondreams - bd_format_filename_command

Release Notes:

V0.1 Initial Release - 2017-04-12

"""

import babylondreams
import lx
import lxu.command

import imp

try:
    imp.find_module('lx.symbol')
    import lx.symbol
except ImportError:
    pass

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

class MyCommand_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

        self.dyna_Add("platform", lx.symbol.sTYPE_STRING)

    def arg_UIHints(self, index, hints):
        if index == 0:
            hints.Label("A provide the platform paths should be formatted for.")

    def cmd_Flags(self):
        return lx.symbol.fCMD_UNDO | lx.symbol.fCMD_MODEL

    def basic_Execute(self, msg, flags):

        if not self.dyna_IsSet(0):
            format = "win32"

        format = self.dyna_String(0, "")
        unix_path = "/Volumes/ProjectsRaid/WorkingProjects"
        win_path = "Z:\AzureSync\CloudComputing\WorkingProjects"

        scene = modo.Scene()

        for i in scene.iterItemsFast('renderOutput'):
            filename = i.channel('filename').get()

            if format == "win32":
                filename = filename.replace(unix_path, win_path)
                filename = filename.replace('/', '\\')
                return filename
            elif format == "darwin":
                filename = filename.replace(win_path, unix_path)
                filename = filename.replace('\\', '/')

            i.channel('filename').set(filename)

        else:
            print("ERROR no valid OS given for path transform")

lx.bless(MyCommand_Cmd, 'bd.format_filename')
