#!/usr/bin/env python
# encoding: utf-8
# Alexander Kucera
# babylondreams.de

import lx
import babylondreams


class CommandClass(babylondreams.CommanderClass):
    _commander_default_values = []

    def commander_arguments(self):
        return [
                {
                    'name': 'blend_type',
                    'label': 'Blend Type',
                    'datatype': 'string',
                    'default': lx.eval("user.value bd.blend_type_pref ?"),
                    'values_list_type': 'popup',
                    'values_list': [('tranAmount', 'Transparency'), ('dissolve', 'Dissolve')],
                    'flags': ['query']
                }
            ]

    def commander_execute(self, msg, flags):
        lx.eval("user.value bd.blend_type_pref %s" % self.commander_arg_value(0))
        lx.out("Set Blend Type to ", self.commander_arg_value(1))


lx.bless(CommandClass, 'bd.prefs_blend_type')
