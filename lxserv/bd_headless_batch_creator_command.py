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
                babylondreams.NAME: 'proc',
                babylondreams.LABEL: "Render Type",
                babylondreams.DATATYPE: 'string',
                babylondreams.VALUE: 'manual',
                babylondreams.VALUES_LIST_TYPE: 'popup',
                babylondreams.VALUES_LIST: [('manual', 'Manual'), ('background', 'Background Process')]
            },
            {
                babylondreams.NAME: 'scene_range',
                babylondreams.LABEL: "Use Scene Range",
                babylondreams.DATATYPE: 'boolean',
                babylondreams.VALUE: True
            },
            {
                babylondreams.NAME: 'range',
                babylondreams.LABEL: "Frame Range",
                babylondreams.DATATYPE: 'string',
                babylondreams.VALUE: bd_headless_batch_creator.get_scene_range()
            },
            {
                babylondreams.NAME: 'pass',
                babylondreams.LABEL: "Render Pass",
                babylondreams.DATATYPE: 'string',
                babylondreams.VALUES_LIST_TYPE: 'popup',
                babylondreams.VALUES_LIST: bd_headless_batch_creator.get_passes
            },
            {
                babylondreams.NAME: 'batchsize',
                babylondreams.LABEL: "Batch Size",
                babylondreams.DATATYPE: 'integer',
                babylondreams.VALUE: 20
            },
            {
                babylondreams.NAME: 'pattern',
                babylondreams.LABEL: "Output Pattern",
                babylondreams.DATATYPE: 'string',
                babylondreams.VALUE: bd_headless_batch_creator.get_output_pattern()
            },
            {
                babylondreams.NAME: 'preview',
                babylondreams.LABEL: "Use Preview Rendering",
                babylondreams.DATATYPE: 'boolean',
                babylondreams.VALUE: True
            },
            {
                babylondreams.NAME: 'time',
                babylondreams.LABEL: "Max Time (in minutes)",
                babylondreams.DATATYPE: 'float',
                babylondreams.VALUE: 5.0
            },
            {
                babylondreams.NAME: 'perFrame',
                babylondreams.LABEL: "Use Time for",
                babylondreams.DATATYPE: 'string',
                babylondreams.VALUE: 'frame',
                babylondreams.VALUES_LIST_TYPE: 'popup',
                babylondreams.VALUES_LIST: [('frame', 'Frame'), ('sequence', 'Entire Sequence')]
            },
            {
                babylondreams.NAME: 'conv',
                babylondreams.LABEL: "Convergence Target",
                babylondreams.DATATYPE: 'percent',
                babylondreams.VALUE: 0.975
            },
            {
                babylondreams.NAME: 'geoUpdate',
                babylondreams.LABEL: "Force Geometry Update per Frame",
                babylondreams.DATATYPE: 'boolean',
                babylondreams.VALUE: False
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
