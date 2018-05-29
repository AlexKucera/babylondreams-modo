#!/usr/bin/env python
# encoding: utf-8

"""

babylondreams - bd_select_by_size_command

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
import lxu.command
import modo

import babylondreams

from bd_tools import bd_select_by_size
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

    def commander_arguments(self):
        return [
            {
                'name': 'mode',
                'label': 'Size Mode',
                'datatype': 'string',
                'default': 'shortest',
                'values_list_type': 'popup',
                'values_list': [
                    ('volume', 'Volume'),
                    ('area', 'Area (X/Z)'),
                    ('shortest', 'Shortest Side'),
                    ('longest', 'Longest Side')
                ]
            },
            {
                'name': 'size',
                'label': 'Size',
                'datatype': 'distance',
                'default': 0.02
            },
            {
                'name': 'invert',
                'label': 'Invert Selection',
                'datatype': 'boolean',
            },
            {
                'name': 'instances',
                'label': 'Include Instances',
                'datatype': 'boolean',
                'default': True
            }
        ]

    def commander_execute(self, msg, flags):
        arguments = self.commander_args()

        reload(bd_select_by_size)
        bd_select_by_size.main(
            mode=arguments['mode'],
            size=arguments['size'],
            invert=arguments['invert'],
            instances=arguments['instances'])


lx.bless(CommandClass, 'bd.select_by_size')
