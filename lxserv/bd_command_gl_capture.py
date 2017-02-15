#!/usr/bin/env python
# encoding: utf-8

"""

A simple example of a blessed MODO command using the commander module.
https://github.com/adamohern/commander for details

"""

import babylondreams
import lx
import modo

from bd_tools import bd_gl_capture

__author__ = "Alexander Kucera"
__copyright__ = "Copyright ${YEAR}, BabylonDreams - Alexander & Monika Kucera GbR"
__credits__ = ["Alexander Kucera"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Alexander Kucera"
__email__ = "a.kucera@babylondreams.de"
__status__ = "Development"

scene = modo.Scene()


class CommandClass(babylondreams.CommanderClass):
    _commander_last_used = []

    def commander_arguments(self):
        """

        :return:
        """
        return [
            {
                babylondreams.NAME: 'gl_recording_size',
                'datatype': 'percent',
                'default': 1.0,
                'values_list_type': 'popup',
                'values_list': [1.0, .5, .25, .1]
            }, {
                'name': 'gl_recording_type',
                'datatype': 'string',
                'label': 'GL Recording Type',
                'default': 'image',
                'values_list_type': 'popup',
                'values_list': [('movie', 'Movie'), ('image', 'Image Sequence')]
            }
            , {
                'name': 'viewport_camera',
                'datatype': 'string',
                'label': 'Viewport Camera',
                'default': 'Render Camera',
                'values_list_type': 'popup',
                'values_list': [('movie', 'Movie'), ('image', 'Image Sequence')]
            }
        ]
    def get_cameras(self):

        cameras = scene.items(itype='camera', superType=True)

        all_cameras = [(scene.renderCamera, "Render Camera")]

        for camera in cameras:
            all_cameras.append((camera, camera.name))

        return all_cameras


    def commander_execute(self, msg, flags):
        """

        :param msg:
        :param flags:
        """
        gl_recording_size = self.commander_arg_value(0)
        gl_recording_type = self.commander_arg_value(1)

        modo.dialogs.alert("breakfast", ' and '.join([gl_recording_size, gl_recording_type]))
        reload(bd_gl_capture)
        bd_gl_capture.main()


lx.bless(CommandClass, 'bd.gl_capture')
