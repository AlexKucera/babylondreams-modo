#!/usr/bin/env python
# encoding: utf-8

"""

babylondreams - bd_reroute_instances_command

Release Notes:

V0.1 Initial Release - 2017-02-23

"""

import babylondreams
import lx
import modo

from bd_tools import bd_reroute_instances

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
                'name': 'new_instance_source',
                'datatype': 'string',
                'default': 'newMesh',
                'values_list_type': 'sPresetText',
                'values_list': self.list_meshes
            },
        ]

    def list_meshes(self):
        scene = modo.Scene()
        meshes = []
        for item in scene.items(itype='mesh', superType=True):
            meshes.append((item.id, item.name))
        return meshes

    def commander_execute(self, msg, flags):
        scene = modo.Scene()
        source = []
        instances = scene.selected
        for instance in instances:
            if not instance.isAnInstance:
                print "not an instance"
                source.append(instance.name)
        if len(source) > 0:
            modo.dialogs.alert('Warning', 'Please select only instances.\nThe following items are no instances:\n{0}'.format(source), dtype='warning')
        else:
            new_source = self.commander_arg_value(0)

            reload(bd_reroute_instances)
            bd_reroute_instances.main(new_source, instances)


lx.bless(CommandClass, 'bd.reroute_instances')
