#!/usr/bin/env python
# encoding: utf-8

"""

batch_event_logger_command

Usage:

batch.event_logger "Starting Render" "/Volumes/projects/logpath.log"

Release Notes:

V0.1 Initial Release - 2017-04-24

Copyright 2017 - BabylonDreams - Alexander Kucera & Monika Kucera GbR

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

"""

import lx
import lxu.command

import imp
import time

try:
    imp.find_module('lx.symbol')
    import lx.symbol
except ImportError:
    pass

import modo

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

        self.dyna_Add("Event String", lx.symbol.sTYPE_STRING)
        self.dyna_Add("Log Path", lx.symbol.sTYPE_STRING)

    def arg_UIHints(self, index, hints):
        if index == 0:
            hints.Label("A string that will be printed to the Event Log.")

        if index == 1:
            hints.Label("The path to an log file on disk.")

    def cmd_Flags(self):
        return lx.symbol.fCMD_UNDO | lx.symbol.fCMD_UI

    def cmd_DialogInit(self):
        cmd_string = self.dyna_String(0, "")
        self.attr_SetString(0, cmd_string)

    def basic_Execute(self, msg, flags):

        cmd_string = self.dyna_String(0, "")
        log_path = self.dyna_String(1, "")

        lx.out(cmd_string)
        with open(log_path, "a+") as log:
            log.write("{} - {}\r\n".format(time.strftime("%Y-%m-%d %H:%M:%S"), cmd_string))
            log.close

lx.bless(MyCommand_Cmd, 'batch.event_logger')
