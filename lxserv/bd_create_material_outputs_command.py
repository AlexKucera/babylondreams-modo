#!/usr/bin/env python
# encoding: utf-8

"""

babylondreams - bd_create_material_outputs_command

Release Notes:

V0.1 Initial Release - 2017-08-28

"""

import babylondreams
import lx

import imp

import modo

from bd_tools import bd_create_material_outputs
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

    def commander_arguments(self):
        return [
            {
                'name': 'outtype',
                'label': "Create Final Color, Alpha or Both:",
                'datatype': 'string',
                'default': "alpha",
                'values_list_type': 'popup',
                'values_list': [("alpha", "Alpha Only"), ("color", "Final Color Only"), ("both", "both")]
            }
        ]

    def commander_execute(self, msg, flags):
        arguments = self.commander_args()
        reload(bd_create_material_outputs)
        bd_create_material_outputs.main(arguments["outtype"])


lx.bless(CommandClass, 'bd.create_material_outputs')
