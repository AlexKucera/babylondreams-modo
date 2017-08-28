#!/usr/bin/env python
# encoding: utf-8

"""

babylondreams - bd_headless_batch_creator_command

Release Notes:

V0.1 Initial Release - 2017-04-10

"""

import babylondreams
import lx
import modo

from pprint import pprint
from bd_tools import bd_headless_batch_creator
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
                'name': 'proc',
                'label': "Render Type",
                'datatype': 'string',
                'default': 'manual',
                'values_list_type': 'popup',
                'values_list': [('manual', 'Manual'), ('background', 'Background Process')]
            },
            {
                'name': 'scene_range',
                'label': "Use Scene Range",
                'datatype': 'boolean',
                'default': True
            },
            {
                'name': 'range',
                'label': "Frame Range",
                'datatype': 'string',
                'default': bd_headless_batch_creator.get_scene_range()
            },
            {
                'name': 'pass',
                'label': "Render Pass",
                'datatype': 'string',
                'values_list_type': 'popup',
                'values_list': bd_headless_batch_creator.get_passes
            },
            {
                'name': 'batchsize',
                'label': "Batch Size",
                'datatype': 'integer',
                'default': 20
            },
            {
                'name': 'pattern',
                'label': "Output Pattern",
                'datatype': 'string',
                'default': bd_headless_batch_creator.get_output_pattern()
            },
            {
                'name': 'preview',
                'label': "Use Preview Rendering",
                'datatype': 'boolean',
                'default': True
            },
            {
                'name': 'time',
                'label': "Max Time (in minutes)",
                'datatype': 'float',
                'default': 5.0
            },
            {
                'name': 'perFrame',
                'label': "Use Time for",
                'datatype': 'string',
                'default': 'frame',
                'values_list_type': 'popup',
                'values_list': [('frame', 'Frame'), ('sequence', 'Entire Sequence')]
            },
            {
                'name': 'conv',
                'label': "Convergence Target",
                'datatype': 'percent',
                'default': 0.975
            },
            {
                'name': 'geoUpdate',
                'label': "Force Geometry Update per Frame",
                'datatype': 'boolean',
                'default': False
            }
        ]

    def commander_execute(self, msg, flags):
        arguments = self.commander_args()

        reload(bd_headless_batch_creator)
        bd_headless_batch_creator.main(proc=arguments['proc'],
                                       use_scene_range=arguments['scene_range'],
                                       frame_range=arguments['range'],
                                       passname=arguments['pass'],
                                       batchsize=int(arguments['batchsize']),
                                       pattern=arguments['pattern'],
                                       preview=arguments['preview'],
                                       time=arguments['time'],
                                       perFrame=arguments['perFrame'],
                                       conv=arguments['conv'],
                                       geoUpdate=arguments['geoUpdate']
                                       )


lx.bless(CommandClass, 'bd.headless_batch_creator')
