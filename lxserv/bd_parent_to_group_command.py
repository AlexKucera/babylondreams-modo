#!/usr/bin/env python
# encoding: utf-8

"""

babylondreams - bd_parent_to_group_command

Release Notes:

V0.1 Initial Release - 2018-05-29

Copyright 2018 - BabylonDreams - Alexander Kucera & Monika Kucera GbR

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
import modo

import babylondreams

from bd_tools import bd_parent_to_group
from bd_tools.var import *

__author__ = "Alexander Kucera"
__copyright__ = "Copyright 2018, BabylonDreams - Alexander & Monika Kucera GbR"
__credits__ = ["Alexander Kucera"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Alexander Kucera"
__email__ = "a.kucera@babylondreams.de"
__status__ = "Development"


class CommandClass(babylondreams.CommanderClass):
    _commander_last_used = []

    def commander_execute(self, msg, flags):

        reload(bd_parent_to_group)
        bd_parent_to_group.main(ui=False)


lx.bless(CommandClass, 'bd.parent_to_group')
