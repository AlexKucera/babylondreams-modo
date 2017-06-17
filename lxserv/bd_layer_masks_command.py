#!/usr/bin/env python
# encoding: utf-8

"""

babylondreams - bd_layer_masks_command

Release Notes:

V0.1 Initial Release - 2017-04-11

"""

import babylondreams
import lx

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


class CommandClass(babylondreams.CommanderClass):
    _commander_last_used = []

    #def commander_arguments(self):
    #    return [
    #         arg_commander 
    #    ]

    def commander_execute(self, msg, flags):

        scene = modo.Scene()

        for item in scene.selected:
            index = 0
            for child in item.children():
                index = max(child.index, index)

            if item.type == 'mask':

                layer = scene.addItem(lx.symbol.sITYPE_RENDEROUTPUT, name="{}_diffColor".format(item.name))
                layer.setParent(item, index)
                layer.channel(lx.symbol.sICHAN_TEXTURELAYER_EFFECT).set(lx.symbol.s_FX_OUTPUT_DIFFUSE_COLOR)

                layer = scene.addItem(lx.symbol.sITYPE_RENDEROUTPUT, name="{}_alpha".format(item.name))
                layer.setParent(item, index - 1)
                layer.channel(lx.symbol.sICHAN_TEXTURELAYER_EFFECT).set(lx.symbol.s_FX_OUTPUT_ALPHA)


lx.bless(CommandClass, 'bd.add_layer_masks')
