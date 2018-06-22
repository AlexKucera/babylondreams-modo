#!/usr/bin/env python
# encoding: utf-8

"""

babylondreams - bd_texture_effect_chooser

Release Notes:

V0.1 Initial Release - 2018-06-22

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

import babylondreams

from bd_tools import bd_texture_effect_chooser
from bd_tools.var import *


class CommandClass(babylondreams.CommanderClass):
    def commander_arguments(self):
        return [
            {
                'name': 'texture_id',
                'label': 'Texture Effect Identifier',
                'datatype': 'string',
                'default': 'base_all',
                'values_list_type': 'sPresetText',
                'values_list': bd_texture_effect_chooser.generate_id_list
            },
            {
                'name': 'channel_fx',
                'label': 'Channel Effect',
                'datatype': 'string',
                'default': 'base_modo',
                'values_list_type': 'sPresetText',
                'values_list': bd_texture_effect_chooser.generate_effects_list
            }
        ]

    def commander_execute(self, msg, flags):
        reload(bd_texture_effect_chooser)
        args = self.commander_args()
        bd_texture_effect_chooser.main(args['texture_id'], args['channel_fx'])


lx.bless(CommandClass, 'bd_texture_effect_chooser')
